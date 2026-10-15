---
name: python-ai-intel-openvino
description: "OpenVINO 2026.x: inference runtime universal para CPU, GPU y NPU Intel. Cubre ov.Core, IR conversion (ov.convert_model), pre/post-processing, quantization con NNCF, heterogeneous execution, model caching, y benchmark_app. Actívala para inference, conversión de modelos, optimización, o deployment OpenVINO."
disable-model-invocation: true
---

# OpenVINO 2026.x — Inference Guide

OpenVINO es el runtime de inference por defecto para hardware Intel. Un mismo modelo IR corre en CPU, GPU y NPU sin cambios de código.

---

## Arquitectura de OpenVINO

```
ov.Core()            ← Coordinador central, detecta dispositivos
  ├── ov.CompiledModel   ← Modelo compilado para un dispositivo
  │     └── ov.InferRequest ← Inference individual
  ├── ov.convert_model() ← PyTorch/ONNX/TF → IR
  └── ov.PrePostProcessor ← Pre/post integrados en el grafo
```

---

## Setup

```bash
uv add openvino  # 2026.2+
```

---

## `ov.Core()` — El entry point

```python
import openvino as ov

core = ov.Core()

# ─── Dispositivos disponibles ───
devices = core.available_devices  # ["CPU", "GPU", "NPU"]

for device in devices:
    name = core.get_property(device, "FULL_DEVICE_NAME")
    print(f"{device}: {name}")

# ─── Versión ───
print(core.get_versions("CPU"))  # → {"CPU": "2026.2.0-..."}

# ─── Propiedades del dispositivo ───
cpu_threads = core.get_property("CPU", "INFERENCE_NUM_THREADS")
gpu_memory  = core.get_property("GPU", "GPU_MEMORY_STATISTICS")
```

### Propiedades clave por dispositivo

| Propiedad | Dispositivo | Descripción |
|-----------|:----------:|-------------|
| `FULL_DEVICE_NAME` | Todos | Nombre completo del hardware |
| `OPTIMIZATION_CAPABILITIES` | Todos | INT8, FP16, BIN soportados |
| `NUM_STREAMS` | CPU, GPU | Paralelismo de streams |
| `INFERENCE_NUM_THREADS` | CPU | Threads para inference |
| `GPU_MEMORY_STATISTICS` | GPU | Uso de VRAM |
| `PERFORMANCE_HINT` | Todos | `LATENCY` o `THROUGHPUT` |
| `CACHE_DIR` | Todos | Directorio de cache de compilación |

---

## Carga y compilación de modelos

```python
import openvino as ov

core = ov.Core()

# ─── Cargar modelo IR ───
model = core.read_model("model.xml")  # .bin debe estar al lado

# ─── Inspeccionar inputs/outputs ───
for i in model.inputs:
    print(f"Input:  {i.name}, shape={i.partial_shape}, dtype={i.element_type}")
for o in model.outputs:
    print(f"Output: {o.name}, shape={o.partial_shape}, dtype={o.element_type}")

# ─── Compilar con performance hints ───
compiled = core.compile_model(
    model=model,
    device="CPU",
    config={
        "PERFORMANCE_HINT": "LATENCY",      # o "THROUGHPUT"
        "NUM_STREAMS": "AUTO",
        "INFERENCE_NUM_THREADS": 8,
    },
)

# ─── GPU ───
compiled_gpu = core.compile_model(
    model=model,
    device="GPU",
    config={"PERFORMANCE_HINT": "THROUGHPUT"},
)

# ─── NPU ───
compiled_npu = core.compile_model(
    model=model,
    device="NPU",
    config={"PERFORMANCE_HINT": "LATENCY"},
)

# ─── AUTO: OpenVINO elige el mejor dispositivo ───
compiled_auto = core.compile_model(
    model=model,
    device="AUTO:CPU,GPU",  # CPU como fallback
)
```

---

## Ejecutar inference

```python
import numpy as np
import openvino as ov

core = ov.Core()
compiled = core.compile_model("model.xml", "CPU")

# ─── Forma 1: InferRequest ───
ireq = compiled.create_infer_request()

# Input como numpy
input_data = np.random.randn(1, 3, 224, 224).astype(np.float32)
ireq.set_input_tensor(0, ov.Tensor(input_data))
ireq.infer()
output = ireq.get_output_tensor(0).data
print(output)

# ─── Forma 2: Llamada directa (Python dict) ───
results = compiled({"input": input_data})
output = results["output"]

# ─── Forma 3: Batch inference ───
batch = np.random.randn(4, 3, 224, 224).astype(np.float32)
# compiled automáticamente hace reshape si el modelo soporta dynamic batch
results = compiled({"input": batch})
```

### `ov.Tensor` — Compartir datos sin copia

```python
import openvino as ov

# Tensor desde numpy (sin copia si el layout coincide)
arr = np.zeros((1, 1000), dtype=np.float32)
tensor = ov.Tensor(arr)              # comparte buffer con arr
tensor2 = ov.Tensor(arr, shape=[1, 1000])  # explícito

# Tensor en dispositivo específico
tensor_gpu = ov.Tensor(arr, device="GPU")

# Modificar tensor y reflejar en numpy
arr[0, 0] = 42.0
print(tensor.data[0, 0])  # → 42.0 (compartido)
```

---

## Conversión de modelos → IR

```python
import openvino as ov

# ─── Desde ONNX ───
model = ov.convert_model("model.onnx")
ov.save_model(model, "model.xml")

# ─── Desde PyTorch (torch.nn.Module) ───
import torch

class MyModel(torch.nn.Module):
    def forward(self, x):
        return x * 2

torch_model = MyModel()
example_input = torch.randn(1, 10)
ov_model = ov.convert_model(torch_model, example_input=example_input)
ov.save_model(ov_model, "model.xml")

# ─── Con input shapes explícitos ───
ov_model = ov.convert_model(
    "model.onnx",
    input=[("images", [1, 3, 224, 224])],
)

# ─── Desde HuggingFace transformers ───
from optimum.intel import OVModelForSequenceClassification

model = OVModelForSequenceClassification.from_pretrained(
    "distilbert-base-uncased",
    export=True,  # Convierte automáticamente a IR
)
model.save_pretrained("distilbert_ov/")  # → .xml + .bin
```

---

## Pre/Post-processing integrado con `ov.PrePostProcessor`

```python
import openvino as ov
import numpy as np

core = ov.Core()
model = core.read_model("model.xml")

ppp = ov.preprocess.PrePostProcessor(model)

# ─── Input: RGB 0-255 → BGR normalizado ───
ppp.input("images").tensor() \
    .set_layout("NHWC") \
    .set_element_type(ov.Type.u8)  # uint8 input

ppp.input("images").model() \
    .set_layout("NCHW") \
    .set_element_type(ov.Type.f32)

ppp.input("images").preprocess() \
    .convert_color(ov.preprocess.ColorFormat.RGB_to_BGR) \
    .mean([103.53, 116.28, 123.675])  # Resta media por canal

# ─── Output: sacar softmax ───
ppp.output("output").postprocess() \
    .convert_element_type(ov.Type.f32)

# Aplicar
model_with_ppp = ppp.build()
compiled = core.compile_model(model_with_ppp, "CPU")

# Inference ya incluye pre/post
image = np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)
result = compiled({"images": image})
```

---

## Model caching (compilación cacheada)

```python
core = ov.Core()

# Cache por dispositivo — la primera compilación es lenta, las siguientes instantáneas
core.set_property("CPU", {"CACHE_DIR": "./ov_cache/"})

compiled = core.compile_model("model.xml", "CPU")  # ~2s primera vez
compiled = core.compile_model("model.xml", "CPU")  # ~50ms con cache
```

---

## Heterogeneous execution (HETERO)

```python
# Repartir capas entre CPU y GPU automáticamente
compiled = core.compile_model(
    "model.xml",
    "HETERO:GPU,CPU",
    config={
        "MODEL_DISTRIBUTION_POLICY": "PERFORMANCE",
    },
)

# Capas específicas en CPU (ej. capas que no corren en GPU)
compiled = core.compile_model(
    "model.xml",
    "HETERO:GPU,CPU",
    config={
        "DEVICE_PRIORITIES": "CPU",  # Fallback a CPU para capas no soportadas
    },
)
```

---

## Multiple devices con `MULTI`

```python
# Balanceo entre múltiples GPUs
compiled = core.compile_model(
    "model.xml",
    "MULTI:GPU.0,GPU.1",
    config={
        "MULTI_DEVICE_PRIORITIES": "GPU.0,GPU.1",
    },
)

# Balanceo CPU + GPU
compiled = core.compile_model(
    "model.xml",
    "MULTI:CPU,GPU",
)
```

---

## NNCF — Quantization

```python
import nncf

# ─── Post-training quantization (INT8) ───
ov_model = core.read_model("model.xml")
calibration_data = nncf.Dataset(np.random.randn(100, 3, 224, 224).astype(np.float32))

quantized = nncf.quantize(
    ov_model,
    calibration_data,
    preset=nncf.QuantizationPreset.MIXED,      # Balance velocidad/precisión
    target_device=nncf.TargetDevice.CPU,
)

ov.save_model(quantized, "model_int8.xml")

# ─── INT4 para edge/LLM ───
quantized_int4 = nncf.quantize(
    ov_model,
    calibration_data,
    preset=nncf.QuantizationPreset.MIXED,
    model_type=nncf.ModelType.TRANSFORMER,
    subset_size=128,
    ignored_scope=nncf.IgnoredScope(names=["/logits"]),  # Capa final sin cuantizar
    target_device=nncf.TargetDevice.CPU_SPR,  # Xeon 4th gen+
)

# ─── Quantization-aware training (QAT, más preciso) ───
quantized_train = nncf.quantize(ov_model, calibration_data)
# ... fine-tune en PyTorch con fake quantization ...
```

---

## Benchmarking

```bash
# Línea de comando
benchmark_app -m model.xml \
  -d CPU \
  -niter 1000 \
  -nstreams 4 \
  -hint latency \
  -t 60 \
  -data_shape [1,3,224,224] \
  -report_type detailed \
  -report_folder ./bench_results/

# Salida: throughput (FPS), latency (ms), memory usage
```

```python
# Benchmark desde Python
from openvino.utils.benchmark import Benchmark

bench = Benchmark(
    model="model.xml",
    device="CPU",
    niter=1000,
    nstreams=4,
)
results = bench.run()
print(f"Throughput: {results['throughput']} FPS")
print(f"Latency median: {results['latency_median']} ms")
```

---

## Checklist OpenVINO

- [ ] `ov.Core().available_devices` check antes de compilar
- [ ] Modelo convertido a IR (`.xml` + `.bin`)
- [ ] Pre/post-processing integrado con `PrePostProcessor` (reduce overhead de Python)
- [ ] Quantization aplicada (INT8 mínimo)
- [ ] `PERFORMANCE_HINT` configurado (`LATENCY` vs `THROUGHPUT`)
- [ ] Model caching activado (`CACHE_DIR`)
- [ ] `NUM_STREAMS` y `INFERENCE_NUM_THREADS` ajustados al hardware
- [ ] Batch inference cuando aplica (dynamic batch en IR)
- [ ] `ov.Tensor` en vez de copias numpy cuando es posible
- [ ] Benchmark con `benchmark_app` antes de deploy
- [ ] Sin `.pth` / `.onnx` crudo en producción — siempre IR
