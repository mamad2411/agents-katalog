# comms/meeting-insights — skill payload

> Machine-readable contract: [`../meeting-insights.manifest.json`](../meeting-insights.manifest.json).

## What this skill does

Parses a meeting transcript (Teams, Zoom, Otter; plain text or VTT)
into a structured artefact:

- One-paragraph summary.
- Decisions taken (with the deciding speaker where attributable).
- Action items with owner and inferred due date.
- Open questions / parked items.

Returns both Markdown (for circulation) and a JSON `actions` array (for
piping into a tracker like Planner / Linear / Jira).

## When to use it

- The meeting was recorded and you want minutes you can actually trust.
- A standup / weekly that recurs and would benefit from automated
  action-tracking.

## When **not** to use it

- The transcript is incomplete or low-quality — garbage in, garbage out;
  re-record or transcribe again first.
- The meeting is highly sensitive (legal, M&A) — output sensitivity
  inherits the input; treat accordingly.

## Determinism and risk

Determinism: **low** — extraction is LLM-mediated. Risk: **low** — the
output is advisory and reviewed by the meeting owner before circulation.

## How it composes

Common upstream of `office/docx-toolkit` (formal minutes), and a
natural input to any action-tracker integration.
