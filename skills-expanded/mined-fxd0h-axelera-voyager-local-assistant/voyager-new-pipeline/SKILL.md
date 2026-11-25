---
name: voyager-new-pipeline
description: Create a YAML pipeline configuration for Axelera AI hardware using the Voyager SDK. Use when the user wants to design detection, classification, segmentation, pose, cascade, or parallel pipelines and explicitly wants YAML-only design. Do not use to build, run, or validate a runnable pipeline; prefer voyager-launch for end-to-end requests.
argument-hint: "<pipeline type and model>"
allowed-tools: Read, Bash, Glob, Grep, Edit, Write, mcp__voyager__*
---

# Create New AI Pipeline

Create a YAML pipeline configuration for Axelera AI hardware using Voyager SDK

## Use This Skill When / Not When

- Use when: the user explicitly wants a YAML pipeline configuration file
  only (detection, classification, segmentation, pose, cascade, parallel).
- Not when: they want it built, run, or validated -- route to voyager-launch.
- Not when: they want Python application code -- route to voyager-new-app.

## Instructions

Follow these steps to create a new AI pipeline: **$ARGUMENTS**

### Step 0: Data Source & Environment Selection

{{INCLUDE common/voyager-sdk-setup.md}}

### Step 0.5: Axelera Voyager Project & Task Integration

{{INCLUDE common/voyager-task-integration.md}}

{{INCLUDE common/examples-catalog.md}}

### Step 1: Pipeline Requirements Analysis

- Parse the pipeline type from arguments (detection, classification, segmentation, pose, cascade, parallel)
- If no arguments provided, ask user for:
  - Pipeline purpose (object detection, classification, segmentation, pose estimation, etc.)
  - Target model from model zoo or custom model
  - Input source type (camera, video file, image, RTSP stream)
  - Output requirements (display, file, metadata only)

### Step 2: Model Selection

- Examples-first: check `common/examples-catalog.md`. If a shipped example matches
  the request, prefer running it (route complete/runnable requests to `voyager-launch`)
  rather than authoring a new pipeline.
- If the user wants a complete runnable package, validation, browser viewer,
  or output artifact, stop and route to `voyager-launch`.
- Query RAG and search local `ax_models/zoo/`, `ax_models/reference/`,
  `pipeline-template/`, and SDK tutorials for the exact task.
- Treat segmentation, depth, cascade, parallel, and LLM-adjacent requests as
  candidates until an SDK YAML and a Metis validation path are proven.
- Prefer existing model-zoo names and ONNX variants when the SDK lists them.
  Do not invent resolution variants or model names.

### Step 3: Pipeline YAML Structure

Do not author generic YAML. Start by copying the nearest SDK YAML from
`ax_models/zoo/`, `ax_models/reference/`, or `pipeline-template/`, then make
the smallest changes needed for the user's task.

SDK model/pipeline YAML must follow the local SDK shape, typically:

```yaml
axelera-model-format: 1.0.0
name: <verified-name>
description: <verified purpose>
pipeline:
  - <task-name>:
      model_name: <verified-model-name>
      input:
        type: image
      preprocess:
        - <operator-from-sdk-yaml-or-docs>:
      inference:
        handle_all: false
      postprocess:
        - <operator-from-sdk-yaml-or-docs>:
models:
  <verified-model-name>:
    class: <sdk-model-class>
    class_path: <sdk-class-path>
    weight_path: <sdk-or-user-weight-path>
    task_category: <sdk-task-category>
    input_tensor_layout: NCHW
    input_tensor_shape: [1, 3, <height>, <width>]
    dataset: <verified-dataset>
datasets:
  <verified-dataset>:
    class: <sdk-data-adapter>
    class_path: <sdk-data-adapter-path>
```

Verify every operator name against the copied SDK YAML or
`docs/reference/pipeline/yaml-operators.md`. Do not use `AxResize`,
`AxNormalize`, `YoloDecoder`, or top-level `tracker` unless the current SDK
evidence uses those exact names.

### Step 4: Preprocessing Configuration

Based on model requirements, configure:

- Image resizing (letterbox, stretch, crop)
- Color space conversion (RGB, BGR)
- Normalization (mean, std values)
- Data type conversion

Use the exact SDK operator names from the evidence YAML, such as
`letterbox` and `torch-totensor` when copied from a verified model-zoo file.

### Step 5: Postprocessing/Decoder Configuration

Configure appropriate decoder based on model type:

- Detection: YOLO decoder, SSD decoder, RetinaFace decoder
- Classification: Softmax, Top-K
- Segmentation: Argmax, threshold
- Pose: Keypoint decoder

Use the exact SDK postprocess operator from the evidence YAML, such as
`decodeyolo` only when copied from a verified YOLO SDK file. Include the
source YAML path in the final response.

### Step 6: Cascade, Parallel, And Tracker Pipelines

For cascade or parallel graphs, copy an existing SDK reference YAML from
`ax_models/reference/cascade/` or `ax_models/reference/parallel/`. For
tracking, use a tracker network/YAML such as a verified
`yolov5m-v7-coco-tracker` source. Do not invent a top-level `tracker` block
or CLI tracker flag.

### Step 7: Calibration Data Setup

Configure calibration through the SDK model `dataset` and `datasets` entries,
using fields from the copied YAML and SDK data adapter docs. Do not add a
generic top-level `calibration` block unless the current SDK evidence uses it.

### Step 8: Validation and Testing

- Validate YAML syntax and SDK schema using the repo's YAML parser or
  existing SDK command path.
- Check model availability through a matching YAML, deploy/list evidence,
  and compiled payload under `build/<model>/` or successful `axdownloadmodel`.
- Verify preprocessing matches model expectations
- Test pipeline deployment only when `.voyager-runtime.json` reports
  `execute_on_device`:
  ```bash
  ./deploy.py <pipeline-name> --mode QUANTCOMPILE
  ./inference.py <pipeline-name> <test-source> --display none --frames 20 --pipe gst --metis auto
  ```
- In package-only mode, do not claim validation. Provide the Linux Metis
  verification command and list the YAML/source evidence used.

### Step 9: Output File Location

Save the pipeline YAML to appropriate location:

- Simple models: `ax_models/zoo/<category>/<model-name>.yaml`
- Reference pipelines: `ax_models/reference/<type>/<pipeline-name>.yaml`
- Tutorial/custom: `ax_models/tutorials/<project>/<name>.yaml`

### Step 10: Documentation

Add inline comments explaining:

- Pipeline purpose and use case
- Model source and expected accuracy
- Input/output specifications
- Any special requirements or limitations
