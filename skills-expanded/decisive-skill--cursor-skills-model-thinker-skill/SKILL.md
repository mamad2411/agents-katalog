---
name: model-thinker
description: Guides many-model thinking using Scott E. Page's The Model Thinker (模型思维)—REDCAPE purposes, diverse model ensembles, and model selection for complex phenomena. Use when the user analyzes systems, forecasts, designs policy/incentives, explains data patterns, faces complexity/uncertainty, or asks for 模型思维, many-model thinking, REDCAPE, multi-model, power-law, Markov, SIR, path dependence, or better reasoning with models. Responds in the user's language (English or 中文).
---

# Model Thinker (Many-Model Thinking)

Based on *The Model Thinker* by Scott E. Page（《模型思维》）。**2–5 个多样模型**（默认 3）优于单一模型；详见 [reference.zh.md](reference.zh.md) / [reference.en.md](reference.en.md)。

## Language

**Match the user's language.** Localized headings only.

| User language | Model reference |
|---------------|-----------------|
| English | [reference.en.md](reference.en.md) |
| 中文 | [reference.zh.md](reference.zh.md) |

**Retrieval**: 用 reference 顶部索引选模型 → **只读对应小节**（定义/背景/原理/使用方法/适用条件/书中语）。勿通读 reference。

Keep **REDCAPE**, **SIR**, **Markov** in both languages.

## When to Apply

- Complex phenomenon (feedback, adaptation, emergence)
- Explain / predict / design / explore — not one-liner opinions
- Single-cause narrative dominates
- User mentions 模型思维, REDCAPE, 多模型, power-law, Markov, SIR, etc.

**Not primary**: trivial lookup; pure code; personal option choice already using WRAP.

**Vs WRAP**: Model Thinker = understand/design systems; WRAP = choose among options. Don't stack as competing primaries.

## Pre-Flight

### 1. REDCAPE（定一个主用途）

| Letter | Purpose |
|--------|---------|
| **R** Reason | Conditions & logical implications |
| **E** Explain | Testable mechanisms |
| **D** Design | Institutions, policies, rules |
| **C** Communicate | Shared frame |
| **A** Act | Policy / strategy guidance |
| **P** Predict | Forecast + uncertainty |
| **E** Explore | Counterfactuals |

Unclear → ask **one** question. R/E/C/Explore → simpler models; P/D/A → can be finer but still ensemble.

### 2. Information Gate

Critical unknowns (metric, time scale, adaptation, network vs mixed, stakes) → Gate only; no confident single-cause claim; no fabricated stats (`待核实` / `pending verification`).

### 3. Actor Stance（含人/组织时）

Fixed rule (low stakes) · Adaptive (feedback) · Rational (high stakes / mechanism design). Label per model if mixed.

## Workflow

Cap **2–5 models** (default **3**). Label: `applied` / `ruled out` / `pending data`.

### Step 1 — Phenomenon type

Map to **one primary type**; pick 2–5 models from the row (default 3). Framework entries（多模型思维、REDCAPE、多模型科学、人类行为者）见 Pre-Flight，不在此表重复。

| Type | Signals | Models（reference 索引名） |
|------|---------|---------------------------|
| Distribution / inequality | ranks, rich-get-richer, scale | 正态分布, 幂律分布, 优先连接 |
| Aggregation / effects | causes → outcomes, regression | 线性模型, 非线性模型 |
| Choice / positioning | products, candidates, attributes, pricing | 空间竞争, 享受竞争 |
| Spread | contagion, adoption, word-of-mouth | 广播模型, 扩散模型, 巴斯模型, SIR 模型 |
| Interaction structure | who connects, topology | 网络模型, 局部互动 |
| Dynamics / equilibrium | states, long-run, convergence | 马尔可夫模型, 随机游走, 路径依赖, 李雅普诺夫函数 |
| Feedback stocks | loops, delays, overshoot | 系统动力学, 阈值模型 |
| Strategic / institutions | payoffs interdependent, rules, contribution | 博弈论, 合作模型, 集体行动与公地, 机制设计, 信号模型, 价值与权力 |
| Search / learning | explore vs exploit, innovation | 学习模型, 多臂老虎机, 崎岖景观 |
| Uncertainty | surprise, information content | 熵 |

**Coverage**: 上表 29 个内容模型全覆盖；4 个框架基础在 Pre-Flight（REDCAPE / 行为者设定 / 多模型原则）。

### Step 2 — Select

Use reference **检索索引** + **常见问题 → 建议集成**（文末）:

1. Match primary REDCAPE
2. Enforce **diverse assumptions** (not near-duplicate partitions)
3. Read only selected reference sections

「Many」≈ **3–5**, not 50.

### Step 3 — Apply (per model)

- **Setup**: entities, variables, core assumption (1–2 lines)
- **Implication** · **Conditionality** · **Falsifier**
- Full mode: append **书中语** from reference (verbatim)

No textbook dump. No formulas unless they change the conclusion.

### Step 4 — Cross-check

Agreement · Tensions (which assumption?) · Blind spots

### Step 5 — Synthesize

Conditional claim · uncertainty · one next probe (if Act/Predict)

## Constraints

1. No single-equation explains complex social systems.
2. Conditionality over slogans.
3. One question per turn (≤3 if Gate).
4. Multi-turn → **Delta** only.
5. Final call stays with user.

## Modes

| Mode | When | Limit |
|------|------|-------|
| **Gate** | Purpose/structure unknown | ≤15 lines |
| **Lite** | Quick multi-lens | ≤35 lines |
| **Full** | Complex + enough context | ≤100 lines |
| **Delta** | Round 2+ | ≤40 lines |

### Gate

```markdown
## 问题框架
[一句]

## 待澄清
1. …

_确认前不做模型集成。_
```

### Lite

```markdown
## 问题框架
## REDCAPE
Primary: …

## 集成（2–3）
1. **[模型]**: 含义 · 失效条件
…

## 综合
```

### Full

```markdown
## 问题框架
## REDCAPE · 行为者设定 · 现象类型

## 集成
### 1. [模型]
- Setup · 书中语 · Implication · Conditionality · Falsifier

## 交叉检验
## 综合
```

### Delta

```markdown
## 问题框架（更新）
## 变化
## 更新集成
## 综合
```

## Examples

- 不平等未知机制 → Gate（独立加总 vs 优先连接？）
- 功能会否传播 → Lite：巴斯/SIR + 阈值 + 网络
- 政策议题 → Full：Act+Explain，读 reference 对应 3 节

## Additional Resources

- Full concept library: [reference.zh.md](reference.zh.md) · [reference.en.md](reference.en.md)
- Important personal option choice → [wrap-decision-making](../wrap-decision-making/SKILL.md)
- Strategic interdependence with others → [thinking-strategically](../thinking-strategically/SKILL.md)
- Time, finitude, or productivity overwhelm → [four-thousand-weeks](../four-thousand-weeks/SKILL.md)
