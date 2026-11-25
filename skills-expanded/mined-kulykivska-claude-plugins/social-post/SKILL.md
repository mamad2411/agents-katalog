---
name: social-post
description: >-
  Create posts for one or several social networks from an idea or recent
  work. Trigger on "write a post", "make a post for...", "post about...",
  "write a post about...", or when the user wants to announce something
  shipped. Orchestrates the content-writer subagent with real material.
---

# Social post

## Steps

1. **Gather material**: if the topic references recent work, pull the real
   story: git log, project memory, the conversation. Real numbers and
   failures make the post; never invent them.
2. **Choose platforms**: default LinkedIn + Threads unless specified. For a
   LinkedIn post, the dedicated linkedin-post-writer skill's formula applies
   if it is available; the content-writer agent knows the same shape.
3. **Delegate**: spawn `content-writer` with the material, platforms, and
   language. For a batch (a week of posts), give it the content-ideas
   backlog and ask for a themed plan first.
4. **Review against voice rules**: no long dashes, hook survives the fold,
   numbers are real, English (or Ukrainian on request).
5. Deliver drafts ready to paste. Do NOT post anywhere yourself; publishing
   is the owner's click.
