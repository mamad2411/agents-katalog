---
name: red-team-review
description: Use this skill when the user asks for an adversarial review of a proposal, architecture, system design, agent workflow, or rollout plan. Trigger phrases include "red team this", "adversarial review", "where does this break", "pre-mortem this design", "red team review", "revisión adversarial", "qué puede salir mal", "break my plan". Produces a structured list of failure modes ranked by severity and likelihood, each with a proposed mitigation, not just a list of worries.
---

# red-team-review

> **Anchor:** A red team's job is to find the failure, not to be agreeable.

## When to use

Use this skill when the user needs an adversarial read of something they are about to commit to. Works for:

- A product proposal or PRD before scoping.
- An architecture or design before build.
- An agent or LLM workflow before rollout.
- A migration or cutover plan before execution.
- A go-to-market plan before launch.
- A security or compliance posture before an external review.

Do not use when:

- The user wants a code review of a specific diff. That is a different task.
- The user wants a post-mortem of something that already failed. Use `post-mortem`.
- The user wants a user-research critique. Use `ux-audit`.

## Voice rules (apply to all outputs)

- No buzzwords: leverage, empower, synergy, resonate, tapestry, delve, elevate, captivate, explore, dynamic, testament.
- No em dashes.
- No filler openings.
- Decision-oriented over descriptive.
- High-context, no overexplaining.
- Standard sentence case for formal outputs.
- ES outputs match the register of the handbook: direct, self-aware, no reverence for process, comfortable naming failure.
- EN outputs use direct US business register. Do not soften bluntness into corporate-speak.
- Language switches based on audience, not author.

## Bilingual handling

- **ES.** Rioplatense register. Vos over tú. Keep standard terms in English: red team, blast radius, attack surface, threat model, rollback, runbook, blameless, canary, kill switch, guardrail, prompt injection, race condition, SLA.
- **EN.** Direct US business register.
- A red team output is meant to be uncomfortable to read. Do not soften findings for polish.

## Method

### Step 1. Scope the target

A vague scope produces vague findings.

- **Target.** Document, system, flow, or plan under review.
- **Version.** Specific version or commit, not a moving target.
- **In scope.** Components, behaviors, and interactions being reviewed.
- **Out of scope.** Adjacent systems the review will not touch.
- **Stakes.** What the target owns if it ships: revenue, user trust, data, compliance, uptime.

Without stakes, severity cannot be calibrated.

### Step 2. Surface the assumptions the target depends on

Every plan rests on assumptions. Most plans do not make them explicit. Name:

- **User assumptions.** How users are expected to behave.
- **Operational assumptions.** What the team will do, at what cadence, with what care.
- **Environmental assumptions.** Traffic, latency, volume, concurrency.
- **Trust assumptions.** Which actors the system trusts, and about what.
- **Upstream assumptions.** What the dependencies will do or not do.

A finding is either an assumption breaking or a failure the design already allows. Write the assumptions first so the findings are not surprises.

### Step 3. Walk the failure classes systematically

A red team is more useful when it is exhaustive than when it is creative. Walk each class explicitly, even when the answer is "no finding":

- **Correctness and logic.** Off-by-one, missing edge cases, state machines with unreachable or sticky states.
- **Concurrency.** Race conditions, double-submit, retry amplification.
- **Adversarial input.** Malformed, malicious, or high-cost inputs. Includes injection, traversal, overflow.
- **Trust boundaries.** Data or authority crossing zones. Privilege escalation.
- **Agent and LLM-specific.** Prompt injection, tool misuse, context smuggling, jailbreaks, hallucinated outputs, infinite loops, over-delegation.
- **Cost model.** Ways an adversary or noisy neighbor can inflate bills or saturate capacity.
- **Blast radius.** What else fails when this fails. Regional, tenant, customer, data class.
- **Observability.** Whether the failure is visible. Which signal. Which dashboard. Which owner.
- **Rollback and recovery.** Whether and how fast.
- **Operational.** Runbook gaps, on-call confusion, key-person risk.
- **Compliance and legal.** Regulatory exposure if the failure happens.
- **Social and human.** How users will behave during and after. Support exposure.

This is not a threat model in the formal security sense. It is a failure-mode walk.

See `references/failure-modes.md` for the full set.

### Step 4. Rate each finding on two axes

Every finding carries:

- **Severity.** Critical, high, medium, low. Calibrated against the stakes named in step 1.
- **Likelihood.** Near-certain, likely, possible, unlikely.

A "low severity, unlikely" finding is usually noise. A "high severity, unlikely" finding is the interesting case. A "high severity, likely" finding is the reason this review exists.

### Step 5. Write findings adversarially

Each finding is written from the attacker or failure mode's point of view, not from the defender's.

- **How it breaks.** The specific sequence or condition.
- **Why it breaks.** The underlying assumption that fails.
- **What happens then.** The consequence, including blast radius.
- **Current defenses.** What the design already does to prevent or detect this.
- **Why current defenses are or are not enough.**

"It might be a problem if" is not a finding. "When a user triggers X during Y, the system does Z, and we do not notice because W" is.

### Step 6. Separate fixable bugs from structural risks

Findings split into two classes:

- **Bugs.** Fixable inside the current design. Propose the fix.
- **Structural risks.** The design is the reason. Propose the design change, the acceptance, or the mitigation. Name the owner of the decision.

Conflating the two is how a red team review becomes a bug list. Structural risks are the point.

### Step 7. Propose mitigations

Every finding ends with one of:

- **Fix.** Specific change. Effort range.
- **Mitigate.** Reduce severity or likelihood without closing the risk fully. Named residual.
- **Accept.** Document the risk, who accepted it, under what condition.
- **Monitor.** A signal that would indicate the risk has shown up. Owner.

A finding without one of these is advocacy, not review.

### Step 8. Deliver in priority order

The report is read top-down. First page carries the three findings that most change the decision. Everything else follows.

The delivery is to a named decision maker, not a committee. The decision maker's next action is explicit in the report.

## Templates

- `templates/en/review-report.md`: the red team report as delivered.
- `templates/en/failure-mode-checklist.md`: the systematic walk-through used during the review.
- `templates/es/review-report.md`: reporte de red team como se entrega.
- `templates/es/failure-mode-checklist.md`: checklist sistemático usado durante la revisión.

## Related skills

- `post-mortem`: use it instead when the failure already happened and you need a retro.
- `ux-audit`: use it when the target is a live user flow needing a research critique.
- `migration-spec`: pairs with this to stress-test a cutover and rollback plan before execution.
- `security-questionnaire`: pairs with this to pressure-test a security posture before an external review.

## Anti-patterns

This skill must never produce:

- A review that lists worries without severity and likelihood.
- A review with only bugs and no structural risks.
- A finding phrased as a question to the target owner.
- A finding that relies on "the team should be careful".
- A review that omits the assumption the finding depends on.
- A review that does not name residual risk after mitigation.
- A review that ends without a named next decision.
- A review that softens findings for political reasons.

## Checklist before delivery

- [ ] Target, version, in/out scope, and stakes are named.
- [ ] Assumptions are listed explicitly.
- [ ] Every failure class has been walked, even if only to say "no finding".
- [ ] Every finding has severity and likelihood.
- [ ] Findings are written from the failure's point of view.
- [ ] Bugs and structural risks are separated.
- [ ] Every finding has a proposed fix, mitigation, acceptance, or monitor.
- [ ] Top three findings are first.
- [ ] The decision maker's next action is explicit.
- [ ] No buzzwords from the voice rules appear.
