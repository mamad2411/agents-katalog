---
name: rjv-pr-descriptions
description: "Use when writing, generating, updating, or fixing a GitHub PR description. Applies the Current-way/New-way + What-To-Test format; on update preserves checked checkboxes + author content; posts the result."
---

# PR Descriptions

## Format

One section per logical change:

```
## Change N: <Short Title>

Current way: <one sentence — what happens today>.
New way: <one sentence — what happens after this PR>.

### What To Test
- [ ] <Action verb: Create / Open / Submit / Uncheck…>
- [ ] Confirm <observable outcome>.
- [ ] <Edge case setup>
- [ ] Confirm <edge case outcome>.
```

**Rules:**
- "Current way / New way" — plain English, user-facing behavior only. No code, no implementation details.
- Test steps start with an action verb. Confirm steps start with "Confirm".
- Cover happy path + key edge cases. Not exhaustive — just the combinations that matter.
- No filler. No "Overview" or "Summary" headers. Jump straight to the changes.

## Workflow

### Writing a new description

1. Read the diff: `gh pr view <number> --json files,commits,body`
2. Identify logical changes (one section per change).
3. Write sections in the format above.
4. Post: `gh pr edit <number> --body-file -` (pipe the body in; inline `--body` breaks on multi-line/special chars).

### Updating an existing description

1. Fetch current body first: `gh pr view <number> --json body`
2. Preserve all `- [x]` checked checkboxes — never uncheck or remove them.
3. Preserve any content manually added by author/reviewer outside the generated format.
4. Merge in new changes — add new `## Change N` sections, append new test steps.
5. Only replace content you explicitly generated in a prior run.
6. Post the merged result back.

## Adding Images

To embed a screenshot or before/after image:

1. Produce the image — via your browser-automation tool (e.g.
   `agent-browser screenshot` on the running app; check the project's
   docs for local login sequences), or use an image the user provides.
2. Pass the absolute path to the `rjv-github-image-upload` skill — it
   returns a `github.com/user-attachments` URL ready to paste inline
   (private-repo images stay private).
