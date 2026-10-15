---
name: alder-export-business-graph
description: Export an Alder Business Design to deterministic Business Graph JSON using the bundled official exporter. Use for requests such as "この業務設計をAlderでJSON化して", "AlderのBusiness Graphを出して", or "Export this Alder Business Design as Business Graph JSON". Do not use for arbitrary Markdown conversion, design authoring, or semantic review.
license: MIT
---

# Export Alder Business Graph

Read [the bundled graph contract](references/business-graph.md) before export. Its profile and [the packaged exporter](scripts/export.py) are byte-identical artifacts from the revision in [provenance](references/provenance.json). Use this installed copy; no product-side Alder checkout, latest-guidance fetch, or manual authority-document selection is needed. Links in the copied authority refer to the original repository; the complete supported profile is bundled here.

1. Read the target project's `AGENTS.md`. Locate the requested Business Design at its explicit path, the project-declared path, or `docs/business-design/`. Resolve multiple plausible targets with a focused question. Record the source revision or working-tree state. Business Design remains the source of business meaning; graph export is optional.
2. Check local script execution and Python 3.12+ availability. The exporter uses only the standard library. If the host cannot execute it, report that concrete limitation and stop; do not manufacture graph JSON with an LLM, add an MCP service, or ask the user to clone Alder. Do not install a runtime without authorization.
3. Invoke the bundled tool, resolving `SKILL_DIR` to this installed skill directory and quoting paths:

   `python3 "$SKILL_DIR/scripts/export.py" "/path/to/business-design.md"`

   For requested file output, use `-o "/path/to/graph.json"` with an existing parent directory. Choose a new output file if no destination was given. Do not overwrite unrelated output or use shell redirection: redirecting to the source can truncate it before the tool runs. The CLI forbids source/output aliases and replaces an output atomically only after successful validation.
4. Treat exit 0 as successful structural projection; exit 2 means invalid input, arguments, graph or file access. Return relevant stderr diagnostics with the source location and useful next step. Do not silently rewrite an unsupported design to fit the profile, guess missing names/relations, or edit the generated JSON to bypass validation. Format corrections or business decisions need a separately requested design revision, followed by a fresh export.
5. Return the generated JSON or its requested location, source revision/state, actual plugin version, exporter source revision and digest. Obtain the plugin version from the installed `../../plugin.json`; distinguish unknown installation commit from a known pinned exporter revision. Keep provenance in the result explanation, not in extra graph fields. Explain that success checks structure only, not business correctness, completeness, agreement or approval. Procedure and How → Exception remain in Business Design and are not projected.

Write only the requested generated output. Do not create a maintained second specification, make export a normal review gate, or upload the graph to an external viewer without authorization. Feed proposed corrections back to Business Design. Authoring, design review, implementation review and traceability drift are separate workflows.
