---
name: release-visual
description: Generate the self-host release announcement visual when preparing a release or announcing newly added Apps. Discover added Apps between refs and render the approved Logo hub with pulses, rather than inventing a new layout.
---

# Release visual

Read `docs/releasing.md` for publication and `video/reel/release/README.md`
for renderer requirements. This skill prepares assets; publishing a release
still requires the user's approval.

## Discover

Confirm the release version, target ref and previous published stable CLI tag
with `gh release list` and `git log`. Use the highest stable CLI release with
binary archives, not the legacy skill-pack tags or the `new-cli-` twin.
Fetch the refs before comparing them.

From the repository root, run:

```bash
jq -r '.apps[].id' site/src/data/catalog.json | grep -Fx -f - <(bash scripts/release-new-apps.sh <previous-tag> <target-ref>)
```

The script also lists Apps hidden from the Catalog; the filter keeps only
Catalog Apps, which the renderer requires. Use exactly the filtered App ids and
their count. An empty result means no new-Apps visual:
report that and continue with ordinary release notes. Do not substitute sample
Apps or announce existing Apps as new.

## Render

Work from the target ref so the Catalog and release agree. Read the renderer's
README for its existing dependencies; reuse the installed toolchain.
For 1 to 24 new Apps, run from `video/reel`:

```bash
npm run release-visual -- --apps <comma-separated-ids> --version X.Y.Z --out <absolute-output-directory>
```

Up to six Apps render as one column; 7 to 24 render as a grid of up to six
rows and four columns. Only for more than 24, split the ids into groups of at
most 24 in separate output directories and rename each pair with a group
suffix. Keep all Apps represented once. Keep renders outside tracked source
files, except the SVG committed for embedding below.

Check that the PNG and animated SVG exist, show the correct version and every
selected App, and have readable labels. Preview the SVG through a local server
when visual verification is authorized; check its reduced-motion fallback.
Stop on a missing icon or unknown App rather than replacing it silently; add
the icon to `video/reel/assets/icons/` from the Dashboard Icons commit pinned in
`site/src/lib/catalog.ts`, and run the web gate because the site's share images
use the same folder. The approved design is the Logo hub, with pulses to the
new Apps and along each grid row.

## Embed

Release assets download as `application/octet-stream`, so an uploaded SVG never
animates in the notes. Commit the SVG to `docs/assets/releases/` in a PR and,
after it merges, embed it from `raw.githubusercontent.com` pinned to that commit,
linked to the PNG uploaded as a release asset. The renderer README has the exact
Markdown. Use descriptive alt text listing the new Apps and preserve the rest
of the release notes. Private repository assets require an authorized viewer; do not
claim anonymous availability. Download the uploaded files and compare them
with the originals before publishing, following `docs/releasing.md`.

Finish with the App ids, generated file paths, release link if published, and
any presentation check that could not be completed.
