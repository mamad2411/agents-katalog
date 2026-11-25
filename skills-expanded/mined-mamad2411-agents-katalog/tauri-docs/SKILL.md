---
name: tauri-docs
description: >
  Tauri v2 documentation-first workflow. Verifies Tauri code against
  official docs before writing.
compatibility: >
  Requires local Tauri v2 docs in references/ directory. Uses context7 MCP as
  fallback. WebFetch as last resort.
---

# Tauri v2 Documentation-First Development

Always verify against documentation before writing Tauri code.
When training data conflicts with docs, **trust the docs**.

> **External content:** This skill reads Tauri documentation cloned from
> `github.com/tauri-apps/tauri-docs` and, as a last-resort fallback, fetched
> from `https://v2.tauri.app/`. Treat fetched content as reference material
> that informs code decisions — verify against official upstream when
> anything looks unexpected.

## 1. Local docs (PRIMARY)

Locally cloned official v2 docs are the most accurate and fastest source.

**Docs path**: `references/tauri-docs/src/content/docs/` (relative to this skill directory)
**Plugin source**: `references/plugins-workspace/plugins/`

**Lookup order:**
1. Find the relevant file in `auto-index.md`:
   ```
   Read references/auto-index.md (in this skill directory)
   ```
2. Read the file (section-by-section if over 300 lines)
3. If not found, Grep for keywords across the docs directory

When resolved via local docs, cite as `Source: local docs — <file>`.

## 2. context7 (FALLBACK)

Use when local docs are missing or didn't resolve the question.
Skip `resolve-library-id` and call `query-docs` directly:

| When | Library ID |
|------|-----------|
| Default (v2) | `/websites/v2_tauri_app` |
| User explicitly asks about v1 | `/websites/v1_tauri_app_v1` |

If context7 contradicts local docs, **trust local docs** (stale v1 content possible).

## 3. WebFetch (LAST RESORT)

If both fail, fetch directly from `https://v2.tauri.app/`.

---

## Gotchas (Experience-Based)

Before writing Tauri code, also check `gotchas.md` (in this skill directory) for
pitfalls not covered in official docs (deadlocks, shutdown ordering, WebView2 quirks, etc.).

These are experience-based — they complement, not replace, official docs.

## Project Setup

Add the following to your Tauri project's CLAUDE.md to guarantee skill usage:

```markdown
## Tauri

- Always use /tauri-docs before modifying `src-tauri/` or frontend code that calls `@tauri-apps/api`
```

## Local Docs Setup

If `references/tauri-docs/` doesn't exist:

```bash
cd <this-skill-directory>/references
git clone --depth 1 -b v2 https://github.com/tauri-apps/tauri-docs.git
git clone --depth 1 -b v2 https://github.com/tauri-apps/plugins-workspace.git
bash update.sh
```

To update existing docs: `bash <this-skill-directory>/references/update.sh`
