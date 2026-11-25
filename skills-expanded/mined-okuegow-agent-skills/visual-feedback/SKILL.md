---
name: visual-feedback
description: Use when the user wants to give feedback on a document, concept, design, plan, or report section by section - e.g. asks for a "Review-Seite", "Feedback-Seite", a kommentierbare HTML-Version, "Feedback zu jedem Abschnitt/jeder Box/jedem Element", comment pins in SVG diagrams, or wants to annotate a deliverable and paste the collected feedback back into the chat. Also when retrofitting an existing HTML page so every element accepts comments.
---

# Visual Feedback

## Overview

Turn any deliverable (concept, report, design, plan) into ONE self-contained HTML
review page where every meaningful element is an inline comment point. Each
comment can carry a category (Question/Error/Change/Praise) and priority
(Must/Optional). Comments persist in localStorage, and the user exports them as
structured markdown WITH a JSON attachment (clipboard or .md file) to paste back
into the chat. The chat paste-back closes the loop: the agent maps each comment
to its target `id` and works the feedback in.

Built for **multiple rounds**: when you produce a follow-up version you embed a
round manifest that records, per prior comment, what you did with it (addressed /
declined / deferred / noted). Resolved points move into a collapsed history and
stop reappearing as open fields; the page builds a per-version changelog and marks
changed sections. See "Iterating across versions".

The UI defaults to English and carries a small EN/DE toggle in the toolbar; the
toggle switches every visible string AND the exported markdown, and persists in
localStorage under `fb:lang`. Category/priority are stored as stable, language-
independent ids (`frage/fehler/aenderung/lob`, `muss/optional`); only their
display labels translate, so the JSON block reads the same in either language.

**Template:** copy and adapt `template.html` in this skill directory. It contains
the complete widget CSS/JS and one example of every target type. Do not rebuild
the mechanics from scratch - that is how past pages drifted into incompatible
variants. The script builds its own toolbar, toast and preview overlay, so
retrofitting an existing HTML page = paste the template's widget CSS block and
complete `<script>` into it, then only add the markers from the recipe plus
`data-fbkey`/`data-fbver` on `<body>`. Nothing else is required.

## Recipe (the page IS this)

1. **Comment points.** `<body>` carries `data-fbkey="<unique-key>"` (never reuse
   across pages) and `data-fbver="<n>"` (bump on every content rewrite, or old
   comments stick to changed spots). Each `<section>` carries
   `data-fbsec="<n> · <Titel>"`. Targets:
   - `data-fbauto` on a section/container auto-pins every `p`, `li`,
     `blockquote`, `h3`, `h4` and **every table row** inside (`data-fbskip`
     excludes subtrees) - the default for prose/tables
   - `data-fb="id"` + `data-fblabel="Label"` for manual targets (cards,
     callouts, diagram units)
   - `data-fb` on SVG elements gives overlay pins with a comment panel below
     the diagram
   - `<textarea data-fb="id">` for always-visible fields: one general-feedback
     field per section plus a "Gesamturteil" at the end
2. **Widget.** A ✎ pin per target opens a textarea in place, plus type/priority
   chips. Input autosaves (debounced). The sticky toolbar (built by the script)
   shows a storage-status pill, an "X/Y commented" counter, an EN/DE language
   toggle, a filter (All/Open/Commented), jump arrows, Preview, Copy feedback,
   Save as .md and Reset. All labels shown here are the English default; the DE
   toggle swaps them (and the export) to German.
3. **Versioning + comment lifecycle (feedback rounds).** Comments live under
   `fb:<key>:v<ver>`. Bumping `data-fbver` carries prior comments with a still-
   matching target into the new version - matching now also requires the target's
   **fingerprint** to still match (auto-targets by content, manual targets by their
   `data-fblabel`), so a drifted auto-target or a relabeled manual target surfaces
   loudly under "Nicht mehr zuordenbar" instead of silently binding to the wrong
   element. Auto ids are content-based (`autoId` hashes the element text; identical
   text gets a stable per-occurrence suffix), so inserting or reordering *other*
   elements no longer shifts ids. Give every `<section>` a stable `data-fbsecid`
   so changelog jumps survive title edits. On top of carry-forward sits an optional
   **round manifest** (`<script type="application/json" id="fb-rounds">`, embedded
   in the page) recording, per round, what you did with each prior comment - see
   "Iterating across versions" below. Without a manifest the page behaves exactly
   as before (carry everything, no history UI).
   Multi-tab: saves are read-modify-write merged and a `storage` listener syncs
   other tabs live (targets with a pending edit or open editor are left alone),
   so the common case (one reviewer, maybe a second tab) never loses data.
   localStorage has no real transactions, so genuinely concurrent saves from two
   tabs in the same instant can still drop one - the tool is built for
   single-reviewer use, not concurrent co-editing.
4. **Export - both ways, structured, dual-format.** "Copy feedback"
   (navigator.clipboard with execCommand fallback), "Save as .md" (Blob
   download) and "Preview" all produce the same document: human-readable markdown
   grouped by section, PLUS a machine-readable JSON block for the agent. The
   markdown headings follow the UI language (English shown below; German when the
   DE toggle is on). The JSON block is language-independent.

   ```markdown
   # Feedback: <page title>
   Captured on <date>
   Page: `<data-fbkey>` · Version v<data-fbver> · <n> comments
   Summary: 2× Error, 1× Question (of which 1× Must)

   ## <data-fbsec>
   **<data-fblabel>**
   <sub>Text · `<id>` · Error · Must</sub>
   _Ref: "<start of the commented element's text>"_
   > comment line(s)

   ...
   ```json
   { "page": ..., "version": ..., "comments": [ {id,type,section,label,quote,category,priority,comment,ts}, ... ], "orphans": [...] }
   ```
   ```

   When working the feedback in, prefer the JSON block: `id` is the stable anchor,
   `quote` the context, `category`/`priority` the intent (values stay
   `frage/fehler/aenderung/lob` and `muss/optional` regardless of UI language).
5. **Reset without dialogs.** Reset is a two-click confirm inside the button
   itself ("Sure? Click again" / "Wirklich? Erneut klicken", auto-disarm after
   3 s). The page contains zero `alert()` / `confirm()` / `prompt()` calls - they
   block the browser.
6. **Self-contained file.** No CDNs, webfonts, or external requests; system font
   stacks (e.g. Charter/Avenir on macOS); light + dark via
   `prefers-color-scheme`; `prefers-reduced-motion` respected; works from
   `file://` (in-memory fallback with a visible warning when localStorage is
   blocked). English UI by default with an EN/DE toggle; German strings use real
   Umlauten, and no text uses em-dashes.
7. **Verify, then open.** Parse the HTML (python `html.parser`: no unclosed tags,
   count of `data-fb` targets matches plan), `node --check` the extracted
   `<script>`, then open with macOS `open` (never browser-automation tools for
   local files). The widget mechanics themselves are covered by the jsdom smoke
   test `template-test.js` next to the template (needs `npm install jsdom`,
   run only after changing the template, not per page).

## Iterating across versions (feedback rounds)

The procedure for every follow-up version. This is what keeps answered points from
reappearing as open fields and produces the change history.

1. **Read the paste-back JSON.** It carries `comments` (open + reopened points)
   AND `rounds` (the history so far). Keep `rounds` - you extend it, never rebuild.
2. **Work each point in and assign exactly one status:** `addressed` (done),
   `declined` (rejected - `note` with the reason is mandatory), `deferred` (not
   this round - stays a live open field), `noted` (acknowledged, e.g. praise - no
   action). If you do not act on a point, mark it `deferred`; never drop it
   silently - the page counts un-responded carried comments as "unanswered" and
   warns in the toolbar.
3. **Bump `data-fbver`** (N to N+1). A manifest change without a version bump does
   nothing; the bump is what re-initialises the page.
4. **Author the manifest** `<script type="application/json" id="fb-rounds">`. Copy
   every prior round object from the paste-back's `rounds` verbatim and APPEND
   exactly one new round:
   `{ version:N+1, basedOn:N, date, resolutions:[{id,status,comment,note,fp}], changes:[{text,section,fromComments}], changedSections:[id | {id,kind:"new"}] }`.
   `id` is the prior comment's target id; copy its `fp` from the paste-back too
   (auto-targets carry a content fingerprint, manual targets a label fingerprint)
   so "Doch offen" can verify the target has not drifted. `section`/`changedSections`
   reference the stable `data-fbsecid`, not the visible `data-fbsec` text.
5. **Never leave an addressed/declined point as a live open field, and never
   re-emit the reviewer's old answers as pre-filled comments.** The manifest, not
   old comment text, is how you respond. `addressed`/`declined`/`noted` archive the
   point into the history; only `deferred` stays live.
6. **Content-level "open questions" you authored** (e.g. an "Offene
   Entscheidungen" box): once decided, remove them from the open section and record
   the decision as a `changes` line, so they stop showing as open.
7. Verify (jsdom `template-test.js` after template edits; parse + open per recipe
   step 7) and open.

The reviewer gets a "Verlauf"/History button (version-grouped changes + resolutions
with "Doch offen" to re-open any point you resolved), "Neu/Geändert in vN" badges on
changed sections, and a check mark on resolved targets.

**Identity model and accepted residuals.** A comment binds to its target by a
fingerprint: auto-targets by content, manual targets by their `data-fblabel` (so a
body edit keeps the comment while a relabel orphans it loudly). What the fingerprint
*guarantees*: inserting or reordering *other* elements never shifts an auto-target's
binding - the occurrence-drift class of silent misassignment is closed. Two residuals
remain, each narrow and of a different kind:
(1) a genuine short-hash collision - two different contents hashing to the same
fingerprint - could in principle misbind an **auto**-target; it is astronomically
unlikely with the double FNV hash and not further mitigated;
(2) reusing the *same* id **and** the *same* label for unrelated content carries onto
the new element, because it is indistinguishable from a legitimate edit-in-place -
a deliberate **manual** id+label reuse (author error). Keep manual id+label pairs
meaningful and give manual targets an explicit `data-fblabel`, and (2) does not occur.

## Common mistakes

| Mistake | Fix |
|---|---|
| Rebuilding widget JS/CSS instead of copying the template | Copy template.html; only content and markers change |
| Hand-marking every paragraph with data-fb | `data-fbauto` on the section; hand-mark only boxes and SVG elements |
| Working feedback in from the prose alone | Use the JSON block: `id` is the stable anchor, `quote` the context |
| Reusing a manual `data-fb` id for different content | Manual identity = id + `data-fblabel` (or, when unlabeled, the leading content). A changed label/content surfaces the old comment as an orphan (loud). An **identical id+label pair carries by design** (that is how body edits keep their comment) - so never reuse the same id+label for an unrelated element. Always give manual targets an explicit `data-fblabel` so body edits stay stable |
| SVG pins at 0/0 or drifting after resize | Positioning runs via getBoundingClientRect on load AND resize - keep the template's positionSvgPins wiring intact |
| Table rows not commentable | Use the ✎-cell + colspan-row mechanism from the template |
| `confirm()` for reset | Two-click confirm in the button (template has it) |
| Export as free-form plaintext | Grouped markdown with `data-fbsec`/`data-fblabel` so the agent can map comments back |
| Only clipboard export | Also offer the .md Blob download (clipboard can fail on file://) |
| Same localStorage key on two pages | Unique key per file, or comments bleed between pages |
| Feedback UI drowns the content | Widgets stay collapsed until toggled; content layout comes first |
| Re-emitting the reviewer's old answers as open comments next version | Respond via the round manifest (status + note); addressed/declined archive, only deferred stays live |
| Bumping content but forgetting the manifest | Every follow-up version appends one round to `fb-rounds`; unanswered carried comments are counted and warned |
| `changes[].section` pointing at the visible title | Reference the stable `data-fbsecid`, not the `data-fbsec` display text, or jumps break after title edits |
| Rebuilding the `rounds` array | Copy all prior rounds from the paste-back verbatim, append exactly one new round |
