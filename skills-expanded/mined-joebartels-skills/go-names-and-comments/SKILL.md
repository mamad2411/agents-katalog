---
name: go-names-and-comments
description: Use when writing or revising Go identifiers, comments or Godoc, especially verbose helper documentation and test prefaces. Skip changes unrelated to names or documentation.
---

# Go names and comments

Use clear names suited to their scope and conventional Go initialisms. Judge names at their use sites; preserve established public and protocol identifiers.

Godoc starts with one plain sentence naming the symbol. Add only facts callers need for correct use: restrictions, defaults, ownership, failure results and misuse warnings. Keep behavior and its limitations with the symbol; deployment policy belongs at its boundary.

Internal comments explain a non-obvious constraint beside the relevant code. In tests, put a short reason beside non-obvious setup, such as using a real handler for opaque options. Let descriptive names and assertions explain the behavior.

Cut implementation narration, design essays, test-proof arguments and hypothetical consequences. Say each fact once. Delete unnecessary prose rather than relocating it. Preserve behavior and necessary contract warnings; brevity is not a sentence quota.

```go
// ResolveRequestID returns candidate if valid, otherwise a new request ID.
// rejected is true only when a nonempty invalid candidate was replaced.
// Validity does not establish who minted the ID.
```
