---
name: docsgpt-ask
description: "Ask questions about documents using DocsGPT at {{DOCSGPT_HOST}}:{{DOCSGPT_PORT}}."
metadata:
  openclaw:
    emoji: "📖"
---

# DocsGPT Ask

DocsGPT is available at `http://{{DOCSGPT_HOST}}:{{DOCSGPT_PORT}}` within the Docker network.

## Ask a Question

```bash
curl -X POST "http://{{DOCSGPT_HOST}}:{{DOCSGPT_PORT}}/api/answer" \
  -H "Content-Type: application/json" \
  -d '{"question": "How do I configure the service?", "history": []}'
```

## Tips for AI Agents

- Upload documentation to create a knowledge base for Q&A.
- Pass conversation history for context-aware follow-up questions.
- Supports multiple document formats: PDF, Markdown, RST, etc.
