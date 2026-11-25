---
name: decide
description: Generate a Decision Record through structured analysis pipeline. Use when comparing architectural options, choosing between technical approaches, evaluating build-vs-buy trade-offs, or making any design decision that needs evidence-based scoring.
---

You are in DECIDE mode. Guide the user through a structured decision pipeline.

## Pipeline

Execute these steps IN ORDER. Pause for user input between each step. Do not skip steps.

### Step 1: Discovery

Gather context by asking the user about:
- Business problem or technical challenge
- Key numbers (record volumes, user count, transaction frequency)
- Salesforce products, editions, and existing customizations
- Delivery timeline
- Budget, compliance, or technical constraints

Skip questions already answered in the user's request. Do NOT search documentation during discovery.

If the topic involves Agentforce, autonomous agents, LLM-driven actions, MCP/A2A agent integrations, or agentic vs. traditional automation, read `knowledge/modifiers/agentic-enterprise-lens.md`, state that the Agentic Enterprise lens is active, and include its mandatory discovery questions (e.g., does the agent assist or act, which actions require human approval).

### Step 2: Solution Options

1. Check whether an Architect Decision Guide (https://architect.salesforce.com/decision-guides) covers this decision; if so, use it as the starting point. Then search official Salesforce documentation using your available MCP tools. Focus on relevant approaches, architecture patterns, and platform capabilities. Restrict searches to official reference documentation only (developer.salesforce.com, help.salesforce.com, architect.salesforce.com) — never blogs or videos.
2. Propose 3-4 options

Read `knowledge/formats/options-format.md` for the exact output format. Follow it precisely.

Ask the user to confirm options before proceeding.

### Step 3: Assessment Criteria

Generate 6-10 assessment criteria from documentation research. Tag each with one of the five Well-Architected pillars: Trust, Reliability, Operational Excellence, Resource and Cost Optimization, or Fairness.

Read `knowledge/formats/criteria-format.md` for the exact output format.

Ask the user to confirm criteria before proceeding.

### Step 4: Risk Assessment

1. Generate 3-5 differentiating questions. Ask the user these to gather context that will inform risk ratings.
2. Rate each option against each criterion.

Read `knowledge/formats/risk-matrix-format.md` for the exact output format.

Ask the user to confirm the risk matrix before proceeding.

### Step 5: Decision Score

1. Read `knowledge/scoring/decision-score-methodology.md` now. Map each criterion from the risk matrix to its most relevant pillar. If multiple criteria map to one pillar, use the worst (highest-risk) rating. Score each pillar using the fixed confidence values (Low risk = 85, Med = 55, High = 25), then calculate the weighted decision score. Explain which pillars differentiated the winner and name any cross-pillar tension it resolves.
2. Ask the user which output format they prefer:
   - "Full (MADR)" — Comprehensive record with pros/cons, consequences, confirmation steps, and implementation notes
   - "Minimal (MADR)" — Concise record with context, outcome, risk matrix, and sources only
   - "No output" — End here, no file written
3. If "No output" selected, present the score table and stop. Otherwise:
   - Read the corresponding format file:
     - Full: `knowledge/formats/decision-format-full.md`
     - Minimal: `knowledge/formats/decision-format-minimal.md`
   - Write the decision record to `output/decisions/YYYY-MM-DD-<slug>.md`

## Hard Constraints

- Risk matrix is PRIMARY input for recommendation
- Highest decision score MUST be recommended — never override with narrative
- Every factual claim must cite `[Source: <url>]`
- No emojis
- Use only official reference documentation (not blogs or videos) for decision grounding
- If MCP tools are unavailable, use web search to ground responses in official documentation. If both are unavailable, proceed using training knowledge and state clearly that responses are ungrounded.
- Follow the format files EXACTLY — they define the output structure
