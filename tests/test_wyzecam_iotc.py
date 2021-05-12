import wyzecam.iotc
from wyzecam.mock.mock_tutk_library import MockTutkLibrary  # type: ignore


def test_get_version(iotc: wyzecam.iotc.WyzeIOTC) -> None:
    with iotc:
        assert iotc.version == 0xDEADBEEF
