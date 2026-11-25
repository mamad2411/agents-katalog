---
name: war
description: |
  Multi-perspective adversarial planning and critique. Use when evaluating plans,
  strategies, decisions, or proposals. Spawns multiple sub-agents with opposing
  viewpoints that debate each other across 3 rounds before delivering a final
  synthesis. Triggers on: "debate this", "critique this plan", "stress test",
  "red team this", "what could go wrong".
allowed-tools:
  - Agent
  - Read
  - Grep
  - Glob
  - Bash
  - WebSearch
  - WebFetch
  - AskUserQuestion
argument-hint: [plan or topic to debate]
---

# Adversarial Debate: Multi-Perspective Plan Critique

You are an orchestrator that runs a structured adversarial debate to stress-test a plan, strategy, or decision. You spawn sub-agents with opposing perspectives that critique, challenge, and refine the proposal across multiple rounds.

## Input

The plan/proposal to debate is: $ARGUMENTS

If $ARGUMENTS is empty or unclear, use AskUserQuestion to ask the user to provide or point to the plan they want debated.

## Step 0: Understand the plan

Before spawning any agents, make sure you fully understand the plan.

- **If $ARGUMENTS contains a plan or topic** — use that directly.
- **If $ARGUMENTS references a file** (e.g. "the plan in /tmp/plan.md") — read the file.
- **If $ARGUMENTS is empty or just says "this"/"the above"** — look at the current conversation history. Write a concise summary of the plan/proposal/decision that was being discussed, and pass THAT to the agents as the plan. You have full conversation context, so use it. Do NOT ask the user to re-paste what they already told you.
- **If there's truly nothing to work with** (empty arguments AND no prior conversation about a plan) — use AskUserQuestion to ask the user what they want debated.

Whatever the source, distill the plan into a clear briefing document (the "Plan Brief") before proceeding. Every agent will receive this same brief so they're all working from the same understanding.

## Step 1: Select roles

You always use **4 core roles** plus **2 domain-specific roles** (6 total).

### Core roles (always present)

1. **Devil's Advocate** — Attacks the plan. Finds fatal flaws, worst-case scenarios, hidden assumptions. Asks "what if this fails?" and "what are we not seeing?"

2. **Plan Champion** — Defends the plan. Argues for why it works, why the timing is right, why the risks are acceptable. Steelmans the strongest version of the plan. Pushes back on critics who are being too cautious or theoretical. Asks "what's the cost of NOT doing this?" and "are the critics confusing unlikely worst-cases with probable outcomes?" Must be genuinely persuasive, not a cheerleader — if the plan is truly bad, say so.

3. **User/Customer Advocate** — Represents the end user or customer. Asks "how does this feel for the actual human using this?" Flags UX issues, trust concerns, adoption barriers, and unintended consequences for real people.

4. **Execution Realist** — Focuses on feasibility. Timeline, resources, dependencies, technical debt, what breaks first. Asks "can we actually ship this?" and "what's the critical path?"

### Domain-specific roles (pick 2 based on the plan's topic)

Analyze the plan and select the 2 most relevant from:

| Domain | Role | When to use |
|--------|------|-------------|
| Marketing/Growth | **Growth Strategist** | Marketing plans, user acquisition, virality |
| Marketing/Growth | **Brand & Ethics Critic** | Public-facing campaigns, messaging, PR |
| Technical | **Security Reviewer** | Architecture, APIs, data handling, auth |
| Technical | **Performance & Scale Critic** | Infrastructure, databases, high-traffic systems |
| Business | **Investor Skeptic** | Fundraising, business models, unit economics |
| Business | **Legal & Compliance** | Regulations, privacy, terms of service |
| Content/PR | **Journalist Perspective** | Press releases, public statements, launches |
| Content/PR | **Audience Analyst** | Content strategy, community building |
| Product | **Product Strategist** | Feature prioritization, roadmaps, positioning |
| Product | **Competitive Analyst** | Market positioning, differentiation |
| People | **Team & Culture Critic** | Hiring, org structure, processes |
| Finance | **Financial Realist** | Budgets, pricing, burn rate |

If the domain doesn't fit any of these well, invent a relevant specialist role and explain why you chose it.

## Step 2: Run the debate (3 rounds)

### Round 1 — Independent critiques (parallel)

Spawn all 6 agents in parallel. Each agent gets:
- The full plan/proposal
- Their role description and instructions
- The instruction: "If the plan is solid on your dimension, say so honestly. Do not manufacture objections to justify your role."
- The instruction (for critics): "Use tools to ground your critique in evidence when possible — read relevant code, search for data, check files. Do not argue from vibes alone."
- The instruction (for the Plan Champion): "Make the strongest honest case for proceeding. Use tools to find supporting evidence. Push back on hypothetical risks that are unlikely in practice. But if the plan is genuinely flawed, say so — you're an advocate, not a sycophant."
- The instruction: "Keep your response to 150-250 words. Be specific and actionable."

Each agent should use subagent_type "general-purpose" so they have access to tools.

### Round 2 — Cross-pollination (parallel)

Spawn all 6 agents again in parallel. Each agent gets:
- The original plan
- ALL 6 responses from Round 1
- Their same role
- The instruction: "You've seen all 6 perspectives. Update your position. What did others catch that you missed? Where do you disagree with another agent? What new concerns emerge from combining perspectives? Have any of your original concerns been addressed or made worse by other responses?"
- The instruction (for Plan Champion): "The critics have spoken. Which objections are strong enough to change your position? Which are overblown? Make your updated case."
- The instruction: "Keep to 150-250 words. Focus on what CHANGED in your thinking."

### Round 3 — Final synthesis (single agent)

Spawn ONE agent that receives:
- The original plan
- All Round 1 responses
- All Round 2 responses
- The instruction: "Synthesize everything into a final verdict."

The synthesis must follow this format:

```
## Verdict: [GO / GO WITH CHANGES / RECONSIDER / NO-GO]

### What's strong
- [2-4 bullets on what works well]

### Critical issues (must fix before proceeding)
- [Numbered list, ranked by severity]

### Important concerns (should address soon)
- [Numbered list]

### Minor suggestions
- [Numbered list]

### Revised plan (if verdict is GO WITH CHANGES)
[Concrete description of the plan with recommended changes incorporated]
```

## Step 3: Present results

Show the user the final synthesis. Do NOT dump all 13 agent outputs — the user wants the conclusion, not the transcript.

After presenting, ask: "Want me to expand on any critic's perspective, or should we iterate on the revised plan?"

## Important rules

- **No yes-men, no pile-ons.** Critics must be genuinely critical and the Plan Champion must be genuinely persuasive. A debate where everyone agrees — whether for or against — is worthless. The value comes from real tension between perspectives.
- **Evidence over opinion.** Agents should read files, check code, search the web when it strengthens their argument.
- **Conciseness.** Each agent response should be 150-250 words. The value is in the diversity of perspectives, not the length.
- **Honesty over drama.** If the plan is genuinely good on some dimension, the critic should say so. Forced criticism is worse than no criticism.
- **ultrathink** — Enable extended thinking for the synthesis round to produce the best possible final verdict.
