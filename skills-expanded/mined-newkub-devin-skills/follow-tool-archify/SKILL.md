---
name: follow-tool-archify
description: Archify — agent skill turning ideas/codebases into interactive HTML diagrams (typed JSON IR)
argument-hint: "[subject-to-diagram]"
related:
  - create-mermaid-diagram
  - draw-excalidraw
  - report-architecture-diagram
  - follow-my-techstack
  - deep-analyze
---

## Goal

Generate communication-grade interactive diagrams with Archify (MIT, `tt-a1i/archify`, v3.x) — the agent authors typed JSON IR, Archify validates it and renders a single self-contained HTML artifact with focus/path-tracing/reach exploration and PNG/video/share-card export

## Scope

Use when a diagram must be explored, shared, or presented — not when inline markdown diagrams suffice

- 10 diagram types: architecture, workflow, sequence, data flow, lifecycle, ERD, class, tree, timeline, waterfall (+ architecture-delta compare)
- Inline doc diagrams stay Mermaid (`/create-mermaid-diagram`); freeform whiteboards stay `/draw-excalidraw`/`/draw-tldraw`
- Archify is not a drawing editor or a Mermaid theme — it turns technical intent into one shareable HTML artifact

## Execute

### 1. Install The Skill

> Goal: get the agent skill + zero-dependency CLI

1. `npx skills add tt-a1i/archify -g` (installs into the agent's skills dir; `npx skills use tt-a1i/archify@archify --agent codex` to try without installing)
2. CLI check: `node archify/bin/archify.mjs doctor`
3. Optional: set `ARCHIFY_UPDATE_CHECK_DISABLED=1` to disable its release-reminder network call

### 2. Pick The Type

> Goal: one prompt, right diagram

1. Unsure → ask the CLI: `node archify/bin/archify.mjs guide "Show an API request with Redis cache miss"`
2. Feed the prompt the type's required content: architecture → scope, core components (8–12), primary path, trust boundaries; ERD → every table/column/key/cardinality; timeline → timestamps with timezone + observed-vs-illustrative flag; waterfall → spans, start times, nesting, measured-vs-illustrative
3. Source-backed map of a real repo: run `/deep-analyze` first, then ask the agent to trace files and pin evidence to one public commit (`SRC` nodes open file:line)

### 3. Generate, Validate, Deliver

> Goal: only verified artifacts replace last-good output

1. The agent writes the typed JSON IR, then `archify.mjs validate <type> <file>.json --quality showcase --json` — apply only `diagnostics[].subject.supportedFixes` (max two correction rounds)
2. Iterate visually with `preview` (loopback-only desktop watch loop, last-good kept through failures) or finish with `deliver <type> <in>.json <out>.html --quality showcase --open --json`
3. Review the rendered HTML yourself — visual review is separate from the validation gates

### 4. Share And Compare

> Goal: the artifact does the explaining

1. Output is one standalone HTML — send the file; viewers need no install; stable links restore `#focus=`, `#route=`, `#reach=` state
2. Export: PNG to clipboard, static/motion downloads, 1200×630 route/reach share cards
3. Design/PR review: `archify.mjs compare architecture base.json head.json out.html --json` renders validated Before/Delta/After snapshots — treat impact claims as authored, never inferred

## Rules

### 1. Truthful Interaction Only

- Nodes/edges come from the authored JSON; focus/reach/routes reuse authored topology — never present illustrative timings or inferred runtime impact as measured

### 2. Validate Before Delivering

- Never ship unvalidated IR; schema/layout/route/label-clearance gates are what make the artifact trustworthy — repairs stay within the skill's two correction rounds, then re-prompt instead of forcing fixes

### 3. Right Tool Boundaries

- Chat/doc-embedded diagram → Mermaid; quick sketch → excalidraw/tldraw; presentation/exploration/sharing → Archify

## Expected Outcome

- One self-contained interactive HTML per subject, validation-gated and shareable
- Source-backed diagrams pinned to a commit when repo evidence was requested
- Iteration in chat ("highlight the rollback path") without regenerating from scratch
