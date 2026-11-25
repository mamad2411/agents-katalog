---
name: runner-add-task
description: |
  Use this skill when the user wants to add a task to the Claude task
  runner queue. Triggers: "/runner-add-task", "add a task to the
  queue", "queue up this work", "enqueue a job for the runner",
  "add a popPK extraction task", or any equivalent
  enqueue-this-for-the-runner phrasing. Walks the operator through
  required fields, validates effort against the per-model TOML, then
  invokes `claude-task-runner queue add` to write the YAML.
---

# /runner-add-task — add a task to the runner queue

This skill is interactive. It collects required fields via
`AskUserQuestion` (where there's a fixed list of choices) or by
asking directly (where there's free-form text), then invokes
`claude-task-runner queue add` to write the task YAML.

> **Authoring a YAML by hand (or setting a field `queue add` doesn't expose —
> e.g. `depends_on`, `deliverable_paths`,
> `account`)?** Run `claude-task-runner queue template` for a complete,
> annotated, copy-paste example, or `queue template --reference` for the
> field-by-field table. Unknown keys are rejected, with an error that names the
> offending field and suggests the closest valid one — so a typo'd key fails
> fast and fixably rather than silently.

## Required fields

Drive the operator through these one at a time. Don't ask for them
all at once.

1. **Task ID** — a short identifier matching `[A-Za-z0-9._-]+`.
   Convention: numeric prefix matching the task's order in the queue
   (`007-name`). If the operator doesn't have a prefix in mind, run
   `claude-task-runner queue list --queue <CWD> --json`, look at the
   highest existing prefix, and propose the next number.

2. **Title** — single line. Ask plainly.

3. **Prompt** — the actual task text. For anything longer than ~3
   sentences, write to a temp file and pass `--prompt-file
   /tmp/<id>.prompt.txt`. Don't try to escape multi-line prompts on
   the CLI.

4. **Model** — `AskUserQuestion` with the configured models from
   `claude-task-runner usage whoami` (or hardcoded common set if you
   can't read it: `claude-opus-5-5`, `claude-sonnet-5`,
   `claude-haiku-4-5`). Default opus for substantive work.

5. **Effort** — `AskUserQuestion` with the per-model accepted set.
   Read `[effort_levels]` from the config: typically `low`, `medium`,
   `high`, `xhigh`, `max` for opus; smaller set for sonnet /
   haiku. The runner passes it to the agent as `claude --effort`, so it
   sets how hard the agent thinks, and its token cost. `queue add`
   rejects a mismatched (model, effort) pair, including `extra_high`,
   the old name for `xhigh`.

6. **Priority** — `AskUserQuestion` with `low | normal | high`.
   Default `normal`.

## Optional fields (ask only if the user volunteers info)

- **Allowed tools** — comma-separated list. Default omits the flag,
  giving the dispatch the runner-default toolset.
- **Tags** — free-form labels. `queue list` reports them; the runner
  attaches no meaning to them.
- **`--weekly-critical`** — set if the user says it must complete
  before the weekly window resets.
- **`--add-dir <dir>`** (repeatable) — extra absolute directories the
  dispatched `claude` subprocess should be allowed to read/write
  outside its cwd. The queue directory is *always* added by the
  dispatcher; only set this for additional paths (e.g. a sibling
  repo, a shared data tree). Each entry persists to
  `additional_dirs` in the task YAML. Missing paths are warned but
  do not block adding the task — they may be created by the
  pre-dispatch hook before the agent runs.
- **`--working-dir <path>` / `--no-working-dir`** — the directory the
  dispatched agent runs in (and the value the pre-dispatch hook
  receives as `$TASK_WORKING_DIR`). See the next section for when
  these flags matter; the short version is that you usually do NOT
  need to ask the operator about working_dir.

## working_dir: when (and when not) to ask

ADR-0023: per-queue `[queue].working_dir_template` (in
`claude_runner.toml`) is the canonical way to set `working_dir`. When
it's configured, `queue add` substitutes `{task_id}` into the template
and writes the result into the new YAML automatically — DON'T ask the
operator about working_dir in this case.

To check, read the per-queue config:

```
python3 -c 'import tomllib, sys
cfg = tomllib.load(open(sys.argv[1], "rb"))
print((cfg.get("queue") or {}).get("working_dir_template", ""))' \
  <CWD>/claude_runner.toml
```

(empty output = no template set).

Decision tree:

1. **Template is set AND the new task fits the convention** → don't
   ask; let the template apply. This is the common case.
2. **Template is set BUT this task legitimately doesn't need a
   working_dir** (e.g. a queue-wide categorization shard that doesn't
   operate on a single per-task checkout) → pass `--no-working-dir`.
   Ask the operator only if you're unsure.
3. **Template is set but THIS task needs a different path** → pass
   `--working-dir <explicit-path>`. Ask the operator for the path.
4. **No template configured AND the queue has a pre-dispatch hook
   that depends on `working_dir`** (read
   `[hooks].pre_dispatch_command` from the same TOML — non-empty
   means a hook is configured) → ask the operator whether this task
   needs a `working_dir`, and if yes for the path. Encourage them to
   add the template to `claude_runner.toml` and run
   `claude-task-runner queue backfill-working-dir` once so future
   `queue add` invocations don't need this question.
5. **No template, no hook** → don't ask; let `working_dir` stay null.

## Invocation

Once collected, run something like:

```
claude-task-runner queue add \
    --queue <CWD> \
    --id 007-foo \
    --title "Extract Bar 2026 abciximab popPK" \
    --prompt-file /tmp/007-foo.prompt.txt \
    --model claude-opus-5-5 \
    --effort high \
    --priority normal
```

If the runner is already up, the supervisor will pick the task up on
the next poll. If not, suggest `claude-task-runner supervisor start`
or rely on the watchdog.

## --add-dir scope: when to set it

Claude Code's `--print` subprocess sandboxes the agent to its cwd; any
`Read`/`Write`/`Bash` call to a path outside cwd is silently blocked.
The runner always adds the queue dir automatically, which covers the
sidecar protocol, reports/, and any sources stored under the queue
root (papers/, from_people/, etc).

Set `--add-dir <path>` only when the task needs access to something
that lives *outside* the queue dir:

- a sibling repo the task should read but not own,
- a shared data tree (e.g. `/data/cohort-X/`),
- a per-team source tree the operator maintains alongside the queue.

Typical setups don't need `--add-dir` at all — if the prompt
references files under the queue, the always-on queue dir is
sufficient.

## Things this skill doesn't do

- Doesn't dispatch the task immediately; only writes the YAML.
- Doesn't ask about `depends_on` or per-task token caps unless the
  operator brings them up — defaults are sane.
- Doesn't validate the prompt content; if the operator wants the
  runner to extract a paper, the operator's prompt is the source of
  truth.
