---
name: skill-author-coach
description: Walks the user from a rough idea to a merge-ready SKILL.md for this repo — interview, draft from the template, self-QA against the authoring standard, then run the validator. Use when the user says "write a new skill", "add a skill to the repo", "turn this workflow into a skill", "is this skill up to standard", or wants to fix a validator failure. Don't use for vetting someone else's skill before install — that's third-party-skill-vetter.
version: 1.0.0
author: Gen AI Hub
license: MIT
metadata:
  hermes:
    tags: [Agent Mastery, Authoring, Skills, QA, Meta]
    related_skills: [third-party-skill-vetter, agent-eval-harness]
---

# Skill Author Coach

Turns "I want my agent to do X" into a SKILL.md that clears the repo's QA gate on the first validator run. The standard it holds: every skill it produces passes `tools/validate_skills.py` clean, reads at student level, and could be followed by a fresh agent with zero outside context.

## When to Use

- The user wants to author a new skill for this repo (or their fork of it).
- An existing skill fails the QA gate or validator and needs a fix.
- A repeated manual workflow deserves to become a skill.
- A skill from another repo passed vetting but needs a rewrite to this repo's standard before merge.
- **Not for:** evaluating a third-party skill before installing it (`third-party-skill-vetter`), or measuring whether a finished skill actually works (`agent-eval-harness`).

## Quick Reference

| Action | Command / Call |
|---|---|
| Read the standard | `read_file AUTHORING-STANDARD.md` |
| Copy the template | `read_file templates/SKILL-TEMPLATE.md` |
| Create the skill folder | `mkdir -p skills/<track>/<skill-name>` |
| Run the QA gate | `python3 tools/validate_skills.py` (from repo root) |
| Count lines | `wc -l skills/<track>/<skill-name>/SKILL.md` (target 80–140) |
| Check the boundary clause | `grep -c "Don't use for" skills/<track>/<skill-name>/SKILL.md` (must be ≥1) |

## Procedure

1. **Precheck** — confirm you're in the repo root (`ls AUTHORING-STANDARD.md tools/validate_skills.py` succeeds) and `python3 -c "import yaml"` works. If PyYAML is missing: `pip install pyyaml`, then continue.
2. **Interview (5 questions, then stop)** — ask the user: (a) What is the ONE job? If their answer contains "and," propose a split into two skills. (b) What are the 3–5 phrases they'd say when they want it? These become the description's triggers. (c) What tools/commands does it run, and does any step spend money, send messages, or delete files? (d) What does a finished, correct output look like? Get a concrete example. (e) What has gone wrong when they did this manually? Seed material for Pitfalls.
3. **Pick track and name** — kebab-case, verb-or-role flavored, matching the folder name exactly (the validator checks folder == frontmatter name). Confirm the track folder with the user.
4. **Draft from the template** — copy `templates/SKILL-TEMPLATE.md` structure exactly; never draft from memory. Write the description as: what it does + "Use when [triggers]" + "Don't use for [adjacent job — sibling skill]." Fill sections in order: When to Use (with a Not for line), Quick Reference (3–8 rows), numbered Procedure (each step = action + expected result), Output Template, Pitfalls (≥3, each with a recovery), Verification. Secrets go in `required_environment_variables` only — if the draft ever says "paste your key," rewrite it.
5. **Add safety rails where triggered** — if step 2c flagged money/messages/deletes, insert an explicit Confirm step (show what will happen, proceed only on yes) and a dry-run mode. This is a hard requirement, not a style choice.
6. **Self-QA against the gate** — walk the AUTHORING-STANDARD QA checklist line by line and mark each item pass/fail before running the validator. Also check length: 80–140 lines, hot path under ~40 lines of instructions. Fix fails now.
7. **Run the validator** — `python3 tools/validate_skills.py` from repo root. Success: `ALL CHECKS PASS`. On failure, fix the exact reported line and re-run — never hand the user a skill with known failures.
8. **Deliver** — write the file to `skills/<track>/<name>/SKILL.md` and give the user the summary in the template below.

## Output Template

```
## New skill: <skill-name>
Track: <track> | Lines: <n> | Validator: PASS

One job: <one sentence>
Triggers: "<phrase 1>", "<phrase 2>", "<phrase 3>"
Safety rails: <none needed | confirm+dry-run on step N>
Related skills wired: <list>

Next: test-drive it — give your agent one of the trigger phrases and
run agent-eval-harness on the result before you rely on it.
```

## Pitfalls

- **Scope creep in the interview** — the user describes three jobs as one skill; the draft description needs "and" twice. Recovery: stop drafting, propose the split explicitly ("that's two skills: X and Y"), author the highest-value one first.
- **Folder/name mismatch** — validator fails with `folder name != frontmatter name` after a late rename. Recovery: pick one canonical name, update both the directory and the `name:` key, re-run the validator.
- **Vague procedure steps** — steps read like advice ("check the output looks right") instead of checks. Recovery: rewrite each step as command + observable success condition; if you can't name what success looks like, the step isn't done being designed.
- **Missing Don't-use-for clause** — description sells the trigger but never fences the boundary, so the agent grabs the skill for adjacent jobs. Recovery: name the nearest sibling skill and add "Don't use for [its job — sibling-name]" to the description.
- **Related skills that don't exist** — validator fails on `related_skill 'x' not in repo`. Recovery: only reference skills already in `skills/*/*/`; if the sibling is planned but unwritten, drop the reference and add it when the sibling merges.
- **Hot path buried** — the common workflow starts at line 60 after edge-case throat-clearing, so every load pays for the rare path. Recovery: reorder — most common workflow first, edge cases at the bottom, and keep the hot path under ~40 lines of instructions.

## Verification

- [ ] `python3 tools/validate_skills.py` prints `ALL CHECKS PASS`
- [ ] Folder name, frontmatter `name`, and any related_skills references all resolve
- [ ] `wc -l` shows 80–140 lines
- [ ] Description contains both "Use when" triggers and a "Don't use for" clause
- [ ] Any money/message/delete action has a confirm step and dry-run in the Procedure
- [ ] No secrets in the file body; env vars declared via `required_environment_variables` if needed
- [ ] Hot path (most common workflow) sits in the first ~40 instruction lines
- [ ] Read the final draft once as a stranger: a fresh agent could execute it with zero outside context
