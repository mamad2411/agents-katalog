---
name: ctf-forensics-disk
description: Disk and memory forensics CTF workflow — partition analysis, filesystem reconstruction, deleted file recovery, file carving, memory dump analysis (Volatility), disk image mounting, LUKS encrypted volume recovery, APFS/ZFS snapshot analysis, Docker layer extraction, RAID reconstruction, VMware snapshot conversion, and MFT/USN journal parsing for authorized lab/competition material.
disable-model-invocation: true
risk: passive
allowed-modes: [ctf, forensic]
authorization-required: yes
evidence-outputs: [artifact-hash, timeline-notes, recovery-notes, redacted-evidence]
---

# Disk and memory forensics — authorized CTF and lab workflow

Use this skill to analyze disk images, filesystem dumps, and memory captures obtained from authorized CTF challenges, competition-provided artifacts, or sanctioned lab exercises. The workflow chains low-level image inspection, partition enumeration, filesystem reconstruction, deleted content recovery, signature-based carving, and memory forensics into a systematic investigation pipeline. All operations must be read-only against the original evidence; never mutate the primary artifact. This skill is for competition and lab contexts only — production system forensics requires separate chain-of-custody procedures and must not be routed through this skill.

## Required inputs

- Disk image, memory dump, hibernation file, or filesystem snapshot from an authorized CTF challenge, lab exercise, or competition platform. The source must be documented: competition name, challenge name, hash, and date received.
- Written lab rules or competition scope: allowed tools, time limits, flag formats, out-of-bounds IP ranges, and any restrictions on network contact or external services.
- Separate proof of registration or lab enrollment for the target competition. CTF platform credentials, team token, or lab access key must not be stored in evidence.
- For memory dumps: approximate capture context. Was the dump taken during user activity, after a compromise event, or from a snapshot? Context informs the triage priority.
- Known flag format for the challenge (e.g., `flag{...}`, `CTF{...}`, hex-encoded output). Flag format drives string searches and carving filters.
- Authorization cache valid for the scope of this specific challenge or lab artifact.

## Required gates

1. `pentest_agent_load_config` → `pentest_agent_validate_policy`. Confirm the repo configuration permits forensic-mode tooling and CTF-mode execution before any image access.
2. `pentest_agent_parse_scope` with competition rules, lab boundaries, challenge metadata, and any network-contact restrictions.
3. `pentest_agent_validate_target` before mounting, before any tool execution against the image, and before any external lookup triggered by extracted data.
4. `pentest_agent_check_authorization` after scope validation. Authorization must be challenge-specific — a CTF platform login for one competition does not authorize forensic work on a different challenge.
5. `pentest_agent_build_command` for every catalog tool invocation. Dry-run the argv preview, confirm read-only flags, and verify the output path target before execution.
6. `pentest_agent_execute_tool` for all tool execution. Never run raw shell, never pipe tool output through unapproved scripts, and never use shell interpolation to construct tool arguments.
7. `pentest_agent_append_evidence` after each completed phase. Record hashes, tool names, output summaries, and redaction notes incrementally.
8. `pentest_agent_record_finding` → report handoff when a flag is recovered or a significant artifact is identified.

## Workflow

### Phase 1 — image intake, hashing, and format identification

Before any inspection step, establish a verifiable baseline for the artifact:

1. Compute the SHA-256 hash of the disk image, memory dump, or filesystem snapshot. Record the hash in the evidence log immediately. This hash becomes the primary identifier for all subsequent phases and prevents confusion when multiple images are in play.
2. Compute a secondary hash (SHA-1 or BLAKE3) for cross-reference if the challenge platform publishes an expected hash.
3. Record the artifact metadata: file size in bytes, file name as received, any embedded timestamps, and the source attribution (competition name, challenge name, download date).
4. Identify the image format using `file` via `pentest_agent_execute_tool`. Common CTF formats include: raw disk dump (dd-style, identified as "DOS/MBR boot sector"), EnCase evidence files (E01, identified by the "EVF" signature at offset 0), Advanced Forensic Format (AFF, identified by the "AFF" header), QEMU QCOW2 (identified by the "QFI" magic at offset 0), VMware VMDK (identified by the "KDMV" descriptor or the sparse extent header), and VirtualPC/VirtualBox VHD (identified by the "conectix" magic string).
5. If the image is compressed (gzip, bzip2, xz, zip), decompress to a working copy. Never decompress in-place over the original file. Record the decompressed hash as a derived artifact.
6. For split images (`.aa`, `.ab`, `.ac` suffix from `dd` splitting, or numbered `.001`/`.002` chunks from archive splitters), reassemble using `cat` via `pentest_agent_execute_tool`, then hash the reassembled image.

### Phase 2 — partition table enumeration and filesystem discovery

Once the image format is understood and hashed, map its internal structure:

1. If the image is a full-disk dump (not a single partition), list the partition table using Sleuth Kit `mmls`. The output identifies: partition type (DOS/MBR vs GPT), partition start sector, partition length in sectors, and partition table slot number.
2. For each partition, compute the sector offset (start sector multiplied by sector size, typically 512 bytes). This offset is required for all subsequent Sleuth Kit commands that operate on a specific partition.
3. Identify the filesystem type for each partition using Sleuth Kit `fsstat` at the partition offset. Common CTF filesystems: ext2/ext3/ext4 (Linux), NTFS (Windows), FAT32/exFAT (USB drives, EFI partitions), HFS+ (older macOS), APFS (modern macOS), XFS (enterprise Linux), Btrfs (modern Linux), ZFS (Solaris/FreeNAS), and ISO 9660/UDF (optical media).
4. For GPT partitioned disks where `mmls` shows a "GPT Header" entry, also check for a protective MBR at sector 0 and a backup GPT at the final 34 sectors of the image. A corrupt primary GPT can sometimes be recovered from the backup.
5. For unrecognized partition types or filesystems where `fsstat` reports "Unknown", broaden the search: scan for known superblock magic bytes at common offsets. ext superblocks appear at byte offset 1024 (magic 0xEF53), NTFS at sector 0 (magic "NTFS"), FAT at sector 0 (magic 0xEB or 0xE9 with "MSDOS" or "FAT" strings), and Btrfs at offset 0x10040 (magic "_BHRfS_M"). This superblock search is conceptual — hand the offset and suspected type to `pentest_agent_build_command` for tool-driven verification.
6. Mount partitions read-only if the operating system supports the filesystem natively. Use the loop device approach via `pentest_agent_build_command` with explicit read-only flags. If mounting is not feasible (unsupported filesystem, encrypted volume, or structural corruption), proceed with Sleuth Kit tools for direct filesystem access without a mount point.

### Phase 3 — file listing, timeline extraction, and known-artifact search

With the filesystem identified and accessible (mounted or via Sleuth Kit):

1. Enumerate all files and directories using Sleuth Kit `fls` in recursive mode. This produces a bodyfile-format listing: inode, name, type (r=regular, d=directory, l=link, v=virtual), size, and MAC times.
2. Filter for files matching the challenge theme: if the challenge title mentions "stolen document" or "exfiltrated data", look for recent files in user directories. If the challenge mentions "hidden message", look for files with unusual names (dot-prefixed, whitespace-only, Unicode homoglyphs).
3. Search for flag-pattern matches in file names: use `grep` via `pentest_agent_execute_tool` against the file listing output. A flag might be embedded in a file name rather than file content.
4. Check common directories that hold user-generated content: `/home/*/Documents`, `/home/*/Downloads`, `/home/*/Desktop`, `C:\Users\*\Documents`, `C:\Users\*\Downloads`, `C:\Users\*\Desktop`.
5. Look for recently modified or recently created files within the expected attack timeframe. Sort the file listing by modification time descending and triage the top entries.
6. Generate a bodyfile-format timeline using Sleuth Kit `fls -m` for integration with timeline analysis tools. Sort chronologically. This timeline becomes the backbone for identifying anomalous activity windows.
7. Check for alternate data streams (ADS) on NTFS: files on NTFS can have multiple data streams beyond the default unnamed stream. The primary stream is accessed as `filename`, while alternate streams are accessed as `filename:streamname`. Malicious actors may hide data in alternate streams because they are not visible in standard directory listings. Use Sleuth Kit `fls` with ADS support or `dir /r` equivalent to enumerate streams.
8. Check for hidden files and directories that are masked by rootkits, file attribute flags (Windows hidden/system), or dot-prefixed names (Linux). On Windows, check the `ATTRIB` column for H (hidden) and S (system) attributes. On Linux, files named `... ` (dots with trailing space) or files with backspace characters in the name appear different in a terminal listing than on disk.
9. For files with apparent zero size but non-zero inode metadata: a zero-size file may have content stored in alternate locations — NTFS resident data, ext4 inline data (data stored in the inode itself for files under ~60 bytes), or fork-based storage on HFS+. If `fls` reports size 0 but the inode allocation suggests data was once present, check for inline data.
10. For log and history files that are append-only: check the end of log files for the most recent entries. The flag may have been written to a log file by an application or script shortly before the system was imaged. Common log paths: `/var/log/`, `C:\Windows\Logs\`, `C:\ProgramData\`, and application-specific log directories.

### Phase 4 — deleted file recovery

Files that have been deleted but not overwritten are recoverable from filesystem metadata:

1. List deleted files using Sleuth Kit `fls` with the deleted-flag enabled. Deleted entries show as type "r" (regular file, deleted) or "d" (directory, deleted) with the filename often prepended with `$` or marked as `(deleted)`.
2. For each deleted file of interest, compute the inode number from the `fls` output. Recover the file content using Sleuth Kit `icat` specifying the inode. Direct recovered content to a separate working directory — never overwrite the recovery output.
3. Check file content for flag patterns using `strings` and `grep` via `pentest_agent_execute_tool`. Many CTF flags are stored in text files that are deleted but still resident in unallocated space.
4. For NTFS images: the Master File Table (MFT) keeps small files (< approximately 700 bytes) as resident data directly within the MFT entry itself. These "resident" files survive deletion more readily than non-resident files. Parse the MFT using Sleuth Kit tools; resident data for deleted small files may still be intact.
5. For ext3/ext4 images: the journal records recent metadata changes. If a file was deleted recently, the journal may still contain the inode block pointers needed for recovery. Use `extundelete` (via `pentest_agent_build_command` and `pentest_agent_execute_tool`) to attempt journal-based recovery.
6. Check trash and recycle locations: `$Recycle.Bin` on NTFS contains metadata about deleted files (each deleted file gets a pair of files: `$Ixxxxxx` with metadata and `$Rxxxxxx` with the actual content). On Linux, check `~/.local/share/Trash/` and partition-root `.Trash-*/` directories. Trash files retain their original content and are often overlooked.
7. For APFS filesystems: deleted files may remain in the APFS snapshot referred to by the file system tree until the space is reclaimed. Use APFS-specific recovery tools (via `pentest_agent_build_command`) to parse the APFS object map and space manager for recently freed blocks. The checkpoint structure in APFS may preserve older versions of the filesystem tree that still reference deleted files.
8. For XFS filesystems: XFS uses extent-based allocation with B+tree indexing. Deleted files have their extents freed but the inode core (which stores the file type, permissions, and extent list for small files) may persist in the inode B+tree until the inode chunk is reallocated. Search for orphaned inodes that still have intact extent maps.
9. For Btrfs filesystems: Btrfs uses copy-on-write, meaning deleted file data may exist in older tree roots that have not been garbage-collected. Use Btrfs recovery tools (via `pentest_agent_build_command`) to enumerate all tree roots and inspect older generations of the subvolume tree. A file deleted in the current generation may still be fully intact in a previous generation.

### Phase 5 — file carving

When filesystem metadata is damaged, deleted, or the file has been partially overwritten, signature-based carving recovers content by scanning for file headers and footers in the raw image:

1. Identify the file types most relevant to the challenge: if the challenge involves a "hidden image", carve for JPEG (header `FF D8 FF E0` or `FF D8 FF E1`, footer `FF D9`) and PNG (header `89 50 4E 47 0D 0A 1A 0A`, footer `49 45 4E 44 AE 42 60 82`). If the challenge involves a "stolen archive", carve for ZIP (header `50 4B 03 04`), RAR (header `52 61 72 21`), and 7z (header `37 7A BC AF 27 1C`).
2. Use `foremost` via `pentest_agent_execute_tool` with the default configuration for a first-pass carve. `foremost` uses header/footer signature pairs and writes carved files to a dated output directory. Run against the full image.
3. Use `photorec` via `pentest_agent_execute_tool` for a more exhaustive carve. `photorec` uses file-type recognition based on internal data patterns rather than simple header/footer matching, so it can recover fragments that `foremost` misses. Let it run against the full image; it may identify 30+ file types.
4. Use `binwalk` via `pentest_agent_execute_tool` to detect files embedded within other files. A ZIP archive appended to a JPEG (steganography via concatenation), an ELF binary embedded in a PNG after the IEND chunk, or a PDF hidden in a slack space region all register in `binwalk` output.
5. After carving completes, scan the carved output directory for flag patterns. Use `strings` via `pentest_agent_execute_tool` with the minimum string length set to the expected flag length. Cross-reference with the known flag format.
6. For documents (PDF, DOCX, ODT): these are ZIP archives internally. If `binwalk` finds a ZIP signature, extract the ZIP and inspect the internal XML for flag text.
7. Carving for unstructured data: if the challenge involves a database dump (SQLite, MySQL IBD files, PostgreSQL heap files), the flag may exist in database records. SQLite databases can be carved by searching for the SQLite header (`53 51 4C 69 74 65 20 66 6F 72 6D 61 74 20 33 00`). Once carved and reassembled, query the database for flag-formatted strings across all tables.
8. Carving for email archives: MBOX files start with `From ` at the beginning of a line. PST files have the signature `!BDN`. EML files start with MIME headers (`From:`, `To:`, `Subject:`). If the challenge narrative mentions stolen emails, prioritize these signatures.
9. Carving for registry hives: Windows registry hives have the signature `regf` at offset 0. A carved registry hive can be parsed for flag strings in key names, value names, or value data. This is especially relevant if the challenge provides a damaged disk image where the filesystem is partially corrupted but hive signatures are intact.
10. Validate carved files: not every carved file is valid. Check each carved output: for images, attempt to decode with an image viewer. For archives, attempt `unzip -t` or `tar -t` to verify integrity. For PDFs, check the `%%EOF` trailer. A carved file with a valid header but corrupted content may need manual repair — for example, a JPEG missing the JPEG trailer can still be partially decoded.

### Phase 6 — memory dump analysis with Volatility

Memory dumps capture the system state at a point in time. Use Volatility for structured analysis:

1. Identify the operating system profile. For Windows dumps, use Volatility `windows.info` (Volatility 3) or `imageinfo` (Volatility 2) to detect the Windows version, service pack, and architecture. For Linux dumps, use `linux.banner` to read the kernel banner string. For macOS dumps, use `mac.banner`.
2. List running processes with `windows.pslist` / `linux.pslist` / `mac.pslist`. Look for suspicious process names (randomized, misspelled system process names, processes running from temporary directories, processes with anomalous parent-child relationships). Cross-reference process names with known malware or CTF challenge themes.
3. List network connections with `windows.netscan` / `linux.sockstat`. Identify established connections, listening ports, and recently closed connections. In a CTF context, look for connections to attacker-controlled IPs or unusual high ports.
4. Extract command-line arguments for each process with `windows.cmdline` / `linux.psaux`. The flag may be passed as a command-line argument to a script, embedded in an environment variable, or visible in the process start command.
5. Dump the memory of a specific process using Volatility `windows.memmap` or `windows.dumpfiles` for the target process ID. After dumping, run `strings` on the extracted memory and search for flag patterns. Process memory often contains plaintext secrets, passwords passed as arguments, and decrypted file content.
6. For Windows memory dumps: check the registry hives in memory. Use Volatility `windows.registry.hivelist` to enumerate loaded hives, then `windows.registry.printkey` to explore specific keys. Look at `NTUSER.DAT` → `Software\Microsoft\Windows\CurrentVersion\Explorer\RecentDocs` for recently accessed files, `RunMRU` for executed commands, and `UserAssist` for GUI application launch history.
7. Search for bash history in Linux dumps: use `linux.find_file` to locate `.bash_history` inode, then `linux.dumpfiles` to extract it. Do the same for `.zsh_history`, `.python_history`, and `.mysql_history`.
8. For Windows dumps, check for PowerShell history: `ConsoleHost_history.txt` in the user's AppData directory. This file records every PowerShell command typed, making it a high-value artifact for finding commands that involve flags or flag manipulation.
9. Search for text editor recovery files: vim swap files (`.swp`, `.swo`), Emacs auto-save files (`#filename#`), and nano emergency save files (`filename.save`). These may contain an earlier version of a file before deletion or modification.
10. For Linux memory dumps, enumerate the dentry cache via Volatility's `linux.dentry_cache` plugin. This reveals recently accessed file paths that may have been deleted from disk but are still cached in kernel memory. A flag file read seconds before the dump was taken may be recoverable even if the file itself is gone from the filesystem.
11. For macOS memory dumps, extract the process working directory from the `proc_info` structure — this may point to a hidden directory where flag artifacts were staged. Also check the dyld shared cache for recently loaded dynamic libraries; a suspicious library injected into a legitimate process may reveal the attack vector.

### Phase 7 — encrypted volume handling

Encrypted volumes appear in CTF challenges where the passphrase or key must be recovered:

1. Identify encrypted volume type using `file` via `pentest_agent_execute_tool`. A LUKS volume reports as "LUKS encrypted file" with a header identifying the cipher and mode. A BitLocker volume shows the "-FVE-FS-" signature at the volume start. A FileVault 2 volume appears as a CoreStorage logical volume group. A VeraCrypt/TrueCrypt volume has no distinguishing header (by design — plausible deniability) but can be identified by high entropy across the entire volume with no recognizable filesystem structures.
2. For LUKS volumes: extract the LUKS header using Sleuth Kit tools via `pentest_agent_execute_tool`. The header contains the cipher name, cipher mode, hash function, key slots, and the encrypted master key. Examine which key slots are active — an inactive key slot may indicate a forgotten passphrase that was never used, but an active slot with a weak passphrase is the attack vector.
3. For passphrase recovery on LUKS: run `hashcat` mode 14600 via `pentest_agent_build_command` and `pentest_agent_execute_tool`. Mode 14600 targets the LUKS header directly. Supply a wordlist built from the challenge context: if the challenge description mentions a specific date, person, or event, build a targeted wordlist with mutations. If the challenge gives a hash from a companion file, cross-reference for a shared passphrase.
4. For AES key recovery from memory: if a memory dump of the running system is available alongside the encrypted volume, extract the AES key schedule from the dump using `aeskeyfind` via `pentest_agent_execute_tool`. The LUKS master key is held in kernel memory while the volume is mounted. `aeskeyfind` scans memory for AES key schedules (the expanded round keys) and outputs candidate keys. Test each candidate against the LUKS header to identify the valid master key.
5. For BitLocker volumes: the recovery key may exist in a memory dump. Search the memory dump for the string "BitLocker Recovery Key" followed by the 48-digit recovery key pattern. If an Active Directory backup or a Microsoft account recovery key is available and authorized for the challenge, use it. BitLocker also stores the VMK (Volume Master Key) in memory while mounted — search for the FVE metadata block signature `-FVE-FS-` and extract the key chain.
6. For FileVault 2: if the challenge provides institutional escrow data or a recovery key, use it directly. Otherwise, check memory for the FileVault master key near CoreStorage kernel structures.
7. For simple encryption (openssl enc, gpg symmetric, zip with password): the file header identifies the format. Use `hashcat` with the appropriate mode: ZIP (mode 13600 for ZIP2.0, various modes for WinZip AES), 7z (mode 11600), RAR5 (mode 13000), PDF (modes 10500/10600/10700 depending on version), and OpenSSL enc (mode 22300 for salted format).
8. For steganographic encryption where the encrypted data is disguised as a benign file: the file may appear as a valid JPEG or PNG that can be opened and viewed normally, but hidden data exists in appended bytes after the image end marker, in comment fields, or in subtly modified pixel values. After standard encryption cracking fails, consider that the file format itself may be a decoy — analyze with `binwalk` and `steghide` via `pentest_agent_execute_tool`.
9. When multiple encrypted volumes share the same passphrase: if the challenge provides a LUKS volume and a companion encrypted ZIP, and one of them yields to a wordlist attack, immediately test the recovered passphrase against all other encrypted artifacts. CTF authors frequently reuse the same passphrase across multiple layers to reward successful cracking of the first layer.
10. For key file-based encryption: some LUKS configurations use a key file (stored on a USB drive, integrated into the initramfs, or hidden as a specific byte range in another file) rather than a passphrase. If no passphrase crack succeeds and the challenge mentions a companion file or a specific device, the companion may be the key file — check its size (typically 2048–8192 bytes of random data for LUKS key files) and provide it to the decryption tool.

### Phase 8 — specialized filesystem and artifact scenarios

Beyond standard filesystem analysis, several CTF-relevant scenarios require targeted techniques:

1. **APFS snapshots**: APFS filesystems on macOS support snapshots for Time Machine backups. A snapshot preserves the filesystem state at a point in time — files that were deleted after the snapshot was taken are still present inside the snapshot. List snapshots using APFS tools via `pentest_agent_execute_tool`. Mount the most relevant snapshot read-only and enumerate its files. A flag file deleted post-snapshot may still be recoverable from the snapshot.
2. **ZFS datasets and snapshots**: ZFS supports recursive snapshots of datasets. Use `zfs list -t snapshot` via `pentest_agent_execute_tool` to enumerate available snapshots. Clone a snapshot to a temporary mount point and inspect for files deleted in the live dataset.
3. **Docker container layers**: Container images are composed of overlay layers, each stored as a tar archive containing only the files changed in that layer. If a flag file was created in an early layer and deleted in a later layer, the file still exists in the early layer. Use the Docker image inspection tools via `pentest_agent_execute_tool` to enumerate layers in order. Extract each layer archive individually and search for the flag across all layers.
4. **Git repositories within disk images**: If the disk image contains a `.git` directory, the commit history may contain flag files that were committed and later removed. Run `git log --all --full-history -- <path>` via `pentest_agent_execute_tool` to trace a file's history across all branches. Dangling blobs in `.git/objects` (objects not reachable from any ref) may also contain flag content — use `git fsck --lost-found` to recover them.
5. **VMware snapshot and suspend files**: A VMware virtual machine snapshot (`.vmsn`) captures the VM state including memory. Convert `.vmsn` to a raw memory dump using Volatility tools via `pentest_agent_execute_tool`, then analyze with the memory forensics workflow from Phase 6. The suspend file (`.vmss`) is equivalent to a memory dump of the paused VM — analyze it directly as a memory image.
6. **RAID reconstruction**: If the challenge provides multiple disk images labeled as RAID members, determine the RAID level from the provided metadata or challenge description. For RAID 0 (striping), concatenate stripes in order using size and stripe-width clues. For RAID 1 (mirroring), any single disk contains the full data. For RAID 5 (striping with distributed parity), identify the parity rotation pattern and rebuild missing data. SoftRAID metadata (mdadm superblock) at the end of each disk identifies the array UUID, member index, and layout.
7. **MFT and USN Journal parsing for NTFS**: The Master File Table ($MFT) records every file and directory on an NTFS volume. Parse it to recover file names, timestamps, and data runs even for deleted files whose directory entries have been reused. The Update Sequence Number Journal ($UsnJrnl) records every filesystem change (create, modify, delete, rename) with a timestamp and reason code — it can reveal when a flag file was created, modified, or deleted even if the file itself is unrecoverable.
8. **Hibernation file analysis**: A Windows hibernation file (`hiberfil.sys`) contains a compressed snapshot of physical memory at the time of hibernation. Use Volatility via `pentest_agent_execute_tool` to convert it to a raw memory dump, then analyze with the memory forensics workflow. The hibernation file uses a proprietary compression (Xpress Huffman) and includes a header with the signature "hibr" at offset 0 and the compression algorithm identifier at offset 4. Decompression yields a raw memory image that Volatility can ingest.
9. **Crash dump analysis**: Windows crash dump files (`.dmp`, `MEMORY.DMP`) contain a subset of physical memory at the time of a system crash (BSOD). Small memory dumps (64KB–256KB) contain only the crash stack and register context — useful for identifying the crashing module but not for broad forensic analysis. Kernel memory dumps and complete memory dumps contain enough data for full Volatility analysis. Parse the dump header to determine the dump type and the physical memory ranges included.
10. **Swap and page file analysis**: On Linux, the swap partition or swap file contains pages evicted from physical memory. On Windows, `pagefile.sys` serves the same purpose. While swap lacks the structure of a memory dump (no process list, no kernel data structures), a plain `strings` search across the swap space can recover plaintext secrets that were in memory but paged out. Search for flag patterns, passwords, and decrypted content that was briefly resident in a process's address space before being swapped.
11. **Thumbcache and thumbnail analysis**: Windows thumbnail caches (`thumbcache_*.db` files in `%LOCALAPPDATA%\Microsoft\Windows\Explorer`) store small preview images of files browsed in Explorer. These persist after the original file is deleted. Extract thumbnail images from the cache database and inspect visually — the flag may be a screenshot, a rendered document, or an image that the user viewed before deletion. The thumbcache also stores the original file's path and last-modified timestamp, providing a timeline of what files were viewed and when.

### Phase 9 — Windows artifact triage (when Windows partitions are present)

Windows systems generate rich forensic artifacts. Triage them in order of evidential value:

1. **NTUSER.DAT registry hive** (per user): Contains `RecentDocs` (file access history by extension), `RunMRU` (commands typed in the Run dialog), `UserAssist` (GUI application launch counts and last execution times in ROT-13 encoded format), and `TypedURLs` (URLs typed into Internet Explorer address bar). Parse these keys via `pentest_agent_execute_tool` with the appropriate registry parsing tool.
2. **Amcache.hve** (Windows Application Experience): Records application execution with SHA-1 hash, file path, and first-seen timestamp. This survives application uninstallation, making it valuable for identifying tools the attacker executed and then removed.
3. **Prefetch files** (`C:\Windows\Prefetch\*.pf`): Record application execution count and last execution timestamp (up to 8 prior executions). The filename is the application name followed by a hash of the full path. Parse the embedded metadata: run count, last run times, and files loaded by the application (up to the first 10 seconds of execution). The files-loaded list reveals which DLLs and data files the application accessed — a suspicious executable that reads `ntds.dit` or `SAM` is performing credential dumping.
4. **LNK files** (shortcut/`.lnk`): Store the target path, arguments, working directory, and MAC timestamps of the target file. LNK files are created when a user double-clicks a file, drags to the taskbar, or opens a recently used document. Parse LNK files from `Recent` folders and the Start Menu. The LNK target path may point to a file on a removable drive, revealing the drive letter and volume serial number — this can link the artifact to a specific USB device.
5. **Jump Lists** (`*.automaticDestinations-ms` and `*.customDestinations-ms`): Track recently opened files per application, stored as OLE compound files containing LNK-format stream entries. Parse with the appropriate Jump List tool to recover application-specific file access history. The AppID in the filename identifies the application — cross-reference the Jump List entries with the application that produced them.
6. **SRUM** (System Resource Usage Monitor, `C:\Windows\System32\sru\SRUDB.dat`): An ESE database that records per-process network usage (bytes sent/received), per-application energy consumption, and per-application CPU time with hourly granularity. This can show data exfiltration through network byte counts for unexpected processes. A process that sends megabytes of data but is not a browser or email client may be exfiltrating data. Parse the SRUM database tables for network data usage and application resource usage.
7. **Event Logs**: `Security.evtx` (logon events 4624 for successful logons and 4625 for failures, privilege escalation 4672, process creation 4688 with command line if enabled, audit policy change 4719), `System.evtx` (service starts/stops 7045, time changes 4616, driver load failures, crash dumps), and `Application.evtx` (application errors and crashes). Filter for events in the incident time window. Event ID 4688 with command-line logging enabled is the highest-value single event type for attacker activity reconstruction — it captures every process start with the full command line and parent process ID.
8. **Shellbags**: Registry keys that record folder view preferences. Each subkey encodes a folder path that the user opened in Explorer, along with the window position and view mode. Even after the folder is deleted, the Shellbag entry persists. Parse with the appropriate tool to recover folder browsing history. Shellbags can reveal access to encrypted volumes (the user browsed into the VeraCrypt mount point), network shares (UNC paths), and removable drives.
9. **BAM/DAM** (Background Activity Moderator / Desktop Activity Moderator): Registry keys under `SYSTEM\CurrentControlSet\Services\bam\State\UserSettings\` that record the last execution time of every executable run on the system, including those executed as `SYSTEM`. This survives application uninstallation and is difficult for attackers to clear without administrative registry access. Cross-reference BAM entries with Prefetch to confirm execution.
10. **RecentFileCache.bcf**: A binary file at `C:\Windows\AppCompat\Programs\RecentFileCache.bcf` that records recently executed applications with their full path and last-modified timestamp. This is a simpler but effective artifact for identifying newly introduced executables. Parse the file structure (a list of UTF-16LE file paths with a header) and check for unusual paths.

### Phase 10 — timeline assembly and anomaly detection

Build a unified timeline across all recovered artifacts to identify patterns:

1. Collect timestamped events from all sources: filesystem MAC times (from `fls -m`), MFT entry timestamps (both $STANDARD_INFORMATION and $FILE_NAME attribute sets — they can differ, indicating timestamp manipulation), USN Journal entries, registry key last-write timestamps, Event Log timestamps, and Prefetch execution timestamps.
2. Normalize all timestamps to UTC for comparison. Filesystem timestamps from FAT32 are local time; NTFS and ext4 store UTC. Document the timezone assumptions.
3. Sort all events chronologically into a single timeline. Identify clusters of activity: a burst of file creates, deletes, and registry modifications within a short window suggests an automated tool or script ran at that time.
4. Look for anti-forensic indicators: timestamps that are in the future (system clock rollback), $STANDARD_INFORMATION timestamps that differ from $FILE_NAME timestamps (timestomping — deliberate timestamp alteration), or gaps in the activity record where expected artifacts are missing.
5. Correlate the timeline with the challenge narrative. If the challenge describes an intrusion at a specific date, zoom to that window and catalog every event. The flag is often created, moved, or referenced during the attacker's activity window.
6. Identify the attacker's first presence on the system: the earliest artifact attributable to the attacker (first malicious process execution, first suspicious file creation, first anomalous logon). This is the pivot point — everything before it is baseline, everything after is in scope for detailed review.
7. Track the attacker's movement across the filesystem: for each file the attacker touched (created, modified, deleted, read), record the full path and timestamp. This file-access trail may reveal the attacker's objectives and the location of the flag.
8. Cross-reference the timeline with external data if the challenge provides it: if a companion PCAP or log file exists, align the network events with the host events. A file downloaded from a C2 server at a specific time should correlate with a file creation event on disk at the same time. Discrepancies between network and host timing indicate either clock skew or anti-forensic manipulation.

## Decision points

- **Stop on hash mismatch**: if the computed SHA-256 does not match the hash provided by the challenge platform, stop and obtain a verified copy. Investigation of a corrupted or modified image wastes time on false artifacts.
- **Escalate on encrypted volume with unknown passphrase**: if the image contains an encrypted volume and no passphrase hint, memory dump, or key file is available, the challenge intent may be cryptographic rather than forensic — pivot approach to dictionary attack against the LUKS/BitLocker header.
- **Escalate on multi-layered obfuscation**: if the flag is not in plaintext after carving, deleted recovery, and timeline analysis, the challenge likely involves steganography, encoding (base64/hex), or archive passwords — hand off to steganography or cryptography skills.
- **Downgrade on sparse image**: if the disk image is mostly zeroes (unallocated space) and the filesystem metadata is intact, the flag is likely in a regular file, not carved from slack space. Prioritize file listing and known-artifact search over carving.
- **Escalate on time-sensitive artifacts**: if the challenge provides log entries or timestamps pointing to a specific incident time, prioritize timeline assembly and window-based triage over exhaustive carving.
- **Escalate on anti-forensic indicators**: if timestomping is detected (mismatched $SI vs $FN timestamps in NTFS, or MAC times that are all zero or all identical), the challenge may involve deliberate evidence manipulation. The flag may be hidden in the manipulated metadata itself — compare the altered timestamps to the USN journal or log entries to identify the true timeline.
- **Downgrade on single-partition VMDK/VHD**: if the image is a virtual disk containing a single filesystem with no deleted files of interest, the challenge is straightforward file-system forensics. Complete Phase 1–3 (hash, partition, file listing) and proceed directly to string search, bypassing carving and deleted recovery.
- **Escalate on multiple operating system artifacts**: if the image contains both Windows and Linux artifacts (e.g., a dual-boot disk or a disk image used with WSL), the challenge may require correlating evidence across both OS environments. Investigate each OS independently, then cross-reference the timelines.

## Prohibited behavior

- Modifying the original disk image, memory dump, or any source artifact in any way. All work must be against copies or via read-only access methods.
- Mounting a disk image read-write. Even accidental write can update filesystem journals and superblock mount counters, altering the evidence.
- Running automated exploitation tools or network scanners against the challenge infrastructure unless explicitly authorized in the challenge rules.
- Attacking other teams, tampering with the competition platform, or accessing challenge files outside the authorized channel.
- Storing raw flags, challenge answers, team tokens, CTF platform credentials, or scoreboard data in evidence or reports. Redact them before recording.
- Using recovered credentials from a CTF disk image to access real-world services, even if the credentials appear valid.
- Publishing challenge solutions, flags, or detailed writeups before the competition author's embargo lifts.
- Running any tool with `sudo` or elevated privileges from this skill.
- Applying filesystem repair tools (`fsck`, `chkdsk`, `xfs_repair`) to the original image — these tools modify the filesystem to achieve consistency, which destroys forensic evidence. If repair is necessary, operate on a copy and document that the copy was repaired.
- Using `mount` without explicit read-only flag (`-o ro,noexec,nodev`). Even a read-write mount that the analyst believes is read-only can result in journal replays, atime updates, or orphan inode cleanup.
- Executing recovered binaries or scripts from the disk image on the analyst's workstation. A CTF challenge may intentionally include harmless binaries, but the principle of never executing evidence applies regardless of context.

## Stop conditions

- The computed image hash does not match the challenge-provided hash and a verified copy cannot be obtained.
- The disk image contains content that matches production system indicators (hostnames, IP ranges, user data) rather than synthetic challenge data — this may indicate a mislabeled image. Stop and verify provenance.
- A tool encounters an encrypted volume that cannot be decrypted with provided material and no further key recovery path exists.
- String search across all recovered artifacts finds no flag-format match after completing Phases 1 through 10 exhaustively.
- Any step requires network contact beyond the competition platform or lab environment scope.
- Tool execution triggers an antivirus alert, filesystem guard, or endpoint detection response on the analyst's workstation.
- Memory dump analysis identifies a process or artifact that appears to be from a real production system (real user accounts, real email addresses, real API keys). Stop and verify the dump provenance before continuing.
- A carved file contains credentials or tokens that grant access to a live service outside the CTF platform. Do not test the credentials. Stop, redact, and notify the challenge author through the appropriate channel.

## Evidence

Record evidence incrementally after each phase. Evidence entries follow this structure:

```text
Artifact: <sha256> | <image filename> | <competition/challenge name> | <date analyzed>
Phase: <phase number and name — e.g., Phase 3 — timeline extraction>
Tool: <catalog tool name> | <command summary without raw shell invocation>
Input: <partition offset | inode | file path | memory region>
Output summary: <what the tool returned — not the full output, a structured summary>
Flag found: <no | yes — redacted, format only noted e.g., "flag{...} pattern matched">
Evidence file reference: <path to redacted output in evidence store>
Confidence: <confirmed | likely | needs-review>

Timeline artifact (when applicable):
<timestamp> | <event source — e.g., MFT $SI, USN, Prefetch, Event Log> | <event description>
```

| Evidence gaps | <count> unrecoverable artifacts — <reason: filesystem damage | overwritten | encryption | beyond-tool-capability> |

After each phase, call `pentest_agent_append_evidence` with the phase entry. When a flag is found, record a single finding entry with the phase, technique, and confidence.

Never store in evidence: raw flag values, challenge answer strings, team tokens or CTF platform session cookies, recovered passwords or private keys, unredacted file content containing PII (rare in CTF but possible in lab exercises with synthetic identities), full tool output dumps that may contain secrets from parallel investigations, or recovered encryption keys that could unlock volumes outside the authorized challenge scope.

## Report handoff

When the investigation is complete (flag found or exhaustive search exhausted):

1. `pentest_agent_record_finding` with: challenge name, forensic technique that produced the flag (or all techniques attempted if no flag found), phase-by-phase summary of recovered artifacts, and the redacted flag format confirmation.
2. Include the timeline summary if it was critical to the recovery: incident window, key events, and any anti-forensic indicators identified. Provide the timeline as a chronological table with event descriptions, sources, and timestamps (UTC).
3. For reporting purposes: map the forensic technique to the CTF challenge category. If the flag was recovered via deleted file recovery, the category is "forensics — filesystem". If via memory analysis, "forensics — memory". If via encrypted volume passphrase cracking, "forensics — crypto". If via RAID reconstruction, "forensics — storage". If via Windows artifact correlation, "forensics — Windows".
4. Recommend: if evidence gaps remain (the flag was found but other artifacts were unrecoverable), note which filesystem regions were damaged and which tools reached their recovery limit.
5. Do not include the flag in the handoff report. Confirm the flag was found and note the phase, tool, and technique, but the flag value remains in the evidence store with redaction applied.
6. For challenges where the flag was not found: document the exhaustive search path — every phase executed, every tool used, every filesystem region scanned, and every carving profile applied. This documentation prevents duplicate effort if the challenge is revisited and provides the starting point for a more specialized approach (e.g., handing off to a steganography or cryptography skill).
7. For multi-artifact challenges where the same investigation produced multiple flags: record each flag as a separate finding, mapped to the specific forensic phase and technique that recovered it. This preserves the one-to-one relationship between technique and evidence.
5. Do not include the flag in the handoff report. Confirm the flag was found and note the phase, but the flag itself stays in the evidence store with redaction applied.
