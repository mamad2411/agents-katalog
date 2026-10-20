---
name: desktop-installer
description: Installers, uninstallers, and first-run provisioning for Windows, macOS, and Linux desktop apps. Auto-invoked when building MSI/EXE/PKG/DMG/DEB/RPM installers, debugging install failures, or designing per-user vs system-wide installs.
---

# Desktop Installer

The installer is the user's first impression and the most environment-dependent
failure surface in the product. Everything from download to first launch — across
three OSes and the enterprise deployment tools layered on top — has to work on
machines you've never seen.

## When to reach for this

- Building or changing an installer (MSI/MSIX, EXE, PKG, DMG, DEB/RPM, Flatpak, AppImage)
- Debugging install/upgrade failures, double installs, or orphaned Add/Remove entries
- Choosing per-user vs per-machine scope, or preparing for SCCM/Intune/JAMF deployment
- Designing uninstall behavior and first-run provisioning (license, telemetry consent, auto-start)

## Principles

1. **Match the OS idiom.** macOS consumer apps ship drag-install DMG; use `.pkg`
   only when postinstall scripts or MDM deployment demand it. Windows enterprise
   expects MSI; consumer apps may ship EXE. Linux: native package for the distro,
   Flatpak/AppImage as the cross-distro fallback.
2. **Silent install is table stakes for enterprise.** Every user-facing choice is
   a documented command-line property or answer-file option. An MSI without
   public properties is not deployable by Intune or SCCM.
3. **MSI upgrade code ≠ product code.** The UpgradeCode is the product family's
   permanent identity — never change it. The ProductCode changes per release.
   Getting this backwards kills in-place upgrades and orphans ARP entries.
4. **Pick install scope once and keep it.** Mixing per-user and per-machine
   across versions produces double installs and upgrade detection failures.
5. **Test on clean VMs per OS version** — Windows 10/11, the last two macOS
   releases, Ubuntu LTS + Fedora current, plus one corporate-locked profile
   (GPO-restricted Windows, MDM-managed macOS). Installer bugs are always
   environment-specific.
6. **Make uninstall honest.** Prompt explicitly about kept user data; remove
   files, registry keys, services, LaunchAgents, and scheduled tasks. Leftovers
   are a trust break and a support-ticket generator.
7. **Log every install.** Windows: `msiexec ... /l*v install.log`. macOS:
   `/var/log/install.log`. Linux: journald + package-manager logs. Without logs,
   enterprise debug cycles take weeks.

## Per-OS format decision

| Target | Consumer default | Enterprise default | Silent install |
|---|---|---|---|
| Windows | EXE (Inno Setup/NSIS) or MSIX | MSI (WiX) with public properties | `msiexec /i app.msi /qn /l*v install.log PROP=value` |
| macOS | DMG drag-install | `.pkg` (productbuild) for JAMF/Kandji | `installer -pkg App.pkg -target /` |
| Linux | Flatpak or AppImage | `.deb`/`.rpm` + signed repo | `apt-get install -y ./app.deb` |

First-run provisioning checklist: license acceptance, telemetry consent
(default-off where law requires), auto-start toggle, protocol/file-type
registration prompts, permissions priming — each persisted so it runs exactly once.

## Pitfalls

- Changing the MSI UpgradeCode between releases (breaks the upgrade path permanently)
- Postinstall scripts that assume a logged-in GUI user or network access
- Writing HKLM or `/Applications` from a per-user installer — fails without elevation or pollutes other users
- Uninstall leaving LaunchAgents, registry Run keys, services, or context-menu hooks behind
- Shipping untested upgrade paths — upgrade-from-previous is a release-blocking test, not a nice-to-have
- Undocumented install properties, forcing enterprise admins to reverse-engineer the package

---
*Related: `desktop-code-signing` (installer signing/notarization),
`desktop-autoupdate` (post-install update path), `desktop-shell-integration`
(file-type / protocol registrations the installer writes) · domain agent:
`desktop-architect` · output/ADR format: `playbook-conventions`*
