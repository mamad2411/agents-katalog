---
name: spice-rpa-install
description: Set up host-side SPICE RPA dependencies for a manual or AI-assisted install using one CPU, NVIDIA, AMD ROCm, Apple MPS, Ascend NPU or Intel NPU requirements profile. Use for environment setup, not guest package updates or running login RPAs.
---

Read repository `README.md` and `docs/INSTALL.md`. Requirements install into the controller host, not the Debian/Windows guest. The only project hardware validation is Ubuntu + NVIDIA; other profiles are unvalidated. Do not install all profiles or claim hardware support from requirements alone.

Identify host OS/architecture/Python, native SpiceClientGLib/PyGObject, existing environments and accelerator runtime. Guest Windows 11 does not imply a Windows controller. Use the host Python that matches GI; `--system-site-packages` cannot bridge different Python ABIs.

Select exactly one `requirements-{nvidia,cpu,amd-rocm,apple,npu-ascend,npu-intel}.txt`. The NVIDIA profile reflects the tested Torch versions. AMD requires compatible ROCm, Ascend requires matching CANN/TorchNPU, Intel requires its NPU driver/OpenVINO, and Apple uses MPS GPU (not Neural Engine). The documentation gives manual pip/uv commands and official runtime references.

Prepare `.venv` with matching native GI, then install the chosen profile. Keep PaddleOCR in `.venv-ocr` with Python 3.12 and `requirements-ocr.txt`. Install uv inside the controller venv if needed. Download/verify models with `scripts/download_models.py`. Preserve a working environment and unrelated user changes; do not replace working CUDA packages with ROCm to investigate compatibility.

A user request to install dependencies authorizes the relevant host dependency setup. It does not authorize guest login submissions, apt update RPAs, credential probing, reboots, or replacing device drivers beyond the requested scope. If a required runtime/OS/Python combination is unavailable, explain that concrete dependency rather than silently choosing another device and claiming acceleration.

Unless the user asks for device testing, do not run AMD/Apple/NPU inference or full live RPA tests. Import/config checks and Robot dry-runs can be used to validate installation syntax; report their actual scope. The current project owner explicitly requested no extra platform testing.

Report selected profile, interpreter/venv locations, installed vs missing native dependencies, and any remaining unverified runtime/model compatibility. Never label installation or dry-run success as a successful hardware or VM workflow test.
