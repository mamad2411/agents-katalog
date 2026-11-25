---
name: walkthrough
description: Create a source-linked HTML code tour for a PR, branch, codebase, or selected code; optionally export a silent video with captions.
metadata:
  version: "0.3.0"
---

# Walkthrough

Explain purpose, before/after behavior, review priorities, and relevant source through an offline code tour. Use chapters for meaningful deep dives.

## Use

```text
/walkthrough pr https://github.com/owner/repo/pull/123 --draft
/walkthrough branch feature/login --base main
/walkthrough video codebase
```

Accept natural-language requests too. Interpret a PR URL as `pr`, named branches as `branch`, selected files or pasted code as a named `docs` target, and the whole current repository as `codebase`. Honor the harness's native invocation syntax.

## Generate

1. Read the bundled [source and delivery guide](runtime/guide.md), then capture the target through this skill's runtime. Resolve paths from this installed skill folder, independently of the current working directory.
2. Follow [the walkthrough workflow](references/workflow.md) and [content schema](references/content.schema.json). Read source before authoring explanations; preserve evidence, source limitations, and existing artifact behavior.
3. Generate and inspect the HTML. For video requests, reuse the same content and export the silent MP4 plus captions. Return usable artifact paths and a short explanation of any missing capabilities.

Dependencies and Chromium are set up automatically when needed. Video requires FFmpeg. The user should not need to run renderer scripts or author JSON. Use available source and browser tools; fall back to direct source when graph tools are unavailable. PR comments require requested live delivery; `--draft` always stays local.
