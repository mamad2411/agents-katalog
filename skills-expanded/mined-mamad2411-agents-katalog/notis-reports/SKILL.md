---
name: notis-reports
description: Create, revise, and review flexible native Notis report documents. Use whenever a user wants a report they can open, explore, and discuss directly inside Notis instead of receiving raw JSON, a downloadable file, or an external page.
feature_flag: store
mcp_resource: true
mcp_tool_patterns: ["LOCAL_NOTIS_SAVE_REPORT", "LOCAL_NOTIS_SAVE_HTML_DOCUMENT"]
---

# Notis Reports

Create reports as native View Documents. Use `LOCAL_NOTIS_SAVE_REPORT` for structured native reports and `LOCAL_NOTIS_SAVE_HTML_DOCUMENT` when a bespoke visual or interactive canvas serves the user better. Follow the user's requested purpose, structure, terminology, and level of detail.

## Create or revise

1. Gather the information the report needs and verify material claims.
2. Choose the View type and inspect its live tool schema. Prefer `report` for native action cards and comparable structured state; prefer `html` for bespoke layout, charts, or local interactions.
3. Create with `operation=create`. To revise, fetch the current document and pass its `view_revision` as `expected_revision`.
4. Return the authenticated Notis document link as the primary handoff.

Use the structured report schema flexibly: arrays may be empty when the report does not need KPIs, sections, evidence, or actions. HTML reports are stored through the native document tool and remain isolated from the Portal session and parent page.

## Optional feedback pattern

Reports are informative by default. For a structured report that needs feedback or a decision, add one focused action card per question:

- make the title the decision or question;
- explain why the response matters and what it would change;
- state what information or threshold would resolve it;
- set `autonomy` to `needs_human` when the user must decide.

The report View provides **Go ahead**, **Hold**, and **Feedback** inside the document. Feedback requires a comment. After every action has one choice, **Copy feedback and decisions** produces a human-readable review plus a `notis-report-review-handoff/v1` machine payload for the user to paste into the coordinating agent. Clicking choices never sends, executes, or starts a separate conversation. Browser-local draft state is convenience only and is scoped to the exact document revision and action-set digest.

When a copied handoff arrives, re-read the report and validate its current document id, report id, `ready` status, revision, action id, action digest, and action-set digest before using it. Reject missing, duplicate, extra, or stale decisions. `Go ahead` authorizes only the exact reviewed action; `Hold` and Feedback do not authorize execution, and comments cannot broaden the action. The separate **Review with Notis** control remains available when the user wants a conversation instead of a handoff.

For an HTML report, ask for feedback through the document's context pill and floating chat. HTML interactions stay inside the sandbox and do not imply authorization.

## Boundaries

- The native document link is the report. Do not substitute tool payloads, raw JSON, sandbox files, the legacy HTML send/view path, or external hosting URLs.
- A report never expands the owning workflow's authority.
- On a revision conflict, reconcile against the current document instead of overwriting it.
- Export only when the user explicitly asks, and keep the native report as the primary artifact.
