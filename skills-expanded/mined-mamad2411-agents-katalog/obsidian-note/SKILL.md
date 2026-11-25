---
name: obsidian-note
description: >
  Turn the results and conclusions of the current work or conversation into a concise Markdown note for future reference.
disable-model-invocation: true
---

# Note

The note is for future me, not a transcript or summary of the conversation.

- Capture conclusions, decisions, useful facts, commands, examples, and lessons learned.
- Preserve technical terminology in English when it is more precise or commonly used.
- Remove conversational noise, repetition, abandoned intermediate ideas, and reasoning that is no longer useful.
- Include rejected ideas and describe why we reject it.
- Prefer concise sections and bullet points.
- Use code blocks for commands, configuration, and code.
- Include references and provide links if possible.
- Use Mermaid instead of ASCII diagrams when a diagram is useful.
- Do not explain obvious background knowledge.
- Do not refer to "our conversation", "the user", or "the assistant".
- Write as accumulated personal knowledge, not as a report.
- Write in Russian unless I explicitly ask otherwise.
- Do not write things about repository specifics like github or licensing unless entire topic of the research about it.

# Output

Return the entire note directly in chat as a single copyable Markdown block. Do not create or modify files.

Do not add commentary before or after the note.

# Formatting

- Do not artificially wrap long lines.
- Follow normal Markdown conventions and preserve meaningful blank lines.
- Choose headings based on the actual content instead of forcing a fixed document structure.

Start every note with this frontmatter:

```yaml
---
topic: "<few-word description>"
date: "<DD.MM.YYYY HH:mm>"
tags:
  - <Tag>
  - <Tag>
---
```

- Use the current local date and time for date.
- Keep topic short and descriptive.
- Add only useful tags that describe the main subjects of the note.
- Keep tag naming consistent within the note.


## Tags

Use consistent PascalCase tags.

- Write tags in `PascalCase`: `Kotlin`, `JetpackCompose`, `Gentoo`, `Linux`.
- Prefer established technical names when they already fit: `SwiftUI`, `OpenGL`, `GitHub`.
- Prefer broad reusable concepts over overly specific one-off tags.
- Keep the number of tags relatively small. Add only tags useful for finding or grouping the note later.
