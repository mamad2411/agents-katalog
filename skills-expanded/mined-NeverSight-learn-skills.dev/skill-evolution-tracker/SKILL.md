---
name: skill-evolution-tracker
description: Use when executing ANY skill to monitor performance, log failures, and auto-update the failing skill's documentation.
triggers:
  - track skill
  - log failure
  - skill error
  - fix skill
  - evolve skill
version: 1.0.0
---

# Skill Evolution Tracker

## Overview
This skill acts as a **Global Quality Assurance System** for all other skills. It observes skill executions, detects when a skill fails or produces suboptimal results, and **immediately refactors the failing skill** to prevent the same mistake from happening again.

**Core Principle:** "One pitfall, never twice." (一坑不踩两次)

## When to Use
- **Continuously**: Ideally, this "mindset" is active during all skill executions.
- **On Failure**: When a skill throws an error, gets stuck in a loop, or the user corrects the output.
- **On Confusion**: When the agent (you) feels the instructions in a skill are ambiguous.

## The Evolution Protocol

### 1. Silent Observation (Monitor)
While executing a task using another skill, watch for:
- **Runtime Errors**: Python exceptions, API failures.
- **Logic Errors**: The plan didn't work, the output format was wrong.
- **User Corrections**: The user said "No, do it this way".

### 2. Incident Recording (Log)
If a failure occurs, use the helper script to update the log.

**Command**:
```bash
python .trae/skills/skill-evolution-tracker/scripts/log_incident.py "skill-name" "trigger description" "issue description" "fix applied"
```

This script will safely append the entry to `evolution.json`.

**Entry Format (Handled by script)**:
```json
{
  "date": "YYYY-MM-DD",
  "target_skill": "skill-name",
  "trigger": "What happened?",
  "issue": "Root cause",
  "fix_applied": "Description of the change made to SKILL.md"
}
```

### 3. Auto-Refactoring (Evolve)
**IMMEDIATELY** after logging the incident, you MUST fix the root cause in the target skill's `SKILL.md`.

**How to Fix:**
1. **Read** the failing `SKILL.md`.
2. **Locate** the weak section.
3. **Edit** the file to add clarification or constraints.

### 4. Review History
To see past improvements:
**Command**:
```bash
python .trae/skills/skill-evolution-tracker/scripts/read_evolution.py
```
