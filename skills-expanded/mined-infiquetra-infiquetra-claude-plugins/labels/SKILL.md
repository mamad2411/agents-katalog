---
name: labels
description: |
  Manage GitHub labels and project field options for Infiquetra repositories.
  Handles applying SDLC labels to issues, auditing repos for missing labels, deploying the
  full label taxonomy, auto-labeling issues based on title/body patterns, and creating
  new field options when new initiatives or
  objectives are introduced.
when_to_use: |
  Use this skill when the user wants to:

  Applying labels to issues:
  - Apply a label to an issue ("label this issue", "add the capability label",
    "tag this as high priority", "mark this as an enhancement", "add the blocked label")
  - Set or correct issue type, priority, or status labels

  Setting project fields:
  - Set Initiative, Objective, or other project fields directly after label or card changes
  - Discover available fields and options on Operations, Asgard, or CAMPPS

  Assigning initiatives and objectives:
  - "this belongs to platform-v1", "assign to the platform-launch objective",
    "this issue is part of the core-platform initiative", "tag this with the Q1 objective"
  - Setting the corresponding project field option

  Auditing label coverage:
  - "check if this repo has all the SDLC labels", "audit labels on infiquetra-core",
    "what labels are missing from this repo", "run a label audit"
  - Comparing repo labels against the canonical SDLC label set

  Deploying labels to repos:
  - "push labels to this repo", "sync labels from the SDLC config",
    "deploy the SDLC labels to this repo", "set up labels on a new repo"
  - Creating or updating repo labels to match `labels.json`

  Auto-labeling based on content:
  - "auto-label this issue based on its content", "apply labels based on the title",
    "run auto-label rules on issue #42"
  - Pattern matching against issue title and body to apply appropriate labels

  Adding new initiatives or objectives:
  - "we have a new initiative", "add a new objective to the board",
    "create a new initiative option called platform-stability",
    "add platform-launch as a new objective"
  - Creating new single-select options on the project board for new initiatives/objectives

  Field discovery:
  - "what fields does an active board have", "show me the board fields",
    "discover project fields"
---

# SDLC Labels

Manage Infiquetra issue labels and synchronize them with the GitHub Projects board fields.

## Script Location

```
$INFIQUETRA_SDLC_PATH/../infiquetra-claude-plugins/plugins/mission-control/scripts/sdlc_manager.py
```

> If `$INFIQUETRA_SDLC_PATH` is unset, use `~/workspace/infiquetra/infiquetra-sdlc` as the default base path.

## Core Operations

### Set Project Fields

Initiative and Objective are project fields, not label-derived state. Set them directly:

```bash
python3 sdlc_manager.py flow set-field --project campps \
  --repo infiquetra-core --number 42 \
  --field Objective --option "platform-launch"
```

The older `labels sync-fields` command remains for compatibility, but new work should prefer
`flow set-field` because it uses live project field discovery.

### Audit Repo Labels

Check whether a repository has all required SDLC labels defined:

```bash
python3 sdlc_manager.py labels audit --repo infiquetra-core
```

Output shows: present labels, missing labels, and extra (non-SDLC) labels.

### Deploy Labels to Repo

Create or update a repo's labels to match the canonical SDLC label set from `labels.json`:

```bash
python3 sdlc_manager.py labels deploy --repo infiquetra-core
```

Safe to re-run — creates missing labels, updates color/description on existing ones,
does not delete extra labels.

### Auto-Label an Issue

Apply labels based on pattern matching against the issue title and body:

```bash
python3 sdlc_manager.py labels auto-label --repo infiquetra-core --number 42
```

See auto-label rules in `references/labels-reference.md`. Current GitHub issue templates apply
`needs-plan` to actionable cards. The older title-pattern auto-label rules in `labels.json` are
legacy fallback behavior and may still add `needs-analysis` or `needs-triage`.
Treat those as legacy fallback labels, not current template defaults.

### Suggest Labels Without Applying Any

`--suggest` turns the same command into a read-only advisory:

```bash
python3 sdlc_manager.py labels auto-label --repo infiquetra-core --number 42 --suggest
```

It prints the union of the labels the regular-expression rules matched and the labels a typed
judgment considered applicable, each tagged with where it came from — `rule`, `model`, or `both`
— and **applies nothing**. Without the flag the command posts its matches exactly as it always
has; the flag is the only thing that changes, and it removes the write rather than adding one.

Two properties worth knowing before you trust the output:

- **The rules are a floor.** Every label the regular expressions matched appears in the union
  whatever the model says. The model may widen the set; it can never narrow it.
- **A rejection cannot add a label.** The threshold is the answer's probability that the label
  applies, not its confidence. A confident "no" is a low probability and stays out.

**Where the text goes.** The judgment sends the issue's title and body to TypeSafe, a third-party
endpoint, and needs `TYPESAFE_API_KEY` in the environment. Credentials and high-entropy strings are
redacted before anything leaves the machine, and the fleet's data rule
(`plugins/fleet-core/references/typesafe.md`) governs what may be sent at all: issue text is
permitted, transcripts and customer content are not.

If the call fails for any reason, the command prints the rule-derived labels alone with a note
naming the failure — it degrades to today's behavior, never to nothing.

### Create a New Field Option

When a new initiative or objective is introduced, create the corresponding option on the
project board's single-select field:

```bash
# Add a new initiative option to the board
python3 sdlc_manager.py fields create-option --project campps --field initiative --option "platform-stability"

# Add a new objective
python3 sdlc_manager.py fields create-option --project campps --field objective --option "platform-launch"
```

### Discover Project Fields

```bash
python3 sdlc_manager.py fields discover --project campps
```

Shows all fields and their available options with IDs. Useful for confirming field names and
verifying that an initiative/objective option exists before trying to sync.

## Key Behaviors

### Label Rules

- **Every issue must have exactly ONE issue type label**: `capability`, `enhancement`,
  `defect`, `exploration`, or `context-update`
- **Defects must have exactly ONE priority label**: `critical`, `high-priority`,
  `medium-priority`, or `low-priority`
- **Other issue types**: priority is optional
- **AI usage labels**: Add when a PR is created — one per PR, tracks AI generation %
- **Size labels**: Add during Analysis phase — one per capability/enhancement
- **Risk labels**: Add during Analysis phase — one per capability
- **Planning/status labels**: current actionable templates use `needs-plan`; `ready` and
  `blocked` may be managed as work progresses; `needs-analysis` and `needs-triage` are legacy
  fallback labels from older auto-label rules

### Initiative and Objective Fields

Initiative and Objective are project fields. Workflow:

1. Confirm the field exists with `fields discover --project <project>`.
2. Create a missing option with `fields create-option` when needed.
3. Set the field with `flow set-field`.

Convention labels such as `initiative:*` and `objective:*` may still exist in old issues,
but they are not the canonical source of truth.

## Natural Language Examples

**"Label this issue as a capability"**
-> Apply `capability` label via `gh issue edit`

**"Add the high-priority label to defect #88"**
-> `gh issue edit 88 --add-label high-priority --repo Infiquetra/infiquetra-core`

**"This issue belongs to the Platform v1 initiative"**
-> `flow set-field --project campps --repo <repo> --number <N> --field Initiative --option "platform-v1"`

**"Sync the initiative field for issue #42"**
-> `python3 sdlc_manager.py flow set-field --project campps --repo infiquetra-core --number 42 --field Initiative --option <name>`

**"Audit labels on infiquetra-core"**
-> `python3 sdlc_manager.py labels audit --repo infiquetra-core`

**"Deploy SDLC labels to a new repo"**
-> `python3 sdlc_manager.py labels deploy --repo infiquetra-new-service`

**"Auto-label issue #55 based on its title"**
-> `python3 sdlc_manager.py labels auto-label --repo infiquetra-core --number 55`

**"We have a new initiative called platform-stability — add it to the board"**
->
```bash
python3 sdlc_manager.py fields create-option --project campps --field initiative --option "platform-stability"
```

**"What fields does an active board have?"**
-> `python3 sdlc_manager.py fields discover --project campps`

## Reference Documents

- `references/labels-reference.md` — Complete label taxonomy with colors, descriptions,
  auto-label rules, and usage rules
