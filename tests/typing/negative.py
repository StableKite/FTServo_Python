"""Every marked line is a genuine invalid argument, result or replacement."""
from collections.abc import Sequence
from scservo_sdk import GroupSyncRead, GroupSyncWrite, PortHandler, protocol_packet_handler, scscl, sms_sts

port = PortHandler(None)
PortHandler(123)  # EXPECT_ERROR
port.readPort(1.5)  # EXPECT_ERROR
port.writePort("wrong")  # EXPECT_ERROR
port.setPortName(1)  # EXPECT_ERROR
port.setBaudRate("fast")  # EXPECT_ERROR
port.baudrate = "fast"  # EXPECT_ERROR
port.is_open = "yes"  # EXPECT_ERROR
port.ser = object()  # EXPECT_ERROR
protocol_packet_handler(object(), 0)  # EXPECT_ERROR
protocol_packet_handler(port, "little")  # EXPECT_ERROR
handler = protocol_packet_handler(port, 0)
bad_end: str = handler.scs_getend()  # EXPECT_ERROR
handler.txPacket(b"\xff\xff\x01\x02\x01\xfb")  # EXPECT_ERROR
handler.write1ByteTxRx(1, 17, "bad")  # EXPECT_ERROR
handler.writeTxRx(1, 17, 2, "bad")  # EXPECT_ERROR
handler.readRx(1, "two")  # EXPECT_ERROR
bad_scalar: str = handler.read2ByteTxRx(1, 17)[0]  # EXPECT_ERROR
bad_read: list[str] = handler.readTxRx(1, 17, 2)[0]  # EXPECT_ERROR
sms = sms_sts(port)
scs = scscl(port)
sms_sts("port")  # EXPECT_ERROR
scscl(object())  # EXPECT_ERROR
sms.WritePosEx(1, 100, "speed", 3)  # EXPECT_ERROR
sms.SyncWritePosEx(1, 100, 20, "acc")  # EXPECT_ERROR
scs.WritePos(1, 100, "time", 20)  # EXPECT_ERROR
sms.groupSyncWrite = object()  # EXPECT_ERROR
writer = GroupSyncWrite(sms, 17, 2)
GroupSyncWrite(object(), 17, 2)  # EXPECT_ERROR
GroupSyncWrite(sms, "address", 2)  # EXPECT_ERROR
GroupSyncWrite(sms, 17, "length")  # EXPECT_ERROR
writer.addParam("one", [1, 2])  # EXPECT_ERROR
writer.addParam(1, ["bad"])  # EXPECT_ERROR
writer.changeParam(1, object())  # EXPECT_ERROR
writer.data_dict[1] = ["bad"]  # EXPECT_ERROR
writer.start_address = 1.5  # EXPECT_ERROR
bad_tx: str = writer.txPacket()  # EXPECT_ERROR
reader = GroupSyncRead(sms, 17, 2)
reader.addParam("one")  # EXPECT_ERROR
bad_available: bool = reader.isAvailable(1, 17, 2)  # EXPECT_ERROR
bad_data: str = reader.getData(1, 17, 2)  # EXPECT_ERROR
parsed, result = reader.readRx(b"", 1, 2)
bad_parser: list[int] = parsed  # EXPECT_ERROR
reader.data_dict[1] = ["bad"]  # EXPECT_ERROR


class InvalidWriter:
    def clearParam(self) -> None:
        pass

    def addParam(self, scs_id: int, data: Sequence[int]) -> str:
        return str((scs_id, data))

    def txPacket(self) -> None:
        pass


sms.groupSyncWrite = InvalidWriter()  # EXPECT_ERROR



class MissingBusyFlag:
    def clearPort(self) -> None:
        pass
    def readPort(self, length: int) -> bytes:
        return b""[:length]
    def writePort(self, packet: list[int] | bytearray) -> int:
        return len(packet)
    def setPacketTimeout(self, packet_length: int) -> None:
        pass
    def isPacketTimeout(self) -> bool:
        return True


class ReadOnlyBusyFlag(MissingBusyFlag):
    @property
    def is_using(self) -> bool:
        return False


class BadReadPort:
    is_using: bool = False
    def clearPort(self) -> None:
        pass
    def readPort(self, length: int) -> str:
        return str(length)
    def writePort(self, packet: list[int] | bytearray) -> int:
        return len(packet)
    def setPacketTimeout(self, packet_length: int) -> None:
        pass
    def isPacketTimeout(self) -> bool:
        return True


class BadWritePort:
    is_using: bool = False
    def clearPort(self) -> None:
        pass
    def readPort(self, length: int) -> bytes:
        return b""[:length]
    def writePort(self, packet: bytes) -> int:
        return len(packet)
    def setPacketTimeout(self, packet_length: int) -> None:
        pass
    def isPacketTimeout(self) -> bool:
        return True


class BadTimeoutPort:
    is_using: bool = False
    def clearPort(self) -> None:
        pass
    def readPort(self, length: int) -> bytes:
        return b""[:length]
    def writePort(self, packet: list[int] | bytearray) -> int:
        return len(packet)
    def setPacketTimeout(self, packet_length: str) -> None:
        pass
    def isPacketTimeout(self) -> bool:
        return True


sms_sts(MissingBusyFlag())  # EXPECT_ERROR
scscl(ReadOnlyBusyFlag())  # EXPECT_ERROR
sms_sts(BadReadPort())  # EXPECT_ERROR
scscl(BadWritePort())  # EXPECT_ERROR
protocol_packet_handler(BadTimeoutPort(), 0)  # EXPECT_ERROR
structural_handler = sms_sts(port)
structural_handler.portHandler = BadReadPort()  # EXPECT_ERROR
