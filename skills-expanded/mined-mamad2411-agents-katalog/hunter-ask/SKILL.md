---
name: hunter-ask
description: >-
  The human-in-the-loop protocol for an autonomous-but-supervised hunt. Defines
  the four sanctioned interaction points (surface-map review, mid-hunt steering,
  blocking escalation, post-hunt triage), a question budget with per-question
  defaults and fallbacks so an unattended hunt proceeds deterministically, the
  blocking-vs-non-blocking rule, and the exact question payload schema the TUI and
  the Claude Code plugin both render. Load whenever about to ask the operator
  anything, escalate for credentials or a destructive-action authorisation, flag
  spec ambiguity, request scope confirmation, or when running unattended and a
  decision point is reached. Assumes hunter-doctrine is loaded.
---

# Hunter Ask

Hunter is autonomous, not unsupervised. The difference is this skill: a small,
fixed set of moments where operator input has real leverage, a hard budget so
Hunter never turns into a chat prompt, and a default on every question so an
unattended hunt runs to completion deterministically instead of hanging.

Escalating is cheap. A wrong assumption executed 200 times across a surface map is
not. But asking too often is also a failure — it converts an autonomous harness
into a manual one. The budget and the four sanctioned points hold both lines.

## The four sanctioned interaction points

Ask only at these. A question that does not belong to one of the four is noise.

| # | Point | When | Blocking? |
|---|---|---|---|
| a | **Surface-map review** | Before the hunt, after hunter-recon builds the map | Blocking by default; auto-confirms in unattended mode |
| b | **Mid-hunt steering** | During the hunt | Non-blocking — the hunt continues while the question is open |
| c | **Blocking escalation** | On a hard gate mid-hunt | Blocking — the affected surface pauses |
| d | **Post-hunt triage** | After Finds are triaged, before final delivery | Blocking on delivery; auto-accepts in unattended mode |

### (a) Surface-map review

The operator confirms or edits scope and marks **forbidden surfaces** — surfaces
Hunter must never probe (production write endpoints, real payment rails, an email
send, a data-deletion path). A forbidden surface is recorded `dark` with reason
`operator-forbidden`, never `cold`. The operator may add missed surfaces, correct
a mis-mapped one, and set the budget. Present the map as a diffable list, not
prose.

### (b) Mid-hunt steering

Non-blocking adjustments: reprioritise the queue, add a surface, kill a surface,
raise the budget. Hunter keeps probing while the question sits open; if it expires
unanswered, the default applies and the hunt is unchanged. Steering never
retroactively invalidates a Find already proven.

### (c) Blocking escalation

The only three reasons to hard-block a surface:

1. **Credentials required** and none provided. Never attempt to bypass a control
   you were not asked to test — that is a forbidden action, not a clever probe.
2. **Destructive-action authorisation** — promotion needs an irreversible or costly
   action (payment, email send, data deletion, production write). Present the exact
   action and its cost; do not perform it on a default of "yes". Its default is
   always the safe branch (skip / mark dark).
3. **Genuine spec ambiguity** — the expected behaviour is not settled by implicit
   correctness, a spec line, or a recorded baseline. State the two readings and
   which one the default assumes.

Only the affected surface pauses; the rest of the hunt continues.

### (d) Post-hunt triage

The operator accepts, rejects, or merges Finds. **Reject-with-reason feeds back to
the Range** as labelled ground truth — a rejected Find with reason
`not-a-deviation` or `intended-behaviour` becomes a Range case that measures
whether Hunter over-reports. Merge decisions are handed to hunter-triage's merge
ledger. Accept is the terminal state that clears a Find for hunter-report.

## Question budget

**Default: at most 3 open questions at any one time.** A fourth waits until one of
the three resolves. This caps the operator's cognitive load and forces Hunter to
prioritise which uncertainty is worth a human's attention.

Every question MUST carry:

- a **recommended default** — the action Hunter takes if unanswered, and
- a **stated fallback** — what happens to the surface/hunt when the default is
  applied (e.g. "surface marked dark", "budget unchanged", "Find accepted").

Because every question has a default, an unattended hunt never hangs: each
question auto-resolves to its default on expiry and the hunt proceeds
deterministically. Blocking questions still pause their surface until answered or
expired; they do not pause the whole hunt.

## Blocking vs non-blocking decision rule

```
Ask: does proceeding on the default risk irreversible harm, a boundary breach,
     a security bypass, or wasting the whole remaining budget?
  YES → blocking. Pause the affected surface. Default is always the SAFE branch
        (skip / mark dark / do-not-perform).
  NO  → non-blocking. Keep hunting. Default applies on expiry.
```

Credentials, destructive-action authorisation, and forbidden-surface confirmation
are always blocking. Reprioritisation, adding/killing a non-destructive surface,
and budget raises are non-blocking. The surface-map review is blocking as a whole
because everything downstream depends on scope, but auto-confirms unattended.

## Question payload schema

The single schema both the TUI and the Claude Code plugin render. Both consume
this verbatim; neither invents fields.

```json
{
  "question_id": "q/2026-08-07T14-05Z-01",
  "hunt_id": "hunt/2026-08-07T14-02Z",
  "point": "escalation",
  "blocking": true,
  "surface": "GET /admin/export",
  "prompt": "GET /admin/export requires admin credentials; none provided. Probe it?",
  "reason": "credentials-required",
  "options": [
    { "id": "provide", "label": "provide credential", "input": "secret", "effect": "probe the surface" },
    { "id": "skip", "label": "skip", "effect": "mark surface dark (operator-declined)" }
  ],
  "recommended_default": "skip",
  "fallback": "surface marked dark with reason operator-declined; hunt continues",
  "expires": "2026-08-07T14:20:00Z",
  "cost": null,
  "resolved": { "choice": null, "by": null, "at": null, "assumption": false }
}
```

Field rules:

- `point` ∈ `surface-map` | `steering` | `escalation` | `triage`.
- `blocking` follows the decision rule above; on a destructive action, `cost`
  states the exact cost (money, rows affected, irreversibility) in the prompt.
- `recommended_default` MUST reference an option `id`; `fallback` states the
  surface/hunt effect in plain terms.
- A credential option uses `"input": "secret"` so the renderer masks it and it is
  never written to the report or logs.
- `resolved.assumption` is set `true` when the default was auto-applied unattended
  (see below).

## Unattended mode

When no operator is attached, Hunter does not stall and does not guess silently.
Every question auto-resolves to its `recommended_default` at `expires` (or
immediately, if configured `--unattended`), sets `resolved.assumption = true`, and
is logged as an **assumption** carried into hunter-report's `assumptions` array.
The report states each assumption beside the verdict so the reader knows which
decisions a human did not make.

Consequences that fall out of the safe-default rule: forbidden and
credentials-required surfaces auto-mark `dark`, which caps the verdict at
`PASS (LIMITED COVERAGE)` at best; destructive actions are never performed; Finds
auto-accept at triage. An unattended hunt is therefore honest-by-construction — it
can never claim a surface it did not dare probe was clean.

## Worked example — an unattended escalation

The example payload above expires with no operator. Hunter applies default `skip`:
`GET /admin/export` is marked `dark` with reason `operator-declined`,
`resolved.assumption = true`, and hunter-report logs
`assumption: GET /admin/export left dark — credentials-required, defaulted skip`.
The verdict cannot exceed `PASS (LIMITED COVERAGE)` because a surface is dark. No
credential was invented; no control was bypassed.

## Handoff

- Surface-map edits and forbidden marks flow into the surface map hunter-recon
  produced and every later denominator.
- Merge decisions at triage flow to hunter-triage's merge ledger.
- Reject-with-reason flows to the Range as labelled ground truth.
- Assumptions flow to hunter-report's `assumptions` array and are rendered beside
  the verdict.

## Self-check before asking or auto-resolving

- [ ] The question belongs to one of the four sanctioned points
- [ ] At most 3 questions open at once
- [ ] Every question has a recommended default and a stated fallback
- [ ] Blocking flag matches the decision rule; blocking defaults are the safe branch
- [ ] Credentials never bypassed; destructive actions never performed on a default
- [ ] Unattended auto-resolutions logged as assumptions and carried to the report
- [ ] Forbidden and credential-declined surfaces marked dark, never cold
