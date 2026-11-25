---
name: agent-prompt-authoring
description: Author and evolve specialized agent system prompts from a specification or performance feedback. Owns the reviewed LLM prompt templates for the agent factory's generation and evolution paths.
---

# Agent Prompt Authoring & Evolution

Reviewed prompt assets for the agent-prompt reasoning in
`teaagent.domain.agent_factory` (ADR-0041 Phase 2, behavior-preserving thinning).
The deterministic template generator and heuristic evolver stay in the harness
as the default and fallback when no LLM adapter is configured; these assets own
the **LLM-path** prompt text.

## Assets

- `generation_prompt.md` — user prompt to author a specialized markdown system
  prompt for a new agent. Placeholders: `{name}`, `{description}`,
  `{task_domain}`, `{specialization_level}`, `{required_tools}`,
  `{personality_traits}`, `{constraints}`.
- `evolution_prompt.md` — user prompt to refine an existing system prompt from
  performance feedback. Placeholders: `{current_prompt}`,
  `{performance_feedback}`, `{success_metrics}`.

## Procedure

1. **Generation:** produce a comprehensive markdown system prompt that defines
   the agent's role/expertise, task-domain instructions, tool usage, personality
   traits, and safety constraints. Return markdown (no JSON wrapper).
2. **Evolution:** analyze feedback and success metrics, identify weaknesses,
   refine the prompt while preserving the agent's core purpose and constraints.
   Return the evolved markdown prompt.

## Contract

`AgentFactory` loads these templates via
`teaagent.domain._prompt_assets.load_prompt_template` and `str.format(...)`s them.
The rendered prompt is byte-identical to the prior inline prompt (locked by
`tests/domain/test_prompt_assets.py`). If an asset is missing, the factory
degrades to its deterministic template/heuristic path — the same path taken when
no LLM adapter is available.
