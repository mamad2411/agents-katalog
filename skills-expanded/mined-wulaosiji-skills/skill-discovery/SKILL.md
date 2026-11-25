---
name: skill-discovery
description: |
  Discover, load, and apply the right skill for any task — scanning installed skill registries,
  matching by keyword and intent, reading SKILL.md, and following its workflow. Use when:
  "找技能", "加载skill", "skill发现", "skill discovery", "匹配技能", "应该用哪个skill",
  "skill matching", "动态加载技能", "技能路由", "skill registry". Ensures no task is done
  manually when a proven skill exists. Part of the UniqueSkills platform toolkit.
---
# Skill Discovery
> Find the right skill, read it, follow it — never reinvent a workflow that's already packaged.

## When to Use
Use this skill when:
- You're about to start a task and want to check if a **matching skill** already exists
- The user mentions a **domain or tool** that likely has a dedicated skill (Excel, PPT, Feishu, PDF, images, video, etc.)
- A **must-match domain** is involved: spreadsheets, slides, documents, Feishu, image generation, data visualization, app building
- You need to **compare multiple candidate skills** and pick the best fit
- A skill was referenced by name but you haven't read its `SKILL.md` yet

Do NOT use this skill if:
- The task is clearly trivial and no skill could add value
- You've already loaded the relevant skill in this conversation
- The user explicitly says not to use skills

Typical triggers:
- 「有没有相关的skill」「该用哪个技能」「帮我找一下处理XX的skill」
- "is there a skill for...", "which skill should I use", "load the skill for..."
- 「按照skill来做」「用专业技能处理」

## Workflow

### Step 1: 探查 — Scan Registries
- Identify all skill root directories available in the environment
- Scan every `SKILL.md` across roots in one pass (recursive glob, not directory-by-directory)
- Extract each skill's `name` and `description` frontmatter for matching

### Step 2: 约束 — Define Matching Criteria
- Map the user's request to core domain terms, synonyms, and both Chinese and English expressions
- For must-match domains (sheet, ppt, doc, Feishu, image, visualization, app), treat a match as mandatory, not optional
- Prefer skills whose description contains explicit "Use when:" triggers that overlap with the request

### Step 3: 证据 — Read Candidates
- For each candidate skill, `Read` its full `SKILL.md` — never act on the description alone
- Confirm the skill's scope matches the task; check its "Do NOT use" section for exclusions
- If multiple skills overlap, pick the most specific one; note the others as related

### Step 4: 执行 — Apply the Skill
- Follow the skill's Workflow section step by step
- Use its scripts, templates, and assets from the same directory
- If the skill references other skills, load those too (chain loading)

### Step 5: 验证 — Confirm Fit
- After execution, check whether the skill's output constraints were met
- If the skill was a poor fit, record why and consider suggesting a new or improved skill
- Verify any generated artifact matches the skill's specified output format

### Step 6: 交付 — Report and Persist
- State which skill was used and why
- If no skill matched, say so explicitly and proceed with base tools
- Persist useful skill-to-task mappings to memory for faster routing next time

## Output
- **Matched skill**: name and one-line reason
- **Skills considered**: list of candidates with fit assessment
- **Execution note**: whether the skill was applied, and any deviations from its workflow
- **Gap note** (optional): if no skill matched, what capability is missing

## Guardrails
- **Always read `SKILL.md` before using a skill** — the description alone is not enough
- **A skill name is not a callable tool** — never put it as a function name in a tool call
- **Must-match domains are mandatory**: Excel/CSV → sheet skill, PPT → ppt skill, Feishu docs → lark-doc skill, etc.
- **Never run a skill without reading it first**, even if you've used similar skills before
- **If a skill fails**, read the error, adjust inputs, and retry; only fall back to base tools after two failures
- **Don't substitute a generic web search** for skill discovery when a matching skill exists

## Related Skills
- **agent-orchestrator** — Delegate skill-driven work to sub-agents
- **tool-router** — After skill selection, route to the right underlying tools
- **memory-manager** — Remember which skills work well for which task types
- **enterprise-knowledge** — Search internal skill documentation and usage patterns

## About
Part of the UniqueSkills platform toolkit — capabilities extracted from the Doubao agent runtime.
🌐 https://uniqueclub.ai | 📂 https://github.com/wulaosiji/skills
