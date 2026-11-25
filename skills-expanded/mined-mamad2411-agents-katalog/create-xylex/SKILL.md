---
name: create-xylex-skill
description: >
  Scaffold a new XYLEX Group agent skill under skills/<name>/SKILL.md with the
  required YAML frontmatter (name, description, metadata.docs, path/bash/import
  triggers, retrieval). Use when the user wants to add a skill, write a SKILL.md,
  fix skill frontmatter, or runs /create-xylex-skill.
summary: Create a skills/*/SKILL.md with correct --- frontmatter
metadata:
  priority: 9
  docs:
    - "https://agentskills.io/specification"
    - "https://skills.sh/"
  pathPatterns:
    - "skills/**/SKILL.md"
    - "skills/**/overlay.yaml"
  bashPatterns:
    - '\bbun\s+run\s+validate\b'
    - '\bnpx\s+skills\s+add\b'
  importPatterns: []
  promptSignals:
    phrases:
      - "create a skill"
      - "new skill"
      - "SKILL.md"
      - "skill frontmatter"
      - "add a skill"
      - "create-xylex-skill"
    allOf:
      - [skill, frontmatter]
      - [skill, create]
      - [skills, SKILL]
    anyOf:
      - "skill"
      - "skills"
      - "agent skills"
    noneOf:
      - "vercel skill marketplace only"
    minScore: 5
retrieval:
  aliases:
    - skill scaffold
    - SKILL.md template
    - agent skill format
  intents:
    - create a new skill
    - fix skill frontmatter
    - document a skill for agents
  entities:
    - SKILL.md
    - frontmatter
    - pathPatterns
    - bashPatterns
    - retrieval
  examples:
    - add a skill for athena-js
    - scaffold skills/my-skill/SKILL.md
    - what frontmatter does a skill need
---

# Create an XYLEX Group skill

Every skill lives at `skills/<name>/SKILL.md` and **must** open with YAML frontmatter between `---` fences.

## Required shape

```markdown
---
name: <skill-name>
description: >
  What it does (1–2 sentences). Use when <triggers / keywords / slash command>.
summary: Short one-line summary for injection banners
metadata:
  priority: 5
  docs:
    - "https://example.com/docs"
  pathPatterns:
    - "path/glob/**"
  bashPatterns:
    - '\bcli-name\b'
  importPatterns:
    - "@scope/package"
  promptSignals:
    phrases:
      - "example phrase"
    minScore: 5
retrieval:
  aliases:
    - alternate name
  intents:
    - do the thing
  entities:
    - key concept
  examples:
    - user says this
---

# Title

Instructions for the agent…
```

## Rules

1. **`name`** must match the parent directory (`skills/<name>/`). Lowercase, digits, hyphens only.
2. **`description`** is required (Agent Skills + auto-invoke). Include “Use when …”.
3. **`metadata.docs`** must be a non-empty list of `https://` URLs.
4. Provide at least one of **`pathPatterns`**, **`bashPatterns`**, or **`importPatterns`** so hooks can match work.
5. Keep the body under ~500 lines; put deep docs in `references/`.
6. Register the skill in `xylex.md` with `⤳ skill: <name>`.
7. Run `bun run validate -- --coverage skip` before shipping.

## Directory layout

```
skills/<name>/
├── SKILL.md          # required
├── references/       # optional deep docs
├── scripts/          # optional helpers
└── overlay.yaml      # optional (build-skills merge)
```

## Checklist

- [ ] Frontmatter starts and ends with `---`
- [ ] `name` === directory name
- [ ] `description` has triggers
- [ ] `metadata.docs` has HTTPS URLs
- [ ] At least one path/bash/import pattern
- [ ] Linked from `xylex.md`
- [ ] `bun run validate -- --coverage skip` is clean
