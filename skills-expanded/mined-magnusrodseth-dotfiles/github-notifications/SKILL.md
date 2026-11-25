---
name: github-notifications
description: GitHub notification opt-in, opt-out, and audit. Use when choosing repository events or email delivery.
disable-model-invocation: true
---

# GitHub Notifications

Manage repository subscriptions and notification delivery as separate choices. Use `gh` for supported repository operations and Brave for Custom events or account delivery settings.

## Resolve the request

1. Identify the operation: audit, opt in, opt out, ignore, or change delivery.
2. Resolve each repository to `OWNER/REPO`. Accept a GitHub URL or use the current checkout when requested. Verify the authenticated account and repository access.
3. For opt-in, ask which events unless the request already specifies them. Offer releases, issues, pull requests, discussions, security alerts, or all activity. Inspect which events the repository supports.
4. Clarify delivery only when relevant: GitHub inbox, email, or both. Read existing settings before proposing an account-wide change.

Read [REFERENCE.md](REFERENCE.md) for the chosen branch's commands, semantics, and verification.

## Apply the chosen branch

- **Audit:** Read account delivery settings and the watching list. Use the UI for exact Custom event selections. Report the inspected scope and proposed changes; an audit authorizes reads.
- **Opt in:** Read the repository's current mode. For specific events, use Watch → Custom in Brave. Preserve existing Custom selections when adding events; use an exact replacement when the user says "only". All activity uses the REST subscription endpoint.
- **Opt out:** Return the named repo to Participating and @mentions. Explain that participation and existing thread subscriptions can still notify. Use Ignore only when the user asks to silence that repository entirely.
- **Delivery:** Use GitHub's notification settings in Brave. Explain every affected category before an account-wide change. Leave unrelated system notification categories as they are.

An explicit request to change a named repo and mode authorizes that change. Ask for missing choices, not repeat approval. Obtain a concrete choice before applying a suggested cleanup or broader delivery change. A repo email request alone does not authorize changing delivery for every repo.

## Verify and report

- Re-read every changed repo. Verify simple modes through REST; reload and inspect Custom event selections in the UI.
- Re-read every changed account delivery category. Report the account-wide effect and whether the requested repo events can reach email.
- For browser changes, save and embed a screenshot showing the result using the browser's documented screenshot workflow.
- List only completed changes and unresolved limits. Link the repos and settings with Markdown links.

## Example invocations

- `$github-notifications opt me into OWNER/REPO` prompts for events.
- `$github-notifications notify me about releases only in OWNER/REPO` sets Custom releases.
- `$github-notifications stop watching OWNER/REPO` keeps participation and @mentions.
- `$github-notifications ignore OWNER/REPO` silences its notifications.
- `$github-notifications audit my GitHub email notifications` proposes changes without applying them.
