---
name: research
description: Investigate a question against primary sources and capture the findings as one cited Markdown note. Use when the user wants a topic researched, a vendor's docs or API facts gathered, a library's or tool's real behavior confirmed, or reading legwork delegated while the main session keeps working.
---

# Research

Reading is cheap to delegate and expensive to get wrong. This skill keeps it cited and keeps
it out of the main conversation. Credit and license: `LICENSE.md` in this folder.

## Who reads

If the agent can start a background subagent, hand the reading to one and keep working. In
Claude Code that is the `researcher` agent, which runs on Sonnet in the background. Otherwise do the reading yourself, following the same brief.

## The brief

1. **Primary sources only**: official docs, source code, specifications, first-party API
   responses, release notes. Not a blog post or forum answer *about* them. Follow every
   claim back to the source that owns it.
2. **One Markdown file** in the session's scratch directory, named for the question. Each
   claim carries its source: a URL and the date it was read. Version-specific facts name
   the version.
3. **Say what could not be verified**, in its own section. An unverified claim is labeled,
   never smoothed into the prose.
4. **Report back** the file's path and a summary of five lines or fewer, not the file's
   contents.

## After the note exists

The main session decides where the note goes: it stays in the scratch directory, becomes a
docs page in the repo, or is pasted into the ticket, PR or wiki page it answers.
Research feeds a decision, a spec or a review; it does not make the decision.
