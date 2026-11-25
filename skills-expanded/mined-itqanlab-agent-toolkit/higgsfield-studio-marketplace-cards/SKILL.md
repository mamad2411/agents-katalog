---
name: higgsfield-studio-marketplace-cards
description: "Make marketplace listing images with Higgsfield: a compliant main image, secondary product images and A+ content modules. Triggers: 'marketplace listing images', 'main image for my listing', 'product infographic', 'A+ content for this product', 'secondary images for my store listing', 'full marketplace image set'. Part of Higgsfield Studio: the whole set is planned and priced for free before any image is made, and every job is written to a ledger. Needs Node 18+ and the higgsfield command line tool."
license: MIT
compatibility: "Requires Node 18 or newer and the Higgsfield command line tool, through the higgsfield-studio skill in the same plugin. Needs network access and a Higgsfield account. Generating spends its credits."
metadata:
  author: itqanlab
  version: 1.1.0
  category: media
  display: "Higgsfield Marketplace Cards"
  short: "Marketplace listing images, priced up front"
  starter: "make the main listing image for this product photo"
---

# Higgsfield Marketplace Cards

Higgsfield keeps the marketplace rules and templates on its side, plans each card and renders it. The guard plans the set first with Higgsfield's free `--enhance-only` step and prices every planned image before anything is made.

## What it costs

Scopes differ a lot in size: `main` is 1 image, `product-images` is 6, `aplus` is 8 and `full-set` is 13. Each card is one image job (Higgsfield's guide says `nano_banana_2`, quoted at 2 credits on 2026-10-12), so a full set is roughly 26 credits or more. Always price the scope with `--dry` and start with `main`.

```
node ../higgsfield-studio/scripts/hf.mjs cards --scope main --prompt "sparkling peach lemonade can" --image can.png --dry
```

## Before anything else

```
sh ../higgsfield-studio/scripts/setup-deps.sh --check
node ../higgsfield-studio/scripts/hf.mjs check
```

The first checks Node and the `higgsfield` tool, and `sh ../higgsfield-studio/scripts/setup-deps.sh` installs what is missing after asking. The second checks the sign-in. If Higgsfield is not signed in, the user signs in once with `higgsfield auth login`, which opens the browser. Never print the sign-in token or open the CLI's credential file.

## Spending credits

This skill is part of the Higgsfield Studio plugin. Every paid command runs through the main skill's guard, `node ../higgsfield-studio/scripts/hf.mjs`. It asks Higgsfield for the price before running, refuses above `--max` or below the reserve, never pays twice for the same request, and writes what each job really cost to `.higgsfield/ledger.jsonl` in the project. The full rules are in `../higgsfield-studio/SKILL.md`. The short form:

- Price first with `--dry`, using every parameter the real job will use. Tell the user the total for anything over about 5 credits.
- Put `--max N` (a little above the price), `--tag` and `--why "..."` on every paid job.
- Ask before spending more than about 10 credits, or 10% of what is left. `node ../higgsfield-studio/scripts/hf.mjs account` shows the balance.
- Anything outward or not undoable goes through `act` and needs `--yes`. Say what will happen and wait for the user's yes before adding it.
- Report in plain words, in the user's language: where the file is, what it cost, what is left. No JSON or job ids unless asked.

Free commands, such as lists, `model get`, presets and uploads, can run as `node ../higgsfield-studio/scripts/hf.mjs run <command>` or as `higgsfield <command>` directly.

## Updates

This skill is versioned with its plugin. Its version is `metadata.version` in the header of this file. The plugin's history, for every skill in it, is in `../higgsfield-studio/CHANGELOG.md`. To check for a newer version, open the address on its `Latest:` line and compare the top version with this one. Read every entry in between and tell the user what changed before anything is updated.

## Higgsfield's guide

Everything below is Higgsfield's official guide for this task, with its paid and outward commands already pointed at `node ../higgsfield-studio/scripts/hf.mjs`. The rules above win where the two differ.

# Marketplace Cards

Create marketplace-ready product visuals with `node ../higgsfield-studio/scripts/hf.mjs cards`.
The CLI first calls the backend enhancer, where marketplace rules and templates are kept private, then creates `nano_banana_2` jobs and prints result URLs.

## Bootstrap

1. If `higgsfield` is not on `$PATH`, install it by running the official installer with Bash: `sh ../higgsfield-studio/scripts/setup-deps.sh`.
2. If `higgsfield account status` fails with authentication errors, ask the user to run `higgsfield auth login`.

## UX Rules

1. Respond in the user's language.
2. Ask at most one concise confirmation question before running.
3. Prefer a product image. If the user provides only text or a URL, proceed only when the product details are clear.
4. Do not write final image-generation prompts yourself. Backend enhancement owns that.
5. Final answer should contain only the ready image URLs and short labels.

## Scope Selection

Use `--scope` when the user asks for a common bundle:

| Scope | Creates |
|---|---|
| `main` | 1 marketplace main image |
| `product-images` | main image + 5 secondary images |
| `aplus` | main image + 7 A+ modules |
| `full-set` | main image + 5 secondary images + 7 A+ modules |

Use repeated `--asset` only for custom subsets:

- `main_image`
- `infographic`
- `multi_angle`
- `detail_shot`
- `lifestyle`
- `whats_in_box`
- `aplus_hero_banner`
- `aplus_pain_points`
- `aplus_features`
- `aplus_ingredients`
- `aplus_efficacy`
- `aplus_how_to_use`
- `aplus_endorsement`

## Command

Build and run one `node ../higgsfield-studio/scripts/hf.mjs cards` command from the user's request.

For common bundles, use `--scope <main|product-images|aplus|full-set>`, `--prompt "<short product and listing intent>"`, optional repeated `--image <path-or-upload-id>`, and optional context flags: `--product_context`, `--brand_context`, `--category`, `--visual_style`.

Examples to mirror when choosing arguments:

- Product images: `node ../higgsfield-studio/scripts/hf.mjs cards --scope product-images --prompt "sparkling peach lemonade can for marketplace listing" --image ./can.png --category "beverage"`
- Full set: `node ../higgsfield-studio/scripts/hf.mjs cards --scope full-set --prompt "premium skincare serum, clean clinical marketplace visual system" --image ./serum.jpg --brand_context "minimal white and sage palette"`
- Custom subset: repeat `--asset`, for example `--asset main_image --asset infographic --asset lifestyle`.
- Existing completed main image job: use `--main-job <completed_main_job_id>` with the requested secondary or A+ `--asset` values.

## Delivery

Print URLs with labels:

```text
Marketplace cards ready:
- Main image: https://...
- Infographic: https://...
- Lifestyle: https://...
```

Avoid JSON, job IDs, internal model names, or enhanced prompt text unless the user explicitly asks.
