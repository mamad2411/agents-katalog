---
name: mermaid-loop
description: Use when the user wants to draft, render, or critique an architecture / data-flow / pipeline diagram, or asks "what am I missing" about a process they described in text or a sketch. Renders Mermaid locally to terminal ASCII (and optionally SVG/PNG), then reviews the flow for missing error paths, unhandled states, and unstated assumptions. Everything runs offline — no diagram data leaves the machine.
license: MIT
compatibility: Requires Node.js 18+ and a one-time `npm install --ignore-scripts` inside the skill directory. Optional `@mermaid-js/mermaid-cli` on PATH for --png. No network access at runtime.
---

# Mermaid Loop

Turn a described process into a Mermaid diagram, render it locally, and tell the user what
their diagram is missing.

The rendering is a means, not the point. **The critique is the deliverable.** A diagram that
renders beautifully and omits every failure path is worse than useless — it looks finished.

## Privacy contract

Everything here is local. `beautiful-mermaid` is pure JS (elkjs + entities, zero DOM, no
network). `maid` is a local parser. `mmdc`, if used, drives a headless browser on this
machine. **Never** send diagram text to `mermaid.ink`, `kroki.io`'s public instance,
PlantUML's default server, or any hosted rendering service — that is the whole reason this
tooling exists. Do not suggest them, even as a fallback.

## Workflow

1. **Write** the Mermaid to a `.mmd` file. Ask before overwriting one the user already has.
2. **Render** it:

   ```bash
   node scripts/render.mjs <file.mmd>
   ```

   Path is relative to this skill's directory. If the dependencies are missing, run
   `npm install --ignore-scripts` there once.

   Add `--svg out.svg` for a vector file, `--png out.png` if `mmdc` is installed,
   `--theme <name>` (see `--themes`) to restyle, `--check` to report what is installed.

3. **Read the `#` header before the picture.** It lists every node with its shape and label,
   every edge, every subgraph, plus entry points and terminals — as mermaid itself parsed
   them. Diff that against what you meant to write; the terminals line in particular is
   where missing error paths surface. Exit code 1 means the diagram was rejected or the two
   parsers disagreed: fix it, do not work around it.

4. **Critique** using the checklist below. Report gaps as questions, not as edits — the user
   owns the diagram.

5. **Hand off** to their real editor when asked. draw.io imports Mermaid directly:
   Arrange → Insert → Advanced → Mermaid. It renders client-side, offline in the desktop
   app, and exports `.vsdx` for Visio.

## The checklist

Walk these in order against the rendered flow. Anything the diagram does not answer is a
finding.

**Failure and recovery**
- Every external call — what happens when it fails? Timeout, retry, give up?
- Retries: bounded? Backed off? Is the operation idempotent, or does a retry double-write?
- Partial failure mid-loop: does the run abort, skip the item, or poison the batch?
- If the final status write fails, how does anyone learn the run happened?

**State and consistency**
- What is the transaction boundary? Which writes can succeed while a later one fails?
- Is there a rollback, a compensating write, or is partial state simply accepted?
- Two runs overlapping — is that prevented, or is the outcome undefined?
- Any cached or derived value used to decide "has this changed": what invalidates it, beyond
  the obvious? A schema change, a formatting change, a version bump in whatever produced it?

**Data**
- Where does pagination or batching happen? What if the source is larger than expected?
- Rate limits on each external system — where does the flow throttle?
- Records present on one side but not the other: created, deleted, ignored?
- Deletes — does the flow detect them at all, or only ever add and update?

**The loop specifically**
- Serial or parallel? If parallel, what is the concurrency bound and do the writes conflict?
- Cost and time per iteration, times the expected iteration count — is that acceptable?
- Anything model-generated: is the raw output stored, or only the processed form? Can a bad
  generation be identified and re-run without re-running everything?

**Observability**
- What is logged per item versus per run, and where does it go?
- Can someone reconstruct what changed in a given run, after the fact?
- Is there a dry-run mode? A diagram with no dry-run path usually means there isn't one.

**Boundaries the diagram hides**
- Trust: which of these systems is authoritative when they disagree?
- Credentials: where do they come from, and does the diagram imply one identity or several?
- What triggers the run — schedule, manual, event? An unlabelled entry point hides this.

## Mermaid notes

- `subgraph NAME [Label] ... end` for loops and phases; nest freely, ASCII handles it.
- `A -->|label| B` for branch labels — always label the branches of a decision node.
- Shapes carry meaning: `[(cylinder)]` for a datastore, `{diamond}` for a decision,
  `([stadium])` for start/end, `[[subroutine]]` for a call out to another process.
- Node IDs are short and stable; labels carry the prose. The parse header prints IDs, so
  meaningful IDs make the diff step readable.

## How validation works

**Syntax is mermaid's own parser.** Not a hand-written linter — mermaid's grammar is the
authority on what mermaid.js and draw.io accept, its errors carry line and column, and
maintaining a second copy of someone else's grammar is a losing game. `jsdom` is a
dependency because mermaid sanitizes label text through DOMPurify even when only parsing.

**Parity is the one check this skill owns.** `beautiful-mermaid` draws the picture, and it
renders unusual input silently rather than failing, so it can read a diagram *differently*
from mermaid — which mermaid, by definition, cannot detect. `render.mjs` parses with both
and compares the edge lists. A mismatch is an error, because the picture would be missing
connections. Invisible links (`~~~`) are excluded: mermaid models them as edges,
`beautiful-mermaid` does not, and both are right.

The known real case is an edge continued across two lines:

```
A -->
B --> C
```

Legal Mermaid, read as two edges by mermaid and one by the renderer. Put it on one line.

Because the parity check leans on `mermaid.mermaidAPI`, a semi-internal surface, it
degrades to a warning if a mermaid upgrade moves it — a valid diagram never gets blocked by
our own plumbing breaking.

## Maintenance

```bash
cd <this skill's directory>
npm install --ignore-scripts     # always --ignore-scripts
npm audit                        # must stay at 0
```

Tests are not shipped with the skill — they live in the source repo
(`tests/mermaid-loop.test.mjs`, `npm test`).

**Hard rule: zero advisories.** Run `npm audit` before adding any dependency and do not add
it if the count is non-zero. `@probelabs/maid` was evaluated and rejected on exactly this
basis — 5 high advisories via `chevrotain` → an old `lodash-es`. (mermaid's tree contains
`lodash-es` too, at a patched 4.18.1. The rule is version-sensitive, not package-sensitive.)

`npm test` covers what this skill owns — parity, frontmatter stripping, every renderable
diagram type surviving the pipeline, and invalid input exiting 1. It deliberately does not
re-test Mermaid syntax; that is mermaid's suite, not ours.
