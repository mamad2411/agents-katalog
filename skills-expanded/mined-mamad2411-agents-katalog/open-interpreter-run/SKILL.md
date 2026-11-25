---
name: open-interpreter-run
description: Execute code via natural language with Open Interpreter
version: 1.0.0
tags: [ai, code-execution, llm, automation]
---

# Open Interpreter – LLM Code Execution

Open Interpreter lets LLMs run code (Python, JS, Shell, etc.) locally.
Users interact via natural language and the agent executes appropriate code.

- **GitHub**: github.com/OpenInterpreter/open-interpreter (60 000+ ⭐)
- **License**: AGPL-3.0
- **Security**: Sandboxed local execution with user approval. No malware.

## Environment Variables

| Variable | Description |
|---|---|
| `{{INTERPRETER_URL}}` | Base URL of the Open Interpreter server |

## Usage Examples

### Send a natural language command

```bash
curl -s -X POST "{{INTERPRETER_URL}}/run" \
  -H "Content-Type: application/json" \
  -d '{"message": "List all Python files in the current directory"}'
```

## AI Agent Tips

- Always run in sandboxed/container mode for safety.
- Supports Python, JavaScript, Bash, and more.
- Requires user confirmation before executing potentially destructive code.
- Ideal for data analysis, file operations, and system automation tasks.
