# WyzeCam Documentation

## Introduction

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
- Support for all wyze camera types (including wyzecam v3!)
- Uses the [tutk](https://github.com/nblavoie/wyzecam-api/tree/master/wyzecam-sdk) protocol for communicating over the
  local network.
- Optional support for opencv and libav for easy decoding of the video feed!

## Requirements

- Mac or Linux (Windows untested)
- A copy of the TUTK C library (see [installation](/installation/) for more details here)

## Installation

See [installation](/installation/) for detailed instructions.
