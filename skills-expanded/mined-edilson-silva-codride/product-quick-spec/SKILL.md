---
name: product-quick-spec
description: Create a fully-specced GitHub issue directly from a task description
---

Use this when the task is small/well-understood enough to skip `product-collect` → `product-refine` → `product-spec`'s staged process. For anything bigger, or with real ambiguity about the problem itself, use that staged pipeline instead so requirements get properly decomposed and validated one step at a time.

You're acting as an AI assistant tasked with creating new issues in our project management tool (GitHub Issues). Your job is to understand the task requirements, review the project's documentation, and create a well-organized issue. Follow these instructions carefully:

First, review the project's current documentation — usually the `README.md` and the markdown files under `docs/`.

The user's request should contain a description of the task to spec out. If it's missing or too thin, ask for it rather than guessing.

Your goal is to create a comprehensive issue based on this description:

1. **Understand the task**:
   - Read the task description carefully.
   - In your internal reasoning, formulate questions to clarify any ambiguity or missing information.
   - Consider how the task fits into the project's existing organization, based on the documentation you reviewed.

2. **Confirm and clarify**:
   - Before creating the issue, confirm your understanding of the task.
   - If you need more information, say what additional detail would help.

3. **Create the issue** with `gh issue create`, including:
   a. A clear functional description
   b. A detailed technical architecture and execution plan
   c. Suggested libraries (prioritizing ones already used in the project)
   d. Affected components
   e. Acceptance criteria, numbered `FR-01`, `FR-02`, ... as `Given/When/Then` scenarios (same format as `product-spec`) — this is what `engineer-work` implements test-first against and `engineer-coverage` checks for gaps
   f. Points of attention for validation/testing

4. **Break the task down**: if it's complex, consider creating a parent issue and child issues (linked via "Part of #<parent>") to reduce complexity. Before doing this, state your intention and briefly explain why.

5. **Label it**: add one of `bug`, `enhancement`, `improvement`, or `research`, whichever is relevant.

6. **Present your final plan to the user and ask for confirmation before creating the issue(s).**

7. **Save `docs/business-context/features/<slug>.md`** — same format `product-spec` produces (title, `**Status**: Planned`, `**Priority**`, `**Scope**`, `**Module**` if applicable, then each `FR-XX` with its description and acceptance criteria). This is what makes the feature visible to `product-sync-github`; skip it only if this task is too small to be worth tracking as a feature (e.g. a one-line fix) rather than a full issue.
