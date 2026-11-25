---
name: anti-slop-ui-design
description: Guidelines for high-conviction, professional developer & cybersecurity software interfaces, eliminating generic AI-generated aesthetic clichés.
---

# Anti-Slop UI/UX Design System for TRUSTY.ai

## 1. Principles of High-Conviction Software Design
Generic AI generation often produces "AI slop": excessive rainbow gradients, random blurred purple/cyan spheres, oversized rounded bubble buttons, and decorative elements that look like generic landing page templates.

For TRUSTY.ai, the user experience must evoke the authority of **VirusTotal, Moody's, Bloomberg Terminal, and Linear**:
- **Surgical, Institutional Precision**: The user is trusting this tool to evaluate whether to grant an agent access to their bank accounts, company codebase, and email inbox. It must feel like an authoritative security instrument.
- **Deep Obsidian Hierarchy**: Strict grayscale foundation (`zinc-950`, `zinc-900`, `zinc-800`, with `border-white/[0.06]`).
- **Functional Accent Colors Only**: Colors have strict semantic meaning:
  - `Emerald (#10b981)`: Cryptographically verified, low risk, clean audit.
  - `Amber (#f59e0b)`: Telemetry warning, unverified org, broad permissions.
  - `Rose (#f43f5e)`: Hard severity override, malware, unsandboxed root access.
  - `Sky (#38bdf8)`: Active telemetry and protocol transport.
- **Tabular Figures & Monospace Accents**: Data metrics, hashes, and scores must use `tabular-nums` and crisp monospace typography.
- **Dense, High-Utility Information Architecture**: Real security analysts prefer scannable density, clear border dividers, and instant keyboard shortcuts over puffy whitespace.
