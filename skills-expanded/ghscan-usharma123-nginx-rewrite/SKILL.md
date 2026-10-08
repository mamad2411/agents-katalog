---
name: explain-code
description: Explains code clearly. Use when explaining how code works, teaching about a codebase, or when the user asks "how does this work?"
---
When explaining code:
1. Summarize what the named unit does.
2. Walk through its key path.
3. Flag surprising behavior.

Ground rules:
- **Stay scoped.** Cover the named unit, immediate callers/callees, return value, and touched state. Do not sweep a whole file unless asked.
- **Cite claims.** Give the path and symbol, and quote the relevant fragment.
- **Flag uncertainty.** Never fill gaps with plausible invention.

Keep explanations clear and concise.
