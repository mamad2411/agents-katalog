---
name: bootstrap-harness
description: Create a complete AI-agent harness (CLAUDE.md + supporting docs system) for any project. Portable across Python/Java/TS/Go. Based on 2025-2026 best practices (AGENTS.md spec, GitHub's 2,500-repo study, ACE paper, context-engineering research). Use when a repo has no harness, was just cloned/scaffolded, or its docs are bloated/stale and need a structured rebuild.
allowed-tools: Read, Glob, Grep, Write, Edit, Bash, AskUserQuestion, TodoWrite
---

# bootstrap-harness

Create a production-quality harness (docs system for AI agents) in any repo. **3 progressive stages** — produce only what the project needs at its current maturity.

File templates live in [templates.md](templates.md) — read it when you reach Step 3, not before.

## When to use

- **Fresh repo / no CLAUDE.md** — just cloned or scaffolded, wants AI-agent workflow
- **Repo with no harness** — team adopting structured AI coding
- **Major rebuild** — current docs bloated / stale / drifted

## When NOT to use

- **Minor tweaks / drift** → `/review-harness` (incremental, no rebuild)
- **Single-file script / experiment** → overkill
- **Harness exists and mostly accurate** → `/review-harness` first to confirm

---

## Core principles (2025-2026 research)

1. **Commands go first** — agents query build/test/run most often (GitHub 2,500-repo study).
2. **✅ / ⚠️ / 🚫 three-tier Boundaries** — Always / Ask first / Never (AGENTS.md spec).
3. **CORRECT / INCORRECT code pairs** — concrete examples beat prose; pull from real repo code.
4. **CLAUDE.md hard limit < 60 lines.** SOTA: instruction-following degrades past ~150-200 total instructions, and — worse — a bloated file gets judged "irrelevant" and **ignored wholesale**, taking your good rules down with it. Design CLAUDE.md as a **pointer, not a description**. Test every line: *"would removing this cause the agent to make a mistake?"* If no, cut it. Other harness files target < 200.
5. **No premature quantification** — no SLO numbers / coverage % / weight tables unless you actually measure.
6. **Separate stable vs dynamic, and give every artifact a home.** Hard rules → `CLAUDE.md` (stable). In-progress work → `docs/exec-plans/active/<plan>.md` (dynamic). **Delivered plans → `completed/`. Rendered byproducts (HTML reports, research dumps, design variants) → ONE archive dir, gitignored** — a second graveyard scatters byproducts and splits references. The index `docs/exec-plans/README.md` connects them; no README inside `active/` `completed/` `archive/`. **Archive reference rule:** tracked docs never markdown-link into the gitignored archive (clicks locally, 404s in every clone) — inline the 3-5 line conclusion, cite the path as backtick text + a "local archive" note.
7. **Bullet + ID for evolving rules** → enables delta edits, not full rewrites (ACE paper). Rewriting a whole doc to add one rule causes *context collapse* (detail erodes) and *brevity bias* (specifics get summarized away). Add/edit small structured items instead.
8. **Prose rots; code / tests / ADRs are truth.** Never let a prose doc become a *second source of truth* for something the code, tests, or an ADR already encodes (capability lists, phase status, schema, counts). It WILL drift, and agents adopt the rotten copy as fact. State it once in the authoritative place; everywhere else **links**, not copies. **And for code-derivable facts (counts, capability lists, enums), even a hand-maintained "single source" doc rots** — derive it from code (a `gen-docs` step) or pin it with a CI assert (`assert len(REGISTRY) == N`); let prose only link. (Real case: a SPEC doc claimed "21 capabilities" while the registry had 11 — the "single source" was itself a stale literal.)
9. **Gates are the immune system — scaffold them on day one.** A 10-day natural experiment (LinkPea 2026-07, three overhaul rounds): every CI-gated invariant stayed correct; **every ungated prose area rotted**. Prose only stays true when something checks it. So Stage 1 ships `scripts/check-harness.mjs` (4 starter gates, zero-dep node — [gates.md](gates.md)) wired into CI, and every rot class discovered later gets the same first question — *"can this become a gate?"* — before it's allowed onto any review checklist. Cadence = two frequencies: **weekly mechanical self-check in CI, pushing green AND red** (a silent week = the check itself died) + **monthly `/review-harness`** for what needs semantic judgment; a human approves changes.
10. **Every file earns its place, every doc a real reader.** If you can't name a concrete agent task that needs the file, skip it. If the reader doesn't exist today, don't write for them (real case: 800-line onboarding for an imagined 5-person team in a solo+agents repo). Ask who actually reads — solo+agents / small team — and size every doc to that.
11. **Write-in needs write-out (retirement).** One-shot content — executed runbooks, superseded specs, finished checklists, migration logs — retires the moment it's done: compress to a **tombstone line** (✅ + date + one-line pointer), delete the body, **keep the heading** so old references don't dangle. **Git history is the archive** — no "kept for archaeology" layers, and never stack dated patch blocks ("⚠️ updated YYYY-MM-DD…"): fold new facts into the section, retire the stale ones. A harness with only write-in rules is a reservoir with no outlet — it WILL silt up.
12. **Root/docs boundary.** Root keeps only ecosystem-pinned files (README, AGENTS/CLAUDE, CONTRIBUTING, CODEOWNERS, justfile/Makefile…); every other doc lives under `docs/`. No new root-level md.

---

## Workflow — 4 steps

Use TodoWrite to track: **Scan → Ask → Generate → Verify.**

### Step 1 — Scan repo silently

```bash
ls -la && git log --oneline -10 2>/dev/null
find . -maxdepth 2 -type f -name '*.md' | head -20
ls package.json pom.xml Cargo.toml pyproject.toml go.mod requirements.txt Gemfile 2>/dev/null   # stack
ls next.config.* vite.config.* nuxt.config.* 2>/dev/null                                         # framework
ls CLAUDE.md AGENTS.md GLOSSARY.md README.md docs/ .claude/ 2>/dev/null                           # existing harness
ls .github/workflows/ tests/ test/ __tests__/ 2>/dev/null                                         # maturity
```

Record internally: language/framework · existing docs worth keeping vs replacing · recent git activity (what's the team actually doing?) · maturity (PoC / MVP / prod?).

### Step 2 — Ask the user (only if uncertain)

**AskUserQuestion** for: one-sentence project description (if README is generic) · target stage (Seed/Standard/Full) · **real reader mix today** (solo+agents / small team — sizes every doc; never write for readers that don't exist yet) · business-domain-heavy? (Y → GLOSSARY) · multi-agent tools? (Cursor+Codex+Claude → AGENTS.md naming; Claude-only → CLAUDE.md). Skip anything obvious from the scan; don't bombard.

### Step 3 — Pick stage, generate files

Read [templates.md](templates.md) and [gates.md](gates.md) now. Track each file `in_progress → completed` with TodoWrite.

**Stage 1 — Seed (any project):**
- `CLAUDE.md` (or `AGENTS.md`) — intro + Commands + Structure + Boundaries + pointer + index. **< 60 lines.**
- `docs/exec-plans/README.md` — index of active/completed/archive plans, **with the status-line vocabulary (📋/🔄/⏸️+Revisit/📌/✅) and the 21-day staleness rule**.
- Empty `docs/exec-plans/active/` + `completed/` + `archive/` dirs. **Leave active/ empty** — the owner writes their own plans. Add `docs/exec-plans/archive/` to `.gitignore` (the ONLY archive dir).
- `scripts/check-harness.mjs` — 4 starter gates (status-line / lifecycle / two-way index / link health), zero-dep node, from [gates.md](gates.md). **Wire into existing CI** (add to the PR gate) if any; and if CI exists, also generate the **weekly self-check workflow** (gates.md — green-or-red notification, deadman built in). No CI → skip the workflow and say so in the closing report (`/review-harness` monthly becomes the only check).

Stop here if the user says "just the basics."

**Stage 2 — Standard (MVP):** add `GLOSSARY.md` (if domain-heavy) · `docs/lessons.md` (seed 3-5 from git log) · `docs/exec-plans/tech-debt-tracker.md` · `docs/design-docs/core-beliefs.md` · root `README.md` (only if current is the framework default).

**Stage 3 — Full (mature), only if each earns its keep:** `ARCHITECTURE.md` (multi-module) · `DESIGN.md` (has UI) · `FRONTEND.md`/`BACKEND.md` (non-trivial split) · `RELIABILITY.md` (prod/multi-service) · `SECURITY.md` (auth/user-data) · `docs/design-docs/NNN-*.md` (decision records) · `docs/generated/` (auto-generatable schemas).

### Step 4 — Verify + hand off

- `wc -l CLAUDE.md` → **< 60** (hard; if over, slim: code blocks → tables; bullet lists → terse prose; move detail to GLOSSARY or a linked doc).
- `node scripts/check-harness.mjs` → **must exit green on the fresh harness** — gates ship working, not as TODOs (this also catches your own dead links / archive fake links).
- If the weekly self-check workflow was generated: tell the owner **the notification chain is live only when a real message arrives from a manual dispatch** — "configured" ≠ "shipped".
- Summary: what was generated, what was skipped and **why**, next steps.

---

## Anti-patterns

- ❌ **Dumping all 20 files at once** — offer Stage 1, confirm, move up.
- ❌ **Template placeholders left in final files** — fill or delete `<TODO>`.
- ❌ **Copying from a previous project** — scan the target first; a payments GLOSSARY is useless in a CMS.
- ❌ **Weights / percentages / SLO numbers without measurement** — false precision.
- ❌ **Promoting a lesson to a hard rule on first sighting** — require ≥2 references.
- ❌ **Prose duplicating code-truth** — a capability list / phase status / schema copied into prose becomes a second source that rots. Link to the one authoritative place.
- ❌ **Keeping ✅-delivered plans in `active/` "for reference"** — `active/` is in-progress only. Delivered → `completed/` in the **same commit** you mark it done. "Move later" = never.
- ❌ **Letting rendered HTML / reports pile up in `active/`** — they're byproducts, not plans → `archive/` (gitignored).
- ❌ **`AGENTS.md` as a symlink to `CLAUDE.md`** — Windows checks the symlink out as a plain text file containing the path, not the content. If you want both names: make **`AGENTS.md` the canonical file** and **`CLAUDE.md` a one-line `@AGENTS.md` import** — Claude Code resolves it natively, other tools read `AGENTS.md` directly, Mac+Win safe, zero-dep. For large multi-tool fan-out, [ruler](https://github.com/intellectronica/ruler) also works.
- ❌ **A four-file set in every directory** (`AGENTS.md`+`DESIGN.md`+`PROGRESS.md`+`BUGS.md` per package) — no real backing, and `PROGRESS`/`BUGS`/`DESIGN` just duplicate `exec-plans/` / `lessons.md` / ADRs (which rot independently). Use **one `AGENTS.md`** per directory that has genuinely local rules; everything else links to the single source.
- ❌ **Creating a project-level copy of `/review-harness`** — it's a user-level skill; reference it, never write `.claude/skills/review-harness/` into the target.
- ❌ **Framing the owner as "intern" / "junior" in any artifact** — harness language treats them as the owner.
- ❌ **Shipping the harness without its gate script** — ungated prose starts rotting the day it's written; the 4 starter gates cost ~100 zero-dep lines.
- ❌ **Onboarding / role-matrix / process docs for readers that don't exist** — write for the reader mix confirmed in Step 2, nothing more.
- ❌ **A second archive/graveyard dir, or clickable links into the gitignored one** — one archive; references = inline conclusion + backtick path.
- ❌ **"⚠️ updated YYYY-MM-DD" patch blocks as the update mechanism** — fold facts into sections; retire stale content with a tombstone line.

---

## Closing report

```markdown
## Harness Bootstrap Done — Stage <N>
### Generated
- CLAUDE.md (<N> lines, < 60 ✓) · docs/exec-plans/README.md + active/ completed/ archive/ · scripts/check-harness.mjs (4 gates, ran green ✓) · <others>
### Gates & cadence
- check-harness.mjs wired into CI: ✓ / no CI found → `/review-harness` monthly is the only check
- weekly self-check workflow: generated ✓ (**acceptance = one real message from a manual dispatch**) / skipped (<why>)
### Skipped (with reason)
- ARCHITECTURE.md — single-module · RELIABILITY.md — not prod-bound
### Key conventions encoded
- Commands/Testing/Structure/Boundaries · ✅/⚠️/🚫 tiers · <N> CORRECT/INCORRECT pairs from real code · status-line vocab 📋/🔄/⏸️+Revisit/📌/✅ + 21-day staleness · active→completed lifecycle + ONE gitignored archive/ · tombstone retirement (git history = the archive)
### Next steps
1. After your next milestone, run `/review-harness` (monthly + after each line closeout)
2. Append to docs/lessons.md as you hit pitfalls
3. New rot class found → first ask "can this become a gate?" (extend check-harness.mjs)
4. If the project grows (UI / prod / multi-module), re-run for Stage 3
```

---

## Sources

- [AGENTS.md spec](https://agents.md/) · [GitHub 2,500-repo study](https://github.blog/ai-and-ml/github-copilot/how-to-write-a-great-agents-md-lessons-from-over-2500-repositories/)
- [ACE paper (2510.04618)](https://arxiv.org/abs/2510.04618) — structured bullets, delta edits, context-collapse / brevity-bias
- [Harness Engineering Best Practices 2026](https://nyosegawa.com/en/posts/harness-engineering-best-practices-2026/) — mechanisms-not-prompts, feedback-speed hierarchy, "docs rot, tests don't"
- [Writing a good CLAUDE.md (HumanLayer)](https://www.humanlayer.dev/blog/writing-a-good-claude-md) — < 60 lines, pointer-not-description
- [openai/codex AGENTS.md](https://github.com/openai/codex/blob/main/AGENTS.md) · [vercel-labs/ralph-loop-agent](https://github.com/vercel-labs/ralph-loop-agent/blob/main/AGENTS.md) — CORRECT/INCORRECT reference
