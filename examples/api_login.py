import argparse
import json

import wyzecam.api

parser = argparse.ArgumentParser()
parser.add_argument("phone_id")
parser.add_argument("username")
parser.add_argument("password")


def main():
    args = parser.parse_args()

    login_resp = wyzecam.api.login(
        args.username, args.password, phone_id=args.phone_id
    )

    with open("auth_credentials.json", "w") as f:
        f.write(json.dumps(login_resp.json(), indent=2))
