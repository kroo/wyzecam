import typing
from typing import Optional, Union

import pathlib
from ctypes import (
    CDLL,
    Array,
    Structure,
    c_char,
    c_char_p,
    c_int,
    c_int32,
    c_uint,
    c_uint8,
    c_uint16,
    c_uint32,
    c_ushort,
    cdll,
    pointer,
    sizeof,
)

BITRATE_360P = 0x1E
"""
The bitrate used by the "360P" setting in the app.  Approx 30 KB/s.
"""

BITRATE_SD = 0x3C
"""
The bitrate used by the "SD" setting in the app.  Approx 60 KB/s.
"""
BITRATE_HD = 0x78
"""
The bitrate used by the "HD" setting in the app.  Approx 120 KB/s.
"""

BITRATE_SUPER_HD = 0x96
"""
A bitrate higher than the "HD" setting in the app.  Approx 150 KB/s.
"""

BITRATE_SUPER_SUPER_HD = 0xF0
"""
A bitrate higher than the "HD" setting in the app.  Approx 240 KB/s.
"""

FRAME_SIZE_1080P = 0
"""
Represents the size of the video stream sent back from the server; 1080P
or 1920x1080 pixels.
"""

FRAME_SIZE_360P = 1
"""
Represents the size of the video stream sent back from the server; 360P
or 640x360 pixels.
"""

FRAME_SIZE_DOORBELL_HD = 3
"""
Represents the size of the video stream sent back from the server;
portrait 1296 x 1728.
"""

FRAME_SIZE_DOORBELL_SD = 4
"""
Represents the size of the video stream sent back from the server;
portrait 480 x 640.
"""

IOTYPE_USER_DEFINED_START = 256

AV_ER_TIMEOUT = -20011
"""
An error raised when the AV library times out.
"""

AV_ER_SESSION_CLOSE_BY_REMOTE = -20015
"""
An error raised when the camera closes the connection.
"""

AV_ER_DATA_NOREADY = -20012
"""
An error raised when the client asks for data not yet available on the camera.
"""

AV_ER_INCOMPLETE_FRAME = -20013
"""
An error sent during video streaming if the camera wasn't able to send a complete frame.
"""

AV_ER_LOSED_THIS_FRAME = -20014
"""
An error sent during video streaming if the frame was lost in transmission.
"""

project_root = pathlib.Path(__file__).parent


class TutkError(RuntimeError):
    name_mapping = {
        -1: "IOTC_ER_SERVER_NOT_RESPONSE",
        -2: "IOTC_ER_FAIL_RESOLVE_HOSTNAME",
        -3: "IOTC_ER_ALREADY_INITIALIZED",
        -4: "IOTC_ER_FAIL_CREATE_MUTEX",
        -5: "IOTC_ER_FAIL_CREATE_THREAD",
        -6: "IOTC_ER_FAIL_CREATE_SOCKET",
        -7: "IOTC_ER_FAIL_SOCKET_OPT",
        -8: "IOTC_ER_FAIL_SOCKET_BIND",
        -10: "IOTC_ER_UNLICENSE",
        -11: "IOTC_ER_LOGIN_ALREADY_CALLED",
        -12: "IOTC_ER_NOT_INITIALIZED",
        -13: "IOTC_ER_TIMEOUT",
        -14: "IOTC_ER_INVALID_SID",
        -15: "IOTC_ER_UNKNOWN_DEVICE",
        -16: "IOTC_ER_FAIL_GET_LOCAL_IP",
        -17: "IOTC_ER_LISTEN_ALREADY_CALLED",
        -18: "IOTC_ER_EXCEED_MAX_SESSION",
        -19: "IOTC_ER_CAN_NOT_FIND_DEVICE",
        -20: "IOTC_ER_CONNECT_IS_CALLING",
        -22: "IOTC_ER_SESSION_CLOSE_BY_REMOTE",
        -23: "IOTC_ER_REMOTE_TIMEOUT_DISCONNECT",
        -24: "IOTC_ER_DEVICE_NOT_LISTENING",
        -26: "IOTC_ER_CH_NOT_ON",
        -27: "IOTC_ER_FAIL_CONNECT_SEARCH",
        -28: "IOTC_ER_MASTER_TOO_FEW",
        -29: "IOTC_ER_AES_CERTIFY_FAIL",
        -31: "IOTC_ER_SESSION_NO_FREE_CHANNEL",
        -32: "IOTC_ER_TCP_TRAVEL_FAILED",
        -33: "IOTC_ER_TCP_CONNECT_TO_SERVER_FAILED",
        -34: "IOTC_ER_CLIENT_NOT_SECURE_MODE",
        -35: "IOTC_ER_CLIENT_SECURE_MODE",
        -36: "IOTC_ER_DEVICE_NOT_SECURE_MODE",
        -37: "IOTC_ER_DEVICE_SECURE_MODE",
        -38: "IOTC_ER_INVALID_MODE",
        -39: "IOTC_ER_EXIT_LISTEN",
        -40: "IOTC_ER_NO_PERMISSION",
        -41: "IOTC_ER_NETWORK_UNREACHABLE",
        -42: "IOTC_ER_FAIL_SETUP_RELAY",
        -43: "IOTC_ER_NOT_SUPPORT_RELAY",
        -44: "IOTC_ER_NO_SERVER_LIST",
        -45: "IOTC_ER_DEVICE_MULTI_LOGIN",
        -46: "IOTC_ER_INVALID_ARG",
        -47: "IOTC_ER_NOT_SUPPORT_PE",
        -48: "IOTC_ER_DEVICE_EXCEED_MAX_SESSION",
        -20000: "AV_ER_INVALID_ARG",
        -20001: "AV_ER_BUFPARA_MAXSIZE_INSUFF",
        -20002: "AV_ER_EXCEED_MAX_CHANNEL",
        -20003: "AV_ER_MEM_INSUFF",
        -20004: "AV_ER_FAIL_CREATE_THREAD",
        -20005: "AV_ER_EXCEED_MAX_ALARM",
        -20006: "AV_ER_EXCEED_MAX_SIZE",
        -20007: "AV_ER_SERV_NO_RESPONSE",
        -20008: "AV_ER_CLIENT_NO_AVLOGIN",
        -20009: "AV_ER_WRONG_VIEWACCorPWD",
        -20010: "AV_ER_INVALID_SID",
        -20011: "AV_ER_TIMEOUT",
        -20012: "AV_ER_DATA_NOREADY",
        -20013: "AV_ER_INCOMPLETE_FRAME",
        -20014: "AV_ER_LOSED_THIS_FRAME",
        -20015: "AV_ER_SESSION_CLOSE_BY_REMOTE",
        -20016: "AV_ER_REMOTE_TIMEOUT_DISCONNECT",
        -20017: "AV_ER_SERVER_EXIT",
        -20018: "AV_ER_CLIENT_EXIT",
        -20019: "AV_ER_NOT_INITIALIZED",
        -20020: "AV_ER_CLIENT_NOT_SUPPORT",
        -20021: "AV_ER_SENDIOCTRL_ALREADY_CALLED",
        -20022: "AV_ER_SENDIOCTRL_EXIT",
        -20023: "AV_ER_NO_PERMISSION",
        -20024: "AV_ER_WRONG_ACCPWD_LENGTH",
    }

    def __init__(self, code):
        super().__init__(code)
        self.code = code

    @property
    def name(self):
        return TutkError.name_mapping.get(self.code, self.code)

    def __str__(self):
        return self.name


class FormattedStructure(Structure):
    def __str__(self):
        fields = "\n\t".join(
            [
                f"{field[0]}: {getattr(self, field[0])}"
                for field in self._fields_
                if getattr(self, field[0])
            ]
        )
        return f"{self.__class__.__name__}:\n\t{fields}"


class SInfoStruct(FormattedStructure):
    """
    Result of iotc_session_check(), this struct holds a bunch of diagnostic
    data about the state of the connection to the camera.

    :var mode: 0: P2P mode, 1: Relay mode, 2: LAN mode
    :vartype mode: int
    :var c_or_d: 0: As a Client, 1: As a Device
    :vartype c_or_d: int
    :var uid: The UID of the device.
    :vartype uid: str
    :var remote_ip: The IP address of remote site used during this IOTC session.
    :vartype remote_ip: str
    :var remote_port: The port number of remote site used during this IOTC session.
    :vartype remote_port: int
    :var tx_packet_count: The total packets sent from the device and the client during this IOTC session.
    :vartype tx_packet_count: int
    :var rx_packet_count: The total packets received in the device and the client during this IOTC session
    :vartype rx_packet_count: int
    :var iotc_version: version number of the IOTC device.
    :vartype iotc_version: int
    :var vendor_id: id of the vendor of the device
    :vartype vendor_id: int
    :var product_id: id of the product of the device
    :vartype product_id: int
    :var group_id: id of the group of the device
    :vartype group_id: int
    :var nat_type: The remote NAT type.
    :vartype nat_type: int
    :var is_secure: 0: The IOTC session is in non-secure mode, 1: The IOTC session is in secure mode
    :vartype is_secure: int

    """

    _fields_ = [
        ("mode", c_uint8),  # 0: P2P mode, 1: Relay mode, 2: LAN mode
        ("c_or_d", c_uint8),  # 0: As a Client, 1: As a Device
        ("uid", c_char * 21),  # The UID of the device.
        (
            "remote_ip",
            c_char * 17,
        ),  # The IP address of remote site used during this IOTC session.
        (
            "remote_port",
            c_uint8,
        ),  # The port number of remote site used during this IOTC session.
        (
            "tx_packet_count",
            c_uint,
        ),  # The total packets sent from the device and the client during this IOTC session.
        (
            "rx_packet_count",
            c_uint,
        ),  # The total packets received in the device and the client during this IOTC session
        ("iotc_version", c_uint),
        ("vendor_id", c_ushort),
        ("product_id", c_ushort),
        ("group_id", c_ushort),
        ("nat_type", c_uint8),  # The remote NAT type.
        (
            "is_secure",
            c_uint8,
        ),  # 0: The IOTC session is in non-secure mode, 1: The IOTC session is in secure mode
    ]


class FrameInfoStruct(FormattedStructure):
    """
    A struct recieved on every video frame, with lots of useful information
    about the frame sent by the camera.

    :var codec_id: 78: h264 80: h265
    :vartype codec_id: int
    :var is_keyframe: True if the frame being described is a keyframe
    :vartype is_keyframe: int
    :var cam_index: The index of the camera
    :vartype cam_index: int
    :var online_num: Not clear
    :vartype online_num: int
    :var framerate: framerate of the video frame, in frames / second
    :vartype framerate: int
    :var frame_size: frame size of the video frame, either `FRAME_SIZE_1080P` or `FRAME_SIZE_360P`
    :vartype frame_size: int
    :var bitrate: bitrate of the video frame, as configured.
    :vartype bitrate: int
    :var timestamp_ms: the millisecond component of the timestamp.
    :vartype timestamp_ms: int
    :var timestamp: the seconds component of the timestamp.
    :vartype timestamp: int
    :var frame_len: the size of the data sent by the camera, in bytes.
    :vartype frame_len: int
    :var frame_no: the current frame number as recorded by the camera
    :vartype frame_no: int
    :var ac_mac_addr: unknown
    :vartype ac_mac_addr: str
    :var n_play_token: unknown
    :vartype n_play_token: int
    """

    _fields_ = [
        ("codec_id", c_uint16),
        ("is_keyframe", c_uint8),
        ("cam_index", c_uint8),
        ("online_num", c_uint8),
        ("framerate", c_uint8),
        ("frame_size", c_uint8),
        ("bitrate", c_uint8),
        ("timestamp_ms", c_uint32),
        ("timestamp", c_uint32),
        ("frame_len", c_uint32),
        ("frame_no", c_uint32),
        ("ac_mac_addr", c_char * 12),
        ("n_play_token", c_int32),
    ]


class FrameInfo3Struct(FormattedStructure):
    _fields_ = [
        ("codec_id", c_uint16),
        ("is_keyframe", c_uint8),
        ("cam_index", c_uint8),
        ("online_num", c_uint8),
        ("framerate", c_uint8),
        ("frame_size", c_uint8),
        ("bitrate", c_uint8),
        ("timestamp_ms", c_uint32),
        ("timestamp", c_uint32),
        ("frame_len", c_uint32),
        ("frame_no", c_uint32),
        ("ac_mac_addr", c_char * 12),
        ("n_play_token", c_int32),
        ("face_pos_x", c_uint16),
        ("face_pos_y", c_uint16),
        ("face_width", c_uint16),
        ("face_height", c_uint16),
    ]


def av_recv_frame_data(
    tutk_platform_lib: CDLL, av_chan_id: c_int
) -> typing.Tuple[
    int,
    Optional[bytes],
    Optional[Union[FrameInfoStruct, FrameInfo3Struct]],
    Optional[int],
]:
    """A new version AV client receives frame data from an AV server.

    An AV client uses this function to receive frame data from AV server

    :param tutk_platform_lib: the c library loaded from the 'load_library' call.
    :param av_chan_id: The channel ID of the AV channel to recv data on.
    :return: a 4-tuple of errno, frame_data, frame_info, and frame_index
    """
    frame_data_max_len = 5 * 1024 * 1024
    frame_data_actual_len = c_int()
    frame_data_expected_len = c_int()
    frame_data = (c_char * frame_data_max_len)()
    frame_info_actual_len = c_int()
    frame_index = c_uint()

    frame_info_max_len = max(sizeof(FrameInfo3Struct), sizeof(FrameInfoStruct))
    frame_info = (c_char * frame_info_max_len)()

    errno = tutk_platform_lib.avRecvFrameData2(
        av_chan_id,
        pointer(frame_data),
        c_int(frame_data_max_len),
        pointer(frame_data_actual_len),
        pointer(frame_data_expected_len),
        pointer(frame_info),
        c_int(frame_info_max_len),
        pointer(frame_info_actual_len),
        pointer(frame_index),
    )

    if errno < 0:
        return errno, None, None, None
    else:
        frame_data_actual: bytes = frame_data[: frame_data_actual_len.value]  # type: ignore
        frame_info_actual: Union[FrameInfoStruct, FrameInfo3Struct]
        if frame_info_actual_len.value == sizeof(FrameInfo3Struct):
            frame_info_actual = FrameInfo3Struct.from_buffer(frame_info)
        elif frame_info_actual_len.value == sizeof(FrameInfoStruct):
            frame_info_actual = FrameInfoStruct.from_buffer(frame_info)
        else:
            from wyzecam.tutk.tutk_protocol import TutkWyzeProtocolError

            raise TutkWyzeProtocolError(
                f"Unknown frame info structure format! len={frame_info_actual_len}"
            )

        return (
            0,
            frame_data_actual,
            frame_info_actual,
            frame_index.value,
        )


def av_recv_io_ctrl(
    tutk_platform_lib: CDLL, av_chan_id: c_int, timeout_ms: int
) -> typing.Tuple[int, int, Optional[typing.List[bytes]]]:
    """Receive AV IO control.

    This function is used by AV servers or AV clients to receive a AV IO control.
    :param tutk_platform_lib: the c library loaded from the 'load_library' call.
    :param av_chan_id: The channel ID of the AV channel to be stopped
    :param timeout_ms: the number of milliseconds to wait before timing out
    :returns: a tuple of (the length of the io_ctrl received (or error number),
              the io_ctrl_type, and the data in bytes)
    """
    pn_io_ctrl_type = c_uint()
    ctl_data_len = 1024 * 1024
    ctl_data = (c_char * ctl_data_len)()
    actual_len = tutk_platform_lib.avRecvIOCtrl(
        av_chan_id,
        pointer(pn_io_ctrl_type),
        ctl_data,
        c_int(ctl_data_len),
        c_int(timeout_ms),
    )

    return (
        actual_len,
        pn_io_ctrl_type.value,
        ctl_data[0:actual_len] if actual_len > 0 else None,
    )


def av_client_set_max_buf_size(tutk_platform_lib: CDLL, size: int) -> None:
    """Set the maximum video frame buffer used in AV client.

    AV client sets the maximum video frame buffer by this function. The size of
    video frame buffer will affect the streaming fluency. The default size of
    video frame buffer is 1MB.

    :param tutk_platform_lib: the c library loaded from the 'load_library' call.
    :param size: The maximum video frame buffer, in unit of kilo-byte
    """
    tutk_platform_lib.avClientSetMaxBufSize(c_int(size))


def av_client_stop(tutk_platform_lib: CDLL, av_chan_id: c_int) -> None:
    """Stop an AV client.

    An AV client stop AV channel by this function if this channel is no longer
    required.

    :param tutk_platform_lib: the c library loaded from the 'load_library' call.
    :param av_chan_id: The channel ID of the AV channel to be stopped
    """
    tutk_platform_lib.avClientStop(av_chan_id)


def av_send_io_ctrl(
    tutk_platform_lib: CDLL,
    av_chan_id: c_int,
    ctrl_type: int,
    data: Optional[bytes],
) -> c_int:
    if data is None:
        length = 0
        cdata = None
    else:
        length = len(data)
        cdata = c_char_p(data)
    errcode: c_int = tutk_platform_lib.avSendIOCtrl(
        av_chan_id, c_uint(ctrl_type), cdata, length
    )
    return errcode


def iotc_session_close(tutk_platform_lib: CDLL, session_id: c_int) -> None:
    """Used by a device or a client to close a IOTC session.

    A device or a client uses this function to close a IOTC session specified
    by its session ID if this IOTC session is no longer required.

    :param tutk_platform_lib: the c library loaded from the 'load_library' call.
    :param session_id: The session ID of the IOTC session to start AV client
    """
    tutk_platform_lib.IOTC_Session_Close(session_id)


def av_client_start(
    tutk_platform_lib: CDLL,
    session_id: Union[int, c_int],
    username: bytes,
    password: bytes,
    timeout_secs: int,
    channel_id: int,
) -> typing.Tuple[c_int, c_uint]:
    """Start an AV client.

    Start an AV client by providing view account and password. It shall pass
    the authentication of the AV server before receiving AV data.

    :param tutk_platform_lib: the c library loaded from the 'load_library' call.
    :param session_id: The session ID of the IOTC session to start AV client
    :param username: The view account for authentication
    :param password: The view password for authentication
    :param timeout_secs: The timeout for this function in unit of second
                         Specify it as 0 will make this AV client try connection once
                         and this process will exit immediately if not connection
                         is unsuccessful.
    :param channel_id: The channel ID of the channel to start AV client
    :return: returns a tuple of two values:
             - av_chan_id: AV channel ID if return value >= 0; error code if return value < 0
             - pn_serv_type: The user-defined service type set when an AV server starts. Can be NULL.
    """
    n_timeout = c_uint(timeout_secs)
    user_defined_service_type = c_uint()
    chan_id = c_uint8(channel_id)
    av_chan_id = tutk_platform_lib.avClientStart(
        session_id,
        c_char_p(username),
        c_char_p(password),
        n_timeout,
        pointer(user_defined_service_type),
        chan_id,
    )
    return av_chan_id, user_defined_service_type


def av_initialize(
    tutk_platform_lib: CDLL, max_num_channels: Optional[int] = 1
) -> int:
    """Initialize AV module.

    This function is used by AV servers or AV clients to initialize AV module
    and shall be called before any AV module related function is invoked.

    :param tutk_platform_lib: the c library loaded from the 'load_library' call.
    :param max_num_channels: The max number of AV channels. If it is specified
                             less than 1, AV will set max number of AV channels as 1.

    :return:The actual maximum number of AV channels to be set. Error code if return value < 0.
    """
    max_chans: int = tutk_platform_lib.avInitialize(max_num_channels)
    return max_chans


def av_deinitialize(tutk_platform_lib: CDLL) -> int:
    """Deinitialize AV module.

    This function will deinitialize AV module.

    :param tutk_platform_lib: The underlying c library (from tutk.load_library())
    :return: Error code if return value < 0
    """
    errno: int = tutk_platform_lib.avDeInitialize()
    return errno


def iotc_session_check(
    tutk_platform_lib: CDLL, session_id: c_int
) -> typing.Tuple[int, SInfoStruct]:
    """Used by a device or a client to check the IOTC session info.

    A device or a client may use this function to check if the IOTC session is
    still alive as well as getting the IOTC session info.

    :param tutk_platform_lib: The underlying c library (from tutk.load_library())
    :param session_id: The session ID of the IOTC session to be checked
    :return: The session info of specified IOTC session
    """
    sess_info = SInfoStruct()
    err_code = tutk_platform_lib.IOTC_Session_Check(
        session_id, pointer(sess_info)
    )
    return err_code, sess_info


def iotc_connect_by_uid(tutk_platform_lib: CDLL, p2p_id: str) -> c_int:
    """Used by a client to connect a device.

    This function is for a client to connect a device by specifying the UID of
    that device. If connection is established with the help of IOTC servers,
    the IOTC session ID will be returned in this function and then device and
    client can communicate for the other later by using this IOTC session ID.

    :param tutk_platform_lib: The underlying c library (from tutk.load_library())
    :param p2p_id: The UID of a device that client wants to connect
    :return: IOTC session ID if return value >= 0, error code if return value < 0
    """
    session_id: c_int = tutk_platform_lib.IOTC_Connect_ByUID(
        c_char_p(p2p_id.encode("ascii"))
    )
    return session_id


def iotc_get_session_id(tutk_platform_lib: CDLL) -> c_int:
    """Used by a client to get a tutk_platform_free session ID.

    This function is for a client to get a tutk_platform_free
    session ID used for a parameter of iotc_connect_by_uid_parallel()
    """
    session_id: c_int = tutk_platform_lib.IOTC_Get_SessionID()
    return session_id


def iotc_connect_by_uid_parallel(
    tutk_platform_lib: CDLL, p2p_id: str, session_id: c_int
) -> c_int:
    """Used by a client to connect a device and bind to a specified session ID.

    This function is for a client to connect a device by specifying the UID of that device,
    and bind to a tutk_platform_free session ID from IOTC_Get_SessionID(). If connection is
    established with the help of IOTC servers, the IOTC_ER_NoERROR will be returned in this
    function and then device and client can communicate for the other later by using this
    IOTC session ID. If this function is called by multiple threads, the connections will
    be processed concurrently.

    :param tutk_platform_lib: The underlying c library (from tutk.load_library())
    :param p2p_id: The UID of a device that client wants to connect
    :param session_id: The Session ID got from IOTC_Get_SessionID() the connection should bind to.
    :return: IOTC session ID if return value >= 0, error code if return value < 0
    """
    resultant_session_id: c_int = tutk_platform_lib.IOTC_Connect_ByUID_Parallel(
        c_char_p(p2p_id.encode("ascii")), session_id
    )
    return resultant_session_id


def iotc_connect_stop_by_session_id(
    tutk_platform_lib: CDLL, session_id: c_int
) -> c_int:
    """
    Used by a client to stop a specific session connecting a device.

    This function is for a client to stop connecting a device. Since IOTC_Connect_ByUID_Parallel()
     is a block processes, that means the client will have to wait for the return of these functions
     before executing sequential instructions. In some cases, users may want the client to stop
     connecting immediately by this function in another thread before the return of connection process.

    :param tutk_platform_lib: The underlying c library (from tutk.load_library())
    :param session_id: The Session ID got from IOTC_Get_SessionID() the connection should bind to.
    :return: Error code if return value < 0, otherwise 0 if successful
    """
    errno: c_int = tutk_platform_lib.IOTC_Connect_Stop_BySID(session_id)
    return errno


def iotc_set_log_path(tutk_platform_lib: CDLL, path: str) -> None:
    """Set path of log file.

    Set the absolute path of log file
    """
    tutk_platform_lib.IOTC_Set_Log_Path(
        c_char_p(path.encode("ascii")), c_int(0)
    )


def iotc_get_version(tutk_platform_lib: CDLL) -> int:
    """Get the version of IOTC module.

    This function returns the version of IOTC module.
    """
    version = c_uint32()
    tutk_platform_lib.IOTC_Get_Version(pointer(version))
    return version.value


def iotc_initialize(tutk_platform_lib: CDLL, udp_port: int = 0) -> int:
    """Initialize IOTC module.

    This function is used by devices or clients to initialize IOTC module and
    shall be called before any IOTC module related function is invoked except
    for IOTC_Set_Max_Session_Number().

    The different between this function and IOTC_Initialize() is this function
    uses following steps to connect masters (1) IP addresses of master (2) if
    fails to connect in step 1, resolve predefined domain name of masters (3)
    try to connect again with the resolved IP address of step 2 if IP is
    resolved successfully.

    :param tutk_platform_lib: The underlying c library (from tutk.load_library())
    :param udp_port: Specify a UDP port. Random UDP port is used if it is specified as 0.
    :return: 0 if successful, Error code if return value < 0
    """
    errno: int = tutk_platform_lib.IOTC_Initialize2(udp_port)
    return errno


def iotc_deinitialize(tutk_platform_lib: CDLL) -> c_int:
    """Deinitialize IOTC module.

    This function will deinitialize IOTC module.

    :param tutk_platform_lib: The underlying c library (from tutk.load_library())
    :return: Error code if return value < 0
    """
    errno: c_int = tutk_platform_lib.IOTC_DeInitialize()
    return errno


def load_library(
    shared_lib_path: Optional[str] = None,
) -> CDLL:
    """Load the underlying iotc library

    :param shared_lib_path: the path to the shared library libIOTCAPIs_ALL
    :return: the tutk_platform_lib, suitable for passing to other functions in this module
    """
    if shared_lib_path is None:
        if pathlib.Path("/usr/local/lib/libIOTCAPIs_ALL.dylib").exists():
            shared_lib_path = "/usr/local/lib/libIOTCAPIs_ALL.dylib"
        if pathlib.Path("/usr/local/lib/libIOTCAPIs_ALL.so").exists():
            shared_lib_path = "/usr/local/lib/libIOTCAPIs_ALL.so"

    if shared_lib_path is None:
        raise RuntimeError(
            "Could not find libIOTCAPIs_ALL shared library.  See documentation, "
            "or specify the full path as an argument to load_library()."
        )
    return cdll.LoadLibrary(shared_lib_path)
