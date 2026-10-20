---
name: operations-category-pointer
description: "Pointer to a library of 8 specialized Operations skills. Use when working on operations-related tasks."
risk: none
---

# Operations Capability Library 🎯

This is a **pointer skill**. The 8 specialized Operations skills are stored in a hidden vault to keep your startup context minimal.

## Available skills in this category

- **anti-sleep** — Keep a Mac awake with caffeinate during long builds, downloads, or supervised automation runs.
- **it-manager-hospital** — World-class Hospital IT Management Advisor specializing in clinical safety, digital maturity (HIMSS/ONA/JCI), and HIS/PEP ecosystems.
- **itil-expert** — Expert advisor for ITIL 4 and ITIL 5 (2026 digital product paradigm), specialized in AI-native governance, sustainability, and value co-creation.
- **mailtrap-setting-up-sending-domain** — Add or verify a Mailtrap sending domain, troubleshoot DNS propagation, publish SPF/DKIM/DMARC records, and complete compliance.
- **pi-custom-model** — Register custom Pi Agent model slugs so saved OpenRouter variants resolve correctly.
- **powershell-windows** — PowerShell Windows patterns. Critical pitfalls, operator syntax, error handling.
- **pre-release-review** — Run a read-only pre-release review for deploy readiness, migrations, config, secrets, rollout order, rollback risk, and launch blockers.
- **vps-server-management** — Manage authorized VPS hosts and server-side agents through cautious SSH and operations workflows.

## How to load a skill

1. Identify the skill name above matching your task.
2. Use `read` to load its `SKILL.md` from the vault:
   `/home/melfiano/.config/opencode/skill-libraries/operations/<skill-name>/SKILL.md`
3. Follow those instructions to complete the request.

**Vault path:** `/home/melfiano/.config/opencode/skill-libraries/operations`

> Do not guess best practices — always read from the vault first.

> ⚠️ **Anti-loop guard**: Do NOT invoke skills recursively or check for applicable skills before every response. Each skill should be loaded at most once per user request. If you have already identified and loaded the relevant skill for this task, proceed with execution — do not re-scan for skills.
