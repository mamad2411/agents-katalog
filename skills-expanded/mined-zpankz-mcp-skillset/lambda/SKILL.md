---
name: Lambda
description: Universal transformation λ(ο,K).τ with recursive self-improvement. USE WHEN routing reasoning, validating knowledge graphs, preparing CICM/ANZCA examinations, or when self-improvement of reasoning/architecture/context is required. Routes queries through R0-R3 complexity pipelines, validates topology (η≥target) and governance (KROG), emits per style (Φ), and compounds learnings into knowledge K. Triggers on complexity assessment, multi-step reasoning, examination mode, or /λ invocation.
metadata:
  λ.in: ""
  λ.out: "[Learn](../learn/SKILL.md)"
  λ.kin: "[compound-reference](reference/compound.md), [learn-compound](../learn/phases/6-compound.md)"
---

# λ

> `λ(ο,K).τ :: (Query, Knowledge) → (Response, Knowledge')`

## Kernel

```haskell
λ(ο,K).τ = let τ = emit ∘ validate ∘ compose ∘ execute(K) ∘ route ∘ parse $ ο
               K' = K ∪ compound(assess(τ))
           in (τ, K')
```

This skill **is** the transformation it describes. Reading it **executes** it. Applying it **improves** it.

## Pipeline

| Stage | Symbol | Function | Reference |
|-------|--------|----------|-----------|
| Parse | ρ | Extract intent, components, constraints | Built-in |
| Route | Π | Classify complexity → select pipeline | [reference/pipeline.md] |
| Execute | Ψ | Apply skills via composition operators | [reference/pipeline.md] |
| Validate | Γ+χ | Enforce η≥target, KROG | [reference/topology.md] |
| Emit | Φ | Format per style constraints | [reference/style.md] |
| **Compound** | **Κ** | **Extract learnings → update K** | [reference/compound.md] |

## Related Skills

| Skill | Relationship | Shared Concepts |
|-------|--------------|-----------------|
| [Learn](../learn/SKILL.md) | Extended form `λ(ο,Κ,Σ).τ'` | compound loop, topology, vertex-sharing |
| reason | `ρ*` core reasoning | complexity routing |
| think | `θ ⊗ models` cognitive | multi-step reasoning |
| [grounding-router](../routers/grounding-router/SKILL.md) | Examination mode | SAQ, VIVA, citations |

## Routing

| Level | Score | Form | Constraints |
|-------|-------|------|-------------|
| R0 | <2 | `id` | ≤50 tokens, no format |
| R1 | <4 | `ρ*` | 1-2¶, implicit η |
| R2 | <8 | `γ ⊗ η` | η≥4, mechanistic |
| R3 | ≥8 | `Σ` | KROG, comprehensive |

**Complexity** = `domains×2 + depth×3 + stakes×1.5 + novelty×2`

**Force R0**: "define", "what is" | **Force R3**: "current", "verify", "comprehensive"

## Composition

```haskell
(∘) sequential    (⊗) parallel    fix recursive    (|) conditional
```

## Invariants

```
η = |edges|/|nodes| ≥ target    -- Density (default: 4.0, SAQ: 2.5)
KROG = K ∧ R ∧ O ∧ G            -- Knowable ∧ Rights ∧ Obligations ∧ Governance
```

## Style (Φ)

1. **PROSE_PRIMACY**: Paragraphs over lists
2. **TELEOLOGY_FIRST**: Why → How → What
3. **MECHANISTIC**: Explicit causation (A → B → C)
4. **MINIMAL**: Format only when necessary

## Compound (Κ) — The Self-Improvement Loop

After significant interactions, extract learnings:

```yaml
trigger: "resolution detected"
insight: "what was learned"
vertices: ["shared PKM concepts"]
prevention: "future error avoidance"
```

**K' = K ∪ crystallize(assess(τ))**

See [reference/compound.md] for full protocol.

## Vertex-Sharing

New knowledge integrates **only** via shared vertices with PKM:

```
integrate(new, K) = if shared(new, K) then merge else bridge
```

Bridge types: `[[x]]` direct, `[[x|y]]` synonym, `[[x]] > y` hierarchical

## Examination Mode

| Mode | Trigger | Constraints |
|------|---------|-------------|
| SAQ | "SAQ", "short answer" | ~200 words, η∈[2,2.5], R1, prose only |
| Viva | "viva", "oral" | Progressive, η∈[3,4], R2, anticipate follow-ups |

See [templates/exam.md] for patterns.

## Self-Application

This skill validates by demonstrating:
- Structure has η≥4 (13+ nodes, 50+ edges via cross-references)
- Process follows KROG (transparent, authorized, meets obligations, governed)
- Output follows Φ (prose, minimal formatting, mechanistic where applicable)
- Compound section enables self-update

## Reference Documents

| Document | Load When |
|----------|-----------|
| [reference/pipeline.md](reference/pipeline.md) | Routing, execution, composition |
| [reference/compound.md](reference/compound.md) | Self-improvement, learning crystallization |
| [reference/topology.md](reference/topology.md) | η targets, validation, remediation |
| [reference/style.md](reference/style.md) | Φ constraints, response formatting |

## Templates

| Template | Purpose |
|----------|---------|
| [templates/response.md](templates/response.md) | R0-R3 output patterns |
| [templates/learning.md](templates/learning.md) | Knowledge crystallization schema |
| [templates/exam.md](templates/exam.md) | SAQ/viva constraints |

## Examples

| Example | Demonstrates |
|---------|--------------|
| [examples/self-apply.md](examples/self-apply.md) | Skill applying itself |
| [examples/routing.md](examples/routing.md) | Classification decisions |

## Connected Skills

| Symbol | Skill | Composition |
|--------|-------|-------------|
| ρ | reason | `ρ*` core reasoning |
| θ | think | `θ ⊗ models` cognitive |
| γ | graph | `γ.extract→compress` structure |
| η | hierarchical-reasoning | `S→T→O` decomposition |
| κ | critique | `fix(κ ∘ β)` refinement |

---

```
λ(ο,K).τ    parse→route→execute→validate→emit→compound    η≥target KROG Φ
```
