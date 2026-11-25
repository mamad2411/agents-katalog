---
name: repetitive-workflow-automator
description: Build reliable local automation projects from demonstration videos, documents, screenshots, written procedures, websites, and spreadsheet inputs. Use when Codex must analyze a repetitive browser-and-Excel workflow, generate or adapt a Playwright and ExcelJS script, map records and fields, add retries/logging/checkpoints/pause controls, validate on a small sample, and prepare a reusable handoff. Do not use for one-off manual data entry, unauthorized access, CAPTCHA bypass, or attempts to evade a site's controls.
---

# Repetitive Workflow Automator

Turn a demonstrated repetitive workflow into a deterministic, reviewable automation project. Treat each new platform as an adapter over a reusable browser, workbook, logging, retry, and checkpoint core.

## Required workflow

1. Collect and inspect every available source: video, document, written instructions, screenshots, sample input files, expected output, and the target website.
2. Read [references/intake-and-analysis.md](references/intake-and-analysis.md) and create a workflow specification before writing site code.
3. Inspect the input workbook and sample files without modifying originals. Record sheet names, headers, column mappings, record keys, formats, duplicates, blank values, and expected output cells.
4. Read [references/architecture.md](references/architecture.md). Copy `assets/automation-template/` into a new task project by running:

   ```text
   node scripts/create-project.mjs <destination> [project-name]
   ```

5. Keep reusable runtime code unchanged where possible. Implement platform-specific behavior only in `src/site-adapter.mjs`; put task-specific mappings in `config.json`.
6. Use Playwright locators based on roles, labels, stable test IDs, or stable attributes. Avoid coordinates unless there is no structured alternative. Read [references/browser-automation.md](references/browser-automation.md).
7. Use ExcelJS through the workbook adapter. Never overwrite the source workbook. Save to a new output path and write atomically. Read [references/excel-automation.md](references/excel-automation.md).
8. Add bounded waits and retries only for transient, safe, and idempotent steps. Do not blindly resubmit a query or form when its outcome is unknown.
9. Read [references/troubleshooting.md](references/troubleshooting.md) when the workflow stalls, times out, fails to write output, loses row alignment, or behaves differently after restart. Diagnose from evidence before changing selectors or timing.
10. Preserve checkpoints, per-item logs, error screenshots, pause/safe-stop controls, and a failed-item report.
11. Run `npm ci`, then `npm test`, then a dry run. Test one representative record before a larger batch.
12. Compare actual output with the expected result. Verify row alignment, workbook formatting needed by the task, resumability, and behavior when files are locked or page elements load slowly.
13. Produce a concise handoff: prerequisites, configuration fields, start/stop controls, output location, known limitations, and third-party notices.

## Troubleshooting knowledge

- Preserve verified, reusable debugging conclusions as `symptom -> likely cause -> evidence -> bounded remedy -> stop condition`; omit chat history and unsuccessful experiments.
- Treat timing values as configurable defaults, not universal constants. Prefer observable readiness conditions and use fixed delays only as bounded supplements.
- Change one variable at a time and verify the smallest failing step before resuming a batch.
- Do not convert a site-specific workaround into shared core behavior until it succeeds on a representative rerun.

## Input rules

- Accept demonstrations as video, documents, written steps, screenshots, or a combination.
- Treat demonstrations as evidence, not executable truth. Identify unclear steps and verify them against the live page or sample files.
- Ask only for missing information that changes the implementation materially. Otherwise state reasonable assumptions and build a one-record prototype.
- Never put credentials, cookies, private workbooks, browser profiles, or production data in the generated repository.

## Reuse boundary

Reuse these layers across projects:

- configuration loading and validation;
- delay, bounded retry, and wait helpers;
- workbook row mapping and safe output writing;
- structured logs and screenshots;
- checkpoint/resume and completed-row skipping;
- pause, safe stop, and emergency stop;
- project validation and tests.

Replace or extend these layers per task:

- login and navigation;
- selectors and page-ready conditions;
- file upload or download behavior;
- query submission and result extraction;
- workbook/document field mappings;
- task-specific correctness checks.

## Safety and scope

- Automate only systems and data the user is authorized to use.
- Follow site terms, published APIs, access limits, and organizational policy.
- Use pacing for stability and service load, not to disguise automation or evade enforcement.
- Stop on authentication failures, access-denied responses, rate-limit responses, unexpected destructive actions, or ambiguous submissions.
- Require explicit confirmation before the first non-dry-run batch and before any workflow with external side effects beyond the user's stated task.
- Keep the original input immutable and make recovery possible.

## Dependency policy

- Use pinned npm dependencies and a committed lockfile; do not bundle `node_modules` or browser binaries.
- Install with `npm ci`. Install Playwright Chromium only when the generated project uses bundled Chromium; system Chrome can be selected through configuration when appropriate.
- Preserve upstream notices. Read [references/open-source-decision.md](references/open-source-decision.md) before changing dependencies.

## Validation commands

Validate this skill:

```text
python <skill-creator>/scripts/quick_validate.py <skill-directory>
node scripts/validate-template.mjs
```

Validate a generated project:

```text
npm ci
npm test
npm run check-config
npm run dry-run
```

## Deferred capability

Do not implement a graphical first-run configuration page in version 1. Keep JSON configuration as the supported setup path. Preserve the configuration schema so a future local setup UI can write the same file without changing runtime behavior. Word and PowerPoint adapters are also future extensions; see [references/roadmap.md](references/roadmap.md).
