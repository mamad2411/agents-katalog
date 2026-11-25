---
name: session-diagnosis
description: >
  Read a session's transcript and its subagent transcripts in place, check first whether Forge loaded, then report
  per dimension what happened, with a path:line for every finding and the question whether the problem occurs
  without Forge. Use when a session went wrong and the user asks why (a skill that did not fire, an ignored plan or
  rule, repeated work, stumbles, unsupported claims, cost or time), or to gather evidence for a Forge report; NOT for
  repairing the defect (use root_cause_fix) or reviewing code (use code_review_board).
status: active
invocation:
  primary: user-facing
  secondary: []
disable-model-invocation: false
uses: []
---

Read and follow `framework/work-principle.md` before taking up work.
Resolve this reference against the framework root; retain the consumer CWD.


# Skill: session-diagnosis

## Source

Superpowers (MIT License, © 2025 Jesse Vincent); Forge's register of adopted methods.

## Purpose

When a session went wrong, the transcript on disk holds what happened. This skill reads it, with the transcripts of
the subagents it started, and reports with evidence: first whether Forge loaded at all, then what the session did
along seven dimensions, then whether the problem would occur without Forge. The report names the layer that failed
in `CONTRIBUTING.md` (installation, instruction loading, session outcome) and carries the evidence that layer asks
for.

The skill reports; it does not repair. A defect the report shows goes to `root_cause_fix` or into a Forge report.

## When to call

- The user asks why a session went wrong, names a past session by id or path, or asks what a running session is
  doing.
- The user wants evidence for a Forge bug report.
- An independent trial asks a participant for evidence of a session, without the transcript itself.

### When not to call

- To repair the defect: `root_cause_fix` takes the report as its evidence.
- To review the code a session produced: `code_review_board`.
- When no transcript is available: ask for its path or an export; do not reconstruct a session from memory.

## Process

1. **Problem statement.** A request that names the session and the event, or the observable the user cares about,
   is the statement. Otherwise ask one question at a time until you can write: the session(s), the turn range if
   known, what was expected, what happened, and the observable (wall time, usage, repeated actions, one action).
   Note whether the goal is a Forge report. "It took too long" is a complaint, not a statement. When nobody can
   answer (the user is away, a headless run), write the questions and stop.
2. **Locate.** Resolve each session to absolute paths: every transcript file, its subagents' transcripts and the
   files the host stores beside them (`dimensions.md` §Reading a transcript). Confirm a past session by its id,
   working directory and first prompt, with its timestamp where the records carry one, not by recency; list
   rejected candidates with the reason. Forge's rules come from the framework root the session used (its boot entry
   names it), not from yours.
3. **Load check, per transcript file, before any dimension.** Three evidence points:
   - the boot entry reached the session (the hook's record, or the adapter's instructions in context);
   - the files the entry names were read, or the entry included them;
   - the first answer (in a headless run, its only answer): a greeting with the boot findings, or the notice that
     an instruction unit did not load (`agents/buddy/boot-status.md` §Greeting findings). A notice that does not
     open the first answer is its own finding, with its position.

   After a compaction or a resume, check also whether the files the boot names for a reread were read again.
   The verdict decides the layer of `CONTRIBUTING.md`:
   - `loaded`: no loading failure. The layer is session outcome when the dimensions show a wrong action, and "none
     shown" when they do not.
   - `cut short` (the step, disclosed or not) or `declined`: instruction loading, on the agent's side; the entry
     arrived and was not followed. Quote the reason the agent wrote. When the reason cites Forge text (an intent
     line, a rule), quote that text beside it with its `path:line` (project or framework root): whether the text misled
     is the maintainers' call. From that point on, the dimensions describe the host model without Forge's process.
   - `not reached`: installation or instruction loading, on the host's side. The host's read-only check
     (the host's plugin check for the plugin; `python3 scripts/forge_setup.py status` for OpenCode, in the framework
     root, or the user's output of it) tells them apart; without it, write "installation or host delivery, not separated".
   - `unknown`: no layer. Name the missing evidence.
4. **Dimensions.** Run the seven dimensions of `dimensions.md` §Dimensions. Up to 300 KB of transcripts in all, read
   them yourself, record by record (intent: one careful read in the deciding context). Beyond that, dispatch one
   analyst per dimension in parallel, on the standard tier (`framework/models.md`, "Any other role"), each with a
   case block: the absolute paths, the problem statement, the load-check verdict, the record meanings you
   established, the framework root and its revision, the instruction files and boot entry, the agreed plan or
   acceptance, and `dimensions.md`. Split a dimension by line range when one file exceeds 1 MB.
5. **Citations.** Every finding carries `path:line` and a quote of at most 200 characters. A finding about an
   absence (no record of X) carries instead the search command, the files and lines it covered, and its zero
   result. Drop a finding with neither, your own and an analyst's alike. Before a finding enters the verdict, reopen
   the cited record or rerun the search: a finding the record does not show is dropped; one it leaves open goes to
   coverage. A number comes from a transcript field or a command you ran, never from memory.
6. **Baseline question.** The report asks whether the problem occurs without Forge.
   - **The problem session's verdict is not `loaded`:** it already ran without Forge's process. The baseline cannot
     separate Forge from the host model: say so.
   - **A comparable session without Forge exists** (the same task, host and model, Forge not installed; ask the user
     for one): run the load check on it too, then answer from it with citations and the number of runs. One run
     shows that the problem can occur without Forge, not how often. A session with another framework in Forge's
     place answers only in part: say so.
   - **Otherwise:** write the question and the run that would answer it; start that run only when the user asks.
7. **Report.** Fill `dimensions.md` §Report in order. Write it to the folder the user names, or by default to a new
   folder under the system's temporary directory; when the named folder lies inside a Git work tree, say so and ask
   for another. Show the report and give the path. Before it is shared (a Forge report, a trial), prepare the shared
   copy (`dimensions.md` §Shared copy) and have the user read it.

## Red Flags

- Reading a session file whole, or with an unbounded `grep`: one record can exceed a megabyte.
- Writing, moving or deleting a session file.
- Copying a transcript into a repository, an issue or an upload; sharing a report that is not the shared copy the
  user has read.
- Treating hook output, system reminders, tool results or a parent agent's dispatch as the user's words.
- Running dimensions before the load check, or reading a host model's behaviour as Forge's when Forge did not load.
- Proposing a fix in the report. Asked whether Forge needs a fix, give the layer and the evidence; the fix is
  decided in `root_cause_fix` or by the Forge report's maintainers.

## Common Rationalizations

| Excuse | Answer |
|---|---|
| "The cause is obvious; skip the load check" | Forge's own process leaves no trace when it did not load. The load check is the first finding. |
| "I remember what happened in that session" | Memory is not evidence. Cite the line or drop the finding. |
| "The analyst is confident; keep its uncited finding" | A finding without `path:line` is dropped, whoever wrote it. |
| "Attaching the transcript is easier for the maintainers" | The report carries citations and short quotes; the transcript stays on the user's machine. |
| "The quotes are short; they can go into the issue as they are" | A short quote can hold a key or a private prompt. The shared copy replaces them, and the user reads it first. |
| "Without Forge it would have gone the same; no need to ask" | The baseline question is answered from a comparable session or stays open with the run that would answer it. |

## Contract

### INPUT

- **Required:** a session the user names by id, path or "this session", with transcripts readable on this machine.
- **Optional:** the turn range; a comparable session without Forge.

### OUTPUT

- **DELIVERS:** a report file per `dimensions.md` §Report, outside the repository: problem statement, load-check
  verdict, the failed layer, findings per dimension with citations, the baseline question, coverage.
- **DOES NOT DELIVER:** a fix, a changed session file, a copy or upload of a transcript.

### DONE

- The load-check verdict has its evidence points.
- Each dimension has its findings or `none found` with what was checked.
- Every finding cites `path:line` (an absence: its search and zero result) and was checked there.
- The layer follows the load-check verdict; `unknown` names no layer.
- The baseline question is answered with citations or written with the run that would answer it.
- A report that leaves the user's machine is the shared copy, read by the user.

### FAIL

- **Retry:** a path does not resolve or a session cannot be told apart from others: ask for the id, path or export.
- **Escalate:** a transcript is unreadable or its records cannot be told apart: report that limit as coverage and
  stop the dimension it blocks.
- **Abort:** the user withdraws the request.

## Standalone justification

`root_cause_fix` diagnoses a defect from a reproduction; it has no method for reading a session transcript, and
`CONTRIBUTING.md` names the evidence a report needs without a method to gather it. Reading a transcript safely, by
dimension and with a citation per finding, is its own method; its report is the input those two consume.
