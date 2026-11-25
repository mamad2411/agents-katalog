---
name: python-ai-intel-pytorch-xpu
description: "PyTorch 2.7 con soporte nativo XPU para GPUs Intel (Arc, Flex, Max). Cubre tensores en XPU, torch.compile + TorchInductor + Triton, mixed precision (FP16/BF16), DataLoader con GPU affinity, migración desde IPEX, y entrenamiento distribuido. Actívala para training en GPUs Intel o migración desde CUDA."
disable-model-invocation: true
---

# PyTorch XPU — Training on Intel GPUs

PyTorch 2.7 soporta GPUs Intel (Arc, Flex, Max) de forma nativa con el backend XPU. IPEX está discontinuado — no lo uses en proyectos nuevos.

---

## Setup

```bash
# PyTorch con soporte XPU (drivers Intel GPU ya instalados)
uv add torch torchvision torchaudio

# Verificar
uv run python -c "
import torch
print(torch.__version__)
print('XPU available:', torch.xpu.is_available())
print('XPU devices:', torch.xpu.device_count())
print('XPU device 0:', torch.xpu.get_device_name(0))
"
```

---

## Tensores y dispositivos XPU

```python
import torch

# ─── Verificar disponibilidad ───
assert torch.xpu.is_available(), "XPU no disponible. Instalar drivers Intel GPU."

device = torch.device("xpu:0")  # o "xpu" para default
print(f"Device: {torch.xpu.get_device_name(0)}")

# ─── Crear tensores en XPU ───
x = torch.randn(2, 3, device="xpu:0")
y = torch.ones(2, 3, device="xpu")

# Operaciones en GPU
z = x + y
print(z.device)  # → xpu:0

# ─── Mover modelos a XPU ───
model = torch.nn.Linear(10, 5)
model.to("xpu:0")

# ─── Mover datos entre dispositivos ───
cpu_tensor = torch.randn(100, 100)
xpu_tensor = cpu_tensor.to("xpu:0")       # explícito
xpu_tensor2 = cpu_tensor.xpu()             # shorthand
back_to_cpu = xpu_tensor.cpu()

# ─── Transferencia non-blocking ───
stream = torch.xpu.Stream()
with torch.xpu.stream(stream):
    xpu_tensor = cpu_tensor.to("xpu", non_blocking=True)
```

---

## Training loop completo

```python
import torch
from torch import nn, optim
from torch.utils.data import DataLoader, TensorDataset

device = torch.device("xpu:0" if torch.xpu.is_available() else "cpu")

# ─── Modelo ───
class MLP(nn.Module):
    def __init__(self, in_dim=784, hidden=256, out_dim=10):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(in_dim, hidden),
            nn.ReLU(),
            nn.Linear(hidden, out_dim),
        )

    def forward(self, x):
        return self.net(x)

model = MLP().to(device)
criterion = nn.CrossEntropyLoss()
optimizer = optim.AdamW(model.parameters(), lr=1e-3)

# ─── Datos sintéticos ───
X = torch.randn(1000, 784, device=device)
y = torch.randint(0, 10, (1000,), device=device)
loader = DataLoader(TensorDataset(X, y), batch_size=64, shuffle=True)

# ─── Training ───
model.train()
for epoch in range(10):
    total_loss = 0
    for batch_x, batch_y in loader:
        batch_x, batch_y = batch_x.to(device), batch_y.to(device)
        optimizer.zero_grad()
        output = model(batch_x)
        loss = criterion(output, batch_y)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    print(f"Epoch {epoch+1}: loss={total_loss/len(loader):.4f}")
```

---

## `torch.compile` en XPU (TorchInductor + Triton)

```python
import torch

model = MLP().to("xpu:0")

# ─── Compilar el modelo ───
# TorchInductor genera kernels Triton para XPU (Beta en 2.7)
model_compiled = torch.compile(
    model,
    backend="inductor",      # Default, usa Triton
    mode="reduce-overhead",  # o "default", "max-autotune"
    options={
        "epilogue_fusion": True,
        "max_autotune": True,
    },
)

# Primera llamada compila (~segundos), siguientes son rápidas
x = torch.randn(64, 784, device="xpu:0")
y = model_compiled(x)          # Compilación sucede aquí
y = model_compiled(x)          # Instantáneo
```

---

## Mixed precision — FP16 / BF16

```python
import torch

model = MLP().to("xpu:0")
optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3)

# ─── Automatic Mixed Precision (AMP) ───
scaler = torch.amp.GradScaler("xpu")

for batch_x, batch_y in loader:
    batch_x, batch_y = batch_x.to("xpu:0"), batch_y.to("xpu:0")
    optimizer.zero_grad()

    with torch.amp.autocast(device_type="xpu", dtype=torch.bfloat16):
        output = model(batch_x)
        loss = criterion(output, batch_y)

    scaler.scale(loss).backward()
    scaler.step(optimizer)
    scaler.update()

# ─── Verificar soporte de dtypes ───
print("BF16 supported:", torch.xpu.is_bf16_supported())
print("FP16 supported:", torch.xpu.get_device_properties(0).has_fp16)
```

---

## DataLoader con GPU affinity

```python
from torch.utils.data import DataLoader

# ─── Pin memory para transferencia rápida a XPU ───
loader = DataLoader(
    dataset,
    batch_size=64,
    shuffle=True,
    pin_memory=True,           # Página bloqueada → más rápido a GPU
    pin_memory_device="xpu",   # Pin memory para XPU (PyTorch 2.6+)
    num_workers=4,
    prefetch_factor=2,
    persistent_workers=True,   # No recrear workers por epoch
)

# ─── Prefetch con stream ───
stream = torch.xpu.Stream()
with torch.xpu.stream(stream):
    for batch_x, batch_y in loader:
        batch_x = batch_x.to("xpu:0", non_blocking=True)
        batch_y = batch_y.to("xpu:0", non_blocking=True)
        torch.xpu.current_stream().wait_stream(stream)
        # ... training ...
```

---

## Migración desde IPEX a PyTorch nativo

```python
# ❌ IPEX (discontinuado):
# import intel_extension_for_pytorch as ipex
# model = ipex.optimize(model)
# x = x.to("xpu")

# ✅ PyTorch nativo (reemplazo directo):
import torch

model = model.to("xpu:0")
model = torch.compile(model)  # Reemplaza ipex.optimize

x = x.to("xpu:0")  # Mismo API, sin IPEX

# ❌ IPEX mixed precision:
# model, optimizer = ipex.optimize(model, optimizer, dtype=torch.bfloat16)

# ✅ PyTorch nativo mixed precision:
# Usar torch.amp.autocast(device_type="xpu", dtype=torch.bfloat16)
```

---

## Multi-GPU training (DDP en Intel)

```python
import torch
import torch.distributed as dist
from torch.nn.parallel import DistributedDataParallel as DDP

def setup(rank, world_size):
    dist.init_process_group(
        backend="c10d",         # Funciona con XPU (c10d es genérico)
        init_method="tcp://localhost:12345",
        rank=rank,
        world_size=world_size,
    )
    torch.xpu.set_device(rank)

def train_ddp(rank, world_size):
    setup(rank, world_size)

    model = MLP().to(f"xpu:{rank}")
    model = DDP(model, device_ids=[rank])

    for batch_x, batch_y in loader:
        batch_x, batch_y = batch_x.to(f"xpu:{rank}"), batch_y.to(f"xpu:{rank}")
        output = model(batch_x)
        loss = criterion(output, batch_y)
        loss.backward()
        optimizer.step()

    dist.destroy_process_group()

# Lanzar: torchrun --nproc_per_node=2 train.py
```

---

## GPU memory management

```python
import torch

# ─── Memoria usada ───
print(f"Allocated: {torch.xpu.memory_allocated(0) / 1024**2:.1f} MB")
print(f"Cached:    {torch.xpu.memory_reserved(0) / 1024**2:.1f} MB")
print(f"Max alloc: {torch.xpu.max_memory_allocated(0) / 1024**2:.1f} MB")

# ─── Vaciar cache ───
torch.xpu.empty_cache()

# ─── Sincronizar ───
torch.xpu.synchronize()

# ─── Peak memory tracking ───
torch.xpu.reset_peak_memory_stats()
model(x)
peak = torch.xpu.max_memory_allocated(0)
print(f"Peak memory: {peak / 1024**2:.1f} MB")
```

---

## Conversión a OpenVINO después del training

```python
import torch
import openvino as ov

model = MLP().to("cpu")  # Bajar a CPU para exportar
model.eval()

# Convertir a IR
example = torch.randn(1, 784)
ov_model = ov.convert_model(model, example_input=example)
ov.save_model(ov_model, "mlp_model.xml", compress_to_fp16=True)
```

---

## Checklist PyTorch XPU

- [ ] `torch.xpu.is_available()` check antes de usar XPU
- [ ] Modelo y datos en el mismo device (`model.to("xpu:0")`)
- [ ] `torch.compile` con backend inductor para optimización
- [ ] AMP con `torch.amp.autocast(device_type="xpu")` para ahorrar VRAM
- [ ] `pin_memory=True` y `pin_memory_device="xpu"` en DataLoader
- [ ] `persistent_workers=True` para evitar recrear workers
- [ ] `torch.xpu.empty_cache()` en puntos de baja memoria
- [ ] Sin imports de IPEX — migrado a PyTorch nativo
- [ ] Conversión a OpenVINO IR post-training para deployment
- [ ] Profiling con PTI (`torch.profiler` + XPU trace) antes de optimizar
