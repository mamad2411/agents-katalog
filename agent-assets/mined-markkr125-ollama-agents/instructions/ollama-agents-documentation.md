---
applyTo: "docs/**,README.md"
description: "Rules for creating and updating user-facing documentation. Keeps docs accurate, in sync with code, and free of fluff."
---

# Documentation Maintenance Rules

> **⚠️ Structural rules**: Do NOT rename, move, or delete files in `docs/`, `.github/instructions/`, or `.github/skills/` without updating all cross-references. Run `npm run lint:docs` to verify. See pitfall #11 in the root `copilot-instructions.md`.

## Keep the Index Updated

[docs/README.md](../../docs/README.md) is the documentation index. **Every time a doc file is added, renamed, or removed inside `docs/`**, update the index table to reflect the change. Broken links in the index are a hard error.

## Cross-Link Rules

- Use **relative paths** between docs (`[Configuration](configuration.md)`, not absolute paths).
- The root `README.md` links into `docs/` with relative paths (`[Getting Started](docs/getting-started.md)`).
- After renaming or moving a doc, search for all references to the old path and update them.

## Every Doc Needs a Table of Contents

Each markdown file in `docs/` must start with an H1 title followed by a **Table of Contents** section linking to all H2 headings:

```markdown
# Page Title

## Table of Contents

- [Section One](#section-one)
- [Section Two](#section-two)

---

## Section One
...
```

## Content Rules — What to Write

✅ **Do write:**
- Accurate descriptions of current behavior
- Step-by-step instructions a user can follow right now
- Configuration tables with real defaults from `package.json`
- Troubleshooting entries for issues users have actually hit
- Links to other relevant docs

❌ **Do NOT write:**
- "Future enhancements" / "Coming soon" / "Roadmap" sections
- "Performance guidelines" or "Best practices" that aren't grounded in real behavior
- Marketing copy or competitive comparisons
- Placeholder URLs (`https://github.com/your-username/...`)
- Features listed as "working" when they aren't implemented

## When to Update Docs

Update documentation when any of these change:

| Change | Docs to Update |
|--------|---------------|
| New/changed VS Code setting | `docs/configuration.md` (settings table) |
| New agent tool | `docs/chat-and-modes.md` (tools table) |
| New chat mode | `docs/chat-and-modes.md` |
| New command | Root `README.md` (commands section) |
| Changed connection behavior | `docs/authentication.md` or `docs/troubleshooting.md` |
| New user-facing feature | Appropriate doc + `docs/README.md` index if new file |
| Changed `package.json` engines/version | Root `README.md` (prerequisites) |

## Root README.md

The root `README.md` is the project landing page. It should be concise and link to `docs/` for details. It contains:

1. One-paragraph project description
2. Key features list (only currently working features)
3. Quick install steps
4. Link to `docs/` for full documentation
5. Build & development commands
6. License

Do **not** duplicate full guides in the README — link to `docs/` instead.
