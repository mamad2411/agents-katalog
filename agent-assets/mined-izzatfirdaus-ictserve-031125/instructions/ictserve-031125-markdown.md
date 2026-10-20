---
applyTo: "**"
description: "CRITICAL POLICY: Mandatory output restrictions for all agents. Prohibits unauthorized file creation and enforces inline chat responses."
---

# 📝 Markdown & Output Policy

**CRITICAL MANDATE**: The default output mode for all agents is **INLINE CHAT**.
You are **STRICTLY PROHIBITED** from creating files to "summarize" or "report" on your work unless the user explicitly commands it.

---

## 🚫 File Creation Restrictions

### Absolute Prohibitions
Do **NOT** automatically create markdown files in these directories:
* `docs/` (Canonical documentation requires explicit approval)
* `.agents/` (Reserved for system configuration)
* `.github/` (CI/CD workflows only)
* `.kiro/`, `.amazonq/`, `.cursor/` (AI configuration)

### Banned File Types
You must **never** create these files as a "deliverable" for a task:
* ❌ `*-report.md`
* ❌ `*-summary.md`
* ❌ `*-analysis.md`
* ❌ `*-checklist.md`
* ❌ `implementation-*.md`
* ❌ `task-*.md`
* ❌ `completion-*.md`

**Reasoning**: These files become stale immediately. Context belongs in the **MCP Memory Server**, not in static files that clutter the repo.

---

## ✅ Approved Output Modes

### 1. Inline Chat Response (Default)
All explanations, summaries, code snippets, and verification steps must be rendered directly in the chat window using standard Markdown.

**Required Formatting:**
* Use `## Headings` to structure the response.
* Use code blocks with language tags (e.g., `php`, `bash`).
* Use tables for data comparison.
* Use checkboxes `[ ]` for actionable steps.

### 2. Explicit User Request (Exception)
You may create a file **ONLY IF** the user says:
* "Create a file named..."
* "Save this to [path]..."
* "Write a documentation file for..."

### 3. Canonical Documentation Updates
You may **edit** existing files in `docs/` (D00-D15) if your task involves updating the system documentation to reflect code changes.

---

## 💻 Code Generation Policy

### Minimal Implementation
When writing code (either in chat or applying edits):
1.  **NO** verbose boilerplate.
2.  **NO** commented-out legacy code.
3.  **NO** speculative features not requested.
4.  **YES** to strict typing (`declare(strict_types=1);`).

### Example

**Bad (Verbose):**
```php
/**
 * This service handles user creation.
 * It was created on 2025-11-30.
 */
class UserService {
    // Constructor
    public function __construct(
        protected UserRepository $repo
    ) {}

    public function create($data) {
        // Log the creation
        Log::info('Creating user');
        return $this->repo->create($data);
    }
}
````

**Good (Minimal & Strict):**

```php
declare(strict_types=1);

namespace App\Services;

class UserService
{
    public function __construct(
        private readonly UserRepository $repository
    ) {}

    public function create(array $data): User
    {
        return $this->repository->create($data);
    }
}
```

-----

## 🔗 Related Protocols

  * **Memory Management**: See `.agents/memory.instructions.md` for how to store context.
  * **Agent Personas**: See `.agents/AGENTS.md` for role-specific behaviors.
  * **Tech Stack**: See `.amazonq/rules/memory-bank/tech.md` for approved libraries.
