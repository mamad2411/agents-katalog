---
name: MotorBoy-ECU
description: Complete Honda motorcycle ECU reverse-engineering toolkit. Provides fingerprint extraction (size/alignment/hash), ECU-ID extraction, data-offset/marker detection, multi-algorithm checksum analysis (sum-mod-256/16/32, XOR, CRC-8/16/32), fuel/ignition/VE map detection with dimension scoring, XDF-style table parsing, and ECU database assembly (ecu-database.json) grouped by model/variant with standard ECU size clustering. Integrated from MotorBoy_TH original source scripts + optimized stdlib-only pipeline. Supports .bin and custom ASCII-hex .hex formats.
metadata:
  version: "2.3.0"
  language: en
  optimized: true
  stdlib-only: true
  perf-optimized: true
  source-integration: true
  ai-models: true
  author: MotorBoy_TH
  email: sirisakkhacha@gmail.com
  icon: "🏍️"
  tags:
    - ecu
    - honda
    - firmware
    - reverse-engineering
    - bin
    - hex
    - xdf
  github: "https://github.com/sirisakboy/sell/tree/main/skills/MotorBoy-ECU/"
  import-mode: read-only
  sync: auto-from-source
---
    - ecu
    - honda
    - firmware
    - reverse-engineering
    - bin
    - hex
    - xdf
---
# MotorBoy-ECU v2.3.0
Complete Honda motorcycle ECU reverse-engineering toolkit by MotorBoy_TH (sirisakkhacha@gmail.com). Merges the original MotorBoy ECU source scripts with the optimized stdlib-only analysis pipeline.
---
## 🚀 Quick Start (Copy-Paste)
```bash
REPO="/path/to/ecu/firmware/repo"
SCRIPTS="$(dirname "$0")/../scripts"   # or ~/.config/poolside/skills/MotorBoy-ECU/scripts
# 1. Fingerprints + correlation (parallel: -j 4 for 4-core speedup)
python3 $SCRIPTS/fingerprint.py "$REPO" -o fingerprints.json -j 4
python3 $SCRIPTS/fingerprint.py "$REPO" --db known.json --report matches.csv -j 4
# 2. ECU-ID / offset / checksum (compact = skip 9-algorithm matrix, ~10x faster)
python3 $SCRIPTS/ecu_analyzer.py "$REPO" --table --compact --progress
python3 $SCRIPTS/ecu_analyzer.py "$REPO" --checksum-offset 0x3fff8 --table -o analysis.json
# 3. Map detection (parallel: -j 4, compact output)
python3 $SCRIPTS/map_detector.py "$REPO" --table -j 4
# 4. AI analysis (anomaly detection + performance scoring)
python3 $SCRIPTS/ai/ecu_ai_analyzer.py "$REPO"
# Automatic fuel/ignition tuning
python3 $SCRIPTS/ai/autotune_engine.py "$REPO"
# 5. ECU communication via K-Line/FTDI (requires hardware)
python3 $SCRIPTS/eculib/__main__.py --list-devices
# 6. XDF map parsing (requires pandas + xlsxwriter)
python3 $SCRIPTS/xdf/xdf_merge.py input.xdf input.map firmware.bin
# 4. ECU database lookup + table parsing (uses original ecu_xdf_database.py engine)
python3 $SCRIPTS/ecu_database.py list
python3 $SCRIPTS/ecu_database.py find --part 38770-K1M-T01
python3 $SCRIPTS/ecu_database.py parse "$REPO/somefile.bin" --part 38770-K1M-T01 --table "Fuel MAP" --csv fuel.csv
# 5. Full database assembly (run per-subdir to avoid CPU overload)
python3 $SCRIPTS/build_ecu_db.py "$REPO" -o ecu-database.json --table
python3 $SCRIPTS/build_ecu_db.py "$REPO/edacg" -o "$REPO/edacg/ecu-database.json" --only ext:bin
# 6. Verify consistency (100% gate: 3 files × 3 methods × 3 rounds)
python3 $SCRIPTS/verify_consistency.py
```
---
## 📜 Script Overview
### Optimized Pipeline (Main `scripts/`)
| Script | Purpose | Key Output | Original Source |
|--------|---------|------------|-----------------|
| `fingerprint.py` | Size / alignment / hash identification (filename-independent) | `fingerprints.json`, `matches.csv` | Adapted from MotorBoy fingerprint tools |
| `ecu_analyzer.py` | ECU-ID extraction, data offset, 9-algorithm checksum matrix | `analysis.json` | Adapted from `advanced_checksum_ecu_skill.py` |
| `map_detector.py` | Fuel / ignition / VE map detection + dimension scoring + CSV export | `maps.json`, `*.csv` | Adapted from `ecu_map_detection.py` |
| `ecu_database.py` | CLI for static ECU lookup + table parsing (uses XDF engine) | ECU defs, parsed tables | Adapted from `ecu_xdf_database.py` |
| `build_ecu_db.py` | Full database assembly → `ecu-database.json` (size clustering + model/variant) | `ecu-database.json` | Original MotorBoy assembly script |
| `verify_consistency.py` | Cross-validate 3 methods × 3 files × 3 rounds (100% consistency gate) | Pass/Fail report | Original MotorBoy verification |
### Original Source Scripts (`scripts/source/`)
All 15 original MotorBoy ECU skill scripts are preserved in `scripts/source/` for full provenance and reference. The `ecu_xdf_database.py`, `ecu_map_detection.py`, and `advanced_checksum_ecu_skill.py` modules directly feed the optimized pipeline. The remaining skill scripts provide extended ECU operations (read/write/flash/backup/recovery), OBD2 diagnostics, graphing, and UI/code review capabilities.
#### Core Analysis Scripts (Integrated Into Pipeline)
| Original Script | Lines | Purpose | Integrated Into |
|----------------|-------|---------|-----------------|
| `ecu_xdf_database.py` | 499 | ECU database with embedded XDF definitions — `ECUXDFDatabase` class with `find_by_part_number()`, `find_by_model()`, `parse_table()`, `export_table_to_csv()` | `ecu_database.py` (parse/lookup functions) |
| `ecu_map_detection.py` | 395 | Map detection: `find_tables()`, `find_ignition_map()`, `find_ve_table()`, `detect_map_dimensions()`, `visualize_map()`, `export_map_to_csv()` | `map_detector.py` (scoring + dimension logic) |
| `advanced_checksum_ecu_skill.py` | 245 | Checksum verification: `verify_hex_checksum()`, `calculate_advanced_checksum()` (16-bit/32-bit), `fix_checksum()`, `batch_verify()` | `ecu_analyzer.py` (checksum matrix + offset mode) |
#### Extended ECU Operational Skills
| Skill Script | Lines | Category | Key Classes / Functions |
|-------------|-------|----------|-------------------------|
| `read_ecu_skill.py` | 110 | ECU I/O | `ReadECUSkill` — Read data from ECU via FTDI/K-Line |
| `write_ecu_skill.py` | 125 | ECU I/O | `WriteECUSkill` — Write data to ECU via FTDI/K-Line |
| `flash_ecu_skill.py` | 163 | ECU I/O | `FlashECUSkill` — Full ECU flash operation (read+write pipeline) |
| `backup_ecu_skill.py` | 194 | ECU I/O | `BackupECUSkill` — Backup ECU data with verification |
| `recovery_ecu_skill.py` | 217 | ECU I/O | `RecoveryECUSkill` — Recover ECU from abnormal/corrupt states |
| `verify_ecu_skill.py` | 146 | ECU I/O | `VerifyECUSkill` — Verify ECU data integrity post-operation |
| `diagnostic_ecu_skill.py` | 264 | Diagnostics | `DiagnosticECUSkill` — Diagnose ECU problems, DTC reading |
| `obd2_diagnostic_skill.py` | 620 | Diagnostics | `OBD2DiagnosticSkill` — OBD2 live data, DTC, ECU ID, data logging |
| `graph_ecu_skill.py` | 478 | Visualization | `GraphECUSkill` — Draw real-time graphs for ECU data streams |
| `design_ecu_skill.py` | 333 | UI/UX | `DesignECUSkill` — UI/UX design for ECU tools and interfaces |
| `code_review_ecu_skill.py` | 384 | Quality | `CodeReviewECUSkill` — Code review for ECU projects |
#### Package Manifest
| File | Lines | Purpose |
|------|-------|---------|
| `__init__.py` | 35 | ECU Skills Package — exports all 12 skill classes, `__version__ = '5.0.0'` |
### AI Model Scripts (`scripts/ai/`)
Two AI-driven modules are integrated from `/run/media/boy/BACKUP-FILE/ECU-M/ai-models/`:
| AI Script | Lines | Purpose | Key Classes / Functions |
|----------|-------|---------|------------------------|
| `ecu_ai_analyzer.py` | 640 | AI anomaly detection, performance analysis, fuel optimization | `SensorReading`, `AnalysisResult`, `AFRTable`, `DataLogger`, `ECUAIAnalyzer` |
| `autotune_engine.py` | 554 | Automatic tuning: AFR learning, fuel table optimization, ignition timing | `FuelCell`, `IgnitionCell`, `TuningSession`, `FuelTable`, `IgnitionTable`, `AutotuneController` |
| `__init__.py` | — | Package init for `ai_models` (v1.0.1) | Exports 9 classes from both modules |
**AI Model Features:**
- Anomaly Detection: sensor readings evaluated against learned patterns (health/efficiency scoring)
- Autotune Engine: bilinear interpolation for AFR targets, fuel/ignition table learning, knock detection
- Data Logging: session-based JSON logging with configurable log directory
### ECU Communication Library (`scripts/eculib/`)
ECU K-Line/FTDI communication library integrated from Telegram (`Telegram eculib/`):
| eculib Script | Lines | Purpose | Key Classes / Functions |
|--------------|-------|---------|------------------------|
| `base.py` | 47 | K-Line adapter via FTDI/pylibftdi | `KlineAdapter`, `ECU` |
| `honda.py` | 270 | Honda ECU protocol implementation | `HondaECU`, `ECUSTATE`, `DTC` table, `FuelTable`, `IgnitionTable`, `checksum8bitHonda()`, `format_message()` |
| `__init__.py` | 3 | Package init — exports `KlineAdapter` + all Honda classes | — |
| `__main__.py` | 53 | CLI entry point for FTDI device testing | `GetFtdiDevices()`, `Main()` |
**ECU Communication Features:**
- K-Line serial protocol via FTDI devices (10400 baud)
- Honda ECU state machine: UNDEFINED, OFF, READ, READING, OK, RECOVER_OLD, RECOVER_NEW, ERROR
- DTC (Diagnostic Trouble Code) reading with 33 fault codes
- Fuel/ignition table read/write/erase/probe operations
- Checksum validation (8-bit Honda protocol)
**Bug Fixes Applied to eculib:**
- `get_faults()`: Added `None` check on `send_command()` return — prevents `TypeError` on timeout
- `send_command()`: Mutable default arg `data=[]` → `data=None` (Python antipattern)
- `format_message()`: `assert` → `raise ValueError` (asserts stripped under `-O` flag)
### XDF Map Parser (`scripts/xdf/`)
XDF (TunerPro) map extraction, inspection, and merge tool integrated from `xdf-parser repo`:
| XDF Script | Lines | Purpose | Key Classes / Functions |
|-----------|-------|---------|------------------------|
| `xdf_merge.py` | 1,031 | Parse XDF + BIN, extract maps, export to Excel/JSON, merge XDF | `XDFParser`, `eval_formula()`, `find_size()`, `find_val()`, `merge_data()`, `merge_map_into_xdf()`, `find_result_table()` |
**XDF Parser Features:**
- Parse TunerPro `.xdf` definition files (XML-based)
- Extract map tables from `.bin` firmware images using XDF metadata
- Export extracted tables to Excel (`.xlsx`) and JSON
- Detect missing maps and auto-add them to XDF
- Generate merged `.xdf` ready for TunerPro
- 35 functions covering formula evaluation, checksum validation, table merging
**Bug Fixes Applied to xdf_merge.py:**
- `find_result_table()`: `==` → `=` assignment (result was never stored, always `None`)
- `find_size()`: `Rowcount * Rowcount` → `Rowcount * Colcount` (wrong dimension multiplication)
- `eval_formula()`: Restricted `__builtins__` to safe functions only (`abs`, `round`, `min`, `max`)
### File Input Support
- **Directory** (recursive scan) — all scripts accept directories (except `ecu_database.py`)
- **Individual files** — `ecu_analyzer.py` and `map_detector.py` accept multiple files
- **`.hex` auto-decode** — `bytes.fromhex()` applied before analysis
- **`.bin`** — analyzed as raw binary
---
## 🔧 What Each Script Extracts
### fingerprint.py
| Field | Description |
|-------|-------------|
| `size` | Raw on-disk byte count |
| `binary_size` | Decoded binary length (`.hex` → divide by 2) |
| `alignment` | Largest power-of-two divisor of `binary_size` |
| `md5` / `sha256` | Full-content digests |
| `first_16` | Hex of first 16 decoded bytes (alignment-sensitive prefix) |
### ecu_analyzer.py
| Field | Description | Source |
|-------|-------------|--------|
| `ecu_ids` | ASCII ID strings (part numbers) + repeating 8-byte header blocks | `advanced_checksum_ecu_skill.py` |
| `offset.data_offset` | Where real map data begins (fill-byte run / repeating header) | MotorBoy analysis |
| `offset.markers` | Offsets of known marker strings (`PARFW`, `xAzF`, `PN`, …) | `advanced_checksum_ecu_skill.py` |
| `checksum` | 9 algorithms at file tail + named offset: sum-mod-256/16/32, XOR-8, CRC-8/16/32 | `advanced_checksum_ecu_skill.py` |
### map_detector.py
| Field | Description | Source |
|-------|-------------|--------|
| `fuel_maps` | 256-byte candidate fuel maps (values 0x60–0xFF, smooth transitions) | `ecu_map_detection.py` `find_tables()` |
| `ignition_maps` | Candidate ignition maps (values 0–60° BTDC, very smooth) | `ecu_map_detection.py` `find_ignition_map()` |
| `ve_tables` | VE tables (full 0–255 range, "hill" shape) | `ecu_map_detection.py` `find_ve_table()` |
| `best_candidate` | Highest-scoring map + detected dimensions (8×8 … 16×16) | `ecu_map_detection.py` `detect_map_dimensions()` |
### ecu_database.py
| Feature | Source Function | Description |
|---------|----------------|-------------|
| `list` | `ECUXDFDatabase.get_all_ecus()` | Show all ECU definitions |
| `find --part` | `ECUXDFDatabase.find_by_part_number()` | Lookup by exact part number |
| `find --model` | `ECUXDFDatabase.find_by_model()` | Lookup by model + optional year |
| `find --size` | MotorBoy size matcher | Auto-detect by flash size |
| `parse --part --table` | `ECUXDFDatabase.parse_table()` | Extract + scale table → CSV |
| `--export-csv` | `ECUXDFDatabase.export_table_to_csv()` | Export parsed table data to CSV |
### build_ecu_db.py
| Section | Description |
|---------|-------------|
| `standard_ecu_sizes` | Size buckets above threshold (`--min-bucket`), tagged `is_standard` |
| `variant_groups` | Per-model-family file counts + size distribution |
| `ecu_model` / `ecu_part_number` | Auto-detected from size matching + ECU-ID string |
| `files[]` | Combined fingerprint + ecu_id + offset + checksum + ECU model |
---
## ⚡ Key Conventions (MotorBoy Repository)
1. **`.hex` files are custom ASCII-hex dumps**, NOT Intel HEX records (no `:` markers, no newlines). Decode with `bytes.fromhex()`.
2. **Never trust filenames** — fingerprint by size + alignment + hash.
3. Some `.hex` files are **0 bytes** (empty) — recorded but flagged.
4. **ECU-ID blocks**: 256-byte `scums.bin`/`scumy.bin` files use a repeating 8-byte header followed by fill `0xFF` and an embedded ASCII part number.
5. **Map markers**: `PARFW` @ offset 6621 and `xAzF` @ offset 7675 are consistent anchors in the 393 KB edacg firmware family.
6. **Checksums**: Most firmware tails are fill bytes (`0xFF`/`0xAA`) — no standard algorithm validates at file tail. Use `--checksum-offset` with the ECU database's `checksum_offset` (e.g. `0x3FFF8` for PCX 150).
7. **Static ECU DB**: `references/ecu-definitions.json` contains 3 verified Honda ECU definitions (CBR150R, Wave 110i, PCX 150) with embedded XDF-style table definitions. Extend by adding entries.
---
## 🌲 Workflow Decision Tree
```
Unknown .hex file
  ↓
Extract fingerprint (size / alignment / md5 / first_16)       ← fingerprint.py
  ↓
Size matches a known entry? ── No ─→ Add to DB (new map candidate)
  ↓ Yes
MD5 matches? ── No ─→ Size collision: same size, different content
                    → Compare first_16, flag divergence
  ↓ Yes
→ Correlated. Cross-check live ECU via K-Line Table 17.
  ↓
Find maps (fuel / ignition / VE) + dimensions                ← map_detector.py
  ↓
Parse table → CSV using XDF definitions                     ← ecu_database.py / ecu_xdf_database.py
  ↓
Verify consistency across all methods                       ← verify_consistency.py
```
---
## 📚 When to Read References
| Reference File | When to Load |
|---------------|-------------|
| `references/hex-format.md` | Need exact byte-level structure of `.hex` vs `.bin`, 0-byte edge case, decoding recipes |
| `references/fingerprint-workflow.md` | Full P1→P5 reverse-engineering loop with diagnostic PDF correlation and K-Line Table 17 protocol mapping |
| `references/ecu-analysis.md` | ECU-ID string patterns, header-block signatures, marker offsets, checksum algorithm matrix, standard ECU size definitions |
| `references/ecu-definitions.json` | Static ECU database lookup (model, part number, MCU, flash size, table definitions, axis values) |
| `references/verification_log.json` | Review 100% consistency test results (3 files × 3 methods × 3 rounds) |
| `scripts/source/ecu_xdf_database.py` | Deep-dive into `ECUXDFDatabase` class methods, custom table parsing |
| `scripts/source/ecu_map_detection.py` | Understand map detection scoring algorithm (fuel/ignition/VE heuristics) |
| `scripts/source/advanced_checksum_ecu_skill.py` | Checksum verification internals, batch processing API |
---
## ✅ Consistency Verification
`verify_consistency.py` cross-checks offset / checksum / ECU-ID extraction across 3 independent methods on 3 representative files, 3 rounds:
| File | Size | Method A (fp+analyzer) | Method B (map_detector) | Method C (build_ecu_db) | Match? |
|------|------|------------------------|-------------------------|------------------------|--------|
| `scums.bin` | 256 B | ECU-ID: `3718023K0071` | size+md5 only | ECU-ID: `3718023K0071` | ✅ 100% |
| `air.bin` | 4 KB | md5=`79dfb6aedb90…` | md5=`79dfb6aedb90…` | md5=`79dfb6aedb90…` | ✅ 100% |
| `a0303.bin` | 393 KB | ECU-ID: `1-PARFW`,`1-xAzF` | size+md5 only | ECU-ID: `1-PARFW`,`1-xAzF` | ✅ 100% |
**Fields verified**: `binary_size`, `md5`, `first_16`, `ecu_ids`, `data_offset` — all fields present in both methods must agree exactly.
---
## 🚀 Performance Optimizations (MotorBoy ECU v2.0.0)
| Optimization | Impact | How |
|-------------|--------|-----|
| **`--compact` flag** on `ecu_analyzer.py` | ~10x faster | Skips the 9-algorithm checksum matrix (proven not to match any file tail) |
| **`--only ext:` filter** on `build_ecu_db.py` / `fingerprint.py` | Reduces scan scope | Run only on relevant extensions per subdirectory |
| **Per-subdir database build** | Prevents CPU overload | Run `build_ecu_db.py` one subdirectory at a time |
| **`skip_checksum=True`** internally in `build_ecu_db.py` | Eliminates redundant computation | Applied when no explicit checksum offset provided |
| **`analyze_data()` refactor** | Runtime reduced from >4 min to ~18s | Reuses pre-loaded data in memory |
| **Standard ECU size threshold** (`--min-bucket 5`) | Filters noise | Only frequent sizes tagged `is_standard` |
| **`-j` parallel processing** on `fingerprint.py` + `map_detector.py` | ~Nx faster (N = cores) | `ThreadPoolExecutor` for parallel file processing (max 8 workers) |
| **Single-pass dual hashing** in `fingerprint.py` | ~2x faster per file | MD5 + SHA256 computed in one pass via chunked `hashlib` update |
| **Early-exit range checks** in `map_detector.py` | ~3x faster per file | Uses C-level `min()`/`max()` for pre-filter before computing diffs |
| **Source script integration** | Full provenance | All 15 original MotorBoy skill scripts preserved in `scripts/source/` |
| **AI model integration** | Extended capability | `ecu_ai_analyzer.py` + `autotune_engine.py` from `ai-models/` added to `scripts/ai/` |
| **ECU communication library** | Hardware I/O | `eculib` (base.py, honda.py) from Telegram added to `scripts/eculib/` with 3 bug fixes |
| **Bug fixes in eculib** | Stability | None-check, mutable default arg, assert→ValueError |
| **ECU communication library** | Hardware I/O | `eculib` (base.py, honda.py) from Telegram with 3 bug fixes |
| **XDF map parser** | Extended capability | `xdf_merge.py` from xdf-parser with 3 bug fixes |
| **Bug fixes in xdf_merge.py** | Stability | `==`→`=` assignment, `Rowcount*Rowcount`→`Rowcount*Colcount`, restricted eval builtins |
---
## 📁 Directory Structure
```
MotorBoy-ECU/
├── LICENSE.txt                          — MIT License (MotorBoy_TH)
├── SKILL.md                             — This file (v2.0.0)
├── scripts/
│   ├── fingerprint.py                   — Fingerprint extraction + correlation
│   ├── ecu_analyzer.py                  — ECU-ID, offset, checksum analysis
│   ├── map_detector.py                  — Fuel/ignition/VE map detection
│   ├── ecu_database.py                  — CLI for ECU lookup + table parsing
│   ├── build_ecu_db.py                  — Full database assembly
│   ├── verify_consistency.py            — Cross-method consistency gate
│   ├── ai/                              — AI model scripts (from ai-models/)
│   │   ├── ecu_ai_analyzer.py           — AI anomaly detection + analysis (640 lines)
│   │   ├── autotune_engine.py           — Automatic fuel/ignition tuning (554 lines)
│   │   └── __init__.py                  — Package init (v1.0.1)
│   ├── eculib/                          — ECU K-Line communication library
│   │   ├── base.py                      — K-Line FTDI adapter (47 lines)
│   │   ├── honda.py                     — Honda ECU protocol (270 lines)
│   │   ├── __init__.py                  — Package init (3 lines)
│   │   └── __main__.py                  — CLI for FTDI testing (53 lines)
│   ├── xdf/                             — XDF map parser (from xdf_parser-main)
│   │   └── xdf_merge.py                 — XDF+BIN map extraction + merge (1031 lines)
│   └── source/                          — Original MotorBoy skill scripts (15 files)
│       ├── __init__.py                  — Package manifest (v5.0.0, all 12 skill exports)
│       ├── ecu_xdf_database.py          — ECU database + XDF table engine (499 lines)
│       ├── ecu_map_detection.py         — Map detection heuristics (395 lines)
│       ├── advanced_checksum_ecu_skill.py — Checksum verification + batch (245 lines)
│       ├── read_ecu_skill.py            — Read ECU data via FTDI (110 lines)
│       ├── write_ecu_skill.py           — Write ECU data via FTDI (125 lines)
│       ├── flash_ecu_skill.py           — Full ECU flash operation (163 lines)
│       ├── backup_ecu_skill.py          — Backup ECU data (194 lines)
│       ├── recovery_ecu_skill.py        — Recover ECU from corrupt state (217 lines)
│       ├── verify_ecu_skill.py          — Verify ECU data integrity (146 lines)
│       ├── diagnostic_ecu_skill.py      — Diagnose ECU problems (264 lines)
│       ├── obd2_diagnostic_skill.py     — OBD2 live data + diagnostics (620 lines)
│       ├── graph_ecu_skill.py           — Real-time ECU data graphs (478 lines)
│       ├── design_ecu_skill.py          — UI/UX design for ECU tools (333 lines)
│       └── code_review_ecu_skill.py     — Code review for ECU projects (384 lines)
└── references/
    ├── ecu-analysis.md                  — ECU-ID patterns, marker offsets, checksum matrix
    ├── ecu-definitions.json             — Static ECU database (3 Honda models)
    ├── fingerprint-workflow.md          — Full P1→P5 reverse-engineering loop
    ├── hex-format.md                    — .hex vs .bin byte-level format spec
    └── verification_log.json            — 100% consistency test results
```
---
## 🏷️ Metadata
- **Author**: MotorBoy_TH
- **Email**: [sirisakkhacha@gmail.com](mailto:sirisakkhacha@gmail.com)
- **Origin**: /run/media/boy/BACKUP-FILE/ECU-M/
- **Language**: Python 3 (stdlib-only)
- **License**: MIT