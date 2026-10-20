---
name: read-metadata
description: Use when the user wants to inspect EXIF, IPTC, XMP, or GPS metadata on images without modifying anything — read out as structured JSON or a human-readable summary. Read-only counterpart to `scrub-metadata` (removes) and `set-metadata` (writes). Triggers - "what camera took this photo", "does this image have GPS in it", "show me the EXIF for this folder".
allowed-tools: Bash(exiftool *), Bash(command *), Bash(find *), Bash(jq *), Bash(head *), Bash(wc *), Read, Write
---

# Read Image Metadata

Extract metadata from image files using `exiftool` and output as structured JSON. Supports single files, batch operations, and filtering by metadata group (EXIF, IPTC, XMP, GPS, etc.).

## When to use

- Inspecting the metadata on a photo before sharing or publishing.
- Auditing a batch of images to verify copyright, GPS, or camera information.
- Programmatically querying metadata for file organization or validation.

## Inputs to gather

- **Input file or directory** — single image or folder. Default: current directory.
- **Recursive?** If directory, ask whether to descend. Default: **no** (flat).
- **Filter/group** (optional) — ask if they want a specific metadata subset (e.g., EXIF only, GPS only, copyright-related tags). Default: all metadata.
- **Output format** — JSON (default) or a human-readable summary. Recommend JSON for programmatic use, summary for quick inspection.

## Procedure

### 1. Check tooling

```bash
command -v exiftool >/dev/null || {
  echo "exiftool not installed — see the image-ops-install-deps skill" >&2
  exit 1
}
```

### 2. Determine scope

- **Single file:** direct read.
- **Directory (non-recursive):** read all image files in the folder.
- **Recursive:** use `find` to walk the tree.

### 3. Read metadata

**Single file, full metadata as JSON:**

```bash
exiftool -j "$file"
```

**Single file, summary (human-readable):**

```bash
exiftool -G1 -a -s "$file" | head -50
```

**Filtered by group (EXIF only):**

```bash
exiftool -j -G1 -EXIF "$file"
```

**Common filters:**

- `-EXIF` — EXIF metadata only.
- `-IPTC` — IPTC tags (description, keywords, copyright).
- `-XMP` — XMP metadata (structured, often used by Adobe).
- `-GPS` — GPS coordinates (latitude, longitude, altitude).

`MakerNote` is a single raw EXIF tag holding an undecoded binary blob, not a group you can filter on like the four above. exiftool decodes maker notes into manufacturer-named groups (`Canon`, `Nikon`, `Sony`, …) — filter on those, or just run unfiltered and read what appears.

**Batch (directory or recursive):**

`exiftool` already walks directories and emits one valid JSON array for the whole set. Use that rather than `find -exec`, which invokes exiftool once per file and concatenates N separate `[...]` arrays into a file that is not valid JSON:

```bash
exiftool -j -r \
  -ext jpg -ext jpeg -ext png -ext heic -ext webp -ext tif -ext tiff \
  "$target" > metadata.json
```

Drop `-r` for the non-recursive case. If a `find`-driven list is genuinely needed (e.g. a filtered subset), pipe it through `jq -s 'add'` to flatten the per-file arrays into one before writing.

### 4. Summarize or display

**For JSON output:**

If the user wants a summary, parse the JSON:

```bash
exiftool -j "$file" | jq '.[] | {File, Make, Model, DateTime, GPSLatitude, GPSLongitude, Copyright}'
```

**For a batch report:**

```bash
exiftool -j -a -s "$target" | jq '.[] | {FileName, Make, Model, LensModel, FocalLength, ISO, ExposureTime, FNumber}'
```

Pass the directory itself, not a quoted glob. `"$target/*"` is quoted, so the shell never expands it and exiftool receives the literal string `dir/*` as a filename that does not exist.

### 5. Report

Print the metadata (JSON or summary, per user preference). If batch:

- Count of files read.
- Any files with missing metadata.
- Common metadata patterns (e.g., "15 images from Canon EOS 5D Mark III", "8 images missing GPS").

## Output / side effects

- Metadata displayed on stdout (or saved to a JSON file if requested).
- No files modified.

## Notes

- **Metadata standards overlap:** EXIF, IPTC, and XMP sometimes describe the same field (e.g., copyright, description, keywords). `exiftool -j` merges these intelligently; check the JSON keys to see what's present.
- **Camera-specific tags:** Each manufacturer embeds maker-specific metadata. exiftool decodes it into a manufacturer-named group — filter with `-Canon`, `-Nikon`, `-Sony`, or run unfiltered with `-G1` to see which groups a given file actually carries.
- **GPS privacy:** Check for `-GPS` tags before sharing a photo. Many smartphone cameras and some cameras embed GPS by default.
- **Phone metadata:** iPhones embed extensive metadata in EXIF and XMP, including model, iOS version, and processing applied.
- **PNG text chunks:** PNG metadata lives in text chunks (`tEXt`, `iTXt`) rather than EXIF. `exiftool` reads them as XMP or PNG metadata.
- **Batch JSON:** prefer letting exiftool walk the directory (`-j -r <dir>`) — it emits one valid array. Only reach for `jq -s 'add'` when you had to drive it from an external file list and ended up with several concatenated arrays.
- Depends on `exiftool` (`apt install libimage-exiftool-perl` on Debian/Ubuntu, `brew install exiftool` on macOS). Use `image-ops-install-deps` rather than installing by hand.
