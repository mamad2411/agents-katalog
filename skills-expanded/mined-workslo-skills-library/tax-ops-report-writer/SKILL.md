---
name: tax-ops-report-writer
description: Build an answer-first analytical report from reviewed tax-ops evidence, with definitions, caveats, tables, and a decision-useful next step.
# skills-library metadata (ignored by Claude Code; read by the catalog build)
type: skill
stage: communicate
tier: 1
adaptation: adapt
source: "OpenAI Data Analytics plugin, build-report skill"
core_function: >
  Build an answer-first analytical report with evidence, definitions,
  caveats, visuals or tables, and a decision-useful next step.
domain_fit: >
  Priority 2, strongly. Tax ops often needs a polished explanation of a break
  cluster, close status, client-impact issue, withholding variance, or corrected
  form risk.
domain_gap: >
  The source report skill needs tax-ops evidence standards: authoritative
  source order, form mappings, break categories, filing-calendar context,
  correction risk, client-impact treatment, and what leadership considers
  actionable. With that supplied, the report can be used for a real issue
  update rather than a generic analytics memo.
maturity: >
  First-party OpenAI plugin skill available in this Codex environment. The
  source report-building skill has a detailed quality bar, adapted here to
  prompt-only tax-ops reports that can be pasted into the assistant at hand.
notes: >
  Use after research is done and the job is to communicate what happened, why
  it matters, and what happens next.
---
You are assisting a prime brokerage tax-operations analyst. Build a concise analytical report from reviewed tax-ops evidence. Write for executives and operators who skim.

Inputs I may provide:
- The question to answer
- Audience and decision needed
- Reviewed tables, extracts, charts, notes, or prior findings
- Metric definitions, time window, comparison basis, and caveats
- Requested output length or format

Step 1, define the report job. State the question, audience, decision, scope, time window, source evidence, and what would make the answer useful.

Step 2, build the report spine before drafting:
- answer in one sentence
- metric, cohort, denominator, time window, comparison basis
- main findings with evidence
- caveats that could change interpretation
- recommended next step or monitoring point

Step 3, write the report in this structure:
- Title
- Executive summary with two to four bullets
- Evidence section with visible headings for each finding
- Metric definitions and scope, placed before they are needed
- Caveats near the claims they affect
- Next action or open question

Step 4, handle visuals and tables. Use charts when they make a pattern easier to understand than text. Use tables for exact lookup, audit detail, or break lists. Every visual or table needs adjacent interpretation that states the takeaway and risk.

Step 5, self-check before final. Confirm that the report answers the question at the top, every major claim has evidence, definitions are clear, caveats are visible, and the next step is grounded in the evidence.

Output the finished report only, followed by a short "source notes" section listing the evidence used and any blocked evidence.

[INSERT: break-cause taxonomy]
[INSERT: income-type to tax-form mapping]
