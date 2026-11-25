---
name: ctf-training-loop
description: Practical CTF training workflow for systematically learning challenge
  categories through real solving, writeups, and skill updates.
version: 1.0.0
license: MIT
metadata:
  hermes_origin: import
tags:
- ctf
- competition
- challenge
- training
- loop
related_skills: []
---

# CTF Training Loop

Use when the goal is not just to answer a single CTF challenge, but to build durable practical capability across CTF categories.

## Trigger conditions
- User asks Hermes to "learn CTF" or "practice CTF"
- User wants broad coverage across challenge families
- User wants reusable methods, scripts, and knowledge solidified into Hermes

## Core principle
Do not stop at taxonomy, notes, or theory. User explicitly wants Hermes to *learn by real CTF practice*. A technique is not learned until Hermes has solved or reproduced it hands-on with runnable artifacts.

Mandatory loop:
1. Classify the challenge family/subfamily.
2. Perform low-cost triage and artifact inventory.
3. Create only the minimal files/scripts needed to solve; full scaffolding is optional, not mandatory.
4. Solve or reproduce the primitive with executable scripts/exploits/extractors.
5. Run the script and verify the flag/expected output.
6. Record the decisive observation/technique when useful.
7. Patch or create the relevant skill so the technique is reusable next time.

Do not claim mastery from reading. Use archived CTF tasks, local reproductions, or user-provided challenges to build practical evidence.

## Coverage map
Minimum practical areas:
- Web Exploitation
- Cryptography
- Forensics
- Reverse Engineering
- Pwn / Binary Exploitation
- Misc / Jail
- OSINT
- Mobile
- Cloud / DevOps
- Blockchain
- Hardware / RF / ICS
- Game / Protocol
- AI / ML

## Execution pattern
For each domain:
1. Load the domain skill if it exists.
2. Pick representative challenge types.
3. Build or reuse triage scripts.
4. Solve with reproducible commands/code.
5. Verify the flag or intended primitive.
6. Extract a stable playbook insight.
7. Save the improved process back into Hermes skills.

## Benchmark mindset
Capability means being able to:
- recognize patterns quickly
- test hypotheses cheaply
- automate repeated checks
- produce a solver/exploit, not only an explanation
- carry forward new tactics into persistent skills

## Deliverables
After a training batch, produce:
- solved/attempted challenge list
- scripts/exploits written
- notable techniques learned
- skill patches or new references added

## Pitfalls
- Over-indexing on theory and not solving real tasks
- Jumping to one category before performing inventory
- Failing to preserve newly learned attack patterns into skills
- Treating writeups as sufficient without reusable scripts
