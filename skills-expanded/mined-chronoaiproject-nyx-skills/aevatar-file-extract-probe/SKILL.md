---
name: aevatar-file-extract-probe
version: "1.0"
description: Verify the read-file path end to end — the user sends a PDF/DOCX/txt/json/md/csv plus the trigger, a workflow document_extract step pulls its text, and the run output proves the file was read. Run it before any file-dependent workflow (invoice, resume screening, reimbursement intake). As of 2026-06-12 this probe is expected to surface a known gap; the result tells you whether read-file is wired yet.
metadata:
  category: plain
  tag:
    - aevatar
    - s-capability
    - probe
    - read-file
    - document-extract
    - workflow
    - diagnostics
---

# Aevatar File Extract Probe

Use this to confirm an attached file actually reaches a workflow `document_extract` step and its
text comes back. Reading files works on the WORKFLOW path only (the `document_extract` tool lives
in the workflow engine, not the chat tool surface). So this probe drives a workflow.

**You (the agent) report the run output honestly.** As of 2026-06-12 there is a known boundary
(below); a FAIL here is a real, useful finding — it tells you the read-file chain isn't wired yet,
not that you did something wrong. Never invent file content.

## Prerequisite (one-time)

The probe workflow `probe_document_extract` must be registered in this chat's scope (ships in the
repo's `workflows/` directory; submit it to your scope if `/workflow run` reports it missing).

## How to run it

1. **Tell the user to send the file and the trigger in ONE message** (attach a small PDF / DOCX /
   .txt / .json / .md / .csv, then type the command, send together):
   `/workflow run probe_document_extract`
   (alias `/run-workflow probe_document_extract`). Image OCR is NOT supported — use a text-bearing
   document.

2. **Read the run output.** The workflow returns JSON: `{"extracted": true|false, "preview":
   "<first 200 chars>", "note": "<verbatim error if extraction failed>"}`.

3. **Verdict:**
   - `extracted: true` + a preview that matches the file the user sent → `READ-FILE OK` — the
     chat-file → document_extract chain works; file-dependent workflows can run.
   - `extracted: false` with a fileRef / argument error in `note` → `READ-FILE BLOCKED (known gap)`.
     The chat file's reference reaches the run on the InputFileRefs channel, but the workflow
     tool_call layer does not yet hand it to `document_extract` (no fileRef injection / no
     `input_file_refs` expression). Quote the `note` verbatim — that error is the confirmation.
   - `unsupported_media_type` → you sent a type document_extract can't read (e.g. an image); resend
     a text document.
   - `未找到 workflow` / `暂未绑定可运行的 actor` → the probe workflow isn't registered/bound; setup step.

## Output

One block: did the run start, what was `extracted`, the preview or the verbatim `note`, and the
verdict above. If BLOCKED, state plainly that file-dependent workflows (invoice / resume /
reimbursement) cannot run until the chat-file → document_extract handoff is wired.

## Guardrails

- Read-only: this probe only extracts text; it never writes, submits, or forwards anything.
- A `extracted: false` result is honest and valuable — report it as a finding, do not retry endlessly
  or pretend the file was read.
- Never ask the user for tokens — your NyxID-brokered tools handle all credentials.
