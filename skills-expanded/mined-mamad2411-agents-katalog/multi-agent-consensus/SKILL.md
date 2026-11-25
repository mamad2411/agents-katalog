---
name: multi-agent-consensus
description: |
  Native Antigravity multi-agent consensus workflow. Spawns parallel workers and reviewers with a 0-10 scoring loop and automatic fix routing.
when_to_use: |
  Use this skill when you want to execute a non-trivial plan using a team of autonomous subagents.
  - The plan has 3+ steps, touches 3+ files, or involves docs/specs
  - The plan involves multiple parallel work streams
  - The user says: "agent team", "use agents", "set up a team", "consensus review", "agentic approach", "run this with agents"
---

# Multi-Agent Consensus Skill

This skill provides a structured workflow for executing plans using Antigravity's native subagent capabilities. You (the main agent) will act as the **Team Lead**. You will use the `invoke_subagent` tool to spawn workers and reviewers, orchestrate their execution, and enforce a strict consensus protocol.

## Receipt-backed deliberation

Before any run claims multi-strategy coverage, materialize the closed manifest defined by
`plugins/multi-agent-consensus/references/deliberation-manifest-schema.json`. Bind the current sanitized host-capability receipt,
declare every applicable strategy, requested model and effort, allowed tools, execution bounds,
expected result fields, convergence rule, retry limit, and escalation policy before dispatch.

Use native agents only when `agy.agent.execution=passed`. When that capability is `unknown` or
`unavailable`, separately isolated sequential conversations may substitute only when
`agy.sequential.isolation=passed`; ordinary same-context role-play never counts. Each execution emits
one result with a unique execution ID. Validate the results with
`plugins/multi-agent-consensus/scripts/deliberation.py`; missing,
duplicate, malformed, or failed coverage follows the manifest's bounded recovery policy, and an
incomplete receipt blocks completion.

From a target repository, resolve the installed plugin and run the complete command rather than
searching that repository for plugin source:

```bash
CONSENSUS_PLUGIN_ROOT="${AGY_PLUGIN_ROOT:-$HOME/.gemini/config/plugins/multi-agent-consensus}"
python3 "$CONSENSUS_PLUGIN_ROOT/scripts/deliberation.py" evaluate \
  --repo-root . --outcome-id <outcome-id> \
  --manifest <manifest.json> --results <results.json> \
  --convergence <convergence.json> --escalation <escalation.json>
```

The command prints the repository-relative receipt path. A non-zero exit blocks the deliberation.

Keep requested and observed model, effort, tools, isolation, and worker facts separate. Leave
unobserved values as `unknown`. Convergence preserves material disagreement, evidence, and
adjudication. A complete receipt can bind into Saga as `deliberation-receipt` evidence; it does not
create a competing settlement state.

## Step 1: Worker Kickoff

1. Break the plan down into independent phases or work streams.
2. For each independent work stream, define a concise task description.
3. Use a single `invoke_subagent` tool call to launch all parallel workers at once.
   - Set `TypeName: "self"` (or `"research"` if it's a read-only task).
   - Set `Role: "[Phase Name] Worker"`.
   - Set `Prompt: "[Task description and codebase context]"`.
4. **Wait** for all workers to finish their tasks and report back via native reactive wakeups. If a worker gets blocked, read their message and send them unblocking instructions using `send_message`.

## Step 2: Reviewer Kickoff

Once the workers have completed their implementations, you must run the **Consensus Protocol**.

1. Identify the necessary Reviewer personas for the changes made.
   - **Base Reviewers** (Always include these 3): `devils-advocate-reviewer`, `security-reviewer`, `architecture-reviewer`.
   - **Optional Reviewers**: Include others if relevant (e.g., `api-reviewer`, `testing-reviewer`, `infra-reviewer`, `privacy-reviewer`, `clarity-reviewer`, `code-quality-reviewer`, `ai-usefulness-reviewer`).
2. Read the selected personas from the `multi-agent-consensus/skills/multi-agent-consensus/references/personas/` directory to get their system prompts.
3. Read the review criteria from `multi-agent-consensus/skills/multi-agent-consensus/references/review-criteria.md`.
4. Gather the git diff of the changes made by the workers. Filter out lockfiles and binary assets to save tokens.
5. Use `invoke_subagent` to spawn the reviewers concurrently.
   - Set `TypeName: "self"`.
   - Set `Role: "[Reviewer Name]"`.
   - Set `Prompt: "[Persona Instructions] + [Review Criteria] + Please review the following diff: [Git Diff]"`.

## Step 3: Consensus Cycle & Fix Routing

1. Wait for all reviewers to reply with their evaluations and their 0-10 scores.
2. **Consensus Check**: All reviewers must score **>= 9.0/10**.
   - If **ALL >= 9.0**: Consensus reached! Proceed to Completion (Step 4).
   - If **ANY < 9.0**: Consensus NOT reached. Consolidate and deduplicate their fix requests.
3. **Fix Routing**:
   - For minor textual or formatting fixes, you (the Team Lead) should implement them directly to save time.
   - For complex logic or architectural fixes, use `send_message` to send the consolidated feedback back to the specific worker subagent(s) that originally wrote the code.
4. **Re-Review**: Once fixes are applied, use `send_message` to send the updated diff ONLY to the reviewers who previously scored < 9.0. (Do not recreate the subagents, just message the active ones).
5. **Cycle Cap**: Repeat this process for a maximum of **3 iterations**. After 3 iterations, proceed to Completion regardless of scores, but document the unresolved issues.
   - *Blocking Exception*: If any Security or Auth dimension scores < 5.0, immediately halt the process and flag the issue to the user. This is a hard stop.

## Step 4: Completion

Generate a summary report for the user detailing:
1. How many review cycles were run.
2. The final scores and verdicts from all reviewers in a markdown table.
3. Whether consensus was reached.
4. Any unresolved issues (if the 3-cycle cap was hit).
5. A summary of the final changes implemented.

## Step 4: Validators and Automation Gates

Before completing the consensus process, you must run automated validators to check for regressions.
Validators are static subagents in `plugins/multi-agent-consensus/agents/` that should be invoked with `TypeName`.

Validator configurations can be found in `.multi-agent-consensus.json` which specifies:
- `required_validators`
- `disabled_validators`
- `nonprod_workflows`
- `scenario_hints`
- `smoke_targets`

Write validator evidence state to `.gemini/multi-agent-consensus/validators/`.

Automation is allowed only when all conditions are true:
- Remote matches `github.com/infiquetra/*`.
- The workflow is explicitly nonprod or publish-nonprod.
- Reviewer consensus and scanner gates passed.

Run testers after deployment. If testers hard-fail, run a maximum 3 remediation loops before escalating to the user.


### Reference Files
- `multi-agent-consensus/references/deliberation-manifest-schema.json`
- `multi-agent-consensus/scripts/deliberation.py`
- `multi-agent-consensus/skills/multi-agent-consensus/references/reviewer-registry.md`
- `multi-agent-consensus/skills/multi-agent-consensus/references/review-criteria.md`
- `multi-agent-consensus/skills/multi-agent-consensus/references/consensus-protocol.md`
- `multi-agent-consensus/skills/multi-agent-consensus/references/validator-registry.md`
- `multi-agent-consensus/skills/multi-agent-consensus/references/validator-criteria.md`
- `multi-agent-consensus/skills/multi-agent-consensus/references/validator-execution-order.md`
- `multi-agent-consensus/skills/multi-agent-consensus/references/validator-evidence-state.md`
- `multi-agent-consensus/skills/multi-agent-consensus/references/validator-spawn-quirks.md`
