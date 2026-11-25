---
name: refactor-agents-md
description: Refactor an AGENTS.md into a wiki of linked Markdown pages. Use when the root AGENTS.md is longer than 100 lines.
---

A good AGENTS.md file should hold:
1. Information that an agent can't infer from the repo.
2. Information that can save the agent effort discovering important things about the repo. 

However, the AGENTS.md file is always loaded into the agent's context, so it should be kept as short as possible. If the AGENTS.md file is longer than 100 lines, the information it contains should be refactored into other Markdown files. Those files should be discoverable from AGENTS.md so the agent can look up important information when it needs it, following the progressive disclosure pattern.

Find and read the current repos AGENTS.md file. If the AGENTS.md file is longer than 100 lines, propose a refactor of the repo's root `AGENTS.md`, following the `wiki/` and `index.md` pattern shown below. Group Markdown pages by domain. End `AGENTS.md` with a table of contents section linking to `wiki/index.md` and the top-level pages in `wiki/`.

Give every wiki folder an `index.md` containing a table of contents that links to its own Markdown pages and its immediate child indexes.

Communicate the proposal for the refactor to the user as a file tree.

```text
AGENTS.md
wiki/
├── index.md
├── guidelines.md
└── billing/
    ├── index.md
    ├── invoicing.md
    └── refunds/
        ├── index.md
        └── eligibility.md
```

Bottom of `AGENTS.md`

```markdown
## Wiki

- [Wiki index](wiki/index.md)
- [Guidelines](wiki/guidelines.md)
```

`wiki/index.md`

```markdown
- [Guidelines](guidelines.md)
- [Billing](billing/index.md)
```

`wiki/billing/index.md`

```markdown
- [Invoicing](invoicing.md)
- [Refunds](refunds/index.md)
```

Once the proposal is approved, create `wiki/` if it is missing.
