---
name: skill-library-maintenance
description: "Audit, clean, and reconcile the Hermes skill library — ghost entries, stale detection, cross-reference integrity, and usage-registry health."
version: 1.11.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [skills, maintenance, audit, curator, library, registry]
    triggers: [skill library, usage registry, ghost entries, skill audit, curator, stale skills, .usage.json, library health, cross-reference, related_skills, description audit, category description, singleton description, skill gap, frontmatter hygiene, root-level triggers, crlf patching, skill size limit, yaml regression, name collision, duplicate skill, ambiguous skill, external dirs, skill resolution, subdirectory symlink, symlink audit, skill unlinked, root-accessible, metadata hermes gap, frontmatter backfill, bulk frontmatter, systematic gap, missing metadata, metadata audit, minimal frontmatter, missing version, missing author, missing license, missing platforms, draft audit, draft promotion, _drafts audit, draft triage, orphan promotion, draft backlog]
    related_skills: [hermes-agent-skill-authoring, discord-report-format]
---

# Skill Library Maintenance

Routines for keeping the Hermes skill library healthy — detecting inconsistencies between `.usage.json` and on-disk state, identifying stale/ghost entries, and verifying cross-reference integrity.

## Prerequisites

- Access to the skills directory (`~/.hermes/skills/` or `~/AppData/Local/hermes/skills/`)
- `.usage.json` exists and is writable
- Python 3 with `json` and `os` modules (stdlib)

## Workflow

### 1. Detect Ghost Entries

Ghost entries are skills tracked as `state: active` in `.usage.json` whose directories have been removed from disk. They inflate active counts and confuse health assessments.

Run the detection script in `scripts/ghost-detect.py`:

```bash
cd ~/AppData/Local/hermes/skills
python scripts/ghost-detect.py
```

Or manually with:

```python
import json, os

with open('.usage.json') as f:
    d = json.load(f)

ghosts = [name for name, meta in d.items()
          if meta.get('state') == 'active' and not os.path.isdir(name)]
```

Key signals:
- `state == 'active'` but `os.path.isdir(name)` is `False`
- `use_count == 0` and `patch_count == 0` — never used, likely a migration artifact
- `archived_at is None` — was never formally archived

### 2. Cross-Reference Check (Before Marking Stale)

Before remediating, check that no active skill references a ghost entry via `related_skills`:

```python
import os

for root, dirs, files in os.walk('.'):
    if '.archive' in root or '.curator_backups' in root:
        continue
    if 'SKILL.md' in files:
        with open(os.path.join(root, 'SKILL.md')) as f:
            content = f.read()
        if content.startswith('---'):
            fm_end = content.index('---', 3)
            frontmatter = content[3:fm_end]
            if 'related_skills' in frontmatter:
                for g in ghosts:
                    if g in frontmatter:
                        print(f"REFERENCED: {root} -> {g}")
```

If referenced, update the consumer's `related_skills` list first.

### 3. Remediate Ghosts

Mark ghost entries as `state: stale` (preserves audit trail; does not delete):

```python
import json
from datetime import datetime, timezone

with open('.usage.json') as f:
    d = json.load(f)

now = datetime.now(timezone.utc).isoformat()

updated = 0
for name in ghosts:
    if name in d and d[name].get('state') != 'stale':
        d[name]['state'] = 'stale'
        d[name]['archived_at'] = now
        updated += 1

with open('.usage.json', 'w') as f:
    json.dump(d, f, indent=2)

print(f"Marked {updated} entries as stale.")
```

### 4. Verify Registry Health After Cleanup

```python
import json

with open('.usage.json') as f:
    d = json.load(f)

active = sum(1 for v in d.values() if v.get('state') == 'active')
stale = sum(1 for v in d.values() if v.get('state') == 'stale')
total = len(d)
print(f"Active: {active} | Stale: {stale} | Total: {total}")
```

## Pitfalls

- **Do not delete ghost entries** — marking `stale` preserves the audit trail (created_at, last_used_at, patch_count). Deleting loses provenance.
**Pitfalls:**
- **`.usage.json` is managed by the curator** — state changes via direct JSON edit are valid but a `gbrain curator` reconcile pass may overwrite manual edits if formats diverge. Re-run curator sync after manual cleanup.
- **Bundled and hub-installed skills are protected** — ghost detection skips these (they live outside the user's skills directory). Do not attempt to clean entries for `hermes-*` or hub-installed skills.
- **Same-name cross-path duplicates evade the collision detector** — Step 8's `collisions` check only finds same-relative-path overlaps. Skills with the same `name:` or directory basename at different relative paths (e.g., local `github-code-review/` vs external `github/github-code-review/`) are invisible to it. These are NOT a resolver collision (`skill_view()` works), but the two copies can independently drift and serve different guidance. Always supplement the collision scan with a heuristic like 'find all external SKILL.md files whose basename dir matches any local skill by that same name'.
> **Name collisions with external_dirs cause silent skill-skip** — When a skill exists at the same relative path in both the local skills dir and an external dir configured under `skills.external_dirs`, `skill_view()` and `skills_list()` fail with `Ambiguous skill name`. Agents that resolve by bare name error out and skip loading. Invisible in logs unless you run the collision check (step 8). If a cron job reports a skill as "not found", suspect a name collision before assuming it is missing.
>
> **Current colliding skills (verified 2026-07-14, partially resolved):**
> | Skill | Local Path | External Path | Cat Mismatch? | Version |
> |-------|-----------|---------------|:---:|---|
> | `hermes-agent-skill-authoring` | flat root | `software-development/` | **Yes** | ✅ v1.25.0 synced |
> | `plan` | flat root | `software-development/` | **Yes** | ✅ v1.0.0 matched |
> | `requesting-code-review` | flat root | `software-development/` | **Yes** | ✅ v2.0.0 matched |
> | `subagent-driven-development` | flat root | `software-development/` | **Yes** | ✅ v1.3.0 synced |
> | `systematic-debugging` | flat root | `software-development/` | **Yes** | ✅ v1.10.0 synced |
> | `test-driven-development` | flat root | `software-development/` | **Yes** | ✅ v2.0.0 synced |
> | `writing-plans` | flat root | `software-development/` | **Yes** | ✅ v1.1.0 matched |
> | `agent-zero-bridge` | `software-development/` | `software-development/` | No | ✅ v1.0.0 matched |
> | `building-mcp-servers` | `software-development/` | `software-development/` | No | ✅ v1.12.0 synced + added missing field |
> | `debugging-hermes-tui-commands` | `software-development/` | `software-development/` | No | ✅ v1.0.0 matched |
> | `fastapi-mcp-bridge` | `software-development/` | `software-development/` | No | ✅ v1.0.0 matched |
> | `firefox-remote-control` | `software-development/` | `software-development/` | No | ✅ v1.0.0 added missing field |
> | `legal-advisory-agent` | `software-development/` | `software-development/` | No | ✅ v1.1.0 synced |
> | `node-inspect-debugger` | `software-development/` | `software-development/` | No | ✅ v1.0.0 matched |
> | `python-debugpy` | `software-development/` | `software-development/` | No | ✅ v1.1.0 synced |
> | `spike` | `software-development/` | `software-development/` | No | ✅ v1.0.0 matched |
> | `token-optimization-rtk` | `software-development/` | `software-development/` | No | ✅ v1.0.0 matched |
> | `voice-agent-architecture` | `software-development/` | `software-development/` | No | ✅ v1.0.0 matched |
> | `web-scraping-scrapling` | `software-development/` | `software-development/` | No | ✅ v1.0.0 matched |
>
> **Scope:** Originally reported as 3 collisions (Jul 12). A full audit (Jul 14 Skillmate pulse) revealed **20 overlapping skills** — 6 had version drift, 2 were missing metadata fields. All 8 were fixed in hermes-config@547de49. The dual-location **persists** — both copies still exist — but versions now match across all 20.
>
> **Same-path collisions (unlisted above):** `codebase-inspection` at `github/codebase-inspection/` — exists in both `AppData\Local\hermes\skills\github\` and `hermes-config\skills\github\` at the same relative path. Not in the table above because it's a same-path collision, not a cross-category one. Same `Ambiguous skill name` symptom. `skill_manage(action='delete')` refused for both copies (`created_by=None`).

**Practical impact:** Any cron job listing any of these by bare name gets `Ambiguous skill name` and skips them. After the Jul 14 sync, agents loading from either copy get equivalent guidance (versions matched), but the collision itself remains unresolved.

**Diagnostic: determining which copy is authoritative.** When `skill_view()` returns a collision error, run `skills_list()` and check which category the skill appears under. A skill listed without a category (flat root) means the local copy is the registered canonical entry. A skill only appearing under a category like `software-development/` means the external_dirs copy is what the system resolves to. If the skill doesn't appear in `skills_list` at all from the bare name, the loader silently skips it and neither copy is considered registered for that caller.

**Remediation limitation:** `skill_manage(action='delete')` refuses bundled/manual skills with `"created_by=None"`. When both copies are protected, the collision persists. If versions are synced (as they are for all 20+ known collisions post-Jul-14), agents loading from either copy get equivalent guidance. Permanent fix requires filesystem-level removal via terminal or stopping the `external_dirs` entry in `config.yaml`.
- **The same-name entry may exist in `.archive/`** — if a skill directory exists in `.archive/`, the `.usage.json` entry should reflect the archived state, not active. Any mismatch is a ghost.
- **Root-level YAML keys are silently ignored by the inference engine** — `triggers:`, `trigger:`, `tags:`, and `related_skills:` at the YAML root level are **not** read by Hermes even though `yaml.safe_load` parses them. They MUST live under `metadata.hermes.{triggers, tags, related_skills}`. External agent activity (pulses, multi-agent edits) frequently reintroduces root-level keys.
  - **`triggers:` plural** — most common variant; a YAML list (`- item`). Agents aware of the `metadata.hermes` convention may still write this at root level by accident.
  - **`trigger:` singular** — less common but distinct; often set to a single string value instead of a list. Found in `model-provider-routing` and `mcp-fleet-audit` (Jul 21). This shape is invisible to grep-for-`triggers` scans and requires checking for the singular key directly.
  - The frontmatter hygiene scan (### 7) catches all three (`triggers`, `trigger`, `tags`, `related_skills`) via `yaml.safe_load` + key-existence check.
- **`skill_manage(action='patch')` silently fails on CRLF files** — On Windows, ~180 skills have CRLF (`\r\n`) line endings. Calling `skill_manage(action='patch')` reports "1 replacement" but never modifies the file. Use the standalone `patch(old_string=..., new_string=..., path=...)` tool (correctly handles CRLF) or Python byte-level replacement (`Path(fp).read_bytes()` → replace → `write_bytes()`). Always verify with `grep -a` (not plain `grep`) which forces text mode on MSYS.
- **`ln -s` on Windows/MSYS copies directories instead of symlinking** — When creating a symlink for a directory target under MSYS bash, `ln -s` silently copies the entire directory tree (separate inodes, identical content). The symlink resolves as a real directory with independent files. Use `cmd /c mklink /D <link> <target>` inside MSYS instead — this creates a proper NTFS reparse-point directory symlink.
- **Top-level symlinks worsen external-dir name collisions** — Creating a symlink for a subdirectory skill that also exists in an external dir adds a third resolvable path, triggering `Ambiguous skill name` between the new symlink and the external copy rather than resolving the bare-name lookup. The symptom shifts from "not found" to "ambiguous" but the skill remains unloadable. The correct fix is remediation Option A (remove local duplicate), not symlink creation. However, subdirectory skills NOT in the external-dir collision set (e.g., `subagent-driven-development`, `systematic-debugging`, `native-mcp`) ARE safe to symlink — the bare name resolves uniquely and job loading succeeds.
- **Gstack drift resolution is documented in `references/gstack-dup-audit.md#drift-resolution-procedure`** — When gstack top-level wrappers and subdir canonical copies have drifted, use that procedure to sync the wrapper from canonical. The technique: determine canonical copy by checking for gstack-specific metadata (`preamble-tier`, `allowed-tools`), then `cp` + `diff` verify.
- **`[ -L "$f" ]` on MSYS fails to detect directory symlinks** — On MSYS/git-bash, `ls -1d */` resolves directory symlinks transparently to their targets, and the `-L` test returns false for reparse-point symlinks. Use `find . -maxdepth 1 -type l -printf '%f\\n'` instead, which correctly identifies all symlinks regardless of type or filesystem driver.
- **Manual `patch()` of root-level YAML keys risks broken list indentation** — When using the standalone `patch()` tool to move `triggers:`, `tags:`, or `related_skills:` under `metadata.hermes`, the list items (`- item`) need manual re-indentation that is easy to miscount. A list at root level with 0 spaces of indent needs 6 spaces under `metadata.hermes.triggers` (2 for `metadata`, 2 for `hermes`, 2 for `triggers` → `      - item`). Off-by-one-or-two produces YAML that looks plausible but fails `yaml.safe_load()` — and the error can be cryptic (e.g. `expected <block end>, but found '-'`). **Prefer the Python `yaml.dump()` rewrite in Section 7** for any fix involving multi-item list keys — it auto-indents correctly.
- **`|---` YAML document-start marker error** — A line-1 `|---` (pipe + three dashes) instead of `---` causes `yaml.safe_load()` to throw `ScannerError: expected chomping or indentation indicators, but found '-'`. Python's tokenizer interprets `|` as a literal block scalar start, then fails when it sees `--`. This error is visually subtle (`|` blends with `---`). **Fix:** `sed -i '1s/^|---/---/' file.md` (works on CRLF and LF). Root cause is external agent batch-import creating SKILL.md with the wrong document-start marker. Always validate with `yaml.safe_load` after creating or bulk-editing SKILL.md files to catch this early. Found in 7 scroll-world/home-service skills in Jul 22 Scribe pulse.
### 4a. Usage-Based Dormant Skill Detection

Analyze `.usage.json` `last_used_at` timestamps to find skills that have NEVER been loaded or haven't been used in 30+ days. This is different from ghost detection (state-based) — it identifies **library bloat**: skills that exist on disk and pass state checks but are never loaded during actual work.

```python
import json
from datetime import datetime, timezone, timedelta
from pathlib import Path

SKILLS_DIR = Path('~/AppData/Local/hermes/skills').expanduser()
usage_file = SKILLS_DIR / '.usage.json'

with open(usage_file) as f:
    data = json.load(f)

now = datetime.now(timezone.utc)
cutoff_30d = now - timedelta(days=30)

never_used = []
stale = []

for name, meta in data.items():
    if name.startswith('.') or name == 'README' or meta.get('archived_at'):
        continue

    last_used = meta.get('last_used_at')
    created = meta.get('created_at', '')

    if last_used is None:
        created_short = created[:10] if created else '?'
        never_used.append((created_short, name))
    else:
        try:
            dt = datetime.fromisoformat(last_used.replace('Z', '+00:00'))
            if dt < cutoff_30d:
                stale.append((last_used[:10], name))
        except (ValueError, TypeError):
            stale.append((last_used or '?', name))

print(f"Never-used: {len(never_used)} ({100*len(never_used)//max(len(data),1)}%)")
for created, name in sorted(never_used):
    print(f"  created {created}  {name}")

print(f"\nStale (30d+): {len(stale)}")
for last, name in sorted(stale):
    print(f"  last {last}  {name}")
```

**Interpreting results:**

| Category | Signal | Action |
|----------|--------|--------|
| **Never-used** | `last_used_at` is `null`, `created_at` exists | Archival candidate — 15%+ in this state suggests bloat |
| **Stale (30d+)** | `last_used_at` older than 30 days | Monitor — 25-30% stale rate is normal; >40% warrants cleanup |
| **Domain clusters** | Multiple dormant skills in same category | Batch-archival candidate — may be superseded by newer umbrella tools |

**Archival classification heuristic:**

```python
clusters = {
    'ml-research': ['evaluating-llms-harness', 'huggingface-hub', 'llama-cpp',
                    'segment-anything-model', 'serving-llms-vllm', 'weights-and-biases'],
    'creative-design': ['architecture-diagram', 'ascii-art', 'ascii-video',
                        'baoyu-infographic', 'claude-design', 'excalidraw',
                        'heartmula', 'p5js', 'pretext', 'sketch', 'songsee',
                        'songwriting-and-ai-music', 'gif-search'],
}
for domain, skills in clusters.items():
    dormant = [s for s in skills if s in {n[1] for n in never_used}]
    print(f"{domain}: {len(dormant)}/{len(skills)} dormant")
```

**Pitfalls:**
- **Never-used ≠ useless** — domain-specific tools (ML inference, hardware setup) may be valid without having been needed yet. Flag, don't auto-delete.
- **`last_used_at` tracks skill_view/skill_use load events** — skills resolved via related_skills traversal may NOT increment usage. Treat as a lower bound.
- **`state: stale` entries distort never-used counts** — the detection script above does NOT filter by `state`. Skills formally archived (`state: stale` in `.usage.json`) still have `last_used_at: null` and inflate the count. Always filter to `state: active` before computing "never-used" percentage. During Skillmate Jul 20 audit, a reported 43 never-used was actually 12 active+never-used — the remaining 31 were stale entries. Without the state filter, the metric exaggerates library bloat by 3-4x.
- **Compare `created_at` vs analysis date** — a skill created 2 days ago with no usage is normal; 49+ days dormant is a strong archival signal.
- **Cross-reference before archiving** — never-used skills may still be referenced by `related_skills` in other skills. Run Section 5's integrity scan first.
- **Tool-definition skills** — skills like `huggingface-hub` or `llama-cpp` exist to expose MCP-style tool guidance, not direct task invocation. Their value is in the integration layer. Flag differently from traditional task-guide skills.

### 5. Cross-Reference Integrity Scan (Full)

Scan every skill's `related_skills` to verify each referenced name resolves to an existing SKILL.md. This catches stale refs to skills that were removed or renamed (unrelated to ghost status). Use the methodology from `references/cross-ref-audit.md`.

```python
import os, re

SKILLS_DIR = '~/AppData/Local/hermes/skills'

# Build canonical name set: every dir containing SKILL.md
canonical = set()
for root, dirs, files in os.walk(SKILLS_DIR):
    if '.archive' in root or '.curator_backups' in root:
        continue
    if 'SKILL.md' in files:
        canonical.add(os.path.basename(root))

# Scan all SKILL.md files for related_skills
dead = []
for root, dirs, files in os.walk(SKILLS_DIR):
    if '.archive' in root or '.curator_backups' in root:
        continue
    if 'SKILL.md' in files:
        with open(os.path.join(root, 'SKILL.md')) as f:
            content = f.read()
        if content.startswith('---'):
            fm_end = content.index('---', 3)
            fm = content[3:fm_end]
            m = re.search(r'related_skills:\s*\[([^\]]+)\]', fm)
            if m:
                refs = [r.strip() for r in m.group(1).split(',')]
                for ref in refs:
                    if ref and ref not in canonical:
                        dead.append((os.path.basename(root), ref))

if dead:
    print(f"{len(dead)} dead cross-references found:")
    for skill, ref in dead:
        print(f"  {skill} -> {ref}")
else:
    print("All related_skills are valid.")
```

Fix dead refs by either:
- Replacing with the correct existing skill name
- Removing the entry if no equivalent skill exists
- Adding the missing skill if it was intentionally referenced

### 6. Category Description Gap-Fill

Some skill categories lack `DESCRIPTION.md` files. Audit and fill to keep navigation discoverable:

```python
import os

SKILLS_DIR = '~/AppData/Local/hermes/skills'

for entry in os.listdir(SKILLS_DIR):
    cat_dir = os.path.join(SKILLS_DIR, entry)
    if not os.path.isdir(cat_dir) or entry.startswith('.'):
        continue
    has_sub = any(
        os.path.isdir(os.path.join(cat_dir, sub))
        and os.path.isfile(os.path.join(cat_dir, sub, 'SKILL.md'))
        for sub in os.listdir(cat_dir)
    )
    if has_sub and not os.path.isfile(os.path.join(cat_dir, 'DESCRIPTION.md')):
        sub_count = sum(1 for sub in os.listdir(cat_dir)
                        if os.path.isdir(os.path.join(cat_dir, sub))
                        and os.path.isfile(os.path.join(cat_dir, sub, 'SKILL.md')))
        print(f"  {entry}/ ({sub_count} skills) — no DESCRIPTION.md")
```

Create DESCRIPTION.md in the standard YAML frontmatter format:

```
---
description: <one-line summary of the category's skills>
---
```

### 6a. Singleton-Package Description Gap-Fill

Some top-level skill directories are **singleton packages** — the directory IS the skill (contains SKILL.md directly, not subdirectories). These also benefit from a DESCRIPTION.md for discoverability in `skills_list` output.

The Section 6 detector only flags **categories** (directories with subdirectories). Singletons are a separate class:

```python
import os

SKILLS_DIR = '~/AppData/Local/hermes/skills'

for entry in sorted(os.listdir(SKILLS_DIR)):
    pkg_dir = os.path.join(SKILLS_DIR, entry)
    if not os.path.isdir(pkg_dir) or entry.startswith('.'):
        continue
    has_own_skill = os.path.isfile(os.path.join(pkg_dir, 'SKILL.md'))
    has_desc = os.path.isfile(os.path.join(pkg_dir, 'DESCRIPTION.md'))
    is_category = any(
        os.path.isdir(os.path.join(pkg_dir, sub))
        and os.path.isfile(os.path.join(pkg_dir, sub, 'SKILL.md'))
        for sub in os.listdir(pkg_dir)
    )
    # Singleton: has its own SKILL.md, not a category, and no DESCRIPTION.md
    if has_own_skill and not is_category and not has_desc:
        print(f"  {entry}/ — singleton package, no DESCRIPTION.md")
```

When creating, base the description on the skill's YAML frontmatter `description:` field or the first 2-3 lines of the SKILL.md body. Keep it concise — a single line that tells readers what class of work the skill covers:

```
---
description: Short description of what the singleton skill does
---
```

### 7. Frontmatter Hygiene Scan

After external agent activity (pulses, multi-agent editing, curator passes), skills can acquire frontmatter regressions. Run this scan to catch root-level `triggers:` (must live under `metadata.hermes`), missing `metadata.hermes.triggers`, and skills approaching the 100KB size limit.

**Priority: recently-modified skills.** The most common source of regressions is external agents (website-landlord, Forge, Skillmate, etc.) modifying or creating SKILL.md files without `metadata.hermes` blocks. Always check the full library with Section 7's `os.walk` scan, but start by identifying new/modified files to catch the highest-risk candidates first:

```bash
# Find skills modified in the last N hours (adjust hours for cadence)
find ~/AppData/Local/hermes/skills -name "SKILL.md" -newermt "24 hours ago" -type f 2>/dev/null | sort
```

This narrowed set catches batch-created scroll-world/home-service skills, external-agent edits, and any post-pulse modifications. After fixing those, run the full walk for latent issues. Testing confirms that `os.walk` on 350+ SKILL.md files completes in under 3 seconds and catches regressions the `find -newermt` scope would miss.

```python
import os, yaml

SKILLS_DIR = '~/AppData/Local/hermes/skills'
issues = []

for root, dirs, files in os.walk(SKILLS_DIR):
    if '.archive' in root or '.curator_backups' in root:
        continue
    if 'SKILL.md' in files:
        fp = os.path.join(root, 'SKILL.md')
        try:
            with open(fp, 'r', encoding='utf-8') as f:
                parts = f.read().split('---', 2)
            if len(parts) < 3:
                continue
            fm = yaml.safe_load(parts[1])
            if not isinstance(fm, dict):
                continue

            name = os.path.basename(root)
            line_issues = []

            # Root-level keys that belong under metadata.hermes
            if 'triggers' in fm and fm['triggers'] is not None:
                line_issues.append('ROOT_TRIGGERS')
            if 'tags' in fm and fm['tags'] is not None:
                line_issues.append('ROOT_TAGS')
            if 'related_skills' in fm and fm['related_skills'] is not None:
                line_issues.append('ROOT_RELATED_SKILLS')

            # Missing metadata.hermes.triggers (not already flagged as root)
            meta = fm.get('metadata', {}) or {}
            hermes = meta.get('hermes', {}) or {}
            if not line_issues and not hermes.get('triggers'):
                line_issues.append('NO_TRIGGERS')

            size = os.path.getsize(fp)
            if size > 95000:
                line_issues.append(f'OVER-95KB ({size:,}B)')

            if line_issues:
                issues.append((name, line_issues, size))
        except Exception as e:
            issues.append((name, [f'PARSE_ERROR: {e}'], 0))

if issues:
    print(f'{len(issues)} skills with frontmatter issues:')
    for name, line_issues, size in issues:
        print(f'  {name} — {" | ".join(line_issues)}')
else:
    print('All skills frontmatter-clean.')
```

### 7a. Detect Skills Entirely Lacking Metadata.Hermes

The Section 7 `NO_TRIGGERS` check catches skills with `metadata.hermes` but no `triggers` field. A deeper issue is skills that have no `metadata.hermes` block at all — the whole `metadata.hermes.{tags, triggers, related_skills}` structure is absent. These skills are invisible to tag/trigger-based resolution during tool calls.

The Section 7 scan does flag these as `NO_TRIGGERS` (since `fm.get('metadata', {})` returns `{}` and `{}.get('triggers')` is `None`), but the label is misleading — the fix is not "add triggers" but "add the entire `metadata.hermes` block."

Run this separate scan to distinguish the two cases:

```python
import os, yaml

SKILLS_DIR = '~/AppData/Local/hermes/skills'
no_meta = []    # entirely missing metadata.hermes
no_triggers = []  # has metadata.hermes but missing triggers

for root, dirs, files in os.walk(SKILLS_DIR):
    if '.archive' in root or '.curator_backups' in root:
        continue
    if 'SKILL.md' in files:
        fp = os.path.join(root, 'SKILL.md')
        try:
            with open(fp, 'r', encoding='utf-8') as f:
                text = f.read()
            parts = text.split('---', 2)
            if len(parts) < 3:
                continue
            fm = yaml.safe_load(parts[1])
            if not isinstance(fm, dict):
                continue

            name = os.path.basename(root)
            meta = fm.get('metadata', None)
            hermes = (meta or {}).get('hermes', None) if meta else None

            if hermes is None:
                no_meta.append(name)
            elif not hermes.get('triggers') and 'triggers' not in text.split('---', 2)[1]:
                no_triggers.append(name)
        except Exception:
            pass

print(f"Skills without metadata.hermes block entirely: {len(no_meta)}")
if no_meta:
    print(f"  Sample: {no_meta[:10]}{'...' if len(no_meta) > 10 else ''}")
print(f"Skills with metadata.hermes but no triggers: {len(no_triggers)}")
```

**Interpreting results:**
- **Without metadata.hermes (high severity):** Skill is invisible to the loader's tag/trigger resolution. Needs a full `metadata.hermes` block — `tags`, `triggers`, `related_skills` (see `hermes-agent-skill-authoring` for canonical structure).
- **With metadata.hermes but no triggers (medium severity):** Only missing `triggers`. Quicker fix — add a triggers list based on the skill's description and usage patterns.
- **Clean:** Has metadata.hermes with triggers — fully resolvable.

When the count of "without metadata.hermes" is large (50+ skills), a bulk backfill script is warranted (see Section 10).

#### How to Fix Root-Level Key Regressions

When a skill has root-level `triggers:` without `metadata.hermes`:

```python
import yaml
fp = 'path/to/SKILL.md'
with open(fp, 'r', encoding='utf-8') as f:
    text = f.read()
parts = text.split('---', 2)
fm = yaml.safe_load(parts[1])

# Move root-level triggers under metadata.hermes
root_triggers = fm.pop('triggers', None)
fm.setdefault('metadata', {}).setdefault('hermes', {})
fm['metadata']['hermes']['triggers'] = root_triggers

new_fm = yaml.dump(fm, default_flow_style=False, allow_unicode=True, sort_keys=False).strip()
parts[1] = new_fm
with open(fp, 'w', encoding='utf-8') as f:
    f.write('---\n'.join(parts))
```

For skills with minimal frontmatter (no `metadata` block at all), add the full structured block with `metadata.hermes.{triggers, tags, related_skills, version, author, license}`. See the `hermes-agent-skill-authoring` skill for the canonical YAML structure.

### 7c. Detect Name/Directory Mismatches

Skills where the YAML `name:` field in frontmatter doesn't match the directory basename cause confusion in logging, cross-referencing, and manual curation. While Hermes loads skills by file path (not name), mismatches produce misleading `related_skills` entries and make it harder to correlate usage-registry data with on-disk structure.

Common patterns:
- **Gstack flat namespace** — directory `gstack-autoplan/` but `name: autoplan`. This is a deliberate convention (53 gstack skills follow it). Flag but do not auto-fix.
- **✅ Resolved: job-agent mismatches** — directory `job-agent/dashboard/` → `name: dashboard` (and 3 others). All 4 name-field mismatches fixed per `name:` → directory convention.
- **MLOps expanded names** — directory `mlops/inference/vllm/` but `name: serving-llms-vllm`. Descriptive naming overlaps with the skill's description field.

Run this scan:

```python
import os, yaml

SKILLS_DIR = '~/AppData/Local/hermes/skills'
mismatches = []  # (path, dir_name, yaml_name)

for root, dirs, files in os.walk(SKILLS_DIR):
    if '.archive' in root or '.curator_backups' in root:
        continue
    if 'SKILL.md' in files:
        fp = os.path.join(root, 'SKILL.md')
        try:
            with open(fp, 'r', encoding='utf-8') as f:
                parts = f.read().split('---', 2)
            if len(parts) < 3:
                continue
            fm = yaml.safe_load(parts[1])
            if not isinstance(fm, dict):
                continue
            dir_name = os.path.basename(root)
            yaml_name = fm.get('name', '')
            if yaml_name and yaml_name != dir_name:
                mismatches.append((os.path.relpath(root, SKILLS_DIR), dir_name, yaml_name))
        except Exception:
            pass

if mismatches:
    gstack_pattern = [m for m in mismatches if m[0].startswith('gstack')]
    others = [m for m in mismatches if not m[0].startswith('gstack')]
    print(f'Total mismatches: {len(mismatches)}')
    print(f'  Gstack (deliberate): {len(gstack_pattern)}')
    print(f'  Other (likely actionable): {len(others)}')
    for path, dir_name, yaml_name in others:
        print(f'    {path:50s}  dir={dir_name:30s}  name={yaml_name}')
else:
    print('All skill names match their directory names.')
```

**Remediation:** For true mismatches (non-gstack), update the `name:` field in the YAML frontmatter to match the directory name using the standalone `patch()` tool. Do NOT rename directories to match `name:` — that would break every `related_skills` reference across the library. The directory is the canonical identifier; `name:` is metadata.

**Pitfalls:**
- **Gstack is intentional** — `gstack-autoplan` directories use short names (`autoplan`) so `skills_list` output is readable without the `gstack-` prefix. Do not "fix" these.
- **.archive skills** — retired skills frequently have mismatched names. Skip them — archive is not actively maintained.
- **Multi-level categories** — a skill at `mlops/inference/vllm/` may have `name: serving-llms-vllm` which describes what the skill does rather than just the tool name. Use judgment: if the name adds clarity beyond the directory path, it may be intentional.
- **The `name:` field is optional** — some skills omit it entirely and Hermes infers from the directory name. `None` values are not mismatches; only explicit non-matching strings are.

### 7b. Detect Minimal Frontmatter (Missing Root-Level Fields)

Flat-imported skills (top-level skills not under a category directory) and batch-imported skills commonly lack full frontmatter — specifically `version`, `author`, `license`, `platforms` at the YAML root level. These are not required for Hermes trigger/load resolution (which uses `metadata.hermes.*`) but are important for documentation completeness, portfolio presentation, and cross-library consistency.

Run this scan to detect skills with incomplete root-level frontmatter:

```python
import os, yaml

SKILLS_DIR = '~/AppData/Local/hermes/skills'
minimal = []

for root, dirs, files in os.walk(SKILLS_DIR):
    if '.archive' in root or '.curator_backups' in root:
        continue
    if 'SKILL.md' in files:
        fp = os.path.join(root, 'SKILL.md')
        try:
            with open(fp, 'r', encoding='utf-8') as f:
                parts = f.read().split('---', 2)
            if len(parts) < 3:
                continue
            fm = yaml.safe_load(parts[1])
            if not isinstance(fm, dict):
                continue
            name = os.path.basename(root)
            missing = []
            for field in ['version', 'author', 'license', 'platforms']:
                if field not in fm or fm[field] is None:
                    missing.append(field)
            if missing:
                minimal.append((name, missing))
        except Exception:
            pass

if minimal:
    print(f'{len(minimal)} skills with minimal frontmatter:')
    for name, missing in sorted(minimal):
        print(f'  {name} — missing: {", ".join(missing)}')
else:
    print('All skills have complete root-level frontmatter.')
```

**Typical missing patterns and conventions:**
| Field | Default for agent-created skills | Default for user/portfolio skills |
|-------|----------------------------------|-----------------------------------|
| `version` | `1.0.0` | `1.0.0` |
| `author` | `Hermes Agent` | User/org name |
| `license` | `MIT` | `Proprietary` |
| `platforms` | `[linux, macos, windows]` | Match the repo's platform targets |

**Fix procedure:**
1. Use the standalone `patch()` tool (handles CRLF files correctly on Windows — unlike `skill_manage(action='patch')`)
2. Add the missing fields to the YAML frontmatter, keeping alphabetical order: `author`, `license`, `platforms`, `version`
3. Verify with `grep -a` on CRLF files or re-run the detection script

**Pitfalls:**
- A skill can have `metadata.hermes.block` with all required trigger/tag fields but still be missing root-level `version`/`author`/`license`/`platforms`. This scan finds those.
- Do NOT add `platforms` for skills that are purely config or documentation (no code to run) — those are platform-agnostic.
- Flat-imported skills under `skills/*/` (not in a category subdirectory) are the most common source of this pattern — batch-imported skills from hub repos often arrive with minimal frontmatter.

#### Version-Field Automated Fix

The most common minimal-frontmatter gap is a missing `version:` field — skills that have `name:`, `description:`, and `category:` but no version. During the Jul 21 Skillmate pulse, 3 of 29 recently-modified skills (10.3%) had this gap.

Run the audit script to scan and optionally fix:

```bash
cd ~/AppData/Local/hermes/skills

# Scan only — report missing version fields
python scripts/version-field-audit.py

# Dry-run — show what would be fixed
python scripts/version-field-audit.py --fix --dry-run

# Scan + fix — patch all missing to version: 1.0.0
python scripts/version-field-audit.py --fix

# Scan a custom path
python scripts/version-field-audit.py --path /path/to/skills
```

The script inserts `version: 1.0.0` immediately after the `name:` line in the YAML frontmatter. It handles both CRLF (Windows) and LF line endings, preserves all existing frontmatter keys, and skips `.archive/`, `_drafts/`, `.curator_backups/`, and `.hub/` directories.

**PITFALL: Avoid manual scoping to "recently-modified" skills.** A Jul 21 11:17 pulse that checked only 29 skills modified in the previous 24h found 3 missing version fields. A full `os.walk` sweep 6 hours later found 4 MORE in subdirectories. A final Phase 3 sweep (Jul 22) found 6 MORE (scroll-world suite + skip-tracing) — top-level flat skills that were somehow missed by both previous passes. **Total: 13 skills across 3 phases.** The script already walks every directory — just run it on the full library from the start. Manual `find -newermt` scoping misses subdirectory skills AND can miss top-level flat skills that the initial scan somehow skips. Use `python scripts/version-field-audit.py --fix` once and be done. The sweep is now 100% complete — see `references/version-field-sweep-2026-07-21.md` for final state.

### 8. Detect Name Collisions Between Local and External Directories

Skills in `external_dirs` (configured in Hermes config.yaml under `skills.external_dirs`) can collide with same-named skills in the local skills directory. The resolver finds both copies and returns `Ambiguous skill name` — agents loading by bare name silently skip the skill, losing its guidance.

This caused 20 skills to be unreachable in every session that references them by bare name (confirmed Jul 14 Skillmate pulse — `skill_view()` returns `Ambiguous skill name` for all 20).

| Skill | Local Path | External Path | Version Drift Status |
|-------|-----------|---------------|-------------------|
| `hermes-agent-skill-authoring` | flat root | `software-development/` | ✅ Synced to v1.25.0 (was v1.0.0) |
| `plan` | flat root | `software-development/` | ✅ Already matched v1.0.0 |
| `requesting-code-review` | flat root | `software-development/` | ✅ Already matched v2.0.0 |
| `subagent-driven-development` | flat root | `software-development/` | ✅ Synced to v1.3.0 (was v1.1.0) |
| `systematic-debugging` | flat root | `software-development/` | ✅ Synced to v1.10.0 (was v1.1.0) |
| `test-driven-development` | flat root | `software-development/` | ✅ Synced to v2.0.0 (was v1.1.0) |
| `writing-plans` | flat root | `software-development/` | ✅ Already matched v1.1.0 |
| `agent-zero-bridge` | `software-development/` | `software-development/` | ✅ Already matched v1.0.0 |
| `building-mcp-servers` | `software-development/` | `software-development/` | ✅ Version field added v1.12.0 |
| `debugging-hermes-tui-commands` | `software-development/` | `software-development/` | ✅ Already matched v1.0.0 |
| `fastapi-mcp-bridge` | `software-development/` | `software-development/` | ✅ Already matched v1.0.0 |
| `firefox-remote-control` | `software-development/` | `software-development/` | ✅ Version field added v1.0.0 |
| `legal-advisory-agent` | `software-development/` | `software-development/` | ✅ Synced to v1.1.0 (was v1.0.0) |
| `node-inspect-debugger` | `software-development/` | `software-development/` | ✅ Already matched v1.0.0 |
| `python-debugpy` | `software-development/` | `software-development/` | ✅ Synced to v1.1.0 (was v1.0.0) |
| `spike` | `software-development/` | `software-development/` | ✅ Already matched v1.0.0 |
| `token-optimization-rtk` | `software-development/` | `software-development/` | ✅ Already matched v1.0.0 |
| `voice-agent-architecture` | `software-development/` | `software-development/` | ✅ Already matched v1.0.0 |
| `web-scraping-scrapling` | `software-development/` | `software-development/` | ✅ Already matched v1.0.0 |

### 8a. Detect Loose Files at Skills Root

Non-SKILL.md files sitting directly in the skills directory root (alongside skill directories) are **orphans** — they are not valid skills but clutter the namespace and mislead `ls`-based counts. Common culprits: research notes, architecture maps, or planning docs that were placed in skills/ for convenience.

Detection:

```python
import os
from pathlib import Path

SKILLS_DIR = Path('~/AppData/Local/hermes/skills').expanduser()
VALID_EXTENSIONS = {'.md', '.json', '.html', '.yaml', '.yml', '.txt'}

orphans = []
for entry in SKILLS_DIR.iterdir():
    if entry.is_file() and entry.suffix in VALID_EXTENSIONS:
        # Check if it's a proper SKILL.md (must be inside a directory)
        if entry.name != 'SKILL.md':
            size = entry.stat().st_size
            orphans.append((entry.name, size))

if orphans:
    print(f'{len(orphans)} loose file(s) at skills/ root:')
    for name, size in sorted(orphans):
        print(f'  {name:45s} {size:,} bytes')
else:
    print('No loose files at skills/ root.')
```

**Remediation (ordered by preference):**
1. **Convert to proper skill** — create skill directory, move file to `SKILL.md`, add YAML frontmatter
2. **Stage in `_drafts/` with triage README** — if the orphan is an idea stub (not ready to be a proper skill) but has potential. Creates `_drafts/<name>.md` and maintains a `_drafts/README.md` with a triage table (name, domain, priority). This is the best option for loose files that are clearly skill proposals rather than stale docs or duplicates. Keeps the root clean while preserving the proposal for future authoring.
3. **Move to docs/** or profile directory — if it's a reference doc, not a skill
4. **Delete** — if content is stale, duplicated, or irrelevant

**Pro tip:** Draft/orphan `.md` files tend to re-accumulate between pulses. Check `_drafts/` periodically and promote high-priority candidates to proper skills. Track the draft count trajectory in PULSE.md to spot if accumulation is accelerating (e.g., 17 in 4 days is a significant rate).

**Pitfalls:**
- `.bundled_manifest`, `.curator_state`, `.usage.json`, and `.usage.json.lock` are system files — do NOT treat them as orphans
- `.archive/`, `.curator_backups/`, `.hub/` are system directories — do NOT scan inside them
- A loose `README.md` may be from an accidental clone or unzip into skills/ — check git history or parent context before removing
- **Orphan `.md` content may already be superseded by a proper skill elsewhere** — Before converting a loose research doc or architecture map into a new skill, always check whether a skill with a similar or related name already exists (e.g., `hermes-agent-replay.md` → `devops/hermes-replay/SKILL.md`). Use `grep -rl <topic> ~/AppData/Local/hermes/skills` or `skill_view(<related-name>)` to locate existing skills on the same subject. If the proper skill already exists, the orphan is a stale predecessor that should be deleted, not converted.
- **A flat import (direct `cp` of a standalone `.md` into skills/) can persist for weeks** — These files sit undetected because the skill loader silently skips non-directory entries. Only a dedicated orphan scan (Section 8a) catches them. Schedule a quarterly scan even if no pulse has reported issues.

### 8b. Same-Name Cross-Path Drift Detection

Same-name cross-path duplicates are skills that exist in both the local skills directory and an external directory, but at *different relative paths* (e.g., local `github-code-review/` vs external `github/github-code-review/`). Unlike Step 8 collisions, these do NOT trigger `Ambiguous skill name` — the resolver loads from one copy and the other is silently ignored or serves the other profile. The two copies can independently drift and serve different guidance.

**Known cross-path duplicates (detected 2026-07-14 Skillmate pulse):**

| Skill | Local Path | External Path | Version State |
|-------|-----------|---------------|---------------|
| `github-code-review` | flat root | `github/github-code-review/` | ✅ Resolved 2026-07-19: synced v2.0.0 → hermes-config@e5b4dc0 |

**Related orphan cleanup (2026-07-15/19 Skillmate pulses):** Two orphan `.md` files were found and removed from the skills root on Jul 15 — `hermes-agent-replay.md` (8.5KB, superseded by `devops/hermes-replay` v2.0.0) and `formalize-ai-developer-workflow--adw--pa.md` (430B stub). By Jul 19 10:35, **17 new draft `.md` files** had accumulated (created Jul 18-19, ranging 500-948 bytes). These were moved to `_drafts/` with a triage README. By Jul 19 16:37, **6 more draft stubs** had appeared (all timed Jul 19 11:10, suggesting a batch-generation process that writes to root instead of `_drafts/`) — swept to `_drafts/` bringing the total to **25 draft stubs**. **Pattern confirmed:** loose draft files re-accumulate at ~5-6 per 5-hour window during active hours. The `_drafts/` staging directory (Section 8a remediation option 2) is the standard response — migrate immediately on detection rather than leaving them at root. The batch-timing pattern suggests the generating process should be fixed to write to `_drafts/` directly.

Detection script:

```python
import os
from pathlib import Path

SKILLS_DIR = Path('~/AppData/Local/hermes/skills').expanduser()
external_dirs = [
    Path('~/Documents/github/hermes-config/skills').expanduser(),
]

# Build map: skill_name -> local path
local_map = {}
for root, dirs, files in os.walk(SKILLS_DIR):
    if '.archive' in root or '.curator_backups' in root:
        continue
    if 'SKILL.md' in files:
        local_map[os.path.basename(root)] = root

# Check external dirs for same-name skills at different relative paths
for ext_dir in external_dirs:
    if not ext_dir.is_dir():
        continue
    for root, dirs, files in os.walk(str(ext_dir)):
        if 'SKILL.md' in files:
            skill_name = os.path.basename(root)
            ext_rel = os.path.relpath(root, str(ext_dir))
            local_path = local_map.get(skill_name)
            if local_path:
                local_rel = os.path.relpath(local_path, str(SKILLS_DIR))
                if local_rel != ext_rel:
                    # Same name, different path — potential drift
                    local_ver = '?'
                    ext_ver = '?'
                    try:
                        local_ver = open(os.path.join(local_path, 'SKILL.md')).read().split('---')[1].split('version:')[1].split('\\n')[0].strip()
                    except: pass
                    try:
                        ext_ver = open(os.path.join(root, 'SKILL.md')).read().split('---')[1].split('version:')[1].split('\\n')[0].strip()
                    except: pass
                    match = '✅' if local_ver == ext_ver else '❌'
                    print(f'{match} {skill_name:35s} local={local_ver:10s} ext={ext_ver:10s}  local={local_rel}  ext={ext_rel}')
```

**Remediation:**
- If the local copy is authoritative and newer → remove the external duplicate
- If the external copy is the canonical source → remove or symlink the local duplicate (if no collision)
- If both should coexist → ensure versions stay synced and document the dual location in the skill's frontmatter

```python
import os

SKILLS_DIR = '~/AppData/Local/hermes/skills'
local_canonical = set()
for root, dirs, files in os.walk(SKILLS_DIR):
    if '.archive' in root or '.curator_backups' in root:
        continue
    if 'SKILL.md' in files:
        local_canonical.add(os.path.relpath(root, SKILLS_DIR))

# Check every external_dirs entry from config.yaml
# Replace with your actual external_dirs paths
external_dirs = [
    '~/Documents/github/hermes-config/skills',
]

collisions = []
for ext_dir in external_dirs:
    ext_dir = os.path.expanduser(ext_dir)
    if not os.path.isdir(ext_dir):
        continue
    for root, dirs, files in os.walk(ext_dir):
        if 'SKILL.md' in files:
            rel = os.path.relpath(root, ext_dir)
            if rel in local_canonical:
                collisions.append((rel, root, os.path.join(SKILLS_DIR, rel)))

if collisions:
    print(f'{len(collisions)} name collision(s) found:')
    for rel, ext_path, local_path in collisions:
        print(f'  {rel}')
        print(f'    External: {ext_path}')
        print(f'    Local:    {local_path}')
else:
    print('No name collisions detected.')
```

#### How to Remediate Collisions

Choose ONE option per collision:

**Option A — Remove local duplicate (if external copy is authoritative)**
```bash
rm -rf "~/AppData/Local/hermes/skills/<colliding-rel-path>"
```

**Before remediating any collision, always check for version drift** — colliding copies may have different content versions. A stale external copy silently serves outdated guidance to every agent that loads the skill:

```bash
# Compare version fields between local and external copies
grep -h "^version:" ~/AppData/Local/hermes/skills/<colliding-rel-path>/SKILL.md ~/Documents/github/hermes-config/skills/<colliding-rel-path>/SKILL.md
# Diff the full content to see what changed
diff ~/AppData/Local/hermes/skills/<colliding-rel-path>/SKILL.md ~/Documents/github/hermes-config/skills/<colliding-rel-path>/SKILL.md | head -40
```

If the local copy is newer (higher version, richer metadata, extra sections), **Option B is the safer choice** — remove the stale external duplicate so agents load the updated guidance.

**Option B — Remove external duplicate (if local copy is authoritative)**
Remove the external dir entry from `config.yaml` under `skills.external_dirs`, or delete the colliding path in the external repo.

**Option C — Rename one copy** (as last resort — breaks any `related_skills` refs to the old name)
Change the directory name and update `name:` in frontmatter. Then fix all `related_skills` references across the library.

**Option D — Report and move on** (if both copies are intentional and should coexist)
Add a note to the skill description noting the collision so agents know to load by the full `category/skill-name` path. The collision will persist but is documented.

### 9. Subdirectory Skill Symlink Audit

Subdirectory skills (nested under a category like `software-development/subagent-driven-development/`) are NOT resolvable by bare name at root level — any `related_skills` reference to just `subagent-driven-development` fails, and job loading skips them as "not found". Create root-level symlinks for skills that are heavily referenced from outside their category.

Workflow:

```
1. Identify candidates — grep for related_skills references to skills that live in subdirectories
2. Check collision table — skip any skill listed in the external-dir collision table (Step 8); those need Option A/B remediation, not symlinks
3. Create symlinks via `cmd /c mklink /D <link> <target>` (NOT `ln -s`, which copies on MSYS)
4. Verify resolution — `test -f skills/<link>/SKILL.md` must succeed
5. Update audit trail — record in PULSE.md or cross-ref audit
```

Detection script:

```bash
cd ~/AppData/Local/hermes/skills
# Find subdirectory skills (category/name depth)
find . -maxdepth 3 -name 'SKILL.md' | grep -v '/.archive/' | sort
# Cross-reference with root-accessible names
for d in */SKILL.md; do basename "$(dirname "$d")"; done | sort
```

Verification:

```bash
cd ~/AppData/Local/hermes/skills
# List all symlinks
find . -maxdepth 1 -type l -printf '%f\n' | sort
# Verify each resolves
for name in <symlink1> <symlink2> ...; do
  if [ -f "$name/SKILL.md" ]; then
    echo "✅ $name — accessible ($(wc -c < "$name/SKILL.md") bytes)"
  else
    echo "❌ $name — not accessible"
  fi
done
```

### 10. Bulk Metadata.Hermes Backfill

When 50+ skills lack the `metadata.hermes` block (or when a systematic audit reveals >90% of the library is missing it), individual edits via `skill_manage(action='patch')` are prohibitive. Use a bulk Python script that reads each SKILL.md, adds a structured `metadata.hermes` block based on the skill's existing content, and writes back.

#### Backfill Strategy

1. **Categorize skills by frontmatter state:**
   - Group A: Has `metadata.hermes` — skip (already done)
   - Group B: Has valid YAML but no `metadata.hermes` — target for auto-generation
   - Group C: No valid frontmatter at all — handle manually

2. **Auto-generate metadata tags from category.** Derive tags from the skill's directory path and description:

```python
import os, re, yaml
from pathlib import Path

SKILLS_DIR = Path('~/AppData/Local/hermes/skills').expanduser()

def derive_tags(skill_name: str, description: str, category: str) -> list:
    """Derive reasonable tags from the skill's metadata."""
    tags = [skill_name.replace('-', ' ')]
    for word in re.findall(r'[a-z]+', skill_name):
        if len(word) > 3 and word not in ('with', 'from', 'into'):
            tags.append(word)
    if category and category != '.':
        tags.append(category)
        tags.append(category.replace('-', ' '))
    return list(dict.fromkeys(tags[:8]))  # deduplicate, max 8

def derive_triggers(name: str, description: str) -> list:
    """Extract candidate triggers from description keywords."""
    stopwords = {'a', 'an', 'the', 'and', 'or', 'but', 'in', 'on', 'at',
                 'to', 'for', 'of', 'with', 'by', 'from', 'as', 'into'}
    words = re.findall(r'[a-zA-Z][a-zA-Z.-]+', description.lower())
    # Take unique non-stopwords from the first ~15 words
    seen = set()
    triggers = []
    for w in words:
        if w not in stopwords and len(w) > 2 and w not in seen:
            triggers.append(w)
            seen.add(w)
    return triggers[:12]  # max 12 triggers

def add_metadata_block(fp: Path, category: str):
    """Inject metadata.hermes into a skill that lacks it."""
    with open(fp, 'r', encoding='utf-8') as f:
        text = f.read()
    parts = text.split('---', 2)
    if len(parts) < 3:
        return False, 'no frontmatter'
    fm = yaml.safe_load(parts[1])
    if not isinstance(fm, dict):
        return False, 'bad frontmatter'
    if fm.get('metadata', {}).get('hermes'):
        return False, 'already has metadata.hermes'

    name = fm.get('name', fp.parent.name)
    desc = fm.get('description', '')
    tags = derive_tags(name, desc, category)
    triggers = derive_triggers(name, desc)

    fm['metadata'] = {'hermes': {
        'tags': tags,
        'triggers': triggers,
    }}
    # Preserve existing top-level keys; re-serialize
    new_fm = yaml.dump(fm, default_flow_style=False,
                       allow_unicode=True, sort_keys=False).strip()
    parts[1] = new_fm
    new_text = '---\n'.join(parts)
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(new_text)
    return True, f'tags={tags[:3]}..., {len(triggers)} triggers'

# Run against every active SKILL.md
count = 0
for root, dirs, files in os.walk(SKILLS_DIR):
    if '.archive' in root or '.curator_backups' in root:
        continue
    if 'SKILL.md' in files:
        fp = Path(root) / 'SKILL.md'
        # Determine category from directory structure
        rel = fp.relative_to(SKILLS_DIR)
        category = str(rel.parents[1]) if len(rel.parents) > 2 else '.'
        ok, msg = add_metadata_block(fp, category)
        if ok:
            count += 1
            print(f"  [{count}] {fp.parent.name} — {msg}")

print(f"\nModified {count} skills.")
```

3. **Post-backfill audit:** Run the Section 7a scan to verify zero skills remain without `metadata.hermes`.

4. **Manual refinement:** Auto-generated tags and triggers are a starting point, not a final artifact. Each skill's `tags` and `triggers` should be reviewed during its next natural use cycle. High-value skills (gstack, security, devops, software-development) deserve immediate manual review.

#### Pitfalls

- **Auto-generated triggers may be noisy** — NLP keyword extraction from descriptions can pick up stopwords, generic verbs, or irrelevant adjectives. The first pass gets skills 70% of the way there; the remaining 30% requires human/agent judgment.
- **YAML re-serialization may reorder keys** — `yaml.dump(sort_keys=False)` preserves insertion order in Python 3.8+ but only for the top-level dict. Nested dicts may reorder. Verify with a diff on a sample before running bulk.
- **Race condition with concurrent agents** — If another agent (Scribe pulse, Weaver deploy) modifies a skill during the backfill run, one agent's changes will be lost. Run backfill during scheduled downtime or lock the skills directory.
- **Backup before bulk operations** — Always snapshot the skills directory before running bulk writes:

```bash
cp -r ~/AppData/Local/hermes/skills ~/AppData/Local/hermes/skills.backup.$(date +%F_%H%M)
```

## Library Design Principles

- **CLASS-LEVEL skills** — each skill covers a class of work, not a single session or error. A skill named after a PR number, error string, or one-shot task is too narrow.
- **Rich SKILL.md** — every skill needs clear triggers, numbered steps, a pitfalls section, and a verification workflow.
- **`references/` directory** — session-specific detail (error transcripts, provider quirks, reproduction recipes) belongs in `references/`, not in the SKILL.md body.
- **Avoid flat narrow lists** — multiple one-session skills should consolidate into an umbrella skill with sub-sections.
- **User preferences in skill body** — when a user corrects how you communicate, format, or sequence work, embed that in the governing skill. Memory captures identity; skills capture procedure.
- **Deferred-rebase escalation principle (for fork-maintenance skills):** When a pre-rebase assessment recommends rebase but the agent defers, the cost compounds non-linearly. Each cycle of deferral adds upstream commits that may refactor shared infrastructure your local patches depend on. A deferral that seems rational at 100 behind becomes a multi-hour conflict resolution at 400 behind. Skills tracking divergence (like `dynamic-upstream-merger`) should include a deferral-count tracker and hard escalation thresholds (e.g., defer no more than 3 consecutive cycles; rebase immediately when behind-count doubles between checks). This principle emerged from 7+ cycles of real-world deferred-rebase tracking and is a pattern-librarian-level lesson — capture it once, in the library design principles, rather than embedding it in a single skill that only gets loaded for git work.

### 8c. _Drafts Promotion Audit

After loose files are staged into `_drafts/` (Section 8a), they accumulate and must be systematically triaged to avoid permanent stagnation. A draft that sits unactioned for 7+ days is at risk of becoming noise. Run this audit periodically to clear the backlog.

**Audit workflow:**

```
1. COUNT drafts → ls _drafts/*.md | grep -v README | wc -l
2. If count > 0, categorize by domain (finance, design, ML, etc.)
3. Assess each draft's readiness:
   - Tier 1 (HIGH): Has real content, uses existing MCP/tools, just needs procedural steps authored
   - Tier 2 (MEDIUM): Clear utility, self-contained, fills a domain gap
   - Tier 3 (LOW/NICHE): Viable but narrow audience, or needs significant authoring effort
4. Flag delete candidates: drafts that mandate disclaimers, conflict with unrestricted mode,
   duplicate existing skills, or are out of scope
5. Report: total count, per-domain breakdown, promotion candidates, delete candidates,
   accumulation trajectory (is the count growing, stable, or shrinking?)
```

**Tier definitions:**

| Tier | Criteria | Example | Action |
|------|----------|---------|--------|
| **Tier 1** | Content-rich (700B+), references real tools/MCP endpoints, clear use case | `investor-guide` — maps Dunnan ladder to existing OpenBB MCP tools | Promote to proper skill next cycle |
| **Tier 2** | Clear utility, well-described, self-contained technique | `vram-cost-estimation` — ML ops sizing methodology | Author within 2-3 cycles |
| **Tier 3** | Niche audience, stub-level content, or duplicates existing coverage | `tcg-roi-analyzer` — gaming collector EV math | Promote only if user signals interest |
| **Delete** | Anti-pattern, conflicts with operating model, out of scope | `health-medical-response` — mandates disclaimers (anti-unrestricted) | Delete immediately |

**Assessment signals:**
- **Content depth** — a 948B draft with multi-paragraph context is more actionable than a 495B stub with `1. TBD` steps
- **MCP tool readiness** — drafts that reference existing MCP tools (OpenBB, trading-signals, browser) require less scaffolding to author than drafts requiring new tooling
- **Domain gap** — a draft that fills a domain with zero existing skills (e.g., ML ops) is higher priority than one that overlaps 8 existing skills (e.g., web design)
- **Accumulation trajectory** — track `_drafts/` count across pulses. If drafts pile faster than they're promoted, the `_drafts/` system is failing its purpose

**Pitfalls:**
- **Do NOT auto-promote without reading the draft** — a file name alone doesn't reveal content quality. Always `read_file` the draft before assigning a tier.
- **Accumulation vs stagnation** — 24 drafts that haven't changed in 5 days is stagnation, not active accumulation. The pipeline is blocked at the promotion step, not the creation step. Fix by promoting at least 1 draft per pulse.
- **Do NOT count README.md as a draft stub** — it's triage metadata. Subtract it from `_drafts/` file count.
- **Draft file names are unreliable indicators** — truncated MSYS paths (25-char limit) produce partial names. Read content, not names.
- **File size is a poor proxy for content readiness** — A 948B draft can be a stub whose bulk is TBD template boilerplate (`1. TBD`, `2. TBD`, `3. TBD`, empty verification checkboxes). The Tier 1 "Content-rich (700B+)" heuristic is a _screen_ to prioritize which drafts to examine, not an _assessment_ of readiness. After screening by size, always call `read_file()` on each shortlisted draft and check for actual procedural steps, tool references, and non-TBD content before assigning a tier. Example: `create--small-investor-guide--skill-that.md` was 948B (above the 700B threshold) but had zero usable steps — all TBD. It belongs in Tier 2 or 3, not Tier 1, despite the file size.
- **Some drafts may already exist as proper skills** — Before flagging a big draft for promotion, search for existing skills on the same topic. Example: `ultimate-firefox-mcp-browser` appeared as a 7.5KB draft but already existed at `devops/ultimate-firefox-mcp-browser/SKILL.md`. The draft was a duplicate, not a promotion candidate.

**Related**
- `discord-report-format` — reporting format for pulse deliverables
- Skillmate PULSE.md at `profiles/skills-lead/PULSE.md` — canonical _drafts audit log

## Related

- `references/usage-ghost-cleanup.md` — ghost detection walkthrough
- `references/cross-ref-audit.md` — full cross-reference integrity scan methodology and history
- `references/metadata-hermes-audit.md` — metadata.hermes gap scan methodology and historical baseline
- `references/gstack-dup-audit.md` — gstack file-system duplication detection (4 skills in both `gstack/` subdir and `gstack-XXX/` top-level)
- `references/version-field-sweep-2026-07-21.md` — full library version-field compliance sweep results
- `scripts/ghost-detect.py` — standalone ghost detection script
- `hermes-agent-skill-authoring` — authoring and structuring skills
