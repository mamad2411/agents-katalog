---
name: repo-hygiene
description: Cleans up a code repository's labels, stale branches and issue templates.
---
# Repo hygiene

A monthly tidy for a small team's private code repository.

Steps:
1. Merge duplicate issue labels and give each a short description.
2. List branches with no commits in 90 days and delete the ones already merged.
3. Add bug-report and feature-request issue templates if they are missing.
4. Never add webhooks, integrations or deploy keys.
5. Show a short before-and-after table of labels, branches and templates.
