---
name: kanban-card-run
description: 'Operate the project Kanban board: create, groom, start, move, review and complete cards through the board helpers, with owner decisions and lifecycle rules. Use when managing tasks or cards. RU: канбан, задачи, карточки, взять задачу, закрыть задачу.'
---

# Kanban cards

Use for starting, moving, grooming, reviewing or completing tasks on a project Kanban board. The first section is the full manual and script reference; the second adds the day-to-day operating rules.

## Kanban manual

### Stages

| Stage    | Canonical path              | Description                                                |
|----------|-----------------------------|------------------------------------------------------------|
| Grooming | `.agents/kanban/grooming/`  | Draft tasks with open questions / unresolved scope         |
| Todo     | `.agents/kanban/todo/`      | Refined tasks ready to start                               |
| Progress | `.agents/kanban/progress/`  | Currently being worked on                                  |
| Test     | `.agents/kanban/test/`      | Implementation handed off; review/QA in progress           |
| Ready    | `.agents/kanban/ready/`     | Evidence checkpoint; awaiting authorized finalization     |
| Done     | `.agents/kanban/done/`      | Authorized successful completion                          |
| Freeze   | `.agents/kanban/freeze/`    | Temporarily paused work awaiting its recorded return condition |
| Closed   | `.agents/kanban/closed/`    | Cancelled or superseded work; terminal archive             |

Lifecycle: `grooming → todo → progress → test → ready → done`.

New boards default to `.agents/kanban`. Resolve an existing board and its
`kanban.lock` through the project helper. Aliases to the same physical path are
one board; distinct conflicting boards or counters fail closed. For an existing
legacy board, consult [board compatibility](references/board-compatibility.md).

`freeze/` is a side state: enter from `grooming/`, `todo/`, `progress/`, `test/`,
or `ready/`; resume the same card only to `todo/` or `progress/` with
`--resume`. Record the pause reason and return condition in `**Decisions:**`.
`closed/` records cancellation/supersession, not successful completion; entering
it from any nonterminal stage, including `freeze/`, requires `--approved`.
`closed/` is terminal even with `--force`; future work gets a new linked card.
Both stages participate in board-wide ID uniqueness checks.

Autonomous runs never enter `grooming/`. `ready/` is a mandatory evidence and
verified local-commit checkpoint, not a compulsory human stop. Continue with
authorized actions when their action-specific authorization and gates pass.
The narrow `kanban-schedule-run` merge-at-ready exception preserves its exact approved
card allowlist and QA/review gates; the manifest alone does not authorize `done`,
push or deploy.

When the current user or applicable project workflow requires explicit user
approval for `done`, preserve that requirement. Standing profile or agent
authority is not a substitute for the required user approval.

### Authorization for automated lifecycle actions

`done`, merge, push, and deploy may and should proceed automatically when the
executing profile/agent already holds valid authorization for that specific
action, target project/task, and applicable limits, and all mandatory
acceptance, quality, review, and operational gates pass. Do not request another
user confirmation merely because execution is automated or a card reached
`ready`. Valid sources include explicit user approval at hand-off, recorded
EPIC-scoped upfront autonomous authorization for its named scope, other
recorded upfront task/workflow authorization, or recorded profile/agent authorization
(standing owner-approved authority assigned to that profile/agent). Existing
valid grants remain effective within their scope.

Check each action independently. Record the authorization source/reference,
executing profile/agent, covered actions and limits, target, and result in the
card. A profile name, credentials, green tests, or stage transition alone is
not a grant. This policy itself grants no production or release permission;
explicit task restrictions and native security/approval controls remain
binding, and a refusal must not be bypassed. `ready` does not imply `done`,
merge, push, or deploy authorization. `done` alone does not authorize merge,
push, or deploy; no grant extends to later EPICs or scope expansion unless it
explicitly includes them.

### IDs & Prefix

Every card carries `<PREFIX>-<NUM>` or a legacy letter-suffixed ID
`<PREFIX>-<NUM><LETTER>` (epic subtasks: `<PREFIX>-<NUM>-<NN>`, see Epics
below). Counters live in the committed `kanban.lock` beside the resolved board
root; allocation uses a companion `flock` marker and reconciles against cards
actually on the board on every allocation — a stale counter after a merge
can't hand out a duplicate ID. The ID parser preserves the optional letter, so
`K-094a` and `K-094b` are distinct IDs; slug words such as `css-grid` are not
prefix candidates.
**First use in a project (no `prefix=` yet) is a confirmation, never a
guess.** `kanban-id.sh next`/`prefix` exits 2 with the board's candidate
prefixes (existing board cards win by count if any, else a dir-name-derived
one) — on that exit, **ask the user** which to use via the runtime's available
question interface (present candidates and a recommendation), then run
`kanban-id.sh set-prefix <PREFIX>` to confirm it; don't auto-pick and don't
retry silently. Full mechanics, lock format, prefix registry →
[scripts.md](scripts.md).

The adjacent `.flock` file coordinates only processes that open the same
resolved lock file. Separate Git worktrees have separate tracked counters and
lock markers; until a shared allocator exists, one canonical board owner must
allocate IDs and perform lifecycle moves from the canonical checkout. Task
worktrees do not allocate IDs or mutate board stages.

### Scripts

Set `ROOT="${AI_AGENTS_SKILLS_ROOT:-${CLAUDE_PLUGIN_ROOT:-${PLUGIN_ROOT:-${CURSOR_PLUGIN_ROOT:-}}}}"` and
`S="$ROOT/skills/kanban-card-run/scripts"`, then invoke every script below as `"$S"/<name>` — never by bare name
(optional leading `--repo <path>`, default git toplevel):

| Script | Purpose | Key flag |
|---|---|---|
| `"$S"/kanban-id.sh` | allocate/inspect IDs (`next`\|`epic`\|`sub`\|`peek`\|`prefix`) | `sub <EPIC-ID>` |
| `"$S"/kanban-new.sh` | allocate ID + render template + stage card | `--epic`\|`--sub <EPIC-ID>` |
| `"$S"/kanban-move.sh` | validated stage transition (uses the bundled Git-aware path helper) | `--approved` for `→done`/`→closed`; `--resume` from `freeze/` |
| `"$S"/kanban-status.sh` | board overview, subtasks grouped under their epic | `--epic ID` |
| `"$S"/kanban-lint.sh` | card validation (shape, template, dupes, counter drift) | — |

Full CLI, flags, exit codes, worked examples → [scripts.md](scripts.md). Manual
fallback requires the resolved board's adjacent `kanban.lock`; if the Git-aware path skill is needed separately, ask the user to invoke it manually. Never bypass a native refusal.

### Task Lifecycle

#### 1. Create

- **Default:** `"$S"/kanban-new.sh --title "…" --stage todo` (or `--stage grooming` when scope isn't settled) — allocates the ID, renders [task template](task-template.md), stages the card, prints its path.
- **Manual fallback:** allocate the next ID by hand against the lock beside the resolved board root, fill in [task template](task-template.md), `git add`.
- **Scope clear** (AC, files, approach all settled) → `todo/`.
- **Open questions remain** → `grooming/`; list them in `**Open questions:**`.

##### Side-found or user-suggested findings

Distinguish a finding from authorization to change it. Fix it only when it is
within the active task or otherwise authorized; small size or suitability for a
subagent is not permission to expand scope. Before creating a new card, search
for a related card to avoid duplicates. Create or update a card or a project
scratch list only when that write is in scope and follows the board policy;
otherwise report the finding, location and evidence without mutating the board.
Preserve existing entries and project conventions. Summarize in-scope repairs
and unresolved findings in the handoff.

#### 1a. Groom (grooming/ → todo/)

Read the card's open questions and identify decisions needed for a safe,
implementable task. Resolve routine choices from the existing request and
project policy when those provide sufficient authority; record the rationale.
Ask the user only when a material choice or authorization is genuinely missing,
using an available runtime question interface, and continue independent work
where possible. Do not invent missing approval or silently decide a required
user preference. Record decisions and keep genuinely unresolved questions on
the card; move to `todo/` only when the applicable readiness criteria are met.

See [reference.md](reference.md) for the grooming protocol.

#### 2. Start (todo → progress)

- **Brief the user first (interactive starts).** Before moving the card to
  `progress/`, post a short, plain-language task briefing to the user **in the
  user's language**: what the task does and why, the acceptance criteria, the
  planned approach, and which files/areas it touches. It's a read-back so the
  user can catch a wrong card or misread scope before work starts — keep it
  concise and explained, don't dump the raw card. Skip only on autonomous/
  unattended runs (no user present, e.g. kanban-schedule-run).
- **From file**: move `.agents/kanban/todo/<task>.md` → `progress/`.
- **From description**: create from [task template](task-template.md) in `todo/`, then move to `progress/` (only if scope is clear).

#### 3. Implement (progress/)

- Read the task file. Plan and track appropriately scoped subtasks using the runtime interface available for this task.
- Add "Execution Log" section to the task file; update after each significant step.

#### 4. Test (progress → test)

Move card to `test/`. Run the QA checks required by the project's applicable instructions and test configuration.

#### 5. Ready (test → ready)

Auto-review passed + AC met + tests green → move to `ready/`. If review finds issues → stay in `test/`.
Use the canonical move helper, then refresh the latest ready-card body and any
remaining owned task files. Make the normal local wrap-up commit without a
separate permission request, using the configured named Git executor when
routing requires it. Verify the commit SHA, message, committed paths and
reviewed bytes, and confirm no task-owned changes remain uncommitted before
reporting the handoff complete. Do not require a globally empty worktree or
capture unrelated work. If Git, access, or a hook genuinely blocks the commit,
report `card ready; commit blocked` with evidence. Ready does not authorize
`done`, merge, push, or deployment.

#### 6. Done (ready → done) — authorized finalization

Authorization for `done` must be explicit current user approval, recorded
upfront task/EPIC/workflow authorization, or recorded profile/agent
authorization, and must cover this card. Record its source and scope. A grant
for `done` alone never implies merge, push, deploy, later-EPIC work, scope
expansion, or bypassing tests/review. Order matters — card first, merge last:

1. Move the card `ready/ → done/` (`kanban-move.sh <ID> done --approved`).
2. Verify the task branch is clean (`git status --short` empty — everything
   committed, nothing stray left uncommitted).
3. Only then squash-merge the branch into the default branch if merge is also
   authorized for this target (see Git Commits below).

If `done` authorization is missing, retain `ready/` and identify the missing
grant. In the normal finalization path, merge only after `done` and clean-branch
verification. If merge authorization is missing, retain the task branch and its
ready/done card and report that the canonical base still has the pre-merge state.
Archive-rename only after a successful, verified, authorized merge. Push and deploy
remain independently authorized actions; read back the exact target and verify
the expected remote revision or deployed version/state before reporting success.

**Narrow `kanban-schedule-run` exception:** a task may be squash-merged from `ready/`
while its card remains in `ready/` only when a valid hash-verified scope manifest
lists that exact card, the scope was approved before scheduling, and QA plus an
independent review passed. This exception permits merge-at-ready and chaining only
inside the manifest. The manifest by itself never grants `done`, push/deploy,
or overrides project-local rules. Those actions may proceed automatically only
under an independently valid action-specific grant and their required gates;
otherwise they remain pending. Do not require a `done` move to exercise this
explicit merge-at-ready exception.

#### Freeze and closed

- A card may enter `freeze/` from `grooming/`, `todo/`, `progress/`, `test/`, or
  `ready/`. Add its pause reason and return condition to `**Decisions:**`; lint
  does not require new headings for these notes.
- Resume from `freeze/` to `todo/` or `progress/` only with
  `kanban-move.sh <ID> <stage> --resume`. `--force` cannot bypass this rule.
- Move a cancelled or superseded card to `closed/` only with
  `kanban-move.sh <ID> closed --approved`. This flag is a caller attestation;
  the caller must already have explicit user authorization to cancel the work.
  A card in `closed/` cannot be moved out, even with `--force`; create a new
  linked card for future work. A successfully completed `done/` card cannot be
  reclassified as cancelled.
- `done/`, `freeze/`, and `closed/` skip active-card content-completeness lint,
  but all exact card IDs across all stages must be unique.

### Epics

An **epic** is a card whose body lists ordered subtask cards. Subtasks are normal
cards; the epic is their parent and their integration point.

- **Naming — reserved shared ID.** The epic always gets an `EPIC-<NUM>` ID
  (`kanban-new.sh --epic`), independently of the project's regular task prefix;
  every subtask reuses that SAME ID plus a 2-digit suffix in execution order
  (`kanban-new.sh --sub <EPIC-ID>`): e.g. `EPIC-042-billing-epic.md`,
  `EPIC-042-01-db-schema.md`, `EPIC-042-02-api-crud.md`… Regular cards retain
  their `<PREFIX>-<NUM>` IDs.
  Epic and subtasks share the leading `^[A-Za-z][A-Za-z0-9]*-[0-9]+` ID token —
  `kanban-schedule-run` groups them as one chain (related-card-first selection,
  dependency blocking) and the byobu window name stays inside its 10-char cap.
- **Start.** Epic card → `progress/`. Create ONE branch `epic/<ID>` for the whole
  epic; every subtask is implemented in that branch, not in its own `task/<ID>`.
- **Subtasks.** Work them in the listed order. Each finished subtask card moves
  `progress/ → test/ → ready/` as usual. A subtask **never** reaches `done/` on
  its own — the epic gates that.
- **Integration.** When the last subtask reaches `ready/`: restart the project,
  refresh all data (re-run imports/migrations), and run the full test suite.
- **Hand-off.** Only then move the epic card to `ready/`. If valid authorization
  covers parent and children `done`, move parent first, then eligible subtasks;
  verify `epic/<ID>` is clean before an authorized squash merge. Rename the
  archive to `done/<ID>` (`git branch -m epic/<ID> done/<ID>`) only after the
  merge succeeds and its result is verified; otherwise retain `epic/<ID>` and
  report that the cards remain on the task branch. Never delete it.

See [reference.md](reference.md) for the full epic protocol.

### Git Commits

Git mechanics follow the [git-repo-run](../git-repo-run/SKILL.md) core. Kanban's delta:
a task is worked **in its own branch** (an epic's subtasks share the epic branch
— see Epics above).

- **Branch.** By default work the task in a NEW branch `task/<ID>` (aligns with
  kanban-schedule-run). Create it at start.
- **Sub-agent commits.** When local commits are authorized, each sub-agent
  commits only its own work, following the repository's message and trailer
  policy. Preserve another actor's staged changes.
- **Normal local commits.** Commit coherent, validated progress proactively
  when useful; a separate user-approval gate is not required for ordinary local
  task commits. At `test → ready`, the orchestrator makes a verified wrap-up
  commit containing the latest card body and any remaining owned task files.
  Do not create an empty or redundant commit when that exact owned state is
  already committed and verified.
- **Authorized finalization.** Review and gates OK → move the card to `done/`
  and verify the branch is clean (`git status --short` empty) only when `done`
  is authorized. If merge is separately authorized, only then **squash-merge**
  the branch into the default branch as ONE commit, verify the merge result, then
  **rename** the branch to
  `done/<ID>` — strip the `task/` prefix (`git branch -m task/<ID> done/<ID>`);
  the archive is `done/<ID>`, NOT `done/task/<ID>`. Kept as an archive for
  optional later cleanup — do not delete immediately. If merge is not
  authorized or does not complete successfully, retain the task branch and do
  not archive-rename it. After any authorized push/deploy, read back the exact
  target and verify the expected remote revision/deployed version or state
  before reporting success.
- Moving cards between stage dirs → `kanban-move.sh` (uses the bundled Git-aware path helper, validates the transition); if a separate path operation is needed, ask the user to invoke `git-path-run` manually.

See [reference.md](reference.md) for the autonomous-run commit contract.

### Stop Conditions

- Do NOT skip planning.
- Do NOT perform `done`, merge, push, or deploy without valid authorization
  explicitly covering that action and target; do not ask again when a valid
  recorded grant already covers it.
- Do NOT start a card from `grooming/` — resolve open questions, move to `todo/` first.
- Resolve routine grooming choices from the authorized context; ask when a
  material user choice or required authorization is missing, and record decisions.
- Do NOT move to `ready/` while tests are red.
- Do NOT fix out-of-scope findings solely because they are small. Search for a
  duplicate before any authorized card creation; otherwise report the finding.

### Task Delegation Rules

1. **One agent — one zone.** Cross-zone task: the main agent does its own zone;
   the shared contract lives in a separate skill (e.g. a protocol/contract
   skill); adjacent implementations are done by their own agents reading that
   same skill.
2. **`security-auditor` — read-only**: emits a report, writes no code. Fixes are
   done by an implementer agent.
3. **`test-engineer` writes tests, not business logic.** If a test needs a new
   endpoint/hook in the code → file a subtask in kanban and delegate it to an
   implementer agent.
4. **New agent — only when clearly needed.** If the task fits an existing
   agent — don't spawn extra agents.

## Operations: decisions, lifecycle and handoff

Use for starting, moving, reviewing, or completing tasks on a project Kanban board. Resolve the board and its supported operations through the project or runtime interface; check current cards and project conventions before changing state.

### Decisions

When a decision is needed, explain its operational consequence and present concrete choices in the same interaction. Recommend one option and its trade-off; use an available choice interface when appropriate. Record the accepted decision on the affected card before the dependent action. If an unanswered decision may be resolved by the runtime's best-judgment policy, choose a reversible option consistent with the actual instructions. See [decision presentation](references/decision-presentation.md) when choosing the interaction.

### Lifecycle

- Present a concise interactive read-back of purpose, acceptance criteria, approach, and affected areas before starting work.
- Follow the project's defined transitions. For the common workflow, preserve `todo → progress → test → ready → done`; pause or cancel only through the supported project mechanism.
- A task reaches `done` only after explicit user approval for that task. Review approval, a profile name, credentials, or a successful gate do not supply that approval.
- If the owner explicitly classifies a card as superseded, history-only, or merged into another card, record the decision and receiving card, including unique acceptance criteria, in both records before archiving it through the supported mechanism. Archival is not implementation completion.
- Add concise execution-log entries after material work, verification, operational actions, or blockers, using the language required by the project.

### Deletion of operational data

Before a separately authorized destructive operation, establish the exact resource boundary, capture durable evidence, and independently verify its count and scope. Perform the narrow authorized deletion, recheck the target and adjacent protected resources, and record the outcome. Creating or moving a task does not authorize deleting its data.

### Verification and handoff

Distinguish static validation, runtime validation, and full-suite results. Report unrelated failures with their owner, and never describe unrun checks as passed. At handoff, summarize verified evidence, remaining work, side findings, and deduplication results. Collect unrelated nits, errors, suspicions, and follow-up candidates; map each to an existing waiting card when possible and state its proposed placement and scope. An active task does not by itself authorize an unrelated card change: obtain explicit owner approval unless the user already requested it or provided a grant covering that change; record that authorization in the card's execution log.
