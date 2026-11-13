"""Native public interface; implementation and wire behavior are unchanged."""
from typing import Union as _Union
from ._interfaces import SyncWriter as _SyncWriter
from ._interfaces import PacketPort as _PacketPort
from .scservo_def import *
from .protocol_packet_handler import *
from .group_sync_read import *
from .group_sync_write import *
IMU_MODEL_L: int
IMU_MODEL_H: int
IMU_ID: int
IMU_BAUD_RATE: int
IMU_GYRO_DPS: int
IMU_ACC_SCAL: int
IMU_SFLP_ODR: int
IMU_LOCK: int
IMU_PRESENT_SLFP_QXL: int
IMU_PRESENT_SLFP_QXH: int
IMU_PRESENT_SLFP_QYL: int
IMU_PRESENT_SLFP_QYH: int
IMU_PRESENT_SLFP_QZL: int
IMU_PRESENT_SLFP_QZH: int
IMU_PRESENT_GYRO_WXL: int
IMU_PRESENT_GYRO_WXH: int
IMU_PRESENT_GYRO_WYL: int
IMU_PRESENT_GYRO_WYH: int
IMU_PRESENT_GYRO_WZL: int
IMU_PRESENT_GYRO_WZH: int
IMU_PRESENT_ACC_AXL: int
IMU_PRESENT_ACC_AXH: int
IMU_PRESENT_ACC_AYL: int
IMU_PRESENT_ACC_AYH: int
IMU_PRESENT_ACC_AZL: int
IMU_PRESENT_ACC_AZH: int

class imu(protocol_packet_handler):
    groupSyncWrite: _Union[GroupSyncWrite, _SyncWriter]
    def __init__(self, portHandler: _PacketPort) -> None: ...
    def readSlfpQxyz(self, scs_id: int) -> tuple[int, int, int, int, int]: ...
    def scs_halffloat(self, h: int) -> float: ...
    def scs_slfp_qw(self, qx: int, qy: int, qz: int) -> float: ...
    def readSlfp(self, scs_id: int) -> tuple[int, int, int, float, int, int]: ...
    def readGyro(self, scs_id: int) -> tuple[int, int, int, int, int]: ...
    def readAcc(self, scs_id: int) -> tuple[int, int, int, int, int]: ...
    def LockEprom(self, scs_id: int) -> tuple[int, int]: ...
    def unLockEprom(self, scs_id: int) -> tuple[int, int]: ...
