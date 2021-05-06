import os

try:
    import cv2
except ImportError:
    cv2 = None
from wyzecam import get_camera_list, get_user_info, login
from wyzecam.iotc import WyzeIOTC


def main():
    assert cv2, "missing opencv-python, required for this example"

    assert os.environ["WYZE_EMAIL"], "missing WYZE_EMAIL"
    assert os.environ["WYZE_PASSWORD"], "missing WYZE_PASSWORD"
    auth_info = login(os.environ["WYZE_EMAIL"], os.environ["WYZE_PASSWORD"])
    account = get_user_info(auth_info)
    cameras = get_camera_list(auth_info)

    cam = [camera for camera in cameras if camera.nickname == "Back Yard Cam"][
        0
    ]

    with WyzeIOTC() as wyze_iotc:
        with wyze_iotc.connect_and_auth(account, cam) as sess:
            session_info = sess.session_check()
            print(f"{sess.state}, session_info = {session_info}")
            for (
                frame,
                frame_info,
                video_stats,
            ) in sess.recv_video_frame_ndarray_with_stats():
                print(
                    f"got av frame {frame_info.frame_no} "
                    f"codec: {frame_info.codec_id} "
                    f"ts: {frame_info.timestamp}.{frame_info.timestamp_ms:06} "
                    f"keyframe: {frame_info.is_keyframe} "
                    f"frame rate: {frame_info.framerate} "
                    f"frame size: {frame_info.frame_size} "
                    f"bitrate: {frame_info.bitrate}"
                )
                cv2.imshow("Video Feed", frame)
                cv2.waitKey(1)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break


if __name__ == "__main__":
    main()
