---
name: explain-code
description: Explains code with visual diagrams and analogies. Use when explaining how code works, teaching about a codebase, or when the user asks "how does this work?"
argument-hint: "<file-path | symbol | code-snippet>"

allowed-tools: Read, Write, Glob, Grep
---

# Explain Code

## 1. Reading the Parameters

The skill is invoked as `/explain-code <params>`. Parse `<params>` before doing anything else:

- **Target** — a file path, symbol name, or code snippet to explain.
- **Instructions** — optional free-text after the target that scopes or steers the explanation.  
  If no params are given, ask the user: _"What would you like me to explain? Please share a file path, function name, or paste the code."_

If a file path is given, read the file first. If a symbol name is given, search for it in the codebase before explaining.

---

When explaining code, always include:

1. **Start with an analogy**: Compare the code to something from everyday life
2. **Draw a Mermaid diagram**: Visualize the flow, structure, or relationships using a Mermaid code block
3. **Walk through the code**: Explain step-by-step what happens
4. **Highlight a gotcha**: What's a common mistake or misconception?

Keep explanations conversational. For complex concepts, use multiple analogies.

## 2. Save as Markdown Report

After explaining, **always write the full explanation to a file** in `./docs/explain/`.

- Filename format: `yyyy-MM-dd-<kebab-case-purpose>.md`  
  Example: `2026-04-14-oauth-proxy-flow.md`
- Use today's date from the system date
- The purpose slug should reflect what was explained (2–5 words, kebab-case)
- The file must contain everything shown in the response: analogy, diagram, walkthrough, and gotcha
- Create the `./docs/` directory if it does not exist

## 3. Mermaid Diagram Guidelines (v11)

Pick the diagram type that best fits the concept:

| Concept                           | Diagram type      |
| --------------------------------- | ----------------- |
| Data / control flow, pipelines    | `flowchart`       |
| Request/response, auth handshakes | `sequenceDiagram` |
| Class hierarchy, interfaces       | `classDiagram`    |
| State machines, lifecycle         | `stateDiagram-v2` |
| DB schema, relationships          | `erDiagram`       |

**Syntax rules (Mermaid v11):**

- Use `flowchart` (not the legacy `graph` keyword)
- Break new line: <br> instead of /n
- Use YAML frontmatter for config — **not** the deprecated `%%{init:...}%%` directive:

  ````markdown
  ```mermaid
  ---
  config:
    theme: default
  ---
  flowchart LR
    A[Start] --> B{Decision}
    B -->|Yes| C[Done]
    B -->|No| A
  ```
  ````

- Keep node labels short and free of special characters
- Prefer `LR` (left-to-right) for flows, `TD` (top-down) for hierarchies
