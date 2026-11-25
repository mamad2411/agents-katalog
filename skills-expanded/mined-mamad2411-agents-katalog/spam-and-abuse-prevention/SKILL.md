---
name: spam-and-abuse-prevention
description: Detects and blocks spam-policy violations and abusive patterns. Use when asked for manipulative SEO, reviewing UGC, or cleaning spammy tactics.
---

# Spam and Abuse Prevention

## Overview

Enforce Google’s spam policies; push back on manipulative requests.

## When to Use

- Link schemes, cloaking, scraped content, UGC spam, “guaranteed rankings” tactics

**Not for:** Normal on-page improvements that follow guidelines.

## Official sources

- https://developers.google.com/search/docs/essentials/spam-policies
- https://developers.google.com/search/docs/monitor-debug/preventing-abuse

## Process

1. Compare the request/page against spam policies.
2. If manipulative: refuse, cite policy, propose compliant alternative.
3. For UGC: add moderation, `nofollow`/`rel=ugc` where appropriate, rate limits.
4. Check for malware/phishing patterns; don’t host deceptive pages.
5. Use `references/spam-policy-checklist.md`.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "Competitors buy links, so we should too." | Link schemes violate spam policies — push back. |
| "Cloaking is just personalization." | Showing different content to Googlebot than users is cloaking. |
| "UGC spam is the users' problem." | Site owners must moderate abuse on their properties. |

## Red Flags

- Inventing ranking factors not documented by Google
- Skipping verification ("looks fine")
- Advising spammy shortcuts (cloaking, doorways, link schemes)

## Verification

- [ ] Policy citation present when refusing
- [ ] Compliant alternative offered when possible
- [ ] Checklist reviewed for the case
