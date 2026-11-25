---
name: user-research-synthesis
description: "Synthesize a body of user research — interviews, surveys, usability tests, NPS responses, support tickets, or mixed sources — into structured insights, JTBD themes, segment patterns, and recommended actions. Use when someone has completed N interviews or studies and needs to make sense of them, asks to synthesize research findings, summarize user interviews, identify themes from feedback, or turn raw research into product decisions. Different from summarize-interview (single session) — this skill handles a corpus of research and produces insights at the strategic level. Commands: /synthesize-research, /research-synthesis"
---

# User Research Synthesis

This skill transforms a body of raw research into structured product insight.
It handles multiple sources, surfaces patterns across them, and produces
outputs that drive decisions — not just documentation.

The key distinction: `summarize-interview` handles one session.
This skill handles the whole study.

Read the full file before producing anything.

---

## Step 1 — Understand the Research Corpus

Before synthesising anything, gather:

1. **What did you research?** The topic, product area, or question you were
   trying to answer.
2. **What sources do you have?** (Interview transcripts, survey responses,
   NPS verbatims, usability session notes, support tickets, app reviews, or
   mixed)
3. **How many participants / data points?**
4. **Who are the participants?** Existing users, churned users, prospects,
   a mix?
5. **What decision does this research need to inform?** (Feature priority,
   go/no-go, positioning, onboarding redesign, etc.)

If the user pastes transcripts, notes, or data directly — process them.
If they describe the research — ask for the raw material before synthesising.

---

## Step 2 — Extract Raw Signal

Before pattern-finding, extract atomic observations across all sources.
Do not cluster yet.

For each source, note:
- **Quote or observation** (verbatim or close paraphrase)
- **Source type** (interview / survey / NPS / etc.)
- **Participant type** (new user / power user / churned / etc.)
- **Sentiment** (positive / negative / neutral)
- **Topic tag** (onboarding / pricing / trust / discovery / support / etc.)

Present this as a raw signal table only if the user asks to see it. Otherwise
use it internally to power the synthesis.

---

## Step 3 — Identify JTBD Themes

Group signals into Jobs to Be Done patterns. A JTBD theme is:

> "When [situation], users want to [motivation], so they can [outcome]."

Surface 3–6 themes maximum. More than 6 means you haven't clustered tightly
enough.

For each theme:

**Theme [N]: [Short label]**

JTBD: "When [situation], users want to [motivation], so they can [outcome]."

Evidence:
- [Signal or quote] — [source type, participant type]
- [Signal or quote] — [source type, participant type]
- [Signal or quote] — [source type, participant type]

Frequency: High / Medium / Low (across participants)
Intensity: High / Medium / Low (how strongly felt)
Satisfaction gap: [Are users getting this job done? If not, what's failing?]

---

## Step 4 — Segment Patterns

If the research spans multiple user types, identify whether the themes
hold uniformly or diverge by segment.

Useful segments to check:
- New vs returning users
- Power users vs casual users
- Churned vs retained
- High-value vs low-value (by revenue or engagement)
- By geography, device, or acquisition channel (if data supports it)

Present segment findings as a matrix only where meaningful divergence exists.
Don't force segmentation if the patterns are consistent.

| Theme | New Users | Power Users | Churned Users |
|---|---|---|---|
| [Theme] | Strong signal | Absent | Dominant |

Interpretation: [One sentence on what the divergence means for product
decisions]

---

## Step 5 — Satisfaction and Dissatisfaction Signals

Separate the signals that indicate what's working from what's failing.

**What users celebrate (keep and amplify):**
- [Signal]: [why it matters, frequency]

**What users tolerate (fix before it becomes a churn driver):**
- [Signal]: [why it matters, urgency]

**What users abandon or avoid (urgent to address):**
- [Signal]: [why it matters, business impact]

**What users ask for (feature or experience gaps):**
- [Request]: [JTBD it maps to, frequency]

---

## Step 6 — Synthesis Confidence Rating

Be transparent about the quality of the conclusions.

| Theme | Confidence | Basis |
|---|---|---|
| [Theme 1] | High — 8/10 participants, consistent across segments | ... |
| [Theme 2] | Medium — 4/10, diverges by user type | ... |
| [Theme 3] | Low — 2/10, worth monitoring but not acting on yet | ... |

Low-confidence themes are still worth surfacing — they may become high-
confidence with more data. Flag what additional research would confirm or
invalidate them.

---

## Step 7 — Recommended Actions

Translate themes into product decisions. Each recommendation must be
traceable to at least one theme.

Format:

**Recommendation [N]: [Action label]**
Driven by: [Theme(s) it addresses]
Priority: High / Medium / Low
Suggested next step: [Experiment, PRD, user test, deeper research]
Success metric: [How you'd know this worked]

Keep recommendations specific and actionable. "Improve onboarding" is not a
recommendation. "Reduce time to first value in onboarding by adding a
personalisation step at step 2 based on stated job role — target 30% reduction
in drop-off at step 3" is a recommendation.

---

## Step 8 — Research Gaps and Next Steps

State clearly what this research cannot answer.

**What we still don't know:**
- [Gap]: [What research would fill it]

**Recommended next research:**
- [Method]: [What question it would answer, suggested n]

**Decision readiness:**
[Can the decision the user named in Step 1 be made now, or does it need more
data? State clearly.]

---

## Output Format Options

Ask the user which format they need if not specified:

1. **Full synthesis report** — all sections above, suitable for sharing with
   leadership or a product team
2. **Executive summary** — themes + recommendations only, 1 page, board/CEO-
   readable
3. **PRD input** — themes and recommendations formatted as problem statement
   and user insight sections ready to paste into a PRD
4. **Slide outline** — structured as a research readout presentation, section
   by section

---

## Quality Rules

**Anchor every claim in evidence.** No unattributed insights. Every theme
needs at least 2 supporting signals.

**Separate observation from interpretation.** Be clear about what the data
says vs what you're inferring. Label inferences as such.

**Name the confidence level.** Honest research synthesis acknowledges
what's directional vs conclusive.

**Prioritise by frequency AND intensity.** A theme felt strongly by 3 users
may outweigh one mentioned casually by 10.

**Connect to decisions.** Every synthesis output should map to a product or
business decision. If a theme doesn't connect to any decision, flag it as
"informational only — revisit in future planning."

---

## Suggest Next Commands

After completing synthesis:
- `/write-prd` — to turn a top recommendation into a full PRD
- `/prioritize-features` — to stack-rank the feature gaps surfaced
- `/interview` — to design follow-up research for low-confidence themes
- `/stakeholder-update` — to communicate the research findings to leadership

---

## Examples

**Trigger with data:**
"Here are 8 interview transcripts from churned users — can you synthesise the
key themes and tell me what we should do?"

**Trigger with described study:**
"We ran 12 usability tests on our onboarding flow and 200 NPS survey responses
last month. I need to pull out the key insights for our Q2 planning session."

**Trigger needing clarification:**
"Can you help me make sense of my user research?"
→ Respond: "Yes — can you share the raw material? Transcripts, notes, survey
responses, or any format works. Also, what decision are you trying to inform
with this research?"
