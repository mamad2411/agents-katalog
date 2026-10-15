---
name: review-as-json
description: Runs `/review` and emits the result as a single structured JSON object. Used by CI; use `/review` directly for human-facing reviews.
license: MIT
metadata:
  version: "2"
---

# Review as JSON

Run `/review` on this change and follow it exactly.

Emit the result as a single JSON object instead of a prose report:

```json
{
  "verdict": "approve | changes_needed | hold",
  "summary": "One or two sentences on the change overall.",
  "findings": [
    {
      "severity": "critical | warning | info",
      "type": "issue | suggestion | question",
      "category": "mission | architecture | implementation | craft | security | performance",
      "title": "Short imperative, e.g. 'Sanitize user input before query'",
      "description": "What it is, why it matters, and the consequence.",
      "file": "path/to/file.ts",
      "line": 42,
      "suggestedFix": "Optional concrete fix."
    }
  ],
  "passes": {
    "mission": "met | missing | different | unclear",
    "architecture": "ok | concern | blocking",
    "implementation": "ok | concern | blocking",
    "craft": "ok | concern | blocking",
    "security": "ok | concern | blocking",
    "performance": "ok | concern | blocking"
  },
  "sectionSummaries": {
    "mustFix": "1-2 sentences on the critical findings, if any.",
    "shouldFix": "1-2 sentences on the warnings, if any.",
    "questions": "1-2 sentences on the questions, if any.",
    "suggestions": "1-2 sentences on the suggestions, if any."
  }
}
```

Rules for the output:

- Emit **only** the JSON object. No preamble, no commentary, no markdown fences around it.
- **Severity.** `critical` blocks merge (bugs, security holes, data loss). `warning` should be addressed but isn't a blocker. `info` is a note.
- **Summary.** Never restate the verdict ("This PR is approved", "Changes requested") — the presentation layer renders it. The summary answers *why*.
- **sectionSummaries.** Explain the underlying theme ("Missing input validation across the new endpoints"), never just count findings.
- **Type.** `question` is something you need answered rather than a defect. `suggestion` is an optional improvement. Everything else is an `issue`.
- **Category.** Every finding's `category` is the pass that found it — this is how the passes show up in CI output.
- **Verify before you flag** still applies. Every finding needs a concrete file, line, and consequence. If you can't verify it, make it a `question`.
- If there are no findings, emit an empty `findings` array and an `approve` verdict.
