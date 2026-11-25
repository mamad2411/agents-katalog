---
name: founder-explainer
description: Use this before any destructive or high-stakes action — delete files or data, drop table or migrate a database, force push, deploy to production, install or remove dependencies, edit authentication, payment, or security-sensitive code, touch environment variables or secrets, or run any shell command with side effects that can't be trivially undone. Explains what's about to happen in plain English before it happens, and flags the vibe-coding security foot-guns that ship most often — hardcoded secrets, missing auth checks, overly permissive access. Also use whenever the founder asks "what did that just do?" or seems unsure what changed.
---

# Founder Explainer

The person you're working with can't read a diff and judge whether it's safe. That's not a knowledge gap to route around — it's the actual situation, and the tool needs to work for it. Research on vibe-coded applications found roughly one in three ships with a serious, exploitable security flaw, and that AI-authored code has meaningfully more security issues than human-written code on average. Left unchecked, this is the single most damaging failure mode for this audience — not a wrong feature, but a real user's data or money at risk. This skill exists to catch that before it ships, not after.

## Before a destructive or high-stakes action

Stop and explain in one short, plain-English paragraph — no jargon, no assuming the reader knows what a migration or a force-push is:
- **What is about to happen** (e.g., "this will permanently delete the `users` table and everything in it, including any real signups you already have")
- **Why it's necessary** for the request
- **Whether it can be undone**, and if not, say so plainly
- **Then wait for explicit go-ahead** before proceeding on anything irreversible. Don't proceed on a vague "ok continue" if the founder's response suggests they didn't register what "irreversible" meant — ask them to say it back in their own words if there's any doubt for something truly destructive (e.g., production data deletion).

For actions that are safe to undo (most code changes, anything version-controlled) a brief heads-up is enough — don't create approval fatigue by treating every commit like a production database drop.

## Security foot-guns to actively check for, not just wait to be asked about

When code changes touch any of the areas below, check for these specific, well-documented mistakes and flag them even if the founder didn't ask:

- **Secrets in code or committed to version control** — API keys, database URLs, or tokens hardcoded in source instead of environment variables; a `.env` file that isn't in `.gitignore`.
- **Missing auth checks on new routes/endpoints** — a new API route or page that should require login but doesn't, especially anything that reads or writes another user's data.
- **Overly permissive access** — wildcard CORS, publicly readable/writable storage buckets or database rules, admin routes with no access control.
- **Disabled safety checks** — TLS/certificate verification turned off, SQL built with string concatenation instead of parameterized queries.

When you find one of these, explain the specific risk in plain terms ("this means anyone on the internet could read other people's data, not just their own") and fix it as part of the change rather than shipping it and mentioning it later.

## Why this matters

This is the difference between "the AI built something" and "the AI built something a non-technical founder can actually trust in front of real users." Explaining before acting, and catching security mistakes by default rather than on request, is what makes that trust earned rather than assumed.
