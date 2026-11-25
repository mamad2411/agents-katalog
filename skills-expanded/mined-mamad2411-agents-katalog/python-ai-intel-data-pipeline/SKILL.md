---
name: python-ai-intel-data-pipeline
description: "Data pipelines optimizados para hardware Intel. Cubre Intel Distribution for Python, NumPy/SciPy acelerados con MKL, pandas optimizado, AVX-512, VNNI, AMX, data loading con XPU affinity, y pre-procesamiento eficiente. Actívala al construir pipelines de datos, optimizar ETL, o preparar datasets para training en GPU Intel."
disable-model-invocation: true
---

# Data Pipelines on Intel Hardware

Preparar datos para AI en hardware Intel: Intel Distribution for Python, MKL-accelerated NumPy/SciPy, AVX-512/VNNI/AMX, y DataLoader con XPU affinity.

---

## Stack de datos Intel

| Herramienta | Optimización Intel | Instalación |
|------------|:-----------------:|-------------|
| **Intel Distribution for Python** | MKL-powered NumPy, SciPy, scikit-learn | `conda install intelpython3_full` |
| **pandas (MKL)** | Acelerado vía MKL en Intel Python | Viene con Intel Python |
| **NumPy (MKL)** | BLAS/LAPACK optimizados | `uv add numpy` (MKL si está en el path) |
| **scikit-learn (MKL)** | Algoritmos acelerados | `uv add scikit-learn` |
| **PyTorch DataLoader** | XPU affinity, pin memory | Viene con PyTorch |
| **oneDNN** | Primitives de bajo nivel | Runtime de PyTorch/OpenVINO |

```bash
# Intel Distribution for Python (recomendado para datos)
# Descargar: https://www.intel.com/content/www/us/en/developer/tools/oneapi/distribution-for-python.html
conda create -n idp python=3.14 -c intel
conda activate idp
uv add numpy pandas scipy scikit-learn
```

---

## Verificar aceleración MKL

```python
import numpy as np

# ─── Verificar que NumPy usa MKL ───
np.show_config()
# Debe mostrar: blas_mkl_info, lapack_mkl_info

# ─── Benchmark rápido: con y sin MKL ───
import time

size = 2000
a = np.random.randn(size, size).astype(np.float32)
b = np.random.randn(size, size).astype(np.float32)

# GEMM (matrix multiplication)
start = time.perf_counter()
c = a @ b
elapsed = time.perf_counter() - start
print(f"{size}x{size} matmul: {elapsed:.3f}s")
# Con MKL: ~0.3s, sin MKL: ~2s (en Xeon)

# ─── Num threads MKL ───
import os
os.environ["MKL_NUM_THREADS"] = "8"   # Forzar número de threads
os.environ["MKL_VERBOSE"] = "1"       # Ver qué kernels usa MKL
```

---

## AVX-512, VNNI, AMX

```python
import numpy as np

# Las CPUs Xeon recientes (4th gen+) soportan AMX (Advanced Matrix Extensions)
# AMX acelera operaciones de matriz (tiles) nativamente
# oneDNN lo usa automáticamente si detecta soporte

# ─── Verificar soporte ISA ───
import subprocess
result = subprocess.run(["lscpu"], capture_output=True, text=True)
print(result.stdout)
# Buscar: avx512_vnni, amx_bf16, amx_int8, amx_tile

# ─── Forzar ISA específica ───
os.environ["DNNL_MAX_CPU_ISA"] = "AVX512_CORE_AMX"  # Usar AMX
# o
os.environ["DNNL_MAX_CPU_ISA"] = "AVX512_CORE_VNNI"  # VNNI sin AMX
```

### Tabla de ISAs y CPUs

| ISA | CPUs | Acelera |
|-----|------|---------|
| AVX-512 | Xeon Scalable 3rd gen+ | GEMM, convoluciones |
| VNNI | Xeon 3rd gen+ | INT8 inference |
| AMX (BF16) | Xeon 4th gen+ (Sapphire Rapids) | Entrenamiento BF16 |
| AMX (INT8) | Xeon 4th gen+ | Inference INT8 |

---

## Pandas con MKL

```python
import pandas as pd
import numpy as np

# ─── Lectura optimizada ───
# pandas con MKL acelera groupby, merge, y transformaciones numéricas

df = pd.read_parquet("large_dataset.parquet")  # Parquet > CSV

# ─── Operaciones vectorizadas (van a MKL) ───
df["total"] = df["quantity"] * df["price"]          # Vectorizado → MKL
df["log_price"] = np.log(df["price"])                # MKL acelera np.log
df["rolling_avg"] = df.groupby("category")["total"].transform("mean")  # Groupby con MKL

# ─── Evitar iterrows (no se beneficia de MKL) ───
# ❌ for _, row in df.iterrows(): row["total"] = ...
# ✅ Operaciones vectorizadas

# ─── Cast a tipos optimizados ───
df["category"] = df["category"].astype("category")   # Memoria reducida
df["price"] = df["price"].astype(np.float32)          # Float32 → MKL más rápido
```

---

## Pre-procesamiento acelerado

```python
import numpy as np
from concurrent.futures import ThreadPoolExecutor
import asyncio

# ─── Normalización vectorizada (un solo paso MKL) ───
def normalize_batch(images: np.ndarray) -> np.ndarray:
    """Normaliza imágenes uint8 a float32 [-1, 1]."""
    return (images.astype(np.float32) / 127.5) - 1.0  # Vectorizado, MKL acelera

# ─── One-hot encoding rápido con NumPy ───
def one_hot(labels: np.ndarray, num_classes: int) -> np.ndarray:
    return np.eye(num_classes, dtype=np.float32)[labels]

# ─── Pipeline paralelo con threads (sin GIL en Python 3.14 free-threaded) ───
def preprocess_parallel(samples: list[np.ndarray]) -> np.ndarray:
    with ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(normalize_batch, samples))
    return np.stack(results)
```

---

## DataLoader con XPU affinity

```python
import torch
from torch.utils.data import DataLoader, Dataset

class IntelDataset(Dataset):
    def __init__(self, data_path: str, preload: bool = True):
        # Preload a CPU pinned memory si hay RAM suficiente
        if preload:
            self.data = torch.from_numpy(np.load(data_path))
        else:
            self.data_path = data_path

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return self.data[idx]

dataset = IntelDataset("images.npy", preload=True)

# ─── DataLoader optimizado para XPU ───
loader = DataLoader(
    dataset,
    batch_size=64,
    shuffle=True,
    pin_memory=True,                # Página bloqueada
    pin_memory_device="xpu",        # Para XPU (PyTorch 2.6+)
    num_workers=4,                  # Workers paralelos
    prefetch_factor=2,              # Prefetch 2 batches por worker
    persistent_workers=True,        # No recrear workers
)

# Consumir
for batch in loader:
    batch = batch.to("xpu:0", non_blocking=True)
    # ... training ...
```

---

## Streaming de datos grandes (memory-mapped)

```python
import numpy as np

# ─── Memory-mapped files (no carga todo en RAM) ───
# Ideal para datasets que no caben en RAM
mmap = np.memmap("large_dataset.npy", dtype=np.float32, mode="r", shape=(1_000_000, 784))

# Acceso por batch
batch_size = 64
for i in range(0, len(mmap), batch_size):
    batch = mmap[i : i + batch_size]
    # batch es una vista, no copia → eficiente
    tensor = torch.from_numpy(batch.copy()).to("xpu:0")  # copy() para contiguous

# ─── Parquet con streaming (PyArrow) ───
import pyarrow.parquet as pq

pf = pq.ParquetFile("large.parquet")
for batch in pf.iter_batches(batch_size=1024):
    df = batch.to_pandas()
    # Procesar
```

---

## Intel-optimized transforms

```python
import torch
import torchvision.transforms as T
import numpy as np

# ─── Transforms en GPU con torchvision ───
# torchvision.transforms corren en XPU si los tensores están ahí
transform = T.Compose([
    T.Resize(256),
    T.CenterCrop(224),
    T.ConvertImageDtype(torch.float32),
    T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

# Dataset custom con transforms en GPU
class GPUAcceleratedDataset(Dataset):
    def __init__(self, images, labels, device="xpu:0"):
        self.images = images
        self.labels = labels
        self.device = device
        self.transform = transform

    def __getitem__(self, idx):
        img = torch.from_numpy(self.images[idx]).to(self.device)
        img = self.transform(img)  # Transform en GPU
        label = self.labels[idx]
        return img, label
```

---

## oneDNN integration directa

```python
# oneDNN es el backend de PyTorch XPU y OpenVINO
# Normalmente no se usa directo, pero se puede para custom ops

import os

# ─── Control fino de oneDNN ───
os.environ["DNNL_DEFAULT_FPMATH_MODE"] = "BF16"     # FP math en BF16
os.environ["DNNL_PRIMITIVE_CACHE_CAPACITY"] = "1024" # Cache de primitives

# ─── Streams para solapar compute y transferencia ───
stream1 = torch.xpu.Stream()
stream2 = torch.xpu.Stream()

with torch.xpu.stream(stream1):
    batch1 = batch1.to("xpu", non_blocking=True)
with torch.xpu.stream(stream2):
    batch2 = batch2.to("xpu", non_blocking=True)

torch.xpu.synchronize()
```

---

## Checklist Data Pipeline

- [ ] Intel Distribution for Python (o NumPy con MKL) verificado con `np.show_config()`
- [ ] Operaciones vectorizadas con NumPy/pandas (nada de `iterrows` en loops calientes)
- [ ] `MKL_NUM_THREADS` configurado según cores disponibles
- [ ] `DNNL_MAX_CPU_ISA` = `AVX512_CORE_AMX` si el CPU lo soporta
- [ ] Datasets pre-cargados (`.npy`, `.parquet`) en vez de CSV/JSON
- [ ] `pin_memory=True` + `pin_memory_device="xpu"` en DataLoader
- [ ] `persistent_workers=True` para evitar recrear workers de datos
- [ ] Memory-mapped files para datasets que no caben en RAM
- [ ] Transforms en GPU cuando es posible (torchvision con tensores en XPU)
- [ ] `non_blocking=True` en transferencias CPU→XPU con streams separados
