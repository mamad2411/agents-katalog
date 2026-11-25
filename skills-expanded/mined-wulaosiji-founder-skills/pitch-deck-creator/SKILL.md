---
name: pitch-deck-creator
description: |
  从结构化JSON生成可编辑的10页创业公司融资Pitch Deck PPTX文件。覆盖问题、方案、商业模式、产品、竞争、 traction、路线图、团队和融资需求，支持中英文内容。
  Use when: "生成pitch deck", "融资PPT", "BP生成", "pitch deck PPTX", "startup deck generator", "10页融资 deck", "投资人演示文稿", "fundraising deck".
  这是BP系列中的可执行选项：产出PPTX而非仅大纲或写作框架。Cross-references: deck-web-converter, fundraising-bp-planner, business-plan-ppt.
  Built by UniqueClub 🌐 https://uniqueclub.ai
license: MIT
---

# Pitch Deck Creator

> 从结构化创业公司数据生成一致的10页融资deck。这是BP系列中的可执行选项：产出PPTX而非仅大纲或写作框架。

## When to Use

Use this skill when:
- 用户已有公司信息，需要生成可编辑的PPTX文件
- 用户需要标准10页结构的融资deck（问题→方案→商业模式→产品→竞争→traction→路线图→团队→融资）
- 用户需要中英文内容的pitch deck

Do NOT use this skill if:
- 用户还在梳理故事/内容框架 → 先用 `fundraising-bp-planner`（中文大纲）或 `investor-pitch-planner`（英文大纲）
- 用户需要特定叙事框架 → use `sequoia-structured-bp`、`yc-insight-driven-bp` 或 `raskin-narrative-bp`
- 用户需要18页中国风格内容和视觉规范 → use `business-plan-ppt`
- 用户需要将已有PPT转为网页 → use `deck-web-converter`

Typical triggers:
- 「帮我生成融资PPT」「做个pitch deck」「BP PPTX」
- "generate pitch deck", "startup deck PPTX", "fundraising presentation"

## Bundled Implementation

- Script: `scripts/generate_pitch_deck.py`
- Dependency: `python-pptx>=0.6.21` from `requirements.txt`
- Input: UTF-8 JSON
- Output: editable 16:9 PPTX
- Default filename: `{project_name}_BP.pptx`

The bundled script does not export PDF. Convert the generated PPTX separately when the user explicitly needs PDF or web delivery.

The two files under `references/` document the legacy 18-page reference style. They are not the output contract of this 10-slide generator; use `business-plan-ppt` when that longer structure is the actual requirement.

## Input Expectations

Collect or extract these JSON fields:

- `project_name`, `tagline`, and up to three `value_props`
- `pain_points` and `market_size` (`tam`, `sam`, `som`)
- `solution.features` and `solution.differentiation`
- `business_model.revenue_streams` and `business_model.pricing`
- `product_status`, `competitors`, `traction`, and `roadmap`
- `team` and `fundraising`
- `language`: `zh` or `en`
- Optional `colors`: `primary`, `dark`, and `accent`

Do not invent traction, market size, customer evidence, team credentials, or fundraising terms. Leave unknown values empty or mark them for confirmation before generation.

## Workflow

本工作流遵循六步推进法，共6个步骤：
1. **探查 (Probe)**：动手前先完整读取全部输入，确认目标和约束。
2. **约束 (Constrain)**：验证输入完整性，设定边界和不可降级的交付标准，受阻时换通道。
3. **证据 (Evidence)**：每个数字必须来自输入、具体信源或可复现计算，收集支撑数据。
4. **执行 (Execute)**：调用脚本/API/生成内容，先给影响与结论，再给行动和必要证据。
5. **验证 (Verify)**：用"可能失败"的动作验证——不同于生成路径的方式回读输出。
6. **交付 (Deliver)**：返回结果，清理临时文件。

### Step 1: 探查 (Probe)
完整读取用户提供的公司信息，提取全部JSON字段，列出缺失的决策关键字段。

### Step 2: 约束 (Constrain)
验证输入完整性，确认每个将出现在deck中的事实声明。未知值留空或标注待确认，不编造。设定输出为16:9 PPTX、固定10页结构，不降级交付物。

### Step 3: 证据 (Evidence)
每个数字必须来自输入、具体信源或可复现计算。traction、市场规模、客户证据、团队背景、融资条款均需可追溯，不将假设呈现为已验证事实。

### Step 4: 执行 (Execute)
1. 使用 `README.md` 中的schema创建UTF-8 JSON输入文件。
2. 需要时安装本地依赖：`python3 -m pip install -r requirements.txt`
3. 运行：
   ```bash
   python3 scripts/generate_pitch_deck.py --input startup.json --output Company_BP.pptx
   ```
4. 先给影响与结论，再给行动和必要证据。

### Step 5: 验证 (Verify)
用不同于生成路径的方式回读输出：
- 打开PPTX检查文字溢出、缺失字段、对比度和事实准确性
- 确认生成文件恰好包含10页幻灯片
- 保持16:9尺寸和选定的颜色token一致
- 将生成的布局视为初稿：手动检查溢出和稀疏页面
- 对外分享前替换空占位符

### Step 6: 交付 (Deliver)
返回PPTX文件路径，清理临时文件。如需PDF或网页交付，分别转换或使用 `deck-web-converter`。修改JSON并重新生成，而非手动修补重复内容。

## Output

### Fixed 10-Slide Output

| # | Slide | Primary input |
|---|-------|---------------|
| 1 | Cover | `project_name`, `tagline`, `value_props` |
| 2 | Market Pain Points | `pain_points`, `market_size` |
| 3 | Solution | `solution` |
| 4 | Business Model | `business_model` |
| 5 | Product Demo | `product_status` |
| 6 | Competitive Analysis | `competitors` |
| 7 | Traction | `traction` |
| 8 | Roadmap | `roadmap` |
| 9 | Team | `team` |
| 10 | Fundraising | `fundraising` |

### Output Standards

- 确认生成文件恰好包含10页幻灯片
- 保持16:9尺寸和选定的颜色token一致
- 将生成的布局视为初稿：手动检查溢出和稀疏页面
- 对外分享前替换空占位符
- 保持源数据和声明可追溯；绝不将假设呈现为已验证事实

## Guardrails

**Anti-patterns**
- NEVER 编造traction、市场规模、客户证据、团队背景或融资条款
- Do NOT 将假设呈现为已验证事实
- Do NOT 手动修补重复内容——修改JSON并重新生成
- NEVER 对外分享包含空占位符的deck
- Do NOT 期望脚本导出PDF——需单独转换

**Constraints**
- 输出固定为10页16:9 PPTX，不增减页数
- 输入必须为UTF-8 JSON，遵循 `README.md` 中的schema
- 依赖 `python-pptx>=0.6.21`，需时安装
- 未知值留空或标注待确认，不降级交付物
- `references/` 下的文件是18页遗留风格参考，不是本10页生成器的输出契约

## Related Skills

- **deck-web-converter** — 将生成的PPTX转为可分享的网页HTML，完成从创建到分享的完整工作流
- **fundraising-bp-planner** — 在生成PPTX前先梳理中文融资BP大纲（六大模块+数据呈现建议）
- **business-plan-ppt** — 如需18页中国风格内容和视觉规范，使用此技能

## About UniqueClub

Part of the UniqueClub toolkit.
🌐 https://uniqueclub.ai
