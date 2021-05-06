# wyzecam

<div align="center">

[![Build status](https://github.com/kroo/wyzecam/workflows/build/badge.svg?branch=master&event=push)](https://github.com/kroo/wyzecam/actions?query=workflow%3Abuild)
[![Python Version](https://img.shields.io/pypi/pyversions/wyzecam.svg)](https://pypi.org/project/wyzecam/)
[![Dependencies Status](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)](https://github.com/kroo/wyzecam/pulls?utf8=%E2%9C%93&q=is%3Apr%20author%3Aapp%2Fdependabot)

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Security: bandit](https://img.shields.io/badge/security-bandit-green.svg)](https://github.com/PyCQA/bandit)
[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/kroo/wyzecam/blob/master/.pre-commit-config.yaml)
[![Semantic Versions](https://img.shields.io/badge/%F0%9F%9A%80-semantic%20versions-informational.svg)](https://github.com/kroo/wyzecam/releases)
[![License](https://img.shields.io/github/license/kroo/wyzecam)](https://github.com/kroo/wyzecam/blob/master/LICENSE)

</div>

Wyzecam is a library for streaming audio and video from your wyze cameras using the wyze native firmware.

That means no need to flash rtsp-specific firmware, and full support for the v3 hardware!

## Basic Usage

Streaming video in 11 lines of code!

```python
import os

import cv2
import wyzecam

auth_info = wyzecam.login(os.environ["WYZE_EMAIL"], os.environ["WYZE_PASSWORD"])
account = wyzecam.get_user_info(auth_info)
camera = wyzecam.get_camera_list(auth_info)[0]

with wyzecam.WyzeIOTC() as wyze_iotc:
  with wyze_iotc.connect_and_auth(account, camera) as sess:
    for (frame, frame_info) in sess.recv_video_frame_ndarray():
      cv2.imshow("Video Feed", frame)
      cv2.waitKey(1)
```

## Features

- Send local commands (via `WyzeIOTC` class)
- Support for all wyze camera types (including v3 cameras!)
- Uses the [tutk](https://github.com/nblavoie/wyzecam-api/tree/master/wyzecam-sdk) protocol for communicating over the
  local network. 
- Optional support for opencv and libav for easy decoding of the video feed!


## Installation

```bash
pip install -U wyzecam
```

You will then need a copy of the shared library `libIOTCAPIs_ALL`. You will need
to [download this SDK](https://github.com/nblavoie/wyzecam-api/tree/master/wyzecam-sdk), unzip it, then convert the
appropriate copy of the library to a shared library, and copy the resultant `.so` or `.dylib` file to somewhere
convenient.

### On Mac:

```shell
unzip TUTK_IOTC_Platform_14W42P1.zip
cd Lib/MAC/
g++ -fpic -shared -Wl,-all_load libIOTCAPIs_ALL.a -o libIOTCAPIs_ALL.dylib
cp libIOTCAPIs_ALL.dylib /usr/local/lib/
```

### On Linux:

```bash
unzip TUTK_IOTC_Platform_14W42P1.zip
cd Lib/Linux/x64/
g++ -fpic -shared -Wl,-whole-archive libAVAPIs.a libIOTCAPIs.a -o libIOTCAPIs_ALL.so
cp libIOTCAPIs_ALL.so /usr/local/lib/
```

Note: you will need to pick the appropriate architecture.

## 🛡 License

[![License](https://img.shields.io/github/license/kroo/wyzecam)](https://github.com/kroo/wyzecam/blob/master/LICENSE)

This project is licensed under the terms of the `MIT` license.
See [LICENSE](https://github.com/kroo/wyzecam/blob/master/LICENSE) for more details.

## 📃 Citation

```
@misc{wyzecam,
  author = {kroo},
  title = {Python package for communicating with wyze cameras over the local network},
  year = {2021},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/kroo/wyzecam}}
}
```

## Credits

Special thanks to the work by folks at [nblavoie/wyzecam-api](https://github.com/nblavoie/wyzecam-api), without which
this project would have been much harder.
