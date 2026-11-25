# Skill: test-plan

Executable test plan runner that wraps `@playwright/cli`.

## Context
This skill converts static markdown test plans (STAN-format) into executable browser-driven verification runs. It prioritizes token efficiency by using Microsoft's CLI-based "Spec-driven testing" instead of sending full accessibility trees to the AI.

## Prerequisite
- `@playwright/cli` must be installed: `npm install -g @playwright/cli@latest && playwright-cli install --skills`

## Usage
Run this skill against a markdown test plan file or URL.

### Arguments
- `target`: Path to the test plan markdown file (default: `docs/testplan.md`).
- `profile`: Auth profile to use from `~/.test-plan/state/<profile>.json`.
- `prod`: Boolean flag. If true, requires explicit host confirmation.

## Workflow

1. **Environment Check**:
   - Verify `playwright-cli` is installed and the specific `spec-driven-testing` skill is active.
   - Load the auth profile and check TTL. Refuse to start if expired.

2. **Parsing**:
   - Parse the markdown table into a JSON manifest of behaviors.
   - Map each row to a coverage state (Manual, Untested, Automated).

3. **Execution**:
   - For every row marked **Manual** or **Untested**:
     - Call `playwright-cli drive --behavior "<behavior_text>"`
     - Capture pass/fail, evidence, screenshot, and trace.
   - For rows marked **Automated**:
     - (Optional) Verify the linked test exists, or skip if already verified by another runner (pytest/vitest).

4. **Reporting**:
   - Emit a `coverage-report.md` in `~/.youros/test-runs/<timestamp>/`.
   - The report must maintain the same table shape as the input.
   - Include a "Parser Confidence" section for rows where the input format was ambiguous.

## Safety
- Refuse to drive against any host not in `~/.test-plan/safe-hosts.json` unless `--prod` is passed.
- `--prod` runs MUST require the user to manually type the target host to confirm.
