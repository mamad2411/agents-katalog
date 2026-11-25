---
name: xkcd
description: Explain source behavior through original stick-figure comics for a PR, branch, codebase, or selected code; requires an image-generation tool.
metadata:
  version: "0.3.0"
---

# Code Comics

Explain meaningful behavior, tricky invariants, and call chains through original black-and-white stick-figure comics with source references and an accessible transcript.

## Use

```text
/xkcd pr https://github.com/owner/repo/pull/123 --draft
/xkcd docs billing --files src/billing.ts
/xkcd branch feature/login --count 2 --panels 3
```

Accept natural language and the harness's native invocation syntax. Interpret PR URLs as `pr`, named branches as `branch`, selected files or pasted code as a named `docs` target, and the whole current repository as `codebase`.

## Generate

1. Read the bundled [source and delivery guide](runtime/guide.md), then capture the target using this installed skill's runtime. Resolve script paths from the skill folder.
2. Follow [the comic workflow](references/workflow.md) and [storyboard schema](references/storyboard.schema.json). Choose distinct topics grounded in actual source behavior.
3. Use an available image-generation tool to generate each complete comic, including its dialogue and labels. Inspect the artwork, render the offline gallery and PNG exports, and return usable artifact paths.

No particular image provider is required. If image generation is unavailable, preserve the storyboard and prompts and report the result as incomplete; do not claim a complete comic. Dependencies and Chromium are set up when needed. The agent handles scripts and JSON. Use direct source when graph tools are unavailable. PR comments require requested live delivery; never publish incomplete artwork, and honor `--draft`.
