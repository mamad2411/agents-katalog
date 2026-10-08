# codex_task

Delegate a task to OpenAI Codex CLI for autonomous code generation and development workflows.

## Input Schema

```json
{
  "type": "object",
  "properties": {
    "task": {
      "type": "string",
      "description": "The task description to send to Codex"
    },
    "workdir": {
      "type": "string",
      "description": "Working directory for Codex to operate in"
    },
    "model": {
      "type": "string",
      "description": "Specific model to use (e.g., \"o4-mini\")"
    }
  },
  "required": ["task"]
}
```

## Usage Hints

- Use this to delegate coding tasks like API creation, test writing, and debugging
- Set `workdir` to the project root so Codex has the right context
- The task runs with a 5-minute timeout
- Codex runs in quiet mode (-q) for non-interactive execution
