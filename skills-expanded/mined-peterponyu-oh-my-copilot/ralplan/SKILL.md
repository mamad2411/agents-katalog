---
name: ralplan
description: "[OMCP] Consensus planning entrypoint that auto-gates vague ralph/autopilot/team requests before execution"
orchestrates-agents: "planner, architect, critic"
argument-hint: "[--interactive] [--deliberate] [--architect codex] [--critic codex] <task description>"
level: 4
---

## Provenance Frontmatter Contract (Wave 7 enforcement)

When this skill produces an output file (spec / plan / artifact), it MUST emit YAML frontmatter at the very top of that file with these fields:

- `produced-by: ralplan`
- `produced-at: <ISO-8601 UTC timestamp>`
- `pipeline-stage: plan`

Output target: `.omcp/plans/<slug>.md`. The smoke test at `scripts/smoke-copilot-cli.sh` asserts this chain end-to-end.

**Pipeline transition recording**: After writing the output artifact, call the `mcp__omcp__pipeline_record_transition` tool with `from: "spec"`, `to: "plan"`, `artifact_path: "<absolute-path-to-the-artifact-just-written>"`. For ralplan, `from: "spec", to: "plan"`. This records the transition in `.omcp/state/pipeline-state.json` so subsequent stages and the smoke test can verify the chain.

# Ralplan (Consensus Planning Alias)

**Ralplan = `/omcp:plan --consensus`. The procedure lives in the plan skill.**

Ralplan is a shorthand alias for `/omcp:plan --consensus`. It triggers iterative planning with Planner, Architect, and Critic agents until consensus is reached, with **RALPLAN-DR structured deliberation** (short mode by default, deliberate mode for high-risk work). The full step-by-step consensus procedure — RALPLAN-DR summary, the sequential Architect → Critic passes, the max-5-iteration re-review loop, and the `--interactive` / `--deliberate` / `--architect codex` / `--critic codex` flags — is defined once in `skills/plan/SKILL.md` under **Consensus mode (`--consensus`)`**. Follow that procedure, then apply the Provenance Frontmatter Contract above to the output artifact.

## Agent orchestration

This skill gates execution by coordinating `planner`, `architect`, and `critic`
roles. The planner drafts, the architect checks structural soundness, and the
critic enforces testability and fair alternative analysis before execution.

## Usage

```text
/omcp:ralplan "task description"
```

```text
/omcp:ralplan --interactive "task description"
```

This forwards to:

```text
/omcp:plan --consensus <arguments>
```

## Pre-Execution Gate

### Why the Gate Exists

Execution modes (ralph, autopilot, team, ultrawork, ultrapilot) spin up heavy multi-agent orchestration. When launched on a vague request like "ralph improve the app", agents have no clear target — they waste cycles on scope discovery that should happen during planning, often delivering partial or misaligned work that requires rework.

The ralplan-first gate intercepts underspecified execution requests and redirects them through the ralplan consensus planning workflow. This ensures:
- **Explicit scope**: A PRD defines exactly what will be built
- **Test specification**: Acceptance criteria are testable before code is written
- **Consensus**: Planner, Architect, and Critic agree on the approach
- **No wasted execution**: Agents start with a clear, bounded task

### Good vs Bad Prompts

**Passes the gate** (specific enough for direct execution):
- `ralph fix the null check in src/hooks/bridge.ts:326`
- `autopilot implement issue #42`
- `team add validation to function processKeywordDetector`
- `ralph do:\n1. Add input validation\n2. Write tests\n3. Update README`
- `ultrawork add the user model in src/models/user.ts`

**Gated — redirected to ralplan** (needs scoping first):
- `ralph fix this`
- `autopilot build the app`
- `team improve performance`
- `ralph add authentication`
- `ultrawork make it better`

**Bypass the gate** (when you know what you want):
- `force: ralph refactor the auth module`
- `! autopilot optimize everything`

### When the Gate Does NOT Trigger

The gate auto-passes when it detects **any** concrete signal. You do not need all of them — one is enough:

| Signal Type | Example prompt | Why it passes |
|---|---|---|
| File path | `ralph fix src/hooks/bridge.ts` | References a specific file |
| Issue/PR number | `ralph implement #42` | Has a concrete work item |
| camelCase symbol | `ralph fix processKeywordDetector` | Names a specific function |
| PascalCase symbol | `ralph update UserModel` | Names a specific class |
| snake_case symbol | `team fix user_model` | Names a specific identifier |
| Test runner | `ralph npm test && fix failures` | Has an explicit test target |
| Numbered steps | `ralph do:\n1. Add X\n2. Test Y` | Structured deliverables |
| Acceptance criteria | `ralph add login - acceptance criteria: ...` | Explicit success definition |
| Error reference | `ralph fix TypeError in auth` | Specific error to address |
| Code block | `ralph add: \`\`\`ts ... \`\`\`` | Concrete code provided |
| Escape prefix | `force: ralph do it` or `! ralph do it` | Explicit user override |

### End-to-End Flow Example

1. User types: `ralph add user authentication`
2. Gate detects: execution keyword (`ralph`) + underspecified prompt (no files, functions, or test spec)
3. Gate redirects to **ralplan** with message explaining the redirect
4. Ralplan consensus runs (procedure in `skills/plan/SKILL.md`):
   - **Planner** creates initial plan (which files, what auth method, what tests)
   - **Architect** reviews for soundness
   - **Critic** validates quality and testability
5. On consensus approval, user chooses execution path:
   - **team**: parallel coordinated agents (recommended)
   - **ralph**: sequential execution with verification
6. Execution begins with a clear, bounded plan

### Troubleshooting

| Issue | Solution |
|-------|----------|
| Gate fires on a well-specified prompt | Add a file reference, function name, or issue number to anchor the request |
| Want to bypass the gate | Prefix with `force:` or `!` (e.g., `force: ralph fix it`) |
| Gate does not fire on a vague prompt | The gate only catches prompts with <=15 effective words and no concrete anchors; add more detail or use `/ralplan` explicitly |
| Redirected to ralplan but want to skip planning | In the ralplan workflow, say "just do it" or "skip planning" to transition directly to execution |
