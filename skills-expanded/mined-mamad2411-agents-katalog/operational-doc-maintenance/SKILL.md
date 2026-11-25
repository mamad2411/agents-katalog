---
name: operational-doc-maintenance
description: "Use when keeping operational and repo documentation current — post-migration stale-reference sweeps, CHANGELOG gap-fills, endpoint/service retirement doc updates."
version: 1.1.0
author: Hermes Agent
license: MIT
platforms: [windows, linux, macos]
metadata:
  hermes:
    tags: [documentation, changelog, migration, staleness, maintenance, docs-lead]
    triggers:
      - post-migration doc sweep
      - docs reference retired endpoint or service
      - stale URL in documentation
      - CHANGELOG gap
      - service migration documentation update
      - documentation freshness check
      - update docs after infrastructure change
      - doc index drift
      - dead link in README index
      - README file count stale
      - reference index audit
      - generated inventory source of truth
      - skills count stale in README
      - reconcile counts across docs
      - README vs ECOSYSTEM count mismatch
      - skills-inventory regeneration
    related_skills: [project-documentation-standards, recurring-status-checks, discord-report-format]
---

# Operational Documentation Maintenance

## Overview

Operational docs (`BRIDGE_SETUP.md`, README indexes, `guides/`) go stale **silently**: an infra migration or service retirement lands as a code commit, the commit message announces the change, and nobody updates the docs. The CHANGELOG usually has a matching gap, because the migration commit skipped it. This is the single most common repair trigger for a docs-manager role — expect it on nearly every maintenance pulse.

This skill covers the maintenance loop: detect stale references after infrastructure changes, fix them, fill CHANGELOG gaps, and verify the docs describe what actually exists.

## When to Use

- A migration/retirement commit landed and docs may reference the old endpoint, URL, hostname, service name, or env var
- A pulse/audit asks "are the docs still current?"
- CHANGELOG `[Unreleased]` is missing entries for recent commits
- You are documenting new scripts/files and need to verify they exist
- Sibling docs (`guides/`, `reference/`, README indexes) may disagree about an endpoint

**Don't use for:** writing new READMEs from scratch (see `project-documentation-standards`), skill-library content audits (`skill-content-audit`), report data-freshness (`report-freshness-diagnostics`).

## Post-Migration Doc Sweep Procedure

1. **Grep for the old identifier** across the whole repo — URL, hostname, service name, env var:
   ```bash
   grep -rn "wss://retired-host\|OLD_SERVICE_NAME\|old-endpoint" docs/ *.md 2>/dev/null
   ```
2. **Update EVERY reference** — Overview paragraphs, architecture ASCII diagrams, Files tables, env-var examples. A diagram showing the old endpoint is as stale as a paragraph naming it.
3. **Add a prominent migration note** (blockquote) near the top of each affected doc: old endpoint → new endpoint, what was migrated (channels/messages/keys/config), migration scripts used, cutover date.
4. **Fill the CHANGELOG gap** — migration commits often skip it. Add an `[Unreleased]` → Changed/Added entry citing the commit SHAs.
5. **Verify before documenting** — every script/file added to a Files table must exist on disk first (`ls` / `test -f`). Never document what isn't there.
6. **Check sibling docs** — a second doc may hold the same stale reference, or may already be updated (don't redo it, don't miss it). `docs/guides/`, `docs/reference/`, README indexes are common second homes.
7. **Commit** with a clear `docs:` message; report the commit SHA.

**Real case (Aug 1 2026):** Buzz relay migration retired `wss://your-relay.communities.buzz.xyz` → local `ws://localhost:3000` (commits a50f54b + 0fcd94e). `docs/BRIDGE_SETUP.md` still documented the hosted relay in its Overview + architecture diagram; `docs/guides/buzz-integration.md` was already current. Fixed BRIDGE_SETUP.md (overview, diagram, migration note, migration scripts added to Files table), filled the CHANGELOG `[Unreleased]` → Changed entry, verified both migration scripts existed on disk, committed `c23e905`.

## Operational vs Historical Docs: two sweep treatments

Not every stale doc gets the same fix. Before editing, classify each hit:

- **Operational docs** (runbooks, SOPs, setup guides, AGENTS.md host tables, artifact maps) — **update the URL in place** to the canonical value. These are read by operators to do things today; a stale URL misroutes a human or agent.
- **Historical/dated docs** (audit reports, repair logs, status snapshots, dated diagnostics like `*-2026-04-28.md`) — **do NOT rewrite history**. Prepend a prominent `> [!NOTE] Consolidation/migration (YYYY-MM-DD):` banner stating the new canonical value and that references below are historical; leave the body intact as a record.

**Real case (Aug 11 2026):** CRM host consolidation moved everything to `crm.your-domain.example`. Operational docs (VA OPS SOP, onboarding plan, setup guides, runbooks) got direct URL replacements; historical docs (CRM_VOICE_STACK_AUDIT, REPAIR_AND_WEBSITE_WORKSPACE_PLAN, browser-calling-*, STATUS_AND_REMAINING_WORK) got banners. A brand-new `docs/CRM_HOST_CONSOLIDATION_2026-08-11.md` became the single source of truth for the final state.

**Cross-repo sweeps:** when ownership spans repos (e.g. GHL + website-landlord both document the same CRM/register URLs), grep **both** repos — the sibling repo's AGENTS.md / REPO_ARTIFACT_MAP.md / routing docs rot just as fast. Commit per-repo with a `docs:` message and report each SHA.

**Bulk URL replacement across many files:** a Python loop (read → `content.replace(old, new)` → count replacements → write with `newline=''`) beats 20 hand-edits. Print per-file replacement counts to verify the sweep. Watch for `https://` vs bare-hostname references — replace only the `https://...` form when bare mentions describe legacy role, or you'll corrupt prose like "keep leads.your-domain.example or dialer?" decision notes.

## Doc Index Drift Audit

README indexes go stale in two silent ways: the "N files (~XKB)" count drifts from reality, and **subdirectory index READMEs** (`reference/README.md`) accumulate dead cross-links that the root index never surfaces — the root README only describes subdirs generically ("Technical reference materials"), so a broken link inside `reference/` is invisible until someone clicks it.

**Verify a count claim:** `N = find docs -type f | wc -l` minus self-referential index README files. `docs/README.md` and `docs/reference/README.md` are NOT counted in the "19 files" claim — 21 on-disk files minus 2 index files = 19, so the claim can be accurate even though `find` says 21. Count the actual index table rows too (`grep -oE '\[[^]]+\]\([^)]+\.md\)'`).

**Audit each subdir index both directions:**
- (a) every on-disk file listed in its local index — on-disk files missing from the index = **index gap** (add them);
- (b) every index link resolves to an existing file — links to nonexistent paths = **dead links** (remove or re-point).

Cross-links pointing **outside the docs tree** (`../../profiles/env-reference.md`, `../../config/README.md`, `../../gateway/README.md`) are the first to rot on repo-layout changes. Verify them with `ls` before trusting the index.

**CRLF preservation when rewriting docs:** hermes-config docs are CRLF ("ASCII text, with CRLF line terminators" per `file`). Rewrite with Python `write_bytes(content.replace('\n', '\r\n').encode())`, then verify `cat -A <file> | grep -c '^M'`. Rewriting CRLF docs as LF creates noisy diffs and mixed-endings files.

**Real case (Aug 4 2026):** `docs/reference/README.md` had 3 dead cross-links (`profiles/env-reference.md`, `config/README.md`, `gateway/README.md` — none existed in the repo) + 3 unindexed on-disk files (`radicle-backup.md`, `auto_action_report.md`, `pim_scan_results.md`) + a stale skills count (399 → actual 433). Root `docs/README.md` claim verified accurate (19 = 21 − 2 index files). Fixed the subdir index (removed dead links, added Operational Reference section, refreshed count), CRLF preserved, committed `c440f32`.

## Generated Inventory as Source of Truth (count reconciliation)

When a **generator script** produces an authoritative artifact (e.g. `scripts/gen-skills-inventory.py` → `docs/reference/skills-inventory.md` with "Total skills: 540, Categories: 175"), that artifact becomes the **single source of truth** for every count-bearing doc in the repo. The generator reflects the live library; prose docs only drift from it. A common multi-doc failure: the inventory says 540, but README.md says "70+ skills", ECOSYSTEM.md says "444 skills", docs/README.md says "19 files" — three docs, three stale numbers, all contradicted by the freshly generated artifact.

**Reconciliation procedure (after regenerating an inventory):**
1. Grep the whole repo for the OLD count and related claims — don't trust one doc to be the only carrier:
   ```bash
   grep -rn "70+\|444\|18+\|19 files" README.md ECOSYSTEM.md docs/ 2>/dev/null
   ```
2. Patch every hit to the generator's number (540 skills / 175 categories / actual `find docs -name '*.md' | wc -l` file count). Check both prose intros AND stats tables AND ASCII architecture diagrams — the diagram box ("38 MCP Servers") is as stale as a paragraph.
3. Bump the index file count with the real on-disk number: `find docs -name '*.md' | wc -l` (remember the index-file subtraction rule above).
4. Commit once with a message naming the generator and the synced counts.

**Real case (Aug 4 2026):** after Scribe regenerated `skills-inventory.md` (540/175) at `43ccce8`, the master README still claimed "70+ skills", ECOSYSTEM.md claimed "444 skills / 18+ categories", and docs/README.md said 19 files (actual 21). Synced all three to the inventory (README both prose spots, ECOSYSTEM stats table, docs/README count), committed `eb7f536`.

**Also check for a divergent clone before trusting counts** — two clones of the same repo on different branches (E: `vps-hybrid` vs C: `master`) can carry different doc generations; the counts on the non-canonical clone may be newer OR older than the canonical one. See `git-clone-divergence-reconciliation` for the canonical-clone check, and measure divergence with `git fetch <local-path-or-origin> <branch>` + `git rev-list --left-right --count HEAD...FETCH_HEAD` (e.g. 48 ahead / 69 behind). Note: fetching from a **local** clone path works with Windows-style `E:/...` paths, not MSYS `/e/...` (see `windows-cron-msys-path-fix`).

## CHANGELOG Maintenance

- Keep `[Unreleased]` current as commits land — don't wait for a release. Group by type: Added / Changed / Fixed.
- Cite commit SHAs for traceability.
- A doc fix belongs under Fixed; a migration belongs under Changed (plus Added for new scripts/files).
- Before assuming the CHANGELOG is current, list what landed since the last entry: `git log --oneline --since="<last pulse timestamp>"` (timestamp form beats `-N` — nothing slips between pulses).
- **Gap-fill procedure (verified Scribe pulse 2026-08-10):**
  1. `git log --oneline --since="<last pulse>" -- docs/` (drop the path filter to catch non-docs commits too)
  2. Read the `[Unreleased]` section with `read_file` (offset = line of `## [Unreleased]`) — a `sed -n "$(grep -n 'Unreleased' ...)"` range one-liner gets hardline-blocked by the terminal guard (see `hermes-terminal-command-guards`)
  3. Confirm the gap: `grep -n "<hash>" CHANGELOG.md` → zero hits = missing entry
  4. Add under the existing `### Docs` subsection, matching style: bold file path, hashes in parens, one-line description, "Scribe pulse YYYY-MM-DD" attribution
  5. CRLF: run `file CHANGELOG.md` first; `patch()` preserves CRLF when old/new strings carry `\r\n` — verify with `git diff` after
  6. Commit + push, then log the entry in the pulse log (PULSE.md) and daily digest

### First-Time CHANGELOG Creation (repo has none)

When a repo has substantial recent activity (10+ commits in ~2 weeks) and no `CHANGELOG.md`, bootstrap one — release notes are a first-class documentation duty. Verified Aug 2 2026 on website-landlord: 87 commits since Jul 20 with zero changelog → created `CHANGELOG.md` (`650301e`).

1. **Confirm absence correctly**: `find . -iname 'CHANGELOG*' -not -path '*/node_modules/*' -not -path '*/.git/*'` — vendored npm changelogs (`node_modules/`, `_prebuilt_nm/`) are NOT project changelogs.
2. **Scope the window**: `git log --oneline --since="<date>"` — last date the repo's docs acknowledged, or ~2 weeks. For the first entry, a generous window (all unrecorded activity) beats a narrow one.
3. **Group commits by theme, don't dump them**: cluster into Keep a Changelog sections (`### Added` / `### Changed` / `### Fixed`) with one bolded feature line per cluster (`**<Feature>** — <what it does>`). A changelog is release notes, not a commit log — 87 commits → ~8-12 clustered bullets.
4. **First-changelog convention**: header states prior history is preserved in git and this file tracks changes from `<date>` onward.
5. **Commit**: `git commit -m "docs: add CHANGELOG.md — release notes for <window>"`.

Also flag a stale `ROADMAP.md` "Last Updated" header when the repo gains major product lines it doesn't mention — note as follow-up; don't rewrite the roadmap mid-development.

## Pitfalls

- **A migration commit ≠ updated docs.** The commit message documents the change for reviewers; docs serve operators. Grep is mandatory — never skip step 1.
- **Architecture diagrams go stale first.** The ASCII flow diagram is usually the last thing updated and the most visible thing wrong.
- **Documenting nonexistent files.** Always `ls` the path before adding it to a Files table. Cheap check, prevents embarrassing READMEs.
- **Multi-agent shared repos.** Sibling agents edit shared files (CHANGELOG.md) mid-session. Use targeted `patch(old_string→new_string)` instead of full-file `write_file` — a targeted replace only touches the matched region, so the patch tool's "modified by sibling subagent" warning is informational, not fatal. Verify with `grep` after patching.
- **Windows path mangling in cron sessions.** `git -C /msys/path` fails, and Windows-native Python mangles `/e/...` → `C:\e\...` (use `E:/...` paths). Full catalog in `windows-cron-msys-path-fix`.
- **patch() can fail to match on CRLF files even when the text looks identical.** The fuzzy matcher normalizes some whitespace but a literal `\r\n` mismatch still defeats it (hit on `OPERATIONS.md` during the Aug 11 sweep — two "match not found" attempts). Fallback: use a Python script that reads the file, normalizes `\r\n`→`\n` for the search, does `content.replace(old_norm, new_norm)`, and writes back with `open(path,'w',encoding='utf-8',newline='')` (preserves original line endings). Grep the section first (`rg -n 'header' file`) to copy the exact on-disk text including blank-line counts — an extra blank line between heading and first bullet broke a match too.

## Verification Checklist

- [ ] `grep -rn "<old-identifier>" docs/ *.md` returns nothing
- [ ] Migration note present in each affected doc
- [ ] CHANGELOG `[Unreleased]` covers the migration commits (SHAs cited)
- [ ] All documented files verified on disk
- [ ] Sibling docs checked for duplicate stale refs
- [ ] Changes committed; SHA reported
