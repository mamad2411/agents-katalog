---
name: holographic-memory-migration
description: "Migrate content from built-in memory (memory tool) and user_profile into Holographic Memory (fact_store). Batch-adds structured facts with categories and tags for queryable long-term storage. Run after initial setup, profile changes, or on user request."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [memory, holographic, fact-store, migration, workflow]
    related_skills: [hermes-agent]
---

# Holographic Memory Migration

## Overview

Hermes has two memory systems:
1. **Built-in memory** — always-injected via `memory` tool, saved in `~/.hermes/memory/`. Compact, always-on, limited char budget.
2. **Holographic Memory (fact_store)** — structured fact database with categories, tags, trust scores, and algebraic query (probe/search/reason/contradict). Deep recall, not always-on.

This workflow migrates relevant content from memory (+ user_profile) into fact_store, and optionally cleans up duplicated entries.

## When to Use

- User says "holographic 可以用了吗" or asks to store everything known
- After initial setup with a new user
- When user changes important preferences/contact/project info
- When user says "把这些都存了" or "存进去"
- Periodically to keep fact_store in sync with learned knowledge

## Workflow

### Step 1: Read current memory and user profile

```
memory(action='list', target='memory')
memory(action='list', target='user')
```

Note: the memory tool's `list` action shows all current entries.

### Step 2: Classify each fact into fact_store categories

| Category | When to use |
|----------|-------------|
| `user_pref` | Communication style, UI preferences, workflow habits, personal rules, contact info |
| `project` | Project paths, tech stack, architecture decisions, business rules |
| `tool` | Environment quirks (macOS, Docker, Git), CLI settings, tool-specific workarounds |
| `general` | Background info (education, math/domain expertise), miscellaneous |

### Step 3: Tags

Use short comma-separated tags for searchability. Examples: `identity, contact, git, docker, macos, java, frontend, email, workflow, documentation`

### Step 4: Batch-add via fact_store

Call `fact_store(action='add', ...)` for each fact. Batch multiple independent adds in parallel (one tool call per fact).

Key principles:
- One fact = one atomic statement. Don't combine unrelated info.
- Prefer declarative statements over imperative instructions.
- Remove stale memory entries after migration (use `memory(action='remove', ...)` in the same turn as verification).

### Step 5: Verify

```
fact_store(action='search', query='<key term>')
```

Probe a couple of key facts to confirm storage. Then optionally clean up duplicate entries in built-in memory to free char budget.

### Step 6: Save as workflow (optional)

If user says "把流程记下来" or "形成工作流", create this skill.

## Common Pitfalls

1. **Over-stuffing entries** — each fact_store entry should be one coherent statement. Split compound facts.
2. **Wrong category** — `user_pref` for preferences/who they are, `tool` for environment quirks, `project` for project-specific.
3. **Missing tags** — tags make search work. Always add at least 1-2 relevant tags.
4. **Forgetting to dedupe** — after migration, trim the built-in memory of entries that are now in fact_store, to free char budget for future session memory.
5. **Imperative phrasing** — write facts as declarative statements ("User prefers X"), not instructions ("Always do X").
6. **Pinyin reversal** — Chinese multi-character company names in pinyin transpose easily (多和美 → duohemei, not heduomei). Read the Chinese characters aloud to verify order when creating directory names from pinyin.
7. **Chinese context naming** — in Chinese-language documents, use descriptive Chinese filenames for references ("营业执照副本", "私募基金管理人公示信息") rather than English-prefix names ("01-business-license"). English prefixes are for internal sorting only, not display. Use en-dash (U+2013) between number prefix and Chinese name.
8. **Evidence package numbering** — when organizing DD materials by numbered conditions (基础池 01-05, 备选池 06-08), use hierarchical numbering: `X-Y-Z–ChineseName.ext`. Single-condition files: `X–Name.pdf`. Multi-item: `X-Y–Name.pdf`. Sub-items: `X-Y-Z–Name.pdf`. The 0 prefix (e.g. `0–申请表.docx`) sorts first.

## Verification Checklist

- [ ] All key facts from memory are present in fact_store
- [ ] Categories are correct (user_pref/project/tool/general)
- [ ] Tags are set for searchability
- [ ] Built-in memory is trimmed of duplicated entries
- [ ] User confirms holographic memory is active and populated
