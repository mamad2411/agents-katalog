---
name: Saving a job as a skill
description: >-
  Use after running a job cleanly by hand, when turning it into a reusable
  skill, or when reviewing an existing skill that keeps producing inconsistent
  results.
---
# Saving a job as a skill

## Before saving: run it by hand once
Run the whole job in one conversation, one step at a time. Before each step, say what you're about to do and why. When a decision comes up that nobody specified, stop and ask instead of picking the reasonable option. At the end, list every decision you had to ask about; that list is the gap to fix in the role or the skill, not in a longer prompt.

## The six parts every skill spells out
1. **When** to use it, and when not to.
2. **Inputs** it needs, and which access or connector each requires.
3. **Sequence** of steps in order, with decision points marked.
4. **Validation**: how to check each result before moving on.
5. **Output**: exact format and exact destination.
6. **Approval**: which steps stop and wait for a person.

## Rules
- Keep it generic: no specific people, channels, repos, clients, secrets, or internal URLs. Those go in the routine or request that runs it.
- Readable end to end in under a minute.
- After writing it, name its weakest part and fix that before sharing.
- If the skill is published to a shared repo, keep the library copy and the repo copy in sync.
