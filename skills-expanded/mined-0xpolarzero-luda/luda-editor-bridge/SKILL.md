---
name: luda-editor-bridge
description: Read and edit supported ProseMirror documents using the separately installed Luda Editor Bridge MCP tools. Use only for applications whose developer registered the application bridge; ordinary websites and general desktop tasks use core Luda instead.
---

# Luda Editor Bridge

This optional add-on verifies text, paragraph/hard-break structure, selections and unaffected bold/italic marks in cooperating ProseMirror editors. It has its own installation, `editor_*` tools, temporary browser and lifetime. Installing core Luda does not install this add-on. Installing this add-on does not register arbitrary websites.

## Readiness and first use

1. Confirm `editor_*` tools are available. If missing, use the add-on installation instructions; do not send its options to `desktop_type`. Core and add-on server/window/element IDs are not interchangeable.
2. `editor_doctor` checks Linux/X11, browser and session prerequisites. It cannot confirm app registration before opening the app. Chromium requires an explicit executable and its real sandbox; do not silently download or disable sandboxing.
3. `editor_open(url, lifetime="temporary_session")` opens a fresh profile. Explain or honor this lifetime when choosing the workflow: **disconnect, process exit or `editor_close` destroys browser/profile and unsaved contents**. Existing profiles, frames, multiple pages and persistent sessions are unsupported.
4. Activate the returned `window_id`, then `editor_inspect(window_id)`. Read `editor_bridge`, `text_fields`, each `supported` flag, `unsupported_reason`, `supported_line_breaks` and `selection_scope`. Filters may hide connected editors: retry inspection without filters before diagnosing missing registration.
5. An empty unfiltered `text_fields` list needs application-developer setup. Do not inject the bridge, modify the site, or claim installation alone makes it compatible. Unsupported nodes/marks require a supported document or another user-approved workflow; do not flatten formatting to force support.

## Normal editing loop

Read the intended `text_fields` element with `editor_read`; confirm text, model and selection before modifying it. IDs expire after 60 seconds and become stale after navigation, replacement or re-registration; re-inspect instead of inventing IDs.

- `editor_focus(element_id)` establishes exact focus. `editor_select(element_id,start_offset,end_offset)` uses **Unicode code points**, not bytes, UTF-16 units or visual columns. Equal offsets place a caret. Read back if the user's requested range is ambiguous.
- `editor_type(element_id,text,mode="insert")` replaces the current selection; **native transport supports only append at end** for insertion. `mode="replace"` replaces the entire document, including its old formatting. Do not choose replacement merely because insertion needs a different transport.
- For an interior selected range, explicitly choose `transport="clipboard"`. It checks exact text and unaffected marks. CLIPBOARD ends as the last nonempty inserted segment; PRIMARY is unchanged. Empty text deletes a selected range without publishing clipboard contents; empty text at a collapsed selection is a no-op.
- Any LF requires explicit `line_breaks="paragraph"`, or `"hard_break"` only when the descriptor declares it. Both read as LF in logical text; the model and `line_break_boundaries` distinguish them. Never substitute one for the other.
- Read the result and, when needed, `editor_read` again. New text formatting follows the application; verification preserves unaffected old formatting and does not promise inherited bold on a new paragraph. Whole replacement deliberately replaces old formatting.

Do not assume keyboard shortcuts such as Ctrl+B are bound by the application. Use observed toolbar actions or documented app-specific bindings only when formatting changes are part of the user's request. Native toolbar nodes from `editor_inspect` support `editor_invoke`; they are not document handles for `editor_type`. `editor_activate`, `editor_press_keys`, `editor_scroll` and `editor_observe` support the add-on's browser workflow; mutations to another window are refused. Screenshots include the desktop context.

**Editing verification does not confirm saving.** Save through the application's observed controls, then verify its saved state separately. Do this before closing or ending a temporary session. Never close an unsaved document solely to get fresh element IDs.

## Failure and interruption

`effect="none"` means no content action occurred at that failed boundary; a clipboard publication can be reported separately. `dispatched` does not prove the app accepted input. `verified` establishes the stated observed postcondition, not future stability or saving. `uncertain` may mean partial content remains.

On mismatch, focus loss, stale target, timeout or cancellation: stop, inspect/read current state, and use `editor_status` if the final outcome is missing. Do not replay the original text, switch transports automatically, or derive a retry offset from progress counts. `editor_report` provides sanitized diagnostics without document text.

Composition must be known inactive. For `IME_COMPOSITION_ACTIVE` or `COMPOSITION_UNKNOWN`, preserve pending input; do not send Escape, fake events or alter the document to bypass the guard. The user/application must resolve composition before a fresh inspection. Focus/model checks are not atomic with input; another actor can still race delivery.

For precise examples, support limits, app setup, paragraph boundaries, partial receipts and recovery, read [editing reference](references/editing.md) when relevant.
