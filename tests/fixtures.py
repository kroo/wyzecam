import pytest
import wyzecam.iotc
from wyzecam.api_models import WyzeAccount, WyzeCamera
from wyzecam.mock.mock_tutk_library import MockTutkLibrary  # type: ignore


@pytest.fixture
def tutk_platform_lib():
    return MockTutkLibrary()


@pytest.fixture
def iotc(tutk_platform_lib):
    return wyzecam.iotc.WyzeIOTC(tutk_platform_lib)


@pytest.fixture
def account():
    return WyzeAccount(
        phone_id="phone_id",
        logo="logo",
        nickname="nickname",
        email="email",
        user_code="user_code",
        user_center_id="user_center_id",
        open_user_id="open_user_id",
    )


@pytest.fixture
def camera():
    return WyzeCamera(
        p2p_id="p2p_id",
        p2p_type=3,
        ip="1.2.3.4",
        enr="AbCdEfGh/JkLmN0p",
        mac="2CAABBCCDDEE",
        product_model="product_model",
        camera_info=None,
        nickname="nickname",
        timezone_name="timezone_name",
    )
