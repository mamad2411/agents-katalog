---
name: feature-implement
description: Execute a feature plan from features/feature-v<N>-<description>/ stage-by-stage on the current branch, following the plan's TDD cycle. Use when the user asks to implement, build, execute, or roll out a plan that already exists — typically as a follow-up to /feature-plan. Refuses to start without both the design and plan files on disk (delegated to feature-resolve). Syncs the repo's current branch with remote first, never creates a new branch, never pushes. Establishes a test baseline first; if any tests already fail, it stops and offers to investigate, file a bug, or halt rather than building on a red suite. Before the stage loop, resolves an execution strategy by rule rather than asking, partitioned by the plan's execution schedule: serial batches run as consecutive three-stage subagent units by default (direct in the main agent when the user asked for that, when two or fewer stages remain, or when almost nothing is delegatable), and the stages of a parallel batch build concurrently — up to four subagents at a time, each in a throwaway detached git worktree this skill creates and removes — with every stage's commit cherry-picked onto the current branch in stage order, still one commit per stage. After each stage: checks coverage against the stage plan, self-reviews the code for bloat / duplication / orphaned-and-superseded code / functional issues / inefficiency / security / design-language conformance, runs tests, and commits. At the end, runs a whole-project dead-code sweep (baseline-scoped, so it removes only orphans this feature stranded), updates the per-feature tracker, surfaces any improvements to this skill itself, and closes by offering to run the plugin's two eval skills (evals-code-run + evals-e2e-run) in parallel read-only subagents. Step 0 confirms with the user via AskUserQuestion before doing any work when invoked proactively; the confirmation is skipped when the user explicitly typed /feature-implement. Because this skill writes code and commits, the proactive-invocation confirmation is non-negotiable.
user-invocable: true
disable-model-invocation: false
argument-hint: "[solo] <optional v<N> to target a specific feature, or omit to use the latest with a plan>"
allowed-tools: Read, Grep, Glob, Write, Edit, AskUserQuestion, Skill, Agent, Bash
---

# feature-implement — Stage-By-Stage TDD Implementation Of A Plan

You are running the `feature-implement` skill. The user may have arrived here by typing `/feature-implement` (with an optional version in `$ARGUMENTS`), by chaining in from `/feature-plan`, or because the model proactively invoked the skill. Your job is to actually build the feature described in the plan at the path returned by `/feature-resolve`, one stage at a time, on the current branch, committing after each green stage.

**Terminology (plugin-wide).** Two words are overloaded; keep them apart. A **step** is a numbered step of *this skill's own procedure* — the `## Step …` headings below (e.g. *Step 4*); the only other "steps" are the **TDD steps** inside a plan stage (write test → confirm fail → implement → confirm pass). A **stage** has two senses: a **chain stage** is one of `storm → design → plan → implement` (it shows up as `stage=…`, `stage_file`, and the tracker's `data-stage`), while a **plan stage** is a committable unit of work *inside* the implementation plan (e.g. `Stage 1`) — `/feature-plan` creates these and `/feature-implement` builds one per commit. A procedure step is never a plan stage, and a plan stage is never a procedure step.

This skill has twelve steps (Steps 0–11). Execute them in order. Do not skip Step 0 (proactive-invocation confirmation), Step 2 (file readiness), Step 3 (repo readiness), Step 5 (strategy choice + TDD loop), Step 7 (final coverage & dead-code sweep), Step 8 (tracker update), or Step 9 (lessons capture) — they are the load-bearing steps.

## Step 0 — Confirm before proceeding (when invoked proactively)

This skill writes code and creates commits — proactive invocation without a clear opt-in is much higher cost than for `/feature-design` or `/feature-plan`. The Step 0 check is therefore strictly enforced.

Check the most recent user message in the conversation for the literal tag `<command-name>/feature-implement</command-name>` or its plugin-qualified form `<command-name>/<plugin>:feature-implement</command-name>` (or, equivalently, a leading `/feature-implement` typed by the user). If present, the user has explicitly opted in via the slash command — skip this step and continue with Step 1.

Also treat as opt-in (and skip this step) if you were just invoked as a chain from `/feature-plan`'s Step 11 — i.e. the immediately previous turn was an `AskUserQuestion` result with header `"Run /feature-implement?"` and the user selected the option starting `"Yes, run /feature-implement"`. In that case the user has already confirmed; do not re-ask.

Otherwise (you arrived here because the model decided to invoke this skill proactively from natural-language intent, with no recent chained opt-in), call `AskUserQuestion` exactly once before any other work:

- **question**: `"Launch /feature-implement to build the feature staged in <plan version, e.g. v3>? This will write code and create one commit per stage on the current branch."` — name the specific version you'd implement.
- **header**: `"Run /feature-implement?"`
- **options**:
  - `{ "label": "Yes, proceed", "description": "Run the skill stage-by-stage on the current branch, committing each green stage." }` (mark this as Recommended)
  - `{ "label": "No", "description": "Don't run; I'll redirect." }`

If the user picks "No" or "Other", stop immediately. Do not write any files, run any tests, or create any commits.

## Step 1 — Resolve the feature folder via `feature-resolve`

**Load your customisations.** First in this step, read the house rules the user recorded for this skill with `/skill-customize feature-implement`. It sits here rather than in Step 0 deliberately: a run the user declined must never have read, announced or applied a customisation first.

**Resolving `${CLAUDE_PLUGIN_DATA}`.**

```text
${CLAUDE_PLUGIN_DATA} is a plugin-config substitution token: Claude Code expands
it inside plugin hook, MCP and LSP command strings, and it is not an exported
environment variable, so a shell that simply reads it almost always gets nothing
back. Resolve the directory yourself, taking the first rule that yields a path:

1. `$CLAUDE_PLUGIN_DATA`, on the chance the environment really does set it.
2. `<config-dir>/plugins/data/<plugin>-<marketplace>`, derived from the running
   skill's own base directory: an installed plugin runs from
   `<config-dir>/plugins/cache/<marketplace>/<plugin>/<version>/skills/<slug>`,
   so `<plugin>` and `<marketplace>` are the two path segments above the version,
   and Claude Code keys the data directory on exactly that pair.
3. The single `<config-dir>/plugins/data/dev-skills*` directory, when `ls` shows
   exactly one. Two of them means a stale second install is present and the rule
   is ambiguous, so it is skipped rather than guessed at.
4. `<config-dir>/plugins/data/dev-skills` — reached only when the plugin is
   running from a working clone rather than an installed copy.

`<config-dir>` is `$CLAUDE_CONFIG_DIR` when that is set, and `~/.claude` when it
is not. A skill's customisation file is then `<extras-dir>/<slug>.extras`.
```

Read `<extras-dir>/feature-implement.extras`.

**A missing file is the ordinary case. Say nothing at all and carry straight on with the rest of this step.** Most projects never customise this skill, and a "no customisations found" line on every run is noise on the common path. The same applies if the file cannot be read for any other reason: carry on without it. A customisation is a preference, and failing to load one never blocks a run.

When the file does exist, treat every `- ` bullet in it as an instruction that applies to this run, on top of everything below. Announce it in one line — `Customisations active: <n> (feature-implement.extras)` — and then actually apply it. Customisations legitimately change defaults, counts, thresholds, tone, formats, which optional behaviours fire, and what you settle yourself instead of asking: the execution strategy (a standing "always run Direct" is an explicit user request under Step 5's rule, and a durable one), how aggressive the final dead-code sweep is, which self-review lenses get extra weight, and how much detail the per-stage reports carry.

**They never override the *Constraints (non-negotiable)* section at the end of this file.** `/skill-customize` refuses that kind of instruction at write time, so one arriving here means the file was hand-edited. Ignore that bullet, name the constraint it collides with in one line, and carry on with the rest. The file is never permission to build on a red `TEST` baseline, batch or skip stage commits, deviate from the mandated commit-message format, create or switch branches, or push.

The customisations belong to the **main agent**, exactly as the usage window does. Step 5's stage subagents never resolve the data directory and never read the file themselves — you loaded it once, here, and you pass the text down in each unit's brief. Re-resolving it inside a fresh context is both wasteful and a way for two units to end up reading different files.

**Check the session.** If `<extras-dir>/session-control.extras` does not exist, skip this block: say nothing and carry on. Otherwise invoke `session-control` via the `Skill` tool with the argument `ensure feature-implement`. It runs inline. On `next: continue`, **do not end your turn** — carry straight on. On `next: end-turn` it has queued a relaunch of this skill on the session this stage is configured for: end your turn now and do nothing else. The relaunch starts this run again from Step 0, and nothing has been opened or written that needs closing — which is why this check sits before the usage window.

**Start the usage window.** Immediately after the session check, invoke `usage-report` via the `Skill` tool with the argument `start feature-implement`, so the final step can report what this run cost. It runs inline, prints nothing, and is a silent no-op when `CLAUDE_CODE_SESSION_ID` is unset — **do not end your turn**, carry straight on with the rest of this step. It sits here rather than earlier deliberately: a declined confirmation, or a relaunch that ends the turn at the session check, must never leave a start marker behind with no report to clear it.

**Control tokens.** Before any other argument parsing, read the leading tokens of `$ARGUMENTS` in the order `[solo] [v<N>] [from=<slug>]`. Strip `solo` when it is the exact lowercase first token, and `from=<slug>` when it is the next token after `solo` and the version token (whichever of the two are present), and remember both; `from=`'s value is not validated. Leave the version token in place for the detection below. When `solo` was read, say so in one line — `Solo run: this stage will not hand over.` — so a requirements statement that merely starts with that word is caught at once.

Parse `$ARGUMENTS` for an explicit version token only — `/feature-implement` does not take requirements text or a description.

- Look for a leading `v<N>` or `version <N>` (case-insensitive; bare `1` does **not** count — only `v1` / `v 1` / `version 1`). If found, record as `explicit_version` and strip from the input. Integer only.
- Free-form text other than the version is ignored.

Invoke `feature-resolve` via the `Skill` tool with the argument string:

```
stage=implement[, version=<N>]
```

Include `version=` only if Step 1 captured an `explicit_version`. Do not pass `description=` — the description is authoritative from the feature folder.

The resolver enforces all of the following:

- Without a version arg, it picks the latest `features/feature-v<N>-<desc>/` folder that has a plan file but no implement file (Rule C) — exactly the right target.
- If the latest folder already has an implement file, the resolver asks the user whether to overwrite or target an older version.
- If no plan exists anywhere, the resolver errors and tells the user to run `/feature-plan` first. Surface that error verbatim and stop.

Parse the resolver's output block. Record `mode`, `version`, `description`, `feature_folder`, `stage_file` (the implement-output path, if you later need to emit one — currently unused; this skill creates commits rather than a single .md), `prereq_file` (the **plan** file), and `tracker_file`. Use these verbatim downstream.

If the resolver stops with an error, pass the message to the user verbatim and stop. Do not retry with invented arguments.

**`feature-resolve` runs inline in this turn — do not end your turn when its result block appears.** The `Skill` tool loads it into your own context rather than delegating to a subagent, so the block is a checkpoint in the middle of *your* run, not a hand-off that returns control anywhere. Once you've recorded the fields above, continue straight into Step 2 in the same turn. Stopping here strands the user with a resolved plan path and nothing built.

## Step 2 — Read the plan, read the design, sanity-check both

The resolver returned `prereq_file` = the plan. Construct the design path from `feature_folder` + `version` + `description`:

```
<feature_folder>/feature-design-v<version>-<description>.md
```

Verify the design file exists with `ls` / `test -f`. If it does not (the resolver should have refused this case, but defend), stop with a one-line error naming the missing path.

`Read` both files in full now. Build an internal model:

- From the design: requirements (§3), components (§5), security/performance/observability decisions (§5), risks (§7), rollout (§9).
- From the plan: every stage with its TDD steps, files touched, definition of done, and the Requirements coverage map.
- From the plan's *Execution schedule*: the batches, each one's mode and stage list, and the critical path. A plan written before that section existed has none: treat every stage as its own serial batch, and say so in one line in Step 5's strategy announcement.

When the design cites `DESIGN.md` (its §5 *Design language* sub-section), `Read` it too: it is the project's recorded design language, which every UI stage follows. A design that does not cite it is implemented without it.

If plan §*Deviations from the design* is non-empty and unresolved, surface it to the user via `AskUserQuestion` and ask whether to proceed as-is or pause for a design refresh (a new feature version via `/feature-design`). Do not silently override.

If a brainstorm file also lives in `feature_folder` (`feature-storm-v<version>-<description>.md`), you may `Read` it for context, but the plan is the binding contract — do not let the storm override the plan.

## Step 3 — Repo readiness

The skill works **on the current branch** and **never creates a new branch** or pushes.

Run these checks in order:

1. `git rev-parse --is-inside-work-tree` — confirm we are inside a git repo. If not, stop and tell the user.
2. Identify the repo's default branch (in priority order: the remote HEAD via `git symbolic-ref refs/remotes/origin/HEAD`, falling back to `main`, then `master`). Call this `<default>`.
3. `git status --short` — check for uncommitted changes.
   - **First, distinguish the chain's own churn from the user's work.** If the only uncommitted changes are this feature's own artifacts (`features/feature-v<version>-*` — the design/plan/tracker files left by the preceding chain stage), `DESIGN.md` and `design/specimen.html` at the project root (modified or untracked — `design-language-update` writes them during `/feature-design`), and/or files that are gitignored-but-tracked, this is the chain's own output, not the user's unrelated work: commit the feature docs and those two files directly as one `docs(...)` commit (ignoring the gitignored churn), note it in the final summary, and proceed. That commit is also what puts `DESIGN.md` into every parallel worktree. There is exactly one sensible outcome here, so offering costs a round-trip that buys nothing. This is near-guaranteed on chained `plan → implement` runs.
   - Otherwise, stop only for **modified or staged tracked files**: show the user what's modified and ask whether to commit/stash/discard before proceeding — do not touch their changes. Pre-existing *untracked* files outside the feature folder (other than the two above) cannot end up in a stage commit (every stage adds by explicit path): leave them alone, note them in the final summary, and proceed.
4. `git rev-parse --abbrev-ref HEAD` — get the current branch.
   - If the current branch is **not** `<default>`, warn the user (e.g. "You're on `feature/x`, not `<default>`. This skill normally implements on `<default>`. Continue on the current branch?") and proceed only if confirmed. Do **not** switch branches yourself. Do **not** create a new branch.
5. `git fetch --prune` — refresh remote refs. Also `git worktree prune`, so a throwaway worktree left behind by an interrupted run (Step 5's parallel batches) never blocks a new one.
6. Compare local against `origin/<current branch>` (use the current branch you're on, since you may have confirmed staying on a non-default branch). Cases:
   - **Up to date** → continue.
   - **Behind** → `git pull --ff-only`. If a fast-forward is not possible, stop and ask the user to reconcile.
   - **Ahead** → continue (your local has unpushed commits; that's fine — this skill never pushes).
   - **Diverged** → stop and ask the user to reconcile. Never resolve a divergence automatically.
   - **No remote configured for this branch** → continue and note in the final summary.

Only proceed past Step 3 when the tracked tree is clean (untracked scratch files noted and left alone) and the branch is either up to date or only ahead.

7. **Detect the project's tooling commands.** Before running anything, identify how this project runs **tests, lint, format-check, type-check**, and (where relevant) **build** and **dead-code analysis**. Inspect in this order:
   - Project manifests: `pyproject.toml`, `package.json` (scripts), `Package.swift` + any `*.xcodeproj`/`xcodebuild` wrappers, `Cargo.toml`, `go.mod`, `pom.xml`/`build.gradle(.kts)`, `Gemfile`, `mix.exs`, `composer.json`, `*.csproj`, etc.
   - Repo-level entrypoints: `Makefile`, `Taskfile.yml`, `justfile`, `fastlane/Fastfile`, `scripts/*` — often the canonical wrapper around raw tooling.
   - CI config: `.github/workflows/*.yml`, `.gitlab-ci.yml`, `.circleci/config.yml`, `azure-pipelines.yml`, `bitrise.yml`. CI shows the commands the maintainers treat as canonical.
   - Docs: `README.md`, `CONTRIBUTING.md`, anything under `docs/` (legacy reference material).

   Record the resolved commands as named slots — `TEST`, `LINT`, `FORMAT_CHECK`, `TYPE_CHECK`, `BUILD` (optional), `DEADCODE` (optional — a whole-program unused-code analyzer), and `PROVISION` (optional — the command that makes a fresh checkout runnable, used only to prepare the throwaway worktrees of Step 5's parallel batches: `uv sync`, `npm ci` / `pnpm install --frozen-lockfile`, `swift build`, `cargo fetch`, `./gradlew dependencies`, or `none` when the suite runs from a bare checkout). Reuse them by name through sub-point 8, Step 5, Step 5e, Step 5h, and Step 7 so command choice stays consistent across stages. Reference examples (adapt to what the project actually uses):
   - **Python (uv):** `TEST="uv run pytest -q"`, `LINT="uv run ruff check ."`, `FORMAT_CHECK="uv run ruff format --check ."`, `TYPE_CHECK="uv run mypy"`, `DEADCODE="uv run vulture src tests"`. `ruff` (LINT) already flags unused imports/locals; `vulture` adds unreachable functions/classes — raise `--min-confidence` or feed a generated whitelist (`vulture … --make-whitelist > whitelist.py`, then pass `whitelist.py`) to suppress dynamic-dispatch false positives. Swap `uv run` for `poetry run` / `hatch run` if those are configured instead.
   - **Swift (SwiftPM):** `TEST="swift test"`, `LINT="swiftlint"`, `FORMAT_CHECK="swift-format lint -r Sources Tests"`, `BUILD="swift build"`, `DEADCODE="periphery scan"` (auto-detects SPM; add `--clean-build` so the baseline and the Step 7 sweep both read a fresh index, and use `--write-baseline`/`--baseline` for the Step 3 baseline). Suppress known false positives with `// periphery:ignore` comments.
   - **Swift (Xcode):** `TEST="xcodebuild test -scheme <S> -destination <D>"`, `BUILD="xcodebuild -scheme <S> build"`, `DEADCODE="periphery scan --project <P>.xcodeproj --schemes <S>"`; prefer the project's fastlane lane or `Makefile` wrapper if present.
   - **JS/TS:** `TEST="pnpm test --silent"` (or `npm`/`yarn` equivalent), `LINT="pnpm lint"`, `FORMAT_CHECK="pnpm format --check"` or `prettier --check`, `TYPE_CHECK="pnpm tsc --noEmit"`.
   - **Go:** `TEST="go test ./..."`, `LINT="golangci-lint run"`, `FORMAT_CHECK="gofmt -l ."` (any output = unformatted), `TYPE_CHECK="go vet ./..."`.
   - **Rust:** `TEST="cargo test --quiet"`, `LINT="cargo clippy --all-targets -- -D warnings"`, `FORMAT_CHECK="cargo fmt --check"`; type-check is implicit in `cargo check`.
   - **Java/Kotlin (Gradle):** `TEST="./gradlew test"`, `LINT="./gradlew check"`, `BUILD="./gradlew build"`. Maven: `TEST="mvn -q test"`, `BUILD="mvn -q package"`.
   - **`DEADCODE` in other ecosystems:** JS/TS → `knip` or `ts-prune`; Go → `deadcode ./...` or `staticcheck`; Rust → the compiler's built-in `dead_code` lint (`cargo build` warnings, or `-D dead_code`). Where a language has no dedicated analyzer, leave `DEADCODE` unset rather than improvising — Step 7 recommends one.

   If a slot has no configured tooling for this project, set it to `none — no baseline` and skip the corresponding action everywhere downstream. (For `DEADCODE`, that means no baseline and no Step 7 sweep — but Step 7 still emits a one-line recommendation to adopt a suitable analyzer.)

   **`PROVISION` covers every dependency root the suite reaches, not the root manifest alone.** List the gitignored dependency directories and lockfiles the main tree holds (`git status --short --ignored`) — nested environments, per-package module directories — and chain one install command per root into the slot. Where a lockfile is itself gitignored or untracked, a clean-install form refuses or dirties a fresh checkout: copy the lockfile in from the main tree first (copy, never symlink), or use an install form that neither needs nor writes one.

8. **Baseline the test failures and lint/type state.** Using the commands recorded in sub-point 7, run `TEST` once and record the names of any tests that already fail on the unmodified working tree. Then run `LINT`, `FORMAT_CHECK`, and `TYPE_CHECK` once and record any pre-existing failures, with the offending files/rules, not just a pass/fail verdict. If `DEADCODE` is set, also run it once and record the pre-existing dead-code findings — prefer the tool's native baseline where it has one (`periphery scan --write-baseline baseline.json`, or vulture's `vulture … --make-whitelist > whitelist.py`) so Step 7's comparison is exact. Save these lists for use in Step 5e, Step 7, and Step 10. Any slot recorded as `none — no baseline` in sub-point 7 is skipped. Like the lint/type baseline, the dead-code list is an *exclusion set*, not a gate — it never blocks the run; it only marks pre-existing dead code that Step 7's sweep must leave alone. The recorded **test**-failure list also drives the pre-implementation gate in sub-point 9: a non-empty test baseline halts the skill (the user decides what to do) rather than being silently carried into the stage loop. The lint/type list, by contrast, is the set of pre-existing problems excluded from regression gating (it does not block — see the next paragraph).

   Step 5e's regression check compares post-stage test failures against the test baseline rather than against zero; any failure already in the baseline is not a stage-introduced regression. The lint/type baseline serves the same purpose: a lint or type error already present on the unmodified tree (commonly in generated/stamped files such as Python's `version.py`, Swift's `BuildInfo.swift`, or a JS `_version.ts`) is not a regression — only ones newly introduced by this implementation are. If a stage's changes clear a *baseline* test or lint failure, that's fine — drop it from the baseline silently. The lists only grow shorter, never longer.

9. **Pre-implementation test gate — never build on a red baseline.** If sub-point 8's `TEST` baseline recorded **any** failing or erroring tests, **do not continue to implementation.** A test suite that is already red before a single line of feature code means the ground is unstable, and Step 5e's regression machinery cannot reliably separate a newly introduced break from the existing mess. Stop here and call `AskUserQuestion` exactly once:

   - **question**: `"<count> test(s) already fail on the unmodified tree, before any implementation: <short list of failing test ids>. I won't build on a red baseline. How do you want to proceed?"`
   - **header**: `"Tests already failing"`
   - **options**:
     - `{ "label": "Investigate now", "description": "Pause and diagnose why these tests fail before deciding — usually the right first move." }` (mark this as Recommended)
     - `{ "label": "File a bug", "description": "Hand off to /bug-submit to file the failing tests as a bug, then stop without implementing." }`
     - `{ "label": "Stop", "description": "Halt /feature-implement now and leave the repo untouched." }`

   Act on the choice. **On any branch that stops the run** (*File a bug*, *Stop*, or an *Investigate now* that ends in one of those), first invoke `usage-report` via the `Skill` tool with `report feature-implement, tracker_file=<tracker_file>, feature_version=<version>, outcome=halted, cycle=true` — the run cost tokens even though it built nothing, and the chain stops here, so it prints the cycle report. Step 11 never runs on a halted baseline, so this is the only place the report fires.
   - **Investigate now** → do not enter the stage loop. Read the failing tests and the code they exercise and establish the root cause *with* the user (do not guess). Then, together: if the failures get resolved, re-run `TEST`; once the baseline is clean, resume from sub-point 8 and continue Step 3 normally. If the failures turn out to be real and out of scope for this feature, fall back to **File a bug** or **Stop** — never silently proceed on red.
   - **File a bug** → invoke the `bug-submit` skill via the `Skill` tool, passing a one-line description that names the failing tests and the `TEST` command as the argument. When it returns, **stop** `/feature-implement` without implementing, and tell the user to re-run it once the bug is fixed.
   - **Stop** (or "Other" with stop-like intent) → stop immediately. Make no edits and no commits; leave the repo untouched.

   **This gate fires even under an autonomous / "work without stopping" instruction** — like the Step 0 and Step 6 gates, a red baseline is a material condition that such instructions do not licence you to ignore. In a genuinely headless run with no channel to ask, default to **Stop** and report the failing baseline tests rather than building on them.

## Step 4 — Determine the starting stage

A run may be a fresh start or a resume. Detect prior stage commits for this feature version using the commit-message format from Step 5h. Anchor the grep on the closing paren so `v3` does not match `v30`:

```
git log --grep="(plan v<version>):" --oneline
```

Where `<version>` is the integer feature version returned by the resolver. Match each line against the format `<type>(plan v<version>): Stage N — <stage title>` to extract `N`.

Resolve the starting stage:

- If no prior stage commits exist for this version → start at **Stage 1**.
- If prior stage commits exist → resume at the **lowest uncommitted stage**. Briefly tell the user ("Detected Stages 1–3 and 5 already committed; resuming at Stage 4.") and proceed without asking. A gap below the highest committed stage is normal when a gated stage was skipped (below) or when a parallel batch (Step 5) landed only some of its stages; only a gap that neither explains, or mixed commit-message formats, is ambiguous — then ask via `AskUserQuestion`.
- If all stages appear already committed → tell the user the plan looks fully implemented; do not re-run stages. Skip to Step 7 (final coverage check) and then to Steps 8–10, but make no new commits.

**Scan for externally gated stages.** Before Step 5, scan the plan's remaining stages for external prerequisites — another repo's work deployed, a live service reachable, a credential or device present, an explicit gate marker in the stage text — and verify each named condition's current state with a cheap probe (`ls`/`grep`/one request), or by asking the user when it cannot be probed. Exclude stages whose prerequisite is unmet from Step 5's remaining-stage count `R`, and surface them in the strategy announcement line as blocked (e.g. `Stages 8–9 blocked on <condition> — implementing 10–11 only`), so the run's real scope is settled before any code lands rather than discovered mid-loop. On a resume where the committed history is non-contiguous because gated stages were skipped, resume at the **lowest uncommitted stage whose gate is open**.

## Step 5 — Resolve the strategy, then implement each stage (TDD loop)

The remaining stages (from the starting stage determined in Step 4 to the last) are implemented batch by batch, following the plan's *Execution schedule*: serial batches build in order in the shared working tree, and the stages of a parallel batch build concurrently, each in a throwaway detached worktree, then land on the current branch **in stage order**. Commits are the resume contract, and the shared working tree and index have exactly one writer at a time — concurrent work happens only in worktrees this skill created. Treat each stage as atomic: it either completes green and gets committed, or it is left uncommitted and the user is consulted.

### Resolving the execution strategy

**Do this before any stage work — do not skip it.** Decide *who* drives the per-stage TDD cycle (the `5a`–`5i` cycle below). Let `R` = the number of stages still to implement (last − starting + 1, minus any stage Step 4 excluded as externally gated).

**The default is chunked subagent execution, and it is not a question.** Do not ask the user to pick a strategy — announce the one you're using in a single line and continue in the same turn. Chunking is the default because the alternative to a unit boundary is not "more context" but a *lossy* boundary: the carry-forward note below can hand on public signatures, toolchain pins and deviations, but never the greps a subagent already ran, the fixture idioms it settled into, or the approaches it tried and rejected. Fewer boundaries means less of that rediscovered.

Run the **pre-scan** described under *Chunked* below first — rule 3 depends on its result. Then resolve the strategy in this order, first matching rule wins:

1. **The user asked for something specific** — they said "do it directly", "one stage at a time", "don't use subagents", or named a unit size, in this run or the message that launched it. Honour it without argument and without re-confirming.
2. **`R ≤ 2`** → **Direct**. Launch and briefing overhead exceeds the benefit at this size.
3. **The pre-scan left ≤1 delegatable stage** → **Direct** for the whole run.
4. **Otherwise** → **Chunked**: serial batches in units of `min(3, R)` consecutive stages, and the schedule's parallel batches as **parallel batches** (below) where they survive the pre-scan.

Then state the resolved strategy in one line before starting, including `R` and the partition, so the user can redirect in their next message without having to answer anything — e.g. `"9 stages remaining → batches: [1] serial, [2–4] parallel ×3, [5–7] one unit, [8–9] parallel ×2; Stage 7 runs here (live UI verification); worktree probe green (provision 40s)."` This line is the only checkpoint between Step 0 and code landing: it must name the scale and the batch shape, so make it concrete.

**Direct** — run the `5a`–`5i` cycle yourself for each stage in order, exactly as written below. Direct's real advantage is visibility: every edit lands in this conversation where the user can watch and interrupt mid-stage, rather than arriving as a report. That is why an explicit user preference (rule 1) always wins over the default.

**Chunked** — partition the remaining stages into consecutive units of `min(3, R)` stages (the last unit may be shorter). Before partitioning, pre-scan the stages and classify what each one's definition of done actually needs:

- **Probe before declaring a check manual.** A stage labelled live-UI / browser / visual is often machine-verifiable: check for a headless browser or renderer, a way to serve or load the real artefact with fixture data, or a programmatic way to drive the framework (load the built bundle and instantiate its entry point, render the real view offscreen and assert on its tree or a snapshot). Where such a route exists the stage stays delegatable, and the executor must run the checks rather than hand back a checklist. Likewise confirm any tool a stage must be *driven through* has a CLI or file-format entry point before the loop begins; a stage whose stated tool is GUI-only is surfaced to the user up front with the choice of handing it over or accepting an equivalent automated route.
- **Not subagent-doable** — needs a skill or context available only in this conversation, or provisions a new environment over the network (dependency installs — a sandboxed subagent typically has no network access). Run these in the main agent at their ordinal position, and say so in the announcement line. This carve-out is per *stage*, not per run: one such stage does not make the whole run Direct.
- **Not agent-doable at all** — a human must observe or act (a physical interaction, an OS consent dialog, judgement on a live screen). Do **not** move these to the main agent, which cannot perform the check either; keep them delegated and rely on the subagent contract's *Verification honesty* clause. Register every check no executor could perform in a run-level **pending-verification list**, and render that list in Step 10 as an explicit human hand-off checklist — a run never closes reporting stages "done" while human-only verification goes unmentioned. Nor is anything unperformed written up as performed: a later stage that consumes the result of an unperformed check or a gated stage (documentation quoting a measurement) ships the value as a stated target with a named backfill point, recorded under *Deviations from plan*, and a result the user reports is recorded as they gave it, with its provenance — one "all good" is never expanded into per-item findings.

**Shrink the next unit to 1 stage** only when the unit that just finished hit a Step 6 stop condition or failed the main-agent verification below — a missing or incorrect stage commit, out-of-scope files in `git show --stat`, or a failed independent `TEST` re-run. A deviation recorded in the plan and landed green is **not** a shrink trigger: a conscientious executor records refinements on almost every unit of a plan meeting a real codebase, and shrinking on them degrades every healthy run to units of 1. Trouble in one unit is the signal that the next needs tighter checking; an untroubled run keeps units at 3. Return to `min(3, remaining)` once a unit lands clean. The rule extends to batches: a batch that needed a `fix:` reconciliation, a conflict re-run or a Step 6 stop demotes the *next* parallel batch to serial and shrinks the next serial unit to one stage; a clean batch restores both.

#### Parallel batches

A batch the plan's *Execution schedule* marks *parallel* builds its stages concurrently: one subagent per stage, **up to four at a time** — a larger batch runs in waves, each wave landing fully before the next wave's worktrees are created from the new `HEAD` — each in a throwaway detached git worktree this skill creates, so the shared working tree and index keep a single writer. A customisation loaded in Step 1 may raise or lower the cap. Parallel batches exist only inside the **Chunked** strategy: rules 1–3 above resolve to Direct and leave nothing to run concurrently.

**Parallelism is off for the whole run** when the user asked for Direct, "one stage at a time" or "no subagents"; when the `Agent` tool is unavailable; when `R ≤ 2` (rule 2 stands — the probe and the provisioning cost more than one stage of wall-clock); when the worktree probe below fails; or when the user rejects any launch in a wave (a rejected launch is a strategy override, exactly as for units: the remainder runs Direct, and that wave's worktrees are removed). **A single batch is demoted to serial** — named in the strategy line with its reason — when the independence re-check fails, when a stage in it is not subagent-doable, needs network provisioning or is externally gated, or when a worktree cannot be created. A demoted batch's stages join the serial units at their ordinal position.

**Independence re-check.** Before trusting a parallel batch, re-check it from the live tree against the plan's seven independence tests, by name: *Disjoint files* (the pairwise *Touches* comparison is mechanical — do it), *No symbol or string-keyed dependency*, *No shared registration point*, *Same base state*, *Category exclusions*, *Security ordering*, *No shared test resource* (read the stage blocks and the tests they name). The plan judged these from the design; you judge them from the code as it is now. Any pair that fails, or that you cannot clear, demotes the batch.

**Worktree probe.** Once per run, before the strategy line is written, only when at least one parallel batch survives. `<scratch>` is the session's scratchpad directory when one is announced, else `${TMPDIR:-/tmp}/dev-skills/`; `<run-id>` is a short token unique to this run (e.g. `date -u +%Y%m%dT%H%M%S`). Run `git worktree add --detach <scratch>/wt-v<version>-probe-<run-id> HEAD`, run `PROVISION` from inside it (`cd <wt> && <PROVISION>` — the working directory does not persist between shell calls) with its exit status visible, never piped through a filter that hides it, and require `git -C <wt> status --short` to be empty afterwards: provisioning that rewrites a lockfile would poison every later clean-tree check. When `BUILD` is set, run it in the probe next: it proves a fresh checkout builds without the main tree's caches, and it warms the probe so the two runs below reach their test phase together. Then run `TEST` **in the probe worktree and in the main tree at the same moment** — one message, two Bash calls — and compare both runs' failure sets against the Step 3 baseline; suites that collide on a port, a database, a device or a temp path show up here rather than as a puzzling combined red later. A failed `PROVISION` or `BUILD`, or a new failure in either run, demotes every parallel batch with a one-line reason. Tests the probe *skipped* and the main tree ran are a different finding — a provisioning gap, not a collision: name it in the strategy line and demote only the batches whose stages touch or are verified by a skipped test, since the main agent's `TEST` after each cherry-pick still runs the rest. Record the provisioning wall time for the strategy line, then remove the probe worktree (`git worktree remove --force`).

**Carry-forward across batches.** Parallel siblings each receive the carry-forward note as of the batch's base commit, never each other's APIs. The unit or batch after a parallel batch receives the union of every landed sibling's *API introduced* list, plus any reconciliation commit.

#### Serial units

Then, **for each unit in order**:

1. **Re-derive the launch state from the live repo immediately before each launch — never reuse values captured at strategy-selection time.** Re-run `git log --grep="(plan v<version>):" --oneline` to establish which stages are already committed, and compute this unit's start stage from that result; if the tree has moved since the last unit returned (an interruption, a release cut, a user edit), re-run `TEST` and refresh the baseline too. A briefing built from stale numbers is how a relaunched unit re-implements an already-committed stage. Then launch a subagent with the `Agent` tool (called `Task` in some Claude Code versions) — `subagent_type: general-purpose`, **default isolation, not a worktree** (it must commit on the *current* branch in the shared working tree; a parallel-batch subagent also uses default isolation — its worktree is one this skill created and passed as a path, never the harness's worktree option). Brief it with the **subagent contract** below. Launch one unit at a time and wait — never launch the next unit before this one returns.
2. When it returns, verify in the main agent — treat the subagent's report as a claim to check, not a result to trust:
   - `git log --grep="(plan v<version>):" --oneline` — confirm a commit exists for every stage the unit was meant to deliver, and `git status` shows a clean tree.
   - `git show --stat` each new stage commit — confirm it touched only that stage's expected files (catches stray files swept in, and inaccurate self-reports).
   - Re-run `TEST` (and `BUILD`, when set and the unit touched non-test code) yourself — the command's exit status is the sole pass/fail authority; never accept the unit's green claim, editor/indexer diagnostics, or the presence/absence of console output in its place.
   - Scan the unit's touched files for newly introduced compiler/linter diagnostics and reconcile them against that authoritative `TEST`/`BUILD` result: fix real ones in a follow-up commit before the next unit launches; treat isolated-analysis false positives (e.g. unresolved same-module or test-framework symbols outside the real build graph) as non-blocking.
   - Read the report's *Handed forward* list, and its risk and pending-verification lines for anything that is really a testable defect. Each item is **resolved, not noted**: it goes into the next unit's brief as required work, with the files it needs added to that unit's scope — or, after the last unit, into Step 7's added stage — and under *Deviations from plan* either way. One that needs a design decision is a Step 6 stop.
3. If any expected stage commit is missing, or the subagent reported a Step 6 stop condition, **do not launch the next unit** — surface the subagent's report to the user and decide together (same handling as Step 6). A deviation the unit recorded in the plan and landed green is not a stop: note it and continue. Step 4's resume logic lets you continue later from the last committed stage.
4. If the unit's subagent times out, crashes on an infrastructure error, returns no report, is interrupted mid-run, or has its launch **rejected by the user**, do not assume wholesale failure and do not re-run the unit. A rejected launch is a strategy override: switch to **Direct** for the remainder of the run and do not re-ask which strategy to use. Reconcile from the main agent: `git log --grep` to identify which of the unit's stages already committed, then handle whatever the working tree holds:
   - **A complete stage, uncommitted, that verifies green** (run `TEST`) → commit it from the main agent with the standard message format.
   - **An incomplete stage whose tests fail on a substantive assertion** → that is a legitimate red point in the TDD cycle, not damage. Leave it uncommitted and hand it forward: give the replacement executor the partial state and the exact failing output, and tell it to review the inherited work critically before completing it. Never discard test-first work that was doing its job, and never commit a stage that has not verified.

   Then resume only the remaining stages — a fresh subagent with an updated carry-forward note, or directly for a small trailing stage. Never re-run an already-committed stage.
5. Otherwise continue to the next unit.

#### Parallel batch procedure

For each parallel batch, and each wave within it:

1. **Re-derive the launch state** exactly as for a unit: `git log --grep`, a clean `git status`, and `base = HEAD`.
2. **Create the worktrees.** Per stage in the wave: `git worktree add --detach <scratch>/wt-v<version>-stage-<N>-<run-id> HEAD`, then `cd <wt> && <PROVISION>` when set. `git -C <wt> status --short` must be empty afterwards; if it is not, or the `add` fails, that stage leaves the wave and runs serially after it.
3. **Launch the wave in one message** — one `Agent` call per stage, `subagent_type: general-purpose`, default isolation (the worktree is yours, passed as a path — never the harness's worktree option). Brief each with the **subagent contract** below plus its **parallel addendum**. Wait for all of them.
4. **Check the main tree is untouched**: `git status --short` must be empty. A dirty main tree means a subagent leaked out of its worktree — handle as Step 6's externally-dirtied-tree stop, after landing whatever verifies.
5. **Land in ascending stage number**, deriving every fact from git rather than from the report: `git -C <wt> log <base>..HEAD --oneline` must show **exactly one** commit, whose subject is that stage's (anything else fails verification and the stage runs serially instead); `git -C <wt> show --stat HEAD` must touch only that stage's expected files; `sha=$(git -C <wt> rev-parse HEAD)`. Then `git cherry-pick <sha>` on the current branch and run `TEST` (and `BUILD`, when set and the stage touched non-test code). Commits therefore land on the branch in stage order, one per stage, messages intact — the sha changes, nothing else does.
   - **Cherry-pick conflict** → `git cherry-pick --abort`; the schedule was wrong about that pair. Re-run the stage serially *now*, in the main tree (a fresh subagent or Direct, per the unit rule), then continue with the next sibling — never land a later sibling first.
   - **Combined red** after a clean cherry-pick, though the stage was green alone → diagnose. A small reconciliation between the two stages lands as `fix: reconcile Stage <N> with Stage <M> after parallel landing` (no `(plan v<version>):` tag; touches only files in the batch's *Touches* union; adds no behaviour beyond making both stages' tests pass) and is recorded under *Deviations from plan* as a schedule defect. Anything larger is a Step 6 stop with the landed commits kept.
6. **Reconcile every worktree before removing it** — the crash-recovery rule for units applies per worktree: a complete stage commit not yet landed → cherry-pick it; a green uncommitted stage → commit it there with the standard message, then cherry-pick; a red partial whose tests fail on a substantive assertion → `git -C <wt> diff > <scratch>/wt-v<version>-stage-<N>-<run-id>.patch` and hand the patch path plus the failing output to that stage's serial re-run. Name every unlanded sha and patch path in any stop report.
7. **Remove the worktrees**: `git worktree remove --force <wt>` and `rm -rf <wt>.tmp` for each, then `git worktree prune`. Never leave a worktree behind — not at the end of a batch, not on a stop.
8. **Record what the subagents could not.** Their deviation text goes into the plan file's *Deviations from plan*, and their pending human-verification items into the run-level list, written by the main agent in one `docs:` commit after the batch lands. *Handed forward* items are resolved as for a serial unit. Siblings also built blind to each other: run 5g's *Duplication / reuse* lens once over the batch's combined diff (`git diff <base>..HEAD`) and hand logic two siblings each wrote to the next unit as a hoist-first task.
9. Stages that left the wave (demoted, failed verification, conflicted, stopped) run serially at their ordinal position before the next batch starts.

Whoever executes, the `5a`–`5i` cycle is identical — nothing about TDD, self-review, coverage, commit format, or the git constraints changes; only the executor does. The final coverage & dead-code sweep (Step 7), tracker update (Step 8), lessons capture (Step 9), summary (Step 10), and eval offer (Step 11) **always run in the main agent** after every unit and batch completes, never inside a subagent (the evals a user accepts in Step 11 are themselves delegated to subagents, but the offer and the launch are the main agent's).

#### Subagent contract (chunked mode)

A subagent starts with a fresh context and cannot see this conversation, so its briefing must be self-contained. Pass, as the prompt, the bullets below. On a run of more than three launches, write the run-invariant ones — Files, Design language, Tooling, Baseline, Customisations, Conventions, Discipline, Git constraints, Stop conditions, Verification honesty, Handed forward, Return format — once to `<scratch>/brief-v<version>-<run-id>.md` before the first launch, and keep the carry-forward note in `<scratch>/carry-v<version>-<run-id>.md`, rewritten after every unit or batch lands. Each prompt then carries Scope, anything specific to that unit, and both paths, with the instruction to `Read` them in full before anything else. One file is one contract: edit it when a rule changes mid-run, never restate it per launch.

- **Scope** — "Implement **only** stage `<N>` [through `<M>`] of the plan, test-first; do not touch any other stage."
- **Files** — absolute paths to the plan file (`prereq_file`) and the design file; tell it to `Read` both and re-read the target stage block before coding.
- **Design language** — the absolute path of `DESIGN.md` when the design cites it — under the stage's worktree for a parallel unit — or `none`. UI stages re-read it in 5a and review against it in 5g.
- **Tooling** — the resolved `TEST` / `LINT` / `FORMAT_CHECK` / `TYPE_CHECK` / `BUILD` commands from Step 3 verbatim (or "none" where unset).
- **Baseline** — the Step 3 lists of pre-existing test and lint/type failures, so it gates regressions against the baseline, not against zero.
- **Customisations** — the `- ` bullets you loaded in Step 1 from `feature-implement.extras`, copied verbatim, or the single word `none`. They apply on top of the `5a`–`5i` discipline below but never over the git constraints, the commit format, or anything else in *Constraints (non-negotiable)*. The subagent must not go looking for the file itself — it has no reliable base directory to resolve from, and a second resolution is how two units end up working to different rules. Pass the same text to every unit, so unit 3 is held to what unit 1 was.
- **Conventions and non-obvious mechanics** — anything the subagent cannot discover from the files but you already know from this conversation. Two kinds: standing user preferences that live in your context or memory rather than in the repo's own instruction files (files not to touch, test-file conventions, house idioms), and any non-obvious harness mechanics worked out during Step 3 grounding — e.g. a suite whose tests are driven through a wrapper or fixture rather than invoked directly, so the obvious-looking command is not the real one. A subagent that rediscovers these by trial pays for it in wasted calls, false "suite is broken" signals, and corrective commits.
- **Prior-stage state** *(units after the first only)* — a short carry-forward note: the stages already completed, the public interface (modules/types/functions and their signatures) of anything earlier units built that this unit will build on, any resolved interpreter / dependency / toolchain pins, and any deviations recorded so far. This keeps later units reusing prior work instead of re-scaffolding or guessing existing APIs.
- **Discipline** — the full `5a`–`5i` cycle: the pre-flight scans, write test → confirm fail → implement → confirm pass, coverage check against the stage plan, self-review (bloat / duplication-reuse / supersession-orphans / functional / inefficiency / security / design-language conformance / style), final `TEST`, and **one commit per stage** with the exact message `<type>(plan v<version>): Stage <N> — <stage title>`. It must `git add` only the files the stage touched. Stage commits contain the stage's source and test files only; plan-deviation notes and repo-mandated side artifacts (changelog, wiki) go in a separate `docs:` commit whose subject omits `(plan v<version>):`.
- **Git constraints** — current branch only; never create or switch branches, never push, never `--amend` / `--no-verify` / force. Commit each stage before starting the next.
- **Stop conditions** — the Step 6 conditions: on an undiagnosable failure, a decision not covered by the plan/design, an externally-dirtied tree, or an unplanned large security issue, it must **stop**, leave completed stages committed and partial work uncommitted, and report rather than invent.
- **Verification honesty** — if part of a stage's definition of done requires verification the subagent cannot perform (live UI, external system, manual check) or must not — launching or driving the real application against the user's live config, credentials or accounts, or making a persistent host change (a login item, a scheduled job, a global install) — it runs every available automated check, the build half and a sandboxed equivalent included, does **not** claim the live verification, and returns an exact live-verification checklist for the main agent to run (Step 7 picks it up).
- **Handed forward** — a defect you can name is fixed, not reported: in your own stage's code, fix it now, test first — a residual security, data-loss or concurrency risk is a defect, never a *pending human verification* item or a "known risk" line. What you cannot resolve inside your scope goes on a **Handed forward** list in your report, each item naming the file or stage that can resolve it: specified behaviour you could not deliver, a defect in code an earlier stage committed, a workaround your file boundary forced (logic re-created, a message string parsed, because the shared module was off-limits).
- **Return format** — a compact report: per stage, the title, commit short-sha, test result, the exact files committed, and an **API introduced** list (new public symbols — types, functions, constants — with signatures) for the main agent to paste verbatim into the next unit's carry-forward note; plus any deviations (and whether it updated the plan's *Deviations from plan*), the **Handed forward** list, any stop condition hit, and the final clean/dirty tree state.

Treat a unit as atomic the way a single stage is: it either lands all its stage commits green, or it stops and the user is consulted.

#### Parallel addendum (parallel batches only)

A parallel-batch brief is the contract above plus these bullets, which win wherever the two differ:

- **Workspace** — "Your work happens in `<worktree path>`, a detached checkout of the repo at `<base sha>`. Your working directory resets to `<repo root>` between shell calls, so prefix every shell command with `cd <worktree> &&` (or use `git -C <worktree>`), give `Read`, `Edit`, `Write`, `Glob` and `Grep` absolute paths under `<worktree>` only, and pass `path=<worktree>` to `Glob` and `Grep`. The only paths you may open outside `<worktree>/` are the plan file, the design file and any brief or carry-forward file named in this brief, read-only; read `DESIGN.md` at the worktree path the *Design language* bullet gives. Logs, captured test output, backups, downloads and any tool cache a sibling could share go under `<worktree>.tmp/` — beside the worktree, yours alone, created on first use — never in the worktree, the scratch root or `/tmp`. Opening or touching any other path outside `<worktree>/` is a stop condition." (The plan and design usually exist only under the repo root — `features/` is often gitignored, so the worktree holds no copy.)
- **Concurrency** — "Other stages are being built at the same moment in other worktrees. Your stage's *Touches* list is a hard boundary: touching a file outside it is a stop condition, not a deviation. Never edit the plan file or any shared artefact (tracker, changelog, wiki) — this overrides the Discipline bullet's `docs:` clause and 5d's plan edit; report the deviation text in your return instead. Make exactly one commit, on the detached HEAD of your worktree, with the standard stage message; the main agent moves it onto the branch."
- **Baseline** — the worktree probe's `TEST` result is the baseline.
- **Return format** additionally carries the worktree path, the commit sha, the files touched, the deviation text you would have written, and every pending human-verification item, alongside the *API introduced* list.

For every stage (whoever is executing it):

### 5a. Re-read the stage details
Re-read the stage block in the plan file (do not rely on memory). Note: goal, design references, files to touch, the four TDD steps, definition of done, stage-specific risks. A stage that builds or changes UI also re-reads `DESIGN.md` when the design cites it (in a subagent, at the brief's *Design language* path).

If the plan flagged the stage as **non-TDD scaffolding**, skip the test cycle for *that* stage — do the scaffolding work (5d), then jump to 5e. Everything else uses the full cycle below.

**Pre-flight testability** — for any stage whose test imports a module that does I/O (network, filesystem, OS-level streams) in its constructor, confirm the module exposes a dependency-injection seam before writing the test; if not, treat adding the seam as the first sub-step rather than discovering it via test failure.

**Pre-flight type identity** — for stages introducing new exception/error types (or other types compared by identity via `isinstance`, `instanceof`, equality on the class itself, `pytest.raises(MyError)`, `XCTAssertThrowsError(MyError)`, `expect().toThrow(MyError)`, etc.), confirm the test imports the type from the *same* module/binding the production code raises from. Some loaders produce two distinct identities for the same source declaration — e.g. Python's `spec_from_file_location` loading `plugin.py` as `mcp_bridge_plugin` while tests do `from mcp_bridge.plugin import MyError`; JVM classloaders treating a class loaded twice as two distinct types; Swift where the same type vended from two frameworks isn't equal at runtime; Node duplicating a package via symlinked/duplicated `node_modules`. Assertions against one identity won't match objects produced against the other. `grep` for dynamic-load patterns (`spec_from_file_location`, `Class.forName`, `dlopen`, duplicated `node_modules`) in test fixtures and verify the test's import path matches the production code's.

**Pre-flight signature-change scan** — when a stage changes a public constructor or function signature (adds a required kwarg, renames a parameter, changes the return type in a breaking way), `grep` across the codebase for every caller / instantiator of that symbol before writing the first test. List them in the stage's notes as "tests likely to need updating in this stage" so the inner-stage TDD slice can plan for them, rather than discovering them only at 5e's wider-suite regression check. Targeted-test green ≠ system green when constructor signatures move.

**Pre-flight time-dependency scan** — when a stage introduces current-time-based logic (clock reads, "now"-relative filtering, time-window cutoffs, TTL/expiry), `grep` existing tests for hardcoded or fixed-date fixtures that the new time logic would retroactively filter out or expire, before writing the first test. Plan to inject and pin the clock through a shared test seam within this same stage, rather than discovering the dated-fixture breakage only at 5e's wider-suite regression check.

**Pre-flight external-claim scan** — when the plan (or the design it quotes) names a *specific external mechanism* as the way a requirement is met — a third-party library's option, property, method or return shape; a shell or CLI invocation handed over verbatim; a rule about how an environment variable resolves — confirm it actually behaves as claimed, against the vendored version's own docs or source, before implementing it. Inherited claims are the one bug class TDD structurally cannot catch: a test written from the same plan co-assumes the mistake and passes green, so the defect surfaces only in the browser, on the device, or in production. On a mismatch, implement the working equivalent and record it under *Deviations from plan* rather than following the plan literally.

**Pre-flight live-run safety** — before starting any long-running project process (app, server, daemon) to satisfy a manual or live-verification step, read how that process resolves its data/config directory and which external integrations it starts on boot. If it can reach real third-party services or the user's own accounts, **do not boot it** — ask the user to run it themselves and report back. A verification step meant as a look at the UI must never mutate live state; some of that damage (revoked pairings, sent messages, deleted remote data) cannot be undone. Separately, where stages carry named environment preconditions in their definition of done (an app open, a session unlocked, a device attached), collect them across *all* such stages during the pre-scan and get the machine set up once before the loop starts, rather than stalling the user on arrival at each stage.

**Pre-flight reuse scan** — before writing any new helper, parse/validate/resolve block, or test fixture, `grep` the target module, its sibling entry-point files (parallel handlers over the same domain), and the test tree for an existing equivalent; prefer calling or generalising it (add a parameter, loop over the kinds) over writing a parallel copy. When the stage adds a new variant of an existing family (an Nth sibling method, row factory, or per-variant test file), read the siblings first — three or more repeating the same boilerplate means the stage extracts the shared helper rather than pasting another copy.

### 5b. Write the test first
Create or modify the test file(s) specified by the stage. Write concrete test cases that describe the new behavior. Do **not** write any production code yet.

### 5c. Run the test and confirm it fails
Run the targeted test (preferred) or the surrounding test command. Capture the actual failure output and verify it matches (or is plausibly the same as) the "expected initial failure" the plan recorded. If the test **passes** at this point, something is wrong — either the test isn't exercising the new behavior, or the behavior already exists. Stop and resolve before continuing.

### 5d. Implement the code
Make the minimum changes needed to satisfy the test. Modify only the files the stage names (or files whose change is a direct, necessary consequence). If the stage's planned files turn out to be wrong, update the plan via `Edit` to reflect reality before continuing — and note the change in *Deviations from plan* (add a section to the plan file if needed). Don't silently drift.

### 5e. Run the test and confirm it passes
Re-run the targeted test, then run a wider relevant test suite (e.g. the module's tests, then the project's full unit suite if it's fast). The targeted test must pass. For the wider suite, **compare failures against the Step 3 baseline**: any failure already in the baseline is pre-existing and not a stage regression; any *new* failure not in the baseline must be fixed before continuing. Do not commit a state with new (non-baseline) failures. If a stage's changes cause a baseline test to start passing, drop it from the baseline list (the list only shrinks).

### 5f. Coverage check against the stage plan
Re-read the stage in the plan and verify, point-by-point, that what you implemented covers what the stage promised:

- Every file the stage said it would touch was either touched or had its omission justified.
- Every behavior the stage said it would deliver has at least one passing test.
- The stage's *Definition of done* checklist is satisfied.
- The Requirements coverage map's design requirements assigned to this stage are now actually exercised by tests.

If gaps appear, fill them within the same stage (go back to 5b). Do not paper over with TODOs.

### 5g. Self-review the new code
Before committing, review the change this stage introduced. Run all of these lenses; fix what you find via `Edit` in the same stage. Every lens but **Duplication / reuse** and **Supersession / orphans** looks only at the new diff — those two deliberately reach outside it: one at existing code the change should have called, the other at code the stage may have stranded:

- **Bloat** — code that wasn't required by the test or the stage goal. Speculative abstractions, premature factories, dead branches, "for future use" parameters. Remove.
- **Duplication / reuse** — logic that re-implements something that already exists, or repeats itself within the stage. This lens reaches beyond the diff: `grep` the module, its sibling entry-point files, and the rest of the repo for the distinctive shapes just written (parse/validate/resolve blocks, dispatch branches, success tails, string-splitting predicates). Two or more contiguous blocks of roughly 4+ lines differing only in a single expression get factored into one helper; a **third near-identical sibling block is a hard trigger** to parameterise rather than paste. Apply the same rule to test fixtures, fakes, and payload builders — reuse or hoist them into the project's shared-fixture mechanism instead of re-declaring per file. Exempt framework-mandated boilerplate and genuine cross-boundary config that cannot be imported.
- **Supersession / orphans** — this lens looks *beyond* the stage's diff. Whenever the stage introduced a path that **replaces or obsoletes** existing code (a new function/class/module/endpoint superseding an old one, a rewired call site that bypasses a previous implementation), `grep` the codebase for remaining references to the superseded symbol(s). If nothing outside its own definition and tests still references it, it is now a dead-code island — **delete it, and its now-dead tests, in this same stage** so the orphan never outlives the commit that stranded it. Record a non-trivial removal under *Deviations from plan*. Do **not** delete on a zero-grep alone when the symbol is reachable in ways a text search misses — public/exported API with external consumers, dynamic dispatch (reflection, string-keyed registries, DI containers), serialization targets, or framework entry points; flag those to the user (or leave them for the Step 7 sweep) instead of removing them.
- **Functional issues** — off-by-one, wrong default, swapped arguments, error paths that swallow errors, missing nullability handling. Fix with another test if behavior is non-obvious.
- **Inefficiencies** — N+1 queries, unbounded scans, blocking I/O on hot paths, redundant work in tight loops, leaks of file handles / connections / listeners. Fix.
- **Security issues** — injection (SQL/command/template/prompt), missing input validation at trust boundaries, secrets in code or logs, unsafe deserialization, path traversal, SSRF, missing authz checks. Fix immediately; never defer security to a later stage unless the plan explicitly stages it that way.
- **Design-language conformance** — UI stages only, when there is a `DESIGN.md` to read. A colour, size, radius, shadow or font not recorded in `DESIGN.md`, or a component variant other than the recorded canonical one, is replaced with the recorded token or component. A value the design lists as a delta is allowed; anything else that must stay is a deviation recorded in the plan's *Deviations from plan*.
- **Style/comments** — remove comments that describe *what* the code does or reference the current task. Keep only comments that explain non-obvious *why*. No multi-paragraph docstrings unless they already exist in the file's style.

If a fix changes behavior, add or update a test to lock it in (go back to 5c briefly).

### 5h. Final test pass and commit
Run `TEST` (the command recorded in Step 3 sub-point 7) one more time after self-review edits. All green.

Then commit. Use one commit per stage with this message format (via HEREDOC). `<version>` is the integer feature version from Step 1; `<N>` is the stage number:

```
<type>(plan v<version>): Stage <N> — <stage title>

<one-paragraph summary of what changed and why,
referencing design §<n> / plan Stage <N>>
```

Where `<type>` is `feat` for new behavior, `refactor` for non-behavioral structural change, `chore` for scaffolding-only stages, `fix` if the stage corrected a bug, `test` if the stage was tests only, and `docs` when the stage's *entire* deliverable is documentation or reference material (a dedicated wiki / changelog / docs stage the plan numbered as a stage of its own).

Stage `git add` should add **only** the files this stage touched. Prefer `git add <files>` over `git add -A` to avoid sweeping in unrelated changes. Never `--no-verify`, never `--amend` a previous commit.

A stage with nothing to commit — verification-only, or acceptance the user has now reported — still gets its stage commit: its results in the project's testing doc where one exists, else `git commit --allow-empty` with the results in the body. Step 4's resume grep depends on it.

A stage commit contains the stage's source and test files only. Anything else that changed alongside it — plan-file deviation notes from 5d, repo-mandated side artifacts (changelog, wiki), tracker edits — goes in a separate `docs:`-typed commit, either straight after the stage commit or folded into the Step 8 tracker commit. Keep `(plan v<version>):` out of these docs commit subjects so they never pollute Step 4's resume grep (e.g. `docs: record plan v<version> Stage <N> deviation`).

**The omit-the-tag rule applies only to side artifacts riding alongside a code stage — never to a stage whose deliverable *is* documentation.** The question is always whether the documentation *is* the stage or merely accompanies one. A plan stage whose whole deliverable is docs is a stage like any other: it commits as `docs(plan v<version>): Stage <N> — <title>`, tag included, so Step 4's resume grep counts it as done. Read the two rules that way and they never conflict. In chunked mode, side artifacts that are *not* their own stage (a wiki or changelog update the plan mandates in its Verification section) are the **main agent's** responsibility after the last unit, in Step 7/8 — stage subagents skip them and say so in their report, so the update is neither duplicated nor dropped.

After the commit, run `git status` to confirm a clean tree before moving to the next stage. In a parallel batch the commit is made in the worktree and moved onto the current branch by the main agent's cherry-pick: the sha changes, the message does not.

### 5i. Move to the next stage
Loop back to 5a for the next stage. Between stages, do not push, do not switch branches, do not modify the plan/design unless 5d forced a deviation note.

## Step 6 — Stop conditions during the loop

Stop the loop immediately (and tell the user) if any of the following happen:

- A test fails after self-review edits and you cannot diagnose it within a reasonable attempt.
- A stage requires a decision not covered by the plan or design — surface to the user via `AskUserQuestion`; do not invent. **This applies even in auto / non-interactive mode**: an instruction to "work without stopping" or "skip clarifying questions" does not authorise inventing requirements. Inventing a missing decision and pushing code on top of it costs more than the pause.
- The working tree becomes dirty in a way you didn't cause (e.g. another process is writing files).
- A security issue is too large to fix within the stage and the plan didn't account for it.
- The plan turns out to be wrong in a way that would require revising the design (not just the plan). Stop; recommend `/feature-design` to produce a new feature version.
- A parallel batch hits a cherry-pick conflict or a combined red that no small reconciliation resolves (Step 5's landing rules), or a parallel subagent touched a file outside its stage's *Touches*.

When stopping, leave the repo in the cleanest reasonable state: uncommitted partial work for the current stage stays uncommitted; never auto-revert the user's view of the tree without asking. Whichever condition fired, invoke `usage-report` via the `Skill` tool with `report feature-implement, tracker_file=<tracker_file>, feature_version=<version>, outcome=halted, cycle=true` before you stop — the stages that did land still cost tokens and belong in the log, and the cycle report shows the feature's cost so far. If a parallel batch was in flight, first reconcile its worktrees as the batch procedure says, then `git worktree remove --force` each and `git worktree prune` — a stop never leaves a worktree behind.

## Step 7 — Final coverage & dead-code sweep

After the last stage commits cleanly, run a coverage sweep:

- For every requirement in design §3, find at least one test that verifies it (search test files via `Grep`).
- For every component in design §5 *Architecture / components*, confirm the file(s) exist and have tests.
- Run `TEST` (from Step 3 sub-point 7) one last time. All green.
- **Dead-code sweep.** Run `DEADCODE` (from Step 3 sub-point 7) across the **whole project** and compare against the Step 3 dead-code baseline — only findings *not* in the baseline are orphans this feature introduced. The whole-project scope is deliberate: cross-stage orphans (one stage builds a path, a later stage supersedes it) live in files no single stage edited, so a diff-scoped scan would miss exactly the islands this sweep exists to catch. **Compare like for like.** Run the sweep exactly as the Step 3 baseline ran — and, where the analyzer reads a build index, from a clean build both times: a stale incremental index reports live code as unused (e.g. `periphery scan --clean-build`; a source-only analyzer such as `vulture` is unaffected). Match findings on file, symbol and message with line numbers stripped — an edit above an old finding otherwise republishes it as new — and count only unused-declaration findings: an analyzer's access-level or style hints are not orphans. For each newly-orphaned symbol, **remove it and its now-dead tests** — *unless* it is reachable in ways static analysis misses (public/exported API with external consumers, dynamic dispatch, serialization targets, framework entry points), in which case surface it to the user rather than deleting. If a baseline finding stops appearing, drop it from the baseline silently. If `DEADCODE` is `none — no baseline` (no analyzer configured), do **not** improvise a scan; instead recommend the right tool for the project's language in the Step 10 summary (`vulture` for Python, `periphery` for Swift, `knip`/`ts-prune` for JS/TS, etc.) so the next run is covered.

If anything is missing (uncovered requirement, untested component, or a confirmed dead-code orphan), add a final lightweight stage following the same TDD cycle and commit it the same way — *Stage N+1 — Coverage gaps* for missing tests, or *Stage N+1 — Dead-code cleanup* (committed as `refactor`) for orphan removals. Update the plan file to reflect the added stage, including a final serial batch for it in the *Execution schedule*.

**Partial runs.** When the loop ends with plan stages still unbuilt that no executor here can build — Step 4 excluded them as externally gated, or they are hands-on acceptance — the run still closes through Steps 7–11 and says so everywhere. The coverage sweep judges only requirements whose stages all landed and lists the rest as not started. Step 8 writes `Stages completed: <n>/<N>` and a **Blocked** list — each remaining stage and what unblocks it — and leaves the progress bar `pending`. Step 10 adds a `**Blocked:**` line carrying the same list, and Step 11's usage report passes `outcome=halted`.

## Step 8 — Update the tracker

The tracker at `tracker_file` already exists from earlier stages. If the file is somehow missing (resolver `notes` flagged `tracker_seed: skipped`), defensively copy the plugin template:

```bash
# 1. Prefer the running plugin's own copy: this skill's announced base directory is
#    .../dev-skills/<version>/skills/<slug>, so the template is at <base>/../../templates/.
# 2. Else search — the *dev-skills* form is deliberate, since installed plugins live at
#    .../dev-skills/<version>/templates/ which "*/dev-skills/templates/*" silently misses.
find ~ -path "*dev-skills*/templates/feature-tracker.html" 2>/dev/null
# cp the winner (base-dir copy first; else a plugins/cache/ match at the highest version;
# else a working clone) to <tracker_file>. Copy, never symlink.
```

If no template can be located, skip the tracker update and note it in Step 10 — do **not** fail the whole skill.

Apply these edits via the `Edit` tool. For each `{{TOKEN}}`, check it is still literal text in the file. Skip silently if already substituted — with two caveats:

- Detect leftover literal tokens **in the rendered body only** — ignore the HTML comment legend at the top of the template, which names every token and makes a fully populated tracker look unfilled if grepped whole-file (risking overwrites of earlier skills' panels with empty placeholders).
- The Implementation panel is this skill's to fill **even when it holds no literal tokens**: if it shows the seeded placeholders (`Awaiting /feature-implement` / `Not yet filled — pending /feature-implement.`), replace them with the real content below. The skip-if-substituted rule protects the header tokens and other skills' panels, not this skill's own section.

**Header tokens** (only edit if still literal):

- `{{FEATURE_VERSION}}` → `<version>`.
- `{{FEATURE_TITLE}}` → `description` with hyphens replaced by spaces, preserving case.
- `{{FEATURE_SLUG}}` → `feature-v<version>-<description>`.
- `{{GENERATED_AT}}` → today's UTC date (`date -u +%Y-%m-%d`).

**Implementation section tokens** (this skill owns these). Compute the timestamp once via `date -u +"%Y-%m-%d %H:%M UTC"` and reuse the same value for the chip:

- `{{IMPLEMENTATION_AT}}` → `Updated <YYYY-MM-DD HH:MM UTC>` (the timestamp chip text — no surrounding HTML).
- `{{IMPLEMENTATION_BULLETS}}` → an `<ul>` of up to 10 high-level highlights a reviewer needs at a glance: e.g. `Stages completed: <N>/<N>`, `Tests: <pass count>/<total>`, `Design coverage: <N>/<N>`, `Pre-existing failures excluded: <count or None>`, `Dead-code orphans removed: <count or None>`, `Deviations from plan: <None | <count>>`, `Final commit: <short-sha>`, and any genuinely surprising outcome. One `<li>` per item, plain text.
- `{{IMPLEMENTATION_DETAILS}}` → free-form HTML rendering the run in increasing detail: a **Stages completed** list (one `<li>` per stage with title and commit short-sha, plus `(parallel, batch N)` for a stage built in a parallel batch) → a **Tests & lint** summary block (final counts, baseline failures excluded from regression gating, naming them) → a **Design coverage** `<table>` mapping requirements to verifying tests → **Deviations from plan** (or "None") → any **Notes** the user needs (e.g. branch left ahead of remote). Use `<h3>` for top-level section titles, `<h4>` for sub-sections, `<ul>` / `<table>` for content. Order content from highest-level to most detailed so a reader can stop reading at any depth.

**Other tokens** — substitute with the empty placeholder *only if still literal* (most will already be content from earlier stages):

- `{{BRAINSTORMING_AT}}` → `Awaiting /feature-storm`
- `{{BRAINSTORMING_BULLETS}}` / `{{BRAINSTORMING_DETAILS}}` → `<p class="empty">Not yet filled — pending /feature-storm.</p>`
- `{{DESIGN_AT}}` → `Awaiting /feature-design` (should never happen — design must exist; defend regardless)
- `{{DESIGN_BULLETS}}` / `{{DESIGN_DETAILS}}` → `<p class="empty">Not yet filled — pending /feature-design.</p>` (same caveat)
- `{{PLAN_AT}}` → `Awaiting /feature-plan` (should never happen — plan must exist; defend regardless)
- `{{PLAN_BULLETS}}` / `{{PLAN_DETAILS}}` → `<p class="empty">Not yet filled — pending /feature-plan.</p>` (same caveat)

**Progress bar** (mandatory transition — only fired in this step, after all stages are green and committed; a partial run (Step 7) leaves it `pending`):

- old_string: `data-stage="implement" data-state="pending"`
- new_string: `data-stage="implement" data-state="complete"`

If the Edit fails, the implement step is already `complete` (rerun on a fully tracked feature) — leave it alone.

Do **not** touch other skills' tokens beyond the empty-placeholder fallback above. Do **not** touch other skills' progress steps.

Finish by committing the tracker update — plus any still-uncommitted docs edits from the run (plan deviation notes, repo-mandated side artifacts) — as one docs commit, e.g. `docs: mark v<version> implementation complete in tracker`, so the run ends with a clean tree. This is a docs commit, not a stage commit: keep `(plan v<version>):` out of its subject so it never matches Step 4's resume grep.

## Step 9 — Capture lessons

Invoke the `lessons-capture` skill in this plugin via the `Skill` tool with the single argument `feature-implement`. It runs the reflection protocol, appends a dated entry to `~/.claude/dev-skills/lessons/feature-implement.md`, and returns the entry body for you to paste under the *Skill-improvement recommendations* heading in Step 10. When it also returns a log-size reminder block, paste that block unchanged directly below the entry.

Do not run the reflection inline — `lessons-capture` is the single source of the protocol for all skills in this plugin.

## Step 10 — Present the final summary

In chat, output a scannable summary. Use this shape:

```
Implemented: <prereq_file path>  (against <design path>)
Branch: <branch> (no new branches created, no pushes)
Tracker: <tracker_file path>

**Feature:** v<version> — <human-readable title>

**Stages completed**
- Stage 1 — <title> — <commit short-sha>
- Stage 2 — <title> — <commit short-sha> (parallel, batch 2)
- ...

**Tests:** <e.g. "All 42 tests passing">
**Pre-existing failures excluded from regression gating:** <"None" or comma-separated test ids from the Step 3 baseline>
**Design coverage:** <N>/<N> requirements verified by tests.
**Dead-code sweep:** <"None found" | "<N> orphan(s) removed in Stage N+1" | "No analyzer configured — recommend installing <vulture|periphery|…>">
**Deviations from plan:** <"None" or short list, one line each>
**Pending human verification:** <"None" or one line per unperformed human-only check, from the run-level pending-verification list>
**Parallelism:** <"<n> stages ran concurrently in <m> batches; <k> demoted to serial (<reason>)" | "None (plan had no parallel batch)">

**Skill-improvement recommendations**
- <as produced in Step 9>

**Next step:** eval offer coming up; push when ready after that (this skill never pushes — run /push when you're satisfied).
```

Keep to the template's shape — one line per stage and per field. Do not paste diffs or full file contents.

## Step 11 — Offer to run the evals

The run ends with the implementation committed but **not pushed** — exactly the state the plugin's two eval skills score. Offer them now, after the summary, so quality metrics for this run are captured before anything is pushed.

Ask via `AskUserQuestion` exactly once:

- **question**: `"Run the eval suite on this implementation? evals-code-run scores the unpushed commits for duplication/bloat/inefficiency/security (logs to ~/.claude/evals/code.json); evals-e2e-run scores the feature's storm/design/plan artefacts and their consistency with the implementation (logs to ~/.claude/evals/design.json). Both are read-only towards the repo."`
- **header**: `"Run evals?"`
- **options**:
  - `{ "label": "Yes, run both", "description": "Run evals-code-run and evals-e2e-run in two parallel read-only subagents; two eval-log appends, no repo changes." }` (mark this as Recommended)
  - `{ "label": "No, skip", "description": "Finish without evals; /evals-code-run and /evals-e2e-run can be run manually later." }`

If the user declines (or picks "Other" with decline intent), the skill is done. In a truly headless run with no channel to ask, default to skipping — the evals can always be run by hand later.

If the user accepts, launch **two subagents in parallel** — one message, two `Agent` calls, `subagent_type: general-purpose` — one per eval skill, and wait for both. Parallel is safe by construction: both skills are read-only towards the repo, and they write to different log files. Each subagent starts with a fresh context, so its brief must be self-contained:

- Instruct it to invoke its skill via the `Skill` tool — `evals-code-run` for one, `evals-e2e-run` for the other (plugin-qualified `dev:` form where needed) — and execute it to completion.
- State explicitly: "You are being run from /feature-implement's eval offer; the user already confirmed via AskUserQuestion — execute the skill without re-asking." This satisfies each eval skill's Step 0 clause for contexts with no user channel.
- Pass the repo root, the current branch, and the feature version `v<version>` for context. If Step 3 found no remote/upstream for this branch, also pass the base ref the evals should diff against (as the skill argument) — without an upstream, "unpushed" is otherwise undefined for them.
- Constraint: read-only towards the repo — no edits, no commits, no pushes; the only writes are the eval logs under `~/.claude/evals/`.
- Return format: the eval skill's own final summary — the score table plus the log-write confirmation — verbatim.

When both return, relay the two score summaries to the user in compact form. If a subagent fails or the `Agent` tool is unavailable in your context, run that eval skill directly in this conversation instead (its own steps handle everything). Never fail the implementation run over an eval error — report it and finish.

**Report the run usage.** With the evals relayed (or declined), invoke `usage-report` via the `Skill` tool with the argument `report feature-implement, tracker_file=<tracker_file>, feature_version=<version>, evals_included=<true|false>, cycle=true` — `evals_included` is `true` on the accepted branch, `false` on the declined one — taking the paths from Step 1's `feature-resolve` block. It appends one line to the usage log, fills the Implementation panel's usage tokens, rewrites the tracker's Usage tab and prints the feature's cycle report.

**This skill reports last, where the other three report before their offer — do not "tidy" the two into line.** The asymmetry is the design's, not an oversight: the three chaining skills hand over through the `Skill` tool on acceptance and never return to their final step, so a trailing report there would never run. This skill's final question hands over to nothing and control returns on every branch, so the end of the step is always reached and is always where the chain stops — which is why this report alone carries `cycle=true` — and only from here do the eval subagents the user chose to run fall inside the window being reported, which is why `evals_included` is recorded alongside the figures.

## Constraints (non-negotiable)

- **No new branches.** Implementation happens on the current branch (default branch unless the user confirms otherwise). Never `git checkout -b`.
- **Never push.** This skill commits only. The user invokes `/push` separately.
- **Never `--no-verify`, never `--amend` a published commit, never force-push.** Standard git safety still applies.
- **Both files must exist on disk.** No implementation begins without the design and plan files confirmed present under the resolver-returned feature folder (Step 1 + Step 2). Never bypass the resolver.
- **TDD as written in the plan is mandatory.** Behavior-changing stages: write test → confirm fail → implement → confirm pass. Scaffolding-only stages may skip the test cycle; the plan must mark them.
- **Never build on a red test baseline.** If Step 3's `TEST` baseline shows any failing tests, stop before the stage loop and let the user investigate, file a bug (`/bug-submit`), or halt (Step 3 sub-point 9) — implementation never proceeds on top of pre-existing test failures. This gate holds even under autonomous "don't stop to ask" instructions; a truly headless run defaults to halting.
- **Report the run usage before you stop.** However this run ends — normal completion, a red-baseline halt, a Step 6 stop condition, a refusal, or an error surfaced to the user — invoke `usage-report` with `report feature-implement, outcome=halted, cycle=true` — plus `tracker_file=<tracker_file>, feature_version=<version>` once Step 1's resolver has run — before you stop (Step 11's normal path passes `outcome=completed` instead). Step 3 covers the red baseline and Step 6 the loop stops; this covers every other exit. The window is the main agent's alone — Step 5's stage subagents never open or close it. The one exception is a Step 1 relaunch (`next: end-turn` from **Check the session**): it ends the turn before the usage window opens, so there is no window to close.
- **A queued relaunch or handover is the one place this skill ends its turn on a success path** besides any wait a helper sanctions; it never ends the turn on a `session-control` result other than `next: end-turn`.
- **One commit per stage.** No batch commits across stages. No commits mid-stage. The commit-message format is the resume contract for Step 4 — do not deviate from `<type>(plan v<version>): Stage <N> — <title>`. The one sanctioned cross-stage commit is the post-batch `fix: reconcile Stage <N> with Stage <M> after parallel landing` — subject without `(plan v<version>):`, touching only files in the batch's *Touches* union, adding no behaviour beyond making both stages' tests pass; anything larger is a Step 6 stop.
- **Execution strategy changes only the executor.** Chunked subagent units and parallel-batch subagents run the identical `5a`–`5i` cycle and obey every constraint here — current branch only, no new branches, no pushes, one commit per stage with the exact message format. Serial units run strictly in order in the shared working tree; a parallel batch's subagents run concurrently only in detached worktrees the main agent creates and removes, and their commits land on the current branch in stage order, one per stage, through `git cherry-pick`. Steps 7–11 always run in the main agent, never in a subagent (Step 11's accepted evals are delegated to subagents by design).
- **The strategy is resolved by rule, never asked and never left to preference.** Chunked (`min(3, R)`) is the default; Direct applies only on an explicit user request, at `R ≤ 2`, or when the pre-scan leaves ≤1 delegatable stage. Do not reintroduce an `AskUserQuestion` here — across 30 recorded runs the same option was chosen 83% of the time and the question was dismissed in 8, so it cost a mandatory round-trip and bought nothing. Equally, do not turn it into free model discretion: under an autonomous instruction the cheap path is Direct, which is the failure this rule exists to prevent. Announce the resolved strategy in one line (with `R` and the partition) instead — that line is the run's only checkpoint before code lands. The partition comes from the plan's *Execution schedule*, never from this skill's own dependency guess: a batch the plan marks parallel runs concurrently unless the pre-scan demotes it (independence re-check failed, a stage in it is not subagent-doable or externally gated, a worktree could not be created), and parallelism is off for the whole run when the user asked for Direct or one stage at a time, the `Agent` tool is unavailable, `R ≤ 2`, the worktree probe fails, or a launch is rejected.
- **The eval offer never blocks or mutates.** Step 11 runs only with user consent, launches read-only skills, and a declined offer or a failed eval never fails the implementation run. The offer comes before any push because both eval skills score unpushed commits.
- **Integer versions only.** `v<N>` in commit messages, file references, and tracker tokens — never `v<N>.<M>`.
- **No silent design or plan drift.** If reality forces a change, update the plan file and record it under *Deviations*. Stop and surface big drifts to the user.
- **Self-review every stage before commit.** Bloat, duplicated or reimplemented logic, superseded/orphaned code, functional issues, inefficiencies, security, design-language conformance on UI stages — fix in the stage, not later.
- **Dead-code sweep is baseline-scoped and never deletes blindly.** Step 7's `DEADCODE` run gates only orphans this feature introduced (diffed against the Step 3 baseline), never pre-existing dead code; symbols reachable via public API, dynamic dispatch, serialization, or framework entry points are surfaced to the user, not auto-removed. With no analyzer configured, recommend one rather than improvising a scan.
- **Tracker edits are defensive.** Substitute only tokens still literal `{{...}}`; never overwrite content placed by `/feature-storm`, `/feature-design`, `/feature-plan`, or any other skill. The progress bar's `data-stage="implement"` entry is this skill's alone to touch.
- **No symlinks.** If a defensive tracker template copy is needed in Step 8, always copy — never link.
- **Lessons capture runs every time.** Step 9 always invokes `lessons-capture`; whether it produces a recommendation or "none this run" is decided by that skill.
- **Never paste full code or plan content into chat.** Step 10 is summary only.
- **Worktrees are throwaway and branchless.** A parallel batch's worktrees are created with `git worktree add --detach` — never a branch, never the harness's worktree option — under the session scratch directory with a per-run suffix, reconciled and then removed before the run ends or stops, and never pushed from. Never symlink `node_modules`, `.venv`, `.build` or any other dependency directory into a worktree to skip provisioning; the no-symlinks rule applies, so each one runs `PROVISION`.
