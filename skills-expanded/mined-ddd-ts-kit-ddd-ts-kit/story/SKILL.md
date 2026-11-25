---
name: story
description: >-
  Takes one user story to a green pull request in its own worktree: questions first, then
  the story file, its rows, a design review, acceptance tests locked before code, one
  context-builder per row, review, verification. Run by the user with /ddd-ts-kit:story.
argument-hint: "<story code> [--headless] [the story in plain words, a file, an intent, or a tracker key]"
disable-model-invocation: true
allowed-tools:
  - Read
  - Write
  - Edit
  - Skill
  - Agent
  - AskUserQuestion
  - Bash(npx ddd-ts-kit *)
  - Bash(cd * && npx ddd-ts-kit *)
  - Bash(cd * && npm run *)
  - Bash(cd * && npm test *)
  - Bash(cd * && git *)
  - Bash(git worktree *)
  - Bash(gh pr create *)
---

# Take one story to its pull request

Story: `$0`. Statement: `$ARGUMENTS`

You are the conductor of this story and of nothing else. The owner answers once, at phase 1;
from phase 2 on you do not stop to ask: a question becomes a provisional decision, recorded, and
the report puts it back to the owner. `npx ddd-ts-kit story $0` says at any time where the
story stands and what is next; the guard of the plugin keeps the code of the contexts closed
until phase 5 is met. Reading costs: [../start/token-economy.md](../start/token-economy.md).

## 0. Its worktree

From the checkout of the trunk, after `git fetch`: `npx ddd-ts-kit story-scope $0`, with
`--from <file>` when `$ARGUMENTS` names an intent (`docs/architecture/intents/<slug>.md`,
written by the `intent` skill and accepted by the owner: `story-scope` refuses one whose header
is not `Status: accepted`) or an incident record (`docs/architecture/incidents/<id>.md`). It opens
`.worktrees/<story>` on `story/<story>`, cut from the branch the trunk follows (`origin/main`)
when it has one (or finds it again: the story resumes where it was left), installs it, records
the origin in `.ddd-ts-kit/story.json`, and names the other stories open in the repository with
the contexts they change. From now on every
command is `cd <worktree> && ...` and every file is written by its absolute path under the
worktree. A story it names on the same contexts is being built in another terminal: read its
rows before you cut yours, and keep yours off its aggregates when you can.

## 1. Every question, at once

The statement is `$ARGUMENTS`: plain words, a file to read, or the key of a ticket a connector
of the session can read. An intent seeds the story: its `## Problem` and `## Proposed outcome`
become `## Statement`, word for word; each line of its `## Constraints` is listed under
`## Questions` as answered "by the intent"; its `## Open questions` join the questions below;
each line of its `## Acceptance, as the author would observe it` is the first draft of a
criterion, rewritten as what a client observes through the API; its author and status go on
the `From:` line of `## Origin`. Read `docs/architecture/plan.md`, the `CONTEXT.md` of each
context the story touches and `npx ddd-ts-kit describe <context>`, once each. List every question
whose answer changes an artefact of the story: a business rule you would have to guess, who
holds a permission, a word missing from a glossary, a criterion that cannot be observed, a
boundary or a relationship between contexts. Ask them in one go with AskUserQuestion (four per
call, your recommended option first, its cost said); none that changes nothing. Then copy
[story-template.md](story-template.md) to `docs/architecture/stories/$0.md` and fill it: the
statement, each question with its answer, the acceptance criteria (`- AC1: <what a client
observes>`, each one observable through the API), and `## Origin`, the record an auditor reads
first: `From:` where the story comes from (the intent path, the ticket key or the incident id
of `$ARGUMENTS`, with who accepted it when the file says); `Built with:` the kit version
(`npx ddd-ts-kit --version`, or the one the guard printed at session start), the plugin version
(`version` of `../../.claude-plugin/plugin.json`, next to this skill), the base and its commit
(`base` and `baseCommit` of `.ddd-ts-kit/story.json`); `Policies in force:` filled at phase 3.
`story $0 --gate close` refuses a story without its `From:` and `Built with:` lines.

A boundary, a new context or a relationship pattern is a strategic decision of the owner:
asked here, never decided later. If one appears after this phase and no reversible option
exists, it is the one reason to stop: write the report (phase 8) with the question, then stop.

## 2. Its rows

Skill `ddd-ts-kit:plan-slices` for this story alone: rows `$0.01`, `$0.02`, ... in
`docs/architecture/slices.md`, contracts and skeletons first, each `slice` row a use case one
agent builds in one context. Glossary terms the rows need go in the `CONTEXT.md` of their
context now (the guard leaves it open). Before cutting them, `npx ddd-ts-kit stories`: the
other open stories, the contexts and files they change, what merging their branch into yours
would leave to settle by hand. Keep your rows off what they change when the story allows it;
otherwise record which story lands first as a decision.

## 3. A design review of each row

In `docs/architecture/reviews/$0.md`, one `## #<id> <slice>` section per row: the aggregate and
its invariants, the command or query and its permission, the events, the errors by business
name, the route, the ports, what it reads from another context and through which contract, the
specs it changes; every class, method and path in backticks. The policies of the project are
skills: those of the plugin (`ddd-ts-kit:access-control`, `ddd-ts-kit:persistence`,
`ddd-ts-kit:cross-cutting`, `ddd-ts-kit:testing`) and the project's own under `.claude/skills/`.
Load the ones the rows need, list them on the `Policies in force:` line of `## Origin`, and in
the section of a row write `Policies: <skill>: <what it imposed here>` whenever a policy changed
the design (a permission it required, a port it moved, a field it masked); when two policies
contradict each other, write both and the choice as a decision `D<n>`. Then launch the
`architecture-reviewer` agent on that file as a design review of rows still to build; it reads
the `Policies:` lines as part of the design. Its blocking findings change the design; a
non-blocking one is settled at once or becomes a decision `D<n>`. `npx ddd-ts-kit cited --rows <ids> --base <base>` lists the names the design
cites that the trunk replaced: write the name the trunk has.

A criterion that states a law over every value of a value object, rather than a case ("never
negative", "the total equals the sum of its lines", "overlaps the other in both directions or in
none", "a parse then a format gives the value back"), gets a line in the section of its row:
`Laws: <ValueObject>: <the law, as a test title>`. It stays a criterion with its scenarios in the
acceptance; the law is the spec of the value object, stated on generated values when the row is
built. A law catches the bound or the symmetry an example misses.

## 4. The acceptance, before any code

Skill `ddd-ts-kit:testing`, `acceptance.md`: `npx ddd-ts-kit generate acceptance $0`, one
or more scenarios per criterion wrapped in `pending(...)`, `npm run test:e2e -- test/acceptance`
to see each fail on an assertion, `npm run format` and `npm run lint -- test/acceptance/<spec>`
on the spec (`--lock` refuses a spec that fails them, and a locked spec is not touched again),
`npx ddd-ts-kit acceptance $0 --lock`. Commit the story file,
the rows, the design review, the acceptance and its lock: one commit,
`docs($0): specify, design and accept the story`.

## 5. The build gate

`npx ddd-ts-kit story $0 --gate build` passes: the guard opens the code of the contexts. It does
not pass: do what its `Next:` line says, never write around it.

## 6. Build, row by row

In the order of `npx ddd-ts-kit plan-waves`, one row at a time, each started with `git fetch`
and `npx ddd-ts-kit stories` (a conflict for you with the trunk is brought in now, with
`merge-trunk`, while it is small). A row of another story it lists under `Rows another story waits
for, not done` is not yours to build: the rows waiting on it start once it is done on the trunk;
tell the owner when no open story carries it.

- a `contract` or `skeleton` row: yourself, with its generator commands, then
  `npx ddd-ts-kit verify-slice <context> --since <base>` and its commit;
- a `slice` row: `npx ddd-ts-kit worker-scope <context> --here --rows <id>` in the worktree, then
  one `ddd-ts-kit:context-builder` agent with the briefing it prints, the worktree path and
  this line: "Commit on the current branch; do not merge, do not push." When `commit.agentTrailer`
  of `ddd-ts-kit.config.json` is `true`, add: "End each commit message with the trailer
  `Agent: <host> ddd-ts-kit@<plugin version> context-builder`" (the host as it names itself,
  `claude-code`; the version from `## Origin`), and end your own commits with the same trailer,
  `story` as the agent name. When the section of the row has a `Laws:` line, add: "State each
  law of the `Laws:` line of `docs/architecture/reviews/$0.md` as a property:
  `npx ddd-ts-kit generate property <context> <ValueObject> --local-only`, the law its title."
  Read its report, the final message of the agent. A `SubagentStop` hook writes it to
  `.ddd-ts-kit/report.md` of the worktree; when that file is missing after the agent returns, write
  it yourself from the final message, for `worker-scope --resume`.
  A blocking need (a contract field, a dependency, a grant, a migration) is yours: do it, commit
  it, launch the next agent on the same row. A scenario it says is wrong is compared with its
  criterion (skill `ddd-ts-kit:testing`): never changed to make code pass.
  An agent that stopped is resumed with `npx ddd-ts-kit worker-scope <context> --resume --worktree .`.

After each row: `npm run test:e2e -- test/acceptance/$0`, the row marked `done` in
`slices.md` in its own commit, `npx ddd-ts-kit story $0`. A host without the agents of the
plugin builds each row itself with skill `ddd-ts-kit:use-case`.

## 7. Close

1. Bring the trunk in: commit, `git fetch`, then `npx ddd-ts-kit merge-trunk --trunk <base>`,
   resolve what it stops on keeping both sides, `--continue` (skill `ddd-ts-kit:quality-gate`,
   `merge-trunk.md`); on exit 3, hand the owner the command it prints and wait.
   A migration to generate (Prisma, TypeORM) or a spec against a real database exits 3 under the sandbox too (no setting reaches the database): the owner or the CI runs it.
   A `generate` or an `init --force` that exits 3 with the schema index under `left` left that index as it stood, to keep a table or a name; its note says what to write, move or restore by hand: hand them to a person with the note, the slice waits for them.
2. The `architecture-reviewer` agent on the branch (`--changed-since <base>`): blocking findings
   fixed, the others settled or written as the `TODO(review)` line the reviewer gives, and each
   line it gives for `## Mistakes seen here` of `AGENTS.md` (the rule of two) committed in this
   branch: skill `ddd-ts-kit:quality-gate`, `review-remarks.md`. Keep the review: append `## Findings`
   to `docs/architecture/reviews/$0.md`, one line per finding with its pass (the rule id or the
   principle the reviewer named), its `file:line` and its outcome, `fixed in <commit>`,
   `written as TODO(review)` or `dismissed by ADR-<n>`; the record outlives the pull request.
   Then the `story-verifier` agent, in a fresh context, with the story code, the worktree path
   and the base: it starts the application as the end-to-end tests do, exercises the routes of
   the rows and the two nearest flows, reads the design review and the report, and reports what
   does not match the design or a `D<n>`; it fixes nothing. Settle each mismatch it reports as
   a finding above: fixed, or a decision. A host without the agents of the plugin skips it, and
   the report says "not verified: the story-verifier agent, not available on this host".
3. `npm run verify`, `npx ddd-ts-kit acceptance $0 --gate passing`, `npx ddd-ts-kit todo --brief`, and
   `npx ddd-ts-kit story-check $0`: every row done, no marker of its own left.

## 8. The report, then the pull request

Write `## Report` in `docs/architecture/stories/$0.md`, short and in this order: what the story
delivers; each decision taken without the owner (`D<n>`, provisional: what, why, the
alternatives, where in the code); each compromise (what was left simpler than the design, and
why); each amendment of the acceptance and each criterion changed after the lock
with its verdict (`npx ddd-ts-kit acceptance $0` lists them); each `TODO(review)` left; then
`### Digest`, what `npx ddd-ts-kit digest --base <base>` prints once the last row is committed
(`<base>` the `base` of `.ddd-ts-kit/story.json`), pasted under it as printed: per context the
use cases, permissions and their grants, routes and their error codes, events and ports the
story changes, its new spec titles, its files to review in reading order and, apart, those the
kit regenerated, which the reviewer reads before the diff; then
`### Verification`, the evidence from the toolchain and not your word: the last lines of
`npm run verify`, of `npm run test:e2e -- test/acceptance/$0` and of `npx ddd-ts-kit
story-check $0`, pasted as they were printed, and `not verified:` for what could not run here
(a broker, a provider, a platform) and why; with `commit.agentTrailer` on, one line counting
the commits of the branch made by an agent (`git log <base>..HEAD --format=%B | grep -c
'^Agent:'`) against those made by hand. `npx ddd-ts-kit story $0 --gate close` passes. Commit, push the branch, and
`gh pr create` with the report as its body, `## Origin` repeated at its top: the record on the
trunk links back to the intent, the ticket or the incident; `/ddd-ts-kit:pull-request` keeps the
digest at the very top of the body afterwards. Give the owner the link and the
report, then stop. When the owner asks for the pull request to be taken to green, the next step
is `/ddd-ts-kit:pull-request <number>` from this worktree: it sweeps the review comments and
the failing checks under the rules of this story, and never force-pushes.

## `--headless`: the specification without an owner

With `--headless` in `$ARGUMENTS` (a job on the merge of an accepted intent, or a session
nobody attends), nobody answers at phase 1. Run phases 0 to 4 as above, with these
differences: every question that changes an artefact is written under `## Open questions` of
the story file, each with its recommended option, taken provisionally and marked
`(provisional, headless)` where it lands (a criterion, a row, a line of the design, a decision
`D<n>`); a boundary, a new context or a relationship pattern is written there too, with no
option taken, and the rows that depend on it wait. The acceptance is written and locked as at
phase 4; the build gate stays closed: no phase 5, no code. Commit, push, and `gh pr create`
with the list of `## Open questions` as the body, `## Origin` at its top. The owner answers in
the review, the pull request merges with the answers written into the story file, and the
build phase starts from them in a session that runs `/ddd-ts-kit:story $0` again, which finds
the worktree and the answers. Then stop.

## While working

- A question after phase 1: take the option easiest to undo, record it as `D<n>` under
  `## Decisions` (what, why, the alternatives, where), go on.
- Never lower a rule, skip a test, suppress a check or change a locked scenario to get to
  green: skill `ddd-ts-kit:deviation`; it is a decision for the report, not one to take.
- The guard says, once per file, when you write a file another open story changes too, and at
  session start where the stories meet and how far the trunk moved: keep the change to what the
  row needs, and say in the report which story lands first. The second to land settles the
  conflict with `merge-trunk`.
- The guard refuses to end the session before the report: a story that is truly blocked ends
  with a report that says what blocks it.
