---
name: zip-recursive-subdocument-conversion
description: Convert a ZIP archive to a single combined markdown document by iterating entries, constructing per-entry StreamInfo from filename+extension, and recursing through the same converter registry for each entry.
category: data-pipeline
version: 1.0.0
tags: [data-pipeline, zip, recursion, converter-registry, python]
source_type: extracted-from-git
source_url: https://github.com/microsoft/markitdown.git
source_ref: main
source_commit: 604bba13da2f43b756b49122cb65bdedb85b1dff
source_project: markitdown
source_path: packages/markitdown/src/markitdown/converters/_zip_converter.py
imported_at: 2026-04-18T00:00:00Z
confidence: medium
version_origin: extracted
---

# Recursive subdocument conversion for ZIP archives

When a container format (ZIP, EPUB, DOCX's unzipped XML, TAR) holds mixed content, don't hard-code per-format conversions inside the container handler. Instead, iterate entries, turn each into a `(BytesIO, StreamInfo)` pair, and recurse through the **same** top-level converter registry. That gives you transparent support for every format the host can convert, including nested containers.

## The shape

```python
import io, os, zipfile
from typing import BinaryIO, Any

class ZipConverter(DocumentConverter):
    """Converts a zip into one markdown doc with each entry labeled by path."""

    def __init__(self, *, markitdown):   # host is passed in so we can recurse
        super().__init__()
        self._markitdown = markitdown

    def accepts(self, file_stream: BinaryIO, stream_info, **kwargs) -> bool:
        ext  = (stream_info.extension or "").lower()
        mime = (stream_info.mimetype  or "").lower()
        return ext == ".zip" or mime.startswith("application/zip")

    def convert(self, file_stream: BinaryIO, stream_info, **kwargs):
        tag = stream_info.url or stream_info.local_path or stream_info.filename
        out = [f"Content from the zip file `{tag}`:", ""]

        with zipfile.ZipFile(file_stream, "r") as zf:
            for name in zf.namelist():
                try:
                    entry = io.BytesIO(zf.read(name))
                    info  = StreamInfo(
                        extension=os.path.splitext(name)[1],
                        filename=os.path.basename(name),
                    )
                    res = self._markitdown.convert_stream(stream=entry, stream_info=info)
                    if res is not None:
                        out.append(f"## File: {name}")
                        out.append("")
                        out.append(res.markdown)
                        out.append("")
                except UnsupportedFormatException:
                    pass      # skip entries the host can't handle
                except FileConversionException:
                    pass      # skip entries that errored

        return DocumentConverterResult(markdown="\n".join(out).strip())
```

Two key decisions:

1. **Host (`self._markitdown`) is injected at construction.** The handler doesn't know about specific sub-converters; it just calls `host.convert_stream(...)` and lets the registry figure out each entry. Works transparently for nested zips, DOCX-inside-DOCX, etc.
2. **Swallow `UnsupportedFormatException` and `FileConversionException` per entry.** One malformed file in a 10,000-entry archive shouldn't nuke the whole conversion.

## Output format

```markdown
Content from the zip file `docs.zip`:

## File: docs/readme.txt

This is the content of readme.txt
Multiple lines are preserved

## File: images/example.jpg

ImageSize: 1920x1080
DateTimeOriginal: 2024-02-15 14:30:00
Description: A beautiful landscape photo

## File: data/report.xlsx

## Sheet1
| Column1 | Column2 | Column3 |
|---------|---------|---------|
| data1   | data2   | data3   |
```

Keep original paths in the `## File:` headings so the LLM can reconstruct structure and reference specific files in its output.

## Why recurse into the same registry

- **Zero coupling to file types.** The ZIP handler doesn't mention PDF, image, or xlsx logic. It only knows "there are entries; hand each to the host."
- **Transparent nesting.** ZIP-in-ZIP works for free. So does ZIP-of-DOCX-of-embedded-images.
- **Converter evolution.** Adding a new file-type converter to the host immediately works inside ZIPs with no ZIP-code changes.

## Memory considerations

- `zf.read(name)` loads the entire entry into memory. For a multi-gigabyte archive that's a problem; swap in `zf.open(name)` which returns a streaming file-like — but then you need the seekable-buffer wrapper (see `filestream-seekable-buffer-fallback`) because zip streams aren't seekable.
- Huge archives with many small entries: consider parallelization (`concurrent.futures.ThreadPoolExecutor`) — but beware of zipfile's thread safety: open the archive once per worker, not share.

## Security considerations

- **Zip bomb defense.** A 42KB zip can expand to petabytes. Enforce a cumulative uncompressed-size limit:

  ```python
  total = 0
  LIMIT = 100 * 1024 * 1024   # 100 MB
  for info in zf.infolist():
      total += info.file_size
      if total > LIMIT:
          raise FileConversionException("Zip uncompressed size exceeds limit")
  ```
- **Path traversal.** The entry name `../../etc/passwd` is malicious if you ever write entries to disk. This converter stays in memory via `BytesIO`, so it's safe — but if you extract to temp files, sanitize with `os.path.normpath` and reject anything escaping the temp root.
- **Symlink entries.** `zipfile` doesn't create symlinks on extract by default, but if you use `tarfile` or `shutil.unpack_archive`, do.

## Anti-patterns

- **Hardcoding a dispatch table inside the container.** `if name.endswith(".pdf"): pdf_convert(...); elif name.endswith(".xlsx"): ...` — duplicates what the registry already does, and breaks when new types are added.
- **Failing the whole archive on one bad entry.** Users lose the other 9,999 working entries.
- **No per-entry heading.** LLMs lose the ability to cite which file a quoted passage came from.
- **Extracting to disk unconditionally.** Tempfile lifecycle, cleanup, and path-traversal defense are harder than staying in memory; stay in memory if you can.

## Variations

- **EPUB**: structurally a zip of XHTML + images. Same pattern, but filter to `.xhtml`/`.html` entries and order by the spine.
- **Office Open XML (DOCX/XLSX/PPTX)**: technically zips of XML, but you usually want a dedicated parser (mammoth, python-docx) that understands the package structure rather than flattening it.
- **TAR / TAR.GZ**: swap `zipfile.ZipFile` for `tarfile.open(fileobj=stream)`; otherwise identical pattern.
- **Per-entry filter**: accept a `should_include: Callable[[str], bool]` so callers can limit which entries are processed.
