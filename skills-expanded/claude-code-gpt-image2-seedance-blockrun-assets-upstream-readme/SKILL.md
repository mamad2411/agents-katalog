# Archived upstream images

## Why this directory exists

This bundle's case library was built by curating five public "awesome" prompt
lists. Four of them are still online, and their images are hotlinked from their
own repos — nothing is copied here.

The fifth, **`EvoLinkAI/awesome-gpt-image-2-prompts`**, was **deleted from
GitHub** after this bundle was built. Every one of its `raw.githubusercontent.com`
image URLs now returns 404, which broke 697 image references across this repo's
README, `GALLERY.md`, and 300 case files.

`evolinkai/` holds an archived copy of those 283 images so the case library
stays readable. They were recovered from the local download cache that
`scripts/build_cover.py` populated while building the README cover mosaic —
as far as we know this is the only surviving public copy.

## Attribution

**These images are not ours.** Each was created by an individual artist and
originally posted to X/Twitter; `EvoLinkAI/awesome-gpt-image-2-prompts` merely
aggregated them, and this directory merely preserves that aggregation.

Every image maps to a case file under
[`prompts/case-library/from-awesome-gpt-image-2-prompts/`](../../prompts/case-library/from-awesome-gpt-image-2-prompts/)
that names the creator and links to the original post. Filenames match the
upstream slug, so `evolinkai/poster_case123.jpg` came from
`.../images/poster_case123/output.jpg` and is documented in the case file
whose title carries the same case number.

**If you are the creator of one of these images and would like it removed,
open an issue or email the maintainer — it will be taken down promptly, no
questions asked.** The prompt text and your attribution will stay; only the
image goes.

## Processing

Recovered images were resized to a **720px long edge at JPEG q80** (from an
average of ~1024px) and stripped of metadata, to keep the repository clone
weight reasonable. 57.6 MB of originals became 20.4 MB. No cropping, no
retouching, no watermark removal — the only change is scale and compression.

## Not archived

`EvoLinkAI/awesome-seedance-2-guide` was also deleted. It contributed 63 case
files but no images, so there is nothing to preserve here — those prompts live
on in the case library with their original attribution intact.
