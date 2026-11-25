---
name: dell-monitor-kvm-setup
description: Recall and troubleshoot Arthur's documented Dell U3225QE multi-computer hub, KVM, DisplayLink, audio, and peripheral topology. Use for Arthur's setup or when someone explicitly asks about this published workstation; do not assume the same wiring for other Dell desks.
---

# Dell monitor and KVM setup

Read [references/workstation-inventory.md](references/workstation-inventory.md) before answering questions about this workstation. It is the authoritative inventory for the package and contains the topology, evidence labels, dated observations, unresolved details, and troubleshooting lessons.

Identify the occupied docking path rather than inferring wiring from the laptop identity. Laptop positions are interchangeable. Separate host video, USB data, charging, DisplayLink, and audio paths when reasoning about failures; a USB-C connector alone does not establish a cable's protocol or direction.

Preserve the reference's evidence labels:

- **Verified** means observed in a dated inspection or checked against the cited manufacturer specification.
- **Arthur-reported** means a concrete description that has not been independently inspected.
- **Historical** means useful prior behavior that may not describe the current state.
- **Ordered / untested** and **proposed** must never be presented as installed or compatible.
- **Unknown** must stay unknown until new evidence resolves it.

Inspect relevant devices and settings before changing current state. Preserve headphone output when adjusting microphone input, back up mutable configuration when practical, and verify observable behavior after changes. Do not convert a successful connector fit, valid configuration file, or detected process into a compatibility guarantee.

Use `windows-macos-input-setup` when the task concerns Arthur's related keyboard remapping, desktop switching, window movement, or natural-scrolling configuration rather than the KVM's physical USB path.

When Arthur confirms a hardware, wiring, or settings change, update only the in-package inventory so this skill retains one authoritative public copy. Keep security-device placement, serial numbers, accounts, network identifiers, employer-specific details, and other personal-risk data out of the package.

Physical furniture, room layout, lighting, power-strip placement, and ergonomics are outside this skill.
