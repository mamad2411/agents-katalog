# GitHub Mention Responder Workflow

This workflow turns trusted GitHub issue-comment mention signals into one
bounded GitHub thread response.

- Consume only the shared inbound-signals routing payload and its nested
  `signal` action form. Raw `inbound.signal.received` is not a responder
  trigger because the dispatcher owns source eligibility.
- Keep actor-integrity, action, malformed-payload, and implementation-request
  gating in code before the response agent runs.
- Keep the agent passive and response-only. GitHub posting happens through the
  `github_comment` tool after the existing workflow approval step.
- Prepared intake comments enter through the post-integration intake event and
  skip the response agent while retaining the same approval and posting rail.
- Implementation requests are intake-owned. This workflow should skip them so
  `github-mention-intake` can create or reject the repo-local work item.
- Do not turn this into a multi-turn GitHub channel. If session routing becomes
  necessary, add a channel as the public surface.
