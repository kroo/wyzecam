from typing import Any, Dict, List, Optional

import time
import uuid
from hashlib import md5

import requests
from wyzecam.api_models import WyzeAccount, WyzeCamera, WyzeCredential

SV_VALUE = "e1fe392906d54888a9b99b88de4162d7"
SC_VALUE = "9f275790cab94a72bd206c8876429f3c"
WYZE_APP_API_KEY = "WMXHYf79Nr5gIlt3r0r7p9Tcw5bvs6BB4U8O8nGJ"

SCALE_USER_AGENT = "Wyze/2.19.24 (iPhone; iOS 14.4.2; Scale/3.00)"
WYZE_APP_VERSION_NUM = "2.19.24"


def login(
    email: str, password: str, phone_id: Optional[str] = None
) -> WyzeCredential:
    """Authenticate with Wyze

    This method calls out to the `/user/login` endpoint of
    `auth-prod.api.wyze.com` (using https), and retrieves an access token
    necessary to retrieve other information from the wyze server.

    :param email: Email address used to log into wyze account
    :param password: Password used to log into wyze account.  This is used to
                     authenticate with the wyze API server, and return a credential.
    :param phone_id: the ID of the device to emulate when talking to wyze.  This is
                     safe to leave as None (in which case a random phone id will be
                     generated)

    :returns: a [WyzeCredential][wyzecam.api.WyzeCredential] with the access information, suitable
              for passing to [get_user_info()][wyzecam.api.get_user_info], or
              [get_camera_list()][wyzecam.api.get_camera_list].
    """
    if phone_id is None:
        phone_id = str(uuid.uuid4())

    payload = {"email": email, "password": triplemd5(password)}
    resp = requests.post(
        "https://auth-prod.api.wyze.com/user/login",
        json=payload,
        headers=get_headers(phone_id),
    )
    resp.raise_for_status()

    return WyzeCredential.parse_obj(dict(resp.json(), phone_id=phone_id))


def get_user_info(auth_info: WyzeCredential) -> WyzeAccount:
    """Gets Wyze Account Information

    This method calls out to the `/app/user/get_user_info`
    endpoint of `api.wyze.com` (using https), and retrieves the
    account details of the authenticated user.

    :param auth_info: the result of a [`login()`][wyzecam.api.login] call.
    :returns: a [WyzeAccount][wyzecam.api.WyzeAccount] with the user's info, suitable
          for passing to [`WyzeIOTC.connect_and_auth()`][wyzecam.iotc.WyzeIOTC.connect_and_auth].

    """
    payload = _get_payload(auth_info.access_token, auth_info.phone_id)
    ui_headers = get_headers(auth_info.phone_id, SCALE_USER_AGENT)
    resp = requests.post(
        "https://api.wyzecam.com/app/user/get_user_info",
        json=payload,
        headers=ui_headers,
    )
    resp.raise_for_status()

    resp_json = resp.json()
    assert resp_json["code"] == "1", "Call failed"

    return WyzeAccount.parse_obj(
        dict(resp_json["data"], phone_id=auth_info.phone_id)
    )


def get_homepage_object_list(auth_info: WyzeCredential) -> Dict[str, Any]:
    """Gets all homepage objects"""
    payload = _get_payload(auth_info.access_token, auth_info.phone_id)
    ui_headers = get_headers(auth_info.phone_id, SCALE_USER_AGENT)
    resp = requests.post(
        "https://api.wyzecam.com/app/v2/home_page/get_object_list",
        json=payload,
        headers=ui_headers,
    )
    resp.raise_for_status()

    resp_json = resp.json()
    assert resp_json["code"] == "1"

    data = resp_json["data"]  # type: Dict[str, Any]
    return data


def get_camera_list(auth_info: WyzeCredential) -> List[WyzeCamera]:
    data = get_homepage_object_list(auth_info)
    result = []
    for device in data["device_list"]:  # type: Dict[str, Any]
        if device["product_type"] != "Camera":
            continue

        device_params = device.get("device_params", {})
        p2p_id: Optional[str] = device_params.get("p2p_id")
        p2p_type: Optional[int] = device_params.get("p2p_type")
        ip: Optional[str] = device_params.get("ip")
        enr: Optional[str] = device.get("enr")
        mac: Optional[str] = device.get("mac")
        product_model: Optional[str] = device.get("product_model")
        nickname: Optional[str] = device.get("nickname")
        timezone_name: Optional[str] = device.get("timezone_name")

        if not p2p_id:
            continue
        if not p2p_type:
            continue
        if not ip:
            continue
        if not enr:
            continue
        if not mac:
            continue
        if not product_model:
            continue

        result.append(
            WyzeCamera(
                p2p_id=p2p_id,
                p2p_type=p2p_type,
                ip=ip,
                enr=enr,
                mac=mac,
                product_model=product_model,
                nickname=nickname,
                timezone_name=timezone_name,
            )
        )
    return result


def _get_payload(access_token, phone_id):
    payload = {
        "sc": SC_VALUE,
        "sv": SV_VALUE,
        "app_ver": f"com.hualai.WyzeCam___{WYZE_APP_VERSION_NUM}",
        "app_version": f"{WYZE_APP_VERSION_NUM}",
        "app_name": "com.hualai.WyzeCam",
        "phone_system_type": "1",
        "ts": int(time.time() * 1000),
        "access_token": access_token,
        "phone_id": phone_id,
    }
    return payload


def get_headers(phone_id, user_agent="wyze_ios_2.19.24"):
    return {
        "X-API-Key": WYZE_APP_API_KEY,
        "Phone-Id": phone_id,
        "User-Agent": user_agent,
    }


def triplemd5(password):
    """Runs hashlib.md5() algorithm 3 times"""
    encoded = password
    for i in range(3):
        encoded = md5(encoded.encode("ascii")).hexdigest()  # nosec
    return encoded
