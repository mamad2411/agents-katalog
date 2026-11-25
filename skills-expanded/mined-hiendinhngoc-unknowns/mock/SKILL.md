---
name: mock
description: Build a throwaway interactive prototype to validate one unresolved interaction or behavior before writing production code. Use when the user explicitly asks to "mock it up first" or "prototype this", or when competing UI behaviors need a disposable hands-on comparison.
version: 1.0.0
author: Hien Dinh
license: MIT
---

# Mock Before Wiring

Validate the idea with a disposable prototype. Cheap to throw away, cheap to redo.

<HARD-RULE>Do not touch the real codebase. The prototype lives ONLY in the
session scratchpad directory. No production files created or modified.</HARD-RULE>

## Process

1. **Pin down what's being validated.** One sentence: "This mock answers: <question>"
   (e.g. "should filtering be inline or a sidebar?"). If you can't write that
   sentence, ask the user what's undecided.
2. **Resolve a disposable location.** Prefer a harness-provided scratchpad. If
   none exists, create a temporary directory outside the repository. Never use
   an untracked directory inside the project as a substitute.
3. **Non-web target? Scope the mock's authority first.** When the product is
   native, CLI, or embedded, say up front what an HTML mock can and cannot
   answer. It CAN validate flows, layout, copy, and state transitions; it
   CANNOT validate platform feel, native gestures, assistive-technology
   behavior, or animation physics. If the undecided question is on the
   cannot list, say so and validate in the platform's own cheap medium
   instead (a throwaway SwiftUI `#Preview`, a `--dry-run` flag, a bench
   sketch) — do not fake confidence with a web approximation.
4. **Build one self-contained HTML file** in that directory:
   - Inline all CSS/JS — no external requests
   - Fake all data with hardcoded fixtures; fake all backend calls with
     setTimeout + canned responses
   - Make the undecided part interactive; keep everything else minimal
5. **Preview with the best available capability.** Render it with the Artifact
   tool when available. If this agent has no Artifact tool, provide the absolute
   file path and, when supported, open it in a local browser. Do not claim it was
   previewed when the environment cannot render or open it.
6. **Iterate.** Apply requested changes to the same file. Refresh the existing
   preview when supported; otherwise provide the unchanged file path.
7. **Exit.** When the user is satisfied, ask: "Does this match what you wanted?"
   Then extract the confirmed decisions into a short spec in conversation:

```
## Decisions validated by mock
- <decision 1>
- <decision 2>
## Explicitly rejected
- <alternative that was tried and declined>
```

The spec — not the prototype code — is the input to real implementation.
Never copy prototype code into the codebase.
