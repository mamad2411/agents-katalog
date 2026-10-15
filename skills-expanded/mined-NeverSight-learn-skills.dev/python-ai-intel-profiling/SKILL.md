---
name: python-ai-intel-profiling
description: "Profiling de AI en hardware Intel. Cubre Intel VTune Profiler, PTI (PyTorch Profiler Integration), OpenVINO benchmark_app, GPU utilization (Intel GPA), oneDNN verbose, y memory profiling. Actívala al optimizar rendimiento, diagnosticar cuellos de botella, o antes de deployar."
disable-model-invocation: true
---

# Profiling AI on Intel Hardware

Profiling antes de optimizar. Las herramientas de Intel: VTune para system-level, PTI para PyTorch traces, y benchmark_app para OpenVINO.

---

## Stack de profiling

| Herramienta | Scope | Instalación |
|------------|-------|-------------|
| **Intel VTune Profiler** | System: CPU, GPU, NPU, memoria | oneAPI Toolkit |
| **PTI** (PyTorch Profiler Integration) | PyTorch ops, GPU kernels, data loading | `uv add intel-pti` |
| **benchmark_app** | OpenVINO inference pura | Viene con OpenVINO |
| **Intel GPA** (Graphics Performance Analyzers) | GPU utilization, frame analysis | Intel GPA standalone |
| **oneDNN verbose** | oneDNN primitives, GEMMs | `export DNNL_VERBOSE=1` |
| **torch.profiler** | PyTorch execution traces | built-in |

---

## Intel VTune Profiler

```bash
# Instalación (viene con oneAPI Toolkit)
# Windows: Intel oneAPI Toolkit installer
# Linux:   sudo apt install intel-oneapi-vtune

# ─── Command-line profiling ───
vtune -collect hotspots \
  -result-dir ./vtune_results \
  -- python train.py

vtune -collect memory-consumption \
  -result-dir ./vtune_mem \
  -- python inference.py

# ─── GPU profiling ───
vtune -collect gpu-hotspots \
  -result-dir ./vtune_gpu \
  -- python train_gpu.py

# ─── Report ───
vtune -report summary -result-dir ./vtune_results
vtune -report top-down -result-dir ./vtune_results
vtune -report callstacks -result-dir ./vtune_results

# ─── GUI ───
vtune-gui ./vtune_results
```

```python
# VTune API desde Python (pausar/reanudar profiling)
import os

# Marcar región de interés
os.environ["ITT_WAIT"] = "1"  # Habilitar pausas ITT

# Iniciar VTune con: vtune -collect hotspots -- python script.py
# VTune detecta las regiones automáticamente
```

---

## PTI — PyTorch Profiler Integration

```python
import torch
import torch.profiler as profiler

model = MyModel().to("xpu:0")
inputs = torch.randn(64, 784, device="xpu:0")

# ─── Perfilar con PTI ───
with profiler.profile(
    activities=[
        profiler.ProfilerActivity.CPU,
        profiler.ProfilerActivity.XPU,  # Trace de GPU Intel
    ],
    schedule=profiler.schedule(
        wait=2,        
        warmup=2,      
        active=6,      
        repeat=1,
    ),
    on_trace_ready=profiler.tensorboard_trace_handle("./log/pti_trace"),
    record_shapes=True,
    profile_memory=True,
    with_stack=True,
) as prof:
    for step in range(20):
        with profiler.record_function("forward"):
            outputs = model(inputs)
        with profiler.record_function("loss"):
            loss = outputs.sum()
        with profiler.record_function("backward"):
            loss.backward()
        prof.step()

# Visualizar:
# tensorboard --logdir ./log/pti_trace
```

### PTI report programático

```python
# ─── Análisis de GPU time ───
print(prof.key_averages().table(
    sort_by="xpu_time_total",
    row_limit=10,
))

# ─── Data loading bottleneck ───
print(prof.key_averages().table(
    sort_by="cpu_time_total",
    row_limit=10,
))
```

---

## `torch.profiler` + XPU (sin PTI)

```python
import torch.autograd.profiler as profiler

model = MyModel().to("xpu:0")
x = torch.randn(64, 784, device="xpu:0")

# ─── Profiling básico XPU ───
with profiler.profile(
    use_device="xpu",     # Trace GPU ops
    use_cuda=False,        # No CUDA
    record_shapes=True,
) as prof:
    with profiler.record_function("inference"):
        y = model(x)
    torch.xpu.synchronize()

print(prof.key_averages().table(sort_by="xpu_time_total", row_limit=15))

# Exportar a Chrome trace
prof.export_chrome_trace("trace.json")
# Abrir en chrome://tracing
```

---

## OpenVINO benchmark_app

```bash
# ─── Benchmark completo ───
benchmark_app \
  -m model.xml \
  -d CPU \
  -hint throughput \
  -niter 1000 \
  -nstreams 4 \
  -t 60 \
  -data_shape [1,3,224,224] \
  -report_type detailed \
  -report_folder ./bench_results/

# ─── Latencia (batch=1) ───
benchmark_app -m model.xml -d GPU -hint latency -niter 500

# ─── Batch variable con dynamic shapes ───
benchmark_app -m model.xml -d CPU \
  -data_shape [1,3,224,224] [4,3,224,224] [16,3,224,224]

# ─── Probar todos los dispositivos ───
benchmark_app -m model.xml -d AUTO
```

```python
# Benchmark desde Python con OpenVINO
import openvino as ov
import numpy as np
import time

def benchmark_inference(model_path, device, n_warmup=50, n_test=500):
    core = ov.Core()
    compiled = core.compile_model(model_path, device)

    # Warmup
    dummy = np.random.randn(1, 3, 224, 224).astype(np.float32)
    for _ in range(n_warmup):
        compiled({"input": dummy})

    # Medir
    start = time.perf_counter()
    for _ in range(n_test):
        compiled({"input": dummy})
    elapsed = time.perf_counter() - start

    fps = n_test / elapsed
    latency = (elapsed / n_test) * 1000
    return {"fps": fps, "latency_ms": latency, "device": device}

print(benchmark_inference("model.xml", "CPU"))
print(benchmark_inference("model.xml", "GPU"))
```

---

## GPU utilization (Intel GPA)

```bash
# Intel GPA: herramienta gráfica para monitorear GPU
# Abrir GPA Monitor:
gpa-monitor

# Capturar frame para análisis:
gpa-frame-analyzer --capture-frame

# Desde línea de comando:
gpa-system-analyzer --app "python inference.py" --duration 10
```

---

## oneDNN verbose

```bash
# Ver qué primitives usa oneDNN (motor de OpenVINO y PyTorch XPU)
export DNNL_VERBOSE=1          # Info general
export DNNL_VERBOSE=2          # Detallado (incluye GEMM shapes)

# Running inference:
python inference.py 2>&1 | grep "dnnl_verbose"

# Salida típica:
# dnnl_verbose,info,primitive,exec,convolution,jit:avx512_core,...
# dnnl_verbose,info,primitive,exec,matmul,brgemm,...
# dnnl_verbose,info,primitive,exec,reorder,jit:uni,...

# Verificar qué ISA se está usando:
export DNNL_VERBOSE=1
python -c "import torch; torch.randn(10).sum()" 2>&1 | head
```

---

## Memory profiling

```python
import torch
import tracemalloc

# ─── PyTorch GPU memory ───
def log_gpu_memory(tag=""):
    alloc = torch.xpu.memory_allocated(0) / 1024**2
    reserved = torch.xpu.memory_reserved(0) / 1024**2
    print(f"[{tag}] Alloc: {alloc:.1f} MB | Reserved: {reserved:.1f} MB")

log_gpu_memory("before model")
model = MyModel().to("xpu:0")
log_gpu_memory("after model")

# ─── Python heap (CPU memory) ───
tracemalloc.start()
# ... ejecutar workload ...
snapshot = tracemalloc.take_snapshot()
top = snapshot.statistics("lineno")
for stat in top[:10]:
    print(stat)

# ─── Peak tracking ───
torch.xpu.reset_peak_memory_stats()
model(x)
peak = torch.xpu.max_memory_allocated(0) / 1024**2
print(f"Peak GPU memory: {peak:.1f} MB")
```

---

## Profiling pipeline end-to-end

```python
import time
from dataclasses import dataclass, field

@dataclass
class PipelineProfiler:
    """Mide cada etapa del pipeline de inference."""
    timings: dict = field(default_factory=dict)

    def measure(self, stage: str):
        start = time.perf_counter()
        yield
        elapsed = (time.perf_counter() - start) * 1000
        self.timings.setdefault(stage, []).append(elapsed)

    def report(self):
        print("\nPipeline Profile:")
        print(f"{'Stage':<30} {'Avg (ms)':<12} {'P99 (ms)':<12}")
        print("-" * 54)
        for stage, times in self.timings.items():
            avg = sum(times) / len(times)
            p99 = sorted(times)[int(len(times) * 0.99)]
            print(f"{stage:<30} {avg:<12.2f} {p99:<12.2f}")

profiler = PipelineProfiler()

for _ in range(100):
    with profiler.measure("preprocess"):
        tensor = preprocess(image)
    with profiler.measure("inference"):
        result = compiled({"input": tensor})
    with profiler.measure("postprocess"):
        output = postprocess(result)

profiler.report()
```

---

## Checklist Profiling

- [ ] VTune system-level profiling antes de optimizar código
- [ ] PTI para traces de PyTorch XPU (ops + memoria + data loading)
- [ ] `benchmark_app` para medir throughput/latencia pura de OpenVINO
- [ ] `torch.xpu.synchronize()` antes de medir tiempos en GPU
- [ ] `DNNL_VERBOSE=1` para verificar que oneDNN usa las instrucciones esperadas (AVX-512, AMX)
- [ ] GPU memory tracking (`torch.xpu.memory_allocated`, `max_memory_allocated`)
- [ ] Pipeline profiling (preprocess → inference → postprocess) para ver dónde está el bottleneck
- [ ] Warmup antes de medir (50-100 iteraciones)
- [ ] Sin profiling en código de producción — usar flags o env vars
- [ ] Resultados exportados a Chrome trace o TensorBoard
