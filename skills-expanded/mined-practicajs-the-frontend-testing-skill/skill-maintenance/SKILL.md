---
name: skill-maintenance
description: Maintain the Frontend Testing Skill in this repo. Use when asked to review the skill, run a spec/quality review, install-local (wire one example app to the local marketplace), sync up (an example app → root), install-marketplace (switch the vitest-browser app to the published GitHub marketplace), run a sanity test of the skill end-to-end (single app or the monorepo example, per package), run validate-release (install from GitHub marketplace → sanity → restore) against the vitest-browser app, or create a fresh example app copy at a given path for manual install testing.
license: MIT
compatibility: For local maintainers of this repo (Claude Code).
metadata:
  author: Yoni Goldberg (Practica.js)
  version: "1.4"
---

# Skill Maintenance

A toolkit for local maintainers of this repo. It reviews, syncs, and sanity-tests
the **Frontend Testing Skill**, whose source of truth is
`plugin/frontend-testing/` (this is what ships to users). The two example apps —
`example-app-vitest-browser/` and `example-app-playwright/` — resolve the skill
via a local marketplace reference; no skill files are embedded in them. The root
`the-testing-skill/` tree is deprecated; ignore it.

Keep all maintenance docs short. Trust your judgment and ask the user when unsure.

## Operations

Pick the matching reference doc and follow it.

| When the user asks to…                                   | Read |
| -------------------------------------------------------- | ---- |
| review / audit the skill, check the spec, find issues    | [references/review.md](references/review.md) |
| install local — wire **one** named example app to the local marketplace (the current, non-copy way both apps are actually set up) | [references/install-local.md](references/install-local.md) |
| sync up — pull **one** named example app back to root    | [references/sync-up.md](references/sync-up.md) |
| install-marketplace — switch **vitest-browser** from local wiring to the published GitHub marketplace | [references/install-marketplace.md](references/install-marketplace.md) |
| sanity-test the skill end-to-end (build a feature, verify tests) | [references/sanity-test.md](references/sanity-test.md) |
| sanity-test the skill in the **monorepo** (`example-monorepo`, per package) | [references/sanity-test-monorepo.md](references/sanity-test-monorepo.md) |
| validate-release — install from GitHub marketplace → sanity → restore, on **vitest-browser** | [references/validate-release.md](references/validate-release.md) |
| publish / release the skill to the **Claude** plugin marketplace | [references/publish-claude.md](references/publish-claude.md) |
| publish / release the skill to the **Cursor** marketplace        | [references/publish-cursor.md](references/publish-cursor.md) |
| fresh example app — copy vitest-browser to a path, stripped of skill/marketplace, ready for a clean install | [references/fresh-example-app.md](references/fresh-example-app.md) |
