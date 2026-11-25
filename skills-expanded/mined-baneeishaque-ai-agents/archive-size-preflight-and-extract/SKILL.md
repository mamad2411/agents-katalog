---
name: archive-size-preflight-and-extract
description: Pre-flight a zip / 7z / tar / tar.gz archive with 7-Zip before extracting — report compressed-on-disk size, uncompressed total, file count, folder count, and compression ratio so the user can decide if there is enough free disk space; then extract reliably to a sibling folder of the same name with progress-only output and verify the extracted size matches the pre-flight report. Includes NTFS cluster-overhead awareness for many-small-file archives.
category: File Handling
---

# Archive Size Preflight & Extract Skill (v1)

When the user asks **"how big is this zip?"**, **"how much disk space will the extracted
contents take?"**, or **"extract this archive"**, this skill drives the decision
sequence: **measure compressed → predict uncompressed → extract → verify**.

It deliberately uses **7-Zip** (`7z.exe`) for inspection and extraction instead of
PowerShell's built-in `Expand-Archive` / `[System.IO.Compression.ZipFile]` because:

- `Expand-Archive` is *slow* on large archives (hundreds of MB to multiple GB).
- The .NET ZipFile API silently truncates entries > 4 GB on Windows PowerShell 5.1.
- 7-Zip reports uncompressed size, file count, and folder count in one cheap `l` call
  **without extracting**, so the user can decide before paying the disk-space cost.
- 7-Zip handles `.zip`, `.7z`, `.tar`, `.tar.gz`, `.tar.bz2`, `.tar.xz`, `.rar`
  (read-only), and many others through one binary.

***

## 1. When to Use This Skill

Use this skill when ANY of the following hold:

- The user asks for the size of an archive (compressed, uncompressed, or both).
- The archive is large enough that **disk-space cost matters** (typically > 100 MB
  compressed, or > 500 MB uncompressed).
- The archive contains **many small files** — NTFS cluster allocation rounds every
  file up to the cluster size (typically 4 KiB), so the on-disk footprint can
  meaningfully exceed the logical byte sum (this skill warns about it).
- Reliable extraction with **progress feedback** matters (PowerShell's built-in
  cmdlet shows no progress on large extractions).

If the archive is < 50 MB and the user just wants the bytes inside, `Expand-Archive`
is fine — this skill is overkill.

***

## 2. Environment & Dependencies

| Requirement   | Verification                                                                                          | Fallback                                                                                                                                       |
| :------------ | :---------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------- |
| PowerShell    | `$PSVersionTable.PSVersion` (5.1+ or 7+)                                                              | Built-in on Windows                                                                                                                            |
| 7-Zip CLI     | `Get-Command 7z, "C:\Program Files\7-Zip\7z.exe", "C:\Program Files (x86)\7-Zip\7z.exe" -ErrorAction SilentlyContinue` | Install via `winget install 7zip.7zip` (or org-managed installer). Defer to the general [`system-wide-tool-management`](../system-wide-tool-management/SKILL.md) skill for the install protocol. |

The skill's scripts resolve `7z.exe` themselves via the discovery chain above (PATH
first, then the two canonical install roots), so callers do not need to pre-set `$env:Path`.

***

## 3. Protocol

### 3.1 Phase 1 — Compressed-on-Disk Size

Report the file's actual on-disk size with bytes + MB + GB:

```powershell
Get-Item -LiteralPath '<archive-path>' |
    Select-Object Name, Length,
        @{N='SizeMB';E={[math]::Round($_.Length/1MB,2)}},
        @{N='SizeGB';E={[math]::Round($_.Length/1GB,2)}}
```

### 3.2 Phase 2 — Uncompressed Pre-flight (no extraction)

Run the pre-flight script to parse 7-Zip's listing summary:

```powershell
.\scripts\Get-ArchiveSizeReport.ps1 -ArchivePath '<archive-path>'
```

Output (`PSCustomObject`):

| Property            | Meaning                                       |
| :------------------ | :-------------------------------------------- |
| `ArchivePath`       | Resolved absolute path                        |
| `CompressedBytes`   | On-disk size of the archive itself            |
| `UncompressedBytes` | Sum of all entry uncompressed sizes           |
| `FileCount`         | Number of file entries                        |
| `FolderCount`       | Number of folder entries                      |
| `Ratio`             | `UncompressedBytes / CompressedBytes` (×.x×)  |
| `UncompressedMB`    | Rounded display value                         |
| `UncompressedGB`    | Rounded display value                         |

**Cluster-overhead caveat the agent MUST surface** when `FileCount` is large
(rule of thumb: > 10 000 files): on a default NTFS volume with a 4 KiB cluster,
every file ≤ 4 KiB consumes a full 4 KiB on disk regardless of its logical size.
Mention this verbatim so the user understands the extracted footprint may exceed
`UncompressedBytes` by a non-trivial margin.

### 3.3 Phase 3 — Extract (sibling folder of same name)

By default, extract to a sibling folder named after the archive (without extension):

```powershell
.\scripts\Expand-ArchiveWithVerification.ps1 `
    -ArchivePath '<archive-path>' `
    [-OutputDir '<custom-output-dir>']
```

Internally the script invokes:

```text
7z x <archive> -o<output-dir> -bso0 -bsp1 -y
```

| Flag    | Effect                                                       |
| :------ | :----------------------------------------------------------- |
| `-bso0` | Suppress per-file stdout noise                               |
| `-bsp1` | Send progress (single percent line) to stdout                |
| `-y`    | Assume "yes" on any overwrite / password prompts             |

The progress line lets a wrapper tail it for status; without `-bso0` 7-Zip would
emit one stdout line per extracted entry — overwhelming for archives with tens of
thousands of files.

### 3.4 Phase 4 — Post-Extraction Verification

The extraction script then walks the output folder and confirms:

| Check                                         | Pass condition                                                       |
| :-------------------------------------------- | :------------------------------------------------------------------- |
| File count = pre-flight `FileCount`           | Equal                                                                |
| Folder count = pre-flight `FolderCount`       | Equal                                                                |
| Sum of file sizes = pre-flight `UncompressedBytes` | Equal (the .NET file-byte sum matches 7-Zip's reported total) |

Any mismatch is a **HARD FAIL** — the script returns exit code 1 with a diagnostic.
The success path emits a 6-row verdict (see §5).

***

## 4. Scripts

| Script                                                                                          | Purpose                                                                                |
| :---------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------- |
| [`scripts/Get-ArchiveSizeReport.ps1`](scripts/Get-ArchiveSizeReport.ps1)                        | Phase 1 + Phase 2 — resolve 7-Zip, parse `7z l` summary, emit the report object        |
| [`scripts/Expand-ArchiveWithVerification.ps1`](scripts/Expand-ArchiveWithVerification.ps1)      | Phase 3 + Phase 4 — extract via 7-Zip with progress, then verify the extracted footprint |

Both scripts are PowerShell-first per
[ai-rule-standardization-rules.md §4 (PowerShell-First mandate)](../../../ai-agent-rules/ai-rule-standardization-rules.md)
and cross-compatible with Windows PowerShell 5.1+ and PowerShell Core 7+.

***

## 5. Hand-Back Verdict

After running both scripts, the agent MUST present a 6-row verdict table so the
user can audit the run at a glance:

| Item                              | Value                                                                |
| :-------------------------------- | :------------------------------------------------------------------- |
| Archive path                      | Absolute path                                                        |
| Compressed (on disk)              | `<bytes>` (`<MB>` / `<GB>`)                                          |
| Uncompressed (pre-flight)         | `<bytes>` (`<MB>` / `<GB>`)                                          |
| File / folder count               | `<files>` files in `<folders>` folders                               |
| Compression ratio                 | `<×.xx>`                                                             |
| Verification                      | `PASS` (or `FAIL` with first divergence)                             |

***

## 6. Pitfalls

| Pitfall                                                                            | Symptom                                                              | Mitigation                                                                                                |
| :--------------------------------------------------------------------------------- | :------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------- |
| Using `Expand-Archive` on a multi-GB zip                                           | Wall-clock minutes → tens of minutes; no progress feedback           | Use this skill (7-Zip native binary)                                                                      |
| Using `[System.IO.Compression.ZipFile]` on Windows PS 5.1 for entries > 4 GB       | Silent truncation; downstream consumers read garbage                 | 7-Zip handles zip64 correctly                                                                             |
| Forgetting `-bso0` on a 30 000-file archive                                        | Terminal floods with per-file stdout lines                           | The shipped script always passes `-bso0 -bsp1`                                                            |
| Ignoring NTFS cluster overhead                                                     | "I have enough space" — extraction fills disk because 30 000 tiny files each take a full cluster | Surface the warning in §3.2 whenever `FileCount > 10 000`                                                 |
| Extracting into the current directory by mistake                                   | Archive contents pollute `$PWD`; no obvious folder to delete         | Default `-OutputDir` is `<archive-parent>\<archive-basename-without-ext>` — always a fresh sibling folder |
| 7-Zip not on `$env:Path`                                                           | `7z : The term '7z' is not recognized...`                            | Scripts fall back to `C:\Program Files\7-Zip\7z.exe` and `C:\Program Files (x86)\7-Zip\7z.exe`            |

***

## 7. Related Skills

| Skill                                                                                                     | Relationship                                                                                              |
| :-------------------------------------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------- |
| [`system-wide-tool-management`](../system-wide-tool-management/SKILL.md)                                  | **Tool-install primitive** — defer here to install 7-Zip if missing                                       |
| [`folder-comparison`](../folder-comparison/SKILL.md)                                                      | **Downstream verification** — once extracted, compare against a reference folder for content-level parity |
| [`large-text-file-stream-split`](../large-text-file-stream-split/SKILL.md)                                | **Sibling file-handling skill** — different problem (text-file splitting), same disk-cost awareness       |
| [Script Management Rules](../../../ai-agent-rules/script-management-rules.md)                             | **Script craftsmanship SSOT** — header style, `pwsh-preview` preference                                   |

***

## 8. Origin

Crystallised from a 2026-05-25 working-tree session where the user needed to know the
extraction footprint of a ~633 MB zip archive before committing the ~2.59 GB of disk
space it would consume. The 7-Zip summary line predicted **≈ 2 785 000 000 bytes /
34 053 files / 1 843 folders**; post-extraction verification matched byte-for-byte.
