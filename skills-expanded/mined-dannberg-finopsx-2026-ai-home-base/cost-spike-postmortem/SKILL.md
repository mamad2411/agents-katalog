---
name: cost-spike-postmortem
description: Generate a standardized writeup after a cost anomaly has been resolved. Triggers on phrases like "postmortem for the X spike", "writeup for the anomaly", "document what happened with X". Produces a structured document covering timeline, root cause, dollar impact, what was changed, and prevention — so postmortems are comparable across the team over time.
---

# Cost Spike Postmortem

When a cost anomaly has been resolved, generate a standardized writeup. The goal is consistency across postmortems so trends become visible (e.g., "we keep getting hit by retry storms in account X") rather than getting lost in differently-shaped writeups.

## Inputs to confirm before starting

- The original anomaly (service, time window, dollar delta)
- The detection mechanism (alert, ad-hoc query, customer report, finance flag)
- The resolution (what was changed, when, by whom)
- Any related tickets, PRs, or Slack threads

If the user already ran `anomaly-triage` for this incident, ask for the output of that skill — it has most of the inputs.

## Required sections

Every postmortem must include all of these, in this order. If a section genuinely doesn't apply, write "N/A" and explain why — don't omit.

### 1. Summary (3 sentences)

What happened, what the impact was, what was done. Written so a CFO could read just this section and understand.

### 2. Timeline

A bullet list with timestamps. Include at minimum:
- When the spend started
- When it was detected
- When the on-call practitioner began investigating
- When root cause was identified
- When the fix was deployed
- When spend returned to normal

### 3. Root cause

One paragraph. The actual technical cause, not the proximate one. ("A new ETL job did full table scans" is the proximate cause; "we don't run cost-aware tests in CI for new BigQuery jobs" is the actual cause.)

### 4. Dollar impact

- Total anomalous spend (above expected)
- Broken down by service / SKU / project as applicable
- Whether it's recoverable (cloud credits, vendor refund) and how much

### 5. What was changed

The specific actions taken to resolve. Include links to PRs, tickets, or config changes where available.

### 6. Prevention

The hardest section to write well. Three categories:
- **Detection improvements** — would we catch this earlier next time?
- **Process improvements** — what should the team be doing differently?
- **Systemic fixes** — what change would make this class of issue impossible?

For each, note whether it's a committed action item (with owner and date) or just a recommendation.

### 7. Open questions

Anything still unclear that's worth tracking. This is the section that turns into next quarter's investigation work.

## House rules

- No blame. The writeup names systems and processes, not people. ("The ETL pipeline" not "Jane's ETL pipeline.")
- All dollar figures are net of credits unless stated otherwise.
- All times are UTC. If the practitioner gives local times, ask which timezone and convert.
- Length: 1–2 pages. If you're going longer, you're writing too much.

## Output format

Markdown with the section headers above. Filename suggestion: `YYYY-MM-DD-<service>-spike.md` (use the date the spike started, not the date you're writing).

## Skeptic check

Before finalizing, prompt the user with:

- Have you confirmed the dollar figures against the billing export?
- Is the root cause the actual cause, or just the trigger?
- Are the prevention items real (with owners and dates) or aspirational?
