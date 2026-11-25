---
name: remake
description: Remake any website pixel for pixel with the Remake engine, ship it to the user's private GitHub repo and Vercel behind a passcode, then build the swap board that makes it theirs. Use when someone asks to remake, clone, copy, rebuild or reverse-engineer a website or landing page, wants "this site, but mine", or sends "/goal Remake <url> with github.com/rubenhassid1/remake …".
---

# Remake

Turn a URL into a working copy that matches the original on every screen, put it live on the user's own GitHub and Vercel (private, passcode, hidden from search engines), then hand them a swap board listing every text, photo, video, font, logo and link to replace so the site becomes theirs.

The finish line is the last line of `remake report`: **REMAKE COMPLETE**. Under `/goal`, the judge only reads this conversation, so paste the full report output into the chat every time you run it.

## 0. Set up the engine (once per machine)

```bash
[ -d ~/.remake ] || gh repo clone rubenhassid1/remake ~/.remake -- --depth 1 || git clone --depth 1 https://github.com/rubenhassid1/remake ~/.remake
git -C ~/.remake pull --ff-only --quiet; npm --prefix ~/.remake install --silent
npm install -g ~/.remake --silent   # puts a `remake` command on the PATH
remake doctor --fix
```

If the global install isn't allowed on this machine, use `node ~/.remake/engine/bin/remake.mjs` wherever this skill says `remake`. Shell aliases don't survive between tool calls, so don't rely on one.

`doctor --fix` installs Chromium for Playwright and the Vercel CLI. If GitHub or Vercel isn't signed in, run `gh auth login --web` or `vercel login` yourself and tell the user, in one sentence, that a browser tab opened and they should click Authorize. That is the only thing the user does.

## 1. Refuse what Remake is not for

- **Sign-in, checkout and banking pages.** The engine stops on visible password or card fields. Don't work around it.
- **Passing as the original.** If the user wants to publish the copy under the original's name, collect its visitors' details, or send people to it as if it were the real company, stop and say why.
- **Bot walls.** If capture says the site shows a bot check, tell the user. Offer `remake capture --archive` (rebuild from the Internet Archive's copy) or another site. Never use proxies, stealth browsers, a fake user agent or CAPTCHA solvers.

A private remake of a public marketing page, to learn from or to turn into your own site, is the use case. The passcode stays on until the swap board reaches 100%.

## 2. The loop

1. **Start.** `remake init <url>` (add `--pages 6` when the user says "website": the home page plus its main navigation; a single page or landing page needs no flag). Then `cd` into the printed folder (default `~/remakes/<site>`).
2. **Capture.** `remake capture`. It visits once at desktop and once at phone size, records every response, writes the site into `site/`, pulls the original source files into `remake/sources/` when the site publishes source maps, removes trackers, and fetches other image sizes one at a time. Read its summary: frameworks, streaming videos, files it couldn't get.
3. **Score.** `remake score`. Both sites are frozen at the same instants (paused clock, seeded randomness, videos on their first frame), and every screen at desktop and phone plus 24 frames of scrolling motion are compared. Pass mark: 98% of stable pixels per screen, 95% per motion frame, page heights within 4 px. Pixels that change between two loads of the original are left out and reported as noise.
4. **Repair** until the score passes. Work on the worst screen first:
   - Open its diff image with Read (`remake/score/<page>-<viewport>-NN.png`: original | remake | red = different, blue = noise left out).
   - Look at the remake live: run `remake serve` in the background and open the printed URL in the browser pane. Click through menus, sliders, tabs. Then `remake fetch --missing` collects every file the remake asked for but didn't have.
   - Script errors from the remake are printed by `score`. Read them; most are an absolute address or an origin check.
   - Fix files in `site/` directly, then re-score only what you touched: `remake score --page / --viewport phone --no-motion`. Run the full `remake score` before shipping.
   - Known causes and fixes: [references/fixing.md](references/fixing.md). After two failed attempts on the same screen, ask the `remake-judge` agent for a fresh read.
5. **List what's theirs.** `remake slots` writes `remake/content.json`, then `remake board` builds the proof page (`/_remake/`), the swap board (`/_remake/swap/`) and `MAKE-IT-YOURS.md`.
6. **Ship.** `remake ship`. Private GitHub repo, Vercel deploy, passcode in the `REMAKE_PASSCODE` variable, gate checked from outside. The user's request to put it on their GitHub and Vercel is the go-ahead; don't ask again. Never make the repo public or remove the passcode unless the user says so.
7. **Report.** `remake report`. Paste the whole output. If it says REMAKE NOT DONE, work on what it lists: a change after shipping means score, then ship, then report again.

## 3. Rules while repairing

- **The site must be the site.** Never put a screenshot, an iframe of the original or an image of a section in place of the markup. The score would pass and the remake would be fake. Remove anything like that if you find it.
- **Don't touch the measuring.** Never edit `remake/original/`, the score files, the thresholds in `remake/remake.json`, or the freeze logic.
- **Accept a difference only when it can't be fixed.** `remake accept "<page> <viewport> screen N" --reason "…"` works for screens at 90% or more, after at least three repair attempts, when the cause is outside the page's own code (a live map or video embed from another company, live data). The report lists every accepted difference with its reason.
- **Re-score after each meaningful fix** and say the numbers in one line. Keep a short running list of what you fixed; the final message uses it.
- **Be polite to their server.** Everything after the first visit comes from the recording. `fetch` goes one file at a time. If a host stops answering, the engine switches to the Internet Archive; don't retry it in a loop.

## 4. Final message

When the report says REMAKE COMPLETE, end with:

1. The report output (already pasted) and one line on what you fixed.
2. Live link, passcode, private repo, proof page (`<url>/_remake/`), swap board (`<url>/_remake/swap/`).
3. **What I need from you to make it yours**: one line per group from `MAKE-IT-YOURS.md` (copy, photos, videos, logos, fonts, colours, links and forms), with the counts and the flags (paid fonts, photos and trademarks that belong to the original, videos still streaming from their account).

## 5. Making it yours (when the user sends material)

Read [references/swap.md](references/swap.md). In short: fill the `swap` field of each slot in `remake/content.json` (new words in the user's voice at the same length, photos matched by shape, a free look-alike font from Google Fonts, their colours, links and form address), then `remake apply`, `remake board`, `remake score` (layout should hold even though content changed), `remake ship`, `remake report`. Remove the passcode only when the user asks and the board shows 100%.

### New pictures without theirs

Never keep the original's photos, and never copy them into a generator. `remake images` measures every image slot that still belongs to the original (shape, palette, brightness, photo or graphic) and writes `remake/images.json` plus contact sheets (`remake/images-sheet-NN.png`). Open the sheets with Read, then write a `prompt` for each entry: what the new brand's picture should show, keeping the original's framing, orientation, light and palette (the entry's `look` says them). Describe a new scene in your own words; never ask for the original's people, text, logos or artwork. Add `keywords` (3–6 words) for the free-stock fallback. When the user has a picture of their own for a slot (their headshot, their office), set `use` to its path instead of a prompt.

Then `remake images --make`. It uses the best source available: Codex image generation on the user's ChatGPT plan (found automatically when the ChatGPT or Codex app is installed and signed in), an `OPENAI_API_KEY` or `GEMINI_API_KEY`, free stock (Openverse, then Wikimedia Commons; public domain and CC0 only), and generated art in the original's palette as the last resort. Every result is credited in `remake/credits.json`. Then `remake apply`. Look at the result in the browser pane; re-prompt and `--make --force` any picture that doesn't fit.

## 6. Rebuild mode (only if asked)

The default remake keeps the original's own HTML, CSS and scripts, which is why it matches. If the user wants an editable component codebase (React, Next.js), read [references/rebuild.md](references/rebuild.md): rebuild one section at a time, with the score as a lock that must keep passing.
