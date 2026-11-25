---
name: turn-session-into-skill
description: >-
  Load this skill right after a task was done in this session and should be repeatable: turn the
  steps that worked into one SKILL.md in `.claude/skills/`, with no interview. Trigger on "turn what
  we just did into a skill", "save this as a skill", "skillify this".
argument-hint: "[skill-name]"
disable-model-invocation: false
user-invocable: true
license: Apache-2.0
---

# Turn session into skill

Write one `SKILL.md` that lets a later session repeat the task this session just finished, built
from what actually ran rather than from an interview. Done when the file exists under
`.claude/skills/<name>/`, every step in it traces to a step that succeeded in this session, and
the user has the list of what came from where. A run that Step 5 hands off, or that a stop
condition ends, is done once the user has been told which and why.

The session is better evidence than anyone's memory of the task: it holds the exact commands and
flags that worked, the order, and every correction the user made. An interview reconstructs that
less accurately and asks questions the transcript already answers.

## Procedure

1. **Recover the run.** List, in order, the tool calls that moved the task forward: commands with
   their exact flags, files read and written, and checks that proved a step worked. If the context
   was compacted and early steps are only summarized, read the session transcript at
   `~/.claude/projects/<project-slug>/<session-id>.jsonl` for the exact calls. Drop steps that
   failed and were redone, and keep only the version that worked.
2. **Collect the corrections.** Every time the user corrected the agent ("no, use X", "don't touch
   Y") is a rule the next run must follow without being told. Write each one as a rule with the
   reason the user gave, or the failure it prevented.
3. **Split what changes per run from what does not.** A value that would differ next time (a
   version, a ticket id, a file name, a date) becomes an argument with an `argument-hint`. A value
   that stays the same stays literal. Hard-coding this run's values is the most common way a
   session-built skill breaks on its second use.
4. **Name the moment.** Write the `description` around what the user is doing when the skill
   should fire, with trigger phrases in their words from this session and a "Not for" line naming
   the nearest neighbor. Name the skill with a verb phrase. Check `.claude/skills/` and the
   session's skill list for one that already covers the task. Extend that one instead of adding a
   twin.
5. **Check it is one skill.** If the steps need a pause for approval mid-run, must resume after an
   interruption, or fan out over many items, a single skill is the wrong shape. Say so, and if
   `ceh-workflow-builder` is installed, hand the recovered steps to
   `ceh-workflow-builder:build-agentic-workflow` as its intake instead of writing the file.
6. **Write the file** to `.claude/skills/<name>/SKILL.md` in the target repo, or to
   `~/.claude/skills/<name>/` when the user says the skill is personal. Use the shape under Output.
7. **Prove it traces.** Walk the written steps against step 1's list: each command appears in the
   session and succeeded there, each argument is used, and each rule maps to a correction. A real
   test run (a fresh `claude -p` session invoking the skill) is a billed model call, so offer it
   and do not run it unasked.

## Rules

- **Only what ran.** Include only steps, branches, and options this session exercised. One observed
  run shows one path, and a branch nobody ran is a guess that will mislead the next run.
- **No secrets.** A token, password, or key that appeared in the session never goes into the file.
  Name the environment variable or the place it is read from instead.
- **Irreversible steps pause.** A step that pushed, published, deployed, sent, or deleted gets an
  explicit confirmation line before it, and the skill sets `disable-model-invocation: true` so it
  runs only when a person invokes it.
- **Decide, do not interview.** Every answer this skill needs is in the session. Ask the user only
  for the skill's scope (repo or personal) when the session gives no sign, and default to the repo.

## Output

The written skill:

```markdown
---
name: <verb-phrase>
description: >-
  Load this skill when <the moment>: <what it does>. Trigger on "<phrase>", "<phrase>". Not for
  <nearest neighbor>.
argument-hint: "<per-run values>"
disable-model-invocation: <true if any step is irreversible, else false>
user-invocable: true
---

# <Title>

<One sentence: what it does and what done looks like.>

## Procedure

1. <Step, with the exact command that worked.>

## Rules

- <A correction from the session.> <Its reason.>
```

Then, in chat, a three-column table mapping each step and rule in the file to where it came from
in the session (the command, or the user's correction), and the line "Not run: a live test of the
skill" unless the user asked for one.

## Stop conditions

- Nothing in this session completed a task → say there is no run to capture, and point to
  `ceh-workflow-builder:build-agentic-workflow` for building from a description.
- The session's steps failed and the task never reached done → stop: a skill built from a failed
  run repeats the failure.
