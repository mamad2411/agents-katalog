---
name: danikuse-post
description: Write launch and update posts about Danikuse for X, Hacker News, and Reddit in a human voice. Use when the user invokes /danikuse-post or asks for a post, thread, or announcement about the Danikuse project.
---

# /danikuse-post — viral posts about Danikuse

## Facts (verified, do not invent beyond these)

- Repo: github.com/dancho133/danikuse, Apache-2.0, open source.
- Three surfaces: `/danikuse-my` (user's Brave via Bridge extension, no restart), `/danikuse-agent` (agent browser on the Brave engine, visible or `--hide`), `/danikuse-desktop` (Windows apps, visible cursor).
- Built on: agent-browser + agent-desktop (Vercel), Playwright dev loop, keyless Firecrawl for public pages, Skyvern ideas for form agents.
- Proof: five-task benchmark, 5/5 passing; ~156 MB install, zero paid keys, Windows-first.
- Honest limits: live captchas and multi-step logged-in forms not yet battle-tested; macOS/Linux uncertified.
- The ask: developers to review the code and the approach.

## Workflow

1. Draft in English: one concrete demo per post (the 20-second chain: GitHub → repo → Gemini answers → YouTube), numbers only from Facts, no adjectives about quality.
2. Run the SlopMonster checker: `python vendor-slopmonster/tools/deslop.py --text "..."`. Fix flagged vocabulary, three-item lists, and essay-summary closings. Do not chase 5/5 by hiding prose in formatting.
3. Second pass by the other model family (AGY) when reachable; otherwise note the pass did not happen.
4. Russian mirror in the same voice, not a literal translation.
5. Save under `danikuse/launch/` as `x-thread.md`, `hn-show.md`, `reddit-post.md` (plus `.ru.md` mirrors). Never publish anything yourself; drafts only.
