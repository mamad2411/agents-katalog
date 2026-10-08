---
name: suggest-icon
description: Suggest an icon suitable for a particular situation, noun, verb, or concept
user-invokable: true
args:
  - name: use-case
    description: A concept, situation, noun, verb or idea that needs an icon
    required: true
---

Your inherent knowledge of Font Awesome icons is useful for a quick initial guess, but it may be inaccurate depending on the version. To give a reliable answer, layer multiple sources of information.

All scripts below are relative to this skill's directory (`plugins/icons/skills/suggest-icon/`). Run them from there.

## Tool selection

At the start, run `command -v fa` to check whether the `fa` CLI is available on PATH.

The `fa kit` subcommand requires `fa` version 0.8.0 or newer. If the `fa kit` subcommand is needed, recommend the user upgrade `fa`, using instructions here: https://docs.fontawesome.com/web/use-with/fa-cli

- **If `fa` is found:** use it for icon lookups and searches (it returns structured JSON). If the project is configured with a Kit (see "Respect the configured Kit" below), also use `fa search --kit-token <TOKEN>` to search only icons available in the Kit, and `fa kit icon` to confirm a specific icon is included. For `fa kit ...` operations, check auth first (`fa whoami` or `FA_API_TOKEN`); if you can't authenticate, fall back to unscoped search and warn the user that Kit coverage couldn't be verified.
- **If `fa` is not found:** fall back to the Python scripts described below. Kit-aware searching requires the `fa` CLI; without it, you cannot scope suggestions to the Kit's subset — warn the user that your suggestions may include icons their Kit does not contain.
- Use `latest-version.py` to get the latest version.

## Respect the configured Kit

If the project has a `.font-awesome.md` file with a **Kit ID** (the kit token), the user's icons come from that Kit, and a Kit only contains a subset of all Font Awesome icons. **Do not suggest an icon the Kit does not include** — recommending an icon that isn't in the Kit leads to a broken, non-rendering result.

When a Kit token is present, scope every suggestion to the Kit:

- Search with `fa search --kit-token <TOKEN> --query <your-guess>` instead of `fa search --version <version> ...`. This returns only icons that are actually available in the Kit, up to the Kit's subset, so every result is safe to recommend.
- Before presenting your primary recommendation, confirm it with `fa kit icon --kit-token <TOKEN> <icon>`. This tells you whether the icon is in the Kit and which family-styles it's available in.
- If the icon you'd most like to recommend is **not** in the Kit, say so plainly, recommend the closest kit-available alternative instead, and let the user know they can add the missing icon to their Kit at https://fontawesome.com/kits (after which it will be available).

If no `.font-awesome.md` exists or it records no Kit, suggest from the full icon set as normal.

## Steps

1. **Determine the version.** If the user specifies a Font Awesome version, use that. Otherwise, use the latest version (See "Tool selection" above). Use the resolved version for all subsequent steps.

   Also check for a `.font-awesome.md` file in the project root. If it records a **Kit ID** (kit token), keep it on hand — you'll scope your search and suggestions to the Kit (see "Respect the configured Kit" above).

2. **Make an initial guess.** Based on your knowledge, pick the icon name you think best fits the use case argument.

3. **Verify the icon exists.**

   - **`fa` CLI:** Run `fa icons --version <version> --name <your-guess>`. The icon exists if `data.release.icon` is non-null. The `familyStylesByLicense` field shows the free/pro breakdown.
   - **Fallback:** Run `./scripts/icon-exists.py --version <version> --icon-name <your-guess>`. Exit code `0` means the icon exists; exit code `1` means it does not.

   **If a Kit token is configured,** also confirm Kit membership with `fa kit icon --kit-token <TOKEN> <your-guess>`. An icon can exist in Font Awesome but still be absent from the Kit's subset — if it's not in the Kit, don't recommend it as-is (see step 5).

4. **Search for alternatives.** Do this regardless of whether your initial guess exists — searching often surfaces more specific or better-fitting icons that you wouldn't think of on your own.

   - **Kit configured (`fa` CLI):** Run `fa search --kit-token <TOKEN> --query <your-guess> --page-size 10`. This returns only icons available in the Kit, so every result is safe to recommend. Prefer this whenever a Kit token is present.
   - **No Kit (`fa` CLI):** Run `fa search --version <version> --query <your-guess> --page-size 10`. Results are at `data.searchPaginated.icons[]`, each with `id`, `label`, `unicode`, and `familyStylesByLicense`.
   - **Fallback:** Run `./scripts/search.py --version <version> --query <your-guess>` to find related icons from the Font Awesome GraphQL API. (This cannot scope to a Kit's subset.)

5. **Present the recommendation.** Pick the best match as your primary recommendation, and include relevant alternatives if the search turned up other good options. If a Kit is configured, every recommendation must be an icon that the Kit includes; if your best conceptual match isn't in the Kit, recommend the closest kit-available alternative and note that the missing icon can be added to the Kit at https://fontawesome.com/kits. Use a markdown table like this example:

   | Icon | Families | Availability |
   |------|----------|--------------|
   | `mug-saucer` | classic, sharp, duotone, sharp-duotone | Free |

   If the icon is pro-only, note that a Font Awesome subscription is required:

   | Icon | Families | Availability |
   |------|----------|--------------|
   | `album-collection` | classic, sharp, duotone, sharp-duotone | Pro (requires a [subscription](https://fontawesome.com/plans)) |

6. **Never provide bare SVG markup.** If the user asks for raw `<svg>` output of an icon, do not generate it from your own knowledge. Instead, direct them to use `/add-icon` which can fetch authoritative SVG markup from the Font Awesome API via `fa icons --svg-format`.

7. **Offer to add the icon.** After presenting your recommendation, ask the user: "Would you like me to add this icon to your code?" If they say yes or provide a location, invoke `/add-icon` with the recommended icon name (and location if given).
