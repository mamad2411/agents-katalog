---
name: prep-images-for-embed
description: Turn raw screenshots into embeddable, CDN-hosted images with real alt text — rename, resize, strip metadata, stage in a gitignored folder, upload to ImageKit, and emit SEO-correct markdown or HTML. Use whenever the user drops screenshots and wants them in a changelog entry, splash page, spec, or any markdown surface; whenever they say "add these screenshots", "put these images in the changelog", "upload these to the CDN", "make this post image-heavy"; whenever local image references need converting to CDN URLs; or whenever an image is destined for an og:image. Encodes the measured content-negotiation result (upload JPEG, never WebP — the WebP fallback is a PNG up to 3x larger), the alt-text-is-not-optional rule, the per-repo gitignored staging convention, and the naming scheme that makes filenames themselves carry SEO weight.
---

# Prep Images for Embed

> **The one thing to remember: upload JPEG, not WebP.** ImageKit converts to WebP
> for browsers that accept it *and* falls back to JPEG for those that don't.
> Upload WebP and the fallback becomes a **PNG up to 3× larger**. Measured, not
> assumed — see [Format](#format-upload-jpeg-always).

## When to use this skill

- The user drops screenshots and wants them in a changelog entry, splash page,
  spec, or any markdown surface
- "Add these screenshots", "put these in the changelog", "upload these"
- Local image references need converting to CDN URLs
- An image is destined to become an `og:image`
- Any markdown surface should become image-heavy without the user manually
  uploading and pasting links

## Why this exists

Screenshots arrive as `Screenshot 2026-08-14 at 9.11.31 PM.png` — 400KB of PNG
with a filename that is useless to a search engine and a reader. Getting one into
a changelog *properly* means renaming it, resizing it, stripping metadata,
hosting it somewhere with correct headers, and writing alt text. That's six steps
of tedium per image, which is why posts end up with no images at all.

This skill makes it one call.

**Prior art worth knowing:** `content-farm/plugin-modules/image-gin` already does
ImageKit upload — but from inside Obsidian, via a modal, on a note you have open.
This skill is the agent-callable path. The auth pattern here (`Basic
base64(privateKey + ':')`) is lifted from `image-gin`'s `imagekitService.ts`
deliberately, so the two don't diverge.

## Prerequisites

```bash
# ~/.secrets (chmod 600) — same pattern as generate-consistent-og-images
IMAGEKIT_PRIVATE_KEY="private_..."
IMAGEKIT_PUBLIC_KEY="public_..."
IMAGEKIT_URL_ENDPOINT="https://ik.imagekit.io/<id>"
```

Tooling: `sips` (macOS built-in) does resize and JPEG. `exiftool` strips
metadata. `cwebp` is only needed for the discouraged `--format webp` path.

## The call

```bash
node scripts/prep-images.mjs \
  --slug plane-first-deploy \
  --repo self-host-stack \
  --src "~/Desktop/Screenshot 2026-08-14 at 9.11.31 PM.png" \
  --name "Railway__Usage-By-Project" \
  --alt "Railway usage dashboard showing \$46.59 current usage broken out across six client projects" \
  --emit html
```

Batch by repeating `--src` / `--name` / `--alt` as ordered triples. Every source
needs its own name and alt — the script refuses otherwise, on purpose.

## The division of labour (this is the important part)

The script does the **mechanical** half. The agent does the **judgement** half,
and the judgement half is what makes the output worth anything:

| Agent decides | Script does |
|---|---|
| Which screenshots are worth including at all | Resize to max width |
| What each one is *of* → the `--name` descriptor | Strip EXIF |
| What it **shows** → the `--alt` text | Encode + compress |
| Where it goes in the prose | Stage, upload, return URL |
| Whether it needs to be an `og:image` | Emit markdown/HTML |

**Read every image before naming it.** You have vision; use it. A name derived
from the file's timestamp is worthless. A name derived from what is actually on
screen — `Railway__Usage-By-Project`, `Plane__Setup-Form`,
`Postiz__Memory-Breakdown--TWF` — makes the filename carry SEO weight and keeps
the CDN folder browsable six months later.

## Alt text is not optional

The script **rejects** alt text under 15 characters, and rejects anything opening
with `image`, `screenshot`, `photo`, `picture`, `graphic`, `untitled`, `tbd`, or
`todo`.

That is deliberate friction. `alt="screenshot"` is worse than no alt at all,
because it looks finished — it satisfies a linter while telling a screen-reader
user nothing and giving a search engine nothing.

**The test:** a reader who cannot see the image should learn the same thing a
viewer would.

```
✅ alt="Railway usage dashboard showing $46.59 current usage broken out across
       six client projects, with the-water-foundation highest at $14.87"

❌ alt="Railway screenshot"
❌ alt="dashboard"
❌ alt="image of the usage page"
```

Where the image is decorative and genuinely adds nothing — a divider, a texture —
it should carry `alt=""`, not bad alt text. But then ask whether it belongs at all.

## Format: upload JPEG, always

This is the finding that most changes behaviour, and it is measured on this
account, not inferred from docs.

ImageKit content-negotiates on `Accept`. What you upload determines the fallback:

| Uploaded as | Browser (accepts WebP) | Unfurler / older client |
|---|---|---|
| `.jpg` | **WebP, 43.5 KB** ✅ | **JPEG, 70 KB** ✅ |
| `.webp` | WebP, 47 KB | **PNG, 151 KB** ❌ |

Uploading JPEG wins on *both* paths. ImageKit's encoder beats hand-rolled
`cwebp` for the browser case, and the non-WebP fallback stays a sane JPEG
instead of ballooning into a PNG three times the size.

Uploading WebP is a trap that looks like an optimisation. The script defaults to
`jpg` and prints a warning if you force `webp`.

This also satisfies the **JPEG-over-WebP rule** in
[[open-graph-share-seo-geo]] — and its `og:image:type` invariant, since most
unfurlers will receive `image/jpeg`, matching a declared `image/jpeg`.

## Naming: BEM, Train-Case, ISO stamp last

```
Block__Element--Modifier_YYYYMMDDTHHMMSSZ.jpg

Plane__Work-Items--Empty_20260815T052358Z.jpg
Railway__Usage-By-Project_20260815T045242Z.jpg
Postiz__Memory-Breakdown--TWF_20260815T045242Z.jpg
```

This deliberately mirrors the house convention already in use for share imagery
(`ogimage__Lossless-At--Banner.jpg`, per [[generate-consistent-og-images]]) —
same BEM shape, same Train-Case segments. Do not fragment it.

**Separators, each meaning one thing:**

| | |
|---|---|
| `__` | block → element |
| `--` | element → modifier |
| `_` | fences the timestamp |
| `-` | word break inside a segment |

**Block is the subject, not the asset type.** `Plane`, `Railway`, `Postiz` — not
`Screenshot`. Everything in the folder is a screenshot, so spending the most
significant position on a constant wastes it.

### The case rule (one principle, both conventions)

> **Lowercase for generic type tokens. Train-Case for proper nouns and named
> things.**

That single rule explains both image conventions in this codebase, so neither is
an exception to be "fixed":

```
ogimage__Lossless-At--Banner.jpg
└─ type   └─ proper noun └─ named variant
   lower     Train-Case     Train-Case

Plane__Work-Items--Empty_20260815T052358Z.jpg
└─ product └─ named view └─ state
   Train-Case  Train-Case   Train-Case
```

`ogimage` is lowercase because it is a *kind of asset*, not a name. Screenshots
carry no type token at all — the subject occupies the block, and the folder
already says what they are.

Train-Case for the rest because these are proper nouns and named conventions, and
reading `Work-Items` beats parsing `work-items` at a glance.

**It is Title-Case, not capitalize-every-word.** Minor words — articles, short
prepositions, conjunctions — stay lowercase *unless* they lead or close a
segment. The capitalised words are the ones carrying meaning, which is the whole
point of the convention:

```
Image-of-Amy              not  Image-Of-Amy
Railway__Usage-by-Project not  Railway__Usage-By-Project
The-State-of-the-Art      not  The-State-Of-The-Art
A-Note-to-Self            not  A-Note-To-Self
```

Minor set: `a an and as at but by for from in nor of on or per so the to v vs
via with yet`. First and last word in a segment are always capitalised, even
when minor — `A-Note-to-Self` keeps its leading `A`.

The script applies this automatically, so pass `--name` however reads naturally
and let it normalise.

**On case-insensitive filesystems:** `Plane.jpg` and `plane.jpg` collide on APFS
but are distinct on the CDN — a real hazard in general, but not here. The script
generates the markdown reference from the same string it writes the file with, so
the case can never drift between them.

**Timestamp: ISO 8601 basic format, UTC.**

```
20260815T052358Z    ← basic format. This IS the standard, not a homemade variant.
2026-08-15T05:23:58Z  ← extended. Colons break URLs and Windows paths.
20260814-235021       ← local time, no offset. Ambiguous forever after.
```

Basic format exists precisely to solve separators-that-break-filenames. Use `T`
and `Z`; don't invent a lookalike. UTC because a local stamp with no offset can't
be resolved six months later and sorts wrongly against captures from another zone.

**Semantics first, timestamp last** is a deliberate trade. Filenames are a weak
ranking signal, so the meaningful part leads. The timestamp still buys
guaranteed uniqueness — which is what makes re-running safe, since two runs can
never collide on a live URL.

## Staging: per-repo and gitignored

Default is `<cwd>/.image-staging/`. Per-repo rather than global, so the processed
image sits next to the content that references it and the provenance is obvious.

**Add it to the repo's `.gitignore`.** The CDN is the source of truth for the
served bytes; the staging copy exists so a re-run doesn't re-download and so you
can eyeball what was uploaded. Committing them doubles the repo weight for no
benefit — the same reasoning that keeps `.ideogram-candidates/` PNGs out of git.

```gitignore
.image-staging/
```

## Emit modes

| `--emit` | Use when |
|---|---|
| `md` (default) | Plain markdown. Maximum portability. **No dimensions → expect layout shift.** |
| `lfm` | **Preferred on our own sites.** Emits `::image{src alt caption}` — the LFM directive rendered by `MarkdownImage.astro`, which also supports `source`, `source-url`, `float`, `caption-position`, `max-height`. |
| `html` | Renderer allows HTML. Includes `width`/`height` (prevents CLS), `loading="lazy"`, `decoding="async"`. |
| `figure` | The image needs a visible caption. Emits `<figure>` + `<figcaption>`. |
| `json` | You want the URLs and dimensions to place yourself. |

**On our own Astro Knots sites, prefer `lfm`.** Those sites do not use Astro's
markdown pipeline at all — LFM parses each entry and `src/components/markdown`
renders it, so the `::image{…}` directive is the richest target available
(captions, sourcing, float layout). Raw HTML also survives, via a `set:html`
fragment, so `html` works if you need dimensions.

**Elsewhere, prefer `html`.** Cumulative Layout Shift is a real ranking factor,
and plain `![](…)` gives the browser no way to reserve space — the page jumps as
each image loads. Use `md` only where the renderer strips HTML.

**Known gap, tracked not fixed:** neither LFM path emits intrinsic
`width`/`height`, so CLS is unsolved on our sites regardless of which you pick.
Latent while no changelog has images. See
[[Images-in-LFM-Render-Without-Intrinsic-Dimensions]].

## SEO checklist, beyond alt text

- **Dimensions on every `<img>`** — reserves space, kills CLS
- **`loading="lazy"`** below the fold; **omit it** for the first image (lazy-loading
  the LCP element makes the metric worse)
- **Responsive variants** via ImageKit transformations rather than re-uploads:
  `?tr=w-800` — one upload serves every breakpoint
- **Caption ≠ alt.** A `<figcaption>` is read *in addition to* alt text, not
  instead. Don't duplicate the string verbatim across both.
- **Don't use `title`** as a substitute for alt — it isn't announced reliably and
  doesn't show on touch devices

## Folder operations

ImageKit folders are created implicitly by the `folder` parameter on upload —
there is no need to pre-create them. What you do need is a way to see and clear
what is there:

```bash
node scripts/prep-images.mjs --list-folder  /self-host-stack/plane-first-deploy
node scripts/prep-images.mjs --purge-folder /self-host-stack/plane-first-deploy
```

`--purge-folder` is irreversible and deletes every file at that path. Use it for
clearing test uploads and abandoned drafts, not for anything published.

The folder path is derived, never passed per-call: `/<repo>/<slug>/`. That
mirrors where the content lives, so the CDN stays navigable and a whole entry's
imagery can be listed or cleared in one command.

## Gotchas

1. **`sips` cannot write WebP.** It handles resize and JPEG fine; WebP needs
   `cwebp` (`brew install webp`). Since JPEG is the recommendation, this rarely
   matters.
2. **Screenshots carry metadata.** Window titles, device identifiers, sometimes
   location. The script runs `exiftool -all=` before upload. Don't skip it on
   anything client-facing.
3. **Re-running is safe, because of the timestamp.** `useUniqueFileName=false` +
   `overwriteFile=true` would normally mean a re-run clobbers a live URL — that
   was true of an earlier `<slug>-<NN>-` scheme and was its worst property. The
   ISO stamp removes it: two runs produce two filenames, so nothing published can
   be overwritten. The cost is that repeated runs accumulate near-duplicates in
   the CDN folder; prune deliberately rather than relying on overwrite.
4. **Retina screenshots are 2×.** A "900px" macOS screenshot is often 1800px of
   pixels. The 1600px default is a reasonable ceiling for in-page content; raise
   it with `--width` when detail actually matters.
5. **The ImageKit folder is derived, not configurable per-call** —
   `/<repo>/<slug>/`. That is intentional: it mirrors where the content lives, so
   the CDN stays navigable.

## Related

- [[open-graph-share-seo-geo]] — where `og:image` should be hosted, the
  JPEG-over-WebP rule this skill's measurement confirms, and the
  `og:image:type`-must-match-bytes invariant
- [[generate-consistent-og-images]] — for *generating* share imagery; this skill
  is for *screenshots of real things*
- [[changelog-conventions]] — the surface these images most often land on
- [[maintain-splash-pages]] — the other main consumer
- `content-farm/plugin-modules/image-gin` — the Obsidian-side counterpart;
  `src/services/imagekitService.ts` is where the auth pattern comes from
