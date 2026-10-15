---
name: python-ai-intel-core
description: "Guía principal de AI en Python con hardware Intel. Cubre el stack oneAPI, OpenVINO, PyTorch XPU, Intel Arc, Core Ultra (NPU), Xeon, y Gaudi. Versiones, instalación, detección de dispositivos, y ciclo dev→deploy. Actívala para cualquier tarea de AI/ML sobre hardware Intel: nuevos proyectos, migración desde CUDA, optimización, o decisión de hardware target."
---

# Python AI on Intel — Core Guide

Guía canónica para desarrollo de AI en Python sobre hardware Intel. Cubre todo el ecosistema 2026: OpenVINO, PyTorch 2.7 con XPU nativo, oneAPI Toolkit, Intel Arc, Core Ultra NPU, Xeon, y Gaudi.

---

## Versiones y ecosistema (2026)

| Componente | Versión | Estado | Rol |
|-----------|---------|:------:|-----|
| **OpenVINO** | 2026.2 (Mayo 2026) | ✅ Estable | Inference runtime universal |
| **PyTorch** | 2.7 | ✅ Estable | Training + inference con XPU nativo |
| **oneAPI Toolkit** | 2026.0 | ✅ Estable | Compiladores, libraries, analyzers |
| **Intel Distribution for Python** | 2026.0 | ✅ Estable | Python optimizado con MKL/oneDNN |
| **TorchInductor + Triton (XPU)** | — | 🔬 Beta | `torch.compile` en GPU Intel |
| **OpenVINO llama.cpp backend** | — | 🔬 Preview | LLM inference en CPU/GPU/NPU Intel |
| **IPEX (Intel Ext. for PyTorch)** | 2.8 (final) | 🛑 Discontinuado | Migrar a PyTorch nativo XPU |
| **Intel NPU Acceleration Library** | 1.4.0 | 🛑 Archivado | Migrar a OpenVINO NPU plugin |

---

## Hardware detection — `ov.Core()` y `torch.xpu`

```python
import openvino as ov
import torch

# ── OpenVINO: qué dispositivos tengo ──
core = ov.Core()
devices = core.get_available_devices()
print(devices)  # → ["CPU", "GPU", "NPU"]

for d in devices:
    print(f"{d}: {core.get_property(d, 'FULL_DEVICE_NAME')}")

# ── PyTorch: XPU disponible? ──
print(f"XPU available: {torch.xpu.is_available()}")       # True si driver OK
print(f"XPU devices:  {torch.xpu.device_count()}")         # 1+ si Arc/Flex
print(f"XPU name:     {torch.xpu.get_device_name(0)}")     # "Intel Arc A770"

xpu = torch.device("xpu:0")
t = torch.randn(2, 3, device=xpu)
print(t.device)  # → xpu:0

# ── NPU check (OpenVINO) ──
if "NPU" in core.available_devices:
    print("NPU detected — Core Ultra or newer")
```

---

## Stack recomendado por defecto

| Propósito | Herramienta | Instalación |
|-----------|-------------|-------------|
| Package manager | `uv` | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| Inference runtime | OpenVINO 2026.x | `uv add openvino` |
| Training framework | PyTorch 2.7 | `uv add torch` (XPU runtime auto) |
| LLM serving | OpenVINO Model Server / llama.cpp | `docker://openvino/model_server` |
| Model optimization | NNCF + OpenVINO | `uv add nncf` |
| Quantization | NNCF / OpenVINO POT | Viene con `openvino` |
| Profiling | VTune + PTI | oneAPI Toolkit |
| Deployment | Docker + OVMS | `docker://openvino/model_server` |
| Data processing | Pandas (MKL) / NumPy (MKL) | Intel Distribution for Python |
| Embeddings | OpenVINO + optimum-intel | `uv add optimum-intel` |
| Vector DB | pgvector (PostgreSQL) | PostgreSQL 18 + extension |
| RAG orchestration | LangChain / LlamaIndex | `uv add langchain` |

---

## Setup rápido

```bash
# 1. Instalar oneAPI Toolkit (prerequisito de sistema)
#    Descargar de: https://www.intel.com/content/www/us/en/developer/tools/oneapi/toolkit.html
#    Windows: instalador .exe
#    Linux:   sudo apt install intel-basekit intel-hpckit
#    WSL2:    igual que Linux

# 2. Verificar drivers GPU Intel
#    Windows: dxdiag → Pantalla → Intel Arc
#    Linux:   clinfo | grep "Device Name"
#    WSL2:    clinfo (con --enable-wsl-gpu)

# 3. Crear proyecto
uv init mi-ai-app
cd mi-ai-app

# 4. Agregar dependencias
uv add openvino torch nncf
uv add optimum-intel langchain
uv add --dev pytest pytest-asyncio

# 5. Verificar stack
uv run python -c "
import openvino as ov; print('OpenVINO:', ov.get_version())
import torch; print('PyTorch:', torch.__version__)
print('XPU:', torch.xpu.is_available())
"
```

---

## Decisiones de hardware target

```
┌─────────────────────────────────────────────────────────┐
│  ¿Qué querés hacer?                                     │
│                                                         │
│  Training modelo propio ──→ Arc GPU / Flex / Gaudi     │
│  Inference batch (API)  ──→ Arc GPU / Xeon             │
│  Inference edge/on-dev  ──→ Core Ultra (GPU o NPU)     │
│  LLM serving            ──→ Arc GPU (discreta)         │
│  RAG on-device          ──→ Core Ultra (NPU+GPU)       │
│  Data pipeline          ──→ Xeon (AVX-512, AMX)        │
│  Prototipado            ──→ Tiber Developer Cloud      │
└─────────────────────────────────────────────────────────┘
```

### Tabla de afinidad modelo ↔ hardware

| Modelo | Mejor target | Alternativa |
|--------|-------------|-------------|
| CNN (ResNet, YOLO) | CPU (oneDNN) o GPU | NPU (edge) |
| Transformer (<1B) | GPU o NPU | CPU con AMX |
| LLM (7B-13B) | GPU Arc | CPU + INT4 quant |
| LLM (70B+) | Multi-GPU / Gaudi | CPU con streaming |
| Embeddings | CPU (oneDNN) | GPU batch |
| Reranker | CPU | GPU |
| Audio (Whisper) | CPU o NPU | GPU |

---

## Ciclo de desarrollo completo

```
┌─────────────┐    ┌──────────────┐    ┌──────────────┐    ┌────────────┐
│  Training   │ →  │  Conversion  │ →  │ Quantization │ →  │  Deploy    │
│  PyTorch    │    │  ov.convert  │    │  NNCF / POT  │    │  OVMS      │
│  XPU/GPU    │    │  .pth → IR   │    │  FP32 → INT8 │    │  Docker    │
└─────────────┘    └──────────────┘    └──────────────┘    └────────────┘
      ↑                                                         │
      └────────── Profile (VTune/PTI) ←─────────────────────────┘
```

```python
# Ejemplo end-to-end compacto
import torch
import openvino as ov
import nncf

# 1. Training (simplificado)
model = torch.nn.Sequential(
    torch.nn.Linear(784, 256),
    torch.nn.ReLU(),
    torch.nn.Linear(256, 10),
)
x = torch.randn(1, 784, device=torch.device("xpu:0"))
model.to("xpu:0")
# ... training loop ...

# 2. Exportar a ONNX
torch.onnx.export(model, torch.randn(1, 784), "model.onnx")

# 3. Convertir a IR + cuantizar
ov_model = ov.convert_model("model.onnx")
quantized = nncf.quantize(ov_model, nncf.Dataset(...))
ov.save_model(quantized, "model_quantized.xml")
```

---

## Convenciones de código

### Naming

| Elemento | Convención | Ejemplo |
|----------|------------|---------|
| Módulos | `snake_case.py` | `inference_pipeline.py` |
| Clases | `PascalCase` | `IntelInferenceEngine` |
| Funciones | `snake_case` | `load_openvino_model()` |
| Variables | `snake_case` | `xpu_device`, `ov_core` |
| Dispositivo | `xpu`, `gpu` | `torch.device("xpu:0")` |
| Modelos IR | `snake_case.xml` | `resnet50_int8.xml` |

### Estructura de proyecto AI Intel

```
miapp/
├── pyproject.toml
├── uv.lock
├── README.md
├── config/
│   └── inference.yaml              # OpenVINO device config
├── src/
│   └── miapp/
│       ├── __init__.py
│       ├── training/
│       │   ├── train.py            # PyTorch training loop (XPU)
│       │   └── data.py             # Dataset/Dataloader con XPU affinity
│       ├── conversion/
│       │   └── export.py           # PyTorch → ONNX → IR
│       ├── optimization/
│       │   └── quantize.py          # NNCF quantization pipeline
│       ├── inference/
│       │   ├── engine.py            # OpenVINO inference engine
│       │   └── pipeline.py          # Pre/post-processing
│       ├── serving/
│       │   └── ovms_config.json     # OpenVINO Model Server config
│       └── profiling/
│           └── benchmark.py         # Benchmark scripts (VTune/PTI)
├── models/
│   ├── original/                    # .pth, .onnx, .safetensors
│   └── optimized/                   # .xml + .bin (IR cuantizado)
├── tests/
│   ├── test_inference.py
│   ├── test_accuracy.py
│   └── test_latency.py
└── docker/
    ├── Dockerfile
    └── docker-compose.yml
```

---

## Reglas de oro

1. **OpenVINO `ov.Core()` como entry point.** Siempre detectar dispositivos disponibles antes de cargar modelos.
2. **Training → PyTorch XPU nativo.** IPEX discontinuado. `torch.device("xpu:0")`.
3. **Deployment → IR.** `.xml` + `.bin` para producción, nunca `.pth` crudo.
4. **Quantization siempre.** INT8 mínimo; INT4 para LLMs y edge.
5. **`torch.compile` con TorchInductor + Triton** para acelerar training e inference en GPU Intel.
6. **Profiling antes de optimizar.** VTune para system-level, PTI para PyTorch traces.
7. **Un modelo, múltiples backends.** El mismo IR corre en CPU, GPU y NPU sin cambios.
8. **Docker con `--device /dev/dri`** para acceso a GPU Intel desde contenedores.
9. **Heterogeneous execution.** OpenVINO puede repartir capas entre CPU + GPU + NPU simultáneamente.
10. **Sin `torch.cuda()`.** Código Intel-only usa `torch.xpu()` o `torch.device("xpu")`.
11. **Tiber Developer Cloud para prototipado.** Gratis, JupyterLab preconfigurado con todo el stack.
12. **`uv` para dependencias.** Compatible con el ecosistema `python-core`.

---

## Sub-skills del kit

> 📁 Cada sub-skill tiene su guía detallada en `./{nombre}/SKILL.md`. Usa `read` para cargarla cuando el tema lo requiera.

| Skill | Cuándo cargarla |
|-------|----------------|
| `python-ai-intel-openvino` | Inference, IR conversion, pre/post-processing, model optimization |
| `python-ai-intel-pytorch-xpu` | Training en GPU Intel, `torch.compile`, mixed precision, XPU tensors |
| `python-ai-intel-llm` | LLMs en Intel: llama.cpp, OpenVINO GenAI, vLLM, quantization AWQ/GPTQ |
| `python-ai-intel-npu` | Core Ultra NPU: OpenVINO NPU plugin, modelos compatibles, limitaciones |
| `python-ai-intel-profiling` | VTune, PTI, OpenVINO benchmarks, GPU utilization, memory profiling |
| `python-ai-intel-deployment` | Docker + OVMS, Intel Tiber Cloud, CI/CD, model packaging, edge serving |
| `python-ai-intel-data-pipeline` | Intel-optimized pandas/NumPy, MKL, AVX-512, data loading XPU affinity |
| `python-ai-intel-rag` | RAG en Intel: embeddings via OpenVINO, pgvector, LangChain/LlamaIndex |
