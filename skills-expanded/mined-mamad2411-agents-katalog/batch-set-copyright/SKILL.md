---
name: batch-set-copyright
description: Use when the user wants to batch-stamp copyright, artist, and rights information across every image in a directory — a photo library heading for distribution or archival. Convenience wrapper around exiftool. For arbitrary tags (description, keywords, GPS) on individual files, use `set-metadata` instead. Triggers - "add my copyright to all these photos", "stamp the artist name across this shoot".
allowed-tools: Bash(exiftool *), Bash(command *), Bash(find *), Bash(date *), Bash(wc *), Read, Write
---

# Batch Set Copyright on Images

Walk a directory and stamp copyright, artist, and rights metadata on every image using `exiftool`. Common real-world use: archiving a photo library with a consistent copyright statement.

## When to use

- Preparing a personal photo library for distribution or archival with consistent copyright metadata.
- Quickly tagging all images from an event or shoot with the same artist and copyright info.
- Ensuring your photo library has baseline legal metadata before sharing or licensing.

## Inputs to gather

- **Target directory** — folder containing images to tag. Default: current directory.
- **Recursive?** Ask whether to process subdirectories. Default: **no** (flat, current folder only).
- **Artist name** — required. Ask for the photographer or creator name.
- **Copyright string** — optional. If not provided, auto-generate from current year and artist: `© 2026 <Artist>`. Allow the user to override.
- **Rights/Usage statement** (optional) — additional rights text (e.g., "All rights reserved", "Creative Commons BY-SA 4.0"). If omitted, skip this field.
- **Backup before write?** Default: **yes**. Automatic via exiftool `_original` sidecars.

## Procedure

### 1. Check tooling

```bash
command -v exiftool >/dev/null || {
  echo "exiftool not installed — see the image-ops-install-deps skill" >&2
  exit 1
}
```

### 2. Build metadata strings

```bash
ARTIST="<user-provided>"                       # required
COPYRIGHT="${user_copyright:-© $(date +%Y) $ARTIST}"
RIGHTS="<user-provided-or-empty>"              # optional
```

- **Artist:** the user-provided value.
- **Copyright:** provided, or auto-generated as `© <YYYY> <Artist>` using the current year from `date +%Y`.
- **Rights/Usage:** used if provided; otherwise omitted entirely.

Print a summary for user confirmation before proceeding.

### 3. Count and preview

```bash
# Count images that will be tagged.
# Non-recursive: -maxdepth 1. Recursive: omit -maxdepth entirely.
find "$TARGET" -maxdepth 1 -type f \
  \( -iname '*.jpg' -o -iname '*.jpeg' -o -iname '*.png' \
     -o -iname '*.heic' -o -iname '*.webp' -o -iname '*.tif' -o -iname '*.tiff' \) | wc -l
```

Quote `"$TARGET"` everywhere — an unquoted path word-splits on the first space and `find` then reports a nonexistent directory.

Print:
- Number of images found.
- Metadata to be applied.
- Request confirmation before applying.

### 4. Apply metadata

Build the tag list as an array first. The optional `-Rights` flag cannot be written inline as `<-Rights="...">` — bash reads a bare `<` and `>` as input/output redirection, so that line breaks the command rather than making the flag conditional:

```bash
ARGS=( -Artist="$ARTIST" -Copyright="$COPYRIGHT" )
[ -n "$RIGHTS" ] && ARGS+=( -Rights="$RIGHTS" )
```

Then apply, tallying per-file status. `find -exec` discards each `exiftool` exit code, so without the inner shell the "count of failures" promised in step 6 cannot be produced:

```bash
: > "$failed_log"

# Non-recursive: -maxdepth 1. Recursive: omit -maxdepth entirely
# (there is no need for a sentinel like -maxdepth 999, which silently
# truncates a tree deeper than that).
find "$TARGET" -maxdepth 1 -type f \
  \( -iname '*.jpg' -o -iname '*.jpeg' -o -iname '*.png' \
     -o -iname '*.heic' -o -iname '*.webp' -o -iname '*.tif' -o -iname '*.tiff' \) \
  -print0 |
while IFS= read -r -d '' f; do
  exiftool "${ARGS[@]}" "$f" >/dev/null || echo "$f" >> "$failed_log"
done
```

`-print0` with `read -d ''` is what makes filenames containing spaces or newlines safe here.

Show progress as files are processed (especially for large batches).

### 5. Verify

Sample 3–5 images across the directory and confirm metadata was applied:

```bash
exiftool -Artist -Copyright -Rights "$sample1"
exiftool -Artist -Copyright -Rights "$sample2"
```

### 6. Report

After completion:

- Count of images successfully tagged.
- Count of failures and their paths, read from `$failed_log`. Say "none" only when that file is empty.
- Reminder: `_original` sidecars have been created (location noted).
- Option: offer to remove `_original` sidecars if the user is confident the write succeeded.

## Output / side effects

- Copyright, Artist, and optional Rights metadata written to all images in scope.
- `_original` sidecars created in the same directories (can be removed post-verification).
- Original images modified; create a backup directory first if preservation is critical.

## Notes

- **Auto-generated copyright:** step 2 uses the system date (`date +%Y`) to build the year. If the images are from a prior year, the user should provide a custom copyright string (e.g. `© 2024 <Artist>`).
- **Metadata format:** `exiftool` writes to EXIF IFD0 / IPTC / XMP as appropriate. Different image readers may check different formats; this skill writes comprehensively so compatibility is high.
- **Batch verification:** For large directories, consider sampling rather than checking every file. Spot-check 5–10% of the batch.
- **Rights field variations:** Some tools recognize `Rights`, others use `UsageRights` or custom XMP fields. The `Rights` tag is most portable; if compatibility issues arise, document alternatives in the report.
- **Preserve prior metadata:** By default, this skill adds/updates copyright metadata without touching other tags. If the user wants a fresh start (nuke all, then add new), use the `scrub-metadata` skill first.
- Depends on `exiftool` (`apt install libimage-exiftool-perl` on Debian/Ubuntu, `brew install exiftool` on macOS). Use `image-ops-install-deps` rather than installing by hand.
