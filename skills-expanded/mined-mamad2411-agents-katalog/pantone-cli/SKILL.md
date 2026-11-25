---
name: pantone-cli
description: Match HEX, RGB, or Lab colors to the closest Pantone colors offline using the pantone-cli command-line tool. This skill should be used when a user asks for the closest Pantone color or code for a given color, Pantone equivalents of brand colors, medium-specific Pantone picks (coated or uncoated paper, textiles, cotton, polyester, product design, CMYK process), or for shades and color harmonies of a Pantone color. Requires no API key; after a one-time index download (pantone-cli fetch-index), matching runs fully offline.
license: MIT
---

# pantone-cli — Offline Pantone Color Matching

## Overview

`pantone-cli` matches an input color (HEX or CIELAB) against an offline Pantone index and returns the closest color in each Pantone book, with a CIEDE2000 (Delta E00) distance, book metadata (intended use and physical medium), and optional shades and harmonies. Matching runs entirely offline from a locally installed index.

Run it with `npx` (Node 20+) — no install or configuration needed:

```bash
npx -y pantone-cli match "#0014DC" --json --no-relationships
```

`bunx pantone-cli` and a global install (`npm i -g pantone-cli`) work the same way.

If a command fails with "Could not find a Pantone match index", install the index once (a small sha256-verified download; it persists in the user's home directory for all future runs):

```bash
npx -y pantone-cli fetch-index
```

## When to Use

- "What's the closest Pantone to `#0014DC`?" — or to an RGB or Lab value.
- "Convert our brand colors to Pantone for print / packaging / textiles."
- "Which Pantone code should I use on uncoated paper vs. cotton fabric?"
- "Give me shades or harmonies for this color."

Do not guess Pantone codes from memory. Trained knowledge of Pantone mappings is unreliable; always run the tool.

## How to Use

### 1. Choose books for the target medium

The same input color maps to different Pantone codes depending on the physical medium. If the user's intent implies a medium, filter with `--books`; otherwise match across all books and organize the answer by medium.

| Book ID | Best for | Medium assumption |
| --- | --- | --- |
| `pantoneSolidCoated` | Graphic design | Spot ink on coated paper |
| `pantoneSolidUncoated` | Graphic design | Spot ink on uncoated paper |
| `pantoneCmykCoated` / `pantoneCmykUncoated` | Graphic design | CMYK process ink |
| `pantoneColorBridgeCoated` / `...Uncoated` | Spot vs. process comparison | Both, side by side |
| `pantoneFhCottonTcx` | Fashion, textiles, soft home | Dye on cotton (TCX codes) |
| `pantoneFhiPolyesterTsx` | Fashion, activewear | Dye on polyester (TSX codes) |
| `pantoneFhiPaperTpg` | Product design | Lacquer on paper (TPG codes) |
| `pantoneSkinToneGuide` | Skin tone reference | SkinTone guide |

To discover all books (IDs, uses, media, color counts):

```bash
npx -y pantone-cli books --json
npx -y pantone-cli books --search textile
```

### 2. Match

```bash
# HEX input (always quote it — unquoted # starts a shell comment)
npx -y pantone-cli match "#0014DC" --books pantoneSolidCoated,pantoneSolidUncoated --json --no-relationships

# Lab input (D50), e.g. from a design tool
npx -y pantone-cli match --lab 33.31 23.24 -58.02 --json --no-relationships

# Several candidates per book instead of one
npx -y pantone-cli match "#0014DC" --top 3 --json --no-relationships
```

For RGB input, convert to HEX first (e.g. `rgb(0, 20, 220)` → `#0014DC`).

Flags that matter for agents:

- `--json` — machine-readable output. Prefer it; the default text output contains ANSI color codes (or pass `--no-color`).
- `--no-relationships` — omit shades/harmonies for compact output. Drop this flag when the user wants shades or harmonies: `results[].relationships.shades` groups related colors by hue/lightness/saturation, and `results[].relationships.harmonies` lists analogous, complementary, monochromatic, split-complementary, triadic, and tetradic colors.
- `--books` — comma-separated exact book IDs (camelCase, from `books`).

### 3. Interpret and report

Key JSON fields per entry in `results[]`: `color.code` (the Pantone code, e.g. `Blue 072 U`), `color.name`, `color.hex`, `color.lab`, `deltaE` (CIEDE2000 distance), `book.id`, `book.info.en.target` (intended use), `book.info.en.description` (medium).

Always report the Delta E00 number alongside the code. Rough perceptual scale:

| Delta E00 | Meaning |
| --- | --- |
| < 1 | Not perceptible to the human eye |
| 1–2 | Perceptible on close inspection |
| 2–4 | Noticeable difference |
| 4–10 | Clearly different color |
| > 10 | No good match in this book — say so |

In the answer, include: Pantone code, name, HEX, Delta E00, and the book's intended use/medium. When matching across multiple books, group by medium so the user can pick the code for their use case.

## Required Disclaimer

When reporting matches, state that matching uses CIEDE2000 against offline Lab values and is an approximation — not a substitute for Pantone Connect, physical Pantone guides, or official Pantone production guidance. For production-critical color decisions, recommend verifying against a physical guide.
