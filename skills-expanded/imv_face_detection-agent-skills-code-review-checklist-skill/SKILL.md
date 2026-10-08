---
name: code-review-checklist
description: Performs thorough code reviews for Flutter/Dart pull requests and merge requests. Use when asked to review a PR, MR, branch, or changed files. Follows a structured checklist covering correctness, security, style, testing, and documentation.
---

# Code Review Skill

## When to Use

Use this skill when:
* Asked to review a pull request, merge request, or branch.
* Evaluating changed, added, or deleted files for correctness and quality.

---

## Review Process

### 1. Branch and Merge Target

- Confirm the current branch is a **feature, bugfix, or PR/MR branch** — not `main`, `master`, or `develop`.
- Verify the branch is **up-to-date** with the target branch.
- Identify the **target branch** for the merge.

### 2. Change Discovery

- List all **changed, added, and deleted files**.
- For each change, look up the **commit title** and review how connected components are implemented.
- **Never assume** a change or fix is correct without investigating the implementation details.
- If a change remains difficult to understand after several attempts, **note this explicitly** in your report.

### 3. Per-File Review

For every changed file, check:

| Area | What to verify |
|---|---|
| **Location** | File is in the correct directory |
| **Naming** | File name follows naming conventions |
| **Responsibility** | The file's responsibility is clear |
| **Readability** | Variable, function, and class names are descriptive and consistent |
| **Logic & correctness** | No logic errors or missing edge cases |
| **Maintainability** | Code is modular; no unnecessary duplication |
| **Error handling** | Errors and exceptions are handled appropriately |
| **Security** | No input validation issues; no secrets committed to code |
| **Performance** | No obvious performance issues or inefficiencies |
| **Documentation** | Public APIs, complex logic, and new modules are documented |
| **Test coverage** | New or changed logic has sufficient tests |
| **Style** | Code matches the project's style guide and coding patterns |

For **generated files**: confirm they are up-to-date and not manually modified.

### 4. Overall Change Set

- Verify the change set is **focused and scoped** to its stated purpose — no unrelated changes.
- Check that the **PR/MR description** accurately reflects the changes.
- Confirm **new or updated tests** cover new or changed logic.
- Evaluate whether tests could **actually fail**, or only verify a mock implementation.

### 5. CI and Tests

- Ensure **all tests pass** in the CI system.
- Fetch **online documentation** when unsure about best practices for a package.

---

## Quick Review Checklist

### Correctness
- [ ] Code does what it's supposed to do
- [ ] Edge cases handled
- [ ] Error handling in place
- [ ] No obvious bugs

### Security
- [ ] Input validated and sanitized
- [ ] No hardcoded secrets or sensitive credentials
- [ ] No XSS, CSRF, or injection vulnerabilities
- [ ] **AI-Specific:** Protection against Prompt Injection (if applicable)
- [ ] **AI-Specific:** Outputs are sanitized before being used in critical sinks

### Performance
- [ ] No N+1 queries
- [ ] No unnecessary loops or rebuilds
- [ ] Appropriate caching
- [ ] Bundle size impact considered

### Code Quality
- [ ] Clear naming (follows Effective Dart)
- [ ] DRY — no duplicate code
- [ ] SOLID principles followed
- [ ] Appropriate abstraction level
- [ ] Trailing commas used consistently

### Testing
- [ ] Unit tests for new BLoC/Cubit logic
- [ ] Edge cases tested
- [ ] Tests are readable, maintainable, and **can actually fail**

### Documentation
- [ ] Public APIs documented with `///` comments
- [ ] README updated if needed

---

## Anti-Patterns to Flag

```dart
// ❌ Magic numbers
if (status == 3) { ... }

// ✅ Named constants
if (status == Status.active) { ... }

// ❌ Deep nesting
if (a) { if (b) { if (c) { ... } } }

// ✅ Early returns
if (!a) return;
if (!b) return;
if (!c) return;
// do work

// ❌ dynamic type
final data = someUntypedFunction();

// ✅ Explicit types
final UserData data = someTypedFunction();

// ❌ Raw boolean state
class MyState { final bool isLoading; }

// ✅ BlocStatus pattern
class MyState { final BlocStatus status; }
```

---

## Feedback Standards

- Be **objective and reasonable** — avoid automatic praise or flattery.
- Take a **devil's advocate approach**: give honest, thoughtful feedback.
- Provide **clear, constructive feedback** with suggestions for improvement.
- Include **requests for clarification** for anything that is unclear.

---

## Output Format

Provide your review covering **per file**:

1. Summary of what changed and why
2. Issues found (with severity: 🔴 **BLOCKING** / 🟡 **SUGGESTION** / 🟢 **NIT**)
3. Specific recommendations or questions (❓ **QUESTION**)
4. Overall verdict: **approved**, **approved with suggestions**, or **changes requested**
