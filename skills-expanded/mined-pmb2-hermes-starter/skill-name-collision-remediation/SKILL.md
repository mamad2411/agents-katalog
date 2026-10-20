---
name: skill-name-collision-remediation
description: Detect and resolve Hermes skill name collisions between local skills dir and external repo — with remediation procedures for flat-root duplicates and categorized-level orphans. Canonical registry of all 22 known collision skills and their current resolutions.
version: 1.3.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [curation, name-collision, duplicate, skill-library, remediation]
    triggers: [name collision, ambiguous skill name, duplicate skill, skill not found, skill collision, external dirs collision, triple collision]
    related_skills: [skill-library-maintenance, skill-content-audit, discord-report-format]
---

# Skill Name Collision Remediation

> Detect, document, and resolve `Ambiguous skill name` errors caused by skills existing in both the local skills directory and an external repository directory (`skills.external_dirs`).

## When to Use

- A cron job or pulse reports a skill as "not found and skipped"
- `skill_view(name)` returns `Ambiguous skill name`
- `skills_list()` shows a skill without a category (flat root) that also exists under a category
- After reviewing `skill-library-maintenance` Section 8 name collision table

## Diagnosis

For any known colliding skill, run:

```
skill_view(name='<skill-name>')  # If ambiguous, error lists all paths
```

## Detection

Run the **frontmatter-exact scan** — do NOT trust bare grep on `^name:`:

```bash
python scripts/scan-name-collisions.py   # exact scanner, ships with this skill
python scripts/audit-dual-tree.py        # full dual-tree audit: collisions + triggerless + versionless + drift + file-set diff (2026-08-05)
```

The scanner reads only the YAML head of each SKILL.md, so `name:` lines in body text, examples, or code blocks are ignored. **Pitfall:** a naive `grep -rh '^name:' | sort | uniq -d` over-reports badly — in the 2026-07-31 audit it flagged 22 "duplicates"; the frontmatter-exact scan found the true 5. Whenever a collision is claimed, re-verify with the exact scan before remediating — registry entries and prior pulses have recorded collisions that don't reproduce (e.g. `the operator-soul` / `multi-agent-system-architecture` claimed as dupes on 2026-07-30, each resolves to exactly 1 file in the local root).

**Classify before remediating:**
- Near-identical byte sizes (≤2KB diff) → redundant duplicate; keep the larger/newer copy, delete the other.
- Large size divergence → different content sharing a name; rename one side or merge — never blind-delete.

**Cheap cross-tree triage (basename level) — but verify before acting.** A one-liner comm over directory basenames finds all candidate overlaps between local and external trees:

```bash
local_names=$(find ~/AppData/Local/hermes/skills -name SKILL.md -not -path '*/.archive/*' | sed 's|/[^/]*$||;s|^\./||' | awk -F/ '{print $NF}' | sort -u)
ext_names=$(find <external_dir>/skills -name SKILL.md -not -path '*/.archive/*' | sed 's|/[^/]*$||;s|^\./||' | awk -F/ '{print $NF}' | sort -u)
comm -12 <(echo "$local_names") <(echo "$ext_names")   # candidates
```

**Basename overlap ≠ collision.** The same basename can be two legitimately different skills in different categories — `model-routing` (fal-ai endpoint routing vs devops LLM provider routing) was flagged by this triage on 2026-07-31 but is not a real collision. Every hit must be confirmed with frontmatter `name:` comparison (the frontmatter-exact scanner is the arbiter) before remediation.

> **Resolved case (2026-08-05):** the external tree carried a THIRD `model-routing` — `hermes-config/skills/autonomous-ai-agents/model-routing` (OpenRouter multi-model guide, 5 triggers) — which WAS a frontmatter-exact collision with `fal-ai/model-routing` (6 triggers, 5 related_skills refs). The loader refused `skill_view('model-routing')` as ambiguous. Fix: renamed the external copy to `openrouter-model-routing` (zero refs pointed at it). Lesson: basename triage must scan BOTH local and external trees — the fal-ai vs devops pair was a false alarm, but the fal-ai vs external autonomous-ai-agents pair was real and load-breaking. What the triage DOES reliably surface: stale archived/consolidated names still loadable in the external tree (`github-code-review`, `codebase-inspection`, `mcp-server-onboarding` on 2026-07-31) — those are dead names to purge from external_dirs, not sync targets.

**Registry claims rot — verify live, every pulse.** The 2026-07-31 double-collision table claimed all 4 flat-root pairs "✅ matched/synced"; a live `skill_view` audit the SAME day found ALL 4 ambiguous (external `plan` missing `triggers`; external `subagent-driven-development` stale v1.1.0/24.8KB vs local v1.3.0/82.4KB + 14 refs; external `test-driven-development` stale v1.1.0 vs local v2.0.0 rewrite; `requesting-code-review` 3 divergent copies). A registry entry is a TODO list, not ground truth — batch `skill_view(name)` on every "resolved" name each pulse; ANY `Ambiguous skill name` result is a live regression regardless of what the table says.

**Audit the CONFIGURED external path, not a guessed one.** Read `config.yaml → skills.external_dirs` before scanning. On 2026-07-31 two same-named hermes-config clones coexisted: the configured `${USER_HOME}/Documents/github/hermes-config` (canonical, holds the sync commits) and a stale `${MY_REPOS}/hermes-config` with divergent content (some files newer, some older). Scanning the wrong clone inverts version-drift conclusions. Also: the `~/.hermes/skills/` legacy tree is NOT in the loader path (loader = HERMES_HOME + `external_dirs` only) — its stale copies are inert for resolution but pollute `find`/`grep` audits. **The legacy tree was fully retired 2026-08-01** — all 88 stale dups moved to `~/.hermes/skills/.archive/legacy-stale-2026-08-01/` (91 SKILL.md total), with 2 genuinely legacy-only skills (`find-skills` → `curation/`, `skybridge` → `software-development/`) promoted to the load path first. The tree now contains only `.archive/` — future pulses should NOT re-scan it as a live tree. Full retirement procedure + case study: `references/legacy-tree-retirement-2026-08-01.md`. **The E: hermes-config clone was retired 2026-08-02** — proven zero unique content (every "newer" copy byte-matched AppData; its only higher-versioned file `project-documentation-standards` v1.3.0 was a stale Jun-5 pre-migration fork while load-path C: v1.0.0 carried the real Jul-31 maintenance commit adding triggers + related_skills). Renamed `skills/` → `skills.retired-2026-08-02/` (reversible). **Version-number trap:** across divergent clones a HIGHER `version:` field is NOT proof of newer content — a fork can carry v1.3.0 while the canonical tree's v1.0.0 is the maintained copy. Always cross-check `git log -- <file>` per tree and diff bodies before concluding which side is canonical.

**Shell `find` silently skips some dirs on MSYS — pathlib is ground truth for tree counts.** The 2026-08-01 retirement found `find ~/.hermes/skills -name SKILL.md -not -path '*/.archive/*'` returned 88 while `pathlib.Path(...).rglob("SKILL.md")` returned 90 — `find-skills/` and `skybridge/` were present on disk with valid frontmatter but invisible to `find`. Every prior pulse's count ("87/88 stale dups, 2 legacy-only") was off by 2 because it trusted `find`/`comm`. **Fix:** for any tree-wide enumeration that feeds a "legacy-only", "duplicate", or count conclusion, use Python pathlib `rglob` (or cross-verify a `find` result against pathlib before trusting a zero/low result). `find`/`comm` output is orientation only, never the final number.

**Audit-script traps (bit the 2026-08-05 pulse — cost 3 verification round-trips):**

1. **`pathlib.rglob('name/SKILL.md')` silently matches `.archive/` copies.** The pattern `next(Path('.').rglob(f'{name}/SKILL.md'), None)` matches ANY path ending in `<name>/SKILL.md` — including `.archive/.../<name>/SKILL.md` — and `next()` returns whatever the iteration order hits first. A drift script comparing AppData vs external reported "0 triggers" for skills that HAD triggers, because it had landed on an archived stale copy. **Fix:** iterate `rglob('*')` and filter by `name in p.parts and '.archive' not in p.parts` (or skip any path with a `.archive` part) — never `rglob` a bare `<name>/SKILL.md` pattern when archives exist in the tree.

2. **`read_text()` translates CRLF→LF on Windows — a `'\r\n' in c` check on the decoded string is ALWAYS False.** Validating "line endings preserved" with `'\r\n' in path.read_text()` produces a false "CRLF lost" verdict on every CRLF file. **Fix:** check raw bytes — `b'\r\n' in path.read_bytes()` — for line-ending verification. (Same class as the skill-authoring Pitfall #7 CRLF-grep blind spot: always verify line endings at the byte level, never through a text-mode read.)

3. **f-strings can't contain backslash expressions** (`f'...{"\\r\\n" in raw}'` is a SyntaxError). Assign the CRLF check to a variable first (`crlf = b'\r\n' in raw`) then interpolate. Minor, but it interrupts a batch-validation loop mid-run.

## Collision Patterns

| Pattern | Description | Severity |
|---------|-------------|----------|
| Flat root + external | Skill at `skills/<name>/` AND `hermes-config/skills/<category>/<name>/` | 🟡 2-way — versions may drift |
| Local categorized + external | Skill at `skills/<category>/<name>/` AND `hermes-config/skills/<category>/<name>/` | 🟡 2-way — identical path |
| Triple collision | Skill at `skills/<name>/` + `skills/<category>/<name>/` + `hermes-config/skills/<category>/<name>/` | 🔴 REGRESSION — duplicates added instead of removed |
| Same-name sibling dirs (local-only) | Skill at `skills/<cat-a>/<name>/` AND `skills/<cat-b>/<name>/` (e.g. `gstack/browse` + `gstack-browse/browse`) | 🟡 2-way — loader ambiguity; usually identical content, one copy stale |

## Known Collisions (as of 2026-07-31)

### 🔴 Triple Collisions

| Skill | Local Root | Local Categorized | External Categorized |
|-------|-----------|-------------------|---------------------|
| ~~`hermes-agent-skill-authoring`~~ | ~~`skills/` flat root~~ | ~~`skills/software-development/`~~ | ✅ `hermes-config/skills/software-development/` — RESOLVED 2026-07-31 |
| ~~`writing-plans`~~ | ~~`skills/` flat root~~ | ~~`skills/software-development/`~~ | ✅ `hermes-config/skills/software-development/` — RESOLVED 2026-07-31 |
| ~~`systematic-debugging`~~ | ~~`skills/` flat root~~ | ~~`skills/software-development/`~~ | ✅ `hermes-config/skills/software-development/` — RESOLVED 2026-07-31 |

Both resolved 2026-07-31 Skillmate pulse via **Option B then A**: external copies were STALE (hasa: external v1.0.0 7.8KB vs local v1.25.0 61.7KB + references/ + scripts/; wp: external 7.5KB missing Strategic-Architecture section vs local 12.9KB complete). Synced local → external first (commit `4ef36b8` in hermes-config), then removed BOTH local copies (flat root + categorized). `skill_view` verified resolving from external only. **Registry lesson:** the earlier "keep external, delete local" guidance was wrong — version drift must be checked BEFORE deciding which side is canonical; the local copies were the newer ones here.

`systematic-debugging` was the same shape and was resolved the same day by the Forge pulse (hermes-config commit `40d8d42`): external was stale v1.1.0/10.8KB vs local v1.10.0/70.6KB + 47 `references/` files. Synced local → external, removed BOTH local copies (flat root AND categorized), verified unambiguous. Its registry row in the double-collision table ("✅ synced") was STALE — the collision was still live at pulse time, proving the same staleness flag the local-internal table already carries for `requesting-code-review` / `test-driven-development`.

**Iterative re-check pitfall:** the ambiguity error lists only TWO matches at a time. A triple collision masquerades as a double — after removing the flat-root copy, `skill_view` surfaced the local CATEGORIZED copy as the remaining collision. After every removal, re-run `skill_view` and repeat until the match list is a single path. Never trust a registry "resolved" claim over a live `skill_view` result.

### 🟡 Double Collisions (Flat Root + External)

| Skill | Local | External | Version |
|-------|-------|----------|---------|
| `plan` | ~~flat root~~ removed 2026-07-31 | `software-development/` | ✅ RESOLVED — local had newer content (triggers + LF); synced to external, local flat+categorized removed |
| `requesting-code-review` | ~~flat root~~ removed 2026-07-31 | `software-development/` | ✅ RESOLVED — merged local triggers into external's newer github-code-review wording; local flat+categorized removed |
| `subagent-driven-development` | ~~flat root~~ removed 2026-07-31 | `software-development/` | ✅ RESOLVED — external was STALE v1.1.0/24.8KB vs local v1.3.0/82.4KB; synced SKILL.md + 14 references to external, local flat+categorized removed |
| `test-driven-development` | ~~flat root~~ removed 2026-07-31 | `software-development/` | ✅ RESOLVED — external was STALE v1.1.0 vs local v2.0.0 rewrite; synced v2.0.0 to external, fixed self-reference in related_skills, local flat+categorized removed |
| `github-code-review` | ~~flat root~~ archived 2026-08-02 | `github/` | ✅ RESOLVED — **sync-created collision**: external was STALE v1.1.0/14KB vs flat-root local v2.0.0/27KB (identical to E: clone copy). Synced external → v2.0.0 (hermes-config commit `f4a69a0`), which immediately made the name AMBIGUOUS (flat root + external both v2.0.0). Archived flat copy to `.archive/github-code-review-flat-2026-08-02/` (had a DESCRIPTION.md support file — archive, don't rm). `skill_view` verified resolving to external canonical (v2.0.0 + `references/review-output-template.md`). |

**Sync-created collision pitfall:** syncing a newer copy INTO the external tree when a same-name copy exists at local flat root CREATES a live ambiguity even when versions now match — the loader refuses both. After ANY external sync, immediately re-run `skill_view(name)`; if ambiguous, archive the local flat copy (prefer `.archive/<name>-flat-<date>/` over `rm -rf` when the flat copy carries support files like DESCRIPTION.md).

### 🟡 Double Collisions (Same Relative Path)

**Batch-resolved 2026-08-05:** the 19 local-categorized + external same-path pairs below were ALL live `skill_view` ambiguities (same bug class as the 2026-07-31 cron break). External copies were STALE triggerless subsets (AppData canonical — 3 had newer versions, several carried 13+ extra `references/` that external lacked, and NO external-only files existed anywhere). Resolved via Option B→A: synced local→external (`hermes-config` commit `7de5b67`, 93 files, +12,103/−481 — references + scripts carried over), archived all 19 local dirs to `.archive/collision-sync-2026-08-05/`, verified `skill_view` per name. `chief-of-staff-operations`, `the operator-soul`, `tac-odds-scroll-world` resolved the same way (commit `c933d4c`). Post-fix: 0 collisions between AppData (453) and external (46).

| Skill | Local Path | External Path | Version | Status |
|-------|-----------|--------------|---------|--------|
| `multi-agent-system-architecture` | ~~`skills/devops/`~~ archived 2026-08-05 | `hermes-config/skills/devops/` | v1.1.0 | ✅ RESOLVED — synced v1.1.0 + 14 references, local archived |
| `the operator-soul` | ~~`skills/autonomous-ai-agents/`~~ archived 2026-08-05 | `hermes-config/skills/autonomous-ai-agents/` | v1.0.0 | ✅ RESOLVED — synced, local archived |

Other same-path pairs resolved 2026-08-05 (all → external canonical, local archived): `kanban-orchestrator`, `kanban-worker`, `memory-migration-mem0-to-mempalace`, `webhook-subscriptions`, `github-stars-extraction`, `project-inventory`, `agent-zero-bridge`, `building-mcp-servers`, `debugging-hermes-tui-commands`, `fastapi-mcp-bridge`, `firefox-remote-control`, `legal-advisory-agent`, `node-inspect-debugger`, `python-debugpy`, `spike`, `token-optimization-rtk`, `voice-agent-architecture`, `web-scraping-scrapling`, `chief-of-staff-operations`, `tac-odds-scroll-world`.

### 🟡 Local-Internal Collisions (detected 2026-07-31 — frontmatter-exact scan, 442 SKILL.md)

Same-name collisions inside the local skills dir alone (no external repo involved):

| Skill | Path A | Path B | Class / Action |
|-------|--------|--------|----------------|
| `browse` | `skills/gstack/browse/` (52.4KB) | `skills/gstack-browse/` (53.4KB) | near-identical — keep standalone, retire nested copy |
| `qa` | `skills/gstack/qa/` (78.6KB) | `skills/gstack-qa/` (80.2KB) | near-identical — keep standalone, retire nested copy |
| `review` | `skills/gstack/review/` (92.8KB) | `skills/gstack-review/` (94.5KB) | near-identical — keep standalone, retire nested copy |
| `requesting-code-review` | ~~`skills/` flat root (3.3KB)~~ removed 2026-07-31 | `skills/software-development/` (8.8KB) | ✅ RESOLVED — content merged + local flat removed; external canonical |
| `test-driven-development` | ~~`skills/` flat root (10.6KB)~~ removed 2026-07-31 | `skills/software-development/` (13.8KB) | ✅ RESOLVED — v2.0.0 rewrite synced to external; local flat + categorized removed |

## Remediation

### Option A — Remove Local Duplicate (preferred)

```bash
# For flat-root copy:
rm -rf ~/AppData/Local/hermes/skills/<skill-name>

# For also-local categorized copy (triple collisions):
rm -rf ~/AppData/Local/hermes/skills/<category>/<skill-name>
```

**Before removal — check version drift:**
```bash
grep "^version:" ~/AppData/Local/hermes/skills/<path>/SKILL.md
grep "^version:" ~/Documents/github/hermes-config/skills/<path>/SKILL.md
```

**After removal — verify:**
```
skill_view(name='<skill-name>')  # Must resolve without ambiguity
```

### Option B — Update External Copy (if local is newer)

Copy the local SKILL.md to the external repo, commit, then proceed with Option A.

## Prevention

- Run `skill-library-maintenance` Section 8 collision scan after any bulk import
- Do NOT create local categorized copies of skills that exist in external_dirs — this inverts remediation and creates triple collisions
- External repo should be the canonical source; local copies only for skills NOT in any external repo
- Document all removals in PULSE.md for audit trail

## Verification

- [ ] `skill_view(name)` resolves without ambiguity
- [ ] `skills_list()` shows skill under proper category, not flat root
- [ ] No stale SKILL.md directories remain at flat-root level
- [ ] All `related_skills` references still resolve — watch for self-references (2026-07-31: `test-driven-development` v2.0.0 listed itself in its own `related_skills`; replaced with `writing-plans`)
- [ ] Cron jobs load the skill by name successfully
- [ ] Re-run `skill_view(name)` for every affected name IN THE SAME SESSION after `rm -rf` — the loader reflects removals immediately (verified 2026-07-31: 5 names resolved to exactly 1 path right after removal)
