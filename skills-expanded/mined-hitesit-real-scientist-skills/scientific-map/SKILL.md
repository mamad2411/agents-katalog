---
name: scientific-map
description: Build or refresh the project’s offline HTML scientific map from study and probe records. Use on request at any study stage or during promotion, with one experiment tab per study.
license: MIT
---

# Scientific map

Build or refresh one project-root `scientific-map.html`. Each in-scope study gets a tab with one connected flow. `/scientific-map [study]` selects the initial tab, not the set of tabs. `/promote` invokes this skill after updating its records and selects the study it just promoted. Standalone use reads records and writes only the map and its approved build files. It does not run experiments, promote or move evidence, or authorize Git actions. The map is separate from study dashboards.

## 1. Read the records

Read `lab-notebook` and `.science/SETUP.md` for locations, presentation voice and the existing runtime. Identify in-scope studies by their records under `.science/<study>/`, including studies with only a question or probes. Keep explicitly excluded studies out of the HTML. Use `STUDY.md` for the starting question, `NOTEBOOK.md` for current state, findings and Ideas, current notebook-linked probe READMEs for methods or results, and cycle READMEs/manifests for dispositions, reusable homes and checkpoints. Use recorded probe directories if a notebook is absent; identify missing questions, states or links as gaps. No promotion cycle is required.

Done when every included study and its recorded probes, ideas and cycles are accounted for, and conflicting or missing records are identified without guessing.

## 2. Assemble the flow

Use a question card, one card per probe, and cards for recorded ideas and cycles. Keep findings, limits, revisions, reusable components and complex substeps in their card details. Keep dropped, inconclusive, superseded and open work visible. Separate scientific state and outcome from physical disposition. A missing record is a gap, not evidence of removal or a verdict. Mark unexecuted ideas as proposals and link them to their notebook entries.

Draw an arrow from a source to its documented consumer, control recipient, replacement, proposal or cycle. Group any component without a documented connection to the question with a clearly labeled **Study membership** link. Membership is not scientific evidence. Show a source link at its current path. Use readable short labels and preserve scientific terms, qualifiers, units and verbatim quotations.
Read a cycle's manifest as recorded rather than assuming one set of field names. Use the current notebook href for a moved probe. When a frozen README's relative link points to its old home, match the recorded probe ID to that current href. Keep `[inference]` on any reading that carries it.

Done when each tab’s scope, findings and arrows match its records, and every included component is reachable from the question without inventing a dependency.

## 3. Render and check

Read [assets/example.json](assets/example.json) for the shape and render with [assets/map.html](assets/map.html). The object contains `studies` and an optional `activeStudy` ID. Each study has `id`, `title`, `nodes`, `edges` and optional `links`. Node IDs are unique within a study; node kinds are `question`, `probe`, `idea` and `cycle`, with optional `state`, `details` and `links`. Edges reference IDs in the same tab; kinds are `membership`, `dependency`, `control`, `supersedes`, `proposed` and `promotion`, with an optional `label`. In `supersedes`, the arrow runs from the earlier record to its replacement.

Reuse or write a small build command in the project's existing tools. Read the authoritative records on each build; a generated graph is a derivative, not a second notebook. Serialize the graph as JSON, escape `<` as `\u003c`, and replace the template's single `__SCIENTIFIC_MAP_DATA__` marker once. Link to verified local files relative to the output. A missing target can be shown in a detail, not as a broken link. The resulting HTML embeds its styles, script and data. It needs only a browser: no server, external renderer, packages, remote assets or network. Use the existing approved map path and approved project-local build homes when available. If a different artifact already occupies the output path, obtain approval before replacing it.

Open the actual HTML offline with `file://` and inspect desktop and narrow mobile. Use headless verification unless the user requests a visible preview. Compare tab, card and typed-edge coverage to the sources; open a complex probe, an unexecuted idea and a moved record where present. Verify tab switching, controls, readable detail and all emitted local links. Rebuild in isolation from the recorded command; exercise the early-study and mixed-cycle forms as applicable. Record sources, build command, verification evidence and limits in the agreed homes; during promotion, add map evidence to the cycle record.

Done when the map renders and the recorded checks pass, or the report names each unresolved check. Return the HTML path, tabs, source gaps and verification scope.
