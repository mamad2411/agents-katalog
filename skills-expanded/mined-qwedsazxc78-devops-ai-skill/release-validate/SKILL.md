---
name: release-validate
description: >
  Validates package release readiness across version consistency, cross-platform
  link integrity, npm package content, setup script smoke testing, skill
  fixture suite runs (Phase 4), shell portability static checks (Phase 5),
  cross-repo-style fixture coverage (Phase 6, shipped in v1.15.0), cross-AI-tool
  registration parity (Phase 7, shipped in v1.15.0), and release artifact generation
  (Phase 8). Use before running `pnpm release` to catch issues that structure
  tests may miss. Top-level orchestrator at `scripts/release_check.sh` runs
  every phase and is wired into `.github/workflows/release.yml` as a
  pre-publish gate. Produces `docs/reports/release-validate/<version>/RELEASE-CHECK.md`
  suitable verbatim for the GitHub Release body.
version: "1.15.0"
---

# Release Validation Skill

## Purpose

Pre-release quality gate that validates the devops-ai-skill pack is ready to publish. Covers four areas that existing structure tests (`test-structure.sh`) do not fully address:

1. **Package release checks** — version sync, changelog, npm pack content, git state, badge accuracy
2. **Cross-platform link validation** — all 4 platforms correctly reference skills, prompts, and agents
3. **Skill & pipeline parity** — every skill/pipeline on disk is registered on every platform
4. **Setup script smoke testing** — dry-run validation of setup scripts in a sandboxed temp directory

This skill is the only one that validates the skill pack itself (meta-validation). It bridges the gap between `test-structure.sh` (static file checks) and `release.sh` (publish). Think of it as a pre-flight checklist that catches semantic issues — dead cross-references, missing registrations, npm packaging gaps, or setup script regressions — that static checks cannot detect.

## Activation

This skill activates when the user:
- Asks to validate a release before publishing
- Runs a pre-release check or readiness assessment
- Wants to verify cross-platform consistency after adding a skill or pipeline
- Asks to smoke-test the setup scripts
- Asks to check if the pack is ready for `pnpm release`

## Step 0: Discover Repository Layout

**Do NOT assume hardcoded counts or file lists.** Discover the pack structure at runtime.

### 0a: Discover All Skills

Build the canonical skill list dynamically:
```bash
find skills/ -mindepth 1 -maxdepth 1 -type d | sort
```
Store the count as `<skill-count>` and the list as `<skill-names>` for all subsequent steps.

### 0b: Discover All Pipelines

Build the canonical pipeline list:
```bash
# Horus pipelines
ls prompts/horus/*.md 2>/dev/null
# Zeus pipelines
ls prompts/zeus/*.md 2>/dev/null
# Shared prompts
ls prompts/shared/*.md 2>/dev/null
```
Store counts and lists for parity checks.

### 0c: Discover Platform Entry Files

Verify each platform's entry point exists:

| Platform | Entry File | Config Files |
|----------|-----------|-------------|
| Claude Code | `CLAUDE.md` | `.claude/agents/*.md`, `.claude-plugin/*.json` |
| Codex | `AGENTS.md` | `.codex/config.toml` |
| Gemini | `GEMINI.md` | `.gemini/agents/*.md`, `.gemini/extensions/devops/gemini-extension.json`, `.gemini/commands/devops/**/*.toml` |
| Antigravity | `.agents/rules/devops.md` | `.agents/skills/*/SKILL.md` |

### 0d: Discover Version Files

Locate all files that must contain the version string:
- `VERSION` (source of truth)
- `package.json` → `.version`
- `.claude-plugin/plugin.json` → `.version`
- `.claude-plugin/marketplace.json` → `.metadata.version` AND `.plugins[0].version`
- `.gemini/extensions/devops/gemini-extension.json` → `.version`

### 0e: Read Current Version

```bash
VERSION=$(cat VERSION | tr -d '[:space:]')
```

## Phase 1: Package Release Checks

### 1a: Version Consistency

Run the existing version consistency check and interpret results:
```bash
bash scripts/version-consistency.sh
```

Verify all 5 files from Step 0d contain the same version. If `version-consistency.sh` is missing, perform the checks inline by reading each file.

**Marketplace.json has TWO version fields** — both `metadata.version` and `plugins[0].version` must match. This is easy to miss because `version-consistency.sh` only checks `metadata.version`.

### 1b: Changelog Validation

Check that `CHANGELOG.md` contains:
- An entry header matching `## [$VERSION]` (required by `release.sh`)
- A date in the entry (format: `YYYY-MM-DD`)
- At least one bullet point describing changes under `### Added`, `### Changed`, `### Fixed`, or similar
- The entry is NOT the placeholder `(describe changes here)` left by `version-bump.sh`

### 1c: npm Pack Dry-Run

Simulate what `npm publish` would include:
```bash
pnpm pack --dry-run 2>&1
```

If `pnpm` is unavailable, fall back:
```bash
npm pack --dry-run 2>&1
```

**Validate the tarball contents against the canonical lists from Step 0:**

Required file categories (validate each dynamically, not by hardcoded count):
- Every `skills/<name>/SKILL.md` from Step 0a is present
- Every `prompts/horus/*.md`, `prompts/zeus/*.md`, `prompts/shared/*.md` from Step 0b is present
- Agent definitions: `.claude/agents/horus.md`, `.claude/agents/zeus.md`
- Plugin config: `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`
- Setup scripts: `scripts/setup.sh`, `scripts/setup/*.sh`
- Core docs: `docs/PROJECT.md`, `VERSION`

**Exclusion check** — the tarball must NOT contain:
- `.env`, `.env.*` files
- `node_modules/`
- `.DS_Store`
- `tests/` directory (test files should not ship to users)
- `.git/` directory
- Any file larger than 1MB (binary bloat check)

Cross-reference with `package.json` `files` field — if a required category is missing from the `files` array, report it as a packaging gap.

### 1d: Git State Check

Verify the repository is in a clean state for release:
- No uncommitted changes: `git status --porcelain` should be empty
- Current branch is `main`
- Tag `v$VERSION` does not already exist
- Local `main` is up-to-date with `origin/main`:
  ```bash
  git fetch origin main --dry-run 2>&1
  git rev-list HEAD..origin/main --count
  ```
  If unpushed or unpulled commits exist, report the count and direction.

### 1e: Badge and Count Accuracy

README badges display counts (skills, pipelines, agents) as shield.io URLs. These must match reality.

```bash
# Extract badge counts from README.md
grep -oP 'SKILLS-\K[0-9]+' README.md
grep -oP 'PIPELINES-\K[0-9]+' README.md
grep -oP 'AGENTS-\K[0-9]+' README.md
```

Compare against canonical counts from Step 0:
- `SKILLS` badge must equal `<skill-count>` from Step 0a
- `PIPELINES` badge must equal total horus + zeus pipeline count from Step 0b
- `AGENTS` badge must equal 2

Check all 3 README files: `README.md`, `docs/README.zh-TW.md`, `docs/README.zh-CN.md`.

Also scan for hardcoded skill counts in prose text:
```bash
grep -n '[0-9] skills\|[0-9] 個 Skills\|[0-9] 个 Skills\|[0-9] skill symlinks' README.md docs/README.zh-TW.md docs/README.zh-CN.md docs/setup.md scripts/setup.sh
```
Every count found must match `<skill-count>`.

### 1f: Version-Tag History Alignment

For informational purposes, verify that previous versions in CHANGELOG.md have corresponding git tags:
```bash
grep -oP '## \[\K[0-9]+\.[0-9]+\.[0-9]+' CHANGELOG.md | while read v; do
  if git rev-parse "v$v" &>/dev/null; then
    echo "  ✓ v$v tag exists"
  else
    echo "  ⚠ v$v tag missing (changelog entry exists but no git tag)"
  fi
done
```
Report missing tags as WARN (not FAIL) — the user may have only recently adopted tagging.

## Phase 2: Cross-Platform Link Validation

### 2a: Discover All Cross-References

Build a reference graph by scanning these entry-point files:

| Platform | Entry File | References To |
|----------|-----------|---------------|
| Claude Code | `CLAUDE.md` | `docs/PROJECT.md`, `prompts/`, `.claude/agents/` |
| Claude Plugin | `.claude-plugin/plugin.json` | skills, agents, commands |
| Codex | `AGENTS.md` | `docs/PROJECT.md`, `prompts/`, `skills/` |
| Gemini | `GEMINI.md` | `docs/PROJECT.md`, `.gemini/commands/`, `.gemini/agents/` |
| Antigravity | `.agents/rules/devops.md` | `docs/PROJECT.md`, `prompts/`, `.agents/skills/` |

### 2b: Validate All Referenced Paths Exist

For each cross-reference found in Step 2a:
1. Extract file paths from markdown links: `[text](path)` and backtick-quoted inline paths
2. Extract paths from code blocks and configuration files (JSON `path` fields, TOML `prompt` fields)
3. Resolve relative paths from the referencing file's directory
4. Verify each referenced file or directory exists on disk

**Path extraction patterns:**
- Markdown: `[text](relative/path.md)` or `[text](relative/path)`
- Backtick: `` `prompts/horus/full-pipeline.md` ``
- JSON: `"path": "../../../skills/repo-detect/SKILL.md"`
- TOML prompt blocks: references to `prompts/` paths inside `prompt = """..."""`

Report:
```
Cross-Platform Link Validation
===============================
Scanning: CLAUDE.md
  ✓ docs/PROJECT.md
  ✓ prompts/horus/full-pipeline.md
  ✗ prompts/horus/migrate.md (NOT FOUND)

Scanning: .claude-plugin/plugin.json
  ✓ skills/terraform-validate/SKILL.md
  ...
```

### 2c: Validate Skill Registration Parity

Ensure every skill from Step 0a is registered on every platform:

1. **Canonical skill list**: `<skill-names>` from Step 0a
2. **Gemini extension**: Parse `.gemini/extensions/devops/gemini-extension.json` → `skills[]` array. Each entry should have a `name` matching a skill directory and a `path` that resolves to an existing SKILL.md
3. **Codex**: Parse `AGENTS.md` for `$<skill-name>` references
4. **Antigravity**: Check `.agents/skills/` — note that Antigravity registers agents-as-skills (horus/zeus) separately from shared skills (symlinked by setup). Only validate that the setup script would create symlinks for all skills.
5. **Claude Plugin**: Skills are auto-discovered from `skills/` at runtime — verify the `skills/` directory is in `package.json` `files` array
6. **docs/PROJECT.md**: Check skill tables list all skills

Report per-platform registration matrix:
```
Skill Registration Parity
===========================
                          Claude  Codex  Gemini  Antigravity  PROJECT.md
terraform-validate          ✓       ✓      ✓         ✓           ✓
terraform-security          ✓       ✓      ✓         ✓           ✓
release-validate            ✓       ✓      ✗         ✓           ✓
                                          ↑ missing from gemini-extension.json
```

### 2d: Validate Pipeline Registration Parity

Ensure all pipelines are documented consistently across platforms:

1. **Canonical pipeline list**: Horus pipelines from `prompts/horus/*.md` and Zeus pipelines from `prompts/zeus/*.md` (from Step 0b)
2. **CLAUDE.md**: Check command table lists all pipelines with correct `*command` names
3. **docs/PROJECT.md**: Check pipeline tables match
4. **Gemini TOML commands**: Check `.gemini/commands/devops/pipelines/` has a TOML file for each pipeline. Naming convention: `horus-<name>.toml`, `zeus-<name>.toml` (with `full-pipeline.md` → `horus-full.toml` as a special case)
5. **Antigravity workflows**: Check that `scripts/setup/setup-antigravity.sh` references all expected workflow names
6. **AGENTS.md (Codex)**: Check command table lists all `*command` entries
7. **GEMINI.md**: Check command table lists all `*command` entries

**TOML count validation:**
```bash
toml_count=$(find .gemini/commands/devops -name "*.toml" | wc -l)
expected_count=$((2 + horus_pipeline_count + zeus_pipeline_count + shared_prompt_count_that_have_tomls))
```
The 2 accounts for `agents/horus.toml` and `agents/zeus.toml`.

### 2e: Validate Gemini Extension JSON Integrity

Parse `.gemini/extensions/devops/gemini-extension.json` and verify:
- All `agents[].definition` paths resolve to existing files
- All `skills[].path` values resolve to existing SKILL.md files
- `skills[]` count matches `<skill-count>` from Step 0a
- Version matches `VERSION` file (already checked in Phase 1a, but verify here too)

## Phase 3: Setup Script Smoke Testing

### 3a: Create Sandboxed Test Environment

```bash
TEST_DIR=$(mktemp -d)
trap 'rm -rf "$TEST_DIR"' EXIT  # Always clean up, even on failure

# Simulate a target repository with the skill pack installed
mkdir -p "$TEST_DIR/target-repo"
cp -r . "$TEST_DIR/target-repo/devops-ai-skill"
cd "$TEST_DIR/target-repo"
```

The `trap` ensures cleanup happens even if a step fails partway through.

### 3b: Test setup.sh for Each Platform

Run each platform setup script in the sandboxed directory. Use **name-based assertions** — verify each specific expected symlink exists, not just a count.

**Claude Code** (`--claude`):
```bash
bash devops-ai-skill/scripts/setup.sh --claude
```
Verify:
- `.claude/agents/horus.md` and `.claude/agents/zeus.md` are symlinks pointing to valid targets
- Every skill from `<skill-names>` has a symlink at `.claude/skills/<skill-name>/` that resolves to a directory containing SKILL.md
- No `[fail]` in output
- Exit code is 0

**Codex** (`--codex`):
```bash
bash devops-ai-skill/scripts/setup.sh --codex
```
Verify:
- Every skill from `<skill-names>` has a symlink at `.codex/skills/<skill-name>/`
- `AGENTS.md` exists (or is symlinked)
- No `[fail]` in output
- Exit code is 0

**Gemini** (`--gemini`):
```bash
bash devops-ai-skill/scripts/setup.sh --gemini
```
Verify:
- `.gemini/commands/devops/` directory has TOML command files
- `.gemini/agents/` has agent definition files
- No `[fail]` in output
- Exit code is 0

**Antigravity** (`--antigravity`):
```bash
bash devops-ai-skill/scripts/setup.sh --antigravity
```
Verify:
- Every skill from `<skill-names>` has a symlink at `.agents/skills/<skill-name>/`
- Workflow symlinks exist in `.agents/workflows/` for all expected pipeline names
- `.agents/rules/devops.md` exists
- No `[fail]` in output
- Exit code is 0

### 3c: Test Idempotency

Run each setup command a second time and verify:
- All items show `[skip]` (not `[link]` or `[fail]`)
- Exit code is still 0
- No duplicate symlinks or files created
- The count of `[skip]` messages matches the expected total (skills + workflows where applicable)

### 3d: Test Uninstall

```bash
bash devops-ai-skill/scripts/setup.sh --uninstall
```
Verify:
- All symlinks created in 3b are removed
- No `[fail]` in output
- Original target repo files (if any) are preserved
- Directories created by setup (`.claude/skills/`, `.codex/skills/`, etc.) may remain empty — this is expected

### 3e: Cleanup

Handled automatically by the `trap` in Step 3a. If running manually, ensure:
```bash
rm -rf "$TEST_DIR"
```

## Phase 4: Skill Fixture Suite Runs (v2.0.0)

Iterate every `tests/*/run-fixtures.sh` and aggregate PASS/FAIL counts per
suite. Delegates to `scripts/run_all_fixtures.sh`:

```bash
bash skills/release-validate/scripts/run_all_fixtures.sh > /tmp/fixtures.json
```

Output JSON shape: `{suites: [...], totalPass, totalFail, totalSuites, verdict}`.

**Gate:** any suite with `verdict: FAIL` → overall verdict `FAIL` → release
blocked. Empty list (no fixture runners present) → `verdict: NONE` (not a
failure, but flagged in the report).

## Phase 5: Shell Portability Static Checks (v2.0.0)

Static lint of every `.sh` file under `skills/` and `scripts/` for cross-OS
compatibility issues. Delegates to `scripts/check_shell_portability.sh`:

```bash
bash skills/release-validate/scripts/check_shell_portability.sh . > /tmp/portability.json
```

Rules:

| # | Rule | Severity | Why |
|---|---|---|---|
| 1 | `#!/usr/bin/env bash` shebang | WARN | `/bin/bash` and `/bin/sh` paths vary across distros |
| 2 | No `declare -A` | ERROR | macOS bash 3.2 lacks associative arrays — caught by us in v1.13.1 |
| 3 | No `mapfile` / `readarray` | ERROR | Bash 4+ only |
| 4 | No `sed -i` without backup suffix | WARN | BSD vs GNU divergence; portable form is `sed -i.bak ...` |
| 5 | No `readlink` with `-f` | WARN | BSD lacks `-f`; use `cd && pwd` pattern |

**Gate:** any ERROR → release blocked. WARN-only → release allowed but
flagged.

## Phase 6: Cross-Repo-Style Coverage (v1.15.0)

For each "Kustomize-touching skill" listed in
`references/repo-style-matrix.md`, verify fixtures exist for each declared
repo style (`kustomize-argocd`, `helm-only`, `mixed`). Delegates to
`scripts/check_repo_style_coverage.sh`:

```bash
bash skills/release-validate/scripts/check_repo_style_coverage.sh --repo-root .
```

Output JSON: `{scanned, matrix: [...], missing: ["skill:style"], coveragePct, verdict}`.

**Convention**: any pre-v1.15.0 fixture under `tests/<skill>/fixtures/`
counts as `kustomize-argocd`-style (matches the current reality). Other
styles must have a directory whose name contains the style keyword
(e.g. `tests/<skill>/fixtures/helm-only-basic/`).

**Gate**: WARN-only. Coverage gaps are surfaced but do not block release —
they're follow-up work, not regressions. To upgrade a row to FAIL, edit
the matrix and add a new column with `required` (no code change needed).

## Phase 7: Cross-AI-Tool Registration Parity (v1.15.0)

For every Zeus command (file under `prompts/zeus/`), verify it is
registered across all 4 AI-tool surfaces. Delegates to
`scripts/check_ai_tool_parity.sh`:

```bash
bash skills/release-validate/scripts/check_ai_tool_parity.sh --repo-root . --all
```

Checks per command:

| # | Where | Required |
|---|---|---|
| 1 | `prompts/zeus/<cmd>.md` exists | yes |
| 2 | `.gemini/commands/devops/pipelines/zeus-<cmd>.toml` exists | yes |
| 3 | `CLAUDE.md` mentions `*<cmd>` | yes |
| 4 | `AGENTS.md` mentions `*<cmd>` | yes |
| 5 | `GEMINI.md` mentions `*<cmd>` | yes |
| 6 | `docs/PROJECT.md` mentions `*<cmd>` | yes |

**Gate**: FAIL on any gap. Every Zeus command must surface identically
across Claude Code, OpenAI Codex CLI, Google Gemini CLI, and Google
Antigravity. Strengthens Phase 2 (cross-platform link validation), which
only checks file references, not command registration.

## Phase 8: Release Artifact Generation (v2.0.0)

Combine Phases 4 + 5 + 6 + 7 outputs into a single Markdown artifact at
`docs/reports/release-validate/<version>/RELEASE-CHECK.md`. Suitable
verbatim as the body of `gh release create --notes-file ...` or as the
npm publish README excerpt.

```bash
VERSION=$(cat VERSION) \
  FIXTURES_JSON=/tmp/fixtures.json \
  PORTABILITY_JSON=/tmp/portability.json \
  REPO_STYLE_JSON=/tmp/repo-style.json \
  AI_TOOL_PARITY_JSON=/tmp/ai-parity.json \
  OUTPUT="docs/reports/release-validate/${VERSION}/RELEASE-CHECK.md" \
  bash skills/release-validate/scripts/render_release_artifact.sh
```

(`REPO_STYLE_JSON` and `AI_TOOL_PARITY_JSON` are optional — when absent,
the artifact renders Phase 6 + 7 verdicts as `SKIPPED`, matching the
v1.14.0 caller contract for backwards compatibility.)

The artifact contains:
- Overall verdict (PASS / WARN / FAIL — worst of all phases)
- Per-phase verdict table (4 rows: Phases 4–7)
- Per-suite breakdown (Phase 4)
- Per-issue table (Phase 5)
- Phase 6 + 7 detail sections (coverage metrics and registration gaps)
- "How to interpret" + "Next steps" sections

The renderer also prints a one-line summary to stdout for CI logs:

```
release-validate v1.15.0: PASS (fixtures=OK, portability=OK, repoStyle=OK, parity=OK)
```

**Gate:** if overall verdict is `FAIL`, the renderer exits 1 — `pnpm release`
should refuse to proceed.

## Top-Level Orchestrator (v1.15.0)

`scripts/release_check.sh` at the repo root runs every phase in sequence
and renders the artifact. Used by both operators (manual pre-release
sanity check) and CI (`.github/workflows/release.yml`).

```bash
pnpm release:check    # or: bash scripts/release_check.sh
```

The orchestrator:
1. Creates `docs/reports/release-validate/<version>/`
2. Runs Phase 4 → `fixtures.json`
3. Runs Phase 5 → `portability.json`
4. Runs Phase 6 → `repo-style.json`
5. Runs Phase 7 → `ai-parity.json`
6. Invokes the renderer → `RELEASE-CHECK.md`
7. Exits 1 if overall verdict is FAIL, else 0

CI uploads `docs/reports/release-validate/` as a workflow artifact named
`release-check-<tag>` so the rendered Markdown is downloadable from the
Actions run page.

## Output Format

Present results as a release readiness report following the standard format from `prompts/shared/report-format.md`:

```
Release Validation Report — v1.6.0
====================================

Phase 1: Package Release Checks
  ✓ Version consistency (5/5 files match: 1.6.0)
  ✓ CHANGELOG.md has entry for 1.6.0 (dated 2026-04-07)
  ✓ npm pack includes all 9 skills, 18 prompts, 2 agents
  ✓ Git: clean tree, on main, tag v1.6.0 available
  ✓ Badge accuracy: SKILLS-9, PIPELINES-14, AGENTS-2 (all correct)
  ⚠ Version-tag history: v1.3.0 has no git tag (WARN)

Phase 2: Cross-Platform Links
  ✓ CLAUDE.md: 12/12 links valid
  ✓ AGENTS.md: 8/8 links valid
  ✓ GEMINI.md: 10/10 links valid
  ✓ Antigravity: 27/27 links valid
  ✓ Skill parity: 9/9 skills registered on all platforms
  ✓ Pipeline parity: 14/14 pipelines registered on all platforms
  ✓ Gemini extension: 9 skills, 2 agents, all paths valid

Phase 3: Setup Script Smoke Tests
  ✓ --claude: 11 items linked (2 agents + 9 skills), idempotent, uninstall clean
  ✓ --codex: 9 items linked (9 skills), idempotent, uninstall clean
  ✓ --gemini: agents + commands linked, idempotent, uninstall clean
  ✓ --antigravity: 27 items linked (9 skills + 18 workflows), idempotent, uninstall clean

====================================
Result: PASS — 0 errors, 1 warning
Ready for: pnpm release
```

When issues are found, append an actionable fix list:
```
====================================
Result: 3 issues found — fix before release
  1. [Phase 1a] marketplace.json plugins[0].version is 1.5.0 (expected 1.6.0)
     Fix: pnpm version:bump 1.6.0
  2. [Phase 2c] release-validate missing from gemini-extension.json
     Fix: Add skill entry to .gemini/extensions/devops/gemini-extension.json
  3. [Phase 3b] --gemini setup exit code 1
     Fix: Check .gemini/agents/ source directory exists
```

## Scope Flags

The user can run specific phases:
- `--all` (default): Run all 3 phases
- `--package`: Phase 1 only (version, changelog, npm, git, badges)
- `--links`: Phase 2 only (cross-platform reference and parity validation)
- `--smoke`: Phase 3 only (setup script smoke tests)
- `--quick`: Phase 1 + 2 only (skip slow smoke tests — recommended for iteration)

## Auto-Fix Capabilities

This skill can auto-fix:
- **Badge counts**: Update shield.io URLs in README files to match actual counts
- **Hardcoded skill counts**: Update prose text ("9 skills", "9 個 Skills") across docs
- **CHANGELOG placeholder**: Warn that the placeholder text from `version-bump.sh` needs replacing

This skill CANNOT auto-fix (requires user judgment):
- Missing platform registrations (each platform has different formats)
- Broken cross-references (the fix depends on whether the target was renamed or deleted)
- Setup script failures (root cause must be diagnosed)
- Git state issues (uncommitted changes may be intentional)

## Error Handling

### Discovery Failures
- **Missing VERSION file**: Report "Cannot determine version — VERSION file not found" and stop. This is fatal — all other checks depend on knowing the version.
- **Missing scripts**: If `version-consistency.sh` or `setup.sh` is missing, report the missing script and skip that check. Continue with remaining checks.
- **pnpm not installed**: Fall back to `npm pack --dry-run` for package content check. If neither is available, skip Phase 1c and report as WARN.
- **python3 not installed**: `version-consistency.sh` uses python3 for JSON parsing. If unavailable, parse JSON manually using `grep` and `jq` (if available) or skip with WARN.

### Phase 2 Failures
- **Entry file missing**: If a platform's entry file doesn't exist (e.g., `GEMINI.md` deleted), report as FAIL for that platform and continue with others.
- **JSON parse error**: If `gemini-extension.json` or `plugin.json` is malformed JSON, report the parse error and skip that file's checks.
- **TOML parse error**: If a Gemini command TOML is malformed, report the file and error but continue checking others.

### Smoke Test Failures
- **mktemp fails**: Skip Phase 3, report that smoke testing requires a writable temp directory.
- **setup.sh crashes mid-run**: Capture both stdout and stderr, report the failure with the error output, continue with remaining platforms.
- **Symlink target doesn't exist**: Report which source file is missing — this usually indicates a file was deleted from `skills/` or `prompts/` but the setup script still tries to link it.
- **Permission denied**: Report and skip. May happen in CI environments with restricted temp directories.

### Edge Cases
- **New skill added but not registered**: Phase 2c catches this — the parity matrix shows exactly which platforms are missing the registration.
- **Pipeline renamed but old name in docs**: Phase 2d catches stale references in command tables.
- **Version already tagged**: Phase 1d reports this — user must either bump version or delete the existing tag.
- **marketplace.json dual-version mismatch**: Phase 1a checks both `metadata.version` and `plugins[0].version` — they can diverge if only one is updated manually.
- **CHANGELOG placeholder not replaced**: Phase 1b checks for the literal text `(describe changes here)` left by `version-bump.sh` scaffolding.
- **Git ahead/behind remote**: Phase 1d reports both directions — unpushed commits and unpulled changes — with counts.

## Dry-Run Support

This skill is **read-only** for Phases 1 and 2 — no files are modified.

Phase 3 creates a temporary directory via `mktemp` but does not modify the source repository. All symlinks and files are created inside the isolated sandbox. The `trap EXIT` ensures cleanup even on failure.

## Rollback Strategy

- **Phases 1 and 2**: No rollback needed — these are pure read operations.
- **Phase 3**: The sandbox is in a temp directory and cleaned up automatically. If cleanup fails (e.g., process killed), the OS will clean `/tmp` eventually. No source files are touched.
- **Auto-fix (badge/count updates)**: If auto-fix is applied, show the diff before writing. Suggest `git checkout -- <file>` to revert if the fix is wrong.

## Dependencies

- `scripts/version-consistency.sh` — Reused for version checks (Phase 1a)
- `scripts/setup.sh` — Tested in Phase 3
- `prompts/shared/report-format.md` — Output format reference
- `pnpm` or `npm` — For pack dry-run (Phase 1c)
- `git` — For state checks (Phase 1d, 1f)
- `python3` — Used by `version-consistency.sh` for JSON parsing
- `mktemp` — For sandboxed smoke tests (Phase 3)
