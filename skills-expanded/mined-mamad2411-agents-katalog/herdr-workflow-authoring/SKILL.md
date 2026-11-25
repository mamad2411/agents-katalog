---
name: herdr-workflow-authoring
description: Write and run a dynamic workflow on Herdr — a JS script whose agent() calls run real coding-agent CLIs (claude, codex, cursor, …) as subagents in Herdr panes, locally or on an ssh host. Use when asked to run a herdr workflow, fan a task out across subagents, pick which CLI or which computer an agent call runs on, or resume an earlier run.
---

# Authoring a herdr workflow

A **workflow** is one JS file that orchestrates other coding-agent CLIs as
subagents. It structures work that would otherwise overflow one agent's
context or benefit from running several agents at once: fan a task out across
files, get independent reviews from two different CLIs and reconcile them,
run a design → implement → review pipeline, or place work on an ssh host.
Each `agent()` call in the script becomes a real CLI
process (claude, codex, cursor, …) running in its own Herdr terminal pane; the
script itself only orchestrates — it never edits files or runs shell commands
directly.

This package does not add a `Workflow` tool to your tool list. Use the
`herdr-dynamic-workflow` CLI through normal shell access. This skill explains
the script and invoke contract; the CLI provides the agent-independent
runtime, so every `agent()` call may use any CLI Herdr supports.

You write the script; Herdr runs it and reports back a result. Nothing about
the *dialect* below is Herdr-specific — it is the same scripting model used by
Claude Code's own `Workflow` tool. What's new here is two fields on every
`agent()` call (`kind`, `ssh`) that pick which CLI and which computer each
call runs on, because unlike Claude Code's tool, a herdr workflow is not
implicitly "more Claude."

## How a run starts

The CLI takes one JSON object. Same fields as Claude Code's Workflow tool,
plus `kind` / `session` / `cwd`. Unlike Claude Code's tool, unknown keys are a
hard error here — `title`/`description` (which Claude Code accepts and
silently ignores) fail validation instead of being a no-op. Write the script
to a file, then pipe the object:

```bash
herdr-dynamic-workflow <<'JSON'
{ "scriptPath": "review.js", "args": { "pr": 412 } }
JSON
```

`args` is real JSON on the object, not a stringified list. `ssh` is an
`agent()` option in the script.

There is no compile step. Zero config: the run appears live in your own
Herdr sidebar as `<meta.name> · <last-4-of-run-id>`, one tab per `agent()`
call, while that call is in flight. Each tab closes as soon as its call
finishes, and the whole workspace closes when the run ends — pass
`cleanup: false` on a call to leave its tab (and the workspace) open instead,
see below. If your session is unreachable it falls back to a hidden `flow`
worker session. On success you get back `{ result, agentCount, durationMs }`.
No token numbers (see "budget", below).

Resume with the same object:

```bash
herdr-dynamic-workflow <<'JSON'
{ "scriptPath": "review.js", "resumeFromRunId": "wf_mt5cpbpy-i2ab" }
JSON
```

Unchanged `agent()` calls replay from the journal. The first edited or new
call and everything after it runs live.

Every worker is a real terminal, reachable while it runs:

```
herdr --session flow                       # the worker session, when one is used
herdr --session flow agent attach <name>   # one worker, in this terminal
ssh -t <host> 'bash -lc "herdr --session flow"' # an ssh host's workers
```

## The script contract

```js
export const meta = {
  name: "hello",
  description: "One agent answers a question",
};

const answer = await agent("What port does Herdr's control plane listen on by default?");
log(`answer: ${answer}`);
return { answer };
```

Five hard rules, because the script runs inside a deterministic, replayable
sandbox — not a general Node process:

1. **The first statement must be `export const meta = { ... }`**, a plain
   object literal — no variables, function calls, spreads, or computed keys.
   `name` and `description` are required; `phases: [{ title, model? }, ...]`
   is optional — `title` only affects progress display, but a phase's `model`
   sets that phase's default model (see `agent()` options, below).
2. **Plain JavaScript, not TypeScript.** No type annotations, interfaces, or
   generics — they fail to parse. No `import` — everything the script needs
   (`agent`, `parallel`, `log`, …) is already a global.
3. **Top-level `await` and a bare top-level `return` both work.** The body is
   not wrapped in a function you write yourself; write it as if it already
   were the inside of an async function.
4. **No `Date.now()`, `Math.random()`, or argless `new Date()`.** They would
   make a resumed run replay differently than it ran live, so the sandbox
   blocks them outright. Need a timestamp or randomness? Take it from `args`,
   or vary it per call by index (`label: `run-${i}``) instead of by RNG.
5. **Return plain, JSON-serializable data.** The result crosses out of the
   sandbox as JSON; functions, class instances, and circular references don't
   survive the trip.

## The globals

| Global | Signature | What it does |
| --- | --- | --- |
| `agent` | `agent(prompt, options?) => Promise<string \| structured \| null>` | Runs one subagent CLI call and waits for it to go idle. The only global that spends an agent slot. |
| `parallel` | `parallel(thunks) => Promise<Array<unknown\|null>>` | Runs `() => agent(...)` thunks concurrently; a **barrier** — waits for all of them. **Thunks, not promises** — `parallel([agent(...)])` starts every call immediately and defeats the concurrency limiter silently; always wrap: `parallel(items.map(x => () => agent(...)))`. |
| `pipeline` | `pipeline(items, ...stages) => Promise<Array<unknown\|null>>` | Items run concurrently; each item's own stages run in order, with **no barrier between stages** — the default for multi-stage fan-out. Each stage gets `(prev, originalItem, index)`. |
| `phase` | `phase(title, {budget?}) => void` | Labels the group subsequent `agent()` calls fall under, for progress display; optional soft call-count sub-budget. |
| `log` | `log(message) => void` | User-visible progress line. Prefer this over `console.log` (routed into it anyway). |
| `args` | `args: unknown` | The only input channel into the script — whatever was passed at invoke time. |
| `budget` | `budget: { total, spent(), remaining() }` | See "budget", below. |
| `workflow` | `workflow(nameOrScript, childArgs?) => Promise<unknown>` | Runs another saved workflow inline, one nesting level deep, sharing this run's limiter/budget. |

A dead agent — crashed pane, exhausted retries, a recoverable error — resolves
to `null` rather than throwing. **Always guard before using a result**:
`(reply && reply.field) || fallback`, or `.filter(Boolean)` on an array of
results from `parallel`/`pipeline`.

### `agent()` options

```js
await agent(prompt, {
  kind,        // which CLI: "claude" | "codex" | "cursor" | ... — see below
  ssh,         // which computer: a name `ssh` already accepts, or omitted
  label,       // names this call in logs, the journal, and the Herdr pane tab
  schema,      // a plain JSON Schema object — turns the reply into structured
               // data instead of a string. Not a builder; the script never
               // imports anything, so this is a literal object.
  model,       // passed to the CLI as --model, verbatim (e.g. "opus")
  tier,        // coarse model name, used when model is omitted — also resolves through --model
  effort,      // passed to the CLI as --effort, verbatim (e.g. "high")
  isolation,   // "worktree" — see "Isolation", below
  cleanup,     // default true — false leaves this call's tab open when it
               // finishes, instead of the usual auto-close — see below
});
```

## `kind` and `ssh`: the two things Claude Code's dialect doesn't have

```js
const review = await agent("Review the diff.", { kind: "codex" });    // which CLI
const built = await agent("Implement it.", { ssh: "linux-box" });     // which computer
```

**Omit both by default** — kind defaults to `claude` (or the invoke object's
`kind`), and omitting `ssh` runs the call on this computer. `ssh` is a name
that already works with `ssh` in your terminal. There is no inventory file
and no tag selectors.

`kind: "cline"` is always rejected, in any spelling herdr would accept as
cline: herdr has no idle-detection rule for it, so the call could never
finish. `model` and `effort` are handed to the CLI verbatim as `--model` /
`--effort`, so the CLI — not this engine — decides whether a name is real.

## `budget` counts agent calls, never tokens or money

Herdr has no token signal. The `{ total, spent(), remaining() }` shape is
unchanged from Claude Code's dialect, but `spent()` counts agent calls (one
per attempt), not tokens. There is no run-wide cap to configure, so
`budget.total` is `null` and `remaining()` is `Infinity` by default; the real
knob is `phase(title, { budget: n })`, which caps that phase at `n` agent
calls. Wall-clock is reported (the envelope's `durationMs`), not capped. If
the user asked to cap *cost*, say so explicitly — this engine caps breadth,
not spend.

## The quality stdlib

Six more globals, all built purely on top of `agent()`/`parallel()` — nothing
privileged about them, just reusable patterns so scripts don't hand-roll them:

| Global | Signature | What it does |
| --- | --- | --- |
| `verify` | `verify(item, {reviewers?, threshold?, lens?})` | Spawns N independent adversarial reviewers, each voting `real: boolean`; accepts if the `real` fraction clears `threshold`. |
| `judgePanel` | `judgePanel(attempts, {judges?, rubric?})` | Scores each candidate 0–1 with N judges per candidate on `rubric`, returns the highest-mean attempt (ties by index). |
| `loopUntilDry` | `loopUntilDry({round, key?, consecutiveEmpty?, maxRounds?})` | Repeats `round(roundIndex)` until N consecutive rounds produce no new keys — for open-ended discovery (bugs, edge cases) where a fixed count would miss the tail. |
| `completenessCheck` | `completenessCheck(taskArgs, results)` | One critic agent that lists what's still missing from `results` given `taskArgs`. |
| `retry` | `retry(thunk, {attempts?, until?})` | Re-runs `thunk(attempt)` until `until(result)` passes or attempts run out. `until` is synchronous. |
| `gate` | `gate(thunk, validator, {attempts?})` | Like `retry`, but `validator(result)` returns `{ok, feedback?}` and `feedback` is threaded into the next attempt. |
| `checkpoint` | `checkpoint(promptText, options?) => Promise<unknown>` | A human gate: journaled and replayable like `agent()`, but consumes no agent budget. Headless runs take the declared default rather than hanging. |

## Isolation is cheap here, and usually right

`isolation: "worktree"` is flagged as expensive in Claude Code, because there
it's extra setup on top of a shared session. Here every call already gets its
own pane, so a worktree is the marginal cost of one `git worktree add`. Use it
whenever agents in the same `parallel()`/`pipeline()` write files — two agents
editing one checkout is a data race the engine cannot fix. (A worktree only
exists on this computer, so combining `isolation` with `ssh` is an error.)

## `cleanup: false` keeps one call's tab open for inspection

By default every tab closes the moment its call finishes, and the run's
workspace closes with it — nothing lingers in your sidebar to clean up by
hand. Set `cleanup: false` on a specific `agent()` call to leave that one tab
open instead, e.g. a review worth reading afterward rather than just trusting
its return value:

```js
const review = await agent("Review the diff for security issues.", { cleanup: false });
```

The workspace then survives the run's own teardown too — closing it, and
everything inside it, becomes something you (or another tool) do explicitly
in Herdr, not something this engine does for you. It applies to every attempt
of a retried call, not just the last one — a failed attempt gets a tab of its
own worth inspecting too, and there's no way to know in advance which attempt
will turn out to be the final one.

## Where to go next

- `reference/patterns.md` — composing `pipeline()`/`parallel()`/the quality
  stdlib for real tasks: when a barrier is actually justified, looping until
  you have enough instead of a fixed count, varying `kind`/`ssh` inside a
  fan-out, hand-rolled adversarial verify, and how to inline an existing
  skill's instructions into an `agent()` prompt when the subagent CLI won't
  have that skill installed.
- `reference/*.js` — one runnable example per pattern above. When asked to
  write a new workflow, start from whichever is closest to the shape of the
  task and adapt it, rather than writing the script shape from memory.
