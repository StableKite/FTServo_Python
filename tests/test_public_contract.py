"""Genuine unopened SDK objects, public storage, and independent wire vectors."""
import unittest
import sys
import sysconfig
import threading
from concurrent.futures import ThreadPoolExecutor

from scservo_sdk import COMM_NOT_AVAILABLE, COMM_RX_CORRUPT, COMM_SUCCESS, GroupSyncRead, GroupSyncWrite, PortHandler, scscl, sms_sts
from test_wire_contract import handler


class PublicContract(unittest.TestCase):
    def test_low_level_mutable_packet_and_busy_state(self):
        sdk, uart = handler()
        packet = bytearray((0, 0, 1, 2, 1, 0))
        uart.expect(1, b"")
        self.assertEqual(sdk.txPacket(packet), COMM_SUCCESS)
        self.assertEqual(packet, bytes.fromhex("ffff010201fb"))
        self.assertEqual(uart.writes, [bytes.fromhex("ffff010201fb")])
        self.assertTrue(sdk.portHandler.is_using)

    def test_independent_ports_with_the_actual_runtime_gil_mode(self):
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
        if hasattr(sys, "_is_gil_enabled"):
            expected = sys._xoptions.get("gil") == "1" or not bool(sysconfig.get_config_var("Py_GIL_DISABLED"))
            self.assertIs(sys._is_gil_enabled(), expected)

    def test_real_port_stays_closed(self):
        port = PortHandler(None)
        self.assertFalse(port.is_open)
        self.assertIsNone(port.ser)
        self.assertIsNone(port.getPortName())
        self.assertEqual(port.getCFlagBaud(115200), 115200)
        self.assertEqual(port.getCFlagBaud(123), -1)
        with self.assertRaises(AttributeError):
            port.closePort()
        self.assertFalse(port.is_open)

    def test_public_writer_replacement_and_deletion(self):
        port = PortHandler("owned-never-opened")
        for series in (sms_sts, scscl):
            sdk = series(port)
            first = sdk.groupSyncWrite
            replacement = GroupSyncWrite(sdk, 17, 2)
            sdk.groupSyncWrite = replacement
            self.assertIs(sdk.groupSyncWrite, replacement)
            self.assertIsNot(first, replacement)
            del sdk.groupSyncWrite
            with self.assertRaises(AttributeError) as caught:
                sdk.groupSyncWrite
            self.assertEqual(caught.exception.args, (f"'{series.__name__}' object has no attribute 'groupSyncWrite'",))
        self.assertFalse(port.is_open)
        self.assertIsNone(port.ser)

    def test_writer_payload_alias_and_mutable_container(self):
        sdk = sms_sts(PortHandler(None))
        writer = GroupSyncWrite(sdk, 17, 2)
        payload = [1, 2]
        self.assertTrue(writer.addParam(1, payload))
        self.assertIs(writer.data_dict[1], payload)
        payload[0] = 7
        writer.makeParam()
        self.assertEqual(writer.param, [1, 7, 2])
        self.assertFalse(writer.addParam(1, b"12"))
        self.assertTrue(writer.changeParam(1, b"12"))
        self.assertEqual(writer.data_dict[1], b"12")
        writer.removeParam(1)
        self.assertEqual(writer.txPacket(), COMM_NOT_AVAILABLE)

    def test_sync_read_literal_valid_and_corrupt_frames(self):
        for series, value in ((sms_sts, 0x1234), (scscl, 0x3412)):
            sdk = series(PortHandler(None))
            reader = GroupSyncRead(sdk, 17, 2)
            self.assertTrue(reader.addParam(1))
            self.assertEqual(reader.isAvailable(1, 17, 2), (False, 0))
            data, result = reader.readRx(bytes.fromhex("ffff0104003412b4"), 1, 2)
            self.assertEqual((data, result), ([0, 0x34, 0x12], COMM_SUCCESS))
            reader.data_dict[1] = data
            self.assertEqual(reader.isAvailable(1, 17, 2), (True, 0))
            self.assertEqual(reader.getData(1, 17, 2), value)
            for wire in ("ffff0104003412b5", "ffff0104003412", ""):
                self.assertEqual(reader.readRx(bytes.fromhex(wire), 1, 2), (None, COMM_RX_CORRUPT))
            reader.data_dict[1] = None
            self.assertEqual(reader.isAvailable(1, 17, 2), (False, 0))

    def test_real_wire_literal_endianness_and_checksum(self):
        for series, expected in ((sms_sts, "ffff0105031434129c"), (scscl, "ffff0105031412349c")):
            sdk, uart = handler(series)
            payload = b"\x14\x34\x12" if series is sms_sts else b"\x14\x12\x34"
            uart.expect(3, payload)
            self.assertEqual(sdk.write2ByteTxRx(1, 20, 0x1234), (COMM_SUCCESS, 0))
            self.assertEqual(uart.writes, [bytes.fromhex(expected)])
            self.assertFalse(uart.expected)


if __name__ == "__main__":
    unittest.main()
