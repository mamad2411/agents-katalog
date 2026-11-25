---
name: atomize
description: Ingest existing documents (markdown, plain text, Word .docx, PDF, interview transcripts, image screenshots) into typed company-brain nodes with provenance. Each ingested document lands as an immutable source node; extracted content becomes derived typed nodes linked via derived_from edges. Uses `cb extract` for binary documents; uses Claude's native vision for image screenshots; reads markdown and plain text directly. Recognizes known skill-output structures (competitor-profiling, customer-research, write-spec, etc.) and routes content accordingly.
---

# atomize

This skill ingests *existing* documents into the vault. Where the `intake` skill turns conversation into nodes, `atomize` turns files into nodes.

The pattern is the same: every ingested document gets one immutable `source` node holding the raw / extracted content, and the typed nodes derived from it carry `derived_from` edges back to the source. The source is the audit trail; the derived nodes are the productized knowledge.

## Before any input format

1. **Confirm the vault path.** Default: current working directory. Reject if no `_system/PROFILE.md` is present.
2. **Load the active schema.** Run `cb describe-profile --path <vault>` to know which node types are active and what fields they require.
3. **For each node type you're about to write**, run `cb describe-node <type>` so you don't miss required fields.
4. **Confirm the user's handle** for `verified_by`.

Universal node-writing rules and edge-writing rules are documented in the `intake` skill (`skills/intake/SKILL.md`). They apply here too.

## Universal source-node convention

Every atomize session starts by writing one immutable `source` node:

```yaml
---
id: source-<source-kind>-<short-slug>-<YYYY-MM-DD>
title: "<Original document title>"
type: source
namespace: <appropriate; e.g. competitive, regulatory-references, customer-research>
summary: "One line about what this document contributes to the graph."
auto_inject: false
applicable_when: null
confidence: 0.85
verified_at: <today>
verified_by: <handle>
staleness_signal: <a concrete trigger; null is OK for frozen historical docs>
tags: [atomized]
source_kind: <one of the 14 registered values — see below>
edges: []
related: []
source_url: <if applicable>
controlled_document: false
---

# <Original document title>

## Summary

<1-2 sentences explaining what this source contributes.>

## Original content

<For text/markdown: paste verbatim.>
<For Word/PDF: paste the extracted text from `cb extract`.>
<For image: paste the vision-extracted text and reference the image file in `_attachments/`.>
```

`source_kind` must be one of: `customer-interview`, `market-data`, `citation`, `founder-vision`, `domain-expertise`, `strategic-thesis`, `internal-data`, `prior-internal-doc`, `skill-output`, `press-release`, `web-snapshot`, `web-snapshot-network`, `fda-510k-summary`, `regulatory-filing`.

Pick the most specific value. When in doubt: a pasted internal document = `prior-internal-doc`; an external article = `citation`; an interview transcript = `customer-interview`.

## Input formats

### Markdown / plain text

Read directly. No `cb extract` needed.

```bash
# (just read the file with your tools)
```

Flow:
1. Read the file end-to-end.
2. Write the source node with the verbatim content in the body.
3. Identify distinct knowledge units (apply the same boundaries as the `intake vision` sub-mode — pillar / decision / pattern / hypothesis / fact / etc.).
4. Propose them as a batched table. Review loop with the user.
5. Write accepted derivations with `derived_from` edges back to the source.
6. Run `cb validate --path <vault>`.

### Word documents (.docx)

```bash
cb extract <file.docx>
```

This emits the document's text (paragraphs + simple tables) to stdout. Read it as the source-node body.

For an **existing PID** (Project Initiation Document) the user is ingesting, route extracted content like this:

- **Project purpose / scope statements** → candidate `pillar` or `decision` nodes (depending on whether they're durable principles or specific choices).
- **Stakeholder lists** → `stakeholder` nodes.
- **Requirement-shaped statements** → `requirement` nodes with appropriate `requirement_class`:
  - "The market needs ..." → `market`
  - "The user must be able to ..." → `user`
  - "The system shall ..." → `system`
  - "The software shall ..." → `software`
  - "The hardware shall ..." → `hardware`
- **Risk language** → `risk-insight` nodes (medical-device profile). Remind the user this is planning, not a controlled risk record.
- **Project goals / success criteria** → `decision` nodes with explicit rules-out.
- **Milestones / timeline** → typically a `note` until the v0.4.0 maintain skill handles them more structurally.

For a **messy product launch outline**, lean heavier on the user to disambiguate. Surface ambiguities like "this looks like either a feature spec or a pillar" and ask.

### PDF

```bash
cb extract <file.pdf>
```

Emits page-by-page text + table content with `--- page N ---` and `--- page N table M ---` markers.

For an **FDA 510(k) summary PDF**, recognize the structure and extract:

- The clearance K-number (usually at the top or in the header).
- Applicant company.
- Device name.
- Product codes.
- The **Indications for Use** statement (look for that exact section heading or "Indications for use:" prefix).
- Predicate device citations (look for "predicate device" or "K###### (predicate)" patterns).

Then create:

- One `source` node with `source_kind: fda-510k-summary`.
- One `regulatory-clearance` node with all the structured fields populated.
- One `indication-for-use` node with `population`, `condition`, `intervention`, `setting` derived from the IFU statement. Link `belongs_to_product` to a product node (creating one if necessary, with the user's confirmation).
- For each predicate cited, add a `preceded_by` edge on the new clearance node. If the predicate isn't yet a node in the vault, prompt the user to either capture it via the `intake competitor-clearance` sub-mode or leave the edge pointing at an id that doesn't yet resolve (the validator will warn, not error, until you fill it in).

### Interview transcripts (.txt with timestamps)

Read directly. Recognize timestamp patterns like `00:12:34`, `[12:34]`, `12:34 -`.

Flow:
1. Source node: `source_kind: customer-interview`. Body contains the transcript verbatim. Tag with attendees and date.
2. Extract **claims** from the interviewee. Each claim worth preserving becomes a `fact` or `pattern` or `hypothesis` node, with the timestamp cited in the node body.
3. Extract **persona signals** — phrases like "as a [role]" or "I usually [behavior]" — and consider whether they update an existing `persona` node or warrant a new one.
4. Extract **direct quotes** worth preserving as `fact` nodes with high confidence (e.g., a customer's exact pricing-related comment that the MRD will cite).
5. All extractions get `derived_from` edges back to the interview source.

### Image screenshots (.png, .jpg)

Use Claude's native vision capabilities to read the image directly. Do not call `cb extract` for images — it doesn't support them.

Flow:
1. Move the image into `<vault>/_attachments/<YYYY-MM-DD>-<descriptive-slug>.<ext>` (the convention is committed alongside the rest of the vault).
2. Write a `source` node with `source_kind: web-snapshot` (if it's a web capture) or `internal-data` / `prior-internal-doc` (if it's an internal screenshot). Include the structured fields for web-snapshot sources: `url`, `captured_at`, `captured_method`, `attachment`.
3. Use vision to extract visible text. Put it in the source-node body.
4. Treat the extracted text like any other source and atomize into derived nodes per the same patterns above.

## Ingest-from-other-skills convention

When the user is ingesting the output of another Claude Code skill the company-brain ecosystem recognizes, identify the producing skill from the file's structure and route content appropriately. Always set `source_kind: skill-output` and add a `producing_skill: <name>` frontmatter field.

Known shapes:

- **competitor-profiling output** — typically one markdown file per competitor with sections like "Positioning", "Strengths", "Weaknesses", "Pricing". Create or update a `competitor` node. Create derived nodes for any claims worth preserving (especially anti-claims as ammo for sales battle cards).
- **customer-research output** — typically a synthesis doc with personas, jobs-to-be-done, and verbatim quotes. Create `persona` nodes for each archetype, `requirement` nodes for surfaced needs, `fact` nodes for the quotes.
- **product-marketing-context output** (`.agents/product-marketing-context.md`) — typically the foundational positioning document. Create `pillar` nodes for the positioning statements and `source` nodes for the citations.
- **write-spec / competitive-brief output** — feature/competitor docs. Route sections to `feature`, `requirement`, `competitor` nodes.

Unknown skill outputs fall back to generic atomization (markdown handling above).

## What this skill does NOT do

- Does not write into folders the active profile doesn't have (run `cb describe-profile` to know which).
- Does not invent content. If the document is sparse or ambiguous, surface that and ask the user to clarify — don't paper over it.
- Does not flip `controlled_document` to `true`.
- Does not extract from image formats with `cb extract` — use Claude's vision for those.
- Does not modify the *original* source file. The atomized version lives in the vault; the original stays where it is.

## After atomizing

Always run:

```
cb validate --path <vault>
```

at the end. Report errors. If there are unresolved edge targets (the validator will list them), surface them — they're usually places where the user needs to confirm follow-up captures.

You do not commit. The user (or their team) decides when to commit.
