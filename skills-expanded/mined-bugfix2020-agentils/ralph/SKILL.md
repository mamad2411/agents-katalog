---
name: ralph
description: 'Run the Ralph multi-agent workflow. Triggers: /ralph, run ralph, 启动 ralph, 执行 ralph, ralph loop.'
user-invocable: true
---

# Ralph — Multi-Agent Handoff Workflow

Ralph is the repository's role-isolated AI workflow. The orchestrating agent
routes work to role-specific subagents, and each role writes its own handoff so
the next role can verify evidence instead of trusting a single agent's summary.

## Standard Trigger

Use `/ralph` as the standard trigger across AI tools.

- Claude Code reads generated agents from `.claude/agents/ralph-*.md`.
- GitHub Copilot reads generated custom agents from `.github/agents/ralph-*.agent.md`.
- Codex reads generated custom agents from `.codex/agents/ralph-*.toml`.

The source of truth for these agents is `docs/agents/ralph-*.md`; generated
targets must not be hand-edited.

## When To Use Ralph

`/ralph` is the primary workflow for non-trivial repository work:

- implementing a plan
- changing instructions, skills, agents, or sync behavior
- preparing or verifying a package release
- touching multiple files or multiple package boundaries
- any task that needs independent product/developer/tester evidence

Direct chat is only for plain tasks:

- explanation or code reading
- one-off command output
- tiny text edits with no review or release impact
- status checks that do not mutate tracked files

If a direct chat request turns into non-trivial repo mutation, switch to the
Ralph workflow before editing.

## Core Chain

```text
product -> developer -> ops? -> tester -> contributor? -> beta -> done
```

- `product` clarifies acceptance criteria, non-goals, edge cases, affected
  surfaces, and `requiredStages`.
- `developer` implements only after reading the product handoff.
- `ops` handles CI/CD, changeset, release, or publish configuration when needed.
- `tester` verifies implementation correctness and can send work back to
  `developer` or `product`.
- `contributor` checks docs and instructions from a new-developer perspective.
- `beta` simulates a real user. Only beta may set `passes=true` and commit the
  completed story.

## Dispatch Protocol

The orchestrator communicates with subagents in three phases, modeled after
aviation TOWER ↔ PILOT communication:

### Phase 1: Dispatch (ORCHESTRATOR → SUBAGENT)

When launching a subagent, include these parameters in the prompt:

```
Clearance: <what to do>
Working directory: <run dir>
Restrictions: <read-only? allowed file scope?>
Output: <handoff file path>
```

### Phase 2: Readback (SUBAGENT → ORCHESTRATOR)

The subagent confirms understanding before starting work. This appears in the
subagent's first output.

### Phase 3: Completion (SUBAGENT → ORCHESTRATOR)

The subagent reports completion with structured evidence.

### Standard Checklists

Each role has a **fixed, task-independent** verification checklist defined in
`docs/agents/ralph-checklist.md`. The next role verifies against this standard,
not against what the previous person wrote. See that file for the full
checklists.

## Orchestrator Checklist

Before launching any subagent, the orchestrator MUST:

1. **Create or verify the feature branch** — branch must be checked out from `main`
   and follow `<type>/<short-kebab>` naming (see `branch-name-standard` skill).
2. **Create the run directory** — `scripts/ralph/runs/<run>/`
3. **Create `prd.json`** — include the `branch` field set to the current branch name.
   This is the authoritative link between the PRD and its working branch.
   The pre-commit hook uses it to route commits to the correct PRD.
4. **Verify `prd.branch` is set** — if `branch` is missing or empty, the product
   agent will block the run. Do NOT skip this step.

Example `prd.json` creation:

```sh
BRANCH=$(git branch --show-current)
mkdir -p scripts/ralph/runs/my-feature
cat > scripts/ralph/runs/my-feature/prd.json << EOF
{
    "id": "US-001",
    "title": "...",
    "branch": "$BRANCH",
    ...
}
EOF
```

## Runtime Files

Use one run directory per task:

```text
scripts/ralph/runs/<run>/
  prd.json
  progress.txt
  handoff/product.md
  handoff/developer.md
  handoff/ops.md
  handoff/tester.md
  handoff/contributor.md
  handoff/beta.md
```

Each subagent may read `prd.json`, `progress.txt`, and its immediate
predecessor's handoff. It writes only its own handoff.

## PRD Shape

Each story uses:

```json
{
    "id": "US-001",
    "title": "Story title",
    "description": "As a user, I want ...",
    "branch": "feat/my-feature",
    "acceptanceCriteria": ["Criterion one", "Typecheck passes"],
    "priority": 1,
    "stage": "product",
    "requiredStages": [],
    "passes": false,
    "blocked": false,
    "handoff": {
        "product": false,
        "developer": false,
        "ops": false,
        "tester": false,
        "contributor": false,
        "beta": false
    },
    "notes": ""
}
```

`branch` is set by the orchestrator when creating the run directory. It is the
authoritative link between the PRD and its working branch — the pre-commit hook
uses it to route commits to the correct PRD. Agents must not modify it.

`product` chooses `requiredStages`. `developer` is always first after product;
`beta` is always last.

## Profiles

Profiles specialize the same role chain. The npm release profile is documented
in `docs/skills/ralph/profiles/npm-release.md`.

For release work:

- New npm packages start at `0.0.1` or `0.1.0` in `package.json` depending on maturity.
- Tags use `<full-npm-package-name>@<version>`.
- Local verification is the main gate; CI/CD only backs it up.
- If registry, `npx`/`dlx`, native asset, or GitHub Release behavior cannot be
  fully verified before publish, use `alpha` or `beta` first.

## Runtime Boundary

`scripts/ralph/` is only runtime scaffolding: a PRD template, active run
directories, progress logs, and handoff files. It is not the source of role
behavior.

Role behavior lives in `docs/agents/ralph-*.md` and is generated to each AI
tool's custom-agent location. If the active tool cannot run an autonomous loop,
the orchestrating agent should run the same stages manually and preserve the
handoff contract.
