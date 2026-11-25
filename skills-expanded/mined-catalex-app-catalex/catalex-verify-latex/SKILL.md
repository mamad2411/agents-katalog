---
name: catalex-verify-latex
description: Verify and repair LaTeX source changes by compiling the resolved document root, fixing actionable diagnostics with bounded retries, and rendering representative PDF pages for visual inspection. Use for tasks that create, edit, diagnose, or claim completion of .tex, .bib, .sty, or related document-source changes. Do not use for read-only questions that make no source changes.
---

# Verify LaTeX

Use the app-provided MCP tools to close the edit → compile → diagnose → repair → render → inspect loop. The app manages the connection; do not install a separate server.

## Preserve the source of truth

- Read and edit project files through filesystem tools. Treat the saved LaTeX sources as authoritative.
- Never manipulate CodeMirror, the DOM, editor selection, cursor position, panes, or other UI state to change document content.
- Preserve the existing preamble, packages, bibliography setup, and document structure unless the task requires a targeted change.

## Run the verification loop

Use at most three compile attempts total: the initial compile plus no more than two repair-and-recompile cycles. Announce each attempt as `LaTeX verification attempt N/3` so progress and retries remain observable.

1. Read the relevant sources and make the smallest coherent edit.
2. Call `mcp__catalex__compile`. It compiles the current agent draft's resolved root using the app's compiler settings.
3. If compilation fails:
   - Read every returned diagnostic before editing.
   - Repair only actionable source problems supported by the diagnostics.
   - Recompile if an attempt remains.
   - Stop immediately for missing toolchains, inaccessible files, or diagnostics that do not support a safe repair.
4. If the third compile attempt fails, stop editing. Report retry exhaustion and the remaining diagnostics.
5. After compilation succeeds, call `mcp__catalex__render_page` for one to three representative pages. Prefer pages affected by the edit; otherwise inspect the first page and any page likely to expose the changed structure.
6. Inspect the returned images for clipping, overflow, overlap, missing content, broken references, placeholder citations, unexpected blank space, and visibly inconsistent typography.
7. If inspection finds an actionable source problem, repair it only when the three-attempt compile budget still permits another compile. Recompile, render the affected page again, and inspect the new image.

## Follow the bounded paths

- Successful first compile: compile → render representative pages → inspect → report verified.
- Actionable compile failure: compile → diagnose → repair → recompile, then render and inspect after success.
- Retry exhausted: stop after attempt 3/3, do not render a stale PDF, and report unresolved diagnostics.
- Visual problem: report what the rendered image shows; repair, recompile, and re-render only within the same three-attempt budget.
- Render failure: report that compilation succeeded but visual verification could not be completed.

## Report completion honestly

State all of the following in the final response:

- the compile result and number of attempts;
- the pages rendered and inspected, or why rendering was not completed;
- any remaining compiler or visual problems;
- whether verification is complete, partial, or failed.

Never claim a successful compile, rendered inspection, or full verification unless the corresponding tool call completed successfully in the current turn.
