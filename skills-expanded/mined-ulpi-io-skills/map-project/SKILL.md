---
name: map-project
version: 2.1.0
description: |
  Refresh a SINGLE app's durable AI context — a thin `CLAUDE.md` router over discovered reference docs so
  future sessions start knowing the repo without paying for stale guesswork. Detects the framework shape,
  discovers the real routes, exports, flows, and subsystems from code, rewrites the imported references,
  then keeps `CLAUDE.md` compact and always-loaded. User-only maintenance workflow that mutates durable
  project memory: every claim is GROUNDED in the real codebase, never invented, and human-authored rules are
  preserved rather than overwritten. Use to initialize or refresh one app's context map after meaningful
  changes.
allowed-tools:
  - Read
  - Edit
  - Write
  - Glob
  - Grep
  - Bash
user-invocable: true
argument-hint: "[project scope or refresh target]"
arguments:
  - request
when_to_use: |
  Use when the user explicitly asks to refresh project memory, sync `CLAUDE.md` with the real codebase, or
  regenerate the context map after meaningful architecture changes — "/map-project", "update CLAUDE.md for
  this repo", "refresh the docs after the refactor". Do NOT use on a Cargo workspace or package monorepo
  (use map-project-monorepo), and do NOT run proactively after routine edits — it mutates durable project
  memory, so it is user-only. It maps what IS; it does not legislate coding rules.
---

<EXTREMELY-IMPORTANT>
This skill mutates durable project memory. Non-negotiable rules:
1. Detect the actual framework shape before writing anything.
2. Perform real codebase discovery before updating `CLAUDE.md` or reference docs.
3. Prefer updating existing project documentation over replacing it wholesale.
4. Keep generated memory compact enough to stay useful in Claude's context budget.
5. Do not run this skill PROACTIVELY on your own initiative (it mutates durable project memory) — only
   on explicit user intent, OR when an explicit user-invoked workflow composes it (e.g. `/ship-playbook`
   refreshing the map after a build).
</EXTREMELY-IMPORTANT>

# Map Project

## Inputs

- `$request`: Optional target scope or refresh note such as `api only`, `after auth refactor`, or `update the docs for the Next.js app`.

## Goal

Refresh `CLAUDE.md` and the imported reference docs so they describe the real project instead of stale, generic, or partial patterns.

## Step 0: Resolve scope and detect the project shape

Determine:

- whether the user wants a full refresh or a scoped refresh
- which primary framework or project shape is active
- whether the repo is a single app or a monorepo with one primary app surface
- which existing memory files already exist and should be updated rather than recreated

Load `references/framework-discovery.md` for:

- framework detection order
- framework-specific discovery requirements
- inventory expectations

Stop early if:

- the repo shape cannot be identified
- the requested scope is too vague to know which memory files to update

**Success criteria**: The project shape and documentation scope are explicit before discovery starts.

## Step 1: Perform exhaustive discovery before writing

Use framework-appropriate discovery to inventory the real codebase:

- routes, screens, or handlers
- exports, models, services, hooks, modules, or packages
- stateful entities and lifecycle flows
- public surfaces such as API routes, CLI entry points, or package exports
- key subsystems and their integration boundaries
- the capabilities the repo itself provides: project-committed skills (`.claude/skills/`) and enabled
  MCP servers (`.mcp.json` / `.claude/settings*.json`)

Rules:

- do not trust memory or old docs; verify from code
- collect counts where the reference contract expects coverage
- search for actual implementation examples to ground the guides
- if the repo is partially documented already, verify and extend instead of rewriting blindly

Load `references/framework-discovery.md` and complete the discovery steps for the detected project shape.
Load `references/skills-and-mcp.md` for skill/MCP discovery sources and redaction rules.

**Success criteria**: You have enough concrete inventory to document the project without placeholders or guesswork.

## Step 2: Update the reference files first

Refresh or create the imported reference files from discovered reality:

- exports or API-surface reference
- development guide
- architecture reference

Load `references/output-contract.md` for:

- required files
- required sections per file
- framework-specific section expectations
- line-budget targets

Writing rules:

- use real project examples, not generic templates
- prefer concise tables over repetitive prose
- document patterns the agent will actually need during implementation
- keep each file focused and avoid duplicating the same content across files

**Success criteria**: The reference files reflect the real codebase and stay within useful size limits.

## Step 3: Update `CLAUDE.md` as the thin entrypoint

Treat `CLAUDE.md` as the compact router:

- import the detailed reference files
- keep only the high-signal quick reference and project-level guidance inline
- do not duplicate large tables or walkthroughs that now live in the imported files
- include a compact, INLINE "Available Skills & MCP — prefer these" section, plus a one-line pointer at
  the very top of `CLAUDE.md`, so future agents use the repo's skills and MCP servers instead of
  forgetting them — this stays in `CLAUDE.md` itself, never an imported reference, because only
  always-loaded text changes behavior

Rules:

- preserve existing checked-in project guidance unless discovery proves it stale or wrong
- do not erase useful human-authored conventions just because they are not part of the generated structure
- make the quick reference actually help agents choose the right imported file

Load `references/output-contract.md` for the expected `CLAUDE.md` shape.
Load `references/skills-and-mcp.md` for the "Available Skills & MCP" section format and discovery sources.

**Success criteria**: `CLAUDE.md` becomes the compact, accurate entrypoint to the refreshed project memory.

## Step 4: Verify coverage, budget, and usefulness

Validate the refresh before declaring completion:

- required files exist
- expected sections are present
- documented coverage is high enough for the chosen project shape
- line budgets remain sane
- there is no obvious duplication between `CLAUDE.md` and imported files
- an implementation agent could plausibly find routes, exports, and workflow guidance from the refreshed docs

Load `references/output-contract.md` for the verification gates and budget rules.

If verification fails:

- tighten the docs
- restore missing sections
- remove duplication
- improve coverage using the discovery inventory

**Success criteria**: The refreshed memory is compact, grounded, and genuinely useful to future agents.

## Step 5: Report what changed

Summarize:

- detected project shape
- files created or updated
- coverage or inventory highlights
- budget status
- any areas still intentionally undocumented or deferred

Do not claim a perfect refresh if the repo has large blind spots or mixed-framework complexity that was intentionally scoped down.

**Success criteria**: The user gets a clear summary of what project memory was refreshed and how complete it is.

## Guardrails

- Do not use this skill PROACTIVELY (it mutates durable project memory) — run it only on explicit user
  intent or when an explicit user-invoked workflow composes it (e.g. `/ship-playbook`). It is no longer
  `disable-model-invocation`, so workflows can call it; that is not license to run it unprompted.
- Do not add `context: fork`; this workflow writes into the active repository.
- Do not add `paths:`; this is a generic maintenance skill.
- Do not overwrite useful human-authored project rules without evidence they are stale.
- Do not keep framework discovery matrices or file-contract encyclopedias inline in `SKILL.md`.
- Do not bloat `CLAUDE.md`; keep large detail in imported references.
- Do not mark the refresh complete without verification.

## When To Load References

- `references/framework-discovery.md`
  Use for framework detection order, framework-specific discovery steps, and inventory expectations.

- `references/output-contract.md`
  Use for required output files, required sections, line budgets, and verification rules.

- `references/skills-and-mcp.md`
  Use to discover the repo's project skills and MCP servers and render the inline "Available Skills &
  MCP — prefer these" section into `CLAUDE.md`.

## Output Contract

Report:

1. detected project shape and scope
2. files created or updated
3. coverage or inventory summary
4. budget and verification result
5. deferred or intentionally skipped areas
