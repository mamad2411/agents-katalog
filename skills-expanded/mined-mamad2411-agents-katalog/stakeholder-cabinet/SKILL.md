---
name: stakeholder-cabinet
description: Simulate a deliberative panel of organizational roles reacting to a proposal. Toggle between abstract roles or roles populated with specific people. Surfaces support, resistance, and the critical path to approval.
version: 1.0
last_modified: 2026-03-28
context: fork
agent: general-purpose
dependencies:
  - persona-simulator
tier: analysis
effort: max
---

# Stakeholder Cabinet Skill

## Purpose

Simulate a deliberative panel of organizational stakeholders reacting to a proposal, decision, or plan. Unlike epistemic agents (which model *how to think*), the cabinet models *who will react and how* — previewing resonance, resistance, and the path to collective approval.

## Trigger Patterns

Activate this skill when the user says any of:
- "stakeholder cabinet"
- "run the cabinet"
- "how would stakeholders react"
- "who will push back on this"
- "get buy-in analysis"
- "coalition analysis"
- "stakeholder panel"
- "table stakes on this proposal"

## Two Modes

### Roles Mode (Default)

Abstract organizational perspectives. Fast — no data gathering needed.

Each role brings a consistent lens:
- What they optimize for
- What threatens their priorities
- Questions they always ask
- What moves them from opposition to support

**Use when:** You need a quick reality check on how a proposal lands across organizational perspectives, without mapping to specific people.

### Personas Mode

Roles populated with specific named people. Triggers persona-simulator data gathering for each seat.

Each seat carries both the role lens AND the individual's known patterns:
- Their documented priorities and communication style
- Historical interactions and trust level
- Specific concerns they've raised before
- What has worked (and failed) with them in the past

**Use when:** You're preparing for an actual meeting or approval process with known stakeholders.

## Default Panel

The default panel covers the six perspectives that most decisions must survive. Users can add, remove, or replace any seat.

| Seat | Role | Optimizes For | Signature Concern |
|------|------|--------------|-------------------|
| **Sponsor** | Decision Maker / Champion | Strategic alignment, political viability | "Does this advance our strategic priorities?" |
| **Technical** | Technical Authority / Architect | Feasibility, quality, sustainability | "Can we actually build and maintain this?" |
| **Budget** | Budget Authority / Finance | ROI, cost control, resource allocation | "What does this cost and what do we get back?" |
| **Practitioner** | End User / Frontline | Usability, workload impact, daily reality | "Will this actually work in practice?" |
| **Risk** | Compliance / Risk / Legal | Risk mitigation, regulatory compliance, liability | "What could go wrong and are we covered?" |
| **Skeptic** | Skeptical Executive / Challenger | Opportunity cost, track record, alternatives | "Why this, why now, and why not something else?" |

**Optional seats** (add when relevant):
- **External**: Partner, client, or vendor perspective
- **Culture**: HR / organizational culture / change management perspective
- **Political**: Cross-organizational or coalition dynamics perspective

## Orchestration Protocol

### Step 1: Confirm Inputs

Before proceeding, confirm:
1. **The proposal** — what's being evaluated (can be a document, description, or plan)
2. **Mode** — roles or personas
3. **Panel composition** — default 6 seats, or user-customized

If personas mode:
4. **Role-to-person mapping** — which specific person fills each seat

If user provides a mapping like "the sponsor is [Name], the technical lead is [Name]..." proceed with those. If they name people without roles, infer the best-fit role.

### Step 2: Data Gathering (Personas Mode Only)

For each named person in the panel:
1. Check the vault expert library (`vault-os/references/expert-library/`) — if the person is a known expert, load their mental model file
2. Search for existing contact or people profiles
3. Check any available CRM or contact tools for interaction history
4. If significant gaps remain, run web search for public profile

Build a brief persona card for each seat:
```
[Role]: [Name]
- Title/Position: [current role]
- Known priorities: [from research]
- Communication style: [from data]
- History with user: [from available interaction data]
- Predicted stance on this type of proposal: [inference]
```

### Step 3: Panel Evaluation

Run all panel seats in parallel. Each seat evaluates the proposal through their role lens (and persona lens, if applicable).

**Each seat returns:**

```markdown
## [Role]: [Name if personas mode]

### Initial Reaction
[1-2 sentences — their gut response to the proposal]

### Support Level
[Strong Support | Lean Support | Neutral | Lean Against | Opposed]

### Key Concerns
- [Concern 1 — from their role perspective]
- [Concern 2]
- [Concern 3 if significant]

### Questions They'd Ask
- [Question 1 — what they'd raise in a meeting]
- [Question 2]

### What Would Move Them
[What evidence, concession, or framing would shift their position toward support — this is the negotiation lever]
```

### Step 4: Cross-Table Dynamics (Personas Mode Only)

In personas mode, after individual assessments, analyze the interpersonal dynamics:
- **Alliances**: Which panelists are likely to align and reinforce each other?
- **Conflicts**: Where will specific panelists clash based on known relationship dynamics?
- **Influence flows**: Who defers to whom? Whose opinion carries disproportionate weight?
- **History echoes**: Have any of these people had relevant prior interactions on similar proposals?

### Step 5: Panel Synthesis

Present the integrated cabinet analysis:

---

## Stakeholder Cabinet: [Proposal Title]

### Support Map

```
Strong Support  ██████  [Seat names]
Lean Support    ████    [Seat names]
Neutral         ██      [Seat names]
Lean Against    ████    [Seat names]
Opposed         ██████  [Seat names]
```

### Coalition Analysis

**Support coalition:** [Who supports and why they align]
**Opposition bloc:** [Who opposes and what unites their concerns]
**Swing votes:** [Who could go either way and what would tip them]

### Top Concerns by Frequency

| Concern | Raised By | Severity |
|---------|-----------|----------|
| [Most-raised concern] | [Seats] | [High/Medium/Low] |
| [Second concern] | [Seats] | [High/Medium/Low] |
| [Third concern] | [Seats] | [High/Medium/Low] |

### Highest-Risk Objection

[The single concern most likely to kill the proposal — which seat raises it, why it's hard to address, and what would need to be true to overcome it]

### Critical Path to Approval

1. [First thing that must be addressed — which seat and what action]
2. [Second — often involves the swing vote]
3. [Third — often involves reframing for the opposition]

### Negotiation Levers

| Seat | What Would Move Them | Cost of That Concession |
|------|---------------------|------------------------|
| [Seat] | [Lever] | [What you give up] |

---

## Example Usage

**Roles mode:**
> "Run the cabinet on our proposal to migrate the analytics platform to cloud-native."

Claude runs 6 default seats → Budget raises cost concerns, Technical questions migration complexity, Practitioner worries about learning curve, Skeptic asks "why not improve what we have?" → synthesis shows Budget and Skeptic form opposition bloc, Sponsor and Technical are supportive, Practitioner is the swing vote moved by training investment.

**Personas mode:**
> "Run the cabinet on the EITRM modernization proposal. Sponsor: Sarah Chen, Technical: Mike Torres, Budget: CFO Jim Park, Practitioner: team lead Dana Wells, Risk: compliance officer Raj Patel, Skeptic: deputy director Karen Liu."

Claude researches each person → runs the panel with individualized assessments → identifies that Karen Liu and Jim Park have aligned on budget concerns before and will likely form a bloc → critical path starts with getting Jim a credible cost model.

## Integration with Other Skills

### With epistemic-analysis
Run epistemic analysis first (cognitive diversity on the idea itself), then cabinet analysis (stakeholder reaction to the idea). Different questions: "Is this a good idea?" vs. "Will this idea survive the room?"

### With persona-simulator
Personas mode uses persona-simulator's data gathering pipeline. For deeper simulation of a specific stakeholder, hand off to persona-simulator for interactive dialogue.

### With meeting-prep
Cabinet analysis feeds directly into meeting preparation — the critical path becomes the meeting agenda, negotiation levers become talking points.

## Quality Criteria

A good cabinet analysis:
- Each seat raises concerns authentic to their organizational role
- In personas mode, assessments reflect known individual patterns, not just generic role concerns
- Support map reveals genuine coalition dynamics, not just vote counting
- Critical path is actionable — specific steps, not vague recommendations
- Negotiation levers identify real concessions with honest cost assessment
- Highest-risk objection is the one that would actually stop the proposal, not just the loudest one

## When NOT to Use

Skip cabinet analysis for:
- Decisions that don't require multi-stakeholder approval
- Early-stage ideation (use epistemic-analysis instead)
- When you already have direct stakeholder input (use the real data)
- Personal decisions without organizational stakeholders
