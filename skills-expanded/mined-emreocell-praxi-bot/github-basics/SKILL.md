---
name: github-basics
description: Navigate github.com repositories, issues, pull requests and search efficiently.
version: 0.1.0
when:
  domains: [github.com]
---
# github.com basics

URLs (replace owner and repo):
- Repo: `https://github.com/owner/repo`; file: `/blob/<branch>/<path>`; raw text: `https://raw.githubusercontent.com/owner/repo/<branch>/<path>`.
- Issues `/issues`, pull requests `/pulls`, one item `/issues/123` or `/pull/123`, PR files `/pull/123/files`.
- Releases `/releases`, commits `/commits/<branch>`.
- Code search: `https://github.com/search?q=<query>&type=code` (requires sign-in); repository search works signed out.

Tips:
- Open URLs directly with `browser_open` instead of clicking through menus.
- Read files via the raw URL to get plain text without page chrome.
- Issue and PR filters go in the search box: `is:open label:bug author:name`.
- Creating issues, commenting, starring, forking or merging are writes: confirm with the user first.
- Never enter passwords or tokens; if sign-in is needed, ask the user to sign in themselves.
- Signed-out browsing may show a "too many requests" page; wait before retrying.
