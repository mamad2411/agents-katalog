---
name: "microservice-iteration-handoff"
description: "Git workflow, code quality checklist, and handoff documentation process for iterative microservices development. Ensures stable, reviewable code sharing between development iterations with proper branch strategy and commit standards."
version: 2
created: "2026-06-09T03:34:24+05:30"
updated: "2026-06-26"
---
## When to Use
Use when completing a development iteration and preparing code for handoff to another team or iteration. Apply before pushing code to remote repository, before creating pull requests, or when establishing team Git workflow standards. Essential for ensuring code is compilation-ready, tested, documented, and follows team conventions. **Resolve the coverage target, migration tool, and secrets vault from the TSA** (`tsa.testing.unit_tests.coverage_target`, `tsa.technology.database.migration_tool`, `tsa.compliance_and_security.security_controls.secrets_management` / `tsa.deployment.configuration_management`) — do not hardcode them.

## Procedure
1. STEP 1: Branch Strategy Setup - Use GitFlow or trunk-based development. Main branches: main/master (production), develop (integration), feature/* (new features), bugfix/* (bug fixes), release/* (release prep). Create feature branch from develop: 'git checkout -b feature/TICKET-123-description develop'. Use naming convention: feature/JIRA-ID-short-description (e.g., feature/SALES-456-lead-api). Keep branches short-lived (< 1 week). Merge to develop when complete, then delete feature branch
2. STEP 2: Pre-Commit Quality Checklist - RUN: 'mvn clean compile' (must succeed with zero errors). RUN: 'mvn clean test' (all tests pass, no skipped tests). RUN: 'mvn jacoco:report' (verify coverage meets `tsa.testing.unit_tests.coverage_target`, e.g. >= 80% line). RUN: 'mvn checkstyle:check' (no violations). VERIFY: No commented-out functional code, no TODO/FIXME/STUB (zero-TODO policy). VERIFY: No hardcoded credentials or URLs (and no tenant IDs unless the TSA declares multi-tenancy). VERIFY: All new public methods have Javadoc. VERIFY: No unused imports, no System.out.println, no .printStackTrace(). VERIFY: Files end with newline, proper indentation (4 spaces)
3. STEP 3: Commit Message Standards - Use conventional commits format: type(scope): description. Types: feat (new feature), fix (bug fix), refactor (code restructure), test (add tests), docs (documentation), chore (build/config). Example: 'feat(lead-api): add POST /api/v1/leads endpoint with validation'. Include JIRA ticket in footer: 'Refs: SALES-456'. Keep subject line <= 72 chars. Use imperative mood: 'add feature' not 'added feature'. Separate subject and body with blank line. Explain WHY in body, not WHAT (code shows what)
4. STEP 4: Code Documentation Requirements - Update README.md with: service purpose, API endpoints (method, path, description), environment variables required, build/run instructions. Create or update ADR (Architecture Decision Record) for significant design choices. Add OpenAPI/Swagger documentation for all REST endpoints (@Operation, @ApiResponse). Document multi-tenant setup in a separate MULTI_TENANT.md only if the TSA declares multi-tenancy. Add inline comments for complex business logic only (not obvious code). Update CHANGELOG.md with feature additions and breaking changes
5. STEP 5: Dependency and Configuration Audit - Run 'mvn dependency:tree > dependency-tree.txt' and commit to docs/. Verify no SNAPSHOT dependencies in pom.xml (only release versions). Check all versions are managed in parent POM dependencyManagement. Verify application.yml has placeholders ${ENV_VAR:default} for environment-specific values. NO hardcoded URLs, credentials, or database names. Document all required environment variables in README.md. Run OWASP dependency check: 'mvn dependency-check:check' (no HIGH/CRITICAL vulnerabilities)
6. STEP 6: Test Evidence Collection - Capture test execution output: 'mvn clean test > test-output.txt'. Capture JaCoCo coverage report: save target/site/jacoco/index.html. Document test strategy: unit test count, integration test count, coverage %. Create test data documentation if using specific test datasets. Document any known test limitations or edge cases not covered. For integration tests, document Docker/Testcontainers requirements
7. STEP 7: Create Pull Request - Push feature branch: 'git push origin feature/TICKET-123-description'. Create PR from feature branch to develop. PR title: conventional commit format (same as main commit). PR description template: ## Summary (what changed), ## JIRA Ticket (link), ## Testing (how tested), ## Checklist (compilation ✓, tests ✓, coverage ✓, documentation ✓). Add reviewers (at least 2). Link JIRA ticket in PR. Add labels: enhancement/bugfix/documentation
8. STEP 8: Code Review Response - Address ALL review comments (fix or explain). DO NOT merge with unresolved comments. Push fixes as new commits (do not force-push during review). Re-run tests after fixes: 'mvn clean test'. Update PR description if significant changes made. Request re-review after addressing comments. Squash commits before final merge if team prefers clean history
9. STEP 9: Merge and Handoff - Verify CI/CD pipeline passes (compilation, tests, quality gates). Squash and merge to develop (or use merge commit if team prefers full history). Delete feature branch after merge: 'git branch -d feature/TICKET-123-description'. Tag release if applicable: 'git tag -a v1.2.0 -m Release 1.2.0'. Update JIRA ticket status to Done/Merged. Notify team in Slack/Teams with: PR link, what was delivered, any breaking changes, next steps
10. STEP 10: Iteration Handoff Documentation - Create HANDOFF.md with: ## Completed Features (list with JIRA tickets), ## Known Issues (bugs, tech debt), ## Next Iteration Priorities (backlog), ## Dependencies (external services, databases), ## Configuration Changes (new env vars, property changes), ## Database Migrations (migration scripts applied via the TSA migration tool, e.g. Flyway V<n>__*.sql), ## Breaking Changes (API changes, deprecated endpoints). Include contact info for questions. Commit HANDOFF.md to repository root

## Pitfalls
- DO NOT commit without running tests - always verify 'mvn clean test' passes before commit
- DO NOT push code that does not compile - run 'mvn clean compile' before every push
- DO NOT commit commented-out code or TODOs without JIRA tickets - clean up before commit
- DO NOT use vague commit messages like 'fix bug' or 'update code' - be specific and follow conventional commits
- DO NOT commit secrets, credentials, or API keys - use environment variables or the secrets vault named in the TSA (e.g. AWS Secrets Manager for reset-password)
- DO NOT skip code documentation - update README.md and add Javadoc for public APIs
- DO NOT merge PRs with unresolved comments - address all feedback before merging
- DO NOT force-push after creating PR - it breaks review history (push new commits instead)
- DO NOT commit dependency-tree.txt or test-output.txt to main branch - these go in docs/ or .gitignore
- DO NOT use SNAPSHOT dependencies in release branches - pin to stable versions
- DO NOT merge without CI/CD pipeline passing - wait for all checks to succeed
- DO NOT delete feature branches before verifying merge to develop - confirm successful merge first
- DO NOT skip JaCoCo coverage check - enforce the `tsa.testing.unit_tests.coverage_target` (e.g. >= 80% line) before merge
- DO NOT commit .idea/, .vscode/, target/, .DS_Store - ensure .gitignore excludes these
- DO NOT use generic branch names like 'feature-1' or 'my-branch' - use JIRA ticket ID and description

## Verification
1. Run 'mvn clean compile' successfully with zero errors
2. Run 'mvn clean test' with all tests passing and coverage meeting the TSA target (e.g. >= 80% line)
3. Run 'mvn checkstyle:check' with no violations
4. Verify README.md updated with API endpoints, env vars, build instructions
5. Check commit messages follow conventional commits format (type(scope): description)
6. Verify no hardcoded credentials or secrets in codebase (grep -r 'password' src/)
7. Confirm .gitignore excludes target/, .idea/, .vscode/, *.log, *.class
8. Validate CHANGELOG.md or HANDOFF.md documents changes for this iteration
9. Check PR description includes summary, testing, checklist, JIRA link
10. Verify CI/CD pipeline passes with green build status
11. Confirm feature branch deleted after successful merge
12. Validate no commented-out functional code (only minimal explanatory comments)
13. Check all public methods have Javadoc documentation