---
name: membase-wiki
description: Store and retrieve factual documents, references, and stable project knowledge in Membase wiki.
---

# Membase Wiki

Use wiki for factual knowledge that should behave like documentation:

- project architecture notes
- onboarding docs
- external references
- stable technical specifications
- handoff documents

Use `search_wiki` for retrieval and `add_wiki` / `update_wiki` for document
management. When adding or updating wiki content, preserve the full artifact
body unless the user explicitly asks to save a summary. If the user names a
Project, pass it as `project`; new Projects are created automatically. A
Project is the Wiki filing location and is separate from the document title.
Leave `project` empty when the user does not name one. After add/update, report
the returned destination, such as `Saved to Project: X`, `Saved to Basic`, or
`Moved to Basic`.

Use `delete_wiki` only after explicit user confirmation, and pass
`confirm: true`. Use memory, not wiki, for user preferences, habits, or
personal context.
