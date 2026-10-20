# Agents

<!-- directory-responsibility -->
Defines specialized assistant roles for implementation, review, documentation, research, and related development work.

Key files: `agents-md.agent.md`, `alpha-vantage.agent.md`, `chrome-devtools.agent.md`, `documentation.agent.md`, `implement.agent.md`, `lint.agent.md`, `mermaid.agent.md`, `next.agent.md`, `plan.agent.md`, `playwright.agent.md`.

```mermaid
flowchart LR
    A["Requested development role"] --> B["Select agent instructions"]
    B --> C["Role-specific execution guidance"]
```

Git tracking defaults to exclusion. Each tracked directory owns a `.gitignore` that explicitly allows its important immediate files and child directories. Add an allowlist entry when introducing content intended for version control, and give each new child directory its own `.gitignore`. This repository applies the workspace policy independently; its root rules cover root entries only. Existing responsibilities and the diagram remain unchanged.
