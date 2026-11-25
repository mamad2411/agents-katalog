---
name: brand-kickstart
description: Brainstorm brand or project names and check which ones are free as the same handle on Instagram, Threads, Facebook, TikTok, YouTube, X, GitHub, npm, PyPI and as domains (.com, .id, ...), then draws a logo, favicons, app icons and social banners for the chosen name. Use when the user is naming a brand, business, creator account, app, library or product, asks whether a username, handle or domain is available, wants consistent social media handles, or wants a logo, favicon, app icon or social banner for a brand.
---

# brand-kickstart

Help the user go from an idea to a launch-ready brand: **one name that is free everywhere they care about**, then a logo and assets for it. You brainstorm; the bundled script checks. `scripts/check.py` lives next to this file. Run it by its full path with `python3`.

Always:
- **The user already has a name?** Do not brainstorm others first. Check that name with `--variants` (step 4), then offer the logo (step 8).
- **Every "free" or "taken" comes from `check.py` output**, never from memory or a web search. If you cannot run code here, say so and give the user the command to run on their own machine.
- **The look comes from the concepts you draw** (step 8). Do not show web or stock photos as a moodboard: they are other brands' work.

## 1. Understand the brief

Learn what is being named, for whom, the language and the vibe. Note any platforms or domain extensions the user names ("check IG, TikTok and .id", "skip X"). If they gave none, use their config file or the defaults.

## 2. Choose the mode

| Mode | Use for | Checks |
|---|---|---|
| `brand` (default) | business, shop, creator, community | Instagram, Threads, Facebook, TikTok, YouTube, X + domains |
| `project` | app, SaaS, library, open-source tool | GitHub, npm, PyPI, Product Hunt, X + domains |
| `all` | unsure, or the user asks for everything | every platform + domains |

## 3. Brainstorm 8–12 candidates

- Short, easy to say and spell, and with no awkward letter clusters.
- Valid on every selected platform. X needs 5–15 characters with only letters, digits and `_`; Facebook needs 5 or more characters with only letters, digits and `.`; YouTube allows `-`; Instagram and TikTok allow `.` and `_`.
- For each one, propose a **display name** next to the lowercase handle, e.g. handle `acmestudio` with display `Acme Studio` or `AcmeStudio`. Handles are case-insensitive everywhere, so casing only matters for the display name.

## 4. Check them

```bash
python3 <skill-dir>/scripts/check.py "Acme Studio" seduhpagi kopilagi --mode brand --tlds com,id --json
```

Useful flags:
- `--platforms ig,tiktok,youtube` checks exactly these platforms; it overrides `--mode`.
- `--skip x` leaves platforms out.
- `--tlds com,id,co` sets the domain extensions (default `com`); `--no-domains` turns domains off.
- `--variants` also tries `acme.studio`, `acme_studio`, `acme-studio`, `…official`, `…hq`, `the…` (plus `get…` and `…app` in project mode). Each platform only gets the variants its rules allow.
- `--country id` adds `name.id` / `name_id` variants.

The JSON has `results` (each with `input`, `handle`, `platform`, `status`, `reason`, `url`) and `hints`. `status` is `available`, `taken`, `invalid` (not allowed on that platform) or `unknown`.

## 5. Present the results

- Show the script's table as-is: one row per platform or domain, one column per name, with ✅ available, ❌ taken, ❓ unknown and ⛔ not allowed. Names that are ✅ everywhere come first.
- **Link every handle and domain you mention** with its `url` from the JSON, e.g. `[facebook.com/acmestudio](https://www.facebook.com/acmestudio)`. This covers ✅? and ❓, which the user must open to confirm, and ❌, so they can see who holds the name.
- Threads shows `🔒` (`reason: held_by:instagram`) when the Instagram account with that name exists but has not turned on Threads. Only that Instagram account can ever use the name on Threads. If it is the user's own account, tell them to turn on Threads. If not, treat the name as taken.
- Facebook shows `✅?` (`reason: likely_free`) for a name it does not find. That usually means free, but an age-restricted page looks the same to a public check. Call it "probably free", never "free", and pass on its link.
- Product Hunt cannot be checked automatically, so it shows 🔗 (`reason: manual_only`) and its links appear under "Check yourself". Pass those links on; they never count against a name.
- For near-misses, rerun only those names with `--variants`. Recommend the variant that is **the same handle on every platform**; that beats a different handle per platform.

## 6. Be honest about unknowns

- **Never present `unknown` as available.** List each unknown with its link, so the user can check it in one click.
- Relay every line in `hints` as-is, e.g. "Instagram limited this IP. Wait a few minutes and rerun with --platforms instagram,threads".
- **Do not retry in a loop.** One rerun later is fine.

## 7. Final advice

Tell the user to register the winning handle on every platform **right away**. A public check cannot see handles held by banned or deactivated accounts; only each platform's signup form can confirm those.

## 8. Logo, favicons, app icons and banners (optional)

Once a name is picked, offer once: "Want a logo, favicons, app icons and banners for it? I will draw 3 styles for you to pick from, show the one you pick on a website, a tote bag and more, and write a brand guide (BRAND.md)." If the user says yes, read `references/brand-kit.md` next to this file and follow it. That file points to `references/styles.md` for typefaces, palettes, mark types and layouts. Do not load it before that.

## 9. The brand kit needs `resvg-py`

The name checks need nothing beyond Python. Only rendering the brand kit to PNG needs one package, `resvg-py` (2 MB). If `brand.py` reports it missing, say so once and **ask before installing it**. Then run:

```bash
python3 -m pip install resvg-py
```

If that fails with an "externally managed environment" error, use a virtual environment instead:

```bash
python3 -m venv ~/.venvs/brand-kickstart && ~/.venvs/brand-kickstart/bin/pip install resvg-py
```

After that, run `brand.py` with `~/.venvs/brand-kickstart/bin/python`.

## Saving preferences

When the user states a lasting preference ("never check X", "always check .id", "I mostly name apps"), offer to save it to `~/.config/brand-kickstart/config.json`. Create the file only if they agree. Merge with any existing content.

```json
{ "mode": "brand", "skip": ["x"], "tlds": ["com", "id"], "country": "id" }
```

Keys: `mode`, `platforms` (exact list), `skip`, `tlds`, `country`. Command-line flags always win over the file.

## Self-check

`python3 <skill-dir>/scripts/check.py --self-test` shows whether each platform still answers as expected. Run it when results look wrong.
