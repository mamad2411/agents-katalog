---
name: foundry-init
description: Bootstrap Foundry in a project — create the .foundry state directory, wire settings and CLAUDE.md, pick a profile, and seed memory from what already exists. Use when a project has no .foundry directory yet, when `foundry doctor` reports missing state, or when the user asks to set up Foundry here.
disable-model-invocation: true
argument-hint: "[profile]"
metadata:
  foundry.vertical: core
  foundry.io: "project -> .foundry state"
---

# Initialise Foundry in this project

Sets up the state that every other Foundry asset assumes exists. Idempotent: safe to re-run, and
re-running is the supported repair path.

## When not to use this

Do not run it inside a git worktree. Foundry state belongs to the main checkout, and nothing links
it into a worktree automatically — Foundry registers no `WorktreeCreate` hook. Initialising inside
a worktree creates a second, private `.foundry/` that the main checkout never sees. Do not run it in
a directory that is not a project root.

## Steps

### 1. Detect what this project is

```bash
ls -a
cat package.json 2>/dev/null | head -30
cat pom.xml 2>/dev/null | head -40
cat build.gradle* 2>/dev/null | head -30
git remote -v 2>/dev/null
```

Establish: primary language, build tool, test command, package manager, whether it is a monorepo,
whether it is public. Do not guess any of these — if a signal is absent, record it as unknown.

### 2. Create state

```bash
node "${CLAUDE_PLUGIN_ROOT}/bin/foundry.mjs" init
```

This creates `.foundry/{memory/facts,runbooks,blackboard,metrics,scratch}`, a default
`config.json`, and appends the scratch directory to `.gitignore`.

### 3. Choose enforcement level

Ask the user once, then write it to `.foundry/config.json`:

| Level | Behaviour |
|---|---|
| `gate` (default) | Destructive commands and secret writes are blocked; protected paths escalate to the user |
| `warn` | The same checks run but ask instead of denying |
| `off` | Hooks observe and record only |

### 4. Seed memory from what already exists

Read `README`, any `docs/adr/`, `CONTRIBUTING.md` and the CI configuration. For each durable
decision you find, write a fact with `memory_write`, `source: code` and honest confidence.
Aim for **5 to 15 facts**, not fifty: the index has a 4000-token budget and seeding it with noise
defeats the purpose.

Good first facts: the deployment target, the test command, the branching model, the database and
its version constraint, the authentication approach, any hard non-functional target already agreed.

### 5. Wire the project

Add to the project's `CLAUDE.md` (create it if absent):

```markdown
## Foundry
Project memory index: `.foundry/memory/INDEX.md` (injected automatically at session start).
Retrieve full facts with the `foundry` MCP tool `memory_search`. Do not read `.foundry/memory/facts/` directly.
Before any recurring or error-prone task, check `runbook_list`.
```

Add to `.claude/settings.json` (merge, never overwrite):

```json
{
  "extraKnownMarketplaces": {
    "foundry": { "source": { "source": "github", "repo": "fedcal/foundry" } }
  },
  "enabledPlugins": { "foundry-core@foundry": true }
}
```

### 6. Apply a profile if one was named

Profiles live in `profiles/*.json` in the Foundry repository and select the plugin set, permissions
and MCP servers for a kind of project. Run:

```bash
node "${CLAUDE_PLUGIN_ROOT}/bin/foundry.mjs" profile <name>
```

### 7. Verify

```bash
node "${CLAUDE_PLUGIN_ROOT}/bin/foundry.mjs" doctor
```

Report the result honestly, including anything that failed.

## Definition of done

- `.foundry/` exists with a populated `INDEX.md` under budget.
- `doctor` reports no errors.
- `CLAUDE.md` references the index.
- The user knows which enforcement level is active and how to change it.
