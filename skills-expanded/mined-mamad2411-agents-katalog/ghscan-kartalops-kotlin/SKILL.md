# Use This Skill — Reusable Prompt

Use this prompt to activate the KotlinForge skill for any Kotlin project work.

---

## Prompt Template

```
You are Claude Code. Use the KotlinForge skill for this Kotlin project.

## Project Context

[Describe the project: new Kotlin backend, Android app, KMP library, etc.]

## What to Do

1. Read `kotlinforge-skill/AGENT_DECISION_TREE.md` to determine the correct track
2. Complete the preflight checklist: `kotlinforge-skill/checklists/project-start.md`
3. Read the relevant guides for your track:
   - Ktor API: `guides/03-ktor-api.md`
   - Spring Boot: `guides/04-spring-boot-kotlin.md`
   - Android: `guides/06-android-clean-architecture.md`
   - KMP: `guides/07-kmp-structure.md`
   - Testing: `guides/08-testing-kotest-mockk.md`
   - Database: `guides/09-database-persistence.md`
   - Observability: `guides/10-observability-logging.md`
   - Security: `guides/11-security-and-config.md`
   - Anti-patterns: `guides/12-agent-anti-patterns.md`
4. Use the appropriate template from `kotlinforge-skill/templates/`
5. Follow the relevant review checklist:
   - API projects: `checklists/api-review.md`
   - Android projects: `checklists/android-review.md`
   - KMP projects: `checklists/kmp-review.md`
   - All projects: `checklists/testing-review.md`, `checklists/release-review.md`
6. Apply quality gates from `QUALITY_GATES.md`

## Key Rules

- Use Gradle Kotlin DSL (not Groovy)
- Use version catalog (`gradle/libs.versions.toml`)
- Never hardcode secrets — use environment variables
- Keep layers separate (domain → data → presentation)
- No business logic in Composables (Android)
- No `android.*` imports in KMP `commonMain`
- Use `viewModelScope` not `GlobalScope`
- Use `runTest` not `runBlocking` in tests
- Use fakes for internal dependencies, mocks only for external

## Output

After completing the work:
1. Run the build command to verify it compiles
2. Run the test command to verify tests pass
3. Use the review checklist to self-verify
4. Report completion with the relevant report file

```

---

## How to Use

Copy the template above, fill in the "Project Context" section, and use it as the starting prompt for any Kotlin project work.

### For New Projects

```markdown
You are Claude Code. Use the KotlinForge skill for this Kotlin project.

## Project Context

Build a lightweight REST API for a todo application using Ktor with PostgreSQL.
```

### For Existing Repos

```markdown
You are Claude Code. Use the KotlinForge skill for this Kotlin project.

## Project Context

Audit the existing Kotlin/Spring Boot codebase at [path]. Focus on:
1. Architecture correctness
2. Testing coverage
3. Security issues
```

### For Specific Features

```markdown
You are Claude Code. Use the KotlinForge skill for this Kotlin project.

## Project Context

Add user authentication with JWT to the existing Ktor API project.
Use the existing project structure and follow the anti-patterns guide to avoid common mistakes.
```

---

## Required Files

The skill requires these files to be present:

```
kotlinforge-skill/
├── AGENT_DECISION_TREE.md           # Track selection
├── QUALITY_GATES.md                 # Quality gate definitions
├── guides/
│   ├── 03-ktor-api.md               # Ktor guide
│   ├── 04-spring-boot-kotlin.md     # Spring guide
│   ├── 06-android-clean-architecture.md
│   ├── 07-kmp-structure.md
│   ├── 08-testing-kotest-mockk.md
│   ├── 09-database-persistence.md
│   ├── 10-observability-logging.md
│   ├── 11-security-and-config.md
│   └── 12-agent-anti-patterns.md
├── templates/
│   ├── ktor-api/
│   ├── spring-kotlin-api/
│   ├── android-clean-app/
│   └── kmp-library/
├── checklists/
│   ├── api-review.md
│   ├── android-review.md
│   ├── kmp-review.md
│   ├── testing-review.md
│   ├── release-review.md
│   └── project-start.md
└── prompts/
    ├── use-this-skill.md
    ├── audit-existing-kotlin-project.md
    └── generate-new-kotlin-project.md
```

---

## Anti-Pattern Checklist

Before generating any code, verify:

- [ ] Kotlin idioms used (not Java-shaped)
- [ ] Immutable by default
- [ ] No hardcoded secrets
- [ ] Version catalog used (not hardcoded versions)
- [ ] Layer separation maintained
- [ ] Tests use `runTest` (not `runBlocking`)
- [ ] ViewModels use `viewModelScope`
- [ ] KMP: no platform imports in `commonMain`

---

## Quality Gate Commands

```bash
# Build gate
./gradlew clean build --no-daemon

# Test gate
./gradlew test --no-daemon

# Lint gate
./gradlew ktlintCheck --no-daemon

# Security check
grep -rE "(api[_-]?key|password|secret|token)\s*=" --include="*.kt" src/

# Health check
curl -s http://localhost:8080/health | jq .
```

---

## Track Reference

| Project Type | Template | Key Guide |
|---------------|----------|-----------|
| Ktor API | `ktor-api/` | `03-ktor-api.md` |
| Spring Boot | `spring-kotlin-api/` | `04-spring-boot-kotlin.md` |
| Android | `android-clean-app/` | `06-android-clean-architecture.md` |
| KMP Library | `kmp-library/` | `07-kmp-structure.md` |
| Audit | — | `prompts/audit-existing-kotlin-project.md` |