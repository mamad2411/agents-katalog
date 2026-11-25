---
name: plan-slices
description: >-
  Use after the bootstrap, when asked what to build first, to order or size the work, or
  before splitting it between agents or people. Vertical slices per bounded context ordered,
  with owners, in docs/architecture/slices.md.
argument-hint: "[context, or nothing for all]"
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash(npx ddd-ts-kit list *)
  - Bash(npx ddd-ts-kit status)
  - Bash(npx ddd-ts-kit plan-waves)
  - Bash(npx ddd-ts-kit plan-waves *)
  - Bash(npx ddd-ts-kit story-check *)
  - Bash(npx ddd-ts-kit cited *)
---

# Plan the slices

Scope: `$ARGUMENTS`

Inputs: `docs/architecture/discovery.md` (the timeline) and `npx ddd-ts-kit list`
(what exists). Output: `docs/architecture/slices.md`. The order is the owner's decision.

## 1. Cut

A **slice** is one use case of one context, end to end: the behaviour of the aggregate, the
command or query handler, the route, their tests. It fits one commit of reasonable size
(skill `ddd-ts-kit:commit-discipline`) and leaves the project green. Each row of the
discovery timeline is a candidate; a reaction to an event of another context (a policy) is a
slice of the context that reacts.

A slice that changes what is already built (a route answers otherwise, a state gains a step,
an event carries more) adapts, in the same row, the tests that hold the former behaviour: the
specs, the end-to-end specs and the acceptance tests of the stories already delivered. Never in
a row at the end of the milestone: until then, the merge of the row turns them red.

Three kinds of rows, because they do not have the same owner:

| Kind | What | Owner |
|---|---|---|
| `contract` | an integration event or a read contract that another context will consume | conductor, before the consumers start |
| `skeleton` | an aggregate with its repository, a scheduled job, a policy, a gateway: the generators that write shared files (`npx ddd-ts-kit generate --help --json`, `writesShared`) | conductor |
| `slice` | a use case, a reaction (`integration-handler`, `event-handler`), a query | the worker of the context |

## 2. Order

1. **Walking skeleton**: the thinnest path through the core context that a user can call
   (one command, one route). It proves the stack.
2. **Contracts**, upstream first, following the context map: what a downstream waits for.
3. **By value** inside each context; core before supporting before generic.

`Depends on` names row ids. A slice depends on the skeleton of its aggregate and on the
contracts it consumes, never on a slice of another context: if it does, a contract is
missing. Rows with no path between them can be built in parallel.

## 3. Write the artefact

```markdown
# Slices

| # | Context | Kind | Slice | Start with | Depends on | Owner | Status |
|---|---|---|---|---|---|---|---|
| US1.01 | ordering | skeleton | Order | `generate aggregate ordering Order` then `generate repository ordering Order` | | conductor | todo |
| US1.02 | ordering | contract | Order placed | `generate integration-event ordering Order Placed` | US1.01 | conductor | todo |
| US1.03 | ordering | slice | Place order | `generate command ordering PlaceOrder --aggregate Order --creates --permission order.place --grant customer`; `generate route ordering PlaceOrder --method POST --path /orders` | US1.01, US1.02 | ordering | todo |
| US1.04 | billing | slice | Invoice a placed order | `generate integration-handler billing ordering ordering.order.placed` | US1.02 | billing | todo |
| US1.05 | incidents | slice | Open an incident | `generate command incidents OpenIncident --module triage --aggregate Incident --creates --permission incident.open` | US1.01 | incidents | todo |
| US1.06 | ordering | slice | Track order | `generate query ordering TrackOrder --permission order.track --term "Track=Follow where a placed order stands"`; `generate route ordering TrackOrder --method GET --path /orders/:id/tracking`; `generate representation ordering TrackOrder xml` | US1.01 | ordering | todo |
```

- Every aggregate a command row names has a `skeleton` row that generates the aggregate **and its
  repository** (`generate repository <ctx> <Aggregate>`, no flag: it reads the aggregate, and
  writes the event store adapter, with no table, when it is event-sourced:
  `generate aggregate <ctx> <Aggregate> --event-sourced`, which needs `stack.eventSourcing` on).
  The command rows depend on it. A worker runs `generate command` with `--local-only`, which
  refuses the command that would create the missing repository (it writes shared files).
- Erasing a person is no row for an event-sourced context: `privacy:erase` destroys the key of
  the subject, which erases its sealed values (`personalData`), and `generate erasure-handler`
  refuses it. Plan `erasure-handler <ctx>` only for a context with a table
  (`generate repository <ctx> <Aggregate> --personal ...`) that runs as a service of its own; a
  retention date on an event-sourced context is a `job` row whose command destroys the key.
- A job or an integration event that a row needs is a conductor row of its own (`skeleton` for
  `generate job`, `contract` for `generate integration-event`), planned before the row of the
  worker, which depends on it: a worker's `--local-only` run of either is refused because both
  write shared files. The worker merges the trunk, then fills the TODOs.
- `Start with` holds the exact generator commands (without `npx ddd-ts-kit` and `--json`), so
  the worker runs them instead of working them out. Every command or query names its
  permission or `--public`. A read that takes criteria, a scope or a page is named `Search...`,
  never `List...` (`naming/search-not-list`: the generator refuses `List...`).
- A command of a kind held to the glossary (`heldToGlossary: true` in
  `npx ddd-ts-kit generate --help --json`, the kinds whose usage shows `--term`) adds the term
  for a word of its name the glossary does not define (`--term "<Term>=<meaning>"`). The kinds
  whose `heldToGlossary` is false (`builder`, `test-world`, `property`, `vocabulary`,
  `repository`, `port`, `route`, `controller`, `route-group`, `guard`, `representation`, `form`,
  `schema`, `personal-fields`, `erasure-handler`, `acl`, `e2e`, `acceptance`, `gateway`,
  `adapter`, `service`, `worker`, `adr`) take no `--term`, which the generator refuses: what they name is read from the
  concept they serve, or was named by an earlier command.
- The commands of a row run in the order written, each after the command that writes what it
  builds on, as the summary of its kind says (`After generate ...`): the aggregate before its
  repository, its builder, its state machine and the command that names it with `--aggregate`;
  the command or query before its route; the route before its `representation` and its `form`; a
  port before its adapter; the integration event before its handler and its projection; the
  command before the job that sends it. That order inside a row is the row's own business:
  `plan-waves` says `put <command> first` when a row breaks it, and names the row to add to
  `Depends on` when a command builds on the file of another row.
- When `contexts.<name>.modules` of `ddd-ts-kit.config.json` is not empty, each row of that
  context names its module, and every generator command of the row whose usage shows
  `[--module <module>]` (`npx ddd-ts-kit generate --help --json`, `writesInModules: true`)
  carries `--module <module>`: aggregates, entities, value objects, domain events, errors,
  domain services, repositories, commands, queries, ports, adapters, gateways, ACLs, routes,
  policies, integration events and handlers, jobs and projections included. The generator
  refuses such a command of that context without it. The generator itself keeps at the level of
  the context what belongs to no module: the codes and permissions at its root, and in its
  `shared/` folder the schema of the database, route groups, guards, shared schemas, worlds and
  the fakes and builders of no module. The kinds that write only those (`test-world`,
  `route-group`, `guard`, `schema`), an `e2e` spec and a `service` refuse `--module`, so their
  commands never carry it; `builder` takes it, a builder following its aggregate. A row that serves two modules is split,
  one row per module.
- `--grant <role>` is written only when `stack.authz` is `rbac`. On `rebac` or `abac` the right
  is decided by the relationship schema or a policy, never by `--grant`: the generator refuses it.
- `Context` is a context of the project; `platform` (the work of `src/platform/`) and `all` (a slice
  across every context) are the two names for a row that belongs to none, owned by the conductor.
- `Owner` is `conductor`, the name of a context (one worker per context) or a person.
- `Status` is `todo`, `in progress`, `done`. A row is `done` when the started application does
  what it says, not when the specs on fakes pass: `check` must report no `authz/granted`,
  `authz/system-actor-granted` nor `scheduling/job-registered` for the permission, job or system
  actor the row adds. Only the conductor edits this file: a worker
  reports, the conductor marks the row at the merge. A story or a milestone is closed when
  `npx ddd-ts-kit story-check <code>` exits 0: its rows are `done` and no marker of its own is
  left, a marker being its own when its text or the commit that wrote it names one of its rows
  (skill `ddd-ts-kit:quality-gate`). `status` names a story whose rows are all done while
  markers of its own keep it open.
- Keep the eight column names as they are: `npx ddd-ts-kit status` reads every table with this
  header, in the order of the file (slices by status and by owner), and `worker-scope` puts the
  `todo` rows of an owner in its briefing. One table per story or milestone is fine.
- `#` is the code of the story or milestone, then a number within it: `US5.03`, `M2.07` (the
  code is the id without its last `.<number>`: `story-check US5` reads the rows `US5.*`). Never
  one sequence across stories: when a story is cut or a row inserted, the numbers after it
  slide, and the ids that briefings, commits, reports and `Depends on` carry stop meaning the
  same row. An id is written once and never renumbered; a row added later takes the next free
  number of its story, a row removed leaves its number unused. `status` names an id used twice
  and an id that is a bare number.
- Keep rule details out of the table: under it, one line per slice that needs it,
  `- #<id>: <invariants and failures by name>` (`- #US1.03: refuses an order without lines`), and
  for a row that changes a delivered behaviour, the tests it adapts
  (`adapts test/e2e/place-order.e2e.spec.ts`). `worker-scope` puts that line in the briefing
  of the row.
- A design worked out before a row is built (a design review) lives in
  `docs/architecture/reviews/<topic>.md`, one heading `## #<id> <slice>` per row, every code
  name in backticks: the section belongs to that row, and `worker-scope` names it under the row.
  Before committing a review, run `npx ddd-ts-kit cited --rows <ids> --base origin/main`: it
  lists the names the review cites that the trunk removed, refuses or replaced, with what took
  their place. Write the name the trunk has.

A story states what its client observes once it is built, before any row is built: its
acceptance criteria in `docs/architecture/stories/<story>.md`, under `## Acceptance criteria`,
`- AC1: ...` each. Its acceptance spec (`generate acceptance <story>`, skill `ddd-ts-kit:testing`)
is written, wrapped in `pending(...)`, locked and committed before the first row of code;
`npx ddd-ts-kit acceptance <story> --gate written` says when. Each `slice` row is named by at
least one scenario: a row no client can observe is a `skeleton` or a `contract`.

Then run `npx ddd-ts-kit plan-waves`, and commit the plan only once it exits 0. It refuses a cycle
in `Depends on`, an id no row carries and a row without owner. It then replays the generator
commands of the rows, in a copy of the project and in the order of the waves, and refuses each
name a command introduces whose words the glossary of its context does not define, counting the
`--term` of the row and of the rows it waits for: add the `--term` it names to that row, or to a
row it depends on, rather than renaming against the glossary. It refuses just as well, with exit
1, each command the generator refuses for another reason (`refused-command`: a missing `--module`
in a context divided into modules, `--grant` where the rights are not roles, an aggregate no
earlier row generates), the refusal and the fix of the generator printed under the row: fix the
row as it says, and when it names the rows that generate what the command builds on, of its
context or of another, add each to `Depends on` (or move the command, when that row waits for this
one). It refuses as well a
command that builds on a file a row it does not wait for generates (`missing-dependency`), which
the replay found only because it runs every row in one copy: add that row to `Depends on`. A row
`in progress` is replayed but its refusals are listed apart, and neither its names, nor its
refusals, nor what it builds on are counted, its commands having run already and its worker
holding its terms. When a refused command also says `then:`, fix
that second refusal in the same pass. Otherwise it shows the rows in waves (wave 1 can start now), cut into
batches of one or two rows that `parallel-work` hands out, each row with the status of the rows it
waits for, and apart the rows of another story that it waits for. A batch it says names no aggregate
gets one in `Start with` (`--aggregate <Name>`, and `--creates` when the slice is the birth of that aggregate) when the slice works on one.

Aim for slices of half a day at most. A slice with more than two failures to handle, two
aggregates or two routes is two slices.

## Done when

Put this to the owner: **can each slice be built, verified and merged on its own, in this
order, and does every row have one owner?** On a yes, build with `ddd-ts-kit:use-case`, row
by row, or hand out with `ddd-ts-kit:parallel-work`.
