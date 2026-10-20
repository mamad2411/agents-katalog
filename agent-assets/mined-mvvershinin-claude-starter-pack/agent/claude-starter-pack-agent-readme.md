# Claude Code Agents System

A multi-agent system for Laravel projects with a mandatory Actor-Critic loop.

---

## CRITICAL RULES

### 1. EVERY COMPLEX TASK GOES THROUGH THE COORDINATOR

For tasks touching > 3 files, new features, refactoring:
```bash
/orchestrate
```

### 2. CRITIC AFTER EVERY TASK — NO EXCEPTIONS

After code is written or changed, the following runs **ALWAYS**, automatically:
```bash
/validate   # architecture check
/review     # code review, bugs, security
```

**If the critic found problems — the agent MUST fix them and run the check again.**
**The loop repeats until APPROVE. The user only ever receives reviewed code.**

### 3. DOMAIN EXPERT

If the project has a domain-expert — consult it whenever you touch business logic. Do not make business-rule decisions on your own.

---

## Slash commands

| Command | Agent | When to use it |
|---------|-------|----------------|
| `/orchestrate` | coordinator | Complex tasks, planning |
| `/develop` | backend-expert | Backend code (Laravel) |
| `/frontend` | frontend-expert | Vue.js/React components |
| `/api-design` | api-architect | REST API design |
| `/integrate` | integrations-expert | External services, APIs, webhooks |
| `/kafka` | kafka-expert | Kafka producers/consumers |
| `/storage` | s3-expert | Files, S3, upload/download |
| `/validate` | architecture-validator | Pattern compliance check |
| `/review` | code-critic | Code review, bugs |
| `/test` | test-expert | Writing tests |

---

## Quick start

### New feature (complex)
```bash
/orchestrate
# → the coordinator plans → launches agents → validate → review → APPROVE
```

### Simple bug (1-2 files)
```bash
/develop
# → fix → review automatically → if problems → fix → review → APPROVE
```

### Quality check
```bash
/validate
/review
```

---

## Available agents

| # | Name | Model | Role | When to use it |
|---|------|-------|------|----------------|
| 0 | **coordinator** | **Opus** | Planner | Complex tasks, decomposition |
| 1 | **backend-expert** | **Opus** | Backend | Laravel: Services, Repositories, Controllers |
| 2 | **frontend-expert** | **Opus** | Frontend | Vue.js/React, Tailwind CSS, Pinia |
| 3 | **db-expert** | Sonnet | Database | MySQL/PostgreSQL, migrations, optimization |
| 4 | **devops-expert** | Sonnet | DevOps | Docker, deployment, CI/CD, servers |
| 5 | **test-expert** | Sonnet | Tests | PHPUnit, Jest, coverage |
| 6 | **architecture-validator** | Sonnet | Validation | Checking that patterns are followed |
| 7 | **code-critic** | Sonnet | Code review | Adversarial review, bugs, security |
| 8 | **api-architect** | **Opus** | API design | REST API endpoints, contracts |
| 9 | **integrations-expert** | **Opus** | Integrations | External services, APIs, webhooks |
| 10 | **kafka-expert** | **Opus** | Kafka | Producers, consumers, schema registry |
| 11 | **s3-expert** | **Opus** | Files | S3, signed URLs, upload/download |
| — | **domain-expert** | Task-dependent | Problem domain | The project's business logic (created from the template) |

### Choosing the model
- **Opus** — code generation, coordination, hard decisions (more expensive, more accurate)
- **Sonnet** — analysis, validation, tests (cheaper, faster)

---

## Actor-Critic Pattern

**MANDATORY after EVERY task. Automatically.**

```
Actor (backend-expert / frontend-expert) produces code
    ↓
Critic (code-critic) reviews it (score 0-100)
    ↓
< 70 (BLOCK / REQUEST_CHANGES)
    → the Actor MUST fix it
    → hands it back to the critic
    → repeat until APPROVE
    ↓
≥ 70 (APPROVE)
    → the code is ready to commit
    → show it to the user
```

**Never:**
- Never show code to the user without it passing the critic
- Never ask "shall I fix it?" — fix it yourself
- Never skip the loop for "small" tasks (there are no small ones)

---

## Domain Expert

### Why
Claude knows code, but it does not know your business. The domain expert:
- Knows the entities and how they relate
- Knows the business rules and constraints
- Knows the critical flows and the race conditions
- Speaks the language of the domain

### How to create one
1. Copy `TEMPLATE-domain-expert.md`
2. Rename it: `02-[domain]-expert.md`
3. Fill in the sections: entities, rules, flows
4. The coordinator and the other agents will consult it automatically

### Examples
- `02-booking-expert.md` — a booking system
- `02-ecommerce-expert.md` — an online shop
- `02-medical-expert.md` — a medical system

---

## Laravel architecture (MANDATORY pattern)

```
HTTP Request → Controller → FormRequest → DTO → Service → Repository → Model → DB
```

### FORBIDDEN
- ❌ Business logic in Controllers
- ❌ DB queries in Services (Repository only)
- ❌ Mass assignment ($fillable/$guarded)
- ❌ try-catch in Controllers
- ❌ Facades in Services/Repositories
- ❌ Business logic in Jobs
- ❌ Hardcoded enum values
- ❌ Inline class paths (`new \App\...`)
- ❌ Generic exceptions

### MANDATORY
- ✅ DTO built in FormRequest->toDTO()
- ✅ Repository for DB access
- ✅ Service for business logic
- ✅ Interface for every Service/Repository
- ✅ DI through the constructor
- ✅ Eager loading (N+1 prevention)
- ✅ Nested Resources
- ✅ Custom exceptions

---

## Workflow patterns

### New feature (Full Stack)
```
Phase 1 (parallel): db-expert (schema) + coordinator (plan)
Phase 2: backend-expert (API + services)
Phase 3: frontend-expert (UI)
Phase 4: test-expert (tests)
Phase 5 (parallel): architecture-validator + code-critic
Phase 6: fixes from the critic's findings → re-check → APPROVE
```

### Bug fix
```
Phase 1: backend-expert / frontend-expert (investigate + fix)
Phase 2: test-expert (regression test)
Phase 3: code-critic (review) → fix if needed → re-review → APPROVE
```

### Refactoring
```
Phase 1: architecture-validator (current state)
Phase 2: backend-expert (refactoring)
Phase 3: test-expert (update the tests)
Phase 4: code-critic (review) → fix → re-review → APPROVE
```

---

## Quality Gates

1. **After implementation** → `architecture-validator` (score ≥ 70)
2. **Before commit** → `code-critic` (score ≥ 70)
3. **If score < 70** → fix → run the check again
4. **Before deployment** → `test-expert` (coverage check)

---

## File layout

```
.claude/
├── settings.local.json             # Permissions, hooks
├── settings.md                     # Behaviour rules
├── agents/
│   ├── README.md                   # This file
│   ├── 00-coordinator.md           # Coordinator
│   ├── 01-backend-expert.md        # Laravel backend
│   ├── 02-frontend-expert.md       # Vue.js/React frontend
│   ├── 03-db-expert.md             # MySQL/PostgreSQL
│   ├── 04-devops-expert.md         # Docker, deployment
│   ├── 05-test-expert.md           # PHPUnit, Jest
│   ├── 06-architecture-validator.md # Pattern compliance
│   ├── 07-code-critic.md           # Code review
│   ├── 08-api-architect.md         # REST API design
│   ├── 09-integrations-expert.md   # External services
│   ├── 10-kafka-expert.md          # Apache Kafka
│   ├── 11-s3-expert.md             # S3/Object Storage
│   └── TEMPLATE-domain-expert.md   # Domain expert template
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
└── hooks/
    ├── on-every-message.sh         # Injects the rules into every message
    ├── check-critic.sh             # Blocks git commit when the review is missing
    ├── bash-output-guard.sh        # Caps the size of Bash output
    ├── context-budget-guard.sh     # Warns when the session context grows
    └── generate-wiki.sh            # Reminder to update the documentation
```
