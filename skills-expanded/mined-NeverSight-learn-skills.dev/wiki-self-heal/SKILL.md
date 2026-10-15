---
name: wiki-self-heal
description: Autonomously audit an LLM wiki (Karpathy pattern) for gaps, contradictions, orphans, and stale data, then research and fill high-priority gaps using quality-gated web research. Supports audit-only dry-run mode. Operates on a dedicated branch and commits changes for human review — never auto-merges. Use when the user asks to "lint my wiki", "self-heal my knowledge base", "find gaps in my wiki", "update my second brain", "auto-research my wiki", "run a health check on my LLM wiki", "audit my wiki without making changes", "dry run the lint", or wants to schedule periodic wiki maintenance.
---

# wiki-self-heal

Audit → research → fill → commit. An autonomous pass over a Karpathy-style LLM wiki that finds what's weak or missing, researches high-quality answers, writes them into the wiki, and commits to a dedicated branch for human review.

Inspired by Karpathy's `autoresearch` loop: isolated branch per run, explicit CAN/CANNOT rules, numbered steps, structured logging, simplicity criterion, and a NEVER STOP autonomy directive once the loop begins.

## When to use

User says: "lint my wiki", "self-heal", "find gaps", "auto-research my wiki", "update my second brain", "health check my wiki", "audit my wiki" or "dry run" (audit-only mode), or has scheduled this skill via cron / GitHub Actions / Claude Code triggers.

## Two modes

- **Full mode** (default) — audit → research → apply → commit. Changes the wiki on a heal branch.
- **Audit-only mode** — audit → report. No research, no changes to wiki pages. The audit report itself is still committed to the branch.

Infer the mode from phrasing. If the user says "dry run", "just audit", "audit only", "don't make changes", or "show me the gaps first" → audit-only. If the user just says "lint" or "self-heal" → full mode. If unsure, ask once.

## Preconditions

Before doing anything:

1. The vault has Karpathy wiki structure: `raw/`, `wiki/`, `CLAUDE.md`, `wiki/index.md`, `wiki/log.md`. If any are missing → stop and suggest running the `llm-wiki-setup` skill first.
2. The vault is a git repo. If not → `git init && git add . && git commit -m "chore: pre-heal snapshot"` before continuing.
3. The git working tree is clean. If dirty → stop and ask the user to commit or stash first.

## Research tool selection

At the start of the first run in a session, ask once:

> I'll default to WebSearch + WebFetch for research. If you have any of these MCPs installed for higher-quality sources, let me know which and I'll prefer them: Apify, Firecrawl, Exa.

Priority order when available: **Exa → Firecrawl → Apify → WebSearch/WebFetch**. Fall back to the next tool on any failure. Never block the loop on tool selection — WebSearch + WebFetch always work.

## First-run guidance

The first time this skill runs on a populated wiki, expect the audit to find **many** gaps. That is normal — the wiki has never been linted before.

**Strong recommendation: use audit-only mode for the first run on any vault.** Let the user read the audit report, understand the landscape, and decide priorities before any research pass writes pages. Don't dump 50 new pages into a wiki on the first pass without the user seeing what's coming.

If the vault is nearly empty (< 5 wiki pages), skip self-heal entirely — there's nothing meaningful to audit. Suggest the user ingest some sources first.

## The loop

Full procedure with commands and edge cases in [references/loop.md](references/loop.md). Core sequence:

1. **Read state** — `CLAUDE.md`, `wiki/index.md`, last 10 entries of `wiki/log.md`.
2. **Create branch** — `git checkout -b wiki-heal/$(date +%Y-%m-%d)`. Append `-2`, `-3`, etc. if a branch for today already exists.
3. **Audit** — scan for the 6 gap types per [references/audit.md](references/audit.md). Write findings to `wiki/audits/audit-<date>.md` and add an entry under the `## Audits` section of `wiki/index.md`.
4. **Audit-only early exit** — if audit-only mode: commit the audit report and index update, append the log entry, print the audit-only report, stop.
5. **Prioritize** — pick top N (default N=3) high-severity, skill-addressable gaps. Skip gaps needing human judgment.
6. **Research each gap** — apply the quality gates in [references/research-quality.md](references/research-quality.md). Every factual claim needs ≥ 2 independent sources. Reject SEO spam and content farms.
7. **Apply** — create or update wiki pages with cited findings. Update `wiki/index.md`. Add bidirectional `[[wikilinks]]`.
8. **Log** — append one consolidated entry to `wiki/log.md` per [references/log-format.md](references/log-format.md).
9. **Commit** — `git add wiki/ && git commit -m "heal: <n> gaps addressed, <s> skipped"`. **Leave on branch. Do not merge.**
10. **Report** — print the final summary in the format below.

## Simplicity criterion

**All else equal, fewer new pages wins.** A 1-source stub that only restates what's already in `[[related-page]]` should be skipped or merged into the existing page, not created as its own file. Prefer updating existing pages over creating new ones when a concept already has a home. Adding 20 thin orphan pages is a regression, not progress.

If a run ends with zero new pages because all gaps were better addressed by updating existing pages → that is a successful run, not a failed one. Report it accordingly.

## CAN / CANNOT

**CAN**:
- Create new wiki pages (when justified by the simplicity criterion)
- Update existing wiki pages
- Update `wiki/index.md` (including a new `## Audits` section if one doesn't exist yet)
- Append to `wiki/log.md`
- Create `wiki/audits/audit-<date>.md`
- Download new sources to `raw/` if research pulls in a fresh document (note in log)
- Create a heal branch and commit to it

**CANNOT**:
- Modify any existing file in `raw/`
- Delete any wiki page (always flag for human review instead)
- Add any factual claim without ≥ 2 qualifying sources
- Merge the heal branch into main
- Skip the log or commit step
- Pause the loop to ask "should I continue?" (see Autonomy rule below)

## Autonomy rule

Once the loop begins (after preconditions and tool selection), **do not pause to ask the human if you should continue**. The human may be asleep, away, or expecting autonomous operation. Work through the top-N gaps, then stop and report. Only stop early if:

- A CANNOT rule would be violated
- Quality gates fail for all sources on a gap → skip that gap, log reason, continue to the next
- The heal branch has drifted from main by more than 50 commits → stop and report
- A git operation fails → stop and report

## Scheduling

Recommended cadence: **weekly** for active vaults (daily or near-daily ingest), **monthly** for slow vaults, **on-demand** after each research burst. Full recipes in [references/scheduling.md](references/scheduling.md) — macOS launchd/cron, GitHub Actions (opens a PR automatically), and Claude Code scheduled triggers.

**First run guidance**: always run `wiki-self-heal` manually at least once — ideally in audit-only mode — before automating it. Never schedule a skill you haven't observed end-to-end.

## Output format

### Full mode

```
Wiki self-heal pass — <YYYY-MM-DD>
Branch: wiki-heal/<tag>
Mode:   full

Audit:     <N> gaps found (HIGH: <h>, MEDIUM: <m>, LOW: <l>)
Addressed: <n>
Skipped:   <s>

New pages:
  - [[<page>]] — <one-line summary> (sources: <k>)

Updated pages:
  - [[<page>]] — <what changed>

Skipped gaps:
  - [<type>] <title> — reason: <short reason>

Sources added: <k>
Commit:        <short-hash>
Status:        keep

Review: git diff main..wiki-heal/<tag>
Merge:  git checkout main && git merge wiki-heal/<tag>
```

### Audit-only mode

```
Wiki audit — <YYYY-MM-DD>
Branch: wiki-heal/<tag>   (audit-only — no changes to wiki pages)
Mode:   audit-only

Scanned:    <N> wiki pages
Gaps found: <total> (HIGH: <h>, MEDIUM: <m>, LOW: <l>)

Top priorities (first 5):
  1. [<type>] <title> — <one-line detail>
  2. [<type>] <title> — <one-line detail>
  3. ...

Audit report: wiki/audits/audit-<date>.md
Commit:       <short-hash>
Status:       keep

Next step:
  Review wiki/audits/audit-<date>.md, then:
  - "Run wiki-self-heal on the top <k> high-priority gaps"
  - or edit the audit report and ask me to address specific items
```
