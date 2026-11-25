---
name: hyperv-rpa
description: Use the separate Windows Hyper-V RPA backend to inspect/start a requested VM and open vmconnect.exe with normal UAC elevation. Use for Hyper-V host code and console launch, not SPICE connections or claims of completed RDP input automation.
---

Read `backends/hyperv/README.md`. This backend is separate from Linux/SPICE `agent/rpas/`. Current capabilities are exact VM selection, optional startup, normal administrator elevation and VMConnect process launch. RDP frame/input automation is not implemented. VMConnect, inventory and bidirectional file exchange were verified in the nested Windows 11 Pro lab on 2026-11-16; physical Windows hardware remains untested. See `docs/VALIDATION.md` for evidence and limits.

Run only on the user's Windows Hyper-V host. Use `.venv-hyperv` and `backends/hyperv/requirements.txt`; do not install Linux GI or reuse `mcp_vm/transports/spice_robot.py`. Current Ubuntu `windows-RPA` is a KVM guest, not evidence of a working Hyper-V host.

Robot entrypoint: `backends/hyperv/rpas/console/run.robot`; Python: `workflow.py` plus `backends/hyperv/scripts/vmconnect.py`; elevated native worker: `Open-HyperVConsole.ps1`. Supply the exact `VM_NAME`, optional `SERVER` and explicit `START_VM:True` only when startup is requested. Do not change a saved/paused VM state automatically.

The Python launcher requests standard Windows UAC approval via runas if not already elevated. When the user explicitly authorizes UAC interaction for the current task, the agent may click Yes on the standard UAC consent prompt after verifying the requested application and operation match the authorized task. This includes explicitly requested nested Hyper-V lab provisioning. Existing authorization persists for that task; do not ask again for the same authorized operation. Otherwise let the user approve it. Do not disable UAC, weaken policies, or install Hyper-V outside the requested scope. If credentials are required and are not available through an authorized credential workflow, ask the user to enter them. The worker uses structured data, matches the VM name exactly and starts only Off VMs when explicitly enabled.

Read summary status. `launch_requested` is process launch plus VM Running, not verified guest access; `guest_connection_verified` remains false. Do not announce login/RPA success from opening VMConnect. On timeout inspect the existing console/UAC state before another launch.

Future RDP implementations need their own screenshot/input adapter and verified guest-area coordinates. Reuse Robot task logic and OCR/YOLO where practical; do not route Hyper-V commands into a SPICE URI. Windows applications start through Win+R and executable names, not desktop-icon coordinates. Exclude credential entry from macro recording. Handle UAC consent as a task-specific action under the authorization rule above; do not include reusable UAC auto-approval in recorded macros.
