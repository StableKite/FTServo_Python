"""Exercise genuine SDK handlers with only the physical UART replaced."""
import sys
import threading
import unittest
from collections import deque
from concurrent.futures import ThreadPoolExecutor

from scservo_sdk import COMM_RX_CORRUPT, COMM_SUCCESS, PortHandler, scscl, sms_sts


def packet(device, instruction, payload=b""):
    body = bytes((device, len(payload) + 2, instruction)) + payload
    return b"\xff\xff" + body + bytes((~sum(body) & 255,))


class UART:
    """Byte boundary only: SDK packet parsing and timing remain real."""
    def __init__(self):
        self.expected = deque()
        self.incoming = bytearray()
        self.writes = []

    def expect(self, instruction, payload, reply=b"", error=0, broadcast=False):
        device = 254 if broadcast else 1
        self.expected.append((packet(device, instruction, payload),
                              b"" if broadcast else packet(device, error, reply)))

    def reset_input_buffer(self):
        self.incoming.clear()

    def write(self, value):
        expected, response = self.expected.popleft()
        assert bytes(value) == expected, (bytes(value).hex(), expected.hex())
        self.writes.append(bytes(value))
        self.incoming.extend(response)
        return len(value)

    def read(self, length):
        value = bytes(self.incoming[:length])
        del self.incoming[:length]
        return value


def handler(series=sms_sts):
    uart = UART()
    port = PortHandler("owned-software-UART-never-opened")
    port.ser = uart
    port.tx_time_per_byte = 1000.0 / port.baudrate * 10.0
    return series(port), uart


class WireContract(unittest.TestCase):
    def test_register_read_lengths(self):
        for series in (sms_sts, scscl):
            for length in (1, 2, 4):
                for actual in (0, length - 1, length, length + 1):
                    for split in (False, True):
                        with self.subTest(series=series.__name__, length=length, actual=actual, split=split):
                            sdk, uart = handler(series)
                            payload = bytes(range(1, actual + 1))
                            uart.expect(2, bytes((20, length)), reply=payload)
                            if split:
                                self.assertEqual(sdk.readTx(1, 20, length), COMM_SUCCESS)
                                data, result, error = sdk.readRx(1, length)
                            else:
                                data, result, error = sdk.readTxRx(1, 20, length)
                            self.assertEqual(error, 0)
                            self.assertEqual(result, COMM_SUCCESS if actual == length else COMM_RX_CORRUPT)
                            self.assertEqual(bytes(data), payload if actual == length else b"")
                            self.assertFalse(uart.expected)

    def test_scalar_read_rejects_short_reply(self):
        for series in (sms_sts, scscl):
            for length in (1, 2, 4):
                sdk, uart = handler(series)
                uart.expect(2, bytes((20, length)), reply=bytes(range(length - 1)))
                value, result, error = getattr(sdk, f"read{length}ByteTxRx")(1, 20)
                self.assertEqual((value, result, error), (0, COMM_RX_CORRUPT, 0))

    def test_position_sign_magnitude_for_all_write_apis(self):
        for position, encoded in ((-100, b"\x64\x80"), (100, b"\x64\x00"),
                                  (0, b"\x00\x00"), (-32767, b"\xff\xff")):
            payload = b"\x29\x03" + encoded + b"\x00\x00\x14\x00"
            for method, instruction in (("WritePosEx", 3), ("RegWritePosEx", 4)):
                with self.subTest(position=position, method=method):
                    sdk, uart = handler()
                    uart.expect(instruction, payload)
                    self.assertEqual(getattr(sdk, method)(1, position, 20, 3), (COMM_SUCCESS, 0))
                    self.assertFalse(uart.expected)
            sdk, uart = handler()
            self.assertTrue(sdk.SyncWritePosEx(1, position, 20, 3))
            uart.expect(131, b"\x29\x07\x01" + payload[1:], broadcast=True)
            self.assertEqual(sdk.groupSyncWrite.txPacket(), COMM_SUCCESS)

    def test_vendor_reset_and_offset_are_real_wire_operations(self):
        # Neither handler opens a physical port.  Check existing upstream API.
        for series in (sms_sts, scscl):
            sdk, uart = handler(series)
            uart.expect(10, b"")
            self.assertEqual(sdk.reSet(1), (COMM_SUCCESS, 0))
            order = "little" if series is sms_sts else "big"
            uart.expect(11, (100).to_bytes(2, order))
            self.assertEqual(sdk.reOfsCal(1, 100), (COMM_SUCCESS, 0))
            self.assertFalse(uart.expected)

    def test_independent_ports_on_native_threads(self):
        barrier = threading.Barrier(8)
        def worker(index):
            sdk, uart = handler()
            barrier.wait(timeout=10)
            for value in range(50):
                expected = bytes((index, value))
                uart.expect(2, b"\x14\x02", reply=expected)
                data, result, error = sdk.readTxRx(1, 20, 2)
                self.assertEqual((bytes(data), result, error), (expected, COMM_SUCCESS, 0))
            return threading.get_native_id()
        with ThreadPoolExecutor(max_workers=8) as pool:
            identities = list(pool.map(worker, range(8)))
        self.assertEqual(len(set(identities)), 8)
        expected = sys._xoptions.get("gil") == "1"
        if hasattr(sys, "_is_gil_enabled"):
            self.assertIs(sys._is_gil_enabled(), expected)


if __name__ == "__main__":
    unittest.main()
