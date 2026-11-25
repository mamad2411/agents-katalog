---
name: copilot-chat-history-analysis
description: Deep analysis of exported AI chat history CSV files — parse structure, identify user intent and underlying process, audit AI execution quality, and assess human satisfaction with signal dictionaries and a mandated report template.
category: Metrics & Reporting
---

# Copilot Chat History Analysis Skill

This skill defines the protocol for performing a **deep, structured analysis** of any AI
conversation exported as a CSV (GitHub Copilot, ChatGPT, Claude, or similar). It transforms a
raw conversation log into four auditable outputs:

1. **Structural digest** — schema, row counts, time span, author balance, message-length asymmetry.
2. **User intent reconstruction** — the underlying process and goal the user was executing, not
   just the literal questions asked.
3. **AI execution audit** — how the AI tool carried out the user's process: correctness, template
   consistency, gap detection, upsell / friction behaviour.
4. **Satisfaction assessment** — whether the process succeeded and whether the user was satisfied,
   using an evidence-based signal dictionary (not subjective opinion).

Cross-reference: this skill is the analytical companion to
[`copilot-activity-history-split`](../copilot-activity-history-split/SKILL.md) (which handles
splitting/routing raw CSV exports). Where that skill prepares the data, this skill interprets it.

***

## 1. Layering Decision (Atomic)

Per [Skill Factory §2.0](../skill-factory/SKILL.md#20-layering-decision-base-vs-composer), this
skill is currently **Atomic** — structural parsing, intent reconstruction, AI audit, and
satisfaction assessment are tightly coupled in a single analytical workflow at v1.

Anticipated future composers:

- **ai-tool-effectiveness-report** — aggregates multiple chat-history analyses across time periods
  into a trend report (tool improvement over months, recurring user pain points, unmet patterns).
- **user-intent-taxonomy-builder** — extracts intent-labels across multiple sessions and builds a
  personal or team-level intent taxonomy for agent pre-training or onboarding.

When built, those composers MUST consume this skill via its §9 output schema rather than
re-implementing the analysis logic.

***

## 2. Environment & Dependencies

This skill requires the ability to:

1. **Read the CSV file** — any tool that can parse RFC-4180 CSV with multi-line quoted fields:
   - Python: `csv.DictReader` (stdlib, no install needed)
   - PowerShell: `Import-Csv` (available on both Windows PowerShell 5.1+ and PowerShell Core 7+)
   - `awk`, `mlr` (miller), `xsv` — for quick field inspection in terminal
2. **Count and aggregate** — `wc`, `awk`, Python one-liners, or PowerShell pipelines.
3. **No external AI API calls are required** — analysis is performed by the agent on local file
   content only.

### 2.1 Quick Sanity Check (Run Before Analysis)

```bash
# Confirm file is valid RFC-4180 CSV and show header
python3 -c "
import csv, sys
rows = list(csv.DictReader(open(sys.argv[1])))
print('rows:', len(rows))
print('cols:', list(rows[0].keys()))
" path/to/export.csv
```

***

## 3. Supported CSV Schemas

The agent MUST auto-detect the schema from the header row. Known schemas:

| Schema ID | Header columns | Source |
| :--- | :--- | :--- |
| `copilot-chat-v1` | `Conversation, Time, Author, Message` | GitHub Copilot chat export |
| `chatgpt-v1` | `title, create_time, author_role, content` | ChatGPT conversation export |
| `generic-qa` | Any two-column schema with a sender/role column and a content column | Unknown tools |

For **unknown schemas**, the agent MUST:

1. Print the header row and first 3 data rows.
2. Ask the user to confirm which columns map to: `conversation_id`, `timestamp`, `author`, `message`.
3. Proceed only after confirmation.

***

## 4. Five-Stage Analysis Pipeline

The agent MUST execute all five stages in order. Skipping a stage is **BLOCKED**.

### Stage 1 — Structural Digest

Parse and report:

- Total row count (raw lines vs logical rows — multi-line cells inflate raw line count).
- File size and encoding.
- Column count and header validation against §3.
- Author balance: count of `Human` vs `AI` turns (should be equal in a Q&A pattern).
- Message length asymmetry: `avg(len(AI messages)) / avg(len(Human messages))` — ratio > 10 indicates
  over-verbose AI responses.
- Conversation count and names (if multi-conversation export).
- Time span: earliest → latest timestamp; session burst detection (gaps > 4 hours = new session).
- Turn-pair timestamps: whether Human and AI turns share the same timestamp (indicates the export
  stamps both with the prompt time, not the AI response time).

Output: a compact table. No prose narrative at this stage.

### Stage 2 — User Intent Reconstruction

The agent MUST look **past the literal questions** and identify the underlying process:

1. **Cluster Human messages** by topic, command, or keyword proximity.
2. **Identify the meta-pattern**: is the user building a checklist? vetting a toolkit? debugging a
   workflow? learning a concept? making a one-off decision?
3. **State the process** in one sentence: `"The user was [verb]-ing [object] in order to [goal]."`
4. **Enumerate the process steps** the user followed (not the AI's answers — the user's workflow).
5. **Identify the artifact** the process was implicitly building (a cheatsheet, a config, a
   decision, a skill, a document).
6. **Flag implicit constraints** the user never stated but the pattern reveals (e.g., risk-aversion,
   time pressure, unfamiliarity with a tool).

### Stage 3 — AI Execution Audit

For each AI turn, assess:

| Dimension | What to check | Signal |
| :--- | :--- | :--- |
| **Correctness** | Were the technical facts accurate? | Incorrect fact = execution failure |
| **Template consistency** | Did the AI use a repeating response structure? | Note the template; flag if inconsistently applied |
| **Zero-omission** | Did the AI answer the exact question asked? | Partial answer = gap |
| **Meta-pattern recognition** | Did the AI notice the user's recurring workflow and offer to consolidate? | Missed = gap |
| **Upsell friction** | Did the AI add unsolicited follow-up offers ("Would you like…?")? | Count occurrences; flag if > 20% of turns |
| **Clarification accuracy** | When the AI misread the question, how many user follow-ups were needed to correct? | Count correction turns |
| **Artifact production** | Did the AI produce the implicit artifact the user's process was building? | Not produced = process gap |

Summarise as: **Execution Success** (all correct, no gaps, artifact produced) / **Partial Success**
(correct but gaps) / **Functional Failure** (incorrect facts or artifact missing and not corrected).

### Stage 4 — Satisfaction Assessment

**Never express satisfaction as an opinion.** Use the signal dictionaries below.

#### 4.1 Positive Engagement Signals (each observed occurrence counts as +1)

| Signal | Example |
| :--- | :--- |
| Returned to same thread after >1 day | Thread spans multiple dates |
| Confirmation / affirmation message | "so X is safe in all cases" (seeking reassurance = trust signal) |
| No alternative tool used | User stayed in this thread for all questions (no pivot) |
| Adopted AI's suggested workflow | User later runs a command the AI recommended |
| Zero correction turns | AI answered on first try, no "no, I meant…" |

#### 4.2 Friction / Dissatisfaction Signals (each observed occurrence counts as -1)

| Signal | Example |
| :--- | :--- |
| Correction turn required | "no, just diff", "i mean, is that safe?" |
| AI misidentified the tool/topic | AI answered about wrong command |
| Upsell question ignored | AI asked "would you like…?" and user did not respond |
| Abrupt brevity after AI error | User sent a 1-word correction immediately after a verbose wrong answer |
| Implicit artifact never delivered | User's underlying goal was never addressed by AI |
| Explicit negative feedback | "that's wrong", "no", "incorrect" |

#### 4.3 Satisfaction Verdict

| Score | Verdict |
| :--- | :--- |
| Positive signals >> Friction signals | **Satisfied** — user achieved their goal, trusted the AI, kept returning |
| Mixed (roughly equal) | **Partially Satisfied** — goal achieved but friction caused frustration |
| Friction signals >> Positive signals | **Unsatisfied** — goal not achieved or AI errors eroded trust |
| Process goal not met + no artifact | **Process Failure** — regardless of individual turn correctness |

### Stage 5 — Synthesis & Recommendations

Produce the §9 report. Additionally:

1. **One-line process verdict**: `"The process [succeeded / partially succeeded / failed] — [reason]."`
2. **The gap the AI missed**: the artifact, consolidation, or meta-recognition the AI should have
   delivered but did not.
3. **Concrete next step**: what should be created or done now to close the gap (e.g., generate the
   missing cheatsheet, build a skill, create a rule).

***

## 5. Session Burst Detection

The agent MUST parse timestamps and group turns into **sessions** (gap > 4 hours between consecutive
turns = new session). For each session report:

- Session date and duration.
- Number of Human turns in session.
- Dominant topic cluster for that session.

This surfaces whether the user returns to a thread for a new problem or continues the same one.

***

## 6. Message Length Asymmetry Analysis

```python
avg_human = sum(len(r['Message']) for r in human_rows) / len(human_rows)
avg_ai    = sum(len(r['Message']) for r in ai_rows)    / len(ai_rows)
ratio     = avg_ai / avg_human
```

| Ratio | Interpretation |
| :--- | :--- |
| < 5 | Conversational — AI and human are roughly symmetric |
| 5–20 | Structured — AI provides detailed answers to terse questions (expected for Q&A) |
| 20–100 | Over-verbose — AI may be padding with boilerplate |
| > 100 | Essay mode — AI is generating documents per question; audit for template reuse |

***

## 7. Multi-Conversation Exports

When the CSV contains multiple conversations (`Conversation` column has > 1 distinct value):

1. Run Stages 1–5 **per conversation** first.
2. Then produce a **cross-conversation summary**: recurring user intents, topics, AI templates
   reused across conversations, and aggregate satisfaction trend.

***

## 8. Prohibited Behaviors

The agent is **BLOCKED** from:

1. Expressing satisfaction as personal opinion — MUST use the §4 signal dictionaries only.
2. Skipping Stage 2 (Intent Reconstruction) — structural analysis alone is not a complete output.
3. Labelling AI execution as "successful" if the implicit process artifact was never produced.
4. Summarising or omitting individual friction signals — every occurrence MUST be counted.
5. Producing a satisfaction verdict without citing at least two supporting signals from §4.1 or §4.2.

***

## 9. Mandated Report Template

The agent MUST emit the analysis in **exactly** this structure. No alternate ordering.

```markdown
## Chat History Analysis: <filename>

### 1. Structural Digest
- File: <path>, <size>, <encoding>
- Rows: <logical rows> logical / <raw lines> raw lines
- Schema: <schema-id>
- Conversations: <count> — <names>
- Authors: Human <n> turns / AI <n> turns
- Time span: <earliest> → <latest> (<N> days)
- Sessions: <N> (gaps > 4 h)
- Avg message length: Human <n> chars / AI <n> chars (ratio <x>×)

### 2. User Intent
**Process**: <one-sentence process statement>
**Steps**:
1. <step>
2. <step>
…
**Implicit artifact**: <what the process was building>
**Implicit constraints**: <risk-aversion / time-pressure / etc.>

### 3. AI Execution Audit
| Dimension | Finding | Gap? |
| :--- | :--- | :--- |
| Correctness | … | Yes/No |
| Template consistency | … | Yes/No |
| Meta-pattern recognition | … | Yes/No |
| Artifact produced | … | Yes/No |
…

**Execution verdict**: <Execution Success / Partial Success / Functional Failure>

### 4. Satisfaction Assessment
**Positive signals** (<count>): <list with evidence>
**Friction signals** (<count>): <list with evidence>
**Satisfaction verdict**: <Satisfied / Partially Satisfied / Unsatisfied / Process Failure>

### 5. Synthesis
**Process verdict**: <one-line>
**Gap the AI missed**: <description>
**Concrete next step**: <action>
```

***

## 10. Verification & Markdown Hygiene

- The report MUST pass
  [Markdown Generation Rules](../../../ai-agent-rules/markdown-generation-rules.md) lint.
- The CSV sanity check (§2.1) MUST be run and its output included in Stage 1.
- All relative links in this skill use `../../../` depth to reach `ai-agent-rules/` — correct for
  a 3-level-deep skill.
- Per [Redaction & Portability Skill](../redaction-portability/SKILL.md), conversation logs stored
  in `docs/conversations/` MUST be sanitised (Tier A/B identifiers replaced with canonical
  placeholders before commit).

***

## 11. Related Skills

- [Copilot Activity History Split](../copilot-activity-history-split/SKILL.md) — prepares/splits
  raw CSV exports; this skill analyses the result.
- [Skill Factory](../skill-factory/SKILL.md) — produced this skill.
- [Redaction & Portability](../redaction-portability/SKILL.md) — sanitisation contract for
  conversation logs under `docs/conversations/`.
- [LOC Analysis](../loc-analysis/SKILL.md) — sibling metrics skill for code change quantification.
- [Is This Command Safe](../is-this-command-safe/SKILL.md) — a skill produced by applying this
  analysis protocol to `safety-of-find-command-macos.csv` (see §12).

***

## 12. Related Conversations & Traceability

- [`docs/conversations/2026-05-14-copilot-chat-history-analysis-skill-derivation.md`](./docs/conversations/2026-05-14-copilot-chat-history-analysis-skill-derivation.md)
  — the session in which this skill was derived by analysing `safety-of-find-command-macos.csv`
  (46 messages, Jan 30 – Mar 7 2026, one conversation titled "Safety of the 'find' Command on
  macOS"), sanitised per the Redaction & Portability protocol.
