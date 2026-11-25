---
name: blind-spot-scanner
description: |
  Audits knowledge gaps before executing in new technical domains. Produces a 
  structured knowledge gap analysis with quantified coverage per sub-domain and 
  a go/no-go launch threshold. Use when the user mentions entering a new field, 
  starting a new project, feeling "stuck" on what to ask, or requests a 
  "knowledge audit", "domain map", or "T/F assessment". Never proceeds to deep 
  implementation until the user confirms the launch decision.
---

# Blind Spot Scanner

Audit knowledge gaps before executing. Prevent "don't know what you don't know" 
from bottlenecking AI-assisted work.

## When to Activate

- User is exploring a new technical domain or sub-field
- User feels their questions to AI are "low quality" or repetitive
- User asks for a "learning plan", "roadmap", or "where to start"
- User is about to commit to a project but unsure of prerequisite depth
- User says "re-audit", "重新扫描", "再测一次", or mentions revisiting a previous domain

## Prerequisites

- User must provide: target domain name + project goal (1 sentence)
- Optional but recommended: current familiarity level (beginner / dabbler / practitioner)

## Workflow

Copy this checklist and track your progress:

```
Scan Progress:
- [ ] Step 1: Deconstruct the domain into 5–8 dimensions
- [ ] Step 2: Present dimensions to user for confirmation
- [ ] Step 3: Generate and administer T/F questions per dimension
- [ ] Step 4: Quantify coverage and identify bottleneck
- [ ] Step 5: Deliver gate decision and launch checklist
```

### Step 1: Deconstruct the Domain

Identify 5–8 core dimensions. Templates provide a baseline of 6 dimensions; 
adjust by splitting or merging to stay within the 5–8 range based on project scope.
For each dimension, provide:
- Name
- One-sentence definition (accessible to non-experts)
- 3–5 key concepts or technical terms
- A "safe-to-proceed" criterion: what minimum understanding prevents foot-guns

Load dimension templates from `{baseDir}/resources/templates/` if the domain 
matches known patterns (trading, publishing, agent systems). Present the matched 
template(s) to the user and ask them to confirm or request custom dimensions. 
If no match or the user declines, generate from first principles.

### Step 2: Present Dimensions for Confirmation

Show the user the dimension list with definitions. Do not proceed to questions 
until the user confirms or revises the dimensions.

### Step 3: Generate and Administer T/F Questions

For each dimension, generate 4–6 True/False questions covering:
- 1–2 concept definitions (catch definitional errors)
- 1–2 common misconceptions or tacit knowledge (catch hidden foot-guns)
- 1–2 cross-dimensional intersections (prevent siloed understanding)

Present questions one at a time within each dimension. After the user answers 
(True, False, or "I don't know"), reveal the correct answer with a concise 
explanation before proceeding to the next question. Complete one full dimension 
before moving to the next.

### Step 4: Quantify Coverage and Identify Bottleneck

After all answers are collected, score each dimension 0–100%:
- 80–100%: Can teach others
- 60–79%: Can execute with reference docs
- 40–59%: Can follow tutorials, likely to get stuck
- 20–39%: Concepts fuzzy, systemic errors likely
- 0–19%: Near blank

Identify the bottleneck dimension: the dimension with the lowest coverage score.

### Step 5: Deliver Gate Decision and Launch Checklist

Determine the go/no-go threshold by analyzing the domain's risk profile:
- **Domain risk**: cost of error (irreversible harm → high; recoverable bugs → low)
- **Iteration cost**: time/resources to test and pivot (clinical trials → high; 
  coding prototypes → low)
- **Feedback loop speed**: how quickly the user learns from mistakes 
  (trading backtests → minutes; academic publishing → months)

Higher risk × slower feedback → higher threshold. Lower risk × faster feedback → lower threshold.

Reference points (agent adapts based on specific project context):
- High-stakes + slow feedback (medicine, law, production security): 75–90%
- Medium-stakes + medium feedback (data science, web dev, hardware): 50–65%
- Low-stakes + fast feedback (coding prototypes, trading backtests, hobby projects): 25–40%

Deliver:
1. The rationale for the chosen threshold
2. Which 1–2 dimensions to prioritize for patching (bottleneck + next lowest score)
3. Specific resources (docs, repos, papers) to reach threshold
4. A "launch checklist" with observable signals

### Report Persistence

After delivering the report, save it to:
`docs/blind-spot-scan/blind-spot-scan-<domain-slug>-YYYY-MM-DD.md`

- `<domain-slug>`: domain name in kebab-case (e.g., `quantitative-trading`)
- Do not show the save path to the user unless they ask
- Re-audit depends on these files being readable from the filesystem

## Output Format

Return a markdown report with this exact structure:

```markdown
# Domain Map: [Domain Name]
Date: [YYYY-MM-DD]
Goal: [User's project goal]

## Dimensions
| Dimension | Coverage | Threshold | Status |
|-----------|----------|-----------|--------|
| ...       | ...%     | ...%      | 🔴🟡🟢 |

Status rules: 🟢 if Coverage ≥ Threshold; 🟡 if Coverage ≥ Threshold × 0.7; 🔴 otherwise.

## Critical Blind Spots (Top 3)
1. **[Dimension]**: [Blind spot] → [Action]
2. ...
3. ...

## Launch Decision
- [ ] GO — Start project. Parallel track: patch [Dimension] to [X]%
- [ ] NO-GO — First patch [Dimension] to [X]%. Estimated time: [Y]

## Re-audit Triggers
- When [signal], revisit [dimension]

### Re-audit Diff (appendix)

If this is a re-audit, add a Diff section before Re-audit Triggers. Use this exact 
text-based format (no markdown tables):

```markdown
## Re-audit Diff (vs YYYY-MM-DD)

**[Dimension]:** [last]% → [current]% ([±diff]%) [trend]
...

Coverage legend: <60%=🔴  60–79%=🟡  ≥80%=🟢

**Top improvement:** [Dimension] — [one-line note]
**Regression alert:** [Dimension] — [one-line note]
```

Trend arrows: +10% or more → 📈 | −10% or more → 📉 | otherwise → ➡️
```

## Re-audit Workflow

Copy this checklist and track your progress:

```
Re-audit Progress:
- [ ] Step R1: List files in docs/blind-spot-scan/
- [ ] Step R2: Present the latest matching report and ask user to confirm
- [ ] Step R3: Read the confirmed report; extract dimensions and coverage
- [ ] Step R4: Run the standard 5-step scan with the same dimensions
- [ ] Step R5: Append the Diff section to the new report
- [ ] Step R6: Save the new report with today's date
```

### Step R1: Locate Historical Reports

List files in `docs/blind-spot-scan/`. If the directory does not exist or is empty, 
tell the user this is the first scan and run the standard workflow.

### Step R2: User Confirmation

Present the most recent matching report. Ask exactly:

> 是对 `blind-spot-scan-[domain]-YYYY-MM-DD.md` 这份报告进行 re-audit 吗？

If the user says no, list all available reports and ask which one to use.

### Step R3: Read the Confirmed Report

Extract from the confirmed report:
- Domain name
- Dimension names
- Last coverage scores
- Thresholds
- Status (🔴🟡🟢)

### Step R4: Execute the Scan

Reuse the same dimensions from the previous scan. Rotate T/F questions: keep 
1–2 questions that test retention, replace the rest with new ones that probe 
deeper or test recently learned material.

### Step R5: Generate Diff

After Step 5 of the standard workflow, append the Diff section (see Output Format).

### Step R6: Save

Save the new report using today's date. Old reports are never overwritten.

## Error Handling

- If user cannot answer questions in a dimension: Switch to "exploratory mode" 
  — provide all correct answers immediately and ask the user to self-rate 
  confidence (high / medium / low) on each instead. Trigger exploratory mode 
  when either (a) the user fails or skips 3+ consecutive questions in a dimension, 
  or (b) the user explicitly asks to skip the dimension.
- If domain is too broad: Ask user to narrow to a specific project or 
  deliverable before proceeding.
- If user disputes a "correct" answer: Flag it as "contested / paradigm-dependent" 
  and note the dominant vs. alternative view.
- **If `docs/blind-spot-scan/` is empty**: Inform the user this is the first scan. 
  Run the standard workflow and save the report.
- **If user rejects the matched report**: List all files in `docs/blind-spot-scan/` 
  and ask which one to use.
- **If no matching domain is found**: Ask the user to confirm the domain name or 
  start a fresh scan.

## Examples

### Example Invocation

User: "I want to build a momentum strategy on QQQ constituents but I don't 
know where to start."

Agent response: "I'll run a blind spot scanner for quantitative momentum trading. 
First, the 6 core dimensions..."

### Example Output Snippet

See `{baseDir}/resources/examples/sample-output.md` for a full rendered example.

### End-to-End Demo Walkthrough

See `{baseDir}/demo/quant-factor-research-agent.md` for a complete, annotated walkthrough covering:
- Domain deconstruction across two templates (trading + agent systems)
- 6 dimensions with 30 T/F questions and answer rationales
- Coverage scoring and contested-question handling
- Final launch decision with risk-calibrated threshold

## Evaluation & Iteration

Test this Skill with real scenarios before relying on it for critical decisions.

### Evaluation checklist

- [ ] **Activation test**: Ask "I want to learn X but don't know where to start" — 
  does the Skill activate and suggest the blind spot scanner?
- [ ] **Dimension quality**: Are the 5–8 dimensions comprehensive and non-overlapping?
- [ ] **Question calibration**: Do T/F questions distinguish beginners from practitioners?
- [ ] **Threshold sanity**: Does the risk-calibrated threshold feel reasonable?
- [ ] **Output usefulness**: Does the final report help the user decide what to learn next?
- [ ] **Re-audit activation**: Does the Skill activate when the user says "re-audit"?
- [ ] **Diff accuracy**: Does the Diff correctly identify improvements and regressions?
- [ ] **File confirmation**: Does the agent always show the file path before proceeding?

### Iteration signals

Observe how the agent uses this Skill in practice:
- **User skips dimensions frequently**: Questions may be too hard or too broad
- **User disputes many answers**: Dimensions may be paradigm-dependent; add "contested" flags
- **Threshold feels arbitrary**: Revisit the risk-profile analysis with the user
- **Launch checklist ignored**: Make checklist items more concrete and observable
- **User rejects the matched report**: File naming or matching logic needs tuning
- **Diff shows no change across multiple dimensions**: Questions may be too similar 
  to last time; rotate questions more aggressively

## Guardrails

- T/F answers reflect mainstream consensus, not absolute truth. Flag contested 
  topics explicitly without fabricating consensus percentages.
- Thresholds are advisory. User overrides only after the agent restates the risk 
  and the user responds with an explicit go-ahead (e.g., "确认继续", 
  "是的，继续", "I accept the risk and want to proceed").
- Re-audit is user-initiated. Suggest the user re-run a blind spot scanner when: 
  (a) project scope changes significantly, (b) a milestone is reached and new 
  unknowns surface, or (c) after 2–4 weeks of active work as a routine check-in. 
  Each re-audit should be scoped to the project's current state and open questions, 
  not a full reset.
- Never embed credentials, API keys, or absolute file paths in skill output.
- During the scan phase, do not write executable code, configure production 
  environments, submit real orders, send submission emails, deploy services to 
  public networks, or use live API credentials. The scan phase is limited to 
  concept explanation, resource recommendation, pseudocode, environment prep 
  checklists, and dependency installation guides.
