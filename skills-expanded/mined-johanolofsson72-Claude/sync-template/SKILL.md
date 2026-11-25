---
name: sync-template
description: Syncs project configuration from the Claude Code template repo. Updates skills, agents, hooks, rules, and docs to match the latest template. Use when starting a new project or upgrading an existing project's Claude Code configuration.
disable-model-invocation: true
argument-hint: "[full|skills|agents|hooks|docs]"
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Sync from template repo

Update this project's Claude Code configuration from the local Claude template repo. The template's location is **auto-detected** per developer — Johan's macOS box has it at `/Users/jool/repos/Claude`, David's Linux box has it at `/home/david/repos/Claude`, etc. Do not hardcode either.

**Resolve `TEMPLATE` once at the start of every sync session.** Ask the sync engine; it owns the
one list of places a clone may live (`$CLAUDE_TEMPLATE_DIR` first, then the usual macOS/Linux roots):

```bash
TEMPLATE=$(bash scripts/template-autosync.sh --template-dir 2>/dev/null)
# A project synced before spec 073 has an engine without --template-dir (it exits "unknown flag").
# The same list, literally, so this skill still finds a clone on the first run after the upgrade.
if [ -z "$TEMPLATE" ]; then
  for CAND in "${CLAUDE_TEMPLATE_DIR:-}" "$HOME/repos/Claude" "$HOME/repos/claude" \
              "$HOME/Projects/Claude" "$HOME/projects/Claude" "$HOME/projects/claude" \
              "$HOME/src/Claude" "$HOME/code/Claude" "$HOME/dev/Claude" "$HOME/git/Claude"; do
    [ -n "$CAND" ] && [ -f "$CAND/scripts/sync-prompt.md" ] && [ -d "$CAND/.claude/rules" ] && { TEMPLATE="$CAND"; break; }
  done
fi
if [ -z "$TEMPLATE" ]; then
  echo "[ERROR] No template clone on this machine." >&2
  echo "        git clone https://github.com/johanolofsson72/Claude.git \$HOME/repos/Claude" >&2
  echo "        (or set CLAUDE_TEMPLATE_DIR to where yours lives) and re-run." >&2
  exit 1
fi
echo "[OK] Template at: $TEMPLATE"
```

**For `full`, the mechanical half is the engine, not this document.** Run it first — it fetches and
fast-forwards the clone, copies every CORE script/rule/doc, rewires the core hooks and stamps
`.claude/.template-sync` — then bring spec-kit to the pin:

```bash
CLAUDE_TEMPLATE_DIR="$TEMPLATE" bash "$TEMPLATE/scripts/template-autosync.sh" --force --no-commit
bash scripts/speckit-sync.sh
```

The per-scope steps below are then the judgment half (merges the engine refuses to make) and the
verification. Until spec 073 this skill copied files itself, never refreshed the clone, and so could
sync months-old content while reporting success.

Throughout this skill, every reference to the template path uses `$TEMPLATE`, never a hardcoded absolute path. If you are reading this skill as instructions to execute, **resolve `$TEMPLATE` first** with the probe above, then substitute it everywhere the skill mentions the template repo location.

The hardcoded `/Users/jool/repos/Claude` references that remain elsewhere in this document are **example paths** showing where the file would be on Johan's machine — they are NOT meant to be used literally. Translate them to `$TEMPLATE/...` when you execute.

## What to sync

Argument controls scope. Default: `full`.

- `full` — sync everything below
- `skills` — only .claude/skills/
- `agents` — only .claude/agents/
- `hooks` — only .claude/settings.json hooks
- `docs` — only .claude/docs/

## Process

### 1. Read template files

Read these files from the template repo at `$TEMPLATE` (resolved via the probe at the top of this skill):

**Skills (`.claude/skills/`):**
- `code-review/SKILL.md`
- `explore-codebase/SKILL.md`
- `deploy-checklist/SKILL.md`
- `tla/SKILL.md`
- `allium/SKILL.md`
- `update-template/SKILL.md`
- `sync-template/SKILL.md`

**Agents (`.claude/agents/`):**
- `dotnet-reviewer.md`
- `security-scanner.md`
- `test-runner.md`
- `db-agent.md`

**Settings:** `.claude/settings.json`

**Rules (`.claude/rules/`):**
- `dotnet.md`
- `frontend.md`
- `security.md`
- `wordpress.md`
- `allium.md`
- `specs.md`
- `tests.md`
- `scenarios.md`
- `design-references.md`
- `continuous-execution.md`
- `validation-followup.md`
- `feature-pipeline.md`
- `spec-register.md`
- `spec-hardening.md`
- `carve-budget.md`
- `project-workflow.md`
- `sqlite.md`
- `spot-resilience.md`
- `github-actions.md`

**Docs (`.claude/docs/`):**
- `skills.md`
- `workflows.md`
- `agents-templates.md`
- `conventions.md`
- `git.md`
- `security.md`
- `testing.md`
- `deployment.md`
- `stress-testing.md`
- `spec-testing-checklist.md`
- `design-reference-library.md`
- `project-template.md`
- `graphify.md`
- `local-llm.md`
- `spot-architecture.md`

**Scripts:**
- `scripts/tla-hook.sh`
- `scripts/allium-hook.sh`
- `scripts/tlc-cleanup.sh`
- `scripts/test-coverage-hook.sh`
- `scripts/continuous-execution-hook.sh`
- `scripts/stop-validation-hook.sh`
- `scripts/ui-design-hook.sh`
- `scripts/after-specify-hook.sh`
- `scripts/feature-pipeline-detect.sh`
- `scripts/spec-register-guard-hook.sh`
- `scripts/spec-register-orientation-hook.sh`
- `scripts/spec-md-coverage-reminder-hook.sh` (deterministic replacement for the legacy `type:"prompt"` spec-completeness hook; never blocks, suppresses reminder on carved-out test slices)
- `scripts/scenario-map-reminder-hook.sh` (PostToolUse advisory; fires the scenario interview when a spec gains interactive behaviour but `specs/SCENARIOS.md` lacks rows for it)
- `scripts/scenario-map-orientation-hook.sh` (SessionStart advisory; PROACTIVE complement — nudges a scenario interview when the project has specs but no `specs/SCENARIOS.md`, catching already-built projects the reactive reminder misses)
- `scripts/local-llm-call.sh` (telemetry funnel + auto-detect)
- `scripts/local-llm-detect.sh`
- `scripts/local-llm-stats.sh` (per-hook ROI reporter)
- `scripts/sync-local-llm-hooks.py` (deterministic settings.json wiring + scripts/ mirror — invoked in step 3.1a)
- `scripts/verify-local-llm-hooks.sh` (cross-check used by step 3.1a)
- `scripts/sync-core-hooks.py` (deterministic settings.json wiring for the core script hooks — pipeline/spec-register/execution/tech-stack; script-presence gated — invoked in step 3.1a-core)
- `scripts/sync-graphify-wiring.py` (deterministic settings.json wiring + scripts/ mirror for the Graphify integration — invoked in step 3.1b)
- `scripts/graphify-bootstrap.sh` (cross-platform Graphify self-installer — handles macOS brew, Linux apt/dnf/pacman/zypper, Windows Git Bash via scoop/winget/choco; idempotent; eligibility-gates by source-file count — invoked in step 3.1c)
- `scripts/graphify-fire-hook.sh` (PostToolUse Bash hook — logs every `graphify query|path|explain|update` invocation to `.claude/graphify-fire.log` with response bytes + graph node/edge counts)
- `scripts/graphify-stats.sh` (per-project Graphify ROI reporter — `--all` flag aggregates across `~/repos/*` and `~/Projects/*`)
- `scripts/project-freshness.sh` (local "keep the project fresh" pass — trufflehog verified-secret scan + key-shape scan for signing material in git history + `npm audit` dependency report; **self-installs trufflehog if missing** (brew/scoop/official-script, `--no-install` to suppress); report-first, `--fix` opt-in runs `npm audit fix --force` + mandates build/test. LOCAL only — never a CI/scheduled Action per `.claude/rules/github-actions.md`)
- `scripts/skill-audit.sh` (local "what skills am I loading?" pass — counts every `SKILL.md` under `~/.claude/skills` + `./.claude/skills`, estimates per-session baseline context cost, flags `[REVIEW]` bundles the project's stack does not use, warns past a soft ceiling. **REPORT-ONLY — never deletes** (global skills are shared; pruning is a developer decision). The complement to the install-only skill sync. LOCAL only — invoked in step 3c)

Note: `scripts/local-llm-*-hook.sh` files are NOT hand-globbed here. Step 3.1 invokes `sync-local-llm-hooks.py`, which atomically mirrors both the wiring AND the hook script files on disk (copying new ones, deleting orphans, verifying no wired hook is missing its script). Hand-globbing this set used to be a prose instruction here and proved unreliable — the LLM short-circuited the glob and produced settings.json entries referencing scripts that did not exist on disk, generating "No such file or directory" errors on every Edit/Bash. The deterministic helper closed that gap.

### 2. Compare and merge

For each file:

1. If the file does not exist in the target project, copy it from the template
2. If the file exists, compare and identify differences
3. Preserve any project-specific customizations (marked with `# PROJECT-SPECIFIC` comments)
4. Update generic template content to match the latest version
5. Report what was changed

### 3. Settings.json merge rules

For `.claude/settings.json`:

**Step 3.1a — local-LLM hooks (deterministic, run the helper script):**

Once `scripts/sync-local-llm-hooks.py` has been copied from the template to the project (in step 1), invoke it from the project root:

```bash
python3 scripts/sync-local-llm-hooks.py "$TEMPLATE/.claude/settings.json"
```

The script does TWO things atomically:

1. **Wiring** — removes every `bash scripts/local-llm-*-hook.sh` entry from the project's `hooks` block and replaces them with the template's exact set. Non-local-LLM hook entries are preserved verbatim.
2. **Scripts on disk** — copies every `scripts/local-llm-*-hook.sh` from the template into the project, and deletes any in the project that the template no longer ships. Template is the source of truth.

Finally it verifies that every wired hook has its script on disk and exits non-zero (with the list of broken refs) if anything is off. If step 3.1a exits non-zero, do NOT continue — investigate the message and rerun the script.

The script is idempotent and prints what it changed; capture that output for the report in step 6.

Do NOT try to merge local-LLM hook entries by hand and do NOT hand-glob `scripts/local-llm-*-hook.sh`. Both prose approaches proved unreliable (the LLM hedged on "REPLACE" wiring and short-circuited the script-copy glob, leaving 17 ghost references in one project). The script removes the ambiguity from both ends.

**Step 3.1a-core — core hooks (deterministic, run the helper script):**

The pipeline reminders, spec-register guard/orientation, pipeline state guard, spec-md-coverage, continuous-execution/stop-validation backstops, and the tech-stack hooks (tla, allium, sqlite, ui-design, test-coverage) are the core script-backed hooks. They used to be merged by prose ("UNION of hooks"), which is exactly what left projects missing the pipeline/register enforcement and forced a second `/project-update`. They are now deterministic. Once `scripts/sync-core-hooks.py` has been copied from the template (step 1), invoke it from the project root:

```bash
python3 scripts/sync-core-hooks.py "$TEMPLATE/.claude/settings.json"
```

It strips every template core hook from the project and reinstalls the template's current set — but only the hooks whose every referenced script already exists in the project. Script-presence is the tech-stack gate: a project that pruned `tla-hook.sh` never gets the tla hook back; one that kept it does. `permissions` and project-specific hooks are never touched. Idempotent (byte-stable on re-run). It exits non-zero with a list if any wired core hook is missing its script — if so, do NOT continue; investigate and rerun. Capture stdout for the report; the `skipped` lines record which tech-stack hooks the project deliberately lacks.

Do NOT hand-merge core hooks. Prose "UNION of hooks" is the exact failure this step replaces.

**Step 3.1b — Graphify wiring (deterministic, run the helper script):**

Same shape as step 3.1a but for the Graphify integration. Once `scripts/sync-graphify-wiring.py` has been copied from the template (in step 1), invoke it from the project root:

```bash
python3 scripts/sync-graphify-wiring.py "$TEMPLATE/.claude/settings.json"
```

The script does TWO things atomically:

1. **Wiring** — removes every existing graphify-related hook entry from the project's `hooks` block (both the PreToolUse Bash nudge and the PostToolUse Bash telemetry entry) and replaces them with the template's exact set.
2. **Scripts on disk** — copies every `scripts/graphify-*.sh` from the template into the project (`graphify-bootstrap.sh`, `graphify-fire-hook.sh`, `graphify-stats.sh`), and deletes any in the project that the template no longer ships.

Both wiring entries are universally safe to inject — the PreToolUse nudge guards on `[ -f graphify-out/graph.json ]` and silently no-ops when the graph is missing, and the PostToolUse hook bails out cleanly when the command isn't a `graphify (query|path|explain|update)` invocation. So wiring is decoupled from whether the project has actually bootstrapped Graphify yet.

Finally it verifies that every wired graphify hook has its script on disk and exits non-zero if anything is off. If step 3.1b exits non-zero, do NOT continue — investigate and rerun.

Do NOT try to merge graphify hook entries by hand. The historical prose approach ("add this snippet to your settings.json's Bash matcher block") dropped silently in roughly one project in ten, producing the juradrop / ighweld-2026 pattern: scripts copied, PreToolUse nudge in place, but the PostToolUse telemetry entry missing and the fire log never accumulating. The script removes the ambiguity.

**Step 3.1c — Graphify bootstrap (cross-platform, deterministic, builds the graph):**

After step 3.1b wires the project, run the bootstrap to actually install Graphify and extract the AST. The bootstrap is independent of the wiring — wiring can be present without a graph (entries no-op until the graph exists), but the inverse is not useful, so 3.1c runs whenever 3.1b succeeds:

```bash
bash scripts/graphify-bootstrap.sh
```

The script:

1. Counts eligible source files (`.cs/.ts/.tsx/.js/.jsx/.py/.go/.rs/...`) excluding vendored dirs. Skips silently if under 30 — Graphify install overhead exceeds savings on small projects.
2. Ensures `pipx` is on PATH. Self-installs via `brew`/`apt-get`/`dnf`/`pacman`/`zypper` (Linux/macOS) or `scoop`/`winget`/`choco` (Windows Git Bash); falls back to `python3 -m pip install --user pipx`. Exits non-zero with a platform-specific install hint if all paths fail.
3. Installs `graphifyy` via pipx if `graphify` is not already on PATH.
4. Runs `graphify install --project` to write the Graphify skill + PreToolUse hook to `.claude/`. Skips if `.claude/skills/graphify/SKILL.md` already exists.
5. Runs `graphify update .` for the initial AST extraction (NOT `graphify .` — the bare command requires an LLM API key; `update` is AST-only and offline). Skips if `graphify-out/graph.json` already exists.
6. Runs `graphify hook install` for git post-commit / post-checkout auto-rebuild. Skips if already installed.
7. Appends `graphify-out/` and `.claude/graphify-*.log` to `.gitignore` if missing.

After bootstrap, verify with the exit-condition snippet — this is the gate that confirms wiring + scripts + graph are all in place:

```bash
command -v graphify && test -f graphify-out/graph.json && test -x scripts/graphify-fire-hook.sh && grep -q 'graphify-fire-hook.sh' .claude/settings.json && echo "[OK] graphify wired" || echo "[FAIL] something missing"
```

If this prints `[FAIL]` the sync is incomplete — do NOT continue. Inspect which check fired and rerun the relevant step (3.1b for missing scripts/wiring, 3.1c for missing graph).

**Step 3.2 — non-local-LLM hook entries and other settings (merge):**

For everything else in `settings.json`:
- MERGE `permissions.deny` lists (union of both).
- MERGE `permissions.allow` lists (union of both) — the template's allow list has expanded git/gh entries (`git push:*`, `git pull:*`, `git fetch:*`, `git checkout:*`, `git switch:*`, `git branch:*`, `git merge:*`, `git rebase:*`, `git stash:*`, `git tag:*`, `git restore:*`, `git cherry-pick:*`, `git status:*`, `git diff:*`, `git log:*`, `git show:*`, `git blame:*`, `git remote:*`, `git config --get:*`, `git config --list:*`, `gh pr:*`, `gh issue:*`, `gh repo view:*`, `gh run view:*`) which the project should pick up.
- If `permissions.ask` contains `Bash(git push *)`, REMOVE it (the template has moved this to allow). Other `permissions.ask` entries are preserved.
- MERGE non-local-LLM `hooks` entries — add missing hooks from the template, preserve existing custom hooks.
- SET `"outputStyle": "Proactive"` if the project has no `outputStyle` key. A built-in style (v2.1.237+) that modifies the **system prompt**, where CLAUDE.md only adds a user message after it — so this is the strongest place the autonomy rules in `.claude/rules/continuous-execution.md` can live. If the project already sets an `outputStyle`, leave it: someone chose that on purpose. Do **not** set `Concise` — it fights the per-finding surfacing in `.claude/rules/validation-followup.md` and the per-spec status summary, both of which are verbose by design.
- Preserve any project-specific settings not in the template.

**Step 3.2.1 — inline-hook OVERWRITE exceptions (the template version wins):**

The merge rule above defaults to preserving customizations, but the following inline hooks have intentionally evolving behavior and MUST be replaced with the template version verbatim — do NOT preserve the project's older copy even if it differs. Match each by the unique grep pattern inside its command string and overwrite the entire hook object with the template version:

| Hook | Match by command containing | Why it must be overwritten |
|---|---|---|
| `UserPromptSubmit` speckit pipeline mandate | `speckit[.:_-](specify\|plan\|tasks\|implement)` or `speckit[.:_-](specify\|clarify\|plan\|tasks\|implement)` | Pipeline phase list evolves; new steps (e.g. `/clarify` between specify and allium, `/speckit.analyze` between tasks and implement) get added over time. The template version mandates `/clarify` immediately after `/specify` on every track and `/allium:elicit` after `/clarify` on full/light tracks — if the project's hook is missing the clarify step, overwrite it. |
| `UserPromptSubmit` speckit.analyze auto-apply | `speckit[.:_-](analyz\|analys)` | Behavior changed from "Reply suggest & apply for all" UX to immediate auto-apply + auto-chain to `/speckit.implement`. The old UX must be removed, not preserved. |
| `UserPromptSubmit` speckit.clarify auto-pick | `speckit[.:_-]clarif` | New hook (auto-picks Recommended). Add if missing; if present in any older form, replace with the template version. |
| `PostToolUse` Edit\|Write spec-completeness `type:"prompt"` | `INTERACTIVE UI` or `always approve and use systemMessage for the reminder` | The LLM-judgment version was observed BLOCKING edits on specs that legitimately carved destructive tests to a later slice (the prompt said "Do NOT block" but the model overrode it under pressure from CLAUDE.md / memory rules). Replace the entire prompt-hook object with the template's `type:"command"` entry pointing at `scripts/spec-md-coverage-reminder-hook.sh`. The new script is deterministic, can never issue a `permissionDecision`, and detects carve-out phrases ("carved to", "out-of-scope", "deferred to", etc.) to suppress false-positive reminders. |

If you find a project's `settings.json` has the OLD analyze hook (containing the phrase `Reply **suggest & apply for all**` or `analyze.md Step 8 default of asking before applying.`), this is the legacy version — overwrite it. Mention the overwrite in the step-6 report so the user knows the analyze behavior has flipped from semi-manual to fully auto.

If you find a project's `settings.json` has the OLD spec-completeness prompt hook (a `PostToolUse` entry with `type:"prompt"` whose prompt contains `INTERACTIVE UI` or `always approve and use systemMessage for the reminder`), this is the legacy LLM-judgment version that was incorrectly blocking edits — overwrite it with the deterministic command hook from the template. Mention the overwrite in the step-6 report so the user knows the spec-completeness check is now deterministic and no longer LLM-mediated.

### 3a. .gitignore — the harness block

The harness writes files that are machine-local in every project: attempt counters, the maintenance
due-state, the bash-write guard's markers, `settings.local.json`, and so on. The list lives in one place,
`HARNESS_IGNORES` in `scripts/harness-gitignore.sh`, with a reason per path. Do not copy it into
`.gitignore` by hand. Write it with the script:

```bash
bash scripts/harness-gitignore.sh --apply .     # prints added / updated, or nothing when current
bash scripts/harness-gitignore.sh --tracked .   # what the index already holds under those paths
```

`--apply` owns the lines between `# >>> claude-code harness … >>>` and `# <<< claude-code harness <<<`
and leaves everything else in `.gitignore` alone. Autosync runs it on every sync, so this step matters
only for a project that has not synced since spec 040. It exits 3 without writing when the markers are
broken (a start with no end, two blocks); fix them by hand.

`--tracked` output is not fixed by the ignore. An ignore rule changes nothing for a file git already
tracks. Report each path to the user with `git rm -r --cached -- <paths>`, and run it only when they say
so: it changes what the next commit records.

A marker written by a hook **the template does not ship** does not belong in `HARNESS_IGNORES`. That
script is CORE, so a project's line in it is eaten by the next sync. Classify those in the project-owned
`.claude/.runtime-markers` instead (`[machine-local]` / `[tracked-by-design]` sections, `path%reason`
lines) and ignore them outside the managed block. `scripts/test-runtime-markers-ignored.sh` fails when a
machine-local path the scripts write is missing from the managed list or from the project's `.gitignore`.

### 3b. Freshness pass (ALWAYS RUNS — regardless of sync mode)

This runs on **every** `/project-update` — full, incremental, or "already current" no-op. It is the recurring "keep the project fresh" ritual: it catches newly-disclosed dependency CVEs and newly-committed secrets independent of whether any template file changed. Do NOT skip it just because the sync was incremental or the project was already up to date.

After `scripts/project-freshness.sh` has been copied from the template (step 1) and made executable, run it from the project root (report-first):

```bash
chmod +x scripts/project-freshness.sh
bash scripts/project-freshness.sh
```

It runs these LOCAL checks (never as a GitHub Action — that violates `.claude/rules/github-actions.md`):

1. **trufflehog** — verified-secret scan of the repo (git history, or working tree if not a git repo). **Self-installs trufflehog if missing** (brew → scoop → the official install script into `~/.local/bin`, mirroring `graphify-bootstrap.sh`); falls back to a skip + manual-install hint only if every install path fails (or `--no-install` is passed). Never hard-fails the sync.
2. **key-shape scan** — Data Protection key rings, PEM/OpenSSH private keys and `.pfx`/`.p12` anywhere in git history, found by name and content because trufflehog cannot verify them. Needs only git. Harmless fixtures go in `.secret-shapes-allow` with a reason.
3. **npm audit** (and osv-scanner, dotnet) — dependency-CVE report for every non-vendored manifest.

This step is **report-first**: it does NOT mutate the tree. Surface the result to the user:

- **Verified secrets or key files found** → STOP and tell the user to rotate them immediately; a committed credential or key is compromised, even when it is in history only. Do not proceed past this silently.
- **npm advisories found** → report the counts and the remediation path. `npm audit fix` (safe, semver-compatible) is the default suggestion. `npm audit fix --force` pulls in breaking major bumps, so only run it on explicit user confirmation, and when you do, follow it with a full `npm run build && npm test` (or `dotnet build && dotnet test` when the React build feeds `wwwroot`) before committing. `bash scripts/project-freshness.sh --fix` does exactly this (force + verification reminder) in one shot.
- **Clean** → note it in the step-6 report and move on.

Do not auto-run `--fix` during a sync. Forced dependency upgrades are a user decision, not a silent side effect of syncing config.

### 3c. Skill audit (ALWAYS RUNS — regardless of sync mode)

The complement to the skill install: that step only ever *adds* skills, so a machine accretes globally-installed `SKILL.md` files over time, each costing baseline context at every session start. This step makes that cost visible on every sync. After `scripts/skill-audit.sh` has been copied (step 1) and made executable, run it from the project root:

```bash
chmod +x scripts/skill-audit.sh
bash scripts/skill-audit.sh
```

It counts every skill under `~/.claude/skills` (global, shared) + `./.claude/skills` (project), estimates the per-session baseline-context cost (name + description only — full bodies load on fire), detects the project's stack (`.claude/.sync-stack`, else markers), and flags `[REVIEW]` bundles the stack plainly does not use. It is **report-only and NEVER deletes** — global skills are shared across all projects, so a bundle this project's stack does not use may still be needed by a sibling. Surface in the step-6 report:

- **Total skill count + estimated baseline tokens** — the headline number.
- **`[CEILING]`** — global count over the soft ceiling; note it and point the developer at the `[REVIEW]` bundles. Do NOT auto-remove anything.
- **`[REVIEW]` bundles** — list as "stack-irrelevant to THIS project (review before removing — global/shared)".

Pruning a global skill is a developer decision, exactly like `--fix` on the freshness pass — never a silent side effect of syncing.

### 4. CLAUDE.md handling

Do NOT overwrite the project's CLAUDE.md. Instead:
- Check if the project's CLAUDE.md references `.claude/docs/skills.md` — if not, update the reference
- Check if `.claude/skills/` is mentioned in the file organization section — if not, add it
- Report any sections that differ from the template for manual review

### 5. Bootstrap caveat

If the project's `sync-template/SKILL.md` is OLDER than the template's, the current sync run is using outdated instructions. After the run, the project's SKILL.md will have been updated — but the changes you just made followed the OLD rules. Tell the user to re-run `/project-update` once more so the new rules take effect. If the SKILL.md was already current, this step is a no-op.

### 6. Report

After syncing, output a summary:

```
Synced from template (YYYY-MM-DD):
- [CREATED/UPDATED/SKIPPED] .claude/skills/code-review/SKILL.md
- [CREATED/UPDATED/SKIPPED] .claude/agents/dotnet-reviewer.md
- ...

Skill audit (step 3c — report-only, nothing deleted):
- Stack detected: web | mobile | hybrid | unknown
- Skills installed: <N> (~<T>k tokens baseline context per session)
- [REVIEW] stack-irrelevant bundles (global/shared — review before removing): <list or none>
- Soft ceiling: within | EXCEEDED

Project-specific files preserved:
- .claude/agents/custom-agent.md
- ...

Manual review needed:
- CLAUDE.md: section X differs from template
- ...
```
