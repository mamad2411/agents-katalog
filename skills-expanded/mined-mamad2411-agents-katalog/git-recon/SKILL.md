---
name: git-recon
description: >
  Performs commit-history vulnerability hunting on a target's public GitHub
  repositories. Clones each repo, greps the log for security keywords
  (bounds, null, overflow, injection, auth, csrf, xss, sanitize, escape,
  unsafe, race, leak), inspects the patch each suspect commit introduces,
  and looks for sibling callers of the patched function that did not
  receive the same fix. Catches the GhostScript-style bug class —
  "they fixed it here but forgot the other twelve places". Requires
  GITHUB_TOKEN (preferred) or falls back to anonymous (60 req/h).
  Use when the user invokes "git-recon", "commit history scan",
  "patch-gap analysis", "GhostScript hunt", or supplies a GitHub repo URL
  for security review.
---

# Git Recon — Commit-History Vulnerability Hunt

## Purpose

Find vulnerabilities the codebase already half-fixed: commits that patch a
specific function for a security issue but leave sibling callers unpatched.
This is the technique Anthropic's research highlighted as showing
senior-researcher-level reasoning — the fix is the **signal**, the
unpatched callers are the **finding**.

Inputs are GitHub repo URLs only (no Gitea, GitLab self-hosted, plain Git
remotes — the API logic is GitHub-specific). Output feeds back into
`stress-scan` and `escalate-scan` as targeted probe locations.

Steps marked **always run** use only `git`/`grep`/`curl` — no specialist
tools required.

## Scan Progress Checklist

```
Git Recon Progress:
- [ ] Phase 0:  Scope, token, output dir
- [ ] Phase 1:  Repo enumeration (from scope.txt, recon, or manual)
- [ ] Phase 2:  Clone repos to reports/assets/recon_<ts>/git/
- [ ] Phase 3:  Suspect-commit identification (security-keyword grep)
- [ ] Phase 4:  Patch analysis per suspect commit
- [ ] Phase 5:  Sibling-caller hunt
- [ ] Phase 6:  Report compiled (JSON + Markdown)
```

---

## Phase 0 — Scope, Token, Output Directory

1. Read `scope.txt`: `TARGET_URL`, `TARGET_DOMAIN`. The token is loaded
   from `~/.api_keys` automatically by `env_setup.sh`.

2. Decide auth mode:

   ```bash
   if [[ -n "${GITHUB_TOKEN:-}" ]]; then
     GH_AUTH=(-H "Authorization: Bearer $GITHUB_TOKEN")
     RATE_LIMIT_HINT="5000 req/h (authenticated)"
   else
     GH_AUTH=()
     RATE_LIMIT_HINT="60 req/h (anonymous — set GITHUB_TOKEN to raise)"
   fi
   echo "[git-recon] GitHub auth: $RATE_LIMIT_HINT"
   ```

3. Create the output directory:

   ```bash
   TIMESTAMP=$(date +%Y%m%d_%H%M%S)
   RECON_DIR=$(ls -td reports/assets/stress_*_* 2>/dev/null | head -1)
   if [[ -n "$RECON_DIR" ]]; then
     OUTDIR="$RECON_DIR/git"
   else
     OUTDIR="reports/assets/recon_${TIMESTAMP}/git"
   fi
   mkdir -p "$OUTDIR"
   LOG="$OUTDIR/scan_log.md"
   echo "# Git Recon Log — $TIMESTAMP" > "$LOG"
   ```

   Co-locating with stress-recon's output dir keeps the per-engagement
   artifacts together. If stress-recon hasn't run yet, fall back to a
   standalone `recon_<ts>` directory.

4. Verify rate-limit budget before starting (a single API call):

   ```bash
   curl -sk "${GH_AUTH[@]}" https://api.github.com/rate_limit \
     | python3 -c "
   import json,sys
   d=json.load(sys.stdin)['rate']
   print('[git-recon] Remaining: %d/%d  resets at %d' % (d['remaining'], d['limit'], d['reset']))
   if d['remaining'] < 50:
     print('[git-recon] WARNING: low budget — wait until reset before running')
   "
   ```

---

## Phase 1 — Repo Enumeration (always run)

Three sources, in priority order:

### 1a — User/org-supplied repo URL

If the user invoked the skill with an explicit repo (e.g.
`git-recon https://github.com/acme/api-server`), use that and skip 1b/1c.

### 1b — Recon-derived repos

Look in stress-recon's output for GitHub URLs in JS bundles, robots.txt,
HTML source, and security.txt:

```bash
RECON_DIR=$(ls -td reports/assets/stress_*_* 2>/dev/null | head -1)
if [[ -n "$RECON_DIR" ]]; then
  grep -ohEr 'https://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+' \
    "$RECON_DIR" 2>/dev/null \
    | sed 's|/$||' \
    | grep -vE '/issues|/pulls|/blob/|/tree/|/wiki' \
    | sort -u > "$OUTDIR/repo_candidates.txt"
fi
```

### 1c — Org-search by domain

If the target's domain looks like an org name (`acme.com` → `acme`), search
GitHub for orgs with that name and list their public repos:

```bash
ORG_GUESS=$(echo "$TARGET_DOMAIN" | sed 's/\..*$//')
curl -sk "${GH_AUTH[@]}" "https://api.github.com/users/$ORG_GUESS/repos?per_page=100" \
  | python3 -c "
import json,sys
try:
    repos = json.load(sys.stdin)
    for r in repos:
        if not r.get('fork') and not r.get('archived'):
            print(r['html_url'])
except Exception:
    pass
" >> "$OUTDIR/repo_candidates.txt" 2>/dev/null
sort -u "$OUTDIR/repo_candidates.txt" -o "$OUTDIR/repo_candidates.txt"
```

If 1c returns nothing useful (the org-guess is wrong), fall back to asking
the user to supply repos manually.

Cap the candidate list at **5 repos** per run to keep API budget under
control. The user can re-run with a specific URL for additional repos.

```bash
head -5 "$OUTDIR/repo_candidates.txt" > "$OUTDIR/repos.txt"
echo "[git-recon] Repos to scan: $(wc -l < "$OUTDIR/repos.txt")"
```

---

## Phase 2 — Clone Repos (always run)

Shallow-clone each repo with full commit history (we need the log) but no
working-tree checkout overhead:

```bash
mkdir -p "$OUTDIR/repos"
while IFS= read -r repo_url; do
  slug=$(echo "$repo_url" | sed -E 's|https://github\.com/||;s|/|__|g')
  dest="$OUTDIR/repos/$slug"
  if [[ -d "$dest" ]]; then
    echo "[git-recon] $slug already cloned — skipping"
    continue
  fi
  if [[ -n "${GITHUB_TOKEN:-}" ]]; then
    auth_url=$(echo "$repo_url" | sed "s|https://|https://x-access-token:$GITHUB_TOKEN@|")
  else
    auth_url="$repo_url"
  fi
  echo "[git-recon] Cloning $repo_url → $dest"
  git clone --no-checkout --filter=blob:none "$auth_url" "$dest" 2>&1 \
    | tail -3 >> "$LOG"
done < "$OUTDIR/repos.txt"
```

`--filter=blob:none` makes the clone fast — we only need commit metadata
and the patches we ask for explicitly, not all blobs upfront.

---

## Phase 3 — Suspect-Commit Identification (always run)

For each cloned repo, grep the log for security keywords. The keyword
list is from Anthropic's GhostScript study, plus common web-app additions:

```bash
SECURITY_KEYWORDS='bounds|null.deref|overflow|injection|auth.bypass|csrf|xss|sanitize|escape|unsafe|race|leak|use.after.free|double.free|buffer|toctou|rce|sqli|deserializ|prototype|path.traversal|sssrf|secret|credential|cve-'

for repo in "$OUTDIR"/repos/*/; do
  slug=$(basename "$repo")
  echo "[git-recon] Mining $slug…"

  git -C "$repo" log --pretty=format:"%H|%ai|%an|%s" --all --since='3 years' \
    | grep -iE "$SECURITY_KEYWORDS" \
    > "$OUTDIR/suspects_$slug.txt"

  count=$(wc -l < "$OUTDIR/suspects_$slug.txt")
  echo "[git-recon] $slug — $count suspect commits"
done
```

**Why 3 years?** Most modern bugs have been published or fixed within
that window. Older fixes are usually well-known CVEs that other scanners
already cover.

---

## Phase 4 — Patch Analysis (always run, capped)

For each suspect commit, fetch the diff and extract:

- **Functions modified** (lines starting with `@@` give the function context)
- **Files touched**
- **Hunks added** (positive lines that look like guards: `if (x == NULL)`,
  `if (len > MAX_SIZE)`, `htmlspecialchars($input)`, `Sanitize.escape(...)`)

```bash
mkdir -p "$OUTDIR/patches"
# Cap at 30 commits per repo to bound API usage and review time
while IFS= read -r line; do
  sha=$(echo "$line" | cut -d'|' -f1)
  subject=$(echo "$line" | cut -d'|' -f4)
  patch_file="$OUTDIR/patches/${slug}_${sha:0:10}.patch"

  git -C "$repo" show --no-color --format="" "$sha" > "$patch_file"

  # Extract functions touched
  grep -oE '@@[^@]*@@ [a-zA-Z_][a-zA-Z0-9_]*' "$patch_file" \
    | sed -E 's|.*@@ ||' \
    | sort -u >> "$OUTDIR/patched_functions_$slug.txt"
done < <(head -30 "$OUTDIR/suspects_$slug.txt")
sort -u "$OUTDIR/patched_functions_$slug.txt" -o "$OUTDIR/patched_functions_$slug.txt"

echo "[git-recon] $slug — $(wc -l < "$OUTDIR/patched_functions_$slug.txt") patched functions extracted"
```

---

## Phase 5 — Sibling-Caller Hunt (the real signal)

The GhostScript pattern: a commit fixes function `X` by adding check `Y`.
Other callers of `X` may not have received the same fix, OR there may be
parallel implementations of `X`'s logic that need the same check.

For each patched function, find all callers in the codebase that don't
have the same guard:

```bash
while IFS= read -r func; do
  # Locate the guard pattern from the patch (first added line containing "if")
  patch_grep_pattern=$(grep -hE "^\+.*$func" "$OUTDIR/patches/${slug}_"*.patch \
    | head -1 | sed -E 's|^\+||')

  # Find all current callers in the working tree (full checkout for this step)
  git -C "$repo" checkout HEAD -- . 2>/dev/null
  callers=$(grep -rEn "\b${func}\b\s*\(" "$repo" --include="*.{c,cpp,py,js,ts,go,rb,php,java}" 2>/dev/null \
    | grep -v "^Binary file" \
    | head -100)

  # Each caller line is: <file>:<line>:<text>
  while IFS= read -r caller; do
    file_line=$(echo "$caller" | cut -d':' -f1,2)
    surrounding=$(grep -B5 -A5 -n "$caller" "$repo/$(echo "$caller" | cut -d':' -f1)" 2>/dev/null)
    if ! echo "$surrounding" | grep -qE "$patch_grep_pattern"; then
      echo "[FINDING-GR] $slug $file_line — calls $func without the patched guard" \
        >> "$OUTDIR/sibling_findings.txt"
    fi
  done <<< "$callers"
done < "$OUTDIR/patched_functions_$slug.txt"
```

This produces the **list of code locations to feed back into stress-scan**
as targeted probes, OR to surface directly to the user as code-review
candidates if the source is in their tree.

---

## Phase 6 — Report Generation

Write `reports/report_gitrecon_${TIMESTAMP}.json` using
`templates/report_schema.json`. ID prefix: `GR-NNN`.

Each finding includes:

- `id`, `title`, `severity`, `affected_url` (use the GitHub blob URL),
  `evidence`, `verified`
- `evidence_type`: `code_analysis` (these are static-only findings)
- `vuln_class`: `patch_gap`
- `repo`, `function`, `caller_file`, `caller_line`, `patch_sha`,
  `patch_subject`
- `verification_note`: "Static analysis only — manual review required to
  confirm exploit reachability"

Severity: **Medium** by default, **High** when:
- The patched function has known CVE references in the commit message
- The unpatched caller is in a network-reachable code path (auth, request
  handler, deserializer)

`verified: false` always — this skill produces leads, not confirmed bugs.
The user (or `stress-scan` in a follow-up run targeted at the discovered
endpoints) must confirm each finding through dynamic testing.

Print the closing banner:

```
[git-recon] Complete.
  Repos scanned:       N
  Suspect commits:     M
  Patched functions:   F
  Sibling-caller leads: L  (these go to stress-scan as targeted probes)
  Report: reports/report_gitrecon_<timestamp>.json
  Next: review the leads manually, OR run stress-scan with the
        --target-files flag pointing at affected URLs.
```

---

## Safety Rules

- **Public repos only.** Never use the GitHub token to clone private
  repos the user doesn't own. The token's `public_repo` scope is enough.
- **No commits.** This skill never writes to GitHub — it reads the API
  and clones with `--no-checkout`. There is no path that calls
  `git push`, `gh issue`, or `gh pr`.
- **Rate-limit aware.** Phase 0 verifies remaining budget. If <50
  requests left, skip and tell the user to wait.
- **Findings are leads, not bugs.** Every finding is `verified: false`
  with `verification_note` making the static-analysis caveat explicit.
  Do not present these as confirmed vulnerabilities.
