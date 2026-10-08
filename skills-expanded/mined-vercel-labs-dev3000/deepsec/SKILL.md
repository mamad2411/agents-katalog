---
name: deepsec
description: Run DeepSec against a Vercel project checkout from dev3000. Use for one-click DeepSec setup, project context bootstrapping, bounded first-pass processing, and report generation.
---

# DeepSec Dev3000 Runbook

Use this skill to turn the manual DeepSec workflow into a repeatable dev3000 run against the current Vercel project checkout.

## Operating Policy

- Work from the real project checkout at `/workspace/repo`.
- Do not write AI credentials into `.deepsec/.env.local` or any tracked file. The dev3000 runtime passes AI Gateway credentials through the process environment.
- Default dev3000 runs are a bounded first pass. Do not run an unbounded `process` or `revalidate` command unless the user explicitly asks for a full DeepSec scan in run-specific instructions.
- Keep generated scan state in the locations DeepSec already gitignores. Commit only the durable setup/context files and human-readable findings report.
- Treat DeepSec as a coding agent with shell access. Do not run it on untrusted source inputs.

## Default Flow

1. Inspect the project shape:
   - Read `README.md` if present.
   - Read `AGENTS.md` or `CLAUDE.md` if present.
   - Skim representative files for auth, middleware, request handlers, data access, billing, webhooks, and security-sensitive boundaries.
2. Initialize DeepSec if needed:
   - If `.deepsec/` is absent, run `npx --yes deepsec@latest init`.
   - If `.deepsec/` already exists, do not force overwrite it.
3. Install DeepSec workspace dependencies:
   - Run `corepack pnpm install` from `.deepsec/`.
   - Ensure the Claude Agent SDK native binary that DeepSec actually uses is available. Do not run a Claude Code postinstall; DeepSec uses `@anthropic-ai/claude-agent-sdk`.
   - If `corepack pnpm` is unavailable, run `pnpm install` only after confirming `pnpm` exists.
4. Fill the generated project context:
   - Read `.deepsec/node_modules/deepsec/SKILL.md`.
   - Read `.deepsec/data/<id>/SETUP.md`.
   - Replace `.deepsec/data/<id>/INFO.md` with concise project-specific context.
   - Keep `INFO.md` to roughly 50-100 lines.
   - Use 3-5 examples per section. Name local primitives such as auth helpers, middleware, database clients, webhook handlers, and privileged APIs.
   - Do not include line numbers, generic CWE lists, or broad framework summaries.
5. Run the scan:
   - Run `corepack pnpm deepsec scan` from `.deepsec/`.
6. Run bounded AI processing:
   - Default command: `corepack pnpm deepsec process --limit 25 --concurrency 2 --batch-size 3`.
   - If the candidate set is below the limit, state that all discovered candidates were processed.
   - If the user explicitly requested a full run, use the requested limit/concurrency or omit `--limit`.
   - If the process command fails, stop and report the failure. Do not generate a manual fallback report from regex candidates.
7. Generate the findings report:
   - Run `corepack pnpm deepsec export --format md-dir --out ./findings`.
   - If there are no findings, create `.deepsec/findings/README.md` summarizing that this bounded pass found no findings and include the exact commands that were run.
8. Summarize the run:
   - Include commands run, project id, limit/concurrency, and whether the report contains findings.
   - Do not include a "Next Steps - Full Scan" section by default.
   - Only include a follow-up scan section if DeepSec reports unprocessed candidates or the user explicitly asked about deeper coverage. Label it "Optional Deeper Follow-Up" and explain exactly how it differs from the completed run.

## Validation

- Prefer DeepSec's own command output, `corepack pnpm deepsec status`, and generated finding files as validation.
- Do not start a dev server or browser unless the user explicitly asks for visual/runtime verification.
- Before finishing, check `git diff --stat` and make sure no secrets, `node_modules`, `.env.local`, or raw scan state are staged by accident.
