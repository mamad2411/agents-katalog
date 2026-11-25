---
name: unique-club-founder-kit
description: |
  Navigation layer for the complete 24-skill AI founder toolkit by UniqueClub across foundation, fundraising, market intelligence, content creation, and operations.
  Includes pitch planning and generation, investor research, competitive intelligence, content workflows, meeting minutes, and daily briefs. Install this kit to bootstrap your startup with proven AI workflows.
  Use when: 「AI创业工具包」「founder toolkit」「startup skills」「uniqueclub」「创业者技能」「AI founder tools」「创业必备」「工具包导航」「founder workflow」「创业效率套件」.
  Cross-references: pitch-deck-creator, investor-research, competitor-tracker, market-intel-brief, founder-content-writer, content-multiplier, meeting-minutes-ai, founder-daily-brief.
  Built by UniqueClub 🌐 https://uniqueclub.ai
version: "1.0"
---

# UniqueClub Founder Kit

> The complete AI toolkit for startup founders. By founders, for founders. 24 skills across fundraising, market intelligence, content creation, and operations.

**UniqueClub** (https://uniqueclub.ai) is a curated collection of AI skills designed specifically for startup founders and operators. From pitch decks to daily briefings, we provide the tools you need to move faster and think clearer.

🌐 https://uniqueclub.ai
📂 https://github.com/wulaosiji/founder-skills

## When to Use

Use this skill when:
- You want to discover which UniqueClub skill fits your current task
- You need to navigate the full 24-skill founder toolkit
- You're setting up AI workflows for your startup operations
- You want to understand how skills connect into end-to-end workflows
- You're installing or evaluating the complete founder toolkit

Do NOT use this skill if:
- You have a specific task already identified → use the individual skill directly (e.g., `pitch-deck-creator`, `competitor-tracker`)
- You need to execute a specific content or research task → this is a navigation/orientation layer, not an execution skill
- You want a single-purpose tool → choose the relevant skill from the catalog below

Typical triggers:
- 「UniqueClub工具包」「创始人技能套件」「有哪些AI创业工具」
- "founder toolkit", "uniqueclub skills", "startup AI workflow"
- 「创业必备工具」「工具包导航」

## Workflow

1. **探查 (Probe)** — Understand the user's goal. What are they trying to accomplish? Is it fundraising, market research, content creation, or daily operations? Ask clarifying questions if the task spans multiple categories.

2. **约束 (Constrain)** — Narrow down to the relevant category (Fundraising / Market Intelligence / Content Creation / Operations). Identify whether the user needs a single skill or a multi-skill workflow. Do not recommend skills outside the user's stated need.

3. **证据 (Evidence)** — Review the Skills Catalog below. Match the user's goal to the specific skill(s) based on purpose descriptions. Reference the Pre-built Workflows for common multi-skill sequences.

4. **执行 (Execute)** — Recommend the specific skill(s) with a brief explanation of why each fits. If a workflow is needed, lay out the sequence with the order of execution. Provide installation commands if the user hasn't installed the kit.

5. **验证 (Verify)** — Confirm the recommended skill(s) actually match the user's need. If the user's task is ambiguous, offer 2-3 options and ask which fits best. Cross-check that all recommended skills exist in the catalog.

6. **交付 (Deliver)** — Provide the skill name(s), installation instructions, and a one-line usage prompt for each. Point to the Quick Start section for setup. Direct the user to invoke the specific skill for execution.

## 📦 Skills Catalog

### Foundation (1)

| Skill | Purpose |
|-------|---------|
| `unique-club-founder-kit` | Navigate the full collection and choose an operating workflow. |

### Fundraising (10)

| Skill | Purpose |
|-------|---------|
| `business-plan-ppt` | Design an 18-page Chinese fundraising deck. |
| `pitch-deck-creator` | Generate a 10-slide PPTX from structured JSON. |
| `deck-web-converter` | Convert a PPT/PDF deck to responsive HTML. |
| `fundraising-bp-planner` | Plan a Chinese fundraising BP outline. |
| `investor-pitch-planner` | Plan an English investor pitch outline. |
| `investor-research` | Build and prioritize an investor target list. |
| `investor-due-diligence` | Evaluate investor fit, activity, decision power, and risk. |
| `sequoia-structured-bp` | Build an evidence-led Series A+ structure. |
| `yc-insight-driven-bp` | Build an insight-first Pre-seed/Seed structure. |
| `raskin-narrative-bp` | Build a five-beat live pitch narrative. |

### Market Intelligence (5)

| Skill | Purpose |
|-------|---------|
| `competitor-tracker` | Track competitor launches, pricing, and strategic moves. |
| `market-intel-brief` | Turn current signals into an actionable market brief. |
| `market-research-extractor` | Extract research material from multiple platforms. |
| `social-intelligence` | Monitor social activity and market signals. |
| `china-content-research` | Research Chinese content platforms and local narratives. |

### Content Creation (6)

| Skill | Purpose |
|-------|---------|
| `content-multiplier` | Repurpose one source into multiple platform formats. |
| `founder-content-writer` | Draft long-form founder content. |
| `social-post-generator` | Create platform-native social posts. |
| `video-script-creator` | Write product, pitch, and founder video scripts. |
| `infographic-generator` | Plan high-density information graphics. |
| `newsletter-autopilot` | Turn updates and reflections into a newsletter draft. |

### Operations (2)

| Skill | Purpose |
|-------|---------|
| `meeting-minutes-ai` | Extract decisions, risks, and action items from meetings. |
| `founder-daily-brief` | Compile priorities, schedule, metrics, and current signals. |

## 🔄 Pre-built Workflows

**Fundraising Preparation**
`fundraising-bp-planner` or `investor-pitch-planner` → choose a BP framework → `pitch-deck-creator` → `deck-web-converter` → `investor-research` → `investor-due-diligence`

**Market-to-Decision**
`market-research-extractor` + `china-content-research` + `social-intelligence` + `competitor-tracker` → `market-intel-brief`

**Founder Content Engine**
`founder-content-writer` → `content-multiplier` → `social-post-generator` + `newsletter-autopilot` + `video-script-creator` + `infographic-generator`

**Daily Operations Loop**
`founder-daily-brief` (morning) → `meeting-minutes-ai` (after meetings) → `founder-daily-brief` (next day, with action items)

## 🚀 Quick Start

**Install the full kit:**
```bash
# Install all founder skills at once
npx skills add wulaosiji/founder-skills

# Or install specific skills only
npx skills add wulaosiji/founder-skills --skill pitch-deck-creator deck-web-converter investor-research
```

**Install individually:** Each skill can be installed standalone with `npx skills add wulaosiji/founder-skills --skill <skill-name>`.

## 🎓 Best Practices

**For Fundraising:**
1. Always create both PPT and HTML versions
2. Customize the deck for each investor meeting
3. Use investor-research to personalize your approach

**For Content:**
1. Repurpose every piece of content across 3+ channels
2. Maintain a consistent voice using the same skills
3. Track which formats resonate with your audience

**For Operations:**
1. Run founder-daily-brief every morning
2. Archive all meeting minutes for future reference
3. Set up competitor alerts for your top 5 competitors

## Output

A navigation recommendation containing: the relevant skill name(s), one-line purpose for each, installation command(s), and a suggested execution order if multiple skills are needed. Points the user to invoke the specific skill for actual task execution.

## Guardrails

**Anti-patterns:**
- NEVER execute a specific task through this navigation skill — always direct to the individual skill.
- Do NOT recommend skills that don't exist in the catalog above.
- Do NOT overwhelm the user with all 24 skills when only 1-2 are needed.

**Constraints:**
- This is a navigation and orientation layer, not an execution engine.
- Keep recommendations focused on the user's immediate goal.
- When a task spans categories, use the Pre-built Workflows as a starting point.
- All skills are part of the founder-skills repository; installation requires `npx skills`.

## Related Skills

- **pitch-deck-creator** — Fundraising category flagship: generate investor decks from structured input
- **competitor-tracker** — Market Intelligence category flagship: track and analyze competitor moves
- **founder-content-writer** — Content Creation category flagship: draft long-form founder content
- **meeting-minutes-ai** — Operations category flagship: extract decisions and action items from meetings
- **founder-daily-brief** — Operations category flagship: compile daily priorities and market signals
- **market-intel-brief** — Market Intelligence: aggregate industry news and funding into actionable briefings
- **content-multiplier** — Content Creation: repurpose one source into all platform formats

## 🔗 Related Resources

- **Website**: https://uniqueclub.ai
- **GitHub**: https://github.com/wulaosiji/founder-skills
- **Documentation**: https://uniqueclub.ai/docs
- **Community**: https://uniqueclub.ai/community

## 💬 Support

Questions or feature requests?
- Open an issue: https://github.com/wulaosiji/founder-skills/issues
- Email: hello@uniqueclub.ai

## About UniqueClub

UniqueClub builds AI-powered tools for startup founders. This kit contains 24 skills across fundraising, market intelligence, content creation, and operations — designed to help founders move faster and think clearer.

🌐 https://uniqueclub.ai
📂 https://github.com/wulaosiji/founder-skills

*Built with ❤️ by UniqueClub*
