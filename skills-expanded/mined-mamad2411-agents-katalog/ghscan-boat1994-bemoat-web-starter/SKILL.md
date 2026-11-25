# Select UI Skill Prompt

Use this before implementing or polishing UI.

```text
You are working in a Bemoat web project.

Inputs:
- Issue or task:
- Relevant repo:
- Design brief / CMS notes / reference pack:
- Target files or screen:
- Known constraints:

Required guardrails:
1. Read the current issue and acceptance criteria first.
2. Read docs/ai/ui-skills.md.
3. Run `npx ui-skills start` when network and tooling are available.
4. Select the smallest useful UI Skills. Do not load every skill by default.
5. If the CLI is unavailable, choose fallback guidance from docs/ai/ui-skills.md.
6. Do not use project-specific references unless they are provided by the current issue, project repo, or Design Ref CMS.

Output exactly:
## Selected guidance
- UI Skills or fallback docs:
- Why these are the smallest useful choices:

## Files to inspect
- List exact repo paths and why each path matters.

## Out of scope
- List scope boundaries that should not be changed.

## Implementation plan outline
- List ordered implementation steps before editing.

## Visual QA plan
- List screen sizes, states, and visual risks to check.

## Accessibility plan
- List keyboard, semantic, focus, and contrast checks to run.
```
