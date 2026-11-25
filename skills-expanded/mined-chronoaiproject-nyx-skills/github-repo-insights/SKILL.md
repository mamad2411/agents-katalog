---
name: github-repo-insights
version: "1.0"
description: On-demand GitHub intelligence for any repo the team's credential can see — weekly activity digest, issue and PR triage table, milestone progress, release-notes draft, and "what changed since X" answers, fetched live through NyxID-brokered GitHub access and delivered in chat. Complements deadline-monitor (deadline risk) and github-candidate-sourcing (hiring).
metadata:
  category: plain
  tag:
    - aevatar
    - s-capability
    - github
    - repo-insights
    - digest
    - triage
---

# GitHub Repo Insights

Use this for ad-hoc repo questions in chat: "这周 aevatar 仓库有什么进展 / 列一下没人认领的 open
issues / milestone 22 还剩什么 / 给上个 tag 到现在写个 release notes 草稿 / PR 积压情况".

**You (the agent) fetch live data yourself** via NyxID-brokered GitHub access: `nyxid_proxy`
`{slug:"api-github", path:"/repos/{owner}/{repo}/...", method:"GET"}`. Read-only by default.
Never invent numbers, titles, or states — every line traces to a fetched record.

## How to run it

1. **Resolve the repo.** From the user's text (`owner/repo`) or this chat's recent context. If
   ambiguous, ask once. Resolve the time window ("这周/自上个 release") to concrete dates.

2. **Fetch only what the question needs** (paginate `per_page=100`, cap ~3 pages per list, say so
   when truncated):
   - Activity digest → `GET /repos/{o}/{r}/issues?state=all&since={iso}` (PRs included, filter by
     `pull_request` key) + `GET /repos/{o}/{r}/commits?since={iso}`.
   - Triage → `GET /repos/{o}/{r}/issues?state=open&sort=updated` — bucket by: unassigned, stale
     (no update 14d+), needs-review PRs (`GET /repos/{o}/{r}/pulls?state=open` + requested
     reviewers), recently hot (most comments).
   - Milestone → `GET /repos/{o}/{r}/milestones` then issues filtered by `milestone=N&state=all`;
     report open vs closed with the open items listed.
   - Release notes draft → `GET /repos/{o}/{r}/releases/latest` (or a user-named tag) then commits
     / merged PRs since it; group by feat/fix/refactor/docs from titles.

3. **Compose the answer** as a compact chat-native report: 1-line headline (counts + trend), then
   grouped bullets with `#number 标题 (作者, 状态)` — each number must be a real fetched id.
   Cap lists at ~15 items and state the remainder count.

4. **Deliver.** Reply in the current chat. If the user asks for a document or the report exceeds a
   comfortable message, create a doc with `lark_docx_create` and send the link. If the user wants
   this regularly, offer to set it up via `scheduled_agent_creator` (cron + this skill +
   their exact ask as `execution_prompt`).

## Failure semantics

- 404 on the repo → the credential cannot see it (private repo not granted) — say that, do not
  retry blindly.
- Rate-limited → report the reset time from the response headers and return what you already have,
  clearly marked partial.

## Guardrails

- Read-only by default. Writing (commenting, labeling, opening issues) ONLY when the user
  explicitly asks for that exact write, and echo the target before doing it.
- Never fabricate issue/PR numbers, authors, or dates; never extrapolate beyond fetched pages
  without saying "前 N 页".
- Never ask the user for tokens — your NyxID-brokered tools handle all credentials.
