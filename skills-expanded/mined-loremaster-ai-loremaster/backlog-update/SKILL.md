---
name: backlog-update
description: >
  Use on /backlog-update or when the user asks to groom/refresh the backlog: cross-check Jira
  backlog status against `raw/decisions/*.md` and the wiki decision history (`## Decision History`
  sections in `wiki/concepts/*.md`), and propose — never auto-apply — the Jira corrections that
  local backlog-complete missed.
version: 0.1.0
author: Loremaster
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [scrum, backlog, jira, SM, write-gate, rest-api]
    related_skills: [daily-scrum, sprint-planning]
---

# Backlog Refresh & Assignment Proposals (SM, write-gated)

## Autonomy gate (absolute rules — never violate)
- **Read:** free (status, sprint, and issue queries).
- **Write:** **proposals only**. Post change/assignment proposals to Slack item by item. Never write to Jira directly.
- **Execute:** apply to Jira **only the items a human approved individually**. No auto-execution without approval.
- **Assignment is never automatic** (setting an assignee requires explicit approval from a designated approver or the PM).

## Role (v2)
- **Primary responsibility for Jira status transitions (In Progress → Done) lies with local `backlog-complete`** (each developer's Claude Code, before push).
- This skill is a second-line safety net that *proposes* the Jira↔document consistency fixes it missed — it never transitions issues itself.
- **progress checklists are not in the lore vault** (they live only in the project repo) — do not try to read them.

## Behavior
1. **Jira first:** when the user mentions a Jira issue key like `PROJ-20` or says "Jira ticket/backlog", **query the Jira issue directly before searching documents**. Do not conclude "no Jira access" from local environment variables alone; check this project's Jira credentials file (`~/.hermes/keys/jira.env` — an example copy ships in this repo's `examples/`; if present, `set -a; . ~/.hermes/keys/jira.env; set +a`) and query via the REST API. Even without a Jira CLI, `/rest/api/3/issue/{KEY}` can be called with Python/urllib + Basic auth.
2. **Cross-check:** progress evidence = **Jira backlog status + `raw/decisions/*.md` + the wiki decision history (`## Decision History` sections in `wiki/concepts/*.md`)**. Compare them against each other —
   - decision docs/wiki show completion evidence but Jira is still open (backlog-complete missed the transition) / Jira says done but there is no matching decision doc or wiki update / work with documented evidence is missing from the backlog and needs a new issue.
3. **Attach evidence:** every proposal carries the *why* (grounds) + a **source (`file:line` or Jira issue key)**. No proposal without a source.
4. **Post proposals + approval:** post priority, status-change, and (when needed) assignment proposals to Slack, and immediately before applying each item, obtain [Allow]/[Deny] button approval via the **`request_approval` tool** (`title` = the item, e.g. "PROJ-12 → Done"). No prose "please approve" and no numbered prompts. Apply only items that come back APPROVED.
5. **Apply:** apply only the human-approved items via the Jira REST API (API token). Leave unapproved items untouched.

## Minimal Jira REST patterns
- Read: `GET /rest/api/3/issue/{KEY}?fields=summary,description,status,issuetype,priority,parent,customfield_10020`
- Update: `PUT /rest/api/3/issue/{KEY}` with `fields.summary` and ADF `fields.description`.
- Jira descriptions are ADF — never send raw prose; convert to paragraph/bulletList.
- After an update, re-fetch the same issue and verify that summary/description actually changed.

## Source-of-truth separation
- **Jira = truth for the execution backlog** (sprints, assignments, status). The primary actor for status transitions is local backlog-complete.
- **`raw/decisions/*.md` + the wiki decision history (`## Decision History` sections in `wiki/concepts/*.md`) = truth for implementation decisions** (what was decided, and why).
- **Documents → Jira, one-way proposals only.** Do not merge the two. Never write Jira status back into the documents.

## Operator-decision follow-up
- When backlog grooming leaves "operator decision needed" items as a comment and the user later replies with numbers, map each answer to the item order and proceed straight to apply proposals. Do not separately ask "which item do you mean?".
- If a decision changes **Jira scope only**, update/create the affected ticket and verify by re-fetching. Example: "Ad SDK not yet — substitute with Pro-plan ads" → change the ad-reward ticket's scope from SDK integration to Pro-plan guidance/ad substitution plus removal of reward farming.
- If a decision changes the **PRD/document source of truth**, apply the `resolve-conflicts`/`impact-analysis` flow as well: write the PROPOSAL file → `request_approval` buttons → patch the PRD → git commit → push approval. Example: "remove PRD §2.2 daily recommended missions" must not touch only Jira — remove the bullet from the PRD and search raw/ and wiki/ for leftovers too.
- A reply like "what am I supposed to decide?" is a confusion signal. Immediately explain the decision point and the options in plain language and propose a clear default, but never change Jira without approval. Example: for pricing-display consistency, explain "if the beta is free, hide the price CTA / show free-tier copy; once billing opens, align in-app price/paywall/current-plan display with the real plans" — deferring the decision is fine.
- If the user corrects a decision in a follow-up message (e.g. "not auto-granting to everyone — a zero-cost discounted subscription instead"), reflect the **semantic difference exactly**: rewrite the Jira description/PRD proposal and get re-approval. Auto-entitlement, zero-cost/discounted subscription, free trial, and billing-disabled are different operating modes — do not lump them together.
- If a numbered answer is submitted twice, apply it only once.

## Gate
- Never invent backlog items without evidence in Jira, `raw/decisions/`, or the wiki.

## Isolation
- This channel = this project only. Query and propose only against this project's Jira project key. Never touch other projects.
