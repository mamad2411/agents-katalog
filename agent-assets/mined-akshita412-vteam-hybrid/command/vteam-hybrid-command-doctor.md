<!-- agent-notes: { ctx: "read-only project health check, 8 diagnostics", deps: [CLAUDE.md, .claude/agents/, .claude/commands/, docs/methodology/agent-notes.md], state: active, last: "sato@2026-03-21" } -->
Run a health check on the vteam-hybrid project setup. This command is **read-only** — it inspects but never modifies files, config, or state.

---

## Instructions

Run all 8 diagnostic checks below. For each check, report one of:
- **[PASS]** — everything looks good (green)
- **[WARN]** — non-blocking issue, project can function but something is suboptimal
- **[FAIL]** — blocking issue, something required is missing or broken

For every WARN or FAIL, include a single-line actionable fix suggestion indented below the status line, prefixed with an arrow.

After all checks, print a summary line: **"N passed, N warnings, N failures"**.

---

## Check 1: Agent Files

Verify that all expected agent definition files exist in `.claude/agents/`.

Expected files (19):
`archie.md`, `cam.md`, `cloud-architect.md`, `cloud-costguard.md`, `cloud-netdiag.md`, `code-reviewer.md`, `dani.md`, `debra.md`, `diego.md`, `grace.md`, `ines.md`, `pat.md`, `pierrot.md`, `prof.md`, `sato.md`, `tara.md`, `user-chorus.md`, `vik.md`, `wei.md`

```bash
# List .claude/agents/*.md and compare against expected list
ls .claude/agents/*.md 2>/dev/null
```

- PASS if all 19 are present.
- WARN if extra files exist beyond the 19 (list them — they may be intentional project additions).
- FAIL if any of the 19 are missing (list which ones).

---

## Check 2: Command Files

Verify that all expected command files exist in `.claude/commands/`.

Expected files (27):
`adr.md`, `aws-review.md`, `azure-review.md`, `cloud-update.md`, `code-review.md`, `design.md`, `devcontainer.md`, `doctor.md`, `gcp-review.md`, `handoff.md`, `kickoff.md`, `pin-versions.md`, `plan.md`, `quickstart.md`, `restack.md`, `resume.md`, `retro.md`, `review.md`, `scaffold-ai-tool.md`, `scaffold-cli.md`, `scaffold-static-site.md`, `scaffold-web-monorepo.md`, `sprint-boundary.md`, `sync-ghcp.md`, `sync-template.md`, `tdd.md`, `whatsit.md`

```bash
# List .claude/commands/*.md and compare against expected list
ls .claude/commands/*.md 2>/dev/null
```

- PASS if all 27 are present.
- WARN if extra files exist beyond the 27 (list them).
- FAIL if any of the 27 are missing (list which ones).

---

## Check 3: CLAUDE.md Initialization

Check whether `CLAUDE.md` has been customized for this project or still contains template placeholders.

```bash
grep -c '\[Your Project Name\]' CLAUDE.md
grep -c '\[Brief description' CLAUDE.md
grep -c '\[Language, framework' CLAUDE.md
```

- PASS if none of the three placeholder strings are found (project has been initialized).
- WARN if any placeholder strings remain. Report which ones.
  - Suggest: "Run `/quickstart` or `/kickoff` to initialize project metadata."

---

## Check 4: Scaffold Status

Check whether stub docs have been deployed from `docs/scaffolds/` to their final locations.

```bash
ls docs/scaffolds/*.md 2>/dev/null
```

- PASS if `docs/scaffolds/` does not exist or is empty (stubs have been deployed).
- WARN if `docs/scaffolds/` still contains `.md` files. List the files.
  - Suggest: "Run a `/scaffold-*` command or `/kickoff` to deploy stub docs."

---

## Check 5: README Swap Status

Check whether the template storefront README has been replaced with the project README.

```bash
ls README-template.md 2>/dev/null
```

- PASS if `README-template.md` does not exist (template cleanup has run).
- WARN if `README-template.md` still exists.
  - Suggest: "Run `/kickoff` or `/quickstart` to swap the README, or manually: `mv README-template.md README.md`."

---

## Check 6: Tracking Adapter

Check whether the tracking adapter is configured and functional.

```bash
# Read the tracking-adapter comment from CLAUDE.md
grep 'tracking-adapter:' CLAUDE.md
grep 'project-number:' CLAUDE.md
grep 'project-owner:' CLAUDE.md
```

If the adapter is `github-projects`:

```bash
# Check GitHub CLI authentication
gh auth status 2>&1
```

- PASS if adapter is set, and (if github-projects) `gh auth status` succeeds AND `project-number` is populated.
- WARN if adapter is set and `gh auth status` succeeds but `project-number` is empty.
  - Suggest: "Run `/kickoff` Phase 5 to create a project board, or set `project-number` in CLAUDE.md manually."
- FAIL if `gh auth status` fails.
  - Suggest: "Run `gh auth login` to authenticate the GitHub CLI."

---

## Check 7: Git Status

Check repository health.

```bash
git rev-parse --is-inside-work-tree 2>&1
git remote -v 2>&1
git status --short 2>&1
```

Report three sub-items:
1. **Repo initialized** — PASS if inside a git work tree, FAIL otherwise.
2. **Remote configured** — PASS if at least one remote exists, WARN if no remote.
   - Suggest: "Run `git remote add origin <url>` to configure a remote."
3. **Working tree clean** — PASS if `git status --short` produces no output, WARN if there are uncommitted changes. Report the count of changed files.
   - Suggest: "Review uncommitted changes and commit or stash them."

---

## Check 8: Agent-Notes Coverage

Spot-check a sample of source files for agent-notes metadata. This is a heuristic, not exhaustive.

**Which files to check:** Sample up to 10 files from these locations (skip if a location does not exist):
- `.claude/agents/*.md` (pick 3)
- `.claude/commands/*.md` (pick 3)
- `scripts/*.sh` or `scripts/*.py` (pick 2 if they exist)
- `src/**/*.ts` or `src/**/*.py` or `src/**/*.rs` (pick 2 if they exist)

Skip files in `docs/methodology/`, `docs/process/`, and `docs/integrations/` — those are methodology docs expected to have notes but are not the concern of this check. Also skip JSON files, lock files, and binaries (per the agent-notes protocol exclusion list).

```bash
# Check for agent-notes pattern in each sampled file
head -5 <file> | grep -c 'agent-notes:'
```

- PASS if all sampled files have agent-notes.
- WARN if some are missing. Report the ratio (e.g., "7/10 files have agent-notes") and list files missing them.
  - Suggest: "Add agent-notes to files missing them per `docs/methodology/agent-notes.md`."
- If no source files exist yet to sample (template is brand new), report as PASS with a note: "No source files to check yet."

---

## Output Format

Print the report using this exact structure:

```
vteam-hybrid Doctor Report
==========================

[STATUS]  Check 1 description
          -> Fix suggestion (only for WARN/FAIL)

[STATUS]  Check 2 description
          -> Fix suggestion (only for WARN/FAIL)

...

--------------------------
Summary: N passed, N warnings, N failures
```

Use plain text, not markdown tables. Each check gets one status line. WARN/FAIL checks get an indented suggestion line immediately below.
