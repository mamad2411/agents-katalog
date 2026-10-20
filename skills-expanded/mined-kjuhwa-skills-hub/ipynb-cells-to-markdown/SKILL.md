---
name: ipynb-cells-to-markdown
description: Convert a Jupyter notebook JSON (.ipynb) into a single markdown document — markdown cells passed through, code cells wrapped in ```python fences, raw cells in bare fences, title auto-detected from first H1 or notebook metadata.
category: data-pipeline
version: 1.0.0
tags: [data-pipeline, jupyter, ipynb, notebook, markdown, python]
source_type: extracted-from-git
source_url: https://github.com/microsoft/markitdown.git
source_ref: main
source_commit: 604bba13da2f43b756b49122cb65bdedb85b1dff
source_project: markitdown
source_path: packages/markitdown/src/markitdown/converters/_ipynb_converter.py
imported_at: 2026-04-18T00:00:00Z
confidence: medium
version_origin: extracted
---

# Jupyter notebook (.ipynb) → markdown

Plain-text conversion of a `.ipynb` for LLM ingestion, linting, or diff-friendly rendering. The notebook JSON's `cells[]` array has three cell types — `markdown`, `code`, `raw` — which map to markdown passthrough, fenced-python, and bare-fenced output respectively. Title resolution: first `# Heading` in any markdown cell, overridden by `metadata.title` if present.

## The shape

```python
import json
from typing import BinaryIO, Any

ACCEPTED_EXTENSIONS = [".ipynb"]
CANDIDATE_MIME_PREFIXES = ["application/json"]

class IpynbConverter(DocumentConverter):
    def accepts(self, file_stream: BinaryIO, stream_info, **kwargs) -> bool:
        ext  = (stream_info.extension or "").lower()
        mime = (stream_info.mimetype or "").lower()
        if ext in ACCEPTED_EXTENSIONS:
            return True
        for prefix in CANDIDATE_MIME_PREFIXES:
            if mime.startswith(prefix):
                # Peek to disambiguate — JSON could be anything
                cur = file_stream.tell()
                try:
                    text = file_stream.read().decode(stream_info.charset or "utf-8")
                    return "nbformat" in text and "nbformat_minor" in text
                finally:
                    file_stream.seek(cur)
        return False

    def convert(self, file_stream: BinaryIO, stream_info, **kwargs):
        charset = stream_info.charset or "utf-8"
        nb = json.loads(file_stream.read().decode(charset))
        return _render(nb)

def _render(nb: dict) -> DocumentConverterResult:
    out, title = [], None
    for cell in nb.get("cells", []):
        ctype = cell.get("cell_type")
        src   = "".join(cell.get("source", []))   # sources are arrays of strings
        if ctype == "markdown":
            out.append(src)
            if title is None:
                for line in src.splitlines():
                    if line.startswith("# "):
                        title = line.lstrip("# ").strip()
                        break
        elif ctype == "code":
            out.append(f"```python\n{src}\n```")
        elif ctype == "raw":
            out.append(f"```\n{src}\n```")
        # else: ignore unknown cell types (forward compat)

    # notebook-level metadata.title wins over auto-detected heading
    title = nb.get("metadata", {}).get("title", title)
    return DocumentConverterResult(markdown="\n\n".join(out), title=title)
```

## Why these design choices

- **Language in the code fence is always `python`.** In practice, 99% of ipynbs are Python. For Julia/R kernels you could read `metadata.kernelspec.language`, but the common case doesn't need it — and guessing wrong here is cheap (the fence is decorative).
- **`source` is an array of strings.** Each line ends in `\n` already, so `"".join(source)` produces the correct multiline text. Don't `"\n".join` — you'll introduce double newlines.
- **Title fallback order**: `metadata.title` → first `# H1` in a markdown cell → `None`. `metadata.title` is rare but authoritative; auto-detect is a heuristic that covers the common case.
- **Skip outputs by default.** `cell.outputs` can contain images (base64 PNGs), rich HTML, tables, and text. For LLM ingestion the source cells are usually enough; keep outputs out of the default pipeline to keep token budgets sane.

## Why the accepts() slow path

`application/json` is too broad — package manifests, configs, and API payloads are all JSON. Peek the content; if it contains both `"nbformat"` and `"nbformat_minor"` keys, it's overwhelmingly likely a notebook. This avoids the IpynbConverter accidentally claiming every JSON file on disk.

## Optional: render outputs

For pipelines that care about computed results, extend the code-cell branch:

```python
elif ctype == "code":
    out.append(f"```python\n{src}\n```")
    for o in cell.get("outputs", []):
        otype = o.get("output_type")
        if otype == "stream":
            out.append(f"```\n{''.join(o.get('text', []))}\n```")
        elif otype in ("execute_result", "display_data"):
            data = o.get("data", {})
            if "text/plain" in data:
                out.append(f"```\n{''.join(data['text/plain'])}\n```")
            # text/markdown, image/png, text/html available in data if you want them
```

Keep this opt-in — outputs can be enormous (bitmaps, multi-MB HTML).

## Anti-patterns

- **Assuming `source` is a string.** In valid ipynb it's an array of strings (one per line). Some exporters flatten to a single string; be defensive: `src = cell.get("source"); src = "".join(src) if isinstance(src, list) else src`.
- **Rendering empty cells.** A trailing empty markdown cell produces a blank `""` in the output and turns into a double-newline in the joined string. Filter `if src.strip()`.
- **Using `\n` as the joiner instead of `\n\n`.** Adjacent cells need blank-line separation to parse as independent markdown blocks.
- **Inlining base64 image outputs.** Data URIs can be multi-megabyte; either strip them or caption them via an LLM (see companion skill `image-as-data-uri-chat-completion`).

## Variations

- **Respect `metadata.kernelspec.language`.** Use it to pick the code fence language tag for non-Python notebooks.
- **Include execution counts**. Prefix code cells with `[N]: ` where N is `cell.execution_count`, if you want to preserve run order.
- **Tag-based filtering.** Notebooks can carry cell-level tags (`metadata.tags`); skip cells tagged `hide`, `private`, etc.
