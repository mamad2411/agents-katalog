---
name: bootstrap-skills
description: Run a short structured interview about a software project (project shape, working style, build stack, quality concerns, production concerns), then search skills.sh for the highest-quality matching skills and install them into the project's local skills folder. Use when the user runs /bootstrap-skills, says "bootstrap this project", "set up skills for this project", "what skills should I install", or starts a new project and wants a recommended skill set.
---

# Bootstrap Skills

Run a short structured interview about a software project, then install the best-matching skills from skills.sh ranked by popularity and quality signals.

This skill is **proactive** — it asks what the project needs at setup time, rather than waiting for the user to ask later. All skills are installed at the project level — `./.claude/skills/` for Claude Code, `./.agents/skills/` for everything else — never globally.

The interview is organized by **software-development concern** rather than stack layer, so it works for web apps, backend services, mobile apps, and CLI tools/libraries equally well. The *options* shown in each section adapt to the project type detected in Section 1.

For lookup tables (search queries per topic and project type, ranking rubric, Claude Code flag rule, example session, HOW_TO_USE.md template), see `REFERENCE.md` in this same folder. Load it when you reach the search/install steps.

## Operating principles

1. **Detect before asking factual stack questions.** Scan the repo first (`package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `Gemfile`, `Package.swift`, `build.gradle`, etc.). Repo scans answer *factual* questions ("what framework is this?") — never *preference* questions ("how should the agent behave?"). Always ask preference questions; confirm stack assumptions rather than asking blind.
2. **One question at a time.** Wait for the answer. Never bundle multiple questions in one turn.
3. **Always use numbered-list format for questions.** Even when there's a strong recommendation, present choices as a numbered list and tell the user to reply with the number(s). This works across every agent (Claude Code, Codex, Cursor, OpenCode, etc.). Format:

   ```
   [The question]

   Reply with the number:
     1) [Option A]  ← recommended
     2) [Option B]
     3) [Option C]
   ```

   For multi-select, say "Reply with comma-separated numbers (e.g. `1, 3`)" and mark the recommended set.
4. **Adapt options to project type.** Section 3 ("Building it") shows a different option list per project type. Section 4 conditionally shows accessibility for UI projects. See "Option lists by project type" below.
5. **Keep a running tally visible.** After each section, show a one-line summary of what's been picked.
6. **Cap the structured interview at ~6 questions.** Section 5.5 ("anything else?") is the escape hatch for niche needs — don't expand the structured sections beyond 6.
7. **Never install without explicit confirmation.** Show the final list, get an explicit yes, then install.
8. **Always install to the project, never globally.** Use `npx skills add <repo> --skill <name> -y` (add `-a claude-code` if this is a Claude Code project — see `REFERENCE.md`). No `-g` flag.

## The interview

### Section 1 — Project shape & language (always ask)

Scan manifests in parallel (`package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `Gemfile`, `Package.swift`, `build.gradle`, etc.) to infer the primary language. Form a mental model of the stack before continuing.

Ask:
> What kind of project is this?
>
> Reply with the number:
>   1) Web app — UI + backend (React/Vue/Svelte/etc.)
>   2) Backend service or API — no UI
>   3) Mobile app — iOS, Android, or cross-platform
>   4) CLI tool or library
>   5) Docs / ADRs / planning repo (no code)
>   6) Other — describe in one sentence

If they pick 5, skip to Section 6 with documentation/ADR skills only.

**Then, if the primary language wasn't detected from manifests**, ask:
> What's the primary language?
>
> Reply with the number:
>   1) TypeScript / JavaScript
>   2) Python
>   3) Go
>   4) Rust
>   5) Swift / Kotlin / Dart (mobile)
>   6) Other — name it

Project type × language drives every option list that follows. Store both.

### Section 2 — Working style (always ask, multi-select)

Ask:
> How should the agent behave on this project? Reply with comma-separated numbers:
>   1) Plan before coding — agent grills you on design before writing code
>   2) Compressed responses — terse, minimal-token output
>   3) TDD discipline — agent insists on red-green-refactor workflow
>   4) Disciplined debugging — structured diagnosis loop for hard bugs

This is about *how the agent interacts moment-to-moment*, not what testing/quality tooling the project uses (that's Section 4).

### Section 3 — Building it (always ask, multi-select)

Show the option list matching Section 1's project type — see "Option lists by project type" below. Pre-mark anything detected in the repo as recommended.

> What's the build stack? Reply with comma-separated numbers:
>   [project-type-specific options here]

Accept free-text answers and search for them directly.

### Section 4 — Quality & correctness (always ask, multi-select)

Universal across project types. **Show option #5 (accessibility) only for web apps and mobile.** For backend/CLI projects, omit it and renumber.

> Which quality concerns matter for this project? Reply with comma-separated numbers:
>   1) Testing — frameworks and patterns for unit/integration/e2e
>   2) Type safety — strict-mode patterns, type-driven design
>   3) Linting & formatting
>   4) Code review — PR checklists, refactoring patterns
>   5) Accessibility  ← only show for web apps and mobile
>   6) Skip — handle quality concerns ad-hoc

For each pick, the search query is language- and project-type-aware. See `REFERENCE.md` for the mapping (e.g. testing for a Rust CLI → `rust test`; testing for a React app → `vitest` or `jest`).

### Section 5 — Running it in production (always ask, multi-select)

Always ask, even for early-stage projects — option 5 gives users an easy out, and prototypes benefit from knowing about logging or error tracking early. For CLI/library projects, the wording of option 1 adapts to "release & distribution."

> What production concerns matter for this project? Reply with comma-separated numbers:
>   1) Deployment & CI (Docker, GitHub Actions, Vercel, AWS, App Store/Play Store)
>      [for CLI/library, instead: Release & distribution (npm/crates.io/PyPI/Homebrew)]
>   2) Observability (logging, metrics, error tracking — Sentry, OpenTelemetry)
>   3) Security (auth patterns, secrets management, dependency scanning, OWASP)
>   4) Performance (profiling, optimization, caching)
>   5) Not in production yet / not applicable
>   6) Skip — handle these later

### Section 5.5 — Anything else? (loop until user opts out)

Before showing the final tally, give the user repeated chances to add anything the structured sections missed.

**First time, ask:**
> Anything specific you want skills for that I didn't cover? (e.g. a particular library, a workflow, documentation generation)
>
> Reply with the number, or describe what you need:
>   1) No, I'm good
>   2) Yes — I'll describe it

**After each item they add, ask again:** "Anything else, or are we good? (1 = good, 2 = add more)"

Continue looping until the user picks "good" (or says "no", "that's all", "done", etc.). For each item:

1. Search skills.sh using the bare-topic approach (see `REFERENCE.md` — "Search strategy").
2. Verify install counts.
3. Tell the user what you found — name, source, install count, one-line fit — before adding to the tally.
4. If you can't find a good match, say so honestly. Don't add a low-quality skill just to satisfy the request.

**Guardrails:**
- If the user lists 5+ items, pause: "Want to keep going, or save the rest for another run? (1 = continue, 2 = stop here)"
- If a user-suggested item duplicates something already in the tally, point that out instead of adding a second one.
- Treat ambiguous answers as a request for help — ask a clarifying follow-up or suggest a specific skill they can accept or reject.

### Section 6 — Confirm and install (always run)

Load `REFERENCE.md` now if you haven't already — you need the search strategy, ranking rubric, and the Claude Code flag rule.

For each picked concern, search skills.sh via `npx skills find <query>` using the project-type- and language-aware bare topic from `REFERENCE.md`. Rank by the criteria in `REFERENCE.md` ("Ranking"). Pick the top result per concern. If two are very close in score, surface both as a numbered choice.

Present the final list:
> Based on your answers, I'll install these skills into your agent's project skills folder:
>
>   1) **[skill-name]** by [author] — [one-line description] ([N] installs, [M] stars)
>   2) **[skill-name]** by [author] — [one-line description] ([N] installs, [M] stars)
>   ...
>
> Reply with the number:
>   1) Install all  ← recommended
>   2) Install all except specific ones (tell me which numbers to drop)
>   3) Swap one out (tell me which number and what to replace it with)
>   4) Cancel

On confirm, check whether this is a Claude Code project (see `REFERENCE.md` — "Agent detection"). Run `npx skills add <repo> --skill <name> -y` for each, adding `-a claude-code` only if it's Claude Code. Report what was installed.

### Section 7 — How to use these skills (offer after install)

> Want me to drop a quick 'How to use these skills' guide into the repo? It lists each installed skill, what it does, and how to invoke it.
>
> Reply with the number:
>   1) Yes, write HOW_TO_USE.md  ← recommended
>   2) Skip

If yes, create `HOW_TO_USE.md` in the agent's skills folder. See `REFERENCE.md` for the template and how to populate it from each skill's frontmatter.

## Option lists by project type

Use these in Section 3 ("Building it"). Pre-mark anything detected in the repo as recommended. Accept free-text answers and search for them.

**Web app:**
>   1) Frontend framework (React/Next, Vue/Nuxt, Svelte/SvelteKit, Solid, Angular)
>   2) Backend framework (Express, Fastify, FastAPI, Django, Rails, etc.)
>   3) Database / ORM (Postgres, Mongo, Drizzle, Prisma, SQLAlchemy, etc.)
>   4) UI / styling (Tailwind, shadcn/ui, styled-components, etc.)
>   5) Skip — let the agent figure it out per task

**Backend service or API:**
>   1) Web framework (FastAPI, Express, Gin, Actix, etc.)
>   2) Database / ORM
>   3) API style (REST, GraphQL, gRPC)
>   4) Message queue / event streaming (Kafka, RabbitMQ, Redis Streams)
>   5) Skip

**Mobile app:**
>   1) iOS native (SwiftUI / UIKit)
>   2) Android native (Jetpack Compose / Kotlin)
>   3) Cross-platform (React Native / Flutter / Expo)
>   4) Backend integration patterns (REST clients, GraphQL, offline-first sync)
>   5) Skip

**CLI tool or library:**
>   1) Framework / argument parsing (clap, click, cobra, commander, oclif)
>   2) Distribution & packaging (npm publish, crates.io, PyPI, Homebrew)
>   3) API design for libraries (semver, public surface, docs generation)
>   4) Skip

## Notes for the agent running this skill

- **The interview is the product.** Don't pad. A user with a clear project should finish in under 2 minutes (excluding any "anything else?" rounds they extend).
- **Show your work on rankings.** When picking between candidates, briefly say why ("Picked X over Y because 30k vs 800 installs and X is from the framework team").
- **Respect existing installs.** Run `npx skills list` before installing. Don't reinstall, don't override user-edited skills without asking.
- **Use `-a claude-code` only for Claude Code; otherwise omit `-a` entirely.** All other agents read from `.agents/skills/`, which `npx skills add` creates by default. Claude Code is the exception — it reads from `.claude/skills/`, which needs `-a claude-code`. Always include `-y` to suppress interactive prompts mid-install.
- **Loop "anything else?" until the user opts out.** Don't ask once and move on.
- **Search queries are project-type- and language-aware.** A "testing" pick for a Rust CLI is not the same query as "testing" for a React app. Always look up the right bare topic in `REFERENCE.md` based on what was picked in Section 1.
- **Always offer the usage guide.** Small step, makes installed skills discoverable to the team.
- **One-off discovery is fine mid-interview.** If the user asks "is there a skill for X" mid-flow, run a quick `npx skills find`, answer briefly, resume the interview.
- **When in doubt, skip the install.** Recommending a skill the user installs manually is fine; installing a wrong skill that pollutes the skills folder is annoying. Lean conservative.
