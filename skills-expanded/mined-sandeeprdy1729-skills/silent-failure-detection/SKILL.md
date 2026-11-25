---
name: silent-failure-detection
description: >
  Silent failure detection skill. Identifies when Claude is being confidently wrong
  — surfacing hidden assumptions, exposing overconfident claims, probing calibration,
  and catching hallucination before it causes damage. Uses specific questioning
  techniques to force the model to reveal its actual uncertainty rather than
  presenting plausible-sounding answers as facts. Turns overconfidence into a
  detectable signal.
  Use when user says: are you sure about this, check your confidence, how do you
  know that, what are you assuming, could you be wrong, probe this, test your answer,
  are you hallucinating, what's your actual confidence, stress test your answer,
  expose your assumptions, calibrate this, fact check yourself, where could you
  be wrong, question your own answer, is this actually true, what if you're wrong,
  what evidence would change your answer.
  Do NOT activate for: creative tasks where factual accuracy is not the concern,
  outputs the user explicitly wants without critique.
  First response: "Silent Failure Detection active. Paste the output or claim
  you want probed. I'll run calibration interrogation and surface what I'm
  less certain about than I appeared."
license: Apache 2.0
---

# Silent Failure Detection

The most dangerous Claude output is the one that sounds exactly right and is wrong.

Claude is a language model. It predicts plausible next tokens. Plausibility is not
accuracy. The output that sounds most confident — specific dates, exact numbers,
named causal mechanisms — is often the output most worth probing. Confidence is a
stylistic property, not an epistemic one.

This skill operationalizes the interrogation techniques that expose the gap between
apparent confidence and actual calibration. It makes overconfidence visible before
it causes damage.

---

## SLASH COMMANDS

| Command | Action |
| --- | --- |
| `/probe <output>` | Run the full interrogation protocol on an output |
| `/assumptions` | List every assumption embedded in a given output |
| `/confidence-audit` | Re-score every claim by actual evidence quality |
| `/falsify <claim>` | Find the condition under which a claim would be false |
| `/source-check` | For every specific claim, ask: where does this come from? |
| `/invert <claim>` | Argue the opposite of the claim — what's the case against it? |
| `/boundary <claim>` | Find the conditions under which the claim stops being true |
| `/specificity-trap` | Probe all specific numbers, dates, names for hallucination risk |
| `/mechanism-check <claim>` | Demand the causal mechanism — not just the conclusion |
| `/training-vs-source` | Distinguish what comes from training data vs. the provided context |
| `/calibrate` | Output every uncertain claim with an explicit confidence percentage |
| `/contrast` | List claims the output could have made but didn't — why not? |

---

## HIGH-LEVEL WORKFLOW

```text
User provides output or claim to interrogate
    │
    ├─ Phase 1: Claim Extraction
    │     Identify every factual claim in the output
    │
    ├─ Phase 2: Confidence Audit
    │     Score each claim by evidence quality, not apparent confidence
    │
    ├─ Phase 3: Assumption Exposure
    │     Surface hidden assumptions behind each high-confidence claim
    │
    ├─ Phase 4: Falsification Pass
    │     For each claim: under what conditions is this false?
    │
    ├─ Phase 5: Specificity Interrogation
    │     Probe specific numbers, dates, names — highest hallucination risk
    │
    └─ Phase 6: Calibrated Revision
          Rewrite with explicit confidence qualifiers where warranted
```

---

## PHASE 1 — CLAIM EXTRACTION

Extract every factual claim from the output. Classify each:

### Claim types

| Type | Description | Hallucination risk |
| --- | --- | --- |
| **Specific fact** | Exact number, date, name, statistic | Very high |
| **Causal claim** | "X causes Y" | High |
| **Categorical claim** | "All X are Y" / "No X is Y" | High |
| **Mechanism claim** | "It works because..." | High |
| **Comparative claim** | "X is better than Y because..." | Medium |
| **General claim** | "X is common in Y contexts" | Medium |
| **Definitional claim** | "X means Y" | Low (but drifts in specialized domains) |
| **Procedural claim** | "To do X, you do Y" | Medium (API versions, deprecated syntax) |

### Claim extraction format

```text
CLAIM INVENTORY

C1: "[exact quote]"  — Type: [claim type] — Risk: [high/medium/low]
C2: "[exact quote]"  — Type: [claim type] — Risk: [high/medium/low]
...

Total claims: [N]
High-risk claims: [N] — [list]
```

---

## PHASE 2 — CONFIDENCE AUDIT

Re-score every claim by evidence quality, not by how confident the output sounds.

### Evidence quality taxonomy

| Level | What it means | Example |
| --- | --- | --- |
| **Grounded** | Claim is directly supported by context the user provided | Document in the prompt states this explicitly |
| **Strong prior** | Claim is well-established consensus in the domain | Water boils at 100°C at sea level |
| **Moderate prior** | Claim is generally accepted but has meaningful exceptions | Startups should find product-market fit before scaling |
| **Weak prior** | Claim is plausible but not well-established | This architecture pattern will scale to 10M users |
| **Training artifact** | Claim sounds specific but may be confabulated | Specific API endpoint, exact version number, named study |
| **Hallucination candidate** | Specific enough to be checkable; likely pulled from pattern-matching | Named author, exact quote, precise statistic, specific date |

### Confidence audit format

```text
CONFIDENCE AUDIT

C1: "[claim]"
  Evidence level:   [Grounded / Strong prior / Moderate / Weak / Training artifact / Hallucination candidate]
  Apparent confidence: [high / medium / low — how confidently was this stated]
  Actual confidence:   [high / medium / low — warranted by evidence]
  Gap:                 [calibrated / overconfident / underconfident]
  Note:               [1 sentence: why the gap exists, if present]

C2: ...

SUMMARY
  Claims at risk of overconfidence: [list C_N, ...]
  Highest-priority to verify: [C_N — why]
```

---

## PHASE 3 — ASSUMPTION EXPOSURE

Every confident claim rests on unstated assumptions. Surfacing them is the
primary defense against silent failure.

### Assumption interrogation questions

For any claim that sounds confident, ask:

1. **Scope assumption:** "Is this true in all contexts, or only in [specific context]?"
2. **Temporal assumption:** "Is this still true? When was this established?"
3. **Source assumption:** "What is the source of this? Is it training data, common knowledge, or the provided context?"
4. **Causal assumption:** "Does X actually cause Y, or do they just correlate? What's the mechanism?"
5. **Counter-evidence assumption:** "What evidence would make this false? Is that evidence available?"
6. **Domain specificity assumption:** "Is this true in the user's specific domain, or only in the domain I trained on?"

### Assumption exposure format

```text
ASSUMPTION AUDIT

Claim: "[C_N]"

Unstated assumptions:
  A1: [assumption] — Confidence this assumption holds: [%]
  A2: [assumption] — Confidence this assumption holds: [%]

If A1 is false, the claim: [fails entirely / changes significantly / still mostly holds]
If A2 is false, the claim: [fails entirely / changes significantly / still mostly holds]

Most fragile assumption: [A_N] — This is fragile because: [reason]
```

---

## PHASE 4 — SPECIFICITY INTERROGATION

Specific claims are the highest-risk. Numbers, names, dates, and quotes are where
language model confabulation concentrates.

### Specificity traps to probe

| Specificity type | Example | Probe |
| --- | --- | --- |
| **Exact statistics** | "73% of users..." | "What study? What year? What population?" |
| **Named studies/papers** | "According to [Author] (Year)..." | "Does this paper exist? What were its actual findings?" |
| **Exact version numbers** | "This works in Python 3.11.2" | "Is this version-specific? What's the behavior in other versions?" |
| **API / function specifics** | "Call `model.fit(X, epochs=10)`" | "Is this the current API? Has this signature changed?" |
| **Named quotes** | "As [Person] said, '...'" | "Did this person actually say this? Exact wording?" |
| **Causal mechanisms** | "This works because the transformer attention..." | "Is this mechanism actually established, or plausibly synthesized?" |
| **Historical facts** | "This was established in 1987 by..." | "Specific enough to verify; may be confabulated detail on a real event" |

### Specificity probe output format

```text
SPECIFICITY PROBE

High-specificity claim: "[C_N]"

Self-interrogation:
  Q: Where does this specific value / name / date come from?
  A: [Training data pattern / Provided context / Unclear origin]

  Q: Could I have confabulated a plausible-sounding specific value?
  A: [Yes — high risk / Possibly / Unlikely]

  Q: If someone fact-checked this, what would they find?
  A: [Likely accurate / Might be off / Should verify before using]

Revised claim with calibration:
  "[Claim rewritten with appropriate qualifier: 'approximately', 'around', 
  'as of [year]', 'verify before using', or 'I'm not certain of the exact figure']"
```

---

## PHASE 5 — FALSIFICATION PASS

Every claim should have a falsification condition. If no evidence could change
the claim, it's not a fact — it's a belief held with too much confidence.

### Falsification format

```text
FALSIFICATION TEST

Claim: "[C_N]"

Falsification condition:
  "This claim would be false if: [specific condition]"

Is this falsification condition verifiable?
  [Yes — can be checked / Requires specific data / Cannot be verified with available information]

Evidence that would change this claim:
  · [Evidence type 1]
  · [Evidence type 2]

If the user has access to [evidence type], they should verify this claim before using it.
```

---

## PHASE 6 — CALIBRATED OUTPUT

Rewrite the original output with explicit confidence qualifiers on all flagged claims.

### Calibration qualifier vocabulary

| Confidence | Qualifier |
| --- | --- |
| Grounded in context (very high) | [no qualifier needed — state directly] |
| Well-established consensus (high) | [state directly; add "generally" for broad claims] |
| Generally true with exceptions (medium-high) | "typically," "in most cases," "often" |
| Plausible but uncertain (medium) | "likely," "tends to," "suggests" |
| Specific claim with confabulation risk (uncertain) | "approximately," "around," "as of [timeframe]" |
| Possible hallucination (low) | "I'm not certain of the exact figure — verify before using" |
| Should not be trusted unchecked (very low) | "This specific detail should be independently verified" |

### Output format

```text
CALIBRATED REVISION

[Original output rewritten with confidence qualifiers on all flagged claims]

─── UNCERTAINTY LOG ────────────────────────────────────────
Claims I'm most uncertain about and why:
1. "[claim]" — reason for uncertainty
2. "[claim]" — reason for uncertainty

Claims most important to verify before acting on:
1. [claim] — consequence of being wrong: [impact]
2. [claim] — consequence of being wrong: [impact]
```

---

## INTERROGATION TECHNIQUES REFERENCE

When probing any output for silent failures, use these forcing questions:

| Technique | Question | What it exposes |
| --- | --- | --- |
| **Inversion** | "What's the strongest case against this claim?" | Overconfident conclusions |
| **Source demand** | "Where exactly does this come from?" | Training artifact vs. grounded claim |
| **Boundary probe** | "When does this stop being true?" | Scope overreach |
| **Mechanism demand** | "What's the causal mechanism?" | Correlation-causation confusion |
| **Specificity trap** | "What's the exact number / date / name?" | Confabulated specifics |
| **Alternative demand** | "What's an equally plausible alternative explanation?" | Premature closure |
| **Pre-mortem** | "If this answer is wrong, what's the most likely way it's wrong?" | Hidden assumptions |
| **Precision reduction** | "Say that with less certainty — what's the honest version?" | Confidence inflation |
| **Context lock** | "Is this based on what I gave you, or what you already knew?" | Prior contamination |
