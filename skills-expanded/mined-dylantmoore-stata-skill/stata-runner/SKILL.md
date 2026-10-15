---
description: "Run Stata .do files in batch mode from the terminal. Provides binary paths and batch execution syntax for macOS."
---

# Stata Runner

This skill only tells you how to execute Stata code. It does not contain Stata programming reference material.

## Running Stata from the Command Line

You can execute Stata code by running `.do` files in batch mode from the terminal.

### Finding the Stata Binary

Stata on macOS is a `.app` bundle. The actual binary is inside it. Common locations:

```
# Stata 18 / StataNow (most common)
/Applications/Stata/StataMP.app/Contents/MacOS/stata-mp
/Applications/StataNow/StataMP.app/Contents/MacOS/stata-mp

# Other editions (SE, BE)
/Applications/Stata/StataSE.app/Contents/MacOS/stata-se
/Applications/Stata/StataBE.app/Contents/MacOS/stata-be
```

If Stata isn't on `$PATH`, find it with: `mdfind -name "stata-mp" | grep MacOS`

### Batch Mode (`-b`)

```bash
# Run a .do file in batch mode — output goes to <filename>.log
/Applications/Stata/StataMP.app/Contents/MacOS/stata-mp -b do analysis.do

# If stata-mp is on PATH (e.g., via symlink or alias):
stata-mp -b do analysis.do
```

- `-b` = batch mode (non-interactive, no GUI)
- Output (everything Stata would display) is written to `analysis.log` in the working directory
- Exit code is 0 on success, non-zero on error
- The log file contains all output, including error messages — check it after execution

### Running Inline Stata Code

To run a quick Stata snippet without creating a `.do` file:

```bash
# Write a temp .do file and run it
cat > /tmp/stata_run.do << 'EOF'
sysuse auto, clear
summarize price mpg
EOF
stata-mp -b do /tmp/stata_run.do
cat /tmp/stata_run.log
```

### Checking Results

```bash
# Check if it succeeded
stata-mp -b do tests/run_tests.do && echo "SUCCESS" || echo "FAILED"

# Search the log for pass/fail
grep -E "PASS|FAIL|error|r\([0-9]+\)" run_tests.log
```

### Tips

- **`clear all` at the top of batch scripts** — batch mode starts with a fresh Stata session, but `clear all` ensures no stale state.
- **`set more off`** — prevents Stata from pausing for `--more--` prompts (fatal in batch mode).
- **Log files overwrite silently** — `analysis.do` always writes to `analysis.log` in the current directory.
- **Working directory** — Stata's working directory is wherever you run the command from, not where the `.do` file lives.
