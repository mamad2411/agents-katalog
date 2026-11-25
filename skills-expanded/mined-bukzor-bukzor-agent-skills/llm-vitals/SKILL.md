---
name: llm-vitals
disable-model-invocation: true
description: "Agent MUST load for 'vitals'/'check-in'/'checkin' commands, wellness journaling, or surfacing wellness-vital debt"
---
--- # workaround: anthropics/claude-code#13003
triggers:
    - read: skill://llm-kb
default: vitals checkin
---

# Vitals — Wellness Check-In (MVP)

Multi-axis attention system; see `design.kb/010-mission.md` for the full
vision. **Only the wellness check-in worksheet is implemented.** The
picker, two-tier SLOs, runway, and themes remain design-only.

## Scope today: one verb

**`vitals checkin`** — the wellness worksheet. Scaffold one dated
worksheet, stage it blank, and let the operator fill its sections in
their editor. Nothing else. Observability floor before metrics
(`design.kb/030-requirements.kb/tier-1-before-tier-2.md`).

## The four wellness vitals

| vital          | captures                                          | cadence |
|----------------|---------------------------------------------------|---------|
| body           | sleep, movement, food, daylight                   | weekly  |
| relationships  | substantive contact — conversations, not texts    | weekly  |
| restoration    | waking recovery: solitude, stillness, screen-free | weekly  |
| meaning        | creative / purpose-aligned activity, non-work     | weekly  |

Authoritative rationale and rejected alternatives:
`design.kb/040-design.kb/wellness-vital-selection.md`. Uniform weekly
cadence is an MVP choice; asymmetric-by-rot-rate is a later refinement
once entries reveal which vital gets skipped.

## Configuration — decoupled data location

The skill MUST NOT hardcode where data lives
(`design.kb/030-requirements.kb/decoupled-data-location.md`). Read config
from `~/.claude/llm-vitals/config.yaml`:

```yaml
vitals_root: /abs/path/to/vitals    # tilde is NOT auto-expanded
cadence_days: 7
vitals: [body, relationships, restoration, meaning]
```

If the config file is absent, offer to create it before proceeding.

## Storage — one worksheet, sections are observations

Each checkin is **one** dated file `<vitals_root>/<YYYY-MM-DD>.md` with a
`## <vital>` heading per vital. The four vitals are **sections, not
directories** — one file to edit, four observations to read. Per-vital
recency is derived by section: a vital is "checked in" on the dates of
worksheets whose section for it is non-empty. (This diverges from
`design.kb/040-design.kb/vital-kinds.md`, which specifies a per-vital
`.kb/`; the worksheet model is an MVP ergonomics choice, reconcile later.)

## `vitals checkin` — the flow

Capture happens **in the operator's editor**, in ONE file. The skill
scaffolds a dated worksheet, stages it blank, and hands over a single
`vim` command; the fill-in reads back as a clean `git diff`.

1. Determine staleness from existing worksheets: for each vital, the
   newest `<vitals_root>/*.md` whose `## <vital>` section has content.
   `debt_days = today − that date` (∞ if never). MVP: all four share a
   weekly cadence, so one worksheet covers them together. Skip the
   checkin entirely if the latest worksheet is still green.
2. Scaffold and stage one worksheet:
   ```sh
   sed "s/{{DATE}}/<DATE>/g" skeleton/worksheet.template.md \
       > <vitals_root>/<DATE>.md
   git -C <vitals_root-repo> add <vitals_root>/<DATE>.md
   ```
   Staging the blank-but-scaffolded worksheet as the baseline is the
   trick: whatever the operator types under each section is exactly the
   `git diff`.
3. Hand over ONE command (operator runs it via the `!` prefix — vim is
   interactive, Claude can't drive it):
   ```
   ! vim <vitals_root>/<DATE>.md
   ```
4. When control returns, read the fill-in with
   `git -C <vitals_root-repo> diff -- <vitals_root>/<DATE>.md`. Each
   `## <vital>` section with content is one observation; an untouched
   section means that vital was not checked in (stays in debt).
5. Stage the filled worksheet so the next checkin starts from a clean
   baseline.

## Automation boundary — the content is the operator's

`design.kb/040-design.kb/automation-boundary.md`: the entry content is
the signal, so it MUST be the operator's own assessment. The vim-and-diff
flow enforces this structurally — Claude scaffolds and stages, the
operator authors in their editor, Claude reads the diff but never edits
the body. Claude may **surface** context as a prompt ("you mentioned a
rough night Tuesday"), but MUST NOT type into the entry. Confabulated
wellness data is worse than a missing entry.

## Anchoring (later)

Designed to fire at session-start (show worksheet) and session-end
(prompt stale rows) — see `design.kb/040-design.kb/anchoring.md`. Wiring
into those skills is a future step; for now, invoke `vitals checkin`
explicitly.
