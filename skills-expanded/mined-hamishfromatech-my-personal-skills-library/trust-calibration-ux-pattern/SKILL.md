---
name: trust-calibration-ux-pattern
description: Design AI interfaces that progressively build appropriate trust through demonstrated competence rather than vanity trust scores. Covers the trust calibration pattern (start supervised, show per-domain track records, tie trust to performance not usage, proactive trust repair, treat under-trust as failure too), the overtrust/undertrust problem, the vanity trust score anti-pattern, and the 5-move implementation framework. Use when designing AI product UX, building agent autonomy escalation, creating trust dashboards, or preventing the two trust failure modes (passive reliance vs. micromanagement).
---

# Trust Calibration UX Pattern

## The Problem: Two Trust Failures

Users interacting with AI agents face a binary failure mode:

1. **Over-trust** — Users stop checking AI outputs. Errors compound unnoticed. The agent is given destructive permissions it hasn't earned. The user becomes passive, and when the AI is wrong, the damage is already done.

2. **Under-trust** — Users micromanage every action. The agent's autonomy is useless because the user verifies everything. The productivity promise of AI delegation evaporates. The user abandons the agent or uses it as a glorified search bar.

**Trust calibration** is the design challenge of aligning a user's perception of the agent's reliability with its actual performance over time. Unlike one-time confidence scores, this is a relationship that evolves — the agent earns more or less trust based on its track record with that specific user.

**The asymmetry:** Trust builds slowly and breaks quickly. The design must account for this.

## When to Use

- Designing AI product UX where users delegate actions to agents
- Building agent autonomy escalation (supervised → autonomous progression)
- Creating trust dashboards or trust indicators
- Preventing over-reliance (passive acceptance of faulty outputs)
- Preventing under-reliance (micromanagement that defeats delegation)
- Designing error recovery and trust repair flows
- Positioning privacy-first architecture as a trust signal

NOT for:
- One-shot or stateless interactions (a per-output confidence score is the right tool, not a track record)
- Interactions where reliability is uniformly high or stakes are trivial (elaborate trust UI is just friction)
- The 4-pillar trust framework (use trust-design)
- Cross-country trust dimensions (use user-trust-ai-major-tech-2026)
- Algorithmic aversion defense (use algorithmic-aversion-defense)

## The Vanity Trust Score Anti-Pattern

The most dangerous implementation is a "trust level" that climbs with usage or time rather than with measured accuracy.

| Vanity Trust Score | Calibrated Trust |
|---|---|
| Rises with time spent | Rises with measured accuracy |
| Rises with clicks/usage | Rises with verified outcomes |
| Encourages over-trust | Matches actual competence |
| Collapses on first visible mistake | Earned through demonstrated performance |
| Manufactures trust not earned | Trust tracks competence, not engagement |

**The trap:** A vanity trust score is the same calibration lie as a fabricated confidence number. It quietly trains users to over-trust, and collapses the first time a "highly trusted" agent makes a visible mistake.

## The Five Implementation Moves

### 1. Start Supervised, Earn Autonomy

Default a new agent to high visibility and human-in-the-loop. Then widen its latitude only when its track record warrants it.

**Granting autonomy on day one is borrowing trust the agent hasn't earned, and the bill comes due on the first unattended mistake.**

Implementation:
- New agent → high visibility mode (all actions shown, all decisions require approval)
- Track record accumulated → gradually reduce approval requirements for verified-reliable domains
- Mistake in domain X → escalation back to supervised mode for that domain only
- Consistent track record across domains → autonomy upgrade offered, not imposed

### 2. Show the Track Record, Per Domain

"Trustworthy" is not global. An agent excellent at scheduling may be unreliable at spending. Show competence per domain.

Implementation:
- Per-domain accuracy display (not aggregate score)
- Track record visible to user at decision points
- Domain taxonomy matches actual task categories (e.g., code generation, refactoring, dependency management, deployment)
- Track record includes outcome verification, not just usage count

| Domain | Actions | Verified Correct | Accuracy | Last Error |
|---|---|---|---|---|
| Code generation | 127 | 118 | 92.9% | 3 days ago |
| Refactoring | 43 | 41 | 95.3% | 12 days ago |
| Dependency updates | 8 | 6 | 75.0% | 1 day ago |
| Deployment | 3 | 3 | 100% | Never |

### 3. Tie the Trust Signal to Performance, Not Usage

A trust level that rises with time-spent or clicks is a vanity metric. It must move with measured accuracy and outcomes.

Implementation:
- Trust indicator = f(verified_accuracy, outcome_quality, error_recovery)
- Trust decreases after errors (not just increases with usage)
- Trust recovers after demonstrated error correction, not automatically with time
- No "loyalty" mechanics — trust is not a rewards program

### 4. Repair Trust Proactively After Mistakes

Trust builds slowly and breaks fast. After an error, surface what happened, what changed, and dial oversight back up yourself.

Implementation:
- Error notification: "I made a mistake on [task]. Here's what happened: [explanation]. Here's what I changed: [correction]. I've increased oversight on this type of action."
- Don't wait for the user to lose faith in silence and walk away — you rarely get told why they left
- Automatic escalation: error in domain X → that domain returns to supervised mode
- Recovery requires demonstrated competence, not just time passage

### 5. Treat Under-Trust as a Failure Too

If a user is double-checking every action the agent reliably gets right, calibration has failed on the other side: the agent is being micromanaged into uselessness.

Implementation:
- Track user verification rate per domain
- If verification rate is high but agent accuracy is high → surface the track record to earn back appropriate delegation
- "You've verified 47 actions in this domain. I've been correct on 46 of them (97.8%). Would you like to reduce verification for this task type?"
- Don't only warn about over-trust — also surface under-trust when the track record supports more delegation

## Real-World Examples

### Navigation Apps (Google Maps)
Started with turn-by-turn with constant visual confirmation. Over time, trust earned through accurate arrival estimates, correct rerouting, and reliable ETA. Users now follow routing decisions largely on trust — but can still see the route, override, and switch to manual at any time. The per-domain track record (highway routing vs. local streets vs. traffic prediction) is implicitly visible.

### Code Review Bots
Started showing every suggestion for manual review. Track record built through accepted/rejected suggestions. Now auto-fixes lint issues with high confidence, flags architectural concerns for human review. Per-domain separation: formatting (high trust) vs. security patterns (supervised) vs. business logic (human required).

### Email Triage Agents
Start with suggestions only ("Consider archiving these 12 newsletters"). Track record builds through user accept/reject patterns. Eventually earn auto-archive for newsletters, auto-label for known senders. But destructive actions (delete, send, pay) remain gated — see the OpenClaw inbox deletion incident.

## Anti-Patterns

| Anti-Pattern | Why It Fails |
|---|---|
| Day-one full autonomy | Borrows trust not earned; first mistake is unattended |
| Aggregate trust score | Hides domain-specific unreliability |
| Usage-based trust escalation | Rewards engagement, not competence |
| Silent error recovery | User discovers the error themselves; trust breaks irreparably |
| No under-trust detection | Agent is micromanaged into uselessness |
| Irreversible autonomy grants | No mechanism to dial back after errors |

## A-Tech Application Matrix

### A-Coder
- **Supervised default:** New A-Coder users start with all agent actions shown inline, requiring acceptance/rejection
- **Per-domain track record dashboard:** Code generation accuracy, refactoring safety, dependency management reliability, deployment success rate — shown per domain
- **Autonomy progression:** After verified track record in a domain (e.g., 95%+ accuracy over 20+ actions), offer reduced friction for that domain only
- **Error repair:** "I suggested a refactor that introduced a type error. Here's what went wrong. I've reverted the change and flagged this pattern for review. Refactoring suggestions will require explicit approval for the next 5 operations."
- **Under-trust signal:** "You've accepted 94 of my last 96 import-optimization suggestions. Would you like to auto-apply these?"
- **Privacy-first trust signal:** On-device processing is a trust signal — your code never leaves your machine, which is itself a track record of data protection

### Be Practical
- **Curriculum module:** "Trust Calibration: How to Build AI You Can Actually Trust" — the five-move framework as practical design checklist
- **Case study:** The OpenClaw inbox deletion incident as the canonical anti-pattern of granting destructive autonomy before earning trust
- **Exercise:** Design a trust calibration UX for a hypothetical AI assistant (per-domain track record, supervised-to-autonomous progression, error repair flow)

### Builder's Club
- **Community trust standard:** Agent marketplace listings include per-domain track records
- **Open-source trust calibration component:** Reusable per-domain track record widget, autonomy escalation controller, error repair flow template
- **Trust audit:** Community members can audit an agent's trust calibration implementation against the five-move framework

## Cross-Skill References

- `trust-design` — The 4-pillar trust model (Ability, Benevolence, Integrity, Predictability)
- `user-trust-ai-major-tech-2026` — Cross-country trust dimensions and design intervention patterns
- `cognitive-surrender-defense` — Preventing over-delegation and the erosion of independent thinking
- `algorithmic-aversion-defense` — Overcoming under-trust of algorithmic systems
- `chain-of-thought-ux-reasoning-transparency` — Reasoning transparency as trust mechanism
- `agentic-supply-chain-exploit-defense` — The OpenClaw inbox deletion incident (anti-pattern for trust calibration)
- `self-determination-theory-developer-motivation` — Autonomy as intrinsic motivation
- `proactive-agent-design-taxonomy` — Proactivity levels and evaluation metrics
- `supervisory-engineering-work` — The creation-to-verification shift and trust in AI outputs

## Measurement Framework

| Metric | Target | Method |
|---|---|---|
| Trust calibration gap | |calibrated_trust - actual_reliability| < 10% | User perception survey vs. measured accuracy |
| Per-domain track record visibility | 100% of decision points | UI audit at each agent action |
| Trust recovery rate after error | > 60% of users resume delegation | Post-error behavior tracking |
| Under-trust detection rate | Flagged within 10 over-verifications | User verification rate monitoring |
| Vanity score absence | 0 vanity-based trust indicators | Code audit of trust UI components |
| Destructive action gating | 100% of destructive ops require approval | Audit log analysis |