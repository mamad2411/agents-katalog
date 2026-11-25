---
name: skill-frontmatter-gray-matter
description: Store Claude-style Agent Skills as SKILL.md with YAML frontmatter (name, description, icon, requiredSources) parsed with gray-matter and a normalization pass that accepts both string and array values.
category: agent-sdk
version: 1.0.0
version_origin: extracted
tags: [skills, frontmatter, gray-matter, yaml]
confidence: medium
source_type: extracted-from-git
source_url: https://github.com/lukilabs/craft-agents-oss.git
source_ref: main
source_commit: 61f7d48a5b4fd0a8094f002c9e3aea5f3824dcfb
source_project: craft-agents-oss
source_path: packages/shared/src/skills/storage.ts
imported_at: 2026-04-18T00:00:00Z
---

# Skill frontmatter + gray-matter parse

## When to use
- App that lets users define agent skills (snippets of reusable instructions) as Markdown files.
- Need a tiny metadata header (name, description, maybe icon / required sources) without adopting a heavyweight schema.
- Want it readable/editable in any text editor.

## How it works
1. Each skill is a directory with a `SKILL.md`:
   ```
   skills/
     build-release-notes/
       SKILL.md
       scripts/helper.py  (optional resources)
   ```
2. `SKILL.md` starts with a YAML frontmatter block:
   ```yaml
   ---
   name: build-release-notes
   description: Generate release notes from git log
   icon: 📝
   requiredSources: [github]
   ---
   ```
3. Parse with [`gray-matter`](https://www.npmjs.com/package/gray-matter):
   ```ts
   import matter from 'gray-matter';
   const { data, content } = matter(fileContent);
   ```
4. Validate required fields (`name`, `description`) - return `null` rather than throw so the loader can skip malformed skills without breaking the UI.
5. Normalize flexible fields - `requiredSources` may be a string OR array; coerce to deduped array:
   ```ts
   const normalized = typeof v === 'string' ? [v] : Array.isArray(v) ? v : [];
   ```
6. Validate the icon field (emoji or URL only, reject inline SVG and relative paths) to keep skill rendering safe.
7. Global vs project skills: look in both `~/.agents/skills/` (global) and `<workspace>/.agents/skills/` (project), merge with workspace precedence.

## Example
```ts
import matter from 'gray-matter';

function parseSkillFile(content: string) {
  const parsed = matter(content);
  if (!parsed.data.name || !parsed.data.description) return null;
  return {
    metadata: {
      name: String(parsed.data.name),
      description: String(parsed.data.description),
      icon: validateIconValue(parsed.data.icon),
      requiredSources: normalizeRequiredSources(parsed.data.requiredSources),
    },
    body: parsed.content.trim(),
  };
}
```

## Gotchas
- `gray-matter` caches by filename by default; pass `{ bustCache: true }` if you re-read during hot-reload, or disable caching when developing.
- Don't trust user-supplied `icon` - validate emoji / URL explicitly; inline SVG opens XSS if rendered naively.
- YAML booleans (`yes`, `no`, `on`, `off`) can accidentally coerce `name: on` -> `true`. Always cast to `String(data.name)`.
- Keep the set of accepted frontmatter fields stable and versioned - adding one is easy, renaming is data migration.
