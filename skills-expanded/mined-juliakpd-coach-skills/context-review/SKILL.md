---
name: context-review
description: Review a repo's context/instruction files (AGENTS.md, .instructions.md, skills) for context-engineering quality and whether the structure will hold as it grows. Read-only, findings first. Use when asked to review agent context, instruction files, or context architecture.
---

# Skill: Context-architecture review

Review a repo's context/instruction files (`AGENTS.md`, `.github/copilot-instructions.md`,
`.github/instructions/*.instructions.md`, prompt/skill files, YAML-frontmatter docs) for
context-engineering quality **and whether the structure will hold as the context grows**.
Be critical, not encouraging. Findings first. Name alternatives unprompted.

## Guardrails (this is a REVIEW)
- **Read-only.** Do not edit, create, or reformat any file. Produce findings only.
- **Evidence-based.** Every finding cites `file:line`. Test rules against the actual files
  (do links resolve? does the template match real docs?) — don't grade the prose in the abstract.
- **No praise padding.** If a file is thin or decorative, say so. Skip encouragement.

## Step 0 — establish purpose and layer FIRST (do not skip)
Fitness questions ("does this file earn its place?") are unanswerable without knowing what the repo
is for and who owns it. Do this before any other check, and **report the answers at the top of the
review** so the reader can correct a wrong premise.

- **Stated purpose.** What does the repo say it is for, and who is the intended user? Quote where it
  says so. **If you cannot find this stated anywhere, that is finding #0** — a repo whose purpose
  must be inferred from folder names will be used wrong. Do not silently infer it and review on.
- **The user's journey.** Walk one concrete task the intended user would do with this repo, start to
  finish. Where does it break, and what would they have to already know? This surfaces more than any
  checklist item.
- **Audience fit — is the path achievable for the *stated* user?** Separate from whether it works at
  all. Count the gates between a fresh start and first value (installs, plugins, accounts, CLI
  steps, config someone must toggle by hand). If the stated user is non-technical and the path runs
  through a terminal, a `curl | bash`, or a global package install, **say the setup is mis-fitted to
  the audience** — do not soften it into "trim the day-one surface". A repo that only works for a
  more technical user than it claims has either the wrong audience or the wrong setup, and the owner
  has to pick one. Name that choice explicitly.
- **Default-path integrity.** Check the very first artifact the user touches against the config that
  produces it — templates against the plugin settings that fill them, examples against the templates
  they came from. Mis-wiring here costs more than any structural finding, because it is the user's
  first impression and they cannot debug it.
- **Layer.** Which is it:
  - **Portable / shareable** (travels across clients or orgs) — must be name-free and abstract.
  - **Org-internal** (lives in the client's own org, stays there) — the client's own name, products
    and team names are *correct context here*, not leakage. Do not flag them.
  - **Personal** — looser still.
- **Privacy scope follows the layer.** Two different things, never conflate them:
  - *Client/company names* — a problem only in a portable-layer repo. Silent in an org-internal one.
  - *Personal data* (people's names, contacts, meeting notes about individuals, anything about an
    identifiable person) — a problem at **every** layer, including org-internal. This is the one
    that needs a mechanism, not just a rule.

## What to check — A. Status quo (is it good today?)
1. **Does each file earn its place?** Signal vs noise. Would removing it change agent behavior at
   all? If not, it's cost with no benefit — say so.
2. **Scoping / altitude.** Is repo-wide guidance in the repo-wide file, and file-specific guidance
   path-scoped (`.instructions.md` with `applyTo` globs)? Flag rules living at the wrong level.
3. **Progressive disclosure.** Is information revealed when needed, or dumped up front? Long
   always-on context that's rarely relevant should become a skill/on-demand file, not a standing rule.
4. **Redundancy & conflict.** Same rule stated in multiple files? Rules that contradict across
   files? Which one wins — is precedence/load order clear to a reader?
5. **Testability.** Is each rule concrete enough to probe ("use tabs, not spaces") or vague
   ("be helpful", "write good code")? Vague rules are decoration — call them out.
6. **Maintainability for non-experts.** Could a teammate who didn't write it understand *why* a rule
   exists and safely edit it? Missing rationale is a maintenance risk.
7. **Decision provenance.** Do choices record why + the alternative rejected, or are they bare
   assertions? Bare assertions rot because no one knows if they're still true.

## What to check — B. Longevity / scale (will it hold at 10x?)
Assume the context keeps growing (more sources folded, more docs, denser relationships). Stress-test:
8. **Reference integrity at scale.** Do cross-links / citations resolve today, and will they keep
   resolving as items move (e.g. inbox → archive)? Is there anything that *could* verify this, or is
   it manual hope?
9. **Hand-maintained bottlenecks.** Which artifacts are updated by hand on every change (indexes,
   maps, logs)? At 10x volume, do they become stale, merge-conflict magnets, or silently drift?
10. **Always-on budget.** Does the standing/always-loaded context stay lean as conventions accrete,
    or does every addition bolt on another permanent rule? Flag unbounded growth of always-on text.
11. **Schema / convention drift.** With no linter or schema, how do N docs stay consistent as N
    grows? Identify the fields/conventions most likely to drift and whether anything guards them.
12. **Graph / structure integrity.** Dangling links, orphaned entries, duplicated ids, ambiguous
    categories — do the rules prevent these from accumulating as the structure densifies?

## What to check — C. Knowledge-base / vault repos (only if the repo is one)
Applies when the repo is a note vault an agent reads rather than a codebase — e.g. an Obsidian
vault: a plain folder of Markdown notes with `[[wikilinks]]`, backlinks and an `.obsidian/`
config dir. Skip this section entirely for code repos.

13. **Vault vs repo boundary.** Is machine-local state committed (`.obsidian/workspace.json`,
    plugin state, caches, sync-conflict files)? It's noise to every reader and a merge-conflict
    source. Check `.gitignore` actually covers it — don't assume from the folder listing.
14. **Links an agent can't follow.** `[[wikilinks]]` resolve in the Obsidian UI, not necessarily
    for an agent reading raw files. If rules, indexes or entry points depend on them, test whether
    a plain file-reader can traverse the structure — or whether it dead-ends.
15. **Entry point.** A vault has no natural "start here". Is there one file telling an agent where
    to begin and what's authoritative, or must it sweep the whole vault every time?
16. **Note-level scoping.** Vaults grow by note, not by module. Is guidance path-scoped to folders
    that carry real meaning, or is it one always-on rule set over an ever-growing folder?
17. **Privacy accumulation.** Vaults collect meeting notes, names, personal data and client
    specifics by their nature — a people/contacts folder is a standing invitation. Is there a
    stated rule *and* a mechanism (gitignore, hook, folder split, pre-commit check), or only good
    intentions? In an org repo, treat "rule with no mechanism" as a high-severity finding.
18. **Source of truth / sync direction.** Is the repo the vault, or a copy of a vault living
    elsewhere? If a copy: what stops the two drifting, and which one wins?
19. **Template/example hygiene.** Do shipped templates and example notes contain *personal* data —
    a real colleague, a real stakeholder, a real meeting? Examples get copied, so a person's name in
    a template propagates into every note made from it. **Company/product names are not a finding
    in an org-internal repo** (see Step 0) — flag those only in a portable-layer repo.

## Output format
- **TL;DR** (max 3 bullets): the single most important fix, the biggest scale risk, and the verdict.
  Skimmable by someone who won't read the rest.
- **Verdict** (one line): keep as-is / trim / restructure.
- **Status-quo findings**, highest-impact first. Each: what's wrong, why it matters, the fix.
  Cite `file:line`.
- **Longevity findings** — what breaks as the context grows, most likely/severe first. Same format.
- **The alternative structure** you'd consider even if you don't recommend it, and why not.
- **What's missing** — a rule/scope/procedure the set should have but doesn't.
- Header line: repo name + date, so the output can live as a tracked, re-runnable document and its
  git history shows how context-health changes over time.
