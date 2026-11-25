---
name: refine-wiki
description: >
  Restructures curated raw/ sources into LLM-searchable wiki/ concept pages —
  concept-level atomization with source traceability and graph-derived
  wikilinks, not summarization — handling each doc_type differently.
  Triggers after conflict-detection passes (no open conflicts on the topic)
  or on an explicit "refine" request.
version: 0.1.0
author: Loremaster
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [wiki, refine, knowledge, atomize, sources, scrum, PM]
    related_skills: [conflict-detection]
---

# raw → wiki refinement

## Core principle
Refinement is **restructuring, not compression**. Preserve the information content; atomize it into searchable, referenceable concept units.
The detail needed to answer an SM/PM's concrete question ("what billing model did we settle on yesterday?") must stay alive.

## Preconditions (abort on violation)
- **Never refine a topic that is open in `conflicts/`.** Hold it and notify.
  - The open check targets `conflicts/CONFLICT-*.md` only. Diff blocks inside `PROPOSAL_*.md` may still contain leftover `Status open` strings from the past, so exclude them from the gate check.
  - Where possible, check only the status line's actual current value (`**Status** open`); never mistake a diff deletion line (`-**Status** open`) or proposal text for an open conflict.
- **Never infer, fill in, or invent content that is not in the raw source.** Leave gaps empty and flag them (→ delegate to conflict-detection as an under-specified decision).
- **Never create a wiki page without `sources`.** Untraceable refinement cannot be trusted.

## 1 concept = 1 page (atomic — no duplicate splits)
**Merge the same topic into one page even when it has multiple sources (`raw/PRD.md` + `raw/decisions/*.md`).** A concept's *current spec* (PRD) and its *decision history* (decisions) live **on one page**. Read raw via the `raw/**/*.md` glob (never assume fixed filenames). **progress is not part of this pipeline** (do not read it).
- ❌ **Forbidden:** creating `Billing Model` (PRD version) and `Billing Model Premium Switch` (decision version) as **separate** pages. They are the same concept → merge into the single `Billing Model` page.
- Decisions/reversals are absorbed into that concept page's **`## Decision History`** section (date/content/rationale/alternatives/reversal status). Never create a separate decision page.
- The test: "what is this decision/progress **about**?" → that concept's page. Before creating a new concept, first check whether `## Decision History` can absorb it.

## Per-doc_type handling (within the 1-concept=1-page rule above)
- **prd** (`raw/PRD.md`): one page per feature/concept, preserving spec detail. Merge that concept's decisions into **the same page**.
- **decision** (`raw/decisions/*.md` — per-backlog decision detail, backlog ID in the filename):
  - ⚠️ **Skip empty skeletons and drafts (not refinement targets).** If the frontmatter says `status: draft`, or the **decision-log table is empty** (header + empty rows only, no filled data rows), it is an *unfinished skeleton* laid down by backlog-kickoff — **do not create empty concepts or empty decision histories in the wiki.** Exclude it and log only "draft skipped: <file>". It gets refined once the developer fills the table and pushes `status: stable`.
  - Process **only filled ones** (`status: stable`, or actual decision rows in the table): **never as standalone pages.** Write each row of the decision table (`date/decision/rationale/alternatives`) as one entry (1 row = 1 entry) in the `## Decision History` of the concept page the decision is *about*; on reversal, preserve the **evolution** via status + previous-decision markers. (If that concept page does not exist yet, create it then, with the history section inside it.) Record which backlog (file) each entry came from in `sources` for traceability.
- **gtm:** split per strategy axis (target/channel/messaging/metrics) + cross-link related PRD features.
- **meeting:** extract decisions and actions only; discard chatter. Meeting decisions become decision-entry **candidates, proposals only** (authority: 1, no automatic adoption).
- **spec:** keep the technical spec in its original shape + link related PRD features.

## Wiki output frontmatter (required)
```yaml
---
concept: (concept name — the raw docs' own term verbatim, e.g. Billing Model, Free Plan Policy; no slugs)
sources: [source-file.md, ...]  # which raw it came from (traceability, required)
authority: (inherit the highest authority among the sources)
last_synced: (YYYY-MM-DD)       # team-local date — TZ="$TEAM_TZ" date +%F (set TEAM_TZ to your team's IANA timezone, e.g. America/New_York)
status: active                  # default; superseded allowed for reversed decision entries
related: [...]                  # wikilinks — derived from the graphify graph (below)
---
```
- **Concept-name language = source (raw) language.** If the team writes raw docs in a language other than English, then `concept:`, the graph `label`, `[[ ]]` links, **and the filename** must **all be that exact same term** in that language.
- Output path: `wiki/concepts/<concept name>.md` — the **filename is the concept name itself** (e.g. `Billing Model.md`). `concept:`, label, `[[ ]]`, and filename must be **identical strings** so that (1) the Obsidian page title reads as the team's own term, (2) the `[[Billing Model]]` link resolves to `Billing Model.md` (an English slug for a non-English team term **breaks every link**), and (3) `graphify query "Billing Model"` matches. **Never slugify to English.** 1 concept = 1 file.

## Wikilinks (graph-derived, one-way — do NOT fill in during refinement)
- **Always leave `related` as `[]`.** Wikilinks are derived not by this skill but by the **deterministic script `~/.hermes/scripts/loremaster-derive-wikilinks.py` from the graphify graph.json**. Reason: when an LLM writes links it invents nonexistent documents (a past failure) — links are computed from the graph only, which blocks fabrication.
- Derivation rule (script): only the top-N graph edges by weight (N≈3–5) become `[[ ]]`. Graph = source of truth; wikilinks = one-way derived view, regenerated on every rebuild. **Neither humans nor LLMs write `[[ ]]`/`related` by hand.**
- Do not insert arbitrary `[[ ]]` into body text either (except obvious directly-quoted references).

## Routing & dedup (Karpathy LLM-wiki pattern)
- **One raw change touches multiple wiki pages.** Do not look at just one file — find every concept page the change affects and update them together (do not stop at one concept).
- After a raw/PRD alignment, the wiki can look "mostly current" while stale sentences remain. Even if graphify plan reports `NOCHANGE`, that can just mean the raw change has not reached the wiki yet. First grep `wiki/concepts/` and `wiki/index.md` directly for retired terms/fields/flows (e.g. a dropped feature term like `quest card` and its bare stem `quest`, renamed fields like `payload.instructions` or `quests.avatars`, an obsolete unique constraint, a superseded "single-provider signup" rule and its "provider-based signup" phrasing, a retired "auth-scope consistency check" step). Patch current-spec sentences, decision histories, and index one-liners to the settled raw, then run graphify plan/build.
- **Cross-cutting changes (auth/onboarding and the like) can span 2+ concept pages.** E.g. a signup-method change lingers not only in the `Onboarding` page but also in `App Identity & Release Infrastructure` and the `wiki/index.md` summaries. Do not stop after updating one concept page — search out and align stale wording across the related concept pages and the index summaries too.
- **Before creating a new page, grep the existing `wiki/concepts/` first (`search_files`).** If the same concept already exists, **do not create a new one — strengthen and update that page** (1 concept = 1 file, no scattering). Add the new raw file to `sources` + refresh `last_synced`.

## Wiki catalog `wiki/index.md` (search entry point, must be maintained)
When refinement finishes, **update `wiki/index.md`** — every page, by category, with a **one-line summary** + link. At small scale, Slack Q&A and search enter through this catalog ("Search via index.md at small scale").
- Format: under `## <category>`, `- [[Concept]] — one-line summary`. Add new pages, refresh summaries of changed pages, remove pages that no longer exist.
- index.md is a catalog (derived view), so it is exempt from `sources`. But **every entry listed in it must be a real wiki page** (no links to nonexistent pages = no orphans).

## After refinement — graphify + wikilinks, automatic (no human approval)
When refinement (concept-page creation) is done, continue **immediately, without human approval**:

**1. Graph build = the session model (you) doing incremental inline semantic extraction → build script.**
**Never use the headless `graphify <path>` CLI** — it requires a separate provider key (Gemini/OpenAI, etc.) and **does not work with the agent session's OAuth** (and do not build crude fallbacks like SHARES_SOURCE just because keys are missing). graphify's keyless path = "the session model is the LLM", and here **you extract directly**. But **do not re-extract everything every time** — use the graphify cache to extract **only the changed pages** (saves LLM work; equivalent to graphify `--update`):
  - **a. Change detection (plan):** run `python3 ~/.hermes/scripts/loremaster-graphify-plan.py wiki/concepts`. Using a content-hash cache, it sets unchanged pages aside as reused entries in `graphify-out/.graphify_cached.json` and writes **only the pages needing re-extraction** to `graphify-out/.graphify_uncached.txt`. (Use `--force` for a full re-refine / cache reset.)
  - **b. Incremental inline semantic extraction:** read **only the pages listed in `.graphify_uncached.txt`**, judge the **semantic relationships** between concepts, and write graphify extraction-spec JSON to `graphify-out/.graphify_extract.json`. **Do not re-extract unchanged pages** (the cache covers them). If uncached is empty (NOCHANGE), skip extraction and go to c.
    - Format: `{"nodes":[{"id","label","file_type":"concept","source_file"}], "edges":[{"source","target","relation","confidence":"EXTRACTED|INFERRED","confidence_score","source_file","weight"}], "hyperedges":[], "input_tokens":0, "output_tokens":0}`
    - **`source_file` must be a cwd-relative path** in the form `wiki/concepts/<name>.md` (cache-key match — same representation as plan/build). Never absolute paths or bare filenames.
    - node `id`: lowercase `[a-z0-9_]` only — a non-ASCII or spaced concept name must become an ASCII slug (e.g. `wiki_concept_pricing`). **`label` is the page's `concept:` value verbatim** — not the file stem or slug. In wiki Q&A the team asks in its own terms, and `graphify query "<the team's term>"` finds the node only if the label is that term. **1 concept = 1 node.**
    - `relation`: **real semantic relations only** — `conceptually_related_to`/`references`/`depends_on`/`supersedes` etc. `EXTRACTED` when there is explicit evidence, `INFERRED` when inferred. **Never invent relations** (a gap beats an excess). "Cites the same raw file" alone is not an edge — that is not semantics.
    - When a changed page produces edges **toward unchanged pages**, those edges are refreshed. But unchanged-page → changed-page edges come from cache and can occasionally be stale — for a large update with big semantic shifts, use `--force` for a full re-extraction.
  - **c. Build (merge):** run `python3 ~/.hermes/scripts/loremaster-graphify-build.py wiki/concepts` → merges the cache reuse (.graphify_cached.json) + the new extraction (.graphify_extract.json) **over the full current page set** into `build_from_json` + clusters + report + `graphify-out/graph.json` (no LLM, no keys needed). Deleted pages drop out automatically. New extractions are stored in the cache for reuse on the next refinement. If the graph is empty, stop and report.
  - **d. (Optional) visualization:** `graphify export html` (deterministic, no keys).
  - `graphify-out/` is a build product — never delete it. In particular `graphify-out/cache/` is the incremental cache; deleting it turns the next refinement into a full re-extraction (gitignored — not a commit target).

**2. Wikilink derivation:** `python3 ~/.hermes/scripts/loremaster-derive-wikilinks.py --graph graphify-out/graph.json --wiki-dir wiki/concepts` derives the `related` `[[ ]]` links deterministically.

- The wiki is an artifact derived from raw, so it carries no separate human-approval gate (judgment/approval already happened at the raw/conflict stage). Body text from raw evidence only — that is the one thing to uphold.

## Last — commit & origin-push approval (automatic)
When refinement, graph, and wikilinks are done, commit the changes (`raw`/`wiki`/`graphify-out`) to git (e.g. `Refine wiki from resolved PRD`).
- **Pre-commit cleanup:** the dot-prefixed working files in `graphify-out/` (`.graphify_extract.json`, `.graphify_analysis.json`, `.graphify_detect.json`, `.graphify_cached.json`, `.graphify_uncached.txt`) are temporary scratch — **do not commit them** (gitignored, or excluded from `git add`). Commit targets: `graphify-out/graph.json`, `graphify-out/GRAPH_REPORT.md`, and the `wiki/` changes (plus raw when needed). Right after committing, **do not wait for a human to say "push"** — immediately raise a **"Push to origin?"** approval button via the **`request_approval` tool**.
- `title` example: `origin push — <project> (raw + wiki updates)`. `detail`: summary of the commits to push (hash + message) and the remote URL.
- **If APPROVED**, run `git push origin main`. **If DENIED/NO_RESPONSE**, do not push (the local commit stays — it can be approved and pushed next time). No retries, no workarounds.
- This approval button covers exactly **one thing: the external push to the remote** (the external-write gate — any write leaving the host requires human approval). The judged/refined **content was already approved at the raw/conflict stage, so do not re-approve content** (do not raise a second "apply the refinement?" button here).
- The host is the single writer — push works via the SSH deploy key (`core.sshCommand`). On auth failure, do not guess or work around; report it as-is.

## Isolation
- Read only this project's (channel/lore vault) documents. Never pull in another project's concepts.
