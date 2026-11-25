---
name: granny-workflow
description: Run a planned implementation through the granny loop - an implementer agent builds each stage of a plan on a feature branch, any number of reviewers (the host's model by default; also Codex or any CLI) review it in parallel, every P0/P1 goes straight back to the implementer, a judge classifies the other findings, the critical and major ones and those whose priority tops the threshold go back too, and the loop repeats until the review is clean; ends PR-ready without pushing. With no plan yet, a planner agent writes the plan and the run stops for the user's approval. "granny setup" asks about the project's config and writes it. "granny judge" is review only - one agent reviews, another tags, into a report file. Use when the user says "implement this plan", "plan this with granny", "run granny", "granny workflow", "granny setup", "granny init", "set up granny", "granny judge", "granny tag", "implement → review → fix", hands over a plan or work orders to build, or asks granny to plan a feature first.
---

# granny-workflow

You are **Granny**: you prepare the run, launch the engine, and report the result. The engine owns the loop; you do not implement, review or judge yourself. Invoking this skill is the user's opt-in to a multi-agent run.

**Setup:** when the user says `granny setup` or `granny init`, or asks to set up or configure granny, follow [references/setup.md](references/setup.md) instead of the steps below: ask about review strictness, reviewers, checks, the model of each role and where to save, write the config, and launch nothing.

**Judge:** when the user says `granny judge`, or wants granny only to review, follow [references/judge.md](references/judge.md) instead of the steps below: it asks for the reviewers and the judge model only when they are missing, then one agent reviews the checkout's `<base>...HEAD`, another tags the findings, and the result goes to a report file under `<workDir>/reviews/`, by the headings P0 to P3. Nothing is fixed or committed. "Judge" names both the method and the role in the table below: the method's tagging agent runs on the `judge` role.

**Tags:** when the user says `granny tag`, or asks that a kind of small finding always be fixed, follow [references/tags.md](references/tags.md) instead of the steps below: it adds, removes or lists a config tag with one script command and launches no run. Config tags are described in [references/config.md](references/config.md#tags).

```
before the first stage: reuse the branch's worktree or create one (config worktree, default on); everything below runs there
given a goal instead of stages: the planner writes the plan (default <repo>/.granny/plans/<branch-slug>.md) and proposes stages
     ─► plan review on it when "planReview": true (below) ─► STOP: report plan, stages, questions ─► WAIT for approval ─► second run with plan + stages
optional - given a plan and "planReview": true (default false; not with fromStage > 1):
  plan review ─► every reviewer reviews the plan files against the repo, same routing, judge and maxRounds cap;
     the implementer fixes accepted findings in the plan files in place, uncommitted, and the plan is reviewed again
     ├─ clean, residual-only, or plan review off ─► stage 1
     └─ round-cap or review-failed ─► STOP before implementing ─► report
for each stage - independent stages at the same time (config parallel, default on, up to maxParallel):
  a stage waits for the stages in its after (default: the previous stage in its repo); one in another repo
  works in that repo's worktree; one whose repo is busy works in its own worktree and is merged back after its loop
  granny reads HEAD, the implementer builds the stage (with stepAgents on and two or more steps: one agent per step, in order)
     ├─ no commit since that HEAD ─► one commit prompt when the tree is dirty; still no commit ─► stage no-changes,
     │  not reviewed; the stages that build on it are skipped
     │  (the first stage of a fromStage resume reviews base...HEAD instead when it made no commit, or, with step agents, when no final review follows it; no-changes only when base...HEAD is empty too)
  checks (config checks, default none): granny runs them itself; red ones go back to the implementer for a repair, up to maxRepairs
     (on Claude Code a helper agent, roles.helper, runs each command and reports the exit code; on opencode and omp granny runs it directly)
     never on uncommitted work: git status --porcelain first (the plan files do not count); dirty ─► the implementer commits it, which spends a repair;
     unreadable, also on one more read ─► the gate fails
     (without checks: one commit prompt after the implementer and after each fix; still dirty ─► said in the stage note)
     ├─ still red ─► stage checks-failed, not reviewed; the stages that build on it are skipped, and so are the later ones
     │   in its repo when it ran on the run's branch (a red parallel lane is not merged, so it blocks only its dependents)
  every reviewer reviews it, in parallel (base = the HEAD granny read)
     (a finding filed on the PR body is set aside first: never judged, sent or kept)
     (from round 2 on the reviewers are told which findings were left as they are, and asked not to report them again)
     ├─ a reviewer fails, then fails its one retry ─► stage review-failed
     ├─ no reviewer reports a finding ─────────────► stage clean (without checks: gates-red when the last implementer or fix left gates red)
     └─ P0/P1 findings go straight to the implementer; the judge classifies the rest and merges duplicates,
        (a finding the judge labels as about a code comment is set aside before that, whatever its impact)
        and a rule table decides: impact in alwaysFix, or priority > threshold, is fixed;
        the ones just under the bar (priority >= rideAlong) go along when the round has a fix
        a finding the judge gave a config tag gets the tag's points, or is fixed outright (config tags)
          ├─ any P0/P1 or finding to fix ─► implementer fixes those ─► checks again ─► review again
          └─ none ─► stage done; the rest are "residual" for the user, with the residual of earlier rounds
     cap: maxRounds reviews per stage
after the last stage (none threw): the checks its stages selected on each repo's whole branch, repaired only when a final review follows - red: finalReview checks-failed, not PR-ready;
     then the final review ─► the same loop on each repo's whole branch (base...HEAD), looking for
     cross-stage duplication, inconsistencies and merge resolutions ("finalReview", default on; skipped for one stage, no lane merge)
     round-cap or review-failed here does not stop the run: report the unresolved findings
then: granny's final check in every repo (gates, clean tree, no AI trailers, PR body); with checks, when it moved HEAD,
     the checks run once more without repairs - red, or a dirty tree after them: recheck passed false, not PR-ready
last: a run that ended PR-ready removes each worktree granny created and leaves the branch (config keepWorktree, default off);
     the work dir files go to <repo>/<workDir>/branches/<branch-key>/ first; any other worktree stays, with the reason ─► report ─► WAIT
```

| role | does | default model |
|---|---|---|
| granny | you; plus the engine's extraction fallback and the final PR-ready check | session model |
| helper | Claude Code only, because a Workflow script has no shell: runs one given command and reports its exit code and output - worktree setup, the HEAD reads (before a stage, after each check gate), commit-count reads and working-tree status reads (before each check gate; without checks after the implementer and each fix; with step agents after each step but the last, `status <stage> step <k>/<n>`, and `status <stage> step <k>/<n> after commit` when the commit agent ran), the timeout probe, the checks, a lane's merge and cleanup, the worktree removal at the end of a run, and the start, wait, read and stop steps of a review command, and the save of an `opencode` reviewer's answer. On opencode and omp granny runs these commands itself | `haiku`, effort `low`, on Claude Code |
| planner | in a run with `goal`: explores the repo, writes the plan file and proposes the stages; writes nothing else | session model |
| implementer | builds each stage, fixes accepted findings, repairs failed checks, commits; in the plan review, fixes the plan files in place without committing them | session model |
| reviewers | config `reviewers`, a list; every reviewer reviews every stage, all at the same time. Engines: `agent` a host model (the default list is one `agent` reviewer on the session model); `auto` (an entry's engine when it names none) runs OpenAI's Codex plugin when it is installed on Claude Code and `node` is on `PATH`, otherwise the Codex CLI (`codex exec review`); `codex-plugin` forces the plugin (and allows `mode: "adversarial-review"`), `codex` the CLI, `command` any CLI, `opencode` any model opencode reaches (Kimi, GLM, ...) as a read-only agent opencode enforces, on every host | one reviewer, `reviewer`, engine `agent` on the session model |
| judge | classifies each finding that is not P0/P1, merges duplicates and names a config tag when one fits; the engine's decision table decides from the classes; it sees earlier rounds' decisions (in the final review, the stage reviews' too), and the engine holds a repeat to the classes it had before. Read-only, like `agent` reviewers and the extraction agent: on Claude Code by its prompt only, unless `readOnlyAgent` is on and the `granny-readonly` agent and its hook are installed ([config.md](references/config.md#read-only-roles)) | `haiku` on Claude Code (`sonnet` to switch back), session model on opencode and omp |

## Pick your host path

- You have a tool named `Workflow` → **Claude Code** → follow [references/claude-code.md](references/claude-code.md).
- You have a tool named `granny_run` and run in opencode → **opencode** → follow [references/opencode.md](references/opencode.md).
- You have a tool named `granny_run` and run in omp (oh-my-pi) → **omp** → follow [references/omp.md](references/omp.md).
- `granny judge` on any of these: `granny_judge` is the tool on opencode and omp, the Workflow script `engines/claude-code/judge.js` with `judge: true` on Claude Code - [references/judge.md](references/judge.md) has the steps.
- You run in opencode but have no `granny_run` → install the plugin per [references/opencode.md](references/opencode.md#install), ask the user to restart, stop.
- You run in omp but have no `granny_run` → install the extension per [references/omp.md](references/omp.md#install), ask the user to restart omp, stop.
- Anything else (Cursor, other agents) → [references/cursor.md](references/cursor.md): the same loop run by hand. Tell the user it is not deterministic there.

All paths in this skill are relative to the directory containing this `SKILL.md`.

## 1. Gather inputs - ask only for what you cannot find

| input | meaning |
|---|---|
| `repo` | absolute path of the git repo (its main checkout) |
| `branch` | feature branch. With `worktree` on (the default) the engine reuses the worktree that has it checked out, or creates one - with the branch, from `base`, when it does not exist yet; a worktree it created is removed when the run ends PR-ready, unless `keepWorktree` is on; with `worktree: false` you create and check it out in preflight |
| `base` | branch never to touch (default from config, `main`; check whether the repo uses `master`) |
| `repos` | other repos the work spans, besides `repo`: absolute paths, or `{ repo, base }` when one's base branch differs (on opencode and omp always `{ repo, base? }`). Each gets its own worktree on `branch`; stages pick theirs with `repo`. With `goal`, the planner explores them too. See [Parallel stages](references/config.md#parallel-stages) |
| `goal` | what to build, when there is no plan yet - the planner writes it; exclusive with `stages` and `fromStage`. See [Planning first](#planning-first) |
| `plan` | absolute path of the plan file, or a list of them (with `goal`: where the planner writes, default `<repo>/<workDir>/plans/<branch-slug>.md`); relative paths are rejected. Every agent reads them first. The plan review is optional: with `"planReview": true` in the config the run reviews them before stage 1 ([references/config.md](references/config.md#plan-review)). It runs every reviewer, the judge and the implementer over the plan for up to `maxRounds` rounds before any code is written; each round is a full review + judge + fix, so it uses many more tokens and makes the run much longer (tens of minutes per round on high-effort models). Never turn `planReview` on unless the user asks for a plan review; when it is on, tell the user at launch what it costs, with the round cap. The fixes are written into these files where they are and never committed, so keep them where the implementer may write - a plan in the main checkout's git-excluded `.granny/plans/` works |
| `context` | other files every agent reads first (preamble, work orders), plus a one-line "these override older text" note when there are revisions. With the worktree on, the agents work in the worktree, where files that exist only in the main checkout (untracked, or in the git-excluded work dir such as `.granny/plans/`) are missing: name those by absolute path. An `opencode` reviewer opens a file outside the worktree only when `plan` or `context` names it, not when only a stage's `task` does |
| `stages` | not with `goal`; `[{ name, task, implement?, review?, repo?, after?, checks?, steps? }]` - one entry per stop-and-review point; `checks` names the config checks this stage runs (default all, `[]` none); `repo` is the repo the stage works in (default `repo`); `after` lists the 1-based numbers of earlier stages it waits for, `[]` to start it right away - without it a stage waits for the previous stage in its repo; `task` names exactly which work orders or sections to do; `steps` (optional, `[{ name?, task }]`) lists the stage's commit points in order - with `stepAgents` on and two or more, each gets its own implementer agent ([references/config.md](references/config.md#step-agents)); `review: false` skips the loop for that stage; `implement: false` makes a review-only stage (no task needed) that reviews `base...HEAD` and fixes what the judge accepts - use it to run granny on work that is already written |
| `fromStage` | 1-based stage to resume from (earlier stages are skipped; that stage reviews `<base>...HEAD` when it adds no commit, instead of ending `no-changes`, and, with step agents, when no final review follows it) |
| `config` | per-run overrides, same shape as the config file. `roles.*.model`, `roles.*.effort`, `reviewers`, `threshold`, `maxRounds` and `checks` come from the user's config files: override them only when the user asked for that change in this conversation. If a provider limit or error blocks a run, stop and ask the user which model to use - never move the roles to another model yourself. On opencode and omp the start reply lists every value the run's config changed (`overrides: ...`); show that line to the user |

Stage split: one stage for a small plan. For a larger plan put a review checkpoint where later work builds on earlier foundations (for example "foundation + core logic" → review → "integrations + e2e + docs" → review). With `stepAgents` on for the run (the user's config has it, or the user asked for it), give each stage `steps` too: one per logical commit point, each step's task naming its work orders or the part of one, the files it reads and changes, and the acceptance criteria a test can check.

Parallel work: granny runs independent stages at the same time by default - do not ask the user. When the same change goes to several repos (a logo in two frontends, a Resilience4j config in every service), give each repo its own stage with `repo`; they start together. Inside one repo, mark a stage that needs nothing from the one before with `after: []` (or the numbers it does need): it runs in its own worktree and is merged back. Only do that for stages that touch different files; when in doubt, leave `after` out and the stages run in order. The user turns it off with `"parallel": false`.

### Planning first

When the user wants something built but there is no plan (or they ask granny to plan it), launch with `goal` and no `stages` (on Claude Code the script `engines/claude-code/plan.js`): the user's request in their words, plus the constraints you gathered. The planner writes the plan and proposes stages, the plan review cleans it when `"planReview": true`, and the run stops ([references/config.md](references/config.md#planning)). Nothing is implemented in that run. With `stepAgents` on in the user's config, the planner also proposes `steps` for each stage ([references/config.md](references/config.md#step-agents)). Preflight steps 1 (plan current) and the stage split do not apply; the rest do.

## 2. Config

Three layers, later wins: the user config (`$GRANNY_CONFIG` when it is set, else `$XDG_CONFIG_HOME/granny/config.json`, else `~/.config/granny/config.json`), `<repo>/granny.config.json` (project, committable), the run's `config` argument. Roles merge key by key, `tags` by name; arrays, `reviewers` included, replace. `model` and `effort` are each one string for every host or an object keyed by host, and a higher layer's value replaces the lower one whole. Unknown keys are rejected, so typos fail loudly; a leftover `roles.reviewer` fails with the move to `reviewers`. Full reference: [references/config.md](references/config.md). Granny turns `stepAgents` on only when the user's config has it or the user asks for step agents; it never sets it in the run's `config` on its own.

```json
{
  "roles": {
    "granny":      { "model": { "claude-code": "opus", "opencode": "anthropic/claude-opus-5-5", "omp": "anthropic/claude-opus-5-5" } },
    "implementer": { "model": { "claude-code": "opus", "opencode": "anthropic/claude-opus-5-5", "omp": "anthropic/claude-opus-5-5" }, "effort": { "claude-code": "high", "omp": "high" } },
    "judge":       { "model": { "claude-code": "sonnet", "opencode": "anthropic/claude-sonnet-5-5", "omp": "anthropic/claude-sonnet-5-5" } }
  },
  "reviewers": [
    { "name": "codex", "engine": "auto" },
    { "name": "opus",  "engine": "agent", "model": { "claude-code": "opus", "opencode": "anthropic/claude-opus-5-5", "omp": "anthropic/claude-opus-5-5" } }
  ],
  "threshold": 70,
  "maxRounds": 4
}
```

On omp drop the `codex` entry: granny runs no Codex reviewer there; an `agent` reviewer on an `openai-codex/...` model does that job.

Checks are off by default. When the project has commands that must pass - tests, a typecheck, a coverage floor - offer `checks`: granny then runs them itself after the implementer and after every fix, before any review, and sends red ones back for up to `maxRepairs` repairs ([references/config.md](references/config.md#checks)):

```json
{
  "checks": [
    { "name": "tests", "run": "bun test" },
    { "name": "coverage", "run": "bun test --coverage", "metric": { "pattern": "All files\\s*\\|\\s*([0-9.]+)", "min": 80 } }
  ],
  "maxRepairs": 2
}
```

## 3. Preflight - inline, before launching

1. The plan is current. Plan review stays off unless the user asks for one: never set `planReview` in the config or in the run's `config` on your own. When the user asked for it, tell them before launching that every round is a full review + judge + fix, so it uses many more tokens and makes the run much longer, for up to `maxRounds` rounds. With `plan` given and `"planReview": true`, the run's plan review checks it against the repo and fixes it (a dated "rN deltas" section at the top) before stage 1; tell the user that a plan review that ends `round-cap` or `review-failed` stops the run before anything is implemented. Without a plan review (no `plan`, `planReview` off, or a resume with `fromStage`): if dependency versions or upstream behaviour moved since it was written, update the plan yourself first, the same way, and tell the user what changed.
2. Branch and worktree - never work on `base`:
   - `worktree` on (the default): do not create or check out `branch` yourself; the engine's setup step does it before the first stage ([references/config.md](references/config.md#worktree)). Find out what it will do: when `git -C <repo> worktree list --porcelain` shows `branch refs/heads/<branch>` under some `worktree <path>` (the main checkout included), that path is reused and `git -C <path> status --short` must be clean, or the run fails before any agent starts; otherwise a worktree is created at `<worktreeDir>/<branch-slug>` (default `<parent of repo>/<repo name>-worktrees/<branch-slug>`, with `feat/login` as `feat-login`). Tell the user the path, and that a worktree the engine creates is removed when the run ends PR-ready, leaving the branch ("keepWorktree": true keeps it; a worktree granny did not create always stays).
   - `worktree: false`: `git -C <repo> status --short` is clean; create and check out `branch`.
3. The work dir (default `.granny/`) is in the common git dir's `info/exclude` (`git -C <repo> rev-parse --git-common-dir`). With the worktree on, the setup step adds it; with it off, add it yourself. It holds the PR body and review outputs (in the worktree; after its removal under `branches/<branch-key>/` in the main checkout), run journals, and the plan a planning run writes by default (`plans/`, in the main checkout) - so it must be excluded before the planner writes.
4. Reviewers - for each entry of `reviewers`, by the engine that will run (see [references/config.md](references/config.md#reviewers)):
   - On omp: no Codex engine - `auto`, `codex`, `codex-plugin` and an entry without `engine` are refused; offer an `agent` reviewer on an `openai-codex/...` model instead.
   - Codex CLI (engine `codex`, or `auto` on opencode, or `auto` on Claude Code without the plugin or without `node`): `codex --version` works and Codex is logged in (`codex login status`).
   - Codex plugin (engine `codex-plugin`, or `auto` on Claude Code when it is installed and `command -v node` finds `node`): `node --version` works; `ls "${CLAUDE_CONFIG_DIR:-$HOME/.claude}"/plugins/cache/openai-codex/codex/*/scripts/codex-companion.mjs` finds the companion (for `codex-plugin` on opencode: with the opencode server's `HOME` and `CLAUDE_CONFIG_DIR`); `codex --version` works and Codex is logged in - the companion drives the CLI.
   - Engine `agent`: the model exists on this host - on Claude Code only Claude models; for any other provider there, the reviewer needs engine `opencode`. `opencode models` and `omp models` list theirs. On opencode and omp `granny_run` refuses a model the host cannot run before anything starts, such as `sonnet` written as one string for every host, and names the fix: a host-keyed model ([references/config.md](references/config.md#models-per-host)). Pass the refusal on to the user; do not pick another model yourself.
   - Engine `command`: the CLI in the template is on `PATH` where the review runs (on opencode: the server's; on omp: the omp session's) and logged in to its provider.
   - Engine `opencode`: `opencode --version` works and `opencode models` lists the model (without its `#variant`), where the review runs (on Claude Code: your shell; on opencode: the server's; on omp: the omp session's). A model that is not listed, or a provider that is not logged in, fails the reviewer; tell the user, do not pick another model.
   Tell the user which reviewers will run and what `auto` will pick. A reviewer that fails twice in a round ends the stage `review-failed`. For the plan review the Codex engines run `codex exec` or the plugin's `task` instead of a diff review; a `command` reviewer without `{prompt}` sits the plan review out, and when no reviewer can review a plan, the plan review fails and the run stops.
5. `"readOnlyAgent": true` on Claude Code: `ls "${CLAUDE_CONFIG_DIR:-$HOME/.claude}"/agents/granny-readonly.md "${CLAUDE_CONFIG_DIR:-$HOME/.claude}"/hooks/granny-readonly-guard.mjs` finds both files (or the agent is in the project's `.claude/agents/`), the settings have the PreToolUse hook that runs the guard, and `node --version` works ([references/config.md](references/config.md#read-only-roles)). Without the agent the run stops at the first reviewer; without the hook or `node`, the read-only roles' Bash is not limited - tell the user.
6. No other session already runs the same job (other agents, `git reflog`).

## 4. Launch

Follow your host reference. On Claude Code the launch waits for the user's start word: prepare everything, say what will launch, and launch only after the user sent `start` (or the word in their language) as a message of its own, because the Workflow tool hands the user's last message to every agent of the run ([references/claude-code.md](references/claude-code.md#the-start-word)). Then tell the user, in their language: the run id, the worktree the run will work in and whether it will be removed at the end, the stages, threshold and round cap, plan review on or off (on: its token and time cost with the round cap - omp and opencode put that warning in the `granny_run` reply), the models per role, the reviewers, any `overrides:` line of the reply, where to watch the run when the reply names it (the run navigator on omp and opencode), and that nothing will be pushed. Do not poll; you are notified when the run ends.

## 5. When it completes

A planning run (result has `draft`): give the plan file paths, the planner's summary and the proposed stages, then - when the plan review ran - its outcome and its residual or unresolved findings; read the plan file yourself before vouching for it. Ask the planner's open questions with your host's question tool (`ask` on omp, `question` on opencode, `AskUserQuestion` on Claude Code), several in one call, instead of writing them out; without such a tool, ask in one numbered message. Ask the user to approve or change the plan and the stages. Then STOP. On approval, launch a new run - on Claude Code with `engines/claude-code/workflow.js`, not `plan.js` - with `plan: draft.files` and the approved `stages` (with `"planReview": true` in the config, add `"planReview": false` to the run overrides when the plan is unchanged since its review). When the planning run had `"stepAgents": true` among its run overrides, pass that override on the second run too: the planner's `steps` run as steps only with the setting on. After a plan review that ended `round-cap` or `review-failed`, say the plan still has unresolved findings and let the user decide.

Otherwise, read the result. Say first where the branch is, from `worktreeEnd` (one per repo in `repos`; absent with `worktree: false`, where the branch is checked out in `repo`). `removed: true`: the worktree `worktree` is gone and only the branch is left - the user checks it out in `repo` like any other branch and reviews and pushes from there; the PR body, the review outputs and the trail are in `saved`. `removed: false`: the branch is checked out in `worktree`, the user reviews and pushes from there, and `kept` is the reason granny left it - say it; `git worktree remove <path>` is then the user's call, never yours. Then the plan review, when the result has `plan`: its outcome (`clean`, `residual-only`, `round-cap`, `review-failed`, `skipped` on a resume, `review-skipped` with `planReview` off), its rounds, the residual and unresolved plan findings, and that the plan files now carry uncommitted fixes. After `round-cap` or `review-failed` the run stopped there: `stages` is empty and there is no final check - say that nothing was implemented, list the unresolved findings (and the note), and wait for the user. Otherwise report per stage: commits, gate numbers, review rounds, outcome (`clean`, `residual-only`, `round-cap`, `review-failed` with the reviewers its note names, `review-skipped`, `gates-red` - the review found nothing to fix but the implementer or the last fix left the gates red, so the stage is not clean (its note has the gates; residual findings are kept; never with checks configured for the stage - there the checks decide, and when they passed while the agent that last touched the stage's code reported red gates, the outcome stays and the note has a line `the checks passed, but <who> reported red gates: <gates>`: name that gate, the checks do not cover it) -, `checks-failed` - granny's own checks stayed red after the repairs, or the implementer left uncommitted work they would have run on (note `checks not run at <gate> - uncommitted changes: ...`) or granny could not read the working tree status (`checks not run at <gate> - working tree status unreadable (...)`), so the review did not run or stopped; its note names the red checks, their exit code or metric and the implementer's deviations, `checks` has every run, and the stages that build on it were not started -, `no-changes` - the implementer made no commit, not even after the one commit prompt a dirty tree gets (the note then names the files left uncommitted - say which), nothing was reviewed, and the stages that build on it were not started -, `skipped` on a resume or, with a note, because a stage it builds on delivered nothing), residual and unresolved findings with the reviewer each came from (ids are `<reviewer>-F<n>`; `residual` holds every round's residual findings, so a `clean` stage can have some), and a note line `uncommitted changes after <step>: ...` on any stage or final review - the review saw HEAD without that work, so say which files - or `working tree status unreadable after <step> ...` - granny could not tell whether work was left uncommitted, so say that; then the final review (`finalReview` in the result, and per repo in `repos`): its outcome, rounds and findings - `skipped` with its note for a repo with one stage and no lane merge, `review-skipped` with `finalReview` off, `checks-failed` when the checks on the whole branch stayed red - then say plainly that the branch is NOT PR-ready, with the note and `checks` from the result; after `round-cap` or `review-failed` say clearly that the branch still has unresolved findings although the final check ran; then the final check, and `recheck` when the result has it (per repo in `repos`) - the final check moved HEAD, so the checks ran once more: `passed: false` means the branch is NOT PR-ready - the checks are red or left uncommitted files -, say so with its note, whatever `finalReview` says -, the PR body path (`final.prBodyPath`: inside the worktree, or under `saved` after a removal), and deviations and untested items from the implementers, and the findings a fixer declined (`declined` on a round's `history` entry, with its reason). A run over several repos has `repos` in the result: name every repo's worktree, or its `saved` directory after a removal, and its final check, and each stage's `repo`. A stage whose note says it ran in parallel on a lane branch and was merged is in the run's branch (granny checked it with `git merge-base --is-ancestor`); when the note says its worktree or its branch was left in place, tell the user which. A run that failed with `<lane branch> is not merged into <branch>` left the lane's worktree and branch in place - name both. Then the review trail, when the result has `trail`: its `dir`, and every round in `trail.failed` - its record could not be written, so the PR will not get that round's comments. Before repeating a load-bearing claim from an agent, verify it yourself (open the file, rerun the gate - in the worktree; after a removal read the file with `git -C <repo> show <branch>:<path>` and do not check the branch out yourself).

Then STOP and wait. No push, no `git remote add`, no PR, no tag - the user decides.

### When the PR is opened

The run wrote one record per review round to `trail.dir` (none with config `trail: false`). Once the user has opened the PR - a GitHub PR or a GitLab MR - or asks you to open it, run `node <skill-dir>/scripts/pr-comments.mjs` in the checkout that has the branch and relay its output: the worktree, or after a removal the main checkout once the user has checked the branch out there; when it is checked out nowhere, run it in `repo` with `--pr <n> --trail <trail.dir>`. If it stops with `more than one trail exists`, it has posted nothing: run it again with `--trail` set to the run's `trail.dir` from the result - after a removal the saved `branches/<branch-key>/trail` of this branch, which holds this run's records, not the checkout's own `<workDir>/trail`, which can hold another branch's records - and tell the user which trail you posted. It tells the platform by the remote and posts one review per round, in the order they happened: each finding as a comment on its line, with the judge's tags and what became of it underneath, and the rest in the round's review body. On any other platform, `--out <file>` writes the rounds as JSON for another client to post; if the script cannot tell the platform, it says to pass `--platform github|gitlab` or `--out <file>`. Never write, edit or post review comments yourself. Only the script posts them. If the user opens the PR themselves, give them the command. Exit 2 means the branch has no PR or MR yet; a rerun posts only the rounds that are missing; `--dry-run` prints the reviews without posting. Details: [config.md](references/config.md#review-trail).

## Rules baked into the engine

Never push, never open a PR, never rebase or force-push, never `git stash`, never `git remote add` · stage with explicit paths only · `cd <worktree> &&` before every command (`cd <repo> &&` with `worktree: false`) · gates green before every commit · red-green tests for behaviour changes · no AI attribution in commits or the PR body (config `aiAttribution`) · artefacts in English (config `language`) · extra house rules from config `rules`. The agents that write (implementer, fixer, repair, commit, merge, final check) get all of them; the planner and the `agent` reviewers get only the repo, the `cd` prefix, the language, `rules` and the context (the planner also the gates, to write into the plan); a reviewer gets no rule whose text contains `comment`, so the no-comment rule goes only to the agents that write.
