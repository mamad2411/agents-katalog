---
name: adversarial-review
description: "Stress-tests a Leeward artifact using five attack vectors: evidence integrity, decision courage, scope discipline, specificity, and structural honesty. Produces a Challenge Report with verdict, findings, and resolution conditions."
category: technical
default_depth: standard
---

# Adversarial Review

Read `docs/workflow-contract.md` once per session before applying this skill. Resolve it from the nearest ancestor of this file containing `manifest.json`; all Shipwright paths are relative to that root.

## Description

Stress-tests a completed Shipwright artifact from an explicitly adversarial posture. The job is not to rewrite the artifact or prove superiority. The job is to find the places where the artifact may be wrong, weakly supported, too comfortable, too generic, or structurally misleading.

This skill produces a **Challenge Report**. A good Challenge Report creates useful friction: it names the exact claim being challenged, explains why the claim is vulnerable, and states what would resolve the challenge.

## When to Use

- After a PRD, strategy doc, design review, or technical handoff passes structural checks
- Before sharing a high-stakes artifact with leadership, engineering, or cross-functional stakeholders
- When the PM wants a separate pass focused on weaknesses rather than polish
- When an artifact feels persuasive but suspiciously comfortable
- When an existing artifact needs pressure-testing without rerunning the full workflow

## Depth

| Scope | Use When | Sections to Include |
|---|---|---|
| **Light** | Time-sensitive review where you only want the highest-signal objections | Context + condensed Analysis (up to 3 material findings) + Decision Frame + condensed Risks and Open Questions + Action Plan + Unknowns & Evidence Gaps + Pass/Fail Readiness + Recommended Next Artifact |
| **Standard** | Typical adversarial review of a completed artifact | All sections with a full 5-vector sweep |
| **Deep** | High-stakes artifact where the PM wants maximum rigor before delivery | All sections + falsification criteria for each major challenged claim + "what evidence would change my mind" notes |

**Omit rules:** At Light depth, do not attempt full coverage. Surface only the strongest findings, up to 3, across all vectors, but still include the required closing signature elements. At Deep depth, do not rewrite the artifact or produce a replacement strategy; remain in review mode.

## Framework

### Pre-Check: Run the Deterministic Validator

Before reviewing manually, find the nearest ancestor containing `manifest.json`. If the artifact
is available as a file, run the postflight validator by its absolute installed path:

```bash
node "<absolute-shipwright-root>/scripts/validate-artifact.mjs" path/to/artifact.md
```

The validator flags unsupported dollar figures and numeric claims without nearby citation markers, and checks for missing expected sections. Treat flags as review candidates. Verify each flag against the actual claim before including it; map it to the appropriate attack vector. If the validator finds no issues, note that and proceed. This step is optional but saves review time on high-volume citation work.

The review itself can assess a valid draft that is not ready for engineering. When this report is
used for an engineering handoff, pass the report's file path to the handoff validator's
`--related` option and let that boundary use `--require-ready`; do not treat an unready
draft as malformed or force it to PASS.

### Step 1: Define the Review Scope

Start by naming what is under review and what standard it should be held to.

```markdown
## Context

- **Artifact under review:** [PRD / Strategy / Design Review / Tech Handoff / Other]
- **Authoring context:** [workflow, agent, or PM-supplied context]
- **Depth:** [Light / Standard / Deep]
- **Intended audience:** [engineering / leadership / product team / cross-functional]
- **Review goal:** [what the PM most wants pressure-tested]
```

If the PM names a specific concern, bias the review toward that concern without skipping the rest of the chosen depth.

### Step 2: Run the Five Attack Vectors

Evaluate the artifact through these vectors:

#### 1. Evidence Integrity

Probe:

- unsourced claims presented as truth
- invented customer evidence
- assumptions blended with facts
- selective use of weak evidence to support strong claims

Questions:

- Which claims cannot be traced to evidence in the artifact or provided inputs?
- Where does the artifact overstate certainty relative to the evidence quality?
- Which claims should be hypotheses instead of findings?

#### 2. Decision Courage

Probe:

- hedging that avoids commitment
- recommendations that cannot be falsified
- options presented without a real decision
- risk language that softens the actual downside

Questions:

- What is the actual decision, and is the artifact willing to make it?
- Under what conditions would this recommendation be judged wrong?
- Where is the artifact optimizing for sounding balanced instead of being useful?

#### 3. Scope Discipline

Probe:

- helpful scope creep
- framework bloat
- extra work smuggled in as obvious
- analysis weight that exceeds the decision size

Questions:

- What appears in the artifact that is not traceable to the stated scope?
- Where does the artifact add surface area instead of clarifying the decision?
- Is the framework serving the problem, or is the problem being stretched to fit the framework?

#### 4. Specificity

Probe:

- generic wording
- symmetrical analysis that feels templated
- interchangeable recommendations
- placeholders disguised as finished thinking

Questions:

- Would this artifact still read the same if the product were different?
- Where are the conclusions suspiciously balanced or boilerplate?
- Which sections sound polished but say little?

#### 5. Structural Honesty

Probe:

- buried critical information
- positivity smoothing
- blockers reframed as "considerations"
- comfortable conclusions that ignore tension

Questions:

- What bad news is being softened or hidden?
- If this artifact were wrong, where would the damage come from?
- Does the structure help the reader see the real risk, or does it hide it?

### Step 3: Convert Objections Into Findings

Each finding must be specific enough that the author could respond to it directly.

Use this structure:

```markdown
| Finding ID | Claim Challenged | Attack Vector | Severity | Why This Is Vulnerable | Question To Answer | What Would Resolve It |
|---|---|---|---|---|---|---|
| [stable report-specific ID] | [specific claim] | [vector] | [Critical / Moderate / Minor] | [evidence-backed critique] | [one precise question] | [specific evidence or revision needed] |
```

Severity rules:

- **Critical:** The artifact's core recommendation may be wrong, not just undersupported
- **Moderate:** The recommendation may still be right, but important support, boundaries, or tension are missing
- **Minor:** The issue weakens clarity or confidence but is unlikely to reverse the core decision

### Step 4: Set the Verdict

Use these verdicts:

- **CLEAR:** No material issues found. Minor issues may exist, but none should block normal use.
- **DEFEND:** The PM should decide whether to send findings back to the producing agent before treating the artifact as settled.
- **ESCALATE:** A Critical integrity issue puts the artifact's core recommendation in doubt and PM attention is required.

`DEFEND` requests a disposition of material findings. It is not an automatic workflow state and does not automatically reopen the authoring agent.

### Step 5: Close With Resolution Guidance

The review should end by making next actions obvious.

- If verdict is `CLEAR`, say why the artifact cleared and what residual risks remain
- If verdict is `DEFEND`, say which findings are worth routing back and why
- If verdict is `ESCALATE`, state the exact decision or assumption that needs PM attention

For Deep reviews, add:

- falsification criteria for each major challenged claim
- "what evidence would change my mind" for each Critical finding

## Minimum Evidence Bar

**Required inputs:** The artifact under review. If the artifact depends on evidence outside itself, include that source evidence when available.

**Acceptable evidence:** The artifact text, linked or pasted source materials, cited metrics, PM-supplied context, and upstream Shipwright artifacts.

**Insufficient evidence behavior:** If the artifact lacks enough context to be reviewed responsibly, produce a partial Challenge Report that says `Insufficient evidence to assess` and list the exact missing inputs needed. Do not fill the gaps with invented counter-evidence.

**Hypotheses vs. findings:**

- **Finding:** A critique grounded in the artifact's own claims, omissions, or structure
- **Hypothesis:** A possible weakness that cannot yet be confirmed because the necessary evidence is missing

When in doubt, downgrade to hypothesis instead of overstating the critique.

## Output Format

When an automated handoff or benchmark explicitly requests structured output, also read `docs/structured-artifacts.md` and the matching schema from the Shipwright installation root. Append the validated envelope and keep it consistent with the visible artifact. Ordinary chat output needs no JSON duplicate.

Produce a **Challenge Report** containing:

1. `## Context`
   - artifact under review
   - depth
   - audience
   - review goal
2. `## Analysis`
   - verdict
   - findings table
   - optional "No material issues found" note if verdict is `CLEAR`
3. `## Decision Frame`
   - recommendation about whether the artifact should proceed, defend, or escalate
   - trade-off of acting now vs. revising
   - confidence and rationale
   - owner
   - decision date
   - revisit trigger
4. `## Risks and Open Questions`
   - unresolved vulnerabilities in the artifact under review
   - open questions the author or PM still needs to answer
   - risks created if the artifact is used without revision
5. `## Action Plan`
   - concrete next steps
   - which findings to route back, if any

In v1, the Challenge Report is conversation-native unless the PM explicitly asks to save it to disk.

Then close with the remaining Shipwright Signature elements:

6. **Unknowns & Evidence Gaps**, Missing context, missing source evidence, or reviewer limitations that reduced confidence in the review itself
7. **Pass/Fail Readiness**, PASS if findings are evidence-backed, severity is calibrated, and each finding includes a resolution condition; FAIL if critique is generic, theatrical, or unsupported
8. **Recommended Next Artifact**, Which Shipwright skill or agent should engage next and why

For machine handoffs, serialize `minor` for Minor severity and record all author responses by finding ID. Use `INSUFFICIENT_EVIDENCE` with FAIL for an incomplete review. A Critical finding requires ESCALATE.

## Common Mistakes to Avoid

- Treating preference disagreement as a flaw
- Flagging every omission as scope failure
- Demanding evidence that the producing artifact was never meant to include
- Mistaking "different conclusion than I would choose" for invalid reasoning
- Rewriting the artifact instead of reviewing it
- Producing many weak nitpicks instead of a few high-signal findings
- Forgetting that the reviewer shares the producing model's blind spots

## Weak vs. Strong Output

**Weak**

> This feels generic and maybe too vague. I would add more evidence and make the recommendation stronger.

Why weak: no specific claim challenged, no severity, no resolution condition.

**Strong**

> The recommendation says enterprise expansion is the priority, but the artifact cites only broad market demand and no enterprise-specific customer evidence. Attack vector: Evidence Integrity. Severity: Moderate. Resolve by citing enterprise-specific signals or downgrading the enterprise thesis to a hypothesis.

Why strong: the finding names the vulnerable claim, explains why it is weak, calibrates severity, and says what would resolve it.
