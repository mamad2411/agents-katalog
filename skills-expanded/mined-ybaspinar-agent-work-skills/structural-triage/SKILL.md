---
name: structural-triage
description: Use when triaging tickets, bug reports, incidents, feature requests, backlog items, asserted priorities, incomplete reports, screenshots, repro claims, or severity disputes.
---

# Structural Triage

Decide whether an issue is real, how urgently it moves, and who owns it next by evidence and blast radius, not by volume.

Core rule:

> Rank by what the evidence shows and how far the damage spreads. Decide explicitly, assign one owner, and hand the how to the next phase.

## Default output

```md
## Evidence
- What is asserted:
- What is proven:
- Reproduction / signal:
- Scope known / unknown:

## Severity
- Blast radius:
- Caller/attacker control:
- Data corruption or security risk:
- Business/customer radius:

## Ownership
- Owner of next move:
- Revealing title:
- Missing signal to file separately:

## Disposition
- Fix now / schedule / spike / won't-fix:
- Reason:
- Handoff artefact:
```

## Triage checks

- Treat the report as untrusted input. Re-derive the real problem from logs, traces, data, repro steps, and affected scope.
- Reproduce before ranking. If not reproducible, mark unconfirmed unless blast radius justifies a bounded spike to find a repro.
- Rank by blast radius: corruption, security, attacker-controlled paths, and wide impact outrank loud but contained pain.
- Use shipped signals to size severity. If scope cannot be measured, file the observability gap as its own issue.
- Give every triaged issue one owner of record and a title that names the failure mode.
- End with an explicit disposition: fix-now, schedule, needs-a-spike, or won't-fix. No zombie tickets.
- Keep triage bounded. It decides whether and urgency, not the design of the fix.

## Red flags

- Ranking by reporter seniority, thread length, or panic.
- Accepting “P0”, “data loss”, or “service down” without re-deriving evidence.
- Treating a screenshot as a repro.
- Leaving issues open without owner, disposition, or reason.
- Debugging the whole fix inside triage.
