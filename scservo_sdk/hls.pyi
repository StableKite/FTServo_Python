"""Native public interface; implementation and wire behavior are unchanged."""
from typing import Union as _Union
from ._interfaces import SyncWriter as _SyncWriter
from ._interfaces import PacketPort as _PacketPort
from .scservo_def import *
from .protocol_packet_handler import *
from .group_sync_read import *
from .group_sync_write import *
HLS_1M: int
HLS_0_5M: int
HLS_250K: int
HLS_128K: int
HLS_115200: int
HLS_76800: int
HLS_57600: int
HLS_38400: int
HLS_MODEL_L: int
HLS_MODEL_H: int
HLS_ID: int
HLS_BAUD_RATE: int
HLS_MIN_ANGLE_LIMIT_L: int
HLS_MIN_ANGLE_LIMIT_H: int
HLS_MAX_ANGLE_LIMIT_L: int
HLS_MAX_ANGLE_LIMIT_H: int
HLS_CW_DEAD: int
HLS_CCW_DEAD: int
HLS_OFS_L: int
HLS_OFS_H: int
HLS_MODE: int
HLS_TORQUE_ENABLE: int
HLS_ACC: int
HLS_GOAL_POSITION_L: int
HLS_GOAL_POSITION_H: int
HLS_GOAL_TORQUE_L: int
HLS_GOAL_TORQUE_H: int
HLS_GOAL_SPEED_L: int
HLS_GOAL_SPEED_H: int
HLS_LOCK: int
HLS_PRESENT_POSITION_L: int
HLS_PRESENT_POSITION_H: int
HLS_PRESENT_SPEED_L: int
HLS_PRESENT_SPEED_H: int
HLS_PRESENT_LOAD_L: int
HLS_PRESENT_LOAD_H: int
HLS_PRESENT_VOLTAGE: int
HLS_PRESENT_TEMPERATURE: int
HLS_MOVING: int
HLS_PRESENT_CURRENT_L: int
HLS_PRESENT_CURRENT_H: int

class hls(protocol_packet_handler):
    groupSyncWrite: _Union[GroupSyncWrite, _SyncWriter]
    def __init__(self, portHandler: _PacketPort) -> None: ...
    def WritePosEx(self, scs_id: int, position: int, speed: int, acc: int, torque: int) -> tuple[int, int]: ...
    def ReadPos(self, scs_id: int) -> tuple[int, int, int]: ...
    def ReadSpeed(self, scs_id: int) -> tuple[int, int, int]: ...
    def ReadPosSpeed(self, scs_id: int) -> tuple[int, int, int, int]: ...
    def ReadMoving(self, scs_id: int) -> tuple[int, int, int]: ...
    def SyncWritePosEx(self, scs_id: int, position: int, speed: int, acc: int, torque: int) -> bool: ...
    def RegWritePosEx(self, scs_id: int, position: int, speed: int, acc: int, torque: int) -> tuple[int, int]: ...
    def RegAction(self) -> int: ...
    def WheelMode(self, scs_id: int) -> tuple[int, int]: ...
    def WriteSpec(self, scs_id: int, speed: int, acc: int, torque: int) -> tuple[int, int]: ...
    def LockEprom(self, scs_id: int) -> tuple[int, int]: ...
    def unLockEprom(self, scs_id: int) -> tuple[int, int]: ...
