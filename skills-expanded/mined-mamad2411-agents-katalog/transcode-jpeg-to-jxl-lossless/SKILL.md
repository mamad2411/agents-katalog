---
name: transcode-jpeg-to-jxl-lossless
description: Use when the user wants to archive a JPEG-only library as JPEG XL — losslessly transcodes JPEG to .jxl, preserving the original bitstream for byte-exact recovery, with a dry-run preview and a byte-savings report (~15–25% reduction). Prefer this over the general-purpose `to-jxl` skill whenever the sources are exclusively JPEG and archival is the goal. Triggers - "archive my JPEGs as JXL", "shrink this photo library losslessly", "JPEG to JXL without quality loss".
allowed-tools: Bash(cjxl *), Bash(djxl *), Bash(command *), Bash(find *), Bash(sh *), Bash(awk *), Bash(wc *), Bash(du *), Bash(tail *), Bash(tee *), Read, Write
---

# Losslessly Transcode JPEG to JPEG XL

Walk a directory of JPEG files and convert them to JPEG XL (.jxl) format using lossless encoding. `cjxl` automatically detects JPEG bitstream and preserves it without re-compression. Reports byte savings; explains how to recover the original JPEG if needed.

## When to use

- Archiving JPEG photo libraries to save space (typically 15–25% reduction) without image degradation.
- Preparing a photo collection for long-term storage where compatibility with JPEG is not required.
- Building a smaller-footprint JXL archive that can still yield the original JPEG byte-exact via `djxl`.

For non-JPEG sources, or for lossy/web-quality JXL encodes, use `to-jxl` — this skill deliberately handles only the JPEG-archival case.

## Inputs to gather

- **Source directory** — folder containing JPEG files (`.jpg` or `.jpeg`). Default: current directory.
- **Recursive?** Ask whether to process subdirectories. Default: **no** (flat, current folder only).
- **Output location** — optional. Default: same directory as originals (`.jxl` files sit alongside `.jpg`).
- **Dry run first?** Recommend a preview pass showing the count and byte savings estimate, before committing to the conversion.

## Procedure

### 1. Check tooling

```bash
command -v cjxl >/dev/null || {
  echo "cjxl not installed — see the image-ops-install-deps skill" >&2
  exit 1
}
```

### 2. Preview

Show the user what will happen. Capture the original total into a variable — step 4 needs it to compute savings, and re-measuring the directory afterwards would count the new `.jxl` files too.

Set the depth limit once, from the answer to "recursive?" in the inputs:

```bash
maxdepth="-maxdepth 1"   # non-recursive
maxdepth=""              # recursive — omit the flag entirely
```

```bash
# Count JPEGs in scope
find "$target" $maxdepth -type f \
  \( -iname '*.jpg' -o -iname '*.jpeg' \) | tee /tmp/jpegs.txt | wc -l

# Original total, in bytes (not human-readable — it has to be arithmetic later)
ORIG_BYTES=$(find "$target" $maxdepth -type f \
  \( -iname '*.jpg' -o -iname '*.jpeg' \) -exec wc -c {} + \
  | awk '$NF == "total" { next } { s += $1 } END { print s+0 }')
```

Skipping the `total` lines matters: `-exec ... +` batches its arguments, so a large tree produces one `total` line per batch and naively summing every line would double-count.

`wc -c` totals exact bytes; `du` rounds to block size and would skew the savings figure on a library of small files.

Print:
- Number of JPEG files found.
- Total original size.
- Estimated output size (advise 20% reduction as a rough baseline).
- Confirm before proceeding.

### 3. Transcode

Use `-d 0` (lossless) and a reasonable effort (suggest 6–7 for balance):

`find` substitutes only the literal token `{}`. There is no `{.}` extension-stripping placeholder — that is GNU parallel syntax, and `find` would pass the literal string `{.}.jxl`, funnelling every file in the tree into one output that each conversion overwrites. Build the output name inside a shell instead, reusing the `$maxdepth` set in step 2:

```bash
: > "$failed_log"

find "$target" $maxdepth -type f \
  \( -iname '*.jpg' -o -iname '*.jpeg' \) \
  -exec sh -c '
    for f do
      cjxl -d 0 -e 7 "$f" "${f%.*}.jxl" || echo "$f" >> "$0"
    done
  ' "$failed_log" {} +
```

(The `-d 0` flag ensures lossless encoding. Effort 7 balances speed and compression. Effort 9 is slower but slightly smaller; only recommend if the user has time.)

`$failed_log` collects every non-zero `cjxl` exit. `find -exec` does not propagate per-file status, so without this file a failed transcode is silently invisible in the step 4 report.

### 4. Verify and report

After transcoding:

```bash
# Count JXL files created
find "$target" $maxdepth -type f -iname '*.jxl' | wc -l

# Total size of the new JXL files, in bytes
JXL_BYTES=$(find "$target" $maxdepth -type f -iname '*.jxl' -exec wc -c {} + \
  | awk '$NF == "total" { next } { s += $1 } END { print s+0 }')

# Bytes saved — an explicit subtraction against the step 2 figure
awk -v o="$ORIG_BYTES" -v n="$JXL_BYTES" 'BEGIN {
  printf "original: %.1f MB\njxl:      %.1f MB\nsaved:    %.1f MB (%.1f%%)\n",
         o/1048576, n/1048576, (o-n)/1048576, (o ? (o-n)*100/o : 0)
}'
```

Do **not** substitute `du -ch "$target"` for this. At this point the directory holds both the originals and the new `.jxl` files, so it measures the sum of the two, not the saving. The saving only exists as the difference between the step 2 figure and the step 4 figure.

Print:
- Files successfully transcoded.
- Original total size vs. new total size.
- Bytes saved and percentage reduction (from the `awk` above).
- Any failures — print the contents of `$failed_log`, and say "none" only when that file is empty.

### 5. Explain recovery path

Inform the user:

> If you ever need to recover the original JPEG bitstream byte-exact (for legal/archival purposes), run:
> ```bash
> djxl archive.jxl recovered.jpg
> ```
> This works because `cjxl` detected and preserved the original JPEG structure. Reconstruction is triggered by the `.jpg` output extension — there is no `--jpeg` flag in current libjxl. If the `.jxl` carries no reconstruction data, `djxl` reports an error rather than quietly writing a re-encoded approximation, so a successful run is itself the proof of byte-exactness.

## Output / side effects

- `.jxl` files created in the source directory (or user-specified output folder).
- Original `.jpg` files remain untouched.
- No backup is created; if the originals must be preserved, the user should copy them first.

## Notes

- **Lossless JPEG preservation:** `cjxl` auto-detects JPEG bitstreams and preserves them exactly. This is why `djxl` can recover the original — it's not a re-encoded approximation.
- **Effort 7 vs. 9:** Effort 7 compresses in seconds per image; effort 9 can take minutes. For batch workflows, 7 is recommended. Use 9 only if compression size is the overriding concern.
- **Size savings:** Typical JPEG → JXL lossless reduction is 15–25%, depending on the original JPEG quality. Do not oversell — some JPEGs may compress only 5–10%.
- **Selective transcoding:** If you want to skip already-small files or transcode only above a size threshold, filter the find output (e.g., `-size +100k` for files larger than 100 KB).
- Do not delete the original JPEG files automatically. Let the user confirm removal after verifying the JXL output.
- Depends on `libjxl-tools` (`apt install libjxl-tools` on Debian/Ubuntu, `brew install jpeg-xl` on macOS). Use `image-ops-install-deps` rather than installing by hand.
