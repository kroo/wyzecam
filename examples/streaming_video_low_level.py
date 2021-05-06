import time

try:
    import av
except ImportError:
    av = None

try:
    import cv2
except ImportError:
    cv2 = None

from wyzecam.tutk import tutk
from wyzecam.tutk.tutk_ioctl_mux import TutkIOCtrlMux
from wyzecam.tutk.tutk_protocol import (
    K10000ConnectRequest,
    K10020CheckCameraInfo,
    K10056SetResolvingBit,
    respond_to_ioctrl_10001,
)


def main(current_camera):
    assert av, "missing PyAV, required for this example"
    assert cv2, "missing opencv-python, required for this example"

    p2p_id = current_camera["p2p_id"]
    enr = current_camera["enr"]
    mac = current_camera["mac"]
    product_model = current_camera["product_model"]
    phone_id = current_camera["phone_id"]
    open_userid = current_camera["open_userid"]

    # Load Library
    tutk_platform_lib = tutk.load_library()

    # Call IOTC_Initialize2, get sdk version
    tutk.iotc_initialize(tutk_platform_lib)
    version = tutk.iotc_get_version(tutk_platform_lib)
    print("Version:", hex(version))

    # connect by UID of the camera
    session_id = tutk.iotc_connect_by_uid(tutk_platform_lib, p2p_id)
    print("Connect by UID returned session_id=", session_id)

    # check session is established
    errcode, sess_info = tutk.iotc_session_check(tutk_platform_lib, session_id)
    print("Session check:", errcode)
    print(sess_info)

    # call AV initialize
    max_chans = tutk.av_initialize(tutk_platform_lib)
    print("AV Initialize:", max_chans)

    # call AV Client Start
    timeout_secs = 10
    channel_id = 0
    av_chan_id, pn_serv_type = tutk.av_client_start(
        tutk_platform_lib,
        session_id,
        b"admin",
        b"888888",
        timeout_secs,
        channel_id,
    )
    print(
        f"AV Client Start: chan_id={av_chan_id} expected_chan={channel_id} pn_serv_type={pn_serv_type.value}"
    )

    tutk.av_client_set_max_buf_size(tutk_platform_lib, 5 * 1024 * 1024)

    mux = TutkIOCtrlMux(tutk_platform_lib, av_chan_id)
    mux.start_listening()

    challenge = mux.send_ioctl(K10000ConnectRequest())
    challenge_data = challenge.result()
    challenge_response = respond_to_ioctrl_10001(
        challenge_data,
        challenge.resp_protocol,
        enr,
        product_model,
        mac,
        phone_id,
        open_userid,
    )
    auth_response = mux.send_ioctl(challenge_response)
    # wait for auth response
    mux.waitfor(auth_response)

    cam_info = mux.send_ioctl(K10020CheckCameraInfo())
    resolving = mux.send_ioctl(
        K10056SetResolvingBit(
            tutk.FRAME_SIZE_1080P, tutk.BITRATE_SUPER_SUPER_HD
        )
    )

    mux.waitfor([cam_info, resolving])
    mux.stop_listening()

    start_video_streaming(tutk_platform_lib, av_chan_id)

    # stop client
    tutk.av_client_stop(tutk_platform_lib, av_chan_id)

    # close session
    tutk.iotc_session_close(tutk_platform_lib, session_id)

    # deinitialize AV subsystem
    tutk.av_deinitialize(tutk_platform_lib)

    # deinitialize IOTC module
    tutk.iotc_deinitialize(tutk_platform_lib)


def start_video_streaming(tutk_platform_lib, av_chan_id):
    codec = None
    i = 0
    buffer = []
    buffer_size = 210
    while True:
        errno, frame_data, frame_info, frame_idx = tutk.av_recv_frame_data(
            tutk_platform_lib, av_chan_id
        )
        if errno < 0:
            if errno == tutk.AV_ER_DATA_NOREADY:
                time.sleep(1.0 / 40)
            else:
                print(f"got av error: {errno}")
                i += 1
            continue

        if codec is None:
            if frame_info.codec_id == 78:
                codec_name = "h264"
            elif frame_info.codec_id == 80:
                codec_name = "hevc"
            else:
                codec_name = "h264"
                print(f"Unexpected codec! got {frame_info.codec_id}.")

            # noinspection PyUnresolvedReferences
            codec = av.CodecContext.create(codec_name, "r")

        assert len(frame_data) == frame_info.frame_len, "Unexpected frame size!"
        print(
            f"got av frame {frame_idx:06} ({frame_info.frame_no}) "
            f"codec: {frame_info.codec_id} "
            f"ts: {frame_info.timestamp}.{frame_info.timestamp_ms:06} "
            f"keyframe: {frame_info.is_keyframe} "
            f"frame rate: {frame_info.framerate} "
            f"frame size: {frame_info.frame_size} "
            f"bitrate: {frame_info.bitrate}"
        )

        if frame_info.frame_size == tutk.FRAME_SIZE_360P:
            print("skipping smaller frame at start of stream")
            continue

        buffer.append(frame_info)
        if len(buffer) > buffer_size:
            buffer = buffer[len(buffer) - buffer_size :]

        if len(buffer) > 1:
            buffer_start = (
                buffer[0].timestamp + buffer[0].timestamp_ms / 1_000_000
            )
            buffer_end = (
                buffer[-1].timestamp + buffer[-1].timestamp_ms / 1_000_000
            )
            buffer_duration = buffer_end - buffer_start
            buffer_total_size = sum(
                b.frame_len for b in buffer[:-1]
            )  # skip the last reading
            bytes_per_second = int(buffer_total_size / buffer_duration / 1000)
            frames_per_second = int(len(buffer) / buffer_duration)
        else:
            bytes_per_second = 0
            buffer_duration = 0
            frames_per_second = 0

        packets = codec.parse(frame_data)
        for packet in packets:
            frames = codec.decode(packet)
            for frame in frames:
                img = frame.to_ndarray(format="bgr24")
                text = f"{frame.width}x{frame.height} {bytes_per_second} kB/s {frames_per_second} FPS"
                cv2.putText(
                    img,
                    text,
                    (50, 50),
                    cv2.FONT_HERSHEY_DUPLEX,
                    1,
                    (0, 0, 0),
                    2,
                    cv2.LINE_AA,
                )
                cv2.putText(
                    img,
                    text,
                    (50, 50),
                    cv2.FONT_HERSHEY_DUPLEX,
                    1,
                    (255, 255, 255),
                    1,
                    cv2.LINE_AA,
                )
                cv2.imshow("Video Feed", img)
                cv2.waitKey(1)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    i = 200

        i += 1
