---
name: qa
description: "QA a change in the running program, the way its user meets it: drive a CLI or terminal UI through tmux, a web app through a browser, and check every requested behavior against what you observe. Use after implementing a change and before code review, or when the user asks for a QA pass, a smoke test, or a click-through of a change, or asks whether it actually works."
argument-hint: "[fixed-point] [spec-path]"
license: MIT
compatibility: Terminal QA requires tmux, Perl, and a POSIX shell. Web QA uses whichever browser tool the session has (Chrome DevTools MCP, Claude in Chrome, Playwright MCP, or the host's own). The no-subagent fallback requires git, rsync, and Bun or Node.js.
---

QA checks the running program against what was requested; tests check the code against what its author expected. A scenario passes only on a result you **observed** in the running program. A green suite, a read of the code, or an exit status on its own is not an observation.

QA hunts for the fail. The author of a change grades it too kindly, so when this session wrote the change, run QA in a fresh subagent: give it the diff, the request, and this skill, and tell it to find where the change breaks. If subagents are unavailable, use a fresh session where possible; otherwise run QA here and report that it was not independent.

When no fresh subagent can start, follow [code-review step 5](../code-review/SKILL.md#5-run-the-available-readers-of-every-axis-in-parallel)'s **Capacity fallback** and **Execution access** brief, but permit QA builds and writes in a disposable copy, never the real repository. Create `$DIR` as below and copy with `rsync -a --no-specials --no-devices --exclude .git <repo>/ "$DIR/scratch/"`. After the [scratch containment and dependency preflight](../../references/scratch-dependencies.md), run `node <this file's directory>/scripts/scratch-sources.mjs prepare <repo> "$DIR/scratch" "$DIR"` (Bun: `bun --no-env-file`). It write-protects only the regular files of the repository's tracked and untracked sources that sit inside the copy, including a file a listed path reaches through a linked directory inside the copy, never following a link out of the copy, and writes the NUL-delimited manifests `$DIR/sources.lst` (sources present in the copy) and `$DIR/deleted.lst` (tracked paths deleted from the working tree). It removes any manifests an earlier run left before it starts. When a listed link, or a listed path under a linked directory, resolves outside the copy, it exits 1 naming each one, protects nothing, and leaves no manifest: stop the fallback and report QA as blocked on those links rather than running the copy. Then create `$DIR/tmp` with `mkdir -p "$DIR/tmp"`. Put the diff, request, and this skill in `$DIR/qa.prompt.md`, pointing execution paths at the copy and telling the reader to write scripts and state under `$DIR`, never into the change's files. Use a fresh same-family CLI reader:

- `TMPDIR="$DIR/tmp" codex exec - --ignore-user-config --disable apps --disable plugins -C "$DIR/scratch" -s workspace-write --add-dir "$DIR" -c sandbox_workspace_write.exclude_slash_tmp=true -c sandbox_workspace_write.exclude_tmpdir_env_var=true --skip-git-repo-check -c 'approval_policy="never"' --ephemeral -o "$DIR/qa.report.md" < "$DIR/qa.prompt.md" > "$DIR/qa.log" 2>&1`
- `(cd "$DIR/scratch" && claude -p --restricted --safe-mode --strict-mcp-config --tools Bash Read Grep Glob Write Edit --add-dir "$DIR" --permission-mode acceptEdits --settings '{"sandbox":{"enabled":true,"allowUnsandboxedCommands":false,"failIfUnavailable":true}}' --no-session-persistence < "$DIR/qa.prompt.md" > "$DIR/qa.report.md")`

Both forms confine writes to the copy and `$DIR` with no network (Codex's workspace sandbox; Claude's `--restricted` plus its OS sandbox); the Codex form also closes `/tmp` and the inherited `TMPDIR`. If a sandbox cannot start, report the QA gap rather than broadening permissions. Give no tracker or GitHub access; the copy has no `.git` to push from. Before the reader starts, copy the trusted, installed [repository snapshot helper](../code-review/scripts/snapshot-tree.mjs) to `$DIR/snapshot-tree.mjs`. From the real repository root, run `node "$DIR/snapshot-tree.mjs" "<repo>" > "$DIR/tree.before"` (Bun: `bun --no-env-file`) and require exit status zero before starting the reader. This captures `HEAD`, status, separate binary-capable working-tree and staged diffs, and nonignored untracked contents. Afterward, run the same helper into `$DIR/tree.after` and require exit status zero before running `cmp "$DIR/tree.before" "$DIR/tree.after"`. A snapshot failure or comparison error is incomplete coverage, never proof of unchanged state. Then run `node <this file's directory>/scripts/scratch-sources.mjs verify <repo> "$DIR/scratch" "$DIR"`, which prints each source in the manifest whose content, type, executable bits, or link target changed in the copy or went missing from either tree, each deleted path the copy recreated, and each entry it cannot read. Report any real-tree difference or any line from the source comparison as a QA failure of the run, not of the change, and name the reader as a same-family fallback.

QA runs before `code-review`: once QA shows the change does what was asked, the review can spend itself on how the code is written and how it fails.

QA reports to its caller and leaves the code and the issue tracker as it found them: it files, comments on, and labels no issue, since a fail in unmerged work is the caller's to fix, not a ticket. Scratch state, scenario lists, reports, screenshots, and raw evidence go in `$DIR`, a fresh `mktemp -d` in the OS temporary directory outside the repository. Return the report to the caller with paths to retained evidence there. Saving or committing QA artifacts in the repository requires an explicit user request; callers keep the same storage rule when handing off or shipping the work. The caller fixes each fail, test-first, and runs QA again.

## Process

### 1. Pin the change and the request

The change is the diff since a fixed point: the one the caller or user names; else the default branch, when `HEAD` is on another branch; else `HEAD`, when the default branch has uncommitted work. Write the diff to disk with `git diff <fixed-point> > "$DIR/diff.patch"` and read that file in full: a shell hook can shorten a diff printed to the terminal, and a redirected one lands on disk whole. Read large files in bounded windows, keeping the combined output of each tool response below the host's limit. Advance to the next window only after the current one is complete; reread a truncated window in smaller parts. Also read each untracked file `git status --short` lists.

The request is what the change was meant to do: the spec or issue the caller passes, else the issue its commits reference, else the request settled in this conversation. With none, ask.

For a follow-up with a prior report and its tested commit, inspect the intervening diff. Rerun the earlier fails, scenarios affected by the fix, and one adjacent regression flow. Carry forward unaffected passes and blocked scenarios with their original evidence and tested commit; a gap stays blocked until observed. Expand only where the diff, a new failure, or an explicit repository requirement makes earlier evidence invalid. Without a usable prior report, run the full pass. A test-only or report-only diff with unchanged runtime code and configuration keeps the earlier browser verdict.

### 2. Write the scenarios

A **scenario** is one thing a user does and the result they should then see: the steps, and the expected result taken from the request. Write the list to `$DIR/scenarios.md` before you launch anything, distinguishing reruns from carried-forward evidence on a follow-up. A full pass covers:

- every requirement in the request;
- every user-reachable path the diff changes that the request never names (a new flag, a reworded message, a moved button);
- the unhappy paths of each: invalid or empty input, cancel or interrupt midway, the same action twice, a first run with no saved state;
- data attacks on each new input: Goldilocks (too small, too big, just right), each boundary and one past it, 0, 1, and many items, and text with unicode, emoji, leading or trailing spaces, quotes, delimiters, and a newline;
- CRUD on each record the change writes: create, read, update, and delete it, and follow the data to every view that shows it and through a restart;
- a flow: the scenarios chained one after another with no reset between them, the way a user's session runs, entering and leaving each state the change adds;
- one existing flow that shares the changed code, to catch a regression next to the change.

Above the scenarios, list the change's invariants under **Never and always**: what must never happen (data lost, a file left half-written, a secret in a log) and what must always hold (the terminal restored, the old data still readable). Check them after every scenario, the unhappy ones most of all.

For a change meant to keep behavior (a refactor), the expected result is the base build's screen. Create the export directory and export the base commit with `mkdir -p "$DIR/base" && git archive <base> | tar -x -C "$DIR/base"` and build it there with a private dependency directory and generated caches. Prepare dependencies with the base's lockfile and repository commands inside the export. Before comparing a scenario, confirm the base renders its normal screen; a server URL that answers with a runner error is a blocked comparison, with its startup evidence. A `git worktree` shares `.git/hooks` with the main checkout, so a dependency install in one runs the old commit's `prepare` script and rewrites the main checkout's hooks. Drive both builds with the same keys, from folders with the same name and the same seeded state, and diff the captures. Mask only what changes on every run, such as a clock.

Done when every requirement and every changed user-reachable path maps to at least one scenario.

### 3. Launch the program

Use the repository's own build and start commands (its README, `package.json` scripts, `Makefile`, or `--help`) when a current build or preview is not already available and verified. Point it at scratch state: a directory under `$DIR`, a test database, a seeded test account, a local server. A scenario that can only run against real user data, a production service, or a live account is **blocked**: name what it needs and move on.

Pick the driver by the program's interface:

- A CLI or terminal UI: read [TERMINAL.md](TERMINAL.md).
- A web app: read [BROWSER.md](BROWSER.md).
- A library or HTTP API with no UI: call its public interface from a scratch script in `$DIR`, or with `curl`, the way its caller would.

### 4. Run the required scenarios

Run every scenario on an initial pass; on a follow-up, run those selected in step 1 and retain the others with their prior evidence. Do each step as the user would: type the command, press the keys, click, fill in the form, submit. After each step, read what the program shows and compare it with the expected result. Check the logs, stderr, and browser console for errors on every scenario you run, passing ones too.

Judge each result with the FEW HICCUPPS oracles as well as the request. A result that matches the request still fails when it contradicts the rest of the product (a sibling command names its flags, keys, or exit codes another way), the program's own claims (`--help`, the README, its error text), or the conventions of its platform and of comparable tools (`NO_COLOR`, `-` for stdin, a 4xx status for a bad request). An error message passes when it names the bad input and what to do next.

A screen that says "Saved" shows only that the program claims the write. Confirm each write at its store: read back the file, the database row, or the API, then restart or reload and read it again.

Record each scenario in `$DIR/scenarios.md` as **pass**, **fail**, or **blocked**, with its evidence: the captured screen, the output, a screenshot path, the error. Evidence is what the tool wrote: redirect or `tee` output into a file in `$DIR` and cite that file, so a retyped summary never stands in for it. A fail also records the steps that reproduce it, the expected result, and the observed one. Before you record a fail, spend a few steps on it:

- **Isolate**: cut the steps to the fewest that still fail.
- **Maximize**: follow the same path to a worse outcome, such as a crash or lost data.
- **Generalize**: try the sibling paths that reach the same code, and name every one that fails.
- **Introduced or pre-existing**: run the same steps on the base build, exported as for a refactor, and record which it is.

A fail ends that scenario, not the run.

Once every scripted scenario has a status, run one exploratory charter on the riskiest part of the change: "Explore <target> with <resources> to discover <information>", for about twenty actions. On a follow-up, keep exploration within the fix and its adjacent regression flow. Add each problem it finds to `$DIR/scenarios.md` as a new scenario with its status.

Done when every scenario has a status and its evidence.

### 5. Clean up and report

Stop everything you started: each tmux session with `tui stop qa-<name>` (the run's tmux server exits with its last session), then servers and browser tabs. Keep the evidence files the report cites in `$DIR`, and delete the remaining scratch state. Use literal paths, typed out as the earlier call printed them: an `rm -rf` on a variable or a command substitution, such as `"$(cat /tmp/qa-dir)"`, is denied. Done when `tmux ls` lists none of your sessions and `$DIR` holds nothing but those evidence files. A cleanup command that fails or is blocked goes in the report as leftover state, with the command to remove it.

Report one line per scenario (status, what it checked, the evidence or its path), then every fail in full, then:

- **Not covered**: what no scenario tested and why, such as a platform, a browser, or a terminal you did not run.
- **Concerns**: what is neither a pass nor a fail but looked wrong, such as a slow first load or a stray warning. A result that contradicts a sentence of the request is a fail, also when that sentence calls the path unchanged or out of scope.

Then the verdict:

- Any fail: **Fails QA**.
- Otherwise, any blocked scenario: **Passes with gaps**, naming each blocked scenario and what it needs.
- Otherwise: **Passes QA**.
