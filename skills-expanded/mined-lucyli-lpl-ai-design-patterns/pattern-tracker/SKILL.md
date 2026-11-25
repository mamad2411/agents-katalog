---
name: pattern-tracker
description: >
  AI 设计模式追踪库 — 按能力模式（而非公司）追踪 AI 产品设计趋势的活字典。
  ALWAYS use this skill when the user wants to: track/record/add an AI design pattern or capability trend,
  query what products implement a specific pattern, compare implementations of the same capability,
  update a pattern's status or evolution log, view the full pattern library,
  or says "设计模式", "能力模式", "追踪", "加到库里", "模式库", "pattern",
  "这个能力谁先做的", "对比一下XX和YY的实现方式", "design pattern".
  Also trigger when a product analysis (via ai-product-tasting) surfaces a reusable capability pattern
  worth tracking — prompt the user: "This looks like a trackable pattern. Add to the library?"
---

# AI Design Pattern Tracker
# AI 设计模式追踪库

A living catalog of AI product capability patterns, organized by **mode** (what the capability does), not by company. Each pattern tracks who originated it, which products implement it, how implementations differ, and how the pattern evolves over time.

This skill manages both **data** (markdown pattern files) and **presentation** (multiple output modes).

---

## Architecture

```
Data layer:     /patterns/*.md          — one file per pattern, structured markdown
Index:          /INDEX.md               — scannable overview of all patterns
Schema:         /DATA_SCHEMA.md         — field definitions and conventions
Presentation:   generated on demand     — HTML/React artifacts for visualization
```

Markdown is the **storage format**. Visualization is the **output format**. This skill manages both.

---

## Commands

The skill responds to these intent categories. Match by intent, not exact wording.

### 1. QUERY — Look up a pattern

**Triggers**: "录屏示教现在什么情况", "Teach-by-Demo 有哪些产品", "谁先做的 shared agent", "pattern status", "查一下XX模式"

**Action**:
1. Read the relevant `/patterns/<name>.md` file
2. Output depends on query specificity:
   - Status check → conversational card (inline, no file)
   - "Show me the full profile" → generate HTML visualization (see Output Mode 2)
   - Comparison request → generate comparison view (see Output Mode 4)

**Conversational card format** (for quick queries):

```
┌─────────────────────────────────────────┐
│ 📐 Teach-by-Demonstration / 录屏示教     │
│ Status: landed · Heat: ████░ 4/5        │
│ First seen: 2026-06 (Codex R&R)         │
│ Products: 3 (Codex · Grok Bot · SkillForge) │
│ Latest: Grok Bot price drop -70% (2026-08) │
│ Key tension: ease of creation vs robustness │
└─────────────────────────────────────────┘
```

Use Unicode box-drawing. Keep it scannable. Respond in the user's language.

### 2. ADD — Record a new pattern

**Triggers**: "把XX加到库里", "track this pattern", "新增模式", "这个能力值得追踪", "add pattern"

**Action**:
1. Confirm the pattern name — search for the community-recognized English term. If uncertain, propose 2-3 options and let the user pick.
2. Check if it already exists in the library (might be under a different name or as a related pattern).
3. Gather information via web search:
   - Who originated it? First productized instance.
   - What other products implement it?
   - What's the technical mechanism?
   - What are known limitations?
4. Generate the pattern file following DATA_SCHEMA.md structure.
5. Write to `/patterns/<pattern-name>.md`
6. Update `/INDEX.md`
7. Show a confirmation card + offer to generate the full visualization.

**Critical**: Always web search before writing. Don't rely on training data for product details — AI products change weekly.

### 3. UPDATE — Modify an existing pattern

**Triggers**: "更新XX", "XX有新动态", "status变了", "加个产品实例", "update pattern", "新增一个实现"

**Action**:
1. Read the existing pattern file.
2. Determine what changed:
   - New product implementation → add to Comparison Matrix + new Detail Card
   - Status change → update frontmatter + add Evolution Log entry (with driver type)
   - New PM insight → append to PM Notes
   - Factual correction → edit in place
3. Write updated file.
4. If status changed, update INDEX.md.
5. Show a diff summary of what changed.

**Evolution Log discipline**: Every status change MUST include:
- Date
- What happened
- Driver type: `product-design` | `ux` | `tech` | `market` | `academic`
- Why it matters

### 4. BROWSE — View the full library

**Triggers**: "给我看整个库", "所有模式", "library overview", "模式库总览", "show all patterns"

**Action**: Generate an interactive React artifact (Output Mode 3).

### 5. COMPARE — Side-by-side pattern or implementation comparison

**Triggers**: "对比XX和YY", "compare implementations", "这两个模式有什么关系", "XX和YY的区别"

**Two sub-types**:
- **Cross-pattern**: Compare two different patterns (e.g., Teach-by-Demo vs Computer Use)
- **Cross-implementation**: Compare products within the same pattern (e.g., Codex R&R vs Grok Bot Teach a Task)

**Action**: Generate a comparison HTML artifact (Output Mode 4).

### 6. VISUALIZE — Render a pattern visually

**Triggers**: "可视化", "visualize", "给我看XX的档案", "show me the full profile", "生成一个好看的版本"

**Action**: Generate HTML visualization artifact for the specified pattern or the full library.

---

## Output Modes

### Mode 1: Conversational Card (inline)
- For quick status checks and simple queries
- Unicode box-drawing, no file generated
- Respond in the user's language
- Keep it to 5-8 lines max

### Mode 2: Pattern Profile (HTML artifact)
- For "show me the full profile of XX"
- Single-pattern deep view
- Sections: header with status badge → one-liner → mechanism diagram → implementation comparison cards → evolution timeline → PM notes
- Design direction: clean, editorial, magazine-layout feel. Dark status badges. Timeline as a vertical line with nodes. Product cards side-by-side. Use the pattern's heat level to set visual intensity.
- Create as `.html` file in `/mnt/user-data/outputs/`

### Mode 3: Library Dashboard (React artifact)
- For "show me the whole library"
- Interactive: filter by status, heat, tags
- Each pattern as a card showing: name (EN/CN), status badge, heat bar, product count, one-liner
- Click to expand shows: implementation list, latest evolution event, related patterns
- Create as `.jsx` file in `/mnt/user-data/outputs/`

### Mode 4: Comparison View (HTML artifact)
- For "compare XX and YY"
- Two-column or multi-column layout
- Dimension-by-dimension comparison with visual diff highlighting
- Shared traits centered, differences on each side
- Create as `.html` file in `/mnt/user-data/outputs/`

### Mode 5: Trend Map (React artifact)
- For "show me trends" or "what's hot right now"
- Bubble chart or grid: x = first_seen date, y = heat, size = product count, color = status
- Hover shows pattern summary
- Create as `.jsx` file in `/mnt/user-data/outputs/`

---

## Data Conventions

Follow DATA_SCHEMA.md strictly. Key rules:

### Pattern naming
- `pattern_name`: Community-recognized English term. Search for what practitioners actually call it.
- `chinese_name`: 2-4 character Chinese shorthand you'd use in conversation.
- File name: lowercase hyphenated English (`teach-by-demonstration.md`)

### Status values
| Status | Meaning |
|--------|---------|
| `concept` | Research/demo only, no shipped product. Note what's blocking it. |
| `landed` | At least one product shipped to real users. |
| `evolving` | Shipped AND actively iterating. Track driver type. |
| `converging` | Multiple products converged on similar approaches. |

### Visual references
- Store URLs only, never embedded images
- Prefer: official product pages, documentation, demo videos, community walkthroughs
- Format: `[description](URL)`

### Cross-references
- Between patterns: use `related_patterns` in frontmatter
- Between this skill and ai-product-tasting: when a tasting surfaces a pattern, link back. "See [Claude Tag tasting](link) for the deep dive that identified this pattern."

---

## Integration with ai-product-tasting

When running an ai-product-tasting analysis (Phase 5.2 — Design Pattern Library), check:
1. Does this product implement any patterns already in the tracker?
2. Does it reveal a NEW pattern worth tracking?

If yes to either, prompt the user:
- "This product uses [pattern name] — want me to update the tracker with this implementation?"
- "I spotted a new capability pattern: [description]. Track it?"

This creates a natural feedback loop: tastings feed the pattern library, and the pattern library enriches future tastings.

---

## Bilingual Behavior / 语言规则

- Respond in whatever language the user is speaking
- **Pattern file body text is written in Chinese** (正文中文). Structure stays bilingual so parsers and readers can key on it:
  - Section headings keep the `## Definition / 定义` / `### How It Works / 运作机制` bilingual form exactly as in DATA_SCHEMA.md
  - Bullet labels keep the bilingual form: `- **Input / 输入**:`, `- **Platform / 平台**:`
  - Comparison Matrix dimension labels keep the bilingual form: `| Vendor / 厂商 |`
  - One-liner keeps BOTH lines: English quote first, Chinese quote second
- Keep in English: `pattern_name`, product names, vendor names, driver types (`product-design` etc.), benchmark names, URLs, technical terms without a settled Chinese equivalent (skill, agent, MCP, tool calling)
- Evolution Log lines keep the machine-readable prefix `- **YYYY-MM** [driver] ` followed by Chinese text
- Visualizations show both `pattern_name` and `chinese_name`
- Search/query works in both languages: "录屏示教" matches "Teach-by-Demonstration"

---

## Quality Checklist

Before writing or updating any pattern file:

- [ ] Body text is Chinese; headings, bullet labels and matrix dimensions keep the bilingual form (see Bilingual Behavior)
- [ ] Pattern name is the community-recognized term (not invented)
- [ ] At least one web search performed for current product status
- [ ] Status accurately reflects landing progress
- [ ] Every status change has an Evolution Log entry with driver type
- [ ] Comparison Matrix covers all known implementations
- [ ] Each Detail Card has an official link
- [ ] PM Notes contain at least one design insight and one tension
- [ ] Related patterns are cross-linked
- [ ] INDEX.md is updated

---

## Example Interactions

**Quick query:**
```
User: 录屏示教现在什么状态？
Skill: [reads pattern file, outputs conversational card]
```

**Add new pattern:**
```
User: 把 Shared Agent 也加到库里
Skill: [web searches for shared agent products] →
       [generates pattern file] →
       [updates INDEX.md] →
       [shows confirmation card] →
       "Added. Want to see the full visualization?"
```

**Cross-skill flow:**
```
User: 深度品鉴 Claude Tag
Skill (ai-product-tasting): [runs 5-phase analysis] →
  Phase 5.2: "Claude Tag uses two trackable patterns:
  Shared-Agent and Ambient-Mode. Add to the pattern library?"
User: 加
Skill (pattern-tracker): [creates/updates pattern files]
```

**Visualization:**
```
User: 给我看 Teach-by-Demo 的完整档案
Skill: [reads pattern file] → [generates HTML artifact with
       status header, mechanism diagram, product cards,
       timeline, PM notes] → [presents file]
```
