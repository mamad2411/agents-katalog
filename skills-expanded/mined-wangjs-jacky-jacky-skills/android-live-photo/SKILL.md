---
name: android-live-photo
description: "Convert a user-provided MP4 video into a verified standard Android Motion Photo (often called Android Live Photo): a JPEG cover with the original MP4 embedded and Google Motion Photo XMP metadata. Use when users ask to turn a video into a Live Photo, dynamic photo, Motion Photo, or social-media-compatible Android live image."
---

# Android Live Photo

Create an Android/Google Motion Photo from a supplied MP4. The output is one untouched `.jpg` binary containing a JPEG cover, standard XMP metadata, and the original MP4 bytes.

## Workflow

1. Use the exact video attachment path supplied by the user. Do not scan attachment folders.
2. Run `ffprobe` on the MP4. Stop and report the issue if it has no readable video stream or duration.
3. Run the bundled script, defaulting the cover to the midpoint:

```sh
node scripts/convert_motion_photo.mjs \
  --input /absolute/input.mp4 \
  --output /absolute/output_MP.jpg
```

Use `--cover-at <seconds>` only when the user specifies a preferred cover moment.

4. Trust completion only after the script reports `validation: passed`. It verifies JPEG SOI, Motion Photo XMP, declared embedded-video length, MP4 signature, and byte-for-byte equality of the embedded MP4 with the source.
5. State the output path and compatibility boundary: the result has worked with social platforms that recognize standard Android Motion Photos; Honor Gallery may not register imported generic Motion Photos as native Live Photos.

## Delivery

Do not send the dynamic JPEG through an image renderer or editor: recompression strips the embedded MP4 and turns it into a static image. Preserve the exact generated binary. If the environment supports general file attachment, send it unchanged; otherwise provide the absolute output path or package it in an untouched archive using the available file-delivery mechanism.

## Requirements

Require Node.js 20+, `ffmpeg`, and `ffprobe` on `PATH`. The script supports MP4 input only and does not alter source media.
