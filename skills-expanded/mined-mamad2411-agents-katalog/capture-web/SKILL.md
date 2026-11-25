---
name: capture-web
description: Use when a web page needs to be preserved as evidence — archives it as a single self-contained file, records the capture context that the page itself cannot prove, hashes the result, and offers to register it. Triggers - "archive this URL", "capture a webpage as evidence", "save this page before it changes".
allowed-tools: Bash(single-file *), Bash(shasum *), Bash(sha256sum *), Bash(command *), Bash(mkdir *), Bash(date *), Bash(curl *), Read, Write
---

# Capture Web Page

Archive a page as a single self-contained file, and record the context that the archive
itself cannot prove.

## When to use

- A page is likely to change, be edited, or disappear.
- A page's current state is itself the evidence.

## Inputs

- URL. Required.
- `--no-log` — capture without offering to register the result. Optional.

## Procedure

### 1. Record the request context first

Before fetching, write down what will not be recoverable afterwards: the exact URL, the
capture time in UTC, and whether the session was authenticated. A page behind a login,
behind a paywall, or personalised to an account is not the page another person sees at
the same URL — say so explicitly in the record.

```bash
date -u +%Y-%m-%dT%H:%M:%SZ
```

### 2. Capture the response headers separately

```bash
curl -sSI "$URL" > "logs/headers-$STAMP.txt"
```

Headers carry the server date, content type, and any redirect chain. They are cheap to
keep and often the only independent corroboration of when the fetch happened.

### 3. Archive the page

```bash
single-file "$URL" "evidence/originals/$SLUG-$STAMP.html"
```

SingleFile inlines images, stylesheets, and fonts, so the archive renders offline
without further requests. If the tool is missing, say so and stop — do not silently fall
back to a plain `curl` fetch, which produces a materially weaker artifact and hides
that fact.

### 4. Hash the result

```bash
shasum -a 256 "evidence/originals/$SLUG-$STAMP.html"
```

### 5. Offer to register

Unless `--no-log` was given, hand the file to the log-custody skill with the source
prefilled as the URL and the capture time, and the custody notes prefilled with the
session context from step 1.

## Output

- A self-contained HTML archive under `evidence/originals/`.
- A headers file under `logs/`.
- A digest, and a register record if logging was accepted.

## Notes

- The archive proves what was rendered to this browser at this moment. It does not
  prove what the server would return to anyone else, then or now.
- Dynamic pages, infinite scroll, and content behind interaction will be captured only
  as far as they had loaded. State what was and was not reached.
- For a stronger record, timestamp the archive as well — see timestamp-evidence.
