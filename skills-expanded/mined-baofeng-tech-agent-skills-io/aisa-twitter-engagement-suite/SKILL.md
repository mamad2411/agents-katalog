---
name: aisa-twitter-engagement-suite
description: 'Research Twitter/X profiles, tweets, and trends, then complete approved engagement or posting follow-through through the AIsa relay. Use when: the user needs Twitter/X research plus likes, follows, unfollows, posting, or post-action follow-through without sharing passwords. Supports relay-based reads, OAuth-approved writes, and media-capable posting flows.'
license: MIT-0
compatibility: Designed for Agent Skills compatible clients such as OpenClaw, Claude Code, Hermes, and GitHub-backed skill catalogs. Requires system binaries python3, environment variables AISA_API_KEY and internet access to api.aisa.one.
metadata:
  author: AIsa
  version: 1.0.3
  homepage: https://aisa.one
  repository: https://github.com/baofeng-tech/agent-skills-so
  tags: twitter,x,search,research,media,aisa
  platforms: agentskills.io,agentskills.so,github
  primary_env: AISA_API_KEY
allowed-tools: Read Bash Grep
---

# AIsa Twitter Engagement Suite

Research Twitter/X profiles, tweets, and trends, then complete approved engagement or posting follow-through through the AIsa relay.

## When to use

- When the user needs Twitter/X research plus action-oriented follow-through such as posting, liking, unliking, following, or unfollowing.
- When the workflow should keep research and approved write actions in one package while using only `AISA_API_KEY` for the shipped runtime.
- When the task can use the bundled Python clients with network access to `api.aisa.one`.
- When the user can complete explicit OAuth approval before write actions or media posting.
- When relay-based Twitter/X reads, writes, and media upload are acceptable and the user should not share passwords.

## When NOT to use

- Do not use this for cookie extraction, password login, or a fully local Twitter/X client.
- Do not use this when the workflow must avoid relay-based network calls, remote writes, or relay-based media upload through `api.aisa.one`.
- Do not use this for undocumented secrets, browser-derived auth values, or hidden credential flows.
- Do not use this when the user needs the broader flagship Twitter lane; use `aisa-twitter-api` for that surface.
- Do not use this for watchlists, trend desks, or recurring monitoring-first workflows better matched to `aisa-twitter-command-center`.

## Quick Reference

| Need | Path / Requirement |
| --- | --- |
| API key | `AISA_API_KEY` |
| Required binary | `python3` |
| Relay target | `api.aisa.one` |
| Read client | `scripts/twitter_client.py` |
| Post client | `scripts/twitter_oauth_client.py` |
| Engage client | `scripts/twitter_engagement_client.py` |
| References | `references/post_twitter.md`, `references/engage_twitter.md` |

## Setup

```bash
export AISA_API_KEY="your-key"
```

Requirements:

- `python3`
- Internet access to `api.aisa.one`
- `AISA_API_KEY` must be set in the environment before running the clients
- Explicit OAuth approval before posting or engagement writes
- Relay-based upload support for approved media posting flows

## Common Commands

```bash
python3 scripts/twitter_client.py search --query "AI agents" --type Latest
python3 scripts/twitter_oauth_client.py authorize
python3 scripts/twitter_engagement_client.py like-latest --user "@elonmusk"
```

## Capabilities

- Research Twitter/X accounts, tweets, trends, lists, communities, and Spaces.
- Publish text, image, and video posts after explicit OAuth approval.
- Like, unlike, follow, and unfollow after authorization exists.
- Keep research and engagement follow-through in one package while making relay target, OAuth approval, upload behavior, and env requirements explicit.

## High-Intent Workflows

- Research a topic or account, then take an approved engagement action from the same runtime surface.
- Review recent Twitter/X activity before deciding whether to like, follow, unfollow, or post.
- Prepare a post, complete OAuth approval, and publish through the relay-backed write path.
- Run post-research engagement follow-through where remote reads, remote writes, and relay-based media upload are acceptable.

## Example Requests

- "Research this Twitter/X account, then like the latest post if it matches our topic."
- "Search Twitter/X for AI agents, review the results, then prepare an approved engagement action."
- "Authorize posting, then publish a Twitter/X update with media through the relay flow."
- "Check recent activity from this account and decide whether to follow or unfollow."

## Trust and Side Effects

- All networked operations go through the AIsa relay at `api.aisa.one`.
- The shipped runtime requires `AISA_API_KEY`; do not imply password-based or cookie-based auth.
- Write actions require explicit OAuth approval before they can succeed.
- Posting with media uses relay-based upload paths supported by the runtime.
- Reads, writes, and uploads are remote API operations, not local-only actions.
- Do not claim a post, like, follow, or unfollow succeeded until the API confirms it.
