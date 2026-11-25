---
name: release-notes
description: Turn a list of changes into release notes a user reads in under a minute
metadata:
  title: Release notes
  version: "1"
  author: Bloks
  tags: launch, writing, engineering
---

Use this when there is a changelog, a list of merged changes or a diff, and someone needs notes for the people who use the product.

1. Read every change and keep only what a user would notice: something new, something that works differently, something fixed that they may have hit.
2. Drop internal work entirely (refactors, test changes, dependency bumps) unless it changes what a user sees, such as speed.
3. Write each kept change as one bullet that starts with a bold lead of two to five words, then one or two plain sentences on what it means for them. Say what they can now do, not what the code does.
4. Order by how many people it touches, biggest first. Put anything that needs action from the user (a setting to change, something removed) at the top, said plainly.
5. Check every name, number and setting against the source. Never describe a change you could not find evidence for.

Not for: an internal changelog for engineers, or a single fix someone asked about. Explain that fix directly.
Return: a title with the version and date, then the bullets. Under 250 words unless asked.
Approval: required before the notes are published or sent anywhere.
