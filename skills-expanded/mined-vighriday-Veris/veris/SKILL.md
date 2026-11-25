---
name: veris
description: Behavioral verification intelligence for autonomous coding agents. Use this skill when the user asks "what could break in this PR?", "which workflows changed?", "what should I test before merging?", "is this change risky?", "what's the blast radius of removing this function?", or any question about understanding the behavioral surface of a TypeScript/JavaScript codebase. Provides workflow grouping (Authentication, Payments, Webhooks, Caching, Queue, etc.), drift detection, counterfactual reasoning, adversarial probe generation, and confidence modeling — entirely local, zero cloud.
---

# Veris — Behavioral Verification Infrastructure

This skill exposes Veris as an MCP server with 17 tools that analyze TypeScript/JavaScript repositories.

## When to Use This Skill

Use this skill when the user:

- Asks "what could break?" / "what's risky?" / "what should I test?" about code changes
- Wants to understand a repo's behavioral structure (workflows, dependencies, blast radius)
- Asks to detect behavioral drift between two states (PR vs main, two runs)
- Asks for concrete adversarial test scenarios (idempotency, retry storms, replay, race conditions)
- Wants a verification budget — "given 15 minutes, what should I test?"
- Asks "what happens if I revert this commit?" (counterfactual reasoning)
- Wants to onboard a new agent or developer to a repo (workflow map)

## Setup

This skill is delivered as an MCP server via the `veris-core` npm package. Configure your agent's MCP settings:

```json
{
  "mcpServers": {
    "veris": {
      "command": "npx",
      "args": ["-y", "veris-core", "mcp"]
    }
  }
}
```

That's it. No API keys. No cloud. State persists locally at `<projectRoot>/.veris/state.db`.

## What the Skill Provides

### 17 MCP Tools

| Tool | Purpose |
|------|---------|
| `analyze_repository` | Full graph + workflow + risk pass on the current repo |
| `export_behavioral_graph` | Returns nodes + edges as JSON for downstream agents |
| `analyze_pr_behavior` | Diff-aware: only what's changed in the current PR |
| `generate_verification_plan` | Tier 1/2/3 verification targets per node |
| `identify_unverified_behaviors` | Nodes flagged risky but no execution coverage |
| `list_workflows` | All 25 semantic workflow domains detected |
| `analyze_workflow` | Drill into one workflow (members, signals, risk, probes) |
| `detect_drift` | Behavioral drift vs prior runs (via SHA-256 fingerprints) |
| `generate_adversarial_probes` | Concrete scenarios per workflow with expected invariants |
| `allocate_budget` | Knapsack-style: best subset to verify in N minutes |
| `what_if_revert` | Counterfactual — what changes if I revert this commit? |
| `report_execution` | Feed test results back to update confidence |
| `confidence_history` | Trend of overall confidence over runs |
| `node_history` | Per-node risk + execution history |
| `export_onboarding` | Generate workflow map for human onboarding |
| `cross_repo_snapshot` | Fleet view across multiple repos |
| `register_repo` | Add a repo to the fleet snapshot |

### What "workflow" means here

Veris classifies every function/class/method into one of 25 semantic domains:

- Authentication, Authorization, Session
- Payments, Billing, Checkout, Cart
- Webhooks, Notifications, Realtime
- Queue, Caching, Persistence, Sync, Search
- Onboarding, Profile, Admin
- Analytics, AI, Routing, Orchestration
- Reporting, Configuration, Infrastructure

Rules live in `data/workflow-rules.json`. Override per repo at `.veris/data/workflow-rules.json`. Add new domains via `.veris/plugins/*.js`.

## Privacy

- MIT license. No paid tier.
- `VERIS_STATE_DISABLED=1` for zero-retention mode (skips all SQLite writes).
- Network permission: none. No telemetry. No phone-home.

## Verify

Veris ships with a synthetic demo app containing 17 planted bugs across 11 workflows:

```bash
git clone https://github.com/vighriday/Veris
cd Veris/examples/demo-app
npx veris-core .
open veris-reports/veris-dashboard.html
```

`GROUND_TRUTH.md` is the answer key — every planted bug + the workflow Veris should detect + the probe it should emit.

## Links

- Repo: <https://github.com/vighriday/Veris>
- NPM: <https://www.npmjs.com/package/veris-core>
- MCP Registry: `io.github.vighriday/veris`
