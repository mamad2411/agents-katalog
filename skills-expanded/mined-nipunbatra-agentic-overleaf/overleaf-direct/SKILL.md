---
name: overleaf-direct
description: Edit Overleaf projects directly in the user's logged-in Chromium browser without Git, downloads, or local project synchronization. Use for reading or changing LaTeX/BibTeX files, uploading paper figures or assets, switching project files, applying exact text replacements, recompiling, checking PDF output and layout, or creating an isolated Overleaf playground for safe testing.
---

# Overleaf Direct

Use Overleaf as the source of truth. Prefer page-level browser control and use
Computer Use only as a fallback. Never open Overleaf's Git integration or GitHub
Sync, generate an Overleaf Git token, or clone a paper project.

## Fast path

1. Read the installed browser-control skill before browser actions.
2. Connect to the Chromium browser containing the logged-in Overleaf session.
3. Name the browser session.
4. Find the target Overleaf URL from the user's open tabs.
5. Prefer an agent-owned duplicate tab at that URL. This avoids disturbing the user's active cursor, selection, and tab.
6. Take one DOM snapshot and confirm exactly one `textbox` named `Source Editor editing`.
7. Resolve and import `scripts/overleaf-direct.mjs` from this skill directory.

Reuse the helper module for full-file reads, conflict-checked writes, exact replacements, file switching, and compilation.

```js
var overleafDirect = await import("<absolute-skill-path>/scripts/overleaf-direct.mjs");
var state = await overleafDirect.inspect(overleafTab);
var baseline = await overleafDirect.readCurrentFile(overleafTab);
var result = await overleafDirect.replaceExact(
  overleafTab,
  "old unique text",
  "new text",
  { expectedSource: baseline }
);
var compile = await overleafDirect.recompileAndVerify(overleafTab, {
  mustContain: ["expected PDF text"]
});
```

Use `inspect` instead of printing repeated full DOM or accessibility snapshots.
It reduces the live editor to a compact project, file, compile, and log contract.

## Safety rules

- For setup, experiments, benchmarks, or uncertain selectors, create a separate blank project named `Agentic Overleaf Playground`. Do not experiment in a real paper.
- Before every write, compare the live source with the source used to prepare the edit. Abort on a mismatch.
- Require the old text to occur exactly once for an exact replacement. Ask for more context when it is absent or repeated.
- After writing, read the complete source back and require an exact byte-for-byte match.
- Recompile after a substantive edit and verify a specific phrase in the PDF when possible.
- Preserve and restore the browser clipboard. Collapse the editor selection after reads.
- Treat a clipboard-restoration error after a write as a partial failure: report
  whether the source was nevertheless verified, then let the user know the
  clipboard could not be restored.
- Keep the user's original Overleaf tab open. Close agent-created duplicate tabs when the task is complete unless the user wants the playground or result left open.
- Do not change project sharing, ownership, integrations, or account settings unless explicitly requested.

## Reading and editing

Use a full-file clipboard round trip because CodeMirror virtualizes off-screen lines in the DOM. A DOM snapshot alone only exposes the visible portion of the file.

For a long edit:

1. Read the complete source.
2. Build the revised source in memory.
3. Re-read immediately before writing and compare with the baseline.
4. Paste the complete revised source in one operation.
5. Read back and compare exactly.

For a small edit, use `replaceExact`; it follows the same compare-and-swap workflow and avoids positional cursor operations.

## Files and compilation

- Use `listVisibleFiles` and `openFile` for top-level files exposed in the file tree.
- Expand a folder through normal browser locators before opening a nested file.
- Use `recompileAndVerify` after edits. Treat a changed PDF build URL plus expected PDF text as the strongest success signal.
- PDF text verification normalizes whitespace by default so phrases split
  across rendered lines still match. Use `textMatch: "exact"` only when
  whitespace itself matters.
- If compilation fails, inspect Overleaf's log panel and report the first actionable LaTeX error with its file and line.

## Papers, figures, and comments

For non-destructive suggestion macros, new binary assets, graphical abstracts,
long equations, tables, or submission-layout work, read
[references/paper-editing.md](references/paper-editing.md). It defines the
additional intent, upload, compiler, caption, and visual checks learned from
full-paper editing.

## Fallback

If page-level browser control is unavailable, read [references/cua-fallback.md](references/cua-fallback.md) and use the Computer Use path. Do not silently switch to Git or project downloads.

For Claude-compatible behavior and tool mapping, read [references/claude.md](references/claude.md).

For the validated selector and state contract, read
[references/overleaf-dom-contract.md](references/overleaf-dom-contract.md).
