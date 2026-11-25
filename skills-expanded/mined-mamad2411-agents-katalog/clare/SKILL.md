# CLARE Framework Rules

This project uses the CLARE framework. Detailed rules are in `.cursor/rules/`.

## Core Rule
After editing a file, run `./clare/verify-ci.sh` before marking work complete. Run it only in a turn where you edited a file — not in plan-mode, research, or read-only turns. See `.cursor/rules/clare-workflow.mdc` for the full procedure.

## Cross-Agent Sync Rule
When CLARE agent configuration changes, update all supported agent environments in the same change:
- Copilot: `.github/copilot-instructions.md` and `install/.github/copilot-instructions.md`
- Claude: `CLAUDE.md` and `install/root/CLAUDE.md`
- Codex: `AGENTS.md` and `install/root/AGENTS.md`
- Cursor: `.cursorrules` and `install/root/.cursorrules`
- Roo/Zoo Code: `.roo/rules/clare.md` and `install/.roo/rules/clare.md`

## Before Any File Change
Check `clare/autonomy.yml` for the file path:
- `full-autonomy` → proceed
- `supervised` → generate + add "⚠ Human review required"
- `humans-only` → STOP, notify user, do not generate code

## Five Principles
- [C] Constrained: rules exist in tests/linters, not comments
- [L] Limited: autonomy.yml defines where AI can work alone
- [A] Assertive: tests enforce invariants, not implementations
- [R] Reality-Aligned: one source of truth per domain concept
- [E] Ephemeral: regenerate generated code, never patch it

## CLARE₂ Commands

When the CLARE₂ pipeline container is running:
- `/project:clare2-capture start` — begin session JSONL capture
- `/project:distill` — trigger on-demand distillation pass

## Full Rules
See `.cursor/rules/` for detailed MDC rule files.
See `clare/principles.md` for the principle reference card.
See `CLAUDE.md` for the complete workflow specification.

## CLARE₂ Temper Routing

Use `clare_temper_route(project, task_kind, capabilities)` for an opaque route
ID and send `X-CLARE-Route-ID` to the policy proxy. Never select/load adapters,
provide adapter paths, call raw vLLM management endpoints, or access Docker.
