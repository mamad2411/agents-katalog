---
name: code-unpacked
description: Generate all five Code Unpacked formats for a PR, branch, codebase, or selected code. Use when a complete bundle or all formats are requested.
metadata:
  version: "0.3.0"
---

# Code Unpacked

Produce a walkthrough, reverse-design documents, code map, review quiz, and comics from one source snapshot and one shared analysis. Run the workflow in the current agent; no other installed skills or parallel agents are required.

## Use

```text
/code-unpacked pr https://github.com/owner/repo/pull/123 --draft
/code-unpacked branch feature/login --base main
/code-unpacked codebase
/code-unpacked docs auth --files src/auth.ts:10-90,src/session.ts
```

Accept natural-language requests and the harness's native invocation syntax. Interpret PR URLs as `pr`, named branches as `branch`, selected files or pasted code as named `docs`, and the whole current repository as `codebase`. Honor requested quiz length and comic counts/panels. Video is an optional addition only when requested; the normal walkthrough is HTML.

## Capture and analyze once

Read the bundled [source and delivery guide](runtime/guide.md) and [shared analysis guide](runtime/references/analysis.md). Resolve `<core>` to this installed skill's `runtime` directory. Capture the target once with its collector, inspect the source, author the shared review analysis, and validate/save it through `analyze`. Reuse an existing capture and analysis only when they match the requested source revision and scope.

Use the same saved `context.json`, evidence IDs, and analysis for every presentation. Do not repeat collection or analysis when reading the individual workflows below. If shared source capture or analysis cannot be validated, stop and explain the cause. Dependencies and browsers are set up automatically when needed.

## Generate all five formats

The following workflows and renderers are bundled here. For each workflow, `<skill-dir>` means this installed skill's `presentations/<name>` directory, and `<core>` remains the shared `runtime` directory. These instructions override workflow references to capturing source again or looking for sibling skills.

| Format | Authoring workflow |
| --- | --- |
| Walkthrough | [Chapters, source excerpts, and optional video](presentations/walkthrough/references/workflow.md) |
| Reverse-design | [Relevant design documents and diagrams](presentations/reverse-design/references/workflow.md) |
| Code-map | [Files, functions, relationships, and flows](presentations/code-map/references/workflow.md) |
| Review-quiz | [Questions, answers, and recommendations](presentations/review-quiz/references/workflow.md) |
| Xkcd | [Storyboards, generated artwork, and transcript](presentations/xkcd/references/workflow.md) |

Read each workflow as you reach that format, author its content against the shared analysis, and run its existing renderer with the same `--context` and target `--root`. Render in the order above. Keep content JSON and artifact generation internal; the user should not need to run scripts or prepare inputs.

For comics, use an available image-generation tool and inspect the complete artwork. Initial rendering without artwork saves prompts and returns an incomplete result; this is an expected preparation step. If image generation is unavailable, preserve those prompts and the storyboard and report comics as incomplete. Continue producing all other formats.

Catch failures per format, preserve completed outputs, and continue with the remaining formats. If requested video cannot be exported, retain the HTML walkthrough and report the video failure separately. Do not label a previous run's artifact as a current success: check the renderer result and its manifest against this run's shared context.

## Return and deliver

Return one concise list of the five results with usable artifact links and statuses: complete, partial, incomplete, or failed. Explain missing capabilities briefly. Outputs retain their existing `.code-unpacked/<scope>/<format>/` locations and per-format manifests; do not create a new artifact schema or claim incomplete comics are complete.

For PRs, prepare each format's existing draft comment and attachment workflow. Post only when the user requested live delivery, and only post complete, publishable outputs. `--draft` always stays local. Missing GitHub or browser-upload access preserves local results and is reported separately from generation status.
