---
name: herdr-pi-subagents
description: Use when user asks to spawn, launch, delegate work to, or coordinate Pi subagents through Herdr tabs. Supports 67 specialized agents across code review, architecture, build resolution, security, networking, ML, mobile, and more.
---

# Herdr Pi Subagents — Agent Catalog

Master orchestrator owns user communication. Pick agent(s) from catalog below, spawn as named panes in batch tab, delegate tasks, collect results, verify, close tab.

Apply applicable `orchestrator` policy to every delegation.

## Orchestration Policy

Before non-trivial work, master must establish: requested outcome, file scope, and relevant code/API patterns. Do not guess. Resolve user-facing ambiguity before spawn; use a scout or researcher for codebase or current-documentation gaps.

- Give each subagent all needed task context: role, goal, scope, constraints, prior scout/research findings, and required output. Subagents have no master-session context.
- Parallelize only independent scopes. Serialize overlapping files or shared configuration.
- Keep master context clean: delegate codebase exploration rather than broad direct reads.
- Workers investigate root cause before changes, make only requested changes, and run relevant verification. Master independently checks claims before reporting completion.

## Agent Catalog

Each agent file in `agents/` defines a specialized agent with frontmatter:

- `name` — agent identifier
- `description` — what it does (use to match task to agent)
- `model` — effort: `low` | `medium` | `high`
- `tools` — allowed tools
- `color` — optional pane color

The rest of the file is the agent's system prompt (role, workflow, rules, examples).

### Browse & Select

```bash
# List all agents with description
ls agents/*.md

# Check specific agent metadata
head -7 agents/<name>.md

# Search by keyword
rg -l "keyword" agents/
rg "description:.*keyword" agents/

# Read full system prompt
cat agents/<name>.md
```

### Full Agent Reference

| #   | Agent                     | Effort | Tools                             | Purpose                                         |
| --- | ------------------------- | ------ | --------------------------------- | ----------------------------------------------- |
| 1   | `a11y-architect`          | medium | Read,Write,Edit,Grep,find, ls     | WCAG 2.2 compliance, accessible UI              |
| 2   | `agent-evaluator`         | medium | Read,Grep,find, ls,Bash               | 5-axis quality assessment                       |
| 3   | `architect`               | high   | Read,Grep,find, ls                    | System design, scalability, ADRs                |
| 4   | `build-error-resolver`    | medium | Read,Write,Edit,Bash,Grep,find, ls    | Fix build/type errors fast                      |
| 5   | `chief-of-staff`          | medium | Read,Grep,find, ls,Bash,Edit,Write    | Communication triage & draft                    |
| 6   | `code-architect`          | medium | Read,Grep,find, ls,Bash               | Feature architecture from patterns              |
| 7   | `code-explorer`           | medium | Read,Grep,find, ls                    | Trace execution, map architecture               |
| 8   | `code-reviewer`           | medium | Read,Grep,find, ls,Bash               | General code quality review                     |
| 9   | `code-simplifier`         | medium | Read,Write,Edit,Bash,Grep,find, ls    | Clarify, deduplicate, simplify                  |
| 10  | `comment-analyzer`        | low    | Read,Grep,find, ls                    | Comment rot, accuracy, completeness             |
| 11  | `conversation-analyzer`   | low    | Read,Grep                         | Extract hook-worthy behaviors                   |
| 12  | `cpp-build-resolver`      | medium | Read,Write,Edit,Bash,Grep,find, ls    | C++/CMake build errors                          |
| 13  | `cpp-reviewer`            | medium | Read,Grep,find, ls,Bash               | C++ memory safety, modern idioms                |
| 14  | `csharp-reviewer`         | medium | Read,Grep,find, ls,Bash               | .NET, async, nullable, performance              |
| 15  | `dart-build-resolver`     | medium | Read,Write,Edit,Bash,Grep,find, ls    | Dart/Flutter build & pub errors                 |
| 16  | `database-reviewer`       | medium | Read,Grep,find, ls,Bash               | PostgreSQL, schema, queries                     |
| 17  | `django-build-resolver`   | medium | Read,Write,Edit,Bash,Grep,find, ls    | Django/pip/migration errors                     |
| 18  | `django-reviewer`         | medium | Read,Grep,find, ls,Bash               | Django ORM, DRF, security                       |
| 19  | `docs-lookup`             | low    | Read,Grep,web_search,fetch_content        | Live API/docs lookup via web search             |
| 20  | `doc-updater`             | low    | Read,Write,Edit,Bash,Grep,find, ls    | Codemaps, README, guides                        |
| 21  | `e2e-runner`              | medium | Read,Write,Edit,Bash,Grep,find, ls    | E2E tests (playwright)                          |
| 22  | `fastapi-reviewer`        | medium | Read,Grep,find, ls,Bash               | FastAPI async, Pydantic, security               |
| 23  | `flutter-reviewer`        | medium | Read,Grep,find, ls,Bash               | Flutter widgets, state, Dart                    |
| 24  | `fsharp-reviewer`         | medium | Read,Grep,find, ls,Bash               | F# functional, type safety                      |
| 25  | `gan-evaluator`           | medium | Read,Write,Bash,Grep,find, ls         | GAN Harness eval (color: red)                   |
| 26  | `gan-generator`           | medium | Read,Write,Edit,Bash,Grep,find, ls    | GAN Harness implement (color: green)            |
| 27  | `gan-planner`             | medium | Read,Write,Grep,find, ls              | GAN Harness spec (color: purple)                |
| 28  | `go-build-resolver`       | medium | Read,Write,Edit,Bash,Grep,find, ls    | Go build/vet errors                             |
| 29  | `go-reviewer`             | medium | Read,Grep,find, ls,Bash               | Go idioms, concurrency, errors                  |
| 30  | `harmonyos-app-resolver`  | medium | Read,Write,Edit,Bash,Grep,find, ls    | ArkTS/ArkUI, HarmonyOS                          |
| 31  | `harness-optimizer`       | medium | Read,Grep,find, ls,Bash,Edit          | Agent harness reliability (color: teal)         |
| 32  | `healthcare-reviewer`     | high   | Read,Grep,find, ls                    | Clinical safety, PHI, CDSS                      |
| 33  | `homelab-architect`       | medium | Read,Grep                         | Home/small-lab network design                   |
| 34  | `java-build-resolver`     | medium | Read,Write,Edit,Bash,Grep,find, ls    | Java/Maven/Gradle build errors                  |
| 35  | `java-reviewer`           | medium | Read,Grep,find, ls,Bash               | Spring Boot, Quarkus, JPA                       |
| 36  | `kotlin-build-resolver`   | medium | Read,Write,Edit,Bash,Grep,find, ls    | Kotlin/Gradle build errors                      |
| 37  | `kotlin-reviewer`         | medium | Read,Grep,find, ls,Bash               | Kotlin coroutines, Compose                      |
| 38  | `loop-operator`           | medium | Read,Grep,find, ls,Bash,Edit          | Autonomous loop control (color: orange)         |
| 39  | `marketing-agent`         | medium | Read,Grep,find, ls,WebSearch,WebFetch | Campaigns, copy, positioning                    |
| 40  | `mle-reviewer`            | medium | Read,Grep,find, ls,Bash               | ML pipelines, training, serving                 |
| 41  | `network-architect`       | medium | Read,Grep                         | Network architecture design                     |
| 42  | `network-config-reviewer` | medium | Read,Grep                         | Router/switch config review                     |
| 43  | `network-troubleshooter`  | medium | Read,Bash,Grep                    | Connectivity & DNS diagnosis                    |
| 44  | `opensource-forker`       | low    | Read,Write,Edit,Bash,Grep,find, ls    | Fork & strip secrets for OSS                    |
| 45  | `opensource-packager`     | low    | Read,Write,Edit,Bash,Grep,find, ls    | OSS packaging (README, LICENSE)                 |
| 46  | `opensource-sanitizer`    | medium | Read,Grep,find, ls,Bash               | Verify fork is clean for release                |
| 47  | `performance-optimizer`   | medium | Read,Write,Edit,Bash,Grep,find, ls    | Speed, bundles, memory, renders                 |
| 48  | `php-reviewer`            | medium | Read,Grep,find, ls,Bash               | PHP PSR-12, Eloquent, security                  |
| 49  | `planner`                 | high   | Read,Grep,find, ls                    | Feature/refactor implementation plans           |
| 50  | `pr-test-analyzer`        | medium | Read,Grep,find, ls,Bash               | PR test coverage quality                        |
| 51  | `python-reviewer`         | medium | Read,Grep,find, ls,Bash               | Python PEP 8, types, security                   |
| 52  | `pytorch-build-resolver`  | medium | Read,Write,Edit,Bash,Grep,find, ls    | PyTorch shape/CUDA/gradient errors              |
| 53  | `react-build-resolver`    | medium | Read,Write,Edit,Bash,Grep,find, ls    | React build failures (Vite/Webpack/CRA/Next.js) |
| 54  | `react-reviewer`          | medium | Read,Grep,find, ls,Bash               | Hooks, render perf, RSC, a11y                   |
| 55  | `refactor-cleaner`        | medium | Read,Write,Edit,Bash,Grep,find, ls    | Dead code removal (knip, depcheck)              |
| 56  | `rust-build-resolver`     | medium | Read,Write,Edit,Bash,Grep,find, ls    | Cargo build, borrow checker                     |
| 57  | `rust-reviewer`           | medium | Read,Grep,find, ls,Bash               | Ownership, lifetimes, unsafe                    |
| 58  | `security-reviewer`       | medium | Read,Grep,find, ls,Bash               | OWASP Top 10, secrets, injection                |
| 59  | `seo-specialist`          | medium | Read,Grep,find, ls,WebSearch,WebFetch | Technical SEO, structured data                  |
| 60  | `silent-failure-hunter`   | medium | Read,Grep,find, ls,Bash               | Swallowed errors, bad fallbacks                 |
| 61  | `spec-miner`              | high   | Read,Grep,find, ls,Bash,Write         | Behavioral spec extraction                      |
| 62  | `swift-build-resolver`    | medium | Read,Write,Edit,Bash,Grep,find, ls    | Swift/Xcode build errors                        |
| 63  | `swift-reviewer`          | medium | Read,Grep,find, ls,Bash               | Swift protocols, ARC, concurrency               |
| 64  | `tdd-guide`               | medium | Read,Write,Edit,Bash,Grep         | Red-green-refactor enforcement                  |
| 65  | `type-design-analyzer`    | medium | Read,Grep,find, ls                    | Encapsulation, invariants                       |
| 66  | `typescript-reviewer`     | medium | Read,Grep,find, ls,Bash               | TS type safety, async, security                 |
| 67  | `vue-reviewer`            | medium | Read,Grep,find, ls,Bash               | Composition API, reactivity, Pinia              |

## Preconditions

- Need concrete task. If missing detail materially changes work, master asks user before spawn.
- Run only inside Herdr:

```bash
test "$HERDR_ENV" = 1 || { echo "Not inside Herdr"; exit 1; }
```

## Spawn Batch

Create one new tab per subagent batch in master workspace. Never split master tab under 5 agents. Every subagent lives in a named pane inside batch tab; never create one tab per agent.

For three agents: launch first in root pane, split root `right` (vertical divider), then split new right pane `down` (horizontal divider). Result: one left pane plus upper-right and lower-right panes. For fourth agent, split left pane `down` on the tallest pane; for further agents, split largest pane and alternate direction to keep layout as balanced as possible.

When spawning more than five agents, utilize two tabs, not just panes. When more than ten agents, use three tabs.

### Prepare: resolve workspace and master pane

```bash
read -r WORKSPACE MASTER_PANE < <(
  herdr pane list | python3 -c '
import json, sys
for pane in json.load(sys.stdin)["result"]["panes"]:
    if pane["focused"]:
        print(pane["workspace_id"], pane["pane_id"])
        break
else:
    raise SystemExit("No focused master pane")'
)

BATCH_LABEL="subagents-<batch-slug>"
TAB_RESULT=$(herdr tab create --workspace "$WORKSPACE" --label "$BATCH_LABEL" --no-focus)
BATCH_TAB=$(printf '%s' "$TAB_RESULT" | python3 -c 'import json,sys; print(json.load(sys.stdin)["result"]["tab"]["tab_id"])')
ROOT_PANE=$(printf '%s' "$TAB_RESULT" | python3 -c 'import json,sys; print(json.load(sys.stdin)["result"]["root_pane"]["pane_id"])')
```

### Launch: select agent from catalog, read config, launch

For each agent you want to spawn:

1. **Select** the right agent from the catalog table above by matching description to task
2. **Read** its agent file to get the exact system prompt: `cat agents/<name>.md`
3. **Extract** the system prompt content (everything below the frontmatter `---` block)
4. **Launch** with the agent's system prompt and the subagent wrapper

```bash
launch_agent() {
  local pane="$1" agent_name="$2" pane_label="$3"

  herdr pane rename "$pane" "$pane_label"
  herdr pane run "$pane" "pi --exclude-tools ask_user_question --append-system-prompt \"You are a scoped subagent working for a master orchestrator in another Herdr pane. Complete only delegated role and task. Do not use ask_user_question. Do not ask user questions by any channel. Do not spawn or delegate to other agents. Work from supplied context, then inspect only assigned scope. Do not guess code or API behavior: report missing evidence or use least-risk reversible assumption. Investigate root cause before changing code; avoid unrelated refactors. Report evidence, changed files, commands run, verification, blockers, and assumptions to master orchestrator.\""
  herdr wait output "$pane" --match "[Prompts]" --timeout 30000 \
    || { herdr pane read "$pane" --source recent --lines 40; return 1; }
}
```

### Spawn example: three agents in balanced layout

```bash
# Agent 1: Read agent file, extract config
AGENT_FILE="agents/typescript-reviewer.md"
AGENT_NAME="typescript-reviewer"
# Read the full agent prompt from the file for use in the task
AGENT_PROMPT=$(cat "$AGENT_FILE")

launch_agent "$ROOT_PANE" "$AGENT_NAME" "subagent-ts-review"

# Agent 2: Split right
RESEARCH_PANE=$(herdr pane split "$ROOT_PANE" --direction right --no-focus \
  | python3 -c 'import json,sys; print(json.load(sys.stdin)["result"]["pane"]["pane_id"])')
launch_agent "$RESEARCH_PANE" "security-reviewer" "subagent-security-review"

# Agent 3: Split research pane down
WORKER_PANE=$(herdr pane split "$RESEARCH_PANE" --direction down --no-focus \
  | python3 -c 'import json,sys; print(json.load(sys.stdin)["result"]["pane"]["pane_id"])')
launch_agent "$WORKER_PANE" "planner" "subagent-planner"

SUBAGENT_PANES=("$ROOT_PANE" "$RESEARCH_PANE" "$WORKER_PANE")
```

`--no-focus` keeps master focused. Returned IDs are source of truth; never guess IDs. `pane rename` is mandatory before launching Pi.

## Delegate Task

Set `SUB_PANE` to target named pane, then set task. The task MUST include the agent's full system prompt (read from its agent file) followed by the specific delegated work.

**Important**: The agent file's system prompt (everything after the frontmatter `---` block) defines the agent's role, workflow, rules, and domain expertise. Include it in the task so the subagent knows its specialization.

```bash
SUB_PANE="$ROOT_PANE"  # or RESEARCH_PANE / any agent pane
AGENT_PROMPT=$(cat "agents/typescript-reviewer.md")  # read the full agent file

TASK=$(cat <<'TASK_PROMPT'
Role: typescript-reviewer
Agent specialization (loaded from agents/typescript-reviewer.md):

<insert agent file content here — everything after the frontmatter --- block>

— Task —

Scope: <files or area>
Context: <prior findings, API docs, or none>
Task: <specific goal>
Constraints: <requirements>
Required output: <findings | diff + tests | sources>

Finish independently. Do not use ask_user_question or request clarification. Do not exceed scope. Report result to master with evidence, changed files, commands run, verification, blockers, and assumptions.
TASK_PROMPT
)
herdr pane send-text "$SUB_PANE" "$TASK"
herdr pane send-keys "$SUB_PANE" Enter
```

**Practical pattern**: Instead of embedding the agent file inline in the heredoc, read it and build the task programmatically:

```bash
AGENT_FILE="agents/typescript-reviewer.md"
AGENT_CONTENT=$(cat "$AGENT_FILE")
SUB_PANE="$ROOT_PANE"
TASK="Role: typescript-reviewer

${AGENT_CONTENT}

--- Task ---

Scope: src/api/
Task: Review the new auth middleware for security issues, type safety, and error handling.
Context: PR adds JWT-based auth with refresh tokens, uses bcrypt for password hashing.
Constraints: Check for token leakage, timing attacks, proper error sanitization.
Required output: List of findings with severity (CRITICAL/HIGH/MEDIUM) and file locations."
herdr pane send-text "$SUB_PANE" "$TASK"
herdr pane send-keys "$SUB_PANE" Enter
```

### Task Template

Every task should follow this structure:

```
Role: <agent-name from catalog>

<full agent file content — system prompt>

--- Task ---

Scope: <files or area>
Context: <prior findings, API docs, link to PR/code>
Task: <specific goal>
Constraints: <requirements, tool limits, time budget>
Required output: <file map | sources | diff + tests | findings>

Finish independently. Do not ask questions. Do not exceed scope. Report with evidence.
```

The `Role:` line helps the subagent understand its identity. The agent file content (system prompt) gives it domain expertise. The `--- Task ---` section is the actual work order.

## Observe and Integrate

For independent work, keep running panes visible. For result needed now:

```bash
herdr wait agent-status "$SUB_PANE" --status done --timeout 120000
herdr pane read "$SUB_PANE" --source recent-unwrapped --lines 100
```

Master verifies subagent claims. Do not treat report as proof. After reading and verifying every pane result, close entire batch tab; this removes all subagent panes. Never leave completed batch tabs open.

```bash
for pane in "${SUBAGENT_PANES[@]}"; do
  herdr wait agent-status "$pane" --status done --timeout 120000
  herdr pane read "$pane" --source recent-unwrapped --lines 100
done
# Verify reports and worktree first, then clean up all subagents at once.
herdr tab close "$BATCH_TAB"
```

## Constraints

| Rule                          | Enforcement                                                                   |
| ----------------------------- | ----------------------------------------------------------------------------- |
| One batch tab, same workspace | `tab create --workspace "$WORKSPACE"` once per batch                          |
| Named panes                   | `pane rename` for every root/split pane before `pi`                           |
| Master stays focused          | `--no-focus`                                                                  |
| No user-question tool         | `--exclude-tools ask_user_question` plus system prompt                        |
| No unclear task delegation    | Master clarifies or scouts/researches before spawn                            |
| Evidence before completion    | Worker verifies; master independently checks report                           |
| Agent file is ground truth    | Read the agent file for system prompt; do not use stale or summarized content |

## Failures

- `HERDR_ENV` absent: stop; cannot manage focused pane safely.
- Pi startup wait times out: read pane output; report failure to master. Do not send task blind.
- Subagent blocked: master resolves blocker; subagent never asks user directly.
- Pi startup fails (provider off, rate limit, auth error): after retry with different model, report blocker.
- Batch complete: master reads and verifies all pane results, then runs `herdr tab close "$BATCH_TAB"`.
- Agent file not found or corrupted: report to master with exact filename; do not substitute a different agent.
