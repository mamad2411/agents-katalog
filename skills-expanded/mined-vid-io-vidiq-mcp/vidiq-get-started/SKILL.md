---
name: vidiq-get-started
description: Set up, verify, or troubleshoot vidIQ MCP and pick a first workflow. Use when asked to connect vidIQ, a YouTube channel, or a social account, 'is vidIQ connected', 'which channel is linked', 'which account is linked', 'check my credits', or when vidIQ tools are missing, a call returns 401, 403, or verification errors, credits run out, or a thumbnail, watch, or script job is stuck. Not for creator research.
---

# vidIQ Get Started

Read [Live surface notes](references/live-surface-notes.md) first, even when using only supplied evidence.

Help the creator connect, diagnose a problem, or choose a workflow. Run only the relevant branch:

- Connection, channel, or balance checks: use the relevant steps below.
- Social account listing or connection: start with `vidiq_social_account_list`. For a requested
  connection, use `vidiq_social_account_connect`, show its authorization link or widget, wait for
  completion, then re-list accounts. A platform in `partial` has unknown connection state.
  Complete only the requested connection work; connecting does not publish anything.
- Errors or charge questions: read [Troubleshooting](references/troubleshooting.md).
- Existing or interrupted jobs: read [Job recovery](references/job-recovery.md). To list active
  jobs, use `vidiq_jobs_list` with `status: "inprogress"`.
- No YouTube channel connected, or a write tool asks for verification: use steps 3 and 6 below.
- Saved research: `vidiq_bookmarks_list` returns the creator's saved videos, channels, and
  keywords when they ask what they bookmarked.
- Capabilities: summarize the outcomes supported by the exposed tools.

## Connect and verify

1. Inspect whether vidIQ tools are visible. Visibility confirms that the client loaded the
   server; successful account-state calls establish authorization.
2. If tools are missing, check installation, enablement, and client reload requirements.
   Use the client's native MCP authentication action when available; otherwise follow its
   connection flow and the [official setup guide](https://support.vidiq.com/en/articles/15082430-vidiq-mcp).
   Wait for browser authorization, then re-check. Never request credentials in chat.
3. Call `vidiq_user_channels` once and report the returned authorized IDs.
   Account labels are optional and useful only for diagnosis.
   An empty or unexpected list can indicate the wrong account; suggest reconnecting with the
   intended account without claiming token expiry. When no channel is connected, or another
   tool reports that no YouTube channel is connected, call `vidiq_connect_youtube_channel`, show
   its widget, wait for the creator to finish, then retry the original request. The connection
   and authorization tools are free and are not exposed by the Claude.ai directory connector.
4. Resolve the intended channel only before channel-specific work. If several IDs are returned,
   use the user's explicit selection; do not pick the first or largest. Enrich titles with
   `vidiq_get_channels_by_ids` only when needed. A channel outside the authorized
   set can receive public research, but not private analytics.
5. Use `vidiq_balance` to explain returned renewable and
   add-on credits, preserving `unlimited` and `null`.
6. Before a write workflow (video details or thumbnail) or when a tool returns
   `status: verification_required`, call `vidiq_authorize_with_youtube`, show its widget, and wait
   for the creator to use it. Do not repeat the write until they confirm verification is complete.

## Choose the next step

After setup, use the creator's stated decision. If it is unclear, ask one compact question and offer:

- **Package an existing idea or video:** `vidiq-packaging-studio`.
- **Discover an idea:** `vidiq-video-ideas`; feed its concept cards into packaging for an
  end-to-end request.
- **Review performance:** `vidiq-channel-audit`, or `vidiq-new-upload-review` for a recent upload.
- **Change something on YouTube:** `vidiq-video-metadata` for a video's details or thumbnail.
- **Prepare or publish social posts:** `vidiq-publishing`, also for saved drafts and delivery.

Honor a more specific request with its matching skill; ask what vidIQ can do and the answer is
the routing table in the agent guide. Supplied-context analysis or text drafting
may need no MCP calls. Do not run research merely to demonstrate the connection.
Onboarding alone does not authorize later generation or state changes.

## Report

Report the requested check's result, any issue, and the next action. For setup, include connection
and authorization state, relevant channels and credits, and one recommended workflow. For job
recovery, report the actual job state and result or pending ID.
