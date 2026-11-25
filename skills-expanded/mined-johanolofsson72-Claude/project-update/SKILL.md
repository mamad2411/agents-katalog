---
name: project-update
description: "Update speckit and sync Claude Code config from the template repo. Use on existing projects to pull the latest rules, docs, agents, skills, hooks, settings. Triggers: update project, sync config, update claude config, sync rules, refresh project."
argument-hint: "[optional: 'speckit-only' or 'sync-only' to run just one part]"
disable-model-invocation: true
allowed-tools: Read, Write, Edit, Bash, AskUserQuestion, Glob, Grep
---

# Project Update

You are updating an existing project's speckit installation and Claude Code configuration to the latest version from the template repo.

**`/project-update` is sufficient on its own.** No `git pull` of the template beforehand, on any machine, from any starting state. Step 4 fetches the sync instructions fresh from GitHub, and their Step -1 finds the template clone, **clones one if the machine has none**, and **fast-forwards it to `origin/main`** before any later step reads a file from it. That refresh is the whole reason the guarantee holds: the instructions come from GitHub but the files come off the local clone, so a clone left behind would deliver months-old content while reporting success. Covered by `scripts/test-sync-prompt-bootstrap.sh`.

This skill does NOT run the project wizard interview, and it does NOT run a spec's per-spec interview. It only syncs infrastructure and tooling. (It DOES install/refresh the enforcement that *requires* the per-spec interview — see the spec-interview gate note in Step 5.)

## Input

```text
$ARGUMENTS
```

## Process

### Step 1: Verify prerequisites

Check that the required tools are available:

```bash
command -v uv && echo "[OK] uv found" || echo "[MISSING] uv — install with: curl -LsSf https://astral.sh/uv/install.sh | sh"
command -v specify && echo "[OK] specify found" || echo "[MISSING] specify — will be installed"
command -v python3 && echo "[OK] python3 found" || echo "[MISSING] python3 — required by the sync helper scripts"
command -v jq && echo "[OK] jq found" || echo "[MISSING] jq — four inline hooks in settings.json parse tool input with jq and SILENTLY no-op without it. Install: apt/dnf/pacman install jq (Linux) · brew install jq (macOS)"
```

If `uv` or `python3` is missing, tell the user to install it and stop. A missing `jq` is not fatal — the sync proceeds — but report it in Step 8, because the affected hooks fail open (no error, no effect), which is the worst kind of broken.

If `$ARGUMENTS` is `sync-only`, skip to Step 4.

### Step 2–3: spec-kit (pinned, handled by the sync)

spec-kit is brought to the template's pin by `scripts/speckit-sync.sh`, which the sync runs in
sync-prompt Step 0.5. The pin is one tag in `scripts/speckit-version` (spec 073), so you and every
other developer run the same phases. The script installs the CLI at the pinned tag only when the
installed version differs, re-initialises `.specify/` only when the project's recorded version
differs (`specify init --force` is not idempotent — an unconditional re-init restores spec-kit 1.0's
two pipeline stops), keeps the constitution across the init, and runs
`speckit-extension-policy.sh` afterwards. Exit 2 means the policy could not find the stop it
removes — spec-kit reworded it — and must be reported in Step 8, never swallowed.

If `$ARGUMENTS` is `speckit-only`: run sync-prompt Step -1 to resolve `$TEMPLATE`, then
`bash "$TEMPLATE/scripts/speckit-sync.sh" --repo "$PWD"`, and skip to Step 7.

To force a re-init (a corrupted `.specify/`, a changed integration), delete
`.specify/init-options.json` first. To move every project to a newer spec-kit, change
`scripts/speckit-version` in the template — never add `--from git+…spec-kit.git` without a tag.

### Step 4: Fetch sync-prompt from template repo

Fetched fresh every run, so the instructions below are always current even when everything on disk is not:

```bash
curl -sL https://raw.githubusercontent.com/johanolofsson72/Claude/main/scripts/sync-prompt.md
```

Read the fetched content carefully.

### Step 5: Execute sync-prompt instructions

Execute all instructions between the `---` markers in the fetched sync-prompt. Specifically:

1. **Run Step -1, Step 0 and Step 0.5 first.** Step 0.5 runs the sync engine
   (`template-autosync.sh --force --no-commit`), which does every mechanical copy and the core hook
   wiring — the same program that runs at every SessionStart, so this skill and autosync cannot
   disagree about what a synced project contains. Everything below is the judgment half. Read
   template files from the local clone, `$TEMPLATE/<path>` — Step -1 has just fast-forwarded it.

2. **Read this project's files** — Read existing `CLAUDE.md`, `.claude/settings.json`, and all files under `.claude/` in THIS project.

3. **Language migration** — If this project still has Swedish content in Claude Code config files, translate to English per the sync-prompt's instructions.

4. **Analyze and update** — For each template file:

   | Situation | Action |
   |-----------|--------|
   | File does NOT exist in this project | Copy from template |
   | File exists and matches template | Skip |
   | File exists but is older | Update to template version, preserve `# PROJECT-SPECIFIC` blocks |
   | File exists with project-specific content | Merge — template structure + project customizations |

5. **CLAUDE.md merge** — Update: critical rules, execution mode, workflow, verification, context management, reference files. Preserve: project description, tech stack, commands, project-specific principles.

   **Stack-aware testing docs (CRITICAL — do NOT re-stamp browser docs onto a mobile app).** The web `testing.md` and `spec-testing-checklist.md` are wrong for React Native / Expo (they assume a browser, Playwright, and `dotnet test`). Before overwriting either file:
   - **Read `.claude/.sync-stack` if it exists.** A line `testing=mobile` means this project was already decided mobile — keep it mobile, do NOT fetch the web `testing.md` over it.
   - **Auto-detect mobile** if `.sync-stack` is absent: a root `package.json` with `expo` or `react-native` in dependencies, or an `app.json` / `app.config.{js,ts}` / `eas.json` (→ React Native / Expo); OR a `pubspec.yaml` with a `flutter:` section / `sdk: flutter` (→ Flutter). Either means mobile.
   - **Mobile project (RN/Expo or Flutter)** → fetch `testing-mobile.md` and `spec-testing-checklist-mobile.md` from the template and write them to the project as `.claude/docs/testing.md` and `.claude/docs/spec-testing-checklist.md` (canonical names, mobile content — the doc carries both a React Native and a Flutter section). Do NOT also fetch the web versions. Write `testing=mobile` to `.claude/.sync-stack`.
   - **Hybrid** (.NET/web backend AND an Expo or Flutter client) → keep the web `testing.md` AND additionally install `.claude/docs/testing-mobile.md` + `spec-testing-checklist-mobile.md`. Write `testing=hybrid`.
   - **Web/.NET project** → normal web `testing.md` / `spec-testing-checklist.md`; remove any stray `-mobile` files. Write `testing=web`.
   - This is the exact mechanism in sync-prompt Step 7c — follow it. Re-stamping browser docs onto a native app is the documented failure that left rundan/iskvalp reading "browser back mid-flow" instructions for an app with no browser.

6. **settings.json merge** — UNION of hooks and permissions.deny, plus `"outputStyle": "Proactive"` when the project sets none (sync-prompt Step 4). Hooks are wired DETERMINISTICALLY via the three helper scripts (`sync-local-llm-hooks.py`, `sync-graphify-wiring.py`, `sync-core-hooks.py`), NOT by hand. Preserve project-specific hooks.

7. **Verify spec testing pipeline** — Ensure rules/specs.md, docs/spec-testing-checklist.md, and the PostToolUse prompt-hook all exist.

8. **Verify Allium + TLA+ pipeline** — Ensure all verification pipeline files exist per sync-prompt instructions.

9. **Install required external skills** — Run the git clone commands for any missing skills. The universal bundles (anthropics/skills, superpowers, trailofbits, ui-ux-pro-max) always install. The **stack-specific four** (dotnet, vercel, qa-test, playwright) are **stack-gated** per sync-prompt Step 6: skipped when `.claude/.sync-stack` (or file markers) shows the stack does not use them — e.g. no browser bundles on a `testing=mobile` project, no `dotnet/skills` without a `.csproj`. Already-installed bundles are always skipped. Unknown stack → install all (the audit in step 11 flags any that turn out irrelevant).

10. **Install TLC model checker** — Verify TLC is available, install if missing.

11. **Skill audit (report-only)** — Run `bash scripts/skill-audit.sh` (sync-prompt Step 8e). It counts every installed `SKILL.md` (global + project), estimates the per-session baseline context cost, and flags `[REVIEW]` bundles this project's stack does not use. It **NEVER deletes** — global skills are shared, so pruning is a developer decision. Fold the totals and any `[REVIEW]`/`[CEILING]` output into the Step 8 report.

> **Spec-interview gate (anti-drift) — must land on every project.** As part of the sync-prompt's rule list + script list + core-hook wiring, this sync installs `.claude/rules/spec-interview.md` and `scripts/spec-interview-guard-hook.sh`, and `sync-core-hooks.py` wires the `spec-interview-guard` PreToolUse hook. That hook hard-blocks source-code edits until the active spec records ≥15 answered questions in `<spec-dir>/interview.md` (target 15–25). **Default is AUTO mode:** Claude auto-answers the base with the recommended option (tagged `**A (auto):**`) and asks the developer only the overflow questions when it judges a spec large/advanced — the hook counts both auto and human answers. A project that wants the old fully-human behaviour sets `SPEC_INTERVIEW_MODE=manual` (settings.json `env` or `CLAUDE.local.md`), and the hook then counts only human `**A:**` answers. Confirm it landed in Step 7's wiring check.

> **Context-cost pre-cleanup (run BEFORE a heavy project).** On a mature project, `specs/INDEX.md` and `specs/SCENARIOS.md` are read (often re-read) on every spec and tend to balloon — a paragraph-per-spec `## history` section is the usual culprit, and it re-bills tokens every turn. This sync installs `scripts/archive-spec-history.sh` and the updated "Keep the register/map lean" rules. If either file is large (the spec-register orientation hook's canary flags it past ~25 KB), run the cleanup once — it moves old history to sibling `*.history.md` archives, keeping the last ~5 inline, and it is git-reversible:
>
> ```bash
> scripts/archive-spec-history.sh --dry-run   # preview
> scripts/archive-spec-history.sh --keep 5    # apply; review with git diff
> ```
>
> It touches only the history section — live spec rows and the SC-id ledger are untouched. Note in the Step 8 report if you ran it and the size delta. (This is a one-shot cleanup, not part of the automated sync — run it deliberately.)

### Step 6: Ask about tech stack and clean up

Use `AskUserQuestion` to confirm the project's tech stack (the sync-prompt has the exact question). Remove irrelevant files based on the answer.

**IMPORTANT**: If this is a re-sync (files already exist and tech stack was already decided), check if the stack rules (`dotnet.md` etc. in the rules folder) have been previously removed. If they were, don't re-add them — respect the previous tech stack decision. Ask the user:

> This project was previously synced. Should I re-evaluate the tech stack, or keep the current file selection?

### Step 6b: Supply-chain defaults

Once the stack is settled, add release-age cooldowns for the package managers this project uses and the NuGetAudit
build gate, only where absent. Existing settings are never rewritten, so a re-sync reports `kept` and changes nothing.
Put any `TODO` lines in the Step 8 report under "Manual review recommended". Background: `.claude/docs/supply-chain.md`.
The block is the same as `/project-wizard` Phase 3F. Keep the two copies identical.

```bash
# Supply-chain defaults (.claude/docs/supply-chain.md). Writes a setting only where it is absent and
# never rewrites one that exists, so a second run changes nothing and prints "kept" for each file.
sc_find() { find . -maxdepth 4 -name "$1" -not -path '*/node_modules/*' -not -path '*/bin/*' \
  -not -path '*/obj/*' -not -path '*/.claude/worktrees/*' 2>/dev/null; }
# Append on a line of its own, even when the file lacks a trailing newline.
sc_add() { [ -s "$1" ] && [ -n "$(tail -c1 "$1")" ] && printf '\n' >> "$1"; printf '%s\n' "$2" >> "$1"; echo "wrote  $1: $2"; }
sc_find package-lock.json | while IFS= read -r f; do       # npm: unit is DAYS
  rc="$(dirname "$f")/.npmrc"
  grep -qs '^min-release-age' "$rc" && echo "kept   $rc" || sc_add "$rc" 'min-release-age=3'
done
sc_find pnpm-lock.yaml | while IFS= read -r f; do         # pnpm: unit is MINUTES
  ws="$(dirname "$f")/pnpm-workspace.yaml"
  grep -qs '^minimumReleaseAge:' "$ws" && echo "kept   $ws" || sc_add "$ws" 'minimumReleaseAge: 4320'
done
sc_find uv.lock | while IFS= read -r f; do
  d="$(dirname "$f")"
  if grep -qs 'exclude-newer' "$d/uv.toml" "$d/pyproject.toml"; then echo "kept   $d (exclude-newer set)"
  # A uv.toml would silently shadow an existing [tool.uv] table, so never create one beside it.
  elif grep -qs '^\[tool\.uv\]' "$d/pyproject.toml"; then echo "TODO   $d/pyproject.toml: add exclude-newer = \"3 days\" under [tool.uv]"
  else sc_add "$d/uv.toml" 'exclude-newer = "3 days"'; fi
done
if [ -f .github/dependabot.yml ] && ! grep -qs 'cooldown:' .github/dependabot.yml; then
  echo "TODO   .github/dependabot.yml: add a cooldown: block to each updates: entry (see supply-chain.md)"
fi
if [ -n "$(sc_find '*.csproj' | head -1)" ]; then
  if [ ! -f Directory.Build.props ]; then
    printf '%s\n' '<Project>' '  <PropertyGroup>' \
      '    <!-- NuGetAudit high/critical fail the build: .claude/docs/supply-chain.md -->' \
      '    <WarningsAsErrors>$(WarningsAsErrors);NU1903;NU1904</WarningsAsErrors>' \
      '  </PropertyGroup>' '</Project>' > Directory.Build.props
    echo "wrote  Directory.Build.props: NU1903;NU1904 as errors"
  elif grep -qs 'NU1904' Directory.Build.props; then echo "kept   Directory.Build.props"
  else echo "TODO   Directory.Build.props exists: add NU1903;NU1904 to <WarningsAsErrors> by hand"; fi
fi
```

A new `Directory.Build.props` turns high and critical advisories into build errors. If `dotnet build` now fails with
NU1903/NU1904, the project already had the vulnerable package. Report it and fix it; do not remove the gate.

### Step 7: Verify

- Verify `settings.json` is valid JSON: `python3 -m json.tool .claude/settings.json`
- Normalize hook paths: `python3 scripts/fix-hook-paths.py .claude/settings.json`. The settings guard (spec 089) refuses this from the agent's shell once it is wired: ask the developer to run it with `!`.
- Verify CLAUDE.md does not exceed ~200 lines
- Verify reference files in CLAUDE.md point to files that actually exist
- **Core-hook wiring check** — every core hook script present on disk MUST be wired (catches the prose-merge gap that previously dropped pipeline/register/interview hooks):

  ```bash
  for s in pipeline-trigger-match emit-pipeline-reminder spec-register-guard-hook pipeline-state-guard-hook \
           spec-interview-guard-hook spec-md-coverage-reminder-hook scenario-map-reminder-hook \
           continuous-execution-hook stop-validation-hook repeat-failure-guard-hook spec-run-log-hook lane-orientation-hook; do
    if [ ! -f "scripts/$s.sh" ]; then
      echo "[MISSING] scripts/$s.sh never copied — re-run the core-script mirror (sync-prompt.md Step 5c)"
    elif ! grep -q "$s.sh" .claude/settings.json; then
      echo "[GAP] $s present on disk but NOT wired — run: python3 scripts/sync-core-hooks.py \"\$TEMPLATE/.claude/settings.json\""
    fi
  done
  echo "core-hook check done (no [MISSING]/[GAP] lines above = complete)"
  ```

  If `spec-interview-guard-hook` prints `[GAP]`, the anti-drift gate is not active — re-run `sync-core-hooks.py` (and confirm `scripts/spec-interview-guard-hook.sh` was copied first).

### Step 8: Report

```markdown
## Project Update Complete

**Speckit**: [at pin / upgraded X → Y / FAIL: <speckit-sync.sh output>] — pin [vX.Y.Z]
**Sync source**: johanolofsson72/Claude (main branch)
**Constitution**: [preserved/untouched]

### Files synced:
- [CREATED] filename — reason
- [UPDATED] filename — what changed
- [SKIPPED] filename — already current
- [REMOVED] filename — not relevant for tech stack
- [TRANSLATED] filename — migrated Swedish → English

### Enforcement gates:
- spec-interview-guard — [wired / GAP] (anti-drift: 15–25 questions per spec before source edits; AUTO by default, human overflow on flag)
- pipeline-state-guard — [wired / GAP]
- spec-register-guard — [wired / GAP]

### Skill audit (report-only — nothing deleted):
- Stack detected: [web / mobile / hybrid / unknown]
- Skills installed: [N] (~[T]k tokens baseline context per session)
- Stack-gated installs skipped this run: [bundles or "none"]
- [REVIEW] stack-irrelevant bundles (global/shared — review before removing): [list or "none"]
- Soft ceiling: [within / EXCEEDED]

### Project-specific preserved:
- filename — what was preserved

### Manual review recommended:
- filename — why

Run `/project-wizard` if you need to update the project's core documents (CLAUDE.md project section, constitution, design system, project brief).
```

## Rules

1. NEVER change the project's core logic or application code.
2. ALWAYS preserve project-specific customizations (marked with `# PROJECT-SPECIFIC` or clearly unique to the project).
3. NEVER overwrite the constitution with speckit's default — always backup and restore.
4. If unsure about a merge conflict: report and ask instead of changing.
5. Do NOT commit automatically — let the developer review first.
6. Template files are read from the local clone Step -1 resolves and refreshes (`$TEMPLATE`), never from GitHub raw URLs file by file. Only sync-prompt.md itself is fetched from GitHub, so the instructions are current even when the clone is not yet.
7. Communicate in English.
