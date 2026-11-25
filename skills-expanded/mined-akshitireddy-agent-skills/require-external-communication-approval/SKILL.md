---
name: require-external-communication-approval
description: Check authorization before sending a direct message, review, comment, or other human-facing communication.
---

# Require External Communication Approval

## Hard rule

Never directly send, post, or reply to another person without the user's
explicit approval for that specific communication.

Require approval before:

- Posting or replying to a pull-request, review, issue, or discussion comment.
- Sending Slack, Teams, email, chat, direct messages, or similar messages.
- Submitting reviews, reactions, mentions, assignments, or reviewer requests.
- Resolving or dismissing another person's review or discussion.

Drafting text without sending it is allowed.

## Do not block operational work

When otherwise authorized by the user's task, proceed without a separate
communication confirmation for:

- Commits, pushes, merges, branch operations, and repository settings.
- Workflow triggers, reruns, cancellations, builds, tests, and deployments.
- Releases, infrastructure changes, and automatic bot-generated pull requests.
- Creating or updating pull requests that the user asked Codex to manage,
  provided Codex does not add reviewers, mentions, or follow-up comments.

Automatic service notifications caused by these operational actions do not
count as Codex directly messaging another person.

Before asking, check whether the current request or prior session instructions
already explicitly authorize this exact communication. Existing authorization
persists; ask only for missing approval or a material change to recipients,
destination, or content. Immediately before sending, verify the planned action
still matches that authorization.

## Approval workflow when authorization is missing

1. Draft the proposed communication without sending it.
2. Show the user the destination, recipients, and exact text or action.
3. Ask for explicit approval.
4. Send only the approved communication without adding wording or recipients.

Requests to fix code, manage a pull request, or perform a deployment authorize
the operational work, but do not authorize a separate human-facing reply.
