---
name: orchestration-workflow
description: >
  Full optimization workflow, sub-agent launch templates, agent communication contracts,
  default configurations, tuning strategy, and knowledge base update protocol. Use when:
  (1) starting an optimization cycle, (2) launching a Profiler or Designer sub-agent,
  (3) interpreting or formatting agent communication, (4) updating the knowledge base
  after a profiling or implementation iteration, (5) deciding default configurations
  or tuning strategy for a kernel.
---

# Orchestration Workflow

## Optimization Cycle

```text
1. ANALYZE    -> Read devlog overview + current best results
2. PROFILE    -> Launch Profiler Agent -> get compact bottleneck analysis
3. SELECT     -> Choose implementation language based on the required control level
4. STRATEGIZE -> Load the shared optimization guidance plus the language-specific optimization catalog
5. DESIGN     -> Launch Kernel Designer Agent -> implement optimizations in new version
6. VERIFY     -> Launch Profiler Agent on new version -> compare with previous
7. EVALUATE   -> Target met? -> Done. Not met? -> Back to step 3
8. LEARN      -> If novel insight: update knowledge base (mandatory)
```

The `LEARN` step is mandatory whenever a profiling or implementation iteration reveals a reusable pattern, a refined applicability condition, or a confuted prior assumption.

---

## Default Configurations

### Speculative Decoding

`b=32, s=16, t=4096` -- reduce `b` if OOM.

### Default Trial Matrix for Exploratory Tuning

- Decode-like: `b=32, s=1, t=4096`
- Speculative-like: `b=32, s=16, t=4096`
- Add a third stress configuration only when a strategy or devlog evidence shows the first two points are insufficient.

### Tuning Space Exploration

- Start with testing a manual tuning tiling configuration that is expected to be good
- Explore some tiling configurations to understand how performance changes with tile sizes
- If the situation is complex, consider gross autotuning to find good configurations, but be mindful of the combinatorial explosion (use domain knowledge to prune the search space), autotuning time should be small enough to keep the kernel design exploration fast (e.g., < 1 hour per kernel version)
- If a kernel version shows significant potential, consider a more fine-grained autotuning to further refine the performance, otherwise, proceed to the next optimization iteration (do not spend too much time autotuning a kernel version that is not promising enough)

For instance, a bad example is `mla_var6_plus_v3`, which has 10'000 autotuning configurations, and does not provide any significant improvement over `mla_var6_plus_v2`. Kernel design is more important than autotuning.

---

## Sub-Agent Launch Templates

Agent definitions are in `.claude/agents/`. Spawn agents by name with a task prompt.

### Profiler

Spawn the `profiler` agent with a task prompt:

```text
Profile <kernel> <version> at b=X, s=X, t=X.
Return compact summary per the output contract.
Update the devlog performance section in docs/kernels/<kernel>.md.
```

The profiler has `/profile-kernel` preloaded via its agent definition.

### Kernel Designer

Spawn the `kernel-designer` agent with a task prompt:

```text
Create <kernel> <new_version> from <current_version>.
Language: <cutile-dsl|cute-dsl>.
Load /design-<language>-kernel and the matching reference skill if one exists.
Apply optimizations: [specific list with rationale].
Return implementation summary per the output contract.
```

The kernel-designer has `/design-kernel` preloaded. Language-specific skills must still be loaded on-demand since the language depends on the orchestrator's selection.

---

## Agent Communication Contracts

### Profiler -> Orchestrator (compact output)

```markdown
## Profile: [kernel] [version] | b=X, s=X, t=X
### Stages
| Stage | Duration | TC% | DRAM% | Occ% | Bottleneck | Key Issue |
### Bottleneck: [Memory/Compute/Latency]-bound
Root cause: [2 sentences]
### Top 3 Opportunities (ranked by estimated impact)
1. [name] -- est. X% gain -- trigger: [metric=value]

### vs Baseline (if applicable)
| Metric | Previous | Current | Change |
|--------|----------|---------|--------|
```

### Orchestrator -> Designer (instructions)

```markdown
## Optimization Task: [kernel] [current] -> [new_version]
### Current Bottleneck: [from profiler]
### Optimizations to Apply:
1. [specific optimization + rationale + link to the shared or language-specific knowledge file]

### Constraints
- register budget, target occupancy, required control level, and language-specific constraints
```

### Designer -> Orchestrator (summary)

```markdown
## New Version: [kernel] [version]
### Changes Applied: [list]
### Files: Created/Modified [paths]
### Correctness: [PASS/FAIL]

### Trial Configurations Checked
1. [b, s, t] -- [why this point matters]

### Devlog Entry Written: [path]
```

---

## Knowledge Base Update Protocol

### When to Update

- After profiling a kernel, if a new relevant optimization or anti-pattern is identified that is not currently in the catalog
- After profiling a kernel, if an existing optimization/anti-pattern is confuted, to update its validity conditions or change it to an anti-pattern/optimization as needed
- When new performance evidence refines the estimated impact of an optimization or the failure mode of an anti-pattern
- When new interactions between optimizations are discovered
- When a device-specific result can be abstracted into a reusable rule

### New Optimization Validated

1. Decide whether the finding is shared algorithmic/hardware knowledge or language-specific implementation knowledge.
2. Shared knowledge goes under `docs/knowledge/optimizations/<name>.md`.
3. Language-specific knowledge goes under `docs/knowledge/languages/<language>/optimizations/<name>.md`.
4. Add the corresponding row to the optimization index in the `/optimization-catalog` skill.
5. Capture the reusable pattern, applicability context, and the primary metrics affected.
6. Explicitly separate local evidence and generalization.

### Optimization Caused Clear Regression

1. Decide whether the failure mode is shared or language-specific.
2. Shared anti-patterns go under `docs/knowledge/anti-patterns/<name>.md`.
3. Language-specific anti-patterns go under `docs/knowledge/languages/<language>/anti-patterns/<name>.md`.
4. Add the corresponding row to the anti-pattern index in the `/optimization-catalog` skill.
5. Document the failure mode in reusable terms, not just the failing kernel/version.
6. Record which metrics exposed the problem and under what context it appears.

### Detail File Template

Every optimization and anti-pattern must refer clearly to the applicable context (e.g., MLA-specific, any online-softmax kernel, any kernel with a certain pattern). The context goes in the `When to Apply` section.

```markdown
# [Optimization Name]

## When to Apply
- [Context 1: e.g., specific kernel design or reference layer/kernel]
- [Context 2]
- [Metric condition 1]
- [Metric condition 2]

## Mechanism
[How and why this optimization works]

## Affected Metrics
- [Metric 1: e.g. occupancy]
- [Metric 2: e.g. registers/thread]
- [Metric 3: e.g. Tensor Core utilization, DRAM throughput, L2 hit rate, local-memory traffic]

## Implementation
\`\`\`python
# Code snippet
\`\`\`

## Performance Evidence
Source type: [local experiment / external report]
| Config | Before | After | Change |
|--------|--------|-------|--------|

## Generalization
[Device-agnostic takeaway. Mention architecture/device facts only insofar as they sharpen the reusable rule.]

## Pitfalls
- [Known failure modes]

## Interactions
- [How this interacts with other optimizations]
```
