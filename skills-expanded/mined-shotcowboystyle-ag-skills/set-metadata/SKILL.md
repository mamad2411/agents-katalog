---
name: set-metadata
description: Use when the user wants to write arbitrary EXIF, IPTC, or XMP tags to images — artist, copyright, description, keywords, GPS coordinates, capture date, lens or camera model. For stamping only copyright/artist/rights uniformly across a whole directory, `batch-set-copyright` is the narrower wrapper. Triggers - "set the description on this photo", "add GPS coordinates to these images", "fix the lens metadata".
allowed-tools: Bash(exiftool *), Bash(command *), Bash(find *), Bash(mkdir *), Bash(cp *), Bash(grep *), Read, Write
---

# Write Metadata to Images

Set metadata tags on image files using `exiftool`. Supports EXIF, IPTC, and XMP metadata, with automatic backup of original files.

## When to use

- Adding copyright and artist information to a photo before distribution.
- Manually setting GPS coordinates if they were not captured.
- Batch-updating descriptions or keywords across multiple images.
- Fixing incorrect camera model or lens metadata.

For the narrow case of stamping the *same* copyright, artist, and rights across an entire folder, `batch-set-copyright` wraps that workflow with a preview and a per-file failure tally. Use this skill for arbitrary tags, per-file values, or anything outside those three fields.

## Inputs to gather

- **Input file or directory** — single image or folder.
- **Metadata key-value pairs** — ask the user for the tags and values they want to set. Common fields:
  - `Artist` — photographer or creator name.
  - `Copyright` — copyright statement (e.g. `© 2026 <Artist>`).
  - `Description` / `ImageDescription` — image description text.
  - `Keywords` — comma-separated keywords.
  - `LensModel` — lens description (if not auto-detected).
  - `GPSLatitude` / `GPSLongitude` / `GPSAltitude` — GPS coordinates.
  - `DateTimeOriginal` — capture date/time (format: `YYYY:MM:DD HH:MM:SS`).
- **Backup before write?** Default: **yes**. exiftool creates `_original` sidecars; offer an explicit backup copy for safety.

## Procedure

### 1. Check tooling

```bash
command -v exiftool >/dev/null || {
  echo "exiftool not installed — see the image-ops-install-deps skill" >&2
  exit 1
}
```

### 2. Validate tag names

Ask the user to confirm the exiftool tag names. Common mappings:

| User-facing | exiftool tag |
|---|---|
| Artist | Artist |
| Creator | Creator |
| Copyright | Copyright |
| Description | ImageDescription |
| Keywords | Keywords |
| Lens | LensModel |
| Camera model | Model |

**Gotcha:** EXIF, IPTC, and XMP may use different tag names for the same logical field. exiftool auto-detects the appropriate target; document which format will be used:

```bash
exiftool -a -G1 "$sample" | grep -i copyright
```

This shows which groups (EXIF, IPTC, XMP) currently carry copyright info on the sample file.

### 3. Confirm metadata and scope

Print a summary:

- Tags to be set: list all key-value pairs.
- Target files: count and confirm.
- Backup location: where `_original` sidecars will be stored.
- Confirm before proceeding.

### 4. Backup (if requested)

exiftool creates `_original` sidecars by default; offer an explicit backup on top of that. Put it **outside** the target tree, or a later recursive pass walks into the backup and rewrites the copies too:

```bash
BACKUP="$(dirname "$TARGET")/.setmeta-backup-$$"
mkdir -p "$BACKUP" || { echo "cannot create backup dir $BACKUP" >&2; exit 1; }

if [ -d "$TARGET" ]; then
  cp -R "$TARGET/." "$BACKUP/" || { echo "backup failed — aborting" >&2; exit 1; }
else
  cp "$TARGET" "$BACKUP/"      || { echo "backup failed — aborting" >&2; exit 1; }
fi
echo "Backup: $BACKUP"
```

The `-d` branch matters — the scope allows a single file, and `cp -R "$TARGET/."` is invalid against one. Never proceed to step 5 if the backup command failed.

### 5. Write metadata

**Single file:**

Build the tag list once as an array, so the same set can be reused for the single-file and batch paths and optional tags can be appended conditionally:

```bash
ARGS=( -Artist="$ARTIST" -Copyright="$COPYRIGHT" )
[ -n "$DESC" ]     && ARGS+=( -ImageDescription="$DESC" )
[ -n "$KEYWORDS" ] && ARGS+=( -Keywords="$KEYWORDS" )
```

**Single file:**

```bash
exiftool "${ARGS[@]}" "$file"
```

**Batch (directory or recursive):**

```bash
: > "$failed_log"

# Non-recursive: -maxdepth 1. Recursive: omit -maxdepth entirely.
find "$TARGET" -maxdepth 1 -type f \
  \( -iname '*.jpg' -o -iname '*.jpeg' -o -iname '*.png' \
     -o -iname '*.heic' -o -iname '*.webp' -o -iname '*.tif' -o -iname '*.tiff' \) \
  -print0 |
while IFS= read -r -d '' f; do
  exiftool "${ARGS[@]}" "$f" >/dev/null || echo "$f" >> "$failed_log"
done
```

`find -exec` discards each exit code, so the loop is what makes a failure count possible. `-print0` with `read -d ''` keeps filenames with spaces intact.

Append `-overwrite_original` to `ARGS` to discard `_original` sidecars, but only if a backup was made in step 4.

### 6. Verify

Sample a few output files and confirm the metadata was written:

```bash
exiftool -Artist -Copyright -ImageDescription "$sample"
```

Also report the contents of `$failed_log` — say "none" only when it is empty.

If metadata did not stick (e.g. PNG text chunks), try the XMP-specific path:

```bash
exiftool -XMP:Artist="$ARTIST" -XMP:Copyright="$COPYRIGHT" "$file"
```

### 7. Cleanup (optional)

If the user accepted `-overwrite_original`, remove `_original` sidecars. Confirm first — this discards exiftool's own safety net:

```bash
find "$TARGET" -maxdepth 1 -type f -iname '*_original' -delete
```

Drop `-maxdepth` for the recursive case.

## Output / side effects

- Metadata tags written to original files (or to a copy if the user requested a separate output directory).
- `_original` sidecars created in the same directory as each file (unless `-overwrite_original` was used).
- Original files are modified (unless a backup was made in step 4).

## Notes

- **EXIF vs. IPTC vs. XMP:** The same field (e.g., copyright) can live in EXIF, IPTC, and/or XMP. Some readers check only one format. `exiftool` intelligently maps to the appropriate group, but document which format was used:
  - EXIF: structured, camera/lens/exposure info. Limited size.
  - IPTC: editorial metadata (keywords, description, copyright). Limited size.
  - XMP: extensible, can hold arbitrary key-value pairs.
- **PNG and HEIC:** exiftool writes metadata to PNG as XMP in iTXt chunks. HEIC is complex; check the `_original` sidecar to ensure metadata persisted.
- **Tag size limits:** EXIF and IPTC have field-length limits. Very long descriptions (>500 chars) should go in XMP. exiftool warns if a value is too large.
- **Permanent writes:** Always create a backup before bulk metadata writes. Metadata corruption is rare but possible.
- **Preserve other metadata:** By default, `exiftool -Tag=value file` preserves all other metadata. Use `-all=` if you want to nuke everything before writing (not recommended).
- Depends on `exiftool` (`apt install libimage-exiftool-perl` on Debian/Ubuntu, `brew install exiftool` on macOS). Use `image-ops-install-deps` rather than installing by hand.
