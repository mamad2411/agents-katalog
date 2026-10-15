---
name: markdown-pipeline
description: Markdown and MDX pipelines with remark rehype - security performance and GFM parity
tags:
  - markdown
  - mdx
  - documentation
version: 1.0.0
category: development
outcomes:
  - Plugin stack list remark-gfm rehype-sanitize or equivalent decision
  - XSS and raw HTML policy stated for user content
  - Bundle size notes for heavy syntax highlighters
stack:
  - react-markdown
  - remark-gfm
  - next
last_reviewed: 2026-05-19
risk_level: low
tools_allowed: read-only
requires_user_approval: false
compatibility:
  - generic-markdown
  - skills-sh
  - cursor
  - claude-code
  - antigravity
  - codex
  - github-copilot
  - windsurf
  - gemini-cli
  - cline
  - amp
  - opencode
  - roo
  - goose
  - kilo
  - kiro-cli
  - droid
  - openclaw
  - trae
references:
  - references/skill-safety.md
---

# Instructions

## When to Use

- Use for MDX/Markdown sanitize + GFM pipelines.
- Prefer `content-creator` for social copy, not MDX plumbing.
- Prefer `skillcodex-browser-ui` for the doc browser shell.

Design a **markdown/MDX** rendering pipeline for **docs or blogs** in Next.js.

1. **User-generated content:** sanitize HTML; forbid raw `dangerouslySetInnerHTML` without allowlist.
2. **GFM:** tables, task lists, strikethrough via `remark-gfm`.
3. **Syntax highlight:** server vs client component for Shiki or prism - pick based on bundle budget.
4. **Links:** `rel` on external; heading slug plugin alignment with TOC.
5. **Images:** `next/image` in MDX wrapper components with dimensions.
## Outcomes

- Plugin list + security policy paragraph + component map.

## Output Rules

No unbounded HTML pass-through in examples.

## Scope and boundaries

- **In scope:** rendering stack, sanitization, MDX component whitelist.
- **Out of scope:** full CMS selection, search indexing backend.

## Safety

- Read-only; highlight XSS risks if user content is involved.

## Troubleshooting

- **Hydration on code blocks:** split highlighter to client leaf or use static HTML at build time.
- **MDX eval:** never suggest `eval` or arbitrary component mapping from URL params.

## Related skills

- [`content-creator`](../content-creator/SKILL.md) - copy before pipeline
- [`skillcodex-browser-ui`](../skillcodex-browser-ui/SKILL.md) - doc browser rendering
- [`secure-dependencies`](../secure-dependencies/SKILL.md) - sanitizer library risk

**GitHub:** https://github.com/bh611627/skillcodex/tree/main/skills/markdown-pipeline/SKILL.md  
**npm:** https://www.npmjs.com/package/@skillcodex/skills
