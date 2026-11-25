---
name: gap-running-destruction
description: >
  Adversarially attacks the current register state through pre-mortem,
  red-team response, constraint inversion, evidence concentration
  analysis, and kill signal audit. Use when a gap pass requires
  adversarial validation of hypotheses and proposals.
license: Complete terms in LICENSE.txt
serves: gap-definer
domain: adversarial-analysis
affects: destruction-log
depends-on: none
produces: destruction-outcomes
---

# Destruction Protocol

Execute adversarial analysis against the hypothesis register. The
purpose is to find what is wrong, not to confirm what is right.
Every mechanism must produce specific, actionable findings -- not
generic warnings.

---

## Process

### Step 1: Extract Attack Surface [S]

From the register, extract:

1. All hypothesis claims (Problem, Segment, Unit Economics, Value Proposition).
2. All load-bearing assumptions (those marked LOAD-BEARING or with BLAST:HIGH).
3. All evidence items with their tiers and provenance.
4. Growth Architecture proposal and its required conditions.
5. Solution Design proposal and its adequacy criteria.
6. GTM Plan proposal and its success/kill criteria.

**Gate:** `surface_extracted: bool` -- at least one hypothesis claim and one assumption extracted. If register is empty, halt: nothing to destroy.
- Pass: Step 2.
- Fail: halt with message "register has no content to run destruction against."

### Step 2: Run Pre-Mortem [K-grounded]

**Grounded in:** extracted claims, assumptions, evidence, market context from register.

Write a 12-month failure scenario:

1. Identify the single most likely failure chain. Trace cause to effect through the register: which assumption fails first, what cascades, what kills the strategy.
2. Name the dominant causal factor. "The strategy failed because..." must be specific (not "we didn't execute well" -- that is a non-answer).
3. Identify what was missed or underweighted in the current register.

**Quality criteria:**
- The failure scenario must reference specific register content (hypothesis claims, assumption IDs, evidence gaps).
- The causal chain must have at least 2 links (trigger -> intermediate effect -> outcome).
- Generic failure modes ("ran out of money", "couldn't find product-market fit") are insufficient. Trace WHY through the register's own assumptions.

**Fabrication boundary:** Reason only over data present in the register and publicly known market dynamics. Do not invent customer reactions or market events.

**Gate:** `pre_mortem_specific: bool` -- failure scenario names specific register content. Causal chain has 2+ links. Not generic.
- Pass: Step 3.
- Fail: rewrite. Identify which register element the failure traces to.

### Step 3: Run Red-Team Response [K-grounded]

**Grounded in:** competitive analysis from register, architecture proposal, positioning statement.

Simulate the incumbent's 90-day response:

1. Identify the top 1-2 incumbents from the register's competitive analysis.
2. For each, determine their most likely response to this strategy's positioning and target segment. Consider: price cuts, feature copies, partnership blocks, distribution leverage, marketing counterpunch.
3. Assess what this response changes in the strategy. Does it invalidate the positioning? Undercut the economics? Block the channel?

**Quality criteria:**
- Response must name a specific incumbent (not "competitors").
- Response must be a concrete action (not "they would compete harder").
- Impact assessment must trace to a specific hypothesis or proposal section.

**Fabrication boundary:** Base incumbent capabilities on competitive analysis already in the register. Do not invent competitor resources or strategies not evidenced.

**Gate:** `red_team_specific: bool` -- at least one named incumbent, one concrete action, one traced impact.
- Pass: Step 4.
- Fail: rewrite. Name the incumbent. Name the action. Trace the impact.

### Step 4: Run Constraint Inversions [R + K-grounded]

**Rule for selection [R]:** Invert every assumption that is:
- LOAD-BEARING, OR
- BLAST:HIGH, OR
- Supporting 2+ hypotheses

**For each selected assumption [K-grounded]:**

1. State the inversion clearly (e.g., "CAC is 3x estimate" not "CAC is higher").
2. Trace the consequence through affected hypotheses and proposals. What breaks? What still holds?
3. Determine survival: YES (strategy holds), NO (strategy breaks), or WITH_MODIFICATION (strategy survives if specific changes are made -- name the changes).

**Quality criteria:**
- Inversions must be specific and quantified where the original assumption was quantified.
- Consequence must name which sections are affected.
- WITH_MODIFICATION must specify the modification.

**Gate:** `inversions_complete: bool` -- every qualifying assumption has been inverted. Each inversion has consequence and survival assessment.
- Pass: Step 5.
- Fail: identify which qualifying assumptions were missed. Invert them.

### Step 5: Run Evidence Concentration Analysis [S]

1. For each evidence source (by provenance), count how many hypothesis claims it supports.
2. If a single source supports claims across 2+ hypotheses, mark it CONCENTRATED.
3. If a single source is the only T1 evidence for any hypothesis, mark it CONCENTRATED regardless of claim count.

Produce a table:

| Source | Claims Supported | Risk Level | Required Mitigation |
|---|---|---|---|
| {source} | {claims} | {OK or CONCENTRATED} | {what additional evidence is needed} |

**Gate:** `concentration_assessed: bool` -- every evidence source evaluated. All CONCENTRATED sources have mitigation noted.
- Pass: Step 6.
- Fail: re-scan evidence items. Ensure provenance is tracked per item.

### Step 6: Run Kill Signal Audit [R + K-grounded]

**Rule [R]:** For each hypothesis, read its Kill Condition.

**Assessment [K-grounded]:**

1. Is there any evidence in the register that suggests the kill condition may be approaching or partially met?
2. Has any contradictory evidence been observed but not acted upon?
3. For each signal: is it being ignored? What is the consequence of ignoring it?

**Quality criteria:**
- Every hypothesis kill condition is checked.
- "No signal observed" is a valid finding but must be stated explicitly.
- If contradictory evidence exists but the hypothesis remains unchanged, flag it as a potential ignored signal.

**Gate:** `kill_audit_complete: bool` -- every hypothesis kill condition checked. Ignored signals flagged with consequence.
- Pass: output.
- Fail: identify which kill conditions were not checked.

---

## Output

Produce:
1. Pre-mortem narrative with specific failure chain.
2. Red-team response with incumbent actions and strategy impact.
3. Constraint inversion table (assumption, inversion, consequence, survival).
4. Evidence concentration risk table (source, claims, risk level, mitigation).
5. Kill signal audit table (signal, observed, ignored, consequence).
6. Summary of contradiction findings (for use by gap-enforcing-decisions).

---

## Edge Cases

| Condition | Handling |
|---|---|
| No competitive analysis in register | Red-team step produces: "No competitive data available. Assume incumbent response is unknown -- this is itself a risk." Flag as gap. |
| No load-bearing assumptions identified | Check if assumptions exist but are not tagged. If genuinely none, constraint inversion step produces: "No load-bearing assumptions identified. Either the strategy has no critical dependencies (unlikely) or assumptions are under-tagged." |
| Kill condition is vague | Flag: "Kill condition for {hypothesis} is not observable or specific. Cannot audit meaningfully." Recommend tightening. |
| Register has only one evidence source for everything | Entire register is CONCENTRATED. Flag at the register level, not per-hypothesis. |
| Destruction finds nothing wrong | Report honestly, but add: "A destruction pass that finds nothing is either evidence of a robust strategy or evidence of an insufficiently aggressive pass. Consider whether the attack surface was fully explored." |

## Boundaries

**In scope:** Pre-mortem, red-team simulation, constraint inversion, evidence concentration analysis, kill signal audit, contradiction detection.

**Out of scope:** Computing gap scores (gap-computing-ledger), enforcing decision rules or changing confidence states (gap-enforcing-decisions), conducting new research (strategist skills), writing to the register (agent handles I/O).
