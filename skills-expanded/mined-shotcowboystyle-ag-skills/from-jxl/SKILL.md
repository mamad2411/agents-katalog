---
name: from-jxl
description: Use when the user wants to decode JPEG XL images (.jxl) back to PNG or JPEG — for compatibility with tools that cannot read JXL, for display, or for further editing. Also recovers the byte-exact original JPEG from a lossless transcode. Reverse of `to-jxl`. Triggers - "convert these JXL files to PNG", "my viewer can't open .jxl", "get the original JPEG back out".
allowed-tools: Bash(djxl *), Bash(command *), Bash(find *), Bash(sh *), Bash(magick *), Bash(mkdir *), Read, Write
---

# Decode JPEG XL Images

Extract images from JPEG XL (.jxl) files using `djxl`. Outputs PNG or JPEG, with optional recovery of original JPEG bitstream if the source JXL was a lossless JPEG transcode.

## When to use

- Converting JXL files back to PNG for general use or compatibility.
- Recovering the original JPEG bitstream from a lossless-transcoded JXL file.
- Batch-decoding a JXL archive to portable formats.

## Inputs to gather

- **Input .jxl file or directory** — single file or folder.
- **Output format** — `png` (default) or `jpeg`. If the user has a JXL that came from a lossless JPEG transcode and wants to recover the original JPEG byte-exact, offer the `jpeg` format and explain that reconstruction is automatic (see step 3).
- **Output directory** — optional. Default: same directory as input.

## Procedure

### 1. Check tooling

```bash
command -v djxl >/dev/null || {
  echo "djxl not installed — see the image-ops-install-deps skill" >&2
  exit 1
}
```

### 2. Determine scope and format

- **Single file:** direct conversion.
- **Directory (non-recursive):** loop over all `.jxl` files.
- **Recursive:** use `find` to locate `.jxl` files in the tree.

Confirm the output format with the user. Set the depth limit once, and reuse it:

```bash
maxdepth="-maxdepth 1"   # non-recursive
maxdepth=""              # recursive — omit the flag entirely
```

### 3. Decode

`djxl` picks its output codec from the output file's extension. There is no format flag to pass.

**Single file to PNG (default):**

```bash
djxl input.jxl output.png
```

**Single file to JPEG:**

```bash
djxl input.jxl output.jpg
```

A `.jpg` output only succeeds when the `.jxl` carries JPEG reconstruction data (JBRD) — that is, it came from `cjxl original.jpg out.jxl`. In that case the result is the original JPEG **byte-exact**, which is the recovery path for an archive built by `transcode-jpeg-to-jxl-lossless`.

For a `.jxl` encoded from PNG or any other source there is no JBRD and this command **fails**; it does not silently re-encode. Decode to PNG and re-encode explicitly instead:

```bash
djxl input.jxl /tmp/decoded.png && magick /tmp/decoded.png -quality 92 output.jpg
```

Check for reconstruction data before promising byte-exact recovery on a batch — a failed `djxl` to `.jpg` is the signal, so let step 4's failure log surface it rather than pre-flighting every file.

**Batch (folder or recursive):**

`find` substitutes only the literal token `{}`. It has no `{.}` extension-stripping placeholder — that is GNU parallel syntax, and `find` passes `{.}.png` through verbatim, so every file decodes onto one output that each iteration overwrites. Derive the name in a shell:

```bash
: > "$failed_log"

find "$target" $maxdepth -type f -iname '*.jxl' \
  -exec sh -c '
    for f do
      djxl "$f" "${f%.jxl}.$0" || echo "$f" >> "$1"
    done
  ' "$format" "$failed_log" {} +
```

Set `$format` to `png` or `jpg`.

### 4. Report

After decoding:

- Count of files decoded, skipped, failed.
- Output file sizes and locations.
- Print the contents of `$failed_log`; say "none" only when it is empty. For a `jpg` batch, a failure most often means that `.jxl` had no JPEG reconstruction data — call that out rather than reporting a generic error.

## Output / side effects

- New PNG or JPEG files created in the output directory.
- Original `.jxl` files remain unchanged.

## Notes

- **Lossless JPEG recovery:** decoding to a `.jpg` output reconstructs the original bitstream only when the `.jxl` was created via lossless JPEG transcode (`cjxl original.jpg encoded.jxl`). Otherwise `djxl` errors out — it will not hand back a silently re-encoded approximation, so a successful `.jpg` decode is itself the guarantee.
- **Alpha channels:** JXL alpha is preserved when decoding to PNG. JPEG does not support transparency, so any alpha will be lost if decoding to JPEG.
- **Color profile:** JXL can carry ICC color profiles; `djxl` preserves them in the output.
- Depends on `libjxl-tools` (`apt install libjxl-tools` on Debian/Ubuntu, `brew install jpeg-xl` on macOS). Use `image-ops-install-deps` rather than installing by hand. The `magick` re-encode path above additionally needs ImageMagick.
