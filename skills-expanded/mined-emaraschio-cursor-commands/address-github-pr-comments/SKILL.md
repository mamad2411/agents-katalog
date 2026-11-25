---
name: address-github-pr-comments
description: Address review comments on the current GitHub PR
user-invocable: false
---
## Overview

Process outstanding reviewer feedback, apply required fixes, and draft clear
responses for each GitHub pull-request comment.

## Steps

1. **Sync and audit comments**
    - Pull the latest branch changes
    - Open the PR conversation view and read every unresolved comment
    - Group comments by affected files or themes
2. **Plan resolutions**
    - List the requested code edits for each thread
    - Identify clarifications or additional context you must provide
    - Note any dependencies or blockers before implementing changes
3. **Implement fixes**
    - Apply targeted updates addressing one comment thread at a time
    - Run relevant tests or linters after impactful changes
    - Stage changes with commits that reference the addressed feedback
4. **Draft responses**
    - Summarize the action taken or reasoning provided for each comment
    - Link to commits or lines when clarification helps reviewers verify
    - Highlight any remaining questions or follow-up needs

## Response Checklist

- [ ] All reviewer comments acknowledged
- [ ] Required code changes implemented and tested
- [ ] Clarifying explanations prepared for nuanced threads
- [ ] Follow-up items documented or escalated
- [ ] PR status updated for reviewers

## Guardrails

- Push only when the user asks; do not push review fixes unrequested.
- Do not dismiss valid security feedback; address it or justify with evidence first.
- Address one comment thread at a time and run tests after impactful changes.
- Do not commit, push, merge, or run production scripts without consent; wait for an explicit request before any destructive git action.
- Do not print, log, or commit secrets or credentials; flag any exposed secret instead of including it in a commit or comment.