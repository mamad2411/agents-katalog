---
name: ai-workflow-audit-skill
description: Use when auditing the ~/dev/AI repo for duplicated, conflicting, stale, or drifting instructions across ai/, root agent files, agents/, and skills/ — produces a coherence report before any edits are made.
---

# AI Workflow Audit Skill

## Description

A coherence pass over the operating-system docs in this repo. Surfaces
duplication, conflicts, drift between root agent files and `ai/`, and
gaps where a referenced doc, prompt, or agent doesn't exist. Audit
first; edits are a separate, approved step.

## When to use

- A coherence pass is overdue (multiple sessions of edits since the
  last one).
- A new agent surface, tool, or doc was added and needs to be absorbed
  into the rest.
- The user notices the docs disagreeing with each other.
- Before promoting `agents/claude/` artifacts into `~/.claude/`.

## When not to use

- Inside an application repo derived from this template (use
  docs-writer instead).
- For a single targeted fix that one of the other agents can handle.
- For new product features.

## Checklist

- [ ] List every Markdown file under `ai/`, root-level agent files
      (`CLAUDE.md`, `GEMINI.md`, `CODEX.md`), `agents/claude/`, and
      `skills/`.
- [ ] Build a map of cross-references: who points at whom.
- [ ] Identify duplications: same instruction appearing verbatim or
      near-verbatim in two places.
- [ ] Identify conflicts: two docs giving different answers to the
      same question (tool routing, security posture, workflow steps).
- [ ] Identify drift: a derivative doc (subagent, skill, root agent
      file) describing behavior the master `ai/` doc no longer
      implies.
- [ ] Identify dangling references: a doc points at a file, prompt,
      script, agent, or skill that does not exist.
- [ ] Identify missing references: a new artifact exists but no doc
      mentions where to find it.
- [ ] Produce a findings report ordered Blocking → Important → Minor.
- [ ] For each finding, propose the minimal edit and which file should
      change. Do not apply edits in this pass.

## Example invocation

> Use the ai-workflow-audit-skill across `ai/` and
> `agents/claude/`. Report findings; do not edit yet.

## Safety notes

- The master `ai/` docs are canonical. When in doubt, the derivative
  is the one that should change.
- Do not modify `ai/SECURITY_NOTES.md`, `ai/DECISIONS.md`,
  `ai/TASKS.md`, or `ai/BUGS.md` as part of an audit. Those require
  explicit approval and a separate task.
- Do not silently change the doctrine ("one canonical system, many
  specialized agents, one branch per agent, no simultaneous writes,
  tests/logs over vibes").
- Do not introduce new agents, skills, or tools as part of the audit.
  Surface the gap; let the user decide.
