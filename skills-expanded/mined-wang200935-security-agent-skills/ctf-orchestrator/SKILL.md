---
name: ctf-orchestrator
description: Orchestrate Capture-the-Flag challenge solving across Web Exploitation,
  Cryptography, Forensics, Reverse Engineering, Pwn/Binary Exploitation, and Misc.
  Use when the user provides a CTF challenge, asks to train for CTFs, wants a writeup,
  or asks which CTF category/attack path to try.
version: 1.1.0
license: MIT
metadata:
  hermes_origin: import
tags:
- ctf
- triage
- writeups
- training
related_skills:
- ctf-web-exploitation
- digital-forensics
- ctf-reverse-engineering
- binary-exploitation
- ctf-misc-toolkit
- ctf-kernel-exploitation
---

# CTF General Solver

## Purpose
Use this as the router and discipline layer for any CTF task. It prevents random guessing by forcing artifact inventory, category detection, reproducible solving, and durable writeups.

## Safety Boundary
Only operate on CTF/lab/authorized targets. For live endpoints, avoid destructive actions, rate-limit requests, and never reuse techniques against real third-party services without permission.

## Skill Integration
This skill is the **CTF orchestrator** in the cybersecurity skill tree:

```
cybersecurity (master router) → ctf-general (CTF orchestrator) → domain skill
```

Load this skill when:
- The user provides a CTF challenge
- User asks to train for CTFs
- User wants a writeup
- User asks which CTF category/attack path to try

**Then** load the appropriate domain skill from the routing table below.

## See Also

- `references/universal-first-10-minutes.md` — Universal First 10 Minutes
- `references/category-router.md` — Category Router
- `references/full-practical-ctf-taxonomy.md` — Full Practical Ctf Taxonomy
- `references/universal-commands.md` — Universal Commands
- `references/practical-training-loop.md` — Practical Training Loop
- `references/training-backlog-template.md` — Training Backlog Template
- `references/solve-ledger-template.md` — Solve Ledger Template
- `references/writeup-template.md` — Writeup Template
- `references/practical-lessons-learned.md` — Practical Lessons Learned
- `references/ctfd-rest-api-challenge-metadata--flag-submission.md` — Ctfd Rest Api Challenge Metadata  Flag Submission
- `references/author-repo-shortcut-ais3--known-ctf-authors.md` — Author Repo Shortcut Ais3  Known Ctf Authors
- `references/ctfd-platform-quick-reference.md` — Ctfd Platform Quick Reference
- `references/solve-cadence--initiative.md` — Solve Cadence  Initiative
- `references/ctfd--per-lab-web-training-platform-pattern.md` — Ctfd  Per Lab Web Training Platform Pattern
- `references/encrypted-zip-attacks-zipcrypto--legacy-pkzip.md` — Encrypted Zip Attacks Zipcrypto  Legacy Pkzip
- `references/ctfd-recon-without-auth-hackerverse-ec-council-public-scoreboards.md` — Ctfd Recon Without Auth Hackerverse Ec Council Public Scoreboards
- `references/static-only-binary-analysis-no-local-execution.md` — Static Only Binary Analysis No Local Execution
- `references/2025-2026-ctf-landscape-update-ai-assisted-solving--new-trends.md` — 2025 2026 Ctf Landscape Update Ai Assisted Solving  New Trends
- `references/ai-assisted-ctf-solving-mcp--llm-workflow-def-con-33-field-report.md` — Ai Assisted Ctf Solving Mcp  Llm Workflow Def Con 33 Field Report
- `references/modprobe-path-af_alg-bypass-2025.md` — Modprobe Path Af_Alg Bypass 2025
- `references/2025-2026-ctf-pyjail-new-techniques-from-pyjail-collection.md` — 2025 2026 Ctf Pyjail New Techniques From Pyjail Collection
- `references/kernel-exploit-dojo-100-kernel-ctf-archive.md` — Kernel Exploit Dojo 100 Kernel Ctf Archive
- `references/cve-2024-2961-cnext-quick-reference.md` — Cve 2024 2961 Cnext Quick Reference
- `references/cloudflare-turnstile-file-download-workarounds.md` — Cloudflare Turnstile File Download Workarounds
- `references/nc-based-binary-challenges--command-injection-via-menu-fields.md` — Nc Based Binary Challenges  Command Injection Via Menu Fields
- `references/maintenance-rule.md` — Maintenance Rule
