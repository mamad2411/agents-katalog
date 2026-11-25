---
name: formax-permissions-workflow
description: Use when implementing or debugging Formax permissions/policy/approval behavior and UI (allow/ask/deny rules, workspace boundaries, approval prompts, and /permissions overlay parity with Claude Code).
---

# Formax permissions / approvals workflow

## Goal

Use this skill when changing policy preflight, approval prompts, remember side-effects, or `/permissions` management.

## Read First

- `docs/contracts/permissions-policy-contract.md`
- `docs/contracts/interactive-input-contract.md`
- `docs/contracts/semantics-contract.md` when the change crosses TUI / app-server / Web

These docs are canonical. If stable behavior changes, update them before or with code.

## Code Map

### 1) Policy preflight (ToolCall -> allow/ask/deny decision)
- `packages/core/src/tools/executor/policyPreflight.ts`: turns `ToolCall` into a `PolicyAction` and decides deny / prompt / allow
- `packages/core/src/tools/executor/policyAction.ts`: `ToolCall` -> `PolicyAction` mapping
- `packages/core/src/tools/executor/policyExplain.ts`: explain / debug text for decisions
- `packages/core/src/tools/modules/bash/policy.ts`: Bash risk classification

### 2) Permissions storage + matching (rules & precedence)
- `packages/core/src/adapters/permissions/permissionsStore.ts`: read / write settings and merge precedence
- `packages/core/src/adapters/permissions/permissionKeys.ts`: stable keys / paths for settings
- `packages/core/src/adapters/permissions/matcher.ts`: matcher semantics

### 3) Approvals (prompt UI + persistence side-effects)
- `packages/core/src/tools/executor/approvalService.ts`: `ensureApproved` flow and remember writes
- UI prompts:
  - `packages/core/src/components/tool/bashApprovalPrompt.tsx`
  - `packages/core/src/components/tool/fsReadApprovalPrompt.tsx`
  - `packages/core/src/components/tool/fsWriteApprovalPrompt.tsx`
  - `packages/core/src/components/tool/skillApprovalPrompt.tsx`
  - `packages/core/src/components/tool/editApprovalPrompt.tsx`
- Shared pieces:
  - `packages/core/src/components/ui/ApprovalHeader.tsx`
  - `packages/core/src/components/ui/ConfirmMenu.tsx`

### 4) /permissions overlay (manage rules + workspace)
- `packages/core/src/tui/permissions/PermissionsDialog.tsx`: state machine + key handling
- `packages/core/src/tui/permissions/ui.tsx`: rendering primitives
- `packages/core/src/features/repl/controller/ui/overlays.ts`: overlay open / close and dismissal messages
- Slash command wiring:
  - `packages/core/src/features/commands/registry.ts`
  - `packages/core/src/screens/repl/createReplCommandRegistry.ts`

If app-server or Web input behavior moves, also inspect:
- `packages/core/src/app-server/turn/inputStore.ts`
- `packages/core/src/app-server/server.ts`
- `packages/web-reference-react/src/store.ts`

## High-Signal Patterns

- Pattern A: tool approval prompt (3 options + Esc)
  - `Yes`
  - `Yes, ...` (remember / allow in repo or session)
  - `Type here to tell Claude what to do differently`
  - cancellation remains `Esc to cancel`, not a bespoke menu item
- Pattern B: destructive confirm prompt
  - use `Yes / No`
  - still support `Esc to cancel`
- Pattern C: partial emphasis in menu options
  - use `ConfirmMenu` emphasis support instead of ad-hoc JSX or ANSI
  - selected rows must not leave mismatched emphasis colors behind

## Minimal Workflow

1. Read the canonical contract(s) above and define the exact behavior delta.
2. Change the narrowest canonical code path first (`policyPreflight`, matcher / store, `approvalService`, or overlay state machine).
3. Preserve existing UI copy / spacing / colors / keys unless the user explicitly asks for UI changes.
4. Keep “what the user sees” separate from “what is injected back into model context”.
5. Run the minimum regression set below, then review via `AGENTS.md` before commit.

## Minimum Regression

- `bun run test -- packages/core/src/tools/executor/policyPreflight.test.ts`
- `bun run test -- packages/core/src/tools/executor/approvalService.test.ts`
- `bun run test -- packages/core/src/components/tool/bashApprovalPrompt.test.tsx`
- `bun run test -- packages/core/src/components/tool/fsReadApprovalPrompt.test.tsx`
- `bun run test -- packages/core/src/components/tool/fsWriteApprovalPrompt.test.tsx`
- `bun run test -- packages/core/src/components/tool/skillApprovalPrompt.test.tsx`
- `bun run test -- packages/core/src/tui/permissions/PermissionsDialog.test.tsx`
- If app-server / Web input behavior changed:
  - `bun run test -- packages/core/src/app-server/turn/inputStore.test.ts packages/core/src/app-server/server.test.ts`
  - `npm --prefix packages/web-reference-react run test -- src/store.test.ts`

## Guardrails

- Do not encode permission semantics inside prompt components; contracts live in policy / approval layers.
- Do not add bespoke key handling or ANSI styling when shared approval components already cover the case.
- Do not loosen permissions or remember scope just to make parity demos pass.
- Preserve approval UI copy / spacing / colors / key paths unless the user explicitly asks for UI changes.
