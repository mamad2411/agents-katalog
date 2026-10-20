---
name: go-names-and-comments
description: Use when writing or revising Go identifiers, comments or Godoc, especially verbose helper documentation and test prefaces. Skip changes unrelated to names or documentation.
---

# Go names and comments

Use clear names suited to their scope and conventional Go initialisms. Judge names at their use sites; preserve established public and protocol identifiers.

Godoc starts with one plain sentence naming the symbol. Add only restrictions, defaults, ownership or failure facts callers need for correct use. Keep each fact with its owner: helper behavior here, grammar on the validator, deployment and trust policy at their boundary.

Internal comments explain a non-obvious constraint beside the relevant code. Descriptive test names and assertions usually need no header prose; comment only unusual fixture choices.

Cut implementation narration, design essays, test-proof arguments and hypothetical consequences. Say each fact once. Delete unnecessary prose rather than relocating it. Preserve behavior and necessary contract warnings; brevity is not a sentence quota.

```go
// ResolveRequestID returns candidate if valid, otherwise a new request ID.
// rejected is true only when a nonempty invalid candidate was replaced.
```
