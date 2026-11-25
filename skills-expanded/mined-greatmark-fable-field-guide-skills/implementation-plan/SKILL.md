---
name: implementation-plan
description: >-
  Write an implementation plan that leads with the decisions the user is most
  likely to change and buries mechanical work at the bottom. Use when the
  user says "implementation plan", "实现计划", "开发计划", "落地方案",
  "先出方案再动手", "先别写代码，想清楚给我看看", asks for an RFC/技术方案
  or a pre-work buy-in proposal (立项提案), or wants a reviewable plan after
  brainstorming. Also read whenever a built-in plan mode is active (Cursor,
  Claude Code, Codex) — before writing any plan, whether you switched into
  it or the session started there. Not for trivial changes or resolving
  open questions (run interview-me first); if a reviewed plan already
  exists, start with implementation-notes instead.
---

# Implementation Plan

A plan's job is to surface the things the user might actually need to alter,
before changing them becomes expensive. Order it by likelihood of change,
not by execution order.

## Workflow

0. **Check the escape hatch.** If the change is single-file, touches no
   interface, data, or UX, and has only one sensible way to do it, say so in
   one sentence and start — no plan. If a reviewed plan for this task
   already exists, do not rewrite it: confirm it still stands, then start
   implementing with implementation-notes.
1. **Gather the inputs.** Collect what this plan is based on: the brainstorm,
   spec, interview decisions (from earlier in the conversation, or from
   `interview-decisions.md` in the project root if the interview ran in a
   previous session), an existing `implementation-plan.md` when continuing
   earlier planning, the porting checklist from an earlier reference hunt
   (`porting-checklist.md`, if present), any chosen prototype under
   `./design-directions/`, plus a read of the code that will be touched.
   If the chat contradicts
   `interview-decisions.md`, the latest chat statement wins — but promote
   the conflict to a pinned decision entry ("changed from X per your latest
   comment — confirm?"). If key inputs are missing: when the missing answers
   would overturn more than one top decision, run interview-me first;
   otherwise record explicit assumptions marked "(assumed — not confirmed)"
   and pin them at the top of the decision section regardless of sort order.
2. **Sort by likelihood of change, not chronology.** Lead with the decisions
   the user is most likely to tweak — data model and schema changes, new
   type interfaces and API shapes, anything user-facing (examples; the
   authoritative sort key is in Rules). Bury the mechanical refactoring at
   the bottom — the user trusts the agent on that part.
3. **Make the top decisions reviewable.** For each high-change-risk decision:
   the chosen option, 1-2 alternatives considered, and what changing it
   later would cost.
4. **Mark the improvisation zones.** Flag the areas where unknowns are likely
   to surface mid-implementation, and state the fallback posture for each
   (e.g. "pick the conservative option and log it").
5. **End with an explicit go/no-go.** Present the plan in chat — decision
   list first — and ask the user to approve, adjust, or reject. If review
   spans sessions or more than one round, persist the current draft as
   `implementation-plan.md` marked `status: draft` (apply the step 6 exclude
   when first writing it); flip it to `approved` on approval. On a vague
   pass ("looks fine, go ahead"), treat only the decisions actually
   discussed as approved: restate each undiscussed high-risk decision in one
   line, then persist.
6. **On approval, persist and hand off.** Write the approved plan to
   `implementation-plan.md` in the project root (or flip the draft's
   status), in the language of the conversation, using the skeleton below.
   If the file already exists from a different task, never overwrite it
   silently: append a new plan section, or rename the old file to
   `implementation-plan-<date>.md` and say so. Do not commit it unless the
   user asks. If this is a git repo, exclude it locally:
   `n=implementation-plan.md; p="$(git rev-parse --git-path info/exclude 2>/dev/null)" && { mkdir -p "$(dirname "$p")" && { grep -qxF "$n" "$p" || echo "$n" >> "$p"; }; } 2>/dev/null || echo "note: could not exclude $n — leaving it untracked, never staging it"`
   Then suggest starting implementation in a fresh session with
   `implementation-plan.md` (and any prototypes) passed in as artifacts.
   Either way, once implementation kicks off — especially in a new
   session — keep notes per the implementation-notes skill, with
   `implementation-plan.md` as the Context input of
   `implementation-notes.md`.

## When a built-in plan mode is active

The host's native plan file is the only artifact: do not also write
`implementation-plan.md` — this overrides the persist-and-exclude parts of
steps 5-6. Put the decisions-to-review section (same fields as the skeleton)
at the top of the native plan body. Keep todos in execution order, but tag
each todo that hangs off a high-risk decision with that decision's number;
mechanical todos sink within dependency constraints. Approval goes through
the host's native flow — in Claude Code, ExitPlanMode; never ask for
approval in chat there. Downstream, implementation-notes' Context input
points at the native plan file instead.

## Plan skeleton

Translate the section names into the language of the conversation; keep the
four-section structure.

```markdown
# Implementation Plan — <task>

## Decisions & invariants to review   ← review this part
<!-- Decision entries per step 3; invariant entries read
"invariant — must hold" instead of a cost. Do not copy this comment. -->

## Improvisation zones

## Mechanical work   ← no review needed

## Go / no-go
```

## Rules

- The plan is for review, not a contract — it should tell the reader where
  it is likely to be wrong.
- The authoritative sort key: how likely the user is to veto the decision,
  weighted by the cost of changing it later. For refactors with little
  user-facing surface, lead with behavior-preservation risks and public API
  touchpoints instead.
- When one decision determines whether another exists, indent the dependent
  entry under its parent marked "only if A=X", and leave a one-line shadow
  entry for the branch not taken.
- If more than ~7 decisions rise to the top, fully expand only the 3-5
  riskiest and compress the rest to one line each.
- If no decision rises above mechanical, say so in one line and offer to
  start immediately — a plan with nothing to veto is noise.
- Do not start implementing in the same breath as presenting the plan.
- If a plan section would just restate the obvious ("write the code, run
  the tests"), cut it; length is not thoroughness.
