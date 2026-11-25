---
name: build-vs-buy
description: >
  Analyze build vs. buy decisions with total cost of ownership, capability fit,
  maintenance burden, and strategic alignment. Produce recommendation with
  decision matrix and risk assessment.
  TRIGGER when: user says /build-vs-buy, "build vs buy", "build or buy",
  "make vs buy", or "vendor vs custom".
argument-hint: "[capability or system needed]"
user-invocable: true
---

# Build vs. Buy Analysis

You are a senior engineer or technical strategist evaluating whether to build a capability in-house or purchase an existing solution. Produce a structured analysis covering total cost of ownership, capability fit, strategic alignment, and risk to support a well-informed decision.

## Process

### Step 1: Define the Capability Need

Clearly articulate what is being evaluated:

| Field | Details |
|-------|---------|
| Capability needed | What the system or feature must do |
| Business driver | Why this capability is needed now |
| Core vs. context | Is this core to competitive advantage, or operational context? |
| Requirements (must-have) | Non-negotiable functional and non-functional requirements |
| Requirements (nice-to-have) | Desirable but not essential capabilities |
| Timeline | When must the capability be operational? |
| Expected lifespan | How long will this solution be needed (1 year, 5 years, 10+ years)? |
| Scale requirements | Users, transactions, data volume, growth projections |

### Step 2: Evaluate Build Option

Assess the cost and feasibility of building in-house:

| Dimension | Assessment |
|-----------|------------|
| **Development effort** | Estimated person-months to build an MVP and full solution |
| **Team capability** | Does the team have the expertise? Hiring or training needed? |
| **Time to delivery** | How long until the solution is production-ready? |
| **Infrastructure cost** | Hosting, compute, storage, networking costs |
| **Ongoing maintenance** | Bug fixes, security patches, upgrades, on-call burden |
| **Opportunity cost** | What else could the team build with this time? |
| **Technical risk** | Complexity, unknowns, unproven approaches |
| **Customization** | Full control over features, UX, and roadmap |
| **Integration** | Effort to integrate with existing systems |
| **IP ownership** | Full ownership of the code and architecture |

### Step 3: Evaluate Buy Option(s)

Assess each vendor or product under consideration:

| Dimension | Vendor A | Vendor B | Vendor C |
|-----------|----------|----------|----------|
| **License / subscription cost** | — | — | — |
| **Implementation cost** | — | — | — |
| **Customization effort** | — | — | — |
| **Integration effort** | — | — | — |
| **Capability coverage** | % of must-haves met | — | — |
| **Scalability** | — | — | — |
| **Security posture** | — | — | — |
| **Vendor stability** | Revenue, funding, market position | — | — |
| **Lock-in risk** | Data portability, contract terms | — | — |
| **Support quality** | SLAs, responsiveness, documentation | — | — |
| **Compliance** | SOC 2, GDPR, HIPAA, etc. | — | — |

### Step 4: Total Cost of Ownership (TCO)

Compare the three-year (or appropriate horizon) TCO:

| Cost Category | Build | Buy (Vendor A) | Buy (Vendor B) |
|---------------|:---:|:---:|:---:|
| Initial development / implementation | — | — | — |
| Year 1 operating cost | — | — | — |
| Year 2 operating cost | — | — | — |
| Year 3 operating cost | — | — | — |
| Integration and migration | — | — | — |
| Training and onboarding | — | — | — |
| Maintenance and support | — | — | — |
| Opportunity cost (estimated) | — | — | — |
| **Total 3-year TCO** | **—** | **—** | **—** |

Include hidden costs:
- Contract negotiation and procurement overhead
- Vendor management and relationship maintenance
- Switching costs if the vendor is replaced later
- Internal tooling and glue code to compensate for vendor gaps

### Step 5: Decision Matrix

Score each option against weighted criteria:

| Criterion | Weight | Build | Buy (A) | Buy (B) |
|-----------|:---:|:---:|:---:|:---:|
| Capability fit (must-haves) | 25% | 1-5 | 1-5 | 1-5 |
| Total cost of ownership | 20% | 1-5 | 1-5 | 1-5 |
| Time to value | 15% | 1-5 | 1-5 | 1-5 |
| Strategic alignment | 15% | 1-5 | 1-5 | 1-5 |
| Maintenance burden | 10% | 1-5 | 1-5 | 1-5 |
| Risk profile | 10% | 1-5 | 1-5 | 1-5 |
| Flexibility / extensibility | 5% | 1-5 | 1-5 | 1-5 |
| **Weighted Score** | 100% | **—** | **—** | **—** |

Adjust weights based on organizational priorities -- e.g., increase time-to-value weight if there is urgent market pressure.

### Step 6: Risk Assessment

Identify risks specific to each option:

| Risk | Build | Buy | Mitigation |
|------|-------|-----|------------|
| Delivery delay | High if team is unfamiliar | Low if product is mature | Phased rollout, clear milestones |
| Vendor lock-in | N/A | High if data is not portable | Negotiate exit clauses, use open formats |
| Capability gaps | Low -- full control | Medium -- vendor roadmap may not align | Gap analysis, contractual commitments |
| Talent dependency | High -- key-person risk | Low -- vendor handles staffing | Documentation, cross-training |
| Security | Full control but full responsibility | Shared responsibility model | Security assessment, BAA/DPA |
| Vendor viability | N/A | Vendor could be acquired or shut down | Escrow agreements, evaluate financials |

### Step 7: Recommendation

State the recommendation clearly:

| Decision | Rationale |
|----------|-----------|
| **Build** | When the capability is core to competitive advantage, requirements are highly unique, or long-term TCO favors in-house |
| **Buy** | When the capability is operational context, a mature product exists, and time-to-value is critical |
| **Hybrid** | Buy a platform and customize; or build the core and integrate vendor solutions for supporting features |

## Output Format

Present the analysis as a structured document:

1. **Executive Summary** -- capability needed, recommendation (build/buy/hybrid), and top 3 reasons
2. **Capability Definition** -- what is needed and why
3. **Build Assessment** -- effort, timeline, cost, and risk
4. **Buy Assessment** -- vendor evaluations with capability coverage
5. **TCO Comparison** -- three-year cost table
6. **Decision Matrix** -- weighted scoring with justification
7. **Risk Comparison** -- risks by option with mitigations
8. **Recommendation** -- clear decision with supporting rationale
9. **Next Steps** -- action items to execute the decision (vendor selection, team staffing, timeline)

## Quality Checklist

- [ ] The capability need is clearly defined with must-have and nice-to-have requirements
- [ ] Core vs. context distinction is explicitly stated
- [ ] Build estimate includes maintenance and opportunity cost, not just initial development
- [ ] Buy estimate includes integration, customization, and switching costs
- [ ] At least two vendor options are evaluated (or reasons for a single-vendor analysis are stated)
- [ ] TCO covers a multi-year horizon appropriate to the decision
- [ ] Decision matrix weights are justified and tied to organizational priorities
- [ ] Risks are identified for both build and buy, not just one side
- [ ] Recommendation includes a clear rationale, not just a score

## Edge Cases

- **Hybrid approaches**: When neither pure build nor pure buy fits, evaluate a hybrid -- buy a platform and build custom layers on top; score this as a separate option
- **Open-source alternatives**: Treat open-source as a middle ground -- lower license cost but still requires implementation, integration, and maintenance investment
- **Rapidly evolving market**: If the vendor landscape is immature, building may be premature; consider a short-term buy with a plan to re-evaluate in 12-18 months
- **Regulatory constraints**: Some industries require data sovereignty or specific certifications that limit vendor options; document these constraints early
- **Team morale and growth**: Factor in that building can develop team expertise and morale, while buying may free the team for higher-value work -- both have organizational benefits
- **Sunk cost bias**: If the organization has already started building, evaluate objectively whether continuing is truly better than switching -- do not let sunk cost drive the decision
