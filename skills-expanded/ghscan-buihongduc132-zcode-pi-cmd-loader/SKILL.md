---
description: Reconstruct a proper skill from a cmd .md + cmd-resource dir. LOSSLESS. Inverse of skill-to-cmd.
---

$ARUGMENTS

---

This is to generalize the process / steps that you did. 

## Global vs local
This is the scope of where the playbook will apply in the machine. 
Local playbook should be able to apply for this project itself. 
Global playbook should be able to apply to ANY project. Make it agnostic. 

if the user mentioned it as "local". Then you can retain the project specific information. 
Otherwise it will be "global" (default). Which should be generic , must strip all the information / workflow / knowledge about the current project and generalize it. 

If it required to be GLOBAL , but you are realize that it is UNABLE to generalize it or unclear how to generalize it. STOP immediately. ASK user. 

### Local
can reference to project document / files / flow/**;
can reference to remote document , git source. 

### Global
ONLY reference to REMOTE source. Do not reference anything in the local project. 

## cmd-resource (OUR INVENTED LAYER — same as skill-to-cmd)

The `_script/` + `_references/` convention is OUR invented layer (NOT documented in pi upstream, NOT findable on the web). This cmd is the canonical doc for the inverse direction. Source layout:

```
<piPromptDir>/
├── <cmdName>.md                       ← the cmd (1 level)
├── _script/<cmdName>/                 ← scripts the cmd calls
│   ├── <file>.sh | .py | .ts
│   └── <sub>/<file>
└── _references/<cmdName>/             ← reference docs the cmd cites
    ├── <file>.md | .yaml | .json
    ├── _manifest.json                 ← OPTIONAL flatten mapping (if depth>2 was flattened)
    └── <sub>/<file>
```

### `<piPromptDir>` resolution
- Local: `./.pi/prompts/`
- Global: `~/.pi/agent/prompts/`

### cmd `.md` structure (what we parse)
```
---
name: <name>
description: <description>
origin: <URL or local path>           ← OPTIONAL but critical for lossless
origin_ref: <exact commit hash>        ← OPTIONAL but critical for lossless
---

<SKILL.md>
<skill body VERBATIM>
<SKILL.md/>

## cmd-resource index
- <abs-path-to-_references-file-1>
- <abs-path-to-_references-file-2>
- <abs-path-to-_script-file-1>
- ...

## User addition request 
$ARUGMENTS
```

### Skill target structure
```
<skill-dir>/
├── SKILL.md                          ← frontmatter + body
├── references/                       ← OR mirror upstream top-level dir name
│   └── <mirror-path-1>
├── scripts/                          ← OR mirror upstream top-level dir name
│   └── <file>
├── assets/ | templates/ | evaluators/ | ...   ← if upstream used them
└── ...
```

## Move vs Copy (MUST ask if ambiguous)

These `<a>-to-<b>` cmds MOVE or COPY content across scopes. Default is AMBIGUOUS. MUST ask user before proceeding if not specified.

### Definitions
- **MOVE**: source cmd (`.md` + cmd-resource dir) is REMOVED after reconstruction. Source scope loses the cmd. Irreversible without backup.
- **COPY**: source cmd REMAINS. Both scopes have it. Reversible.

### Ask gate (step 1 enforcement)
If user did NOT explicitly say "move" or "copy":
- STOP. Ask: `MOVE or COPY? (MOVE = delete cmd + cmd-resource after reconstruction; COPY = keep them)`
- Default suggestion: COPY (safer, reversible). But MUST get explicit confirmation before proceeding.
- DO NOT assume. DO NOT default silently. DO NOT proceed on ambiguity.

### Duplication / bloat callouts (MANDATORY)

**During the operation** — as you walk cmd-resource files (step 3 enumeration), if you spot content that MIGHT already exist in the destination scope (`<output-dir>/`), callout IMMEDIATELY before writing:
- "Potential duplicate: `<cmd-resource-file>` may already exist at `<output-dir>/<existing-skill>/<path>` OR in another skill at the same `<output-dir>/`. Verify before writing."
- Check by basename + content hash (md5/sha256). Near-duplicate (same intent, different wording) also counts — callout.

**After the operation** — once reconstruction is done, scan the destination scope for duplication/bloat:
- Same file content appearing 2+ times (within the new skill dir, OR across other skills at the same `<output-dir>/`).
- Same skill dir already exists at the destination (would have been overwritten — callout, ask user).
- Bloat: total destination size grew significantly (e.g. >2x) without clear reason.

Callout ALL findings in the final report (step 9). Do NOT silently deduplicate. Do NOT silently overwrite. Do NOT silently skip.

## GOAL (DOD)

Given a cmd (path to `<cmdName>.md` OR cmd name to resolve in `<piPromptDir>/`), produce a proper skill dir at `<output-dir>/<skill-name>/` containing:
- **`SKILL.md`** — frontmatter (`name`, `description`) + body verbatim from `<SKILL.md>` wrapper
- **Every cmd-resource file** mirrored back to its skill path
- **LOSSLESS** — byte-for-byte identical to the original skill (or to what `skill-to-cmd` would have produced)
- **Gist-pinned scripts** fetched + verified against pinned sha, written back as the original file content
- **cmd-only artifacts dropped** — `## cmd-resource index`, `## User addition request`, `$ARUGMENTS`, `origin`/`origin_ref` frontmatter fields (these are NOT skill content)

If `origin` + `origin_ref` are present, MUST re-fetch upstream and DIFF against the reconstruction. The reconstruction MUST match upstream byte-for-byte (or callout any unavoidable divergence).

If `origin` is missing or unreachable, reconstruct from cmd-resource alone, normalize top-level dir to `references/` + `scripts/`, callout that upstream top-level dir names may differ.

The reconstruction MUST satisfy lossless verification (step 9). If it fails, STOP and callout — do NOT report partial work as done.

---

## IRONCLAD RULE — content is verbatim

EVERY piece of content reconstructed into the skill MUST be byte-for-byte identical to its source:
- **SKILL.md body** — verbatim from `<SKILL.md>...</SKILL.md/>` wrapper in the cmd `.md`
- **cmd-resource files** — copied verbatim to their mirror paths
- **Gist-pinned scripts** — fetched from pinned gist URL, verified `sha256` (or gist blob sha) matches, written as the original file content

- DO NOT reword ANY single word.
- DO NOT paraphrase.
- DO NOT "improve" grammar, punctuation, formatting, or wording.
- DO NOT translate.
- DO NOT fix typos.
- DO NOT add comments that look like part of the original.
- Whitespace, blank lines, trailing spaces — preserve as the source has them.
- DO NOT silently resolve flatten mappings — apply `_manifest.json` and record what was un-flattened.

The skill dir is a CARRIER, not an author. If the source content is wrong, callout in report — DO NOT silently fix.

LOSSLESS is non-negotiable. If any byte differs from source (cmd `.md` body, cmd-resource files, or pinned upstream), STOP and surface the diff. Do NOT proceed.

---

## Steps (imperative)

### 1. Locate the cmd source + ask MOVE vs COPY
- Input may be: path to `<cmdName>.md`, OR just `<cmdName>` (resolve via `<piPromptDir>/<cmdName>.md`).
- Resolve `<piPromptDir>`: try global (`~/.pi/agent/prompts/`) first, then local (`./.pi/prompts/`).
- Verify the cmd `.md` exists. If not, STOP, callout.

**MOVE vs COPY ask gate (see Move vs Copy section):**
- If user did NOT explicitly say move or copy → STOP, ask now. DO NOT proceed on ambiguity.
- Record user's choice for the report + for the post-operation cleanup (move = delete cmd `.md` + cmd-resource dirs after verify passes; copy = leave source intact).
- Deletion of a cmd + its cmd-resource is irreversible. MUST get explicit confirm.

### 2. Parse the cmd `.md`
Parse these sections in order:

**A. Frontmatter** (between `---` fences at top):
- Extract `name` → skill name.
- Extract `description` → skill description.
- Extract `origin` (URL or path) — OPTIONAL but critical for lossless verify.
- Extract `origin_ref` (exact commit hash) — OPTIONAL but critical for lossless verify.
- Record all for the report.

**B. `<SKILL.md>` / `<SKILL.md/>` wrapper:**
- Everything between (exclusive of the wrapper tags) is the SKILL.md body. Verbatim.
- Preserve whitespace, blank lines, trailing spaces EXACTLY.

**C. `## cmd-resource index` section:**
- Each line under the heading that starts with `-` is an ABSOLUTE path to a cmd-resource file.
- Collect them into an ordered list. Split into `_references/...` and `_script/...` groups.

**D. `## User addition request` section:**
- Drop entirely. This is cmd-only, NOT skill content. `$ARUGMENTS` line also dropped.

**E. Anything outside the above sections** (between wrappers, between sections):
- If non-empty and non-whitespace → callout as "unexpected cmd content outside known sections". DO NOT silently drop. Ask user whether to include in SKILL.md body or drop.

### 3. Enumerate cmd-resource dirs (exhaustive — NO shortcuts)
```bash
find <piPromptDir>/_references/<cmdName> <piPromptDir>/_script/<cmdName> -type f ! -name ".DS_Store" 2>/dev/null | sort
```
- Compare against the `## cmd-resource index` list from step 2C.
- If file count differs (dirs have files not in the index, or index cites non-existent paths) → STOP, callout, ask user.
- DO NOT stop at top-level. Recurse into every subdir.

### 4. Reconstruct skill dir — SKILL.md

Write `<output-dir>/<skill-name>/SKILL.md`:

```
---
name: <name from cmd frontmatter>
description: <description from cmd frontmatter>
---

<SKILL.md body verbatim from step 2B>
```

**Rules:**
- Skill SKILL.md frontmatter has ONLY `name` + `description`. DO NOT copy `origin`/`origin_ref` (those are cmd-only).
- Body is verbatim from the cmd's `<SKILL.md>` wrapper. No rewording.

### 5. Reconstruct cmd-resource → skill mirror paths

For each file in step 3, compute its skill target path:

**A. Reference / prose file under `_references/<cmdName>/`:**
- `<mirror-path>` = path relative to `_references/<cmdName>/`.
- Skill target = `<output-dir>/<skill-name>/<top-level-dir>/<mirror-path>`.

  Where `<top-level-dir>` is determined by:
  1. If `_manifest.json` exists at `_references/<cmdName>/_manifest.json` AND maps this mirror-path back to an original path → use the original top-level dir from the mapping.
  2. ELSE if `origin` + `origin_ref` are available AND upstream can be fetched → fetch upstream tree, find the file by basename + parent dir, infer the original top-level dir. Verify by content match.
  3. ELSE → default to `references/` (normalized). Callout that original top-level dir may differ.

**B. Script file under `_script/<cmdName>/`:**
- `<mirror-path>` = path relative to `_script/<cmdName>/`.
- Skill target = `<output-dir>/<skill-name>/<top-level-dir>/<mirror-path>`.

  Where `<top-level-dir>`:
  1. If `_manifest.json` exists and maps this mirror-path → use original.
  2. ELSE if upstream fetchable → infer from upstream tree.
  3. ELSE → default to `scripts/`. Callout.

**C. Gist-pinned shim file** (script file containing `# Gist (pinned): <url>` marker):
- Parse the shim: extract gist raw URL (with blob sha), upstream origin URL, commit hash, blob sha, run command.
- Fetch the pinned gist content: `curl -fsSL "<gist-raw-url-with-sha>"` (or `gh gist view <gist-id> --raw`).
- Verify the fetched content's sha matches the pinned sha recorded in the shim. If mismatch → STOP, callout (drift detected — the pinned gist content has changed since the cmd was built, which should be impossible with sha-pinned URLs but check anyway).
- Write the fetched content to the skill target path (per step 5A/5B path resolution), WITHOUT the shim metadata. The reconstructed file IS the upstream code, verbatim.
- Drop the shim wrapper lines (`# Source: ...`, `# Gist (pinned): ...`, `# Run: ...`) — those are cmd-only.

**D. Binary file** (PNG, SVG, JPEG, etc.):
- Copy verbatim to skill target. DO NOT base64.

**E. `_manifest.json` itself:**
- DO NOT copy into the skill. It is cmd-only metadata. But USE it (steps 5A.1, 5B.1) to resolve mirror paths.

**F. Empty file:**
- Copy as empty to skill target. Callout in report.

### 6. Apply `_manifest.json` flatten reverse (if present)

If `_references/<cmdName>/_manifest.json` exists:
```bash
cat <piPromptDir>/_references/<cmdName>/_manifest.json
```
Parse it. Format (from skill-to-cmd step 6):
```json
{
  "rubrics/quality-scoring.md": "rubrics/eval/quality/scoring.md",
  "reason": "skill nesting depth > 2; flattened to stay within cmd-resource 2-level limit"
}
```
- Keys are FLATTENED paths (what's in cmd-resource).
- Values are ORIGINAL paths (what should be in the reconstructed skill).
- For each entry: write the cmd-resource file to `<output-dir>/<skill-name>/<value>` (the original path).
- Callout each un-flattened path in the report (proves we restored the original nesting).

### 7. Write the skill files

For each cmd-resource file (after step 5 + 6 path resolution):

```bash
mkdir -p $(dirname <skill-target-path>)
# For verbatim copy:
cp <cmd-resource-source-path> <skill-target-path>
# For gist-pinned shim: write fetched+verified content to <skill-target-path>
```

**Mirror cmd-resource subdir structure** under the skill's top-level dir. Do NOT collapse.

**Dir depth guard:** if the reconstructed skill path exceeds the original skill's depth (no way to know without upstream — use `_manifest.json` or upstream fetch to verify), STOP and callout.

### 8. Verify LOSSLESS (MANDATORY before reporting done)

**Sub-case A — `origin` + `origin_ref` available and upstream fetchable:**

```bash
# Clone upstream at pinned commit
git clone --depth 1 --filter=blob:none --sparse <origin-url> /tmp/upstream-<cmdName>
cd /tmp/upstream-<cmdName>
git fetch origin <origin_ref> --depth 1
git checkout <origin_ref>

# Diff upstream skill dir vs reconstructed skill dir
diff -r <upstream-skill-dir> <output-dir>/<skill-name>/
```
- `diff -r` MUST output nothing (identical). ANY output → reconstruction is NOT lossless.
- For gist-pinned scripts: the reconstructed file content MUST match the upstream file content (because we fetched from the pinned gist which mirrors upstream at the pinned commit). Verify separately if `diff -r` flags the script.
- If diff produces output → STOP, surface the diff, fix, re-verify. Do NOT report partial work as done.

**Sub-case B — no `origin`, or upstream unreachable:**

```bash
# Count check
skill_files=$(find <output-dir>/<skill-name> -type f ! -name ".DS_Store" | wc -l)
cmd_files=$(find <piPromptDir>/_references/<cmdName> <piPromptDir>/_script/<cmdName> -type f ! -name "_manifest.json" 2>/dev/null | wc -l)
# skill_files MUST == cmd_files + 1 (for SKILL.md)
```

Then byte-for-byte diff each pair:
```bash
# For each cmd-resource file (excluding _manifest.json):
diff <cmd-resource-source-path> <skill-target-path>
# MUST output nothing for verbatim copies.
# For gist shims: skip diff on the shim, diff the fetched content vs upstream if available.
```

If ANY diff produces output (other than expected gist shim differences) → reconstruction is NOT lossless → STOP, fix, re-verify.

**Sub-case C — partial upstream (e.g. origin present but origin_ref missing):**
- Fetch upstream HEAD, diff, callout any mismatch. Treat as advisory, NOT a hard fail (because we can't pin the exact version).
- Better: ask user for the exact commit hash if lossless is required.

### 9. Report
- Output dir written: `<output-dir>/<skill-name>/`.
- Source cmd: `<cmdName>.md` + cmd-resource dirs.
- Origin (if any) + origin_ref (if any) used for lossless verify.
- Lossless verification result: pass/fail + any diffs found + which sub-case (A/B/C) was used.
- File count: cmd-resource files vs reconstructed skill files (must match +1 for SKILL.md).
- Gist scripts reconstructed: which files, gist URLs, blob shas, whether sha verify passed.
- Flatten reverse applied: which paths were un-flattened via `_manifest.json`.
- Verbatim confirmation: state that no content was reworded.
- **MOVE vs COPY**: user's choice + (if MOVE) confirmation cmd `.md` + cmd-resource dirs were deleted after verify passed.
- **Duplication / bloat callouts**: every potential duplicate spotted during op + every duplicate/bloat found in post-op scan. With paths + hashes.
- Callsout:
  - Any top-level dir normalization (sub-case B) — original dir name may differ.
  - Any binary files.
  - Any empty files.
  - Any cmd-only content dropped (`## cmd-resource index`, `## User addition request`, `$ARUGMENTS`, `origin`/`origin_ref`).
  - Any gist sha mismatch (drift detected).
  - Any unexpected content found in the cmd outside known sections.

---

## What WORKS (follow next time)

- **Parse cmd `.md` section-by-section** — frontmatter, `<SKILL.md>` wrapper, `## cmd-resource index`, `## User addition request`. Each has a known shape. Parse strictly, don't freehand.
- **`origin` + `origin_ref` are GOLD** — when present, lossless verify against upstream is deterministic. Always prefer sub-case A.
- **`diff -r <upstream> <reconstructed>`** — single command catches every byte of drift. Use it.
- **`_manifest.json` flatten reverse** — preserves original deep nesting that was flattened in cmd-resource. Always apply it if present.
- **Gist sha verification on fetch** — catches gist drift (shouldn't happen with sha-pinned URLs but defense in depth).
- **`find -type f | sort`** for exhaustive enumeration — deterministic order, catches nested dirs.
- **Mirror cmd-resource subdir structure under skill top-level dir** — preserves provenance.
- **Drop cmd-only artifacts explicitly** — `## cmd-resource index`, `## User addition request`, `$ARUGMENTS`, `origin`/`origin_ref`. List them in the report so it's clear what was intentionally dropped vs what might have been lost.
- **MANDATORY lossless verify (step 8)** — diff every file. Catches silent omissions before reporting done.

## What does NOT work (AVOID)

- **Freehand-parsing the cmd `.md`** — sections have known boundaries (frontmatter fences, `<SKILL.md>` tags, `## ` headings). Parse strictly. Freehand leads to body corruption.
- **Copying `origin`/`origin_ref` into SKILL.md frontmatter** — those are cmd-only. Skill frontmatter has ONLY `name` + `description`.
- **Including `## cmd-resource index` or `## User addition request` in SKILL.md** — those are cmd-only. Drop them.
- **Rewording ANY content** — verbatim is the contract. Copy typos. Callout separately.
- **Defaulting to `references/` + `scripts/` when `origin` is available** — wastes the lossless verify opportunity. Always try upstream fetch first (sub-case A).
- **Skipping the lossless verify** — without the diff, omissions hide. ALWAYS run step 8 before reporting done.
- **Silently dropping `_manifest.json`** — it's metadata, but USE it before dropping. Silent drop loses flatten reverse info.
- **Treating gist shim file as the script content** — the shim is metadata, NOT code. Fetch the gist, write the code.
- **Skipping gist sha verification** — defense in depth. Drift should be impossible with sha-pinned URLs, but verify anyway.
- **Reporting partial work as done** — if lossless verify fails, the reconstruction is INCOMPLETE. Stop, surface the diff, fix.
- **Guessing top-level dir names when `origin` is missing** — callout that the original may differ. Do not silently normalize.

## Tips / tricks

- **Resolve cmd name → path**: `ls ~/.pi/agent/prompts/<name>.md ./.pi/prompts/<name>.md 2>/dev/null` — picks first match.
- **Quick cmd-resource tree view**: `eza -TAL2 ~/.pi/agent/prompts/_references/<cmdName>` and `eza -TAL2 ~/.pi/agent/prompts/_script/<cmdName>`.
- **Sparse-checkout upstream at pinned commit** (large repos):
  ```bash
  git clone --depth 1 --filter=blob:none --sparse <origin-url> /tmp/upstream
  cd /tmp/upstream
  git fetch origin <origin_ref> --depth 1
  git checkout <origin_ref>
  git sparse-checkout set <skill-path-prefix>
  ```
- **Gist fetch + sha verify**:
  ```bash
  curl -fsSL "<gist-raw-url-with-sha>" > /tmp/gist-content
  # If gist blob sha is in URL, the URL itself pins it. Verify response matches.
  ```
- **`diff -r` for whole-tree compare**: `diff -r <upstream-skill-dir> <output-dir>/<skill-name>/` — single shot, recursive, lists every differing file.
- **Batch mirror copy**: `rsync -av --exclude='_manifest.json' <piPromptDir>/_references/<cmdName>/ <output-dir>/<skill-name>/references/` — but ONLY if normalization to `references/` is acceptable (sub-case B). Use `cp` per file for sub-case A to preserve upstream dir names.
- **Verify after write** — count reconstructed files == cmd-resource files + 1 (SKILL.md). Then `diff` every pair.
- **Drift detection on re-reconstruction** — if you've reconstructed before, `diff -r <old-reconstruction> <new-reconstruction>` reveals what changed between cmd versions. Surface to user; do NOT auto-apply.

## Useful references (REMOTE only — global)

- GitHub CLI sparse-checkout docs: https://git-scm.com/docs/git-sparse-checkout
- `gh gist view` docs: https://cli.github.com/manual/gh_gist_view
- `diff -r` recursive docs: https://www.man7.org/linux/man-pages/man1/diff.1.html
- Example skill with references (the kind that motivated cmd-resource): https://github.com/lyndonkl/claude/tree/main/skills/one-pager-prd

**NOTE on cmd-resource:** The `_script/` + `_references/` convention is OUR invented layer — NOT documented in pi upstream, NOT findable on the web. This cmd + `skill-to-cmd` together are the canonical docs for it. Do NOT cite external sources for cmd-resource layout.

## Mistakes / lessons learned

- **L1**: Freehand-parsed cmd `.md`, accidentally included `## cmd-resource index` in SKILL.md body → skill broke at runtime because the index path didn't exist in the skill dir. LESSON: parse sections strictly. Drop cmd-only sections explicitly.
- **L2**: Copied `origin`/`origin_ref` into SKILL.md frontmatter → upstream parser rejected unknown fields. LESSON: skill frontmatter has ONLY `name` + `description`. `origin`/`origin_ref` are cmd-only.
- **L3**: Treated gist shim file as the script content → reconstructed skill had shim metadata as code, broke execution. LESSON: shim is metadata. Fetch the gist, write the code.
- **L4**: Skipped gist sha verify "because sha-pinned URLs can't drift" → gist had been re-published with same filename but different blob (rare but possible if creator force-updated and sha wasn't actually in URL). LESSON: ALWAYS verify sha. Defense in depth.
- **L5**: Defaulted to `references/` + `scripts/` when `origin` was present → lost the original `templates/` and `evaluators/` top-level dir names. Upstream diff caught it. LESSON: always try upstream fetch (sub-case A) first.
- **L6**: Silently dropped `_manifest.json` without applying flatten reverse → reconstructed skill had flattened paths instead of original deep nesting. Upstream diff caught it. LESSON: apply `_manifest.json` BEFORE dropping it.
- **L7**: Forgot the lossless verify step → 2 cmd-resource files missing in reconstruction, skill broke at runtime. LESSON: step 8 (lossless verify) is MANDATORY. Always diff every file before reporting done.
- **L8**: Reworded a typo in SKILL.md body "to be helpful" → user diffed against cmd source and thought the reconstruction had drifted. LESSON: verbatim is the contract. Copy typos. Callout separately.
- **L9**: Reported partial work as done after lossless verify failed on one file → user trusted the report, shipped broken skill. LESSON: if lossless verify fails, reconstruction is INCOMPLETE. Stop, surface the diff, fix.
- **L10**: Didn't enumerate cmd-resource dirs recursively, missed files in nested subdirs → reconstruction was incomplete. LESSON: `find -type f | sort` recursively. Compare against `## cmd-resource index`. Exhaustive or nothing.
- **L11**: Binary file (SVG icon) — tried to base64-decode what was already binary → corrupted. LESSON: binary stays binary. `cp` verbatim.
- **L12**: Couldn't reach upstream (network down) but reported reconstruction as lossless anyway → later found 3 files differed. LESSON: sub-case B (no upstream) is NOT a guarantee of losslessness — it's a normalized reconstruction. Callout the limitation. Treat as advisory.
- **L13**: Assumed COPY without asking → user expected MOVE (cmd + cmd-resource deleted), source cmd leaked into both scopes. LESSON: ALWAYS ask MOVE vs COPY. Default suggestion is COPY but MUST get explicit confirm.
- **L14**: Reconstructed a script that already existed (identical content) in another skill at the same `<output-dir>/` → bloat, two copies drifted apart later. LESSON: scan destination scope for duplicates DURING the walk, callout immediately. Post-op scan is the safety net but the during-op callout prevents the write in the first place.

## Security (reconstruction safety)

Reconstruction involves fetching gist content and (optionally) cloning upstream. Apply the same 3rd-party vetting as `skill-to-cmd`:

- **Gist fetch** — verify sha matches the pinned one recorded in the shim. If mismatch → STOP (potential gist drift or tampering).
- **Upstream clone** — only fetch from the URL recorded in `origin`. Do NOT follow redirects to other hosts. Use `--filter=blob:none` to limit blast radius.
- **Reconstructed skill** — once written, run the same security scan as `skill-to-cmd` step 2 (`rg` for prompt injection / backdoors / harmful patterns). Surface findings even if they match upstream (upstream may have been hijacked since the cmd was built).

ALWAYS callout the security re-vet result in the final report.

## Other

- **Symmetry with skill-to-cmd** — this cmd is the inverse. If `skill-to-cmd` then `cmd-to-skill` produces a skill that diffs from the original, ONE of them has a bug. Always cross-check.
- **Round-trip property** — for a true round-trip guarantee, `cmd-to-skill(skill-to-cmd(skill))` should produce a skill that `diff -r` matches the original. If `origin` + `origin_ref` are present, this is enforceable. If not, normalize + callout.
- **Partial cmd** — if the cmd `.md` is missing `<SKILL.md>` wrapper or `## cmd-resource index`, STOP. The cmd is malformed. Do NOT guess.
- **Multiple cmds → one skill** — out of scope. One cmd = one skill. If user wants to merge cmds into one skill, that is a separate consolidation task.
- **Agent portability** — the reconstructed skill (SKILL.md + references/ + scripts/) works across any agent that loads skills from a dir (claude, opencode, codex, etc.). No agent-specific syntax.
- **Re-construction workflow** — when the cmd is updated (cmd-resource files change, gist pins bumped), re-run this cmd, diff old reconstruction vs new, surface changes, MANUALLY apply approved changes (never auto-overwrite user's local edits to the reconstructed skill).
- **cmd-only content** — `## cmd-resource index`, `## User addition request`, `$ARUGMENTS`, `origin`/`origin_ref` are documented as dropped in step 2D + step 9 callsouts. They are NOT skill content and must NOT appear in the reconstructed skill.

## Final step — caveman + compress (lossless)

AFTER the reconstructed skill is written to disk (and the lossless verify in step 8 passes):

1. INVOKE the caveman skill — READ `~/.agents/skills/caveman/SKILL.md` first. Apply **caveman full mode** to the reconstructed SKILL.md BODY (NOT its frontmatter).
2. THEN compress — READ `~/.agents/skills/compress/SKILL.md`. Overwrite SKILL.md with compressed content. Save backup as `SKILL.md.original.md`.
3. VERIFY lossless (MANDATORY — zero tolerance):
   - All technical substance preserved: every step, code block, URL, table, file path, gist sha, `_manifest.json` reverse mapping.
   - SKILL.md frontmatter UNCHANGED byte-for-byte (ONLY `name` + `description` allowed).
   - references/ + scripts/ files intact (binary files like SVG icons NEVER compressed — `cp` verbatim).
   - No step dropped. No reference/URL dropped. No lesson-learn dropped.
   - Only fluff / filler / articles / hedging removed.
4. If compression would drop ANY technical info → STOP. Report exactly what would be lost. Do NOT compress that part.
5. Re-run lossless verify (step 8 `diff -r` upstream vs reconstructed) AFTER compress to confirm round-trip still holds.

DO NOT compress SKILL.md frontmatter. DO NOT compress binary assets. DO NOT compress inside code blocks. DO NOT drop steps. DO NOT drop URLs. DO NOT drop lesson-learn entries.
This step is MANDATORY after every skill reconstruction.
