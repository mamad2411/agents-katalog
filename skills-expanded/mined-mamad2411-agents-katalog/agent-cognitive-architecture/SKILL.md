---
name: Agent Cognitive Architecture
description: Use when enhancing the agent reasoning loop with ReAct, Tree of Thoughts, Reflexion, self-reflection, skill libraries, or orchestrator-workers patterns for TheSearch memory system.
---

# Agent Cognitive Architecture

## Overview

TheSearch's agent loop (PRÉ → DURANTE → PÓS) is a linear pipeline. Research in cognitive architectures (ReAct, ToT, Reflexion, Voyager, Generative Agents, MemGPT, GWA) provides patterns to evolve this into a richer cognitive loop: **Observe → Retrieve → Reason → Act → Reflect → Store**.

**Core principle:** The agent should reason about *why* it stores memories, not just mechanically extract them.

## When to Use

- Enhancing `AgentLoopService` with reasoning strategies
- Adding self-reflection to memory quality assessment
- Implementing multi-step tasks that require planning
- Deciding between ReAct, ToT, or Reflexion for a given task
- Building a skill library (Voyager pattern) for procedural memory
- Designing orchestrator-workers decompositions

## Current State: Linear 3-Phase Loop

```
PRÉ  → pre_task_context()   → load design rules, patterns
DUR  → during_task_query()  → semantic search on demand
PÓS  → post_task_summary()  → extract → admit → persist
```

Limitations:
- No reasoning about retrieval quality
- No self-correction when extraction fails
- No planning for multi-step tasks
- No procedural memory (skill library)

## Enhanced Cognitive Loop

```
┌──────────────────────────────────────────────────────────┐
│                   Cognitive Loop                          │
│                                                          │
│  OBSERVE   → Receive task, load context (PRÉ)            │
│  RETRIEVE  → Hybrid search with relevance judgment       │
│  REASON    → Select strategy (ReAct/ToT/Reflexion)       │
│  ACT       → Execute task, consult memory during (DUR)   │
│  REFLECT   → Evaluate quality of actions & outputs       │
│  STORE     → Extract, evaluate, persist (PÓS)            │
└──────────────────────────────────────────────────────────┘
```

## Strategy Selection: ReAct vs ToT vs Reflexion

```python
def select_strategy(task: Task) -> str:
    if task.is_multi_step and task.has_dependencies:
        return "orchestrator_workers"
    if task.requires_exploration and task.branching_depth > 2:
        return "tree_of_thoughts"
    if task.previous_attempts > 0:
        return "reflexion"
    return "react"
```

| Strategy | When | Cost | Example |
|----------|------|------|---------|
| **ReAct** | Simple lookup, single-step tasks | Low | "Find the design rule for API versioning" |
| **Tree of Thoughts** | Complex reasoning, multiple valid paths | High | "Plan the migration strategy for the payment module" |
| **Reflexion** | Task failed, need self-correction | Medium | "Extraction returned 0 candidates — retry with different prompt" |
| **Orchestrator-Workers** | Multi-step with independent subtasks | High | "Ingest all PRs from Q1 and consolidate duplicates" |
| **Evaluator-Optimizer** | Quality-critical output | Medium | "Ensure extracted memories pass all 5 admission gates" |

## 1. ReAct: Interleaved Reasoning + Action

For most TheSearch operations. The agent reasons about each step:

```python
class ReActStep(BaseModel):
    thought: str
    action: str
    observation: str

async def react_search(query: str, project: str) -> list[dict]:
    steps: list[ReActStep] = []
    
    # Thought 1: What am I looking for?
    steps.append(ReActStep(
        thought=f"User asks about {query}. Need to search memories.",
        action="memory.query",
        observation="",
    ))
    
    results = await search.search(query_text=query, project=project, top_k=10)
    
    # Thought 2: Are these results sufficient?
    if len(results) < 3:
        steps.append(ReActStep(
            thought="Few results. Try broader query or different category.",
            action="memory.query(broader=True)",
            observation=f"Got {len(results)} results, retrying...",
        ))
        results = await search.search(query_text=query, project=project, top_k=20)
    
    return results
```

**When in TheSearch:** Most `during_task_query` calls, single-step memory lookups.

## 2. Tree of Thoughts: Systematic Exploration

For complex planning where multiple paths exist:

```python
from dataclasses import dataclass, field

@dataclass
class ThoughtNode:
    content: str
    score: float = 0.0
    children: list["ThoughtNode"] = field(default_factory=list)

async def tot_plan(task: str, project: str, max_depth: int = 3) -> ThoughtNode:
    root = ThoughtNode(content=task)
    
    candidates = await llm.generate_thoughts(task, n=5)
    
    for candidate in candidates:
        score = await llm.evaluate_thought(candidate, task)
        node = ThoughtNode(content=candidate, score=score)
        
        if score > 0.7 and max_depth > 1:
            node = await tot_plan(candidate, project, max_depth - 1)
        
        root.children.append(node)
    
    root.children.sort(key=lambda n: n.score, reverse=True)
    return root
```

**When in TheSearch:** Migration planning, architecture decisions, multi-domain queries.

## 3. Reflexion: Self-Reflection for Memory Quality

When extraction or admission produces poor results, the agent reflects:

```python
@dataclass
class Reflection:
    task_summary: str
    outcome: str
    success: bool
    lessons: list[str]

async def reflective_extraction(
    content: str, project: str, max_attempts: int = 3
) -> list[MemoryCandidate]:
    reflections: list[Reflection] = []
    
    for attempt in range(max_attempts):
        candidates = await extraction.extract_candidates(content, project)
        
        if not candidates:
            reflection = Reflection(
                task_summary=f"Attempt {attempt + 1}: 0 candidates extracted",
                outcome="No durable knowledge found",
                success=False,
                lessons=["Content may lack durable knowledge", "Try broader extraction"],
            )
            reflections.append(reflection)
            content = f"{content}\n\nPREVIOUS ATTEMPTS FAILED: {[r.lessons for r in reflections]}"
            continue
        
        admitted = []
        for candidate in candidates:
            result = await admission.evaluate(candidate)
            if result.status in ("active", "proposed"):
                admitted.append((candidate, result))
        
        if admitted:
            return [c for c, _ in admitted]
        
        reflections.append(Reflection(
            task_summary=f"Attempt {attempt + 1}: {len(candidates)} candidates, 0 admitted",
            outcome="All rejected by admission gates",
            success=False,
            lessons=["Review extraction prompt", "Check category inference"],
        ))
    
    return []
```

**When in TheSearch:** Post-task when `post_task_summary` returns all rejections.

## 4. Voyager Skill Library (Procedural Memory)

Store successful task patterns as reusable skills:

```python
@dataclass
class Skill:
    name: str
    description: str
    pattern: str
    examples: list[str]
    success_count: int = 0

class SkillLibrary:
    def __init__(self, neo4j: Neo4jService):
        self.neo4j = neo4j
    
    async def record_skill(self, skill: Skill) -> str:
        return await self.neo4j.upsert_node(
            label="ProceduralMemory",
            properties={
                "name": skill.name,
                "description": skill.description,
                "pattern": skill.pattern,
                "examples": skill.examples,
                "success_count": skill.success_count,
                "type": "skill",
            },
        )
    
    async def find_skill(self, task_description: str) -> Skill | None:
        results = await self.neo4j.search_by_embedding(
            text=task_description, label="ProceduralMemory", top_k=3
        )
        if results and results[0].get("score", 0) > 0.8:
            return Skill(**results[0])
        return None
```

**Cypher for skill nodes:**
```cypher
MERGE (s:ProceduralMemory {name: $name})
SET s.description = $description,
    s.pattern = $pattern,
    s.examples = $examples,
    s.success_count = s.success_count + 1,
    s.updated_at = datetime()
```

## 5. Orchestrator-Workers Pattern

For complex multi-step tasks (Anthropic pattern):

```python
async def orchestrator_execute(task: str, project: str) -> dict:
    subtasks = await llm.decompose_task(task)
    
    results = await asyncio.gather(*[
        worker_execute(subtask, project) for subtask in subtasks
    ])
    
    synthesized = await llm.synthesize(results)
    return await post_task_summary(task, synthesized, project)
```

**When in TheSearch:** Bulk ingestion, cross-project consolidation, complex queries spanning multiple domains.

## 6. Evaluator-Optimizer for Memory Quality

```python
async def evaluate_and_optimize(
    candidates: list[MemoryCandidate],
    threshold: float = 0.7,
    max_rounds: int = 3,
) -> list[MemoryCandidate]:
    optimized = list(candidates)
    
    for round_num in range(max_rounds):
        scores = await llm.batch_evaluate(optimized)
        passing = [c for c, s in zip(optimized, scores) if s >= threshold]
        failing = [(c, s) for c, s in zip(optimized, scores) if s < threshold]
        
        if not failing:
            return passing
        
        improved = []
        for candidate, score in failing:
            feedback = await llm.generate_improvement_feedback(candidate, score)
            improved_candidate = await llm.apply_feedback(candidate, feedback)
            improved.append(improved_candidate)
        
        optimized = passing + improved
    
    return [c for c, s in zip(optimized, await llm.batch_evaluate(optimized)) if s >= threshold]
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Using ToT for simple queries | ReAct is sufficient for 80% of TheSearch operations |
| Skipping reflection when all candidates are rejected | Always reflect on failures — it's the core learning signal |
| Storing ephemeral details as skills | Skills must be *reusable patterns*, not one-off solutions |
| Running orchestrator synchronously | Workers are independent — use `asyncio.gather` |
| Ignoring cognitive load | Limit ToT depth to 3, Reflexion retries to 3 |

## References

- ReAct: Yao et al. (2023) — interleaved reasoning + action
- Tree of Thoughts: Yao et al. NeurIPS 2023 — systematic path exploration
- Reflexion: Shinn et al. NeurIPS 2023 — verbal self-reflection
- Voyager: Wang et al. (2023) — skill library as procedural memory
- Generative Agents: Park et al. (2023) — observe → reflect → plan loop
- MemGPT/Letta: Packer et al. (2023) — virtual context management
- GWA: Global Workspace Agents (2025) — entropy-based drive
- Anthropic: Building Effective Agents (2024) — prompt chaining, orchestrator-workers, evaluator-optimizer
- Source: `knogdement/06_ai_agents_vanguard.md`, `knogdement/02_temporal_memory_trees.md`
