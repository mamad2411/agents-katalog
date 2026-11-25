---
name: gpu-first-execution
description: Verify and enforce actual NVIDIA CUDA GPU execution for ML training, inference, evaluation, or benchmarking when GPU use is required. Unexpected CPU fallback is a defect.
---

# Procedure
1. Detect NVIDIA GPU and driver.
2. Verify framework CUDA support.
3. Select the intended device explicitly.
4. Run a minimal GPU smoke test.
5. Run the target workload.
6. Verify actual model/tensor/device placement.
7. Inspect VRAM or utilization when useful.
8. Capture evidence.

`cuda.is_available()` alone is not proof of workload execution.
