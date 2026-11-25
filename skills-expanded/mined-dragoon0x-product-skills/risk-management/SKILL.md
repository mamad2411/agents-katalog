---
name: risk-management
description: "Identify, assess, and mitigate product risks before they become fires. Covers risk categorization, mitigation strategies, and communication frameworks. Use when planning complex launches, managing dependencies, or when too many things could go wrong."
---

# Risk Management

Find what could go wrong early enough to do something about it.

## How to use

- `/risk-management` Apply risk management constraints to this conversation.
- `/risk-management <initiative>` Identify and assess risks for the described initiative.

## Constraints

### Risk Identification
- MUST identify risks across four categories: technical (can we build it?), market (will anyone want it?), execution (can we deliver on time?), dependency (what external factors could block us?)
- SHOULD run a pre-mortem: "It's 3 months from now and this failed. What happened?"
- MUST document risks early, not when they've already materialized
- NEVER assume everything will go according to plan. The plan is the best case.

### Risk Assessment
- MUST score each risk on probability (1-5) and impact (1-5)
- Priority = probability × impact. Address high-priority risks first.
- MUST distinguish between risks you can control and risks you can only monitor
- SHOULD identify leading indicators for each risk — how will you know it's materializing?
- NEVER ignore low-probability high-impact risks. Those are the ones that destroy projects.

### Mitigation
- Every high-priority risk MUST have a mitigation plan: what you'll do to reduce probability or impact
- SHOULD have contingency plans for risks that can't be fully mitigated
- MUST assign an owner to each risk — unowned risks don't get managed
- SHOULD build risk reduction into the project timeline, not treat it as overhead
- NEVER accept "we'll deal with it when it happens" as a mitigation strategy for high-impact risks

### Communication
- MUST surface risks to stakeholders early and with context: what's the risk, how likely, what's the plan
- SHOULD update risk status regularly as part of project updates
- NEVER hide risks to avoid difficult conversations. Hidden risks become surprises.
- MUST frame risks constructively: "here's what could happen and here's how we're handling it"

### Anti-Patterns
- Risk Blindness: not thinking about what could go wrong because the plan looks good
- The Risk Register Nobody Reads: documenting risks and never looking at them again
- Over-Mitigation: spending more to mitigate a risk than the risk itself would cost
- The Optimist Trap: assuming every risk is low probability because you want it to be
- Risk as Blame: using risk identification to point fingers instead of solve problems
