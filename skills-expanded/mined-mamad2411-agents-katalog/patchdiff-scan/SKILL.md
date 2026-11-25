---
name: patchdiff-scan
description: >
  Identifies the exact library versions used by the target (from stress-recon
  tech fingerprint output), fetches the immediately-prior CVE patches and
  release-notes for those versions, diffs each patch to extract the patched
  function and the security guard that was added, then looks for OTHER
  callers of the same function — in the target's own code OR in the
  dependency tree — that did NOT receive the same fix. This is the
  "they fixed it in dependency X, but their fork/wrapper/parallel impl
  still calls the old version" pattern. Requires stress-recon tech-stack
  output. Produces a JSON lead list compatible with stress-scan and
  escalate-scan.
  Use when the user invokes "patchdiff-scan", "patch gap", "CVE patch
  diff", "missed-patch hunt", "dependency vulnerability hunt", or
  supplies a library version to audit.
---

# Patchdiff Scan — CVE-Patch Sibling-Caller Hunt

## Purpose

Catch the "they fixed the library, but their wrapper / fork / parallel
implementation didn't get the same fix" class. The signal is the
upstream patch; the finding is the unpatched caller in the target's
ecosystem.

This skill complements `git-recon`:
- `git-recon` mines **public commit history** for security keywords
- `patchdiff-scan` walks from a **specific library version** to its
  **published CVE patches** and looks for unpatched siblings

Together they cover both "we fixed it ourselves" and "upstream fixed it,
we forgot to update".

Steps marked **always run** use only `curl`/`grep`/`python3`/`git`.

Before starting, read **[references/source_strategy.md](references/source_strategy.md)**
for how the skill picks which version to audit and where to look for
sibling callers.

## Scan Progress Checklist

```
Patchdiff Progress:
- [ ] Phase 0:  Scope + GitHub token + output dir
- [ ] Phase 1:  Tech-stack version extraction (from stress-recon)
- [ ] Phase 2:  Per-library: prior-version CVE / changelog discovery
- [ ] Phase 3:  Patch fetch + function/guard extraction
- [ ] Phase 4:  Sibling-caller hunt (target tree, OR public deps)
- [ ] Phase 5:  Lead deduplication + ranking
- [ ] Phase 6:  Report compiled (JSON + Markdown)
```

---

## Phase 0 — Scope & Setup

1. Read `scope.txt`: `TARGET_URL`, `TARGET_DOMAIN`. The `GITHUB_TOKEN`
   is auto-loaded from `.api_keys` via `env_setup.sh` (see git-recon's
   plumbing — same token, same fallback).

2. Decide auth mode:

   ```bash
   if [[ -n "${GITHUB_TOKEN:-}" ]]; then
     GH_AUTH=(-H "Authorization: Bearer $GITHUB_TOKEN")
     RATE_LIMIT_HINT="5000 req/h (authenticated)"
   else
     GH_AUTH=()
     RATE_LIMIT_HINT="60 req/h (anonymous)"
   fi
   echo "[patchdiff-scan] GitHub auth: $RATE_LIMIT_HINT"
   ```

3. Create output dir, co-located with stress-recon if available:

   ```bash
   TIMESTAMP=$(date +%Y%m%d_%H%M%S)
   RECON_DIR=$(ls -td reports/assets/stress_*_* 2>/dev/null | head -1)
   if [[ -n "$RECON_DIR" ]]; then
     OUTDIR="$RECON_DIR/patchdiff"
   else
     OUTDIR="reports/assets/patchdiff_${TIMESTAMP}"
   fi
   mkdir -p "$OUTDIR"
   LOG="$OUTDIR/scan_log.md"
   echo "# Patchdiff Scan Log — $TIMESTAMP" > "$LOG"
   ```

---

## Phase 1 — Tech-Stack Version Extraction (always run)

Pull `tech_stack.txt` (and the JS-library array from front-end-scan, if
present) and parse out **exact** versions. Anything we can't pin to a
specific version is dropped — we need the version to look up the next
patch.

### 1a — From stress-recon

```bash
# Format expected: lines like "nginx/1.24.0", "Spring Boot 3.1.4",
# "Express 4.18.2", "Rails 7.1.3", "Django 4.2.7"
TECH_FILE=""
[[ -f "$RECON_DIR/recon/tech_stack.txt" ]] && TECH_FILE="$RECON_DIR/recon/tech_stack.txt"

if [[ -z "$TECH_FILE" ]]; then
  echo "[patchdiff-scan] No tech_stack.txt — running stress-recon Phase 2 first is recommended"
  exit 0
fi

# Normalise to "name|version" pairs
python3 - "$TECH_FILE" > "$OUTDIR/libraries.tsv" <<'PYEOF'
import re, sys
pat = re.compile(r'([A-Za-z][A-Za-z0-9_+.\-]+)[/\s\-]+(\d+(?:\.\d+){1,3})')
seen = set()
for line in open(sys.argv[1]):
    for name, ver in pat.findall(line):
        key = (name.lower().strip('-_'), ver)
        if key in seen: continue
        seen.add(key)
        print(f'{name}\t{ver}')
PYEOF

echo "[patchdiff-scan] Libraries with pinned versions: $(wc -l < "$OUTDIR/libraries.tsv")"
```

### 1b — Cap at top-N

Audit the top 10 libraries by relevance (web framework, HTTP server, JS
runtime, common middleware libs first). Anything beyond that has
diminishing return relative to API budget:

```bash
head -10 "$OUTDIR/libraries.tsv" > "$OUTDIR/audit_targets.tsv"
echo "[patchdiff-scan] Audit targets: $(wc -l < "$OUTDIR/audit_targets.tsv")"
```

---

## Phase 2 — Prior-Version CVE / Changelog Discovery (always run)

For each `(name, version)` pair, find the **next 3 patch releases** AND
any CVEs published against the current version. Two data sources:

### 2a — GitHub Security Advisories (preferred, structured)

```bash
while IFS=$'\t' read -r name ver; do
  q=$(printf '"%s" version:"%s"' "$name" "$ver" | python3 -c "import urllib.parse,sys; print(urllib.parse.quote(sys.stdin.read()))")
  curl -sk "${GH_AUTH[@]}" "https://api.github.com/search/issues?q=$q+repo:advisories" \
    > "$OUTDIR/advisories_${name}_${ver}.json"
done < "$OUTDIR/audit_targets.tsv"
```

GitHub's advisory database covers ~90% of npm, pip, RubyGems, and Maven
CVEs from the last 5 years. The response includes `references` linking
to the upstream patch commits — those are the diffs we actually need.

### 2b — Repo release-notes (fallback for projects not in GHSA)

```bash
# Resolve name → repo URL via best-effort heuristic
# (e.g., "Spring Boot" → spring-projects/spring-boot,
#        "Express"     → expressjs/express,
#        "nginx"       → nginx/nginx)
while IFS=$'\t' read -r name ver; do
  repo=$(python3 -c "
KNOWN = {
  'spring-boot': 'spring-projects/spring-boot',
  'express':     'expressjs/express',
  'rails':       'rails/rails',
  'django':      'django/django',
  'nginx':       'nginx/nginx',
  'flask':       'pallets/flask',
  'fastapi':     'tiangolo/fastapi',
  'next':        'vercel/next.js',
  'nextjs':      'vercel/next.js',
  'react':       'facebook/react',
  'vue':         'vuejs/core',
  'angular':     'angular/angular',
  'lodash':      'lodash/lodash',
  'jquery':      'jquery/jquery',
}
import sys
print(KNOWN.get(sys.argv[1].lower().replace(' ', '-').replace('.js',''), ''))
" "$name")

  [[ -z "$repo" ]] && continue

  # Fetch the next 5 release tags after $ver
  curl -sk "${GH_AUTH[@]}" "https://api.github.com/repos/$repo/tags?per_page=100" \
    > "$OUTDIR/tags_${name}.json"
done < "$OUTDIR/audit_targets.tsv"
```

Parse the tag list and identify the **next patch**, **next minor**, and
**next major** above the current version. The patch upgrade is highest
signal — it's almost always a security fix.

---

## Phase 3 — Patch Fetch + Guard Extraction (always run, capped)

For each candidate patch (ranked Phase 2 outputs), fetch the diff and
extract the function and the guard:

```bash
mkdir -p "$OUTDIR/patches"

# Cap at 3 patches per library to bound API usage
# Patch ranking: explicit-CVE first, then security-keyword-tagged release notes,
# then ordinary patch releases.
while IFS= read -r commit_url; do
  sha=$(echo "$commit_url" | sed -E 's|.*/||')
  patch_file="$OUTDIR/patches/${name}_${sha:0:10}.patch"

  # GitHub-formatted patch
  curl -sk "${GH_AUTH[@]}" -H "Accept: application/vnd.github.v3.patch" \
    "$commit_url" > "$patch_file"

  # Extract patched function names
  grep -oE '@@[^@]*@@ [a-zA-Z_][a-zA-Z0-9_.]*' "$patch_file" \
    | sed -E 's|.*@@ ||' | sort -u >> "$OUTDIR/patched_${name}.txt"

  # Extract added guard lines (heuristic: lines starting with + that
  # contain a check keyword)
  grep -E '^\+.*\b(if|assert|return|raise|throw|guard|check|sanitize|escape|validate)\b' "$patch_file" \
    >> "$OUTDIR/guards_${name}.txt"
done < <(head -3 "$OUTDIR/patch_candidates_$name.txt")
```

The `guards_${name}.txt` file is the **library-specific check pattern**
we need to find missing in the target's caller code.

---

## Phase 4 — Sibling-Caller Hunt

Two scopes for the hunt:

### 4a — Target's own source (if a repo URL was supplied)

If the target's source is on GitHub (passed via `--repo` or discovered by
`git-recon`), clone it and grep for callers of the patched functions
that lack the guard:

```bash
TARGET_REPO="${TARGET_REPO:-}"
if [[ -n "$TARGET_REPO" ]]; then
  git clone --filter=blob:none --no-checkout \
    "$TARGET_REPO" "$OUTDIR/target_src" 2>/dev/null
  git -C "$OUTDIR/target_src" checkout HEAD 2>/dev/null

  while IFS= read -r func; do
    grep -rEn "\b${func}\b\s*\(" "$OUTDIR/target_src" \
      --include="*.{js,ts,py,rb,go,java,php,c,cpp,rs}" 2>/dev/null \
      > "$OUTDIR/callers_${name}_${func}.txt"
  done < "$OUTDIR/patched_${name}.txt"
fi
```

For each caller, check if the surrounding ±5 lines contain a guard that
matches the patch's added guard. Callers without the guard go to the
finding list.

### 4b — Public-dependency tree (always run when 4a unavailable)

Even without the target's source, we can check the **public dependency
graph**: are there NPM packages, Pip packages, RubyGems, or Maven
artifacts that depend on the affected library and may not have updated?

This is best-effort — we surface a **list of suspect packages** rather
than confirmed unpatched code:

```bash
# NPM example: find packages whose manifest pins a vulnerable version range
curl -sk "${GH_AUTH[@]}" \
  "https://api.github.com/search/code?q=%22${name}%22+%22${ver}%22+filename:package.json" \
  > "$OUTDIR/dependents_${name}.json"
```

Note this surfaces *manifest references*, not *call-site references* —
the lead is "this package may pull in a vulnerable transitive dep",
which the user then verifies manually.

---

## Phase 5 — Lead Deduplication + Ranking

Combine 4a and 4b leads. Rank by:

1. **Severity** of the underlying CVE (if a CVE was associated)
2. **Confidence** — 4a (explicit-caller-without-guard) is higher
   confidence than 4b (manifest-level dependency)
3. **Reachability** — callers in handlers / middleware / auth code
   beat callers in test fixtures or build scripts
4. **Patch recency** — fixes from the last 6 months beat fixes from
   2 years ago (less likely the user has already updated)

Write the top 20 leads to `$OUTDIR/leads.txt` with file:line, function,
patch SHA, and CVE reference (if any).

---

## Phase 6 — Report Generation

Write `reports/report_patchdiff_${TIMESTAMP}.json` using
`templates/report_schema.json`. ID prefix: `PD-NNN`.

Each finding includes:

- `id`, `title`, `severity`, `affected_url` (the GitHub blob URL of the
  unpatched caller), `evidence`, `verified` (always `false`)
- `evidence_type`: `code_analysis`
- `vuln_class`: `unpatched_dependency` | `unpatched_caller`
- `library`, `current_version`, `patched_version`
- `patch_sha`, `patch_url`, `cve_id` (when known)
- `caller_file`, `caller_line` (4a) OR `dependent_package` (4b)
- `verification_note`: "Static lead — confirm reachability with stress-scan
  or manual review before reporting as a vulnerability"

Severity:

| Confidence path | CVSS of underlying CVE | Default severity |
|-----------------|------------------------|------------------|
| 4a + reachable handler | ≥ 7 | High             |
| 4a + reachable handler | < 7 | Medium           |
| 4a + non-reachable     | any | Low              |
| 4b (manifest only)     | any | Info             |

`verified: false` for all entries — this skill produces leads, not
confirmed bugs. Confirmation requires either dynamic testing (stress-scan
hitting the affected endpoint) or manual code review.

Print the closing banner:

```
[patchdiff-scan] Complete.
  Libraries audited:    L
  CVE patches analysed: P
  Sibling-caller leads (4a): X
  Manifest-dep leads (4b):   Y
  Report: reports/report_patchdiff_<timestamp>.json
  Next:
    - Manual review of high-confidence leads
    - Or run stress-scan with the affected URLs as targeted probes
```

---

## Safety Rules

- **Read-only.** This skill never writes to GitHub, never opens issues,
  never pushes. Cloning target source uses `--no-checkout` and stays
  local to `$OUTDIR/target_src`.
- **No exploit attempts.** Findings are static-analysis leads only.
  `verified: false` always. Severity caps at High; Critical requires
  dynamic confirmation.
- **API-budget aware.** Phase 0 verifies the rate-limit budget. Phase
  1 caps at 10 libraries; Phase 3 at 3 patches each — total of ~30 API
  calls per run plus tag-fetches.
- **No private repos.** The token's `public_repo` scope is sufficient.
  If the target has private source, the user must supply a clone
  manually; the skill won't authenticate against private repos.
