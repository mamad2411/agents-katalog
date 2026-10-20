# AGENTS.md

This project uses CursorRules—a collection of development standards and anti-pattern rules. This AGENTS.md provides guidance for non-Cursor agents (Aider, Gemini CLI, Zed). Cursor users get full rules from `.cursor/rules/`.

## Forbidden Phrases (without proof)

"compiles", "builds", "zero warnings", "build succeeded" → Must show build output or say "verification pending"

## File and Directory Naming

No spaces in file or directory names; use underscores, hyphens, or language-appropriate case. Use only safe characters (letters, digits, underscore, hyphen). Dates in names: YYYY-MM-DD or YYYYMMDD. Zero-pad version suffixes (v01, v02). One convention per project; if the project already has one, keep it. For non-source assets (docs, exports, logs), optional pattern: subject_date_code with dashes in subject and underscores between parts. Source file naming per language: Python snake_case modules; Java one public class per file, filename = class name; Go lowercase + underscores; Swift PascalCase; Rust snake_case for modules and files; JavaScript/TypeScript follow project or use kebab-case. Full rules: `.cursor/rules/general-llm-anti-patterns.mdc` Category 12.

## Top 15 Universal Anti-Patterns

### 1. Ghost Layer Prevention

❌ Bad: `class Service { func get() { return repo.get() } }` (>80% delegation)
✅ Good: Service coordinates multiple repos OR adds logic OR delete layer
⚠️ Why: Adds complexity without value, violates SRP
📍 See: `.cursor/rules/general-llm-anti-patterns.mdc` section 1.1

### 2. Fake Abstraction Patterns

❌ Bad: `actor Repo { func process() async { await MainActor.run { } } }` (defeats isolation)
✅ Good: `actor Repo { func process() async { /* actual async work */ } }`
⚠️ Why: Creates illusion of concurrency without benefits, adds overhead
📍 See: `.cursor/rules/general-llm-anti-patterns.mdc` section 1.2

### 3. Placeholder & Dead Code Ban

❌ Bad: `func method() { throw NotImplementedError() }` or `_ = expensiveOperation()`
✅ Good: Implement, remove, or mark unavailable with explanation
⚠️ Why: Broken functionality, wasted resources, technical debt
📍 See: `.cursor/rules/general-llm-anti-patterns.mdc` section 1.3

### 4. Business Logic Location

❌ Bad: Repository contains switch statements, state transitions, business calculations
✅ Good: Repository is pure CRUD, business logic in Domain layer
⚠️ Why: Creates God Objects, untestable code, tight coupling
📍 See: `.cursor/rules/general-llm-anti-patterns.mdc` section 1.4

### 5. Performance-First Collection Handling

❌ Bad: `for item in items { await processItem(item) }` (I/O in loop = O(N²))
✅ Good: Batch operations - fetch once, modify in-memory, save once
⚠️ Why: UI freezes at scale, database exhaustion, poor UX
📍 See: `.cursor/rules/general-llm-anti-patterns.mdc` section 2.1

### 6. Zero-Hallucination Policy

❌ Bad: Multi-step search workaround when direct lookup API exists
✅ Good: Verify framework documentation, use official APIs
⚠️ Why: Fragile code, security risk (slopsquatting), build failures
📍 See: `.cursor/rules/general-llm-anti-patterns.mdc` section 4.1

### 7. Hardcoded Secrets

❌ Bad: `apiKey = "sk-live-1234567890abcdef"` in source code
✅ Good: `apiKey = process.env.API_KEY` (environment variables)
⚠️ Why: Security vulnerability, credential exposure, compliance violations
📍 See: `.cursor/rules/general-llm-anti-patterns.mdc` section 5.1

### 8. Missing Input Validation

❌ Bad: `database.query("SELECT * FROM users WHERE id = " + userInput)`
✅ Good: Validate input, use parameterized queries
⚠️ Why: SQL injection, XSS, command injection, system compromise
📍 See: `.cursor/rules/general-llm-anti-patterns.mdc` section 5.2

### 9. Silent Failures

❌ Bad: `try { op() } catch { pass }` (swallows errors)
✅ Good: Handle specific errors or explicitly propagate with context
⚠️ Why: Hidden bugs, difficult debugging, silent data loss
📍 See: `.cursor/rules/general-llm-anti-patterns.mdc` section 5.3

### 10. Test-Implementation Mismatch

❌ Bad: Mock returns different types/behavior than real implementation
✅ Good: Mocks match real API signatures and behavior exactly
⚠️ Why: False confidence, integration failures, production bugs
📍 See: `.cursor/rules/general-llm-anti-patterns.mdc` section 6.1

### 11. Warning Dismissal Anti-Pattern

❌ Bad: Comments dismissing warnings as "false positives" or "won't affect runtime"
✅ Good: Fix all warnings; if truly unfixable, document technical reason and escalate
⚠️ Why: Warnings indicate real issues; dismissing them creates technical debt
📍 See: `.cursor/rules/general-llm-anti-patterns.mdc` section 3.7

### 12. False Compilation Claims

❌ Bad: "All code compiles with zero warnings" (without running build)
✅ Good: "Code changes complete. Build verification pending." OR show actual build output
⚠️ **STOP:** If typing "compiles"/"builds"/"zero warnings" → Verify: Did I run a build? If no → Use "Build verification pending"
⚠️ Why: Creates false confidence, wastes user time, violates trust, leads to broken code
📍 See: `.cursor/rules/general-llm-anti-patterns.mdc` section 3.8

### 13. False Test Verification Claims

❌ Bad: "All tests pass" (without running tests)
✅ Good: "Code changes complete. Test verification pending." OR show actual test output
⚠️ Why: Creates false confidence, wastes user time, violates trust, leads to broken code
📍 See: `.cursor/rules/general-llm-anti-patterns.mdc` section 3.9

### 14. Package Verification (Slopsquatting Prevention)

❌ Bad: `import suspicious_package` (unverified package), importing plausible-sounding packages without checking
✅ Good: Verify package exists in registry, check maintainer, check download stats, verify owner
⚠️ Why: Security risk (slopsquatting), attackers register packages with LLM-hallucinated names, build failures
🔧 Fix: Always verify packages exist, check package registry before importing, verify maintainer identity
📍 See: `.cursor/rules/general-llm-anti-patterns.mdc` section 4.2d

**Detect:** Import statements without verification, plausible-sounding but unverified packages, no package registry checks

### 15. Example Over-Reliance

❌ Bad: Example code used verbatim without adaptation
✅ Good: Adapt examples to project patterns, verify examples match requirements
⚠️ Why: Example code may not fit project patterns, introduces inconsistencies
📍 See: `.cursor/rules/general-llm-anti-patterns.mdc` section 4.4

**Detect:** Example code used verbatim, example code not adapted to project patterns, copy-paste without modification

**Security (OWASP):** Security practices align with the [OWASP Secure Coding Practices Quick Reference](https://owasp.org/www-project-secure-coding-practices-quick-reference-guide/stable-en/02-checklist/05-checklist.html). Full checklist and detection criteria: `.cursor/rules/owasp-secure-coding-practices.mdc`.

## Cooperative Communication (Grice-inspired)

Before sending a response, check: **Epistemic quality** — no unsupported build/test/API claims; say "verification pending" with commands attempted when unverified. **Quantity** — match depth to task; no essay for simple asks. **Relation** — answer the ask first; stay on-scope. **Manner** — lead with outcome; then steps/evidence; prefer active voice and short full sentences; cut pleasantries and filler; keep code, paths, APIs, and errors exact.

Details: `.cursor/rules/critical-rules-quick-reference.mdc` Cooperative Communication; `.cursor/rules/general-llm-anti-patterns.mdc` §9.6–9.8a.

## Phase Verification Workflows

After completing a development phase, run the appropriate brutal audit from `.cursor/rules/`:

- **Swift/iOS projects**: `swift-5-9-brutal-audit.mdc` (Swift 5.9) or `swift-6-brutal-audit.mdc` (Swift 6 language mode)
- **Python projects**: `python-3-brutal-audit.mdc`
- **Java projects**: `java-brutal-audit.mdc` (Java 17/21)
- **Go projects**: `go-1-21-brutal-audit.mdc`
- **JavaScript/TypeScript projects**: `javascript-3-brutal-audit.mdc`
- **Rust projects**: `rust-brutal-audit.mdc`

**When to run:** After each development phase, before marking work "ready for next phase," or when code quality concerns arise.

**How to invoke:** Mention "run the audit", "check for anti-patterns", or "verify phase completion"

## For Contributors (CursorRules repository)

When contributing to CursorRules itself, see [CONTRIBUTING.md](CONTRIBUTING.md) and [RULE_COMPOSITION.md](RULE_COMPOSITION.md). Rules live in `.cursor/rules/`.

**Obsidian vault rules:** `obsidian-vault-standards.mdc` (glob-scoped anti-patterns), `obsidian-integration.mdc` (CLI). Pair with upstream [obsidian-skills](https://github.com/kepano/obsidian-skills)—link only, do not vendor skill files in this repo.

**Taskplane task packets:** `taskplane-task-authoring.mdc` (create `PROMPT.md` / `STATUS.md` packets; runner-agnostic), `taskplane-worker-cursor.mdc` (execute a packet in-editor). Templates: `.cursor/rules/taskplane/prompt-template.md`, `status-template.md`. See README Taskplane section and [Cursor Rules](https://cursor.com/docs/rules).

**pi-spine task packets:** `spine-task-authoring.mdc` (author `SP-*` packets with Contract + `dependencies.json`), `spine-operator-cursor.mdc` (operate `spine` CLI batches), `spine-worker-cursor.mdc` (manual in-Cursor execution when batch inactive). Pair with [pi-spine](https://github.com/beettlle/pi-spine) (`pi install npm:pi-spine`). See README pi-spine section and `RULE_COMPOSITION.md` examples 9–11. Declare spine vs Taskplane in consumer `AGENTS.md`.

## Project-Specific Sections

<!-- Fill in for your project -->

### Dev environment tips

- Setup commands, build, run

### Testing instructions

- How to run tests, validation checks

### PR/commit instructions

- Follow [.cursor/rules/git-workflow-and-pr.mdc](.cursor/rules/git-workflow-and-pr.mdc) for commit messages (Conventional Commits), branch naming, rebase/merge safety, and PR titles/descriptions.

## Nested AGENTS.md (optional)

For monorepos or large codebases, place `AGENTS.md` in subdirectories. Agents (e.g., Codex, Gemini CLI) read the nearest file in the directory tree; the closest one takes precedence.
