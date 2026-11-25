---
name: no-ai-attribution
description: Keep AI-assistant credit lines out of anything published on the user's behalf. Use before writing a commit message, pull request, issue, comment, review reply, ticket, wiki page or chat message.
---

# No AI attribution

The user signs what they publish. Text written for them reads as theirs, with no line crediting an AI assistant or tool.

## Leave out

- Footers such as "Generated with …", "Written with …" or a robot emoji followed by a tool name, with or without a `---` rule above them.
- Links to an assistant session.
- Commit trailers that name an assistant or its vendor, for example `Co-Authored-By: <assistant> <noreply@…>`. GitHub shows every `Co-Authored-By` trailer as a co-author on the commit, and squash merges carry it into the PR.
- An assistant listed as an author, co-author, reviewer or watcher anywhere.

Co-author trailers for real people the user paired with are fine. Add them when the user asks.

## How to apply it

1. Before any tool call that creates or edits published text, re-read the text and delete any attribution line. A commit message ends with its own last line of content; a PR description ends with the last section of the repository's template.
2. Check the result after posting. Some tools append a footer on their own; edit it out.
3. If something already posted carries a footer and you cannot edit it, tell the user exactly where it is.
