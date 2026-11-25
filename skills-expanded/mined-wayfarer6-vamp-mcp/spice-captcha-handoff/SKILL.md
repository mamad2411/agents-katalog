---
name: spice-captcha-handoff
description: "Run the Robot/Python CAPTCHA handoff package to detect multilingual verification instructions in a SPICE VM, pause automation for the user, and recheck after manual completion."
---

Work from `/home/ssh1032007/spice_kvm_based_rpa` or the checkout. The package is `agent/rpas/captcha_handoff/`: `manifest.json`, `run.robot`, `workflow.py`. Run `.venv/bin/python scripts/run_rpa.py captcha_handoff`. It checks the current screen without navigating, clicking or typing. `--var LANGUAGES:ko,en,ja,zh` is the default. Read `artifacts/rpas/captcha_handoff/summary.json`.

Local PaddleOCR detects instructional phrases, not challenge solutions. When OCR-only work is requested, read JSON rather than invoking an image viewer or multimodal model. The login package runs the same checks before credential entry and after submission.

For `needs_user_captcha` or `needs_user_verification`, stop automated input and tell the user:

“보안 확인 화면이 감지되어 자동화를 멈췄습니다. VM 창에서 CAPTCHA나 추가 인증을 직접 완료한 뒤 ‘완료’라고 알려주세요. 완료 후 제가 화면 상태를 다시 확인하겠습니다.”

Robot publishes the handoff result and marks the task SKIP. Teardown releases its SPICE connection and lock so the user can reconnect their viewer. Leave the page as it is. Do not poll continuously, reload, resubmit credentials, click challenge controls, extract answers or route the challenge to another model/service.

After the user explicitly reports completion, run this package once again. If instructions remain, retain the handoff. `no_challenge_text` means no known instruction was recognized; it does not prove clearance or successful login. Require positive OCR evidence of the expected next screen before resuming. Never navigate back to the login URL merely to recheck a challenge.

Purely graphical challenges, missing fonts and OCR errors can be missed. Report unverified states honestly. Existing `rpa.py check-verification` remains compatible. Future listener-based recording must exclude private credential/verification entry; no built-in recorder is currently provided.

Model lifetime: real SPICE connections auto-start detached YOLO/OCR processes. Keep them running across RPA/skill calls; do not stop/restart after each task. Use `scripts/model_service.py status` or explicit start/stop only when needed. See `docs/MODEL_BACKGROUND.md`; no systemd service is installed. Hyper-V uses its separate experimental `hyperv-rpa` skill/backend, not SPICE transport.
