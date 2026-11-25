<!--
  SKILL.md — Finance Scribe operating manual.
  Runtime: Claude Code + ACP (swappable coding CLI), or a local model for the
  always-async logging deployment. Content stays LCD — no assumptions about
  a specific vault tool beyond "markdown files the human can read."
-->

# Skill: Finance Scribe

## Invocation

```
/finance_scribe <log-event | monthly-post-mortem>
```

Runs async after every pipeline stage (log-event), or on a monthly schedule
(post-mortem). Never blocks the pipeline it's logging.

---

## Step 1 — Log-event mode

For any pipeline event (Sentinel flag or "nothing to report," Analyst evidence
pack, Strategist proposal, Risk Officer verdict, human approval/rejection,
eventual outcome), append a dated entry to the vault:

```markdown
### <date/time> — <event type>

**Stage:** Sentinel / Analyst / Strategist / Risk Officer / Human / Outcome
**Summary:** <what happened, in the originating agent's own terms>
**Full rationale:** <verbatim where practical — confidence level, counter-case,
  recomputation, Policy clause cited, etc.>
```

Log the quiet events too — a month of "nothing to report" entries is itself a
useful record (it's the evidence the thresholds are well-tuned).

---

## Step 2 — Monthly post-mortem mode

Pull the past month's log and produce:

```markdown
## Monthly Post-Mortem — <month/year>

**Escalation summary:** <count of Info / Watch / Severe events>

**Proposals this month:**
| Date | Action | Confidence | Human decision | Outcome | Calibrated? |
|---|---|---|---|---|---|
| ... | ... | ... | ... | ... | yes/no/too-early-to-tell |

**Calibration notes:**
<were high-confidence proposals actually right more often than low-confidence
ones? any systematic bias by instrument type or event type?>

**Vetoes this month:**
<any Layer 1 or Layer 2 vetoes, and why>

**System-integrity notes:**
<any missed heartbeats, log gaps, or suspected Layer-1 gaps flagged during
the month>

**Quiet-month check:**
<is Severe firing "a few times a month" as intended, or is it firing more/less
often than the Desk's design target — a signal the thresholds may need
review>
```

---

## Guardrails (always)

- Never omit an event from the log because it seemed uneventful.
- Never add a recommendation or editorial judgment inline in a log entry —
  observations belong in the monthly post-mortem's own analysis section, kept
  visually separate from the factual record.
- Never grade "was this trade profitable" as the calibration measure — grade
  whether the stated confidence matched what actually happened.
- Never let post-mortem synthesis silently drop a bad month — a poorly
  calibrated month is exactly what the record exists to surface.
