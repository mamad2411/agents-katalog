---
name: build-agentic-workflow
description: >-
  Load this skill when product work repeats in the same shape (a weekly SEO pass, a pre-release
  check) and an agent should run it: emit one skill or a gated workflow into `.claude/skills/`.
  Trigger on "turn this into a workflow", "we run the same check every release".
disable-model-invocation: false
user-invocable: true
license: Apache-2.0
---

# Build an agentic workflow

Turn a repeated task into a runnable artifact. Repetition is the reason to build one at all: the
same steps run again in the same shape and only the input changes. A task that will not repeat is
done by hand, not built. There are two possible outputs, and choosing between them is the main
decision this skill makes:

- **One skill**, the default. A single `SKILL.md` the agent loads and follows.
- **A workflow**: a `flow.yaml` that owns ordering and gates only, a thin trigger skill that hands
  it to `ceh-workflow-runner:run-agentic-workflow`, and the step skills, scripts, saved workflows
  and handoff schemas the stages delegate to. The format and its validation rules are in
  `${CLAUDE_PLUGIN_ROOT}/references/flow-config-schema.md`. Read it before Phase 3. This skill does
  not restate it.

Target runtime is Claude Code only. Use its capabilities directly.

**Two build modes.** With a person in the session, the build ends with files written after they
agree to the file list. With no one to answer (`claude -p`, or called by another agent), it ends
with a draft and the questions a person must answer, per Headless build. The emitted workflow runs
in both modes.

The build is done when the user has agreed to the file list, the files are written under
`.claude/skills/`, and the Final checklist items that apply to the output pass. A headless build is
done when the draft and `QUESTIONS.md` are written to `<build-dir>/<name>-draft/`.

## Procedure

Assumed capabilities and Directories under Rules apply from step 1.

1. **Intake.** Confirm all nine spec answers exist, filling gaps through the interview skill
   (Phase 1).
2. **One skill or a workflow.** Default to one skill, named from the moment (Phase 2).
3. **What each step becomes.** Workflow only: native capability first (Phase 3).
4. **Data contracts.** Workflow only: give every cross-step handoff a file and a schema (Phase 4).
5. **Emit.** Write leaf-first and check the result, only after the user agrees to the file list
   (Phase 5). Headless, write a draft instead (Headless build).

### Phase 1 — Intake

This skill designs from a spec and does not conduct the interview. The nine answers live in
`<build-dir>/<name>-workflow-spec.md`. If they were given in this conversation, write them there
now so every later phase reads one source.

| #   | Must be answered                                        | Not satisfied by                                                                              |
| --- | ------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| 1   | Moment                                                  | a topic or domain noun. A schedule ("every Friday") passes — recast it as the moment it fires |
| 2   | Manual procedure, step by step                          | "the usual release process"                                                                   |
| 3   | Preconditions and proof per step                        | a proof no command or file check can settle, unless it is a declared human go/no-go gate      |
| 4   | Data flow per step, naming the _producing_ step         | an artifact named with no producer                                                            |
| 5   | Tooling: CLIs, credentials, services, network           | —                                                                                             |
| 6   | Done: what is true at the end that was not at the start | —                                                                                             |
| 7   | Interruption: one sitting, or resumable                 | —                                                                                             |
| 8   | Which steps damage something if they run twice          | silence                                                                                       |
| 9   | Which steps are irreversible outside this machine       | silence                                                                                       |

**A gap is not a "none".** Invoke the Skill tool with
`skill="ceh-workflow-builder:interview-workflow-task"` to fill any open row, then re-check this
table against what it wrote. Check all nine, row by row. The rows that slip through are the ones
you can nearly answer: an assumed-empty 8 emits a workflow with no re-run guard, an assumed-empty 9
emits one that publishes without pausing, and a row 4 derived from what each step appears to read
reads plausibly and is still a guess. Only the user knows whether step 3 pulls its input from
somewhere no step names.

Never supply a missing answer yourself, however obvious: not as an "assumption" written under the
heading, not as the missing half of a `Partial` row, not in the sentence after naming the row
unanswered. The user never chose it. In an interactive build an open row blocks the build: name
every blocking row and stop. A headless build carries open rows forward as questions, still
unfilled (Headless build).

**A declined row ends the loop.** When the spec records `Declined` under a heading, do not invoke
the interview again, or the two skills bounce off each other forever. Take the conservative
reading, write it into the spec as an assumption, and tell the user what it costs:

| Declined      | Assume                                            | Costs                                        |
| ------------- | ------------------------------------------------- | -------------------------------------------- |
| 8             | every step is unsafe to run twice                 | each step opens by checking the world        |
| 9             | every step with an outside effect is irreversible | the flow pauses for confirmation before each |
| any other row | nothing — these cannot be assumed safely          | stop and say which row blocked the build     |

Write into the spec only under the nine headings. The consumer gates on them by name, so build
notes go in the reply, never in a tenth section.

### Phase 2 — One skill or a workflow

**Default to one skill.** Emit a workflow only if at least one of these holds:

1. A step has a gate that can fail and must block the next step.
2. Steps need different tools or permissions.
3. Several steps deserve their own context windows, or one step spans many items, cross-checks its
   own results, or loops until a check passes. One large step alone does not qualify: a single
   skill can dispatch one subagent itself, and that is the smaller artifact.
4. The run must survive interruption and resume.
5. A step is already owned by an existing skill worth delegating to.
6. One step's output is another step's input, so the handoff needs a declared contract.

"It has several paragraphs" is not a reason. If none hold, write one skill from the single-skill
template (Templates under Output), skip phases 3 and 4, and keep only the destination and the
agreement step from Phase 5. Three rules still apply, because they guard the world rather than a
handoff: never write a secret to disk, only a reference to where it lives; a step from spec
question 8 opens by checking the world; and the skill pauses for confirmation immediately before a
step from question 9. It runs in the main context, so it can ask.

**Naming.** Derive `<name>` from the moment as a short kebab verb phrase the user would recognise
(`prepublish`, `onboard-tenant`, `rotate-keys`), never from the domain noun. Confirm it before
emitting, because every filename depends on it.

### Phase 3 — What each step becomes

**Native first.** A stage goes to the Claude Code capability that covers its step wherever one
does: an existing skill, a saved dynamic workflow, an `Agent` dispatch, a script. The runner keeps
only what native lacks: approvals between stages, world checks before a re-run, run state that
survives sessions, and the `FLOW STATUS:` line. The reason is that Claude Code keeps gaining what
hand-written orchestration does. A flow built on native capabilities shrinks as they grow, and one
that re-describes them in prose competes with them and drifts. When a native capability later
covers an inline step, the step moves to it.

Decide per step, in this order, and stop at the first that fits:

| Becomes                  | When                                                                                                                                                                                                                                       |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| An existing skill        | Something already owns the step. Check it is installed in this session and model-invocable first, else drop to the next row. A plugin skill may be absent where the flow later runs, so its stage declares a `fallback`                    |
| A saved workflow         | The step fans out over many items, cross-verifies, or loops until a check passes, and needs no human input mid-step. Always declare a `fallback`: the Workflow tool is off by default. A step one agent can do is an `Agent` stage instead |
| A script                 | The step is mechanical and deterministic                                                                                                                                                                                                   |
| Its own step skill       | The step is triggerable on its own outside the flow, or the flow dispatches it in a subagent                                                                                                                                               |
| Inline prose in the flow | Nothing above fits                                                                                                                                                                                                                         |

**Isolation comes from `Agent`, not from being a skill.** A step skill called with the `Skill` tool
runs in the flow's own context and saves nothing. Dispatch a step with `Agent` when it reads a lot
or its working notes would crowd the run, and only when its output outlives the subagent: a file,
or state a command can check, such as a commit or an open PR.

**A step earns its own skill only on the fourth row.** Every skill added to `.claude/skills/`
competes for auto-triggering in the target repo, and the directory is flat, so a generated set is
grouped only by naming: flow `<name>-flow`, steps `<name>-<step>`. A step skill cannot be hidden
with `disable-model-invocation: true`, which would block the flow's own call, so its `description`
names the owning flow and routes away from direct use.

**Nesting is capped at one level.** A step skill is never itself a workflow, and no stage calls the
runner: a stage runs as a subagent, so a nested runner's approvals would have no one to ask.

### Phase 4 — Data contracts

The failure this prevents: a later step gets no declared shape, infers one from whatever artifact
it finds, infers it wrong, and the run keeps producing garbage past a green gate.

- **A schema whenever any later step reads the output**, N+m and not only N+1. A terminal artifact
  nobody downstream reads gets none.
- **Handoff is a file, never conversation state.** An `Agent` step cannot see the caller's
  transcript, and compaction drops anything held only in context. Inside a saved workflow, the
  handoffs between its own agents are script variables: map the schema onto
  `agent(..., { schema })`. The stage boundary stays a file.
- **Artifacts live for the whole run.** The consumer may be four steps away.
- **One writer, many readers.** The schema belongs to the producing step, and every consumer
  points at that one file. When a later step amends the artifact, the schema names that step and
  the part it owns. An undeclared second writer is the bug this catches.
- **A committed file in an owned format** (`CHANGELOG.md`, a manifest) is read in place and names
  its owner. A copy or a restated format is a second version that drifts.

**Where it lives.** `.claude/skills/<name>-flow/references/<artifact>-schema.md`: required fields,
optional fields, one complete worked example, and the consuming steps. Name each required field as
a literal heading or key, so a gate checks it with `Grep` rather than by judgement. Use JSON Schema
only when the artifact is JSON and the step already runs a script. Never add a dependency for this.

**Schemas make gates falsifiable.** Replace "the plan is complete" with "`{run}/plan.md` exists and
carries every required field in `plan-schema.md`".

### Phase 5 — Emit

Leaf-first, so every reference resolves the moment it is written:

1. Schema docs → `.claude/skills/<name>-flow/references/`
2. Scripts → `.claude/skills/<name>-flow/scripts/`
3. Saved workflows, if any → `.claude/workflows/<name>-<step>.js`
4. Step skills → `.claude/skills/<name>-<step>/SKILL.md`
5. The config → `.claude/skills/<name>-flow/flow.yaml`
6. The thin trigger skill → `.claude/skills/<name>-flow/SKILL.md`, and the invocation guide
   `.claude/skills/<name>-flow/README.md` (a skill directory's README is never loaded as context)

Paths inside `flow.yaml` are relative to its directory, so a script is `scripts/<x>.sh` there. A
step skill reaches it through `${CLAUDE_SKILL_DIR}/../<name>-flow/scripts/<x>.sh`. A bare
`scripts/<x>.sh` in a skill body resolves against the repo root, where `Bash` runs, and finds a
different file or none.

**Each `.js` saved workflow.** Write it with LF line endings: CRLF fails at launch with "control
characters that would be hidden in the approval dialog". Add `.claude/workflows/*.js text eol=lf`
to the target repo's `.gitattributes`. Then check:

- `export const meta` comes first, as a plain literal with `name` and `description`
- no `import()`, no `Date.now()`, no `Math.random()`, no no-argument `new Date()`
- every `phase()` title matches an entry in `meta.phases`
- at most 4,096 items in any one `parallel()` or `pipeline()`
- `null` results are filtered before use

Recommend the bundled `/workflow-authoring` skill (Claude Code v2.1.248+) for the body. This plugin
repo's `validate.py` does not know these checks, so they run here.

Then check:

- **Resolution.** Every generated step skill's directory exists. Every pre-existing skill delegated
  to is installed and model-invocable, since a call to one with `disable-model-invocation: true`
  fails silently.
- **Config.** `flow.yaml` passes every Validation rule in the schema doc. The likeliest generation
  bug is a `reads` whose `from` names no earlier `writes`, once handoffs stop being adjacent. A
  `headless: stop` or `preapproved-only` approval forces `resumable: true` even when spec question 7
  said one sitting, so tell the user why.

**The thin trigger skill.** Its body is only the moment and a hand-over to the runner. Its
`compatibility` names the `ceh-workflow-runner` plugin and, when a stage is a saved workflow,
Claude Code v2.1.269+ with the Workflow tool on. If the runner cannot be called, it stops and says
the plugin must be installed, and never runs the stages by hand.

**The invocation guide** gives the interactive and headless commands, derived from the config:

- `--allowedTools` is the union of every stage's `tools`, `Workflow(<workflow>)` per saved workflow
  stage, and a `Bash` rule per `script` stage, because headless nobody can approve a prompt.
- `--settings '{"enableWorkflows": true, "disableWorkflows": false}'` only when a `workflow` stage
  exists, noting that the `enableWorkflows` key is undocumented and may change.
- PowerShell and Bash forms apart: PowerShell cuts a Bash-style `\"` at the first quote, so use a
  single-quoted prompt with plain `"` inside.
- When any `approval` exists, the round trip: `FLOW STATUS: awaiting-approval <stage-id>`, then
  `--resume <session-id> 'APPROVED <stage-id>'`, or a fresh session with
  `resume=latest approve=<stage-id>`.

Show the user the file list and the stage/gate table (rendered from `flow.yaml`) before writing,
and write only after they agree: a wrong `<name>` means cleaning up every file. The destination is
the target repo's `.claude/skills/`, picked up with no install step. Offer plugin packaging only
when the user says the workflow is shared across repos.

### Headless build

The interview's headless path records open rows and asks nothing. This path designs from what that
leaves and writes nothing a person has not agreed to.

1. **Intake.** Invoke the interview as in Phase 1. Every row it leaves open stays open: never fill
   it, and never give it the declined-row reading.
2. **Design** phases 2 to 4 from the answered rows. Where an interactive build would ask, take the
   conservative choice and record it as an assumption: `<name>` derived from the moment, `stop` for
   every approval's `headless` value, no plugin packaging. Where an open row shapes a stage, mark
   that spot `OPEN: spec row <n>` in the draft instead of deciding it. The draft's `flow.yaml` may
   fail validation for that reason, so list each failing rule with the row behind it.
3. **Write the draft** to `<build-dir>/<name>-draft/`, laid out as the Phase 5 file list. Nothing
   goes into `.claude/skills/`, `.gitignore` or `.gitattributes`, and nothing is committed: a skill
   in `.claude/skills/` loads in the next session, so a draft there is already live.
4. **End with the questions**, in one round, each with a recommended answer: every open spec row,
   then every recorded assumption to confirm. Write them to `<build-dir>/<name>-draft/QUESTIONS.md`
   as well, so the next session finds them.

A later interactive run of this skill reads the spec, the draft and its questions, asks them, then
runs Phase 5 as usual. The draft is input to Phase 5, never copied into the repo unchecked.

## Rules

### Assumed capabilities

The emitted artifact relies on Claude Code's built-in tools and does not list them.
`compatibility` is for software the machine may lack. Three differences decide the design:

- **`Skill`** loads into the caller's context. It never isolates a step.
- **`Agent`** is the only way to give a step its own context window. A subagent cannot see the
  caller's transcript.
- **`AskUserQuestion`** is stripped from every subagent, so only the flow itself can ask.

**The Workflow tool is not assumed.** It is off by default (Dynamic workflows in `/config`;
headless, the undocumented `enableWorkflows` setting). Without it, a session imitates a workflow by
hand and the run looks successful on disk. A `workflow` stage therefore declares a `fallback`, and
the flow's `compatibility` names Claude Code v2.1.269+ and the setting.

### Directories

|            | Variable                  | Default              | Holds                                                 |
| ---------- | ------------------------- | -------------------- | ----------------------------------------------------- |
| Build time | `$CEH_WORKFLOW_BUILD_DIR` | `.agents_workspace/` | the workflow spec, build notes and headless drafts    |
| Run time   | `$CEH_WORKFLOW_RUN_DIR`   | `.agents_workspace/` | the generated workflow's step artifacts and run state |

Both default to one place, so both namespace by name: `<build-dir>/<name>-workflow-spec.md` and
`<run-dir>/<name>/`. Use a provisional slug until the name is settled, then rename the spec, or a
second build overwrites the first one's.

**One directory per run.** Each run writes to `<run-dir>/<name>/<run-id>/`, the `{run}` of
`flow.yaml`. A fixed per-flow directory would let last week's artifacts pass this week's
exists-checks, and a finished `run-state.md` would make the new run skip every step. State that
outlives a run, such as a watermark, sits one level up and is written only after every step it
summarises succeeded. For a workflow, the runner creates the directory. A single skill has no
runner, so it names `$CEH_WORKFLOW_RUN_DIR` and its default in its own body, because the agent that
runs it never saw this build.

Run artifacts are never committed. When there is a run directory, check that the target repo's
`.gitignore` covers it and append it if not.

### Gates, re-runs and irreversible steps

- **A failed gate stops or retries, nothing else.** "Do not proceed past a red gate" is a
  prohibition, not a behaviour, and leaves the agent inventing one at the worst moment. Stop is the
  default. Retry only where re-running can change the outcome, such as test → fix → test, and then
  state what changes between attempts, a bound of usually 2 or 3, and the stop when it is spent. In
  the stage/gate table write `<condition> — retry up to N, then stop`.
- **Run state only when spec question 7 says the run can stop partway.** Then set
  `resumable: true` and the runner keeps it. Git alone cannot show where a run stopped, because
  uncommitted work leaves no trace. A single skill keeps its own `<run>/run-state.md` and opens by
  offering to resume the newest run. A long step, such as a fact-check over twenty claims, appends
  each unit to its output file as it completes, because context that dies mid-step takes unwritten
  results with it.
- **Re-running is not resuming.** `run-state.md` shows where a run stopped only if it survived the
  failure, so a step from spec question 8 checks the world, not the ledger: does the schema exist,
  is the row inserted? In `flow.yaml` that is `unsafe_to_rerun` with a `world_check`. In a single
  skill it is the step's first instruction.
- **Irreversible steps from spec question 9** go as late as the data flow allows, so an upstream
  failure costs nothing outside the machine. Each gets one confirmation immediately before it, one
  per batch rather than per item. Consecutive irreversible steps with only a mechanical gate between
  them, merge then tag, share one. A declined confirmation stops with the step `pending`, so a
  resumed run asks again.
- **The confirmation belongs to the flow, not the step**, because a subagent cannot ask. Declare it
  as an `approval`. Ask the user which `headless` value each approval takes, because it decides
  whether an unattended run can ever reach that step. Never emit a "proceed anyway".

### Frontmatter for everything emitted

`description` is a folded block scalar (`>-`) with a uniform 2-space indent and no blank lines, the
only style with no escaping burden. It carries the trigger moment and negative routing to the
nearest neighbour. Any other key containing `: ` gets single quotes. If `skill-creator` is
installed, use it for the mechanical `SKILL.md` authoring. This skill does not depend on it.

## Output

### Templates

Every emitted `SKILL.md` starts from a template in
`${CLAUDE_SKILL_DIR}/references/emitted-templates.md`: the single skill, the thin trigger skill,
and the step skill. Read it in Phase 5, before writing the first `SKILL.md`.

### Final checklist

- [ ] Every intake row answered by the user or the interview, or declined with its conservative
      reading in the spec. Headless: open rows are questions, never filled.
- [ ] A workflow only because a Phase 2 condition holds, otherwise one skill.
- [ ] Each stage on a native capability wherever one covers the step.
- [ ] Every gate falsifiable, against a schema where one exists, and it stops or retries with a
      bound.
- [ ] Every cross-step handoff a file with a schema, every `reads` with an earlier `writes`.
- [ ] `flow.yaml` passes every schema rule, and the thin trigger only hands it to the runner.
- [ ] Every step unsafe to run twice has a world check, and every irreversible step sits late behind
      an `approval` with a `headless` value.
- [ ] No secret in any artifact or config value, only references.
- [ ] Each saved workflow has a `fallback`, LF endings, the `.gitattributes` line and the `.js`
      checks.
- [ ] No bare `scripts/` path in a skill body.
- [ ] `compatibility` present if and only if a step needs software the machine may lack, each tool
      with a minimum version and what fails without it.
- [ ] Run directory, if any, in the target repo's `.gitignore`.

## Stop conditions

- An intake row is unanswered and not declined in an interactive build → name every row that
  blocked it and stop.
- A declined row other than 8 or 9 → stop and say which row blocked the build.
- The user has not agreed to the file list and the stage/gate table → write nothing to the repo.
- No human can answer → follow Headless build and end with its questions; never emit into
  `.claude/skills/`.
- `flow.yaml` fails a schema rule → fix it before writing. If the fix changes an intake answer,
  stop and say which.

## Hands off to

- Invoke the Skill tool with skill="ceh-workflow-builder:interview-workflow-task" to fill any
  intake row the spec leaves open (Phase 1).
