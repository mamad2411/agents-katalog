---
name: spice-vm-rpa
description: "Control an authorized SPICE VM through packaged Robot Framework RPAs backed by Python SPICE, YOLO and Korean, English, Japanese, Chinese OCR. Use for visual guest interaction without installing a guest automation agent."
---

Work from `/home/ssh1032007/spice_kvm_based_rpa` or the repository checkout. Read `agent/rpas/README.md` for the package contract. Every RPA owns a manifest, one or more `.robot` entrypoints and a Python `workflow.py`; shared SPICE/OCR engines stay at repository root.

## Packaged entrypoints

| Task | Robot file | Python library | Command |
| --- | --- | --- | --- |
| Inspect or control desktop | `agent/rpas/desktop_control/run.robot` | `agent/rpas/desktop_control/workflow.py` | `.venv/bin/python scripts/run_rpa.py desktop_control` |
| Launch Firefox | `agent/rpas/firefox_launch/run.robot` | `agent/rpas/firefox_launch/workflow.py` | `.venv/bin/python scripts/run_rpa.py firefox_launch` |
| Visit Naver | `agent/rpas/firefox_naver/run.robot` | `agent/rpas/firefox_naver/workflow.py` | `.venv/bin/python scripts/run_rpa.py firefox_naver` |

Choose one package/entrypoint. Never execute the entire `rpas` directory except with `--dryrun`. Results are in `artifacts/rpas/<id>/summary.json`; read full details only for an unresolved failure. `report.html` and `log.html` hold Robot evidence. Existing CLI commands remain compatibility options.

## Observe and act

Targets are Debian `debian13` and Windows 11 `windows-RPA`, both using a 1920×1080 baseline. Existing GNOME launch/login/update workflows are Debian-specific; Windows flows are not implemented/validated. SPICE ports are auto-assigned: inspect the actual running VM URI instead of assuming the development default `spice://127.0.0.1:5900`. A new client can replace its viewer. Do not reboot/reconfigure the VM to reconnect and do not type concurrently with the user or another RPA.

The desktop package defaults to capture only. Add `--var ACTION:ocr` for OCR-only inspection, `ACTION:analyze` for YOLO+OCR, or `ACTION:screen-info`. Other actions: `click`, `move` (`X`, `Y`), `move-relative` (`DX`, `DY`), `hotkey` (`KEYS:ctrl+l`), `write` (`TEXT`), `click-text`, `find-image`, `click-image` (`TEMPLATE`), `detect`. Set `LANGUAGES:ko,en,ja,zh` or `DEVICE:cpu` as needed.

Read the JSON and inspect a guest image only when the task permits multimodal viewing. Coordinates are native guest pixels, not host-window pixels. YOLO candidate regions are not guaranteed accessible buttons; combine text and scene context. Capture/check after meaningful actions. `executed` means input was dispatched, not that an application succeeded.

Use the login package for private credentials, not generic `TEXT` or Robot argument variables. PyAutoGUI is only for guest image matching; never call its host mouse/keyboard functions.

## Runtime and extension boundaries

SPICE uses the system-Python `.venv`; PaddleOCR uses `.venv-ocr` (Python 3.12). YOLO auto-selects CUDA/ROCm, MPS, Ascend, then CPU; Intel NPU is explicit. Read docs/INSTALL.md for host-specific requirements. Only Ubuntu/NVIDIA has project hardware validation; AMD/Apple/NPU are unvalidated. PaddleOCR currently runs on CPU. Recognition of CJK does not imply CJK text entry; keyboard input assumes US ASCII.

Absolute clicks require CLIENT mode. Relative motion in SERVER mode does not guarantee pixel mapping because of guest acceleration. Stop after two failed attempts and inspect the cause before continuing.

Use Robot keyword boundaries and `scripts/run_rpa.py --listener <listener>` for future recording integration. No built-in video/macro recorder currently exists. A screen recorder must reuse the existing SPICE session. Do not claim automation is undetectable.

For a genuine workflow/locator failure within an authorized repair task, use `spice-rpa-repair/SKILL.md` to diagnose the saved run before changing coordinates. Preserve this skill's verification and credential boundaries; a system error or user handoff is not automatically a broken locator.

For newly authored or repaired startup steps, use a shared OS launcher: Windows Win+R plus an executable/command; Debian GNOME Alt+F2 plus a command. Avoid desktop-icon coordinates because desktops differ by user. For manual recorder imports or package scaffolding, use `spice-recording-convert/SKILL.md` and the public `scripts/convert_recording.py` / `scripts/new_rpa.py` tools.

Model lifetime: the Linux Python MCP server preloads detached YOLO/OCR workers at startup unless `VAMP_PRELOAD_MODELS=0`; direct perception requests start required workers lazily. Keep them running across RPA/skill calls; do not stop/restart after each task. Use `scripts/model_service.py status` or explicit start/stop only when needed. See `docs/MODEL_BACKGROUND.md`; no systemd service is installed. Hyper-V uses its separate experimental `hyperv-rpa` skill/backend, not SPICE transport.

For repeated work, prefer a compatible saved RPA and local outcome checks. Return compact status and evidence paths on success, not full OCR/YOLO output, images, logs or source. Escalate to a targeted observation only for ambiguity, failure, UI changes or requested inspection; avoid unchanged-frame LLM polling. Follow [the low-token output policy](../../../docs/LOW_TOKEN_AUTOMATION.md).

When authoring or repairing a GUI RPA, include task-specific local OCR/YOLO verification in Python and a Robot assertion of its result by default. Add produced-file/content checks when available. Keep an unconfigured or unverified status until an actual outcome is checked; use [the authoring checklist](../../../docs/LOW_TOKEN_AUTOMATION.md#새-gui-rpa를-작성할-때).
