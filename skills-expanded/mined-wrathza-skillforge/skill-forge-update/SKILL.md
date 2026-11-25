---
name: skill-forge-update
description: "Guided update for an existing SKILL.md: structured recap, drift detection, change elicitation with conflict checking, per-item application with approval, and post-change quality gate. Use when an existing SKILL.md needs revision, modification, or improvement."
when_to_use: "Triggers: update/modify/revise/change this skill, edit SKILL.md, improve a skill."
argument-hint: "[skill-name or path]"
---

# Skill Forge Update
<!-- Pattern: Process (guided skill update workflow) -->

Understand before touching. Confirm before applying. Judge what you've done.

---

## Phase 0 — Load & Recap

**Skip condition**: If a `/skill-forge-recap` result for the same skill is already in the conversation context, verify the skill name matches, skip Phase 0 entirely, and proceed to Phase 1 using that recap. Ensure the agentskills spec cache (`~/.claude/tmp/agentskills-spec-<today>.md`) is current before Phase 1 — frontmatter validation in Phase 1 requires up-to-date field lists.

**MANDATORY** — Before reading the skill, fetch current platform docs in parallel:
- **WebFetch `https://agentskills.io/specification`** — live frontmatter requirements and field constraints
- **WebFetch `https://code.claude.com/docs/en/skills`** — Claude Code-specific features (new frontmatter fields, description char limits, invocation controls)

If either fetch fails, proceed with spec knowledge already in context; note "spec/docs unavailable — using cached knowledge" in the drift check output.

Note any constraints or features relevant to the skill being updated. These inform both the recap and the consistency checks in Phase 1.

Identify the target skill. The user may name it, paste a path, or point to it in context.

If no skill is identified, ask once: "Which skill do you want to update? (name or path)"

If the named skill file does not exist, stop: "Can't find [name] — check the path and re-invoke."

Read the skill completely. Produce a structured recap:

```
## [Skill Name] — Recap

**Does:** [1–2 sentences: core task and when it fires]
**Pattern:** [Tool / Process / Navigation / Mindset / Philosophy]
**Workflow:** [numbered phases or key steps, one line each]
**NEVER rules:** [count] covering [topics]
**References:** [list references/ files, or "none"]
```

**Drift check**: before flagging anything, ask: *would an agent reading only the description load this skill at the right moment, and would what loads match what the description promised?* That question — not symptom-matching — is the test. Then compare the frontmatter `description` field against the actual implementation. If they diverge (description omits key phases, misnames the trigger, or claims behaviour the skill doesn't exhibit), surface the discrepancy:

```
Drift detected: [what the description says] vs [what the skill actually does]
(s)uggest fixes / (i)gnore and continue
```

On `(s)`: produce a corrected description and add it to the Phase 1 change list as item 0 (applied first). On `(i)`: proceed without changing the description.

State the recap to the user. Confirm:

```
Does this match your understanding? (y)es / (n)o
```

On `(n)`: collect the correction, update the recap, confirm again before proceeding. After two corrections without agreement, ask directly: "What specifically is inaccurate?" rather than guessing again. Use that answer to produce a third recap iteration; if it still doesn't match, stop and ask the user to draft the recap themselves before continuing.

---

## Phase 1 — Change Elicitation Loop

**Goal**: A numbered change list that is specific, unambiguous, and consistent with the existing skill and principles. Do not touch the file until the list is confirmed.

### Loop

Elicit changes, paraphrase back with the updated change list and consistency check below, then ask:

```
(c)ontinue / (r)evise
```

On `(r)`: collect more input, update the change list recap, loop again.

On `(c)`: lock the numbered list and proceed to Phase 2.

After each response, produce:

```
## Proposed changes

1. [Change — specific enough to apply unambiguously]
2. ...

## Consistency check

[ ] Rule conflict: [conflicting rule text, or "none"]
[ ] Duplicate guidance: [overlapping section, or "none"]
[ ] Principles violation: [issue, or "none"]
[ ] Scope unclear: [vague term that needs scoping, or "none"]
```

### What triggers each consistency flag

**Rule conflict**: New NEVER contradicts an existing NEVER; new step breaks existing flow order.

**Duplicate guidance**: New section covers the same ground as an existing one — flag and ask: "merge or replace?"

**Principles violation**: NEVER missing WHY or INSTEAD. Request for generic advice ("write clean code", "be thorough"). Any rule that restates what Claude does by default. Unknown frontmatter field added (valid Claude Code extensions: `when_to_use`, `argument-hint`, `disable-model-invocation`, `context`, `agent`, `model`, `effort`, `paths`, `hooks`, `shell`, `user-invocable`, `allowed-tools`).

**Scope unclear**: "Make it shorter" without specifying what to cut; "improve it" without specifying how. Resolve to specific sections or criteria before adding to the list.

Loop does not advance on ambiguity. Every item in the confirmed list must be independently actionable.

---

## Phase 2 — Apply Changes

If skill-forge-hitl is not installed, stop: "skill-forge-hitl is required — install it before running skill-forge-update."

Invoke `/skill-forge-hitl` on the confirmed change list from Phase 1. Apply each item the user approves; skip declined items. When hitl outputs its final board, proceed immediately to Phase 3 — do not treat hitl's completion message as the end of the workflow. After hitl completes, show a concise diff summary:

```
## Changes applied

- [file]:[lines] — [one-line description]
```

If any change affects the skill's structure or pattern type, select the correct pattern before applying:

| Pattern | ~Lines | Use when |
|---------|--------|----------|
| Mindset | ~50 | Creative tasks requiring taste/judgment; high freedom |
| Navigation | ~30 | Multiple distinct scenarios routed to sub-files |
| Philosophy | ~150 | Art/creation requiring originality; internalize-then-express |
| Process | ~200 | Complex multi-step projects with phased checkpoints |
| Tool | ~300 | Precise operations on specific formats; low freedom |

If any change affects frontmatter fields, verify compliance against the spec and Claude Code docs. If Phase 0 was skipped, fetch them now before applying.

---

## Phase 3 — Judge & HITL

If skill-forge-judge is not installed, stop: "skill-forge-judge is required — install it before running skill-forge-update."

Invoke `/skill-forge-judge` on the modified skill. Always invoke `/skill-forge-hitl` on the findings it produces. After skill-forge-hitl completes, proceed to Phase 4.

If skill-forge-hitl applied zero findings (every item skipped or marked obsolete), do not silently advance — surface:

```
No judge findings applied — (a)ccept current grade / (r)evise scope / (q)uit without saving
```

On `(r)`, return to Phase 1 with the judge report's improvement list pre-loaded as draft. On `(a)`, proceed to Phase 4 with a note in the close-out that judge findings were reviewed but not applied.

If skill-forge-hitl stalls on an item (same rejection after 3 revisions), surface to the user:

```
Stuck on [item] — (a)ccept current state / (r)evise scope / (s)kip
```

Do not loop indefinitely.

---

## Phase 4 — Save & Activate

Write the updated SKILL.md to the path it was read from. Project-level skills (anywhere under the current repo, including `.claude/skills/<name>/` or a dedicated skills repo) are the default — they activate automatically once written and need no further install step.

If — and only if — the source path lives under `~/.claude/skills/` (user-level install), verify the symlink resolves correctly. Project-level files require no symlink check.

Print a one-block close-out:

```
## skill-forge-update — done

**File:** [path] ([N] lines, pattern: [Tool/Process/...])
**Scope:** project-level | user-level
**Applied:** [count] / [total] proposed changes
**Judge:** [grade] — [N applied / M reviewed-not-applied from Phase 3]
**Next:** [reload session if user-level / nothing if project-level]
```

The close-out is the user's only confirmation that work landed; never end on hitl's board or a silent file write.

---

## NEVER

- **NEVER apply changes before Phase 1 produces a confirmed change list**
  **Instead:** Run the elicitation loop until the user responds `(c)ontinue`.
  **Why:** Applying ambiguous changes produces a result the user didn't want; the subsequent skill-forge-judge then evaluates the wrong output.

- **NEVER skip the four-point consistency check on each proposed change**
  **Instead:** Run all four checks every iteration, even for simple-sounding requests.
  **Why:** "Add a NEVER rule" sounds trivial but frequently introduces rule conflicts or violates the three-part format — these only surface under cross-reference.

- **NEVER use skill-forge-hitl in Phase 1**
  **Instead:** Phase 1 is elicitation only — collect changes, update the recap, loop with `(c)ontinue / (r)evise`. Use skill-forge-hitl in Phase 2 for application confirmation.
  **Why:** Mixing elicitation and hitl confirmation in the same phase conflates two distinct loops and confuses which loop the user is in.

- **NEVER skip Phase 3 (skill-forge-judge) after applying changes**
  **Instead:** Always judge the modified skill before presenting for final approval.
  **Why:** A change that looks correct can silently drop the skill below grade; catching this before install is far cheaper than fixing it post-install.

- **NEVER proceed to Phase 3 if hitl applied zero changes**
  **Instead:** Show the final HITL board and offer `(r)evise change list / (q)uit without saving`. On `(r)`, re-enter Phase 1's elicitation loop with the existing change list pre-loaded as draft so the user can adjust rather than rebuild.
  **Why:** Judging an unchanged file produces the same grade as before and misleads the user into thinking changes were validated.

- **NEVER apply Phase 2 changes outside skill-forge-hitl**
  **Instead:** Always hand the confirmed change list to `/skill-forge-hitl` — never iterate edits inline, even for a single-item list.
  **Why:** Per-item approval is the user's only veto point before the file is written; an inline apply loop removes that gate and turns Phase 1's confirmation into a blank cheque.

