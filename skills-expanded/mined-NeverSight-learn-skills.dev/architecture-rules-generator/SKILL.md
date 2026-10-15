---
name: architecture-rules-generator
description: (NS) Scan a codebase and generate or refresh a lean architecture-rules.md constitution for AI agents — stack, layout, patterns, constraints, and pointers to deeper rules. Use whenever the user asks to generate architecture rules, create .nextstage-harness/rules/architecture-rules.md, bootstrap agent context, codify project conventions, document stack and module layout for agents, or set up always-on project rules — even if they say "document how this repo works for the AI" or "create rules the agent reads every session". Do NOT use for business/functional specs (codebase-reverse-spec), SDD brownfield maps (bootstrap-brownfield), or ad-hoc single-topic Cursor rules without a full architecture pass.
depends:
  - nextstage-harness
---

# Architecture Rules Generator

Produce **hot memory** for coding agents: a single always-loaded `{harness_root}/rules/architecture-rules.md` that encodes how this repository is structured and which constraints agents must not violate.

This is **not** a business spec (`codebase-reverse-spec`) or an SDD planning artifact (`bootstrap-brownfield`). It is the **constitution** — loaded every session, kept lean, written for machine consumption with explicit paths and do/don't rules.

## Design principles

1. **Agent-first** — file paths, entry points, forbidden zones, and test commands. A developer skimming prose is not the audience.
2. **Lean by default** — target **80–200 lines** (hard cap ~250). Depth belongs in scoped layer rules or `docs/`; this file routes to them.
3. **Evidence-based** — every rule must trace to something found in the repo. Mark `inferred` items; do not invent stack or patterns.
4. **Load-bearing** — agents trust this absolutely. Stale rules cause silent failures; prefer omission over guesswork.
5. **Separation** — universal architecture here; file-type or domain detail in sibling rules (`backend-rules.md`, `frontend-rules.md`, etc.).

See `references/compression-guide.md` when the draft exceeds the line budget.

## Harness discovery

See `../nextstage-harness/references/harness-discovery.md` and `../nextstage-harness/references/rules-sync.md`.

| Output path                                                     | When                                          |
| --------------------------------------------------------------- | --------------------------------------------- |
| `{harness_root}/rules/architecture-rules.md`                    | Default — canonical constitution              |
| `{product_root}/.nextstage-harness/rules/architecture-rules.md` | Monorepo product folder is the harness anchor |

Read `AGENTS.md` and existing `{harness_root}/rules/*.md` before scanning — reuse and link; do not duplicate sibling rules. Legacy: `.cursor/rules/*.mdc` only if `{harness_root}` is absent.

## When to use

| Trigger                                                      | Action                                    |
| ------------------------------------------------------------ | ----------------------------------------- |
| New repo / first agent setup                                 | **Generate** initial constitution         |
| Major stack or layout change                                 | **Refresh** in place                      |
| `architecture-rules.md` missing but other rules exist        | **Generate** and cross-reference siblings |
| User says rules are stale or agents keep making same mistake | **Refresh** targeted sections             |

## Workflow

### Step 1 — Anchor and baseline

1. Resolve `{harness_root}`, `{product_root}`.
2. Read `AGENTS.md`, existing `architecture-rules.md`, and list `{harness_root}/rules/*.md`.
3. Note gaps the user mentioned (if any) and whether this is **create** or **refresh**.

If the user did not specify scope, confirm once: whole repo vs `{product_root}` subtree.

### Step 2 — Reconnaissance

Follow `references/reconnaissance-checklist.md` and `references/stack-signals.md`. Read-only — do not modify application code.

Minimum scan:

1. Root manifests (`package.json`, `composer.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`, `docker-compose.yml`, etc.).
2. Directory tree (~2 levels under `{product_root}`).
3. Entry points (HTTP routers, `index.php`, `main.ts`, CLI commands, workers).
4. Module/domain folders and **generated** or **build** directories (never-edit zones).
5. Test layout and how tests are run (scripts, Docker, CI snippets).
6. Existing docs under `docs/`, `.nextstage-harness/docs/`, `README.md`.

**Checkpoint (recommended):** Present a short recon map (stack, layout, modules, generated zones, test command) and ask the user to confirm or correct before drafting. Skip only on explicit autonomous run.

### Step 3 — Extract architecture facts

Turn evidence into agent-actionable rules:

| Category       | What to capture                                                                                                      |
| -------------- | -------------------------------------------------------------------------------------------------------------------- |
| **Scope**      | Product root, monorepo vs standalone, where specs and agent assets live                                              |
| **Stack**      | Languages, frameworks, DB, cache, queue, local URLs/ports when discoverable                                          |
| **Layout**     | Folder tree (abbreviated), module boundaries                                                                         |
| **Patterns**   | API style, multitenancy, auth, module conventions, integration boundaries                                            |
| **Forbidden**  | Generated dirs, migration constraints, secrets locations                                                             |
| **Dev & test** | Docker services, **test container name**, copy-pasteable test commands (behavioral rules stay in `AGENTS.md`) |
| **Discipline** | Language for code/docs vs user chat, minimal diff, completion style — only if present in repo rules or `AGENTS.md`   |

For large subsystems, **do not inline** — add one line pointing to a dedicated layer rule and offer to generate that sibling in a follow-up.

### Step 4 — Draft the constitution

Use `references/architecture-rules.template.md` as the skeleton.

**No YAML frontmatter** in the canonical file — adapter metadata lives in `.nextstage-harness/manifest.json`.

Writing rules:

- Prefer tables and bullet lists over paragraphs.
- Use **MUST / MUST NOT** only for constraints that prevent real breakage; explain _why_ in a few words when non-obvious.
- End with **Key references** — table mapping topic → file path (specs, sibling rules, `AGENTS.md`).
- English only in the output file.

Run the compression pass (`references/compression-guide.md`) before writing.

### Step 5 — Write, sync, and report

1. Write `{harness_root}/rules/architecture-rules.md` (or `{product_root}/.nextstage-harness/rules/...`).
2. Ensure `architecture-rules` exists in `.nextstage-harness/manifest.json` with `cursor.alwaysApply: true` and `claude.paths: null`.
3. Run `npx @nextstage-brasil/harness sync` (or instruct the user to run it) to regenerate adapters.
4. Do **not** modify application source unless the user explicitly asked.
5. Report briefly (3–6 bullets): what was detected, line count, new vs updated sections, suggested sibling rules still missing.

If a previous `architecture-rules.md` existed, mention what was removed, merged, or deferred to other files.

## Refresh mode

When updating an existing file:

1. Preserve stable sections the user may have hand-edited (communication locale, GitLab MCP server name, protected branches) unless recon proves them wrong.
2. Replace stack/layout/modules from current evidence.
3. Drop rules that no longer match the codebase; add a `## Changelog` comment block at the bottom only if the user asked for audit trail — otherwise omit.

## Quality bar (self-check before save)

- [ ] Canonical file has no YAML frontmatter
- [ ] `manifest.json` has `architecture-rules` with `alwaysApply: true`
- [ ] Line count ≤ 250 (ideally ≤ 200)
- [ ] Every stack row verified from manifests or config
- [ ] Generated/forbidden paths listed if they exist
- [ ] Test command is copy-pasteable when Docker/CI is detected
- [ ] When a separate test container/service exists, constitution documents the test service name and commands (not dev container or host)
- [ ] No duplication of full content from sibling rules — links only
- [ ] No business-domain rules (those belong in `docs/specs/`)
- [ ] `harness sync` run or user instructed to run it

## Related skills

- `bootstrap-brownfield` — `brownfield-map.md` for SDD planning (broader, planning-oriented)
- `codebase-reverse-spec` — technology-agnostic **business** behavior
- `nextstage-harness` — artifact paths and gate conventions
