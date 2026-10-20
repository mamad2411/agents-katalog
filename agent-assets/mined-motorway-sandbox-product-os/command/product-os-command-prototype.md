<!-- owner: shared | audience: all-pms | last-updated: 2026-04 -->
<!-- purpose: Solution prototyping: generate structurally different concepts from a hypothesis, run psych audit and persona fit, get early panel signal, produce comparison and recommendation -->

# Prototype

Generate and validate solution concepts for a prioritised opportunity or hypothesis.

**Input:** $ARGUMENTS

This command covers PM playbook **Stage 2: Solution Prototyping & Validation**. It takes the output of discovery (a hypothesis or opportunity) and produces tested solution concepts ready for experiment design.

**Important: Run the full prototype process in one pass. Pause only at the final step for user feedback.**

## Step 0: Load context

1. **Parse the input.** The user should provide one of:
   - A hypothesis in IF/THEN/BECAUSE format
   - A path to an investigation output or opportunity summary
   - A description of the opportunity to prototype against

2. **Read supporting context:**
   - `data/funnel-context.md` — metric definitions, funnel baselines
   - `context/current-priorities.md` — strategic alignment
   - `context/personas/customer-personas.md` and `context/personas/partner-personas.md` — priority personas
   - `context/brand/messaging/` — brand voice and terminology constraints

3. **Check for prior work:**
   - Search `projects/` for existing experiment docs on this topic
   - Search `insights/` for relevant UXR studies, CX analysis, and review data
   - Read agent memory files if available: `team/{initials}/agents/memory/product-manager.md`, `team/{initials}/agents/memory/uxr.md`

4. **Extract the core problem.** Before generating solutions, clearly state:
   - **The user problem:** What pain point are we solving? For which personas?
   - **The business problem:** What metric are we trying to move? By how much?
   - **The mechanism:** Why does this problem exist? What's the root cause?
   - **The constraint:** What must we NOT break? (guardrail metrics)

If the input doesn't contain enough information to define these, state what's missing and ask.

## Step 1: Generate solution concepts

Produce **3 structurally different solution concepts**. These must be genuinely different approaches — different psych levers, different UX patterns, different points in the journey — not just copy variants of the same layout.

For each concept:

### Concept structure

```markdown
### Concept [N]: [Name]

**Approach:** [One-line description of what this does differently]

**Psych lever:** [Which psychological mechanism does this use? Reference Reforge psych framework — e.g. positive psych/value demonstration, negative psych/loss aversion, social proof, credibility, effort reduction, commitment/consistency]

**How it works:**
1. [Step-by-step user experience description]
2. [What the user sees, feels, and does at each point]
3. [What happens after they take the desired action — the reward state]

**Persona fit:**
- [Priority persona 1]: [How they'd experience this — positive/neutral/negative and why]
- [Priority persona 2]: [How they'd experience this — positive/neutral/negative and why]
- [At-risk persona]: [Who might react badly and why]

**Hypothesis-design alignment:**
- Does this directly test the hypothesis? [Yes/No + explanation]
- If the user never reads the body copy, would they understand the value from the design alone? [Yes/No]
- Is the size of this change proportionate to the expected uplift? [Yes/No]

**Assumptions:**
1. [Key assumption that must be true for this to work]
2. [Second assumption]

**Estimated build complexity:** [Low / Medium / High — relative to each other]
```

### Concept generation principles

Follow the design principles from `pm-playbook/process/4-design.md`:

- **Design experiences, not screens.** If a concept is "add a card with copy and a CTA", push harder — what experience communicates the value without needing the user to read?
- **Show, don't tell.** Visual comparison, progress indicators, before/after states, and visible rewards are stronger than body copy
- **Match change to expected uplift.** If the hypothesis expects a 20% improvement, a small text change won't get there
- **Include the 10x version.** For concept 3, push to the most ambitious version — what would we build if there were no constraints? This calibrates ambition

## Step 2: Psych audit

For each concept, run a structured psych audit:

| Dimension | Concept 1 | Concept 2 | Concept 3 |
|-----------|-----------|-----------|-----------|
| **Primary psych lever** | [Which lever] | [Which lever] | [Which lever] |
| **Positive psych** (value shown, not told?) | [Score 1-5 + note] | | |
| **Negative psych** (loss/urgency appropriate?) | [Score 1-5 + note] | | |
| **Effort** (friction reduced or introduced?) | [Score 1-5 + note] | | |
| **Social proof** (credibility signals present?) | [Score 1-5 + note] | | |
| **Reward state** (what does the user get after acting?) | [Description] | | |
| **Hypothesis alignment** | [Strong/Moderate/Weak] | | |

## Step 3: Run persona panels (early signal)

Decide which panels to run based on who is affected:
- **Customer-side opportunity** → customer panel (`.claude/agents/customer-panel.md`)
- **Partner/B2B-side opportunity → stakeholder panel (`.claude/agents/stakeholder-panel.md`)
- **Marketplace/both sides** → both panels

Feed each panel all 3 concepts and the hypothesis. Request:
- Which concept resonates most and why
- Which concept would change their behaviour
- Any concerns or objections per concept
- Which persona has the strongest/weakest reaction

Present panel results per concept:

```markdown
## Panel verdict

### Customer panel
- **Preferred concept:** [N] — [why]
- **Strongest persona reaction:** [Persona] on Concept [N] — [quote/reason]
- **Biggest concern:** [What and from which persona]
- **Behaviour change likelihood:** Concept [N] > Concept [N] > Concept [N]

### Partner panel (if applicable)
[Same structure]
```

## Step 4: Assumption mapping

For each concept, map the riskiest assumptions and how they could be tested:

| Assumption | Concept(s) | Risk level | How to test | Test cost |
|-----------|-----------|-----------|------------|----------|
| [Assumption 1] | 1, 2 | High | [User test / data check / prototype test] | [Low / Med / High] |
| [Assumption 2] | 3 | Medium | [Method] | [Cost] |

Flag any assumptions that are shared across all concepts — these are the ones most worth testing early.

## Step 5: Comparison and recommendation

### Comparison table

| Dimension | Concept 1 | Concept 2 | Concept 3 |
|-----------|-----------|-----------|-----------|
| **Psych lever** | | | |
| **Hypothesis alignment** | Strong/Moderate/Weak | | |
| **Panel preference** | [Rank] | [Rank] | [Rank] |
| **Priority persona fit** | [Good/Mixed/Poor] | | |
| **Build complexity** | Low/Med/High | | |
| **Assumption risk** | Low/Med/High | | |
| **Proportionate to expected uplift?** | Yes/No | | |

### Recommendation

```markdown
## Recommendation

**Lead concept:** Concept [N] — [Name]

**Why:** [2-3 sentences grounded in panel signal, persona fit, hypothesis alignment, and build pragmatism]

**Key risk:** [The biggest assumption to validate before committing]

**What to test first:** [The cheapest way to validate the key risk — e.g. unmoderated user test, prototype test, data analysis]

**What to take from other concepts:** [Any elements from rejected concepts worth incorporating]
```

## Step 6: Output and next steps

### Save the prototype doc

Save to `projects/{slug}/prototypes.md` with the full comparison, panel verdicts, and recommendation. Use the same initiative folder as the discovery doc if one exists — check `projects/` for an existing folder matching the topic. Create the folder if it doesn't exist.

### Update canonical doc

Update `projects/{slug}/canonical.md` per the convention in `pm-playbook/conventions/canonical-documents.md`:
- Set **Current stage** to "Prototype"
- Update the **Stage artifacts** table: set Prototype row to `[prototypes.md](prototypes.md) | Complete`
- Update **Current status** with the recommendation summary
- Add a **Key decisions** entry: "{date}: Prototype complete — Concept {N} ({name}) recommended. Panel preferred {concept}. Key risk: {assumption}"

If no canonical doc exists, create one using the initiative canonical template from the convention doc.

### Present to user

Display a summary:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PROTOTYPE — {opportunity name}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

┌─ CONCEPTS ────────────────────────────────
│ 1. {Name} — {psych lever} — Build: {complexity}
│ 2. {Name} — {psych lever} — Build: {complexity}
│ 3. {Name} — {psych lever} — Build: {complexity}
└───────────────────────────────────────────

┌─ PANEL VERDICT ───────────────────────────
│ Preferred: Concept {N} ({panel source})
│ Strongest signal: {persona} on Concept {N}
│ Key concern: {one-line}
└───────────────────────────────────────────

┌─ RECOMMENDATION ──────────────────────────
│ Lead with Concept {N}: {Name}
│ Key risk: {assumption to validate}
│ Test first: {method}
└───────────────────────────────────────────
```

Then ask:

> "Three concepts above. Concept {N} is the recommendation based on panel signal and hypothesis fit. Want to adjust, combine elements, or proceed to experiment design with `/experiment-setup`?"

### Offer next steps

- "Want me to run `/experiment-setup` with the recommended concept?" (→ Stage 3)
- "Want me to create the experiment doc with `/create-new-project`?" (→ Stage 3)
- "Want me to run the stakeholder agents ({CEO}, {VP Sales}, {VP Ops}) for early feedback?" (→ if stakeholder buy-in is needed before committing)
- "Want me to adjust a concept and re-run the panels?"

## Principles

- **Solutions must address the stated problem.** If a concept doesn't directly test the hypothesis, it doesn't belong
- **Structural variety over cosmetic variety.** Three versions of the same card with different copy is not prototyping
- **Design experiences, not screens.** Every concept should describe what the user sees, feels, and does — not just what appears on screen
- **Persona fit is non-negotiable.** Every concept must be evaluated against priority personas
- **Assumptions are explicit.** Every concept carries assumptions — surface them, don't hide them
- **Panel signal is directional, not conclusive.** Simulated persona reactions inform direction but don't replace real user testing
- **UK English** throughout
