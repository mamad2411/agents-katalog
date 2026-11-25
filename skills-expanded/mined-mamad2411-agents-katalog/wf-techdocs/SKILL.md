---
name: wf-techdocs
description: Generate the missing-only Backstage catalog and TechDocs baseline with the wf_techdocs_baseline MCP tool (CLI fallback wf techdocs-baseline), then have the technical-writer specialist author the published pages with Guru, architecture, security, qa, and docs-contract collaboration (Refresh TechDocs / Author TechDocs). An explicit read-only request selects the review-only branch, which runs the wf_techdocs_audit publication audit (CLI fallback wf techdocs-audit) and returns findings and proposed edits without writing. Renders once docs/prompts/refresh-techdocs.prompt.md exists (every target after seed-100 reconciliation).
---

# Refresh TechDocs (Wavefoundry skill)

This skill is a thin pointer: the workflow lives in `docs/prompts/refresh-techdocs.prompt.md`. Read that document and follow it; do not improvise the steps from this summary.

- Step 1 runs the baseline, `wf_techdocs_baseline(mode='dry_run')` then `mode='run'` over MCP or the `wf techdocs-baseline` CLI without MCP (missing-only; existing files are preserved byte-for-byte; a mixed trio yields one warning). Steps 2 and 3 author and validate the published pages, and Step 3 runs the `wf_techdocs_audit` publication audit. On an explicit read-only request, use the prompt's read-only procedure instead: it runs the audit only, never the baseline, and writes nothing.
- The workflow writes only inside the `mkdocs.yml` publication boundary; the one exception is removing the generated-by line from the trio's root members when the writer takes ownership of the trio.
- Registration with a Backstage instance and publication of the site stay operator/Backstage-owned; the prompt's follow-up checklist lists what remains.
