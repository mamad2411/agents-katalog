---
name: generate-alts
description: Write alt text for the images in the Sanity dataset. A script lists every image usage (document, field, current alt, the asset's title/description/alt text, a caption, the section heading and the text around it), downloads one small preview per asset into a local cache (`.alts/`, never the same image twice), the agent looks at each image and proposes one alt per usage in the site's content language (or marks it decorative), then the script builds an HTML page where the user reviews, edits and approves them and exports `approved.json`; approved alts go into drafts with a dry-run-first script (`--apply` to write). Use when the user asks to "generate/write/fill alt texts", "images without alt", "alt audit", "accessibility of images", "describe our images", after a content import or migration, or before an accessibility or SEO review. Works on Nexity projects (`img` objects) and on similar Sanity sites.
---

# Generate alt texts

Flow: **scan → fetch → describe → report → the user reviews → apply (dry run, then
`--apply`) → scan again.** Nothing is written to the dataset before the user has approved
the alts in the report and said go.

## What the site reads

Every image in the starter is an `img` object (`studio/src/sanity/schemaTypes/objects/img.tsx`):
`image` (the asset, `image.asset._ref`), `responsive[]` (art-directed variants that share
the same alt) and **`alt`**. The web component (`web/src/ui/components/image/index.tsx`)
renders `alt` prop `||` `img.alt` `||` `image.asset->altText` `||` `""`:

| Where | What counts |
|---|---|
| Sections, document fields (`post.coverImage`, `case-study.image`/`logo`, `author.avatar`, `site.logo`, …) | `img.alt`, then the asset's `altText` |
| Rich-text images (`img` blocks in `richText`/`pageRichText`, callout background, pullquote avatar, video poster) | Only `img.alt`: `RICHTEXT_QUERY` does not expand the asset |
| `metadata.image` (social sharing) | Not on the page; `alt ?? asset.altText` goes into the JSON-LD graph (`web/src/lib/schema-org/route-graph.ts`) |
| Markdown twins (`/x.md`) | `img.alt` (`imageHint`) |

So **the script writes `img.alt` on the usage only.** The asset's `altText` stays as it is:
one asset serves many contexts, an asset document has no draft (a write is live at once),
and rich-text images never read it. Keep in mind the fallback the other way: an **empty**
`img.alt` shows the asset's `altText`, so an image can only render as decorative when the
asset has no `altText` either. The report and `apply` warn about those.

Asset `title`, `description`, `altText` and `creditLine` (`sanity.imageAsset`, set in the
Studio's media browser or the Media Library) are **inputs** for the proposal, never the
answer on their own.

## The script

`scripts/alts.mjs` (logic in `scripts/lib.mjs`, the page in `scripts/report.mjs`), plain
Node ESM, no extra packages. **Run it from the starter's `web/` folder**: it loads
`@sanity/client` and `dotenv` from there and reads `web/.env.local`, then `web/.env`.

```bash
ALTS=../.agents/skills/generate-alts/scripts/alts.mjs
node $ALTS scan                       # manifest + counts
node $ALTS fetch                      # one preview per asset, cached
node $ALTS batches [--size=12]        # work packages for the describe step
node $ALTS report [--embed]           # merge proposals, write report.html
node $ALTS apply --file=<approved.json> [--apply] [--live]
node $ALTS --help                     # every option
```

| Argument / env | Meaning |
|---|---|
| `--include-existing` | `fetch`/`batches` also take images that already have an alt (to review their quality). Default: only missing and decorative ones |
| `--lang=` | Content language. Default: `<html lang>` in `web/src/app/(frontend)/layout.tsx` |
| `--studio=` | Studio URL for the report's links. Default: `NEXT_PUBLIC_BASE_URL` + `/admin`, else `http://localhost:3000/admin` |
| `--dir=` | Working folder, default `../.alts` (the project root) |
| `--dataset=` | Overrides `NEXT_PUBLIC_SANITY_DATASET` |
| `NEXT_PUBLIC_SANITY_PROJECT_ID`, `NEXT_PUBLIC_SANITY_DATASET` | Required for `scan` and `apply` |
| `SANITY_API_READ_TOKEN` | Without any token drafts are invisible |
| `SANITY_API_WRITE_TOKEN` (or `SANITY_API_TOKEN`) | Editor token, required for `apply --apply` |

Never read or print an `.env` file or a token; the script says what is missing. Creating a
token and writing to a production dataset are the user's calls.

### The `.alts/` folder

Local working state, not content. It belongs in the project's `.gitignore` (`/.alts/`);
add the line if it is missing.

| File | Written by | Holds |
|---|---|---|
| `manifest.json` | `scan` | Every usage: key `<documentId>#<path>`, document type and title, slug, `altPath`, field label (`sections › hero › image`), asset id, current alt (per draft/published), status, a field hint, context (section heading, nearby fields, rich-text paragraph before/after, caption), a context hash; plus the asset metadata |
| `images/<assetId>.<ext>` | `fetch` | A 640 px preview from the Sanity image CDN (`?w=640&fit=max&fm=jpg`, PNG when the asset has transparency, SVG as is). Asset ids are content hashes, so a cached file never goes stale |
| `cache.json` | `fetch`, `report`, `apply` | Per asset: the preview file and a context-free alt. Per usage: the proposal with the asset id and context hash it was made for, and `appliedAt` |
| `batches/batch-NN.json` | `batches` | Usages without a valid cached proposal, grouped so all usages of one asset sit in the same batch |
| `proposals/batch-NN.json` | the agent | Proposals for a batch; `report` merges them into `cache.json` and moves them to `proposals/merged/` |
| `report.html` | `report` | The review page |

A cached proposal is reused as long as the usage still shows the same asset with the same
context (heading, nearby text, caption, asset metadata). Change any of them and the usage
comes back in the next `batches`.

## Step 1: scan

Run `scan` and report the counts: usages, assets, documents, **missing**, **has alt**,
**decorative** (empty, and either a decorative field such as a background, or decided
earlier), fields without an alt, and missing alts by document type. If it warns that
there was no token, ask for a read token first: draft-only images would be missing.

Settle the **content language**. The script's guess comes from `<html lang>`; check it
against the actual copy and `BRAND.md` (voice, product names, terms the brand uses). The
alt is written in the language of the page it sits on. A multilingual project (a
`language` field, per-locale documents) needs one language per document: say so and
take it from the document.

Ask the user what the run covers: only missing alts (default), or existing ones too
(`--include-existing`), and whether to limit it to some document types (edit the batch
list, or run in rounds).

## Step 2: fetch

`fetch` downloads the previews for the selected usages, six at a time, and skips what is
already in `images/`. Re-runs are cheap. Failures are usually deleted assets; they stay
in the list without a preview.

## Step 3: describe

`batches` writes the work packages and prints them. Each batch has `lang`, the target
`proposalsFile`, and per asset the preview's absolute path, metadata and any cached
context-free alt, then the usages with their context.

- **Agents with subagents:** hand each batch to the `alt-text-writer` agent
  (`.agents/agents/alt-text-writer.md`), several in parallel, each with the batch file
  path. It reads the images and returns the proposals JSON; write it to the batch's
  `proposalsFile` unchanged. Images are expensive in context, which is why this runs in
  subagents.
- **Agents without subagents:** work through the batches one by one yourself: open each
  preview, write the proposals file, move on. For many images, do a few batches, run
  `report` so the user can check the tone early, then continue.

Proposals file:

```json
{
  "assets": {
    "image-<sha>-800x600-jpg": { "alt": "Two people reviewing a pipeline chart on a laptop" }
  },
  "usages": [
    {
      "key": "<documentId>#<path>",
      "alt": "Sales team reviewing the quarterly pipeline chart",
      "decorative": false,
      "reason": "Hero image next to the forecasting headline",
      "sources": ["image", "asset.title", "section heading"]
    }
  ]
}
```

`assets.*.alt` is a short, context-free description of what the image shows, kept in the
cache so the next usage of the same asset starts from it. Each `usages[]` entry is the alt
for that one place. `sources` lists what the alt is based on: `image`, `asset.title`,
`asset.description`, `asset.altText`, `caption`, `section heading`, `nearby text`,
`document title`, `field hint`.

### Writing the alts

The alt says what the image **contributes on that page**, for someone who cannot see it.

1. **Look at the image first**, then read the metadata and context. Asset title,
   description and filename are often wrong or stock captions: use them for names
   (people, products, places, customers), not as a description.
2. **Content language** of the page (`lang`), in the brand's terms from `BRAND.md`.
3. **Short:** one phrase or sentence, usually under ~125 characters, no full stop needed
   for a phrase. Don't start with "Image of", "Photo of", "Picture showing"; the screen
   reader already says it is an image. Say "Screenshot", "Illustration" or "Chart" only
   when the medium matters.
4. **No keyword stuffing**, no marketing claims the image doesn't show, no file names.
5. **Context decides the content.** The same team photo is "Our support team in the Berlin
   office" on the About page and can be decorative next to a quote that already names
   them. A product screenshot names the screen and what it shows ("Forecast dashboard with
   deals grouped by risk"), not every number on it.
6. **Text in the image** (a chart title, a quote card, a sign) goes into the alt when it
   carries the message. A chart: what it shows and the takeaway, not the full data.
7. **Don't repeat the adjacent text.** If the caption or the heading next to it already
   says it, describe what it adds, or mark the image decorative. Never copy the caption
   verbatim.
8. **Logos:** the organization's name only ("Acme"), not "Acme logo". A logo inside the
   home link: the company name. A logo next to the same name in text: decorative.
9. **People:** the name and role when the context gives it; otherwise describe without
   guessing identity, age, ethnicity or other sensitive traits.
10. **Decorative** (`"decorative": true`, `"alt": ""`, a `reason`): backgrounds,
    textures, dividers, faint wordmarks, avatars right beside the person's name, icons
    next to a label that says the same. The field `hint` in the batch marks the usual
    ones; it is a hint, not a rule.
11. **Existing alts** (`--include-existing`): keep a good one (propose it unchanged) rather
    than rewording it for the sake of it; the review then shows no change.

## Step 4: report and review

Run `report` and give the user the path of `.alts/report.html` (`--embed` puts the
previews inside the file, to send it to someone). Each card shows the preview (click for
the original), the document and a Studio link, the field, the current alt, the asset
metadata, the context, the proposal and why, and warnings (filler words, too long, repeats
the caption, replaces an existing alt, decorative but the asset's `altText` will show).

The user edits the text, ticks **Decorative** or **Approve**, and clicks **Download
approved.json** (or **Copy JSON**). Proposals that fill an empty alt and have no warnings
start approved; anything that replaces an existing alt starts unapproved. Edits are kept
in the browser's local storage until the next scan.

## Step 5: apply

Ask where the file is (usually the Downloads folder; moving it to `.alts/approved.json`
is tidy), then always show the dry run first and read it back in short: how many alts, in
how many documents, how many new drafts, what is skipped and why.

```bash
node $ALTS apply --file=../.alts/approved.json            # dry run, writes nothing
node $ALTS apply --file=../.alts/approved.json --apply    # writes
```

Then ask: **run it yourself, or should I run it?** If the user runs it, give the exact
command from `web/` and suggest the `! <command>` prefix so the output lands in the
conversation. On a production dataset suggest a backup first:
`pnpm exec sanity dataset export <dataset> backup.tar.gz` from `studio/`.

What `apply` does:

- **Writes to drafts.** A document with an open draft gets the alt in the draft (guarded by
  its revision); a published document without one gets a new draft copied from it, with
  the alt set. An editor reviews and publishes in the Studio. Release versions are never
  touched.
- **`--live`** (only when the user asks for it): patches the published document **and** its
  open draft, so publishing the draft later doesn't bring the old alt back. The revalidate
  webhook updates the site like a Studio publish.
- **Never replaces an alt that wasn't approved.** An empty alt is filled; a non-empty one is
  replaced only when the user approved that card (`overwrite`) **and** it still is the alt
  they saw. Changed since the review, replaced image, image moved: skipped and listed.
- Writes only `<path>.alt`; nothing else in the document changes. One transaction per
  document. Records `appliedAt` in `cache.json`.

## Step 6: verify

Run `scan` again. Missing should drop by the number written (drafts count, because the scan
prefers the draft). Tell the user how many new drafts wait to be published, with their
document types.

| Symptom | Likely cause | What to do |
|---|---|---|
| `document changed since it was read` | Someone edited the draft during the run | Re-run `apply`; done items are skipped as `already set` |
| 401 / 403 / permission | Viewer token, expired, or another project | The user creates an Editor token as `SANITY_API_WRITE_TOKEN` |
| `The file is for dataset …` | `approved.json` came from another dataset | `--dataset=` to match, or re-scan the right one |
| Count unchanged | Dry run (no `--apply`) | Compare the header lines |
| Decorative image still has an alt on the site | The asset has `altText` and the empty field falls back to it | Clear the asset's alt text in the Studio's media browser, if no other usage needs it |
| An image type is never found | A project-specific image object without `image.asset` | Extend `findImageUsages` in `scripts/lib.mjs` |
| A field gets the wrong hint | Hints match field names | Edit `FIELD_HINTS` at the top of `scripts/lib.mjs` |

## Report back

The dataset and language, counts before (missing / has alt / decorative), how many
proposals and how many approved, what was written (alts, documents, new drafts) and
skipped with reasons, the counts after, and what is left: drafts to publish, decorative
images blocked by an asset `altText`, fields without an alt.
