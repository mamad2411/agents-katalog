---
name: terminal-print
description: Print iTerm2 terminal output to network printer. Also documents AirPrint blank-page workaround for HP LaserJet Pro MFP 3101/3108 family. TRIGGERS - print terminal, terminal PDF, print session output, AirPrint blank page, printer prints blank, lpr no output, HP LaserJet driverless blank, IPP-Everywhere blank page.
allowed-tools: Bash, Read
---

# Terminal Print

Print terminal output from iTerm2 to your HP network printer with a single command.

> **Self-Evolving Skill**: This skill improves through use. If instructions are wrong, parameters drifted, or a workaround was needed — fix this file immediately, don't defer. Only update for real, reproducible issues.

## When to Use This Skill

Use this skill when:

- Printing terminal output to a network printer
- Creating PDF copies of command-line session output
- Archiving terminal logs in print-friendly format
- Sharing terminal output in meetings or documentation

## Quick Start

1. **Copy** terminal output in iTerm2 (Cmd+C)
2. **Invoke** this skill
3. **Review** PDF preview, press Enter to print

## How It Works

```
Clipboard → Strip ANSI → Markdown code block → pandoc/xelatex → PDF → Preview → Print
```

- **ANSI codes stripped**: Colors and escape sequences removed for clean B&W output
- **Monospace font**: DejaVu Sans Mono for proper character alignment
- **Landscape orientation**: Fits ~120 characters per line
- **US Letter paper**: Auto-detected from printer settings

## Execution

```bash
/usr/bin/env bash << 'PRINT_EOF'
SKILL_DIR="$(cc-plugin-root doc-tools)/skills/terminal-print"
bash "$SKILL_DIR/assets/print-terminal.sh"
PRINT_EOF
```

## Options

Run with arguments by modifying the execution block:

```bash
/usr/bin/env bash << 'PRINT_EOF'
SKILL_DIR="$(cc-plugin-root doc-tools)/skills/terminal-print"
bash "$SKILL_DIR/assets/print-terminal.sh" --no-preview
PRINT_EOF
```

| Flag                | Description                                                                                                                |
| ------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| `--file FILE`       | Read from file instead of clipboard                                                                                        |
| `--no-preview`      | Skip PDF preview, print directly                                                                                           |
| `--no-print`        | Generate PDF only, don't send to printer                                                                                   |
| `--printer NAME`    | Override target printer queue (default: system default)                                                                    |
| `--bypass-airprint` | Use socket-9100 + PostScript queue. Workaround for HP LaserJet Pro MFP 3101/3108/3201/3208/3301/3308 AirPrint blank pages. |
| `-h, --help`        | Show help message                                                                                                          |

## Examples

### Print from clipboard (default)

```bash
# Copy terminal output in iTerm2, then:
/usr/bin/env bash << 'EOF'
bash "$(cc-plugin-root doc-tools)/skills/terminal-print/assets/print-terminal.sh"
EOF
```

### Print from file

```bash
/usr/bin/env bash << 'EOF'
bash "$(cc-plugin-root doc-tools)/skills/terminal-print/assets/print-terminal.sh" --file ~/session.log
EOF
```

### Generate PDF only (no print)

```bash
/usr/bin/env bash << 'EOF'
bash "$(cc-plugin-root doc-tools)/skills/terminal-print/assets/print-terminal.sh" --no-print
EOF
```

## Prerequisites

All dependencies are already available on macOS with MacTeX:

| Tool      | Purpose          | Status            |
| --------- | ---------------- | ----------------- |
| `pandoc`  | Markdown to PDF  | Required          |
| `xelatex` | PDF engine       | Required (MacTeX) |
| `pbpaste` | Clipboard access | Built-in          |
| `lpr`     | CUPS printing    | Built-in          |

## Output

- **PDF location**: `/tmp/terminal-output-YYYYMMDD_HHMMSS.pdf`
- **Markdown source**: `/tmp/terminal-YYYYMMDD_HHMMSS.md`
- **Cleanup**: macOS automatically cleans `/tmp` periodically

## Troubleshooting

### "No text in clipboard"

Copy terminal output first using Cmd+C in iTerm2.

### "Missing pandoc" or "Missing xelatex"

Install MacTeX: `brew install --cask mactex`

### Printer not found

Check printer status: `lpstat -p -d`

The script auto-detects the system default printer. Override with `--printer NAME` or set `TERMINAL_PRINT_PRINTER` in the environment.

### Blank page came out (or `lpr` reported success but nothing printed)

Strong fingerprint of the **HP LaserJet Pro MFP 3101/3108/3201/3208/3301/3308 AirPrint blank-page bug** — the printer's IPP-Everywhere PDF interpreter silently drops jobs while CUPS reports `completed`. Confirmed with this exact symptom on 2026-05-09.

**Quick fix:**

```bash
# 1. One-time setup of bypass queue (socket-9100 + Generic PostScript PPD)
"$(cc-plugin-root doc-tools)/skills/terminal-print/assets/setup-socket-9100-queue.sh"

# 2. Reprint with --bypass-airprint
bash "$(cc-plugin-root doc-tools)/skills/terminal-print/assets/print-terminal.sh" --bypass-airprint
```

**Full diagnostic playbook with command sequences and decision tree:** see [airprint-blank-page-troubleshooting.md](references/airprint-blank-page-troubleshooting.md).

Key takeaway: do not trust `lpstat -o` or `job-state=completed` — query the **printer's own job ledger** via `ipptool -tv ipp://<printer>.local.:631/ipp/print` for `job-impressions-completed` and `job-media-sheets-completed`. CUPS lies; the printer (mostly) tells the truth.

## Related Skills

- [pandoc-pdf-generation](../pandoc-pdf-generation/SKILL.md) - General Markdown to PDF conversion
- [asciinema-converter](../../../asciinema-tools/skills/asciinema-converter/SKILL.md) - Convert terminal recordings

## Post-Execution Reflection

After this skill completes, check before closing:

1. **Did the command succeed?** — If not, fix the instruction or error table that caused the failure.
2. **Did parameters or output change?** — If the underlying tool's interface drifted, update Usage examples and Parameters table to match.
3. **Was a workaround needed?** — If you had to improvise (different flags, extra steps), update this SKILL.md so the next invocation doesn't need the same workaround.

Only update if the issue is real and reproducible — not speculative.
