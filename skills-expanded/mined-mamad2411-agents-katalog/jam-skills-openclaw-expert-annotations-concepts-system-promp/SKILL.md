---
upstream: https://docs.openclaw.ai/concepts/system-prompt.md
relevance: jambot-critical
last-verified: 2026-07-25
audit_anchors: [5]
related_pages: [concepts__agent-workspace, reference__templates__AGENTS]
---

# System prompt — JamBot annotation

## What docs say (TL;DR)

Prompt assembled from ~26 sections at session start. Bootstrap files (`AGENTS.md`, `TOOLS.md`, `MEMORY.md`, `HEARTBEAT.md`, `SOUL.md`, `IDENTITY.md`, `BOOT.md`, `BOOTSTRAP.md`, `USER.md`) injected with caps. `/context list` shows what's consuming tokens.

## Anchor #5 — Per-file bootstrap caps (v5.2 production-observed)

v4.20 line 2393 introduced **per-file caps** (vs. flat `bootstrapMaxChars: 20000`). Specific values are NOT in changelog — production-observed against 5.2:

| File | Cap (chars) | Auto-truncated? |
|------|-------------|-----------------|
| TOOLS.md | ≈ 24,000 | Yes, with marker |
| MEMORY.md | ≈ 10,500 | Yes, with marker |
| Other workspace bootstrap files | ≈ 20,000 | Yes, with marker |

**JamBot's MEMORY.md is currently 56KB / 561 lines.** Most index entries past ~150 lines are NOT visible at runtime. Trim aggressively.

## New v4.x knobs (audit doc §2.1)

| Key | Default | Introduced |
|-----|---------|-----------|
| `agents.defaults.skipOptionalBootstrapFiles` | false | v5.2 line 35 |
| `agents.defaults.contextInjection: "never"` | enabled | v4.24 line 1792 |
| `agents.defaults.systemPromptOverride` | unset | v4.7 |

`contextInjection: "never"` is for agents that fully own their prompt lifecycle (skip workspace injection entirely).

## v4.7 heartbeat prompt-section controls

Heartbeat runtime behavior can stay enabled WITHOUT injecting heartbeat instructions every turn. Saves tokens.

## Bootstrap file load order

1. `AGENTS.md` — agent role + standing orders
2. `IDENTITY.md` — name, persona
3. `SOUL.md` — personality + hard blocks
4. `TOOLS.md` — tool routing for skills
5. `BOOT.md` / `BOOTSTRAP.md` — first-turn context
6. `USER.md` — principal info (delegate model, anchor #N — delegate-architecture)
7. `MEMORY.md` — long-term memory index
8. `HEARTBEAT.md` — periodic injection (controlled separately v4.7)

Order matters when caps bite — files later in the order may be more truncated.

## Skills snapshot invalidation (v4.15)

Session `skillsSnapshot` invalidates when ANY of these write:
- `skills.allowBundled`
- `skills.entries.<id>.enabled`
- ~~`skills.profile`~~ — **does not exist**, see correction below

Forces a re-bootstrap on next turn.

> **⚠️ CORRECTED 2026-07-25 — `skills.profile` does not exist.** Verified absent from the live
> `2026.5.7` schema (`openclaw config schema`, 6,441 paths — the only `skills.*` keys are
> `allowBundled`, `entries.*`, `install.*`, `limits.*`, `load.*`) **and** absent from the 7.x
> config-reference docs. The snapshot-invalidation claim holds for `skills.allowBundled` and
> `skills.entries.<id>.enabled`; treat the third as an error in the original audit, not a key to set.

## /context commands

- `/context list` — what's consuming tokens
- `/context show <section>` — full section text
- `/context skills` — current skills snapshot

## JamBot impact

- MEMORY.md heavily truncated (anchor #5) — 75%+ of content unseen at runtime
- TOOLS.md is a bigger file across all clients now (ovui-desktop, mesh tools, custom skills) — at risk of cap
- Action item: per-client TOOLS.md audit, especially for clients with many skills

## Related JamBot files

- `audit-anchors/anchor-05-per-file-bootstrap-caps.md`
- `/home/mike/.claude/projects/-home-mike-MIKE-AI/memory/MEMORY.md` (the file getting truncated)
- `docs/jambot/openvoiceui-system-prompt.md`
- `annotations/concepts__memory.md`

---

<!-- verification-stamp -->
## Verification — 2026-07-25

**Method (be precise about what this stamp does and does not mean):**

- Every config key this file asserts was checked against the **live schema of the version JamBot actually runs** — `openclaw config schema` inside `openclaw-test-dev` at `2026.5.7`, 6,441 schema paths.
- Upstream page re-fetched as Markdown on 2026-07-25 (`scripts/fetch-page.sh --no-cache`).
- **Not done:** the prose was not re-read line-by-line against the 7.x docs. Upstream is at `2026.7.1`; this file is verified for our pin, not for upstream HEAD.

**Config keys asserted here: 3/4 confirmed present in the 2026.5.7 schema.**

Not resolvable as schema paths (expected for RPC method names, plugin-manifest fields, OTel metric names, and shorthand references — confirm the kind before treating as drift):

- `skills.profile`

If you change this file, re-run `python3 scripts/sync-annotations.py` so `lastVerified` reaches `catalog.json`.
