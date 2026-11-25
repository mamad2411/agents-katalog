---
name: agent-context
description: >-
  Create, validate, and maintain a structured .agent-context directory for a
  repository so AI agents navigate the codebase efficiently and make
  higher-quality decisions. Use when setting up agent context for a new repo,
  updating context after agent work, or catching up context after human work.
metadata:
  version: "0.5.1"
---

# Agent Context

Create, validate, and maintain a structured `.agent-context/` directory for a
repository. This is the single most impactful thing you can do to improve how
AI agents work on a large codebase.

## How It Works — The Big Picture

### What gets created

A `.agent-context/` directory in the repo root with three layers:

- **Content** (5 markdown files) — architecture, code map with risk ratings, change checklists with explicit file paths, silent failure modes, operations. Readable by humans and all agents.
- **Authority** (3 JSON files) — task routing, completeness contracts ("these files MUST be in your answer"), reporting rules. This layer is what makes the pack worth loading: a task route leads to a contract and a scoped search.
- **Navigation** (1 JSON file) — search scopes ("search HERE, not THERE"), verification shortcuts with line ranges. Used by Codex, Cursor, and similar agents that verify everything against code.

Plus a short managed routing block in `AGENTS.md` (the canonical route) and a literal `@AGENTS.md` import in `CLAUDE.md`, so every agent reads the pack before opening repo files.

### Pack shape (tiers)

Always build the full pack (tier 3, 11 files). It is the default for `init` and the only shape new packs should use. A small repo simply fills fewer routes, contracts and reporting rules; the verifier still checks that every reference resolves.

| Tier | Files | Status |
|------|-------|--------|
| **Tier 3** (full) | all 5 markdown + `manifest.json` + `acceptance_tests.md` + authority layer (`routes.json`, `completeness_contract.json`, `reporting_rules.json`) + `search_scope.json` | **Default.** Build this. |
| **Tier 2** (standard) | `00_START_HERE.md`, `20_CODE_MAP.md`, `30_BEHAVIORAL_INVARIANTS.md`, `manifest.json`, `acceptance_tests.md`, `search_scope.json` | Deprecated for new packs (0.5.0 warns, 0.6.0 removes). Existing packs stay supported. |
| **Tier 1** (minimal) | `20_CODE_MAP.md` + `search_scope.json` | Deprecated for new packs. Little more than grep for a current agent. |

If using the CLI: `agent-context init --install-hook .` (tier 3). When asked to **promote** an existing tier 1-2 pack, add the missing templates from `templates/` by hand, fill them, then run `agent-context routing .` and `verify .`. Never use `init --force` on a filled pack.

### First time setup

You ask an agent: **"set up agent context for this repo"**

The agent reads the entire repo, fills the pack files describing the architecture, key paths, change patterns, and search boundaries, copies the helper tools, installs the advisory freshness hook when safe, validates everything, runs acceptance tests with grep verification, and commits. Takes ~15-20 minutes for a large repo.

After merge, **every agent that opens a session in the repo** automatically reads the routing block and follows the pack. No per-developer setup. No configuration. It just works.

### Ongoing — when agents do the work

When an agent finishes work and opens a PR, it automatically includes `.agent-context` updates as a **separate commit**. The agent knows what it changed, so it patches only the affected sections — a new CODE_MAP entry, an updated checklist row, shifted line numbers in verification shortcuts.

**Reviewers see code changes and context updates as separate commits** in the same PR. Easy to review, easy to revert independently.

### Ongoing — when humans do the work

When humans merge code without using agents, the agent context gradually goes stale. A pre-push hook warns about this (advisory only, never blocks).

When ready, anyone can ask an agent: **"update the agent context"**

The agent diffs since the last validation, reads each changed file, and proposes the minimal edit per section. **You approve each change** — the agent never overwrites context it didn't write. This takes 2-5 minutes.

### Ongoing — mixed work

In practice, most teams have a mix:
- Agents handle routine work → context updates automatically in the PR
- Humans handle sensitive/creative work → periodic catchup when context drifts
- Pre-push hook catches the gap → you decide when to update

### What the agent touches — and never touches

| Touches | Never touches |
|---|---|
| `.agent-context/` (pack files + helper tools) | Source code (no modifications without approval) |
| `CLAUDE.md` / `AGENTS.md` / `GEMINI.md` / `.cursorrules` (routing blocks only) | Human-authored PRs (agent stays silent) |
| `.git/hooks/pre-push` (advisory freshness check, when no unmanaged hook blocks safe install) | Secrets or credentials |

### When to use it — and when not to

| Repo size | Recommendation |
|---|---|
| <50 files, simple structure | **Skip** — agents can scan everything efficiently |
| 50-200 files, 2-3 subsystems | **Recommended** — the full pack with a few routes gives measurable quality and efficiency gains |
| 200+ files, complex architecture | **Strongly recommended** — routed contracts prevent silent failures, cut token cost 50-70% |

---

## When to Use

- **Create**: first time setting up agent context for a repo (>50 files or >3 subsystems)
- **Update (agent PR)**: agent opens a PR — prep `.agent-context` updates as a separate commit
- **Update (catchup)**: significant human work merged — agent diffs and proposes patches

## Trigger Phrases

- "set up agent context for this repo"
- "set up agent context"
- "create agent-context for this repo"
- "update the agent context"
- "refresh the agent context"

## Prerequisites

- Git repository with at least one commit
- For update triggers: existing `.agent-context/` directory with a validated pack

---

## Flow: Create

### Step 1 — Assess

Check whether agent context is warranted:

```bash
git ls-files | wc -l
```

- **>50 files or >3 top-level source directories**: proceed.
- **<50 files, simple structure**: warn the user that agent context may add overhead without benefit. Proceed only if they confirm.

Check for an existing pack:

```bash
ls .agent-context/current/ 2>/dev/null
```

- If exists and validated: ask whether to update (use the Update flow) or reinit from scratch.
- If exists but empty/scaffolded: proceed with filling.
- If missing: proceed with full init.

### Step 2 — Scaffold

Prefer the CLI because it copies helper tools, writes routing blocks, and can install the advisory freshness hook:

```bash
agent-context init --install-hook .
```

If the CLI is unavailable, create the directory structure manually:

```bash
mkdir -p .agent-context/current .agent-context/tools
```

Create these files:
- **Markdown files** in `.agent-context/current/` — start from the starter templates in `templates/` (00_START_HERE.md, 10_SYSTEM_OVERVIEW.md, 20_CODE_MAP.md, 30_BEHAVIORAL_INVARIANTS.md, 40_OPERATIONS_AND_RELEASE.md). Remove all `REPLACE:` guidance text after filling.
- **JSON artifacts** in `.agent-context/current/` — start from the starter templates in `templates/` (routes.json, completeness_contract.json, reporting_rules.json, search_scope.json). The templates include inline `_rules` that define the format contract for each file. Remove `_rules` and `_EXAMPLE` entries after filling.
- **Manifest** in `.agent-context/current/manifest.json` — use the template in `templates/manifest.json`. Fill `repo`, `git_revision` (from `git rev-parse HEAD`), and `generated_at` (ISO 8601 UTC).
- **Acceptance tests** in `.agent-context/current/acceptance_tests.md` — use the template from `templates/acceptance_tests.md`. Fill during Step 7.
- **Helper tools** in `.agent-context/tools/` — copy `tools/verify_agent_context.py`, `tools/check_freshness.sh`, and `tools/pre-push-hook.sh`. These are the canonical machine-checkable validator, freshness checker, and advisory local hook used by the reference CI and hook examples.
- **Routing files:** use one canonical `AGENTS.md` and a `CLAUDE.md` managed block containing the literal, unfenced `@AGENTS.md` import. Preserve unmanaged instructions and host-specific notes. Shared project rules belong in AGENTS.md; resolving conflicting handwritten rules requires maintainer review.

The CLI defaults to this canonical layout. For an existing filled pack, use
`agent-context routing .` to update managed routing without overwriting pack content.
Do not use `init --force` to migrate a filled pack: it replaces templates.
Only modify repositories whose maintainers authorized the change.

The shared route for a full pack: start-here and invariants, then the selected `routes.json` read order and named patterns; load completeness/search/reporting contracts and consult the code map before source inspection. Do not eagerly load unrelated routes.

For existing legacy packs the route only references files the pack ships (`routing` infers the tier from the files on disk, the same way `verify` does):
- Tier 2: start-here, invariants, code map and search scope.
- Tier 1: code map, search scope, then bounded source inspection.

If scaffolding manually, use these same rules in the canonical managed block and
keep the CLAUDE adapter to the import. Do not copy whole policy bodies into adapters.
Existing `.cursorrules` can point to AGENTS.md; the default does not create one.
In canonical mode a `GEMINI.md` that already carries a managed block is refreshed to
point at AGENTS.md, so no legacy per-agent policy survives; a handwritten `GEMINI.md`
without a managed block is left alone, and a new one is created only with
`--include-gemini`. Provider support is a repository-maintainer choice.
`--layout per-agent` retains the legacy provider-specific generation for compatibility.

Review symlinks, hard links, malformed managed markers and unknown ownership before
migration. The CLI refuses ambiguous targets instead of overwriting linked policy.

### Step 3 — Inventory

Before writing any content, mechanically enumerate the repo's subsystems. This prevents the most common pack failure: deep coverage of a few subsystems while others are silently omitted.

1. **List all significant source directories** — find every directory under the main source root(s) that contains >3 files:

```bash
# Adapt the root paths (app/, src/, lib/, etc.) to the repo
find app/ -mindepth 1 -maxdepth 2 -type d -exec sh -c 'echo "$1 $(find "$1" -maxdepth 1 -name "*.py" -o -name "*.ts" -o -name "*.go" | wc -l)"' _ {} \; | awk '$2 > 3'
```

2. **List all distinct data store and external integration patterns** — scan imports for database clients, SDKs, and external service connectors:

```bash
grep -rn "import.*sqlalchemy\|import.*pynamodb\|import.*databricks\|import.*elasticsearch\|import.*redis\|import.*boto3\|import.*openai\|import.*mlflow" app/ --include="*.py" -l | head -30
```

3. **Produce a subsystem inventory** — a flat list with one line per subsystem:

| Directory | File count | Data store / integration | Covered in pack? |
|---|---|---|---|
| (one row per significant directory) | | | (fill after Step 4) |

This inventory is your **coverage checklist**. After filling the pack, every row must appear in at least one pack file (system overview, code map, behavioral invariants, search scope, or completeness contract). If you choose not to cover a subsystem in detail, list it in a "Not covered in detail" section in `00_START_HERE.md` so agents know it exists.

### Step 4 — Fill content layer (markdown)

Read the repo structure and fill each markdown file. Use the inventory from Step 3 to ensure breadth. Follow this order:

1. **00_START_HERE.md**: Fill Fast Facts (product, languages, quality gate, core risk, version). Fill Scope Rule. Fill Stop Rules based on repo patterns.

2. **10_SYSTEM_OVERVIEW.md**: Fill Product Shape, Runtime Architecture (3-5 steps), Silent Failure Modes (any code path where failure produces no error), Command/API Surface table, Tracked Path Density.

3. **20_CODE_MAP.md**: Identify 8-15 high-impact paths, **with at least one path per major subsystem in the inventory**. If the repo has >8 subsystems, prioritize breadth over depth — cover each subsystem at least once rather than covering 5 subsystems deeply. For each path: what it does, why it matters, risk level, authority (authoritative/derived/reference). Fill Quick Lookup Shortcuts (4-6 patterns). Fill Cross-Cutting Tracing Flows for changes that ripple through multiple files. Fill Extension Recipe.

4. **30_BEHAVIORAL_INVARIANTS.md**: Write 3-8 testable invariants. **Before asserting any universal rule** (words like "every", "all", "must", "always"), search the repo for counter-examples using grep. If counter-examples exist, qualify the invariant (e.g., "Snowflake CRUDs extend BaseCRUD" not "every CRUD extends BaseCRUD"). Fill Update Checklist with one row per common change type — explicit file paths, not descriptions (P7). Identify File Families (glob pattern, member count, report-as-family or enumerate) — verify member counts with `git ls-files | grep ... | wc -l`. Write Negative Guidance (what NOT to do — common over-exploration patterns).

5. **40_OPERATIONS_AND_RELEASE.md**: Fill validation commands, CI checks, release flow, agent context maintenance.

### Step 5 — Fill authority layer (JSON)

> Skip this step only when updating an existing legacy tier 1-2 pack that you have not been asked to promote.

Fill the structured JSON artifacts with repo-specific content:

1. **routes.json**: Verify the default task routes make sense for this repo. Add `named_patterns` for repo-specific lookup and change patterns.

2. **completeness_contract.json**: For each common change type, fill `contractually_required_files` with explicit file paths and `required_file_families` with glob patterns. These are the files that MUST appear in an impact analysis answer. **Include at least one contract entry per subsystem in the inventory that has a distinct change pattern.** If a subsystem is too simple for its own contract, fold it into a broader contract and note it in the description.

   **Pattern format rules:**
   - `contractually_required_files` — exact paths only (e.g., `app/api/v1/endpoints/v1.py`)
   - `required_file_families` — valid shell globs using `*` wildcards (e.g., `app/api/v1/endpoints/*.py`, `tests/unit/crud/test_*.py`)
   - Template variables like `{name}` or `{domain}` are **NOT valid glob patterns** and must NOT be used. They will not resolve against the repo and will silently weaken the contract.
   - Every glob pattern must match >=1 real file — verify with `ls` or `git ls-files` before finalizing.

   Example of a correctly filled contract entry:
   ```json
   "add_endpoint": {
     "description": "Adding a new API endpoint",
     "contractually_required_files": ["src/routes/index.ts"],
     "required_file_families": ["src/routes/*.ts", "src/handlers/*.ts", "tests/routes/test_*.ts"]
   }
   ```

3. **reporting_rules.json**: Fill `groupable_families` (homogeneous file sets to report as family, not individually). Fill `never_enumerate_individually` (derived/generated files). Fill `authoritative_vs_derived_paths` in global rules.

4. **search_scope.json**: For each task family, fill `search_directories` (where to look), `exclude_from_search` (where NOT to look), and `verification_shortcuts` (specific file + line range or function name for quick checks).

### Step 6 — Validate

Validate the pack before committing. Run **all** of these checks:

**Structural checks:**
- All markdown files present and non-empty (no unfilled template markers)
- All structured artifact file references resolve on disk
- Grouped families don't point to generated files as authoritative edit targets
- `.agent-context/tools/verify_agent_context.py`, `.agent-context/tools/check_freshness.sh`, and `.agent-context/tools/pre-push-hook.sh` exist if you copied the helper tools

**Semantic checks:**
- Every `required_file_families` glob pattern matches >=1 real file (run each glob and verify)
- Every `contractually_required_files` path exists on disk
- No template variables (`{name}`, `{domain}`, etc.) remain in any JSON artifact
- Every invariant in `30_BEHAVIORAL_INVARIANTS.md` that uses universal language ("every", "all") has been verified against at least one counter-example search
- File family member counts (e.g., "~25 files") are within +-20% of actual `git ls-files` count
- Every `verification_shortcuts` `look_for` string actually appears in the referenced file

**Routing checks:**
- AGENTS.md contains the shared tier-appropriate route and only references files the pack ships.
- CLAUDE.md contains a literal, unfenced `@AGENTS.md` import, not a prose promise to read it.
- Existing adapters agree with the canonical route; legitimate host-specific notes and unmanaged text survive.
- Re-running `agent-context routing .` is a no-op and does not change the filled pack.
- Verify actual instruction loading in supported hosts when adopting a layout; structural verification does not prove runtime loading.

**Coverage check** (against the Step 3 inventory):
- Every source directory with >3 files in the inventory is referenced in at least one pack file
- If any significant directory is absent from all pack files, either add coverage or list it in the "Not covered in detail" section of `00_START_HERE.md`

**Preferred machine check:**
- Run `python3 .agent-context/tools/verify_agent_context.py` from the repo root and make sure it exits 0 before committing. The shipped verifier checks the machine-checkable subset above, including a lightweight coverage heuristic.

Fix any validation errors before proceeding.

### Step 7 — Acceptance test

Run a structured acceptance test against the pack. This is not a self-assessment — it requires verifying pack answers against actual code using grep. The test catches gaps that structural validation cannot: missing subsystems, understated blast radius, and cross-cutting blind spots.

**Generate 4 test questions** that span these categories:

1. **Lookup** — find a specific config value, function location, or integration point. Pick something from a subsystem the pack covers lightly, not one of the top code map entries.
2. **Impact analysis** — list all files that must change for a common modification. Pick a change type that touches >=2 subsystems.
3. **Cross-cutting impact** — map the blast radius of a change that spans 3+ subsystems. Good candidates: auth/identity changes, config/env variable changes, shared utility changes, data store migrations. This is the most important test — it catches the deep-but-narrow failure mode.
4. **Diagnosis** — trace a runtime failure to its root cause. Pick a failure that involves an external integration (database, API, cache, file storage).

**For each question, follow this protocol:**

1. Answer using ONLY the agent context files (no source code).
2. Verify the answer by grep-searching the actual codebase.
3. Score:
   - **Files identified by pack** vs **files found by grep** (the coverage ratio)
   - **False positives** — files the pack pointed to that turned out irrelevant
   - **False negatives** — files grep found that the pack missed entirely

**Pass criteria:**

- Lookup and diagnosis: pack must point to the correct starting files
- Impact analysis: pack must surface >=80% of files in the real change set
- Cross-cutting: pack must surface >=80% of core infrastructure files in the blast radius. Downstream files found via grep guidance (e.g., "grep for X across Y/") count as surfaced.
- No test should send the agent to the wrong subsystem entirely

**If any test fails**, improve the relevant pack section (add missing paths to code map, add a contract, add a search scope family, add an invariant) and re-run that test. Iterate until all 4 tests pass.

**Record the test results** in `.agent-context/current/acceptance_tests.md` using the template from `templates/acceptance_tests.md`. This file is committed with the pack so reviewers can see what was tested and how the pack scored.

### Step 8 — Adapt to existing repo automation

Before adding any new workflow file, inspect the repo's existing automation and adapt the agent-context checks into it.

1. **Inspect existing workflows first**:
   - List `.github/workflows/*.yml`
   - Identify which workflow already gates pull requests against the default branch
   - Prefer patching that workflow instead of creating a second competing CI workflow

2. **Reuse the repo's runtime setup**:
   - If the repo already installs Python/Node/uv/pnpm/etc. in CI, reuse that setup
   - Add the agent-context verification step after checkout and dependency/runtime setup
   - Do NOT introduce a different runtime path just for agent-context if the repo already has one

3. **Infer `CONTEXT_RELEVANT_PATHS` from the repo's real source roots**:
   - Start from the actual top-level source directories in the repo
   - Include directories the pack explicitly claims to cover in `00_START_HERE.md`
   - Exclude generated artifacts and vendored dependency directories

4. **Choose integration strategy**:
   - If there is an existing PR workflow: patch it
   - If there is no suitable PR workflow: create a dedicated workflow using `docs/references/ci-example.yml`
   - If CI cannot be changed safely in the current task: document the exact follow-up in `40_OPERATIONS_AND_RELEASE.md`

5. **Record the adaptation**:
   - In `40_OPERATIONS_AND_RELEASE.md`, state which workflow file was patched (or created)
   - Record the chosen `CONTEXT_RELEVANT_PATHS`

See `docs/ci-adaptation.md` for repo-adaptation heuristics and examples.

### Step 9 — Set up CI enforcement

Set up both local advisory freshness and CI verification before treating the pack as production-ready.

**Local advisory hook:**

```bash
agent-context install-hook .
```

Expected outcomes:
- If there is no existing hook, `.git/hooks/pre-push` is installed and calls `.agent-context/tools/pre-push-hook.sh`.
- If a managed agent-context hook already exists, it is updated in place.
- If an unmanaged pre-push hook already exists, it is preserved and a `pre-push.agent-context.sample` chain block is written. Document the follow-up in `40_OPERATIONS_AND_RELEASE.md` or manually merge the block into the repo's hook chain.

The hook is advisory only: it warns when context-relevant paths changed without `.agent-context/` changes, but never blocks a push.

**CI enforcement:**

Add an `agent-context` verification check to your PR workflow. This is **not required for the initial pack commit**, but should be set up before the pack is treated as production-ready.

The CI check should:
- verify the machine-checkable subset of pack integrity
- fail when context-relevant code changes without a corresponding pack update
- run on pull requests against your main branch

A reference CI job is provided in `docs/references/ci-example.yml`. The advisory pre-push hook is provided in `tools/pre-push-hook.sh` and copied into `.agent-context/tools/` by `init`.

If CI enforcement cannot be set up immediately, document it as a follow-up in `40_OPERATIONS_AND_RELEASE.md` so the gap is visible.

### Step 10 — Commit

```bash
git add .agent-context/ AGENTS.md CLAUDE.md
# Stage optional adapters only when they exist and their changes were reviewed.
git commit -m "feat: add agent context (.agent-context)"
```

---

## Flow: Update (Agent PR)

When you are an agent that has just completed work and is preparing a PR:

1. **Determine what changed** — review your own work: which files did you create, modify, or delete?
2. **Map changes to agent context sections** — is it in CODE_MAP? Does it affect a checklist row in BEHAVIORAL_INVARIANTS? Does it shift line numbers in search_scope.json verification shortcuts? Is it a new file that should be added to a completeness contract?
3. **Patch only affected sections** — do not rewrite entire files
4. **Re-validate** — check all file references still resolve, contracts match real files
5. **Commit separately**: `git commit -m "chore: update agent context for <change>"`

The context update must be a **separate commit** from the code changes. This lets reviewers assess them independently and revert the context update without reverting the code.

---

## Flow: Update (Manual Catchup)

When a human asks you to update the agent context after significant changes were merged without agent involvement:

1. **Find what changed since last validation**:

```bash
# Find when the pack was last validated
LAST_VALIDATED=$(jq -r '.generated_at' .agent-context/current/manifest.json)

# Show what changed since then
git log --oneline --since="$LAST_VALIDATED" -- . ':!.agent-context'
git diff $(git log -1 --before="$LAST_VALIDATED" --format=%H)..HEAD --stat -- . ':!.agent-context'
```

2. **Propose patches** — for each changed area, state what changed in the code, which agent context section is affected, and show the specific before/after edit. Ask the user to approve or reject each section.
3. **Wait for approval** — do NOT apply changes without approval. The user authored this code — you may misunderstand the intent.
4. **Apply approved patches and re-validate** — check all references still resolve after changes.

```bash
git add .agent-context/
git commit -m "chore: catchup agent context with recent changes"
```

---

## Quality Bar

Agent context is ready when:

- Validation passes — all structural, semantic, routing, and coverage checks from Step 6 pass
- Every markdown file has content (no unfilled template markers)
- Every JSON artifact has at least some repo-specific entries (no all-empty arrays)
- No template variables (`{name}`, `{domain}`) remain in any JSON artifact
- Every completeness contract glob matches >=1 real file
- Every invariant with universal language has been verified against counter-examples
- Acceptance test passes: 4 tests (lookup, impact, cross-cutting, diagnosis) all meet pass criteria, results committed in `acceptance_tests.md`
- AGENTS.md is the shared route; CLAUDE.md imports it literally and all mandatory references exist for the selected tier.
- 00_START_HERE.md gives a coherent mandatory read order consistent with the generated route.
- Entry files stay short; detailed context remains in the task-routed pack.
- Every significant subsystem from the Step 3 inventory is referenced in at least one pack file, or listed in "Not covered in detail" in `00_START_HERE.md`
- CODE_MAP has at least one path per major subsystem in the inventory
- CI enforcement is either set up or documented as a follow-up in `40_OPERATIONS_AND_RELEASE.md`
- The advisory pre-push hook is installed, updated, or explicitly documented as a follow-up when an existing unmanaged hook prevents safe automatic installation

## What NOT to Do

- Do not create agent context for repos with <50 files unless the user explicitly asks
- Do not touch actual repo source files — only `.agent-context/`, `CLAUDE.md`, `AGENTS.md`, `GEMINI.md`, `.cursorrules`
- Do not auto-update the agent context on human-opened PRs — you lack the context of why changes were made
- Do not rewrite the entire pack on updates — patch only affected sections
- Do not include secrets, credentials, or sensitive configuration in the agent context
- Do not add the agent context to `.gitignore` — it is meant to be committed and shared
- Do not use template variables (`{name}`, `{domain}`) in JSON artifacts — use `*` glob wildcards
- Do not assert universal invariants ("every X does Y") without searching for counter-examples first
- Do not recreate separate agent-specific policy bodies when the repository uses canonical routing.
- Do not claim file counts without verifying against `git ls-files`
- Do not start writing pack content before completing the subsystem inventory (Step 3) — enumerate first, narrate second
- Do not concentrate CODE_MAP paths in a few subsystems while leaving others uncovered — breadth matters more than depth for large repos

## Evidence

Tested across 3 repo types (ML pipeline, CLI library, React frontend), 7 experiment runs, 78+ graded results:

- Answer quality: 50% -> 88% correct
- Claude efficiency: -70% files opened, -65% tokens, zero dead ends
- Risk elimination: 0 production-risk answers with agent context (was 7 without)
- Templates are general-purpose — zero modifications needed across repo types
- Real-world feedback led to P16: routing wording must be imperative, not suggestive

Full evidence: [`docs/evidence/`](docs/evidence/)
Design principles: [`docs/design-principles.md`](docs/design-principles.md)
Architecture: [`docs/architecture.md`](docs/architecture.md)
