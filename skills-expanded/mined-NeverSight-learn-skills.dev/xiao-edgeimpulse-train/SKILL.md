---
name: xiao-edgeimpulse-train
description: >
  Train and deploy a TinyML model for the XIAO ESP32S3 (Sense) using the Edge
  Impulse REST API only — no edge-impulse-cli needed (its serialport dep fails
  to build on modern Node/Windows). Covers: dataset upload, impulse creation
  (audio MFCC / vision transfer-learning), training jobs, downloading the
  Arduino library, and the on-device fixes required to actually run it on the
  ESP32-S3. Use this skill whenever the user wants to train/retrain a model
  ("재훈련", "edge impulse", "TinyML 훈련", "모델 배포"), upload a dataset to
  Edge Impulse, or gets EI Arduino-library build/runtime errors (mel
  filterbank, objs.a, tensor arena, EI_MAX_OVERFLOW_BUFFER_COUNT).
---

# Edge Impulse training pipeline for XIAO ESP32S3 (REST API, verified)

Everything below was executed and verified end-to-end (2026-07). The
edge-impulse-cli is NOT needed — do not try to install it (its
serialport@8 dependency needs VS C++ build tools on Node 22+).

## Step 0 — API key (ask the user)

Ask the user for an Edge Impulse **admin** API key (`ei_...`), or read it
from the project's `.env` (`EI_API_KEY=...`) if the user points you there.

- The auto-created project key has role "Ingestion & deployment" — it can
  upload data but **cannot** create impulses or start training (symptom:
  `insufficient permissions (valid roles: [admin])`).
- If needed, tell the user: Studio → Dashboard → Keys → Add new API key →
  Role **Admin (full access)** → copy the full key immediately (it is
  truncated in the list afterwards).
- Get the project id: `GET https://studio.edgeimpulse.com/v1/api/projects`
  with header `x-api-key` → `projects[0].id`.
- PowerShell warning: `$pid` is a READ-ONLY reserved variable — use `$proj`.

## Step 1 — upload dataset (ingestion API)

One POST per file; label comes from the `x-label` header:

```powershell
curl.exe -s -X POST -H "x-api-key: $key" -H "x-label: $cls" `
  -F "data=@$($f.FullName)" https://ingestion.edgeimpulse.com/api/training/files
```

WAV: 16 kHz 16-bit mono. Images: jpg/png as-is. After uploading everything,
auto-split train/test: `POST /v1/api/$proj/rebalance`.

One project = one model. To retrain for a different task first wipe:
`POST /v1/api/$proj/raw-data/delete-all` (archive any deployed lib zip first).

## Step 2 — create the impulse

`POST https://studio.edgeimpulse.com/v1/api/$proj/impulse` (POST, not PUT).

Audio (keyword spotting) — `implementationVersion: 4` on the MFCC block is
REQUIRED; without it you get v1 and feature generation fails with
"mel filterbank contains all zeros":

```json
{"inputBlocks":[{"id":1,"type":"time-series","name":"Time series data","title":"Time series data","windowSizeMs":1000,"windowIncreaseMs":500,"frequencyHz":16000,"padZeros":true}],
 "dspBlocks":[{"id":2,"type":"mfcc","name":"MFCC","axes":["audio"],"title":"MFCC","implementationVersion":4}],
 "learnBlocks":[{"id":3,"type":"keras","name":"Classifier","dsp":[2],"title":"Classification"}]}
```

Vision (image classification, MobileNet transfer learning):

```json
{"inputBlocks":[{"id":1,"type":"image","name":"Images","title":"Image data","imageWidth":96,"imageHeight":96,"resizeMode":"squash"}],
 "dspBlocks":[{"id":2,"type":"image","name":"Image","axes":["image"],"title":"Image","implementationVersion":1}],
 "learnBlocks":[{"id":3,"type":"keras-transfer-image","name":"Transfer learning","dsp":[2],"title":"Transfer learning (Images)"}]}
```

## Step 3 — generate features, then train

```powershell
# start: returns a job id
POST /v1/api/$proj/jobs/generate-features   body: {"dspId":2,"calculateFeatureImportance":false}
# poll until finished (10-15 s interval):
GET  /v1/api/$proj/jobs/$jobId/status   -> job.finished / job.finishedSuccessful
# on failure read newest-first logs:
GET  /v1/api/$proj/jobs/$jobId/stdout   -> stdout[0..] .data

# train (after features succeed):
POST /v1/api/$proj/jobs/train/keras/3
#   audio body:  {"trainingCycles":100,"learningRate":0.005}
#   vision body: {"trainingCycles":20,"learningRate":0.0005}
```

Accuracy is in the train job stdout (`val_accuracy` lines). Keep each poll
loop's total wait under your tool timeout — resume polling in a new call
rather than one giant sleep.

## Step 4 — build + download the Arduino library

```powershell
POST /v1/api/$proj/jobs/build-ondevice-model?type=arduino   body: {"engine":"tflite-eon"}
# poll job, then:
GET /v1/api/$proj/deployment/download?type=arduino   -> save as <name>.zip
```

Install: find the sketchbook with `arduino-cli config get directories.user`,
extract into `<sketchbook>\libraries\<project>_inferencing`. The zip usually
nests one folder — flatten so `src\<project>_inferencing.h` exists.
Archive the zip per task (audio/vision) — swapping tasks overwrites the lib.

## Step 5 — on-device fixes (ESP32-S3, REQUIRED for vision)

1. **`--clean` on the first compile after swapping the library.** The
   arduino-cli cache keeps stale objects for the same library name/version —
   symptoms: `objs.a ... is not an object` link errors, or edits that appear
   to change nothing (identical byte sizes).
2. **Tensor arena overflow crash** (`Failed to allocate persistent buffer ...
   EI_MAX_OVERFLOW_BUFFER_COUNT` + Guru Meditation on boot): edit
   `src\edge-impulse-sdk\porting\ei_classifier_porting.h` — near the end,
   `#if defined(CONFIG_IDF_TARGET_ESP32S3)` hard-defines
   `EI_MAX_OVERFLOW_BUFFER_COUNT 30` with no #ifndef guard, so -D flags and
   model-file defaults are ALL ignored. Change `30` to `2048`, then `--clean`.
3. **Put the arena in PSRAM** — add to the sketch (the SDK's allocators are
   weak symbols) and build with `--board-options PSRAM=opi`:

```cpp
#include "esp_heap_caps.h"
void *ei_malloc(size_t size) {
  void *p = heap_caps_aligned_alloc(16, size, MALLOC_CAP_SPIRAM);
  if (!p) p = heap_caps_aligned_alloc(16, size, MALLOC_CAP_DEFAULT);
  return p;
}
void *ei_calloc(size_t n, size_t s) { void *p = ei_malloc(n*s); if (p) memset(p,0,n*s); return p; }
void ei_free(void *ptr) { heap_caps_free(ptr); }
```

## Step 6 — inference sketch integration

- Feed data via the static-buffer pattern (`signal.get_data`), NOT the EI
  example's `<I2S.h>` code (breaks on esp32 core 3.x — use `ESP_I2S.h`).
- Vision feature packing: one float per pixel = `(r<<16)|(g<<8)|b`.
- Camera on XIAO Sense renders rotated 90°: rotate CW while downscaling
  (`sx = y*W/H; sy = H-1-(x*H/W)`) or accuracy collapses. Verify orientation
  empirically by classifying one frame 3 ways (none/cw/ccw) and comparing.
- Audio level gap: mic audio is far quieter than full-scale training WAVs —
  best fix is collecting training data through the device mic itself.
- Camera AWB needs warmup: grab and discard ~8 frames before the real capture.
