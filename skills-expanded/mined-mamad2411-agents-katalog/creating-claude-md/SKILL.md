---
name: creating-claude-md
description: Use when the user wants to create a new CLAUDE.md from scratch for a repository, bootstrap project memory for a new repo, set up a repo for Claude Code for the first time, or completely rewrite an existing CLAUDE.md deemed unsalvageable. Produces a lean, high-signal file under 80 lines (120 hard cap) by scanning the repo for mechanical content (stack, commands, structure) and interviewing the user for judgment content (WHY, gotchas, out-of-scope, approval gates, testing philosophy, external docs like Confluence pages). NOT for auditing or incrementally improving an existing CLAUDE.md — that is the claude-md-improver skill's role.
---

# Creating a CLAUDE.md From Scratch

Generate a lean, high-signal CLAUDE.md for a repository by combining an autonomous repo scan with a focused 6-question user interview.

**Core principle:** Every line must earn its place. If removing a line would not cause Claude to make a specific mistake, it does not belong in the file.

## When to Use vs. Not Use

**Use when:**
- Repo has no CLAUDE.md and user wants one.
- Repo has a CLAUDE.md that the user considers unsalvageable and wants rewritten from scratch.
- User says "set this repo up for Claude Code", "bootstrap project memory", "write me a CLAUDE.md".

**Do NOT use when:**
- User wants to audit, improve, or incrementally fix an existing CLAUDE.md. Route to `claude-md-improver` instead.
- User wants to add a single rule / gotcha to an existing file. Edit directly.
- Repo is a scratch directory with no meaningful content yet.

## The Iron Rule

**Target ≤ 80 lines. Hard cap 120.** This is a forcing function. Bloat triggers the harness to uniformly down-weight all instructions in the file (not just the tail). If the draft exceeds 80 lines, split oversized sections into `agent_docs/*.md` before writing anything to disk.

## 4-Phase Workflow

Follow in order. Do not skip phases.

### Phase 1: Scan the Repo (Autonomous)

Gather mechanical content the repo can tell you:

- **Manifests** — read whichever exist: `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `pom.xml`, `build.gradle`, `Gemfile`, `composer.json`, `Makefile`. Extract: language, framework, versions, scripts.
- **Structure** — `ls` top-level + one level deep. Detect monorepo via `workspaces` in `package.json`, `pnpm-workspace.yaml`, `lerna.json`, `turbo.json`, `nx.json`, or `packages/` / `apps/` directories.
- **Enforced conventions** — read `.editorconfig`, `.eslintrc*`, `biome.json`, `.prettierrc*`, `ruff.toml`, `pyproject.toml` (`[tool.ruff]` / `[tool.black]`), `rustfmt.toml`, `.golangci.yml`. **Record these — the corresponding rules are BANNED from CLAUDE.md** (linter does the job).
- **Existing docs** — `README.md`, any `agent_docs/`, `.claude/rules/`, subdirectory `CLAUDE.md` files. Do not overwrite auxiliary files that already exist without asking.
- **Git** — `git log --oneline -20` to detect commit conventions (Conventional Commits, prefix patterns).
- **Boundary check** — look for existing `CLAUDE.md`, `AGENTS.md`, `CLAUDE.local.md`. If `CLAUDE.md` exists with meaningful content (> 20 lines, not just a stub), STOP and ask user: `[rewrite / run claude-md-improver / cancel]`. Proceed only if they confirm rewrite.
- **Auto-memory** — check `~/.claude/projects/<path-hash>/memory/` if it exists. Note what Claude has already auto-learned so you do not duplicate it.
- **External-doc MCPs** — check which MCPs are configured in this session for external docs. Common names include `confluence-dc`, `confluence`, `notion`, `atlassian`. Record the exact MCP name (e.g., `confluence-dc`) so Phase 3 can reference it by the same name in the generated `## External Docs` section. If none are configured but the user references external docs in Q6, record that as plain URLs without MCP instructions.

### Phase 2: Interview the User

Ask all questions in a **single numbered list**. User answers all together. Do not ask one at a time.

**Fixed 6 (always ask):**

1. **WHY** — In one sentence, what does this project do and who uses it?
2. **Gotchas** — What has tripped up new contributors or Claude in this repo? Non-obvious traps, modules with weird behavior, required setup steps not in the README.
3. **Out of scope** — Any files, directories, or areas Claude should NEVER modify autonomously? (auto-generated files, migrations, infra, other teams' code)
4. **Approval gates** — Any actions that require your explicit approval before Claude runs them? (destructive git, DB schema changes, deploys, production-adjacent changes)
5. **Testing philosophy** — How do you verify changes work? Is there any check that must always pass before shipping?
6. **External docs** — Are there Confluence pages (or Notion / wiki / Google Docs) that document parts of this repo? For each, paste: (a) the URL, (b) a one-line description of what it covers, (c) policy — `read` (reference only, never modify) or `update` (keep in sync when related code changes). Leave blank if none.

**Adaptive follow-ups (add up to 3, only when the scan surfaced ambiguity):**

- Monorepo detected → "I see N packages: X, Y, Z. Which ones does Claude frequently confuse or work across incorrectly?"
- `migrations/` directory found → "Any rules around creating or running migrations?"
- Multiple lockfiles (`package-lock.json` + `yarn.lock` + `pnpm-lock.yaml`) → "Which package manager is authoritative?"
- CI config present but no local check script → "Any CI checks that must pass locally before pushing?"
- External infra configs present (`docker-compose.yml`, `terraform/`, k8s manifests) → "Which of these does Claude own versus another team?"

Ask at most 9 total questions (6 fixed + up to 3 adaptive). If the user's answers are vague, re-ask once; do not invent content.

### Phase 3: Draft (In-Memory Only)

Compose the file against the Output Spec below. Before writing anything to disk:

1. Count lines.
2. If > 80: pick the section(s) that contributed most (typically Gotchas or Architecture detail) and extract them into `agent_docs/*.md` stubs. Replace with a 1-line pointer under `## References`.
3. If still > 120 after aux-file splits: drop the least-load-bearing rules. The file must fit.
4. Run the Red Flag Self-Check (below). Fix every flag before writing.

### Phase 4: Write

- Write `CLAUDE.md` to repo root.
- Write any auxiliary files to `agent_docs/*.md`.
- Do NOT commit to git.
- Report to the user:
  - Files written, with line counts.
  - Brief summary of what lives where.
  - Reminder: "Add `CLAUDE.local.md` to `.gitignore` if you want personal overrides. Do not create it here — that is your personal concern."

## Output Spec

### Section Set

Include a section **only** if the scan or interview produced real content for it. Empty sections are worse than missing ones.

| # | Section | Source | When |
|---|---|---|---|
| 1 | `# <Project>` + 1-line WHY | Interview Q1 | Always |
| 2 | `## Stack` | Scan: manifests | Always |
| 3 | `## Project Structure` | Scan: ls | If > 3 top-level dirs or monorepo |
| 4 | `## Commands` | Scan: scripts | Always |
| 5 | `## Conventions` | Scan: git log + interview | Only non-default conventions |
| 6 | `## Gotchas` | Interview Q2 | Only if user surfaced any |
| 7 | `## Out of Scope` | Interview Q3 | Only if user surfaced any |
| 8 | `## Approval Required` | Interview Q4 + Q6 policy | Only if user surfaced any |
| 9 | `## Testing` | Scan + Q5 | Always |
| 10 | `## External Docs` | Interview Q6 + scan (MCP availability) | Only if Q6 surfaced any pages |
| 11 | `## References` | Aux files created | Only if aux files exist |

### Formatting Rules

- Max 3 heading levels (`#`, `##`, `###`).
- Commands in fenced ` ```bash ` blocks with inline `# ...` comments for flags. Never in prose.
- Every rule in **imperative** form: "Use X", "Never Y; instead do Z".
- **Every negative rule paired with a positive alternative.** "Never force-push" alone leaves Claude stuck; "Never force-push; rebase locally then push normally" gives it a path.
- Max 2 `IMPORTANT:` or `YOU MUST` markers in the entire file. Reserved for security or data-integrity rules only. More than 2 makes emphasis invisible.
- No pasted code blocks > 10 lines. Use `path/to/file.ts:42` pointers instead.
- No `@path/to/doc.md` import syntax. Use plain `see path/to/doc.md` references — plain references load only when Claude decides they are relevant; `@` imports load immediately and burn context.

### The `## External Docs` Section (Confluence / Notion / Wiki)

Emit this section only if Q6 produced at least one page. One bullet per page. Each bullet has three parts: URL + one-line purpose + policy (read vs. update) + which MCP name to use.

Template (substitute the MCP name recorded in Phase 1; if no external-doc MCP is configured, drop the MCP clause and leave the URL as a plain reference):

```markdown
## External Docs

- **<One-line purpose>** — <URL>
  - READ via `<mcp-name>` MCP when working on <specific code area, e.g., `app/api/**`>. Prefer reading this page over inferring behavior from code.
  - UPDATE via `<mcp-name>` MCP before pushing any change that <specific trigger, e.g., adds/removes/modifies endpoints, changes request/response shapes>.

- **<One-line purpose>** — <URL>
  - READ-ONLY. Never modify this page. If content here conflicts with code, flag the discrepancy to the user.
```

Rules for the section:
- Pages with policy `read` → emit only the READ or READ-ONLY bullet.
- Pages with policy `update` → emit both READ and UPDATE bullets. The UPDATE bullet MUST specify a concrete trigger (what kind of code change forces a doc update), sourced from the user's Q6 answer or the file globs most relevant to the page. Never emit a generic "update when things change".
- Never paste Confluence page content into CLAUDE.md. URL + purpose + policy only.
- If the user lists > 5 external doc pages, emit only the top 3 most-referenced and move the rest into `agent_docs/external-docs.md` with the same format.

**Automatic rule when Q6 surfaces any `update` pages:** append one line to `## Approval Required`:

```markdown
- Before `git push`, if any change touches code referenced by an `update`-policy page in `## External Docs`, update that page (or confirm with me first).
```

This is the forcing function that makes per-page update rules actually fire. Do not add it if all Q6 pages are `read`-only.

### Banned Content

Delete from the draft on sight:

- Personality instructions: "be a senior engineer", "think step by step", "approach this carefully".
- Style rules already enforced by linter configs detected in Phase 1 (indentation, quote style, semicolons, import order, etc.).
- Standard language idioms Claude already knows (use `async/await`, use `pathlib`, prefer `const` over `var`).
- Pasted architecture essays. Summarize in two sentences, link the doc.
- Secrets, tokens, connection strings, API keys.
- Descriptive prose ("we generally prefer…", "try to…"). Rewrite as imperative or delete.
- Contributor names, roadmap items, sprint-specific notes.
- Version numbers inside descriptive prose (stale within weeks). Put versions in the Stack section only, sourced from manifests.
- Pasted content from Confluence / Notion / wiki pages. CLAUDE.md is not a cache. URL + purpose + policy only.

### Auxiliary Files (Moderate Progressive Disclosure)

Trigger aux-file splits only when the root file exceeds 80 lines after drafting. Do not scaffold them speculatively.

Typical splits:
- `agent_docs/architecture.md` — layered architectures with > 3 components worth describing.
- `agent_docs/testing.md` — when the test workflow has > 3 commands or non-trivial patterns.
- `agent_docs/<domain>.md` — when gotchas cluster around one domain (e.g., `agent_docs/auth.md`).

Each aux file follows the same rules as root: imperative, no pasted code, pointers not copies, no linter-replaceable style rules.

Root references them via a `## References` section:
```markdown
## References

- `agent_docs/architecture.md` — service boundaries and data flow
- `agent_docs/testing.md` — how to run and write tests
```

For monorepos with packages that have materially different conventions, **offer** (do not force) to stub `packages/<name>/CLAUDE.md` files. These are loaded on demand only when Claude works in that directory.

## Red Flag Self-Check (Before Writing)

Run every item before writing to disk. Fix any flag or start that section over.

- [ ] File > 120 lines → split to aux file.
- [ ] Empty section with a stub header → delete the section.
- [ ] Any rule duplicated in a linter/formatter config detected in Phase 1 → delete.
- [ ] Any rule phrased as "we generally…" / "try to…" / "it is preferred that…" → rewrite imperative or delete.
- [ ] Any negative rule without a positive alternative → fix or delete.
- [ ] More than 2 `IMPORTANT:` / `YOU MUST` markers → reduce to the 2 most critical.
- [ ] Pasted code block > 10 lines that is not a verbatim command → replace with `path:line` pointer.
- [ ] Personality instruction present → delete.
- [ ] `@` import syntax used → replace with plain reference.
- [ ] Rule covers a hypothetical rather than a real incident the user described → delete.

## Boundary: Handling an Existing CLAUDE.md

If Phase 1 finds an existing `CLAUDE.md` with meaningful content (> 20 lines, not an auto-generated stub):

> Existing CLAUDE.md found (N lines). This skill rewrites from scratch; it does not preserve content. Choose:
> - `rewrite` — overwrite with a fresh one
> - `improver` — exit and run the `claude-md-improver` skill to audit and improve what's there
> - `cancel` — do nothing

Proceed only on `rewrite`. On `improver`, exit and tell the user to invoke that skill. On `cancel`, exit.

Stub / near-empty existing files (< 20 lines, clearly auto-generated) can be overwritten without prompting.

## Anti-Pattern Rationalizations

Capture these so the model cannot rationalize around the rules under pressure:

| Rationalization | Reality |
|---|---|
| "This repo has no manifest, I'll infer the stack from file extensions" | No. Halt and ask the user. Guessed commands are worse than no commands. |
| "The user's answer to Q2 was vague, I'll flesh it out with likely gotchas" | No. Invented content is how bad CLAUDE.md files are born. Re-ask once, then skip the section. |
| "I'm at 95 lines, let me cram in 25 more — still under 120" | No. 80 is the target; 120 is the ceiling only after aux-file splits. Split first. |
| "The user did not pick a commit convention, I'll recommend Conventional Commits" | No. If the repo's `git log` shows no pattern, the user does not care. Omit the section. |
| "The existing CLAUDE.md has a few good rules, I'll keep those" | No. This skill is from-scratch. If the user wants to preserve, route them to `claude-md-improver`. |
| "Let me add 'be a senior engineer' to set the tone" | No. Zero behavioral effect. Banned. |
| "I'll add the style rules the user mentioned even though `.eslintrc` already enforces them" | No. Tell the user which linter rule covers it. Keep CLAUDE.md for things tools cannot enforce. |
| "The user gave vague out-of-scope answers, I'll write generic warnings" | No. Skip the section entirely if Q3 did not surface specifics. |
| "The Confluence page content might be stale, let me paste a snapshot into CLAUDE.md as a backup" | No. CLAUDE.md is not a cache. URL + purpose + policy only. If staleness is a concern, flag it to the user so they update the page. |
| "The user just said 'update the Confluence page when things change' — I'll write that as a generic update rule" | No. Generic triggers do not fire. Re-ask for specifics: which code areas trigger an update to which page. |

## Example Output (Reference, Not Template)

Here is what a well-shaped CLAUDE.md looks like for a mid-size Next.js app. Do not copy verbatim — generate based on actual scan + interview results.

````markdown
# ShopFront

Next.js 14 e-commerce site with Stripe payments, served to retail customers.

## Stack

- Next.js 14 (App Router), TypeScript 5.4, Node 20
- Prisma ORM + Postgres 15
- Tailwind CSS 3, shadcn/ui components

## Project Structure

- `app/` — Next.js App Router pages and API routes
- `components/` — reusable UI (shadcn-based)
- `lib/` — shared utilities and DB client
- `prisma/` — schema and migrations

## Commands

```bash
pnpm install              # Install deps (pnpm only — do not use npm/yarn)
pnpm dev                  # Dev server on :3000
pnpm test                 # Vitest unit tests
pnpm test:e2e             # Playwright end-to-end
pnpm lint                 # Biome check
pnpm db:migrate           # Prisma migrate dev
```

## Gotchas

- Stripe webhooks in `app/api/webhooks/stripe/route.ts:14` require `stripe-signature` validation — never short-circuit it.
- Product images live in Cloudinary, not the repo. Never commit binary assets under `public/`.
- `lib/auth.ts:42` has custom retry logic; do not "simplify" it — it handles a known race with our identity provider.

## Out of Scope

- `prisma/migrations/` — never edit existing migration files; create a new one via `pnpm db:migrate`.
- `infra/` — owned by platform team; ask before changing.

## Approval Required

- Any schema change (Prisma migration).
- `git push --force` on any branch (rebase locally then push normally instead).
- Touching `app/api/webhooks/stripe/route.ts` (payment-critical).
- Before `git push`, if any change touches code referenced by an `update`-policy page in `## External Docs`, update that page (or confirm with me first).

## Testing

Run `pnpm test && pnpm test:e2e` before any PR. IMPORTANT: Stripe webhook changes require running the signature verification test suite (`pnpm test -- webhooks`).

## External Docs

- **REST API reference** — https://confluence.example.com/display/ENG/ShopFront+API
  - READ via `confluence-dc` MCP when working on any `app/api/**` route. Prefer reading this page over inferring behavior from code.
  - UPDATE via `confluence-dc` MCP before pushing any change that adds/removes/modifies endpoints, request/response shapes, or auth requirements.

- **Payments runbook** — https://confluence.example.com/display/ENG/ShopFront+Payments+Runbook
  - READ-ONLY. Never modify this page. If content here conflicts with code, flag the discrepancy to the user.
````

Notice what is NOT there: no indentation rules (Biome enforces), no "be careful" prose, no contributor list, no roadmap, no `@imports`, no pasted code, no personality instructions, no pasted Confluence content. Every line prevents a specific mistake.

## After Writing

Report to the user with:
- Files written (paths + line counts).
- One-line summary of what each aux file covers (if any).
- Reminder: "For personal overrides (editor preferences, verbose logging, etc.), create `CLAUDE.local.md` and add it to `.gitignore`. That is a personal file and this skill does not generate it."
- Suggestion: "Review the file — every line should prevent a real mistake. Delete anything that does not."
