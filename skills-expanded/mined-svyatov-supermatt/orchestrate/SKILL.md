---
name: orchestrate
description: "Work through GitHub, Linear, or local Markdown issues unattended in parallel lanes, with workers in Herdr or Rex panes and git worktrees."
argument-hint: "[parallel runs]"
disable-model-invocation: true
compatibility: Designed for Claude Code, Codex, Cursor, and OMP. Requires the matching host CLI and Herdr integration, or Rex for Codex, gh for GitHub PR shipping, and Bun or Node.js 18.17 or later (built-in modules only). Linear trackers require a connected Linear MCP. The notification uses osascript, so it shows on macOS only.
license: MIT
---

# orchestrate

You are the orchestrator. You do not write code. You pick issues, drive workers in the same harness that runs you, and check their results. The work runs in LANES parallel lanes: each lane has a terminal pane beside yours and a git worktree of its own, and works one issue at a time. A spec whose tickets are all closed comes first: one worker session **V** checks the whole spec against the code (see [SPEC.md](SPEC.md)). Bugs come next, then the other tickets. Each ticket runs through up to four worker sessions, each with a fresh context:

1. **T**: `/triage REF`, only for a bug that is not triaged yet, to make it ready for an agent.
2. **A**: `/implement REF`, which QAs, reviews, and fixes its own work, then any fixes it left.
3. **B**: `/refactor`, then `/ship-pr` to merge.
4. **C**: `/retro` over A and B, reporting candidates for the operator without applying them.

Repeat until a stop condition is met. Never ask the user anything, through a question tool or otherwise: answer every question and dialog as below.

Before dispatching, read the [orchestrator dispatch contract](../../references/harnesses.md#orchestrator-dispatch). This explicit invocation delegates only its listed worker commands within this run. Use [Send the prompt](WORKER.md#dispatch-preamble) for every instruction prompt: it attaches the assigned issue, worktree, phase, approval scope, and relevant prior evidence at dispatch. Keep the called skills' invocation policies unchanged; park when a required human approval is outside the delegated scope.

## Setup

Select the terminal from the current host session. In Rex, use [Rex terminal operations](REX.md) for setup steps 1 through 4 and every pane or worker operation in the loop. Continue with common setup step 5. In Herdr, use the commands below. When inherited markers identify both, require authoritative current-terminal context before choosing. An ambiguous, incomplete or inaccessible target stops setup. Never fall back to another terminal after an access failure.

1. For Herdr require `HERDR_ENV=1`. Outside either supported terminal, report that `orchestrate` requires Herdr or Rex and stop.
   Check the host's execution restrictions before the first Herdr, GitHub, or Git write call. This run needs access to the local Herdr socket, GitHub, and the checkout's Git metadata. Use the host's permission mechanism for access outside its sandbox, retaining any approval already granted. Confirm socket access with `herdr agent list` and GitHub access with the default-branch query in step 6. Stop if required access is denied or unavailable; report the exact blocked operation.
2. PROJECT is the repo folder name (`basename "$(git rev-parse --show-toplevel)"`) made into a valid herdr agent name: lowercase it, change each character outside `a-z`, `0-9`, `_` and `-` to `-`, drop leading characters that are not letters, and keep at most 20 characters. Choose K as the lowest positive number unused by live `PROJECT-orch-K` or `PROJECT-work-K-L` agents and by any registered or existing `.claude/worktrees/orch-K-L` path. Check `herdr agent list`, `git worktree list --porcelain`, and the worktree directory before naming this run. Retained lanes reserve their K until separately cleaned up. Now, before any check that can stop, run `herdr agent rename "$HERDR_PANE_ID" PROJECT-orch-K` and `herdr pane report-metadata "$HERDR_PANE_ID" --source orchestrate --display-agent orchestrator`.
3. Set KIND from the harness running this skill: `claude`, `codex`, `cursor`, or `omp`. Use authoritative current-session harness metadata first. When unavailable, read `herdr agent get "$HERDR_PANE_ID"` `.result.agent.agent`; accept only those four values. If that does not identify it, `CLAUDE_CODE_CHILD_SESSION=1` identifies Claude Code, and any of `CODEX_SANDBOX`, `CODEX_SESSION_ID`, or `CODEX_THREAD_ID` identifies Codex. `CLAUDECODE`, `OMP_PROFILE`, `OMPCODE`, and model or provider names do not identify the host. Set CLI to `agent` for Cursor and to KIND otherwise, then require `command -v "$CLI"`. Every worker and restart uses KIND; a failed launch parks its lane instead of switching harnesses.
   For Cursor and OMP, require the matching kind in `herdr agent start --help` and an enabled matching integration in `herdr integration status`. Report the exact unsupported integration or missing CLI and stop without upgrading or installing it. Claude Code uses SESSION_ROOT `$CLAUDE_CONFIG_DIR/projects/`, or `~/.claude/projects/` when unset. Codex uses `$CODEX_HOME/sessions/`, or `~/.codex/sessions/` when unset. Cursor and OMP use only Herdr-reported session IDs or paths because their storage can move. Send skills using the notation below.
4. Run `herdr --skill` and follow its rules. Parse every ID from JSON output. Never close a tab or pane you did not create.
5. Read `docs/agents/issue-tracker.md` and `docs/agents/triage-labels.md`. If either is missing, or the tracker is outside the supported GitHub, Linear, and local Markdown modes, say so and stop. READY, BUG, and TRIAGE are the label strings that `triage-labels.md` maps to the ready-for-agent, bug, and needs-triage roles. For local Markdown, read [LOCAL.md](LOCAL.md) now and retain its tracker ownership rules for every worker. For Linear, read [LINEAR.md](LINEAR.md) for queue reads and lane ownership. GitHub hosts PRs in every mode.
6. Your working directory is the repo's main checkout. It stays on DEFAULT for the whole run; the workers work in the lanes' worktrees. DEFAULT is the output of `gh repo view --json defaultBranchRef --jq .defaultBranchRef.name`. Run `git switch DEFAULT && git -c pull.rebase=false pull --ff-only`. The command-local setting keeps a user's rebase default out of this fast-forward operation. The tree must be clean. If it is not, stop. If `git check-ignore -q .claude/worktrees/x` fails, append the line `.claude/worktrees/` to `.git/info/exclude`, so the worktrees stay out of `git status`.
7. LANES is the number in the arguments, or 1 when there is none. RUN_START is `date -u +%Y-%m-%dT%H:%M:%SZ`. RUN is `bun` when `command -v bun` finds it, else `node`. QUEUE is `RUN <this skill's directory>/scripts/next-issue.mjs READY BUG TRIAGE`; for local Markdown insert `--local ROOT` before the labels, with ROOT from LOCAL.md. For Linear, QUEUE includes a fresh MCP read and the selector invocation in LINEAR.md. Run QUEUE and print its output so the operator sees what will run. A nonzero result is a failed queue read, never an empty queue.
8. Open the lanes (see Lanes).

### Skill notation

Every `/name` skill reference below and in the linked procedures is notation: translate it before sending a worker prompt. Claude Code uses `/supermatt:name` when this skill comes from the installed plugin, or `/name` when linked into its skill directory. A bare `/code-review` from that plugin would run Claude Code's bundled review instead. Cursor uses `/name`. Codex uses `$name`, including from its plugin. OMP uses `/skill:<name>`. Preserve all arguments. Shell-quote prompts, paths, and values; quote Codex prompts so `$name` reaches the worker literally, for example `herdr agent prompt WORKER '$implement #123' --wait`. Native commands such as `/exit` keep their spelling in all four harnesses.

For Cursor and OMP, require the SuperMatt skill commands to be discoverable by the worker before work starts. Resolve each required `/name` or `/skill:name` to SuperMatt, including existing `~/.agents/skills` discovery where the host supports it. A missing or conflicting same-named skill parks the lane; never substitute a bare command or another harness.

## Lanes

Lane L, from 1 to LANES, has a pane, a worker agent named `PROJECT-work-K-L`, and a worktree at `<repo root>/.claude/worktrees/orch-K-L`, inside the repo so Claude Code's folder trust carries over. Every host uses the same worktree location. Below, PANE, WORKER, and WT are the current lane's, and every git command about the lane's work runs as `git -C WT`. IN_FLIGHT is the set of issue keys the lanes hold, parked lanes included: GitHub numbers, full Linear identifiers, or repository-relative Markdown paths. For Linear, REF and DISPLAY are the full identifier (such as `ENG-42`). Otherwise REF is `#N` for GitHub or the absolute canonical file path for local Markdown; DISPLAY is `#N` or the repository-relative path. Use REF in worker prompts and DISPLAY in phase names and reports.

- **Open the lanes** once, at setup, as shell panes stacked in one column right of yours, with equal heights. Lane 1: `herdr pane split "$HERDR_PANE_ID" --direction right --no-focus --cwd "$PWD"`. Lane L above 1: `herdr pane split <lane L-1's pane> --direction down --ratio R --no-focus --cwd "$PWD"`, where R is 1/(LANES-L+2), the share lane L-1 keeps. Save each `.result.pane.pane_id`. The panes stay for the whole run.
- **Create the worktree** on branch B: `git fetch origin && git worktree add -b B WT origin/DEFAULT`, or `git worktree add --detach WT origin/DEFAULT` with no branch. Leave `.env*` files uncopied by default. Have the worker try the repository's checks and local preview without credentials. Supply environment values only when a required operation reports that it needs them and existing user authorization permits access. Preserve user restrictions on reading, copying, linking, or loading environment files; if a required value cannot be supplied within those restrictions, park the lane with the exact requirement.
- **Remove the worktree**: stop any live worker and confirm its harness process has exited, so its hooks no longer need WT. If WT exists, `git worktree remove WT`, and delete each still-local branch recorded for this lane only after its PR is confirmed merged and its local head matches the recorded PR head (B plus any CI repair branches). Retain unmerged or externally changed branches for inspection. A worker that has not exited or a worktree with changes parks the lane.
- **Park the lane**: stop driving it, ignore its later notifications, and leave its pane, worker, and worktree as they are. Its issue stays in IN_FLIGHT. If it holds the ship slot, release it; a failed or blocked post-merge workflow keeps the separate default-branch merge hold set. Send the notification (see On stop) with the title `PROJECT lane L needs you` and the reason as its body, and add the reason to the friction log. The other lanes go on.

## Run the lanes

Each lane runs the Loop on its own issue. Start by running Pick the issue for lanes 1 to LANES in order, so lane 1 takes the first issue in the queue. Then act on whichever lane's background wait notifies you, take that lane through its next steps up to its next wait, and wait again.

Before dispatching concurrent lanes, read [Parallel resources](../../references/parallel-resources.md). Keep resource ownership with lane state, pass the assignment on every worker launch and restart, and recheck it when a phase introduces a new resource. A parked lane retains resources its live processes still use. This resource gate is separate from the ship slot below.

- A lane whose Pick finds nothing goes idle. Whenever an issue closes or a lane goes back to Pick, run Pick for every idle lane too: a closed issue can unblock others.
- The ship slot: one lane at a time runs from Sync through CI recovery, post-merge workflow verification, and Close out. A lane that reaches Sync while another holds the slot waits for it. A failed or blocked default-branch workflow sets a separate merge hold; releasing a parked lane's slot does not clear that hold. Other lanes may finish work through Refactor, but start no new issue and perform no Sync or merge while the hold remains. If recovery parks, retain those waiting lanes for inspection and stop once every other busy lane reaches that boundary.
- When every lane is idle or parked, stop (see Stop conditions).

Before the first worker launch, read [WORKER.md](WORKER.md) for every host's model and effort policy, launch and restart recipes, and session evidence handling. Apply it to all worker phases below, including spec verification and triage.

## Answers

When a worker is `blocked`, or has an open question (QUESTION is not NONE, or it ended its turn on a question), read [ANSWER.md](ANSWER.md): its Answer a dialog and Answer a question are the procedures the steps below name, and its Safe actions decide what you may approve.

## Loop

### 1. Pick the issue

If the operator asked you to pause, the lane goes idle. Otherwise run QUEUE in the main checkout. It lists the open, unassigned issues to work on, with an open blocker (native, or a `Blocked by:` line) dropped: specs whose tickets are all closed, then bugs, then the rest, lowest number first, then path for tied local numbers. Each line is `key<TAB>title<TAB>spec|ready|triage`. GitHub specs and TRIAGE bugs count only when the repo's own team filed them. Linear uses the configured project and native relations in LINEAR.md. Local files use the repository's trusted tracker; malformed or missing blocker references fail the read.

Take the first line whose key is not in IN_FLIGHT. If there is none, the lane goes idle. Add its key to IN_FLIGHT, set REF and DISPLAY, and say `lane L: DISPLAY title`. Empty SESSIONS. Create the worktree: with no branch for a `spec`; otherwise on branch `fix/ID-<slug>` for an issue labelled BUG and `feat/ID-<slug>` for any other, where slug is the title in lowercase kebab case, at most 40 characters. ID is N for GitHub or the full team-prefixed identifier in lowercase for Linear; for local files use K-L plus a counter incremented on each pick in that lane, so repeated numbers and titles cannot collide. If its last column is `spec`, verify it: read [SPEC.md](SPEC.md). If it is `triage`, triage it first: read [TRIAGE.md](TRIAGE.md).

### 2. Implement (session A)

1. Show phase `implement`. Start the worker.
2. `herdr agent prompt WORKER "/implement REF" --wait` with no `--timeout`, then wait for the worker. Substitute and quote REF before sending. For Codex, Cursor, and OMP, append to the translated prompt: `Complete implementation and QA, then stop before code-review. The orchestrator will run code-review and fix its findings in a fresh session.` This can take a long time.
3. Run `git -C WT log --oneline origin/DEFAULT..HEAD`. If it is empty, ask the five-line question from step 3. If QUESTION is not NONE, answer it, wait for the worker, and run this check again. Otherwise read the pane, report what the worker said, and park the lane.

### 3. Check the worker

Keep the latest QA and review reports with their checked commits in the lane's state; request them from the worker if its handoff gives only verdicts. A fresh worker's `NONE` means that session has no result; it does not erase an earlier result or its open findings. Before reusing one, inspect changes since its checked commit: retain unaffected QA evidence and review dispositions, and pass the prior reports and intervening diff to any follow-up. Review is current only when the intervening diff is empty or a completed follow-up covers it. Missing reports or changes that invalidate coverage require verification. Ask the worker, do not guess from scrollback:

```bash
herdr agent prompt WORKER "Reply with exactly five lines and nothing else. Line 1: BUSY=<yes if a background task or sub-agent you started is still running, else no>. Line 2: QA=<the verdict line of the last QA pass in this session, or NONE if none ran>. Line 3: REVIEW=<the verdict line of the code-review you ran in this session, or NONE if you did not run it>. Line 4: UNFIXED=<the code, or file:line if it has no code, of each verified finding and each QA fail that is still open: not fixed, and not settled by an answer to your question, or NONE>. Line 5: QUESTION=<a question you asked the user in this session that has no answer yet, or NONE>." --wait
herdr agent read WORKER --source recent-unwrapped --lines 40
```

- BUSY=yes: run `sleep 60` in the background, then ask again. If BUSY is still yes after 30 minutes, park the lane.
- QUESTION is not NONE: answer it (see Answer a question).
- Missing, incomplete, or invalidated QA coverage, including QA=NONE with no reusable lane result: run `git -C WT log --format=%s origin/DEFAULT..HEAD`. If every subject has the type `refactor` and the actual diff confirms no user-visible behavior change, QA may be `skipped, refactor only`, with that justification recorded. Otherwise show phase `qa`, restart the worker, prompt it with `/qa origin/DEFAULT REF` (`--wait`, no timeout), passing prior reports, checked commits, and the intervening diff so it completes only missing or affected coverage. Wait for the worker and ask it the same five-line question.
- Missing, incomplete, or invalidated review coverage, including REVIEW=NONE with no reusable lane result: show phase `review`, restart the worker, prompt it with `/code-review` (`--wait`, no timeout), passing prior reports, checked commits, and the intervening diff for follow-up coverage. Wait for the worker and ask it the same five-line question.

**Coverage gate:** inspect the full reports, not just the five-line reply or the presence of a verdict. Every required QA scenario and every review axis (Standards, Spec, Adversarial) must have current, complete evidence or an explicit, evidence-backed not-applicable justification. A missing report, unavailable check, blocked or untested scenario, or incomplete axis is a coverage gap, never N/A; no findings does not mean complete coverage. Preserve justified N/A cases and unaffected evidence under the reuse rules above. Complete missing or invalidated checks as above within the delegated approval scope; if a prerequisite is unavailable or any gap remains after follow-up, park with the exact unresolved coverage and what it needs. Route open failures and findings through Fix findings and reapply this gate on the resulting head. Advance only with complete coverage and no unresolved failures or findings.

### 4. Fix findings

If UNFIXED is not NONE, show phase `fix`, prompt the current worker with `/fix-findings <the UNFIXED value>` (`--wait`), the prior reports and their checked commits, and instructions to verify behavior-changing fixes test-first, run affected QA, and obtain independent review of the fix commits, carrying prior reports and checked commits forward. Test-only fixes need affected tests and independent review, not repeated QA of unchanged runtime behavior. Wait for the worker. Then ask the five-line question again, and answer any open question. A finding that `/fix-findings` reported as `pending, <choice>` or `deferred, follow-up pending` waits on a choice, even when QUESTION is NONE: answer that choice through Answer a question (a follow-up issue offer is a yes/no question), and ask the five-line question again. A finding that `/fix-findings` settled with no edit, because the option it applied (its own recommendation, or what the issue asks for) keeps the code as it is, counts as fixed, and so does one it reports as `deferred to <issue>` or `deferred, follow-up declined` after your answer. If UNFIXED still names a finding that is open, park the lane. Then prompt `/commit` (`--wait`) and wait for the worker, so the tree is clean for session B. Reapply Check the worker's coverage gate before advancing.

### 5. Refactor (session B)

1. Show phase `refactor`. Restart the worker.
2. Prompt `/refactor the changes on this branch since origin/DEFAULT` (`--wait`, no timeout) and wait for the worker. Its questions and plan approval go through Answer a dialog and Answer a question.
3. If `git -C WT status --porcelain` prints anything, prompt `/commit` (`--wait`) and wait for the worker.

### 6. Sync

Other lanes may have merged since this branch started. Wait for the ship slot (see Run the lanes), then bring the branch onto the current DEFAULT. The branch is not pushed yet, so a rebase rewrites nothing shared.

1. Show phase `sync`. Run `git -C WT fetch origin && git -C WT rebase origin/DEFAULT`. If it rebased clean, go to Ship.
2. It stopped on conflicts: add `DISPLAY rebase conflicts in <files>` to the friction log, prompt the current worker with `/resolving-merge-conflicts` (`--wait`, no timeout), and wait for the worker. The rebase is done when `git -C WT status` no longer reports a rebase in progress and `git -C WT status --porcelain` prints nothing. If it is not, park the lane.
3. The resolved code is code that no QA pass ran: prompt `/qa origin/DEFAULT REF` (`--wait`, no timeout), passing prior reports, checked commits, and the conflict-resolution diff. Wait for the worker and ask the five-line question from step 3. If its QA report has a fail, park the lane. Otherwise apply Check the worker's coverage gate, including review of the resolved changes. Retain the resulting reports and checked commits for Ship.

### 7. Ship

1. Before dispatching, apply Check the worker's coverage gate to the final head after Refactor and Sync, including a clean rebase. Only when it passes, show phase `ship` and prompt the current worker with `/ship-pr QA of this branch stands: <the current QA verdict>` (`--wait`, no timeout), including the resulting QA/review reports and checked commits, current resource assignment, and any existing shipping record. Session B otherwise has no record of session A's QA. Let the explicitly invoked ship-pr skill complete its bounded CI recovery through `recover-ci`, including the [post-merge repair](../ship-pr/CI.md) follow-up PRs and post-merge verification; keep the ship slot throughout. A failed check during that procedure is progress to diagnose, not an immediate park condition.
2. Read its report and shipping record. Retain all original/repair PR URLs, branch names, merge and checked commits, run IDs/attempts, recovery counters, and the latest QA/review reports in lane state. Show phase `repair` while recovery is active. A new session or dispatch carries the same record and budget, never a fresh allowance. Record each diagnosis, rerun, repair and outcome in the friction log. Set the default-branch merge hold as soon as a failed or blocked post-merge workflow is reported.
3. Independently confirm each reported merge with `gh pr view <url> --json state,mergedAt,mergeCommit` and the reported CI outcomes with `gh`. Proceed only when the original and any repair PRs are MERGED and the applicable post-merge workflows at the latest repair merge (the original merge when no repair was needed) have succeeded, or configuration proves none apply. A verified repair resolves the historical failure; retain its failed run without requiring a rerun or changing its recorded result. Clear the merge hold only with that evidence for current DEFAULT. If the worker returned only the original merge result, have it finish post-merge verification with the existing record. Park when CI recovery stops with an unresolved failure or blocker, or a push/merge is refused. Preserve successful merges separately from failed recovery; do not restart an exhausted repair loop.

### 8. Close out

1. For Linear, verify the assigned REF is an explicit resolution target and follow the completion procedure in LINEAR.md. For GitHub and local Markdown, read REF with the configured tracker's **Read an issue** operation. If still open, use its **Close** operation with `Merged in <PR URL>.` For local Markdown, verify the canonical file has its `Closed:` date and comment. A closed issue unblocks the issues that wait on it.
2. Stop the worker and confirm its harness process has exited.
3. In the main checkout: `git -c pull.rebase=false pull --ff-only`. The tree must be clean.
4. Remove the clean worktree and release the ship slot.
5. Create a detached worktree for the read-only retrospective.

### 9. Retro (session C)

1. Show phase `retro`. Start the worker.
2. Prompt `/retro the sessions <SESSIONS>. Report candidates only. Leave this repository and external sources unchanged; do not apply candidates, create checks, file issues, or publish a lessons PR.` (`--wait`, no timeout). Pass OMP's recorded absolute transcript paths and Cursor's authoritative Herdr session IDs or paths. For Claude and Codex, use resolved paths when recorded, otherwise include `with transcripts under <SESSION_ROOT>` with the actual root. Wait for the worker.
3. Record each surviving candidate in the friction log with its source and proposed fix. LESSONS is `none` or `<count> candidates reported`. Applying candidates is separate work for an explicit user request, not another step in this loop.
4. Stop the worker and confirm its harness process has exited. Confirm `git -C WT status --porcelain` is empty. Unexpected changes park the lane for inspection; do not commit or discard them. Remove the clean worktree and go to Report.

### 10. Report

1. Drop the key from IN_FLIGHT.
2. For GitHub, run `gh issue list --state all --search "created:>=RUN_START" --json number,title`. For Linear, list issues created since RUN_START across all teams of the configured project, following pagination. For local Markdown, compare current ticket paths with the initial inventory from LOCAL.md. Add each new issue not yet in the friction log as `filed DISPLAY title`. Workers file bugs they find outside their issue; the next pick takes them first.
3. Report one line: `lane L: DISPLAY -> <PR URLs, including repairs>, merged, post-merge CI <outcome>, QA <verdict>, review <verdict>, lessons <LESSONS>`. Retain recovery evidence before cleanup.
4. Go back to Pick the issue.

## Operator

- **Pause**: the operator can type into your pane while you work. A request to pause or stop means every busy lane finishes its current issue through Report and no lane picks a new one; then stop. A request to stop now means stop at once.
- **Friction log**: keep a running list across issues, each entry with its lane and issue: each dialog and question you answered (phase, what you chose), each `--wait` that returned `timeout` or `agent_prompt_stalled`, each restart of the worker outside Refactor and Retro, each rebase conflict, each history edit you made in a lane and its check result, each parked lane and its reason, each reported retro candidate, each triage outcome other than READY, and each issue filed during the run. Print it when you stop; it is the operator's input for tuning this skill.
- **On stop**: send one macOS notification, then print the reason and the friction log, including reported retrospective candidates. The operator is notified only here and when a lane parks: when the run is finished, or when it needs them.
  - No lane is parked: title `PROJECT done`, body `<count> issues merged, <count> filed`.
  - A lane is parked, or Setup failed: title `PROJECT needs you`, body the reason, or each parked lane with its issue and reason.

  Pass the text as arguments, so quotes in a reason cannot break the script: `osascript -e 'on run argv' -e 'display notification (item 2 of argv) with title (item 1 of argv) sound name "Glass"' -e 'end run' "TITLE" "BODY"`.

## Stop conditions

Park the lane when: triage left a bug untriaged, a spec found gaps on its second verification, `/implement` made no commits, a question stays open after three answer rounds (five in session T), a dialog stays open after two answers, the worker asks to run an unsafe action, findings stay unfixed after `/fix-findings`, Check the worker's coverage gate cannot be completed, a rebase stays unfinished after `/resolving-merge-conflicts` or its QA fails, CI recovery stops with an unresolved failure or blocker, a push or merge is refused, the read-only retrospective changes files, a worktree with changes refuses removal, or a Linear MCP, terminal, gh, or git control operation about the lane fails outside a handled recovery path. A nonzero CI check result follows CI recovery instead of this command-failure stop.

Stop the run when every lane is idle or parked (including lanes retained at the merge hold after another lane's recovery stopped): the queue has nothing left that no lane holds, or the operator paused. Stop it at once when a Setup step fails or a terminal command about the run itself fails. On stop, close the panes of idle lanes, and leave the panes and worktrees of parked lanes open, so the operator can inspect them.

## Rules

- One issue per lane, so at most LANES in flight. A lane starts its next issue after its issue is merged and its retrospective candidates are reported.
- One lane at a time holds the ship slot.
- When you move a lane's commits yourself outside Sync (cherry-pick, reset, revert, or another history edit, including splitting work into another issue), the resulting HEAD is code that no check has run on. Before the next phase, run the repository's typecheck and tests in WT, using the commands named in its AGENTS.md, CONTRIBUTING.md, or CI configuration. If either fails, send the worker the failure as a finding through `/fix-findings` with the failing output, and hold QA and review until the finding is fixed and the checks pass. You move commits and verify the result; the worker makes all code changes. Sync keeps its own handling.
- Never remove a worktree the run did not create.
- Run unattended. Never hand a question or dialog to the user; answer it as above.
- If a `--wait` returns `timeout` or `agent_prompt_stalled`, read the pane before you do anything, since the prompt may have landed.
