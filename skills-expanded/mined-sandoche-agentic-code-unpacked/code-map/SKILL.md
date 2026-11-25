---
name: code-map
description: Build an interactive source-backed map of files, functions, call relationships, and flows for a PR, branch, codebase, or selected code.
metadata:
  version: "0.3.0"
---

# Code Map

Create an offline canvas for exploring files, functions, relationships, behavioral topics, and review flows.

## Use

```text
/code-map codebase
/code-map pr https://github.com/owner/repo/pull/123 --draft
/code-map docs auth --files src/auth.ts,src/session.ts
```

Accept natural language and the harness's native invocation syntax. Interpret PR URLs as `pr`, named branches as `branch`, selected files or pasted code as a named `docs` target, and the whole current repository as `codebase`.

## Generate

1. Read the bundled [source and delivery guide](runtime/guide.md), then capture the target using this installed skill's runtime. Resolve script paths from the skill folder.
2. Follow [the map workflow](references/workflow.md) and [content schema](references/content.schema.json). Use verified relationships; a directory relationship does not establish a call. Read direct source when graph tools are missing or incomplete.
3. Render and inspect navigation, function drill-down, and source links. Return the offline HTML path and a concise account of coverage limitations.

Dependencies are set up automatically. The agent handles scripts and content JSON. PR comments require requested live delivery; `--draft` always stays local.
