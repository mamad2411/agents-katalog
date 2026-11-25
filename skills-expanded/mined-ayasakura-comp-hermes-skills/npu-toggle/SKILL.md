---
name: npu-toggle
description: Enable or disable the AMD XDNA NPU on this Strix Halo box by switching the saved GRUB boot entry (IOMMU on vs amd_iommu=off), and report NPU/boot-mode status. Use when the user asks to 開/關 NPU、enable/disable NPU、切 NPU 模式、GPU 全速模式、update grub for NPU, or asks whether the NPU is on.
compatibility: Ubuntu GRUB with GRUB_DEFAULT=saved and /etc/grub.d/41_boot_modes (entries npu-mode / gpu-max); passwordless sudo; XRT at /opt/xilinx/xrt.
---

# NPU toggle (GRUB boot mode)

The NPU driver `amdxdna` needs the IOMMU on. `amd_iommu=off` gives the GPU ~5% more
LLM throughput (measured 2026-09-25: prefill 1401→1338, decode 81.1→77.2 tok/s) but
the NPU then fails to probe (`IOMMU is off, require carveout memory`, ret -19).
The GPU is already in an identity IOMMU domain, so `iommu=pt` does NOT recover the loss —
the only choice is which mode to boot.

| Mode | GRUB id | Kernel args | NPU | GPU |
|---|---|---|---|---|
| enable  | `npu-mode` | IOMMU on (default) | works, `/dev/accel/accel0` | ~5% slower |
| disable | `gpu-max`  | `amd_iommu=off`   | unusable | full speed |

## Run

```bash
S=~/.claude/skills/npu-toggle/scripts/npu-toggle.sh   # also ~/bin/npu-toggle
$S status                  # saved entry, running mode, /dev/accel/accel0
$S enable                  # default boot -> npu-mode
$S disable                 # default boot -> gpu-max
$S disable --once          # only the next boot uses gpu-max, then back to saved
$S enable --reboot         # set + reboot in 1 minute (cancel: sudo shutdown -c)
```

Only use `--reboot` when the user explicitly asks to reboot. Otherwise tell them the
change takes effect on the next reboot. A reboot kills this session and every running
service (qwen-mtp etc.), so announce it before it happens.

## After a reboot, verify

```bash
cat /proc/cmdline                                    # amd_iommu=off present only in gpu-max
ls /dev/accel/                                       # accel0 only in npu-mode
sudo journalctl -k -b | grep amdxdna                 # npu-mode: "PASID address mode enabled"
source /opt/xilinx/xrt/setup.sh && xrt-smi validate  # npu-mode: gemm ~51 TOPS PASSED
```

`qwen-mtp` needs `~/.cache/llama-slots/` to exist or it crash-loops after boot
(`--slot-save-path ... not a directory`); `mkdir -p` it if the dir is gone.

## Setup it relies on (already installed 2026-09-25)

- `/etc/default/grub`: `GRUB_DEFAULT=saved`; `GRUB_CMDLINE_LINUX_DEFAULT` has **no** `amd_iommu` flag.
  Backups: `/etc/default/grub.bak-20260925`, `/etc/default/grub.bak-bootmodes-20260925`.
- `/etc/grub.d/41_boot_modes`: the two menu entries. They boot `/boot/vmlinuz` and
  `/boot/initrd.img` (symlinks), so kernel upgrades need no edits. To change kernel args
  for both modes, edit this file and run `sudo update-grub`.
- The script runs `update-grub` itself if an entry is missing from `grub.cfg`, and exits
  with an error if the setup above is missing. Don't let it silently fall back to editing
  `GRUB_CMDLINE_LINUX_DEFAULT`.
