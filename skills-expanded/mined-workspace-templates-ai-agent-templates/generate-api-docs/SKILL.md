---
name: generate-api-docs
description: Builds API reference pages from your source code in the docs format and folder your project already uses.
disable-model-invocation: true
---

Generate API reference documentation for: $ARGUMENTS (folder, module or route file; whole public API if empty).

1. Find the existing docs format first: look in docs/, a docs site config (mkdocs.yml, docusaurus, typedoc, sphinx), or an openapi file. Match its folder, front matter, heading levels and page layout. If nothing exists, use one Markdown page per module.
2. Enumerate the public surface. For web services: every route with method, path, auth requirement, path and query parameters, request body and response shapes. For libraries: exported functions and types with signatures.
3. Take descriptions from existing doc comments. Where there are none, write a plain description from the code and mark it `(inferred)`.
4. Document errors: status codes or exceptions and when each occurs, read from the handler code.
5. Include one runnable example per entry, such as a curl command or a short code call, using realistic values.
6. Compare with the pages already there. Update changed entries and list entries that no longer exist in code; do not delete them.

Show a summary of pages created and updated and the list of inferred items, then ask before writing files.
