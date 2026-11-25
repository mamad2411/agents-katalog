---
name: large-text-file-stream-split
description: Stream-split a very large text file (build log, SQL dump, CSV, JSONL) into N byte-exact, LF-aligned chunks that any editor can open in constant memory; ships a portable single-source-file C program (any C89/C99 compiler — MSVC / gcc / clang / MinGW / tcc on Windows, Linux, macOS) plus a PowerShell build script, and emits a self-describing chunk-folder layout (predictable filenames encoding serial + global line range, `INDEX.csv` for machine lookup, `INSTRUCTIONS.md` for humans) so concatenating the chunks in alphabetical order reproduces the source byte-for-byte.
category: File Handling
---

# Large Text File Stream-Split Skill (v1)

When a text file (CI build log, SQL dump, JSONL trace, CSV export) grows past the point
where an editor can open it without thrashing — typically **> 100 MB**, certainly
**> 500 MB** — this skill splits it into N byte-exact, LF-aligned chunks. Each chunk
opens instantly in any editor, the chunk filenames make navigation obvious to humans
and machines, and concatenating the chunks in name order reproduces the source
**byte-for-byte**.

***

## 1. When to Use This Skill

Use this skill when ALL of the following hold:

- The source is a **text** file (UTF-8 or ASCII; not a binary blob).
- The file is large enough that opening it directly **hangs the editor** or refuses
  outright (VS Code's hard cap is 50 MB; most editors degrade well before 500 MB).
- Lossless round-trip matters — you need to be able to reconstruct the original
  byte-for-byte from the chunks.
- You don't need to *modify* the file — only read / search / share subsets of it.

If the file is small enough to grep directly or you need to edit it in-place, this
skill is overkill. If the file is binary, this skill's LF-boundary cut will corrupt
records — use a binary splitter instead.

***

## 2. Why C (and not PowerShell)?

The default automation language under
[script-management-rules.md](../../../ai-agent-rules/script-management-rules.md)
and the script-language mandate in
[ai-rule-standardization-rules.md §4](../../../ai-agent-rules/ai-rule-standardization-rules.md)
is **PowerShell**. This skill ships a C program instead, with the following documented
justification (required for any non-PowerShell script):

| Aspect                       | PowerShell 5.1                                          | C (this skill)               |
| :--------------------------- | :------------------------------------------------------ | :--------------------------- |
| Wall-clock on ~1 GB / 2M lines | minutes (interpreter overhead, byte-by-byte LF scans) | **~4 s** (verified)          |
| Memory                       | constant if carefully written, but easy to get wrong    | constant 4 MiB buffer        |
| Scope/state correctness      | script-scope leakage causes subtle off-by-one bugs      | local variables, no leakage  |
| Byte-exact LF boundary cut   | hard to get right; PS prefers `[string]` semantics      | trivial in C                 |

The build script (`scripts/build_split_log.ps1`) IS PowerShell and obeys the standard
script mandates. The C program is the single performance-critical leaf and is itself
small (< 200 LOC), portable, and dependency-free.

***

## 3. Environment & Dependencies

The skill ships **source**, not a binary. The user (or the agent) builds it once and
re-uses the executable.

| Requirement                | Verification                                              | Fallback                                                                 |
| :------------------------- | :-------------------------------------------------------- | :----------------------------------------------------------------------- |
| PowerShell 5.1+ or 7+      | `$PSVersionTable.PSVersion`                               | Always present on Windows; use [`pwsh`](https://aka.ms/powershell) on Linux/macOS |
| A C compiler on `$env:Path` | `Get-Command gcc, clang, cl -ErrorAction SilentlyContinue` | See §3.1 below                                                          |

### 3.1 Compiler Discovery Order

The build script tries, in order:

1. `gcc.exe` on `$env:Path`.
2. `clang.exe` on `$env:Path`.
3. `cl.exe` on `$env:Path` (MSVC; usually present inside a *VS Developer PowerShell*).
4. **Organization-specific fallback** — if your organization ships a toolbase with a
   bundled C compiler at a known root, plug its discovery in as a fourth step. See
   the canonical pattern in the general
   [`system-wide-tool-management`](../system-wide-tool-management/SKILL.md) skill;
   organizations that maintain an internal toolbase typically have a sibling skill
   that resolves a toolbase-mounted `gcc.exe` and prepends its `bin\` to `$env:Path`
   for the current session only.

If none of the above succeed, the build script prints actionable installation guidance
and exits non-zero.

***

## 4. Protocol

### 4.1 Phase 1 — Inventory the Source

Confirm the file is text and measure it before splitting (so the chunk-count target
is informed):

```powershell
$src = '<path-to-large-file>'
$fi  = Get-Item -LiteralPath $src
"Size : $($fi.Length) bytes / $([math]::Round($fi.Length / 1MB, 2)) MB"

# Sanity-check that it really is text (no NUL bytes in the first 1 MB).
$peek = [System.IO.File]::Open($src, 'Open', 'Read', 'ReadWrite')
$buf  = New-Object byte[] (1MB)
$null = $peek.Read($buf, 0, $buf.Length)
$peek.Close()
if ($buf -contains 0) { Write-Warning 'NUL byte in first 1 MB — file may be binary; this skill is for text only.' }
```

### 4.2 Phase 2 — Build the Splitter (once per machine)

```powershell
.\scripts\build_split_log.ps1
```

The build script is **idempotent** — it skips the rebuild if `split_log.exe` is newer
than `split_log.c`. Pass `-Force` to recompile unconditionally.

### 4.3 Phase 3 — Split

```powershell
# .\scripts\split_log.exe <source> <out_dir> [parts=100] [base_name=part]
.\scripts\split_log.exe '<source>' '<out_dir>' 100 '<base_name>'
```

Recommended chunk sizing:

| Source size | Chunks | Resulting chunk size | Comment                                  |
| :---------- | :----- | :------------------- | :--------------------------------------- |
| < 100 MB    | —      | —                    | Don't split. Editor can handle it.       |
| 100 MB – 1 GB | 100  | 1 – 10 MB            | Sweet spot for any editor                |
| 1 – 10 GB   | 500 – 1000 | 2 – 20 MB        | Keep chunks under ~20 MB                 |
| > 10 GB     | 1000+ | ~10 MB              | Cap chunk size, not chunk count          |

The `base_name` is embedded in every chunk filename. Pick something the human reader
will recognize at a glance — typically the source file's basename (e.g., `194` for
`#194.txt`, `query` for `slow_query.log`).

### 4.4 Phase 4 — Emit the Companion Files

The splitter produces `INDEX.csv` automatically but does **NOT** produce
`INSTRUCTIONS.md`. The chunk folder is not consumer-ready until the
self-describing `INSTRUCTIONS.md` is also present. Materializing it manually
from the template is error-prone (the most common skill-execution failure mode
is the agent forgetting this step entirely — see §7), so the skill ships an
automation script that renders the template with all placeholders filled from
`INDEX.csv` + the source file:

```powershell
.\scripts\emit_instructions.ps1 -OutDir '<out_dir>' -SourcePath '<source>'
# add -Force to overwrite an existing INSTRUCTIONS.md
```

The script auto-derives every placeholder (`SOURCE_FILENAME`, `SOURCE_SIZE_MB`,
`SOURCE_LINE_COUNT`, `CHUNK_COUNT`, `CHUNK_SIZE_MB`, `BASE_NAME`) from the
emitted `INDEX.csv` and the original source file's metadata, so the agent never
hand-substitutes values. The template itself lives at
[`templates/INSTRUCTIONS.md.template`](./templates/INSTRUCTIONS.md.template) and
remains the SSOT — `emit_instructions.ps1` only reads it.

### 4.5 Phase 5 — Verify Byte-Exactness

This step is **mandatory**. The skill's correctness contract is that
concatenation reproduces the source byte-for-byte.

```powershell
$src    = '<source>'
$chunks = Get-ChildItem '<out_dir>\<base>_part_*.txt' | Sort-Object Name
$rebuilt = Join-Path $env:TEMP '_rebuilt_split_check.tmp'
$out = [System.IO.File]::Create($rebuilt)
foreach ($c in $chunks) {
    $bytes = [System.IO.File]::ReadAllBytes($c.FullName)
    $out.Write($bytes, 0, $bytes.Length)
}
$out.Dispose()

$hSrc = (Get-FileHash -LiteralPath $src     -Algorithm SHA256).Hash
$hReb = (Get-FileHash -LiteralPath $rebuilt -Algorithm SHA256).Hash
if ($hSrc -ne $hReb) { throw "Round-trip MISMATCH: source $hSrc vs rebuilt $hReb" }
Remove-Item -LiteralPath $rebuilt
"Round-trip OK: $hSrc"
```

Also assert the companion files are both present — a missing `INSTRUCTIONS.md`
is a Phase 4 omission, not a split error, but it leaves the chunk folder
un-consumable for downstream humans:

```powershell
foreach ($f in 'INDEX.csv','INSTRUCTIONS.md') {
    $p = Join-Path '<out_dir>' $f
    if (-not (Test-Path -LiteralPath $p)) { throw "missing companion file: $p" }
}
```

If the hashes differ, the split is invalid — investigate the source for non-LF line
terminators (CR-only Mac Classic files) or mixed encodings before re-running.

***

## 5. Chunk Naming Convention (the SSOT)

```text
<base>_part_NNN_of_TTT__lines_SSSSSSS-EEEEEEE.txt
       │      │            │       │
       │      │            │       └─ end   global line in this chunk (inclusive)
       │      │            └─ start global line in this chunk (inclusive)
       │      └─ total number of chunks (zero-padded to width of TTT)
       └─ this chunk's serial (zero-padded, 1-based)
```

Properties this guarantees:

- **Serial visibility**: the predecessor and successor of any chunk are obvious
  (chunk `042` → neighbours `041` and `043`).
- **Alphabetical = source order**: lexicographic sort of the chunk folder gives the
  correct read order, because `TTT` is zero-padded.
- **Line range visibility**: a grep result like *"hit in line 87 of chunk 042"* can be
  translated to a global line number without consulting `INDEX.csv`
  (`global = chunk's StartLine + LocalLine - 1`).
- **Line ranges are NOT uniform**: chunks are byte-balanced, not line-balanced, so
  `EndLine - StartLine` varies. For exact mapping use `INDEX.csv`.

***

## 6. INDEX.csv Schema (the machine-readable SSOT)

```text
Part,FileName,StartLine,EndLine,LineCount,StartByte,EndByte,ByteSize
```

| Column     | Meaning                                                         | Indexing  |
| :--------- | :-------------------------------------------------------------- | :-------- |
| `Part`     | Serial number of this chunk                                     | 1-based   |
| `FileName` | The chunk file's basename (no path)                             | —         |
| `StartLine` / `EndLine` | First / last global line of the source in this chunk | 1-based, inclusive |
| `LineCount` | `EndLine - StartLine + 1`                                       | —         |
| `StartByte` / `EndByte` | First / last source byte offset in this chunk      | 0-based, inclusive |
| `ByteSize` | `EndByte - StartByte + 1`                                       | —         |

***

## 7. Pitfalls

| Pitfall                                                          | Failure mode                                       | Avoidance                                                                       |
| :--------------------------------------------------------------- | :------------------------------------------------- | :------------------------------------------------------------------------------ |
| Cut at byte offset (no LF alignment)                             | Concat-reproducibility holds, but every chunk has a half-line at each end → most editors render the first/last "line" wrong | Always cut at the next LF after the byte threshold (this skill's algorithm does it for you) |
| Static per-part target (`total / N`)                             | Always overshoot by LF-distance → either run out early (got 77 chunks, wanted 100) or last chunk huge (~13× over) | Use **dynamic** per-part target: `remaining_bytes / remaining_parts`, recomputed when each part opens (this skill's algorithm does it for you) |
| `Get-Content` to count lines on 1 GB file                        | OOM, hours of wall-clock                          | Use `StreamReader.ReadLine()` in a loop, or — better — let the splitter report the line count from its single pass |
| File has CR-only line endings (Mac Classic)                      | LF scan finds zero LFs → one giant chunk          | Pre-convert with `(Get-Content -Raw $f -Encoding utf8).Replace("`r", "`n") \| Set-Content ...`, or use a CR-aware splitter |
| `#` in source filename on POSIX shell                            | Shell treats it as start of comment               | Quote: `'./split_log #194.txt out 100 194'`                                     |
| Committing the chunk folder to Git                               | Repository bloat, useless history                  | `.gitignore` the chunk folder + the source — they are derived artifacts        |
| Editing a chunk in place                                         | Round-trip verification will fail                  | Treat chunks as **read-only**. Regenerate the source and re-split if needed.    |
| Stopping after `split_log.exe` returns — forgetting `INSTRUCTIONS.md` | Chunk folder has chunks + `INDEX.csv` but no human-readable navigation guide; downstream consumers re-discover the layout from scratch | Always run `scripts/emit_instructions.ps1` as Phase 4, and assert `INSTRUCTIONS.md` presence in the Phase 5 verification block |
| Em-dash / non-ASCII glyphs in PowerShell `.ps1` source saved without UTF-8 BOM | Windows PowerShell 5.1 reads source as ANSI → `â€"` mojibake → parser errors that cascade through the rest of the file | Use ASCII (`--`, `->`) in `.ps1` source, or save with UTF-8-with-BOM. The Markdown template can keep em-dashes — it is rendered, not parsed |

***

## 8. Related Skills

| Skill                                                                                                     | Relationship                                                                                          |
| :-------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------- |
| [`system-wide-tool-management`](../system-wide-tool-management/SKILL.md)                                  | **Compiler-discovery primitive** — used by the build script's PATH-first probe                        |
| [`archive-size-preflight-and-extract`](../archive-size-preflight-and-extract/SKILL.md)                    | **Sibling file-handling skill** — different problem (archive sizing + extraction), same disk-cost awareness; use it first when the source large text file arrives inside an archive |
| [Shell Execution Rules §2.5](../../../ai-agent-rules/shell-execution-rules.md)                            | **Invocation discipline** — `build_split_log.ps1` runs in the current session, no child PS subprocess |
| [Script Management Rules](../../../ai-agent-rules/script-management-rules.md)                             | **Script craftsmanship SSOT** — header style, `pwsh-preview` preference, `Common-Utils.ps1`           |
| [`redaction-portability`](../redaction-portability/SKILL.md)                                              | **Pre-commit audit** — chunk-folder `INSTRUCTIONS.md` MUST be redacted before sharing externally      |

For organizations whose workstations ship a toolbase-bundled C compiler that is not on
`$env:Path`, see your organization's internal interpreter-discovery skill (if one
exists) and add it as a fourth step in `build_split_log.ps1`'s compiler probe.

***

## 9. Hand-Back Verdict

After applying this skill, emit a 5-row verdict table so the consumer can audit the
result at a glance:

| Item                            | Value                                                       |
| :------------------------------ | :---------------------------------------------------------- |
| Source path / size              | e.g. `#194.txt` / 922.56 MB                                 |
| Chunk count / target chunk size | e.g. 100 / ~9.66 MB                                         |
| Chunk size spread (min – max)   | e.g. 5.8 MB – 12.6 MB (slack = LF-boundary alignment)       |
| Round-trip SHA-256 verification | **MUST be PASS** — paste the matching hash                  |
| Companion files emitted         | `INDEX.csv`, `INSTRUCTIONS.md`                              |
