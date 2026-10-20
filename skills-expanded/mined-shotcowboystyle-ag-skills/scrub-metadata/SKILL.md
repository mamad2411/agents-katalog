---
name: scrub-metadata
description: Strip EXIF / IPTC / XMP metadata from images using exiftool. Use when the user wants to remove identifying metadata (GPS, camera, timestamps, thumbnails) from a single image, a folder, or a recursive tree before sharing or publishing. Supports preview, backup-first, whitelist of fields to keep (e.g. Orientation), and recursive operation. Logs each run to notes/.
allowed-tools: Bash(exiftool *), Bash(command *), Bash(mkdir *), Bash(cp *), Bash(test *), Bash(dirname *), Bash(mktemp *), Bash(find *), Bash(wc *), Bash(date *), Read, Write
---

# Scrub Image Metadata

Remove EXIF / IPTC / XMP metadata from images in place (or to a copy), with preview and logging. Wraps `exiftool` — do not hand-roll metadata parsing.

## When to use

- Before publishing photos to a public blog, social media, or client deliverable.
- Bulk-cleaning an archive that may contain GPS or serial-number metadata.
- Preparing reference images for distribution where only orientation should be preserved.

## Procedure

### 1. Establish scope

Ask the user (and confirm before touching files):

- **Target path** — single file, folder, or recursive tree. Default: current working directory.
- **Recursive?** If the target is a folder, ask whether to descend into sub-folders. Default **no** (flat, current folder only) unless the user says "recursive" or supplies a root.
- **Backup first?** Default **yes** — `exiftool` keeps `_original` sidecars automatically, but offer an explicit `backup/` copy for the nervous case.
- **Whitelist** — fields to preserve. Common sensible default: keep `Orientation` so the image renders right-way-up. Ask if the user wants to preserve anything else (ColorSpace, ICC profile, copyright).
- **Dry run vs apply** — always preview first.

### 2. Check tooling

```bash
command -v exiftool >/dev/null || {
  echo "exiftool not installed — see the image-ops-install-deps skill" >&2
  exit 1
}
```

### 3. Preview what will be stripped

Set the depth limit once, from the answer to "recursive?" in step 1:

```bash
maxdepth="-maxdepth 1"   # non-recursive
maxdepth=""              # recursive — omit the flag entirely
```

Then run a read-only pass and show the user a summary:

```bash
# Show metadata currently present on a sample file
exiftool -G1 -a -s "$sample"

# Count files that would be touched
find "$TARGET" $maxdepth -type f \
  \( -iname '*.jpg' -o -iname '*.jpeg' -o -iname '*.png' \
     -o -iname '*.heic' -o -iname '*.webp' -o -iname '*.tif' \
     -o -iname '*.tiff' \) | wc -l
```

Print:
- File count by extension.
- Which tag groups will be removed (EXIF, GPS, IPTC, XMP, MakerNotes, Thumbnail).
- Which tags will be kept (the whitelist).
- Whether a `backup/` copy will be made.

Wait for user confirmation.

### 4. Backup (if requested)

The backup must live **outside** the target tree. A `backup/` created inside the target gets copied into itself by `cp`, and — worse — is then walked by the recursive `exiftool -r` pass in step 5, which strips the very copies meant to be pristine.

```bash
STAMP=$(date +%Y-%m-%d-%H%M%S)
BACKUP="$(dirname "$TARGET")/.scrub-backup-$STAMP"
mkdir -p "$BACKUP" || { echo "cannot create backup dir $BACKUP" >&2; exit 1; }

if [ -d "$TARGET" ]; then
  cp -R "$TARGET/." "$BACKUP/" || { echo "backup failed — aborting" >&2; exit 1; }
else
  cp "$TARGET" "$BACKUP/" || { echo "backup failed — aborting" >&2; exit 1; }
fi
echo "Backup: $BACKUP"
```

The `-d` branch matters: the scope in step 1 allows a single file, and `cp -R "$TARGET/."` is invalid against a regular file.

If `$(dirname "$TARGET")` is not writable, fall back to `BACKUP="$(mktemp -d)/scrub-backup"` and tell the user the path — never silently place the backup inside the target.

Report the backup path to the user before step 5 runs, and never proceed to step 5 if the backup command failed.

Note that `exiftool` also keeps its own `<file>_original` sidecars in-place unless `-overwrite_original` is passed — decide with the user whether to keep those or clean them up at the end.

### 5. Strip metadata

Two patterns — pick based on scope:

**Folder (non-recursive):**

```bash
exiftool -all= -tagsFromFile @ -Orientation \
  -ext jpg -ext jpeg -ext png -ext heic -ext webp -ext tif -ext tiff \
  "$TARGET"
```

**Recursive tree:**

```bash
exiftool -r -all= -tagsFromFile @ -Orientation \
  -ext jpg -ext jpeg -ext png -ext heic -ext webp -ext tif -ext tiff \
  "$TARGET"
```

The recursive form is why the step 4 backup has to sit outside `$TARGET`: `-r` descends into every subdirectory, including one named `backup/`.

If the user asked to keep additional fields, extend the `-tagsFromFile @ -Field1 -Field2 ...` list. If the user asked to preserve **nothing** (full nuke), drop the `-tagsFromFile` clause — just `-all=`.

To discard the `_original` sidecars in the same run, append `-overwrite_original`. Only do this if a backup was made in step 4, or if the user explicitly waived backup.

### 6. Verify

Sample a few output files and show their remaining metadata:

```bash
exiftool -G1 -a -s "$sample_output"
```

Confirm only whitelisted tags remain. If unexpected metadata survived (common with PNG text chunks or XMP sidecars), flag it and offer a second pass with `-xmp:all=` or a manual `exiftool -ext xmp -overwrite_original -all= "$TARGET"`.

### 7. Log

Write `notes/scrub-metadata-$STAMP.md` in the target folder (or the cwd if the target was a single file), reusing the `$STAMP` computed in step 4 — or, if no backup was taken, `STAMP=$(date +%Y-%m-%d-%H%M%S)`. Include:

- Target path and whether recursive.
- Backup taken? Where?
- Whitelist used.
- File count processed, count skipped, count failed.
- Sample before/after metadata dump for one file.
- Any warnings (XMP sidecars found, MakerNotes that resisted strip, etc.).

If `notes/` doesn't exist, create it.

## Notes

- `exiftool` is the only sane tool for this — don't use `convert -strip` (ImageMagick) as the primary path; it silently drops colour profiles and doesn't touch XMP sidecars reliably.
- **GPS is the most common sensitive leak** — always explicitly confirm it's gone in step 6 (`exiftool -GPS:all "<file>"` should return nothing).
- For HEIC from iPhones, there are often **two** copies of EXIF (container + embedded). `exiftool -all=` handles both, but verify.
- For PNGs, metadata lives in `tEXt` / `iTXt` / `eXIf` chunks — `exiftool -all=` covers them. Do not rely on `optipng -strip all` as a primary scrubber.
- Never operate on the only copy of irreplaceable originals without a backup. If the user is working on an archive, insist on step 4.
- Do not push scrubbed files anywhere automatically — that's a human decision.
