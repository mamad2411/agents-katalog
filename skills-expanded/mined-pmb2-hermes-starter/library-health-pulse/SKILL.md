---
name: library-health-pulse
version: 1.3.6
description: Rotating sweep patterns for scheduled pulse cycles that maintain a skill/artifact library — platform-mismatch audits, draft promotion, category distribution, and cross-pulse verification.
metadata:
  hermes:
    tags: [curation, library, pulse, sweeps, platform-audit, draft-promotion, skill-maintenance]
    triggers: [library health, skill library pulse, platform audit, draft promotion, rotating sweep, skill audit pulse, inventory census, skills inventory, full inventory audit, skills-inventory.md, catalog regeneration, inventory drift]
    related_skills:
    - skill-content-audit
    - discord-report-format
    - recurring-status-checks
author: Hermes Agent
license: MIT
---

# Library Health Pulse

Rotating sweep patterns for agents running scheduled pulse cycles that maintain a skill/artifact library. Extends the general pulse workflow with artifact-specific checks designed to fit in a single pulse window without reading the full library.

## When to Use

- Running a scheduled pulse as a library-owner role (Skillmate, Scribe, curation)
- You have 1 pulse cycle to make progress — not a full deep-dive session
- Previous pulse left a "next action" that needs follow-up

## Rotating Sweeps (Pick ONE per Cycle)

Rotate through these so the library gets broad coverage over 5-6 cycles without burning a whole cycle on any single check.

### Sweep A: Empty SKILL.md Check
```bash
find skills/ -name "SKILL.md" -empty -type f
```
Zero empties = nominal. Any hit = flag for immediate fix (stub content or archive).

### Sweep B: Root Lint + Empty Subdir Check
Check for loose files and orphan embedded directories:

```bash
# Loose .md at root
find skills/ -maxdepth 1 -name "*.md" -type f

# Empty subdirectories under active skills (not category dirs, not .archive)
# These accumulate when a skill's internal organization is abandoned mid-restructure
find skills/ -mindepth 3 -maxdepth 3 -type d -empty ! -path '*/.archive/*' ! -path '*/_drafts/*' ! -path '*/.hub/*'
```

Loose .md at skills/ root should be zero. If > 0, move to `_drafts/` or `_archive/`.
Empty subdirectories under active skills (e.g. `hallmark/macrostructures/`) are clutter from abandoned restructure attempts — delete them.

### Sweep C: Recently-Modified Version Compliance Audit
Identify skills modified since the last audit boundary and run a structured frontmatter check.

**Find boundary:** Use the last PULSE.md entry or the last sweep's boundary file as the `-newer` reference.

```bash
# Version-compliance audit: find recently-modified skills missing the version field
# The version field is the single most common frontmatter omission
boundary="path/to/PULSE.md"
find skills/ -name "SKILL.md" -newer "$boundary" -type f -exec sh -c '
  n=$(echo "{}" | sed "s|./||;s|/SKILL.md||")
  v=$(head -10 "{}" | grep -c "^version:")
  [ "$v" -eq 0 ] && echo "MISSING version: $n"
' \;

# Also check for duplicate frontmatter keys (e.g. two version: lines)
find skills/ -name "SKILL.md" -newer "$boundary" -type f -exec sh -c '
  n=$(echo "{}" | sed "s|./||;s|/SKILL.md||")
  c=$(head -10 "{}" | grep -c "^version:")
  [ "$c" -gt 1 ] && echo "DUP version: $n"
' \;
```

**Spot-check** (pass/fail per skill):
- Valid YAML frontmatter (name, description, version all present, no duplicate keys)
- Platform tags match the host OS
- Content >20 lines (substantive, not a stub)
- Run a full version-compliance pass before any other Sweep C checks — it's the highest-ROI scan

**When FIXING a missing `version:` (not just detecting), insert it ABOVE the `description:` line** — if `description:` is a folded/literal block scalar (`description: >-` or `|`), inserting the new key after it lands INSIDE the block: YAML parses cleanly but `version` silently absorbs the description's indented continuation lines (`version: 1.0.0 Systematic methodology...`) and the description empties — two fields corrupted, zero error (real case Aug 03 2026: `devops/api-provider-integration`, `local-business-revenue`). Pre-scan with `re.search(r"^description:\s*[>|][-+]?\s*$", fm_text, re.M)`; if it matches, insert after `name:` instead. Post-edit, assert exact VALUES not just parseability — block-scalar absorption passes a parse-only check: `fm["version"] == "1.0.0"` and description non-empty. Prefer `skill-library-maintenance`'s `scripts/version-field-audit.py` (inserts after `name:`, block-scalar-safe).

**Simpler universal rule (verified Aug 3 2026):** always insert the missing key immediately AFTER the `name:` line — it sits above `description:` for every description shape (`>-` folded, `|` literal, single-line), so the block-scalar pre-scan is unnecessary. Verified on the 50-skill gstack-family version sweep (all files used `description: |` literal blocks): 50/50 patched, 0 absorption, 0 YAML errors, CRLF intact. **CRLF bonus:** on Windows a plain `read_text()` → string-edit → `write_text()` round-trip preserves CRLF automatically (write_text translates `\n` to `os.linesep`) — byte-level ending handling is needed only for *detecting* endings (`read_bytes()`), not for preserving them on pure-CRLF files.

**Empty block-scalar description variant (Aug 4 2026):** a `description: >-` (or `|`) line with NO continuation lines below it parses as an empty string — YAML is happy, but the skill reports NO_DESCRIPTION and loses description-based discovery. This is the mirror of absorption: the block opener survives but its content was stripped (often by an earlier edit that deleted the indented lines). Real case: `design/service-site-animations` + `devops/model-provider-routing` both had bare `description: >-` immediately followed by `metadata:`. Fix: replace the empty `description: >-` line with a quoted one-liner (`description: "..."`) — the same anchor-replace pattern as other frontmatter fixes. Detection: `validate-frontmatter-lib.py` flags it as NO_DESCRIPTION in the same pass as NO_TRIGGERS.

### Sweep D: Platform Mismatch Audit
```bash
find skills/ -name "SKILL.md" | xargs grep -l "^platforms:" | xargs grep -L "windows"
```
Finds skills that declare platforms but DON'T list Windows. On a Windows host, verify each and archive truly Mac/Linux-only skills. Compare against the previous pulse's flagged list — verify every assumption before acting.

### Sweep E: Draft Promotion Assessment
Read `_drafts/README.md` tier list. Pick one Tier 1 draft and either promote or prune.

**Promotion procedure (7 steps):**
1. **Read the stub** — `read_file('skills/_drafts/<draft-name>.md')`. Understand the concept, gap, and intended category.
2. **Gap-check before authoring** — if the draft's domain overlaps an existing skill, grep the existing skill for the draft's core concepts before promoting. Near-zero hits on the draft's defining terms = genuine gap (promote); dense coverage = mark 🔄 REDUNDANT/absorbed instead (saves a full authoring pass). Real case (Aug 4 2026): `create-market-lead-wholesaling-skill-wit` looked redundant next to `land-wholesaling` — but `grep -io "MAO\|ARV\|after repair value\|offer calculat" land-wholesaling/SKILL.md` returned 1×ARV, 0×MAO/offer-math: land-wholesaling covers vacant-lot deals only, so house wholesaling was a genuine gap → promoted as `market-lead/house-wholesaling`. The grep converts promote-vs-redundant from a guess into a decision.
3. **Author full SKILL.md** — Use `skill_manage(action='create', name='<kebab-name>', ...)`. Include complete frontmatter (name, description, version, platforms, author, metadata.tags, metadata.triggers, metadata.related_skills), at minimum: 5+ procedural steps, reference tables where appropriate, a Verification section, and a Pitfalls section.
4. **Cross-reference related skills** — Set `metadata.hermes.related_skills` to link to 2-4 existing skills in the same domain. This forms discoverable skill clusters. Verify by checking those related skills exist with `skill_view(name)`.
5. **Update draft README stats** — Patch `_drafts/README.md`: mark the promoted draft with the promotion note (e.g. `✅ **PROMOTED** → category/skill-name (date, this pulse)`), decrement `Total stubs` and the relevant tier count, update the status description line.
6. **Delete the promoted draft file** — `rm skills/_drafts/<draft-name>.md` (via terminal).
7. **Log to PULSE.md** — Append a structured pulse entry with Status, Focus, Findings (including library counts), and Next Action.
8. **Append to daily digest** — Use the project's append-digest script (e.g. `python E:/path/to/append-digest.py "Role Name" "- finding"`) to share findings across agents.
9. **Verify deletion** — After step 5, confirm the file is actually gone: `[ -f "skills/_drafts/<draft-name>.md" ] && echo "STALE PROMOTED: still present!" || echo "deleted OK"`. Stale promoted drafts accumulate quickly when this verification is skipped.
- Prune it: if stale 7+ days with TBD content, delete it. Also update the draft README and digest.

### Sweep E.2: Stale Draft Cleanup (Rotating companion check)

Run after Sweep E (or standalone every 3-4 cycles) to catch resolved drafts — marked ✅ PROMOTED **or** 🔄 REDUNDANT in the README — that prior cycles failed to delete:

```bash
# Find draft files marked PROMOTED/REDUNDANT in the README but still on disk
readme="skills/_drafts/README.md"
[ -f "$readme" ] && grep -oP '`\K[^`]+' "$readme" | while read -r stub; do
  f="skills/_drafts/$stub"
  [ -f "$f" ] && echo "STALE RESOLVED: $f — marked PROMOTED/REDUNDANT in README but never deleted"
done
```

If any hits: delete them immediately. Count reflects prior-cycle misses — backlog, not a blocker. The 2026-07-31 pulse found `task-complexity-based-model-tier-assignm.md` still on disk a day after being marked 🔄 REDUNDANT — the REDUNDANT variant of this bug is as common as the PROMOTED one.

**After cleanup, reconcile README stats to physical disk** — README totals drift silently:

```bash
# Physical stub count MUST equal the README's "Total stubs"
ls skills/_drafts/*.md | grep -v README.md | wc -l
# Spot-check per-tier counts against table rows, and that each table row
# starts with a single "|" — broken "|||" rows accumulate from prior patches
```

The 2026-07-31 pulse found the README claiming 25 stubs / Tier 3 = 12 while disk had 24 (Tier 3 = 11) — stats off by one from an earlier unresolved deletion. Fix stats and any `|||` rows in the same pass.

### Sweep E.3: Draft Cluster Consolidation (thin stubs → 1 substantive draft)

The third draft-backlog path alongside promotion (Sweep E) and pruning (Sweep E.2): when multiple `_drafts/` stubs share one domain/intent cluster, merge them into ONE substantive draft instead of promoting or pruning each individually. Real case (Aug 10 2026): 12 design/taste stubs → `_drafts/design-system-prompt-standardization.md` (3.4KB), drafts 22 → 11.

Procedure:
1. **Identify the cluster** — group stubs by domain from filenames + `_drafts/README.md` tier notes. A prior pulse may have flagged a smaller core (Aug 7 flagged "5 design-prompt-template stubs"); re-scan for domain siblings before acting — the actual cluster was 12 design/taste stubs spanning Tier 2 and Tier 3.
2. **Reference-check before archiving** — grep for exact stub FILENAME substrings, never generic concept words: `grep -e "opinion"` noise-matched 19 SKILL.md bodies (common English word) while zero files referenced the actual stub names. 0KB stubs have no content, so only the README can reference them; any real filename hit means another skill's body mentions the idea — read that hit before archiving.
3. **Author the consolidated draft** — `write_file` `_drafts/<umbrella-name>.md` with REAL content (3-4KB minimum): concept, one proposal part per absorbed stub, recommended sequencing, open questions, verification criteria. The deliverable is an actionable proposal, not another 0KB stub — this is what turns a dozen empty names into one promotable artifact.
4. **Archive originals, never delete** — `mkdir -p _drafts/.archive/<consolidation>-YYYY-MM-DD/ && mv <stubs> _drafts/.archive/<consolidation>-YYYY-MM-DD/`. Same reversibility rule as skill archives (Sweep P step 3).
5. **Update `_drafts/README.md`** — remove archived stub rows from their tier tables (an emptied Tier 3 table becomes a one-line pointer note), add the consolidated draft to its tier with `✅ **CONSOLIDATED YYYY-MM-DD**` + absorbed-count note, and reconcile summary stats: `Total = old − N + 1`, tier counts adjusted.
6. **Verify** — physical count (`ls _drafts/*.md | grep -v README | wc -l`) equals the new README `Total stubs`; re-run `scripts/pulse-audit.py` to confirm no collateral frontmatter regressions.

### Sweep F2: Post-Archival Orphan Category Cleanup (After any bulk archive action)

After archiving skills from a shared category directory (e.g., archiving all `apple/` sub-skills to `.archive/apple-YYYY-MM-DD/`), the now-empty category dir may remain with only `DESCRIPTION.md`. This inflates directory counts and confuses future sweeps.

```bash
find skills/ -maxdepth 2 -mindepth 2 -name 'DESCRIPTION.md' ! -path '*/.archive/*' ! -path '*/_drafts/*' | \
  while read f; do
    d=$(dirname "$f")
    remaining=$(find "$d" -mindepth 1 -maxdepth 2 ! -name 'DESCRIPTION.md' 2>/dev/null)
    [ -z "$remaining" ] && echo "ORPHAN: $d"
  done
```

If any orphans found, confirm their content is fully accounted for in `.archive/`, then `rm -rf <dir>`.

### Sweep G: Category Distribution (Periodic — every 5-7 cycles)
```bash
find skills/ -maxdepth 2 -name "SKILL.md" -type f | sed 's|/SKILL.md||; s|.*/skills/||; s|/.*||' | sort | uniq -c | sort -rn
```
Run every 5-7 cycles to detect library shape drift (one category growing too large, dead categories persisting).

### Sweep H: NO_TRIGGERS Regression (Every cycle)

Highest-ROI check. Skills imported from hubs or created without frontmatter miss `metadata.hermes.triggers`, making them invisible to auto-loading.

**Scan BOTH trees.** The loader resolves local skills dir + `config.yaml skills.external_dirs` (NOT profile-local, NOT bundled). A triggerless external-tree file is just as invisible to auto-loading — and stale archived/consolidated names (e.g. `github-code-review`, `codebase-inspection`, `mcp-server-onboarding`) can persist there as loadable files. The 2026-07-31 Scribe pulse found 35/46 external-tree skills triggerless while the local-only scan showed zero — the local pass alone gives a false all-clear. External quick pass (CRLF-safe: `grep -qa`, plain grep silently misses CRLF files):

```bash
for f in $(find <external_dir>/skills -name SKILL.md -not -path '*/.archive/*'); do
  grep -qa 'triggers:' "$f" || echo "NO_TRIGGERS: $f"
done
```

**Fix pattern for bare-frontmatter files** (the recurring hub-import shape): insert a full `metadata.hermes` block (version/author/license + tags/triggers/related_skills) after the `description:` line via Python anchor-replace preserving CRLF (see `hermes-agent-skill-authoring` Pitfall #7 Option E); guard idempotency by skipping files whose frontmatter block already contains `metadata:`; validate with `yaml.safe_load` after each write; then verify by re-running the scan to zero. Prefer patch-in-place — never copy an external-dir skill into the local tree (creates "Ambiguous skill name" collisions).

**External-dir skills are READ-ONLY to `skill_manage`** — `skill_manage(action='patch'|'edit')` refuses with "externally owned and read-only to autonomous curation" for any skill under `config.yaml skills.external_dirs` (e.g. the hermes-config repo). This is a tool-level guard, not a CRLF/cross-profile issue. To fix an external-dir skill: edit the file directly with the standalone `patch()` tool (path = the external repo path, e.g. `C:/Users/<user>/Documents/github/hermes-config/skills/.../SKILL.md`), then `git add` + `git commit` in that repo — the loader reads it live from disk. Verified Aug 3 2026: `hermes-agent-skill-authoring` (external canonical) rejected skill_manage patch; the fix path is file-tool + git commit, same as prior pulses did for version bumps.

**Batch fix with `scripts/batch-fix-notriggers.py`** — when a whole imported family is triggerless (10+ files), hand-editing is slow and CRLF-prone. Fill the FIXES dict (keyed by DIRECTORY name — imported families often differ from their YAML `name:`, e.g. dir `taste-skill` → name `design-taste-frontend`, dir `emilkowalski-motion` → name `improve-animations`) and run the script. It inserts full metadata blocks byte-level, preserving `\r\n`/`\r\r\n`/LF endings, and prints a per-file FIXED line. Verified Aug 2026: 10/10 fixed in one pass (emilkowalski-* ×8 + impeccable + taste-skill). Cross-check `related_skills` targets exist in a tree AND are not the skill itself before writing — a dead ref is worse than missing triggers, and a self-ref (Aug 4 2026: `calcom-selfhosted-ops` metadata block initially listed itself in `related_skills` while hand-building the block) is the same defect class: it parses cleanly, passes existence checks, and only surfaces on review. When authoring a metadata block by hand, never include the skill's own name in its `related_skills`.

```bash
python3 -c "
import yaml, os, glob
root = '.'
missing = []
total = 0
for f in sorted(glob.glob(os.path.join(root, '**', 'SKILL.md'), recursive=True)):
    total += 1
    with open(f, 'r', encoding='utf-8') as fh:
        text = fh.read()
    parts = text.split('---', 2)
    if len(parts) < 3:
        continue
    try:
        data = yaml.safe_load(parts[1])
    except:
        continue
    if not data:
        continue
    meta = data.get('metadata', {})
    if not isinstance(meta, dict):
        continue
    hermes_meta = meta.get('hermes', {})
    if not isinstance(hermes_meta, dict):
        continue
    triggers = hermes_meta.get('triggers', [])
    if not triggers:
        missing.append(os.path.relpath(f, root))
print(f'Total: {total}')
print(f'NO_TRIGGERS: {len(missing)}')
for m in missing:
    print(f'  {m}')
"
```

**Fix by diagnosis:**
- **No metadata block**: Add `metadata:\n  hermes:\n    triggers: [...]\n    tags: [...]\n    related_skills: [...]`
- **Root-level `triggers/tags/related_skills`**: Migrate under `metadata.hermes.*`, remove root-level copies
- **`metadata.triggers` instead of `metadata.hermes.triggers`**: Move one level deeper

Target: **0 NO_TRIGGERS after every cycle.**

### Sweep I: Size Threshold Monitoring (Every other cycle)

Skills over 95KB approach the 100KB hard load limit. Track the 86-95KB watch zone and flag crossers.

**Scan with pathlib, NOT shell `find`** — the MSYS `find` silent-skip failure applies to size scans too (the watch exists to catch skills nobody noticed; a `find` that skips dirs defeats it). Python one-liner over the tree:

```python
from pathlib import Path
root = Path.home() / "AppData/Local/hermes/skills"
for s in sorted(root.rglob("SKILL.md")):
    if ".archive" in s.parts: continue
    sz = s.stat().st_size
    if sz > 86000:
        print(f"{sz:>8,}  {s.parent.parent.name}/{s.parent.name}")
```

**Priority: non-bundled skills first.** Bundled skills (e.g. gstack-* from site-packages) can't be modified — only note their growth for upstream awareness. The *actionable* targets are local-tree skills near the limit; they're the ones that can actually have sections extracted to `references/`. Real case (Aug 4 2026): the watch had tracked only gstack for cycles, while `market-lead/land-wholesaling` (91.6KB) and `productivity/intelligence-pulse` (91.4KB) crossed 90KB unnoticed — both local, both trimmable. When the 95KB+ list is all bundled, scan the 86-95KB zone for local crossers and flag those for extraction instead.

**Action on breach:** Monitor trend in PULSE.md. If a LOCAL skill is over 95KB for 2+ consecutive cycles, extract the largest section to `references/`. **Extract vendored appendices FIRST** — a self-contained "APPENDICES" block (install commands, canonical source links, code skeletons) is the cleanest extraction target: zero body cross-references to rewire, numbered section flow preserved, and it usually yields 5-10KB in one cut. Real case (Aug 7 2026): `taste-skill` (dir `taste-skill`, YAML name `design-taste-frontend`) 88.7KB → 81.5KB in one pass — appendices A/B/C (7.5KB) moved verbatim to `references/appendices.md`, body replaced with a short pointer section naming the reference file and why it moved. Verification after any extraction: frontmatter parses, every numbered section header still present (assert each `## N.` header exists in the trimmed body), and the reference file contains the expected appendix headers. The pointer section keeps the vendored content discoverable by the loader.

**Cross-skill consumers need their OWN pointer — `related_skills` chains do not count.** When the extracted section feeds ANOTHER skill's workflow (most commonly a cron consumer that references the owning skill), that consumer needs a direct pointer line in ITS body to the new reference file — a `related_skills` entry pointing at the owning skill is not a discoverable pointer for the reference. Real case (Aug 11 2026): `intelligence-pulse` extracted the 72-line "Morning Brief Consolidation (7:01 AM EST)" section to `references/morning-brief-consolidation.md` and indexed it in its own Reference-files list, but `productivity/quiet-hours-pulse-digest` — the skill that RUNS that 7:01 AM cron — only linked `intelligence-pulse` via `related_skills`; its "Morning Brief Cron Job" section had no pointer to the new ref, so the next-cycle "spot-check the ref for the cron consumer" surfaced a gap instead of a confirmation. Grep for consumers before declaring an extraction done: `grep -ral '<owning-skill-name>' skills/*/*/SKILL.md`, read each hit's workflow section, and add a direct `references/<file>.md` pointer wherever the consumer describes the workflow the extracted section feeds. The post-extraction spot-check verifies BOTH (a) the ref file is intact + indexed in the owning skill, AND (b) every consumer skill's relevant section carries a direct pointer.

**Dedup-against-references FIRST — free bytes before extracting anything.** Before extracting new material, inventory the skill's existing `references/` files and diff inline sections against them: if an inline section duplicates a reference (common after a consolidation where the ref was created but the inline copy was never removed), replace the inline block with a pointer. **Never lose unique sub-sections** — append any inline-only sub-sections (role tables, unit economics, card-display specs) to the reference file BEFORE removing the inline copy, then verify zero residual probes of the moved headers in the trimmed SKILL.md. Real case (Aug 7 2026, same cycle as the taste-skill extraction): `market-lead/land-wholesaling` 91.6KB → 86.9KB (-4.6KB, below the 88KB watch line) by deduping two inline sections — Lee County Quick Reference (→ existing `references/lee-county-resource-map.md`) and the 93-line VA Operations Framework (→ `references/va-operations-framework.md`, grown 4.9KB→6.4KB after appending the 3 unique sub-sections first). Same CRLF-safe byte-level pathlib surgery as extraction, but no new file and no cross-reference rewiring — strictly easier than extraction, so check `references/` before drafting new appendix moves.

**Quantify overlap before choosing extract-vs-merge** — when a candidate inline section sits next to existing `references/` files, compute shared-sentence overlap instead of guessing: `sec_sent = set(re.split(r'(?<=[.;])\s+', section)); ref_sent = set(re.split(r'(?<=[.;])\s+', ref_text)); len(sec_sent & ref_sent)/len(sec_sent)`. Near-zero overlap (≤5%) → extract verbatim to a NEW `references/<topic>.md` (real case Aug 10/11 2026: `software-development/twenty-crm-administration` 90.0KB — the 433-line "View Fields (Columns)" section (24.4KB) scored 1% shared sentences vs existing `references/view-field-configuration.md` (a June batch-memo, complementary) → moved verbatim to `references/view-fields-columns.md`; SKILL.md 90,042B → 65,609B, version bumped 1.9.0→1.10.0, 42 triggers intact). Substantial overlap → the land-wholesaling merge-dedupe path instead. The overlap fraction converts extract-vs-merge from a guess into a decision, same role as the Sweep E gap-check grep.

**Trimmed skills stay on the watch — re-cross is the norm, not the exception.** Two Aug 10/11 2026 cases: `productivity/intelligence-pulse` was trimmed 91.4→87.1KB (Aug 7) yet re-crossed to 88.2KB within 4 days (other agents append sections); `twenty-crm-administration` crossed 90KB purely from routine Aug-10 edits between pulses, with no size-related maintenance touching it. Rules: (a) keep every trimmed skill on the size watch for 3+ cycles after the trim; (b) trim to WELL under the line (target ≤80KB), not barely under — 87.1KB re-crosses in a single edit; (c) cross-reference the recently-modified list (`find -mtime`) against the size scan — recently-edited large skills are the highest-risk crossers.

**Trim verification, byte-level** (Aug 10/11 2026 run): after extraction assert (1) frontmatter parses and version bumped, (2) a unique marker phrase from the removed section is ABSENT from the trimmed SKILL.md (`assert 'Omitting it causes a NOT NULL constraint violation' not in c2`), (3) the reference file contains the expected section markers, (4) H2 heading sequence still sane, (5) CRLF preserved via `read_bytes()` count. Absence-assert beats presence-assert: it proves the body is actually gone, not just that a pointer was added.

**New reference files can come out MIXED-ending** — a header written with `\n` concatenated onto an extracted CRLF section produces a ref file with two line-ending families (LF header + CRLF body). Real case (Aug 11 2026): `intelligence-pulse`'s new `references/morning-brief-consolidation.md` had an LF 4-line header over a CRLF 72-line body; `read_text()` universal-newline hides it, `file` reports it, and downstream tooling chokes. Fix: after assembling any new reference file, normalize the WHOLE file to the source's ending family byte-level — `raw.replace(b'\r\n', b'\n').replace(b'\n', b'\r\n')` (or the `\r\r\n`-aware variant) — then assert zero residual bare LFs. Normalizing the reference file is part of the trim, not an optional cleanup.

### Sweep J: Root-Level YAML Hygiene (Every 5-7 cycles)

Checks for `tags/triggers/related_skills` at YAML root instead of under `metadata.hermes`. These are silently ignored by inference but fool grep-based scans.

```bash
python3 -c "
import yaml, os, glob
root = '.'
bad = []
for f in sorted(glob.glob(os.path.join(root, '**', 'SKILL.md'), recursive=True)):
    with open(f, 'r', encoding='utf-8') as fh:
        text = fh.read()
    parts = text.split('---', 2)
    if len(parts) < 3:
        continue
    try:
        data = yaml.safe_load(parts[1])
    except:
        continue
    if not data:
        continue
    root_keys = [k for k in ['triggers', 'tags', 'related_skills'] if k in data]
    meta = data.get('metadata', {})
    if isinstance(meta, dict) and 'hermes' in meta and root_keys:
        name = data.get('name', os.path.basename(os.path.dirname(f)))
        print(f'ROOT KEYS in {name}: {root_keys}')
        bad.append(f)
    elif 'metadata' not in data and root_keys:
        name = data.get('name', os.path.basename(os.path.dirname(f)))
        print(f'NO METADATA BLOCK in {name}: root keys {root_keys}')
        bad.append(f)
print(f'Total with issues: {len(bad)}')
"
```

**Fix:** If `metadata.hermes` exists, move root-level keys under it. If no metadata block exists, add a full `metadata.hermes.{triggers,tags,related_skills}` block. Run after hub imports or every 5-7 cycles.

### Sweep K: Full Inventory Census (Every 10-15 cycles or on demand)

Produce a comprehensive multi-dimensional snapshot of the entire skill library — not just category counts but source provenance, version-field compliance, SKILL.md completeness, symlink state, and bundled-vs-custom breakdown. More expensive than other sweeps but produces the richest trend data.

**When to use:** After major import/restructure operations, or on explicit "audit the skills inventory" requests. Also useful as a quarterly deep-dive baseline.

```bash
cd ~/AppData/Local/hermes/skills

# 1. Count SKILL.md at every depth
echo "=== SKILLS WITH SKILL.MD ==="
find . -name "SKILL.md" -not -path './.archive/*' -not -path './.curator_backups/*' -not -path './.hub/*' -type f | wc -l

# 2. Top-level vs subdirectory split
echo "=== TOP-LEVEL DIRS ==="
ls -1d */ 2>/dev/null | grep -v '^\.' | wc -l
echo "=== SUBDIRECTORIES (category containers) ==="
find . -maxdepth 3 -mindepth 2 -name "SKILL.md" -type f 2>/dev/null | sed 's|/SKILL.md||' | xargs -I{} dirname {} | sort -u | wc -l

# 3. Symlink audit
echo "=== SYMLINKED SKILLS ==="
find . -maxdepth 1 -type l 2>/dev/null -printf '%f\n' | sort

# 4. Source provenance: bundled manifest
echo "=== BUNDLED MANIFEST ==="
cat .bundled_manifest 2>/dev/null || echo "(no bundled manifest)"

# 5. Version-field compliance
echo "=== SKILLS MISSING VERSION FIELD ==="
find . -name "SKILL.md" -not -path './.archive/*' -not -path './.curator_backups/*' | \
  while read f; do
    n=$(echo "$f" | sed 's|./||; s|/SKILL.md||')
    v=$(head -10 "$f" | grep -c "^version:")
    [ "$v" -eq 0 ] && echo "$n"
  done | sort

# 6. Category distribution (rich format)
echo "=== CATEGORY DISTRIBUTION ==="
find . -name "SKILL.md" -type f -not -path './.archive/*' -not -path './.curator_backups/*' | \
  sed 's|/SKILL.md||; s|/[^/]*$||; s|^\./||' | \
  grep -v '^[^/]*$' | sed 's|/.*||' | sort | uniq -c | sort -rn
```

**Cross-dimensional analysis** — use Python for the richer breakdown:

```python
import os, yaml, json
from pathlib import Path
from collections import defaultdict

SKILLS = Path('~/AppData/Local/hermes/skills').expanduser()

data = {
    'total_dirs': 0,
    'with_skill_md': 0,
    'category_containers': 0,
    'leaf_skills': 0,
    'symlinked': 0,
    'with_version': 0,
    'without_version': 0,
    'with_metadata_hermes': 0,
    'without_metadata_hermes': 0,
    'size_distribution': defaultdict(int),
}

for entry in sorted(SKILLS.iterdir()):
    if not entry.is_dir() or entry.name.startswith('.'):
        continue
    data['total_dirs'] += 1

    if entry.is_symlink():
        data['symlinked'] += 1

    skill_file = entry / 'SKILL.md'
    has_skill = skill_file.exists()

    has_subskills = any(
        (entry / sub).is_dir() and (entry / sub / 'SKILL.md').exists()
        for sub in os.listdir(str(entry))
    )

    if has_skill:
        data['with_skill_md'] += 1
        data['leaf_skills'] += 1

        text = skill_file.read_text(encoding='utf-8')
        parts = text.split('---', 2)
        if len(parts) >= 3:
            try:
                fm = yaml.safe_load(parts[1])
                if isinstance(fm, dict):
                    data['with_version' if fm.get('version') else 'without_version'] += 1
                    meta = fm.get('metadata', {}) or {}
                    hermes = meta.get('hermes', {}) if isinstance(meta, dict) else {}
                    bucket = 'with_metadata_hermes' if hermes else 'without_metadata_hermes'
                    data[bucket] += 1
            except yaml.YAMLError:
                pass

        sz = skill_file.stat().st_size
        if sz == 0:           data['size_distribution']['empty'] += 1
        elif sz < 1000:       data['size_distribution']['<1KB'] += 1
        elif sz < 10000:      data['size_distribution']['1-10KB'] += 1
        elif sz < 50000:      data['size_distribution']['10-50KB'] += 1
        elif sz < 95000:      data['size_distribution']['50-95KB'] += 1
        else:                 data['size_distribution']['95KB+'] += 1

    if has_subskills:
        data['category_containers'] += 1
        data['leaf_skills'] -= 1

# Report
print(f"Total directories:            {data['total_dirs']}")
print(f"Category containers:           {data['category_containers']}")
print(f"Leaf skills (has SKILL.md):   {data['leaf_skills']}")
print(f"Symlinked:                    {data['symlinked']}")
print(f"With version field:           {data['with_version']}")
print(f"Without version field:        {data['without_version']}")
print(f"With metadata.hermes:         {data['with_metadata_hermes']}")
print(f"Without metadata.hermes:      {data['without_metadata_hermes']}")
print(f"Size distribution:")
for label in ['empty', '<1KB', '1-10KB', '10-50KB', '50-95KB', '95KB+']:
    c = data.get('size_distribution', {}).get(label, 0)
    if c:
        pct = 100.0 * c / max(data['with_skill_md'], 1)
        print(f"  {label:>8s}: {c:4d} ({pct:.1f}%)")
```

**Baseline reference:** `references/inventory-census-baseline-2026-07-30.md` captures the first full-library census produced July 30, 2026 with domain-level breakdown, source provenance, and quality findings. Compare future census runs against it to measure drift.

### Sweep L: Legacy-Tree vs Load-Path Reconciliation (every 3-4 cycles)

When a legacy tree exists outside the load path (e.g. `~/.hermes/skills/` while HERMES_HOME is `~/AppData/Local/hermes/`), find skills with NO copy in the load path before bulk-deleting anything. Load path = local skills dir + `config.yaml skills.external_dirs` ONLY — trees outside it are inert for loader resolution (no collisions) but can hold unique content that would be silently lost.

**Normalize ALL trees to the same name shape BEFORE `comm` — external-dir paths are repo-root-relative and carry a `skills/` prefix:**

```bash
# Read load path first
grep -A8 external_dirs ~/AppData/Local/hermes/config.yaml

# Local tree:  skills/software-development/plan  ->  software-development/plan
find ~/AppData/Local/hermes/skills -name SKILL.md -not -path '*/.archive/*' | sed 's|.*/skills/||;s|/[^/]*$||' | sort > /tmp/local.txt
# External tree:  skills/software-development/plan  ->  software-development/plan  (strip the "skills/" prefix!)
find ~/Documents/github/hermes-config -name SKILL.md -not -path '*/.git/*' -not -path '*/.archive/*' | sed 's|.*/hermes-config/skills/||;s|/[^/]*$||' | sort -u > /tmp/ext.txt
# Legacy tree:  .hermes/skills/software-development/plan  ->  software-development/plan
find ~/.hermes/skills -name SKILL.md -not -path '*/.archive/*' | sed 's|.*/skills/||;s|/[^/]*$||' | sort > /tmp/legacy.txt

cat /tmp/local.txt /tmp/ext.txt | sort -u > /tmp/loaded.txt
echo "=== TRUE LEGACY-ONLY (not in load path) ==="
comm -23 /tmp/legacy.txt /tmp/loaded.txt
```

**Pitfall — false "legacy-only" hits from prefix mismatch:** using `sed 's|.*/skills/||'` on the external list leaves the `skills/` prefix on those names (`skills/software-development/plan` vs `software-development/plan`), so `comm` flags every shared skill as legacy-only. Real case (2026-08-01): first pass reported **15 legacy-only**; after fixing the external-side strip to `s|.*/hermes-config/skills/||` only **2** were actually missing. If a diff claims a double-digit count of legacy-only skills, re-check the normalization before acting.

**Resolve each true legacy-only skill:**
- **Promote** substantial skills (SKILL.md + `references/` + `templates/`) into the load path via `cp -r`, then validate frontmatter (`yaml.safe_load`). A 15KB+ skill with refs/templates is a real artifact, not clutter.
- **Archive** platform-irrelevant or superseded variants (e.g. macOS-only skill on a Windows host, superseded by a generic umbrella) — move to `.archive/` rather than delete.
- **Spot-check "duplicate" pairs with `cmp -s`** to classify identical vs diverged — diverged does NOT mean the legacy copy is newer; check version field and content depth to pick the canonical side (load-path copy is canonical in practice).
- Re-count after: `find <load-path> -name SKILL.md | wc -l`; log promote/archive decisions in PULSE.md.

### Sweep M: Metadata-Only Frontmatter Check (Every 5-7 cycles)

Checks for skills whose frontmatter has NO root `name`/`description` — everything (`tags`/`triggers`/`related_skills`/`version`/`author`/`license`) nested under `metadata.hermes`. The loader falls back to the directory name as the description, failing the validator's hard `name`/`description` requirements and silently breaking description-based discovery. These skills still trigger-load (the nested block is read correctly), so only listings/discoverability degrade — easy to miss.

**Detection — frontmatter-only YAML parse is authoritative. Do NOT use whole-file greps for this class:** `grep -ral '^triggers:'` false-positives on YAML code blocks in skill bodies (Aug 2 2026: `gstack-skillify` matched a body example while its parsed frontmatter had 0 root keys). The definitive scan is `scripts/validate-frontmatter-lib.py` — it now reports NO_NAME/NO_DESCRIPTION in the same one-pass run as NO_TRIGGERS/parse errors/root-level keys.

**Fix — rebuild root fields from the nested block, preserve body + line endings:**
```python
import pathlib, yaml
p = pathlib.Path("SKILL.md")
c = p.read_text(encoding="utf-8")
rest = c[3:]; close = rest.find("\n---")
h = yaml.safe_load(rest[:close])["metadata"]["hermes"]
new_fm = (
    f"name: {p.parent.name}\n"
    f"description: \"<one-line Use-when... from body>\"\n"
    "version: 1.0.0\nauthor: Hermes Agent\nlicense: MIT\n"
    "metadata:\n  hermes:\n"
    f"    tags: [{', '.join(h['tags'])}]\n"
    f"    triggers: [{', '.join(h['triggers'])}]\n"
    f"    related_skills: [{', '.join(h['related_skills'])}]\n"
)
p.write_text("---\n" + new_fm + "---\n" + rest[close + 4:], encoding="utf-8")
```

**Real case (Aug 2 2026):** 4 skills found metadata-only (`media/youtube-content`, `sales/scroll-world-demo-sales`, `web-development/home-service-sites`, `web-development/scroll-world-hermes`). 3 unique-content → fixed with the recipe above and verified (name/desc/version/triggers all present). 1 (`youtube-content`) was a stale duplicate of consolidated `youtube` → archived instead of fixed. **Before archiving a broken-frontmatter skill, check cross-references + support files:** `youtube-content` had `scripts/fetch_transcript.py` that looked load-bearing, but canonical `youtube` carried its own copy (7 refs) — safe to retire. Post-fix tree scan returned 0 offenders.

### Sweep N: Archived-Skill Restoration (when gap analysis flags one)

The dream-cycle gap analysis occasionally flags a curator-archived skill worth restoring (real case Aug 7 2026: `the operator-soul` — substantive identity/decision-framework content, `platforms: [windows]`, valid frontmatter, but archived with NO live copy). Decision heuristic:

- **Restore** if: content is substantive (not a stub), platform matches host, frontmatter is valid, and no live copy exists anywhere in the load path.
- **Leave archived / prune** if: content is stale (superseded by memory/profile), platform-irrelevant, or a live duplicate exists.

Workflow:

```bash
hermes curator restore <skill-name>   # restores to skills/<name> at top level
```

- `hermes curator list-archived` lists TOP-LEVEL archive dirs (often category names) — the skill may be nested (e.g. `autonomous-ai-agents/the operator-soul`); `restore` resolves by bare skill name regardless.
- **Verify the restore landed:** `find ~/AppData/Local/hermes/skills -maxdepth 3 -name <name> -type d -not -path '*/.archive/*'` shows the live copy, and SKILL.md is intact (frontmatter + body). Same "verify, don't trust the log" rule as archiving.
- **Don't confuse profile SOUL.md files** (`~/AppData/Local/hermes/SOUL.md`, `profiles/*/SOUL.md`) with a missing skill — they are profile identity files, separate from skill archives.
- Duplicate archive copies (category archive + collision-sync snapshot) are normal — restore from either; the CLI handles resolution.

Real case: gap analysis flagged `the operator-soul` archived in two spots (`.archive/autonomous-ai-agents/` and `.archive/collision-sync-2026-08-05/`), no live copy. `hermes curator restore the operator-soul` → `skills/the operator-soul`, verified intact.

### Sweep O: Catalog Regeneration — hermes-config `skills-inventory.md` (after any bulk skill change)

The hermes-config repo's `docs/reference/skills-inventory.md` catalogs the whole library (local shared tree + external tree, deduped). It goes stale FAST when multiple agents touch skills between pulses — real case (Aug 7 2026): 540 → **566 skills / 176 categories in 3 days** (+9 new skills from Skillmate syncs, +17 newly-archived from a system tidy, +1 category). The catalog is only as fresh as the last regen; treat it as drift-prone, not authoritative.

**Regenerate + verify drift:**
```bash
cd ${USER_HOME}/Documents/github/hermes-config   # relative paths avoid MSYS issues
python scripts/gen-skills-inventory.py            # prints Total/Categories/Errors/Missing
git diff --stat docs/reference/skills-inventory.md
git diff docs/reference/skills-inventory.md | grep -E "^[-+]\*\*"   # header count change
```

**Classify the delta** (don't guess what moved): diff the category table for per-category changes, then a name-set diff over table rows separates ADDED from REMOVED and surfaces archive growth (`.archive` count rising = recent archivals). New skills appear as new `| name | desc |` rows; a renamed skill shows as add+remove of the same category.

**Cascade the count — grep every referencer, not just the inventory:**
```bash
grep -rn "<old_total>" README.md ECOSYSTEM.md docs/README.md docs/reference/README.md
```
Real case Aug 7 2026: **5 stale references** across `README.md` ×2, `ECOSYSTEM.md` ×2 (skills + categories rows), `docs/reference/README.md` (also carries a scan date — bump it). Patch each with the standalone `patch()` tool (CRLF-safe). Add a CHANGELOG entry under `[Unreleased]` → `### Docs` with the delta breakdown (new skills list + archive count), commit, push.

**Pitfalls:** run the generator from the repo cwd with a RELATIVE script path — `python /e/...` MSYS forms fail on Windows python (see `cron-script-path-resolution`). Re-run after EVERY bulk skill change (Skillmate syncs, archive actions, renames), not just when a pulse has spare time — 3 days of multi-agent activity produced a 26-skill swing.

**Commit conventions for the hermes-config docs pulse (verified across ~10 pulses, Aug 2026):**
- **Message format:** `docs: CHANGELOG gap-fill — <one-line description> (<shortsha>), Scribe pulse <YYYY-MM-DD>` (e.g. `38b4d24`, `e7caa79`, `bcc10a4`, `d67d6d5`). Do NOT use `docs(changelog):` scoped prefixes — the established convention is the flat `docs:` + `gap-fill` phrase.
- **Stage ONLY `CHANGELOG.md` — never `git add -A` / `git commit -am`.** The repo carries persistent working-tree noise (`dashboard/report.html` modified, untracked `docs/findings/system-tidy-*` dirs) that is NOT Scribe scope; a blanket add drags it into the docs commit. Real case Aug 11 2026: `dashboard/report.html` had 214 lines of churn; `git add CHANGELOG.md` kept the commit to 5 insertions.
- **Push immediately** (`git push origin master`) so the next pulse starts from a clean base; verify with `git status --short` that only known noise remains.
- **Reading CHANGELOG.md with offset/limit pagination is fine for `patch()`** — the tool's "partial view" warning is about `write_file` truncation; `patch()` operates on the on-disk file and the warning is harmless (confirmed Aug 11 2026).

### Sweep P: Within-Tree Name-Collision Scan (Every 3-4 cycles)

Same-name SKILL.md pairs INSIDE one tree break `skill_view` resolution ("Ambiguous skill name" — the load-breaking class documented in `hermes-agent-skill-authoring` Pitfall #17). Cross-tree sweeps (Sweep L) never catch these: they compare load path vs external/legacy trees, not load-path vs itself. First full within-tree scan (Aug 8 2026) found **4 collisions that had survived every prior sweep** — including an Aug-4 trigger-fix pass that patched the nested copies (all 4 share that sweep's 16:10:08 mtime) without noticing the stale roots that shared their names.

**Scan — group by frontmatter `name:` (not directory name), pathlib not shell `find`:**

```python
import pathlib, yaml, collections, os
root = pathlib.Path(os.environ['USERPROFILE']) / 'AppData/Local/hermes/skills'
names = collections.defaultdict(list)
for p in root.rglob('SKILL.md'):
    if '.archive' in p.parts or '_drafts' in p.parts: continue
    c = p.read_text(encoding='utf-8', errors='replace')
    rest = c[3:] if c.startswith('---') else c
    close = rest.find(chr(10)+'---')
    try: fm = yaml.safe_load(rest[:close] if close > 0 else rest) or {}
    except Exception: continue
    if isinstance(fm, dict): names[fm.get('name','?')].append(str(p))
for n, ps in names.items():
    if len(ps) > 1:
        print(f'COLLISION {n}:')
        for p in ps: print(f'  {p}')
```

Dir name ≠ frontmatter name in import families (e.g. dir `lm-evaluation-harness` → `name: evaluating-llms-harness`), so grouping must use the parsed YAML `name:` field, not `p.parent.name`.

**Consolidation procedure** (only for genuine duplicates — same description/domain; gstack browse/qa/review trio is the known intentional platform-divergent exception):
1. **Determine canonical** — newer mtime + higher `version:` + body matching current tool docs wins. Cross-check which copy carries the last fix-sweep mtime — the one prior sweeps chose to patch is the maintained one.
2. **Merge unique metadata into canonical FIRST** (byte-level pathlib, preserve LF/CRLF — `hermes-agent-skill-authoring` Pitfall #7 Option E): union richer `triggers:`, add missing `author`/`license`, keep non-empty `related_skills`. Grep canonical for each root-only body bit before declaring it unique — the newer copy often already contains it (Aug 8 2026: `computer-use` canonical already had the web-automation note; only metadata was root-unique).
3. **Archive the stale copies** — `mkdir -p .archive/dupe-consolidation-YYYY-MM-DD/ && mv <stale-dir> .archive/dupe-consolidation-YYYY-MM-DD/<name>-dupe`. Reversible; never delete.
4. **Re-run scan to zero** — 0 non-exempt collisions; then re-run the full-tree audit (Aug 8 2026: 463 active after 4 archives, 0 YAML errors, 0 missing version/triggers). Confirm remaining name refs are body-text documentation-level mentions, not dir deps.

## Cross-Reference Previous Pulse

### One Action Per Cycle

Do not let analysis crowd out action. Pick exactly one:
- Archive N platform-mismatched skills
- Promote 1 draft from Tier 1
- Patch 1 skill with missing version field
- Prune N stale drafts (7+ days idle, TBD content)
- Consolidate a thin-stub cluster into 1 substantive draft (Sweep E.3)
- Add 1 reference file under an existing umbrella
- **Fix NO_TRIGGERS regressions (Sweep H — highest ROI)**
- **Size threshold extraction (Sweep I)**

The previous pulse's "Next Action" is this cycle's first todo:

1. **Verify flags from last cycle** — If the last pulse flagged skills as "Mac-only" or "platform-mismatched", read their actual `platforms:` frontmatter before acting. **Do not trust the flag verbatim.** A skill tagged `platforms: [linux, macos, windows]` is NOT Mac-only.
2. **Report corrections** — If you find a prior pulse made an incorrect assumption, surface it. Corrections build trust and improve future pulse accuracy.
3. **Trend the three numbers** — Active SKILL.md count, archived count, draft count. 3+ cycles of data reveals growth/shrinkage trends.

## Report Format

Pulse entry for PULSE.md append:
```
## Pulse @ YYYY-MM-DD HH:MM TZ
- **Status**: 🟢 Nominal / 🟡 Attention / 🔴 Issue Found
- **Focus**: [which sweep + what action]
- **Findings**:
  - ✅ action taken | outcome
  - ✅ sweep result | key finding
  - ✅ correction from prior pulse | if any
- **Next Action**: [one concrete item for next cycle]
```

Discord delivery (via `discord-report-format`):
```
🔵 **ROLE PULSE** | timestamp
━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 LIBRARY STATE
| Metric | Value |
|--------|-------|
| Active SKILL.md | N |
| Archived | N |
| Drafts | N |
| Empty SKILL.md | N |

📊 RECAP
✅ action | outcome
✅ finding | detail

━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 NEXT ACTIONS
- One item for next cycle

━━━━━━━━━━━━━━━━━━━━━━━━━━
🔍 Checked: timestamp | sweep completed
```

## Pitfalls

- **Do NOT trust prior pulse's platform flags verbatim** — read the actual frontmatter.
- **Do NOT re-read the full library every cycle.** Rotate sweeps. One sweep + one action sustains health.
- **Do NOT skip reporting corrections.** If you found a previous pulse was wrong, say so.
- **Do NOT count every skill on every pulse** — just the three trend numbers.
- **Do NOT trust shell `find` for authoritative SKILL.md counts on MSYS/Windows — it silently skips some directories.** Aug 3 2026: `find` counted **431** active SKILL.md while pathlib `rglob` found **462** — a 31-skill undercount on the live load path (same failure class that made prior legacy-tree diffs miss 2 skills, Aug 1 2026). The gap is invisible — no error, just wrong totals that propagate into trend numbers and "legacy-only" conclusions. Any count that drives a decision (Sweep K census, Sweep L diffs, trend numbers) must come from Python `pathlib.rglob('SKILL.md')` or `os.walk`, never shell `find`. Cross-check: if a pulse's active-count suddenly drops without archives, suspect `find`, not deletion.
- **Do NOT use depth-limited `glob('*/*/SKILL.md')` for library counts — it silently misses 3+ level nesting.** Aug 11 2026: a pulse audit globbed `*/*/SKILL.md` and reported 321 active SKILL.md — that figure was category-level ONLY (321 `category/skill/SKILL.md`), missing all 136 top-level skills (`taste-skill/SKILL.md`, `skill-crossref-hygiene/SKILL.md`, etc.) and 12 nested skills. The undercount then propagated into the PULSE.md entry and the trend numbers. Rules: (a) always use recursive `rglob('SKILL.md')` (or `os.walk`) for counts — `glob('*/*/SKILL.md')` is only valid for flat 2-level trees; (b) if a depth-limited scan and a recursive scan disagree, the recursive one is ground truth; (c) when reporting a count that looks low vs prior pulses, sanity-check against `find | wc -l` before logging it; (d) **break out depth components when a count looks off** — the full-tree breakdown is the diagnostic: `rglob` counts by `len(parts)` (e.g. 136 top-level + 321 category + 12 nested = 469), and a "find saw N" claim should be re-verified against `rglob` because `find` undercounts on this tree (Aug 11 2026: `find` saw 438 while `rglob` saw 469 — a 31-skill silent skip, same signature as the Aug 3 case above).
- **Do NOT attempt a full content-depth audit in a pulse window.** The detailed 10-check audit belongs to dedicated sessions. Pulsing is for lightweight maintenance.
- **Do NOT use `head -N`-bounded grep scans for field presence.** Verbose frontmatter pushes `triggers:` past line 25 — Aug 2 2026: `comfyui` (line 26) and `teams-meeting-pipeline` (line 27) were both false-flagged NO_TRIGGERS by a `head -25` scan; both were fine. **Recurred Aug 3 2026 with `head -20`** — 9 clean skills false-flagged (ai-video-pipeline, comfyui, scroll-world-content, fal-recipes, gstack/review, gstack-review, teams-meeting-pipeline, python-import-debugging, simplify-code); the YAML scan showed 458/458 with triggers, 0 parse errors. **Recurred Aug 8 2026 with `head -5` on the VERSION field** — block-scalar descriptions (`description: >-` with 4-5 continuation lines) push `version:` to line 7+, so a `head -5` version-compliance scan false-flagged 20+ compliant skills as "missing version" (all 20 were fine; pathlib ground truth showed 0 missing). The version field is NOT safe from this failure either — every head-bounded scan for ANY field is suspect. Hand-rolled head/grep scans keep resurfacing in pulses a week apart — run `scripts/validate-frontmatter-lib.py` (or the Sweep H inline YAML scan) instead of writing a new grep each cycle. Grep the full file (`grep -qa 'triggers:' "$f"`) or run the definitive YAML-level scan — `scripts/validate-frontmatter-lib.py` in this skill reports NO_TRIGGERS, NO_NAME/NO_DESCRIPTION (metadata-only frontmatter class), YAML parse errors, root-level keys, duplicate keys, and >95KB in one pass over any skills tree (exit 1 on defects). The YAML-level scan also surfaces the real regressions head-scans bury: same cycle it caught `integrations/knowledge-mcp-integration` (root-level tags/triggers/related_skills + dead `mcp-server-onboarding` related_skills link — fix dead refs while migrating, a dead ref is worse than missing triggers).
- **Do NOT count NO_TRIGGERS with `grep -Lq` inside a loop.** `grep -Lq 'triggers:' "$f" && echo "$f"` is broken: `-q` makes grep exit 0 on the FIRST match while `-L`'s file listing is suppressed entirely — the combination inverts to "echo files that HAVE the pattern". Observed Aug 2 2026: 427/427 false positives from this exact pattern. Count with `grep -rL 'triggers:' <dir>` (no `-q`), the Sweep H per-file `grep -qa 'triggers:' "$f" || echo` check, or the YAML-level scan (`scripts/validate-frontmatter-lib.py`) — the gold standard.
- **Do NOT append PULSE.md/digest entries containing markdown backticks via `python -c "..."` in bash.** Backtick-wrapped tokens (skill names, file paths) are command-substituted by the shell before Python sees them, silently writing holes into the appended entry. Observed Aug 2 2026: a PULSE.md entry lost every backtick-wrapped token (`` `integrations/knowledge-mcp-integration` `` became an empty string); repaired with the standalone `patch()` tool. **Recurred Aug 8 2026** — a `python -c "..."` append with backtick-wrapped skill names executed them as shell commands (`computer-use: command not found`, `author: command not found`, etc.) and wrote the mangled noise into PULSE.md; only caught by a post-append corruption check. Safe alternatives: (a) `write_file` the entry to a temp `.txt` file and have the script read + append it — zero shell interpolation; (b) `patch()` anchored at the file's end; (c) single-quote the `-c` string or drop the backticks. **Also:** python `open(..., 'a')` writes LF lines into CRLF logs (PULSE.md is CRLF) — normalize afterwards with `c.replace('\r\n','\n').replace('\n','\r\n')` (or the `'\r\r\n'`-aware variant) so the log stays single line-ending. **Heredoc is NOT a safe alternative** — `cat >> PULSE.md << 'EOF'` with `&` anywhere in the entry body trips the terminal tool's backgrounding guard (exit -1, "Foreground command uses '&' backgrounding", nothing written) and backtick content still risks interpolation in unquoted heredocs. **Repair pattern (verified Aug 8 2026):** when a mangled append lands, truncate at the last clean anchor — `idx = c.rfind('## Pulse @ <last-clean-timestamp>')` — keep `c[:idx]`, then reconstruct the tail by writing the restored + new entries to temp files with `write_file` and appending them from a quoted heredoc `python - << 'PYEOF'` (no interpolation, reads temps from disk). Verify with a corruption probe before declaring done: `'command not found' in final or 'Is a directory' in final` must be False.
- **Verify CRLF preservation with `read_bytes()`, never `read_text()`.** Python's `read_text()` applies universal-newline translation, so a post-patch check like `'\r\n' in path.read_text()` reports CRLF as lost even when the file on disk is intact. Observed Aug 3 2026: a byte-preserving patch was "verified" via `read_text()` which claimed `CRLF preserved: False` — the byte-level count (`read_bytes().count(b'\r\n')`) showed 807 intact CRLF endings, and `file` agreed. The false alarm costs a needless re-check round-trip. Rule: after any byte-preserving patch, verify line endings at byte level.
- **Do NOT assume deletion happened just because the log says so.** Prior cycles routinely claim "draft file deleted" in PULSE.md entries while the file remains on disk. Run Sweep E.2 every 3-4 cycles to verify no stale promoted drafts persist. 4 stale drafts were found in one cleanup sweep at 2026-07-29 — all from prior cycles that logged "deleted" but left the files.
- **Do NOT trust an "archived" log entry — verify the live path is gone.** Aug 4 2026: the Aug-2 19:55 pulse logged `media/youtube-content` as archived, but the live `media/youtube-content/` dir survived (bare-frontmatter, still loadable, still counted in live totals) while the full copy sat in `.archive/youtube-content-stale-2026-08-02/`. The archive dir existing does NOT imply the live copy was removed — they are independent filesystem facts. Caught only because the Sweep H scan flagged the live copy NO_TRIGGERS. Rule: after any pulse claims a skill was archived, confirm the live path is gone (`[ -d "skills/<path>" ] && echo "STILL LIVE"`), and treat a "dead" skill name appearing in scan output as a canary that a prior archive claim never landed.
- **Do NOT treat "marked 🔄 REDUNDANT in the README" as cleanup** — the draft file must be deleted too, exactly like PROMOTED drafts. The 2026-07-31 pulse found `task-complexity-based-model-tier-assignm.md` on disk a day after being marked redundant.
- **Do NOT trust `_drafts/README.md` stats verbatim** — reconcile `Total stubs` and per-tier counts against the physical file list after any promotion/prune. README stats drifted by one (25 vs 24 on disk) in the 2026-07-31 pulse.
- **Do NOT let append-digest.py's quiet-hours echo suppress the report.** The script prints its own gate notice (`[Digest] Quiet hours (00:00-06:59 EST) — saved to digest only. [SILENT]`) based on its own clock basis, which can disagree with the job's TZ check. Real case (Aug 4 2026): job TZ check (`TZ='EST5EDT,M3.2.0/2,M11.1.0/2' date +%H`) said 22:14 ET = report hour, yet the digest script echoed `[SILENT]`. The echo is informational about the *digest*, not a delivery directive. Rules: (a) the delivery decision follows the job's TZ check only; (b) confirm the append landed via the `[Digest] Appended to ...` line — that line + a quiet-hours echo means the finding WAS saved, so deliver the normal report; (c) the `python /e/...` MSYS failure also prevents the append, so success signal = the `Appended` line, not exit code alone. **Recurred Aug 10/11 2026** — echoed `[SILENT]` at 21:45 ET (report hour); append confirmed via the `Appended` line and the normal report was delivered per rule. **Reverse direction confirmed Aug 11 2026** — at 03:59 ET (job TZ check hour 03 = quiet window) the script echoed `[Digest] Waking hours — saved to digest + ready for delivery`; the correct action was still `[SILENT]` per the job TZ check, with findings saved to the digest for the morning brief. The disagreement runs BOTH ways — never let either echo direction override the job's TZ check.
- **Invoke native Windows python with Windows-style paths** — `python ${MY_REPOS}/.../append-digest.py` fails with `can't open file 'C:\\e\\yourdata\\...'` because python.exe is a native binary and MSYS path translation does not apply to its arguments. Use the `${MY_REPOS}/...` form (see Sweep E step 8).
- **When `skill_manage(action='patch')` refuses with "content has not been loaded in this review turn", force a full-content `skill_view` via `file_path`.** The read-before-write guard is satisfied only by a view that RETURNS the content. A re-view after an earlier load in the same conversation returns `dedup: true, content_returned: false` (\"refer to the earlier result\") and does NOT count — the patch then bounces with the refusal. Workaround (verified Aug 7 2026): call `skill_view(name='<skill>', file_path='SKILL.md')` to force the full content to be returned in the current turn, then retry the patch.

## Reference Files
- `scripts/pulse-audit.py` — one-shot consolidated pulse audit (pathlib ground truth): active SKILL.md count, YAML parse errors, missing version/triggers, root-level/duplicate keys, within-tree name collisions grouped by frontmatter `name:`, >88KB size watch, `_drafts` count in one run. `python pulse-audit.py [root]` (default `~/AppData/Local/hermes/skills`). Verified Aug 8 2026: 465 skills scanned, caught the `market-signal-scanner` bare-frontmatter regression.
- `references/pulse-lessons-2026-08-04.md` — Aug 4 2026 pulse lessons: size-watch must prioritize local non-bundled skills + scan with pathlib; append-digest.py quiet-hours echo is not a delivery instruction; gap-check (grep) before promoting a draft.
- `references/cron-fleet-error-triage-2026-08-07.md` — cron fleet error triage playbook: config-drift spend-guard (#44585) fix via `hermes cron edit --provider/--model` + jobs.json verification (cron list shows stale errors); stale-`last_error` verification before re-fixing script-path jobs; provider-side 429/402/502/503 classification (user-action vs transient — not code bugs); **`enabled:false` disabled-job class** (invisible to `hermes cron list` — check jobs.json before treating flagged jobs as broken; never re-enable autonomously); **scheduler catch-up tick** (overdue jobs re-tick in batch; drift-guard hit on catch-up = live break → pin + `hermes cron run`); **Hermes managed-runtime venv recreation wipes no_agent script deps** (venv has no pip; reinstall project requirements via `uv pip install --python <venv>`, verify with native Windows paths).
- `references/cron-fleet-error-triage-2026-08-10.md` — Aug 10 2026 addendum to the above: full sections for the `enabled:false` disabled-job class, the scheduler catch-up tick, and the runtime-venv dep-wipe fix (written as a companion file when the Aug 7 reference couldn't be patched in-session; merge into the base file on the next clean pass).
