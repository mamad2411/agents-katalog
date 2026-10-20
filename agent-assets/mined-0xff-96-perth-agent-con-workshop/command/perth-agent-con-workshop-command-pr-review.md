---
description: Review a PR with this repo's methodology (CI gate + AI-comment triage + domain rubric) and post the verdict as a GitHub comment
argument-hint: <pr-number>
---
Review pull request **#$ARGUMENTS** in this repo using the methodology in
`docs/cloud-container-guide.md`, then post a single verdict comment on the PR.

Use the GitHub MCP tools (`mcp__github__*`) — there is no `gh` CLI here.

1. **Gate on CI.** Read the PR's check runs. If `verify` is failing, pull the job
   log, diagnose, and report the failure — do **not** post a GO verdict on a red
   build. (CI failures are often environment issues, not the diff.)
2. **Triage automated reviews.** Read the DeepSeek and Copilot review comments.
   Classify each as **actionable** (fix it, note the commit), **no-op** (dismiss
   with a one-line reason — it's wrong or contradicts a deliberate decision), or
   **defer** (out of scope). Do not blindly act on every suggestion; each push
   re-triggers the reviewers and can loop.
3. **Run the domain rubric** (CopilotKit v2 + A2UI): default array/object props,
   `/v2` subpath imports, slash model format, `dotenv/config` first in `server.ts`,
   `useSingleEndpoint={false}` + `agentId`, host-authored L4 with inlined literals,
   colocated tests for new L3 components, and no secrets/`.env` committed.
4. **Post the verdict comment** to the PR using the template in
   `docs/cloud-container-guide.md` (GO / NO-GO + CI + triage + checklist).

Be frugal: post exactly one summary comment. Don't push code changes unless I ask —
this command reviews, it doesn't fix.
