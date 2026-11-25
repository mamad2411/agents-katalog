---
name: incident-response-fileanalyser
description: "Static malware reverse-engineering and threat-intelligence triage for unknown files, Windows EXE/PE binaries, scripts, archives, ISOs, JavaScript, PowerShell, documents, and unpacked payloads. Use when a user provides a sample path, hash, filename, or file and asks whether it is malicious, benign, suspicious, contains IoCs, or should be reverse engineered with Ghidra, strings, capa, YARA, public TI, and structured phase artifacts."
compatibility: "Shell-capable coding agents such as Codex CLI, Gemini/Antigravity, Claude Code, or similar. Requires Bash; prefers file, sha256sum, strings, objdump, readelf, exiftool, unzip/7z, Ghidra analyzeHeadless, jq, curl. Headless only; never use Wine."
---

# Malware Static Reverse Triage

## Mission
Perform defensive malware triage and reverse-engineering of a user-provided file, archive, script, ISO, hash, or filename. The goal is to answer quickly and defensibly whether the artifact is malicious, suspicious, likely benign, legitimate vendor software, or inconclusive, while preserving evidence and keeping large reverse-engineering outputs out of the active LLM context.
This skill is optimized for incident responders, incident triage analysts, security researchers, and malware reverse-engineering workflows. It favors static analysis, controlled unpacking, Ghidra headless decompilation, local signatures/capability extraction, local enrichment scripts, and public threat-intelligence correlation.

## Use when
- The user gives a file path, uploaded sample, archive, ISO, script, hash, filename, or extracted payload and asks for malware triage, reverse engineering, IoCs, suspicious behavior, or a benign/malicious verdict.
- The artifact may be a Windows PE/EXE/DLL/SYS, .NET assembly, PowerShell, JavaScript, HTA/VBS, JAR, archive, ISO, Office/PDF document, or mixed dropper bundle.
- The user wants Ghidra headless analysis, imports, strings, call graph, decompiled behavior, local signature matching, public hash reputation, or APT/malware-family correlation.
- If user choose this skill manually always include Ghidra headless analyses
## Do not use when
- The user is asking to build, improve, weaponize, persist, evade detection, or deploy malware.
- The task requires live detonation, lateral movement, credential theft, exploit execution, or malware operation outside an explicitly authorized lab.
- The user only needs a normal software code review with source code and no malware/IoC question.

## Hard rules
- Treat every sample and extracted child file as hostile. Never execute it.
- Never use Wine, `wine`, `wine64`, Windows GUI tools through Wine, or Windows-only tools that require a GUI.
- Run all tools headless from Bash. Do not invoke `ghidraRun`, `xdg-open`, GUI launchers, browsers to open local files, or anything that spawns a separate analysis window.
- Prefer hash and indicator lookups. Do not upload the full sample or decompiled proprietary/client code to public services unless the user explicitly authorizes sample upload.
- Preserve raw evidence before transforming or extracting. Do not overwrite the original sample.
- Keep API keys secret. Read them from environment variables or key files, but never print them, store them in reports, or include them in command transcripts.
- A clean public reputation result is not proof of benignness. A single noisy detection is not proof of malware. Verdicts must be tied to evidence.
- If a tool is missing, times out, crashes, or does not support the file type, record the gap and continue with the next phase.
- If possible each run with this skill should include all phases. Especially if posible always try to reverse it vith ghidra.
## Context-control model
Reverse engineering can generate very large files. Use phase artifacts as the memory boundary.
At the end of every phase, write both a compact Markdown summary and a machine-readable JSON summary. In the next phase, load only:
1. `00_manifest.json`
2. the previous phase `phase_summary.json`
3. small high-signal slices selected with `jq`, `rg`, `grep`, `head`, or a purpose-built parser
Do not paste or read entire decompiled C files, raw strings dumps, archive listings, sandbox reports, or Ghidra logs into the conversation unless the user specifically asks for that file. Store them on disk and reference paths.
Recommended case layout:
```text
malware_triage/<case_id>/
  00_manifest.json
  00_tool_status.json
  01_inventory/
  02_unpacking/
  03_static_features/
  04_reverse_ghidra/
  05_local_interpretation/
  06_local_enrichment/
  07_public_ti/
  08_correlation/
  final_report.md
  final_verdict.json
```
Use this minimal phase summary schema:
```json
{
  "phase": "01_inventory",
  "status": "complete|partial|failed|skipped",
  "utc_completed": "YYYY-MM-DDTHH:MM:SSZ",
  "inputs": [],
  "artifacts": [],
  "tool_runs": [
    {
      "tool": "strings",
      "command_redacted": "strings -a -n 5 <sample>",
      "exit_code": 0,
      "stdout_artifact": "path",
      "stderr_artifact": "path"
    }
  ],
  "facts": [],
  "indicators": [],
  "suspicious_signals": [],
  "benign_signals": [],
  "gaps": [],
  "next_phase_inputs": {}
}
```

## Sub-agent model
If the runtime supports sub-agents, split work after the manifest exists:
- `collector`: owns file inventory, hashing, early tools, unpacking, and IoC extraction.
- `ghidra-worker`: owns headless Ghidra analysis and reverse-engineering artifacts for native binaries.
- `script-reviewer`: owns PowerShell, JavaScript, VBS/HTA, batch, Python, JAR, .NET, Office macro, and document-script interpretation without execution.
- `ti-researcher`: owns public web, Google/DuckDuckGo/Playwright, VirusTotal, MalwareBazaar, ThreatFox, URLhaus, AbuseIPDB, ANY.RUN public/report lookup, and other TI sources.
- `verdict-synthesizer`: runs last, reads only compact summaries plus selected evidence references, and produces the final answer.
Do not let two workers write into the same directory. Each worker must finish with a `phase_summary.json` and `phase_summary.md`.

## Phase 0: Intake, safety, and workspace
Normalize the input into one of these modes:
- `file_mode`: a local file path or uploaded file is available.
- `hash_mode`: only MD5/SHA1/SHA256 is available.
- `metadata_mode`: only a filename, URL, or weak clue is available.
If the artifact is only a hash, skip local static analysis and run public TI phases with clear limitations. If a file is available, create a case directory and compute hashes before all other work.
Use deterministic shell behavior and prevent accidental GUI launchers:
```bash
set -euo pipefail
export LC_ALL=C
unset DISPLAY WAYLAND_DISPLAY
umask 077
```
Create the manifest with at least:
- original path and basename
- case ID
- UTC start time
- file size
- SHA256, SHA1, MD5
- MIME/type from `file`
- analyst/user context from the prompt
- configured limits: max recursion depth, max files, max extracted bytes, per-tool timeout
Recommended defaults:
```text
MAX_RECURSION_DEPTH=3
MAX_EXTRACTED_FILES=5000
MAX_TOTAL_EXTRACTED_BYTES=2147483648
TOOL_TIMEOUT_SECONDS=120
GHIDRA_TIMEOUT_SECONDS=900
```

## Phase 1: Early inventory and required headless tools
Run these tools early for every available file. Capture stdout, stderr, exit code, command, timestamp, and artifact path. Some tools will fail on unsupported formats; preserve the failure because it is useful type evidence.
Required early tools:
```bash
file <sample>
exiftool -json -ee <sample>
strings -a -n 5 <sample>
strings -a -el -n 5 <sample>
objdump -x <sample>
readelf -aW <sample>
```
Use a wrapper so unsupported file types do not stop the workflow:
```bash
run_capture() {
  name="$1"; shift
  mkdir -p "$PHASE_DIR"
  set +e
  timeout "${TOOL_TIMEOUT_SECONDS:-120}" "$@" \
    >"$PHASE_DIR/${name}.stdout" \
    2>"$PHASE_DIR/${name}.stderr"
  rc=$?
  set -e
  printf '%s\n' "$rc" >"$PHASE_DIR/${name}.exit"
}
run_capture file file "$SAMPLE"
run_capture exiftool_json exiftool -json -ee "$SAMPLE"
run_capture strings_ascii strings -a -n 5 "$SAMPLE"
run_capture strings_utf16le strings -a -el -n 5 "$SAMPLE"
run_capture objdump_x objdump -x "$SAMPLE"
run_capture readelf_all readelf -aW "$SAMPLE"
```
Then classify the artifact type. Prefer exact type signals over extensions:
- Windows PE/COFF: `MZ`, PE headers, import table, sections, version info, Authenticode data.
- .NET: CLR header, `mscoree.dll`, managed metadata, C#/.NET strings.
- ELF: ELF header, program headers, dynamic imports.
- Script: PowerShell, JS/JScript, VBS, HTA, BAT/CMD, Python, shell.
- Archive/container: ZIP, 7z, RAR, CAB, ISO, MSI, JAR/APK, OneNote, Office, PDF.
- Document macro/script: OLE, OOXML, PDF JavaScript, embedded files.
Write `01_inventory/phase_summary.json` with candidate file type, hashes, tool status, high-signal metadata, and next targets.

## Phase 2: Safe unpacking and recursive target discovery
If the file is an archive, ISO, installer, document container, packed bundle, or JAR/APK, list contents before extraction and reject path traversal or absolute output paths. Try extraction only into the case directory. Do not execute installers or scripts.
Preferred headless commands when present:
```bash
7z l -slt <sample>
unzip -l <sample>
bsdtar -tf <sample>
isoinfo -l -i <sample>
```
Extraction examples:
```bash
7z x -y -bb0 -bd -o"$CASE_ROOT/02_unpacking/extracted" -- <sample>
unzip -qq <sample> -d "$CASE_ROOT/02_unpacking/extracted"
bsdtar -xf <sample> -C "$CASE_ROOT/02_unpacking/extracted"
```
For password-protected malware archives, try only a user-provided password first. If none is provided, common lab passwords such as `infected`, `malware`, and `virus` may be attempted and must be recorded as guesses. Do not brute-force archives.
Recursively inventory extracted files until max depth, max file count, or max extracted bytes is reached. Rank child files for analysis:
1. Executables, DLLs, SYS, MSI, CPL, SCR, OCX, COM
2. Scripts: PS1, JS, VBS, HTA, BAT/CMD, WSF, JSE/VBE
3. Documents with macros, embedded files, or JavaScript
4. JAR/APK/class/dex
5. Configs, resources, shortcut/LNK, URLs, autorun files
6. Everything else with suspicious strings or metadata
Write `02_unpacking/extracted_tree.json`, `02_unpacking/targets.json`, and a compact summary. Each target must have parent relationship, path, hashes, type, size, and reason selected.

## Phase 3: Static feature extraction and local signatures
For each ranked target, extract capabilities and indicators without running it.
Preferred optional tools, if available:
- `capa -j` and `capa -vv` for PE, ELF, .NET, shellcode, and supported sandbox reports.
- `floss --json` or `floss` for decoded, stack, tight, and static strings.
- `yara -r` against local curated rule directories.
- `ssdeep`, `tlsh`, `rabin2`, `rizin/radare2`, `pefile`, `lief`, `osslsigncode`, `pesign`, `sigtool`, `oleid`, `olevba`, `pdfid`, `pdf-parser.py`, `monodis`, `ilspycmd`, `javap`, `jadx`, `apktool` when present and relevant.
Do not fail the phase if these are missing. Record them in `00_tool_status.json`.
Useful PE/.NET fields:
- imports and delayed imports
- exports
- section names, permissions, entropy, raw/virtual size mismatch
- timestamp and linker version, with caveat that timestamps can be forged
- resources and version info
- Authenticode/signer verification if supported by installed tools
- PDB paths
- imphash, TLSH, ssdeep when available
- overlay size
- subsystem and entry point
- .NET metadata, assembly name, type/method names, resources
Extract IoCs into `03_static_features/iocs.json`:
- hashes: MD5, SHA1, SHA256, imphash, TLSH, ssdeep
- URLs, domains, public IPs, email addresses
- mutexes, named pipes, registry keys, service names, scheduled task names
- file paths, dropped filenames, user agents, campaign IDs, bot IDs
- crypto wallet addresses, Tor/onion addresses
- certificates, signer metadata, PDB paths
- suspicious command lines and LOLBins
Create capped high-signal views instead of loading raw dumps:
```bash
rg -n -i -C 2 'powershell|cmd\.exe|wscript|cscript|mshta|rundll32|regsvr32|schtasks|CurrentVersion\\Run|CreateProcess|ShellExecute|WinHttp|InternetOpen|URLDownloadToFile|VirtualAlloc|WriteProcessMemory|CreateRemoteThread|SetWindowsHookEx|IsDebuggerPresent|CheckRemoteDebuggerPresent|NtQueryInformationProcess|CryptUnprotectData|lsass|vssadmin|bcdedit|wevtutil|http://|https://|\.onion' \
  "$CASE_ROOT/03_static_features" \
  > "$CASE_ROOT/03_static_features/high_signal_grep.txt" || true
```
Write `03_static_features/phase_summary.json` with capability hits, suspicious strings, benign metadata, extracted IoCs, and analysis gaps.

## Phase 4: Headless Ghidra reverse engineering
Use Ghidra for native binaries and other supported compiled targets where decompilation or control-flow insight is needed. Skip Ghidra for clear-text scripts unless native embedded payloads are found.
Only use Ghidra headless. Prefer existing helper scripts from installed Ghidra skills when present, otherwise invoke `analyzeHeadless` directly. Never run `ghidraRun`.
Find a headless launcher:
```bash
GHIDRA_HEADLESS="${GHIDRA_HEADLESS:-}"
if [ -z "${GHIDRA_HEADLESS}" ]; then
  GHIDRA_HEADLESS="$(command -v analyzeHeadless || true)"
fi
if [ -z "${GHIDRA_HEADLESS}" ]; then
  GHIDRA_HEADLESS="$(find /usr/share /opt /root /tmp -path '*/support/analyzeHeadless' -type f 2>/dev/null | head -n 1 || true)"
fi
```
Prefer helper exports if a `ghidra-analyze.sh` wrapper is available:
```bash
GHIDRA_ANALYZE_SH="$(command -v ghidra-analyze.sh || true)"
if [ -z "$GHIDRA_ANALYZE_SH" ]; then
  GHIDRA_ANALYZE_SH="$(find /root /tmp . -path '*skills/ghidra/scripts/ghidra-analyze.sh' -type f 2>/dev/null | head -n 1 || true)"
fi
if [ -n "$GHIDRA_ANALYZE_SH" ]; then
  timeout "${GHIDRA_TIMEOUT_SECONDS:-900}" "$GHIDRA_ANALYZE_SH" \
    -v \
    --keep-project \
    --project-dir "$CASE_ROOT/04_reverse_ghidra/projects" \
    --project-name "ghidra_${CASE_ID}" \
    --timeout "${GHIDRA_TIMEOUT_SECONDS:-900}" \
    -s ExportAll.java \
    -s ExportCalls.java \
    -s ExportSymbols.java \
    -o "$CASE_ROOT/04_reverse_ghidra" \
    "$TARGET"
fi
```
If no helper wrapper exists, create a minimal temporary Ghidra post-script in the case directory that exports functions, imports, strings, symbols, selected decompiled functions, and a triage note. Keep generated scripts in `04_reverse_ghidra/scripts/` and logs in `04_reverse_ghidra/logs/`.
Direct headless pattern:
```bash
timeout "${GHIDRA_TIMEOUT_SECONDS:-900}" "$GHIDRA_HEADLESS" \
  "$CASE_ROOT/04_reverse_ghidra/projects" \
  "ghidra_${CASE_ID}" \
  -import "$TARGET" \
  -analysisTimeoutPerFile "${GHIDRA_TIMEOUT_SECONDS:-900}" \
  -scriptPath "$CASE_ROOT/04_reverse_ghidra/scripts" \
  -postScript MalwareTriage.java "$CASE_ROOT/04_reverse_ghidra" \
  -deleteProject \
  -log "$CASE_ROOT/04_reverse_ghidra/ghidra.log"
```
Minimum Ghidra artifacts:
- `functions.csv` with name, entry, size, namespace, external flag
- `imports.json` grouped by library and API
- `exports.json` when present
- `strings.json` with address, value, length, encoding
- `calls.json` or edge list when available
- `decompiled/` split by function, not one unbounded context blob
- `suspicious_slices.md` with decompiled snippets around high-signal imports/strings
- `ghidra_triage.md` with entry point, likely `main`, suspicious functions, benign functions, limitations
When function names are autogenerated, reason from imports, strings, call sites, constants, and data flow. Do not overstate certainty based on Ghidra names alone.

## Phase 5: Local interpretation without public TI
Interpret only local evidence first. This phase answers: “What does this file appear to do if we ignore reputation?”
For Windows PE/native binaries, look for:
- process execution: `CreateProcess`, `ShellExecute`, `WinExec`, `cmd.exe`, `powershell.exe`, `wscript`, `mshta`, `rundll32`, `regsvr32`
- persistence: Run keys, services, scheduled tasks, startup folder, WMI event subscription, DLL search order, Winlogon, IFEO
- network: WinHTTP/WinINet, sockets, DNS, hardcoded URLs/domains/IPs, custom user-agent, beacon loops
- injection/evasion: `VirtualAlloc`, `VirtualProtect`, RWX memory, `WriteProcessMemory`, `CreateRemoteThread`, APC, hollowing, anti-debug, anti-VM, sleep/jitter
- credential access: LSASS, browser profile paths, DPAPI, `CryptUnprotectData`, clipboard, keylogging, screenshot APIs
- collection/exfiltration: file enumeration, archive creation, staging directories, C2 upload, SMTP/FTP/HTTP POST
- destructive/ransom behavior: mass file traversal, crypto APIs with file rewrite, shadow copy deletion, `vssadmin`, `bcdedit`, `wevtutil`
- loader/dropper behavior: embedded PE/resources, shellcode, decompression, decryption loop, process migration
For scripts, do not execute. Beautify/deobfuscate safely and identify:
- encoded/base64/compressed layers
- download/execute chains
- LOLBins
- persistence changes
- Defender/AMSI bypasses
- credential or browser data access
- C2 endpoints
- payload drops and child artifacts
For likely benign software, collect positive evidence:
- valid vendor metadata and signed Authenticode chain when verifiable
- expected product/company/version strings
- imports matching stated functionality
- no process/network/persistence/credential/injection behavior beyond expected product purpose
- public hash reputation and prevalence, only after TI phase
- file path/package context consistent with vendor distribution
Write `05_local_interpretation/local_assessment.md` and `05_local_interpretation/phase_summary.json` with a provisional local-only verdict: `malicious`, `suspicious`, `likely_benign`, `inconclusive`, or `unsupported`.

## Phase 6: Run local enrichment script `/root/Tools/mal.sh`
After SHA256 is known, run the local enrichment helper exactly once if it exists and is executable:
```bash
if [ -x /root/Tools/mal.sh ] && [ -n "${SHA256:-}" ]; then
  mkdir -p "$CASE_ROOT/06_local_enrichment"
  set +e
  timeout 300 /root/Tools/mal.sh "$SHA256" \
    > "$CASE_ROOT/06_local_enrichment/malsh.raw.txt" \
    2> "$CASE_ROOT/06_local_enrichment/malsh.stderr"
  rc=$?
  set -e
  printf '%s\n' "$rc" > "$CASE_ROOT/06_local_enrichment/malsh.exit"
fi
```
If the script returns structured data, parse it into `06_local_enrichment/malsh.parsed.json`. If parsing is not reliable, keep the raw output and summarize only high-confidence fields. If the script is missing, not executable, times out, or fails because of missing API keys/network, record the gap and continue.

## Phase 7: VirusTotal file triage and analysis
Use VirusTotal as a file-intelligence phase after the local hashes are known. Prefer hash-based lookups first, then submission only when needed. This phase is intended for pipeline chaining, so keep output machine-readable and truncate aggressively with `jq`, `--include`, or `--exclude`.

Recommended command order:
1. Submit the sample for scanning with `vt scan file`.
2. Resolve the file record with `vt file <sha256>`.
3. Retrieve analysis IDs with `vt file analyses <sha256> -I`.
4. Fetch the finished analysis with `vt analysis <analysis_id>`.

Use JSON output by default:
```bash
vt --format json scan file "$SAMPLE"
vt --format json scan file "$SAMPLE" -w
vt --format json file "$SHA256"
vt --format json file analyses "$SHA256" -I
vt --format json analysis "$ANALYSIS_ID"
```

When you need bounded output for a pipeline, select only the fields you need:
```bash
vt --format json file "$SHA256" | jq '.[0] | {
  sha256,
  md5,
  type_description,
  signature_info,
  last_analysis_stats,
  tags
}'
vt --format json analysis "$ANALYSIS_ID" | jq '.[0] | {
  _id,
  status,
  date,
  stats
}'
```

Useful VT CLI behaviors for this skill:
- `vt scan file <path>` uploads one or more files and returns analysis IDs.
- `vt scan file <path> -w` waits for completion and prints the analysis result.
- `vt file <hash>` returns file metadata by SHA-256, SHA-1, or MD5.
- `vt file analyses <hash> -I` lists analysis IDs for the file.
- `vt analysis <analysis_id>` returns the completed analysis object.
- `--format json` is preferred for codex-cli pipeline chaining.
- `-i` and `-x` can trim large responses before they reach the next phase.
- `-P` is only for private-file visibility when the account supports it.

For this phase, record only the high-signal VT fields into `07_virustotal/phase_summary.json`:
```json
{
  "phase": "07_virustotal",
  "status": "complete|partial|failed|skipped",
  "utc_completed": "YYYY-MM-DDTHH:MM:SSZ",
  "inputs": [],
  "artifacts": [],
  "tool_runs": [],
  "facts": [],
  "indicators": [],
  "suspicious_signals": [],
  "benign_signals": [],
  "gaps": [],
  "next_phase_inputs": {}
}
```

If the file is already queued, already submitted, or already analyzed, reuse the existing analysis IDs instead of resubmitting. A clean VT result does not prove benignness, and an EICAR-style detection is only a validation signal.

## Phase 8: Public threat intelligence and web research
Run this phase after local IoCs are extracted. Use hashes and indicators first; use filenames and fuzzy behavior later because they are weaker.
Public research order:
1. Exact SHA256, SHA1, MD5.
2. Exact imphash/TLSH/ssdeep where available.
3. Exact URL, domain, public IP, mutex, registry path, PDB path, certificate subject, unique user-agent.
4. Filename plus hash, filename plus vendor, filename plus suspicious behavior.
5. Behavior cluster: API set, strings, mutexes, C2 path, campaign markers.
6. APT/family articles only when IoCs or TTPs strongly match.
Recommended web queries for Google, DuckDuckGo, or Playwright:
```text
"<sha256>"
"<md5>" malware
"<filename>" "<sha256>"
"<filename>" malware OR stealer OR loader OR backdoor OR ransomware
"<imphash>"
"<mutex_or_pdb_path>"
"<domain>" malware OR C2 OR IOC
"<url_path>" malware
"<unique_user_agent>" malware
"<api_or_string_cluster>" "<malware_family_candidate>"
site:any.run "<sha256>"
site:virustotal.com/gui/file "<sha256>"
site:bazaar.abuse.ch/sample "<sha256>"
site:malpedia.caad.fkie.fraunhofer.de "<family_candidate>"
```
Source quality ranking:
1. Exact hash report from a reputable TI platform.
2. Vendor writeups with exact IoCs or matching YARA/capa behavior.
3. MalwareBazaar/ThreatFox/URLhaus/AbuseIPDB records with timestamps and families.
4. Sandbox reports by exact hash.
5. Public YARA/Sigma/Suricata rules with matching unique strings.
6. Blog/forum/social posts, only as low-confidence leads unless corroborated.
Use APIs when keys are present. Check environment variables first, then `/root/Tools/apikeys.txt`, then `~/Tools/apikeys.txt`. Accept common key names such as `VT_API_KEY`, `VIRUSTOTAL_API_KEY`, `MALWAREBAZAAR_API_KEY`, `THREATFOX_API_KEY`, `URLHAUS_API_KEY`, `ABUSEIPDB_API_KEY`, `ANYRUN_API_KEY`. Do not display loaded values.
VirusTotal by hash only:
```bash
curl -sS --fail \
  --header "x-apikey: ${VT_API_KEY}" \
  "https://www.virustotal.com/api/v3/files/${HASH}" \
  > "$CASE_ROOT/07_public_ti/virustotal_${HASH}.json"
```
MalwareBazaar by hash:
```bash
curl -sS --fail \
  -H "Auth-Key: ${MALWAREBAZAAR_API_KEY:-}" \
  --data-urlencode "query=get_info" \
  --data-urlencode "hash=${HASH}" \
  "https://mb-api.abuse.ch/api/v1/" \
  > "$CASE_ROOT/07_public_ti/malwarebazaar_${HASH}.json"
```
ThreatFox by hash or IOC:
```bash
curl -sS --fail \
  -H "Auth-Key: ${THREATFOX_API_KEY}" \
  -H "Content-Type: application/json" \
  -d "{\"query\":\"search_hash\",\"hash\":\"${HASH}\"}" \
  "https://threatfox-api.abuse.ch/api/v1/" \
  > "$CASE_ROOT/07_public_ti/threatfox_hash_${HASH}.json"
```
AbuseIPDB for public IPs only:
```bash
curl -sS --fail -G \
  "https://api.abuseipdb.com/api/v2/check" \
  --data-urlencode "ipAddress=${IP}" \
  -d "maxAgeInDays=90" \
  -H "Key: ${ABUSEIPDB_API_KEY}" \
  -H "Accept: application/json" \
  > "$CASE_ROOT/07_public_ti/abuseipdb_${IP}.json"
```
URLhaus and ANY.RUN:
- For URLhaus, query public URL/domain/payload data when URLs or payload hashes are present and the account/API access supports it.
- For ANY.RUN, prefer public report lookup or TI lookup by hash/IOC. Do not submit or detonate the sample unless the user explicitly authorizes sandbox upload.
- If API syntax is not available in the local environment, use web/Playwright search against public pages and record the gap.
For every TI result, normalize into `07_public_ti/ti_normalized.json`:
```json
{
  "source": "virustotal|malwarebazaar|threatfox|urlhaus|abuseipdb|anyrun|web",
  "query_type": "sha256|md5|ip|domain|url|filename|imphash|tlsh|behavior",
  "query": "redacted-or-ioc",
  "match_strength": "exact|strong|weak|none",
  "malicious_score": null,
  "family": null,
  "first_seen": null,
  "last_seen": null,
  "facts": [],
  "source_url_or_artifact": "path-or-url",
  "retrieved_utc": "YYYY-MM-DDTHH:MM:SSZ"
}
```
Do not attribute to an APT group from generic behavior alone. Require exact IoCs, unique tooling, infrastructure overlap, YARA/config match, or a reputable report explicitly tying the sample/hash/campaign to that actor.

## Phase 9: Correlation and final verdict
The final synthesis must read only compact summaries plus selected evidence references. Resolve contradictions explicitly.
Verdict values:
- `MALICIOUS`: strong static evidence, confirmed public reputation, or exact family/sandbox match shows harmful capability/intent.
- `SUSPICIOUS`: meaningful malicious capability or anomaly exists, but intent or execution path is not fully proven.
- `LIKELY_BENIGN`: local behavior and metadata are consistent with legitimate function, no material malicious indicators, and reputation/signing/context support benignness.
- `BENIGN_WITH_LIMITATIONS`: strong benign signals exist, but analysis gaps remain, such as packed code, missing signature verification, or absent TI.
- `INCONCLUSIVE`: insufficient evidence, unsupported format, encrypted/packed sample without unpacking, or tool failures prevent a defensible verdict.
Confidence values:
- `High`: multiple independent high-quality signals agree, or exact hash/signature behavior is conclusive.
- `Medium`: local and TI evidence mostly agree but one important gap remains.
- `Low`: evidence is sparse, weak, filename-only, packed/obfuscated, or tool support is limited.
High-confidence malicious examples:
- Exact hash is known malware in multiple reputable sources and local static behavior matches the family.
- Decompiled code or script clearly downloads/executes payloads, persists, steals credentials, injects into processes, encrypts files for ransom, or contacts hardcoded C2.
- capa/YARA/FLOSS/Ghidra evidence shows coherent malicious capability and IoCs corroborate it.
High-confidence benign examples:
- Valid vendor signature and version metadata match the expected product.
- Public exact-hash reputation and prevalence support legitimacy.
- Imports, strings, and decompiled logic match the stated benign purpose and lack unrelated risky behavior.
- Any network/process/file behavior is expected and explained by the product function.
Common false-positive traps:
- Packer or high entropy alone is not malware.
- Compile timestamp alone is not reliable.
- One AV engine detection alone is weak.
- Filename-only search hits are weak.
- No VirusTotal hit or zero detections does not prove benign.
- Benign admin tools can legitimately use process, network, service, registry, or crypto APIs.
- Each phase before should have its own output, own verdict and own IOC´s. The final correlation needs to check all of them the get a detaild overall result.


## Final chat output
The user usually wants the agent answer, not all generated files. Keep the final response concise and decision-ready:
```markdown
## Verdict
<VERDICT> — <confidence>
Assessment: <one or two sentence analyst conclusion>
## Why
- <highest-signal malicious/suspicious evidence>
- <highest-signal benign evidence>
- <what was ruled out or not observed>
## Key IoCs
| Type | Value | Source | Confidence |
| --- | --- | --- | --- |
## Threat-intel correlation
- <exact hash matches, family/signature, first/last seen, source names>
- <web/API gaps if sources were unavailable>
## Reverse-engineering findings
- <entry point/main behavior, imports/capabilities, notable functions/scripts/resources>
## Limitations
- <packed/encrypted/unsupported/missing tools/no sample upload/no dynamic analysis>
## Artifacts
- Case directory: `<path>`
- Manifest: `<path>`
- Static features: `<path>`
- Ghidra output: `<path>`
- TI normalization: `<path>`
```
When the evidence is benign, still include limitations and the exact basis for legitimacy. When malicious, include containment-relevant IoCs and recommended next defensive steps, but do not provide instructions for operating or improving the malware.
Menten which Phase was successfull executed and which was skipped. 
