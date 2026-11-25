---
name: resume-bullet-from-workflow
description: Distill multi-step processes into one resume bullet.
version: 0.1.0
author: Hermes
---

# Writing Resume Bullets from Workflow Descriptions

When the user describes a multi-step process (daily ritual, quarterly cycle, research pipeline), distill it into a single concise resume bullet that captures the core deliverable, not the intermediate steps.

## When to Use

- User says "我做市场分析并在每天进行汇报" (I do market analysis and report daily)
- User describes a workflow with 3+ steps and asks "写成简历的一句话"
- User explains their actual day-to-day process and needs it compressed

## Procedure

### Step 1 — Extract the Skeleton

From the narrative, identify:

| Signal | Question |
|--------|----------|
| Core deliverable | What gets produced/presented/decided? Not the intermediate data-fetching. |
| Cadence | Daily? Quarterly? One-off ad hoc? Drives verb choice. |
| Input sources | What data, tools, or documents feed in? (markets, valuation sheets, compliance docs) |
| Audience | Who consumes it? (IC, PMs, morning meeting) |

### Step 2 — Filter Out

These do NOT belong in the bullet:
- Data collection mechanics (who cares that you used Python? Unless it's the headline)
- Unnecessary sub-steps between input and output
- "我负责" / "Responsible for" / "帮我..."

### Step 3 — Write the First Draft

Formula: `[Action Verb] [Scope] [Cadence] [Deliverable] [Audience if relevant]`

Action verb options:
- Daily routines: `Delivered`, `Produced`, `Provided`
- Research: `Conducted`, `Analyzed`, `Evaluated`, `Researched`
- Management: `Orchestrated`, `Managed`, `Led`, `Oversaw`

### Step 4 — Apply Style Rules (EN)

Run through resume-content-writer rules:
1. Past-tense active verb? ✅
2. No a/an/the? ✅ (keep proper nouns: "the S&P 500")
3. No passive voice? ✅
4. No gerunds? (`covering X` → `on X`)
5. No filler? (`various`, `several`, `multiple`)

### Step 5 — Compress (ZH)

For Chinese bullets, strip:
- `采集数据开展分析` → just `分析` (the action implies inputs)
- `负责` `进行` `通过` `使用` `完成` (weak verbs)
- `各种` `多项` `大量` (filler quantifiers)

## Examples

### Workflow → Bullet (from this session)

**User described:** 每天8:00采集行情数据→分析板块资金流向→识别事件催化→复盘→8:30晨会汇报→映射到FoF持仓→负面舆情筛查

**ZH distilled:**
`每日复盘市场行情，覆盖指数涨跌、板块资金流向及事件催化，为8:30晨会投后持仓分析提供依据`

**EN distilled:**
`Delivered daily market intelligence briefings on index movements, sector capital flows, event catalysts, and FoF portfolio mapping for 8:30 AM investment meetings`

### Interview Technique

When the user's description is vague, ask:
- "这个工作每天/每周/每季度做一次？"
- "做完之后产出是什么？给谁看？"
- "输入的数据从哪来？"
