---
name: yolo-feature
description: Use when the user wants to build, add, or implement a feature. Captures intent, drafts a brief, confirms, then composes research → plan → execute → verify → finish. In a YOLO-initialized repo this takes precedence over generic brainstorming for feature intent.
---

# yolo-feature

The conversational entry point. You turn "I want X" into a landed, verified change.
You confirm at exactly **two gates** — the plan gate and the ship gate
(`.claude/yolo/conventions.md` *The two gates*); everything between them flows.

## 0. Resume or start fresh (cheap)
Derive the `slug` first (lowercase kebab-case noun phrase of the goal — drop leading imperative verbs like add/build/implement, so "add CSV export" → `csv-export`, not `add-csv-export`), then check for existing work before drafting anything new. Match robustly, not by exact string only: list `workspace/features/*`, compare case-insensitively, AND scan whether any existing brief's `goal` describes the same change — slug derivation can drift (`csv-export` vs `export-csv`), so don't rely on an exact coincidence.
- If a matching `workspace/features/<slug>/` or `feature/<slug>` already exists, this is a RESUME, not a new feature. Run yolo-status for that slug and pick up at the first incomplete step — do NOT re-draft the brief over existing work. If the slug collides with an *unrelated* feature, disambiguate (suffix the slug) and tell the user.
- If the brief lists `depends_on`, surface any dependency not yet `done` before starting, so the user can reorder.

## 1. Capture intent (cheap — no confirmation)
- Ask a light 2-question check (skip if the user signals they just want to proceed): what the user can DO after this, and how they'd know it works.
- Derive a `slug`, `goal`, and `success_criteria`. Write `workspace/features/<slug>/brief.md` from `.claude/yolo/templates/brief.md`. Commit it (`yolo: brief <slug>`). The brief now existing = status "planned" (`.claude/yolo/conventions.md`).

## 2. Branch, research, plan (billed — authorized by the user's request)
The user's "build X" request authorizes the research + plan that lead up to the plan gate; no separate pre-research stop.
- `git switch -c feature/<slug> <base_branch>` (branch explicitly from base so the merge-base is correct). Create a worktree (`../.<repo-name>-worktrees/<slug>`) only if work will run in parallel or you need walk-away isolation; otherwise a plain branch. See `.claude/yolo/conventions.md` for the worktree naming rule.
- Run each billed atom as a subagent at its `workspace/config.yaml` `agents.<step>` tier; invoke the named skill *inside* that subagent rather than reimplementing it here. Each subagent starts from a **clean context** and hands off **only** through its committed artifact (`research.md` → `plan.md` → task commits (`YOLO-Task`) → `verification.md`) — that artifact is simultaneously the human's review surface and the next phase's clean input. This is deliberate: it keeps the main context off the measured 30–50% context-rot curve.
  - **yolo-research** (`agents.research`) — invoke when the change is non-trivial or the codebase is unfamiliar; skip for tiny obvious changes.
  - **yolo-plan** (`agents.plan`) — produce `plan.md`.

## 3. The plan gate (first confirmation)
Present, in order: the **key findings & assumptions from research** (the codebase facts the plan rests on — a wrong assumption here is the most expensive thing to catch late), then the task plan, then rough scope/cost. STOP for approval or redirect before any code is written — this is the cheap, high-leverage moment to catch a wrong approach. Approving authorizes the execute → verify run through to the ship gate. Skip only if the user pre-consented ("just go"). See `.claude/yolo/conventions.md` *The two gates*.

## 4. Execute + verify (flows through — no confirmation gate)
- **execute** (`agents.execute`) — for each task in `plan.md`, work test-first with the task's `relevant_tests` (existing contract to keep green) and `test_spec` (new tests) **loaded into the subagent's context** — the measured TDD win is knowing *which* tests to check, not the ritual; a bare "do TDD" instruction without that context regresses worse than nothing. Commit each task with `--trailer "YOLO-Task: <id>"`. Run tasks in parallel subagents **only when their `files` scopes don't overlap**; writes that touch shared files stay serial (concurrent writers on shared code produce mismatched assumptions). The throwaway branch + one commit per task is the cheap rollback that *earns* this no-gate interior.
- **yolo-verify** (`agents.verify`) — check `success_criteria`; on pass it writes the `YOLO-Verified: true` trailer. **On any unmet criterion, return to execute for the failing task(s), then re-run yolo-verify** — do not proceed to finish until `YOLO-Verified: true` is written. **Bound this loop** (`.claude/yolo/conventions.md` *The two gates* — ~2–3 attempts); if criteria still fail, STOP and escalate to the human — repeated failure means the plan or the criteria need rethinking, not another pass.

## 5. The ship gate (second confirmation)
- **yolo-finish** (`agents.finish`) — land per the finishing policy + risk classifier. The irreversible merge onto `base_branch` is confirmed here; risk hard-triggers always stop even when pre-consented. See `.claude/yolo/conventions.md` *The two gates*.

## Rules
- Two confirmations only — the plan gate (§3) and the ship gate (§5), per `.claude/yolo/conventions.md` *The two gates*. "Just ship it" / "walk me through each step" are per-feature prose overrides, not config.
- Store no status — every "where are we" is derived from git via yolo-status.
- Precedence: in a YOLO repo, feature intent routes here; generic brainstorming yields.
- The atoms are defined once in their own skills — invoke them, don't reimplement them here.
