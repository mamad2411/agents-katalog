---
name: devel-jb-cli-e2e-test
description: "| | **Scope** | Skillshare project-specific E2E | General-purpose runbook authoring | | **Infrastructure** | Devcontainer, ssenv, binary build | None — format and assertions only | | **Config** | `ai_docs/tests/runbook."
domain: cybersecurity
---

|
| **Scope** | Skillshare project-specific E2E | General-purpose runbook authoring |
| **Infrastructure** | Devcontainer, ssenv, binary build | None — format and assertions only |
| **Config** | `ai_docs/tests/runbook.json` (build, setup, teardown) | Assertion types, snapshot, coverage |
| **Lessons** | Checklist items, CLI flag gotchas | `.mdproof/lessons-learned.md` |
| **When** | Running or debugging a test | Writing or improving a runbook |

### How they work together

1. **Writing a new runbook** → invoke `/mdproof` first for format guidance (assertion types, `jq:` patterns, snapshot usage), then `/cli-e2e-test` to execute it in isolation
2. **Improving existing runbooks** → invoke `/mdproof` for assertion quality review (python3 → jq:, idempotency), then `/cli-e2e-test` to verify changes pass
3. **Debugging failures** → `/cli-e2e-test` Phase 3 step 4 handles manual docker exec; `/mdproof` lessons-learned captures recurring patterns
4. **After a test run** → `/mdproof` Self-Learning section guides recording discoveries to `.mdproof/lessons-learned.md`

### Rule of thumb

- Need to **run** tests or **debug** in devcontainer? → `/cli-e2e-test`
- Need to **write** assertions or **improve** runbook quality? → `/mdproof`
- User says "run extras E2E" → `/cli-e2e-test`
- User says "improve runbook assertions" → `/mdproof` then `/cli-e2e-test` to verify
