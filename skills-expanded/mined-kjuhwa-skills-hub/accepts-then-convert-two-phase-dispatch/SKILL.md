---
name: accepts-then-convert-two-phase-dispatch
description: Two-method handler contract — a cheap accepts() that inspects metadata plus optional stream peek, and a convert() that does the real work — with a strict stream-position-invariant between the phases.
category: architecture
version: 1.0.0
tags: [architecture, dispatch, contract, binaryio, invariant, python]
source_type: extracted-from-git
source_url: https://github.com/microsoft/markitdown.git
source_ref: main
source_commit: 604bba13da2f43b756b49122cb65bdedb85b1dff
source_project: markitdown
source_path: packages/markitdown/src/markitdown/_base_converter.py
imported_at: 2026-04-18T00:00:00Z
confidence: medium
version_origin: extracted
---

# accepts() then convert() — two-phase handler contract

When a handler has to make a "should I touch this?" decision based on incomplete metadata and sometimes a peek at the input, split the contract into two methods: `accepts()` (cheap, side-effect-free, stream-position-preserving) and `convert()` (real work). Have the dispatcher call `accepts()` first, then call `convert()` only on the first affirmative hit. The invariant is: **`accepts()` must leave the stream exactly where it found it**, so `convert()` starts from a known position.

## The contract

```python
class DocumentConverter:
    def accepts(self, file_stream: BinaryIO, stream_info: StreamInfo, **kwargs) -> bool:
        """Cheap. MUST not change file_stream position."""
        raise NotImplementedError

    def convert(self, file_stream: BinaryIO, stream_info: StreamInfo, **kwargs) -> Result:
        """Real work. Assumes file_stream is at the position accepts() observed."""
        raise NotImplementedError
```

`accepts()` and `convert()` must share the exact same signature — if `accepts()` returns True, the dispatcher must be able to call `convert()` with the same arguments without any adapter.

## Fast path vs slow path inside accepts()

Most converters make the determination from metadata alone (extension + MIME prefix). When metadata is ambiguous, you sometimes need to read a few bytes and restore the stream. The idiom:

```python
def accepts(self, file_stream, stream_info, **kwargs) -> bool:
    # Fast path — metadata only, no I/O on the stream
    mimetype = (stream_info.mimetype or "").lower()
    extension = (stream_info.extension or "").lower()
    if extension in ACCEPTED_FILE_EXTENSIONS:
        return True
    for prefix in ACCEPTED_MIME_TYPE_PREFIXES:
        if mimetype.startswith(prefix):
            return True

    # Slow path — peek at the bytes, then restore
    cur_pos = file_stream.tell()
    try:
        header = file_stream.read(100)
        return _looks_like_my_format(header)
    finally:
        file_stream.seek(cur_pos)   # INVARIANT: pos unchanged on return
```

Note the `try/finally`: the seek-restore must run even if the peek raises.

## Dispatcher contract

```python
cur_pos = file_stream.tell()
for reg in sorted_converters:
    _accepts = False
    try:
        _accepts = reg.converter.accepts(file_stream, stream_info, **kwargs)
    except NotImplementedError:
        pass
    # Hard assertion — catch broken accepts() implementations in tests
    assert cur_pos == file_stream.tell(), (
        f"{type(reg.converter).__name__}.accepts() must not change stream position"
    )
    if _accepts:
        try:
            return reg.converter.convert(file_stream, stream_info, **kwargs)
        finally:
            file_stream.seek(cur_pos)   # reset for the next converter to have a fair look
```

Two critical details:

1. **Assert the invariant on every dispatch.** Catches the bug where a new contributor forgets the `finally: seek(cur_pos)` in `accepts()`. In production you can demote this to a warning, but never silently drop it.
2. **After `convert()` — succeed or fail — reset stream position.** If `convert()` raised, the next converter in the loop still needs the stream at the original position.

## Why this split

- **Cheapest rejection possible.** 90% of candidates are rejected on extension/mimetype alone, no I/O.
- **Peek-restore is localized.** The invariant lives inside one method, not spread across the dispatcher.
- **No adapter layer.** Because `accepts()` and `convert()` share a signature, there's nothing to wire up per converter.
- **Plugin-friendly.** Plugin authors write two methods, no inspection API.

## Peek-with-restore helpers

If you catch yourself repeating the `try/finally: seek(cur_pos)` idiom, wrap it:

```python
from contextlib import contextmanager

@contextmanager
def peek(stream):
    cur = stream.tell()
    try:
        yield stream
    finally:
        stream.seek(cur)

def accepts(self, file_stream, stream_info, **kwargs):
    ...
    with peek(file_stream) as s:
        header = s.read(100)
        return _looks_like_my_format(header)
```

## Anti-patterns

- **Consuming the whole stream in `accepts()`.** Any converter downstream now sees an empty stream. Peek only what you need; restore.
- **Relying on duck-typed return from `convert()` to mean "I accept, but actually I didn't."** `convert()` is the expensive path; don't let it be the decision point.
- **Different signatures between the two.** Breaks the no-adapter guarantee.
- **Not resetting position after a failed `convert()`.** The next attempt starts mid-stream and fails in a mysterious way.

## Variations

- **Async streams.** Same invariant, but use `await stream.tell()`/`await stream.seek(...)` and an async context manager.
- **Unseekable inputs.** Buffer into `BytesIO` before entering the loop (see companion skill `filestream-seekable-buffer-fallback`).
- **Multi-guess metadata.** If `stream_info` itself is uncertain, iterate over multiple `stream_info` guesses in an outer loop, converters in an inner loop.
