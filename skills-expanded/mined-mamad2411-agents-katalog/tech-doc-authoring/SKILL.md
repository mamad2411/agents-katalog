---
name: tech-doc-authoring
description: >
  Authoring-time rules for writing and editing Markdown technical documentation —
  the counterpart to tech-doc-consistency-check (which audits existing docs). Use this
  skill whenever you write or edit a Markdown doc, especially the user's guide docs
  ("Infra Guide to GCP AI Agents.md", "DevOps Guide to agents-cli.md"), or any time you
  add a heading, a section cross-reference (§X.Y), a link, an image, a Table-of-Contents
  entry, or an inline HTML anchor. Trigger on: "write this section", "add a heading",
  "link to section X", "cross-reference the other guide", "add an anchor", "insert an
  image", "edit the doc". Covers hard-wrap rules, in-doc and cross-doc link construction,
  GFM slug anchors, non-heading and image anchors, hyperlinking figure/diagram/table
  references, bidirectional cross-links, title-case headings, sibling-heading numbering,
  empty-section-preamble tolerance, list-vs-inline enumeration, color-blind-safe diagram
  color and palette economy, forward-reference fragility, and pretty-printing an embedded
  JSON string. Do NOT use this for auditing a
  finished doc (use tech-doc-consistency-check) or for general prose style (that stays in
  the user's global CLAUDE.md).
license: Apache-2.0
metadata:
  author: Vincent Yin
  version: "1.12.0"
---

# Tech Doc Authoring

Apply these rules while writing or editing Markdown technical documentation. They are authoring-time rules — they shape what you produce. Auditing an already-written doc is a separate skill (`tech-doc-consistency-check`); general prose style (short sentences, active voice, plain words) stays in the user's global CLAUDE.md.

## Hard Line Breaks

Do not insert hard line breaks inside a paragraph or list item. Write each paragraph and each list item as a single continuous line and let the viewer wrap to window width. Some of the user's renderers use markdown-it `breaks: true`, where a mid-paragraph newline becomes a literal `<br>` and does not reflow. Leave headings, table rows, and fenced code blocks untouched.

## In-Document Section References

In-document section references (e.g. `§6.4`, `§5.4`, `§4A.2`) must be written as Markdown hyperlinks to the section's GFM slug anchor — e.g. `[§6.4](#64-a2a-registration-on-cloud-run)`. Build the anchor from the heading using GFM slug rules, or copy it from the auto-generated Table of Contents. This applies to new prose and when editing existing sections — do not leave a plain `§X` reference behind.

## Cross-Document References to a Known Sibling Doc

Cross-document references to a **known sibling doc** — one the user distributes side-by-side in the same folder (e.g. the "Infra Guide to GCP AI Agents.md" and "DevOps Guide to agents-cli.md" pair, which share an `images/` subfolder) — are hyperlinked with an **angle-bracket relative link**, because the filenames contain spaces: `[link text](<Other Doc.md#anchor>)`. Angle brackets are required (a bare space breaks the link in strict parsers); do not percent-encode. Deep-link to the specific section wherever a section is cited: build the anchor from the target heading's GFM slug, copying it from that doc's own Table of Contents rather than recomputing it (the em-dash and `--flag=value` slug cases are easy to get wrong). When one sentence cites multiple sections of the other doc, make each `§X.Y` its own separate deep link. The visible link text must still name the target so it degrades gracefully in raw text — keep the full `.md` filename where the prose already uses it, or a clear short name like "the DevOps Guide" — never a vague name that leaves the reader guessing which file is meant. A reference to a file that is **not** a known sibling (not guaranteed to sit in the same folder) stays plain text and names the target by its full filename including the `.md` extension.

## Table of Contents and Heading Anchors

The user's Markdown editor auto-regenerates the Table of Contents on save (a "Markdown All in One"-style extension), rebuilding each entry from the heading text using GFM slug anchors. Do not hand-edit TOC entries' anchors, and do not add custom `<a id>` anchors inside headings (they are stripped when slugs are computed) — reuse the existing GFM slug for cross-references.

## Non-Heading Anchors

To link to a non-heading location — a paragraph, a `**Note:**`, a blockquote, a callout, a sidebar that is not itself a heading — add an inline HTML anchor at the start of that block: `<a id="kebab-name"></a>**Note:** …`. Place it on the same line as the text so it stays in the same paragraph (a separate line risks splitting into its own block under `breaks: true`). Then link to it with `[link text](#kebab-name)`. This is the counterpart to the heading rule above. A heading already has an auto-computed GFM slug, so never add a custom anchor there. A non-heading target has no slug, so an explicit `<a id>` is the only way to link to it. The anchor renders invisibly in GitHub and markdown-it.

## Image Anchors

Exception for an **image** target: put the anchor on its own line before the image, separated by a **blank line** (so the anchor sits in its own paragraph, with the `![...]` in the next block), not on the same line. On the same line the browser jumps to the *end* of the image and scrolls past it, missing the screenshot. A single line break with no blank line fixes some renderers (markdown-it) but not the GitHub web UI, which still scrolls past — the blank line is required for GitHub and works everywhere. With the blank line, the jump lands at the *top* of the image. This is the one non-heading target where a separate block is correct, overriding the same-line rule above.

## Referencing a Figure, Diagram, or Table

When prose refers to a captioned object in the same doc — a Figure, System Diagram, Table, Listing, or the like — make the reference a Markdown hyperlink to that object, the same way an in-document `§X` reference is hyperlinked. Do not leave a plain-text "Figure 3" or "Table 2" behind.

Create the target anchor if it does not exist yet. A caption is a non-heading target, so it needs an explicit `<a id>` (a heading's auto GFM slug does not apply). Use a stable kebab-case id that names the object: `figure-3`, `system-diagram-6`, `table-2`. Place the anchor per the anchor rules above — inline at the start of a **text** caption (`<a id="figure-3"></a>**Figure 3: …**`, so the reader lands on the caption with the object right below), or on its own line before a blank line when the target is an actual `![...]` image (the image-anchor exception).

Point the reference at the caption anchor, never at the enclosing section heading. Linking "Figure 2" to its section's heading slug lands the reader at the section top, not the figure, and silently breaks if the figure moves within the section or a sibling figure is added ahead of it.

Only anchor the doc's own captioned objects. A caption borrowed from an external source (e.g. "RFC 6749's own Figure 3") stays plain text — it is not a target in this doc.

## Mermaid Diagrams

For a line break inside any Mermaid label — node text, edge label, `note for ...`, subgraph title — use `<br/>`, never `\n`. `<br/>` is the portable break that renders everywhere the user's diagrams appear (GitHub, markdown-it, the consistency-check pipeline, artifacts). `\n` is renderer- and diagram-type-dependent: some renderers ignore it or print it literally. Standardizing on `<br/>` also matches the existing System Diagrams in the guides (which use `<br/>` and `&nbsp;`). Related global rule: call a connector between nodes an "arrow", not an "edge".

Fold a node's annotation INTO the node, not into a floating note box. A `note for X` (classDiagram) or a detached note node renders as its own box, competing visually with the real nodes and pulling the reader's eye away from the topology. Put the annotation text inside the class body (or node label) instead. Reserve a separate note only when the annotation genuinely belongs to no single node. Prefer conveying a structural fact through the arrows themselves over restating it in text.

### Diagram Color Must Survive Color Blindness

**The user is color blind.** These rules are not a nicety; a diagram that fails them is unreadable to its primary reader.

**Color is never the only channel.** Any distinction a diagram draws — works vs blocked, primary vs secondary, changed vs unchanged — must survive being read in greyscale. Carry it on at least one non-color channel as well: line style (solid vs dotted), terminator shape (arrowhead vs `x`), border weight, or explicit label text. Color is then reinforcement, never the message itself. This rule outranks the palette rule below, because a palette blocklist only names the combinations already known to fail.

**Red is the least reliable hue.** Do not pair red with green, black, dark grey, or brown to mark contrasting components. Red-green is the most common deficiency. Red against a dark neutral fails separately, under protan-type deficiency, where red's perceived brightness collapses so red reads as dark rather than as a distinct hue. Blue against red is a safe pair. The guides use blue `#2563eb` for a working path and red `#dc2626` for a blocked one.

**A marker can silently inherit the wrong color.** Mermaid mints per-color arrow markers keyed by hex (`crossEnd__dc2626`, `pointEnd__2563eb`) and derives that color from `linkStyle default`, ignoring an indexed `linkStyle`. So `linkStyle default stroke:<color>` recolors a blocked arrow's `x` terminator to the working-path color while leaving the line itself red — the shape that means "blocked" ends up wearing the color that means "works." Assign stroke **by index** whenever any arrow needs its own color. Then confirm in the rendered SVG that each `marker-end` points at the expected `__<hex>` variant:

```bash
mmdc -i diagram.mmd -o diagram.svg
grep -o 'marker-end="[^"]*"' diagram.svg | sort | uniq -c
```

Verify color changes by rendering, never by reading the source. Related: the `reference-mermaid-cli-diagram-verification` memory.

### Keep the Palette Small

Every distinct color in a diagram reads as a claim that something differs. A diagram that gives each distinction its own color becomes a mosaic, and it communicates less than one built from a few coarse colors. Two rules follow.

**Do not spend a color on a meaning another channel already carries.** Topology, shape, position, line style, and label text all encode meaning, and unlike color they survive greyscale and any color deficiency. A node that a dozen arrows converge on is already visibly the centerpiece of the diagram, so a unique border color for it buys nothing and costs a hue. Before adding a color, name the channel that would be missing without it. If you cannot, do not add it. This is the converse of the never-only-color rule above: color must never be the sole channel, and it must not be a redundant one either.

**Sharing one color across boxes that mean different things is an acceptable trade, not a defect.** Weigh palette size against precision. Reserve distinct colors for the differences the section is actually about, and let everything else share. "Same color, different meaning" is only a real problem when the reader must tell those things apart to follow the diagram. Do not propose recoloring on the grounds of exactness alone.

In practice, prefer adding a node to an existing `classDef` over writing a one-off `style` line for it. That removes the exception rather than restyling it, and it keeps the palette from growing one node at a time.

**Never leave a node or subgraph on mermaid's default styling.** An unstyled node renders `#ECECFF` on `#9370DB` purple, and an unstyled subgraph renders `#ffffde` on `#aaaa33` yellow. Those are theme defaults nobody chose, and nothing in the output distinguishes them from a deliberate decision — so a reader takes the purple as a category that means something. Give every node a `classDef` and every subgraph an explicit `style`, even where the value you pick is close to the default it replaces.

**Use one color for all subgraphs, at every nesting depth.** A nested region does not get its own fill. The nesting already shows containment and the subgraph title already names the region, so a second color spends a hue on what 2 channels carry. The inner box stays legible regardless, because its own stroke still draws the outline. Vary a subgraph only when it differs in *kind* rather than in position — a conceptual grouping versus a deployment boundary, say — and express that with `stroke-dasharray` rather than with another color.

(Set 2026-08-04. I had recommended 6 edits to fix a shared green that no reader would have been confused by, and separately kept a unique color on a node whose importance the arrows already showed.)

## Bidirectional Cross-Links

Prefer bi-directional cross-links. When one passage points to another (body→sidebar, note→detail section, section→section), add the return link too, so each end references the other. Point each link at the target's anchor: the heading's GFM slug for a heading target, or a custom `<a id>` (per the rule above) for a non-heading target.

## Title-Case Headings

Write all section headings in title case, not sentence case. Capitalize the first and last word, and every major word in between. Lowercase only the minor words: articles (`a`, `an`, `the`), coordinating conjunctions (`and`, `but`, `or`, `nor`, `for`, `yet`, `so`), and prepositions regardless of length (`of`, `on`, `in`, `to`, `by`, `with`, `from`, `for`, `vs.`, etc.). Capitalize the first word after a colon. Capitalize both parts of a hyphenated compound (e.g. `Per-User`, `Three-Stage`, `High-Code`). Keep code-span/backtick terms (e.g. `` `curl` ``, `` `agents-cli run` ``) and proper nouns verbatim. Capitalization does not change GFM slugs, so converting case never breaks TOC anchors or in-doc cross-reference hyperlinks.

## Matching Sibling Heading Convention

When adding a heading to an existing document, match the convention of a nearby **content** heading of the same level: its numbering scheme and depth, title vs. sentence case, and anchor style. If sibling content headings are numbered (e.g. `##### 6.3.6.1.`), number the new one to continue the sequence; if they are unnumbered, leave it unnumbered. Do not model a content heading on a special-case named callout. `Sidebar` headings (and similar named blocks such as `Note:` or `Example:` callouts) deliberately break the numbering convention and are exempt, so they are the wrong exemplar to copy. The trap to avoid: reaching for the nearest heading when that heading is a callout exception rather than a real content sibling.

## Empty Section Preamble

An "empty section preamble" is fine. A section heading may be immediately followed by a subheading with no text between them (e.g. an `##` heading directly followed by its first `###`). Do not flag this as an issue, and do not insert filler text just to fill the gap. Add a lead-in paragraph only when it carries real orienting content.

## Cold Open

A section may open directly on its first line of content, with no orienting lead-in. The heading has already named the subject, so a paragraph restating it adds nothing. Do not flag a cold open, and do not propose adding a lead-in — not when the section follows code blocks, not when it follows another section's conclusion, and not when the first line is a bare list lead-in.

The user's guide docs use a settled cold-open form for a walkthrough: the heading, then `<Actor> starts like this:`, then the list of steps. Infra Guide §5.3.1 opens `Bob starts like this:` and §6.3.2.4 opens `Peter (the end user) starts like this:`. Both are deliberate.

Add a lead-in only when it carries orienting content the heading does not — a scope limit, a prerequisite, or a pointer the reader needs before step 1. "The reader just came from a code block and needs easing in" is not such content.

(Set 2026-07-29, after I flagged §6.3.2.4's cold open twice and the user pointed at §5.3.1 as the established precedent.)

## List vs. Inline Enumeration

Prefer a list over a paragraph that enumerates items inline — whether parallel/comparative ("A carries X, while B carries Y"; "on one hand… on the other…"; "if ADK then… if A2A then…"; "A does X, after which B does Y") or inline-enumerated ("(1)…, (2)…, (3)…"; "(a)…, (b)…, (c)…"; "(i)…, (ii)…, (iii)…"). Use a **numbered list** when items are sequential steps or when surrounding prose may need to refer to a specific item by number; use a **bullet list** for unordered parallel or comparative items. Use a lead-in clause ending in ":", one item per entry, and any non-parallel prose that follows as a separate paragraph after the list — never appended to the last item. Inside a parent list item, that means a blank line followed by indented continuation text. Keep prose for narrative/causal flow where sentences connect and for a single short comparison.

**Trigger — announcing a count commits you to a list.** The moment you write a cardinal followed by a countable noun ("Two things differ", "3 reasons", "four main differences", "two ways", "several caveats"), you have promised the reader an enumeration. Deliver it as a Markdown list or a table, never as the following prose sentence. This is the single most-missed case of the rule above, because the inline form reads fine one sentence at a time — "Two things differ. The path carries an extra segment, and the URL uses a number." — and only the promise makes it wrong. Treat the count word itself as the cue: on writing it, stop and set up a `:` lead-in with bullets.

The trigger does **not** fire on a back-reference to something already enumerated — "the two forms", "all four types", "the same 3 steps". A definite determiner before the number marks it as a pointer backward, not a promise forward.

**Mixed-altitude passages — commit the structure, and use the list as a diagnostic.** A flat paragraph linearizes the logical tree of its sentences: some are parallel siblings, and one may be a summary that closes over several earlier ones. Flattening loses that shape, so adjacency implies false parentage — a sentence that concludes *several* earlier ones, left trailing after the last, reads as elaborating only that last one. When a passage mixes per-item detail with a cross-item conclusion, structure it up front: a list for the parallel items, then the conclusion as its own paragraph after the list (per the rule above). The list is also a diagnostic. If you cannot place every sentence as either a parallel leaf or the closing summary, the paragraph has a hidden scoping error.

## Write to the Reader's Altitude

Include a fact only if the target reader needs the concept at that point in the doc. The test is not "is it true" or "is it a real API" — it is "does *this reader* need this *here*." A fact can be accurate and still not belong: harness-internals and access-mechanism detail sit below the line of a reader who only writes application code, so they are cut even when correct. Name the reader for the passage (e.g. the `agent.py` author, the operator, the client developer), keep what that reader must know to use the thing, and drop what only its maintainer would.

This is why a concept primer omits the plumbing that *implements* the concept. Example — a Session/State primer for an app developer: keep `session`, `state`, and what the framework deposits there; cut the classes that drive the runtime (`Runner`, the session-service implementation) and the several code surfaces that reach state (`ToolContext.state`, `callback_context.state`, `invocation_context.session.state`). The reader never writes them, so naming one implies a precision it lacks and naming all is sprawl. This is distinct from concision, which trims wordiness: this rule decides inclusion by *whose need*, and it can cut a whole true subtopic, not just words.

## Forward-Reference Fragility

Do not write a sentence in one part of a doc that hard-codes a fact about a *different* part of the doc — an item count ("Four facts follow:") or a description of what another section covers ("[§7.2.1] covers what the runtime cannot reach"). An edit to that other part later can silently make the sentence wrong, and nothing flags the break. Prefer a phrasing with no dependency on the other location's current state: a count-free lead-in ("Characteristics:" instead of "Four facts follow:"), or simply cutting a cross-section description that the reader can get by following the link instead.

This is the general form of the item-count trap already named in **List vs. Inline Enumeration** above (a stale "The 3 behaviors listed above" after a 4th bullet was added elsewhere) — that trap is one instance of this rule, not a separate concern.

(Set 2026-08-07, from a 2026-08-04 co-edit of the Infra Guide. The user rejected both "Four facts follow:" and "[§7.2.1] covers what the runtime cannot reach" on this reasoning, over my initial argument that both were more precise phrasings.)

## Mark Every Omission Inside a Code or Capture Block

When you abridge anything inside a fenced block — omitted HTTP headers, dropped JSON fields, skipped code, truncated output — mark the cut **in the block** with a bare `...` line at the point of the omission. Saying "abridged" in the surrounding prose is not enough on its own. The reader studies the block, not the lead-in, and an unmarked cut silently misrepresents the block as complete.

Put the marker where the removed content was, at the indentation of its neighbors. A bare `...` on its own line is the form for a cut between lines (headers, statements, array elements); an inline `{ ... }` or `"parameters": { ... }` is the form for a collapsed object or argument list. Keep the surrounding prose's "abridged" note as well — the two work together, the prose explaining *why* and the marker showing *where*.

Redaction is a separate act from omission and gets its own marker, so do not collapse the two. Replacing a secret's value keeps the field visible and only hides what it held (`Bearer ya29.******<REDACTED, the parent runtime SA>******`), whereas `...` says a field or line is missing entirely. Match whatever redaction idiom the doc already uses, and preserve any non-secret prefix that carries meaning — a `ya29.` left in front of a redacted token still tells the reader what kind of credential it is.

## Fencing a Mixed Command-Plus-Output Block

When one code block shows a shell command followed by its JSON output, fence it as ```` ```json ```` — not ```` ```console ````, ```` ```shell ````, or ```` ```text ````. The JSON is the bulk of the block and the part the reader studies, so pretty-printing it is what matters. A `console`/`shell`/`text` fence renders the JSON flat and unhighlighted, which loses far more than it gains. The cost is that the 2 or 3 leading `$ curl …` lines highlight oddly, and that cost is accepted deliberately.

Never "correct" such a fence to a shell language, and never report the language as a mismatch — it is an intentional choice about which half of the block gets good rendering.

## Pretty-Printing an Embedded JSON String

A JSON field's value is sometimes itself a JSON document stored as an escaped string (JSON-in-JSON), such as `jsonAgentCard` or `source_extension_json`. When reflowing one for readability, keep it a **literal string** — do NOT expand it into a well-formed nested object. Retain every escape character verbatim (`\"` for inner quotes, `\\n` for a newline inside an inner string, `\\uXXXX` for a non-ASCII char). Add only structural line breaks and 2-space indentation between JSON tokens, as a pretty-printer would. Open the value with `"{` and close it with `}"`. Keep each string value on a single line (a JSON pretty-printer never breaks inside a string), even a long one. A trivially short nested object or array may stay inline. Two constraints on when to do this at all: (1) only pretty-print an embedded JSON string when the user explicitly asks — leave it as the captured single line otherwise; (2) usually apply it only to strings longer than 100 characters, leaving shorter ones on one line. Verify the reflow is lossless: strip the added whitespace and the result must decode back to the identical object. Example — before:

```json
"payload": "{\"id\": 7, \"note\": \"line1\\nline2\", \"tags\": [\"a\", \"b\"]}"
```

After:

```json
"payload": "{
  \"id\": 7,
  \"note\": \"line1\\nline2\",
  \"tags\": [
    \"a\",
    \"b\"
  ]
}"
```


