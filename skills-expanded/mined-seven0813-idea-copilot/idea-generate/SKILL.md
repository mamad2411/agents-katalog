---
name: idea-generate
description: Generate and rank concrete research idea candidates from a landscape map. Use for brainstorming publishable AI/CS research ideas with structured creativity frameworks and PI-style filtering.
argument-hint: "[research-direction] [--run-dir path]"
---

# Idea Generate

Generate serious research idea candidates for: **$ARGUMENTS**.

Use `${IDEA_STAGE_DIR}/LANDSCAPE.md` if present.

## Output Language

All user-facing text and all saved artifacts must be in **Chinese** by default. Keep official paper titles, benchmark names, model names, file paths, and code identifiers unchanged when needed. Follow `shared-references/output-language.md`.

Resolve `IDEA_STAGE_DIR` by following `shared-references/run-directory.md`.

## Divergence Lenses

Generate ideas using multiple lenses rather than one generic brainstorm:

- **Problem-first**: start from a concrete bottleneck or failure.
- **Solution-first**: start from a new capability and find a real problem it solves.
- **Tension hunting**: resolve performance/efficiency, generality/specialization, safety/capability, interpretability/performance, or scale/accessibility tensions.
- **Boundary probing**: expose where a widely used method breaks.
- **Abstraction ladder**: move up to a general principle, down to an extreme case, or sideways to an adjacent domain.
- **Constraint manipulation**: relax, tighten, or replace a hidden assumption.
- **Simplicity test**: ask whether a simpler method can match a complex trend.
- **Why now**: revisit old negative results under new model, data, or compute conditions.

## Candidate Format

Generate 8-12 raw ideas. Each must include:

```markdown
### Idea N：[标题]
- 核心论点：
- 问题锚点：
- 机制假设：
- 最近似方向：
- 为什么这不是简单的“把 X 用到 Y”：
- 最小可行实验：
- 预期贡献类型：方法 / 经验发现 / 诊断分析 / 理论 / benchmark
- 成功信号：
- 负结果价值：
- 风险：低 / 中 / 高
- 预计工作量：
- 最强审稿人反对意见：
```

## Filtering

After generating raw ideas, write all of them to `${IDEA_STAGE_DIR}/RAW_IDEAS.md` before filtering. Then reduce to 4-6 serious candidates by scoring:

| Criterion | Question |
|----------|----------|
| Importance | Would a strong reviewer care if this is true? |
| Novelty potential | Is there a plausible technical delta over prior work? |
| Testability | Can we get a clear signal quickly? |
| Mechanism clarity | Is the method more than a vague module name? |
| Feasibility | Is data/compute/tooling realistic? |
| Story sharpness | Can this become one paper with one dominant contribution? |

## Output

Write both files:

1. `${IDEA_STAGE_DIR}/RAW_IDEAS.md`: every generated candidate, including weak or speculative ideas.
2. `${IDEA_STAGE_DIR}/IDEA_CANDIDATES.md`: the filtered serious shortlist used by later phases.

`${IDEA_STAGE_DIR}/RAW_IDEAS.md`:

```markdown
# 原始 Idea 池

**生成数量**：
**生成依据**：`${IDEA_STAGE_DIR}/LANDSCAPE.md`

## 全部候选
[all 8-12 raw candidate cards]

## 初筛备注
| Idea | 初筛状态 | 原因 | 是否进入 shortlist |
|------|----------|------|-------------------|
```

`${IDEA_STAGE_DIR}/IDEA_CANDIDATES.md`:

```markdown
# Idea 候选

## 候选排序
| 排名 | Idea | 分数 | 风险 | 成本 | 排名理由 |
|------|------|-------|------|------|-----------------|

## 候选详情
[candidate cards]

## 未进入后续讨论的 Idea
| Idea | 淘汰/暂缓原因 | 是否值得以后回收 |
|------|-------------------|-------------------|
```

## Rules

- Include ideas that could produce publishable negative findings if they answer an important question.
- Do not keep ideas whose only novelty is a different dataset unless the dataset changes the scientific question.
- Flag any idea whose proof requires unavailable data, long training, or hidden infrastructure.
- Do not discard raw candidates silently. Weak ideas are still useful negative memory.
