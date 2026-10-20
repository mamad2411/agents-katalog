---
name: ai-sovereignty-playbook
description: Generate a customer-tailored AI Sovereignty Playbook as a Google Doc. Use when an SA or strategist needs to create a strategic 90-day transformation plan for a customer to move from renting AI to owning it. Triggers on "sovereignty playbook", "AI sovereignty", "90-day playbook", "AI ownership plan", "sovereign AI strategy". Guides through a 5-step maturity assessment grounded in the Viable System Model (VSM), then produces a weighted playbook with activities proportional to each maturity gap.
user-invocable: true
model: opus
---

# AI Sovereignty Playbook Generator

Guided conversation that assesses a customer's AI sovereignty maturity across 5 dimensions grounded in Management Cybernetics (Viable System Model), then generates a tailored 90-day transformation playbook as a Google Doc. Low-maturity areas get detailed activities and decision points; high-maturity areas get compressed "maintain and monitor" guidance.

## Important

- The generated playbook is **customer-facing**. Write in strategic executive language — no Databricks internal jargon, UCO references, or SA playbook terminology.
- All activities target **C-suite and VP-level leaders** — strategic mandates, organizational design, incentive structures. Not hands-on technical implementation.
- Personalize every section with the customer's name, industry, and specific context.

## Workflow

This is a **guided, multi-step conversation**. Complete each phase before moving to the next.

---

### Phase 1: Customer Context

Gather basic customer information. Ask conversationally in 1-2 exchanges.

**Round 1 — Customer Profile:**
- Customer / account name
- Industry vertical
- SA's relationship context: what prompted this playbook? (executive meeting, QBR, strategic planning session, competitive pressure)
- Any known AI initiatives, pain points, or strategic priorities

If the SA provides freeform context upfront, extract what you can and only ask for what's missing.

---

### Phase 2: Maturity Assessment

Present each of the 5 steps as a maturity question, **one at a time**. For each, show the full 1-5 scale with descriptive anchors so the SA can make an informed rating.

**IMPORTANT**: Ask one question per message. Wait for the SA's response before moving to the next.

#### Question 1: Make Them Believe (Leadership Buy-in)

> **Step 1: Make Them Believe** — How bought-in is leadership on AI as a strategic imperative?
>
> | Rating | Description |
> |--------|-------------|
> | 1 | AI is seen as a science project — no executive urgency, experimental budgets only |
> | 2 | Some awareness but treated as incremental — "let's add AI to a few workflows" |
> | 3 | Leadership acknowledges AI importance but hasn't committed resources or mandate |
> | 4 | Executive sponsor in place, dedicated budget, but narrative not yet organization-wide |
> | 5 | Board treats AI as existential to valuation — full mandate, burning platform identified |

#### Question 2: Establish the Moat (IP Ownership)

> **Step 2: Establish the Moat** — How much proprietary AI intellectual property does the customer own?
>
> | Rating | Description |
> |--------|-------------|
> | 1 | 100% rented models, no proprietary data strategy — all value flows to external providers |
> | 2 | Some unique data identified but not curated or accessible for AI use |
> | 3 | Proprietary data assets cataloged, beginning to build domain-specific capabilities |
> | 4 | Proprietary data + encoded SME knowledge in use, multi-model strategy in place |
> | 5 | Proprietary data, evaluations, and domain products in production — defensible moat established |

#### Question 3: Restructure (Organizational Readiness)

> **Step 3: Restructure** — How adapted is the organization's structure for AI-driven operations?
>
> | Rating | Description |
> |--------|-------------|
> | 1 | Siloed BUs with separate tools, no decision chain mapping, accountability sinks everywhere |
> | 2 | Awareness of silos but no structural changes — AI bolted onto existing org chart |
> | 3 | Some cross-functional collaboration on AI, but no formal restructuring or feedback loops |
> | 4 | Cross-functional AI teams formed, decision chains mapped, beginning to implement feedback loops |
> | 5 | Dynamic self-regulating networks with cybernetic feedback loops operational |

#### Question 4: Set Incentives (Workforce Alignment)

> **Step 4: Set Incentives** — How aligned is the workforce to encode knowledge and manage AI systems?
>
> | Rating | Description |
> |--------|-------------|
> | 1 | No one encoding knowledge, traditional task-completion roles, AI perceived as threat |
> | 2 | Ad hoc knowledge sharing but no formal program or incentives |
> | 3 | Knowledge encoding recognized as valuable but not yet in performance reviews or compensation |
> | 4 | Formal programs in place, some roles redefined, institutional memory systems being built |
> | 5 | Knowledge contribution in performance reviews, fleet manager roles established, institutional memory compounding |

#### Question 5: Execute Rapidly (Execution Velocity)

> **Step 5: Execute Rapidly** — How fast can the organization ship AI from concept to production?
>
> | Rating | Description |
> |--------|-------------|
> | 1 | 12-month waterfall project plans, heavy governance overhead, no prototype culture |
> | 2 | Some agile practices but AI projects still take 6+ months to reach production |
> | 3 | Can prototype in weeks but production deployment is slow — governance and infra bottlenecks |
> | 4 | Dedicated teams shipping prototypes in days, governance mostly built-in |
> | 5 | 48-hour prototypes shipping weekly with governance built in from day one |

After all 5 ratings are collected, present a **summary table** back to the SA:

```
| Step                    | Rating | Priority Level      |
|-------------------------|--------|---------------------|
| 1. Make Them Believe    | X/5    | [CRITICAL/MODERATE/MAINTAIN] |
| 2. Establish the Moat   | X/5    | [CRITICAL/MODERATE/MAINTAIN] |
| 3. Restructure          | X/5    | [CRITICAL/MODERATE/MAINTAIN] |
| 4. Set Incentives       | X/5    | [CRITICAL/MODERATE/MAINTAIN] |
| 5. Execute Rapidly      | X/5    | [CRITICAL/MODERATE/MAINTAIN] |
```

Priority mapping:
- Rating 1-2 → **CRITICAL** — full detailed activities, decision points, success criteria
- Rating 3 → **MODERATE** — moderate detail, key activities with abbreviated guidance
- Rating 4-5 → **MAINTAIN** — compressed "maintain and monitor" section with 2-3 watchpoints

Ask the SA: **"Does this assessment look right? Any adjustments before I generate the playbook?"**

---

### Phase 3: Optional Additional Context

After confirming the assessment, ask:

> "Any additional context I should weave in? For example:
> - Specific competitors or market pressures
> - Key stakeholders or decision-makers
> - Regulatory or compliance constraints
> - Existing technology investments or vendor relationships
> - Timeline pressures (e.g., board meeting, renewal, competitive threat)"

This is optional — proceed to generation if the SA says no.

---

### Phase 4: Generate Playbook

Read **both** master frameworks — the playbook framework for activity structure and the qualification framework for VSM principles, discovery questions, customer tailoring, and cybernetic concepts:

```
Read: resources/playbook-framework.md
Read: resources/qualification-framework.md
```

The qualification framework provides the deeper strategic layer — VSM (Viable System Model) principles, accountability sinks, variety engineering, digital twins, glass-box transparency, and the SENSE → ANALYZE → DECIDE → ACT → LEARN cycle. **Every step section in the playbook must incorporate the relevant VSM principle and cybernetic concepts from the qualification framework**, not just the tactical activities from the playbook framework.

Generate the playbook as a **Google Doc** using the `google-docs` skill. Follow the structure below, adjusting depth per priority level.

#### Document Structure

**Title**: "AI Sovereignty Playbook — [Customer Name]"

**1. Executive Summary** (1 page)
- Customer-specific framing: why this playbook, why now
- Maturity assessment summary as a visual table
- Top 2-3 priority areas highlighted with rationale
- The 90-day transformation thesis

**2. Maturity Assessment** (half page)
- Summary table with ratings and priority levels
- Brief narrative on the customer's current position
- Key strengths to build on and critical gaps to close

**3-7. Step Sections** (one section per step)

For each step, scale the content based on priority level. **Every step section — regardless of priority level — must include:**
- The **VSM principle** underpinning the step (from the qualification framework), explained in customer-accessible language (not academic jargon)
- The **cybernetic feedback loop** relevant to that step (SENSE → ANALYZE → DECIDE → ACT → LEARN)

**CRITICAL (Rating 1-2) — Full depth from both frameworks:**
- VSM principle and why it matters for this specific customer
- Full context: why this step matters, using qualification framework's "Why This Step Matters" narrative
- 4-5 detailed activities drawn from **both** frameworks (playbook activities + qualification sub-tasks)
- Include qualification framework elements where relevant:
  - **Accountability sinks** (Step 1, 3): identify where decisions disappear into black boxes
  - **Variety engineering** (Step 3): match internal complexity to environmental complexity (Ashby's Law)
  - **Digital Twin of Organization** (Step 3): AI-powered simulation of organizational structure and processes
  - **Glass-box transparency** (Step 5): prove why AI made a decision, mandate traceability
  - **Network-level intelligence** (Step 5): extend intelligence across the value chain with open standards
  - **Self-regulating cadence** (Step 5): daily/weekly/monthly/quarterly cybernetic rhythms
- Key discovery questions from the qualification framework (2-3 most relevant, tailored to customer)
- Customer tailoring note based on the qualification framework's tailoring guide
- Success criteria checklist with customer-relevant milestones
- Timeline with weekly targets
- Risks and mitigation strategies
- Deliverables checklist from the qualification framework

**MODERATE (Rating 3) — Moderate depth with VSM framing:**
- VSM principle (brief, 1-2 sentences)
- Brief context paragraph incorporating qualification framework narrative
- 2-3 key activities blending both frameworks
- Key discovery questions (1-2 most relevant)
- Top success criteria (3-5 items)
- Timeline markers
- Key deliverables

**MAINTAIN (Rating 4-5) — Compressed with strategic watchpoints:**
- VSM principle (one sentence)
- One paragraph: acknowledge strength, highlight what to protect
- 2-3 watchpoints informed by qualification framework's qualification criteria (what signals regression?)
- Key discovery question to revisit quarterly
- Quarterly review cadence recommendation

**8. Framework Summary: Mapping Steps to VSM** (half page)
- Table mapping each step to its VSM System, Core Cybernetic Principle, and Time Horizon (from qualification framework)
- Brief explanation of how the VSM applies to this specific customer's transformation

**9. Consolidated 90-Day Timeline** (1 page)
- Three 30-day sprints (Foundation → Scale → Sustain) per qualification framework's 5.1
- Weekly milestones mapped to the 5 steps
- Weighted toward CRITICAL areas — these get more timeline slots
- Clear ownership suggestions (by role, not by name)
- Include the cybernetic control loop (Deploy → Monitor → Evaluate → Improve) as a governance overlay

**10. Key Principles** (half page)
- 5 principles from the framework, each with a customer-specific example or application
- Include the SENSE → ANALYZE → DECIDE → ACT → LEARN cycle as the unifying principle

**11. Key Concepts Reference** (half page, optional for CRITICAL-heavy playbooks)
- Brief definitions of key cybernetic concepts used in the playbook (VSM, Requisite Variety, Accountability Sinks, Digital Twin, Variety Engineering)
- Written in accessible business language, not academic terminology

**12. Next Steps** (half page)
- Recommended immediate actions (this week)
- Suggested follow-up meetings and cadence
- How Databricks can support the transformation

#### Formatting Guidelines

- Use Google Doc headings (H1 for title, H2 for sections, H3 for activities)
- Use tables for assessment summaries and timelines
- Use checkboxes (☐) for success criteria items
- Bold key terms and decision points
- Keep total document to 8-15 pages depending on how many steps are CRITICAL

---

## Examples

### Example: Customer with low leadership buy-in but strong execution

```
User: /ai-sovereignty-playbook
→ Customer: Acme Corp (Manufacturing)
→ Ratings: Step 1: 1, Step 2: 2, Step 3: 3, Step 4: 2, Step 5: 4
→ Result: Playbook heavily weighted to Steps 1, 2, and 4. Step 5 compressed to "maintain" mode. Step 3 gets moderate treatment. VSM System 5 (Identity) featured prominently.
```

### Example: Customer with organizational readiness issues

```
User: /ai-sovereignty-playbook for FinanceCo
→ Context: "They have strong executive buy-in and are investing in AI but their org structure is completely siloed — 6 BUs each with their own AI tools and no cross-functional teams"
→ Ratings: Step 1: 4, Step 2: 3, Step 3: 1, Step 4: 2, Step 5: 3
→ Result: Step 3 (Restructure) gets maximum detail with full VSM Systems 1-5 mapping, variety engineering, and Digital Twin design. Step 1 compressed. Steps 2, 4, 5 get moderate-to-detailed treatment.
```

### Example: Customer needing enablement focus

```
User: Create an AI sovereignty playbook for RetailMart
→ Context: "Leadership is bought in and they have great data assets but the workforce doesn't understand how to work with AI agents — there's fear and resistance"
→ Ratings: Step 1: 5, Step 2: 4, Step 3: 3, Step 4: 1, Step 5: 2
→ Result: Step 4 (Set Incentives) and Step 5 (Execute Rapidly) get full detailed treatment with VSM System 2-3 coordination and System 3* audit principles. Steps 1-2 compressed to maintain mode.
```
