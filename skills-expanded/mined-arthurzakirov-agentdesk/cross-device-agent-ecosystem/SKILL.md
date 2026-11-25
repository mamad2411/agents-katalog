---
name: cross-device-agent-ecosystem
description: Route work across Arthur's private Mac, Windows/WSL, and Android agent environments. Use when choosing between ChatGPT Remote, raw SSH, app SSH projects, Computer Use, Logitech Flow, or SkillPort synchronization, or when diagnosing cross-device behavior; not for detailed monitor cabling.
---

# Cross-Device Agent Ecosystem

Choose the execution layer before acting. The same physical computer can expose
different hosts, shells, permissions, projects, and browser capabilities.

## Preserve These Boundaries

- Keep the Windows ChatGPT desktop app's **Agent Environment** set to **Windows
  native**. This owner's Windows Chrome-extension and Computer Use path is
  verified in that mode. Do not claim that it works with a WSL agent unless
  current official documentation establishes that behavior.
- Treat **Integrated Terminal Shell** as independent from Agent Environment.
  Changing one is not a fix for the other.
- Keep WSL2 available in parallel for Linux development and remote Codex
  projects. A Mac-to-WSL app SSH connection does not require changing the
  Windows desktop app's native agent environment.
- Distinguish ChatGPT Remote, raw SSH, and an app SSH project. They can use SSH
  under the hood or reach the same computer without being interchangeable.
- Apply the permissions, sandbox, tools, browser setup, and trust state of the
  selected host. Do not assume configuration or SSH trust copies between
  devices.
- Never inspect or publish credential-capable files, network coordinates, key
  material, fingerprints, account identifiers, or machine-specific absolute
  paths. Use configured SSH aliases and environment variables.

## Route The Task

Read [topology and routing](references/topology-and-routing.md) whenever choosing
a device, connection, shell, browser, or troubleshooting layer. It contains the
owner-verified device inventory, interface table, preconditions, and diagnostic
rules. It also contains the concrete Codex task-dispatch procedure for starting
work on another connected desktop host without reusing an unrelated task.

Read [synchronization and public-safety rules](references/synchronization-and-safety.md)
when changing repositories, skills, global guidance, refresh automation, or
push policy. Remote Git repositories remain canonical; generated skill installs
and rendered global instructions are not editable sources.

Global `AGENTS.md` may use lazy-loaded runtime-mode references in a sibling
`agents-md-references/` directory. Keep only runtime detection and conditional links in the
main file; keep detailed mode-specific instructions in separate Markdown files
and load only the file for the identified product mode. The private context
repository owns personal runtime content, while SkillPort materializes managed
`agents-md-references/*.md` copies next to the generated `AGENTS.md`. Do not put private
runtime instructions in this public AgentDesk repository.

For detailed monitor, dock, KVM, or physical cabling work, use
`dell-monitor-kvm-setup` when installed. This skill retains only the digital
routing context needed to select a host and interface.

## Before Acting

1. Name the exact execution layer: desktop host, raw native-Windows SSH, raw WSL
   SSH, app SSH project, browser extension/Computer Use, SkillPort, or Git.
2. Confirm its preconditions and gather evidence from that layer before
   changing settings.
3. Make the narrowest layer-local correction. Do not change a system-wide shell
   or Agent Environment to repair a different layer.
4. Verify observable behavior on the selected host and report what was actually
   checked versus what remains intended or unverified.
