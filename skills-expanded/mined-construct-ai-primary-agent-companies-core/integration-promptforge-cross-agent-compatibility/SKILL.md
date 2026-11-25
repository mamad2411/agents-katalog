---
name: integration-promptforge-cross-agent-compatibility
description: >
  Use when testing and validating cross-agent compatibility, ensuring prompts work
  correctly across different agents, models, and company boundaries. This skill
  provides integration testing procedures for multi-agent prompt ecosystems.
---

# Integration - Cross-Agent Compatibility Testing

## Overview
Integration tests cross-agent compatibility for PromptForge AI. A prompt that works perfectly for one agent might fail for another. Integration ensures prompts are compatible across all agents, models, and company boundaries that will use them.

## When to Use
- Before deploying a prompt that will be used by multiple agents
- When testing prompt compatibility across different AI models
- When validating cross-company prompt interoperability (PromptForge ↔ DevForge ↔ QualityForge)
- When adding a new agent to the ecosystem
- When troubleshooting compatibility issues between agents
- **Don't use when:** Testing a prompt used by a single agent in isolation

## Core Procedures

### Step 1: Identify Compatibility Matrix
Map out what needs to be tested:
- **Agents:** Which agents will use this prompt?
- **Models:** Which AI models will run this prompt? (Claude, GPT, Gemini, etc.)
- **Companies:** Which companies will share this prompt?
- **Versions:** Which versions of each agent/model need testing?

### Step 2: Design Compatibility Tests
For each cell in the compatibility matrix:
```
COMPATIBILITY TEST
==================
Prompt: [name and version]
Agent: [agent name and version]
Model: [model name and version]
Company: [company context]
Test Inputs: [representative inputs for this agent/model]
Expected Output: [what this agent/model should produce]
Acceptance Criteria: [what "compatible" means for this test]
```

### Step 3: Execute Compatibility Tests
Run the prompt against each agent/model combination:
1. Send identical prompt to each agent/model
2. Record outputs and any errors
3. Compare outputs against acceptance criteria
4. Note any model-specific or agent-specific behavior differences
5. Document compatibility status for each combination

### Step 4: Resolve Compatibility Issues
For each incompatibility found:
- **Minor:** Output differs slightly but is acceptable → Document the difference, accept
- **Moderate:** Output quality varies significantly → Optimize prompt for the weaker model/agent
- **Severe:** Prompt fails entirely on specific model/agent → Create model-specific variant or fix root cause

### Step 5: Report Compatibility Status
```
COMPATIBILITY REPORT
====================
Prompt: [name and version]
Test Date: [date]
Matrix Size: [agents × models × companies = total tests]
Passed: [count]
Failed: [count]
Warnings: [count - minor differences]
Overall Status: [fully compatible / partially compatible / incompatible]
Incompatible Combinations: [list with details]
Recommended Actions: [what to fix and priority]
```

## Success Metrics
- Compatibility coverage: 100% of shared prompts tested across all agent/model combinations
- Compatibility pass rate: >=95% of tests pass on first run
- Resolution time: <24 hours to resolve critical incompatibilities
- Cross-company compatibility: 100% of shared prompts work across company boundaries

## Error Handling
- **Error:** Prompt works on Claude but fails on GPT
  **Response:** Analyze the difference (model capability vs. prompt structure), create model-specific variant if needed, or redesign prompt to be model-agnostic
- **Error:** Agent-specific context causes different behavior
  **Response:** Add agent-specific instructions or context handling, or standardize the context format across agents
- **Error:** Cross-company handoff changes prompt behavior
  **Response:** Test the handoff protocol, ensure context transfer preserves all necessary information

## Cross-Team Integration
**Related Skills:** flowdesigner-promptforge-agent-handoff, harmonic-promptforge-orchestration-strategy, collaborator-promptforge-cross-company-knowledge-sharing, validator-promptforge-syntax-logic-validation
**Used By:** FlowDesigner, Harmonic, Collaborator, Validator, ALL agents sharing prompts across boundaries