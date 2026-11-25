---
name: heyeddi-ci-runners
description: "PLACEHOLDER: author eddi-ci.yaml pipeline jobs from live contract + inspect_repo. Spot runners are fail-closed — never claim jobs ran. Use when configuring runners or pipeline YAML."
version: 1.0.0
product-version: 3.4.2
author: HeyEddi-com
---

# HeyEddi CI Runners (PLACEHOLDER)

Author valid Spot **`pipeline:`** jobs in `eddi-ci.yaml` using the living contract. **Execution is not available** — fail-closed until the product ships runners.

## Hard truth (mandatory)

- Spot jobs **do not run** yet
- App may **lint** sealed YAML; that is not execution
- **Never** claim a job ran, succeeded, or was dispatched
- Run `assert_runners_placeholder --check` on any draft that might imply execution

See `reference/placeholder.md`.

## Pipeline

```
load_policy_contract
inspect_repo
→ author/update pipeline: only with evidenced commands + path filters
assert_runners_placeholder --check --agent-text "<your summary>"
tell user: declared but not executed (fail-closed)
```

Prefer `@heyeddi-ci-config` decision gate for whether to create the file at all. Billable / runner knobs need explicit opt-in.

## When Spot runners ship

Hooks for invoke/status will land here. Do **not** invent APIs ahead of the product.

## Tools

| Tool | Purpose |
|------|---------|
| `load_policy_contract` | Living knobs / guide |
| `inspect_repo` | Languages + evidenced commands |
| `assert_runners_placeholder` | Fail-closed claim detector |

## Safety

- Never secrets in YAML
- Never invent test commands
- Never `auto_merge`
- Never merge without **authorize merge**
