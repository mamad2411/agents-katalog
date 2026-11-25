---
name: reply-to-google-reviews
description: Reply to Google reviews on a Google Business Profile (GMB, Google My Business) with the Reach MCP server. Finds unanswered reviews, triages them by rating and age, drafts replies in the reviewer's language, shows each reply word for word and posts only the ones the owner approves. Use when someone asks to answer, respond to or manage their Google reviews, reply to a bad review, or clear a review backlog.
license: MIT
---

# Reply to Google reviews

Answer a business's unanswered Google reviews through Reach, one approved reply at a time.

## Setup

This skill needs the Reach MCP server connected in your AI client:

- Server URL: `https://reach.locus-intelligence.com/api/mcp` (remote, Streamable HTTP, OAuth sign-in, no API key)
- Setup for Claude, ChatGPT, Claude Code, Codex, Cursor, VS Code and others: [README](https://github.com/LocusIntelligence-DauAgency/google-business-profile-mcp#install)

The owner signs in with their own Reach account. Replying needs the Google Business Profile connected in Reach.

## Steps

1. **Pick the location.** Call `get_account`. If the account has more than one location, ask which one. If that location's `connectionStatus` is not `active`, tell the owner to reconnect Google in Reach (Connections page) and stop.
2. **Find unanswered reviews.** Call `get_listing` with `sections: ["reviews"]` and `reviewFilter: { replyStatus: "not_replied" }`. If the list is empty, read `limitations` first: say "no unanswered reviews" only when `limitations` is empty.
3. **Triage.** List the unanswered reviews briefly: star rating, age, first line. Put 1 and 2 star reviews first, then the oldest. Work through at most 5 at a time.
4. **Offer a draft.** For each review, the owner can write their own reply (free) or ask for drafts. `draft_review_reply` with the review's `reviewId` returns reply options and uses 2 Credits per call; say so and give the remaining Credits from the result. Nothing is posted by drafting.
5. **Show the exact reply.** Show the final text the owner chose or edited, word for word, and the current reply if the review already has one. Remind them the reply is public under the review and cannot be removed from here; replying again replaces it.
6. **Wait for a yes.** Post only after an explicit yes to that exact text. A yes covers one reply, never a batch.
7. **Post.** Call `reply_to_review` with the `reviewId` and the approved `text`. Pass an `idempotencyKey` so a retry does not post twice.
8. **Read back.** Call `get_listing` again and confirm the review now shows as replied.

## Writing the reply

- Thank the reviewer by name when the review shows one. Mention something specific they said.
- For a complaint: acknowledge it, do not argue, do not admit legal fault, and offer a way to continue offline (phone or email the owner gives you). Never invent a phone number, email, discount or promise.
- Keep it short: two to four sentences.
- Never include customer details beyond what the reviewer made public.

## Language

Reply in the language the review is written in, unless the owner asks for another language. Talk to the owner in the language they use with you. If a review mixes languages, use the main one and tell the owner which you chose.

## Safety

- Never post without the owner's explicit yes to the exact text. Show it word for word first.
- Stop if the location's `connectionStatus` is not `active`.
- Read `limitations` before saying there is no data.
- On `rate_limited`, tell the owner `retryAfterSeconds` and do not retry right away. Changes to Google are limited per business per hour.
- On `limit_reached` or `monthly_quota_exhausted`, say what was blocked, give the `manageUrl`, and stop.
- On `listing_only`, relay the message and `connectUrl`, and stop.
- Talk about usage in Credits, never money.
