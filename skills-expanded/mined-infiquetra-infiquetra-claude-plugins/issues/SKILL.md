---
name: issues
description: |
  Create and manage SDLC issues in Infiquetra GitHub repositories using the 5-type issue
  taxonomy: capability, enhancement, defect, exploration, and context-update.
  Handles issue type selection, template-guided creation, Hermes label application, project
  board assignment, and milestone linking.
when_to_use: |
  Use this skill when the user wants to:

  Direct issue creation:
  - "create a capability", "create a defect for this bug", "file an enhancement",
    "open an exploration", "create a context update"
  - "create an issue in infiquetra-core", "file a bug against the auth service"
  - "create an issue of type capability", "I need to open a defect"

  Blueprint-driven creation:
  - "review the blueprint and create issues", "look at the blueprint and figure out what
    issues we need", "create issues for all the capabilities in this objective"
  - "based on the spec, what issues should we create?"

  Contextual issue creation:
  - "this needs to be tracked as a defect", "let's turn this into a capability issue"
  - "we should track this work", "open an issue for this"

  Issue type guidance:
  - "what type of issue should this be", "is this a capability or enhancement",
    "how should I categorize this work", "help me pick the right issue type"

  Batch creation:
  - "create issues for all the capabilities in this objective"
  - "set up the issues for the platform launch objective"

  Existing issue assignment to Team Mimir:
  - "assign this issue to Mimir"
  - "route this covered issue through Mimir intake"

  Prepared issue creation:
  - "create an issue from the brainstorm", "handoff the plan as an issue"
  - "create a CAMPPS issue from this text"
  - "create an Asgard issue from these notes"
  - "turn this queue entry into an issue for the router repo"
---

# SDLC Issues

Create and manage SDLC issues across Infiquetra repositories using the 5-type taxonomy.
Handles type selection, template-guided creation, Hermes label application, and project board
assignment.

For an already-created issue that should enter Team Mimir, use the flow helper rather than adding
the trigger by hand:

```bash
python3 sdlc_manager.py flow assign-mimir --repo <repo> --number <N>
```

The command reads Team Mimir's live exact-repository coverage and verifies open issue state,
current GitHub authority, the existing `intake:mimir` label, mutation readback, and any live
Objective project-field value. It never admits a repository or creates the trigger label.

## Script Location

```
$INFIQUETRA_SDLC_PATH/../infiquetra-claude-plugins/plugins/mission-control/scripts/sdlc_manager.py
```

> If `$INFIQUETRA_SDLC_PATH` is unset, use `~/workspace/infiquetra/infiquetra-sdlc` as the default base path.

## Issue Types

Five issue types cover all Infiquetra issue-backed work:

| Type | Hermes Actionable | Duration | When to Use |
|------|-------------------|----------|-------------|
| **capability** | Yes | 1-4 weeks | New end-to-end deployable functionality |
| **enhancement** | Yes | 2-5 days | Improving existing functionality |
| **defect** | Yes | Hours-2 days | Broken functionality that an agent can fix |
| **exploration** | No | 1-3 days | Research, POC, or architectural investigation |
| **context-update** | No | Hours-1 day | Updating Blueprint repository documentation |

An Objective is an `Objective` project-field option plus an Outcome Scorecard
doc, not an issue type. Capabilities are top-level by default and carry the
Objective field value. Add a native parent only for real decomposition, such as
a Capability's executable child or an Outcome proof card on a board that
explicitly uses that tier.

See `references/issue-types.md` for the complete guide and decision tree.
See `references/templates-reference.md` for the generated template field and label reference.

## Hermes Actionable Contract

Actionable issue types are `capability`, `enhancement`, and `defect`. Their canonical templates
apply `needs-plan` and the type label.

Each actionable card must render the following exact H3 section headers in the GitHub issue body:

- `### Objective`
- `### Intent`
- `### Out-of-scope / non-goals`
- `### Files expected to change`
- `### Tests to add or update`
- `### Context library links`
- `### Acceptance criteria`
- `### Verification`

Hermes validation expects these semantics:

- `Context library links` is required for Hermes readiness; use `_none_` when no context applies.
- `Acceptance criteria` includes at least one `- [ ]` checklist item and names a runnable check.
- `Verification` includes exact commands, preferably in a fenced shell code block.
- `Files expected to change` includes at least one path-like line.
- High and very-high risk cards also require `Inputs inventory`, `Failure modes / pre-mortem`,
  and `Stop conditions`.
- `Lifecycle Origin` is auto-populated by prepared handoff flows, not author supplied.
- `### Recommended Tier Band` is auto-stamped at issue creation from the issue type
  (defect/capability→`opus/high`, enhancement/context-update→`sonnet/medium`,
  exploration→`sonnet/low`) — a coarse seed saga's `/plan` pre-fills its tier
  table from (repo `.saga/tier-defaults.json` overrides win). Auto-populated, not author supplied;
  never double-stamped on recompile.
- Empty placeholder sections such as `_No response_` are invalid.

Optional actionable sections include `Notes / conventions`. Capability cards also include optional
`Capability size (human planning hint)`.

## Non-actionable Templates

Exploration and Context Update templates carry only their context labels. Do not present these as
Hermes task cards or dispatch them directly to agents. Use them for research or documentation
context.

## Core Operations

### Prepared Issue Draft from Source Text

Use the prepared workflow when the user starts from rough text, notes, copied queue entries, or
asks for an Asgard or CAMPPS issue that should be reviewed before mutation.

`/issue` is the primary user-facing command for this path. `/issue` remains a
compatibility alias. `--prepare` is the canonical non-mutating mode; `--draft` means the same
thing. `--from` accepts a local path, GitHub issue/PR URL, branch ref, or natural search hint.
`--maturity` overrides the source's path-derived handoff maturity fallback; the
owner classifies the value, so `pending-confirmation` and `deferred-context` are
accepted alongside the four ready states. When the source itself carries a
declaration (draft sidecar or Saga state) that differs from `--maturity`,
prepare records a blocking gap naming both values instead of letting the flag
win.

```bash
python3 sdlc_manager.py issue prepare \
  --repo hermes-claude-code-router \
  --type capability \
  --team campps \
  --project campps \
  --risk medium \
  --title "Prepared issue workflow" \
  --from docs/plans/example.md \
  --maturity plan-ready

python3 sdlc_manager.py issue create-prepared docs/sdlc-issue-drafts/<draft>.md
```

The prepared workflow writes a markdown draft and JSON sidecar under
`docs/sdlc-issue-drafts/`. `issue create-prepared` re-runs readiness checks, renders the mutation
plan, asks for confirmation, repairs missing labels/templates after confirmation, opens a mapping
PR when needed, and only then creates the issue.

### Advisory suggestions on a prepared draft

`--suggest` records what a typed judgment thought about the draft, beside what you chose:

```bash
python3 sdlc_manager.py issue prepare \
  --repo hermes-claude-code-router \
  --type capability --team campps --project campps \
  --title "Prepared issue workflow" \
  --from docs/plans/example.md \
  --suggest \
  --objective-option improve-claude-plugins
```

The sidecar gains a suggested issue type with its full probability distribution over all five
types, a suggested risk tier, and — when you pass candidates with the repeatable
`--objective-option` — a suggested Objective, plus a suggested board Status. The distribution is
shown rather than a single answer because the measured agreement against this repository's own
labels is 19 of 30, and most of the misses are places where the label is the thing that is wrong.

**Nothing is applied.** Your `--type`, `--risk` and `--status` remain the decision. A suggestion
that differs from one of your flags is recorded as an override in the verdict log, which is what
later makes it possible to ask whether the judgment is worth trusting. The suggestions never
reach the issue body, and the risk suggestion never touches the card's Risk — the body still owns
that.

The flag is opt-in and off by default, so an ordinary prepare makes no model call at all.

**Where the text goes.** With the flag, the draft body and this repository's own issue-types
reference are sent to TypeSafe, a third-party endpoint, and `TYPESAFE_API_KEY` must be in the
environment. Credentials and high-entropy strings are redacted before anything leaves the machine,
and the fleet's data rule (`plugins/fleet-core/references/typesafe.md`) governs what may be sent at
all: issue and plan text is permitted, transcripts and customer content are not.

If the call fails, the draft is written exactly as it would have been and the sidecar carries a
note saying why there are no suggestions; a prepare never fails because a suggestion did.

### Ship-policy intent envelope on the issue (#380)

When the operator's autonomy answers for the eventual run are already known at capture time,
record them ONCE, on the issue, as a schema-validated block — so `/outcome start` reads them and
never re-interrogates the operator (ask-once). Render the block and embed it in the draft body:

```bash
python3 sdlc_manager.py issue intent-envelope \
  --run-mode unattended --merge auto --authored-by jeff
```

This emits a `### Intent envelope` heading plus a fenced `intent-envelope` JSON block validated
against the fleet's closed envelope schema (canonical:
`plugins/fleet-core/scripts/fleet_commons/intent_envelope.py`; contract:
`plugins/saga/references/intent-envelope.md`). Answer values are typed against the single fleet
interview — off-vocabulary values fail loudly at render. Prepared-issue readiness treats a
present-but-invalid envelope block as a BLOCKING gap (fail closed at capture); an absent block
stays fine — the envelope is optional, and `/outcome start` falls back to its run-start
interview. Do not author the envelope as prose or invent a second posture question — the fleet
drift-guard test fails on one.

Prepared handoff drafts include `handoff_maturity` in the sidecar and a body section with the
suggested next action. Readiness vocabulary and assessment are owned by the saga plugin's
handoff envelope (`#942`) — mission-control delegates to it and keeps no local vocabulary.
Maturity values are:

- `idea-ready` -> the owner suggests `/plan <published source>`.
- `requirements-ready` -> the owner suggests `/plan <published source>`.
- `plan-ready` -> the owner suggests `/work <published source>`.
- `resume-ready` -> the owner suggests `/work <published source>`.
- `deferred-context` -> creatable with clarification text; the owner never attaches a live command.
- `pending-confirmation` -> creatable, proposed-only; the owner never attaches a live command until an operator confirms.

Sources without an explicit declaration fail closed: an undeclared saved draft or Saga state
file is refused at prepare time (the drafts folder or state path alone never makes it ready),
and out-of-root sources are refused outright.

Source artifact resolution:

- Explicit local path: `--from docs/brainstorms/example.md`.
- GitHub issue or PR URL: fetched through `gh issue view` or `gh pr view`.
- Branch ref: `--from branch:current` or `--from branch:<name>` captures resume context.
- Natural language such as "from the brainstorm" or "handoff the plan" searches durable
  lifecycle artifact directories before asking for a path.
- Ambiguous matches must be shown to the user; do not pick one silently.

Natural-language routing rules:

- "Create an issue from the brainstorm" -> search `docs/brainstorms/`, prepare, then
  create-prepared after review.
- "Create a CAMPPS issue from this text" -> prepare with `--team campps --project campps`,
  then create-prepared after review.
- "Create an Asgard issue from this text" -> prepare with `--team asgard --project asgard`, then
  create-prepared after review.
- If team or project is ambiguous, ask. Do not guess.
- Do not bypass prepared readiness checks with ad hoc `gh issue create` when the prompt asks to
  create from source text.
- Do not suggest `/loop` to a team recipient. Use `/plan <issue>` or `/work <issue>` only when the
  recipient has `saga`.

Safe starting statuses (the declared Stage drives them):

- A prepared issue's `Status` defaults to the declared `Stage`'s entry option —
  the first configured option of that Stage's `stage_statuses` list in
  `config/sdlc-schema.json` (`Intake`→`Capturing`, `Shaping`→`Discovering`,
  `Planning`→`Designing`, `Active`→`Implementing`, `Verify`→
  `Awaiting verification`, `Retro`→`Gathering evidence`).
- Readiness accepts any `Status` configured for the declared `Stage`, plus the
  cross-cutting `Blocked`; retired (`Idea`, `Shaping`, `Done`), unknown, and
  out-of-Stage values are refused.
- Never auto-move a prepared issue to `Ready for Planning`.

### Create Issue with Template

```bash
# Launch interactive template for a specific issue type
python3 sdlc_manager.py issue create --repo infiquetra-core --type capability
python3 sdlc_manager.py issue create --repo infiquetra-auth --type defect
python3 sdlc_manager.py issue create --repo infiquetra-blueprint --type context-update

# Create via gh CLI directly (alternative)
gh issue create --repo Infiquetra/infiquetra-core --template capability.yml
```

After template creation, apply labels and add to the project board where applicable.

### Labels from Canonical Templates

**Actionable templates**:

- `capability` -> `capability`, `needs-plan`
- `enhancement` -> `enhancement`, `needs-plan`
- `defect` -> `defect`, `needs-plan`

**Non-actionable templates**:

- `exploration` -> `exploration`, `research`
- `context-update` -> `context-update`, `documentation`

**Apply labels manually** via gh CLI when a template did not apply them:

```bash
gh issue edit <N> --repo Infiquetra/<repo> --add-label "needs-plan,capability"
gh issue edit <N> --repo Infiquetra/<repo> --add-label "needs-plan"
```

### Add to Project Board

```bash
# Auto-detect project from repo mapping and add
python3 sdlc_manager.py board add --repo infiquetra-core --number <N>
```

The script reads `project-mappings.json` from the infiquetra-sdlc config to determine which
project a repo belongs to.

**If the repo is unmapped**: warn the user and offer to add manually via the GitHub web UI.
Most new repos need to be added to `project-mappings.json` first.

### Sync Project Fields

Set project fields with the `flow` helpers after the issue is added to a board:

```bash
python3 sdlc_manager.py flow set-field \
  --repo <repo> \
  --number <N> \
  --project campps \
  --field Status \
  --option Implementing
```

Use live field discovery rather than cached field IDs.

## Issue Creation Workflow

Follow these steps when creating any issue:

### Step 1: Determine Issue Type

Use the decision tree (see `references/issue-types.md`) or ask the user:

- New end-to-end deployable functionality? -> **CAPABILITY**
- Improving existing functionality? -> **ENHANCEMENT**
- Broken functionality for an agent to fix? -> **DEFECT**
- Coordinating multiple capabilities with a target date? -> **OBJECTIVE**
- Researching or investigating? -> **EXPLORATION**
- Updating Blueprint documentation? -> **CONTEXT UPDATE**

If uncertain, present the decision tree and ask clarifying questions.

### Step 2: Choose Target Repository

Issue can be created in any Infiquetra repo. Common repos:

- `infiquetra-core`, `infiquetra-auth`, `infiquetra-infra`
- `infiquetra-blueprint` — for Context Updates and Explorations
- `infiquetra-claude-plugins`

If the user doesn't specify, ask which repo the work belongs to.

### Step 3: Gather Required Fields

For actionable cards, gather these exact required fields:

- Objective
- Acceptance criteria
- Out-of-scope / non-goals
- Files expected to change
- Tests to add or update
- Verification

Ask for optional Notes / conventions and Context library links when they would improve planning.
Ask for Capability size only for capability cards and treat it as a human planning hint.

For non-actionable cards, use the fields in `references/templates-reference.md` and preserve the
actionable / non-actionable distinction.

### Step 4: Create the Issue

```bash
# Interactive template (prompts for all fields)
python3 sdlc_manager.py issue create --repo <repo> --type <type>

# Or open gh CLI template directly
gh issue create --repo Infiquetra/<repo> --template <type>.yml
```

### Step 5: Verify Labels

1. Confirm actionable templates applied `needs-plan` and the type label.
2. Confirm non-actionable templates applied their context labels.
3. Use `flow verify-label` for any required label that is missing.

### Step 6: Add to Project Board

```bash
python3 sdlc_manager.py board add --repo <repo> --number <N>
```

Issue starts in **Backlog** unless the current project workflow moves it elsewhere.

### Step 7: Set Objective and Link a Real Decomposition Parent

```bash
# Group the card by Objective.
python3 sdlc_manager.py flow set-field \
  --project <project> --repo <repo> --number <N> \
  --field Objective --option <objective-name>

# Add a native parent only when this card is a decomposition child.
python3 sdlc_manager.py flow link-sub-issue \
  --parent-repo <parent-repo> \
  --parent-number <parent-number> \
  --child-repo <repo> \
  --child-number <N>
```

If an accidental or retired parent layer exists, remove only the relationship:

```bash
python3 sdlc_manager.py flow unlink-sub-issue \
  --parent-repo <parent-repo> --parent-number <parent-number> \
  --child-repo <repo> --child-number <N>
```

## Natural Language Examples

**"Create a capability in infiquetra-core"**
-> `issue create --repo infiquetra-core --type capability`

**"File a defect for the auth API crashing"**
-> `issue create --repo infiquetra-auth --type defect`

**"Create an exploration to research biometric SDK options"**
-> `issue create --repo infiquetra-blueprint --type exploration`

**"Create an issue from the plan"**
-> Search `docs/plans/`; if one plan matches, prepare with
`issue prepare --from <plan> --maturity plan-ready`. If multiple plans match, ask the user to
choose.

**"Create a CAMPPS issue from this text for the router repo"**
-> Prepare a CAMPPS draft with `issue prepare --team campps --project campps`, review
readiness gaps, then use `issue create-prepared`.

**"Create an Asgard issue from these notes"**
-> Ask for the target repo if missing, prepare an Asgard draft with
`issue prepare --team asgard --project asgard`, review gaps, then use `issue create-prepared`.

**"Is this a capability or enhancement?"**
-> Walk through decision tree: Is it new end-to-end deployable functionality? If yes -> capability.
If it improves existing functionality -> enhancement.

**"Create issues for all the capabilities in this objective"**
-> List capabilities from the Objective scorecard or source artifact, create each with
`--type capability`, and set the same `Objective` project-field value on each. Do not create or
link an Objective parent issue.

**"What type of issue should this be?"**
-> Present the decision tree from `references/issue-types.md`.

## Label Reference

### Actionable Labels

| Type | Labels |
|------|--------|
| `capability` | `capability`, `needs-plan` |
| `enhancement` | `enhancement`, `needs-plan` |
| `defect` | `defect`, `needs-plan` |

### Non-actionable Labels

| Type | Labels |
|------|--------|
| `exploration` | `exploration`, `research` |
| `context-update` | `context-update`, `documentation` |

### Content Labels

| Label | Applied When |
|-------|-------------|
| `security` | Security vulnerability or CVE |
| `performance` | Performance regression or optimization |
| `breaking-change` | API or interface breaking change |

## Key Behaviors

- **Always confirm issue type** before creating — wrong type causes downstream confusion.
- **Preserve Hermes actionable/non-actionable distinction** — only capability, enhancement, and defect are Hermes task cards.
- **Default parent linkage to none** — use native sub-issues only for real decomposition.
- **Use exact actionable H3 headers** — the Hermes validator matches section header text.
- **Require checklist acceptance criteria** — at least one `- [ ]` item is mandatory.
- **Require verification commands** — commands should be copy-pasteable and prove success.
- **Unmapped repos** will warn on board add — this is expected for newer repos.

## Reference Documents

- `references/issue-types.md` — Complete guide to all 5 issue types with decision tree
- `references/templates-reference.md` — Generated view of canonical issue templates
