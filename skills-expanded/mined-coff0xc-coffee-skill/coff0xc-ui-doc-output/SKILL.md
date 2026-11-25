---
name: coff0xc-ui-doc-output
description: "Use when the user requests UI/frontend/product surface/report/translation polish: dashboard/admin/SaaS, component/design system, responsive/mobile, accessibility/ARIA/contrast, loading/empty/error/hover/focus/keyboard states, browser smoke/screenshot/console cleanliness, anti-AI visual polish. Use office-doc-tools for formal Office files. Manual trigger: Use coff0xc-ui-doc-output."
---

# coff0xc-ui-doc-output

<!-- skill-id: cs-udo-c8e51b29 -->

## Quick Rules (read this first for everyday tasks)
> **[Scan the system first]** First look at existing routes/components/tokens/themes/icons/copy/tests/browser paths and reuse the project's design language.
> **[State gate]** UI must cover loading, empty, error, success, disabled, focus, hover, mobile, and long-text/empty-data states.
> **[Visual evidence]** Major UI changes need browser smoke, screenshots, or equivalent render checks, with console/overlap/responsive issues recorded.
> **[Hard boundary]** Confirm first for publishing websites, downloading external assets, uploading documents, customer/private data handling, and paid services.

Run ordinary UI/report/translation tasks through the fast path in this section; read references only for deep aesthetics, merging an external UI skill, quality eval, or release gates.

## Capability
Artifact-quality capability for UI, frontend experience, report expression, and technical translation delivery. It does more than polish words: interfaces, interaction states, and report narrative must be genuinely usable, readable, and verifiable.

For formal Office/PDF file deliverables — creating, editing, commenting on, or formula/render-validating PPTX, DOCX, PDF, Excel/XLSX/CSV — prefer `coff0xc-office-doc-tools`.

## What It Can Deliver
- Usable UI/component/page changes or design recommendations
- Desktop/mobile screenshots or browser smoke results
- Report structure, delivery copy, and layout recommendations
- Polished translation drafts, terminology consistency, and delivery notes

## What Input It Can Take
- Frontend repos, page screenshots, design drafts, component code
- Markdown, report drafts, translation text, screenshots, page copy
- User feedback, mobile issues, accessibility or layout problems

## Safe-Use Boundaries
- Local UI and document artifacts can be handled directly
- Formal PPTX/DOCX/PDF/XLSX/CSV file delivery goes to `coff0xc-office-doc-tools`
- Downloading external assets, uploading documents, publishing websites, and paid services must be confirmed first
- Content containing personal information or customer data needs its de-identification requirements confirmed first
- Only local, reversible, verifiable low-risk work by default; confirm first for anything involving production, credentials, payment, remote writes, deletion, publishing, or permission changes.

## Why You Can Trust It
- Layout work must be verified by rendering or screenshots
- UI covers loading/empty/error/success and similar states
- Translation does not change facts, numbers, commands, or paths

## Typical Usage
```text
Use coff0xc-ui-doc-output to optimize this dashboard and check mobile with screenshots.
Use coff0xc-ui-doc-output to translate and polish this Chinese report into an English delivery version.
Use coff0xc-ui-doc-output to polish the report narrative and UI copy for these findings.
```


## Core Gates
- For a clear UI/report/translation task, execute this skill directly; only cross-domain or uncertain tasks go to `coff0xc-skill-router` first.
- Before UI work, check existing components, tokens, themes, icons, style systems, screenshots, and available verification commands.
- External/friend/project-specific UI skills may only be abstracted into generic rules; do not keep personal names, machine paths, absolute taste bans, or default authorization statements.
- UI must not be a happy-path static shell: consider at least populated, empty, loading, error, disabled, hover/focus, long-content, and small-screen states.
- Avoid AI flavor: template heroes, piles of three-column cards, purple-blue neon, cards inside cards, meaningless bento, explaining features only with icons/caption text.
- Do not invent numbers in data displays: key totals, amounts, percentages, time ranges, units, and chart axes must come from trusted data/APIs/formulas or be marked as assumptions.
- Reports/translations preserve facts, numbers, code, commands, paths, citations, and uncertainty; formal PPTX/DOCX/PDF/XLSX/CSV delivery goes to `coff0xc-office-doc-tools`.

## Verification
- After UI code changes, start the local service when it can be started; give the local HTML path when it can be opened statically.
- Check at least one desktop and one mobile viewport; add narrow-screen/tablet widths for complex tools.
- Check console, resource loading, blank rendering, overlap, clipping, text overflow, button clickability, basic form paths, and focus states.
- Canvas/WebGL/Three.js must be checked for non-empty pixels, scene framing, and mobile/interaction visibility.
- If the browser or screenshots are unavailable, write "code changed but no visual acceptance done" at the end; do not say the UI is verified.

## Default Output
- Close with only done, verified, remaining, and next steps; give a path or location for any file/code/rule artifacts.
- Checks not actually run are marked unverified; security/architecture conclusions carry an evidence level.

## References
Do not read these files by default for ordinary tasks.

| Reference | When to read |
| --- | --- |
| `references/ui-generalized-rules.md` | Merging an external UI skill, deep aesthetics/frontend-engineering review, Figma/Playwright/screenshot quality gates, UI quality eval. |

## Output Contract
```markdown
Done:
- ...

Verified:
- ...

Remaining:
- ...

Next steps:
- ...
```
