---
name: anti-ai-audit
description: Audit frontend UI and docs for AI slop, anti-patterns, and generic generated design. Use when the user asks for an anti-AI audit, a slop check, a design review, or a doc quality pass. Read the local references in `references/` before judging anything.
---

# Anti-AI Audit (/anti-ai-audit)

Audit UI and docs for anti-AI patterns, generic template slop, and copy that feels generated.

## 1. Target discovery

1. If the user gives a path, scan that target.
2. Otherwise scan likely UI/doc roots: `src/`, `ui/`, `components/`, `pages/`, `styles/`, `*.css`, `docs/`, `README.md`, `AGENTS.md`.
3. If the scan is broad, show the candidate files and ask for confirmation before auditing.

## 2. Audit rules

Read + apply + find things mentioned in these files from `references/`:

- `references/hallmark-slop-test.md`
- `references/hallmark-anti-patterns.md`
- `references/design-taste-frontend-anti-slop.md`
- `references/impeccable-audit.md`
- `references/humanise-text-overused-ai-patterns.md`


## 3. Output path

- If `docs/` exists, write to `docs/anti_ai_pattern_findings.md`.
- If there is no `docs/` folder, ask before creating a root-level output file.

## 4. Report format

Use this exact structure:

```markdown
# Anti-AI Pattern Findings

Files scanned: <list>

## 1. Hallmark Audit
- [critical] <Pattern> — <file>:<line>
  - Why: <why it reads as AI-generated>
  - Fix: <actionable fix>
  - Safety: <CSS-only / zero risk / etc.>
- [major] <Pattern> — <file>:<line>
  - Why: <why>
  - Fix: <actionable fix>

Summary — N critical · M major · K minor
Verdict — <ships as slop | reads as AI-generated | close, fix minors>

## 2. Design-Taste-Frontend Audit
- **<Rule>**: <Finding, line ref>

## 3. Impeccable Critique & Layout Structure
- **Heuristic Score**: <Score>
- **Action**: <short guidance>
  > ⚠️ **EXTRA CAREFUL (POTENTIAL FUNCTIONAL RISK):** <state/event/bubbling/navigation/streaming warning>

## 4. Humanise-Text Review
- **AI Pattern**: <phrase> (<file>:<line>)
  - Fix: <clean replacement>

## 5. Implementation Agent Prompt
<ready prompt for the fix-up agent>
```

## 5. Risk rule

If the fix touches forms, modals, stream UIs, icons, event bubbling, or state logic, add the ⚠️ risk tag and be explicit about the risk.


