---
name: nvidia-cuda-workflows
description: Develop and verify bounded CUDA, GPU Python and video-encoding workloads while preserving a desktop GPU's availability.
---

# NVIDIA and CUDA

Inspect the GPU, active driver, installed toolkit and workload requirements.
The CUDA version displayed by `nvidia-smi` is a driver capability, not proof
of an installed development toolkit.

- Prefer distribution-managed drivers. Do not mix runfiles, foreign-release
  repositories or driver branches casually.
- Check native host compiler compatibility and select it within the project.
  Do not replace the system GCC or assume a particular GPU architecture.
- Use a framework's documented runtime wheels inside its environment. A system
  CUDA toolkit is not required merely to run many prebuilt GPU wheels.
- Verify allocation, actual device execution, synchronization and correct
  output. A silent CPU fallback is not working CUDA.
- Keep tests representative and bounded. Leave VRAM for the desktop and other
  applications; never kill another job or change clocks/power settings as a shortcut.
- Diagnose GPU errors with scoped workload/kernel evidence, not stress tests
  or certificate/sandbox bypasses.
- Use generated frames to test NVENC unless the user requested a recording.
  Do not capture or upload an unrelated desktop.
