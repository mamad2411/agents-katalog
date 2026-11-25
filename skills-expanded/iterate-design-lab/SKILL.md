---
name: iterate-design-lab
description: "Maintain this lab (the design-skill-lab repository): add or fix catalogue resources, run the link check, refresh catalogue thumbnails, add or re-review a research source, digest usage feedback into skill changes (evolve), run an eval round, cut a release. Repo-local and invoked by the owner. Not for: design work in any project (use design-studio), design reviews (critique-design) or building a design in code (implement-design)."
disable-model-invocation: true
metadata:
  version: 0.3.0
  short-description: Maintain this lab
---

# Iterate Design Lab

The maintenance counterpart of the shipped suite (`skills/`). Pick a mode, run its steps, finish with the
Definition of Done. Scripts do the mechanical work; this file says which one and when.

## The lab in one table

| What | Source of truth (edit) | Generated (never edit) |
| --- | --- | --- |
| Catalogue | `catalog/resources.jsonl`, `catalog/taxonomy.json`, `catalog/shot-overrides.json` | `skills/design-studio/references/catalog/`, `docs/data/`, the `<!-- gen:* -->` regions of `docs/index.html` and `docs/catalog/index.html` |
| Observations | written by scripts only: `catalog/observed.jsonl`, `docs/assets/thumbs/manifest.json` | |
| Evidence | `research/sources/`, `research/topics/`, `research/field/`, `research/log.md` | `research/INDEX.md` |
| Skills | `skills/*/` (shipped), this file (repo-local) | |
| Feedback | `feedback/inbox/`, `feedback/log.md`, `feedback/proposals.md` | `feedback/report.md` |
| Evals | `evals/` | `evals/runs/<date>/` results |

Ground rules:

- Visit, never remember. Licences come from the licence page. An unreachable host is not a dead one.
- Scripts before subagents: `scripts/check-links.py` checks the whole catalogue in minutes at zero model cost.
  If subagents are used at all, few of them, a cheaper model, results written to disk early.
- Every row, digest and field note is dated. One rule has one owner file; others link to it.
- Survey, propose, confirm: pre-fill domain, section, tier and the predicted version bump; ask only for a real choice.

## Modes

### add-resources

1. Deduplicate: `grep -i <host> catalog/resources.jsonl`, and
   `python3 skills/design-studio/scripts/catalog.py find <term>` for near-duplicates under another name.
2. Visit each site (fetch, or a real browser for JavaScript sites) and write a v2 row from what is there:
   `id` (kebab, permanent) · `name` (+ `name_zh`) · `url` (https, canonical, no tracking parameters) · `domain` +
   `section` (from `catalog/taxonomy.json`; `also` for a second home) · `kind` (taxonomy `kinds`) · `tags` (≤ 6,
   kebab) · `best_for` (one specific sentence, no praise) · `how_to_use` (filters, deep-link patterns, API) · `zh`
   (required Chinese one-liner; `zh_how` optional) · `access` · `login` · `license` (fonts, icons, assets, code) ·
   `tier` · `status` · `lang` · `region` · `entry_points` / `api` / `caveats` when useful · `origin`
   (`user-YYYY-MM-DD` or `research-YYYY-MM-DD`) · `added`. No `|` in text fields.
   Tier: S = the first place a senior designer looks (≤ 15% of a domain, and agent-reachable or with
   `entry_points` / `api`); A = strong and reliable; B = niche or with a stated weakness. Owner-supplied sites are
   always included; weak ones go to B with the reason in `best_for`.
3. `scripts/check-links.py --ids a,b,c` appends observations (verdict, `agent_access`) to `catalog/observed.jsonl`.
4. `npm run shoot -- --ids a,b,c --sheet <scratch>/sheet.png`, then look at the sheet (see refresh-thumbnails).
5. `scripts/build-catalog.py`, then `scripts/check-lab-invariants.sh`.
6. Release: PATCH (see release). Update a section note in `catalog/taxonomy.json` only when it no longer describes
   its rows.

### link-check

1. `scripts/check-links.py --report <scratch>/links.md` (full run; appends to `catalog/observed.jsonl`).
2. Triage by verdict. `dead` / `soft404`: find the new URL (a deep link that decayed to the home page counts), else
   set `status: sunset` and keep the row as history. Redirected to another host: usually an acquisition or rename;
   update the URL and say so in `best_for` when people search for the old name. `parked`: the domain lapsed; sunset
   or replace. `blocked` / `js`: true for this network, not a verdict on quality; an S row needs `entry_points` or
   `api` an agent can use (the build warns). `unreachable`: confirm with a web search or another network before
   touching the row; never delete on unreachable.
3. Re-read a sample of S rows for paywalls, decline and licence changes; demote or annotate.
4. Rebuild, gates, one line in `research/log.md`.

### refresh-thumbnails

1. `npm run shoot` shoots rows without an ok thumbnail; add `--stale 90` to refresh old ones, `--only-failing` to
   retry failures, `--ids a,b --force` to reshoot specific rows. Always pass `--sheet <scratch>/sheet.png`.
2. Review the contact sheet by eye: bot walls, consent banners, loading states, blank or header-only frames, a
   generic page where a better deep link exists. Pixel QA catches most, not all.
3. Fix a bad capture in `catalog/shot-overrides.json` (`url`, `hide`, `css`, `wait`, `ready`, `scroll`,
   `localStorage`, `force`, `image`, `fit`, `block`, and always a `note` saying why), then reshoot those ids.
   Placeholders are fine: the page draws a designed card; a wrong picture is worse than none.
4. `scripts/build-catalog.py` (regenerates `docs/data/thumbs.js`), gates; `npm run smoke` when the site changed.

### add-source

1. Follow `research/README.md` (怎么加一份来源): pick a permanent id, fetch the primary source (structured APIs and
   pinned repo commits first), write `research/sources/<id>.md` with the header block, `## Key facts` (exact
   numbers and rules with the URL fragment), `## What it changes for the skills`, `## Not verified / open`.
   Paraphrase; never mirror. A new version of a source gets a new id and `superseded_by` on the old one.
2. Edit the skill references it changes and add the id to their frontmatter `sources:`; set `reviewed` and
   `review_by` (+90 days perishable, +365 durable). Update the `research/topics/` file whose conclusion moved.
3. `python3 scripts/build-research-index.py`, a line in `research/log.md`, gates.
4. Re-review (a `review_by` passed, so gates fail): re-fetch, correct the digest and say what changed, move
   `fetched` and `review_by`, rebuild the index.

### evolve

Feedback arrives in `feedback/inbox/` per `skills/design-studio/references/feedback.md`.

0. Harvest (interactive, owner names a host project that logged little): read its `.design/decisions.md`,
   critique reports, the round's commits and the session transcript; write one inbox entry per finding. Describe
   the host by its kind only (`project: office-addin-web`), never by product, customer or directory name. Show the
   owner the entries before triage.
1. `scripts/collect-feedback.py`; read `feedback/report.md`, then every raw entry (the entries are the evidence).
2. Cluster by root cause, not by skill. An entry that repeats a "won't fix" in `feedback/log.md` is archived with a
   pointer to it.
3. Tier each cluster. **A**: misleading wording, factual errors, dead paths, two files contradicting each other;
   apply. **B**: new guidance inside an existing section or reference; apply interactively and list it in the
   summary so the owner can veto. **C**: new sections, references, modes or skills, contract changes, conflicting
   entries, a lone nit or preference; write to `feedback/proposals.md` with evidence and a concrete plan.
4. Apply A/B in the file that owns the rule; stay inside the line budgets; judge the version bump (release).
5. Append one section to `feedback/log.md` (date, entries, per-cluster action), then
   `scripts/collect-feedback.py --archive`, gates.
6. Unattended runs are `scripts/evolve.sh` (launchd: `scripts/com.design-skill-lab.evolve.plist`): proposals and
   Tier A only, on an `evolve/<date>` branch the owner reviews. Check it with `scripts/evolve.sh --dry-run`.

Act only on logged evidence. Thin evidence (one minor entry) goes to proposals, not into a skill. A correction from
the owner outweighs any inference.

### eval

1. Output eval: follow `evals/README.md` (six fixed briefs × arms no-skill / previous suite / current suite,
   canonical renders by `evals/render.mjs`, measured facts, three blind judges per `evals/judging.md`).
   Trigger eval: `evals/run_triggers.md`; the set must pass `python3 evals/tools/score_triggers.py --validate`.
2. Results go to `evals/runs/<date>/` (`results.json` validated against `evals/results.schema.json`, `report.md`).
3. Summarise in `research/field/evals-<date>.md` (Chinese) and add the rows to
   `docs/assets/showcase/showcase.json` (format: `docs/assets/showcase/README.md`) so `/skills/` shows them.
4. Report losses and "no clear difference" as prominently as wins; feed each loss into skill changes or proposals.

### release

- Judge the bump at commit time, for every non-trivial commit; one closed loop = one version. SemVer on the
  design-studio contract (modes, deliverables, output layout, reference paths): PATCH wording, catalogue rows,
  routine re-reviews; MINOR new guidance, references, sources that change guidance, or a contract reshape while
  at 0.x; MAJOR a removal or rename from 1.0 on (after two MINOR releases under `弃用登记` in the CHANGELOG).
- A suite release moves together: `skills/design-studio/SKILL.md` `metadata.version`, the README literal
  `suite 当前 X.Y.Z`, the top `## [X.Y.Z] - YYYY-MM-DD` entry of `CHANGELOG.md` (Chinese; what changed and why,
  per file), and `version` in `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json` (gate G7).
  Other skills bump their own `metadata.version` only when their content changes.
- Gates pass; `npm run smoke` when `docs/` changed. The owner commits, one commit per logical step, staging named
  files (never `git add -A`); branch for anything beyond a catalogue patch; never push or merge unasked.
- The site is GitHub Pages from `main:/docs`. A page fix is done when
  `gh api repos/caocong1/design-skill-lab/pages/builds/latest` shows `built` for that commit.

## Definition of Done

`scripts/check-lab-invariants.sh` exits 0 (stdlib, no network, seconds; details in `scripts/gates.py`):
G1 catalogue schema + generated views fresh · G2 every catalogue id has a thumbnail record (ok with its file, or
placeholder) · G3 research source headers valid, cited ids exist, `research/INDEX.md` fresh (fails when a
`review_by` passes) · G4 skill frontmatter, line budgets (design-studio and this file 200, other SKILL.md 150,
references 300), reference frontmatter (sources resolve, `review_by` not past), links and backtick paths resolve ·
G5 feedback entries valid · G6 eval trigger set valid · G7 one version everywhere · G8 no hand-typed catalogue
counts or dead links in `docs/` · G9 no stray files tracked. CI (`.github/workflows/check.yml`) runs the gates and
the site smoke test on every push. When a gate is wrong, fix the gate in the same change and say so.

Also: new rows were visited, licences read at the source, tiers defensible; digests say what was actually read;
only intended files are staged.

## Anti-patterns

- Editing a generated file, or committing `catalog/resources.jsonl` without rebuilding.
- A row without `zh`, a thumbnail or a link-check observation; a site added from memory; a guessed licence.
- Deleting a row because this network could not reach it.
- Tier inflation: if everything is S, the tier means nothing.
- Perishable specifics (pixel specs, library APIs, trend lists) in a SKILL.md instead of a dated reference.
- Host product or customer names in feedback, field notes or commits.
- Fanning out expensive subagents for verification a script can do.
