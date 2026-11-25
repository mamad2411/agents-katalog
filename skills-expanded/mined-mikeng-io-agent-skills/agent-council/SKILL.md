---
name: agent-council
description: Role-diverse local council. Dispatches multiple expert roles (Devil's Advocate, Integration Checker, Domain Experts, Synthesis Lead) within one runtime/model family to review, audit, or brainstorm. Complements Model Council, Runtime Council, and Deep Council; use when role diversity and local adversarial debate are needed.
location: managed
dependencies:
  - context
  - preflight
  - debate-protocol
  - domain-registry
allowed-tools:
  - Read
  - Glob
  - Grep
  - Task
  - Write
  - Bash(ls *)
---

# Agent Council: Role-Diverse Local Council

Execute this skill to run a local expert council using one runtime/model family with multiple specialized roles. Unlike deep-council (which composes multiple bridge/runtime councils and may also include model diversity), agent-council uses role-diverse expert PERSPECTIVES to catch:

- **Shared assumptions** that a single viewpoint misses
- **Integration gaps** between components
- **Hidden failure modes** through adversarial challenge
- **Cross-domain implications** no single expert catches

## When to Use Agent Council

| Scenario | Use Agent Council | Use Deep Council |
| --- | --- | --- |
| Need fast local role-diverse review | ✓ | Optional |
| Need phase-end closure artifact | ✓ | Optional for high-risk phases |
| Need each bridge/runtime to run its own local council | As child council | ✓ |
| Need runtime/toolchain diversity (Codex vs Claude Code vs OpenCode) | ✗ alone | ✓ |
| Need model diversity inside a bridge | ✗ alone | ✓ if bridge supports Model Council |
| Need cross-council debate | ✗ alone | ✓ |

**Agent Council is the local role-diverse primitive. Deep Council may compose multiple Agent Councils, Model Councils, or runtime-native councils and then run cross-council debate.** For shared terminology, read `council-taxonomy`.

---

## Modes

Agent Council supports multiple modes:

- `review` / `audit` — produce findings, challenge them, and return a verdict.
- `brainstorm` / `design` — produce competing proposals, challenge assumptions, merge or reject proposals, and recommend a design direction.
- `research` — produce evidence-backed observations, contradictions, confidence levels, and gaps.

### Brainstorm Mode

Brainstorm mode is for generating alternatives, not validating a coordinator's idea. The first round must be independent and minimally framed. Experts receive scope, objective, constraints, and output contract only. Do not include expected findings, a preferred design, or other experts' outputs in Round 1.

Brainstorm-mode output uses proposals, not severity findings:

```json
{
  "participant": "{role-name}",
  "mode": "brainstorm",
  "proposals": [
    {
      "id": "P001",
      "title": "Short proposal title",
      "summary": "What this design does",
      "rationale": "Why it could work",
      "tradeoffs": [],
      "failure_modes": [],
      "open_questions": [],
      "recommended_when": "When to choose this proposal"
    }
  ],
  "assumptions": [],
  "questions": []
}
```

Proposal states: `proposed`, `expanded`, `challenged`, `revised`, `merged`, `split`, `accepted`, `rejected`, `parked`, `superseded`.

---

## Execution Instructions

When invoked, you will:

0. **Resolve scope and context** — invoke preflight (if sparse) + context skill
1. Populate council context from working_scope
2. Select expert roles based on domains and task type
3. Dispatch expert agents in parallel via Task tool
4. Run debate protocol between expert perspectives
5. Produce a consolidated expert council report

---

## Step 0: Scope & Context Resolution

Follow the same pattern as deep-council Step 0:

1. **Invoke context skill** — always required
2. **Invoke preflight skill** — only if context confidence is low
3. **Merge into working_scope**

```yaml
working_scope:
  artifact: "" # from context + preflight
  intent: "" # from context or preflight
  domains: [] # from context_report.domains (authoritative)
  constraints: [] # from preflight (empty if skipped)
  context_summary: "" # combined description for agent prompts
  intensity: "standard" # from routing signals
```

---

## Step 1: Populate Council Context

```yaml
council_context:
  review_scope: "" # from working_scope.artifact
  context_summary: "" # from working_scope.context_summary
  artifact_type: "" # from context_report.artifact_type
  domains: [] # from working_scope.domains
  intensity: "standard" # from working_scope.intensity
  review_id: "" # Generate: agent-council-{YYYYMMDD-HHmmss}
  task_type: "review" # from working_scope.intent
```

Read domain-registry to map domains to expert focus areas:

```
Read: [skills-root]/domain-registry/domains/technical.md
Read: [skills-root]/domain-registry/domains/business.md
Read: [skills-root]/domain-registry/domains/creative.md
```

---

## Step 2: Select Expert Roles

Agent Council spawns these expert roles (always present):

### Core Roles (Always Dispatched)

| Role                    | Purpose                                        | Domain                  |
| ----------------------- | ---------------------------------------------- | ----------------------- |
| **Primary Reviewer**    | Direct analysis of scope with domain expertise | `{domain}` (per domain) |
| **Devil's Advocate**    | Challenge assumptions, find failure modes      | `cross-domain`          |
| **Integration Checker** | Surface cross-component implications           | `integration`           |
| **Synthesis Lead**      | Aggregate findings, resolve disputes           | `meta`                  |

### Role Count Formula

```
expert_count = len(domains) + 3  # domains + DA + IC + Synthesis Lead
```

Minimum: 4 (1 domain + 3 core roles)
Maximum: 8 (5 domains + 3 core roles) — if more domains, group related domains

---

## Step 3: Dispatch Expert Agents in Parallel

For each expert role, spawn a Task agent. All experts receive the SAME context but DIFFERENT role instructions.

### Expert Input (same for all, role varies)

```json
{
  "expert_input": {
    "session_id": "{review_id}",
    "role": "{expert_role}",
    "scope": "{review_scope}",
    "task_type": "{task_type}",
    "context_summary": "{context_summary}",
    "domains": {domains},
    "intensity": "{intensity}",
    "focus_areas": "{role-specific focus from domain-registry}"
  }
}
```

### Expert Task Prompts

**Primary Reviewer (one per domain):**

```
You are a {domain} expert reviewing: {review_scope}

## Context
{context_summary}

## Your Domain Focus
{domain-specific focus areas from domain-registry}

## Your Task
Analyze the scope from your domain perspective. Return findings as JSON:
{
  "findings": [
    {
      "id": "{domain}-001",
      "severity": "CRITICAL | HIGH | MEDIUM | LOW | INFO",
      "title": "...",
      "description": "...",
      "evidence": "...",
      "remediation": "...",
      "domain": "{domain}",
      "confidence": "high | medium | low"
    }
  ],
  "domain_coverage": "{domain}",
  "assumptions_made": ["..."]
}

Be thorough. Challenge surface-level explanations. Look for root causes.
```

**Devil's Advocate:**

```
You are the DEVIL'S ADVOCATE for this review session.

## Context
{context_summary}
Scope: {review_scope}
Intensity: {intensity}

## Your Obligations (read debate-protocol/experts/devils-advocate.md for full protocol)

1. **MUST challenge every CRITICAL and HIGH finding** from primary reviewers
2. **SHOULD challenge MEDIUM findings** when you detect a pattern
3. **Cross-domain synthesis**: look for findings whose combination implies a worse issue
4. **Pre-mortem focus**: for each component, ask "what would cause this to fail in production?"

## Challenge Quality Standard

A valid challenge must either:
- (a) Identify a missing assumption that, if corrected, reduces severity
- (b) Propose an alternative explanation at least as plausible as the stated cause
- (c) Surface a scenario where the finding does not apply

Invalid challenges: "I don't think this is serious" (without mechanism).

## Output Format

{
  "challenges": [
    {
      "target_finding_id": "...",
      "challenge": "...",
      "proposed_severity": "CRITICAL | HIGH | MEDIUM | LOW | WITHDRAWN",
      "rationale": "...",
      "status": "pending"
    }
  ],
  "new_findings": [...],  // Failure modes you discovered through challenge
  "cross_domain_implications": [...]
}
```

**Integration Checker:**

```
You are the INTEGRATION CHECKER for this review session.

## Context
{context_summary}
Scope: {review_scope}

## Focus Areas (read debate-protocol/experts/integration-checker.md for full protocol)

1. **Interface mismatches**: where does component A assume something about B that isn't guaranteed?
2. **Undocumented contracts**: implicit dependencies that work by accident
3. **Error propagation gaps**: errors one component produces but callers don't handle
4. **Timing and ordering dependencies**: race conditions, initialization ordering
5. **Cross-cutting assumptions**: things that must be true globally but are only enforced locally

## Your Task

For each finding from primary reviewers: does it have cross-component implications beyond its stated scope?
If yes, surface those as integration findings.

## Output Format

{
  "integration_findings": [
    {
      "id": "INT-001",
      "severity": "...",
      "title": "...",
      "description": "...",
      "components_involved": ["..."],
      "implicit_contract": "...",
      "remediation": "...",
      "domain": "integration"
    }
  ],
  "cross_component_gaps": [...]
}
```

### Parallel Dispatch

Spawn ALL expert Task agents simultaneously:

```
Task: primary-reviewer-{domain1}
Task: primary-reviewer-{domain2}
...
Task: devils-advocate
Task: integration-checker
```

Wait for ALL to complete before proceeding to Step 4.

---

## Step 4: Debate Protocol

After all experts complete their initial analysis, run a debate round:

### Round 1: Challenge Phase

Spawn a new Task agent as **Debate Coordinator**:

```
You are a DEBATE COORDINATOR for expert council synthesis.

## Context
{context_summary}
Scope: {review_scope}

## Expert Outputs (from {N} experts)
{all expert outputs JSON}

## Your Task

1. **Collect Devil's Advocate challenges** against primary reviewer findings
2. **For each challenge**, determine outcome:
   - CONFIRMED: Finding holds after challenge
   - DOWNGRADED: Severity reduced (state new severity + rationale)
   - DISPUTED: Challenge has merit but finding not withdrawn
   - WITHDRAWN: Challenge reveals finding was invalid

3. **Collect Integration Checker findings** and merge with relevant primary findings

4. **Surface cross-expert synthesis**: findings that multiple experts independently surfaced

## Output Format

{
  "debate_round": 1,
  "confirmed_findings": [...],
  "downgraded_findings": [...],
  "disputed_findings": [...],
  "withdrawn_findings": [...],
  "integration_findings": [...],
  "multi_expert_confirmed": [...],  // Findings 2+ experts agreed on
  "challenge_notes": [...]
}
```

### Round 2 (thorough intensity only): Second Challenge

For `intensity: thorough`, run a second debate round where the Devil's Advocate challenges Round 1 survivors.

---

## Step 5: Synthesis

The **Synthesis Lead** aggregates all debate outputs:

```yaml
final_findings:
  multi_expert_confirmed: # 2+ experts independently surfaced
  single_expert: # One expert surfaced, survived challenge
  integration: # Cross-component implications
  disputed: # Challenge not resolved
  withdrawn: # Invalidated by challenge

verdict:
  FAIL:
    - Any CRITICAL confirmed by 2+ experts
    - 3+ HIGH confirmed findings

  CONCERNS:
    - 1-2 HIGH confirmed findings
    - Any disputed CRITICAL/HIGH

  PASS:
    - No CRITICAL/HIGH confirmed
    - Only MEDIUM/LOW/INFO
```

---

## Step 6: Produce Output

### Council Report Structure

```json
{
  "type": "agent-council",
  "review_id": "{review_id}",
  "verdict": "PASS | FAIL | CONCERNS",
  "timestamp": "{ISO-8601}",
  "model_used": "single-model",
  "expert_roles": [
    "domain-technical",
    "devils-advocate",
    "integration-checker",
    "synthesis-lead"
  ],
  "domains_covered": ["{domain1}", "{domain2}"],
  "intensity": "standard",
  "debate_rounds": 1,
  "multi_expert_confirmed": [
    {
      "id": "MEC001",
      "severity": "HIGH",
      "title": "...",
      "description": "...",
      "evidence": "...",
      "remediation": "...",
      "confirmed_by": ["primary-reviewer-{domain}", "devils-advocate"],
      "domains": ["{domain}"]
    }
  ],
  "single_expert_findings": [
    {
      "id": "SE001",
      "severity": "MEDIUM",
      "title": "...",
      "description": "...",
      "source_role": "integration-checker",
      "domains": ["integration"]
    }
  ],
  "disputed_findings": [
    {
      "id": "D001",
      "title": "...",
      "positions": [
        { "role": "primary-reviewer", "severity": "HIGH", "position": "..." },
        { "role": "devils-advocate", "severity": "LOW", "position": "..." }
      ]
    }
  ],
  "integration_findings": [
    {
      "id": "INT-001",
      "severity": "MEDIUM",
      "title": "...",
      "components_involved": ["..."],
      "implicit_contract": "..."
    }
  ],
  "synthesis_notes": "Summary of expert council analysis"
}
```

---

## Step 7: Save Artifact

Save to `.outputs/council/{YYYYMMDD-HHMMSS}-agent-council-{review_id}.md`:

```yaml
---
skill: agent-council
timestamp: { ISO-8601 }
artifact_type: council
model_type: single-model
domains: [{ domain1 }, { domain2 }]
verdict: PASS | FAIL | CONCERNS
expert_roles: [{ role1 }, { role2 }]
debate_rounds: 1
review_id: "{unique id}"
context_summary: "{brief description}"
---
```

Also save JSON companion: `{YYYYMMDD-HHMMSS}-agent-council-{review_id}.json`

---

## Comparison: Agent Council vs Deep Council vs Model Council

| Feature | Agent Council | Deep Council |
| --- | --- | --- |
| **Primary diversity** | Roles/perspectives | Roles + models + runtimes + toolchains + debate layers |
| **Scope** | One local runtime/model family | Multiple bridge/runtime councils |
| **Dispatch method** | Local agents/roles | Bridge adapters, each running a local council when possible |
| **Catches** | Local assumptions and integration gaps | Cross-runtime blind spots, shared-bias failures, runtime/toolchain-specific discoveries |
| **Latency** | Lower | Higher |
| **Availability** | Available when local agent dispatch exists | Conditional on bridges/runtimes |
| **Confidence tier** | Local debate-confirmed | Cross-council debate-confirmed |

**Recommendation**: Use Agent Council as the default phase-end local council. Use Deep Council when runtime/tool diversity, model diversity, or cross-council debate materially improves confidence.

---

## Notes

- **Single model, multiple perspectives**: All experts use the same model but different role framings
- **Debate is mandatory**: Don't skip the challenge phase — it's where hidden assumptions surface
- **Integration findings are valuable**: Cross-component gaps are often missed by domain-focused reviews
- **Complementary to deep-council**: Run agent-council first for speed, then deep-council for maximum confidence
- **Fallback mode**: If running inside an executor without Task tool, return SKIPPED with advisory
