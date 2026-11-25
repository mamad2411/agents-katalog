---
name: vibe-audit
description: Performs a comprehensive, platform-agnostic static audit of a codebase. Returns a structured JSON report identifying architectural inconsistencies, security flaws, AI-generated technical debt, and violations of clean code principles. Provides a targeted migration path for refactoring. Triggers when the user asks to audit, review, or assess a codebase for quality, consistency, architecture, or security — even casual phrasing like "check my code", "review this repo", "find problems in my project", or "what's wrong with this codebase". Also triggers for architecture recommendations, code smell detection, dependency health checks, or security hygiene reviews across a project. Do NOT use for single-file code reviews, runtime profiling, or performance benchmarking.
---

# Universal Codebase Audit Skill

Perform a comprehensive, platform-agnostic static audit of the entire codebase. Focus on code quality, consistency, architecture, and security standards using established software engineering principles.

## Phase 1: Reconnaissance & Gatekeeping

### Step 1: Discovery (Read Light First)
Do NOT read all source files immediately. Instead:
1. Use `bash` with `find` or `ls -R` to get the file tree — structure and naming only.
2. Use `view` to read dependency and configuration files (e.g., `package.json`, `Podfile`, `build.gradle`, `pom.xml`, `go.mod`, `CMakeLists.txt`, `Dockerfile`, `.env.example`).
3. Use `view` to read the `README` or existing architecture docs if present.
4. Use `bash` with `find <root> -name '*.ext' | wc -l` to count source files per language.

### Step 2: Scope & Gating (CRITICAL HALT)
Evaluate the discovery data. You **MUST HALT** and ask the user for input if either of these conditions are met:
- **Ambiguity:** The framework, scale, or project purpose cannot be deduced from the README/configs.
- **Scale Exceeded:** The codebase contains >80 source files. (Warn the user about context window limits and ask them to specify 2-3 core domains or folders to focus the audit on).

If the codebase is ≤80 files, decide your approach automatically:
- **Small (≤30 files):** Audit all files.
- **Medium (31–80 files):** Audit core/business-logic modules fully; scan peripheral modules (tests, config) for structure only.

### Step 3: Audit Category Selection
Present the user with the available audit categories and let them choose which to include. Default recommendation is 1-3.
1. **Tech Stack Consistency**
2. **Structure & Design Patterns**
3. **Security Hygiene**
4. **Dependency Health**
5. **Test Coverage Consistency**
6. **Documentation Consistency**
7. **Logging & Observability**
8. **Code Duplication**

## Phase 2: Targeted Clean Code & Vibe-Coding Audit

### Step 4: Chunked Codebase Analysis
Analyze the codebase one domain or top-level module at a time. While checking the categories the user selected, evaluate the code through two primary lenses:

**Lens A: Robert C. Martin's Clean Code Principles**
- Meaningful naming (intention-revealing, no disinformation).
- Function design (SRP, small size, monadic/dyadic arguments, no side effects).
- Exception-based error handling (no returning/passing `null`).
- Class design (cohesion, Open-Closed principle).

**Lens B: AI "Vibe-Coding" Pitfalls**
- Context Window Amnesia (duplicate logic with slightly different names, orphaned code).
- Deep Architectural Incoherence (mixing async paradigms or design patterns in the same module).
- Verbose Debt (redundant guard clauses, hyper-fragmented files).

For detailed checklists of what to look for in each category, read `references/category-checklists.md` and follow the relevant sections.

Log all findings — including Clean Code and Vibe-Coding violations — into the appropriate category in the `categories` object. Tag each finding's description with `(Clean Code)` or `(Vibe-Coding)` when the violation originates from one of these lenses.

## Phase 3: Synthesis & Output

### Step 5: Architecture Recommendation
Based on the project context and findings:
1. Describe the current architecture as-found.
2. Identify whether it fits the project's goals and scale.
3. Recommend a target architecture with rationale.
4. Propose a migration path formatted as an array of structured, actionable steps.

### Step 6: Output Generation
Generate the audit report as `audit-report.html` in the project root.

#### 1. Write `findings.json`

The JSON schema must strictly match the following format:

```json
{
  "project_name": "MyApp",
  "generated_date": "2026-04-07",
  "overall_score": 78,
  "context": "One paragraph describing project scale and platform.",
  "tech_stack": ["Python 3.11", "FastAPI", "PostgreSQL", "Docker"],
  "current_architecture": "Layered monolith with service/repository pattern.",
  "coverage": {
    "audited": ["src/api", "src/core", "src/models"],
    "skipped": ["tests/", "scripts/", "migrations/"]
  },
  "categories": {
    "structure_patterns": [
      {
        "description": "Function OrderProcessor.process() is 150 lines and violates SRP (Clean Code).",
        "severity": "confirmed",
        "severity_score": 7
      }
    ],
    "security_hygiene": [
      {
        "description": "DATABASE_URL hardcoded in config.py line 14.",
        "severity": "confirmed",
        "severity_score": 10
      }
    ]
  },
  "target_architecture": {
    "recommendation": "Move to a domain-driven layered structure with dedicated service classes.",
    "rationale": "The current flat structure causes cross-cutting concerns to leak.",
    "migration_path": [
      "Step 1: Extract auth middleware to satisfy SRP.",
      "Step 2: Create service classes per domain.",
      "Step 3: Introduce repository interfaces to facilitate unit testing."
    ]
  }
}
```

**Field reference:**
- `severity`: `"confirmed"`, `"likely"`, or `"uncertain"`.
- `severity_score`: Integer from `1` (lowest impact) to `10` (highest impact).
- `overall_score`: Integer `0`–`100`. Compute as `100 - (confirmed × 5) - (likely × 2) - (uncertain × 1)`, clamped to 0–100.
- `coverage`: Object with `"audited"` and `"skipped"` arrays of path strings. Renders as a two-column grid.
- `migration_path`: Array of strings.
- Only include categories the user selected in Step 3. Omit unselected categories entirely.

#### 2. Validate the JSON

```bash
python3 scripts/generate_audit_report.py --validate-only --findings findings.json
```

If validation fails, fix the JSON and re-validate. Only proceed once validation passes.

#### 3. Generate the report

```bash
python3 scripts/generate_audit_report.py --findings findings.json --output audit-report.html
```

### Manual Verification Reminder

Always include a section in the report reminding the user to:
- Run platform-specific vulnerability scanners (e.g., OWASP, `npm audit`, `pip-audit`).
- Run platform linters (e.g., SwiftLint, Ktlint, ESLint, Ruff).
- Check actual test coverage percentages with their CI tools.
