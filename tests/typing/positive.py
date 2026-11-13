"""Genuine unopened SDK objects and public replacement contracts."""
from collections.abc import Sequence
from typing import assert_type

import serial
from scservo_sdk import COMM_NOT_AVAILABLE, GroupSyncRead, GroupSyncWrite, PortHandler, protocol_packet_handler, scscl, sms_sts


class WriterView:
    """Delegate all three shared operations to the genuine SDK writer."""
    def __init__(self, writer: GroupSyncWrite) -> None:
        self.writer = writer

    def clearParam(self) -> None:
        self.writer.clearParam()

    def addParam(self, scs_id: int, data: Sequence[int]) -> bool:
        return self.writer.addParam(scs_id, data)

    def txPacket(self) -> int:
        return self.writer.txPacket()


class MemoryStream:
    """Replace only the byte transport; never open an operating system port."""
    def __init__(self) -> None:
        self.buffer = bytearray()

    def reset_input_buffer(self) -> None:
        self.buffer.clear()

    def read(self, length: int, /) -> bytes:
        result = bytes(self.buffer[:length])
        del self.buffer[:length]
        return result

    def write(self, value: Sequence[int], /) -> int:
        self.buffer.extend(value)
        return len(value)


def actual_wire_result_types(handler: protocol_packet_handler) -> None:
    """Static public return contracts also exercised by the real wire suite."""
    assert_type(handler.read1ByteTxRx(1, 17), tuple[int, int, int])
    assert_type(handler.read2ByteTxRx(1, 17), tuple[int, int, int])
    assert_type(handler.read4ByteTxRx(1, 17), tuple[int, int, int])
    assert_type(handler.readTxRx(1, 17, 2), tuple[list[int], int, int])
    assert_type(handler.rxPacket(), tuple[list[int], int])
    assert_type(handler.txRxPacket([0, 0, 1, 2, 1, 0]), tuple[list[int] | None, int, int])
    assert_type(handler.syncReadRx(2, 1), tuple[int, list[int]])
    assert_type(handler.action(254), int)


port = PortHandler("owned-typed-port-never-opened")
assert not port.is_open and port.ser is None
assert_type(port.getPortName(), str | None)
assert_type(port.getBaudRate(), int)
assert_type(port.getCurrentTime(), float)
assert port.getCFlagBaud(115200) == 115200
closed_serial = serial.Serial(port=None)
assert not closed_serial.is_open
port.ser = closed_serial
assert port.ser is closed_serial
stream = MemoryStream()
port.ser = stream
assert port.writePort([1, 2]) == 2
assert assert_type(port.readPort(2), bytes) == b"\x01\x02"
assert not port.is_open

low_level = protocol_packet_handler(port, 0)
mutable_packet = bytearray((0, 0, 1, 2, 1, 0))
assert assert_type(low_level.txPacket(mutable_packet), int) == 0
assert mutable_packet == bytes.fromhex("ffff010201fb")
assert port.is_using  # The low-level tx-only primitive retains its real busy state.

sms = sms_sts(port)
scs = scscl(port)
assert sms.portHandler is port and scs.portHandler is port
writer = GroupSyncWrite(sms, 17, 2)
payload = [1, 2]
assert assert_type(writer.addParam(1, payload), bool)
assert writer.data_dict[1] is payload
sms.groupSyncWrite = writer
assert sms.groupSyncWrite is writer
view = WriterView(writer)
sms.groupSyncWrite = view
assert sms.groupSyncWrite is view
sms.groupSyncWrite.clearParam()
assert assert_type(sms.groupSyncWrite.txPacket(), int) == COMM_NOT_AVAILABLE
assert sms.SyncWritePosEx(1, 100, 20, 3) is False  # The replacement really has length two.
scs.groupSyncWrite = GroupSyncWrite(scs, 17, 2)
assert scs.groupSyncWrite.changeParam(1, b"12") is False

reader = GroupSyncRead(sms, 17, 2)
assert reader.addParam(1)
assert assert_type(reader.isAvailable(1, 17, 2), tuple[bool, int]) == (False, 0)
parsed, result = reader.readRx(bytes.fromhex("ffff0104003412b4"), 1, 2)
assert_type(parsed, list[int] | None)
assert parsed is not None
assert_type(parsed, list[int])
reader.data_dict[1] = parsed
assert reader.isAvailable(1, 17, 2) == (True, 0)
assert assert_type(reader.getData(1, 17, 2), int) == 0x1234
reader.data_dict[1] = None
assert reader.isAvailable(1, 17, 2) == (False, 0)
assert not port.is_open



class StructuralPort:
    """Closed, non-inheriting transport with the Root adapter's port signatures."""

    def __init__(self) -> None:
        self.is_using = False
        self.writes: list[bytes] = []
        self.timeouts: list[int] = []

    def clearPort(self) -> None:
        pass

    def readPort(self, length: int) -> bytes:
        return b""[:length]

    def writePort(self, packet: bytes | bytearray | list[int]) -> int:
        self.writes.append(bytes(packet))
        return len(packet)

    def setPacketTimeout(self, packet_length: int) -> None:
        self.timeouts.append(packet_length)

    def isPacketTimeout(self) -> bool:
        return True


structural_port = StructuralPort()
structural_sms = sms_sts(structural_port)
structural_scs = scscl(structural_port)
assert structural_sms.portHandler is structural_port
assert structural_scs.portHandler is structural_port
assert not isinstance(structural_port, PortHandler)
# Run the genuine packet builder and timeout path over the in-memory boundary.
assert structural_sms.ping(1) == (0, -6, 0)
assert structural_port.writes == [bytes.fromhex("ffff010201fb")]
assert structural_port.timeouts == [6]
assert not structural_port.is_using
