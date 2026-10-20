---
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Agent
description: Run health check, collect errors, pass to SDLC workflow for fixing
model: opus
---

# Purpose

Run the project health check (build, type-check, tests), collect all errors and failures, then pass the collected errors to the ADW SDLC workflow for automated fixing. Follow the `Instructions` and `Workflow` sections below.

## Instructions

- Run all three health checks: build, type-check (svelte-check), and tests
- Capture the full error output from each failing step
- Do NOT stop at the first failure — run all checks and collect all errors
- Format the errors into a structured error report
- Pass the error report to the ADW SDLC workflow via the ADW_PROMPT env var
- The SDLC workflow lives at `adws/workflows/classic/adw_sdlc.ts`
- Generate a short unique ADW ID for the healing run (e.g. `heal_<8-char-hex>`)
- If no errors are found, report a clean bill of health and exit

## Workflow

1. Run `bun run build` and capture stdout+stderr. Record pass/fail and any error output.
2. Run `bun run check` and capture stdout+stderr. Record pass/fail and any error output.
3. Run `vitest run adws/tests/` and capture stdout+stderr. Record pass/fail and any error output.
4. If all three steps pass, report "Health check passed — no healing needed" and stop.
5. Compile a structured error report with sections for each failing step, including the full error output.
6. Generate an ADW ID: `heal_` followed by 8 random hex characters.
7. Launch the SDLC workflow to fix the errors:
   ```bash
   ADW_PROMPT="<error_report>" bun run adws/workflows/classic/adw_sdlc.ts --adw-id <generated_id>
   ```
8. Report the result of the healing run.

## Report

- List which health checks passed and which failed
- Show a summary of collected errors (file, line, message) for each failing step
- Report the ADW ID used for the healing run
- Report whether the SDLC workflow succeeded or failed