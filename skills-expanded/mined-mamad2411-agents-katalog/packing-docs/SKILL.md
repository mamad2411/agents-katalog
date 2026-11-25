---
name: packing-docs
description: Render the trip's packing documents — a one-page airport counter card of the binding allowances and bag weights, and a full per-bag packing list with tick boxes — as PDF via Typst and as Markdown, then deliver them by email, to cloud storage, into a static-site repo, or to disk. Use when the user asks for a packing list, a PDF, something to print, a page on their site, or to have the plan sent to them.
allowed-tools: Read, Write, Edit, Bash(typst *), Bash(python3 *), Bash(mkdir *), Bash(ls *), Bash(cp *), Bash(curl *), Bash(git status *), Bash(git add *), Bash(git commit *), Bash(git push *), Glob
---

# Packing Documents

`$TPA` below is this plugin's `new-workspace` skill directory — the folder holding its `SKILL.md`,
`scripts/`, `schema/`, `typst/` and `template/`. Find it by name in your tool's skills folder (some
tools prefix it, e.g. `travel-packing-assistant__new-workspace`) and set `TPA` once per session.

Renders `plan.yaml`, `allowances.yaml`, `bags.yaml` and `inventory.yaml` into two documents.

**The counter card** is one A4 page: the binding limits in large type, each bag's projected
weight against its allowance, the per-segment allowance table, and the excess-baggage prices.
It exists to be printed and read standing up, in a queue, with a bag on a scale. Its real job
is to let a traveller check a claim at the desk against the carrier's own published figure —
which is why every number on it carries the confidence and the date it was verified.

**The packing list** is the working document: bag by bag, cube by cube, with a tick column,
carriage markers for the cabin-only and checked-only items, and the not-packed list at the end.

## Rendering

Both renderers read the workspace YAML directly, so no number is transcribed by hand.
Transcription is where totals go wrong, and these totals are read at a check-in desk.

### PDF, with Typst

**Typst refuses to compile a source file that sits outside `--root`**, and a symlink does not
get around it. So the root has to contain both the template and the workspace, which means
`--root /` and absolute paths. This is the form to use — the obvious `--root .` from inside the
workspace fails, because the template lives in the plugin:

```bash
mkdir -p "$TRIP/output"

typst compile --root / \
  --input itinerary="$TRIP/itinerary.yaml" \
  --input allowances="$TRIP/allowances.yaml" \
  --input plan="$TRIP/plan.yaml" \
  "$TPA/typst/counter-card.typ" "$TRIP/output/counter-card.pdf"

typst compile --root / \
  --input itinerary="$TRIP/itinerary.yaml" \
  --input plan="$TRIP/plan.yaml" \
  --input bags="$TRIP/bags.yaml" \
  --input inventory="$TRIP/inventory.yaml" \
  "$TPA/typst/packing-list.typ" "$TRIP/output/packing-list.pdf"
```

To make a workspace renderable without the plugin installed, copy the templates in once
(`cp -r $TPA/typst "$TRIP/.typst"`) and then `--root .` works from inside the
workspace with `.typst/counter-card.typ`. Offer this when a trip repo is being handed to
someone else.

If `typst` is not installed, say so and give the install line for the user's platform rather
than silently producing only Markdown — the plain-text form is a fine substitute, but only if
they know that is what they got.

### Markdown

```bash
python3 "$TPA/scripts/render_markdown.py" "$TRIP" --doc both --out-dir "$TRIP/output"
```

`--doc counter-card | packing-list | both`, `--out FILE` for a single document, `--now ISO8601`
to pin the timestamp. `--frontmatter key=value` (repeatable) emits a YAML frontmatter block,
which is what a static site needs:

```bash
python3 "$TPA/scripts/render_markdown.py" "$TRIP" --doc counter-card \
  --frontmatter 'layout=../../layouts/Wiki.astro' --title 'Counter card — BOS → TLV'
```

`title` and `generated` are added automatically whenever frontmatter is requested; keys you
pass win over them.

### Both media must agree

The Typst templates and the Markdown renderer apply the same rule: where a bag has a scale
reading heavier than its itemised projection, the **reading** governs, and headroom and status
are recomputed against it rather than reprinted from `plan.yaml`. A bag can therefore show
`OVER` in the documents while `plan.yaml` still says `tight` — that is deliberate, and the
documents are the conservative view. If the PDF and the Markdown page ever disagree with each
other, that is a bug, not a rounding difference.

Check the output exists and is non-trivial in size before reporting success. A Typst compile
that fails on a missing field exits non-zero; a compile that succeeds against an empty
`plan.yaml` produces a valid, useless PDF.

## Delivery

Read `~/.config/travel-packing-assistant/delivery.yaml` if it exists:

```yaml
default: local                 # local | email | drive | repo
email:
  to: you@example.com
  from: null                   # required by some providers
drive:
  folder: "Travel/Packing"
repo:
  path: ~/repos/example/site   # an existing git working copy
  docs_dir: src/pages/wiki
  assets_dir: public/travel    # null to skip the PDFs
  format: markdown+pdf
  frontmatter:
    layout: ../../layouts/Wiki.astro
  commit: true
  push: false
print: false
```

That file lives outside the plugin and outside the workspace deliberately: it survives
`/plugin update`, and it never gets committed to a trip repo. If it does not exist, save to
`output/` and offer to create it.

**Local** — the default when nothing is configured. Save to `output/`, report the absolute
paths.

**Email** — send to the configured address with both PDFs attached. Sending mail leaves this
machine, so say what is being sent and to whom before sending it. With the Gmail/Workspace MCP,
attachments above roughly 100 KB should go by URL rather than inline base64: presign a PUT to a
transient object store, upload the file, presign a GET, pass that URL as the attachment, and
delete the staged object afterwards. Base64ing a PDF into tool arguments works for small files
and wastes a great deal of context on larger ones.

**Drive / cloud storage** — upload to the configured folder. Never write to the root of a
drive; if the configured folder does not exist, ask rather than picking one.

**Repo** — copy the finished documents into an existing git working copy, typically a static
site, so the packing list becomes a page readable on a phone rather than a PDF that has to
have been downloaded. Markdown goes to `docs_dir`, PDFs to `assets_dir`, named
`packing-<trip-id>-counter-card.*` and `packing-<trip-id>-list.*` so trips coexist and a
re-render overwrites its own pages.

Write only into those two directories. Do not edit the site's index, navigation or README to
link the new page — say it needs linking and let the user do it. A delivery step that edits a
site's structure is a delivery step that breaks the site.

**Pushing is publishing.** `push` defaults to `false`. A repo wired to a host builds on push,
so a push is a deploy, and a deploy makes the document reachable by anyone who can reach the
site — a private repo is not the same as a private site. Confirm before every push, separately
each time.

That caution is sharper for this document than for most: a packing list states the dates a home
will be empty and enumerates what is worth taking from it, and the counter card names the
flights. Before the first push to any site, establish what actually guards it. If the answer is
nothing, publish the counter card if the user wants and keep the packing list local.

## Timing

Offer to render at two moments and not otherwise:

- When the plan is final, before packing starts — the list is for use while packing.
- The evening before departure, after the last weigh-in — the counter card should carry the
  actual final weights, not the projected ones.

A counter card rendered from a provisional plan must say `PROVISIONAL` on it. The templates do
that automatically when `plan.yaml` carries warnings; do not strip the warnings to get a
cleaner-looking document.
