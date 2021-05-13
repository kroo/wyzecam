# type: ignore

import ctypes
import json
import random
import string
import time

from wyzecam.tutk import tutk, tutk_protocol

RESPONDED = 2

RECIEVED = 1


def allow_retval(func):
    func.retval = None

    def wrapper(*args, **kwargs):
        if func.retval is not None:
            return func.retval
        return func(*args, **kwargs)

    def get_retval():
        return func.retval

    def set_retval(val):
        func.retval = val

    wrapper.get_retval = get_retval
    wrapper.set_retval = set_retval

    return wrapper


class MockTutkLibrary:
    """A mock tutk_platform_lib, for testing"""

    def __init__(self):
        self.got_resolving_bit_doorbell = None
        self.client_stop_called = False
        self.deinitialize_called = False
        self.session_closed_called = False
        self.got_hello = None
        self.got_auth = None
        self.got_resolving_bit = None

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
        if isinstance(timeout_ms, ctypes.c_int):
            timeout_ms = timeout_ms.value

        if self.got_hello == RECIEVED:
            encoded_response = self.respond_10000_hello()
            ctl_data[: len(encoded_response)] = encoded_response
            ctl_data_len.value = len(encoded_response)
            self.got_hello = RESPONDED
            return len(encoded_response)
        elif self.got_auth == RECIEVED:
            encoded_response = self.respond_10002_auth()
            ctl_data[: len(encoded_response)] = encoded_response
            ctl_data_len.value = len(encoded_response)
            self.got_auth = RESPONDED
            return len(encoded_response)
        elif self.got_resolving_bit == RECIEVED:
            encoded_response = self.respond_10056_resolving_bit()
            ctl_data[: len(encoded_response)] = encoded_response
            ctl_data_len.value = len(encoded_response)
            self.got_resolving_bit = RESPONDED
            return len(encoded_response)
        elif self.got_resolving_bit_doorbell == RECIEVED:
            encoded_response = self.respond_10052_resolving_bit_doorbell()
            ctl_data[: len(encoded_response)] = encoded_response
            ctl_data_len.value = len(encoded_response)
            self.got_resolving_bit = RESPONDED
            return len(encoded_response)
        else:
            time.sleep(timeout_ms / 10_000)  # 10x faster than usual
            return tutk.AV_ER_TIMEOUT

    def respond_10056_resolving_bit(self):
        response = bytes(1)
        encoded_response = tutk_protocol.encode(10057, len(response), response)
        return encoded_response

    def respond_10052_resolving_bit_doorbell(self):
        response = bytes(1)
        encoded_response = tutk_protocol.encode(10053, len(response), response)
        return encoded_response

    def respond_10002_auth(self):
        response = json.dumps({"connectionRes": "1", "cameraInfo": {}}).encode(
            "ascii"
        )
        encoded_response = tutk_protocol.encode(10003, len(response), response)
        return encoded_response

    def respond_10000_hello(self):
        camera_status = 3
        challenge_bytes = "".join(
            random.choice(string.ascii_letters) for _ in range(16)
        ).encode("ascii")
        response = bytes([camera_status]) + challenge_bytes
        encoded_response = tutk_protocol.encode(10001, len(response), response)
        return encoded_response

    def avClientSetMaxBufSize(self, size):
        pass

    def avClientStop(self, av_chan_id):
        self.client_stop_called = True

    def avSendIOCtrl(self, av_chan_id, ctrl_type, cdata, length):
        data = ctypes.cast(cdata, ctypes.POINTER(ctypes.c_char))[:length]
        print(data)
        header, data = tutk_protocol.decode(data)
        if header.code == 10000:
            self.got_hello = RECIEVED
        elif header.code == 10002:
            self.got_auth = RECIEVED
        elif header.code == 10056:
            self.got_resolving_bit = RECIEVED
        elif header.code == 10052:
            self.got_resolving_bit_doorbell = RECIEVED
        else:
            raise ValueError("Unexpected command sent!")
        print(header, data)

    def avClientStart(
        self,
        session_id,
        username,
        password,
        n_timeout,
        user_defined_service_type_ptr,
        chan_id,
    ):
        return 0

    def avInitialize(self, max_num_channels):
        return 0

    def avDeInitialize(self):
        self.deinitialize_called = True

    def IOTC_Session_Check(self, session_id, sess_info_ptr):
        return 0

    def IOTC_Session_Close(self, session_id):
        self.session_closed_called = True

    def IOTC_Connect_ByUID(self, p2p_id):
        return 0

    @allow_retval
    def IOTC_Connect_ByUID_Parallel(self, p2p_id, session_id):
        return session_id

    def IOTC_Set_Log_Path(self, path, max_size):
        pass

    def IOTC_Get_Version(self, version_ptr: ctypes.POINTER):
        version_ptr.contents.value = 0xDEADBEEF

    def IOTC_Initialize2(self, udp_port):
        return 0

    def IOTC_DeInitialize(self):
        pass

    def IOTC_Get_SessionID(self):
        return 0
