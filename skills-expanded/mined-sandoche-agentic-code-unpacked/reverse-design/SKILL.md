---
name: reverse-design
description: Reconstruct source-backed architecture, behavior, and design documents for a PR, branch, codebase, or selected code.
metadata:
  version: "0.3.0"
---

# Reverse Design

Turn code into useful architecture and review documents, distinguishing observed behavior from inferred intent and proposed changes.

## Use

```text
/reverse-design pr https://github.com/owner/repo/pull/123 --draft
/reverse-design branch feature/login --base main
/reverse-design docs auth --files src/auth.ts
```

Accept natural language and the harness's native invocation syntax. Interpret PR URLs as `pr`, named branches as `branch`, selected files or pasted code as a named `docs` target, and the whole current repository as `codebase`.

## Generate

1. Read the bundled [source and delivery guide](runtime/guide.md), then capture the target using this installed skill's runtime. Resolve script paths from the skill folder.
2. Follow [the design workflow](references/workflow.md) and [content schema](references/content.schema.json). Select document families that answer useful questions about the actual source; no family is mandatory.
3. Render and inspect the offline documents and diagrams. Return artifact paths, the key findings, and any source or capability limitations.

Dependencies and Chromium are set up automatically when needed. The agent handles scripts and content JSON. Use available tools and direct source when graph tools are unavailable. PR comments require requested live delivery; `--draft` always stays local.
