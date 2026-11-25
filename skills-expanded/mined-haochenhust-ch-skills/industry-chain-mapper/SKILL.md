---
name: industry-chain-mapper
description: "This skill should be used when the user asks to '梳理一下XX产业链', '这个行业的上下游是什么', '哪个环节弹性最大', or when starting research on a new industry theme. Builds and maintains persistent industry-chain maps (upstream/midstream/downstream, key companies, market share, investment-elasticity ranking). Artifact-focused; complements the process-focused industry-chain-research skill."
version: 1.0.0
---

# Industry Chain Mapper

Build structured industry chain maps for investment research. Maps are persistent files that get updated over time, not rebuilt from scratch. (For the step-by-step research process/methodology, see the `industry-chain-research` skill; this skill focuses on producing and maintaining the map artifact.)

## When to Use

- Starting research on a new industry chain
- Updating an existing chain map with new information
- Comparing companies within a chain to find the best investment target

## Workflow

### Step 1: Check Existing Maps

```bash
ls industry-chain-*.md
```

If a map already exists for this chain, READ it first and UPDATE rather than rebuild.

### Step 2: Research the Chain

For a new chain, gather information via:
1. **WebSearch**: "{industry} 产业链 上游 中游 下游 2026"
2. **WebSearch**: "{industry} 产业链 龙头公司 市占率"
3. **WebSearch**: "{industry} 产业链图谱 研报"
4. **Articles/reports** the user has provided
5. **Financials** for key companies (via the `financial-data-fetcher` / `tushare-data` skills)

### Step 3: Build/Update the Map

Save to `industry-chain-{name}.md` in your research notes directory.

## Map Template

```markdown
# {Industry Name} 产业链图谱

> 创建日期：{date}
> 最后更新：{date}
> 置信度：{X}%

## 产业链概览

{1-2 sentence description of the industry chain and why it matters for investment}

## 产业链结构

### 上游 — {upstream category name}
| 环节 | 代表公司 | 市占率/地位 | A股标的 | 投资弹性 |
|------|----------|-------------|---------|----------|
| {sub-segment} | {companies} | {share/position} | {stock code} | {high/medium/low} |

### 中游 — {midstream category name}
| 环节 | 代表公司 | 市占率/地位 | A股标的 | 投资弹性 |
|------|----------|-------------|---------|----------|
| {sub-segment} | {companies} | {share/position} | {stock code} | {high/medium/low} |

### 下游 — {downstream category name}
| 环节 | 代表公司 | 市占率/地位 | A股标的 | 投资弹性 |
|------|----------|-------------|---------|----------|
| {sub-segment} | {companies} | {share/position} | {stock code} | {high/medium/low} |

## 弹性排序

按投资弹性从大到小排列（结合市占率变化潜力、估值空间、催化剂）：

1. **{company}({code})** — {why highest elasticity}
2. **{company}({code})** — {reason}
3. ...

## 关键变量

影响这条产业链投资价值的核心变量：
1. {variable 1}: {current status} → {what to watch}
2. {variable 2}: {current status} → {what to watch}

## 产业链传导逻辑

{How does a change at one level propagate through the chain?}
{Which segment benefits most/least from a demand increase?}

## 更新日志

- {date}: {what was updated and why}
```

## Rules

1. **Maps are living documents** — update, don't rebuild
2. **Every company must have a stock code** if it's A-share listed
3. **Elasticity ranking must have logic** — not just "this one is big so it's good"
4. **Mark uncertainty** — if market-share data is estimated or from a single source, say so
5. **Link back to your research notes** — after creating/updating a map, update the corresponding track in your notes
