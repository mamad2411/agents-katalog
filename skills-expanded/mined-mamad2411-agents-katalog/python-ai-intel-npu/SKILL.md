---
name: python-ai-intel-npu
description: "Intel Core Ultra NPU: inferencia en la Neural Processing Unit integrada. Cubre el plugin NPU de OpenVINO, modelos compatibles (CNN, transformers pequeños), limitaciones de memoria, conversión de modelos, y casos de uso edge (video analytics, audio, NLP liviano). Actívala para inference on-device en Core Ultra o al evaluar NPU vs GPU."
disable-model-invocation: true
---

# Intel Core Ultra NPU Guide

La NPU (Neural Processing Unit) integrada en procesadores Intel Core Ultra (Meteor Lake, Arrow Lake, Lunar Lake) permite inferencia de bajo consumo para modelos pequeños directamente en el chip.

---

## Estado y advertencias

| Componente | Estado | Recomendación |
|-----------|:------:|---------------|
| `intel-npu-acceleration-library` | 🛑 Archivado (GitHub) | No usar en proyectos nuevos |
| OpenVINO NPU plugin | ✅ Activo | Usar `ov.Core().compile_model(model, "NPU")` |
| NPU driver | ✅ En Windows/Linux | Requiere driver Intel NPU |

> **Regla:** La NPU es para modelos pequeños (<100M params) y baja latencia. Si necesitás throughput o modelos grandes, usá GPU.

---

## Setup y detección

```bash
# El plugin NPU viene con OpenVINO 2026.x (Windows y Linux)
uv add openvino
```

```python
import openvino as ov

core = ov.Core()

# ─── Detectar NPU ───
if "NPU" in core.available_devices:
    print("✅ NPU detectada")
    props = core.get_property("NPU", "SUPPORTED_PROPERTIES")
    print(f"Nombre: {core.get_property('NPU', 'FULL_DEVICE_NAME')}")
else:
    print("❌ NPU no detectada — requiere driver NPU instalado")

# ─── Verificar capabilities ───
caps = core.get_property("NPU", "OPTIMIZATION_CAPABILITIES")
print(f"Capabilities: {caps}")  # Ej: FP16, INT8

# ─── Memoria disponible ───
try:
    mem = core.get_property("NPU", "AVAILABLE_MEMORY")
    print(f"NPU memory: {mem} bytes")
except:
    pass
```

---

## Modelos compatibles con NPU

```python
import openvino as ov

core = ov.Core()

# ─── Compilación básica ───
model = core.read_model("model_int8.xml")  # NPU requiere INT8 o FP16
compiled = core.compile_model(
    model,
    device="NPU",
    config={
        "PERFORMANCE_HINT": "LATENCY",
    },
)

# ─── Inference ───
import numpy as np
input_data = np.random.randn(1, 3, 224, 224).astype(np.float32)
results = compiled({"input": input_data})
```

### Tipos de modelos que funcionan bien en NPU

| Tipo de modelo | Ejemplos | Parámetros típicos |
|---------------|----------|:-----------------:|
| CNN liviana | MobileNet, EfficientNet-Lite | <10M |
| Detector de objetos | YOLO-nano, SSD-MobileNet | <20M |
| Clasificador de audio | YamNet, Whisper-tiny | <40M |
| NLP liviano | DistilBERT, ALBERT | <70M |
| Face detection | UltraFace, BlazeFace | <1M |

> **Limitación:** Modelos grandes (>100M params) o con operaciones complejas (atención multi-head grande) no compilan en NPU o exceden la memoria.

---

## Conversión para NPU

```python
import openvino as ov
import nncf
import torch

# ─── 1. Training en PyTorch ───
model = torch.hub.load("pytorch/vision", "mobilenet_v2", pretrained=True)
model.eval()

# ─── 2. Convertir a IR ───
example = torch.randn(1, 3, 224, 224)
ov_model = ov.convert_model(model, example_input=example)

# ─── 3. Cuantizar a INT8 (NPU lo requiere) ───
import numpy as np
calib_data = nncf.Dataset(np.random.randn(100, 3, 224, 224).astype(np.float32))

quantized = nncf.quantize(
    ov_model,
    calib_data,
    target_device=nncf.TargetDevice.NPU,  # Específico para NPU
    preset=nncf.QuantizationPreset.PERFORMANCE,
)
ov.save_model(quantized, "mobilenet_npu.xml")

# ─── 4. Compilar y usar en NPU ───
compiled = core.compile_model("mobilenet_npu.xml", "NPU")
results = compiled({"input": input_data})
```

---

## NPU vs GPU: cuándo elegir NPU

```python
def choose_device(model, batch_size, latency_budget_ms):
    """Lógica de decisión para elegir NPU vs GPU."""

    # NPU: mejor para baja latencia, batch pequeño, bajo consumo
    if latency_budget_ms < 5 and batch_size == 1:
        return "NPU"

    # GPU: mejor para throughput, batch grande, modelos complejos
    if batch_size > 4:
        return "GPU"

    # Fallback a CPU si nada funciona
    return "CPU"

device = choose_device(model, batch_size=1, latency_budget_ms=3)
compiled = core.compile_model(model, device)
```

### Tabla comparativa

| Métrica | NPU | GPU (integrada) | GPU (discreta) |
|---------|:---:|:---:|:---:|
| Latencia (batch=1) | ⭐⭐⭐ | ⭐⭐ | ⭐ |
| Throughput (batch=32) | ⭐ | ⭐⭐ | ⭐⭐⭐ |
| Consumo energético | ⭐⭐⭐ | ⭐⭐ | ⭐ |
| Modelos soportados | Pequeños | Medianos | Todos |
| Memoria típica | ~1-2 GB | 4-8 GB (compartida) | 8-48 GB |

---

## Caso de uso: Video analytics on-device

```python
import openvino as ov
import cv2
import numpy as np

core = ov.Core()

# Modelo de detección liviano en NPU
det_model = core.compile_model("ssd_mobilenet_int8.xml", "NPU")
# Modelo de clasificación en CPU (como fallback)
cls_model = core.compile_model("resnet18_int8.xml", "CPU")

cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Preprocess en CPU (NPU requiere tensor en CPU → transferencia automática)
    input_tensor = cv2.resize(frame, (300, 300))
    input_tensor = np.expand_dims(input_tensor, 0).astype(np.float32)

    # Inference en NPU (bajo consumo)
    detections = det_model({"input": input_tensor})

    # Post-process en CPU
    for det in detections["detection_out"][0][0]:
        if det[2] > 0.5:  # confidence > 50%
            x1, y1, x2, y2 = map(int, det[3:7] * [frame.shape[1], frame.shape[0], frame.shape[1], frame.shape[0]])
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    cv2.imshow("NPU Video Analytics", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
```

---

## Heterogeneous execution con NPU

```python
# Repartir capas entre NPU y CPU
compiled = core.compile_model(
    "model_int8.xml",
    "HETERO:NPU,CPU",
    config={
        "MODEL_DISTRIBUTION_POLICY": "PERFORMANCE",
        "DEVICE_PRIORITIES": "NPU",
    },
)
# OpenVINO asigna capas compatibles a NPU, el resto a CPU automáticamente
```

---

## Troubleshooting NPU

```python
import openvino as ov

core = ov.Core()

# ─── Error común: modelo FP32 en NPU ───
try:
    compiled = core.compile_model("model_fp32.xml", "NPU")
except RuntimeError as e:
    print(f"❌ Probablemente el modelo no está cuantizado: {e}")
    # Solución: cuantizar a INT8/FP16 con nncf.quantize()

# ─── Error: operación no soportada ───
try:
    compiled = core.compile_model("complex_model.xml", "NPU")
except RuntimeError as e:
    print(f"❌ Alguna capa no es soportada: {e}")
    # Solución: usar HETERO:NPU,CPU

# ─── Query de soporte ───
supported_ops = core.get_property("NPU", "SUPPORTED_OPS")
print(f"Ops soportadas: {len(supported_ops)}")
```

---

## Checklist NPU

- [ ] Driver NPU instalado (Windows Update o Intel Driver & Support Assistant)
- [ ] `ov.Core().available_devices` incluye `"NPU"`
- [ ] Modelo cuantizado a INT8 (NPU no soporta FP32)
- [ ] Modelo <100M parámetros (limitación de memoria NPU)
- [ ] `target_device=nncf.TargetDevice.NPU` al cuantizar
- [ ] Batch size = 1 (NPU optimizada para baja latencia, no batch)
- [ ] Fallback a CPU o GPU vía `HETERO` si el modelo tiene capas no soportadas
- [ ] Sin dependencia de `intel-npu-acceleration-library` (archivada)
- [ ] Medir consumo energético real vs GPU para justificar NPU
