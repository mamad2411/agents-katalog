---
name: github-issue
description: "Creates and maintains scoped GitHub issues with local labels and relationships. Use for bugs, ideas, decisions, implementation work or epics."
---

# GitHub issues

Read AGENTS.md and the repository's contributing docs.
Resolve repo identity and domain terms before writing. An explicit request to
create or update an issue authorizes that requested action; a review request
produces recommendations.

1. Search open and closed issues and related PRs. Paginate every collection
   used to claim complete coverage, including comments and relationships.
   Record unavailable scope rather than treating it as empty.
2. Classify the request as an idea, decision, bug, implementation or maintenance
   item. Use [the templates](references/templates.md). Keep implementation
   plans proportional to code actually inspected. An early idea needs its
   problem and decision owner, not invented classes and file changes.
3. Fetch the complete live label list. Apply only existing locally mapped
   labels. Preserve repository language, domain vocabulary and ADR decisions.
4. Prepare the exact body and intended native parent/blocking relations. When
   only assessment is requested, present the proposal before any mutation.
   For authorized changes, refresh affected items and preserve remaining work.
5. Submit using a body file. Add only authorized relationships after the item
   exists, then read back its body, labels and native relationships. Return the
   real issue link and any partial failure.

Use triage or backlog-grooming when selected for request verification or a wider
review. Those skills do not grant extra write authority. Keep project views,
fields and board configuration outside ordinary issue authoring.
