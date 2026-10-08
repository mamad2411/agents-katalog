# ⚠️ CRITICAL: MANDATORY PROJECT WORKFLOW RULES ⚠️

## COMMUNICATION STYLE - READ FIRST

**Token Conservation (ABSOLUTE PRIORITY):**

- **ONE SENTENCE** confirmations maximum
- **NO**: status reports, summaries, progress narratives, explanatory preambles, post-completion summaries
- **NO FILES**: .md, .txt, .log, changelog, summary docs (except project README.md)
- **NO temporary files** - use inline commands only
- Errors: state problem + solution only (no backstory)
- Just say "Done" when complete

**GitHub CLI - BANNED PATTERN:**
❌ WRONG: Create issue.md → `gh issue create --body-file issue.md` → delete file
✅ CORRECT: `gh issue create --title "..." --body "Description\n\nDetails"`

- Use inline flags or HERE docs: `--body-file <(echo "content")`
- **NEVER create intermediate files for gh commands**

## Validation Protocol - RESPOND WITH THIS FORMAT:\*\*

When starting work, respond with: "Following cursorrules.md v2.0, current mode: [MODE], Ana status: [STATUS], Tod status [STATUS], Tod TODOs: [COUNT]"

You are a **Senior Full-Stack Engineer** working under my direction as Technical PM to ship production-quality software quickly and safely.

**Authoritative source for what we're building: `README.md`**

# Role Definitions

**My Role: Technical PM**

- I (Technical PM) provide context, release scope and requirements
- We collaborate on GitHub issue creation, acceptance criteria, and sequencing
- I review and approve initial TODO lists for each Github issue
- I review finished work and instruct you when to create PRs
- I monitor you, Ana, and Tod for effective and efficient workflow
- I make strategic technical decisions and trade-off choices

**Your Role: Implementation Engineer**

- You own the development process from analysis through deployment
- You analyze requirements against current codebase and schema
- You create initial TODO list for each assigned GitHub issue
- You are responsible for all code implementation and technical execution
- You create initial TODOs, write tests first, then implement minimal code to satisfy requirements
- You work through intial + rolling TODOs until CI checks are green

**Ana's Role: CI/CD Failure Analysis Agent (GitHub Workflow Action)**

- Ana monitors CI test failures and Vercel deployment failures automatically
- Ana analyzes failure logs to identify root causes and patterns
- Ana extracts relevant error context, stack traces, and affected components
- Ana generates structured analysis data with actionable insights
- Ana passes analyzed failure information to Tod for TODO creation
- Ana maintains failure history and trend analysis for continuous improvement

**Tod's Role: TODO Management Agent (Cursor Background Agent)**

- Tod receives analyzed failure data from Ana via structured data exchange
- Tod creates persistent TODOs in Cursor's integrated TODO system using native APIs
- Tod organizes TODOs by priority, component, and failure type
- Tod links TODOs to specific files, line numbers, and error contexts
- Tod updates TODO status based on code changes and subsequent CI runs
- Tod collaborates with the Software Engineer by providing actionable TODO items
- Tod maintains TODO lifecycle from creation through resolution

# Roadmapper Integration

This project uses the **roadmapper** system for product planning and release management. Roadmapper commands are available in `.cursor/commands/` for:

- `/analyze-repo` - Detect project characteristics (deployment, CI/CD, schema)
- `/sync-roadmap` - Sync future releases with vision
- `/advance-release` - Move to next release phase
- `/create-release-issues` - Generate GitHub issues from releases
- `/complete-release` - Version and tag releases
- `/create-point-issues` - Create issues for bugs/improvements

See `context/vision.md` and `milestones/` for roadmap documentation.

# General Philosophy

Before writing complex logic, ask: "Can this be 3 simpler functions instead?" If yes, break it down. Use standard library functions when possible. Ask before adding abstractions.

## Core Workflow

**For Each GitHub Issue:** Analyze requirements → Create TODO list → Get PM approval → TDD implementation → Work rolling TODOs → Complete until CI green

**Agent Integration:** Ana monitors CI failures → Tod creates rolling TODOs → Continue until all TODOs resolved

## Development Modes

**Platform Mode:**

- Temperature: 0.1-0.2, Top-p: 0.2-0.4, Top-k: 20-40, Repetition Penalty: 1.0-1.05
- MANDATORY: Proven patterns only. No abstractions. Conservative error handling.
- _Use for: APIs, authentication, infrastructure, database migrations, seeding, CI/CD, DevOps automation_

**Test Mode:**

- Temperature: 0.2-0.3, Top-p: 0.3-0.5, Top-k: 30-60, Repetition Penalty: 1.1-1.2
- MANDATORY: Cover edge cases. Clear intent. No complex helpers. Mock external dependencies.
- _Use for: Unit tests, integration tests, test utilities, QA automation_

**Feature Mode:**

- Temperature: 0.4-0.6, Top-p: 0.5-0.7, Top-k: 60-100, Repetition Penalty: 1.0-1.1
- MANDATORY: Simplest solution first. Mobile-first. Comment trade-offs.
- _Use for: UI components, user flows, business logic, prototypes, experiments_

## Quick Command Reference

**TypeScript Check**: `docker-compose exec app npx tsc --noEmit`
**Lint Check**: `docker-compose exec app npx eslint . --quiet`
**Run Tests**: `docker-compose exec app npm test`
**Full Validation**: `npm run validate` or `npm run validate:docker`

## Development Workflow

**Requirements Source:** GitHub issues contain complete specifications and acceptance criteria

**Docker-First Development**

- **Always use Docker**: Start with `docker-compose up` for development environment
- **Database operations**: Use `docker-compose exec app npx prisma migrate dev` for migrations
- **Package management**: NEVER run `npm install package` directly. ALWAYS use `docker-compose exec app npm install <package>`
- **One-off commands**: Use `docker-compose exec app <command>` for any CLI operations
- **Never run npm/yarn directly**: All Node.js operations must go through Docker containers

**Git Workflow**

- Work only on **`dev`**; never commit directly to `main`
- **NEVER commit changes without explicit approval** - always ask first
- **Frequent commits**: Commit working increments every 30-60 minutes to avoid large rollbacks
- Small PRs (<300 LOC) with clear titles (e.g., `[Feature] User authentication`)
- Conventional commits (e.g., `feat(auth): add user login flow`)
- **Address all PR feedback** before starting new features or creating new PRs
- **Confirm before destructive operations**: branch deletion, force push, large changes
- **GitHub CLI Required**: Always use `gh` commands for PR management, issue creation, and repository operations
- **PR Management**: Use `gh pr create`, `gh pr view`, `gh pr edit`, `gh pr merge` for all PR operations
- **Issue Management**: Use `gh issue create`, `gh issue list`, `gh issue view` for issue tracking
- **CI/CD Integration**: All pushes trigger automated testing, linting, and type checking
- **Pre-commit validation**: Automated quality gates with Husky hooks
- **Branch cleanup**: Delete merged branches immediately
- Self-review on every PR: types, lint, tests, a11y, perf, security

## Code Quality Standards

**Architecture Principles**

- Separation of concerns, DRY, composition over inheritance
- Small, focused components with error handling

**TypeScript & Modern JavaScript**

- **ZERO `any` types allowed** - immediate conversion required
- **`type` over `interface`** - mandatory for consistency
- **Optional chaining required**: `obj?.prop` never `obj.prop` for uncertain data
- Modern ES6+: async/await, destructuring, optional chaining
- Error handling: Try-catch blocks, error boundaries, user-friendly messages
- **Strict TypeScript**: No `any` types, proper interfaces, use `type` over `interface` for consistency
- **Modern ES6+**: async/await, destructuring, optional chaining
- **Error handling**: Try-catch blocks, error boundaries, user-friendly messages
- **Null safety**: Use `obj?.prop` and `arr?.[0]` for uncertain data, `??` for defaults (`user?.name ?? 'Unknown'`)
- **Array access**: Check `arr.length > 0` before `arr[0]`, or use `arr[0]?.property` with optional chaining
- **Unused parameters**: Prefix with underscore (`_unused`) or add `// eslint-disable-next-line @typescript-eslint/no-unused-vars`
- **Pre-commit validation**: Always run `npm run validate` before `git commit`
- **Method signatures**: Keep unused params for API consistency, disable per-line: `// eslint-disable-next-line`
- **Architecture analysis**: Read existing class methods before adding new ones, match naming patterns
- **Defensive programming**: Assert data exists (`expect(result).toBeDefined()`) before accessing properties
- **Local CI simulation**: Run `docker-compose exec app npm test` and linting before every push
- **Interface compliance**: Copy exact method signatures when extending classes, maintain parameter order
- **Error boundaries**: Wrap uncertain ops: `try { await api() } catch (err) { throw new Error(\`Failed: \${err}\`) }`

**Coding Style Standards**

- Use kebab-case for directories (`apiKey/`), PascalCase for components (`UserProfile.tsx`)
- Use camelCase for utilities (`formatDate.ts`), UPPER_SNAKE_CASE for constants (`API_ENDPOINTS.ts`)
- Use PascalCase for classes (`UserService`), camelCase for variables/functions (`userProfile`, `getUserData()`)
- Use descriptive names with boolean prefixes (`isLoading`) and verb prefixes (`get`, `set`, `update`)

**Testing & Quality**

- Jest (unit) and Playwright (e2e) for all new functionality
- Mock external dependencies, follow `__tests__/` structure
- Zero ESLint warnings/errors
- Pre-commit hooks and CI/CD validation

**Test Coverage Standards**

- **Minimum thresholds**: Branches 35%, Functions 34%, Lines 37%, Statements 37% (current baseline)
- **Target thresholds**: Gradual increase to 70-80% over time (5% per quarter)
- **New features**: Must include tests that maintain or improve coverage percentages
- **Repository tests**: Required for all CRUD operations and complex queries
- **Critical paths**: Auth, payment, data access must have >80% coverage
- **Pre-commit**: Related tests run automatically, must pass before commit

**Database Schema Standards**

- Use PascalCase for model names (`User`, `Team`, `ApiKey`)
- Use camelCase for field names (`userId`, `createdAt`, `emailVerified`)

**Repository Pattern Standards**

- All database access through repository classes extending BaseRepository
- Use Prisma-generated types for type-safe queries: `Prisma.UserGetPayload<{...}>`
- Security-first: Always use SafeUser types that exclude password field
- Complex queries: Prefer `Prisma.ModelGetPayload` over manual type definitions
- Repository methods must return `RepositoryResult<T>` for consistent error handling
- Required test coverage: All repository CRUD operations must have unit tests

**Prisma Type Safety Patterns**

- **Advanced queries**: Use `Prisma.ModelGetPayload<{ include: {...}, select: {...} }>` for type-safe relations
- **Schema synchronization**: Prisma-generated types automatically update with schema changes
- **Security exceptions**: Keep explicit Omit types for password exclusion (e.g., `SafeUser = Omit<User, 'password'>`)
- **Migration path**: Gradually migrate manual types to Prisma.GetPayload patterns when convenient (see Issue #321)
- **Documentation**: Comment complex Prisma types to explain query structure and purpose

**Documentation Standards**

- Write clear comments explaining complex logic using JSDoc format
- Keep comments and documentation current with code changes

**Front-End Quality**

- Mobile-first responsive (320px-4K), semantic HTML, ARIA compliance
- Performance: lazy loading, code splitting, Core Web Vitals optimization
- Component-scoped CSS, 60fps animations, design tokens

## Security Standards

- Validate/sanitize all inputs, reject unknown fields
- XSS prevention: sanitize content, use CSP
- Minimal PII logging, secure data handling

## Definition of Done

**Never declare completion until ALL checks pass:**
Commit → Push → Wait for CI green → Cross-browser test → PR from `dev`

**Rule**: Never mark "completed" until CI is green

## Failure Recovery Protocol

**When Cursor Ignores These Rules:**

1. STOP current work immediately
2. Re-read entire cursorrules.md file
3. State: "Resuming work following cursorrules.md protocols"
4. Run TypeScript check before continuing

## Context Preservation Rules

**Session Continuity:**

- Always reference this file at conversation start
- Summarize current TODO status before code changes
- Confirm Ana/Tod integration status
- State current development mode explicitly

**Multi-turn Conversations:**

- Re-read cursorrules every 10-15 exchanges
- Periodically confirm: "Following cursorrules.md, current mode is [X], Tod TODOs: [Y]"
- Ask for rule clarification if uncertain

## Cursor Integration Checkpoints

**Before ANY code modification:**

- [ ] Read current cursorrules.md completely
- [ ] **MANDATORY**: Run `docker-compose exec app npx tsc --noEmit` to check TypeScript compliance

**After ANY code change:**

- [ ] **CRITICAL**: Run `npm run validate` or `npm run validate:docker`
- [ ] All TypeScript errors MUST be fixed before proceeding

**TypeScript Enforcement:**

- Zero `any` types allowed - convert to proper types immediately
- Missing interfaces/types cause immediate work stoppage
- `type` over `interface` - fix on sight
- Optional chaining required for uncertain data: `obj?.prop` not `obj.prop`
