---
name: spice-vm-update
description: "Run the Debian apt update RPA package through Robot Framework and Python SPICE keyboard control, verifying terminal/root/apt outcomes with OCR only."
---

Work from `/home/ssh1032007/spice_kvm_based_rpa` or the checkout. The package is `agent/rpas/debian_update/`: `manifest.json`, `run.robot`, `workflow.py`. Read `agent/rpas/README.md` for the shared contract and `docs/VM_UPDATE.md` for terminal troubleshooting.

Run `.venv/bin/python scripts/run_rpa.py debian_update`. Or invoke Robot directly: `.venv/bin/python -m robot --outputdir artifacts/rpas/debian_update agent/rpas/debian_update/run.robot`. The Robot file invokes the package Python keyword, publishes a compact result, and requires `status == succeeded`.

Read `artifacts/rpas/debian_update/summary.json` first. Full OCR events remain in `artifacts/rpas/debian_update/update/result.json`. `report.html`/`log.html` contain Robot evidence. `VM_CONFIG` and `APT_TIMEOUT` are Robot variables (`--var NAME:VALUE`). If overriding `SPICE_URI`, match the configuration URI. Existing `rpa.py vm-update` and `tests/vm_update.robot` remain compatible.

This refreshes indexes with `apt update`. Upgrades, installs, source-list changes and reboot require a corresponding user task. The sandbox is `debian13` at `spice://127.0.0.1:5900`, hostname `debian`. `config/sandbox-vm.json` intentionally contains the owner's publicly distributable test root password. Use it only for this configured sandbox and do not treat private website credentials as public.

Python opens the terminal via Ctrl+Alt+T with an Alt+F2 → `gnome-terminal --maximize` fallback, verifies the terminal, sends `su root` only in a verified shell, waits for OCR of `Password:`, and verifies root prompt plus UID. Do not auto-retry failed authentication.

Use OCR text only for verification. Do not call an image viewer, multimodal model, SSH, guest agent or host apt. Screenshots are local PaddleOCR inputs and evidence. Escaped printf markers distinguish actual results from echoed commands. Missing markers/timeouts are unverified, not success.

Report `succeeded`, `completed_with_warnings`, `failed` or the exact unverified state. The completed flow sends `exit` and reports `root_shell_exited`; timeout can leave apt/root active, so inspect OCR before more input. Do not modify repositories merely to turn a failed test green.

Future recording hooks belong around Robot tasks/keywords (`--listener`); the current package does not implement video recording.

For a genuine workflow/locator failure within an authorized repair task, use `spice-rpa-repair/SKILL.md` to diagnose the saved run before changing coordinates. Preserve this skill's verification and credential boundaries; a system error or user handoff is not automatically a broken locator.

Model lifetime: real SPICE connections auto-start detached YOLO/OCR processes. Keep them running across RPA/skill calls; do not stop/restart after each task. Use `scripts/model_service.py status` or explicit start/stop only when needed. See `docs/MODEL_BACKGROUND.md`; no systemd service is installed. Hyper-V uses its separate experimental `hyperv-rpa` skill/backend, not SPICE transport.
