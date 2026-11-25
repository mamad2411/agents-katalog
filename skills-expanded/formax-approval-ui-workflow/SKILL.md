---
name: formax-approval-ui-workflow
description: Use when adding or changing any Approval prompt/presenter.
---

# formax-approval-ui-workflow

## Goal

- Keep **Approval prompts** visually consistent + Claude Code-aligned (only when explicitly requested).
- Preserve existing **behavior + keyboard flow** (Enter/Esc/Shift+Tab), avoid UI regressions.
- Keep preview rendering **fast and safe** (no sync IO in render; guard against quadratic diffs).
## Where to change what

- Shared approval “chrome”
  - `packages/core/src/components/ui/ApprovalHeader.tsx` (top divider + title color)
  - `packages/core/src/components/ui/ConfirmMenu.tsx` (numbered options + selection color)
- Preview (optional section under header)
  - `packages/core/src/components/tool/ApprovalPreview.tsx` (simple file preview)
  - `packages/core/src/components/tool/PatchApprovalPreview.tsx` (edit-file wrapper: header + file + preview)
  - `packages/core/src/components/tool/PatchPreview.tsx` (diff rendering + performance guards)
- Per-tool approval prompts (labels, options, allow/ask/deny / remember write paths)
  - `packages/core/src/components/tool/bashApprovalPrompt.tsx`
  - `packages/core/src/components/tool/fsReadApprovalPrompt.tsx`
  - `packages/core/src/components/tool/fsWriteApprovalPrompt.tsx`
  - `packages/core/src/components/tool/skillApprovalPrompt.tsx`
  - (if present) `packages/core/src/components/tool/editApprovalPrompt.tsx` (legacy)
- Tool presenters that mount approval prompts
  - `packages/core/src/tools/modules/bash/presenter.tsx`
  - `packages/core/src/tools/modules/read/presenter.tsx`
  - `packages/core/src/tools/modules/write/presenter.tsx`
  - `packages/core/src/tools/modules/edit/presenter.tsx`
  - `packages/core/src/tools/modules/skill/presenter.tsx`
- Colors / theme
  - `packages/core/src/tui/theme.ts` (`theme.permission`, `theme.text`, `theme.diff.*`)
## Patterns

- Layout skeleton (keep consistent)
  - `[Top divider line]`
  - `Title` (color = `theme.permission`)
  - Optional `Preview` box
  - Question line (e.g. “Do you want to … <file>?”)
  - Options list (numbered)
  - Bottom hint (e.g. “Esc to cancel”)

- Options rendering (text + emphasis)
  - If an option needs mixed styling (e.g. make `capture-terminal/` bold/white): make `ConfirmMenu` accept `ReactNode` labels.
  - Ensure **selection color wins** over nested `Text color={...}` when highlighted:
    - Prefer passing “unstyled” children and let row wrapper decide color, or
    - In nested text, only set `bold`, avoid hardcoding `color` unless required.

- Preview performance (must not block UI)
  - No `fs.readFileSync`/`fs.statSync`/blocking IO inside render path (`useMemo` included).
  - If file context is needed (e.g. line numbers), compute via async `fs/promises` + `useEffect`.

- Diff safety (avoid OOM / hangs)
  - Any token/word diff based on DP/LCS must have a **hard cap** (max cells).
  - If cap exceeded: fall back to truncated / line-only / “too large to diff” preview.
## Tests to update

- Unit/component tests (minimum regression set):
  - `packages/core/src/components/ui/ConfirmMenu.test.tsx` (ReactNode label + selection color)
  - `packages/core/src/components/tool/bashApprovalPrompt.test.tsx` (if exists)
  - `packages/core/src/components/tool/fsReadApprovalPrompt.test.tsx` (if exists)
  - `packages/core/src/components/tool/fsWriteApprovalPrompt.test.tsx` (if exists)
  - `packages/core/src/components/tool/skillApprovalPrompt.test.tsx` (if exists)
  - `packages/core/src/tools/modules/edit/presenter.test.tsx` (preview/diff layout + performance guard)

- Manual spot-check (fast)
  - Trigger one approval for each kind: `Bash`, `Read(outside workspace)`, `Write`, `Edit`.
  - Verify: top divider, title color, option numbering, selection color, Esc behavior.
## Guardrails

- Do **not** change UI copy/spacing/colors unless explicitly requested for Claude Code parity.
- Treat **UI output vs model context injection** as orthogonal; don’t change injection behavior as a side-effect of approval UI work.
- Do **not** add a syntax highlighting library (keep preview rendering lightweight).
- Do **not** broaden scope (“refactor approval system”); only touch what the prompt requires.
- Keep rendering responsive:
  - no sync IO in render
  - hard caps for quadratic diff algorithms
- Loop discipline:
  - run targeted tests first, then `bun run test` if needed
  - run review before committing using `AGENTS.md` -> `Review Profile (Single Source of Truth)`; fix all high/medium findings
