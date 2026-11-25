---
name: bmem
description: Drive the bmem CLI to find, add, and run reusable web skills with whatever browser you already have (Playwright, claude-in-chrome, etc.).
---

## What bmem is

`bmem` is an open catalog of **web skills** — reusable, battle-tested recipes for
operating specific sites (search LinkedIn, read a Reddit thread, …). A skill ships
the exact selectors and, when possible, the direct in-page XHR, so you don't have to
read a whole DOM to figure the site out. You run the skill with **your own browser**;
bmem never drives a browser and never sees your cookies.

Use this loop whenever a task involves operating a website.

## The loop

1. **Search first.** Before exploring a site by hand, look for a skill:
   ```
   bmem search <query>              # e.g. bmem search linkedin people
   bmem search --site linkedin.com  # filter by site
   bmem list --limit 50             # browse the whole catalog
   ```
   Results are tiny index entries: `name`, `intent`, `side_effect`, `needs`, `verified`.

   Want the full recipe before committing? Read it without installing:
   ```
   bmem show linkedin.com/search-people   # prints the SKILL.md, no install
   ```

2. **Add the skill.** If one fits, register it as a native skill:
   ```
   bmem add linkedin.com/search-people   # one skill
   bmem add linkedin                     # a bare site adds every skill it has
   ```
   After this the skill appears in your **own** skill list — invoke it natively.
   You do NOT call `bmem` again to read it.

   > **Never invent a skill id.** Only `add` a `name` that came back verbatim from
   > `search` or `list`. The catalog is curated and read-only — a made-up id like
   > `linkedin.com/find-jobs` will just 404. If nothing matches, go to step 4.

3. **Run it with your browser** (see Execution below).

4. **No skill found?** `bmem search` is empty → explore the site yourself, find the
   real XHR endpoint in the network log (more robust than clicking), and author a new
   `SKILL.md`. Authoring is out-of-band — see the project's authoring guide.

## Reading a SKILL.md

A skill declares the browser **capabilities** it needs (`needs: [navigate, evaluate]`)
and writes its `## Execute` steps in those generic verbs. It never names a concrete
tool — you map each capability to whatever browser you have.

- `needs: [evaluate]` (± `navigate`) — the robust case: one in-page `fetch` + parse.
- `needs` includes `click`/`type`/`snapshot` — UI-driven, more fragile. Requires a
  browser that can drive the rendered page.

Check `needs` up front: if your browser can't provide a capability, switch to one that can.

## Capability → tool mapping

Translate each capability verb to your browser's tool:

| Capability      | Playwright MCP             | claude-in-chrome        | browser-memory `bm_*` |
| --------------- | -------------------------- | ----------------------- | --------------------- |
| `navigate(url)` | `browser_navigate`         | `navigate`              | `bm_navigate`         |
| `evaluate(fn)`  | `browser_evaluate`         | `javascript_tool`       | (in-page eval)        |
| `snapshot()`    | `browser_snapshot`         | `read_page`             | `bm_snapshot`         |
| `click(ref)`    | `browser_click`            | `computer`              | `bm_click`            |
| `type(ref,t)`   | `browser_type`             | `form_input`            | `bm_type`             |
| `network()`     | `browser_network_requests` | `read_network_requests` | `bm_network`          |

Skills ship a **CSS selector / description**, never an ephemeral ref or coordinate —
resolve it at runtime. Prefer doing DOM actions inside `evaluate`
(`document.querySelector(sel).click()`, `scrollIntoView()`) — it's uniform across
every browser and beats native click/type.

## Execution

One path, browser-agnostic:

1. `navigate` to the URL in the skill's Execute step 1 (establishes the session /
   same-origin for the fetch).
2. `evaluate` the skill's `## Extractor` function with the skill's `params`. It does the
   in-page authenticated fetches and parsing, and returns the JSON described in `returns`.
3. Read the result back via your browser's evaluate-result channel and check the skill's
   `## Success assertion`.

The browser holds the session — **no cookies ever leave it.**

## Auth (`auth: session`)

Some skills need a logged-in session. Check the skill's `## Preconditions`:

- If the site is already logged in in the browser profile you drive → just run it.
- If not → `navigate` to the site, let the **user** log in manually, then retry. The
  session persists in the browser profile; don't try to automate the login.
- Expired session mid-run → re-prompt the user to log in, then retry. Don't re-author.

## Self-host / staging

Point the CLI at another catalog with `BMEM_SKILLS_API_BASE_URL`. No config command needed.
