---
name: recmd
version: 1.0.0
description: Parse and extract Windows Registry hive data using Eric Zimmerman's RECmd. Covers CLI flags, batch mode, search mode, output formats (CSV/JSON), key/value queries, deleted key recovery, and output field reference.
metadata:
  tool-name: RECmd
  tool-vendor: Eric Zimmerman
---

# RECmd Skill

RECmd is Eric Zimmerman's command-line tool for parsing Windows Registry hive files. It supports batch processing with predefined key definitions, ad-hoc key/value lookups, regex-based searching across keys, values, data, and slack space, and recovery of deleted entries. Forensic interpretation of Registry data (persistence mechanisms, user activity, configuration analysis, etc.) belongs in a separate analysis skill.

## Command Syntax

```
RECmd.exe -f <file> --bn <batchfile> --csv <dir> [other options]
RECmd.exe -d <directory> --bn <batchfile> --csv <dir> [other options]
RECmd.exe -f <file> --kn <keyname> [other options]
RECmd.exe -f <file> --sa <term> [other options]
```

Single-letter options use a single dash (`-`). Multi-character options use double dashes (`--`).

## Input (one required)

| Flag | Description |
|------|-------------|
| `-f` | Single hive file to process |
| `-d` | Directory to recursively search for hive files |

## Operation Modes

At least one of the following is required:

| Flag | Description |
|------|-------------|
| `--bn` | Path to batch file with key/value search definitions. Requires `--csv` or `--json`. |
| `--kn` | Display details for a specific key name including subkeys and values |
| `--vn` | Dump only a specific value name (use with `--kn`) |
| `--sa` | Search keys, values, data, and slack simultaneously |
| `--sk` | Search in key names |
| `--sv` | Search in value names |
| `--sd` | Search in value data |
| `--ss` | Search in value slack space |
| `--minSize` | Find values greater than or equal to specified byte size |
| `--base64` | Find Base64-encoded values greater than or equal to specified byte size |

## Output Formats

| Flag | Description |
|------|-------------|
| `--csv` | Directory to write CSV output (batch mode only) |
| `--csvf` | Custom filename for CSV output (overrides default) |
| `--json` | Directory to write JSON output |
| `--jsonf` | Compress names for profile-based hives |
| `--saveTo` | Save binary value data to specified file path |

It's recommended to specify at least one output format to write results to a file. CSV output is only available in batch mode (`--bn`). Search mode (`--sa`, `--sk`, `--sv`, `--sd`, `--ss`) outputs to console only.

## Options

| Flag | Description | Default |
|------|-------------|---------|
| `--details` | Show extended details in results | FALSE |
| `--nd` | Suppress data display with `--sd`/`--ss` | FALSE |
| `--regex` | Treat search strings as regular expressions | FALSE |
| `--literal` | Prevent ASCII/Unicode byte interpretation in `--sd`/`--ss` | FALSE |
| `--recover` | Recover deleted keys and values | FALSE |
| `--dt` | Custom date/time format string | `yyyy-MM-dd HH:mm:ss.fffffff` |
| `--nl` | Ignore transaction log files for dirty hives | FALSE |
| `--vss` | Process Volume Shadow Copies on the drive | FALSE |
| `--dedupe` | Deduplicate files via SHA-1 | FALSE |
| `--sync` | Download latest batch files from GitHub. Requires network access. | FALSE |
| `--debug` | Show debug information | FALSE |
| `--trace` | Show trace information | FALSE |

## Common Output Fields — Batch Mode (CSV)

CSV output is only produced in batch mode (`--bn`). Output columns depend on tool version.

| Column | Description |
|--------|-------------|
| **HivePath** | Path to the source hive file |
| **HiveType** | Type of hive (SYSTEM, SOFTWARE, NTUSER, etc.) |
| **Description** | Description from the batch file definition |
| **Category** | Category from the batch file definition |
| **Comment** | Comment from the batch file definition |
| **KeyPath** | Full registry key path |
| **ValueName** | Registry value name |
| **ValueType** | Registry value type (displays `(plugin)` when a plugin parsed the data) |
| **ValueData** | Parsed value data |
| **ValueData2** | Additional parsed data from plugins |
| **ValueData3** | Additional parsed data from plugins |
| **LastWriteTimestamp** | Key last write timestamp (UTC) |
| **Recursive** | Whether the batch entry was processed recursively |
| **Deleted** | Whether the entry is a deleted/recovered key or value |
| **PluginDetailFile** | Path to plugin-generated detail CSV (if applicable) |

## Workflow Examples

### Batch process a hive to CSV

```
RECmd.exe -f "C:\Cases\Evidence\NTUSER.DAT" --bn "C:\Tools\RECmd\BatchExamples\BatchExampleRun.reb" --csv "C:\Cases\Output"
```

### Batch process a directory of hives

```
RECmd.exe -d "C:\Cases\Evidence\Registry" --bn "C:\Tools\RECmd\BatchExamples\BatchExampleRun.reb" --csv "C:\Cases\Output"
```

### Look up a specific key

```
RECmd.exe -f "C:\Cases\Evidence\SOFTWARE" --kn "Microsoft\Windows\CurrentVersion\Run"
```

### Look up a specific value within a key

```
RECmd.exe -f "C:\Cases\Evidence\NTUSER.DAT" --kn "Software\Microsoft\Windows\CurrentVersion\Explorer\RunMRU" --vn "MRUList"
```

### Search all fields for a term

```
RECmd.exe -f "C:\Cases\Evidence\NTUSER.DAT" --sa "powershell"
```

### Search with regex

```
RECmd.exe -f "C:\Cases\Evidence\SOFTWARE" --sd "https?://" --regex
```

### Recover deleted keys and values

```
RECmd.exe -f "C:\Cases\Evidence\NTUSER.DAT" --bn "C:\Tools\RECmd\BatchExamples\BatchExampleRun.reb" --csv "C:\Cases\Output" --recover
```

### Parse dirty hive without transaction logs

```
RECmd.exe -f "C:\Cases\Evidence\SYSTEM" --bn "C:\Tools\RECmd\BatchExamples\BatchExampleRun.reb" --csv "C:\Cases\Output" --nl
```
