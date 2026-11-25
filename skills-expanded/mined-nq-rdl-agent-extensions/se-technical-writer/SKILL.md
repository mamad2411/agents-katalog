---
name: se-technical-writer
description: >-
  Draft developer documentation, tutorials, ADRs, user guides, and technical
  blog posts from source material, adapting structure and depth to the audience.
  Use for new technical writing; for copyediting existing prose, use
  tech-writing:copyedit.
license: MIT
metadata:
  upstream: https://github.com/github/awesome-copilot/blob/main/agents/se-technical-writer.agent.md
  repo: https://github.com/nq-rdl/agent-extensions
---

# Author

Identify the audience and requested document type, then draft from verified source material. Apply the tech-writing:copyedit skill to documentation, tutorials, guides, and ADRs, including its mandatory STE review. Keep the blog-specific style separate and report unresolved factual gaps.

## Optional delegation

[references/subagent.rst](references/subagent.rst) contains the subagent outline,
handoff inputs, execution boundaries, and expected result. Read it when delegating
would help or the user asks to “create a subagent to execute this.” Otherwise,
work directly from this skill; the reference does not need to be loaded.
