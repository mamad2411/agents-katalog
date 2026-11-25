---
name: mig-plan
description: Creates comprehensive migration plans for application modernization projects. Use this skill whenever the user mentions migrating, modernizing, or upgrading an application from one platform/framework/language to another (e.g., Java EE to Spring Boot, monolith to microservices, on-prem to cloud). Also trigger when users ask for migration roadmaps, migration strategies, or how to plan a migration. This skill orchestrates the full planning workflow including specification, design, task breakdown, and user story generation.
---

# Migration Planning Skill

This skill creates comprehensive, actionable migration plans for application modernization projects. It produces structured documentation that guides teams through complex migrations.

## What This Skill Does

When invoked, this skill:

1. **Analyzes the codebase** using rgctl to build a knowledge graph
2. **Uses migration prompt** from mig-prompt-builder as the planning foundation (contains specification and design)
3. **Produces tasks.md** - granular task breakdown with subtasks
4. **Generates UserStory.md** - user stories linking tasks to business value

All outputs are saved to `mig-plan-workspace/`.

**Note**: This skill leverages the comprehensive migration prompt from mig-prompt-builder which already contains specification and design details, eliminating the need for separate spec.md and design.md files. This optimizes token usage while maintaining planning quality.

## When to Use This Skill

Use this skill when the user:
- Wants to migrate from technology A to technology B
- Asks "how do I plan this migration?"
- Needs a migration roadmap or strategy
- Mentions modernization, platform upgrade, or technology transition
- Has a complex migration ahead and needs structure

## Workflow

### Phase 1: Knowledge Gathering

First, ensure you have the knowledge graph:

1. Ensure the codebase is indexed with rgctl (invoke **mig-rgctl** if needed — see [workflow](../mig-rgctl/references/workflow.md))
2. Query the knowledge graph to understand:
   - Code structure and dependencies
   - Architectural patterns
   - Technology stack
   - Integration points

### Phase 2: Use Migration Prompt as Foundation

The migration prompt from mig-prompt-builder already contains:
- Current application summary (from rgctl analysis)
- Target platform and technologies
- Migration approach and strategy
- Required deliverables (containerization, OpenShift, test coverage)
- Success criteria and constraints

Use this as the foundation for task and story generation instead of creating separate spec.md and design.md files.

### Phase 3: Generate Tasks (tasks.md)

Create `mig-plan-workspace/tasks.md` with detailed task breakdown.

**Task Structure**: Group related work into numbered task groups. Each task has subtasks with checkboxes.

**Critical Integration Points**: Every task group MUST include these subtasks:

A. **Test Generation**: Hook into mig-test-gen
B. **Containerization & Deployment**: Hook into mig-containerization and mig-deploy  
C. **Documentation**: Document the changes

```markdown
# Migration Tasks

## Task Group 1: [Task Group Name]

- [ ] 1.1 [Subtask description]
- [ ] 1.2 [Subtask description]
- [ ] 1.3 [Subtask description]
- [ ] 1.4 **Test Generation**: Use mig-test-gen to create test cases for [specific aspect]
  - Command: `/skill mig-test-gen` for [component/feature]
  - Expected: Unit tests for [X], integration tests for [Y]
- [ ] 1.5 **Containerization**: Use mig-containerization to containerize [component]
  - Command: `/skill mig-containerize` for [component]
  - Config needs: Environment variables for [X], secrets for [Y], ConfigMaps for [Z]
- [ ] 1.6 **Deployment**: Use mig-deploy to create deployment manifests
  - Command: `/skill mig-deploy` for [component]
  - Dependencies: [service A], [database B]
  - Network: Expose port [X], connect to [Y]
- [ ] 1.7 **Documentation**: Document [aspect]
  - Update README with [migration notes]
  - Add runbook for [operations]

## Task Group 2: [Next Task Group]
...
```

**How to create tasks**: 

1. Break the migration into logical phases based on the design
2. Each phase becomes a task group
3. Within each group, create subtasks that are:
   - **Actionable**: Clear what needs to be done
   - **Testable**: Can verify completion
   - **Sized appropriately**: 2-8 hours of work each
4. Always include the integration subtasks (test gen, containerization, deploy, docs)

**Example task breakdown for "Migrate Authentication Service"**:

```markdown
## 1. Migrate Authentication Service

- [ ] 1.1 Create new Spring Security configuration class
- [ ] 1.2 Migrate JWT token generation logic
- [ ] 1.3 Implement OAuth2 integration
- [ ] 1.4 Migrate user credential storage to target database
- [ ] 1.5 **Test Generation**: Use mig-test-gen for auth service
  - Command: `/skill mig-test-gen` targeting authentication module
  - Expected: Security tests, token validation tests, OAuth flow tests
- [ ] 1.6 **Containerization**: Use mig-containerization for auth service
  - Command: `/skill mig-containerize` for auth-service
  - Config needs: JWT_SECRET (secret), OAUTH_CLIENT_ID (secret), DB_CONNECTION (ConfigMap)
- [ ] 1.7 **Deployment**: Use mig-deploy for auth service
  - Command: `/skill mig-deploy` for auth-service
  - Dependencies: PostgreSQL database, Redis session store
  - Network: Expose 8080, connect to postgres:5432 and redis:6379
- [ ] 1.8 **Documentation**: Document authentication changes
  - Update API docs with new auth endpoints
  - Create migration guide for user credentials
  - Add troubleshooting guide for common auth issues
```

### Phase 4: Generate User Stories (UserStory.md)

Create `mig-plan-workspace/UserStory.md` that groups tasks into user stories.

**User Story Principles**:
- **Simple**: 1-2 sentences
- **User-focused**: Role + action + benefit
- **Clear language**: No jargon

```markdown
# User Stories

## User Story 1: [Title]

**As a:** [role/persona]  
**I want:** [action]  
**So that:** [benefit/outcome]

---

### Tasks
- [Link to task group: ## 1. Task Group Name from tasks.md]
- [Link to task group: ## 2. Another Task Group]

### Acceptance Criteria
- [ ] [Specific, testable criterion with expected result]
- [ ] [Another criterion]
- [ ] [Another criterion]

---

### Details
- **Priority:** [High / Medium / Low - based on migration dependencies]
- **Estimate:** [Story points or t-shirt size based on task complexity]

---

### Preconditions
- [What must be true before starting this story]
- [Dependencies from design.md]

---

### Steps to Reproduce / Implementation Notes
1. [High-level step referencing task groups]
2. [Another step]
3. [Validation step]

---

### Dependencies
- [Other user stories that must complete first]
- [External dependencies]

---

### Test Cases
- Test 1: [scenario] - expected result [reference to mig-test-gen output]
- Test 2: [scenario] - expected result

---

### Notes / Comments
- [Migration-specific context]
- [Risk mitigation notes]

---

[Repeat for each user story]
```

**Creating User Stories**: 

1. Group related task groups into stories
2. Each story should be completable in 1-2 sprints
3. Order stories by dependency (what must happen first)
4. Link back to specific task groups in tasks.md

**Example User Story**:

```markdown
## User Story 1: Secure Authentication Migration

**As a:** Platform Engineer  
**I want:** To migrate the authentication service from Java EE to Spring Security with OAuth2  
**So that:** Users can securely authenticate using modern OAuth2 standards and we can deprecate the legacy auth system

---

### Tasks
- ## 1. Migrate Authentication Service (from tasks.md)
- ## 2. Migrate User Database Schema (from tasks.md)

### Acceptance Criteria
- [ ] Users can authenticate using OAuth2 flow with no downtime
- [ ] All existing user credentials are successfully migrated with password hashes intact
- [ ] Legacy authentication endpoints return 410 Gone with migration instructions
- [ ] Security tests pass with 100% coverage on auth flows

---

### Details
- **Priority:** High
- **Estimate:** 8 story points

---

### Preconditions
- PostgreSQL database is deployed and accessible
- OAuth2 provider is configured
- SSL certificates are in place

---

### Steps to Reproduce / Implementation Notes
1. Deploy new Spring Security auth service alongside legacy system
2. Migrate user credentials using batch script with validation
3. Enable OAuth2 endpoints and validate token flow
4. Switch traffic to new service with canary deployment
5. Monitor for 48 hours before deprecating legacy endpoints

---

### Dependencies
- Database migration user story must complete first
- Certificate management user story

---

### Test Cases
- Test 1: OAuth2 login flow - user redirected to provider, receives valid JWT token
- Test 2: Migrated credentials - existing user can login with same password
- Test 3: Token validation - API endpoints accept new JWT format
- Test 4: Load test - auth service handles 1000 req/sec

---

### Notes / Comments
- Plan for 48-hour parallel run before cutting over
- Keep legacy auth service running for 30 days post-migration for rollback
- Monitor failed login attempts for credential migration issues
```

## Executing the Workflow

When this skill runs, follow these steps in order:

1. **Invoke mig-rgctl** if the repo is not indexed yet ([workflow](../mig-rgctl/references/workflow.md))
2. **Query knowledge graph** via mig-rgctl recipes; map task groups from `.rgctl/migration_plan.json` v2 `.steps[]` (exclude `"root"`; bound with `jq`)
3. **Read migration prompt** from mig-prompt-workspace/migration-prompt.md (should already exist from mig-prompt-builder)
   - If migration prompt doesn't exist, prompt the user to run mig-prompt-builder first or provide migration context
4. **Generate tasks.md** breaking down the migration prompt into actionable work, using knowledge graph for specifics
5. **For each task with integration hooks**, actually invoke the relevant skill:
   - Call `/skill mig-test-gen` with context from the task
   - Call `/skill mig-containerize` with component details
   - Call `/skill mig-deploy` with deployment requirements
   - Capture outputs and embed references in the task
6. **Generate UserStory.md** grouping tasks into stories
7. **Present summary** to user with links to all documents

## Output Structure

```
mig-plan-workspace/
├── tasks.md          # Task breakdown with subtasks
└── UserStory.md      # User stories linking tasks
```

**Note**: Specification and design details are in `mig-prompt-workspace/migration-prompt.md` (created by mig-prompt-builder).

## Important Notes

**Uses mig-prompt-builder output**: This skill expects a migration prompt from mig-prompt-builder. If the prompt doesn't exist, guide the user to run mig-prompt-builder first.

**Auto-execution of integration skills**: Unlike traditional planning tools, this skill actively invokes mig-test-gen, mig-containerize, and mig-deploy during plan generation. This produces concrete, actionable outputs rather than placeholders.

**Incremental refinement**: After generating the initial plan, offer to refine specific sections based on user feedback. The plan is a living document.

**Realistic estimates**: When creating tasks and user stories, base estimates on actual code complexity from the knowledge graph, not generic assumptions.

**Link everything**: Maintain traceability from user stories → tasks → migration prompt → knowledge graph. Each decision should trace back to code reality.

**Token optimization**: By using the migration prompt instead of generating separate spec.md and design.md files, we significantly reduce token usage while maintaining comprehensive planning.

## Example Invocation

User: "I need to create a migration plan" (after running mig-prompt-builder)

Skill flow:
1. Ensure rgctl index exists (invoke rgctl if needed)
2. Read migration prompt from mig-prompt-workspace/migration-prompt.md
3. Generate tasks.md with detailed migration tasks based on the prompt and knowledge graph
4. For each task, invoke integration skills to generate tests, containers, and deployment configs
5. Generate UserStory.md grouping work into deliverable stories
6. Present complete plan to user

**Typical workflow**:
1. User runs `/skill mig-prompt-builder` (creates migration-prompt.md)
2. User runs `/skill mig-plan` (creates tasks.md and UserStory.md)
3. User executes tasks using the generated plan

## Tips for Success

- **Start with mig-prompt-builder**: Ensure a comprehensive migration prompt exists before planning
- **Use the knowledge graph**: Don't guess about code structure, query it via rgctl
- **Reference the migration prompt**: All task details should align with the approach defined in the migration prompt
- **Be specific**: Include actual class names, file paths, and code patterns from the codebase
- **Consider dependencies**: Order tasks and stories based on technical dependencies
- **Plan for testing**: Every migration task needs corresponding tests
- **Plan for deployment**: Every component needs containerization and deployment configuration
- **Document everything**: Migration knowledge is valuable for future maintenance
