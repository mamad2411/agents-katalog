---
name: vision-camera-v5
description: Use react-native-vision-camera v5 (Nitro Modules rewrite) — CameraSession, CameraOutputs (Photo/Video/Frame/Depth/Preview/Object), Constraints API, Multi-Cam, Skia, Barcode Scanner, Location, Resizer
metadata:
  author: Paulo R. Lima
  version: "2026-05-21.1"
  source: https://github.com/mrousavy/react-native-vision-camera @ 980cbb33 + https://visioncamera.margelo.com/llms-full.txt
  license: MIT
  homepage: https://github.com/paulorlima9/vision-camera-v5-skill
  keywords:
    - react-native
    - vision-camera
    - nitro-modules
    - camera
    - frame-processor
    - barcode-scanner
    - skia
    - ml
    - photography
    - video-recording
---

> Based on `react-native-vision-camera` v5 (Nitro Modules rewrite).
> The v5 API is a full break from v3/v4 — there is no `<Camera photo={true} video={true} />`, no `useFrameProcessor`, no `useCameraFormat`.
> Instead the model is: **inputs → connections → outputs**, with constraints negotiating safe combinations.

## Mental model

VisionCamera v5 is built on three primitives:

1. **`CameraDevice`** (input) — a physical or virtual camera lens (`'back'`, `'front'`, `'external'`, or virtual `'triple'`, `'dual'`, etc).
2. **`CameraOutput`** — one of `CameraPhotoOutput`, `CameraVideoOutput`, `CameraFrameOutput`, `CameraDepthFrameOutput`, `CameraPreviewOutput`, `CameraObjectOutput` (iOS), or library-provided outputs (e.g. the Barcode Scanner output).
3. **`CameraSession`** — connects an input to many outputs, negotiates `Constraint`s (`fps`, `videoDynamicRange`, `photoHDR`, `resolutionBias`, `videoStabilizationMode`, ...) and returns a `CameraController` for runtime controls (zoom, exposure, focus, torch).

There are three API styles, all wrapping the same primitives:

| Style | Use when |
|---|---|
| `<Camera />` view | Default. Renders a preview + manages session lifecycle from `isActive`. |
| `useCamera({...})` hook | Need imperative `CameraController` but still want `<NativePreviewView />`. |
| `CameraSession` imperative | Multi-cam, custom preview layout, low-level lifecycle. |

> See [api-style](references/api-style.md) for a side-by-side of the three styles.

## Core References

| Topic | Description | Reference |
|---|---|---|
| Getting started | Install, permissions, expo vs bare, first render | [getting-started](references/getting-started.md) |
| API style | `<Camera />` vs `useCamera()` vs `CameraSession` | [api-style](references/api-style.md) |
| Camera Session | Lifecycle, configure, interruptions, multi-cam | [camera-session](references/camera-session.md) |
| Camera Devices | `getCameraDevice`, virtual devices, capabilities | [camera-devices](references/camera-devices.md) |
| Camera Controller | Zoom, exposure, focus, torch, white-balance | [camera-controller](references/camera-controller.md) |
| Camera Factory | Global `VisionCamera` singleton + `CameraDeviceFactory` | [camera-factory](references/camera-factory.md) |
| Camera Outputs (overview) | Per-output basics, mirror modes, resolution negotiation | [camera-outputs](references/camera-outputs.md) |

## Views

| Topic | Description | Reference |
|---|---|---|
| `<Camera />` | Convenience view with everything wired up | [camera-view](references/camera-view.md) |
| `<NativePreviewView />` | Lower-level preview view with layout flexibility | [nativepreview-view](references/nativepreview-view.md) |
| `<SkiaCamera />` | Skia-rendering camera for custom GPU drawing | [skiacamera-view](references/skiacamera-view.md) |
| `<NativeFrameRendererView />` | Render `Frame`s without Skia | [frame-renderer-view](references/frame-renderer-view.md) |
| `<CodeScanner />` | Drop-in barcode scanner from `-barcode-scanner` | [codescanner-view](references/codescanner-view.md) |

## Outputs

| Topic | Description | Reference |
|---|---|---|
| Preview Output | `<NativePreviewView />` + `CameraPreviewOutput` | [outputs-preview](references/outputs-preview.md) |
| Photo Output | Capture, settings, callbacks, RAW, HDR, preview image | [outputs-photo](references/outputs-photo.md) |
| Photo Output Callbacks | The 4 callbacks fired during capture | [photo-output-callbacks](references/photo-output-callbacks.md) |
| Configuring Photo Quality | `qualityPrioritization`, `quality`, container formats | [photo-quality](references/photo-quality.md) |
| Capturing RAW Photos | DNG / Apple ProRAW dedicated guide | [raw-photos](references/raw-photos.md) |
| Photo HDR (constraints + iOS) | Photo HDR via constraint API | [photo-hdr-raw](references/photo-hdr-raw.md) |
| Video Output | `Recorder`, codecs, persistent recording, max duration | [outputs-video](references/outputs-video.md) |
| The Recorder | Recorder lifecycle, start/pause/resume/stop, single-use rule | [recorder](references/recorder.md) |
| Frame Output | Frame Processors, pixel formats, async runner | [outputs-frame](references/outputs-frame.md) |
| Depth Output | Disparity/depth frames, conversion | [outputs-depth](references/outputs-depth.md) |
| Object Output (iOS) | Native QR/face scanner | [outputs-object](references/outputs-object.md) |

## Capabilities & APIs

| Topic | Description | Reference |
|---|---|---|
| Constraints API | `{ fps }`, `{ photoHDR }`, `{ resolutionBias }`, `{ videoDynamicRange }`, `{ binned }` | [constraints](references/constraints.md) |
| Coordinate systems | View ↔ Camera ↔ Frame conversions | [coordinate-systems](references/coordinate-systems.md) |
| Orientation | `orientationSource`, mirroring, physical buffer rotation | [orientation](references/orientation.md) |
| Orientation Manager | Imperative orientation tracking via `OrientationManager` | [orientation-manager](references/orientation-manager.md) |
| Gesture Controllers | `ZoomGestureController` + `TapToFocusGestureController` | [gesture-controllers](references/gesture-controllers.md) |
| Tap to focus | `focusTo()`, metering modes, scene adaptiveness | [tap-to-focus](references/tap-to-focus.md) |
| Locking AE/AF/AWB | Manual exposure/focus/white-balance, subject-area events | [locking-aeafawb](references/locking-aeafawb.md) |
| Exposure Bias | EV compensation via `setExposureBias()` / `exposure` prop | [exposure-bias](references/exposure-bias.md) |
| Zoom | Virtual device switching, animated zoom | [zoom](references/zoom.md) |
| FPS | Per-device ranges and constraint negotiation | [fps](references/fps.md) |
| Photo HDR | Photo HDR via constraints + Apple ProRAW + HDR Camera Extensions | [photo-hdr-raw](references/photo-hdr-raw.md) |
| Video HDR | HLG/PQ, 10-bit, ExtendedDynamicRange, custom dynamic ranges | [video-hdr](references/video-hdr.md) |
| Video Stabilization | Cinematic / preview-optimized / low-latency modes | [video-stabilization](references/video-stabilization.md) |
| Low Light Boost | `enableLowLightBoost`, `'night'` extension, binned formats | [low-light-boost](references/low-light-boost.md) |
| Multi-Camera | Front + back simultaneously, supported combinations | [multi-camera](references/multi-camera.md) |
| Camera Extensions (Android) | Vendor `'hdr'`, `'night'`, `'bokeh'`, `'face-retouch'` | [camera-extensions](references/camera-extensions.md) |
| Output Synchronizer (iOS) | Sync `CameraFrameOutput` + `CameraDepthFrameOutput` per timestamp | [output-synchronizer](references/output-synchronizer.md) |
| Camera Calibration Data | Intrinsic/extrinsic matrices for 3D projection (iOS) | [camera-calibration-data](references/camera-calibration-data.md) |
| Pixel Formats Map | Pixel format catalog + platform-native mapping | [pixel-formats-map](references/pixel-formats-map.md) |
| Lifecycle | `isActive`, foregrounding, mounted vs configured | [lifecycle](references/lifecycle.md) |
| Performance | Picking devices, pixel formats, FPS, deferred start | [performance](references/performance.md) |
| Snapshot capture | Fast non-photo capture via Preview View (Android) | [snapshot-capture](references/snapshot-capture.md) |

## Frame / Depth / Buffer types

| Topic | Description | Reference |
|---|---|---|
| A Frame | `Frame` type — properties, methods, dispose | [a-frame](references/a-frame.md) |
| A Photo | `Photo` type — toImage, save, getFileData, dispose | [a-photo](references/a-photo.md) |
| A Depth Frame | `Depth` type — distance/disparity formats, conversion | [a-depth-frame](references/a-depth-frame.md) |
| A Barcode | `Barcode` type — format, valueType, rawBytes, displayValue | [a-barcode](references/a-barcode.md) |
| A ScannedObject | `ScannedObject` + `ScannedCode` + `ScannedFace` (iOS Object Output) | [a-scannedobject](references/a-scannedobject.md) |
| NativeBuffer | Cross-library buffer pointer for Skia + native interop | [a-frames-nativebuffer](references/a-frames-nativebuffer.md) |
| Frame Converter | `HybridFrameConverter` — Frame/Depth → Image | [frame-converter](references/frame-converter.md) |

## Ecosystem packages

| Topic | Description | Reference |
|---|---|---|
| Skia integration | `<SkiaCamera />`, custom GPU rendering | [skia-integration](references/skia-integration.md) |
| Barcode Scanner | MLKit-based `<CodeScanner />`, `BarcodeScanner`, output | [barcode-scanner](references/barcode-scanner.md) |
| Barcode vs Object Output | When to use which scanner | [barcode-scanner-vs-object-output](references/barcode-scanner-vs-object-output.md) |
| Location | EXIF/MOV location tagging | [location](references/location.md) |
| Resizer | GPU resize + RGB/YUV conversion for ML | [resizer](references/resizer.md) |
| Worklets / Async | `react-native-vision-camera-worklets`, `AsyncRunner` | [worklets-async](references/worklets-async.md) |
| Async Frame Processing | Patterns for off-thread heavy work | [async-frame-processing](references/async-frame-processing.md) |
| Native plugins | Building Frame Processor plugins with Nitro | [native-plugins](references/native-plugins.md) |
| Custom native CameraOutput | Implementing a custom `CameraOutput` from scratch | [custom-native-camera-outputs](references/custom-native-camera-outputs.md) |
| Native Threads | `NativeThread`, `NativeThreadFactory` (advanced) | [native-threads](references/native-threads.md) |

## Constants

| Topic | Description | Reference |
|---|---|---|
| `CommonResolutions` | Pre-defined resolution constants for 16:9 / 4:3 | [common-resolutions](references/common-resolutions.md) |
| `CommonDynamicRanges` | Pre-defined `ANY_SDR` / `ANY_HDR` constants | [common-dynamic-ranges](references/common-dynamic-ranges.md) |

## Migration

| Topic | Description | Reference |
|---|---|---|
| Migration from v3/v4 | What changed: outputs, Nitro, no `format`, no `useFrameProcessor` | [migration-from-v3](references/migration-from-v3.md) |

## Key rules for agents (read this first)

When generating v5 code, follow these invariants:

1. **Never use v3/v4 props.** `photo={true}` / `video={true}` / `frameProcessor={...}` / `format={...}` / `fps={...}` props **do not exist** on `<Camera />`. Use outputs and `constraints={...}` instead.
2. **Pixel formats moved to outputs.** `pixelFormat` is on `useFrameOutput({...})`, not on `<Camera />`.
3. **Photos return a `Photo` instance, not a `PhotoFile`.** Always call `photo.dispose()` after you're done. Use `await photo.toImageAsync()` to render via `react-native-nitro-image`, or `await photo.saveToTemporaryFileAsync()` (path is filesystem path — prepend `file://` only at consumer call sites).
4. **Video recording uses a `Recorder`.** `videoOutput.createRecorder({...})` → `recorder.startRecording(onFinished, onError, ...)` → `recorder.stopRecording()`. The `Recorder` is **single-use** — create a new one per recording.
5. **Frame Processors are `useFrameOutput({...}).onFrame(frame)` worklets.** They require `react-native-vision-camera-worklets`. Always `frame.dispose()` in `finally`.
6. **Constraints describe intent, not absolutes.** Pass `[{ fps: 60 }, { resolutionBias: photoOutput }]` — the order is priority. The session always starts; values get clamped to what the device supports.
7. **Orientation is metadata, not a physical rotation.** Frame consumers must handle `frame.orientation` / `frame.isMirrored` unless you opt in to `enablePhysicalBufferRotation: true`.
8. **`takeSnapshot()` is Android-only.** It snapshots the Preview View. iOS doesn't expose this (use `capturePhoto` with `qualityPrioritization: 'speed'` instead).
9. **`<CodeScanner />` and `useBarcodeScanner` need `react-native-vision-camera-barcode-scanner`.** It is **not** in core. Same for `-skia`, `-worklets`, `-resizer`, `-location`.
10. **`Recorder.filePath` is a filesystem path, not a `file://` URL.** Same for `photo.saveToTemporaryFileAsync()`. Add the `file://` prefix only where required by another library.
11. **Camera Extensions are Android-only**, do NOT support Video HDR, RAW capture, or (some of them) Frame Output. See [camera-extensions](references/camera-extensions.md).
12. **Multi-cam needs `createCameraSession(true)` AND `VisionCamera.supportsMultiCamSessions === true`.** Combinations are listed on `deviceFactory.supportedMultiCamDeviceCombinations` (a 2D `CameraDevice[][]`).
13. **`Barcode` (MLKit) coordinates are in Frame coords; `ScannedObject` (iOS native) coordinates are in Camera coords.** They're different — see [coordinate-systems](references/coordinate-systems.md).
14. **`HybridObject.dispose()` is mandatory** for `Photo`, `Frame`, `Depth`, `NativeBuffer`, `GPUFrame`, `Recorder` (implicit), and any output. Forgetting it stalls the pipeline.
15. **Apple ProRAW** is automatically promoted when DNG is supported on iOS — you don't opt in.

## Minimal working example

```tsx
import { StyleSheet } from 'react-native'
import { Camera, useCameraPermission, usePhotoOutput } from 'react-native-vision-camera'
import { NitroImage } from 'react-native-nitro-image'
import { useEffect, useRef, useState } from 'react'

export default function App() {
  const { hasPermission, requestPermission } = useCameraPermission()
  useEffect(() => { if (!hasPermission) requestPermission() }, [hasPermission, requestPermission])

  const photoOutput = usePhotoOutput({ qualityPrioritization: 'balanced' })
  const [image, setImage] = useState()

  const onCapture = async () => {
    const photo = await photoOutput.capturePhoto({ flashMode: 'off' }, {})
    setImage(await photo.toImageAsync())
    photo.dispose()
  }

  if (image != null) return <NitroImage style={StyleSheet.absoluteFill} image={image} />

  return (
    <Camera
      style={StyleSheet.absoluteFill}
      isActive={hasPermission}
      device="back"
      outputs={[photoOutput]}
      enableNativeZoomGesture
    />
  )
}
```
