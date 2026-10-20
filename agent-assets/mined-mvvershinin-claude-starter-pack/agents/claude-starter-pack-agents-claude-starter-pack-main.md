# Agents and Skills — the detailed guide

## Two mechanisms for extending Claude Code

Claude Code out of the box is one AI that does everything itself. That works for simple tasks. For complex ones you need specialisation. There are two mechanisms:

| | Agents | Skills |
|---|---|---|
| **What it is** | Claude subprocesses with their own rules | Instructions that are loaded into the current session |
| **How it works** | A separate Claude is launched with a separate context | The skill's text is inserted into the current Claude's context |
| **When to use it** | Parallel work, isolation, heavy tasks | Quick actions, templates, procedures |
| **Where they live** | `.claude/agents/` | `.claude/skills/` |
| **How to call one** | Through the Agent tool (Claude decides itself) | Through `/command` (the user calls it) |
| **Context** | Its own (it does not see the whole main session) | Shared (it works in the current session) |
| **Parallelism** | Yes — several agents at once | No — one skill at a time |

---

## Agents

### What they are

An agent is a separate instance of Claude launched as a subprocess. It has:
- Its own system prompt (the file `.claude/agents/XX-name.md`)
- Its own set of tools (Read, Write, Edit, Bash, etc.)
- Its own model (Opus for the hard work, Sonnet for the simple work)
- Its own context (it does not see the main session's whole history)

**An analogy:** you are the project manager. The agents are your team. You give a task to the backend developer, they do it and hand back the result. You do not dictate every line — you give the task and the context.

### How to create an agent

The file `.claude/agents/XX-name.md`:

```markdown
---
name: backend-expert
description: Laravel backend developer
tools: Read, Write, Edit, Grep, Glob, Bash
model: opus
---

# Backend Expert

## Role
You are a senior Laravel developer. You write code following the pattern:
Controller → FormRequest → DTO → Service → Repository → Model

## Rules
- Business logic only in Services
- DB queries only through Repositories
- No mass assignment
[...]

## Checklist before answering
- [ ] The code follows the architectural pattern
- [ ] No hardcoded values
- [ ] Eager loading where it is needed
```

### The frontmatter

```yaml
---
name: agent-name          # A unique name
description: Description  # What it does (one line)
tools: Read, Write, ...   # Which tools are available
model: opus               # The model: opus (stronger) or sonnet (faster/cheaper)
skills: sequential        # Extra skills (optional)
---
```

### The available tools

| Tool | What it does | When to grant it |
|------|--------------|------------------|
| `Read` | Read files | Almost always |
| `Write` | Create files | When the agent writes code |
| `Edit` | Edit files | When the agent changes code |
| `Grep` | Search by content | For exploring the codebase |
| `Glob` | Find files by pattern | For navigating the project |
| `Bash` | Run commands | Carefully — it can be restricted |
| `Agent` | Launch other agents | Only for the coordinator |
| `WebSearch` | Search the internet | For research/debugging |
| `WebFetch` | Fetch web pages | For documentation |

**The principle:** give an agent the minimum set of tools it needs. The critic does not need Write — it only reads and analyses. The coordinator needs Agent — it launches the others.

### Choosing the model

| Model | When to use it | Cost |
|-------|----------------|------|
| **opus** | Code generation, complex logic, architectural decisions | More expensive, slower |
| **sonnet** | Analysis, validation, planning, review | Cheaper, faster |
| **haiku** | Simple tasks, formatting, parsing | The cheapest |

**In practice:** backend-expert and frontend-expert on Opus (they write code), the rest on Sonnet (they analyse).

### How Claude picks an agent

Claude reads each agent's `description` and decides itself which one to launch, based on the task. Or you can say so explicitly through a slash command (`/develop` → backend-expert).

### How agents communicate

Agents **do not talk to each other directly**. The scheme:

```
User → Claude (the main session)
                  ↓
              Coordinator (an agent)
                  ↓
    ┌─────────────┼─────────────┐
    ↓             ↓             ↓
backend-expert  db-expert   frontend-expert
    ↓             ↓             ↓
    └─────────────┼─────────────┘
                  ↓
              Results → Claude → User
```

The coordinator launches the agents, collects the results and passes them on.

---

## The agents in the starter pack

### 00-coordinator (the orchestrator)

**Model:** Opus
**Role:** the single entry point for complex tasks. It decomposes, plans, delegates.
**Call:** `/orchestrate`

```
User: "Add a notification system"
    ↓
The coordinator:
  1. Reads CLAUDE.md, docs/
  2. Breaks it into subtasks
  3. Phase 1: db-expert (schema) + backend-expert (API)
  4. Phase 2: frontend-expert (UI)
  5. Phase 3: test-expert (tests)
  6. Phase 4: architecture-validator + code-critic
  7. If critic < 70 → fixes → re-check
  8. Report to the user
```

### 01-backend-expert

**Model:** Opus
**Role:** writes PHP/Laravel code following the architectural pattern.
**Call:** `/develop`

Knows: Controllers, FormRequests, DTOs, Services, Repositories, Models, Jobs, Resources, Enums, Exceptions. Watches SOLID, DI, no mass assignment, no Facades in business logic.

### 02-frontend-expert

**Model:** Opus
**Role:** writes Vue.js/React code.
**Call:** `/frontend`

Knows: Composition API, `<script setup>`, Pinia, Tailwind, accessibility, loading/error states. Forbidden: Options API, v-html with user data, hardcoded translations.

### 03-db-expert

**Model:** Sonnet
**Role:** database design, migrations, optimization.

Knows: MySQL/PostgreSQL, indexes, foreign keys, JSON columns, full-text search, N+1 prevention, lockForUpdate for race conditions.

### 04-devops-expert

**Model:** Sonnet
**Role:** Docker, deployment, servers, CI/CD.

Knows: docker-compose, Dockerfile, rootless Docker, Nginx/Apache, SSH, nohup, deployment procedures, rollback. NEVER: `docker compose down -v`.

### 05-test-expert

**Model:** Sonnet
**Role:** writes tests.
**Call:** `/test`

Knows: PHPUnit (unit + feature), Jest (Vue), factories, mocks, coverage goals (100% critical, 80% services, 60% overall).

### 06-architecture-validator

**Model:** Sonnet
**Role:** checks the code against the pattern checklist.
**Call:** `/validate`

Checks every layer: Controller (thin?), FormRequest (toDTO?), Service (no DB?), Repository (no logic?), Model (no $fillable?), DTO (readonly?). Produces a score of 0-100.

### 07-code-critic

**Model:** Sonnet
**Role:** adversarial review — it looks for what will break.
**Call:** `/review`

Checks: OWASP Top 10, bugs, performance, N+1, race conditions, the frontend↔backend contract, data compatibility. Verdict: APPROVE (≥70) / REQUEST_CHANGES / BLOCK (<50).

### 08-api-architect

**Model:** Opus
**Role:** designs the REST API — endpoints, HTTP methods, status codes, request/response contracts.

Knows: RESTful conventions, API versioning (/api/v1), status codes, error format, naming conventions (plural nouns, kebab-case). Works in a pair with backend-expert: the architect designs → the expert implements.

### 09-integrations-expert

**Model:** Opus
**Role:** integration with external services — APIs, webhooks, queues.

Knows: the Interface + Mock + Real pattern, Service Provider binding for mock/real switching, a timeout on every request, custom exceptions for service unavailability. Mandatory: credentials only through .env, logs without PII.

### 10-kafka-expert

**Model:** Opus
**Role:** Apache Kafka integration — producers, consumers, Schema Registry.

Knows: RdKafka, SASL_SSL, Confluent wire format, consumer groups, dead-letter queues. Producer/Consumer are separate classes, not in Services. Schema validation before producing. Config through .env.

### 11-s3-expert

**Model:** Opus
**Role:** file storage — S3, Yandex Object Storage, MinIO.

Knows: config/filesystems.php, signed URLs, `guessExtension()` (NEVER `getClientOriginalExtension()`), random file names (`bin2hex(random_bytes(16))`), FormRequest MIME validation. Never serve files directly — only through a Laravel route.

### TEMPLATE-domain-expert

**Model:** task-dependent
**Role:** the template for a domain expert — it knows the project's business logic.

You fill in: entities, business rules, critical flows, race conditions, terminology. The other agents consult it for context.

---

## Skills

### What they are

A skill is a markdown file of instructions that is loaded into the current Claude session on command. Unlike an agent, a skill **does not create a separate process** — it extends the current Claude.

**An analogy:** an agent is calling a colleague in. A skill is opening the manual and following it yourself.

### How to create a skill

The file `.claude/skills/skill-name/SKILL.md`:

```markdown
---
name: deploy
description: The production deployment procedure
---

# Deploy Procedure

## Before the deployment
1. All tests green (`php artisan test`)
2. Code review passed
3. Database backup on production

## The deployment
1. `git push origin main`
2. SSH to the server: `ssh user@host`
3. `cd /path/to/project && git pull`
4. `php artisan migrate --force`
5. `php artisan config:cache`
6. `php artisan route:cache`
7. `php artisan queue:restart`

## After the deployment
1. Check the home page
2. Check the API endpoints
3. Watch the errors for 15 minutes

## Rollback
1. `git revert HEAD`
2. `php artisan migrate:rollback`
3. Redo the caching
```

### The directory structure

```
.claude/
└── skills/
    └── skill-name/
        ├── SKILL.md          # The main file (mandatory)
        └── references/       # Extra material (optional)
            ├── checklist.md
            └── examples.md
```

### How to call a skill

```
> /deploy
```

Claude loads the contents of `SKILL.md` and follows the instructions.

### When to use a skill rather than an agent

| Situation | What to use |
|-----------|-------------|
| Writing code | **Agent** (backend-expert) |
| A deployment procedure | **Skill** (a step-by-step instruction) |
| Code review | **Agent** (code-critic, isolation is needed) |
| Generating a changelog | **Skill** (a template + the current context) |
| Parallel work | **Agents** (each in its own process) |
| A pre-release checklist | **Skill** (sequential steps) |
| Analysing the codebase | **Agent** (a separate context, it does not clutter the main one) |

### Examples of useful skills

**Deploy** — the deployment procedure (steps, checks, rollback)

**Hotfix** — an emergency fix (the minimal process, a fast deployment)

**New-feature** — a checklist for a new feature (from planning to review)

**Onboarding** — instructions for a new developer (the stack, the architecture, how to run it)

**Incident** — the incident procedure (diagnosis, fix, postmortem)

---

## Commands vs Skills

Claude Code has two similar mechanisms:

### Commands (`.claude/commands/`)

```markdown
# .claude/commands/develop.md
Launch the backend-expert agent for this task.
Use the Controller → FormRequest → DTO → Service → Repository → Model pattern.
Afterwards — /review, without exception.
```

**Call:** `/develop`
**The essence:** a short instruction that usually launches an agent or sets a working mode.

### Skills (`.claude/skills/name/SKILL.md`)

A more complex structure with frontmatter, references, and detailed instructions.

**Call:** `/skill-name`
**The essence:** a full procedure with context and steps.

### Which to choose

- **A single line, "launch such-and-such agent"** → Command
- **A procedure of 10+ steps with context** → Skill
- **Not sure** → start with a Command; if it gets complicated, turn it into a Skill

---

## In practice: building the system from scratch

### The minimal configuration (1 day)

```
.claude/
├── settings.local.json      # Permissions
├── hooks/
│   └── on-every-message.sh  # A reminder about the review
└── commands/
    ├── develop.md            # "Write code following the pattern"
    └── review.md             # "Check the code"
```

### The medium configuration (1 week)

```
.claude/
├── settings.local.json
├── settings.md               # Behaviour rules
├── hooks/
│   ├── on-every-message.sh
│   └── check-critic.sh
├── agents/
│   ├── 01-backend-expert.md
│   ├── 06-architecture-validator.md
│   └── 07-code-critic.md
└── commands/
    ├── develop.md
    ├── review.md
    └── validate.md
```

### The full configuration (the starter pack)

```
.claude/
├── settings.local.json
├── settings.md
├── hooks/
│   ├── on-every-message.sh
│   ├── check-critic.sh
│   ├── bash-output-guard.sh
│   ├── context-budget-guard.sh
│   └── generate-wiki.sh
├── agents/
│   ├── 00-coordinator.md
│   ├── 01-backend-expert.md
│   ├── 02-frontend-expert.md
│   ├── 03-db-expert.md
│   ├── 04-devops-expert.md
│   ├── 05-test-expert.md
│   ├── 06-architecture-validator.md
│   ├── 07-code-critic.md
│   ├── 08-api-architect.md
│   ├── 09-integrations-expert.md
│   ├── 10-kafka-expert.md
│   ├── 11-s3-expert.md
│   ├── TEMPLATE-domain-expert.md
│   └── README.md
├── commands/
│   ├── orchestrate.md
│   ├── develop.md
│   ├── frontend.md
│   ├── api-design.md
│   ├── integrate.md
│   ├── kafka.md
│   ├── storage.md
│   ├── review.md
│   ├── test.md
│   └── validate.md
└── skills/
    └── deploy/
        └── SKILL.md
```

---

## FAQ

### "Do agents burn more tokens?"

Yes. Every agent is a separate context, separate API requests. But the time and quality saved outweigh the cost. One piece of correctly written code is cheaper than three rewrites.

### "Can I manage without agents?"

You can. CLAUDE.md + hooks + commands already give you 80% of the benefit. Agents are for scale: when the tasks are complex and specialisation is needed.

### "Can an agent launch another agent?"

Technically yes, if it has the `Agent` tool — but in this pack it must not. The depth is exactly one level: human → coordinator → agent → report. An agent that needs another one writes so as a line in its report and stops; a human makes the decision. The measurement behind this is in `PITFALLS.md` §10.

### "Can a skill launch an agent?"

Not directly. A skill is an instruction for the current Claude. But the instruction can say "launch the backend-expert agent" and Claude will do it.

### "How do I debug an agent?"

1. Run it by hand: tell Claude "launch the backend-expert agent with task X"
2. Watch what it does — Claude will show the result
3. If it does the wrong thing — correct the instructions in the agent's file
4. Iterate: edit → run → look at the result

### "How many agents do I need?"

For a small project: 2-3 (backend-expert, code-critic, maybe db-expert).
For a medium one: 5-6 (+ coordinator, frontend-expert, test-expert).
For a large one: all 12 + domain-expert (including api-architect, integrations, kafka, s3).

Do not create agents "just in case". Add one when a real need appears.
