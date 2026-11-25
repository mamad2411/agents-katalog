---
name: seemd
description: Use when the user asks for a shareable web URL for a local markdown file. Triggers on phrases like "share this markdown", "share this doc", "give me a link for this", "send this as a URL", "publish this", "make a public page for this", and Korean equivalents like "공유해줘", "이 README 공유", "링크로 보내줘". Especially when the user names a `.md` file path together with one of those phrases. Runs `npx @tentagrip/seemd <path>`, returns a slug URL on https://seemd.xyz. Linked `.md` files are uploaded together and cross-document links rewritten to slug URLs. Documents auto-expire after 3 days.
user-invocable: true
allowed-tools: Bash
argument-hint: "<path-to-md-file>"
---

# seemd — share markdown via URL

## How to invoke

```bash
npx @tentagrip/seemd <path-to-md-file>
```

The last line of stdout is the share URL.

## Output format — keep it terse

**Reply with the URL alone, on its own line.** Nothing else.

Don't:
- Preamble ("Here is the link:", "공유 링크입니다:")
- Recap what got uploaded ("3 linked docs uploaded too")
- Mention the 3-day expiry
- Echo the path
- Summarize stderr progress

The user asked for a link. Give them the link. That's the entire job.

Exceptions:
- Upload failed → one short line with the error
- User explicitly asked for details ("공유하고 어떤 파일들이 같이 갔는지", "tell me what got uploaded") → then add a brief summary AFTER the URL

## Picking the file when ambiguous

If the user names a generic noun ("README", "이 문서") without a path and multiple files match, ask them which one — *briefly*. A short list of paths and a one-line question. Don't dump grep results, don't narrate the search.

If exactly one match exists, just use it.

## What the CLI does (for context)

- Walks markdown links and uploads every reachable relative `.md`
- Rewrites cross-document links to slug URLs (anchors preserved)
- Skips images, external URLs, non-md targets
- Tolerates link cycles (back-edge stays as original path)
- Documents auto-expire 3 days after upload

## Gotchas

### 1. Don't paraphrase the URL
Slug URLs are 21-character nanoids. Copy them verbatim. Any rewording breaks the link.

### 2. `npx` wrapper interception
If the bash call returns `Unknown command: "@tentagrip/seemd"` or `Missing script: "@tentagrip/seemd"`, the user has a tool wrapping `npx` (e.g. Rust Token Killer). Retry once with:

```bash
rtk proxy npx -y @tentagrip/seemd <path-to-md-file>
```

If that's not available either, suggest the user install globally (`npm i -g @tentagrip/seemd && seemd <path>`) and stop retrying.

### 3. Broken relative links in the source
The CLI prints `Warning: linked file not found: ...` to stderr for broken `[text](missing.md)` links. The upload still succeeds and the URL is still valid — don't surface these warnings unless the user asks.
