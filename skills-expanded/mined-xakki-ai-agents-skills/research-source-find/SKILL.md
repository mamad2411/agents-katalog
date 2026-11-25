---
name: research-source-find
description: 'Research documented API or data-source contracts, cite evidence, and recover permitted alternative sources when a source is inaccessible. Use for source-grounded contract or comparison tasks. RU: найти документацию, источник недоступен.'
disable-model-invocation: true
---

# Documentation research and source recovery

Use when the task asks for a source-grounded contract or comparison from documentation, or when a requested source cannot be reached. Identify the question, source classes, date, permitted inputs and requested output before retrieval. When scope is documentation-only, do not fetch actual records, feed entries, samples or live APIs; a documented example is not proof of runtime compatibility.

Find authoritative current documentation for the relevant service and version. Search snippets help discover sources but do not establish detailed claims; read the actual page or specification when available. Record direct citations for documented facts, version or date, explicit limits and unanswered questions. Separate documented behavior, inference and live verification, and distinguish access terms and authentication from implied permission to use the data.

For API contracts compare relevant endpoints, methods, authentication, request/response shapes, pagination, errors and streaming only where sources support them. For source-landscape decisions describe population, identifiers, geography, time, access and limitations needed by the actual question. Do not fill gaps with invented endpoints, values or a blanket recommendation. A proposed source, working endpoint or accepted research design does not authorize publication, processing real records or sending messages. For edits to existing API documentation use `api-docs-sync`.

## When a source is unavailable

Establish whether the failure is transient, rate-limited, access-controlled or a missing permission. Do not repeat the same failure without a new diagnostic reason, defeat an access or security control, or infer authorization to access restricted content. Look for permitted official documentation, public excerpts, author-provided copies, alternative primary sources or archives, using the available retrieval interface and respecting access conditions. Verify the actual content and provenance rather than treating an HTTP success or generic landing page as the requested source. Label archived material with its snapshot date and never present it as current; cite the actual supporting source and disclose a missing, stale or partial one. Third-party rendering and archival services may receive the requested URL, so use them only within the task's privacy and authorization boundaries.
