---
name: fetch-docs
description: >
  Use when you need to understand a library or API.
  Works through a fallback chain: installed source, llms.txt, doc pages, DeepWiki MCP, shallow clone.
  Don't give up after one failed approach.
user-invocable: true
auto-trigger: true
---

# Fetch Documentation Skill

When you need to understand a library or API, work through this fallback chain. Stop as soon as you have what you need.

1. **Read installed source** — check `.venv/lib/python3.*/site-packages/` for method signatures and types. Fast, but won't have usage examples.
2. **Try llms.txt** — fetch `https://docs.libraryname.com/llms.txt` (or the main domain). Use the URLs it returns to fetch specific doc pages.
3. **Fetch doc pages directly** — from llms.txt URLs or a web search. Also look for `openapi.json` at the API root.
4. **DeepWiki MCP** — query the GitHub repo. If the repo isn't indexed, move on.
5. **Clone to /tmp** — `git clone --depth 1` to `/tmp/repo-name`, read what you need. Check `docs/`, `examples/`, and root `*.md` files.

Don't give up after one failed approach. If you already know a docs URL, skip straight to it.
