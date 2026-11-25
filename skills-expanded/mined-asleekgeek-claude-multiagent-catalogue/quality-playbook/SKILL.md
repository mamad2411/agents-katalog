---
name: quality-playbook
description: >
  Phase execution skill for the Quality Playbook. Read by qp-orchestrator and passed
  to each phase sub-agent via the Task tool. Contains the seven-phase audit protocol,
  Mode A walkthrough instructions, domain exploration framework, role taxonomy, and
  challenge gate. Do not invoke this skill directly — invoke qp-orchestrator instead.
  Upstream: https://github.com/andrewstellman/quality-playbook
compatibility: Claude Code (Task tool, bash, file tools)
version: 1.5.6
---

# Quality Playbook Skill

This skill file is loaded by the `qp-orchestrator` agent and passed to phase sub-agents.
The full phase logic is in the `phase_prompts/` directory alongside this file.

## Quick-start (Mode A — Claude Code direct)

You are a Claude Code agent running a phase. For each phase N:

1. Read `phase_prompts/phaseN.md` from alongside this skill file
2. Execute per the prompt — read named inputs, do analysis, write to `quality/`
3. STOP at the end-of-phase boundary (every phase prompt ends with "Do NOT proceed
   to Phase N+1" — honour it)
4. Report back to the orchestrator with: files written, summary of findings, any
   blockers

**Scope invariant:** Do NOT modify any file outside the target's `quality/` directory
(except `AGENTS.md` at the repo root, which Phase 2 writes). In Mode A you are the
gate; the orchestrator is not running a subprocess interceptor.

## Phase prompt location

Look for `phase_prompts/phaseN.md` alongside this SKILL.md, in this order:

1. `.claude/skills/quality-playbook/phase_prompts/phaseN.md`
2. `phase_prompts/phaseN.md` (if QPB runner is installed at project root)
3. `~/.claude/skills/quality-playbook/phase_prompts/phaseN.md`

If phase prompts are not found, tell the orchestrator. Install from:
https://github.com/andrewstellman/quality-playbook

## References

The `references/` directory alongside this skill contains:
- `orchestrator_protocol.md` — per-phase verification gates (read this before Phase 1)
- `run_state_schema.md` — cycle event format (calibration only)
- `challenge_gate.md`, `constitution.md`, `functional_tests.md`, etc.

All references are loaded on demand by phase sub-agents as needed.

## Claude Code Notes

Adapted from `SKILL.md` v1.5.6 by Andrew Stellman.

The full SKILL.md from the upstream repo is the authoritative source for all phase
logic, the complete role taxonomy, Mode B (runner-driven) invocation, iteration
strategies, and the bootstrap self-audit protocol. This file is a Claude Code-oriented
wrapper that points phase sub-agents at the right locations.

Install the upstream skill for full functionality:
```bash
git clone https://github.com/andrewstellman/quality-playbook /tmp/qpb
cp -r /tmp/qpb/phase_prompts .claude/skills/quality-playbook/
cp -r /tmp/qpb/references .claude/skills/quality-playbook/
```
