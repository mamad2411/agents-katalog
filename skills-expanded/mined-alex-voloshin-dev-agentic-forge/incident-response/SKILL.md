---
name: incident-response
description: Drive a production incident — classify severity (sev1-4), capture impact and timeline, coordinate mitigation, and draft a postmortem, recorded as an incident handoff. Use for an outage or production issue, to triage or classify an incident, coordinate the response, or write a postmortem. Not routine deploy health checks (deploy-watch) or cutting a release (release).
allowed-tools: Read, Grep, Glob, Bash, Task, Write, Edit
---

# Incident response (phase workflow)

The incident phase: triage a production incident — classify severity, capture impact and timeline,
coordinate mitigation, and draft the postmortem — recorded as an `incident` handoff. The severity
classification is deterministic (`incident-classify` in the plugin's `bin/af.py`); the skill assembles the
record and drives mitigation before root cause. (Design: `docs/architecture/quality-ops.md` in
the agentic-forge repository.)

## When to use

When there is an active or recent incident to triage, coordinate, or write up — an outage, a
degradation, a sev-anything. **Not** for routine rollout monitoring (`deploy-watch`), cutting a
release (`release`), or implementing a fix from scratch (`develop`).

## Process

The classification prints one JSON object and needs nothing installed. Pass a flag for each fact
that holds:

```
python3 -E "${CLAUDE_PLUGIN_ROOT}/bin/af.py" incident-classify --outage --data-loss --degraded --workaround
```

1. **Assess the signal.** From the alerts/impact, determine the facts: is it a full **outage**?
   **data loss**? **degraded** (still working, slower/partial)? is there a **workaround**? For a
   live incident, pull active alerts via a connector (see
   [references/connectors.md](references/connectors.md)). **No signal and no connector** (the
   prompt is all there is): triage from the prompt — take the facts it states, mark each missing
   one `unknown` in the record (onset time, blast radius, workaround, …), classify with the
   conservative default for every unknown (`--degraded` only
   unless the prompt says otherwise), and proceed; ask for the missing facts only when interactive
   — a headless run has no one to ask.
2. **Classify severity.** `incident-classify`
   → `sev1` (outage / data loss), `sev2` (degraded, no workaround), `sev3` (degraded, workaround),
   `sev4` (cosmetic / latent). Use the derived level — do not eyeball it.
3. **Assemble the record.** Write an `incident` handoff (frontmatter `type` (= `incident`),
   `severity`, `status`, `impact`, `timeline` — at least the detection event — `remediation`,
   `action_items`), then validate it (the read-back below;
   see [handoff.md](../../patterns/handoff.md)).
   Then **read the file back** — `python3 -E "${CLAUDE_PLUGIN_ROOT}/bin/af.py" handoff-load --path <path> --type incident` — and
   fix whatever it reports: this reads the file, so it sees the YAML you typed, and a single
   malformed value (a flow sequence with prose after it, an unquoted `:`) leaves an artifact the
   next phase cannot read (ADR 0096).
4. **Mitigate first, then root-cause.** Prioritize the fastest safe mitigation (a workaround or a
   rollback) over a root-cause fix. For an actual code fix or a security angle, fork the relevant
   role (`software-engineer` / `security-engineer`) via `Task`; keep the incident record updated.
5. **Postmortem.** Once resolved, complete the timeline, the root cause, and concrete action items
   (no blame).

## Output

An `incident` handoff: severity, impact, timeline, remediation, and action items — the live record
during the incident and the postmortem after.

## Definition of done

- Severity is classified via `incident-classify` and matches the signal (outage → sev1, etc.).
- Impact, a timeline (≥ the detection event), and remediation are captured; mitigation is
  prioritized over root cause.
- A valid `incident` artifact is produced; the postmortem (when resolved) has action items, no blame.
