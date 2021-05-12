import pytest
from wyzecam.iotc import WyzeIOTCSessionState
from wyzecam.mock.mock_tutk_library import MockTutkLibrary  # type: ignore
from wyzecam.tutk import tutk


@pytest.mark.usefixtures("iotc", "account", "camera")
def test_connect_and_auth(iotc, account, camera):
    with iotc.connect_and_auth(account, camera) as session:
        assert session.state == WyzeIOTCSessionState.AUTHENTICATION_SUCCEEDED
    assert session.tutk_platform_lib.session_closed_called
    assert session.tutk_platform_lib.client_stop_called


@pytest.mark.usefixtures("iotc", "account", "camera")
def test_connect_failed(iotc, account, camera):
    iotc.tutk_platform_lib.IOTC_Connect_ByUID_Parallel.set_retval(
        -42
    )  # IOTC_ER_FAIL_SETUP_RELAY

    session = iotc.connect_and_auth(account, camera)
    with pytest.raises(tutk.TutkError):
        with session:
            assert (
                session.state == WyzeIOTCSessionState.AUTHENTICATION_SUCCEEDED
            )

    assert session.state == WyzeIOTCSessionState.CONNECTING_FAILED
    assert session.tutk_platform_lib.session_closed_called
    assert not session.tutk_platform_lib.client_stop_called


@pytest.mark.usefixtures("iotc", "account", "camera")
def test_auth_failed(iotc, account, camera):
    session = iotc.connect_and_auth(account, camera)
    with pytest.raises(tutk.TutkError):
        with session:
            pass  # exception raised before this point

    assert session.state == WyzeIOTCSessionState.CONNECTING_FAILED
    assert session.tutk_platform_lib.session_closed_called
    assert not session.tutk_platform_lib.client_stop_called
