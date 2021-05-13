import pytest
import wyzecam
from wyzecam import WyzeAccount, WyzeCamera, WyzeIOTC, WyzeIOTCSessionState


@pytest.mark.usefixtures("iotc", "account", "camera")
def test_connect_and_auth(
    iotc: WyzeIOTC, account: WyzeAccount, camera: WyzeCamera
):
    camera.product_model = "WYZEDB3"
    with iotc.connect_and_auth(account, camera) as session:
        assert session.state == WyzeIOTCSessionState.AUTHENTICATION_SUCCEEDED
    assert session.tutk_platform_lib.session_closed_called
    assert session.tutk_platform_lib.client_stop_called
