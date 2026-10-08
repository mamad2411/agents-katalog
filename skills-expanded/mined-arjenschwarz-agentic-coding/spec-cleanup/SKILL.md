---
name: spec-cleanup
description: Identify and clean up stale or superseded feature specs in a project's specs/ directory. Use whenever the user wants to prune, tidy, audit, consolidate, or declutter specs, mentions outdated/overruled/replaced/superseded specs or a spec that has a v2 or improved version, or asks which specs are still relevant — even if they don't explicitly say "cleanup".
---

# Spec Cleanup

Spec directories accumulate history: a feature gets specced, then re-specced with a better approach, and the old spec lingers. Those leftovers cost mindshare — every overview scan, every "which spec is current?" question pays for them. This skill finds superseded specs and resolves them in one of two ways:

- **Fully replaced** — a newer spec covers everything the old one did. The old spec should be removed.
- **Extended** — a newer spec builds on a still-valid base, adding features. Both hold unique information, so a human must decide: consolidate into one spec, or remove one.

The skill is deliberately conservative. It deletes nothing without explicit approval, and when classification is ambiguous it errs toward "extended" because that routes the call to the user instead of the trash.

## Prerequisites

- A `specs/` directory in the project root with at least two spec subdirectories.

## Process

### 1. Discover

- List all subdirectories under `specs/`, excluding `specs/bugfixes/` (bug reports are historical records, not competing specs).
- For each spec, read the primary document (`requirements.md`, `smolspec.md`, `design.md`, or `plan.md` — whichever exists first in that order), plus `decision_log.md` and `tasks.md` if present.
- If the project is a git repository, collect per-spec dates: creation (`git log --diff-filter=A --format='%aI' -- 'specs/<dir>/'`, oldest entry) and last modification (newest entry without the filter). Parallelize these lookups.

### 2. Detect supersession candidates

Group specs into candidate pairs or clusters when any of these signals appear:

- **Naming**: shared stem with a version or revision suffix (`feature` / `feature-v2`, `-revised`, `-improved`, `-new`, `-redesign`).
- **Explicit references**: one spec says it "supersedes", "replaces", "builds on", or "extends" another, or links to it as prior art.
- **Decision logs**: a decision with status `superseded by ...`, or an entry recording that an approach was abandoned in favour of another spec.
- **Scope overlap**: two specs describe the same feature area or repeat substantially the same requirements.
- **Git corroboration**: the older spec has had no commits since the newer one was created, or its tasks sit unchecked while the newer spec's tasks progressed.

A single signal — especially naming — is a hint, not a verdict. `payments` and `payments-v2` might be a replacement, or v2 might be phase two of a still-valid phase one. Read both specs' content before pairing them; a spec that merely mentions another is not automatically its successor.

### 3. Classify each candidate

For each pair/cluster, compare scope and decide:

- **Fully replaced**: the newer spec covers all of the older spec's requirements (possibly with a different approach), or the older spec was abandoned before implementation in favour of the newer one. Nothing in the old spec is still the authoritative record for anything. → Recommend removal.
- **Extended**: the newer spec adds features on top of the older one, and the older spec remains the authoritative record for the base behaviour. → Recommend a user decision: consolidate both into one spec, or remove one and accept the information loss.
- **Not actually related**: on reading, the specs cover different things. Drop the pair from the report; do not pad the findings.

Implementation status matters: a *completed* old spec whose behaviour is restated in the new spec is safe to remove (the code and the new spec carry the knowledge). A completed old spec whose details the new spec does *not* restate is an "extended" case — removing it loses the only written record.

When genuinely unsure, classify as **extended**. The cost of asking an unnecessary question is small; the cost of deleting the only record of a design decision is not.

### 4. Report — approval gate

Present the findings before touching any file. Use this structure:

```markdown
# Spec Cleanup Report

| # | Stale spec | Superseded by | Classification | Recommended action |
|---|-----------|---------------|----------------|--------------------|
| 1 | user-auth | user-auth-v2  | Fully replaced | Remove             |
| 2 | export-csv | export-formats | Extended      | Decide: consolidate or remove |

## 1. user-auth → user-auth-v2 (fully replaced)

**Evidence:**
- user-auth-v2/requirements.md states "This spec supersedes user-auth"
- All 6 requirements in user-auth appear in user-auth-v2 (revised approach)
- user-auth untouched since 2025-03-02; tasks 2/9 complete, abandoned

**Recommended action:** remove `specs/user-auth/`

## 2. export-csv → export-formats (extended)
...
```

Every claim in the evidence list must be checkable — quote the supersession sentence, name the decision entry, give the dates. The user is approving deletions based on this report; vague evidence makes the gate meaningless.

Then **stop and wait for explicit approval**. The user may approve all items, a subset, or override a classification (e.g. "consolidate #2 instead"). Do not proceed on silence, and do not treat the original "clean up my specs" request as pre-approval for specific deletions — unless the user explicitly granted it (e.g. "remove anything fully replaced without asking").

### 5. Execute approved actions

**Removal** (fully replaced, or the user chose removal for an extended pair):
- Use `git rm -r specs/<dir>` so the spec stays recoverable through history. If the directory is untracked, flag that deletion would be unrecoverable and confirm before using `rm`.

**Consolidation** (the user chose to merge an extended pair):
- Move content the surviving spec lacks into it: unique requirements, design sections, and unchecked tasks. Rewrite for coherence; do not paste-append.
- Carry over the absorbed spec's decision log entries — they are historical record. Renumber to fit the survivor's sequence and note their origin.
- Add a new decision entry to the survivor recording the consolidation itself (what was merged, why, date). Follow the project's decision-log format if one is defined.
- Then remove the absorbed spec's directory via `git rm -r`.

### 6. Refresh the overview

If `specs/OVERVIEW.md` exists, regenerate it: use the `specs-overview` skill if available; otherwise edit the file directly, removing table rows and detail sections for deleted specs and updating consolidated ones. Skip this step if the file doesn't exist — don't create it as a side effect.

### 7. Summarize

Report what was removed, what was consolidated and where the content went, and what was left alone (including candidates the user declined). Mention that removed specs are recoverable via git history.

## Constraints

- Never remove or modify a spec without explicit approval for that specific spec in this conversation.
- Never touch `specs/bugfixes/`.
- Classify by content, not names alone — read the specs before pairing or recommending.
- Old age alone is not staleness: a spec with no successor is out of scope, no matter how old. At most, mention it as an observation; recommend no action.
- Prefer `git rm` over `rm` so removals are recoverable.
