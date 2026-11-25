---
name: paper-research-workflow
description: Use when the user asks to read, process, classify, explain, reproduce, store, query, or mine innovation ideas from local computer-science research papers. Orchestrates the paper research skill suite across ingest, plain explanation, expert reading, reproduction planning, knowledge-base updates, and innovation mining.
---

# Paper Research Workflow

## Role

Act as the complete installable paper research skill suite. This single skill is the recommended `npx skills add` target and includes the scripts, schemas, templates, and references needed to run without installing the six child workflows separately.

Route natural user requests to the six internal child workflows:

- `references/child-skills/paper-ingest-classifier.md`
- `references/child-skills/paper-plain-explainer.md`
- `references/child-skills/paper-expert-reader.md`
- `references/child-skills/paper-code-reproducer.md`
- `references/child-skills/paper-knowledge-base.md`
- `references/child-skills/paper-innovation-miner.md`
- `references/child-skills/paper-web-workbench.md`

Use this skill when the user asks to "read this paper", process a local PDF, update the paper knowledge base, prepare a reproduction plan, or find innovation ideas from stored papers.

## Language Rule

Default to Chinese for all user-facing conversation, prompts, Markdown reports, explanations, expert readings, reproduction plans, innovation briefs, and status summaries. Keep paper titles, author names, method names, model names, datasets, metrics, benchmark names, code identifiers, equations, and quoted technical terms in their original language when translation would reduce recognizability.

Support hot language switching inside the same paper workspace:

- When the user says `切换英文`, `英文模式`, `English mode`, or asks to answer in English, switch subsequent user-facing outputs to English.
- When the user says `切换中文`, `中文模式`, `Chinese mode`, or asks to answer in Chinese, switch subsequent user-facing outputs back to Chinese.
- If the user's current message is mostly English, answer in English for that request unless a saved or explicit Chinese preference is active.
- If the user's current message is mostly Chinese, answer in Chinese for that request and keep Chinese as the default.

The language setting affects generated Markdown artifacts, but does not change machine-readable JSON field names or schema values unless a schema field explicitly stores natural-language prose.

## First-Run Rule

Before processing the first paper, check whether `.paper-workspace.json` exists in this skill directory. If it does not exist, ask the user where to create the long-term paper workspace. Do not silently create `workspace/` by default.

After the user chooses a directory, run:

```bash
python scripts/paper_workflow.py setup --workspace <chosen-dir> --save-default
```

All later paper PDFs, extraction artifacts, Markdown analyses, reproduction plans, innovation briefs, and knowledge-base JSON files must use this saved workspace unless the user explicitly overrides it.

## MinerU Cloud Rule

This skill is self-contained and must not assume another MinerU skill exists. For high-quality cloud PDF parsing, ask the user for their MinerU token the first time, then run:

```bash
python scripts/paper_workflow.py configure-mineru --standard-token <token>
```

The token is saved in `.paper-mineru.json` inside this skill directory. Later high-quality runs should use the saved config and must not ask again unless parsing reports a missing or invalid token.

Use high-quality cloud parsing with:

```bash
python scripts/paper_workflow.py ingest <pdf> --prefer-mineru --mineru-backend standard-cloud
```

If the user does not want to configure a token, use `--mineru-backend agent-cloud` for lightweight cloud parsing or let `--mineru-backend auto` choose the best available backend.

Cloud MinerU requests default to direct connections and ignore system proxy environment variables. Use `MINERU_USE_PROXY=1` only if the user explicitly asks to route MinerU through a proxy.

## Local Docker MinerU Rule

This skill bundles its own local Docker MinerU entry and should reuse it for `--mineru-backend local`. Do not depend on another installed MinerU skill.

Check status with:

```bash
python scripts/paper_workflow.py local-mineru --status
```

If local Docker MinerU is not enabled yet and the user wants local high-quality parsing, ask whether to enable it first. After the user confirms, run:

```bash
python scripts/paper_workflow.py local-mineru --enable
```

If the user does not already have a prepared MinerU Docker directory, this command may also be called with `--docker-dir <dir>` plus `--source-archive-url <url>` and `--source-subdir <path>` so the skill can prepare a full official build context automatically. Use `--dockerfile-url <url>` only as a fallback when a full source archive is unavailable.

Then use:

```bash
python scripts/paper_workflow.py ingest <pdf> --prefer-mineru --mineru-backend local
```

`auto` prefers configured high-quality cloud token, then local Docker MinerU or local `mineru`, then lightweight `agent-cloud`.

## Shared Contracts

Use `scripts/paper_workflow.py` for setup, status, validation, query, and deterministic state updates.

For later requests, use the saved default workspace unless the user explicitly overrides it with `--workspace`.

Use `templates/` for output shape. Use `schemas/` for validation. Use `references/` for PDF extraction, MinerU, and child workflow guidance. Every paper should maintain canonical memory at:

```text
workspace/knowledge/papers/<paper-id>.json
```

Workspace layout:

```text
workspace/inbox/
workspace/extracted/<paper-id>/
workspace/knowledge/cards/
workspace/knowledge/expert-readings/
workspace/knowledge/reproductions/
workspace/knowledge/innovations/
workspace/state/papers.json
```

## Web Workbench

This skill also bundles a React/Vite visual workbench template in `web/`. During first workspace setup, copy it into the user's selected paper workspace at `<workspace>/web`; run npm install, npm run dev, service state, and logs in that target workspace copy, not in the installed skill directory.

Setup and Web maintenance commands export live workspace data to `<workspace>/web/public/paper-workbench-data.json`. The running React app hot-reads this JSON every 5 seconds, so the visualizer reflects real workspace papers, categories, full Markdown reading artifacts, reproduction plans, and innovations. Empty workspaces show an empty state and must not fall back to bundled sample papers. Use `web --web-command release --force-release` to refresh an existing released template; it backs up the old `<workspace>/web` and copies a clean template while excluding runtime directories and build outputs.

The workbench presents category navigation on the left and reading entry buttons on the right: `通俗易懂`, `专家阅读`, and `复现计划`. Clicking an entry opens the built-in Markdown document reader for the full generated `.md` artifact. The reader includes a platform request box for `Codex`, `Claude Code`, or `OpenClaw`, producing a structured prompt that asks the selected platform to refine that part of the workflow and save a new version unless the user explicitly requests overwrite.

The `创新挖掘` view shows ranked innovation ideas, scores, and source links back to the specific papers and reading cards that inspired the idea.

Run it from the installed skill directory:

```bash
python scripts/paper_workflow.py web --web-command start --workspace <workspace>
python scripts/paper_workflow.py web --web-command status --workspace <workspace>
python scripts/paper_workflow.py web --web-command release --workspace <workspace> --force-release
python scripts/paper_workflow.py web --web-command refresh-data --workspace <workspace>
python scripts/paper_workflow.py web --web-command validate-release --workspace <workspace>
python scripts/paper_workflow.py web --web-command logs --workspace <workspace>
python scripts/paper_workflow.py web --web-command stop --workspace <workspace>
```

Read `references/child-skills/paper-web-workbench.md` for Web service lifecycle and maintenance tasks.

## Routing

For a full paper read:

1. If no default workspace exists, ask where to create it and run `python scripts/paper_workflow.py setup --workspace <chosen-dir> --save-default`.
2. Read `references/child-skills/paper-ingest-classifier.md` to extract, classify, archive, and create initial memory.
3. Read `references/child-skills/paper-plain-explainer.md` to create the plain-language card.
4. Read `references/child-skills/paper-expert-reader.md` to create the expert reading and innovation seeds.
5. Read `references/child-skills/paper-code-reproducer.md` to create the reproduction plan.
6. Read `references/child-skills/paper-knowledge-base.md` to update and validate memory.
7. Read `references/child-skills/paper-innovation-miner.md` only when the user asks for related papers or innovation directions.
8. Read `references/child-skills/paper-web-workbench.md` only when the user asks to start, stop, inspect, debug, build, test, preview, or maintain the Web visualizer.

For partial requests, call only the matching child skill and keep `workspace/knowledge/papers/<paper-id>.json` updated.

## Stop Conditions

Stop and report clearly when the local PDF is missing, extraction fails, schema validation fails, or the knowledge base has too few related papers for useful innovation mining. Do not invent missing tables, formulas, code availability, or benchmark results.
