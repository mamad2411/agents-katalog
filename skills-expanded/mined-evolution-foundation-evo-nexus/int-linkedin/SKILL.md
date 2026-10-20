---
name: int-linkedin
description: "Query LinkedIn API — profile info, posts (when approved), org stats. Supports multi-account via OAuth. Use when user asks about LinkedIn metrics, LinkedIn profile, LinkedIn posts, or any reference to LinkedIn analytics."
---

# LinkedIn API

LinkedIn integration to monitor user profile and (future) Company Page. Multi-account via OAuth (Social Auth App).

## Setup

Accounts configured via `make social-auth`. Saved in `.env`:
```env
SOCIAL_LINKEDIN_1_LABEL=Your Name
SOCIAL_LINKEDIN_1_ACCESS_TOKEN=YOUR_TOKEN
SOCIAL_LINKEDIN_1_PERSON_URN=urn:li:person:YOUR_URN
```

## API Client

```bash
python3 {project-root}/.claude/skills/int-linkedin/scripts/linkedin_client.py <command> [args]
```

### Commands

```bash
linkedin_client.py accounts                    # List accounts
linkedin_client.py profile [account]           # Profile (name, email, photo)
linkedin_client.py my_posts [account] [N]      # Recent posts (requires scope w_member_social)
linkedin_client.py post_stats POST_URN         # Reactions/comments of a post
linkedin_client.py org_followers [account]     # Org followers (requires Advertising API)
linkedin_client.py summary                     # Summary of all accounts
```

## Available scopes

| Scope | Status | LinkedIn Product |
|-------|--------|-----------------|
| `openid profile email` | Active | Sign In with OpenID Connect |
| `w_member_social` | Active | Share on LinkedIn |
| `r_organization_social` | Pending | Advertising API (request form) |
| `r_organization_admin` | Pending | Advertising API (request form) |

## Current limitations
- **Posts:** Reading posts requires an additional scope not available in the current tier
- **Company Page:** Requires Advertising API (pending approval)
- **Workaround:** Export CSV from LinkedIn Analytics for Company Page data

## Note on versioned API
- Base URL: `https://api.linkedin.com/rest/` (org/analytics endpoints)
- Required headers: `Linkedin-Version: 202603`, `X-Restli-Protocol-Version: 2.0.0`
- Personal profile uses `/v2/userinfo` (OpenID Connect)
