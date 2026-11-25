---
name: reflektor
license: MIT
description: Builds a visual HTML review report for the current branch or PR against its base branch, with a plain-English title and summary, review order, highlights, request flows, GitHub-style diffs with notes, and test coverage of new lines. The user can comment in the report and send the comments back for fixing. Use when the user asks for a PR report, a review report, a summary of branch changes for review, or wants to review changes before opening a PR. Works with any language or stack.
argument-hint: "[base-branch] [--since last] [--session] [resume] [push]"
allowed-tools: Bash(node "${CLAUDE_SKILL_DIR}/scripts/collect.mjs" *), Bash(node "${CLAUDE_SKILL_DIR}/scripts/checks.mjs" *), Bash(node "${CLAUDE_SKILL_DIR}/scripts/build.mjs" *), Bash(node "${CLAUDE_SKILL_DIR}/scripts/review.mjs" *), Bash(node ${CLAUDE_SKILL_DIR}/scripts/collect.mjs *), Bash(node ${CLAUDE_SKILL_DIR}/scripts/checks.mjs *), Bash(node ${CLAUDE_SKILL_DIR}/scripts/build.mjs *), Bash(node ${CLAUDE_SKILL_DIR}/scripts/review.mjs *)
---

# reflektor

You write the judgment in `report.json`: words, grouping, risks and flows. Scripts handle the facts: git data, diffs, coverage numbers and rendering. Never copy code into report.json. Point at files and lines instead.

Scripts and reference files live in `${CLAUDE_SKILL_DIR}`. That is this skill's folder: the folder this file is in. Where a command below still shows a `${...}` name instead of a real path, put the folder's absolute path there, with forward slashes. Needs git and Node.js 18 or newer. `gh` is optional.

The request can carry arguments: a base branch, `--since last`, `--session`, `resume` or `push`. In Claude Code the user types them after `/reflektor`, in Codex after `$reflektor`; with another agent they say them in words. For `resume`, or when the user asks to continue or pick up a review, go to "Pick up a review" at the end and skip the other steps. For `push`, or when the user asks to push, publish or upload the report to Reflektor, go to "Publish to Reflektor" and skip the other steps.

## 1. Pick the base branch and scope

Base branch, first match wins:

1. A branch the user passed as an argument, or named in this conversation as the PR target.
2. Otherwise leave `--base` out. collect.mjs then tries the open PR for this branch (through `gh`), then `base` in `.reflektor.json`, then the remote's default branch, then a common name (main, master, develop, staging, demo, trunk), and last the branch this one most recently forked from. When it prints `(guess)`, name the base in your message to the user, so they can correct it with `/reflektor <branch>` (in Codex, `$reflektor <branch>`).

Scope:

- **Default:** the whole branch since the merge base, plus uncommitted and untracked files. This matches what reviewers will see.
- **`--since last`:** only changes since the previous report, when the user asks for a report about just those. After fixing review comments, use `--update` instead (step 8.5): it shows the whole branch and marks what changed. A `--since` or `--files` report does not update `pr-description.md`.
- **`--files a,b,c`:** only these files. Use it when the user asks for this session's changes (argument `--session`): pass the files you created or edited in this conversation. If the branch also holds large unrelated earlier work and the user asks about "recent" changes, ask whether they want the whole branch or only this session's files.
- **`--no-uncommitted`:** committed work only, when the user asks for it.

## 2. Find or make coverage

Coverage is optional, but try to get it.

1. `coverage.files` in `.reflektor.json`. collect.mjs reads these itself.
2. A coverage file already in the repo: `lcov.info`, `coverage.xml`, `cobertura.xml`, `coverage.out`, `cover.out`, `jacoco.xml`, `clover.xml`, or a coverage.py `coverage.json`. Look in the repo root, `coverage/` folders and package folders. Skip `node_modules`, `vendor` and build output. collect.mjs prints which file it used and marks it STALE when it is older than the latest change; then try step 3 for a fresh one.
3. Get a fresh one from the test run in step 2b. Use `coverage.command` from `.reflektor.json` as the test command if it is set. Otherwise add a coverage flag to the project's own test command:

| Stack | Command that writes a supported file |
|---|---|
| Vitest | `npx vitest run --coverage --coverage.reporter=lcov` |
| Jest | `npx jest --coverage --coverageReporters=lcov` |
| pytest | `pytest --cov --cov-report=xml` (needs pytest-cov) |
| coverage.py | `coverage run -m pytest && coverage json` |
| Go | `go test ./... -coverprofile=coverage.out` |
| Rust | `cargo llvm-cov --lcov --output-path lcov.info` (needs cargo-llvm-cov) |
| Gradle / Maven | `./gradlew test jacocoTestReport` / `mvn test jacoco:report` (when JaCoCo is set up) |
| .NET | `dotnet test --collect:"XPlat Code Coverage"` (writes Cobertura XML) |
| PHP | `vendor/bin/phpunit --coverage-clover clover.xml` |

Rules:

- Never install packages, add plugins or change project config to get coverage. If the tool is missing, skip coverage and say so in one line.
- Ask first if the tests need services you would have to start (a database, Docker), or look like they take more than about 5 minutes.
- In a monorepo, run only the packages that changed.
- If tests fail but a coverage file was written, use it and add the failing tests to `beforeMerge`.
- Pass each file with `--coverage <file>`.

## 2b. Start the project's checks in the background

Start the project's own lint, typecheck and test commands now, so the report shows what passes. They run while you collect and read the change; do not wait for them.

First ask which checks this repo has:

```bash
node "${CLAUDE_SKILL_DIR}/scripts/checks.mjs" --repo . --plan
```

It prints the commands and where they come from: `checks` in `.reflektor.json` (shared with the team), or the ones saved for this repo in `~/.reflektor/repos/` from an earlier report. It also lists checks it skips because nothing they cover changed.

**When it lists commands and says to start them,** start them as a background process, so you can go on while they run (in Claude Code: the Bash tool with `run_in_background`):

```bash
node "${CLAUDE_SKILL_DIR}/scripts/checks.mjs" --repo .
```

**When it says to ask the user first,** the branch has commits by someone else, such as a teammate's PR, and the checks would run their code. Ask in one line, naming the authors it lists. On a yes, add `--trust` to the background command; it remembers those authors for this repo. On a no, skip the checks and say so in the report's testing gaps.

**When it says there are none yet, or that the saved ones are out of date or could not run,** work them out once and save them, then start them as above:

1. Read the CI config first (`.github/workflows/*.yml`, `.gitlab-ci.yml`, `Jenkinsfile`, `.circleci/config.yml`, and so on): its lint, typecheck and test commands are the ones the team already trusts. Without CI config, use the project's own files: package.json scripts, Makefile targets, `go vet ./...` and `go test ./...`, `cargo clippy` and `cargo test`, `ruff check`, `mypy` and `pytest`, and so on.
2. Give the test command the coverage flag from step 2, so one run gives both the result and the coverage file.
3. In a monorepo, make one check per package, limited to its folder with `--when`, so a report only runs the packages it changed.
4. Never install anything, and ask first if a command needs services or looks slow.
5. Write them for bash, the same as the commands you run yourself. On Windows they run in Git Bash.
6. Save them, naming the files they came from so a later change to those files marks them out of date:

```bash
node "${CLAUDE_SKILL_DIR}/scripts/checks.mjs" --repo . --save --source "<where they came from, in a few words>" --from <file>... \
  --run "lint=<command>" --run "typecheck=<command>" --run "tests=<command>" [--when "tests=apps/api/**,packages/shared/**"]
```

In your final message, list the checks you saved, and say that `checks.mjs --forget` deletes them and `checks.mjs --share` copies them into `.reflektor.json` for the team. Do not ask before saving; the report should not wait. (Asking about other authors' code, above, is the one time to wait.)

`--run` on the background command overrides everything, for a one-off run. The run writes `checks.json` next to diff.json as it goes, and the review page shows each result as it arrives; step 7b updates the report when the checks end. If you cannot run a background process, run it in the foreground and wait.

## 3. Collect

```bash
node "${CLAUDE_SKILL_DIR}/scripts/collect.mjs" --repo . [--base <branch>] [--since last] [--files a,b] [--coverage <file>]...
```

It writes diff.json into the repo's git folder and prints:

- **Diff file** and **Report file**: the paths to use in steps 5 and 6. Always use these printed paths. In a git worktree the git folder is not `.git/`.
- the base branch, commits and patch coverage
- the `git diff` command to read the changes
- a table of changed files with their target (from `.reflektor.json`) and flags (generated, uncommitted, untracked)

It also prints **Safety checks**: fixed rules that flag likely secrets (key formats, passwords in code, committed `.env` or key files) and risky migrations (dropped tables or columns, NOT NULL without a default, renames, type changes, writes without WHERE, indexes that lock a table). Rollback code is not checked: a migration's down section or down file runs only on a rollback. Secret values are masked.

When the reader has turned on Subagentic Mode in Settings, it also prints `Subagent mode: on` and the path of a file. Read that file before step 4 and follow it.

When the reader has turned on Screenshots in Settings and the change touches UI files, it also prints `Screenshots: on` and the path of a file. Read it and start the screenshots subagent it describes before step 4. It runs in the background; do not wait for it.

Exit code 3 means there are no changes: tell the user and stop.

Lines starting with `Hook preRun` come from the project's own hook (`hooks` in `.reflektor.json`), and what it prints is for you, such as a ticket's text. When it fails, collect exits 1: tell the user what the hook printed and stop. Do not work around a hook.

While the tests from step 2b run, their coverage file may be missing or STALE. That is expected: step 7b collects again once they are done.

collect.mjs fetches the base branch first. If the fetch fails, it warns and uses the local copy; tell the user. Pass `--no-fetch` to skip fetching, for example when offline.

Do not read diff.json. It holds full file contents. Read the changes with the printed `git diff` command, file by file, and read untracked files directly.

## 3b. Open the page while you read

Publish the facts now, so the user can read the diffs and watch the checks while you write the report:

```bash
node "${CLAUDE_SKILL_DIR}/scripts/build.mjs" --diff <diff file> --draft
node "${CLAUDE_SKILL_DIR}/scripts/review.mjs" open --report <json file from build> --open
```

The page names the agent it talks to. `review.mjs` and `build.mjs` work that out from the shell they run in, so there is normally nothing to do. If `review.mjs open` prints a `note:` line saying the page does not know which agent you are, add `--agent-name "<the product you are running in>"` to every `review.mjs` command from then on.

After `collect --update` in a later round, add `--report <report file>` to the build, so the draft shows the carried report. The page says you are still writing the notes and holds back sending until the real report replaces it. Do not start the waiter yet, and say nothing to the user until step 7.

## 4. Understand the change

Before writing, find out:

- **Why** the change was made: this conversation, commit messages, the PR title if there is one, and anything a preRun hook printed.
- **What** each changed file does now, and what it did before.
- **Who else is affected:** search the repo for changed functions, routes, types and tables. Callers outside the diff become `affected` highlights.
- **What can break:** migrations, contract changes (API, database schema, public types, events), env vars, deploy order, concurrency, error handling, security (auth checks, input validation, secrets).
- **What is not tested.**
- **The safety checks:** every high or medium finding must appear in the report as a `risk` highlight with a `ref` to its line and a `fix`. A secret also gets a `beforeMerge` item: remove it, rotate it, and load it from the environment. A false positive still gets a highlight that says why it is safe. Never copy a secret value into report text.

For large changes (more than about 60 files or 3000 changed lines), read must-review files fully and skim the rest. Say in the summary that the report focuses on the most important parts.

## 5. Write report.json

Write report.json to the **Report file** path that collect printed. Its shape is `Report` in `${CLAUDE_SKILL_DIR}/schema/types.ts`; read that file first. The allowed values for every field are the string unions in it. Write all text by `${CLAUDE_SKILL_DIR}/style-guide.md`; read it too.

**Header**

- `tag`: HOTFIX only when this conversation says it is urgent (outage, data loss, broken production). SECURITY when it fixes a vulnerability. FEATURE for a new capability, FIX for a bug, PERF for speed, REFACTOR when behavior does not change, CHORE for dependencies, config or docs only.
- `title`: plain verb phrase plus a technical anchor in brackets, under 90 characters, without the tag. Example: `Stop double charges when users click Pay twice (idempotency key on POST /payments)`.
- `summary`: at most two sentences: what users or callers get, and the main technical change.
- `targets`: every area touched. Use the target column from collect when it is filled; otherwise judge by path and content. Lockfiles, generated files and root config files add no target on their own.
- `reviewMinutes`: write 0. build fills it in: the words in the must-read sections at 200 a minute, plus 1 minute, plus 1 minute per flow.

**beforeMerge:** what must happen before or at merge: migrations, env vars, deploy order, feature flags, breaking changes, uncommitted files, anything that will fail CI. At most 6 items. When an item covers several files, name them in the text and point `ref` at the main one. Empty when there is nothing.

**sections**

- Default order: database, infrastructure, config, dependencies, backend, frontend, cicd, tests, refactors, generated, other. Move a section up when it carries more risk than its place suggests. Leave out empty sections.
- Every changed file goes in exactly one section. Lockfiles and generated files go in `generated` with review `skip`.
- Sections group files by kind of change, not by area, so a file's section can differ from its target. A package manifest goes in `dependencies` and an env example file goes in `config`, even when their target is backend.
- `review`: `must` for anything that can break production, data, CI or everyone's local setup, `skim` for normal changes, `skip` for generated or trivial files. `reason`: one line.
- `highlights`: at most 5 per section, most important first. Add a `ref` whenever a highlight is about specific code. Kinds:
  - `behavior`: what works differently now, for users or callers
  - `risk`: what can break, and where
  - `contract`: a changed API, schema, public type or event payload
  - `decision`: why this approach, only when it is not obvious
  - `gap`: unhandled cases, missing pieces, leftover TODOs
  - `affected`: unchanged code that this change affects
- `fix`: give every `risk` and `gap` a suggested fix: the change you would make, in one sentence or a short list. The page shows it next to a "Fix this" button, so a click means "do exactly this".
- `questions`: decisions the author must make before opening the PR. Leave empty when there are none.
- `files`: one entry per file. `note` is 1 to 4 short sentences or a short list: what changed and why. Add `lineNotes` (at most 3 per file) only for lines a reader could misread or that carry a risk. Generated files get a one-line note.

**flows:** add a flow when the change adds or changes an entry point: an HTTP route, UI action, job, queue consumer, webhook or CLI command. Otherwise leave it empty.

- `trigger`: what starts it, in plain words.
- `steps`: in call order, from the trigger to storage or the final side effect. Include existing steps where the new code plugs in, with status `existing`.
- `symbol`: the real function, component, table or route, like `BookService.createBook` or `POST /books`. The build looks for the last word of it (`createBook`, `/books`) anywhere in the referenced file and marks the step "unverified" when it is missing.
- Include middleware or error handlers only when the change relies on them.
- `details`: the checks (validation, auth), rules (business logic), effects (writes, events, cache) and errors (wrong status codes, races) at that step. Give every `error` detail a `fix`, like risks.

**schema:** when the change touches the database (migrations, ORM models, schema files), describe the tables so the page can draw them.

- Every new, changed or removed table, with all its columns and a `status` per column.
- Existing tables that a new relation points to, with only the columns involved.
- `references: "table.column"` on columns that point to another table. Add `enforced: false` when there is no real foreign key in the database.
- Keep `note` to a few words, like "NOT NULL, no default".

**contracts:** the types, interfaces, enums and constants that the change adds, changes or removes, so the reviewer sees the shapes other code depends on in one place. Leave it out when there are none.

- Include exported ones and any that other files, the API, the database or the UI depend on. Leave out local helper types.
- `kind`: `type` for type aliases, structs, classes and records; `interface`; `enum` (including union types of fixed values); `constant` for exported constants and limits that change behavior.
- `name` exactly as in the code; `ref` points at its definition (the old line when removed). The build drops any name it cannot find in that file.
- `members`: for a new one, every field or value; for a changed one, only what changed (`added`, `removed`, or `changed` with the old type in `was`). Give `type` as written in the code.
- Constants: `value`, and `was` when it changed.
- `note`: one sentence on what it is for or what breaks, such as two copies of the same type that can drift apart, or a removed field that callers still read.
- Generated files are marked by the build. A change there usually comes from a schema or spec; say which one in `note`.

**plan:** when this conversation had a plan, check the diff against it. A plan is a plan the user approved (such as one from plan mode), a task list you kept, a numbered list the user gave or agreed to, or a ticket the user pasted. Without one, leave `plan` out.

- `source`: one line on where the plan came from, like "Plan approved in this session".
- `items`: every planned item with `status` `done` (with a `ref` to where it happens), `partial` (say what is left in `note`) or `missing`. Then add `extra` items for notable changes the plan did not ask for, so the user can catch scope creep. Leave out small supporting changes.
- Missing and partial items show "Finish it" and "Not needed" buttons. In the fix loop, a `fix` comment on one means: finish it.

**testing.gaps:** behavior no test checks, most important first, at most 5. When collect printed per-file coverage (tested lines and untested line numbers), use it.

Line numbers refer to the new version of a file. Use `"side": "old"` only for deleted lines.

## 6. Build

```bash
node "${CLAUDE_SKILL_DIR}/scripts/build.mjs" --diff <diff file> --report <report file>
```

It writes the report data, `<branch>-<sha>-r<round>.json`, next to the report file and records the run for `--since last`. Fix every `warning:` line by editing report.json and building again, at most two rounds. Mention anything left. `note:` lines need no report change (for example a stale coverage file, or project checks still running), but tell the user when they matter. Build without waiting for the checks.

## 7. Open it for review

Publish the report to the reflektor daemon. It is one local server for every review on this machine (`http://127.0.0.1:7337`, with an inbox of all reviews at `/`), and `review.mjs` starts it when it is not running. It replaces the draft from step 3b in the open tab:

```bash
node "${CLAUDE_SKILL_DIR}/scripts/review.mjs" open --report <json file from build> --open
```

It prints the review address and the review id, and opens the browser unless a tab already shows this review (open tabs get a banner for each new round instead). Then start the waiter. Run it as a background process when its exit wakes you (in Claude Code: the Bash tool with `run_in_background`). Some agents, Codex among them, are not woken when a background process ends: they only see its output when the user writes next. There, tell the user the lines below first, then run the waiter in the foreground with the longest time limit your tool allows. If it stops at the time limit with nothing to report, run it again.

```bash
node "${CLAUDE_SKILL_DIR}/scripts/review.mjs" wait --id <review id>
```

Tell the user, in a few lines:

- the title, how many files are must-read, and the top one or two risks
- that they can comment (hover a line number and click +), use "Fix this" or "It's fine" on problems, answer the questions, ask you live with the "Ask ... now" button, and send the review with the button at the bottom of the page when done

Do not paste the report into the chat. Do not poll: the waiter exits when the reviewer does something. With a background waiter, end your turn, and its exit wakes you. Its output says what happened and what to run next. After handling it, start the waiter again the same way, unless the review is done.

**reflektor was updated:** the user can update reflektor from the page while you wait. The waiter then prints that reflektor was updated and exits with code 3. Tell the user that line, and do not start the waiter again from this session: they continue with `/reflektor resume` (in Codex, `$reflektor resume`), which runs the new version.

**An update is out:** while a newer reflektor is out, `review.mjs` ends some answers with a line starting `note: reflektor`. Pass it on to the user once per session, in one sentence, and do not update on your own: the user updates from the report's menu, or asks you to run `review.mjs update`.

**A live question:** read the code it points at and answer in 1 to 4 short sentences or a short list, following the style guide. Answer only: do not change code. If the answer shows something should change, say so and suggest a comment or "Fix this".

```bash
node "${CLAUDE_SKILL_DIR}/scripts/review.mjs" answer --id <review id> --question <question id> --text "<answer>" [--ref path:line]
```

**A sent review:** go to the fix loop. **A review sent with no comments:** the review is done. The waiter says whether the project's onApproved hook ran; if not, offer to open the PR (step 9).

**A request for an updated report:** the page tells the reviewer when the code changed after the report was built, and offers to ask you for an update. Run collect.mjs with `--update`, fix the report for the files the waiter names, build, and publish: it stays the same round, and the reviewer's comments stay.

If you cannot run a background process, run build.mjs with `--open` instead. It writes one self-contained HTML page and opens it. The page then shows a "Copy for ..." button, and the user pastes the comments into the chat. When the user wants a file to keep, pass `--html <file>` to build.mjs.

## 7b. When the checks end

When the background checks from step 2b exit (you are notified; with a foreground waiter, look each time it returns), the page already shows their results. Update the report with what they found:

1. If the tests wrote a coverage file, run collect.mjs again with `--update` and the same `--base` and `--coverage` arguments, for the fresh coverage. `--update` keeps report.json and moves its line references if code changed.
2. In report.json, add a `beforeMerge` item for each failed check (its name and first error), and update the test gaps and `gap` highlights from the new coverage.
3. Build and publish again with `review.mjs open --report <new json>`. It is the same round, so comments and progress stay, and open pages reload it in place.

Skip this when the reviewer already sent the round: the next round includes the results. If you cannot get notified, check with `checks.mjs --repo . --wait` before you end your turn.

## 8. Fix loop

The reviewer follows along in the page: your plan and your progress on each comment show up live.

1. **Read the review file** the waiter named. Its shape is `Review` in schema/types.ts. Each comment's `target` says what it is about: a line range (with the code), a file, a highlight (with its suggested fix), a question, a plan item, a flow problem, a before-merge item, a screenshot, or the whole report.

   **A screenshot comment** is about what the reviewer saw on screen:
   - `file` is the picture, relative to the review file's folder. Look at it with your file reading tool before you plan. Pictures are taken at twice a 1280 by 800 window, so 2 pixels in the picture are 1 CSS pixel.
   - `pin`, when there is one, is where they clicked, as fractions of the picture's width and height from its top left (`{ "x": 0.42, "y": 0.18 }` is 42% across and 18% down). Without one, the comment is about the whole picture. A pin is approximate: read the comment first, then use the pin to choose between the elements near it.
   - `screenshots.json`, next to the review file, has the shot: `set` matches a set's `id` and `shot` a shot's `id`. Its `refs` point at the changed markup; follow it to where it is styled, even in a file the branch does not change.
   - When a comment names something the project does not have, such as an accent color with no color defined, pick a value and say so in the plan step, or make it a `question` when the choice matters.
   - After fixing, the next round takes the screenshots again, so the reviewer sees the result.
2. **Work out the kind** of every comment that has none:
   - `question`: asks why, what or whether, or starts with `q:`. Answer it; no code change.
   - `fix`: asks for a change.
   - `nit`: starts with `nit:`, or is optional or cosmetic. Fix it if it is cheap.
   Split a comment that mixes kinds into separate steps. Kinds set by buttons are final: `fix` with empty text means "do the suggested fix", `accepted` means the reviewer accepts the risk (no change, and do not flag it again in later reports), `decision` is the reviewer's answer to a report question (apply it).
3. **Post the plan** and wait for the decision. Write a plan file, then:

   ```bash
   node "${CLAUDE_SKILL_DIR}/scripts/review.mjs" plan --id <review id> --file <plan.json>
   ```

   The file: `{ "steps": [{ "comments": ["<comment id>"], "where": "book.service.ts:19", "kind": "fix" | "question" | "nit", "action": "<what you will do>" }], "note": "<optional>" }`. Every comment belongs to at least one step. Start the waiter again. The reviewer approves in the page (and can change a step's kind or skip it) or asks for a new plan. If the user approves in the chat instead, go ahead.

   When no comment needs a code change (every comment is `accepted`, or a question you can answer), skip the plan and go straight to step 4.
4. **Make the changes,** reporting each comment as you go:

   ```bash
   node "${CLAUDE_SKILL_DIR}/scripts/review.mjs" status --id <review id> --comment <comment id> --status working|fixed|answered|wontfix|noted --text "<one line>" [--ref path:line]
   ```

   Mark a comment `working` when you start it and give the final status when done. If you think a requested fix is wrong, do not make it; use `wontfix` and say why.

   When every comment has a final status and none is `fixed`, no code changed: the daemon ends the review, and the last `status` call says so. A running waiter exits with the same news and runs the onApproved hook, as above. Skip steps 5 and 6 and offer to open the PR (step 9) if the hook did not.
5. **Rebuild for the next round.** Every round shows the whole branch, so the reviewer approves what will be merged; the page can also show only what changed since the round they sent.

   ```bash
   node "${CLAUDE_SKILL_DIR}/scripts/collect.mjs" --repo . --update [--base <branch>] [--coverage <file>]...
   ```

   It collects the whole branch again, plus what changed since the round the reviewer sent, and carries report.json forward: its line references move to where those lines are now. Update that report.json; do not write a new one:
   - Read the changes since that round with the `git diff` command it prints.
   - Fix what it lists: references on lines that changed, files new to the branch (add them to a section), and files no longer in it (remove them).
   - Rewrite the notes, highlights, flows and contracts the fixes made wrong, and the title or summary if the change itself changed. Leave the rest as it is.
   - Set `review: { round, replies }`: `round` is the round you answered, and every comment gets one reply with the same status and text as above (`fixed` with a `ref` to the new code, `answered`, `wontfix` with the reason, `noted` for `accepted` comments and nits you skipped).
   - Leave `refsAt` as it is; collect uses it to move the references again next time.
6. **Build and publish** with `review.mjs open` (steps 6 and 7) and start the waiter again. Open tabs show "Round N is ready". Repeat until the reviewer sends a round with no comments.

## 9. Open the PR

build.mjs also writes `pr-description.md` next to the report: the first line is the title, the rest is the Markdown body. Only whole-branch builds write it, so it always describes the whole PR. When the user asks to open the PR, or the review ends with no comments and the user wants a PR:

1. Ask first: opening a PR is visible to others.
2. Use the repo's own tool: `gh pr create --title "<title>" --body-file <body file>` for GitHub, `glab mr create --title "<title>" --description "$(cat <body file>)"` for GitLab. Write the body without the title line to a temporary file first.
3. On GitHub, tell the review page right after `gh pr create`, with the URL it printed:

   ```bash
   node "${CLAUDE_SKILL_DIR}/scripts/review.mjs" pr --id <review id> --url <pull request url>
   ```

   The page then shows the pull request and follows it: when it is merged or closed on GitHub, the open page and the inbox say so without a new report. Skip this when the review was not opened through `review.mjs`.
4. Without a CLI for the host, give the user the file path; the report page also has a "PR description" button with copy buttons.

## Pick up a review

A review outlives the session that made it: when no session listens for it, the page tells the user how to pick it up: `/reflektor resume` in Claude Code, `$reflektor resume` in Codex, or asking the agent to resume the reflektor review. In the repo of the review:

```bash
node "${CLAUDE_SKILL_DIR}/scripts/review.mjs" resume --repo .
```

It finds this branch's review (or pass `--id`) and prints what waits for you, the same way the waiter does: a sent review, a plan decision, a question, or a fix loop that was cut off, with the comments still open. Follow it from there; for a cut-off fix loop, comments that already have a final status are done. When nothing waits for you, it says to start the waiter.

## Publish to Reflektor

Reflektor is where the user's organization reads published reports. When the user asks to publish or share the report there, or passes `push` (for example because the daemon's own publish failed or never ran):

```bash
node "${CLAUDE_SKILL_DIR}/scripts/review.mjs" publish [--org <slug>]
```

It publishes this branch's newest finished round and prints where it went, or why it did not. Tell the user the outcome in one or two lines, with the link when there is one:

- **Already up:** a round that went up before answers with its link and is not sent again. Say so; nothing else to do.
- **Several organizations:** ask the user which one and run it again with `--org`.
- **Not signed in:** run `review.mjs login` in the background and tell the user to approve the code it prints in the browser tab it opens, then publish again.
- **No review for this branch, or only a draft:** say there is no finished report to push yet, and offer to build one (the steps above).
- **No remote:** the report was collected before the repo had a remote naming its host and owner. Ask the user to add one (or for its URL, and add it), then collect, build and open the report again (step 8.5 with `--update`, or from step 3 when there is no review) and publish that round. Adding the remote alone does not change a report already collected.
- **Repository not approved:** nothing was uploaded; an admin of the organization has to approve the repository on Reflektor first.
- **Network or server error:** say what it printed. Pushing again later is safe.

A pushed round carries the pull request it was built with. When the branch's pull request opened after the newest round was built, the push still works, but Reflektor cannot tie that round to the pull request. Say so, and offer an updated report (step 8.5): its new round records the pull request and the daemon publishes it.

While the branch's pull request is open, the daemon publishes each new round by itself once the user is signed in; `push` is for when that did not happen.

## Follow-ups

- **Wording or grouping changes:** edit report.json and run build.mjs again. No need to collect again.
- **After code changes:** run collect.mjs with `--update`, update the carried report.json for what changed, build, and publish again. Use `--since last` only when the user wants a report about just the new changes.
- **"Viewer not found" from build.mjs:** tell the user to run `pnpm build`, then `pnpm run deploy`, in the reflektor repo.

## Repo config (optional)

`.reflektor.json` in the repo root, read by the scripts:

```json
{
  "base": "develop",
  "targets": {
    "backend": ["services/**", "packages/server/**"],
    "frontend": ["apps/web/**"],
    "database": ["**/migrations/**"],
    "infrastructure": ["infra/**", "Dockerfile", "*.tf"],
    "cicd": [".github/**", ".gitlab-ci.yml"]
  },
  "generated": ["**/__generated__/**"],
  "coverage": { "command": "make test-coverage", "files": ["coverage/lcov.info"] },
  "checks": [
    { "name": "lint", "command": "pnpm lint" },
    { "name": "api tests", "command": "pnpm -C services/api test --coverage", "when": ["services/api/**"], "timeout": 900 }
  ],
  "hooks": { "preRun": "pnpm codegen", "onApproved": "node tools/open-pr.mjs" }
}
```

`checks` here come before the ones saved in `~/.reflektor/repos/`; `checks.mjs --share` writes the saved ones here. `when` limits a check to changes in those paths.

`screenshots` says where the app answers (`url`), how to start it when it does not (`start`, waited for `readySeconds`), and any hosts besides localhost the browser may open (`hosts`). `screenshots.mjs --share` writes the saved one here.

`hooks` are the team's commands at fixed points, and the scripts run them: `preRun` before collect fetches (a failure stops it), `postRun` when a round's report is first published, `onApproved` when the reviewer finishes with nothing to fix. Screenshots add four: `preScreenshots` before the first shot (to seed test data and sign a test user in), then `onScreenshotsPassed` or `onScreenshotsFailed`, then `postScreenshots`. Like the checks, they do not run while the branch has commits by authors the user has not trusted (`checks.mjs --trust`). When the user asks you to write one, the top of `${CLAUDE_SKILL_DIR}/scripts/hooks.mjs` lists what each hook is handed.

Globs follow .gitignore rules: a pattern without `/` matches at any depth. When the user asks for one, write it from the repo's real folder layout.
