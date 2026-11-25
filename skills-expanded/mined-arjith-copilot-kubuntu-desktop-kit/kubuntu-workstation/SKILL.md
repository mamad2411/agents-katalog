---
name: kubuntu-workstation
description: Diagnose and configure a Kubuntu workstation using current hardware, package and session evidence while preserving data, security and existing work.
---

# Kubuntu workstation

Inspect the current OS, desktop session, relevant hardware, package state and
symptom before changing settings. Treat saved inventories as historical context,
not permanent facts.

- Prefer Ubuntu packages and official KDE/NVIDIA documentation. Simulate package
  changes and check removals, compatibility and reboot requirements.
- Keep changes per-user where practical. Do not reboot, log out, repartition,
  disable security or terminate unrelated processes without explicit approval.
- Do not add backups, encryption, firewall rules or extra services to an
  unrelated setup request. Explain any prerequisite rather than silently adding it.
- Compare current and previous boot logs for freezes. Distinguish GPU faults,
  memory pressure, thermal problems, storage errors and app-only failures.
- Keep credentials and private logs out of reports. A sanitized summary is
  preferable to a full journal dump.
- Verify the requested behavior, not merely package installation or a running PID.

Use `kde-desktop-integration`, `python-uv-development` or
`nvidia-cuda-workflows` for their narrower jobs. Explain Windows-to-Linux
differences when useful; do not equate virtual workspaces with separate users.
