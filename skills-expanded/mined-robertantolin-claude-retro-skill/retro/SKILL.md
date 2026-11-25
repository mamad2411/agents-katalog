---
name: retro
description: Use at the end of any working session, or when the user asks for a retrospective, lessons learned, or a post-mortem of what went wrong this session.
license: MIT
metadata:
  author: Robert Antolin
  source: https://github.com/robertantolin/claude-retro-skill
---

Run a retrospective on THIS session. Plain language, full sentences, no tool names where a plain description exists. The retro proposes and asks; it applies only what the user approves or has set to approve-always. It never writes a TSV or JSON file directly; every state change goes through the commands below.

Paths: skill folder `~/.claude/skills/retro/`, data folder `~/.claude/retro/`. Run every command with `python` from the skill folder, one command per tool call, exactly as written here: a command wrapped in `python -c`, a heredoc or a shell function trips project hooks and loses the step. `<project>` is this project's memory folder name under `~/.claude/projects/` (the transcript's parent folder name). `<transcript>` is `~/.claude/projects/<project>/${CLAUDE_SESSION_ID}.jsonl`, this session's file; when that name holds no session id or no such file exists, it is the newest `.jsonl` in that folder whose contents match this session.

## 0. Prepare

1. `python settings.py show`. It prints JSON with the keys `approve_always`, `raised_bar`, `first_run_done`, `history_scan` and `session_budget_chars`. A missing settings file is not an error; the command prints the defaults. When `"first_run_done"` is `false`, this is the first run: do step 0a before continuing.
2. `python journal.py begin --project <project>` and keep the first printed line, the run id, as `<run>`.
3. `python scan.py --session <transcript>` and keep its JSON. The command can instead exit 1 with an `error` in its JSON, and two of those errors are normal. `history scan in progress; session scan skipped` means a background scan of your history holds the lock; `cannot read transcript: ...` means this session's file could not be read, and only after the command, run once more on the newest `.jsonl` in that folder whose contents match this session, fails the same way. On either one, say so in one line, continue the retro from your own memory of the session, and set the Housekeeping "Session scan" row to `skipped, history scan running` for the first and `failed` for the second.
4. `python health.py --store <project>` and keep the output for Housekeeping.
5. `python ledger.py pending --project <project>` and `python ledger.py recent --project <project>`. Pending rows are proposals from an earlier retro that got no decision; recent rows are what other sessions raised in the last 24 hours. Then `python ledger.py criteria`: any lines it prints are the user's own list of what a proposal worth raising looks like, and step 2 reads them; it prints nothing when no list is kept.
6. `python scan.py --open <project>`. Its `Open findings` block is the list step 2 reads; its `Dormant lessons` block goes to the store review (step 4a).
7. `python journal.py ask` and keep its line, `ask: boxes` or `ask: print`: it says how this run can ask for decisions, and step 4 reads it.

### 0a. First run

Run `python settings.py init`. Then ask ONE question with the question tool, header "History scan", text: "The retro can scan your past sessions once. Benefit: corrections you have already made become findings on day one, lessons that have gone quiet are flagged, and pattern spotting starts from your history instead of from zero. It reads the transcripts on this machine within the range you pick and sends the model your own messages, the last 600 characters of the Claude reply before each one, the one-line titles of your existing lessons, global instruction bullets, rules files and skills, the instruction bullets, rules files and skills of each session's own project, and, for a history scan, the text of past retro replies. It never sends tool output or the contents of your files. Which range?" Options: "Last 90 days (Recommended)", "Everything", "Skip". Then:
- Last 90 days: `python settings.py set-history <date>` where `<date>` is today minus 90 days in `YYYY-MM-DD`.
- Everything: `python settings.py set-history everything`.
- Skip: `python settings.py set-history skip`.

Then `python settings.py mark-first-run` and continue with step 0.2.

Start the history scan only after step 0.6, never here: it holds a lock for as long as it runs, and a session scan that starts while the lock is held is skipped. For Last 90 days run `python scan.py --since <that same date> --background`; for Everything run `python scan.py --background` with no `--since`; for Skip run nothing.

## 1. Session review

Three bullets, from the session scan output plus your own context. The scan's corrections are evidence; you may add context, and you may not drop a scan-reported correction without saying why.

- **Attempted:** what the session set out to do and whether it landed. Two sentences at most.
- **Corrected by you:** each correction in one sentence, quoting the user's words. "None" if none.
- **Rework:** artifacts redone or loops of three or more rounds, with the cause. "None" if none.

A slip you caught before the user saw it is not a correction and is not listed.

## 2. Findings

A finding is one of:
- A correction this session that qualifies: it reached the user wrong AND there is a concrete action that would have prevented it. "Be more careful" is not an action.
- A scan match: the session scan reported `match_key` with high or medium confidence and `predates` false. The lesson already exists and failed again.
- An open finding for this project or `global`, of type `recur` or `candidate`: every row in the `Open findings` block of the `scan.py --open` output from step 0.
- A candidate the scan marked `confirmed` or `hard`.

Nothing else is a finding: not a slip you caught before the user saw it, not a conflict you settled yourself, not a thing you merely noticed. A session with no correction and no confirmed candidate has no findings; it still gets the store review in step 4a when its store is over cap, and goes to step 6 when that raises nothing.

Print the table `# | Problem | Insight | Status`. Problem is what went wrong in plain words. Insight is what would prevent it. Status is `New. Proposal N.`, `Seen before. Proposal N.`, or `No action.` with the reason in Insight. `Seen before` means the scan reported a `match_key` for it or a `recent` row's title matches; a finding this scan created, a candidate included, is `New`. Every row with a proposal number gets exactly one proposal in step 4.

When `ledger.py pending` returned rows, put them on one line under the table: "Undecided from a previous retro: <title>; <title>" (when the proposal file is gone, show the finding id instead). Then ask as step 2a says.
- Raise them: each pending row becomes a proposal in this run's numbered list, still inside the limit of three.
- Drop them: for each row, `python ledger.py append --run-id <run> --project <project> --proposal <N from the row> --finding-id <F-id or none> --kind <kind from the row> --decision none --refine-count 0 --applied n` (decision `none`, not `deny`, so dropping stale rows never raises the bar for that kind), and when the row carries a finding id also `python scan.py --resolve <F-id> --status denied --reason "dropped from pending"`.

Then, before choosing any proposal:
- Recurrence: pick the lesson's three most distinctive content words and run `python recur.py --project-dir <this session's working directory> --words <w1> <w2> <w3>`. It searches each word separately across `~/.claude/projects/*/memory/`, `~/.claude/CLAUDE.md`, `~/.claude/rules/` and that folder's CLAUDE.md, `.claude/rules/` and `.claude/skills/*/SKILL.md`, and prints every file that holds two of the three words, or `none`. A printed file means the lesson exists: the proposal is a mechanism (rule, hook, script) or "No action", never a second copy. Either way the Insight names the mechanism you weighed, so a "No action" row says which rule, hook or script you considered and why it would not hold.
- Duplicate check: if a `recent` row's title matches, cite it in Status instead of raising the proposal again.
- Raised bar: `settings.py show` lists `raised_bar` per project. A kind listed under this project, or under `*`, is not proposed. Record it instead with `python candidates.py log --project <project> --category <category> --key "<key>" --summary "<one line>"`, where `<category>` is one of `repeat-manual`, `revisited`, `rework-loop`, `tool-friction` or `time-sink` and any other value is refused as a bad argument. Say in Status that the bar is raised for that kind, so the point was noted rather than proposed. This is the only place the retro logs a candidate itself.
- Criteria: when `ledger.py criteria` printed lines at step 0, hold each proposal that comes from this session's findings against them. A proposal that fails a line is not proposed: its Status is `No action.` and its Insight quotes the line it failed; when the finding has an id, resolve it as `resolved:noted` with that line as the reason. A lesson that exists and failed again does not handle the problem, so the mechanism of the Recurrence bullet is still weighed and named. Proposals of steps 4a and 4b and of a typed request are not held against the lines.

At most three proposals per retro. Prefer the one with the strongest evidence.

### 2a. Undecided proposals

When the line step 0.7 kept reads `ask: boxes`, first run the recurrence, duplicate and raised-bar checks that follow the Raise and Drop bullets, so the table is final, then end the message after the undecided line with the question in plain words: raise them in this retro or drop them, the answer you recommend and why, and an example answer such as "drop them". The user types the answer. On their reply, act on it as Raise them or Drop them in step 2 says, then continue at step 3 in a new message that picks up where the first one stopped: Candidates, the cards and the reply line.

When it reads `ask: print`, nobody can reply: ask nothing, leave the rows undecided, and continue from the recurrence check in step 2.

## 3. Candidates

Print "Candidates logged, not yet confirmed" with one line per scan candidate that is neither confirmed nor hard: what was observed, and what it would become if it repeats. Omit the section when there are none. Apart from the raised-bar case in step 2, do not log candidates yourself; the scan did it.

## 4. Proposals

For each proposal N, decide its kind:

| Kind | Target |
|---|---|
| `store-write` | Add or edit a lesson file in `~/.claude/projects/<project>/memory/`, plus its MEMORY.md line |
| `store-delete` | Remove a lesson file that evidence shows is wrong |
| `global-line` | A line in `~/.claude/CLAUDE.md` |
| `rule-skill-hook` | A `.claude/rules/`, `.claude/skills/` or `.claude/agents/` file, a hook file, or `settings.json` |
| `other-file` | Any other path |

Never propose adding a lesson or rule to a project's `CLAUDE.md` (it is loaded every session and kept under 200 lines). A project-scoped rule goes to a `.claude/rules/` file (`rule-skill-hook`) or the project memory store (`store-write`). A proposal may still shorten or correct an existing project `CLAUDE.md` line as `other-file`.

Write the exact edit as a unified diff to `~/.claude/retro/proposals/<run>/N.diff` and the card's bullets to `~/.claude/retro/proposals/<run>/N.md`, whose first line is `# Proposal N of M: <imperative title>`. Once every proposal's `N.diff` and `N.md` are written (those of steps 4a and 4b included), run `python files.py --run <run> --project-dir <this session's working directory>` and keep the line it prints, if it prints one.

Every edit, whatever its kind, carries no dates, commit hashes or narrative. Lesson entries are at most 120 words and follow the store's existing format. A lesson names the kind of situation it applies to and the action to take there: too general changes no behaviour ("be thorough"), too specific never fires again ("the fee rose to 250 on 1 January"). Machine-level or user-general lessons go to `global-line`, never a project store: a lesson that would hold just as well in a different project is global; one that stops making sense when the project changes stays in the project store. A store over cap (more than 20 entries on the health.py line for this project) gets a store review (step 4a), and a store-delete is raised only for a lesson that evidence shows is wrong. A `global-line` into Machine gotchas when that section has fewer than 35 free words (the `Machine gotchas:` line of health.py) shortens or removes an existing gotcha in the same diff so the section stays within 350 words, and What-changes names the line cut. A `global-line` anywhere else in `~/.claude/CLAUDE.md` names in What-changes the existing line it shortens or removes to pay for the words it adds, or says that none can go and why.

Print all M proposal cards in the report, one after another, directly after Candidates and before any question is asked. Each card:

**Proposal N of M: <title>**
- What changes: one or two sentences, naming the file in plain words.
- What you get: the behaviour that is different next time.
- Why you might say no: one sentence, written as step 4d says: an objection of a kind listed there, or exactly "No strong reason against." Every card carries this line.
- Exact edit: `<full path to N.diff>`
- Mechanism instead: on a `store-write` or `global-line` card only, one line naming the mechanism that would enforce the lesson, tried in this order: a skill, a script or command, a subagent, then a hook, rule file or gate; or "none fits" with the reason. A line of always-on text is the last resort, since every session pays for it. A line that names a skill, a script or command, a subagent, a hook or a gate is followed by the three comparison lines of step 4e.
- How it will be checked: on a `rule-skill-hook` card only, the check that will show the change works once it is applied, written as step 4c says.

Then, when at least one proposal needs a decision, read the line step 0.7 kept: `ask: boxes` or `ask: print`.

When it reads `ask: print`, this run has no question tool: append a ledger row with `--decision no-decision` for each proposal that needs a decision and apply each approve-always one as its bullet below says, then send one final message: the Session review, the Findings table, Candidates, the cards, the line "No decisions were recorded; the next retro in this project will offer these again.", then Housekeeping.

When it reads `ask: boxes`, end the message that holds the report and the cards with the line `files.py` printed, copied exactly as printed (when it printed one), then the line `Read the proposals above, then reply and the decision boxes open. Example answer: "go", or "deny 2: seen once, wait for a repeat"`. Nothing is applied yet: the question dialog hides the report while it is open, so the user reads the cards first. On the user's next message, ask for every decision in one call of the question tool: one question per proposal still undecided, all in the same call, in proposal order (the tool takes up to four questions and a retro has at most three proposals). Each question is short: header "Proposal N", text "Proposal N of M: <title>. Apply it?", and four options in this order: "Approve", "Deny: not worth a change", "Deny: already covered", "Deny: wrong fix". A card whose Mechanism-instead line says "none fits" names no mechanism: it keeps the four default options above, never "Approve the mechanism instead". A card whose Mechanism-instead line names a mechanism has the four options "Approve", "Approve the mechanism instead", "Deny: not worth a change", "Deny: already covered" (the tool takes four options, so a wrong-fix reason arrives as words under Other), and the description of "Approve the mechanism instead" names the mechanism in at most 30 words. Words typed under Other are a Refine. A reply that already decides a proposal (approve, a deny with its reason, or an edit instruction) is that proposal's answer, and it gets no question. A proposal whose kind is on approve-always (set only through "retro settings", never offered in the dialog) gets no question.

When every answer is in, act on the proposals in order:
- Approve: apply (step 5); `python ledger.py append --run-id <run> --project <project> --proposal N --finding-id <F-id or none> --kind <kind> --decision approve-once --refine-count <n> --applied y --verified <y|n|na>`. On a card that showed the comparison lines of step 4e, then `python ledger.py chose --run-id <run> --proposal N --option rule`.
- Approve the mechanism instead: rewrite the proposal as that mechanism, overwrite `N.diff` and `N.md`, and its kind becomes `rule-skill-hook`; apply (step 5) and append the Approve row with `--kind rule-skill-hook --refine-count <n + 1>`. On a card that showed the comparison lines of step 4e, then `python ledger.py chose --run-id <run> --proposal N --option mechanism`.
- A kind on approve-always: apply (step 5); the same ledger row with `--decision auto`; list it under Applied.
- Deny, any of the three: append `Denied: <the words after "Deny:", or the words typed under Other, or the reason given in the reply>` as the last line of `N.md`. Then the ledger row with `--decision deny --applied n`; `python scan.py --resolve <F-id> --status denied --reason "<that answer>"` when the finding has an id; for a candidate finding also `python candidates.py status --project <project> --category <c> --key "<key>" denied`. When the ledger command prints a `bar raised` line, repeat it to the user in plain words: this kind is now logged instead of proposed in this project until they say "retro settings".
- Refine, the words typed under Other: when they are an edit instruction, rewrite the proposal to it, overwrite `N.diff` and `N.md`, print the card again, increment the refine count, end the message with the same reply line, and after the user's reply ask about that proposal alone, with the same question shape and options. When they are a question or a remark, answer it in one or two sentences, print the card again unchanged, end the message with the same reply line, and after the user's reply ask about that proposal alone the same way, unless the reply already decides it; that counts as a refine too. When they are plainly a reason for saying no, they are a Deny with those words as the reason. The second answer is acted on like a first one.
- If the question tool is unavailable or errors: a ledger row with `--decision no-decision` for each proposal that needs a decision and apply each approve-always one as its bullet above says, then one final message: the Session review, the Findings table, Candidates, the cards, the line "No decisions were recorded; the next retro in this project will offer these again.", then Housekeeping.

Findings with `No action.` and an id: `python scan.py --resolve <F-id> --status resolved:noted --reason "<why>"` when the lesson or mechanism already exists. A candidate finding set aside only because you lack the details a mechanism needs gets `--status deferred:<what is missing>` instead, so its next sighting raises it again; `resolved:` closes it for good.

The only statuses `--resolve` accepts are `open`, `denied`, `no-decision`, and any status beginning `resolved:` or `deferred:`. Anything else is refused as a bad argument, so keep to the statuses named in this file.

A `python candidates.py status` call for a key the candidates file does not hold exits 1 and changes nothing. When that happens, say so in one line and carry on.

### 4a. Store review

When the health.py line shows this project's store over 20 entries and the findings leave a proposal slot free, run the review before writing any proposal file, in every run, including a run with no finding. Run `python ledger.py denied-review --project <project>`, read `store-review.md` in the skill folder and dispatch one subagent with the Agent tool, model `opus`, whose prompt is that file's text followed by: the store folder `~/.claude/projects/<project>/memory/`, this session's working directory `CLAUDE.md` path or "none", the `Dormant lessons` rows from step 0 or "none", the number of free slots, the kinds under a raised bar for this project or "none", and the denied-review titles that command printed. It returns up to that many proposals, each a `store-write` (a consolidation or a refinement) or a `rule-skill-hook` (an automation), with its kind, its entry count, the card lines of step 4 and its diff. These become proposals numbered after the findings' ones and go through step 4 like any other: their `N.diff` and `N.md`, their cards, the one question call. A consolidation's What-changes line writes out every absorbed file name one by one, and the merge is one proposal however many files it absorbs. Each one gets its question in that call even when its kind is on approve-always. Their ledger rows carry `--finding-id review`, so a denied review proposal leaves the bar for new lessons where it was, and `review` is passed over by every step that resolves a finding id.

### 4b. Mod signal proposals

When the `Mod signals` block of the step-0 `scan.py --open` output holds a signal whose `overall` row shows 3 or more windows, that signal is a finding of its own (one per signal) and gets one mechanism proposal: a hook, a mod change or a nudge that acts at the moment the signal fires, because the signal kept repeating with the instructions already loaded, so the fix lives in that mechanism rather than in a CLAUDE.md line. `fanout-miss` is a fan-out miss: a turn where Claude read 10 or more files itself and dispatched no subagent; `reads` counts those files. Its kind is `rule-skill-hook` for a hook, rule or settings change, and `other-file` for a file under `~/.claude/mods/`. What-changes names the mechanism and the signal exactly as the ledger writes it (for example `fanout-miss`), so the next run finds it, and quotes the signal's windows and read counts, and the Exact edit is that mechanism's diff. These proposals are numbered after the findings' ones and go through step 4 like any other.

When an `overall` row ends with `windows since approved fix <date>: <n>`, that `<n>` is the figure counted against the threshold of 3. The indented `earlier proposal <date> <decision>: <title>` lines under an `overall` row are that signal's history: read them there in place of a search through old proposals, and search by hand only for a signal whose row shows none. A line matches an older card on the signal's name, on the lines its diff changes or on a file only that signal's cards edit; a line ending ` (matched by diff)` or ` (matched by file only)` never counts as the approved fix.

### 4c. How it will be checked

On a `rule-skill-hook` card, the How-it-will-be-checked line names the test, command or run against the real file that step 5's Verify will perform after its read-back, and the result that counts as a pass (for example "run the hook's tests: all pass"), or says "none can run now" and why; a check that then fails gets `--verified n` (say so).

### 4d. Why you might say no

The Why-you-might-say-no line names an objection when one of these kinds applies to the proposal, in one plain sentence that states its particular:
- a measured cost of this proposal, giving the number, such as words added to always-on text or seconds per run;
- an overlap with an existing rule or lesson, giving its name;
- a concrete case where the change would misfire, describing the case;
- a decision the user made that it reverses, naming the decision;
- a likely one-off, giving how many times it was seen.

When none of these applies, or the card's other lines already answer the only objection there is, the line reads exactly "No strong reason against."

### 4e. Rule or mechanism

When a card's Mechanism-instead line names a skill, a script or command, a subagent, a hook or a gate, three lines follow it on the card:
- Rule: plus <one advantage>; minus <one drawback>.
- Mechanism: plus <one advantage>; minus <one drawback>.
- Recommend: <rule or mechanism>, because <one reason>.

Rule is the text this card proposes; Mechanism is the one the line names. Take each plus and minus from what actually differs between the two: when it acts (a rule at every session's reading, a mechanism at the moment of the mistake), what it covers and what it misses, where it can misfire, and what it costs to build and keep. A rule file is the same text in another place, so a line that names one prints alone, as a "none fits" line does.

## 5. Applying an approved proposal

Never edit a target file without the journal.
- Add or edit: `python journal.py snapshot --run <run> --path <file> --kind <kind> --proposal N`, make the edit, `python journal.py commit --run <run> --path <file>`. Repeat per file, including MEMORY.md.
- Delete: `python journal.py delete --run <run> --path <file> --kind store-delete --proposal N`, then remove its MEMORY.md line with snapshot and commit.
- Merge, a store review's consolidation: write the merged file and MEMORY.md with snapshot and commit, and move each absorbed file with `python journal.py delete --run <run> --path <file> --kind store-write --proposal N`, so one undo puts the whole merge back. Every file a store review proposal absorbs or rewrites that has a row in the `Dormant lessons` block gets `python scan.py --resolve <F-id> --status resolved:reviewed --reason "<proposal title>"`.
- Verify: re-read the file and confirm the diff applied; `--verified y` only when you read it back, `--verified n` when the read-back differs (say so), `--verified na` for a rule, skill or hook that cannot be exercised now.
- Close the finding: once the write is committed, a proposal that came from a finding with an id gets `python scan.py --resolve <F-id> --status resolved:approved --reason "<proposal title>"`. This applies to Approve and to the approve-always path alike.
- For a candidate finding that was approved: `python candidates.py status --project <project> --category <c> --key "<key>" promoted` and `python scan.py --resolve <F-id> --status resolved:promote` in place of `resolved:approved`.

Snapshot, commit and delete are also what makes the run undoable: a file changed outside those steps cannot be put back later.

## 5a. Applied

After the last proposal and before Housekeeping, print the heading "Applied" and one line per file this run wrote, naming the file and what happened to it: edited, created, or moved to trash. Omit the heading and the section entirely when the run wrote nothing. When no question was asked this run, the message that carries Applied starts with the Session review, the Findings table, Candidates and the cards, in that order, then Applied, then Housekeeping.

## 6. Empty run

When steps 2 and 3 produce no finding and no candidate, and step 4a raised no store review proposal: print Session review, then the sentence "Nothing durable surfaced this session.", then Housekeeping, and append one ledger row: `python ledger.py append --run-id <run> --project <project> --proposal 0 --finding-id none --kind none --decision none`.

A run that found something but raised no proposal, because every row is `No action.`, is not an empty run: print the report without that sentence, and append the same ledger row so every run leaves exactly one line in the ledger.

## 7. Housekeeping

Always last. A table with these rows, values from the `health.py` output and the session scan; a row whose Value carries an "only when" condition joins the table when that condition holds:

| Item | Value |
|---|---|
| Lesson store | `N of 20 entries`, from the line health.py prints for this project; over cap, followed by `review ran, M proposals`, or `review deferred` when the findings took all three slots, plus `bar raised for <kinds>` when a raised bar held review proposals back |
| Global gotchas budget | `W of 350 words`, from the `Machine gotchas:` line of health.py (only when a `global-line` was proposed; state the number after the proposal) |
| Open findings for this project | the number from the `Findings:` line of health.py |
| History scan | the `History scan:` line from health.py (only when it reads `never run` or ends in `days old`, or a history scan is running: step 0.3 reported one or this run started one) |
| Session scan | `ok`, `truncated to the last N messages` where N is `messages_seen` from the scan JSON, `skipped, history scan running`, or `failed` |
| Approve-always | the kinds (only when at least one kind is set) |
| Raised bar | the kinds on the `Raised bar` line of health.py for this project (only when health.py prints that line) |
| Earlier runs | each `note:` line that `journal.py begin` printed under the run id, without the `note:` prefix (only when it printed any) |

If the `health.py --store <project>` output carried the one-time line `Ledger: pre-v3 ledger moved to retro-log.v2.tsv`, add one sentence under the table saying the older ledger was set aside under that name and the current one starts from this version.

Then, when the Applied section was printed, one closing line: the `Undo this run with:` line that `journal.py commit` or `journal.py delete` printed under its result, copied exactly as printed. A run that wrote nothing has nothing to undo, so the line is omitted. Nothing goes after the closing line.

## 8. Requests the user may make in any session

- "retro settings": run `python settings.py show`, explain each approve-always kind and each raised bar (per project) in one line, and offer `python settings.py set-always <kind> on|off` (the only way a kind gets onto approve-always; the proposal dialog never offers it) or `python settings.py reset-bar <kind> <project>` (without the project, the kind is reset in every project).
- "undo retro" or "undo <run>": `python journal.py undo <run>` and print its output. When the user names no run, take the newest file in `~/.claude/retro/journal/`, whose name is the run id with `.json` removed, and pass that id as the argument; the command needs a run id and is refused as a bad argument without one. It refuses, and changes nothing, when a file has been edited since the retro touched it; print the reason and stop. An undo puts back only what that run recorded: files edited through a snapshot and commit, and files the run removed through the journal's delete step. Anything else changed during the session stays as it is, so say that plainly rather than describing undo as a full rewind.
- "restore <file>": `python journal.py restore <run> <file name>`. This puts back a single file the run removed, matched on the file name, so pass the name rather than the full path. It does not reverse an edit; undo is what reverses edits.
- "review the store": a store review at any store size. Run steps 0.1, 0.2, 0.4, 0.6 and 0.7, then run step 4a with three free slots. Print its cards and continue from the line step 0.7 kept, in step 4, through step 5a, then a Housekeeping table holding the Lesson store row alone, with `review ran, M proposals`, then the undo line as in step 7 when Applied was printed. A review that returns no proposal gets one line saying so and the step 6 ledger row.
- "rebuild check": asks of the standing setup "If you rebuilt this CLAUDE.md and hook set today, what would you keep?", so that rules get cut as well as added. Run steps 0.1, 0.2, 0.4 and 0.7, then `python ledger.py denied-review --project <project>`, read `rebuilder.md` in the skill folder and dispatch one subagent with the Agent tool, model `opus`, whose prompt is that file's text followed by: `~/.claude/CLAUDE.md`, the folder `~/.claude/hooks/` and `~/.claude/settings.json` (each as a path, or "none" when it is missing), three free slots, the kinds under a raised bar for this project or "none", and the denied-review titles that command printed. Its proposals are numbered from 1 and go through step 4 like any other, each with its question even when its kind is on approve-always, and their ledger rows carry `--finding-id review`. Print its cards, then its closing `Rebuild check:` line, and continue from the line step 0.7 kept, in step 4, through step 5a, then a Housekeeping table holding the Global gotchas budget row alone, then the undo line as in step 7 when Applied was printed. A check that returns no proposal gets its closing line and the step 6 ledger row.
- "retro criteria": updates the list step 0 prints. Run steps 0.1, 0.2 and 0.7, then `python ledger.py criteria` and `python ledger.py denials`, which prints one line per denied proposal: date, project, title, the reason the user gave and the objection the card raised against itself. Print those lines as a table. When the reasons the user wrote in their own words (anything beyond "not worth a change", "already covered" and "wrong fix") support adding, rewording or cutting a line of `~/.claude/retro/good-proposal.md`, raise one proposal that edits that file, kind `other-file`, ledger rows with `--finding-id review`, keeping the list to seven lines. Print its card and continue from the line step 0.7 kept, in step 4, through step 5a, then the undo line as in step 7 when Applied was printed. When the reasons support no change, say so in one line and write the step 6 ledger row.
- "retro metrics": `python health.py --metrics`.
- "scan history": `python scan.py --background`.
