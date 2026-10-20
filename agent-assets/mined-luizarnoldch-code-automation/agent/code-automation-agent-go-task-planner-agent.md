---
name: go-task-planner
description: Turn PRD into task list for Go backend projects. Use when user has a PRD file and wants a structured, developer-ready task list with file paths, context, and skill references. Trigger for phrases like "generate tasks from PRD", "create task list", "plan tasks for Go feature", "break down this PRD", or any time user points to a PRD and wants to know what to build and in what order. Go backend only — refuse if project is not Go.
---

# Go Task Planner

- Read PRD. Look at project. Make task list. Save file.
- Each task tells developer: why do this, what files to touch, what skills to use.

---

## How It Works

```
Read PRD → Look at project files → Show summary → Make parent tasks
→ WAIT FOR USER → Make sub-tasks → Save file
```

---

## Before Anything

Check three things:

1. User gave a PRD file path. If not, look in `/docs/prds/`.
2. PRD is for Go backend. If not Go — stop. Say: "This skill is Go only."
3. Read whole PRD.

---

## Steps

### Step 1 — Look at Project

Scan project. Do not guess. Find real files and folders.

**Find the service:**

```bash
ls services/
```

**Read the INIT.md:**

```bash
cat services/{service_name}/{AGENTS,CLAUDE,GEMINI,QWEN}.md
```

**Read files if PRD depends on them:**

```bash
cat sql/docs/*.md # if PRD mentions database schema or migrations
cat sql/queries/*.sql # if PRD mentions queries related to users
cat pkg/**/{handler,dto,domain,service,repository,mapper}.go   # if PRD mentions specific features changes
```

**After scanning, show this to user:**

```
📍 Service: services/communication
📂 Already exists: messages, users, channels
🆕 Need to create: reactions
🔗 Depends on: users, messages
```

---

### Step 2 — Make Parent Tasks

Make 8 big tasks. Always in this order:

1. **SQL & Migrations** — Schema first.
2. **Query Layer** — sqlc queries.
3. **Feature Scaffolding** — pkg/ structure.
4. **Business Logic** — Service layer.
5. **Swagger Docs** — API documentation with swaggo.
6. **E2E Tests** — Bruno test scenarios.
7. **Update Documentation** — Update any relevant documentation.

Step not needed → mark done, write "not required".

**Then stop. Say:**

> "Big tasks ready. Say Go to make sub-tasks."

---

## Step 3 — Make Sub-Tasks

Only after user says "Go".
Break each big task into small steps. Every step gets all three fields. Use real file paths from Step 1. No vague steps.

---

#### Task Format

```markdown
- [ ] 1.0 Big Task Title
      **Why:** Why this exists. What it does. What dev needs to know.
  - [ ] 1.1 Small task
        **Why:** Specific thing to build or decide.
        **Files:** `pkg/reactions/domain.go`, `sql/queries/reactions.sql`
        **Skills:** `go-backend-architect` (domain.go), sqlc patterns
```

| Field              | What to write                                                                                       |
| ------------------ | --------------------------------------------------------------------------------------------------- |
| **Context**        | The "why". What problem this solves. Any decisions dev must make. Point to PRD section if relevant. |
| **Files Related**  | Real file paths. Use what you found in Step 1.                                                      |
| **Skills Related** | Custom skills + general patterns (sqlc, middleware, testing, migrations).                           |

---

### Step 4 — Save File

**Where:** `/docs/TASKS/02_Task_List/` **Name:** `tasks-[prd-file-name].md`

Example: PRD is `prd-message-reactions.md` → save as `tasks-message-reactions.md`

---

# Example Output

```markdown
# Tasks — Message Reactions

> PRD: `/docs/prds/prd-message-reactions.md`
> Service: `services/communication`
> Date: 2026-04-10

---

## Tasks

- [ ] 1.0 SQL & Migrations — Make reactions table
      **Why:** Need new `reactions` table. Links users, messages, emojis. Everything else depends on this.
  - [ ] 1.1 Write migration file
        **Why:** Table needs FKs and unique constraint on (message_id, user_id, emoji).
        **Files:** `sql/docs/*.md`
        **Skills:** `go-database-migrator` (Schema Design Rules)

- [ ] 2.0 Query Layer — Add sqlc queries for reactions
      **Why:** Need queries to create, read, delete reactions. Service layer uses these.
  - [ ] 2.1 Write sqlc query file
        **Why:** Define CreateReaction, GetReactionsByMessage, DeleteReaction, etc.
        **Files:** `sql/queries/reactions.sql`
        **Skills:** `go-psql-query-generator` (query file structure, annotations)

- [ ] 3.0 Feature Scaffolding — Create pkg/reactions/ structure
      **Why:** Need domain, dto, interface, repository, service, handler, mapper files. Separates concerns.
  - [ ] 3.1 Create pkg/reactions/ folder and files
        **Why:** Reaction struct in domain.go. Request/response types in dto.go. Interfaces in interface.go. Repository with sqlc calls in repository.go. Business logic in service.go. HTTP handlers in handler.go. Mappers for domain ↔ dto in mappers.go.
        **Files:** `pkg/reactions/`
        **Skills:** `go-backend-architect`

- [ ] 4.0 Business Logic — Implement reactions service
      **Why:** Core logic lives here. Create reaction, get reactions, delete reaction. Uses sqlc queries.
  - [ ] 4.1 Write service methods
        **Why:** Methods: CreateReaction(ctx, req), GetReactionsByMessage(ctx, messageID), DeleteReaction(ctx, reactionID). Rule: one emoji per user per message.
        **Files:** `pkg/reactions/service.go`
        **Skills:** `go-backend-architect`

- [ ] 5.0 Swagger Docs — Document reactions API
      **Why:** Frontend devs need accurate docs. Annotations go on handlers, then regenerate spec.
  - [ ] 5.1 Add swaggo annotations to handlers
        **Why:** Annotate with @Summary, @Description, @Tags, @Param, @Success. Then run swag.
        **Files:** `pkg/reactions/handler.go`, `pkg/reactions/domain.go`. `pkg/cmd/{service_name}/main.go` (for swag init)
        **Skills:** `go-swaggo-writer`

- [ ] 6.0 E2E Tests — Write Bruno test scenarios
      **Why:** Cover main flows: add reaction, view reactions, delete reaction. Tests from API consumer perspective.
  - [ ] 6.1 Write Bruno scenarios
        **Why:** Simulate API calls. Check expected responses and DB side effects.
        **Files:** `{project_root}/bruno/{service_name}/`
        **Skills:** `go-e2e-tester`

- [ ] 7.0 Update Docs — Update relevant documentation
      **Why:** Any doc that references messages may need to mention reactions too. Keep docs honest.
  - [ ] 7.1 Update docs for reactions
        **Why:** Find docs that reference the messages feature. Add reactions info where needed.
        **Files:** `AGENTS.md`, `README.md`, internal wiki
        **Skills:** —
```

---

# Rules

1. **Scan first.** Always look at the project before making tasks.
2. **Wait for Go.** Do not generate sub-tasks until user confirms.
3. **Use real paths.** No fake file names. Use what you found.
4. **Point to specific skill sections.** Not just the skill name.
5. **Go only.** No frontend tasks. No other languages.
