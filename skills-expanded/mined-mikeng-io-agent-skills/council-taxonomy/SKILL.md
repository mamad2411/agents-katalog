---
name: council-taxonomy
description: Shared vocabulary for Agent Council, Model Council, Runtime Council, and Deep Council. Use before designing or invoking council workflows so role, model, runtime/toolchain, and debate-layer diversity are not conflated.
location: managed
context: reference
---

# Council Taxonomy

This reference defines council primitives used by `agent-council`, `deep-council`, `debate-protocol`, and bridge adapters.

## Core Principle

Deep insight does not come from model diversity alone. Different runtimes using the same model can produce materially different findings because their planning loop, tool affordances, context packaging, file discovery, browser/repo access, session continuity, and error recovery differ.

Council reports must therefore record all diversity sources:

- **Role diversity** — different expert perspectives inside one council.
- **Model diversity** — different model weights/providers.
- **Runtime diversity** — different agent executors such as Claude Code, Codex, OpenCode, Gemini CLI, or Hermes subagents.
- **Toolchain diversity** — different available tools, MCP servers, browser/repo access, and shell/file workflows.
- **Evidence-channel diversity** — different ways of grounding claims: tests, logs, source files, web sources, browser observations, human input.
- **Debate-layer diversity** — local/intra-council debate and cross-council debate.

## Council Types

### Agent Council

**Diversity source:** role / perspective.

A single runtime or model family runs multiple expert roles, usually including domain experts, Devil's Advocate, Integration Checker, and Synthesis Lead.

Use for:

- phase-end reviews
- architecture/design critique
- implementation audits
- local adversarial validation

Limitations:

- Same runtime/model can share blind spots.
- Strong role prompts do not equal independent tool/runtime diversity.

### Model Council

**Diversity source:** model/provider.

One runtime/toolchain dispatches the same task to multiple configured models and synthesizes the results.

Use for:

- style/quality comparison
- model-role allocation
- subjective scoring
- checking model-specific overconfidence

Limitations:

- If all models receive the same over-specified prompt through the same runtime, they may share the same framing and tool-context blind spots.

### Runtime Council

**Diversity source:** runtime/toolchain/agent loop.

Multiple agent runtimes review or brainstorm the same scope. The models may be identical or different; the runtime/tool flow is the key independent variable.

Examples:

- Claude Code local council
- Codex local council
- OpenCode local council or model council
- Gemini CLI council
- Hermes subagent council

Use for:

- surfacing tool-affordance discoveries
- comparing repo exploration strategies
- validating whether findings survive different execution flows
- identifying runtime-specific blind spots

### Deep Council

**Diversity source:** composed role + model + runtime + toolchain + debate layers.

Deep Council is a **council-of-councils**. Each bridge/runtime runs a local council using its native strengths. The root orchestrator then runs cross-council debate over the local reports.

```text
Deep Council
├─ Claude Code bridge
│  └─ local Agent Council
├─ Codex bridge
│  └─ local Agent Council
├─ OpenCode bridge
│  └─ local Agent Council or Model Council
└─ Cross-Council Debate
   ├─ frame comparison
   ├─ finding challenge
   ├─ shared-bias challenge
   └─ final synthesis
```

Deep Council is not merely “multi-model review.” It is layered adversarial synthesis across independently operating councils.

## Brainstorm vs Review

Councils can run in different modes:

- **review/audit mode:** produce findings and validate them adversarially.
- **brainstorm/design mode:** produce competing proposals, challenge assumptions, merge or reject proposals, and converge on a design recommendation.
- **research mode:** produce evidence-backed observations, contradictions, and confidence-scored synthesis.

Brainstorm-mode councils must not be forced into finding/severity schemas. They use proposal lifecycle states instead.

## Discovery-First Context Discipline

Round 1 of any council intended for discovery or brainstorming must receive a minimal, non-leading packet:

Include:

- artifact or topic scope
- user goal / objective
- hard constraints
- allowed mutation level
- broad domains, if useful
- output contract

Exclude:

- expected findings
- suspected root cause
- coordinator’s preferred architecture
- other participants’ findings
- desired verdict
- implementation narrative presented as truth

Later rounds may introduce proposal inventories, findings, challenges, prior reports, and reconciliation packets.

## Required Reporting Fields

Council artifacts should record:

```json
{
  "council_type": "agent-council | model-council | runtime-council | deep-council",
  "mode": "review | audit | brainstorm | design | research | synthesis",
  "diversity_sources": ["role", "model", "runtime", "toolchain", "evidence", "debate-layer"],
  "participants": [],
  "models_used": [],
  "runtimes_used": [],
  "toolchains_used": [],
  "exchange_modes_used": [],
  "debate_layers": [],
  "context_policy": "minimal-non-leading | packetized-summary | full-context | targeted-challenge"
}
```

## Project-Specific Governance

Project-specific closure rules should live in the consuming project docs. For example, a project may require every phase to end with an Agent Council artifact and every major milestone to run Deep Council when bridge runtimes are available.
