# type: ignore

import ctypes


# noinspection PyPep8Naming,PyMethodMayBeStatic
class MockTutkLibrary:
    """A mock tutk_platform_lib, for testing"""

    def avRecvFrameData2(
        self,
        frame_data_ptr,
        frame_data_max_ptr,
        frame_data_actual_len_ptr,
        frame_data_expected_len_ptr,
        frame_info_ptr,
        frame_info_max_len,
        frame_info_actual_len_ptr,
        frame_index_ptr,
    ):
        pass

    def avRecvIOCtrl(
        self,
        av_chan_id,
        pn_io_ctrl_type_ptr,
        ctl_data,
        ctl_data_len,
        timeout_ms,
    ):
        pass

    def avClientSetMaxBufSize(self, size):
        pass

    def avClientStop(self, av_chan_id):
        pass

    def avSendIOCtrl(self, av_chan_id, ctrl_type, cdata, length):
        pass

    def avClientStart(
        self,
        session_id,
        username,
        password,
        n_timeout,
        user_defined_service_type_ptr,
        chan_id,
    ):
        pass

    def avInitialize(self, max_num_channels):
        return 0

    def avDeInitialize(self):
        pass

    def IOTC_Session_Check(session_id, sess_info_ptr):
        pass

    def IOTC_Session_Close(self, session_id):
        pass

    def IOTC_Connect_ByUID(self, p2p_id):
        pass

    def IOTC_Set_Log_Path(self, path, max_size):
        pass

    def IOTC_Get_Version(self, version_ptr: ctypes.POINTER):
        version_ptr.contents.value = 0xDEADBEEF

    def IOTC_Initialize2(self, udp_port):
        return 0

    def IOTC_DeInitialize(self):
        pass
