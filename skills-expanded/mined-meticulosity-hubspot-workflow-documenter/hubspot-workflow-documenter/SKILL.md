---
name: hubspot-workflow-documenter
description: Use when documenting or auditing a HubSpot portal's workflows, when asked what a portal's automation actually does, or when looking for broken automation such as duplicate enrolment, dead email references or unreachable steps. Read only.
---

# HubSpot Workflow Documenter

Reads a HubSpot portal's workflows and writes documentation for them: what each
one does in plain English, a Mermaid diagram of its logic, and a severity-ranked
list of what is broken.

**This skill only ever reads.** It never creates, edits or deletes anything in
the portal.

## Before you run it

The agency needs a HubSpot private app token in the client's portal. Point them
at `SETUP.md`, which lists the exact scopes and explains why none of them can be
read-only. Then:

```bash
export HUBSPOT_TOKEN='pat-na1-...'
PYTHONPATH=src python3 -m workflow_documenter --out output/portal.md
```

To show somebody the output before any access is granted:

```bash
PYTHONPATH=src python3 -m workflow_documenter --dry-run --out output/sample.md
```

Generated documents contain the client's workflow names and internal structure,
so they belong in `output/`, which is git-ignored.

That renders from bundled fixtures and opens no network connection.

If the client will not grant API access at all, export what you can and use
`--from-dir ./export`. Say plainly that a file-mode run is a thinner analysis.

## Reading the output

The document has four sections. **Findings** is the one that matters: it is
sorted worst first, where "worst" means most able to reach a real person right
now. A defect in a disabled workflow ranks below the same defect in a live one.

Lead with anything under **Critical**. Overlapping enrolment sits there because
two live workflows triggered by the same form catch the same contact twice,
which is the usual cause of duplicate emails and is invisible in the HubSpot UI.

## Things to tell the client honestly

- Webhook URLs are redacted by default because they are credentials. Only pass
  `--include-webhook-urls` if the document is going somewhere private.
- If a scope is missing the run still produces a document, with the unresolved
  names labelled. It does not fail.
- HubSpot has no read-only scope for workflows, so the token can technically
  write. This tool cannot: every call it makes is a GET, and `tests/test_no_writes.py`
  proves it mechanically.
