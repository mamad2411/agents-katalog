---
name: ai-adoption-calibration
description: Calibrate an individual's or team's adoption of AI tools against the automation-bias / algorithmic-aversion spectrum so that delegation matches task verifiability and the user's actual ability to detect AI errors. Integrates automation bias, algorithmic aversion, the cognitive offloading ladder, the ability-cue trap, and the Dunning-Kruger-style confidence gap into a single adoption-decision framework. Use when setting personal or team AI-usage policy, diagnosing why a user over-trusts or under-trusts AI, deciding which tasks to delegate vs. keep, or designing onboarding that builds calibrated adoption rather than blind acceptance or reflexive rejection. NOT for choosing which AI tool to buy (use developer-experience skills) or for trust-calibration UI mechanics (use trust-calibration-ux-pattern).
---

# AI Adoption Calibration

## Overview

Adopting AI tools is not a binary "use it or don't." It is a calibration problem: how much to delegate, to which tasks, with what verification, given the user's actual ability to detect the AI's errors. Two failure modes dominate AI adoption in 2026, and they are mirror images:

- **Automation bias (over-delegation):** the user accepts AI output because it came from the AI, skipping verification. Errors compound. The ability-cue trap (a polished explanation signals competence without delivering understanding) is the mechanism that makes this feel justified to the user.
- **Algorithmic aversion (under-delegation):** the user rejects or micromanages AI output, often after one visible error, even on tasks where the AI is reliably correct. The productivity promise evaporates; the user treats the AI as an unreliable search bar.

Neither extreme is rational. Both are predictable. This skill is the calibration framework that matches delegation depth to task verifiability and the user's error-detection ability — the missing decision layer between "we adopted AI" and "we use it well."

## When to Use

- Setting personal or team AI-usage policy (what to delegate, what to keep, what to verify)
- Diagnosing why a user over-trusts AI (automation bias) or under-trusts it (algorithmic aversion)
- Deciding which tasks to delegate to AI vs. keep human-owned vs. co-pilot
- Designing onboarding that builds calibrated adoption (not blind acceptance or reflexive rejection)
- Coaching an individual from one failure mode to the other (the over-trusting junior, the over-skeptical senior)
- Evaluating whether an AI tool is building the user's skill or eroding it (the cognitive-offloading question)

NOT for:
- Choosing which AI tool to purchase (use developer-experience and DevEx skills)
- Trust-calibration UI mechanics (use `trust-calibration-ux-pattern`)
- The explanation-depth design question (use `ai-explanation-ability-cue-trap`)
- Cognitive-load reduction techniques (use `cognitive-load-reduction-ai-scaffolding`)
- Calm-technology interaction patterns (use `calm-technology-ai-coding`)

## Core Process / Workflow

### Step 1 — Locate the User on the Bias-Aversion Spectrum

| Failure mode | Behavioral signal | Root cause | Outcome |
|-------------|--------------------|-----------|---------|
| **Automation bias** | Accepts AI output without checking; "the AI said so" | Perceived ability cue; fluency heuristic; effort avoidance | Errors compound unnoticed; capability erodes |
| **Calibrated adoption** | Delegates verifiable tasks; keeps unverifiable; verifies at the right boundary | Matches delegation to verifiability + own error-detection ability | AI amplifies without eroding |
| **Algorithmic aversion** | Rejects AI after one error; micromanages; "I'll just do it myself" | Loss aversion (one error weighs more than many successes); control preference; identity threat | Productivity promise wasted |

Diagnostic questions:
1. After the AI produces output, does the user verify? Always, never, or selectively?
2. When the AI was wrong, did the user catch it before or after the error propagated?
3. Does the user delegate more after a success or retreat after a failure? (Loss-aversion signature)
4. Can the user explain the AI's output in their own words? (Comprehension check)
5. Without the AI, could the user still do the task? (Capability-retention check)

### Step 2 — Classify the Task by Verifiability

The single most important variable: can the user detect the AI's error on this task?

| Task verifiability | Definition | Examples | Default delegation |
|--------------------|------------|----------|--------------------|
| **Immediately verifiable** | The user can see the error in seconds (it runs, it looks wrong, it fails a check) | Formatting, syntax the IDE lints, a query that returns obviously wrong rows | Delegate freely; verify by result |
| **Verifiable with effort** | The error is detectable but requires careful review, tests, or domain knowledge | Refactoring that preserves behavior, a refactor across files, a summary of a known document | Delegate; verify with a structured check (test, diff review, checklist) |
| **Verifiable only by outcome (delayed)** | The error only surfaces later, in production or in a downstream decision | Architecture choice, a security-relevant change, a prediction used in a decision | Co-pilot only; human owns the decision; AI advises |
| **Effectively unverifiable** | The user cannot detect the error even with review (knowledge the user doesn't hold) | A legal citation in an unfamiliar jurisdiction, a medical reasoning step outside the user's expertise | Do not delegate; use AI to inform, not to decide; or acquire the expertise first |

**The rule:** delegation depth is bounded by the user's ability to detect errors on that task. Where the user cannot detect the error, delegation is dangerous regardless of how good the AI is — because the user cannot calibrate.

### Step 3 — Match Delegation Depth to the Task-Verifiability × User-Ability Matrix

|  | User can detect errors easily | User can detect errors with effort | User cannot detect errors |
|--|-------------------------------|-----------------------------------|---------------------------|
| **Low-stakes task** | Delegate (verify by result) | Delegate (verify with a quick check) | Co-pilot; do not auto-accept |
| **Medium-stakes task** | Delegate (verify by result) | Delegate (verify with structured check) | Co-pilot; human owns output |
| **High-stakes task** | Delegate (verify by result) | Co-pilot (verify with structured check + second opinion) | Do not delegate; AI informs only |

**The diagonal is the safe zone.** Off-diagonal is where failures happen:
- Over-delegation: delegating an unverifiable, high-stakes task (top-right) — automation bias.
- Under-delegation: refusing to delegate a verifiable, low-stakes task (bottom-left) — algorithmic aversion.

### Step 4 — Counter the Specific Failure Mode

#### If the user is automation-biased (over-delegating)
- **Insert a verification gate** before the AI output propagates (commit gate, publish gate, send gate).
- **Match explanation depth to stakes** (use `ai-explanation-ability-cue-trap`): the over-trusting user needs uncertainty disclosure, not more-convincing rationales.
- **Measure behavioral reliance separately from attitudinal trust** (surveys miss the bias).
- **Move the irreducible verification complexity to the system** (Tesler's Law — use `ai-ux-laws-translation`): static analysis, adversarial test layers, not unaided human eyes.
- **Restore the capability the AI is eroding** (climb the `cognitive-offloading-ladder`): require the user to do the task unaided periodically to retain the skill that lets them detect errors.

#### If the user is algorithm-averse (under-delegating)
- **Surface the AI's track record** on this specific task type (the `trust-calibration-ux-pattern` "show per-domain track records" move). Aversion is often based on one vivid error; the actual hit rate may be high.
- **Start with immediately-verifiable, low-stakes tasks** to rebuild the baseline: let the user see the AI succeed and verify it themselves. Confidence is rebuilt by verified success, not by persuasion.
- **Frame the AI as an extension of the team, not a replacement** (the `agentic-coding-trends-2026` supervisory-engineering framing): the human keeps judgment; the AI handles the toil.
- **Expose the reasoning, not just the output** (the `chain-of-thought-ux-reasoning-transparency` spectrum): aversion drops when the user can trace *why* the AI concluded what it did.

### Step 5 — Design Onboarding for Calibrated Adoption

The default onboarding failure: users either accept everything (automation bias) or, after the first error, reject everything (algorithmic aversion). Calibrated onboarding sequences the user through the verifiability ladder:

| Onboarding phase | Task type | Goal |
|------------------|-----------|------|
| Phase 1 | Immediately-verifiable, low-stakes | User sees the AI succeed AND verifies the result themselves (builds calibrated trust, not blind trust) |
| Phase 2 | Verifiable-with-effort, medium-stakes | User learns the structured-verification habit (test, diff review, checklist) — the skill that scales |
| Phase 3 | Outcome-verifiable, high-stakes | User learns the co-pilot mode (AI advises, human decides) — the mode that prevents over-delegation |
| Phase 4 | Effectively-unverifiable (for this user) | User learns the boundary: "do not delegate what you cannot check" — and either acquires the expertise or escalates to a human who has it |

**The principle:** never let a user's first AI experience be a high-stakes, unverifiable task. That produces either automation bias (if it happens to work) or algorithmic aversion (if it doesn't). Sequence from verifiable to unverifiable.

## A-Tech Application Matrix

### A-Coder (AI Coding IDE)
- **Adoption calibration as a product feature:** A-Coder tracks per-user delegation patterns (what the user accepts, rejects, verifies) and surfaces a calibration indicator — "you're auto-accepting 94% of suggestions on security-sensitive files" — to catch automation bias before it causes harm.
- **Task-verifiability tagging:** A-Coder tags suggestions by verifiability (lintable, testable, review-required, judgment-required) and adjusts the verification gate accordingly.
- **Onboarding sequence:** the first-run experience starts with immediately-verifiable suggestions (formatting the user can see is right) and climbs to judgment-required changes, teaching the verification habit at each rung.
- **Anti-aversion:** A-Coder surfaces the agent's per-task-type track record so a user who got burned once doesn't generalize to "never trust it."

### Be Practical (Playbooks / Curriculum)
- **Curriculum module:** "Calibrated Adoption: Delegate to Verifiability, Not to Hope" — the bias-aversion spectrum, the verifiability ladder, the matrix, the onboarding sequence.
- **Exercise:** the user audits their own last 20 AI interactions — which were over-delegated, which under-delegated, which calibrated — and designs their personal delegation policy.
- **Case study:** a junior developer who auto-accepted a security-relevant change (automation bias on an unverifiable task) and a senior who refused to delegate a trivial formatting task (algorithmic aversion on a verifiable one) — and the calibration fix for each.

### Builder's Club (Community)
- **Community delegation-policy templates:** shared, versioned "what we delegate / what we keep" policies that teams can fork.
- **Calibration audit:** a community protocol where members review each other's AI-usage patterns for bias or aversion signatures.
- **The "do not delegate what you cannot check" rule** as a community principle — paired with "and here's how to gain the ability to check it" (the boosting approach from `boosting-empowering-behavior-change`).

## Cross-References

- `cognitive-science-and-ux/ai-explanation-ability-cue-trap` — the mechanism behind automation bias (the ability cue manufactures unearned trust)
- `cognitive-science-and-ux/trust-calibration-ux-pattern` — the UI-level trust-escalation mechanics this skill relies on
- `cognitive-science-and-ux/cognitive-offloading-ladder` — the capability-retention framework (climb the ladder to avoid skill erosion from over-delegation)
- `cognitive-science-and-ux/chain-of-thought-ux-reasoning-transparency` — reasoning visibility reduces algorithmic aversion
- `community-and-growth/algorithmic-aversion-defense` — the community/growth-side treatment of aversion
- `developer-experience-and-flow/devex-verification-bottleneck-framework` — the verification complexity this skill relocates to the system
- `behavioral-psychology-and-nudging/boosting-empowering-behavior-change` — building the competence that lets the user detect errors (the "acquire the expertise" path)
- `cognitive-science-and-ux/ai-ux-laws-translation` — Tesler's Law (verification is irreducible; move it to the system) and Doherty/Parkinson (budgets and perceived speed)

## Anti-Patterns

| Anti-Pattern | Failure Mode | Why It Fails |
|--------------|--------------|-------------|
| "Adopt AI everywhere" policy | Automation bias | Delegates unverifiable, high-stakes tasks the user cannot calibrate |
| "Never trust AI" policy | Algorithmic aversion | Wastes the AI on verifiable tasks where it is reliably correct |
| First-run onboarding on a high-stakes task | Either extreme | One vivid success → blind trust; one vivid error → permanent aversion |
| Trust surveys without behavior tracking | Misses the bias | Attitudinal and behavioral trust decouple (the ability-cue-trap finding) |
| Persuading the averse user with more rationale | Compounds aversion | The user doesn't lack information; they lack verified-success experience |
| Removing verification to "reduce friction" | Automation bias | The verification gate is the calibration mechanism; removing it removes calibration |

## References

- See [references/adoption-calibration-evidence-base.md](references/adoption-calibration-evidence-base.md) for the automation-bias and algorithmic-aversion literature, the verifiability taxonomy, the loss-aversion asymmetry, the Dunning-Kruger-style confidence gap, and the links to each cross-referenced skill's evidence.