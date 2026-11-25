---
name: read-jar
description: Use when the user wants to inspect the contents of a Java JAR file — list its entries, extract a specific entry's content, read bundled `.java` sources from a `-sources.jar`, or decompile its .class files back into Java source. Triggers on mentions of "jar", "jar 包", "JAR 文件", "看 jar 内容", "jar 里有什么", "jar 内有哪些类", "反编译 jar", "-sources.jar".
---

# Read JAR

Read the contents of a Java JAR file: list its entries, extract a single entry's content, decompile its `.class` files back into Java source, or read the `.java` sources bundled in a `-sources.jar`. Treats the JAR as a ZIP archive and does not parse bytecode by itself — decompilation is delegated to the CFR engine.

The entry-point is the script `scripts/read_jar.py` (Python 3, stdlib only), invoked relative to this skill's directory. Run it with `python3`, not `python`.

## Step 1: List entries

`python3 scripts/read_jar.py list <jar> [--match GLOB] [--json]`

- Prints one entry path per line, in archive order. Pure directory entries are skipped.
- `--match GLOB`: keep only entries whose name matches the glob (e.g. `*.properties`, `com/foo/*`). A pattern without wildcards degrades to substring matching.
- `--json`: print a JSON array `[{"path", "size", "compressed", "is_dir"}]`.

**Done when:** you have the entry list (or a filtered subset) you need.

## Step 2: Extract an entry

`python3 scripts/read_jar.py extract <jar> <entry> [--output PATH]`

- Text entries print their full content to stdout, never truncated.
- Encoding detection prefers `charset_normalizer`; if it is missing, the script falls back to UTF-8 → latin-1 heuristics. No setup step is needed.
- Binary entries (e.g. `.class`, images, nested zips) print a hex preview of the first 256 bytes plus a note on stderr.
- `--output PATH`: write the raw bytes to a file (auto-creates parent dirs; errors if the target already exists). Use this to pull a nested jar out so you can read it in turn — this skill does not recurse into jar-in-jar; it only peels one layer.

**Done**: the content is on stdout or written to the requested path.

## Step 3: Decompile to Java source

`python3 scripts/read_jar.py decompile <jar> --output DIR [--class GLOB]`

- Decompiles the jar's `.class` files into `.java` source under `DIR`, arranged by package path (e.g. `com/foo/Main.java`).
- `--class GLOB`: decompile only matching `.class` entries (same filter semantics as Step 1). Inner classes are emitted together with their outer class.
- `--output DIR` must not already exist.
- The CFR engine is downloaded on first use to `vendor/cfr-0.152.jar` inside this skill (version + SHA256 pinned in the script; `vendor/` is git-ignored). If CFR is unavailable, it downloads once and reuses offline thereafter.
- Decompilation failures are reported on stderr and skipped; the command still succeeds overall.

**Done**: the decompiled `.java` files exist under `DIR`, with a per-package directory structure matching the original class packages.

## Step 4: Read bundled sources (prefer over decompiling)

`python3 scripts/read_jar.py source <jar> <cls> [--output PATH]`

Many Maven builds ship source alongside the binary jar as a sibling `-sources.jar` (e.g. `app-1.2.3-sources.jar` next to `app-1.2.3.jar`). This step prefers the bundled `.java` over decompiling, and only falls back to CFR when a class genuinely has no source.

- `<cls>` accepts a `.class` path (`com/foo/Main.class`), a fully-qualified class name (`com.foo.Main`), a `.java` path (`com/foo/Main.java`), or a glob (batch). Class references are normalized to the matching `.java` entry.
- Mode is inferred from the jar's name:
  - `<jar>` ends with `-sources.jar` — **direct mode**: reads `.java` straight from it, no decompile fallback.
  - otherwise — **main-jar mode**: looks up the sibling `<basename>-sources.jar` in the same directory; if the sibling is missing or lacks a class's `.java`, that one class is decompiled via CFR as a fallback.
- Output dispatch:
  - No `--output`, single match: source text to stdout (bundled source first, decompile fallback only when needed).
  - No `--output`, multiple matches (glob): error, exit 3 — add `--output DIR` to materialize all.
  - `--output PATH`, single match: writes one file (errors, exit 4, if it already exists).
  - `--output PATH`, multiple matches: `PATH` is a directory (must not exist, exit 4); bundled sources are copied verbatim preserving package structure, missing ones are decompiled into it; a `materialized N/M` summary goes to stderr.

**Done**: the `.java` source is on stdout or materialized under the requested path.

## End-to-end example

User: "What configs are in this jar?"

1. `python3 scripts/read_jar.py list app.jar --match '*.properties'`
2. `python3 scripts/read_jar.py extract app.jar com/foo/config.properties`

User: "Show me the source of com.foo.Main in this jar."

1. `python3 scripts/read_jar.py source app.jar com.foo.Main` — returns the bundled `.java` from `app-sources.jar` if present
2. If no source is found, fall back to decompiling: `python3 scripts/read_jar.py decompile app.jar --output app_src --class 'com/foo/Main.class'`
3. `python3 scripts/read_jar.py extract app_src/com/foo/Main.java` (or read the file directly)

## Exit codes

0 success · 1 jar-level error (missing file / not a zip / CFR download failed) · 2 usage error · 3 entry not found (including no `.class` to decompile, or no source/class match for `source`) · 4 output target already exists.

## Vocabulary

See `CONTEXT.md` for the skill's language: **jar 包**, **读取**, **反编译**, **列清单**, **提取条目**, **条目过滤 (match)**, **二进制条目**, **嵌套 jar**, **sources jar**, **字符集探测**, **退出码**.
