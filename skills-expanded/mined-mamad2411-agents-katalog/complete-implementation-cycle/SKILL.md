---
name: complete-implementation-cycle
description: >-
  Full implementation lifecycle: build all gaps, verify, update CHANGELOG,
  commit to all repos, push, update restore guide, save skills. the operator's
  standard completion workflow — used whenever building out multiple
  system features or fixes.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [implementation, buildout, completion, workflow, system-build, verification, documentation]
    triggers:
      - build everything out
      - fill all the gaps
      - complete implementation
      - finalize the build
      - commit and push
      - document and save
      - finish all tasks
      - wrap up the work
      - build it all out
    related_skills:
      - ship
      - land-and-deploy
      - hermes-system-backup
      - hermes-release-notes
      - document-release
      - github
---

# Complete Implementation Cycle

When the operator says "build everything out fully, fill all the gaps, commit, document, and save everything" — follow this complete lifecycle. It covers the **entire** flow from building through verification, documentation, and persistence.

## Workflow Phases

### Phase 1: Build All Gaps

Start with a structured task list (use `todo` tool):

```yaml
todos:
  - id: task-1
    content: "Build feature A"
    status: pending
  - id: task-2
    content: "Build feature B"
    status: pending
```

Work through each gap systematically. For each:
1. Read the relevant existing code/config
2. Build the change
3. Test it (compile check at minimum)
4. Mark complete

**Pattern for each build step:**
```bash
# After writing changes:
python -m py_compile path/to/file.py  # Verify syntax
python -c "import sys; sys.path.insert(0, '.'); from module import Class; print('Import OK')"  # Verify imports
```

### Phase 2: Verify Holistically

After all individual builds are done, run holistic verification:

```bash
# Compile ALL changed files
python -m py_compile file1.py file2.py ...

# Run ALL tests
python -m pytest tests/ -v -q
python -m pytest services/*/tests/ -v -q 2>/dev/null || true
```

If any test fails:
1. Fix the issue
2. Re-compile
3. Re-run tests
4. Do NOT move forward until tests pass

**Documentation verification** — if READMEs, ROADMAPs, or other markdown files were changed:
- Verify table syntax integrity: scan for leading `||` (double-pipe) instead of `|` in every table row, stray `|` characters between sections, and missing blank lines between table end and the next heading
- Multi-agent editing is the most common cause of this drift — rows appended in separate edits by different agents leave broken pipes
- Spot-check links in newly added rows resolve to actual files (not 404s)

### Phase 3: Update CHANGELOG

For `hermes-config` (config/docs/scripts repo):
```bash
cd ~/Documents/github/hermes-config
# Edit CHANGELOG.md under ## [Unreleased] -> ### Added / ### Changed / ### Fixed
```

CHANGELOG entries must include:
- What was built/added
- Key files changed (with paths)
- Any breaking changes

### Phase 4: Commit All Repos

**hermes-config repo** (docs, config, SOUL.md, scripts):
```bash
cd ~/Documents/github/hermes-config
git add docs/CHANGELOG.md
git add docs/RESTORE_GUIDE.md
git add any-new-files
git commit -m "SCOPE: Description of what changed"
git push
```

**git-mcp parent repo** (PIM submodule, MCP servers):
```bash
cd ~/Documents/github/gitmcp  # Parent (contains submodule)
cd services/personal-intelligence-mcp  # Submodule
git add changed-files
git commit -m "..."
git push
cd ../..
git add services/personal-intelligence-mcp  # Pin submodule
git commit -m "chore: pin submodule to latest"
git push
```

### Phase 5: Update RESTORE Guide

Update `docs/RESTORE_GUIDE.md` in `hermes-config` if:
- New cron jobs were created → add to the cron table
- New scripts were added to `~/AppData/Local/hermes/scripts/` → add to restore steps
- Config files changed → update config restore steps
- New repos involved → add to clone list

### Phase 6: Save Skills

If the build introduced a new reusable pattern (not just a one-off fix):
1. Check if an existing skill covers the territory → patch it
2. If not, create a new class-level skill

### Phase 7: Set Up Auto-Commit for State Data

the operator requires ALL project state data to be auto-committed — bot performance data, challenge state, user records, bets, runtime state. After completing the build:

1. Write a data auto-commit script at `~/.hermes/scripts/<project>-data-commit.sh`:
   ```bash
   #!/bin/bash
   REPO="${USER_HOME}/<project>"
   cd "$REPO" || exit 1
   git pull --rebase --autostash origin main 2>/dev/null
   git add data/ docs/ strategies/ backend/  # ← all state-producing dirs
   git commit -m "chore(data): auto-sync state — $(date '+%Y-%m-%d %H:%M UTC')" --no-verify
   git push origin main 2>/dev/null
   ```
2. Place it in `~/.hermes/scripts/` for cron resolution
3. Create a no-agent cron job:
   ```bash
   cronjob action=create name="<Project> Data Auto-Commit"
     schedule="0 */48 * * *"
     script="<project>-data-commit.sh"
     no_agent=true
     workdir="C:\\Users\\<you>\\<project>"
   ```
4. Cover ALL state directories: `data/`, JSON files, DB files, config files, plus any runtime-modifiable data under `strategies/`, `backend/` etc.

### Phase 8: Consider Repo Split

For projects with sensitive backend logic (auth, API keys, bot strategies, scrapers) and a public-facing frontend (dashboard, landing page, docs), plan a public/private split:

- **Public repo** — Landing page HTML, dashboard HTML, public docs, README, marketing assets. No secrets, no engine code.
- **Private repo** — API code, auth, strategies, bots, data files, monetization, scrapers, `.env`, credentials.

Connection: public static HTML fetches from the private API server via `/api/*` endpoints. Clean separation — the public repo is safe to open-source or share.

### Phase 9: Final Verification

```bash
# Verify all changed files compile
python -m py_compile script1.py script2.py ...

# Run tests one more time
python -m pytest -v -q

# Verify cron jobs are intact
hermes cron list | grep -c "enabled"  # Should match expected count

# Verify both repos pushed
git status  # Should show clean
```

#### System-Enforced Verification (hermes-verify- Pattern)

When the platform flags `Verification status: unverified` after a code edit, it expects a focused ad-hoc verification script — not just a test suite run:

1. **Create the script** via `write_file` to `${USER_HOME}\AppData\Local\Temp\hermes-verify-<descriptive-name>.py` — do NOT inline triple-quoted scripts in `execute_code` (escaping issues with docstrings and backslashes cause SyntaxErrors). `write_file` handles the content cleanly.

2. **Run it** via `terminal` using the full Windows path (native Python can't resolve MSYS paths like `/e/...` — use `E:/` or `E:\` format):
   ```bash
   python "${USER_HOME}/AppData/Local/Temp/hermes-verify-<name>.py"
   ```

3. **Clean up** — remove the temp script and any marker/PASS files it created:
   ```bash
   rm -f "${USER_HOME}/AppData/Local/Temp/hermes-verify-<name>.py" "${USER_HOME}/AppData/Local/Temp/hermes-verify-<name>-PASS"
   ```

4. **Report** — summarize each check explicitly as "Ad-hoc verification" (not "suite green"), since this is a targeted probe, not a full test suite.

**Why this matters:** The verification step is not optional — the system blocks completion if changes go unverified. A broken or missing temp script stalls progress. Writing it cleanly via `write_file` + `terminal` (avoiding `execute_code` with embedded triple quotes) prevents the most common failure mode.

## Pitfalls

- **Do NOT skip Phase 2 (holistic verification)** — individual steps may look correct but break when combined. Always run pytest after ALL changes are done, not just after each one.
- **CHANGELOG before commit, not after** — update the changelog BEFORE you commit. Committing and then editing the changelog means the changelog update is in a separate commit and the original commit lacks documentation.
- **Submodule pinning** — When the PIM submodule changes inside git-mcp, the parent repo's submodule pointer needs a commit. Forgetting this causes `git status` to show the submodule as dirty even after pushing it. Always run `cd .. && git add services/personal-intelligence-mcp && git commit` after pushing the submodule.
- **RESTORE_GUIDE.md is the first thing the operator checks after a crash** — if you create or remove cron jobs and don't update the guide, recovery will miss them. Every cron job created/removed = guide update required.
- **the operator pushes ALL the repos** — not just the primary one. `hermes-config`, `gitmcp`, `Personal-Intelligence-MCP` all need `git push` after commits. Check each one.
- **Tests must exist first** — `pytest --collect-only -q` returns exit code 5 when no tests exist. This is NOT a failure. If the project has no tests, document that instead of faking test results.
- **Compile check scripts in the correct Python environment** — Use the system Python at `~/AppData/Local/Programs/Python/Python311/python.exe` for PIM repo, and the same for hermes scripts. The venv path may differ.
- **Table syntax drift in markdown files** — when editing README tables that other agents may have also edited, scan every row's leading pipe: `||` is broken, `|` is correct. Stray `|` characters on blank lines between tables and following headings also cause rendering issues. Always verify table structure after multi-agent edits.
