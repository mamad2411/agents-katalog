---
name: go-symphony
description: Project scaffolding expert for go-symphony. Use when generating or planning a new Gin-based Go project with PostgreSQL, Supabase, SQLC, Docker, GitHub Actions, WebSocket support, or optional SvelteKit/Next.js frontend integration.
---

# Go Symphony Project Scaffolder

Expert skill for using `go-symphony` effectively in both human-driven and AI-driven workflows. This skill helps an agent decide when to use `plan` versus `create`, how to choose compatible flags, how to avoid interactive prompts, and how to validate the generated project after scaffolding.

## Core Philosophy

> **Scaffolding should be predictable before it is convenient. Always understand what will be generated before generating it.**

`go-symphony` works best when the workflow is:

1. Build a concrete spec.
2. Preview the scaffold plan.
3. Generate the project with explicit flags.
4. Verify the generated files and follow-up commands.

For AI agents, `plan` and `--no-interactive` should be the default posture.

## Thinking Process

When activated, follow this structured approach:

### Step 1: Understand the Desired Project Shape

**Goal:** Identify the exact project combination the user wants before running any scaffold command.

**Key Questions to Ask:**
- Is this a backend-only project or a full-stack project?
- Which database mode is intended: `postgres`, `supabase`, or `none`?
- Are Docker assets actually wanted, or just local code generation?
- Is this for a human workflow or an AI/CI workflow?
- Should dependency installation and external bootstrap steps run now, or later?

**Thinking Framework:**
- "Database choice determines major file layout and bootstrap behavior."
- "Frontend choice determines external CLI requirements."
- "Docker is optional and should be explicit."
- "If the environment may not have a TTY, default to non-interactive mode."

**Actions:**
1. Translate the user's request into a concrete scaffold spec.
2. Normalize choices into the supported enums and features.
3. Identify whether the agent should use `plan`, `create --dry-run`, or `create`.

**Decision Point:** You can say:
- "This project should use [driver], [features], [frontend], and [git mode]."

### Step 2: Validate the Combination Before Execution

**Goal:** Catch invalid or misleading combinations before scaffolding begins.

**Key Questions to Ask:**
- Is `supabase-mode` only being used with `driver=supabase`?
- Are SvelteKit flags only being used with `frontend=sveltekit`?
- Did the user request Docker assets without `feature=docker`?
- Is `--no-interactive` compatible with all required inputs being present?

**Thinking Framework:**
- "A good scaffolder fails early and specifically."
- "Never rely on prompts when automation is possible."

**Actions:**
1. Ensure required flags are present for non-interactive execution.
2. Ensure feature flags match the user's real intent.
3. For AI usage, prefer `--git skip` unless the user explicitly wants git side effects.

**Decision Point:** You can explain:
- "This flag set is valid because each option is compatible with the others."

### Step 3: Preview the Plan First

**Goal:** Use `go-symphony plan` or dry-run mode to understand what will happen before writing files.

**Key Questions to Ask:**
- What files and directories will be created?
- Will any external commands be required?
- Will frontend or Supabase bootstrap steps require extra tooling?
- Is JSON output more useful than human-readable text for this workflow?

**Thinking Framework:**
- "Use `plan` for intent verification."
- "Use JSON when another tool or agent will consume the output."

**Actions:**
1. Run `go-symphony plan` with the intended flags.
2. If the user needs machine-readable output, add `--output json`.
3. Inspect required external steps before moving to `create`.

**Decision Point:** You can state:
- "The plan shows [N] scaffold steps, including [important external steps]."

### Step 4: Generate with the Smallest Safe Side Effects

**Goal:** Run `create` in the safest mode that still satisfies the user's request.

**Thinking Framework - Preferred Modes:**

| Situation | Recommended Command Shape |
|---|---|
| Human exploring options | `go-symphony create` |
| Human wants explicit choices | `go-symphony create --no-interactive ...` |
| AI agent generating files only | `go-symphony create --no-interactive --skip-install ...` |
| Agent needs preview only | `go-symphony plan ...` |
| CI / structured consumers | `go-symphony plan --output json` or `create --output json` |

**Actions:**
1. Prefer `--no-interactive` for automation.
2. Prefer `--skip-install` when follow-up tools will be run separately.
3. Only include `--feature docker` when Docker assets are explicitly wanted.
4. Use `--output json` when the result needs to be parsed by another tool.

**Anti-Patterns to Avoid:**
- Running interactive `create` in CI or non-TTY automation.
- Assuming Postgres should automatically imply Docker assets.
- Passing frontend-specific flags without a matching frontend choice.
- Running bootstrap commands blindly without previewing the plan.

**Decision Point:** You can justify:
- "This create command minimizes side effects while still generating the required scaffold."

### Step 5: Verify the Generated Project

**Goal:** Confirm the scaffold output matches the requested intent.

**Key Questions to Ask:**
- Was the target directory created at the expected path?
- Were optional features actually generated?
- Were unexpected files created?
- Did non-interactive or JSON modes behave correctly?

**Actions:**
1. Check the generated project directory.
2. Verify expected files like `Dockerfile`, `docker-compose.yml`, `.github/workflows`, `sqlc.yaml`, or frontend directories only when requested.
3. Run `go test ./...` in the generated project when feasible.
4. If `--skip-install` was used, explain that dependency/bootstrap commands were intentionally deferred.

**Decision Point:** You can say:
- "The scaffold matches the requested shape and the expected files are present."

### Step 6: Present Results Clearly

**Goal:** Report what was planned or generated in a way that helps the user take the next step immediately.

**Actions:**
1. Summarize the chosen stack.
2. Mention any skipped install/bootstrap behavior.
3. Highlight follow-up commands such as `make run`, `make docker-run`, or frontend dev commands.
4. If JSON was used, explain what the JSON is intended for.

**Decision Point:** The user should be able to answer:
- "What got generated, what was skipped, and what should I run next?"

## Usage

`go-symphony` is a CLI workflow skill, not a shell script wrapper skill. Use the CLI commands directly.

### Plan a Backend-Only Project

```bash
go-symphony plan \
  --name github.com/acme/my-api \
  --driver postgres \
  --feature sqlc \
  --frontend none \
  --git skip
```

### Plan a Full-Stack Project with SvelteKit

```bash
go-symphony plan \
  --name github.com/acme/my-app \
  --driver postgres \
  --feature docker \
  --frontend sveltekit \
  --sveltekit-template minimal \
  --sveltekit-types ts \
  --sveltekit-package-manager pnpm \
  --git skip
```

### Generate Files Without Interactive Prompts

```bash
go-symphony create \
  --name github.com/acme/my-api \
  --driver postgres \
  --feature sqlc \
  --feature docker \
  --frontend none \
  --git skip \
  --no-interactive \
  --skip-install
```

### JSON Output for Agents

```bash
go-symphony plan \
  --name github.com/acme/my-api \
  --driver supabase \
  --supabase-mode init-only \
  --frontend none \
  --git skip \
  --output json
```

## Output

### Human-Readable Plan Output

```text
Planned project: github.com/acme/my-api
1. [create_dir] Create project root (.../my-api)
2. [run_command] Initialize Go module -> go mod init github.com/acme/my-api
3. [write_file] Write backend scaffold files
```

### JSON Plan / Apply Output

```json
{
  "mode": "plan",
  "spec": {
    "project_name": "github.com/acme/my-api",
    "db_driver": "postgres"
  },
  "succeeded": true,
  "steps": [
    {
      "name": "Create project root",
      "kind": "create_dir",
      "status": "planned"
    }
  ]
}
```

## Present Results to User

When presenting results:

1. Start with the chosen stack.
2. Say whether you planned or created the project.
3. Call out optional external tooling requirements.
4. Mention any skipped install/bootstrap behavior.
5. End with the exact next command the user should run.

Suggested structure:

```markdown
Generated a `gin + postgres + sqlc` project plan.

Key points:
- Docker assets are included because `feature=docker` was enabled.
- Frontend bootstrap requires `node` and `npx`.
- Install/bootstrap commands were skipped intentionally.

Next step:
- Run `go-symphony create ...` with the same flags.
```

## Troubleshooting

### `open /dev/tty: device not configured`

Use `--no-interactive` in non-TTY environments.

### Docker assets are missing

Add `--feature docker`. Postgres does not imply Docker assets automatically.

### Supabase flags are rejected

Use `--driver supabase` together with `--supabase-mode init-only` or `--supabase-mode local-db`.

### SvelteKit flags are rejected

Use `--frontend sveltekit` before adding `--sveltekit-template`, `--sveltekit-types`, or `--sveltekit-package-manager`.

### JSON output is needed for automation

Use `plan --output json` first. If creating directly, use `create --output json --no-interactive`.
