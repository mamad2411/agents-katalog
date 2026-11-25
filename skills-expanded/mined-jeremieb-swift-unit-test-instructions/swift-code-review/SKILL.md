---
name: swift-code-review
description: Reviews Swift, SwiftUI, and UIKit code for MVVM compliance, testing standards, naming conventions, async correctness, and anti-patterns. Produces structured feedback grouped by severity. Use when user says "review this code", "check this PR", "code review", "is this correct", "give me feedback on", "review my implementation", or "what's wrong with this code".
metadata:
  author: swift-unit-test-instructions
  version: 1.0.0
  category: swift
---

# Swift Code Review

## Instructions

### Step 1: Read All Provided Files

Read every file mentioned or pasted before writing any comments. Do not review code you have not fully read.

If reviewing a PR, ask for:
- The feature or bug being fixed
- The files changed
- Any context about constraints or trade-offs

### Step 2: Apply the Review Checklist

**Architecture (MVVM)**
- [ ] Business logic is in ViewModel or Service — not in View/ViewController body
- [ ] External dependencies (network, storage, time) are injected via protocol, not hardcoded
- [ ] No `URLSession.shared`, `UserDefaults.standard`, or `Date()` called directly from Views
- [ ] No global singletons used without injection support
- [ ] Thin View layer: no conditional business logic, no data fetching in `onAppear` without ViewModel delegation

**Swift Quality**
- [ ] No force unwraps (`!`) in production paths
- [ ] Errors propagated via `throws` or `Result` — not silently swallowed
- [ ] `let` preferred over `var` where value does not change
- [ ] No magic numbers or hardcoded strings — use named constants or localizable strings
- [ ] One primary type per file

**Concurrency**
- [ ] `async/await` used for all new async code (not completion handlers)
- [ ] `@MainActor` applied to ViewModel and any type that updates UI state
- [ ] No `DispatchQueue.main.async` in ViewModel or Service layers
- [ ] No `sleep()` anywhere
- [ ] `Sendable` conformance considered for types crossing actor boundaries
- [ ] `Task` objects are stored and cancelled if the parent scope is deallocated

**Testing**
- [ ] New business logic has corresponding tests
- [ ] New dependencies are injectable (protocol-backed)
- [ ] Existing tests still compile and pass
- [ ] No test changes that weaken coverage of critical paths

**Naming**
- [ ] Types: `UpperCamelCase`
- [ ] Functions / variables: `lowerCamelCase`
- [ ] Booleans: assertion form (`isLoading`, `hasError`, `canSubmit`, `isPremium`)
- [ ] Avoid abbreviations unless universally understood (`url`, `id`, `api`)
- [ ] Test methods: `test_when_<Condition>_should_<ExpectedOutcome>()`
- [ ] Protocol names: noun or adjective, not `Protocol` suffix (prefer `UserRepository` over `UserRepositoryProtocol` where unambiguous, but `Protocol` suffix is acceptable for clarity)

**SwiftUI Specific**
- [ ] `@StateObject` / `@State` used in the View that owns the instance
- [ ] `@ObservedObject` / `@Binding` used for passed-in instances
- [ ] No `@EnvironmentObject` used for types that should be injected explicitly
- [ ] `#Preview` compiles and shows correct content
- [ ] Accessibility labels on interactive elements that lack visible text

**UIKit Specific**
- [ ] ViewControllers are thin: no network calls, no business logic
- [ ] `IBOutlet` and `IBAction` limited to UI wiring only
- [ ] Memory management: no retain cycles in closures (use `[weak self]`)
- [ ] No layout code hardcoded in `viewDidLoad` that belongs in a dedicated setup method

### Step 3: Format the Review

Group by severity. Be specific. Include file name and line number or code excerpt.

```markdown
## Code Review: [File or Feature Name]

### Critical — Must Fix
These block approval. Fix before merge.

- **[Issue title]** in `FileName.swift`
  ```swift
  // Problematic code
  ```
  **Why**: [Clear explanation of the problem and risk]
  **Fix**:
  ```swift
  // Suggested fix
  ```

### Suggested — Should Fix
Strong recommendations that improve correctness, testability, or maintainability.

- [Issue] — [file] — [brief explanation and fix direction]

### Minor — Nice to Have
Style, preference, or low-risk improvements. Non-blocking.

- [Note]

### Approved
What is done well — acknowledge good patterns explicitly.

- [What works well and why]
```

### Step 4: Final Verdict

End with one of:
- **Approved** — ready to merge as-is
- **Approved with suggestions** — can merge, but consider the Suggested items
- **Changes requested** — Critical items must be resolved before merge

## Examples

### Example 1: ViewModel review

User says: "Review my LoginViewModel"

Actions:
1. Read `LoginViewModel.swift`
2. Read `LoginViewModelTests.swift` (if it exists)
3. Apply checklist
4. Note: is it testable? Are dependencies injected? Is async correct?
5. Output structured feedback

### Example 2: PR review across multiple files

User says: "Review my PR for the checkout feature — here are the changed files"

Actions:
1. Read all changed files
2. Understand the feature end-to-end
3. Apply checklist to each file
4. Identify cross-file issues (e.g., a service that's not injectable, a missing mock)
5. Output grouped review by file, then overall verdict

### Example 3: Quick sanity check

User says: "Is this code correct?"

Actions:
1. Read the code
2. Focus checklist on correctness (async, force unwraps, error handling)
3. Brief response: "This looks correct, but note X" or list Critical issues

## Troubleshooting

**Too many issues to list**: Focus on Critical and top Suggested. List remaining Minor issues as a bullet group: "Additional minor style notes: [list]". Do not overwhelm with exhaustive nit-picking.

**Reviewer disagreement on style**: If the project has a style guide (`CLAUDE.md` or linting config), defer to it. Otherwise, note it as Minor and avoid blocking on pure preference.

**Legacy code with known issues**: When reviewing a small change in a large legacy file, focus the review scope on the changed lines. Do not audit the entire file — note "broader refactoring needed in this file" as a separate future work item.
