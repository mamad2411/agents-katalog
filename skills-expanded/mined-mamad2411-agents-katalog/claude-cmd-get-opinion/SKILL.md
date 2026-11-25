---
allowed-tools: all
description: Get brutally honest opinions from multiple agents in parallel
---

# 🗳️ /get-opinion ARGUMENTS$

**🚨 CRITICAL PARALLEL EXECUTION REQUIREMENT:**
This command MUST spawn ALL agents IN PARALLEL using single messages with multiple Task tool invocations.
NEVER spawn agents sequentially - this defeats the purpose of parallel opinion gathering.

## Arguments Integration

**Task**: ARGUMENTS$

Apply to: store_fr3k: Store opinion topic and evaluation criteria

---

## Phase 1: Opinion Strategy

**CRITICAL: Use PARALLEL spawning - ALL agents in ONE message:**
```
"I'll spawn multiple agents IN PARALLEL to analyze opinion requirements:
- opinion: Evaluate topic complexity and opinion count needed
- sherlock: Research existing patterns or precedents
- opinion: Determine DIVERSE vs CONSENSUS mode

Spawning all 3 agents simultaneously now..."
[Use single message with multiple Task tool invocations]
```

## Phase 2: Parallel Opinion Gathering

**CRITICAL: Spawn ALL opinion agents IN PARALLEL - single message, multiple tools:**
```
"I'll spawn [5-8] opinion agents IN PARALLEL for comprehensive evaluation:
- opinion (agent 1): [Specific evaluation angle 1]
- opinion (agent 2): [Specific evaluation angle 2]
- opinion (agent 3): [Specific evaluation angle 3]
- opinion (agent 4): [Specific evaluation angle 4]
- opinion (agent 5): [Specific evaluation angle 5]

Spawning all opinion agents simultaneously now..."
[MUST use single message with 5-8 Task tool invocations]
```

**⚠️ ENFORCEMENT: NEVER spawn agents sequentially. ALWAYS batch all Task invocations in one message.**

## Phase 3: Synthesis & Recommendation

**CRITICAL: Spawn synthesis agents IN PARALLEL - all at once:**
```
"I'll spawn synthesis agents IN PARALLEL to process all feedback:
- opinion: Aggregate scores and identify consensus issues
- opinion: Evaluate outlier opinions and critical concerns
- opinion: Generate final recommendation with next steps

Spawning all synthesis agents simultaneously now..."
[Use single message with multiple Task tool invocations]
```

**🚨 PARALLEL EXECUTION RULE:**
- NEVER: Spawn agent 1, wait for result, spawn agent 2...
- ALWAYS: Spawn ALL agents in ONE message with multiple tool calls
- Example: One message → 5 Task tool invocations → All run in parallel

## Success Criteria

Before marking complete:
- [ ] Multiple opinion agents completed evaluation
- [ ] Scores collected and averaged (0-10 scale)
- [ ] Consensus issues identified
- [ ] Critical concerns highlighted
- [ ] Final recommendation provided
- [ ] User has actionable next steps

## Opinion Synthesis

- Collect scores from all agents
- Identify patterns in feedback
- Highlight critical concerns and strengths
- Store synthesis results with store_fr3k

---

**Core principle: Multiple perspectives provide better decision-making.**