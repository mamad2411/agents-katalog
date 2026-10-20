# Schema Instructions

Use this specification to define agent schemas.

## Format

Use a single `<schema>` node that lists all session files:

```xml
<schema>
- Session ID: ${sessionId}
- Prompt: (.copilot/sessions/${sessionId}/prompt.md)
- Artifact: (.copilot/sessions/${sessionId}/artifact.md)
</schema>
```

## Position

Place the schema immediately after YAML frontmatter (lines 6+):

```chatagent
---
name: AgentName
---

<schema>
- Session ID: ${sessionId}
- Prompt: (.copilot/sessions/${sessionId}/prompt.md)
- Artifact: (.copilot/sessions/${sessionId}/artifact.md)
</schema>

<meta_prompt>
...
</meta_prompt>
```

## Session ID

Generate `sessionId` in the format `YYYYMMDDHHMMSS`. Record the prompt before any work begins.

## Validation

- Verify all required files exist before executing.
- Confirm output files match the schema paths and formats.
- Adhere to the schema in the Constraints section.
