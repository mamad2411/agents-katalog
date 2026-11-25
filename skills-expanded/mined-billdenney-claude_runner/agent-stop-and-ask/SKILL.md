---
name: agent-stop-and-ask
description: |
  How a task-running agent stops and asks the operator a question via
  the claude_task_runner sidecar protocol. Domain-specific skills (e.g.
  extract-literature-model) state WHEN to stop; this skill states HOW
  to stop. An agent reaches this skill when it hits any "stop and ask"
  trigger from its host skill while running under claude_task_runner —
  i.e., its working_dir is a per-task git worktree
  (<repo>/.claude/worktrees/<task_id>/) and the env var TASK_ID is set.

  Triggers: "/agent-stop-and-ask", "I need to ask the operator",
  "this needs a sidecar question", or any time a domain skill says
  "sidecar-ask the operator". Do NOT trigger interactively (no
  TASK_ID); use AskUserQuestion in that case.
---

# /agent-stop-and-ask — write a sidecar request and exit cleanly

When a domain skill (like `extract-literature-model`) tells you to
stop and ask the operator, you write a sidecar request to disk and
**exit cleanly**. The runner detects the unanswered request when your
subprocess exits and transitions the task's status to
`awaiting_sidecar` automatically — your concurrency slot frees up for
the next pending task while this one waits for the operator.

## When to use this skill

Invoke this skill when **all** of these are true:

1. A domain skill's stop-and-ask trigger has fired (ambiguous source
   parameter, missing data, novel covariate name, etc.).
2. You are running as a `claude_task_runner` task — i.e., the env var
   `$TASK_ID` is set and your `cwd` is a per-task worktree.
3. The decision is **operator-actionable** with a small set of
   discrete options. (If you genuinely have all the information you
   need, do NOT trigger a sidecar — just decide.)

If you are running interactively (`$TASK_ID` unset), use the built-in
`AskUserQuestion` tool instead — it's cheaper for the user and shows
the same options as a sidecar would.

## Never file a sidecar to announce completion

**Finishing a task is not a question.** Commit, push, and move the task
YAML from `todo/` to `done/` — that IS the completion signal, and it is
the only one the runner needs. Then exit.

Do **not** file a sidecar to:

* report that the work is done, pushed and green ("NOTIFICATION ONLY -
  no decision required");
* ask whether the operator wants the PR opened, or hand over a PR title
  and body for them to paste;
* ask them to confirm a close when nothing is outstanding.

Those cost a real dispatch each and they do not terminate. A task whose
YAML stays in `todo/` is still a dispatch candidate, so answering its
notification sidecar makes it eligible again: it re-runs, finds nothing
to do, and files another one. On 2026-09-11 the nlmixr2lib ingestion
queue held **27** such sidecars, and one task (`oasweep_PMC11754279`)
had burned three dispatches confirming work that had been merged since
2026-09-07.

**Why moving the YAML is sufficient.** `queue.store.list_pending()`
enumerates candidates from `todo/` only, and `tick_dispatch` then
filters on `_DISPATCHABLE_STATUSES = {pending, failed}`. A YAML in
`done/` is never a candidate, whatever its state file says.

**The one hazard: move it only after the push is verified.** A YAML
moved to `done/` on work that did not actually reach the remote
disappears from the queue silently and will never be re-dispatched.
Verify the branch is on origin (e.g. `git ls-remote --heads origin
<branch>` returns the SHA you just pushed) BEFORE moving it.

**PRs are not the agent's job.** The operator's `gh` key is read-only by
policy, so you could not open one anyway. Put the suggested title and
body in the deliverable report and stop — pushed branches are landed by
a bulk consolidation pass (`/runner-merge-claude-branches`), not one PR
per model.

This rule is about NOTIFICATIONS. A genuine question — an ambiguous
source value, a novel canonical name, a structural choice — still gets a
sidecar, exactly as described below.

## Protocol

### 1. Build the SidecarRequest payload

The schema is in `claude_task_runner.queue.schema.SidecarRequest`. The
runner accepts JSON with these fields:

```json
{
  "schema_version": 2,
  "task_id": "<from $TASK_ID>",
  "sequence": <int, see step 2>,
  "created_at": "<ISO-8601 UTC, e.g. 2026-05-06T01:23:45Z>",
  "summary": "<one-line description of why you're stopping>",
  "context": "<multi-paragraph explanation including verbatim quotes from the source location that triggered the question>",
  "questions": [
    {
      "id": "q1",
      "prompt": "<the actual question — concrete and answerable>",
      "options": [
        {"value": "A", "label": "<short choice>", "description": "<what happens if the operator picks this>", "proposed_names": []},
        {"value": "B", "label": "<short choice>", "description": "<what happens if the operator picks this>", "proposed_names": []}
      ],
      "recommended": "A",
      "multi_select": false,
      "allow_free_text": false
    }
  ]
}
```

Required fields per question:

- `id` — short identifier (`q1`, `q2`, ...). **Unique within the request.**
  The runner tracks answers per question id, so two questions sharing an id
  collapse into one and the second silently never gets answered.
- `prompt` — the operator-facing question. Phrase it so a click on
  one of your options is enough; never a yes/no without options.
- `options[]` — at least 2 concrete choices. Common pattern for an
  extraction-style sidecar:
  - A — extract anyway with this specific assumption
  - B — skip this task
  - C — defer pending operator investigation

Optional but recommended:

- `recommended` — your best guess of the right option. The operator
  sees it first with "(Recommended)" appended; one click ships your
  recommendation. Don't recommend if you genuinely have no preference.
- `multi_select` — set true only if multiple options can be chosen
  together (rare).
- `allow_free_text` — set true to let the operator type a custom
  answer. Default false (forces a click).

### 1b. If you are proposing a canonical name, make it machine-readable

Naming questions — "ratify `FED_HIGHFAT` as the canonical covariate for a
high-fat meal" — are the single largest category of sidecar traffic, and
they are the most mechanically triageable: a queue-side script can
collision-check a proposed name against the project's registers and
auto-approve it under the operator's standing rule, without the operator
reading anything. That only works if a machine can tell which token is the
proposed name.

**Two rules, both required:**

1. **Put the names in `proposed_names`** on each option that would create
   or adopt them. This is the authoritative, structured field:

   ```json
   {"value": "A",
    "label": "Adopt `MEAL_INTERVAL` as the canonical name",
    "description": "New canonical; no existing register entry covers dose-to-meal interval.",
    "proposed_names": ["MEAL_INTERVAL"]}
   ```

   Multiple names per option are fine (`["CLCR", "CLCR_CG"]`). Leave it
   `[]` — or omit it — on options that propose no name ("skip this task",
   "defer to the operator").

2. **Also write each name in backticks inside `label`**, exactly as it
   would appear in code. The operator reads the label, not the JSON, and a
   backticked token shows them precisely which string they are ratifying.

**Why both.** The structured field is what a script should read. Backticks
are the fallback for anything that misses it, and they are the reason to
never write a proposed name as bare prose. Recovering names from prose was
tried on a real backlog and abandoned: it pulled ordinary English words
("other", "label", "scope", "list"), producing both bogus collision hits
and — far worse — false clean results, where a question looked
collision-free only because the actual names were never checked. Of 118
naming questions, only 10 could be cleared mechanically; the other 88
failed purely because their names were not backticked.

- ❌ `"label": "Use the high fat meal covariate name"`
- ❌ `"label": "Adopt FED_HIGHFAT"` — extractable only by guessing which
  bare word is the name.
- ✅ `"label": "Adopt \`FED_HIGHFAT\`"` + `"proposed_names": ["FED_HIGHFAT"]`

### 2. Compute the sequence number

A task may file multiple sidecars across its lifetime. Each request
gets a fresh task-scoped sequence:

```python
import re
from pathlib import Path

sidecar_dir = Path(f"<queue>/.claude_task_runner/sidecar/{task_id}")
sidecar_dir.mkdir(parents=True, exist_ok=True)

existing = []
for p in sidecar_dir.iterdir():
    m = re.match(r"^request-(\d+)\.json$", p.name)
    if m:
        existing.append(int(m.group(1)))
sequence = max(existing, default=0) + 1
```

### 3. Resolve the queue directory

If the task's preamble or env doesn't tell you the queue path
explicitly, walk up from `$PWD` looking for a `.claude_task_runner/`
sibling. The conventional pattern: per-task worktrees live under
`<repo>/.claude/worktrees/<task_id>/` and the queue lives elsewhere
(e.g. `~/.../queue/`). If you can't find the queue, fall back to
asking via `AskUserQuestion` — but the runner usually exposes the
queue path via an env var or a preamble note.

### 4. Write the request atomically

```python
import json, os, tempfile
from pathlib import Path

target = sidecar_dir / f"request-{sequence:03d}.json"
with tempfile.NamedTemporaryFile(
    mode="w",
    encoding="utf-8",
    dir=sidecar_dir,
    delete=False,
    prefix=f".{target.name}.",
    suffix=".tmp",
) as tmp:
    json.dump(payload, tmp, indent=2, default=str)
    tmp.flush()
    os.fsync(tmp.fileno())
    tmp_path = Path(tmp.name)
os.replace(tmp_path, target)
```

The atomic tempfile + `os.replace` write is required: a partial JSON
file would crash the operator's `/runner-answer-sidecar` skill.

### 5. Exit cleanly — DO NOT POLL FOR THE RESPONSE

After writing the request file, **immediately exit your process**
(`exit` from Bash, return from the agent, stop emitting output —
whatever it takes for the `claude --print` subprocess to terminate).
Do not continue with the extraction. Do not write a partial result.
Do not best-guess the question's answer.

**ANTI-PATTERN — explicitly forbidden:**

```bash
# ❌ DO NOT do this. Burns a concurrency slot indefinitely.
until [ -f .../response-NNN.json ]; do sleep 10; done
```

A polling loop that waits for the response file blocks your task
slot for as long as the operator takes to answer (often hours, even
overnight). It defeats the entire `awaiting_sidecar` mechanism: the
orchestrator can't free your slot to dispatch the next pending task
because your subprocess is still alive.

**What actually happens after you exit:**

1. Your `claude` subprocess exits (any exit code is fine — clean,
   error, or even cap-killed).
2. The runner's `runner.dispatcher.dispatch` post-run code scans
   `<queue>/.claude_task_runner/sidecar/<task_id>/` for an unanswered
   request. "Unanswered" is judged **per question**: a request is open
   while any `questions[].id` it asked is missing from the response's
   `answers[].id`. A `response-NNN.json` that answers only `q1` of a
   `q1`/`q2`/`q3` request leaves the task waiting on `q2` and `q3`.
3. If found, it overrides the task's final status to
   `awaiting_sidecar` regardless of how you exited.
4. The orchestrator's eligibility check skips `awaiting_sidecar`
   tasks, so your slot **frees up for the next pending task in the
   queue**.
5. When the operator answers (`/runner-answer-sidecar` writes
   `response-<NNN>.json`), the next supervisor tick detects the
   response and re-dispatches this task via
   `claude --resume <session_id>`.
6. The resumed agent reads the response file (your previous run's
   request + the operator's response sit side-by-side in the sidecar
   dir) and continues from where you stopped, using the operator's
   chosen option.

**The contract is: you write the request, you exit, the runner
handles everything else.** Polling is the agent re-implementing the
runner's job badly.

## What this skill does NOT do

- **Doesn't second-guess the trigger.** If the domain skill says
  "stop and ask", stop and ask. Don't decide it's overcautious.
- **Doesn't handle interactive mode.** Use `AskUserQuestion` when
  `$TASK_ID` is unset. Sidecar files in an interactive session would
  never be answered.
- **Doesn't write the response.** That's the operator's job via
  `/runner-answer-sidecar`.
- **Doesn't manually transition task status.** The dispatcher handles
  status transitions based on the request file's presence.

## Anti-patterns

- ❌ "I'll write the sidecar AND continue with my best guess in case
  the operator doesn't answer in time." — defeats the protocol.
  Don't.
- ❌ "I'll skip the sidecar and just pick the safest option." —
  exactly what the protocol exists to prevent.
- ❌ "I'll write a vague yes/no question." — give the operator
  concrete options with descriptions.
- ❌ "I'll set `allow_free_text: true` so the operator can type
  anything." — most decisions are between a small set of options;
  free-text is a fallback, not a default.
- ❌ "I'll reuse `q1` for both questions." — ids are the unit of
  answer accounting; a duplicate id means one question is never answered.
- ❌ "I'll name the proposed canonical in the description prose." — put it
  in `proposed_names` and in backticks in the label, or it stays manual
  forever.

## See also

- The `runner-answer-sidecar` skill (operator-facing) walks the
  operator through pending sidecars and writes the response file.
- `claude_task_runner.queue.schema.SidecarRequest` — Pydantic schema
  the runner validates against. Field validation errors surface in
  `/runner-answer-sidecar` if your JSON is malformed.
