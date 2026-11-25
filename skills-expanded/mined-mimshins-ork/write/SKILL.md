---
name: write
description: Use when writing or changing an Ork workflow (a `.ork/workflows/*.ork.yaml` file) - its nodes, edges, conditions and loops - and checking each draft until Ork accepts it.
---

# Writing an Ork workflow

An Ork workflow is one YAML file in the project, `.ork/workflows/<name>.ork.yaml`.
It names the nodes (Claude sessions, programs, a person's decisions) and the
edges that carry work between them. Ork runs it on the person's machine with
their own accounts.

## How to work

1. **Look first.** Ork's `workflows` tool lists the project's workflows; read
   one that's close. `agents` lists the agents a node can use. Before you split
   the work, read `/ork:principles`: a program where a program will do, a
   session only for judgment.
2. **Don't guess a field.** `workflow_format` gives the format; ask it for one
   node type (`nodeType: "human.gate"`) to see that type's fields.
3. **Check every draft** with Ork's `check` tool (`text`, or `workflow` for a
   file), and fix what it says until it has no error. Read its warnings: they
   mean something. Without Ork's tools, run `ork validate <file>`.
4. **Then save the file**, beginning with the schema line below, so editors can
   check it too.

## The shape of a file

```yaml
# yaml-language-server: $schema=https://raw.githubusercontent.com/mimshins/ork/main/packages/schema/workflow.schema.json
schemaVersion: 1
name: fix-and-ship
description: Fix a failing test, check it with the test suite, and ask before opening a pull request.
inputs:
  issue:
    type: string
    required: true
    description: What fails.
defaults:
  model: claude-code.sonnet
  budgetUsd: 2
limits:
  budgetUsd: 10
nodes:
  fix:
    type: agent.worker
    prompt: "Fix this, and keep the change small: {{inputs.issue}}"
  tests:
    type: tool.shell
    command: pnpm test
    allow: [pnpm test]
  ask:
    type: human.gate
    question: "Open a pull request for {{nodes.fix.output.branch}}?"
    options: [open, hold]
    recommended: hold
  pr:
    type: tool.gh
    command: pr create --fill --head {{nodes.fix.output.branch}}
    allow: [pr create]
edges:
  - fix -> tests
  - from: tests
    to: fix
    when: "!ok"
    maxRounds: 2
  - from: tests
    to: ask
    when: ok
  - from: ask
    to: pr
    when: "choice == 'open'"
```

Node ids are lowercase: letters, digits, `-` and `_`. Secrets never go in the
file: a tool reads one with `env:` and `{{env.NAME}}`.

## Nodes

| Type                              | Does                                                                |
| --------------------------------- | ------------------------------------------------------------------- |
| `agent.worker`                   | An agent session that does one task and reports                     |
| `agent.leader`                   | A session that plans and delegates to the nodes it owns (`parent:`) |
| `agent.subagent`                 | A subagent inside its parent's session; it takes no edges           |
| `tool.shell`                      | Any program, run without a shell; `allow:` lists command prefixes   |
| `tool.git`, `tool.gh`, `tool.aws` | The person's own `git`, `gh`, `aws`, with an allow list             |
| `mcp.call`                        | One tool call on an MCP server, with no session                     |
| `human.gate`                      | A question with options and a recommended one                       |
| `control.join`                    | Waits for its inputs: `all` (default), `any`, or `n` of them        |
| `control.router`, `control.split` | Pass their input on; a router takes its first matching edge         |
| `workflow.call`                   | Starts another workflow as its own run                              |

A `model` may start with its driver (`claude-code.opus`,
`open-code.anthropic/claude-sonnet-5-5`); the node then runs on that tool, and
needs no `driver`. A file with the old `claude.worker`, `claude.leader` or
`claude.subagent` types needs `ork migrate`.

A worker, tool node, `mcp.call` or `workflow.call` can run once per entry of a
list: see [One node per item](#one-node-per-item).

- **An agent node reports** `status` (`pass`, `changes_requested`, `done` or
  `fail`), `summary`, `artifacts`, `branch`, and any field its `output.schema`
  declares, such as `verdict: [approve, escalate]`. For another verdict, declare
  a field: `status` can't take other values.
- **A tool node reports** `exitCode`, `stdout`, `stderr`, and with
  `output: { format: json, schema: { state: [OPEN, CLOSED] } }` its JSON as
  `json`. Declare the fields you read: a run then checks them, and a typo can't
  pass.
- **A gate reports** `choice` and `answeredBy`. A `timeout` needs a `default`.

## Edges and conditions

- `a -> b`, `a -> b, c`, `b, c -> j` are plain edges, taken when the source
  succeeded. A failed node takes no plain edge: handle a failure with
  `when: "!ok"`, or `status == 'fail'` on an agent node.
- `{ from: a, to: b, when: "..." }` is taken when the condition holds. A bare
  name reads the source's output: `when: "verdict == 'approve'"`. Quote any
  condition that starts with `!`, or YAML reads it as a tag.
- Conditions have `==`, `!=`, `<`, `>`, `&&`, `||`, `!`, and `any`, `all`,
  `count`, `len`, `contains`. A join's `statuses` suits `any(statuses, 'fail')`.
- A node runs when any edge into it is taken; only a join waits. A node with no
  way in taken is skipped, and so is what follows it.
- Templates, `{{inputs.x}}`, `{{nodes.a.output.field}}`, `{{run.id}}`, go in
  `prompt`, `instructions`, `command`, `cwd` and `question`, and in an agent
  node's `model` and `effort` (read when its session starts, so a script node
  can pick the model). Each value stays one argument of a command, so it can't
  inject one.

## One node per item

`forEach` runs a worker, a tool node, an `mcp.call` or a `workflow.call` once
per entry of a list, with no model turn to fan out or gather. Not a leader, a
gate, a subagent or a control node.

```yaml
plan:
  type: agent.worker
  prompt: "Split this into at most 6 independent tasks: {{inputs.goal}}"
  isolation: readonly
  output:
    schema:
      tasks:
        list: { title: string, detail: string } # declare the list and its shape
build:
  type: agent.worker
  prompt: "Task {{index}}: {{item.title}}. {{item.detail}}"
  isolation: worktree
  forEach:
    from: "{{nodes.plan.output.tasks}}" # exactly one path to a declared list
    maxItems: 6 # required with `from`: the cap on sessions started
    maxParallel: 3
```

- `forEach: { items: [a, b] }` takes a list written in the file instead.
- `{{item}}` and `{{index}}` work only in a node with `forEach`, in `prompt`,
  `command`, `arguments`, `inputs`, `env` and `ref`, and `{{item.<field>}}` in a
  agent node's `model` and `effort`. A program also gets `ORK_ITEM` and
  `ORK_INDEX`.
- The next node reads `items`, `results` (each item's output, `summary`,
  `branch`), `statuses` and `count`: `{{nodes.build.output.results}}`,
  `when: "all(statuses, 'pass')"`. Items follow no edges; the node does.
- `onFailure: finish` (default) runs every item; `stop` starts no more after a
  failure. A list over `maxItems` makes Ork ask a person.
- Declare the source's `list`, or `check` warns `forEach.undeclared`. Fix
  `forEach.not-list`, `forEach.order` and `item.field` errors; they name the
  field or node.

## Loops

Every cycle needs an edge with `maxRounds`. Give the way back a condition and
the way out its opposite, as `!ok` and `ok` above; a plain edge beside a loop
fires every round. When a loop runs out, Ork asks a person what to do.

## What `check` refuses, and why

- **A value the source can't have** (`when.value`): `status == 'failed'` (it's
  `fail`), a gate's `choice == 'aprove'` for `approve`, a value outside a
  declared list. The message names the values it can have.
- **A loop no condition ends**, a plain edge beside a loop, a loop of sessions
  with no `limits.budgetUsd` or `limits.timeout`: warnings, each worth fixing.
- **`no way the walk tried reaches x`**: Ork tried every way through, and none
  got to `x`. A join waiting on a branch a first-match router never takes is
  the usual cause.
