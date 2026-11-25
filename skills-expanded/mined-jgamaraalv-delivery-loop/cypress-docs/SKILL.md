---
name: cypress-docs
description: Search and extract Cypress information from official documentation (docs.cypress.io, cypress.io); prefer LLM markdown under /llm/* and refuse unverified API or behavior claims.
---

# Cypress Documentation

Retrieve accurate, verifiable Cypress information by treating the **official docs as the source of
truth** — never memory.

## Core rules

- **Search before you claim.** Never assert "Cypress can / cannot…" from memory — search the docs
  first, retrying with alternate terminology before concluding a feature is missing.
- **Prefer the LLM-optimized docs.** On `docs.cypress.io`, fetch `/llms.txt`, then read the Markdown
  mirror under `/llm/*` — every page has one (e.g. `…/app/faq` → `…/llm/markdown/app/faq.md`). Fall
  back to the HTML page only if the `/llm` version is incomplete.
- **Primary sources only:** https://docs.cypress.io and https://www.cypress.io (plus `/changelog/`
  and the cypress.io blog for version/update questions).
- **Never invent.** If the docs can't verify a claim, say "I could not verify this in Cypress docs,"
  offer the closest documented alternative, and never guess an API, signature, or default. Prefer
  "unknown" over incorrect.
- **Be version-aware.** Use the version if given, else assume latest stable; when behavior differs by
  version, call it out explicitly.

## References

Read on demand (progressive disclosure):

- `references/search-strategy.md` — query-type → doc-section routing table, the `/llm/*` → standard →
  changelog → blog search flow, error-message routing, and `/llms.txt` auto-discovery · read when
  locating the right doc page.
- `references/extraction-rules.md` — how to extract commands / concepts / configuration, response
  style and confidence annotation, caching, safety rules, and a worked example · read when
  structuring an answer from a fetched page.
