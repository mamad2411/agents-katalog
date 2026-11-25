---
name: virtualbox-rpa
description: Control or observe an authorized VirtualBox VM through the pinned mcp-virtualbox adapter and separate Robot/Python packages; supports detachable user observation.
---

Read `backends/virtualbox/README.md` in the project for installation and commands. Use `backends/virtualbox/client.py` or the stdio server; SPICE URIs and Hyper-V VMConnect are separate backends.

On a Windows host, VAMP MCP servers require administrator privileges. The `vamp-mcp` CLI can request host UAC and start the server in a separate elevated process. Start VS Code with **Run as administrator** for extension-provided servers, or use an administrator terminal for direct server commands. If VAMP tools are missing, verify server elevation and the client's MCP registration. Handle host elevation and guest UAC as separate steps.

List VMs before selecting a target. Start only when requested; default `vm_start` frontend is `separate` so the user can observe via VirtualBox Manager Show. Detach the UI to keep the VM running; do not select shutdown/save/power-off. Starting is not evidence the guest or application is ready.

Keep each scenario as a folder with `.robot`, `workflow.py` and manifest under this backend. Launch Windows programs through Win+R, Linux GNOME through Alt+F2 or another environment-appropriate common launcher rather than desktop icon positions. Send keyboard/mouse to the VM, using coordinates from the VM screenshot, not the host observation window. Mouse clicks require USB tablet plus working host VirtualBox Python SDK. Do not install a guest automation agent just to control input.

For UI success, run existing OCR/YOLO on captured PNGs and check task-specific evidence; no success solely because keys were sent. Keep model workers loaded when vision is used. This backend currently provides capture/input and an observation example, not an already-validated VirtualBox login RPA. Do not claim hardware testing without user evidence.

Credentials belong in a private user entry flow, not CLI arguments, committed recordings or logs. On CAPTCHA/additional verification, pause for the user and recheck after completion. Do not automatically retry credential submission.

For unattended VM creation, ask for the host ISO path if missing, disclose public defaults `vboxuser` / `password123!`, then call `vm_create` once. It detects supported ISO types, creates a new VM and starts a deterministic installer; no AI polling loop is needed for OS installation. Do not call again merely because the response says installation_started. Preserve partial failures and inspect the journal. Recorder setup is wired to Debian postinstall / Windows first desktop login; installed flags remain unverified until checked. See `docs/GUEST_RECORDER.md`.

VAMP's VS Code extension bundles basic VirtualBox tools and offers a managed host venv; it does not bundle the full vision stack or the SPICE MCP branch. Marketplace publish requires a publisher account; existing editor GitHub login is not evidence of publisher access.

Guest-native resolution is 1920x1080 for both GNOME Debian and Windows; OS/browser scale 100%. Use Scaled Mode only for the host frontend, with guest auto-resize disabled. See `docs/VM_DISPLAY.md`. `vm_configure_display` checks screenshot dimensions; do not claim resolution is correct from a sent hint alone. Windows `vm_insert_guest_additions` inserts media only; tell the user to install VBoxWindowsAdditions.exe, approve UAC and reboot. Never replace an occupied storage slot. For explicitly requested automated Packer Windows setup, install verified vendor Guest Additions automatically, reboot, wait 60 seconds and finish post-install setup before reporting completion.

Read `docs/GUEST_AUTOMATION.md` for first-run setup, current resource profiles, network mirror scripts, per-login guest resolution hooks, recorder shares and snapshots. First use: ask about setup and ISO/specs, Debian default, Windows explicit opt-in plus user activation/license notice. `preflight_only:true` never creates a VM; unsupported ISO/host detection is a blocker, not success.

At each new session ask once whether the user wants a snapshot and explain disk/RAM space. A refusal persists for that session. Snapshots preserve their capture time, not later changes. Restore only after explicit target/loss confirmation on an already powered-off VM; never auto-stop or claim an initial snapshot exists.

Guest display hooks run every user login, never once-only. Windows reads registry and tests/applies user32 modes; GNOME uses session Mutter D-Bus at scale 1. Read result.json and actual capture dimensions. Do not use stale registry values or a sent hint as success. No ActiveX installation is involved.

Recorder UI shows SHARED WITH HOST or LOCAL ONLY. Prepare VAMPRecords with `vm_recording_share`, verify mounting and read the chosen saved source with inspect; never execute recordings while importing. Modified guest recorder is GPL-3.0. For GNOME global recording use Xorg; Wayland GUI startup alone does not prove global input recording works. Debian non-sudo users need `su root` and install-debian-root.sh. CD-ROM APT entries must be removed by configure-debian-mirrors.py before apt update. Only send shell commands after observing terminal/root state; user focus changes can invalidate a previously observed editor.

For execution evidence use `docs/EXECUTION_HISTORY.md`. The Robot RecordingListener optionally records native VM video at 640x360/5fps with 180s/20MB limits, and stores screenshot paths/task results in host SQLite. This is separate from GUI action recording. Use vm_run_history and explicit vm_run_artifact show_image only when needed. Preserve Robot status separately from evidence capture completion; no video artifact means no verified recording. Do not start recording implicitly, overwrite another active recording, or create snapshots for this feature.

For repeated work, prefer a compatible saved RPA and local outcome checks. Return compact status and evidence paths on success, not full OCR/YOLO output, images, logs or source. Escalate to a targeted observation only for ambiguity, failure, UI changes or requested inspection; avoid unchanged-frame LLM polling. Follow [the low-token output policy](../../../docs/LOW_TOKEN_AUTOMATION.md).

New or repaired GUI RPAs must include task-specific local OCR/YOLO verification in Python, called and asserted by Robot, rather than using LLM screenshot reading as the normal verifier. Check artifacts too when produced; dispatch alone stays unverified. See [the authoring checklist](../../../docs/LOW_TOKEN_AUTOMATION.md#새-gui-rpa를-작성할-때).

New VM creation now runs the shared HashiCorp Packer backend. Explain the managed CLI/plugin downloads and separate golden-image/live-disk storage. Use vm_packer_prepare for preparation, vm_create once for a queued build and vm_golden_images for compact status/paths. Do not infer completion from installation_started. Debian automatically logs into the public sandbox account; post-install setup waits 60 seconds after first reboot. vm_golden_image_delete must first inspect path/size and obtain explicit deletion consent; active builds and attached partial-build disks cannot be deleted.
