# Super Dev Integration for codex-cli

Super Dev 是“超级开发战队”，一个流水线式 AI Coding 辅助工具。
Super Dev does not provide model inference or coding APIs.
The host remains responsible for model execution, tools, and actual code generation.
Use the host model/runtime as-is; Super Dev only enforces the delivery protocol.
Use Super Dev generated artifacts as source of truth.

## Runtime Contract
- Treat Super Dev as a local Python CLI plus host-side rules/skills, not as a separate model provider.
- When the user triggers Super Dev, enter the protocol immediately instead of treating it as normal chat.
- Use host-native web/search/browse for research and host-native editing/execution for implementation.
- Use local `super-dev` commands to generate/update documents, spec artifacts, quality reports, and delivery outputs.

## First-Response Contract
- On the first reply after `/super-dev ...` or `super-dev: ...`, explicitly state that Super Dev pipeline mode is now active rather than normal chat mode.
- The first reply must explicitly state that the current phase is `research`, and that you will read `knowledge/` plus `output/knowledge-cache/*-knowledge-bundle.json` first when available before similar-product research.
- The first reply must explicitly state the next sequence: research -> three core documents -> wait for user confirmation -> Spec / tasks -> frontend first with runtime verification -> backend / tests / delivery.
- The first reply must explicitly promise that you will stop after the three core documents and wait for approval before creating Spec or writing code.

## Local Knowledge Contract
- Read relevant files under `knowledge/` before drafting documents.
- If `output/knowledge-cache/*-knowledge-bundle.json` exists, read its `local_knowledge`, `web_knowledge`, and `research_summary` first.
- Treat matched local knowledge, checklists, anti-patterns, and scenario packs as project constraints that must flow into docs, spec, and implementation.

## Trigger
- Preferred: say `super-dev: <需求描述>` in the host chat so AGENTS.md + the `super-dev` skill can govern the workflow.
- Local terminal only handles `super-dev`, `super-dev update`, and `super-dev uninstall`; normal development should continue inside the host chat.
- Do not rely on `/super-dev` in this host.

## Required Context
- output/*-prd.md
- output/*-architecture.md
- output/*-uiux.md
- output/*-execution-plan.md
- .super-dev/changes/*/tasks.md

## Execution Order
1. Use the host's native browse/search/web capability to research similar products first and produce output/*-research.md
2. Freeze PRD, architecture and UIUX documents
3. Stop after the three core documents, summarize them to the user, and wait for explicit confirmation before creating Spec or coding
4. Create Spec proposal/tasks only after the user confirms the documents
5. Implement and run the frontend first so it becomes demonstrable before backend-heavy work
6. Implement backend APIs and data layer, then run tests, quality gate, and release preparation
