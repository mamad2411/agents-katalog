---
name: voyager-add-model
description: Add a custom model to the Voyager SDK model zoo for Axelera AI hardware. Use when the user wants to integrate a new PyTorch, ONNX, timm, or Ultralytics model.
argument-hint: "<model name or path>"
allowed-tools: Read, Bash, Glob, Grep, Edit, Write, mcp__voyager__*
---

# Add Custom Model

Add a custom model to the Voyager SDK model zoo for Axelera AI hardware

## Instructions

Add the specified model: **$ARGUMENTS**

### Step 0: Data Source & Environment Selection

{{INCLUDE common/voyager-sdk-setup.md}}

### Step 0.5: Axelera Voyager Project & Task Integration

{{INCLUDE common/voyager-task-integration.md}}

### Step 1: Model Source Identification

Determine model source format:

- **PyTorch**: `.pt`, `.pth` files or torchvision/timm model name
- **ONNX**: `.onnx` file
- **TensorFlow**: Convert to ONNX first
- **Custom**: Define custom model class

### Step 2: Model Requirements Analysis

Gather model information:

- Input shape (batch, channels, height, width)
- Input format (RGB/BGR, NCHW/NHWC)
- Normalization parameters (mean, std)
- Output format and shape
- Model task (detection, classification, etc.)

### Step 3: SDK-Native YAML Integration

Do not author a freehand YAML schema. Start from the nearest existing SDK
YAML under `ax_models/zoo/`, `ax_models/reference/`, `pipeline-template/`,
or `docs/tutorials/custom-weights.md`, then change only fields backed by the
model metadata and the Grounding Ledger.

Required SDK YAML fields normally include:

- `axelera-model-format`, `name`, `description`
- `pipeline` tasks with SDK operators such as `letterbox`, `torch-totensor`,
  and `decodeyolo` only when verified in the source YAML or
  `docs/reference/pipeline/yaml-operators.md`
- `models` entries with SDK classes such as `AxONNXModel`,
  `AxTorchvisionResNet`, or a `types.Model`/`TorchModel` subclass
- `class_path`, `weight_path`, optional `weight_url` and `weight_md5`
- `task_category`, `input_tensor_layout`, `input_tensor_shape`,
  `input_color_format`, `dataset`
- `datasets` entries using SDK data adapters such as `ObjDataAdapter`,
  `TorchvisionDataAdapter`, `KptDataAdapter`, or `SegDataAdapter`

For ONNX models, prefer `class: AxONNXModel` and
`class_path: $AXELERA_FRAMEWORK/ax_models/base_onnx.py` unless a closer
model-zoo YAML proves a different class is required. For Ultralytics YOLO,
copy an existing YOLO model-zoo YAML and update `weight_path`, `num_classes`,
`dataset`, and decoder parameters only when the source model metadata proves
those values. For torchvision/timm-style classifiers, copy a torchvision
classifier YAML and preserve its `pipeline-template/torch-imagenet.yaml`
pattern unless SDK evidence supports another template.

### Step 4: Custom Model Class

For models requiring custom code:

```python
# ax_models/torch/<model_name>.py

import torch
import torch.nn as nn

class CustomModel(nn.Module):
    def __init__(self, num_classes=1000):
        super().__init__()
        # Define model architecture
        self.features = nn.Sequential(...)
        self.classifier = nn.Linear(512, num_classes)

    def forward(self, x):
        x = self.features(x)
        x = self.classifier(x)
        return x

    @classmethod
    def from_pretrained(cls, weights_path):
        model = cls()
        state_dict = torch.load(weights_path, map_location='cpu')
        model.load_state_dict(state_dict)
        return model
```

### Step 5: Custom Decoder

If model postprocessing is not covered by an existing SDK decoder, implement
an `AxOperator` pattern from `ax_models/tutorials/general/tutorials.md` and
register it in the YAML `operators` block with `class` and `class_path`.
Use methods such as `exec_torch` and `build_gst` only as documented by the
SDK. Do not invent `Detection`, `BBox`, or `CustomDecoder` APIs.

### Step 6: Custom Dataset/Calibration

Use SDK `types.DataAdapter` or a built-in adapter from
`docs/tutorials/custom-weights.md` / `docs/reference/models/adapters.md`.
Custom adapters must provide the SDK-documented data adapter methods, such as
calibration loader/reformat hooks, and be referenced from the YAML
`datasets` section. Do not invent a `CalibrationDataset` base class unless
local SDK evidence shows it exists in this SDK version.

### Step 7: Model Validation

Before adding to zoo, validate:

```bash
# Test deployment or prebuilt retrieval only on execute_on_device hosts
./deploy.py <model-name> --mode QUANTIZE

# Test bounded inference and capture logs/artifacts
./inference.py <model-name> <test-source> --display none --frames 20 --pipe gst --metis auto

# Optional accuracy check when a dataset adapter is verified
./inference.py <model-name> dataset --display none --pipe torch-aipu
```

Success requires: zero exit code, a valid YAML parse, deploy/inference logs,
compiled payload under `build/<model-name>/` (`.axnet` or model/kernel
payload), a real output artifact or dataset metric, and a final report that
states whether `.voyager-runtime.json` allowed Metis hardware validation. In
package-only mode, say "not hardware validated" and provide the Linux
validation command instead of claiming integration is complete.

### Step 8: File Locations

- Model YAML: `ax_models/zoo/<category>/<model-name>.yaml`
- Custom model code: `ax_models/torch/<module>.py`
- Custom decoder: `ax_models/decoders/<task>.py`
- Custom dataset: `ax_datasets/<dataset>.py`
- Custom evaluator: `ax_evaluators/<task>.py`

### Step 9: Documentation

After adding model:

- Add entry to model zoo documentation
- Include expected accuracy metrics
- Document any special requirements
- Add example usage in comments
