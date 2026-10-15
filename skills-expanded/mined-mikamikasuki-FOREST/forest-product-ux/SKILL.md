---
name: forest-product-ux
description: Redesign FOREST navigation, user journeys, action placement, and workspace panels while preserving scientific capabilities. Use for product interaction changes, not research hypothesis analysis.
---

# FOREST product UX

FOREST organizes persistent research through a graph, real execution, human intervention, evidence, and an evolving manuscript. Design around the researcher's current task and object, with graph and manuscript retaining their identities outside any conversation.

Before changing navigation, read [the current entry map](references/navigation-map.md). For a full redesign, read [the task and parity rubric](references/task-rubric.md). Recheck the affected source at the working HEAD; the map is a starting point, not a promise that every requested feature exists.

## Establish the task

1. Trace the existing journey in the browser, including the API or local state effect of each action. Record its target entity, persistence, prerequisite, success state, and failure state.
2. Classify actions by frequency and selection context. Keep frequent actions directly visible, intermediate actions in a clear object menu or secondary view, and rare technical controls in Advanced.
3. Map every existing capability to a new entry before retiring the old entry. Preserve independently stored ideas, theory, nodes, runs, references, and files even when navigation groups them.

## Navigation and shell

Use five project destinations: **Workspace**, **Library**, **Experiments & Results**, **Paper**, and **Files**. Keep Settings at the bottom of the global sidebar. Workspace houses overview, goals, graph, ideas, hypotheses, theory, branches, progress, and intervention; results has Experiments / Runs / Data / Figures secondary views.

- Implement grouping through routes and contextual views; preserve old route compatibility and meaningful query state, selected entity, demo state, and browser history.
- Resolve run, branch, node, and document links against the correct project. Do not reuse an ID merely because it is a string.
- Distinguish unknown route, missing project/object, permission denial, authentication, and unavailable resource. Avoid a universal redirect that hides the failure.
- Build the project switcher from real projects: search, select, create, and return to all projects. Expose only additional operations actually supported.
- Cmd/Ctrl+K should find pages and real entities and offer executable commands whose availability matches the current context. Preserve confirmation for operations whose impact requires it.

## Working layout

Give the main research task the largest usable area. A compact shell can show project, actual status, attention, and the primary scoped run action. Prefer one active secondary surface: a manuscript panel, temporary inspector, or run drawer according to the task. Avoid squeezing the graph between several permanent inspectors.

- A live manuscript panel reads the same document and revision as the full editor. Keep its entire dirty draft session when hiding, expanding, or switching surfaces; shared server identity alone does not preserve edits. Determine the empty state from the actual paper read contract in the entry map.
- Allow hide/show, pin, resize, expand, and focus where they serve the task. Persist layout preferences; keyboard resizing must respect minimum/maximum sizes and offer reset.
- A compact status bar links to actual runs, decisions, connection state, and last update. Do not manufacture activity to fill an empty bar.
- At narrow widths, move auxiliary surfaces into accessible drawers or tabs. Preserve access to search, run actions, settings, and object tools at intermediate breakpoints too.

## Scientific interaction semantics

Keep annotation, research suggestion, formal instruction, human decision, graph mutation, and execution request distinct. Explain scope and consequence using supported contract fields. Do not offer a generic Send that obscures which persistent action will occur.

Node actions should expose edit, run, results, and evidence when supported. Single click selects, blank canvas clears, double click opens focus, and right click opens an actual contextual action menu. Escape closes the top temporary surface, then clears selection without a later effect reselecting a node. Preserve editor and terminal keyboard behavior.

Run labels identify scope: node, selection, branch, research controller, individual run, or project bulk control. Submit → accepted → running → finished is shown from actual server evidence, independently of scientific validation.

## Verify the improvement

For each major journey, measure clicks, context switches, and required user decisions before and after under the same starting state. Define what is counted; record observed counts instead of estimates. Frequent actions should not gain unnecessary steps.

Keep errors at the affected form or object, with recovery and retained drafts. Toasts can supplement durable feedback. Validate empty, loading, failure, running, and pending-decision states as well as populated pages.

Update the redesign's feature and API coverage records with actual source, new entry, test, and verification status. Use `forest-browser-testing` for acceptance, `forest-research-graph` for graph changes, and `forest-run-lifecycle` for execution/intervention changes.

Deliver functioning code and measured journeys when implementation is requested; a skill or design specification by itself is not product completion.
