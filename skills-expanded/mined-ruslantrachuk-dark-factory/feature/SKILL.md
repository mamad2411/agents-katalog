---
name: feature
description: Launch the feature pipeline for one task with the project's saved settings — reads .claude/factory/feature-pipeline.json, fills in the run's own arguments (branch type and slug, tracker ID, bd task, requirements source, stamp) and calls the Workflow dark-factory:feature-auto (or dark-factory:feature-lite with --lite). Stops at a committed branch; never merges. Invoked by the human as /dark-factory:feature.
argument-hint: "[--lite|--full] [--mode session|pipeline] <task: bd id, OpenSpec change + phase, spec path or a sentence>"
disable-model-invocation: true
---

# /dark-factory:feature — one task through the feature pipeline

The workflows ship with this plugin (`dark-factory:feature-auto`, `dark-factory:feature-core`,
`dark-factory:feature-lite`); the factory keeps the project's settings in `.claude/factory/feature-pipeline.json` (the
`feature-pipeline` module). This command joins the two so the settings are never re-typed. The run rules and the
argument table are in the module's `MANIFEST.md` and the plugin's `workflows/README.md`.

## Rules

1. **The file is the project's settings; the task is the run.** Pass every key of `.claude/factory/feature-pipeline.json`
   as it is (`appSubdir`, `testCmd`, `lintCmd`, `frontendDir`, `i18nFile`, `invariantsDoc`, `surfaces`, `models`,
   `maxAgents`, …). Do not invent values for keys the file leaves out — the workflows have defaults. A key whose value
   still holds a `<placeholder>` is left out, and you tell the human it is unfilled.
2. **Never guess the run's required arguments.** `bdId` comes from the task or the human, `slug` and `trackerId` from the
   change (`openspec/changes/<slug>/`, its proposal header), the source from the task. Missing and not derivable — ask one short question.
3. **`args` is an object** of JSON values, never a JSON-encoded string.
4. **The run stops at a committed branch.** Merging is `scripts/merge-feature.sh <branch>` once CI is green, outside
   this command.

## Steps

1. Read `.claude/factory/feature-pipeline.json` in the project's main checkout (the first path of
   `git worktree list`; a session's worktree does not have it — the file is on the server, not in git), else a
   `.claude/feature-pipeline.json` still in git (MANIFEST §Setup moves it). No file → tell the human the `feature-pipeline` module is not set up
   (its `MANIFEST.md` §Setup) and stop.
2. Build the run's arguments from `$ARGUMENTS` and the repository:
   - `request` — the task in one or two sentences (the bd task's title when only an id is given: `bd show <id>`).
   - `bdId` — the full bd id `<prefix>-<hash>[.N]`; required by `feature-auto`.
   - the source: `changeDir` + `phase` (an approved OpenSpec change and its `tasks.md` phase), or `specPath`
     (absolute path of a ready spec), or neither (the bd task's description is the source).
   - `slug` — the change slug (`openspec/changes/<slug>/`; a phase of a spec without sub-cards: `<slug>-p<K>`);
     `trackerId` — the tracker ID of the change when there is one (it goes into the branch name); `type` —
     `feat|fix|ui|refactor|chore|docs`.
   - `stamp` — a unique suffix the scripts cannot make themselves: `date +%Y%m%d-%H%M` plus a short tag
     (e.g. `20261021-1430-p3`). Keep it for a resume.
3. Show the human the call in short — workflow name, the run's arguments, the settings taken from the file — and
   launch after their "yes":
   ```
   Workflow({ name: "dark-factory:feature-auto", args: { ...settings from the file, request, stamp, slug, trackerId, bdId, ... } })
   ```
   `--lite` in `$ARGUMENTS` → `dark-factory:feature-lite` with the same settings (`bdId` optional there); `--full` →
   `path: "full"`. Without either, take the path from the owner-approved `size-task` verdict of this phase (`lite` →
   `dark-factory:feature-lite`, `full` → `path: "full"`); only with no verdict at all is `path` left out, and the run's
   triage agent sizes the work — say so to the human before the launch.
   **Under Codex** there is no Workflow tool. Do not imitate the pipeline with subagents. Offer one of two runs and
   start it after the human's "yes":
   - **A run left alone.** Start it detached with the same arguments:
     `setsid nohup python3 <plugin>/scripts/codex_feature.py run --stamp … --request … --bd … [--change … --phase …]
     [--tracker …] [--type …] > <scratch>/run.json 2>&1 &`. It runs session mode in its own Codex threads.
     - **Outside this session's sandbox.** The run writes its state under `~/.local/state/dark-factory/` and starts
       `codex exec`, which needs Codex's home. Neither works inside the sandbox. Ask to run the command with escalated
       permissions; the human approves. If that is not possible, give the human the command to run in a terminal.
       A run started inside the sandbox stops with `error: "cannot run here: …"`.
     - **Resume and status.** Rerunning with the same stamp resumes it. `codex_feature.py status --stamp …` shows
       where it is (workflows/README.md, "On Codex").
   - **The task in this session.** `$dark-factory:plan` → `$dark-factory:build-tdd` per slice →
     `$dark-factory:integrate` → one reviewer pass → `$dark-factory:wrap`, with the same settings from the file.

   Both stop at a committed branch, as the pipeline does. `--mode pipeline` has no Codex runner; say so.
   `--mode session|pipeline` sets `buildMode` for this run over the file's value and the verdict's (`session`, the
   default: one builder does the whole task by the stage skills, then one reviewer; `pipeline`: every stage by its
   own agents, for a wide phase of independent slices; `feature-lite` ignores it).
4. Read the result's `error`, not the harness status. `null` — show the branch, the assumptions and the PR description (`prBody`; the branch's PR gets it: `gh pr create --draft --body-file -`)
   and ask for the owner's acceptance. Anything else — show the error, the `stage` it stopped at and `agentsUsed` /
   `maxAgents`; a stop on `budget exhausted` or `agent limit reached` is resumed with `resumeFromRunId`, the same
   args and the same `stamp` (with a larger `maxAgents` for the second one, after the human agrees).
