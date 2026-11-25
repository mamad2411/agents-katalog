---
name: "gpu-optimization-patterns"
description: "GPU optimization patterns with code: memory profiling and budgeting, torch.compile modes, torch.profiler bottleneck analysis, BF16 and FP16 mixed precision, 4-bit quantization with bitsandbytes, and DataLoader tuning. Use when a GPU workload is slow or runs out of memory."
---

# GPU Optimization Patterns

Expert patterns for memory management, torch.compile, profiling, quantization, and kernel optimization.

## Pattern 1: GPU Memory Profiling and Budgeting

Profile and track GPU memory usage with explicit memory math.

```python
import torch

def memory_report(label: str = ""):
    allocated = torch.cuda.memory_allocated() / 1e9
    reserved = torch.cuda.memory_reserved() / 1e9
    print(f"[{label}] Allocated: {allocated:.2f} GB | Reserved: {reserved:.2f} GB")

def estimate_model_memory(num_params: int, dtype: torch.dtype = torch.float32) -> dict:
    """Estimate memory requirements for a model."""
    bytes_per_param = {
        torch.float32: 4,
        torch.float16: 2,
        torch.bfloat16: 2,
        torch.int8: 1,
    }[dtype]

    param_memory_gb = num_params * bytes_per_param / 1e9

    # Adam optimizer states: 2 fp32 states per param
    optimizer_memory_gb = num_params * 8 / 1e9  # fp32 moment1 + moment2

    # Gradients: same dtype as params
    gradient_memory_gb = num_params * bytes_per_param / 1e9

    return {
        "parameters_gb": round(param_memory_gb, 2),
        "optimizer_gb": round(optimizer_memory_gb, 2),
        "gradients_gb": round(gradient_memory_gb, 2),
        "total_training_gb": round(param_memory_gb + optimizer_memory_gb + gradient_memory_gb, 2),
        "inference_only_gb": round(param_memory_gb, 2),
    }

# Example: 7B parameter model
print(estimate_model_memory(7_000_000_000, torch.bfloat16))
# {'parameters_gb': 14.0, 'optimizer_gb': 56.0, 'gradients_gb': 14.0, 'total_training_gb': 84.0}
# ^ This is why 7B training requires FSDP or DeepSpeed ZeRO

# Track peak memory in training loop
torch.cuda.reset_peak_memory_stats()
memory_report("before forward")
output = model(x)
memory_report("after forward")
loss.backward()
memory_report("after backward")
print(f"Peak: {torch.cuda.max_memory_allocated()/1e9:.2f} GB")
```

## Pattern 2: torch.compile Modes

Apply torch.compile with appropriate mode for training vs inference.

```python
import torch

# Training: default mode is usually best (compilation time vs runtime tradeoff)
model = MyTransformerModel().cuda()
compiled_model = torch.compile(model, mode="default")

# Inference: reduce-overhead uses CUDA graphs, eliminates Python dispatch overhead
inference_model = torch.compile(model, mode="reduce-overhead")

# Maximum optimization: max-autotune runs autotuning for best tiling/layout
# Takes significantly longer to compile but yields best throughput
tuned_model = torch.compile(model, mode="max-autotune")

# Benchmarking compile vs eager
import time

def benchmark(model, x, n_iters=100, warmup=10):
    # Warmup
    for _ in range(warmup):
        _ = model(x)
    torch.cuda.synchronize()

    start = time.perf_counter()
    for _ in range(n_iters):
        _ = model(x)
    torch.cuda.synchronize()
    elapsed = time.perf_counter() - start
    return elapsed / n_iters * 1000  # ms per iteration

x = torch.randn(32, 512, device='cuda')

eager_model = MyTransformerModel().cuda().eval()
compiled = torch.compile(eager_model, mode="default")

# Note: first call triggers compilation — warmup handles this
eager_ms = benchmark(eager_model, x)
compiled_ms = benchmark(compiled, x)
print(f"Eager: {eager_ms:.2f}ms | Compiled: {compiled_ms:.2f}ms | Speedup: {eager_ms/compiled_ms:.2f}x")

# Debug graph breaks (breaks reduce compilation effectiveness)
explanation = torch._dynamo.explain(eager_model)(x)
print(explanation.break_reasons)
```

## Pattern 3: torch.profiler for Bottleneck Analysis

Profile training steps to find CPU/GPU overlap issues and slow kernels.

```python
import torch
from torch.profiler import profile, record_function, ProfilerActivity

def profile_training_step(model, loader, optimizer, num_steps=5):
    model.train()

    with profile(
        activities=[ProfilerActivity.CPU, ProfilerActivity.CUDA],
        schedule=torch.profiler.schedule(
            wait=1,      # skip first step (JIT warmup)
            warmup=1,    # profile but don't record
            active=3,    # record 3 steps
        ),
        on_trace_ready=torch.profiler.tensorboard_trace_handler('./profiler_log'),
        record_shapes=True,
        profile_memory=True,
        with_stack=True,
    ) as prof:
        for step, (x, y) in enumerate(loader):
            if step >= num_steps:
                break

            with record_function("data_to_gpu"):
                x, y = x.cuda(non_blocking=True), y.cuda(non_blocking=True)

            with record_function("forward"):
                logits = model(x)
                loss = criterion(logits, y)

            with record_function("backward"):
                optimizer.zero_grad()
                loss.backward()

            with record_function("optimizer_step"):
                optimizer.step()

            prof.step()

    # Print top kernels by CUDA time
    print(prof.key_averages().table(
        sort_by="cuda_time_total",
        row_limit=15
    ))

    # Key metrics to look for:
    # - High CPU time relative to CUDA time → Python overhead (use torch.compile)
    # - DataLoader showing up high → increase num_workers or use prefetching
    # - Small kernel launches → kernel fusion opportunity
```

## Pattern 4: BF16/FP16 Mixed Precision

Reduce memory and increase throughput with mixed precision training.

```python
import torch
from torch.cuda.amp import autocast, GradScaler

# BF16 (preferred on A100/H100 — no loss scaling needed)
def train_bf16(model, loader, optimizer, epochs):
    model = model.cuda()
    for epoch in range(epochs):
        for x, y in loader:
            x, y = x.cuda(), y.cuda()
            optimizer.zero_grad()

            # BF16 doesn't need GradScaler — stable range matches FP32
            with autocast(device_type='cuda', dtype=torch.bfloat16):
                logits = model(x)
                loss = criterion(logits, y)

            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()

# FP16 (required on Volta/Turing GPUs, needs GradScaler)
def train_fp16(model, loader, optimizer, epochs):
    scaler = GradScaler()
    for epoch in range(epochs):
        for x, y in loader:
            x, y = x.cuda(), y.cuda()
            optimizer.zero_grad()

            with autocast(device_type='cuda', dtype=torch.float16):
                logits = model(x)
                loss = criterion(logits, y)

            # Scale loss to prevent FP16 underflow
            scaler.scale(loss).backward()
            scaler.unscale_(optimizer)
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            scaler.step(optimizer)
            scaler.update()  # adjusts scale factor based on overflow detection

# Memory savings: 7B BF16 = 14 GB vs 7B FP32 = 28 GB
```

## Pattern 5: 4-bit Quantization with bitsandbytes

Load large models in 4-bit precision for inference or QLoRA fine-tuning.

```python
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
import torch

# NF4 quantization configuration (best for LLM weights)
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",          # NF4 > FP4 for normal-distributed weights
    bnb_4bit_compute_dtype=torch.bfloat16,  # compute in BF16, store in 4-bit
    bnb_4bit_use_double_quant=True,     # quantize the quantization constants too
)

model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-2-7b-hf",
    quantization_config=bnb_config,
    device_map="auto",  # auto-distribute across available GPUs
)

# Memory: 7B fp16 = 14 GB → 7B int4 = ~3.5 GB (fits on a single 4090)

# Verify memory usage
for name, param in model.named_parameters():
    if 'weight' in name:
        print(f"{name}: {param.dtype}, size={param.data.nbytes/1e6:.1f} MB")
        break
```

## Pattern 6: DataLoader Optimization for GPU Throughput

Prevent data loading from starving GPU compute.

```python
from torch.utils.data import DataLoader
import torch

def optimal_dataloader(dataset, batch_size: int, is_training: bool = True):
    """DataLoader configuration for maximum GPU throughput."""
    return DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=is_training,
        num_workers=4,           # tune: 4 is good for most cases (not too many to cause overhead)
        pin_memory=True,         # page-locked memory → faster CPU→GPU transfer
        prefetch_factor=2,       # prefetch 2 batches per worker ahead of time
        persistent_workers=True, # keep worker processes alive between epochs (~10% faster)
        drop_last=is_training,   # consistent batch sizes for fixed-shape compilation
    )

# For very large datasets: pre-tokenize and cache as PyTorch tensors
# memmap for HDF5/NumPy → avoids Python object overhead in __getitem__
import numpy as np

class FastMemmapDataset(torch.utils.data.Dataset):
    def __init__(self, path: str):
        self.data = np.load(path, mmap_mode='r')  # memory-mapped: no full load

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        x = torch.from_numpy(self.data[idx].copy()).float()
        return x
```

## Anti-Patterns

### Anti-Pattern 1: Profiling Without Warmup
The first forward pass triggers kernel compilation. Profile results from step 0 are unrepresentative. Always use at least 10 warmup steps before profiling.

### Anti-Pattern 2: torch.cuda.empty_cache() in Training Loop
`empty_cache()` releases reserved memory back to the allocator pool. Calling it every step causes the allocator to reallocate memory next step — this is slower, not faster. Only call it when you're switching workloads (e.g., training to inference).

### Anti-Pattern 3: FP16 for LLM Training on A100
A100 has native BF16 hardware support (256 TFLOPs). FP16 on A100 requires GradScaler overhead and is more prone to overflow. BF16 matches FP32 in stability. Always use BF16 on Ampere+ hardware.

### Anti-Pattern 4: Small Batch Size Without Gradient Accumulation
Underloading the GPU with small batches wastes compute. If your batch_size is limited by memory, use gradient accumulation: accumulate N steps before `optimizer.step()`. Effective batch size = batch_size × N.

### Anti-Pattern 5: torch.compile on Dynamic Shapes
`torch.compile` compiles a specific input shape. Dynamic shapes cause recompilation or graph breaks. Use `torch.compile(dynamic=True)` or pad inputs to fixed shapes for variable-length data (e.g., text with padding to power-of-2 lengths).
