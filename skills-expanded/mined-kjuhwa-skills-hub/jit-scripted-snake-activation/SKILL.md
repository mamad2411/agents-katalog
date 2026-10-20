---
name: jit-scripted-snake-activation
description: JIT-scripted Snake activation (x + sin²(αx)/α) for audio codec networks, ~1.4× faster than eager
category: audio
version: 1.0.0
tags: [activation, jit, audio, codec, pytorch]
confidence: medium
source_type: extracted-from-git
source_url: https://github.com/OpenBMB/VoxCPM.git
source_ref: main
source_commit: 13605c5a0e6b99d6d3527a43bd1a4e0e69c8800e
source_project: VoxCPM
source_paths:
  - src/voxcpm/modules/audiovae/audio_vae_v2.py
imported_at: 2026-04-18T00:00:00Z
version_origin: extracted
---

# JIT-scripted Snake activation (x + sin²(x)/α) for audio codecs

## When to use
Use Snake activation instead of ReLU/ELU/SiLU in audio codec networks (encoders, decoders, discriminators) where the network needs to capture periodic patterns in audio signals. The `sin²` term gives the activation a natural frequency bias. JIT-scripting the free function and wrapping it in a module makes it a drop-in replacement for any `nn.ELU()` or `nn.ReLU()` call with a learnable per-channel frequency parameter.

Snake was originally introduced for neural audio synthesis (Ziyn et al., 2021). The ~1.4× speedup over eager comes from TorchScript fusing the arithmetic into fewer CUDA kernels.

## Pattern

### JIT-scripted free function
```python
import torch
import torch.nn as nn

@torch.jit.script
def snake(x: torch.Tensor, alpha: torch.Tensor) -> torch.Tensor:
    """
    Snake activation: x + sin²(α·x) / α
    Numerically stable version avoids division by small alpha.
    """
    return x + (alpha + 1e-9).reciprocal() * torch.sin(alpha * x).pow(2)
```

### Module wrapper with learnable per-channel alpha
```python
class Snake1d(nn.Module):
    """
    Drop-in activation for 1D conv layers (audio).
    alpha is learnable and per-channel (shape: [1, C, 1]).
    """
    def __init__(self, channels: int, alpha_init: float = 1.0):
        super().__init__()
        # One alpha per output channel
        self.alpha = nn.Parameter(
            torch.full((1, channels, 1), alpha_init)
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # x: [B, C, T]
        return snake(x, self.alpha)
```

### Replacing ELU in an audio decoder block
```python
class DecoderBlock(nn.Module):
    def __init__(self, in_channels: int, out_channels: int, stride: int):
        super().__init__()
        self.conv = nn.ConvTranspose1d(
            in_channels, out_channels,
            kernel_size=stride * 2, stride=stride, padding=stride // 2,
        )
        # Replace: nn.ELU()
        # With:
        self.act = Snake1d(out_channels)

    def forward(self, x):
        return self.act(self.conv(x))
```

### Benchmarking snippet
```python
import time

def bench(fn, x, n=1000):
    torch.cuda.synchronize()
    t0 = time.perf_counter()
    for _ in range(n):
        fn(x)
    torch.cuda.synchronize()
    return (time.perf_counter() - t0) / n * 1000  # ms per call

x = torch.randn(8, 256, 4096, device="cuda")
alpha = torch.ones(1, 256, 1, device="cuda")

eager_ms  = bench(lambda x: x + (alpha + 1e-9).reciprocal() * torch.sin(alpha * x).pow(2), x)
script_ms = bench(lambda x: snake(x, alpha), x)
print(f"Eager: {eager_ms:.2f} ms  |  JIT: {script_ms:.2f} ms  |  Speedup: {eager_ms/script_ms:.2f}×")
```

## Source reference
- Upstream: `OpenBMB/VoxCPM` @ `main` / `13605c5a`
- Key files:
  - `src/voxcpm/modules/audiovae/audio_vae_v2.py:50-65` — `@torch.jit.script snake()` and `Snake1d` module definition

## Notes
- The `1e-9` epsilon in `(alpha + 1e-9).reciprocal()` prevents division by zero if alpha is initialized at or near zero; keep it even if your init is nonzero.
- Snake works best for audio; for image or text tasks, standard activations usually perform comparably at lower implementation complexity.
- Confidence is medium because the 1.4× speedup claim is hardware-dependent — benchmark on your own GPU/batch size before committing.
