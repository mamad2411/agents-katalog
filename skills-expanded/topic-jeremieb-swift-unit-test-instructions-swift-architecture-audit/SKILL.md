---
name: swift-architecture-audit
description: Audits an existing Swift/SwiftUI/UIKit codebase for MVVM compliance, testability issues, architectural violations, concurrency problems, and anti-patterns. Use when user says "audit the codebase", "review the architecture", "why is this hard to test", "onboard to this project", "analyze the code structure", "find issues in the code", or "what needs refactoring".
metadata:
  author: swift-unit-test-instructions
  version: 1.0.0
  category: swift
---

# Swift Architecture Audit

## Instructions

### Step 1: Explore the Project Structure

Identify the UI framework in use (SwiftUI, UIKit, or Mixed) by scanning the project — look for `@main`, `UIApplicationDelegate`, or `UIHostingController`. Then load the matching structure reference from `../swift-project-setup/references/` and use it as the baseline when identifying structural deviations.


Use subagents to parallelize exploration of large codebases.

Scan for:
- All feature folders and their naming patterns
- Number of `UIViewController` subclasses vs `ViewModel` types
- Number of SwiftUI `View` types
- Presence of protocol files in `Core/` or `Protocols/`
- Existing test targets and approximate test count

### Step 2: MVVM Compliance Check

Read representative files from 3-5 key features. Look for:

**Red flags (report each with file:line):**
- Business logic, network calls, or storage access directly inside SwiftUI `View` bodies
- Business logic inside `UIViewController` subclasses
- `URLSession.shared` or `UserDefaults.standard` called from Views or ViewControllers
- Missing ViewModel for any screen with non-trivial state
- `@State` or `@StateObject` holding data that belongs in a ViewModel or service

**Green flags (note these):**
- `ObservableObject` or `@Observable` ViewModels with clear state
- Services and repositories injected via initializer or `@Environment`
- Thin View layer (only layout and presentation)
- Coordinator / navigation layer separate from ViewModels

### Step 3: Testability Assessment

For each audited type, check:
- [ ] Are dependencies hardcoded (`let service = NetworkService()`) instead of injected?
- [ ] Do networking/storage types hide behind protocols?
- [ ] Are global singletons used without injection support?
- [ ] Is there any existing test coverage? How much?
- [ ] Are ViewModels testable in isolation (no UIKit/SwiftUI imports)?

Scoring:
- **High testability**: Protocols + DI everywhere, existing tests
- **Medium testability**: Some DI, some singletons, few tests
- **Low testability**: No protocols, no DI, no tests — refactoring needed before testing is possible

### Step 4: Concurrency Review

Identify:
- Completion handler usage where `async/await` should be used (new code)
- `DispatchQueue.main.async` scattered in ViewModel or service layers (use `@MainActor`)
- `@Published` properties updated from background threads without actor isolation
- Non-`Sendable` types crossing actor boundaries (potential data races)
- `sleep()` anywhere in the codebase

### Step 5: Anti-Pattern Inventory

| Anti-Pattern | Impact | Action |
|---|---|---|
| Massive ViewController | Untestable, unmaintainable | Extract ViewModel + Services |
| No protocol for external deps | Can't mock in tests | Wrap in protocol |
| Singleton abuse | Hidden coupling | Inject via init |
| Completion handlers in new code | Fragile async | Migrate to async/await |
| Force unwrap in production | Crashes | Replace with guard/if let |
| Business logic in View | Untestable | Move to ViewModel |

### Step 6: Generate Audit Report

```markdown
# Architecture Audit: [ProjectName]
Date: [date]

## Health Summary
Overall: [Good / Needs Work / Critical Issues]
MVVM Compliance: [High / Medium / Low]
Testability: [High / Medium / Low]
Concurrency: [Modern / Mixed / Legacy]

## Critical Issues (Fix First)
- [issue] in `FileName.swift:line` — [impact and suggested fix]

## Architectural Violations
- [violation] — [file(s) affected] — [recommended refactoring]

## Testability Blockers
- [blocker] — [which types are affected] — [fix: add protocol / inject dependency]

## Concurrency Issues
- [issue] — [file:line] — [suggested migration]

## Refactoring Priority
1. [Most critical — blocks testing or causes crashes]
2. [High priority — causes maintainability issues]
3. [Medium priority — worth cleaning up]
4. [Low priority / nice to have]

## Strengths
- [what the codebase does well — acknowledge good patterns]
```

## Examples

### Example 1: Legacy UIKit project

User says: "Audit the architecture, I want to add tests but everything is hard to test"

Actions:
1. Explore folder structure with subagent
2. Read 3 ViewControllers — assess logic placement
3. Check for protocol/DI usage across service layer
4. Generate prioritized audit report with specific files and lines

### Example 2: SwiftUI project onboarding

User says: "I just joined this project, give me an architecture overview"

Actions:
1. Map all feature modules
2. Identify patterns: which architecture style is in use (MVVM, MV, etc.)
3. Note testing state
4. Generate onboarding summary + list of known issues

## References

- `../swift-project-setup/references/structure-swiftui.md` — expected SwiftUI layout
- `../swift-project-setup/references/structure-uikit.md` — expected UIKit layout
- `../swift-project-setup/references/structure-mixed.md` — expected Mixed layout
- `../swift-project-setup/references/file-naming.md` — naming rules and "What Never Goes Where" table

## Troubleshooting

**Codebase is too large to read fully**: Use subagents to parallelize exploration. Focus the audit on the 3-5 most critical or highest-risk features (main flows, payment, authentication). Note coverage limitations in the report.

**No clear architecture pattern found**: Document what exists honestly. Don't assume intent. Recommend a migration path to MVVM with concrete first steps.
