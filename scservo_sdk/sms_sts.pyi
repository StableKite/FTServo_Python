"""Native public interface; implementation and wire behavior are unchanged."""
from typing import Union as _Union
from ._interfaces import SyncWriter as _SyncWriter
from ._interfaces import PacketPort as _PacketPort
from .scservo_def import *
from .protocol_packet_handler import *
from .group_sync_read import *
from .group_sync_write import *
SMS_STS_1M: int
SMS_STS_0_5M: int
SMS_STS_250K: int
SMS_STS_128K: int
SMS_STS_115200: int
SMS_STS_76800: int
SMS_STS_57600: int
SMS_STS_38400: int
SMS_STS_MODEL_L: int
SMS_STS_MODEL_H: int
SMS_STS_ID: int
SMS_STS_BAUD_RATE: int
SMS_STS_MIN_ANGLE_LIMIT_L: int
SMS_STS_MIN_ANGLE_LIMIT_H: int
SMS_STS_MAX_ANGLE_LIMIT_L: int
SMS_STS_MAX_ANGLE_LIMIT_H: int
SMS_STS_CW_DEAD: int
SMS_STS_CCW_DEAD: int
SMS_STS_OFS_L: int
SMS_STS_OFS_H: int
SMS_STS_MODE: int
SMS_STS_TORQUE_ENABLE: int
SMS_STS_ACC: int
SMS_STS_GOAL_POSITION_L: int
SMS_STS_GOAL_POSITION_H: int
SMS_STS_GOAL_TIME_L: int
SMS_STS_GOAL_TIME_H: int
SMS_STS_GOAL_SPEED_L: int
SMS_STS_GOAL_SPEED_H: int
SMS_STS_LOCK: int
SMS_STS_PRESENT_POSITION_L: int
SMS_STS_PRESENT_POSITION_H: int
SMS_STS_PRESENT_SPEED_L: int
SMS_STS_PRESENT_SPEED_H: int
SMS_STS_PRESENT_LOAD_L: int
SMS_STS_PRESENT_LOAD_H: int
SMS_STS_PRESENT_VOLTAGE: int
SMS_STS_PRESENT_TEMPERATURE: int
SMS_STS_MOVING: int
SMS_STS_PRESENT_CURRENT_L: int
SMS_STS_PRESENT_CURRENT_H: int

class sms_sts(protocol_packet_handler):
    groupSyncWrite: _Union[GroupSyncWrite, _SyncWriter]
    def __init__(self, portHandler: _PacketPort) -> None: ...
    def WritePosEx(self, scs_id: int, position: int, speed: int, acc: int) -> tuple[int, int]: ...
    def ReadPos(self, scs_id: int) -> tuple[int, int, int]: ...
    def ReadSpeed(self, scs_id: int) -> tuple[int, int, int]: ...
    def ReadPosSpeed(self, scs_id: int) -> tuple[int, int, int, int]: ...
    def ReadMoving(self, scs_id: int) -> tuple[int, int, int]: ...
    def SyncWritePosEx(self, scs_id: int, position: int, speed: int, acc: int) -> bool: ...
    def RegWritePosEx(self, scs_id: int, position: int, speed: int, acc: int) -> tuple[int, int]: ...
    def RegAction(self) -> int: ...
    def WheelMode(self, scs_id: int) -> tuple[int, int]: ...
    def WriteSpec(self, scs_id: int, speed: int, acc: int) -> tuple[int, int]: ...
    def LockEprom(self, scs_id: int) -> tuple[int, int]: ...
    def unLockEprom(self, scs_id: int) -> tuple[int, int]: ...
