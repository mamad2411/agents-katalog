---
name: review-quiz
description: Create an offline comprehension quiz with architecture diagrams, scored answers, and source-linked explanations for a PR, branch, codebase, or selected code.
metadata:
  version: "0.3.0"
---

# Review Quiz

Test understanding of architecture, actual behavior, execution flow, failure cases, and extension points. Include diagram questions when the source supports them. Default to eight meaningful questions, with fewer when evidence is insufficient.

## Use

```text
/review-quiz pr https://github.com/owner/repo/pull/123 --draft
/review-quiz docs auth --files src/auth.ts --questions 12
/review-quiz codebase
```

Accept natural language and the harness's native invocation syntax. Interpret PR URLs as `pr`, named branches as `branch`, selected files or pasted code as a named `docs` target, and the whole current repository as `codebase`.

## Generate

1. Read the bundled [source and delivery guide](runtime/guide.md), then capture the target using this installed skill's runtime. Resolve script paths from the skill folder.
2. Follow [the quiz workflow](references/workflow.md) and [content schema](references/content.schema.json). Ground answers and recommendations in source evidence. Honor the requested question count without inventing trivia.
3. Render and inspect the offline quiz, including scoring, explanations, and reset. Return the HTML path and any evidence shortfall.

Dependencies are set up automatically. The agent handles scripts and content JSON. Use available tools and direct source when graph tools are unavailable. PR comments require requested live delivery; `--draft` always stays local.
