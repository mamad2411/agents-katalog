---
name: linkedin-poster
description: |
  Create and publish LinkedIn posts for business/sales content using the
  official LinkedIn UGC Posts API. Use when asked to post on LinkedIn,
  schedule a sales post, or process an approved LinkedIn post action from
  vault/Approved/. Always draft first and require human approval before posting.
---

# LinkedIn Poster

Publish posts to a LinkedIn personal profile using the official UGC Posts API (no browser required).

## When to Use

- Processing an `APPROVAL_SEND_LINKEDIN_POST_*.md` file from `vault/Approved/`
- Creating a new sales/business post when explicitly instructed by the user
- Drafting post content for human review (no approval needed for drafts)

**Never post directly** — always route through `vault/Pending_Approval/` first.

## One-Time Setup

### 1. Create a LinkedIn Developer App

1. Go to https://www.linkedin.com/developers/ → **Create App**
2. Select your LinkedIn Company Page as the associated company
3. Under **Products**, request: **Share on LinkedIn** + **Sign In with LinkedIn using OpenID Connect**
4. Under **Auth** tab → copy **Client ID** and **Client Secret**
5. Add Redirect URL: `http://localhost:8765/callback`

### 2. Add credentials to `.env`

```
LINKEDIN_API_CLIENT_ID=xxxxx
LINKEDIN_API_CLIENT_SECRET=xxxxx
```

### 3. Run the OAuth helper to get your access token

```bash
python watchers/auth_linkedin_api.py
```

This opens your browser, completes the OAuth flow, and prints the values to add to `.env`:

```
LINKEDIN_API_ACCESS_TOKEN=xxxxx
LINKEDIN_API_PERSON_URN=urn:li:person:xxxxx
```

Tokens last ~60 days. Re-run the auth helper when expired.

## Approval File Format

```markdown
---
type: approval_request
action: send_linkedin_post
status: approved
---

# What will happen after approval?

The following post will be published to LinkedIn.

## Message / Content

  [Hook line here]

  [Body paragraphs]

  [CTA]

  #hashtag1 #hashtag2 #hashtag3
```

Save to `vault/Approved/APPROVAL_SEND_LINKEDIN_POST_<topic>_<YYYY-MM-DD>.md`

## Dry-Run Mode

```bash
python .claude/skills/linkedin-poster/scripts/create_post.py \
  --content "Post text..." --dry-run
```

Expected output:
```json
{"status": "dry_run", "content_len": 42, "preview": "Post text...", "timestamp": "..."}
```

## Live Post

```bash
python .claude/skills/linkedin-poster/scripts/create_post.py \
  --content "Post text..."
```

Expected output:
```json
{"status": "posted", "post_id": "urn:li:share:...", "post_url": "https://www.linkedin.com/feed/update/...", "timestamp": "..."}
```

## Post Strategy — Sales Content Framework

Every LinkedIn post should follow one of these proven frameworks:

| Type | When to Use | Hook Pattern |
|------|-------------|--------------|
| **Problem → Solution** | New service/offer | "Most [audience] struggle with X. Here's how we solve it:" |
| **Story / Social Proof** | After a win or client result | "We helped [client type] achieve X in Y days. Here's exactly how:" |
| **Value List** | Education + awareness | "5 things [audience] should know about [topic]:" |
| **Direct Offer** | Promotion or launch | "We're opening [N] spots for [service]. Here's what's included:" |
| **Question / Poll** | Engagement | "Quick question for [audience]: [specific question]?" |

### Post Structure
```
[HOOK — 1-2 lines, no period at end, creates curiosity]

[BODY — 3-7 short paragraphs or bullet points, deliver value]

[CTA — 1 clear call to action: DM, comment, link in bio]

[HASHTAGS — 3-5 relevant hashtags on last line]
```

**Max 3,000 characters.** Script enforces this limit.

## LinkedIn DM

LinkedIn DMs to arbitrary users are **not supported by the API** (requires special partner access).
The `linkedin-dm` skill continues to use Playwright for DMs.

## Rules (non-negotiable)

- **Never** post without a file in `vault/Approved/`
- **Never** post competitor mentions, pricing without approval, or personal information
- **Max 1 post per day** — LinkedIn penalises over-posting
- **Always** log every post attempt to `vault/Logs/`
