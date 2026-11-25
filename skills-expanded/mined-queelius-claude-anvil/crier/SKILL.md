---
name: crier
description: Cross-post blog content to platforms with the crier MCP tools. Publishes one file (pass its path) or finds what needs cross-posting; holds the canonical rules for rewrites, approval, paste/import platforms, and failure recovery.
argument-hint: "[content file, e.g. content/post/my-post/index.md]"
---

# Crier Cross-Posting

Crier cross-posts blog content; the blog is the source of truth. Crier's MCP
tools do the mechanics (publish, track, validate); Claude does the judgment
(rewrites, platform voice, asking the user). This skill is the single home for
the rules below: `/crier:chronicler` and the `cross-poster` agent follow it.

Arguments: `$ARGUMENTS`

## Workflow

- **A file was given**: publish that one file (steps 1-5 below).
- **No file**: run `crier_search(since="1m")` and `crier_missing(platforms=<targets>)`,
  show what is unposted grouped by post, and ask which post to do. For a
  date-scoped batch catch-up, use `/crier:chronicler` instead.

1. **Targets.** Call `crier_doctor()`. The API targets are the platforms whose
   `status` is `"healthy"`; `manual_mode` and `import_mode` platforms are
   handled by hand (see below); skip `error` platforms and tell the user to fix
   their config. Never hardcode a platform list.
2. **Limits.** Read the `crier://platforms` MCP resource. Per platform it gives
   `mode`, `max_content_length`, and `is_short_form`. A platform needs a rewrite
   when `is_short_form` is true. Never hardcode limits.
3. **Validate and check status.** `crier_check(file, platforms=<targets>)` (skip
   the file on errors) and `crier_article(file)` (skip platforms it is already
   on; "Article not found" means it is on none).
4. **Approve.** Draft rewrites for the short-form targets, show the user the
   plan (platforms, each rewrite with its character count) and get explicit
   approval. Never publish without it.
5. **Publish** each approved platform with the two-step flow, then report a
   table of platform, status, URL.

## Two-step publish

1. `crier_publish(file, platform)` (add `rewrite_content=<rewrite>,
   rewrite_author="claude-code"` for short-form) returns a `preview` and a
   `confirmation_token`. If `preview.already_published` is true, stop: do not
   confirm. Check `preview.unrecorded_publication` (see Failures).
2. `crier_publish(file, platform, confirmation_token=<token>)` executes. The
   token carries the file, platform, and rewrite; step-2 arguments other than
   the token are ignored, so the rewrite need not be repeated. Tokens expire
   after 5 minutes: request a new preview if one does.

`dry_run=True` is a separate no-side-effects preview with no token; it cannot
start the two-step flow. `crier_publish` refuses `manual` and `import` mode
platforms.

## Rewrites (short-form platforms)

1. **Lead with insight, not summary.** Open with the most specific or
   provocative idea in the article. Read the article first.
2. **No meta-language.** Not "New blog post", "I wrote about", "Check out my
   latest", "In this article, I explore".
3. **Never include the URL.** Crier appends `\n\n<canonical URL>` itself.
4. **Budget for that URL.** The limit applies to rewrite plus URL, so the budget
   is `max_content_length - (len(canonical_url) + 2)`. The step-1 preview's
   `body_length` is the rewrite's length: check it against the budget before
   confirming. A rewrite over the raw limit fails at preview; one that only
   overflows once the URL is added fails at the confirmed publish.
5. **Not generic.** If it could describe any article or just restates the
   title, rewrite it.

Platform voice: Bluesky is conversational and personal, one punch. Mastodon is
slightly more formal and technical, and can carry more nuance. Twitter is
Bluesky with less room.

Good example. Article: "pagevault: Hiding an Encryption Platform Inside HTML".
Bluesky: "What if a single HTML file could encrypt anything you drop into it?
No backend, no JS libraries. Just the browser's Web Crypto API and some careful
engineering."

## Manual (paste) and import platforms

These are never published by a tool call, and never recorded until the user
says the post exists.

- **Manual mode** (`crier_doctor` status `manual_mode`): write the rewrite
  (budget as above), then show the user the exact text to paste: the rewrite,
  a blank line, and the canonical URL. Ask them to post it and give you the
  post URL.
- **Import mode** (`import_mode`, typically Medium): give the user the canonical
  URL to import on the platform, and ask for the resulting post URL.

Only after the user confirms it is posted, record it:

```
crier_record(title, platform, platform_id="manual",   # "import" for import mode
             url=<post url>, canonical_url=<canonical>, source_file=<file>,
             rewritten=True, rewrite_author="claude-code", posted_content=<rewrite>)
```

`platform_id` must be set (crier counts a publication only when it has one);
omit the three rewrite fields for an import. Never use the CLI's `--yes`: it
records a manual post as done before anything was posted.

## Failures

A failed `crier_publish` comes in three shapes:

- **`{"error": "..."}` at step 1** (validation: rewrite too long, mode, missing
  key, unreadable receipt): nothing was sent. Fix the cause and preview again.
- **`{"error": "Publish failed: ..."}` at step 2**: nothing reached the
  platform. Retry after fixing the cause (auth, length, rate limit). For a
  short-form platform, retry with the same approved `rewrite_content`.
- **`{"error": "Published remotely but registry recording failed: ...",
  "remote_published": true, "article_id": ..., "url": ...}`**: the post IS
  live; only the registry write failed, and crier saved a recovery receipt.
  Request a fresh preview: if `unrecorded_publication` is set, confirming
  records the live post from the receipt (result `"recovered": true`) without
  reposting. If it is null, do NOT confirm (short-form platforms have no update
  path, so a confirm would double-post); instead call `crier_record(title,
  platform, platform_id=<article_id>, url=<url>, canonical_url=<canonical>,
  source_file=<file>)`, plus `rewritten=True, rewrite_author="claude-code",
  posted_content=<rewrite>` for a short-form post. Count it as published.

**Retrying old failures.** List them with `crier_failures()`. Retry short-form
failures through `crier_publish` with a rewrite (write a new one and get it
approved if the original is gone): the MCP path checks the recovery receipt
before any remote write. The CLI `crier audit --retry` (preview with
`--dry-run`) also checks receipts, but it retries every recorded failure and
re-publishes WITHOUT any rewrite, so a short-form failure would post crier's
generic title-and-description text. Use it only when every remaining failure is
on a long-form platform.

## Bulk work and agents

Agents cannot ask the user anything (Claude Code removes AskUserQuestion from
subagents), so asking happens in the main session.

- **cross-poster**: for many publishes. Get approval for the exact posts,
  platforms, and rewrites FIRST, then pass that scope (with the rewrites) in the
  launch prompt. It publishes exactly that and returns anything else under
  `## Decisions Needed`; put those to the user with AskUserQuestion.
- **auditor**: read-only analysis (gaps, performance, staleness, failures). It
  ends with a numbered recommendations menu; present it and act on the answer.
  When it recommends drift repair, run `crier_reconcile()` (dry-run) here, show
  the `untracked_live` and `gone_from_platform` buckets, and only call
  `crier_reconcile(apply=True)` after the user approves.

## Platform notes

- Dev.to sanitizes tags: lowercase, alphanumeric only (no hyphens), max 4.
- Medium is usually import mode; check `crier_doctor` rather than assuming.
