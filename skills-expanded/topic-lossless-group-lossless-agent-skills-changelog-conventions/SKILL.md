---
name: changelog-conventions
description: How The Lossless Group writes and structures changelog/ entries across all repos (projects, true monorepos, pseudomonorepos). Use whenever shipping or pushing a coherent chunk of work, when scaffolding a new repo's changelog/ directory, when authoring a product release message, when the user says "log this", "write a changelog", or "ship note", or when reviewing a changelog/ file. Also fires when the user drops screenshots for an entry or the work being logged is visual — composes with prep-images-for-embed so images get CDN-hosted with real alt text without the user naming both skills. Encodes the strict frontmatter (publish, lede, ISO dates), filename pattern, "it exists" priority, the never-use-relative-image-paths rule (entries get rolled up into parent sites, so relative paths break), and the show-don't-enforce ethos.
---

# Changelog Conventions

> **The single most important rule: it exists.** Everything else is refinement.

Every Lossless repo at every level (project, true monorepo, pseudomonorepo) should have a `changelog/` directory at the root, parallel to `context-v/`. Entries are written when meaningful chunks of work ship — or at least when they push.

**Changelog First Development** is a working Lossless theory: a fast-moving, meaningful changelog signals momentum to clients, audiences, contributors, and your own future self. The bus is leaving. The cruise ship is full. See `references/changelog-first-development.md`.

## When to use this skill

- You just shipped or pushed a coherent chunk of work
- The user drops screenshots for an entry, or the work being logged is visual enough that prose alone undersells it (compose with [[prep-images-for-embed]])
- The user says "log this", "write a changelog", "ship note", "publish update"
- Scaffolding a new repo's `changelog/` directory
- Reviewing or updating an existing changelog entry
- Authoring a product release message (see `releases/` subfolder below)

## When to write an entry

**Yes:**
- A coherent chunk of work shipped (deployed, merged, released)
- Or at least pushed to a remote where someone else might land on it
- A new convention, blueprint, or tool became available
- Multiple smaller changes have accumulated into something worth announcing

**Not necessarily:**
- Every commit (most aren't worth a changelog)
- Typo fixes, minor refactors, work-in-progress

> **Future direction:** the team is open to a "tweet-style" subset — short, frequent micro-changelogs for the in-between work that doesn't merit a full entry. Not implemented yet; flagged as a candidate.

## Where it lives

```
<any-repo>/
├── context-v/        # living documentation
└── changelog/        # ← this skill governs this directory
    ├── YYYY-MM-DD_NN.md       # entries
    ├── YYYY-MM-DD_NN.md
    └── releases/              # for product-style projects only
        ├── v1.0.0.md
        └── v1.1.0.md
```

- **Filename:** `YYYY-MM-DD_NN.md` where `NN` is a daily counter (`01`, `02`, ...). ISO date with dashes — always.
- **`releases/` subfolder:** only for product-style projects with versioned releases. Release messages live there as `<version>.md` (or whatever versioning scheme the product uses). Standard changelog entries live in `changelog/` proper.

## Mandatory frontmatter (last few months and forward)

These fields are **hardcoded** for new entries — non-negotiable. Older entries may have less or more; respect them.

```yaml
---
title: "Human-readable title"
lede: "Subtitle-length hook — 140 chars max, two rendered lines. The long version goes in Why Care?, not here."
publish: true                        # Obsidian publisher convention. STRICTLY ENFORCED.
date_authored_initial_draft: YYYY-MM-DD   # When the content was first *set*: real, coherent, not a stub.
date_authored_current_draft: YYYY-MM-DD   # When it last got a SUBSTANTIVE revision. Never earlier than initial.
authors:                             # Humans only. Always a list. Preferred ul format (not [a, b] inline).
  - Firstname Lastname
augmented_with:                      # AI tools used. Format: "<tool> on <model name version>".
  - Pi on Claude Sonnet 4.5
files_changed:                       # Optional but strongly recommended. Paths from project root.
  - src/components/NameOfComponent.astro
  - context-v/blueprints/Some-Blueprint.md
---
```

### Two families of dates, and why both exist

This is the part agents get wrong. There are **filesystem dates** and **editorial dates**, and they answer different questions.

| Family | Keys | Source of truth | Answers |
|---|---|---|---|
| **Editorial** | `date_authored_initial_draft`, `date_authored_current_draft` | A human's judgment about the content | "When was this actually written and last meaningfully revised?" |
| **Filesystem** | `date_created`, `date_modified` | `stat` on the file | "When did these bytes appear and last change?" |

**Editorial dates are what timelines should read.** Filesystem dates lie in two directions:

- `date_modified` **overstates** recency. Obsidian bumps mtime just for *opening* a file. A doc untouched in substance for three months can show yesterday's date.
- `date_created` **can overstate** age-of-origin. A machine recovery in this tree reset birthtime on a batch of files to the recovery date. Where frontmatter records an *earlier* creation date than the filesystem, **the frontmatter is the more accurate record** — never overwrite it with `stat`.

Corollary for agents deriving a missing `date_created`: if the file has a `date_authored_initial_draft`, that is a better source than filesystem birthtime. A document cannot have been created *after* its own first draft.

### Recognized optional date keys — never strip these

The tree uses a fuller vocabulary in places, applied unevenly on purpose. **These are not required, but they are never to be removed, renamed, or "cleaned up" when you find them:**

```yaml
date_authored_final_draft:      # Present-but-empty is meaningful: "not final yet."
date_first_published:           # When it actually went out, distinct from when it was written.
date_last_updated:              # Any touch, substantive or not.
at_semantic_version: 0.0.1.0    # Four-part epoch.major.minor.patch.
date_created: YYYY-MM-DD        # Filesystem. Kept where present.
date_modified: YYYY-MM-DD       # Filesystem. Kept where present.
```

The maintenance cost of writing these is near zero for an agent, and different surfaces read different ones — that asymmetry is why the vocabulary is broad rather than minimal. **Fill one when you genuinely know the answer; leave it alone otherwise. Deleting an unfamiliar key is always wrong.**

### Why this vocabulary is quieter on a changelog than in `context-v/`

The whole draft-tracking apparatus exists because **`context-v/` documents constantly evolve.** A spec gets revised across months; a plan accumulates phases and post-ship notes; a blueprint gets superseded. There, `date_authored_current_draft`, `date_authored_final_draft`, `date_last_updated`, and `at_semantic_version` are doing real work — they are how you tell a doc that moved last week from one that has been stable since spring.

**A changelog entry is normally write-once.** You ship, you log it, it stays. So in practice:

- `date_authored_initial_draft` and `date_authored_current_draft` will usually be **the same date, forever.** That is correct and expected — not a sign anything was missed.
- `date_authored_final_draft` and `date_first_published` are frequently left empty on changelog entries. Also fine.
- The fields are still carried for consistency, and for the entries that *do* get revised — a correction, a follow-up ship note folded into the original, a post-ship addendum. When that happens, bump `date_authored_current_draft` and you have the history.

**Redundant fields you don't use cost nothing.** Do not prune them from a changelog entry on the grounds that they're unused there — the uniform shape is what lets one aggregator read both trees.

### Key migrations

Two legacy spellings are being renamed as files are touched. Preserve the value verbatim; change only the key:

| Legacy | Current |
|---|---|
| `date:` | `date_authored_initial_draft:` |
| `created:` | `date_created:` |

### Notes on the fields

- **`publish: true`** is set by Obsidian publisher and is strictly enforced there. Do not toggle it off without understanding the publishing implications.
- **`lede`** is intentional — not "description". The word signals: *write something that grabs attention*; the reader should want to keep reading. **It is subtitle-*length*: 140 characters maximum, target 90–130 — two rendered lines, never three.** A hard budget, not a guideline: "a few sentences" is too vague to constrain anyone, and a sweep briefed against that wording produced ledes averaging 370 characters that clipped mid-sentence in every unfurl. The lede has to do its job in two seconds, and a paragraph can't. When you feel it wanting to carry the full context — the journey, the stakes, the inventory of what shipped — that's the cue to **stop and put that material in the `## Why Care?` section** directly below the title. Lede = the two-second hook; `Why Care?` = the paragraph that earns the scroll. A lede that has swelled past a subtitle is a `Why Care?` section wearing a lede's clothes — move it down.
- **`date_work_started` / `date_work_completed`** are optional and record **when the work happened**, as opposed to when the entry was written. Every other date on the entry is about the document; these are about the thing the document describes. Worth setting whenever work spanned more than the day it was written up — a timeline built on `date_authored_*` shows when someone sat down to type, not when anything shipped, and rendered project histories want the second. Skip them for a same-day change where all four dates collapse. **Never derive them from the filesystem and never backfill** — an absent field is honest; a guessed one corrupts the timeline it was added to serve. Live precedent: eleven entries in `content-farm/plugin-modules/perplexed`.
- **`site_uuid` / `hex_code`** are **write-once identity fields — mint them on every new entry.** `site_uuid` is a lowercase v4 UUID; `hex_code` is 6 chars of `[a-z0-9]` and is the entry's own citation ID (`[^7c1e0a]` inline → `[^7c1e0a]: [[2026-04-29_03]]` in `## References`). Changelog entries need this most: filenames are dates, so two unrelated entries in two repos routinely share one, and every entry gets copied into two or three roll-ups. `site_uuid` is what tells an aggregator "four copies of one entry" from "four different entries" — and gives Chroma/Graphiti a key that survives re-ingest. **Generate with a command, never type one:** `uuidgen | tr 'A-Z' 'a-z'` and `LC_ALL=C tr -dc 'a-z0-9' </dev/urandom | head -c6` (**not** `openssl rand -hex 3` — wrong charset, collides at 20% today). See `references/frontmatter-spec.md`.
- **`summary`** is optional and **agent-facing** — the counterpart to `lede`, not a longer version of it. `lede` earns a human's click and is what flows into OpenGraph automatically; `summary` says what the entry is *for*, where it sits in the workflow, what it unblocks or supersedes, and how pseudomonorepo / `context-vigilance` logic should treat it. Because nothing renders it in a card, it isn't length-constrained the way a lede is. Write one going forward — an agent produces it in the same pass as the lede. **Check first that the repo isn't already using `summary` as a legacy spelling of `lede`** (fullstack-vc is the known case); see `references/frontmatter-spec.md`.
- **`authors`** is for **humans only**. Preferred form is the YAML list (one author per line), not inline `[a, b]`. AI agents do not go here, even when they wrote substantial content.
- **`augmented_with`** is for the AI tooling that helped produce the entry. Format is **`<tool> on <model name version>`**, e.g., `Pi on Claude Sonnet 4.5`, `Claude Code on Claude Opus 4`, `Cursor on GPT-5`. Same ul-list preference as `authors`. Include this field whenever an AI agent contributed materially — honesty about augmentation matters more than authorship credit.
- **ISO dates with dashes for everything** — both dates and timestamps. Never `2026/05/04` or `May 4, 2026`.

See `references/frontmatter-spec.md` for edge cases and optional fields.

## Public by default

Changelogs are written **for the public web**. Assume:

- A reader with no prior context lands on this entry from a Google search
- The lede has to do its job in two seconds
- Internal jargon needs a one-sentence translation or a `[[wikilink]]`
- Embarrassments and bugs can be discussed honestly — that's part of building in public

A long-running goal: aggregate all changelogs across all Lossless repos via the GitHub API into a "Lossless Changelog" umbrella view. Write entries that would render well in that aggregated context.

## Marketing up top, engineering notes as the narrative unfolds

**Every `README.md`, every `changelog/` entry, and every `changelog/releases/<version>.md` carries the same discipline: marketing up top, engineering notes as the narrative unfolds.** The opening — lede, Why Care?, What's New? — is marketing-shaped; it has to earn the click and answer "what does this do for me?" The deeper sections — How it Works, Under the Hood, Files Touched — are engineering-shaped; they reward the reader who came for substance with the actual substance. **Both belong in the same document. What differs is sequence.**

The failure mode this rule fights isn't "too engineering" or "too marketing" — it's mixing them in the wrong order. Engineering details in the lede lose the general audience before they get to the value. Marketing language in the Under the Hood section feels evasive to the engineer who scrolled there specifically for the gnarly bits. **Treat the document as a cascade from broad to specific**, and each audience gets dropped at the right station — and trusts what they read on the way down because the voice matches the depth.

The audience cascade isn't "the team plus whoever happens to wander by." It's a deliberate four-tier sequence, and the document is structured so that each tier gets value and is invited to keep reading.

### The four audiences, in the order they appear in the document

| # | Reader | What they want | Where they stop reading |
|---|---|---|---|
| 1 | **General audience** | *Why should I care? What does this thing do for me?* | After the lede if you don't earn the click; after Why Care? if the framing isn't compelling |
| 2 | **Nerds passing by** | *What's actually new? Does this overlap with something I know?* | After What's New? if nothing piques their interest |
| 3 | **Nerds paying close attention** | *How does it work? What are the gotchas? What did you have to figure out?* | After the deep-dive sections once they've gotten the substance they came for |
| 4 | **Internal team** | *What changed in the codebase? Where do I find X? What's the followup state?* | They read to the end because they have to; this is the tail |

The whole point: **the same document serves all four** by sequencing the content from broadest to most-specific. Lede → Why Care? → What's New? → How it Works → Under the Hood → Files Touched / What's Next / References. **Marketing voice up top dissolves into engineering voice further down** — the lede speaks to anyone, the Files Touched block speaks to the team. Each reader gets dropped at the right station and the prose meets them there.

### The pragmatic argument

"No one will read this" is sometimes literally true. **It's the same amount of effort to draft a release entry someone might want to read as to draft one no one will.** The upside-case (someone lands on it via search, via a sibling-plugin's cross-link, via the org's "Lossless Changelog" rollup, via a tweet) costs nothing extra in effort, and a single positive impression from a stranger is worth more than the same prose buried as internal notes.

This is not about copywriting flair. It's about **sequence**. The lede answers "why care," the H2 sections give increasingly technical readers more depth, and the file-trees and SHA references live at the bottom where the internal team expects them. The doc reads as warm and competent to a general audience and as technically substantive to an engineer because it's both at once, just stacked correctly.

### Long files are fine; stamp a TOC

If a release narrative or a substantial changelog entry runs long, the answer is **not** to trim out the depth — it's to add an **anchor-link table of contents at the top** so each audience tier can jump to their section. Astro's MDX rendering picks up `[Section title](#section-title)` anchors automatically from H2 IDs; for plain Markdown the GitHub renderer handles it the same way. A TOC with 4–6 entries that maps to the audience cascade (`#why-care`, `#whats-new`, `#how-it-works`, `#under-the-hood`, `#whats-next`) is the canonical shape.

### How this composes with the rest of the skill

- The `Body shape` section below codifies the canonical opening sequence (`Why Care?` → `What's New?`)
- The `Tell a story` section frames the structural arc each entry should follow
- The `Voice` section governs the tone in which all four audiences are addressed
- This section above sets the **audience model** the other three sections serve

## Roll-up at every level

The same aggregation principle applies **at every parent → children boundary**, not only at the org-wide top. A pseudomonorepo's splash, site, or gallery should surface its own `changelog/` *and* roll up the changelogs of its submodules into one feed. A reader landing on `content-farm/splash/changelog/` should see ship notes from `image-gin`, `cite-wide`, `perplexed`, and the rest — not just from content-farm itself.

**Mechanism preference:** the **GitHub Content API**, authenticated, at build time. For each submodule, derive the API endpoint from the parent's `.gitmodules` (`url =` → `{owner}/{repo}`, `branch =` → `ref`) and query `/repos/{owner}/{repo}/contents/changelog/`. Merge the results into the parent's collection, sorted by date across the union, with **provenance** rendered on each card (which submodule it came from). Same pattern for `context-v/`.

**Implication for how you write entries:** assume your changelog can be read in three different aggregations — your repo's local list, the parent pseudomonorepo's rolled-up list, and (eventually) the org-wide Lossless Changelog. The lede is your only handhold in the bigger feeds. Make it work without the surrounding repo as context.

For mechanism details — auth, rate-limit handling, failure modes, loader sketch, and provenance metadata — see `pseudomonorepos/references/content-rollup.md`. The composition is intentional: changelog-conventions governs *how to write* an entry; the pseudomonorepos skill governs *how parents aggregate* their children's entries.

**Status:** aspirational. The first two splashes (`memopop-site`, `content-farm/splash`) render local-only changelogs as of writing. Roll-up is the documented next step, not yet implemented in any production splash.

## Show, don't enforce

Conventions here are evolving. People are encouraged to experiment. The way to spread the convention is to **show it working** — not to police existing entries.

- ✅ Write your own entries to the convention
- ✅ Nudge a contributor toward the format when they ask
- ❌ Go around "fixing" old entries to match current frontmatter
- ❌ Reject a PR for using `description` instead of `lede`

The aspiration is consistency. The reality is generative-first. Respect that.

### The one carve-out: directed normalization sweeps

"Show, don't enforce" governs **incidental** edits — do not rewrite someone's frontmatter as a side effect of unrelated work. It does **not** forbid a deliberate, operator-directed sweep to bring a repo up to standard.

When such a sweep is running, these rules bind:

1. **Additive only.** Add missing keys. Rename the two legacy spellings above. Never delete, reorder, restyle, or re-serialize anything else. A frontmatter round-trip through a YAML library is forbidden — it collapses multi-line `lede:` blocks and reorders hand-authored keys.
2. **Never touch the body.** A frontmatter sweep that changes one line of prose is a failed sweep.
3. **An explicit `publish` value is a decision.** If the key is already there, leave it. Never flip an existing `false` to `true`.
4. **`publish` is a read, not a count.** Judge it by reading the document. A stale "Stub" banner on a fully-written doc means `true`; a polished title over twelve `[awaits discussion]` placeholders means `false`. Word-count heuristics get both wrong.
5. **Edit originals, never rollups.** Collated copies (`context-vigilance-kit/corpus/`, `splash/src/rollup/`) and vendored skill copies (`context-v/agent-skills/`) are derived. Fix the source; the rollup regenerates.
6. **Renaming a key can break a consumer.** Grep for readers of the old key before a rename lands. `date:` → `date_authored_initial_draft` broke two changelog ingesters that read `date` as their metadata field and temporal anchor.

## Reference / submodule projects

**Don't expect them to have proper changelogs or frontmatter.** Many submodules in our pseudomonorepos are external projects we're studying or vendoring. They are out of scope for our conventions. When working *on* an external project's content, follow that project's conventions; when working in *our* code, follow these.

## Body shape: lead with the previewable sections

List views and preview cards on the rendered site use the **first body sections** as previews — just like the lede. Structure entries so the first two sections after the title can stand alone:

1. **`## Why Care?`** — the audience-facing answer. Why does this matter to a reader who isn't on the team? One to three short paragraphs.
2. **`## What's New?`** — the concrete summary. Bullet list or short paragraphs of the actual changes, links to artifacts.
3. **(Then go deeper.)** — the how, the journey, the visuals, the technical details. Readers who care will follow you down. Readers who don't have already gotten the value.

Unless the audience is contributors specifically, **lead with `Why Care?` not with `What's New?`**. The audience cares about impact before inventory.

Both headings are phrased as **questions** — the parallel rhetorical shape ("Why Care? What's New?") signals to the reader that the entry is having a conversation with them, not lecturing them.

## Length: not a factor

Rendering a Markdown file through an SSG costs nothing. **Write what's needed — no more, no less.** Don't pad to look thorough; don't trim to look tight.

The failure modes seen in practice:

- "Make it concise" → too concise, loses the journey
- "Make it robust" → padded with irrelevant minor nonsense

The target: **enough to convince someone to care, plus enough that a reader who cares can follow along and learn something meaningful.**

## Tell a story

A changelog entry is a small journey, not a journal entry and not a list of disconnected fixes.

- ✅ A coherent arc: "We hit X, tried Y, learned Z, here's what shipped"
- ✅ The struggle plus the resolution — readers learn from both
- ❌ Two paragraphs of miscellaneous CSS fixes — not a story
- ❌ A yak-shaving rabbit hole with no resolution — not a story by itself

If you can't articulate the arc, the work probably isn't ready for a changelog entry yet. Combine with related work, or wait.

## Voice

**We are moving fast and learning a ton and we are excited to share this with you. We speak human, we are human. But we are nerdy and we open our nerdy doors.**

In practice:

- First person plural ("we shipped", "we tried") for team work; first person singular when accurate
- Active verbs, present tense for what's now true, past tense for the journey
- Direct address to the reader is welcome
- Jokes that land are welcome; jokes that don't land are skipped
- Show your work — don't hide the messy middle
- Don't use corporate filler ("various improvements", "enhanced experiences")

See `references/voice-and-shape.md` for the full voice/shape guide with examples.

## Use visuals

Visuals make entries skimmable, memorable, and honest about complexity. Use them generously:

- **Code blocks in fences** — with language tags for syntax highlighting
- **Mermaid diagrams** — flowcharts, sequence diagrams, state diagrams
- **ASCII diagrams** — for tree structures, simple boxes-and-arrows, rendering everywhere
- **Tables** — when comparing options or showing before/after
- **Screenshots** — for UI work. **Not relative paths — see below.**

The rule: **pretend you need to convince someone to care, and pretend anyone who cares wants to follow along and learn something meaningful.** Show enough of the "how we did this" that it clicks for the reader who reads that far.

### Screenshots go to the CDN, never a relative path

When the user drops screenshots for an entry — or when the work you are logging
is visual and screenshots would carry it better than prose — **use
[[prep-images-for-embed]]**. Do not ask which skill to load; an entry that wants
images is the trigger.

```bash
node ~/.claude/skills/prep-images-for-embed/scripts/prep-images.mjs \
  --slug <changelog-slug> --repo <repo-name> \
  --src "~/Desktop/Screenshot ….png" \
  --name "Plane__Work-Items--Empty" \
  --alt "<what the image SHOWS, not that it is an image>" \
  --emit lfm
```

**Relative paths are not a style preference — they break.** Changelog entries are
**rolled up** into parent splash sites (see `pseudomonorepos/references/content-rollup.md`):
the markdown is copied out of its own repo into another site's content
collection. A `![](./images/foo.png)` that resolves locally resolves to nothing
once the entry is rendered somewhere else. A CDN URL survives every aggregation.

The three things that matter, so you rarely need to open the other skill:

1. **Alt text describes what the image shows.** A reader who cannot see it should
   learn the same thing a viewer would. The script rejects `alt="screenshot"`.
2. **`--emit lfm`** on our own sites — the `::image{…}` directive supports
   `caption`, `source`, `source-url` and float layout. `--emit html` elsewhere.
3. **Naming is `Block__Element--Modifier_ISOSTAMP.jpg`**, Title-Case, matching the
   `ogimage__` convention. The script normalises it; pass whatever reads naturally.

Everything else — resizing, EXIF stripping, JPEG-over-WebP, folder layout — the
script handles. Load [[prep-images-for-embed]] only when something is unusual.

## Templates

When creating a new entry, start from `templates/entry.md` (standard changelog) or `templates/release.md` (product release).

## Composition with other skills

- **`pseudomonorepos`** — the `lossless-loop` Phase 2 (Progress) and Phase 4 (Publish) both write to changelogs. Project changelog = Progress. Parent pseudomonorepo changelog = Publish.
- **`context-vigilance`** — changelogs sit alongside `context-v/`, not inside it (aspirationally). Some legacy projects nest them; respect what's there.
- **`astro-knots`** — changelog content gets aggregated and rendered on Astro Knots sites. Write with that publication path in mind.
- **`prep-images-for-embed`** — how screenshots get into an entry: renamed, resized, metadata-stripped, uploaded to ImageKit, emitted as `::image{…}` or `<img>` with real alt text. **An entry that wants images is enough of a trigger — the user should not have to name both skills.**

## Typical flow

1. **You just shipped something.** Pause before opening a new task.
2. **Decide:** is this a coherent chunk worth logging? (Apply the "Yes/Not necessarily" guide above.)
3. **Find the changelog/** at the repo root. Create it if missing.
4. **Filename:** `YYYY-MM-DD_NN.md`. Increment `NN` if today already has entries.
5. **Copy** `templates/entry.md`. Fill in every mandatory field — ISO dates with dashes, `publish: true`, and both `date_authored_*` dates (identical on a brand-new entry).
6. **Write the lede first.** If you can't write a compelling lede, the work might not warrant an entry.
7. **Body:** what shipped, why it matters, what it enables next. Link related work via `[[wikilinks]]`.
8. **Commit and push.** This entry is part of the work, not separate from it.

## See also

- `references/frontmatter-spec.md` — full frontmatter rules, optional fields
- `references/filename-conventions.md` — daily counter, releases subfolder
- `references/what-counts.md` — heuristics for when an entry is warranted
- `templates/entry.md`, `templates/release.md` — scaffolds
- `pseudomonorepos/references/lifecycle-workflow.md` — how changelogs fit the 5-phase loop
- `pseudomonorepos/references/content-rollup.md` — how a parent splash aggregates `changelog/` (including `changelog/releases/<version>.md`) from each submodule into one feed; two reference implementations (`content-farm/splash` via GitHub Content API, `ai-labs/splash` via local filesystem)
