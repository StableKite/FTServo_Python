"""Native public interface; implementation and wire behavior are unchanged."""
from typing import Union as _Union
from ._interfaces import SyncWriter as _SyncWriter
from ._interfaces import PacketPort as _PacketPort
from .scservo_def import *
from .protocol_packet_handler import *
from .group_sync_write import *
SCSCL_1M: int
SCSCL_0_5M: int
SCSCL_250K: int
SCSCL_128K: int
SCSCL_115200: int
SCSCL_76800: int
SCSCL_57600: int
SCSCL_38400: int
SCSCL_MODEL_L: int
SCSCL_MODEL_H: int
scs_id: int
SCSCL_BAUD_RATE: int
SCSCL_MIN_ANGLE_LIMIT_L: int
SCSCL_MIN_ANGLE_LIMIT_H: int
SCSCL_MAX_ANGLE_LIMIT_L: int
SCSCL_MAX_ANGLE_LIMIT_H: int
SCSCL_CW_DEAD: int
SCSCL_CCW_DEAD: int
SCSCL_TORQUE_ENABLE: int
SCSCL_GOAL_POSITION_L: int
SCSCL_GOAL_POSITION_H: int
SCSCL_GOAL_TIME_L: int
SCSCL_GOAL_TIME_H: int
SCSCL_GOAL_SPEED_L: int
SCSCL_GOAL_SPEED_H: int
SCSCL_LOCK: int
SCSCL_PRESENT_POSITION_L: int
SCSCL_PRESENT_POSITION_H: int
SCSCL_PRESENT_SPEED_L: int
SCSCL_PRESENT_SPEED_H: int
SCSCL_PRESENT_LOAD_L: int
SCSCL_PRESENT_LOAD_H: int
SCSCL_PRESENT_VOLTAGE: int
SCSCL_PRESENT_TEMPERATURE: int
SCSCL_MOVING: int
SCSCL_PRESENT_CURRENT_L: int
SCSCL_PRESENT_CURRENT_H: int

class scscl(protocol_packet_handler):
    groupSyncWrite: _Union[GroupSyncWrite, _SyncWriter]
    def __init__(self, portHandler: _PacketPort) -> None: ...
    def WritePos(self, scs_id: int, position: int, time: int, speed: int) -> tuple[int, int]: ...
    def ReadPos(self, scs_id: int) -> tuple[int, int, int]: ...
    def ReadSpeed(self, scs_id: int) -> tuple[int, int, int]: ...
    def ReadPosSpeed(self, scs_id: int) -> tuple[int, int, int, int]: ...
    def ReadMoving(self, scs_id: int) -> tuple[int, int, int]: ...
    def SyncWritePos(self, scs_id: int, position: int, time: int, speed: int) -> bool: ...
    def RegWritePos(self, scs_id: int, position: int, time: int, speed: int) -> tuple[int, int]: ...
    def RegAction(self) -> int: ...
    def PWMMode(self, scs_id: int) -> tuple[int, int]: ...
    def WritePWM(self, scs_id: int, time: int) -> tuple[int, int]: ...
    def LockEprom(self, scs_id: int) -> tuple[int, int]: ...
    def unLockEprom(self, scs_id: int) -> tuple[int, int]: ...
