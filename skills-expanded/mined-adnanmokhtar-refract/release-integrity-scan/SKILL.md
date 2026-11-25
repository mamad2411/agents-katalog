---
name: release-integrity-scan
description: "Releases you cannot trust or undo: movable tags, split versions, rebuilt-after-scan images, verify-anything, pruned N-1."
kind: skill
pack: devops
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: release-integrity-scan

## Premise

A release is a promise about one artifact: this digest is the one that was built from a reviewed commit, tested, scanned and signed, it carries one version everywhere, a re-run cannot change it, and the one before it is still there to roll back to. Each part breaks silently:
- a `v*` tag pushed from an unmerged branch publishes;
- the scan reads a `load: true` image and a second build pushes something else;
- `cosign verify --certificate-identity-regexp '.*'` accepts a signature from any workflow;
- a valid attestation proves only that *some* workflow built it. TanStack's postmortem (2026-05-11) shipped npm packages with valid SLSA provenance from a poisoned build, so a verify that does not pin **which workflow and which ref** proves nothing;
- a cleanup job keeps one version, and `/rollback-deploy` has no N-1.

No tool in the ledger joins these. zizmor and actionlint see no release semantics; trivy scans whatever ref it is handed; `ci-graph.py` does not count a `docker/build-push-action` that pushes through `outputs: …push=true` with no `push:` input as a publish [V 2026-10-10, sample `build.yml:27`].

This skill owns `ownership.json` row `release-integrity` (§1–§7). `release-security` (this pack) is its executor: §5 hands it a digest to scan, verify and compare when a registry is reachable. `@deployment-engineer` (this pack) judges its rows.

**Every finding cites the line `<file:line>` + the release unit (workflow job, script, release tool) + the artifact it produces (registry, package, asset) + the fact it rests on (with its date) + the oracle and its tier + the fix in the project's own syntax.** A grep hit or a `JOB` row is a candidate, and a `ci-graph.py` row is a structural fact; neither is a finding. "Releases look fine" is never printed; the output is the class-coverage block (§ Output). Verification follows [`refute-before-report.md`](../../../../snippets/refute-before-report.md) with [`precedents/devops.md`](../../../../snippets/precedents/devops.md) (release § 17–21; tools and versions § 41–46). The oracles are [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § DevOps, V220–V226; the tool floors are `THR-SCANNER-FLOOR` in `templates/governance/thresholds.json`.

## The rule

A candidate is a finding when all four hold (the seven gates as `precedents/devops.md` § Reading the seven gates applies them to releases):

1. **The unit publishes something that ships** (gates 1, 7). A job or script that pushes an image, a package or a release asset a deploy or a consumer pulls. A per-PR preview image, a scratch tag a test reads, or a docs site is Hardening or Refuted.
2. **The event happens** (gate 2). The release job is re-run; a second producer writes the same tag; someone with write access pushes a tag; the cleanup job runs; a deploy resolves a tag after the scan.
3. **No control already handles it** (gate 4). A tag ruleset or an immutable release, an ancestry check, an existence guard (precedents § 18), a digest hand-off, an exact-identity verify at admission (infrastructure `admission-policy`), a retention rule that keeps N-1.
4. **The oracle fired, or both ends are cited** (gate 6). Without a run, cite both ends — the scan and the second producer; the verify and the identity it accepts; the cleanup and the rollback that needs N-1 — and the row is `[report-flagged]`.

## Boundaries

- **Attacker paths in release CI are security's**, when the security pack is installed: a long-lived `NPM_TOKEN` / `TWINE_PASSWORD` where trusted publishing exists (RL-4), OIDC width, a PR-writable cache read by the release job → `ci-security-scan` §6 and §5; a secret build arg (which `provenance: mode=max` also records) → `iac-scan` grep 2b; **deploy by a mutable tag** and **registry tag mutability as an attack** ("whoever can push the tag replaces prod") → `iac-scan` 4j. §4 and §7 here corroborate 4j with the reproducibility and rollback half; they never re-grade it. Without the pack, those rows print `security-class (owner pack security not installed)` at this skill's severity (precedents § 1).
- **A publish not gated on tests** (RL-3) → `pipeline-integrity-scan` §4; **cache-poisoned release jobs** → security. **Registry immutability and lifecycle as IaC** (ECR `imageTagMutability`, a Terraform lifecycle block) → infrastructure; §7 reads the rule's effect on N-1. `revisionHistoryLimit` → infrastructure.
- **Admission enforcement of signatures** → infrastructure `admission-policy`. §5 reads whether a verify exists and what it accepts; the policy is that skill's.
- **The Dockerfile and the image's contents** (user, PID 1, layers, `--check`) → `container-build-scan`; **image CVEs, SBOM, signing and the verify run** → `release-security` (this skill's executor). **Deploy concurrency, rollout gates** → `deploy-safety-scan`. **App-store releases** (Play, App Store Connect) → the mobile pack.

## Adapt to the codebase — the lanes

Discover every release unit (pre-flight 0a–0d); never assume `.github/`, `release.yml` or `./Dockerfile`. A **release unit** is a GitHub job, a GitLab job or `extends:` base, a Jenkins stage, a CircleCI/Bitbucket/Azure file (read as one unit), a release script, a Makefile target or an npm script. Print the lanes you ran in the header.

| Lane | Release trigger (§1) | Producer (§3, §4) | Verify (§5) | Rollback target (§7) |
|---|---|---|---|---|
| **GitHub Actions** | `push: tags`, `release: published`; tag rulesets + immutable releases (GA 2025-10-28) [R] | job (`ci-graph.py publishes=`, 0c `BUILD`/`PUSH`) | `cosign verify`, `gh attestation verify` in a deploy job | the registry and the cleanup workflows |
| **GitLab CI** | `rules: - if: $CI_COMMIT_TAG`; protected tags (`glab api projects/:id/protected_tags` [K]) | job, `extends:` base | same verbs in `script:` | registry cleanup policy [K] |
| **Jenkins · CircleCI · Bitbucket · Azure** | `buildingTag()` / tag filters (read) | the file | same verbs | registry |
| **Scripts, Makefiles, npm scripts** | who runs it is the control | the file (0d joins `\` lines) | same verbs | what `--to` / `rollback` redeploys |
| **Release tools** | release-please 17.11.2, changesets 3.0.3, semantic-release 25.0.9, goreleaser 2.18.3 [R, versions read 2026-10-10] | the tool's publish | goreleaser `signs:` / `checksum:` | — |

| Registry | Version or tag immutable? | Retention read |
|---|---|---|
| npm, PyPI, crates.io | a published version cannot be republished: a re-run fails red, after earlier steps already ran (RL-5) | unpublish rules are the registry's |
| GHCR | no tag-immutability setting [R]: only the digest is fixed | `actions/delete-package-versions` workflows; the versions list (A) |
| ECR · GAR · Docker Hub | ECR `imageTagMutability: IMMUTABLE` (with exclusion filters) [R]; GAR and Docker Hub immutable tags [K] | ECR lifecycle JSON `countNumber`; GAR cleanup policies [K] |

## Tool lane and ledger

| Lane | Command | Trap that makes a clean result false |
|---|---|---|
| Graph | `python3 "$G" . --deploy-ancestors` (`ci-graph.py`, repo baseline; fallback `$HOME/.claude/templates/repo-baseline/.claude/scripts/ci-graph.py`) | Exit 2 = NOT-RUN, never clean (precedents § 41, § 44). **`publishes=` misses `docker/build-push-action` with `outputs: …push=true` and no `push:` input** [V 2026-10-10]: 0c prints those as `publish=outputs` / `PUSH-VIA-OUTPUTS` |
| Settings | `gh api repos/{o}/{r}/rulesets --jq '.[]\|select(.target=="tag")\|{id,name,enforcement}'`, then `gh api repos/{o}/{r}/rulesets/<id> --jq '{rules:[.rules[].type],bypass:.bypass_actors}'`; `gh api repos/{o}/{r}/releases/latest --jq '{tag_name,immutable}'`. Offline: `rulesets.json` in a snapshot dir → `ci-graph.py --settings-dir=<dir>` prints `RULESET` rows, and `RULESET target=tag name=NONE` when no tag ruleset exists (0b passes `$SETTINGS_DIR`) | 403/404 = `UNREADABLE(gh api …: 403)`, never "absent" (precedents § 6). The tag-rule `type` values and the immutable-release field are [K?] (research unknown 4): settle on the first real read and quote it |
| Registry | `crane digest <ref>`, `crane manifest <repo>@<digest>`, `docker buildx imagetools inspect <ref>` | Registry unreachable or no credential → `blocked (registry)`, with the command written out (precedents § 41). Reads only: this skill never pushes, tags or deletes |
| Release dry runs | `npx --no semantic-release --dry-run --no-ci`, `npx --no changeset status --verbose`, `goreleaser check`, release-please `release-pr --dry-run` [K flags] | A dry run that needs a token it does not have prints an error, not a version: `blocked` |
| Executor | `release-security` (this pack) in audit mode, given the digest, the expected identity and the floors | Its rows come back `NOT-RUN` when a tool is below `THR-SCANNER-FLOOR` or missing; §5 is then `blocked`, never `checked` |
| Floors | `cosign version`, `trivy --version`, `syft version`, the CI pins (5b) | `THR-SCANNER-FLOOR`: cosign ≥ 3.1.3 (GHSA-fx35-mq7g-6g98, a verification bypass via a public key in a legacy bundle, fixed 2026-08-06 [R]); trivy pinned by version **and** digest (the 2026-03-19 compromise moved 76 of 77 `trivy-action` tags [R]); zizmor ≥ 1.28; actionlint ≥ 1.7.12 |

## Pre-flight

Run as **one** script from the repo root (shell state does not survive between tool calls; bash 3.2 and zsh print the same rows). Grep **N** feeds **§N**; 0 is the inventory, the graph, the GitHub step table and the joined-line file. Every `rg` names its path; an rg exit 2 is a failed grep, never zero hits; in every rg call the include globs come first and the exclusion array last, because ripgrep lets the later `-g` win; `--hidden` is required for `.github`, `.gitlab-ci.yml` and `.changeset`. Nothing is written inside the repo, nothing is pushed or pulled: the graph, the step table and the joined lines go to `$SCAN`.

```bash
X=(--hidden -g '!.git/**' -g '!**/node_modules/**' -g '!**/{dist,build,out,target,vendor,.venv,venv,__pycache__,coverage,.next,.turbo,generated}/**'
   -g '!**/{test,tests,__tests__,spec,e2e,fixtures,__fixtures__,mocks,__mocks__,testdata,examples}/**' -g '!**/*.{spec,test}.*' -g '!**/{docs,ai,.claude}/**' -g '!*.{md,mdx,snap,lock,svg,map}')
CI=(--hidden -g '.github/workflows/*.{yml,yaml}' -g '**/.gitlab-ci*.yml' -g '.gitlab/**/*.{yml,yaml}' -g '.circleci/*.{yml,yaml}' -g '**/bitbucket-pipelines.yml'
    -g '**/azure-pipelines*.yml' -g '**/Jenkinsfile*' -g '**/action.{yml,yaml}' -g '!**/{node_modules,vendor,test,tests,fixtures,__fixtures__,testdata}/**')
SH=(-g '*.{sh,bash}' -g '**/Makefile' -g '**/Justfile' -g '**/package.json' -g '!**/{node_modules,vendor,test,tests,fixtures,__fixtures__,testdata,docs,.claude,.git}/**')
NC=(rg -v --pcre2 '^[^:]+:\d+:\s*(#|//)')   # drops comment-only hit lines
PUB='\b(npm|pnpm)\s+publish\b|\byarn\s+npm\s+publish\b|\btwine\s+upload\b|\bcargo\s+publish\b|\bgem\s+push\b|\bdocker\s+push\b|\bbuildx\s+build\b[^\n]*\s--push\b|\bgh\s+release\s+(create|upload)\b|\bgoreleaser\s+release\b|\bchangeset\s+publish\b|\bsemantic-release\b|pypa/gh-action-pypi-publish@|softprops/action-gh-release@|goreleaser/goreleaser-action@'
G=.claude/scripts/ci-graph.py; [ -f "$G" ] || G="$HOME/.claude/templates/repo-baseline/.claude/scripts/ci-graph.py"
SCAN="${SCAN:-$(mktemp -d "${TMPDIR:-/tmp}/release-integrity.XXXXXX")}"; echo "SCAN=$SCAN"
echo '# 0a inventory: CI files, release scripts, release tooling and version files'
rg --files "${CI[@]}" "${SH[@]}" . | rg -v 'package\.json$' | sort
rg --files --hidden . -g '{.release-please-manifest.json,release-please-config.json,.releaserc*,release.config.*,.goreleaser.y*ml,Chart.yaml,lerna.json,CHANGELOG.md}' -g '.changeset/{config,pre}.json' -g '!**/node_modules/**' | sort
echo '# 0b graph (GitHub): which jobs deploy or publish; exit 2 = NOT-RUN, never clean'
: > "$SCAN/graph.txt"; if [ -n "$(rg --files --hidden -g '.github/workflows/*.{yml,yaml}' .)" ]; then python3 "$G" . --deploy-ancestors ${SETTINGS_DIR:+--settings-dir="$SETTINGS_DIR"} > "$SCAN/graph.txt"; echo "ci-graph exit=$?"
  rg 'deploys=yes|publishes=yes|RULESET|NOT-RUN|UNREADABLE' "$SCAN/graph.txt"; else echo 'ci-graph: N/A (no GitHub workflow)'; fi
DJ=" $(rg -o --no-filename --pcre2 '^[^:]+:\d+: JOB job=\S+ deploys=yes' "$SCAN/graph.txt" | sed -E 's/:[0-9]+: JOB job=/:/; s/ deploys=yes//' | tr '\n' ' ')"
echo '# 0c GitHub steps: BUILD / SCAN / PUSH / RELEASE-BOT rows, then one JOB row with its flags'
rg --files --hidden -g '.github/workflows/*.{yml,yaml}' . | sort | while IFS= read -r f; do awk -v DJ="$DJ" -f - "$f" <<'AWK'
function ind(s) { match(s, /^[ \t]*/); return RLENGTH }
function val(s) { sub(/^[^:]*:[ \t]*/, "", s); gsub(/[\x27"]/, "", s); return s }
function row(k, n, rest) { printf "%s:%d: %s job=%s %s\n", FILENAME, n, k, job, rest }
function build(n, p, l, via) { row("BUILD", n, "via=" via " publish=" p " load=" l); nb++; if (p != "no") { np++; if (ns) late = 1 } else if (l == "yes") nl++ }
function scan(n, r, via) { row("SCAN", n, "via=" via " ref=" r); ns++; if (r == "tag") stag = 1 }
function step() { if (sl == 0) return
  if (su ~ /^docker\/build-push-action@/) { p = (sp ~ /^true/) ? "yes" : (sp ~ /^\$\{\{/) ? "expr" : "no"; if (p == "no" && so ~ /push=true/) { p = "outputs"; viaout = 1 }
    build(sl, p, (sld ~ /^true/ || so ~ /type=docker/) ? "yes" : "no", "build-push") }
  if (su ~ /^(aquasecurity\/trivy-action|anchore\/scan-action|docker\/scout-action)@/) scan(sl, (sr ~ /@sha256|digest/) ? "digest" : "tag", su)
  if (su ~ /(release-please-action|^changesets\/action|semantic-release-action)@/) row("RELEASE-BOT", sl, "uses=" su " token=" ((stok == "") ? "default(GITHUB_TOKEN)" : (stok ~ /GITHUB_TOKEN|github\.token/) ? "GITHUB_TOKEN" : "other"))
  sl = 0; su = sp = sld = so = sr = stok = "" }
function jobend() { step(); fn = FILENAME; sub(/^\.\//, "", fn); dep = index(DJ, " " fn ":" job " ") > 0
  if (job != "" && (nb || ns)) printf "%s:%d: JOB job=%s builds=%d publishes=%d loads=%d scans=%d digest-ref=%s%s%s%s%s%s\n", FILENAME, jl, job, nb, np, nl, ns, (dg ? "yes" : "no"),
    (late ? " REBUILD-AFTER-SCAN" : ""), (viaout ? " PUSH-VIA-OUTPUTS" : ""), (stag && np ? " SCAN-BY-TAG" : ""), (dep && nb ? " BUILD-IN-DEPLOY" : ""), (np && !dg ? " NO-DIGEST-HANDOFF" : "")
  nb = np = nl = ns = dg = late = viaout = stag = 0; si = -1 }
/^jobs:/ { injobs = 1; next }
injobs && /^  [A-Za-z0-9_-]+:[ \t]*$/ { jobend(); job = $1; sub(/:$/, "", job); jl = FNR; next }
job == "" || /^[ \t]*#/ { next }
/outputs\.digest|@sha256:|imagetools[ \t]+create|crane[ \t]+(copy|digest)/ { dg = 1 }
/^[ \t]*-[ \t]/ { i = ind($0); if (si < 0 || i == si) { si = i; step(); sl = FNR } }
sl && /uses:[ \t]*/ { s = $0; sub(/.*uses:[ \t]*/, "", s); sub(/[ \t].*/, "", s); su = s }
sl && /^[ \t]+push:/ { sp = val($0) }
sl && /^[ \t]+load:/ { sld = val($0) }
sl && /^[ \t]+outputs:/ { so = val($0) }
sl && /^[ \t]+image-ref:/ { sr = val($0) }
sl && /^[ \t]+token:/ { stok = val($0) }
/docker[ \t]+(buildx[ \t]+)?build[ \t]/ { p = ($0 ~ /--push/) ? "yes" : "no"; build(FNR, p, (p == "yes") ? "no" : "yes", "run") }
/(npm|pnpm|yarn)[ \t]+(run[ \t]+)?build\b|go[ \t]+build[ \t]|mvn[ \t]+(package|install)|gradlew?[ \t]+(build|assemble)/ { row("BUILD", FNR, "via=run kind=app"); nb++ }
/docker[ \t]+push[ \t]/ { row("PUSH", FNR, "via=run"); np++; if (ns) late = 1 }
/trivy([:@][^ \t]*)?[ \t].*image|grype([:@][^ \t]*)?[ \t]|docker[ \t]+scout[ \t]+cves/ { t = $0; sub(/.*(trivy|grype)([:@][^ \t]*)?[ \t]|.*scout[ \t]+cves/, "", t); scan(FNR, (t ~ /@sha256|digest|DIGEST/) ? "digest" : "tag", "run") }   # a docker-run scanner's own @sha256 pin is not the scanned ref
END { jobend() }
AWK
done | tee "$SCAN/steps.txt"
echo '# 0d logical lines of every CI file and release script, `\` continuations joined: greps 3-5 read this, so a command split over lines is one hit'
rg --files "${CI[@]}" "${SH[@]}" . | sort | while IFS= read -r f; do awk -v F="$f" '{ l = $0; if (b == "") s = FNR; if (l ~ /\\[ \t]*$/) { sub(/\\[ \t]*$/, "", l); b = b l " "; next } print F ":" s ":" b l; b = "" }' "$f"; done > "$SCAN/lines.txt"
L() { rg -N --no-filename --pcre2 "$@" "$SCAN/lines.txt" | "${NC[@]}"; }
wc -l < "$SCAN/lines.txt" | sed 's/^ */logical lines: /'
echo '# 1a release triggers (tag push, release published, GitLab tag pipelines, Jenkins tag stages); 1b files with no ancestry check'
rg -n --sort path --pcre2 "${CI[@]}" '^\s{4}tags\s*:|^\s{2}release\s*:|^on\s*:[^\n#]*\brelease\b|^\s*types\s*:\s*\[?\s*(published|released)\b|\bif\s*:\s*[\x27"]?\$CI_COMMIT_TAG\b|^\s*-\s*tags\s*$|\bbuildingTag\s*\(|\bwhen\s*\{\s*tag\b' . | "${NC[@]}" | tee "$SCAN/triggers.txt"
cut -d: -f1 "$SCAN/triggers.txt" | sort -u | while IFS= read -r f; do rg -q --pcre2 'merge-base\s+--is-ancestor|branch\s+(-r\s+)?--contains|\bgithub\.event\.base_ref\b|\$CI_COMMIT_REF_PROTECTED\b' "$f" || echo "$f: NO-ANCESTRY-CHECK"; done
echo '# 2 version sources: manifests, chart, release-please manifest, changesets pre mode, ldflags / VERSION build args, changelog head'
rg -n --sort path --pcre2 -g '**/package.json' -g '**/pyproject.toml' -g '**/Cargo.toml' -g '**/Chart.yaml' -g '**/pubspec.yaml' "${X[@]}" '^\s{0,2}"version"\s*:\s*"[^"]+"|^\s*version\s*=\s*"[^"]+"|^(version|appVersion)\s*:\s*\S+' . | rg -v '"0\.0\.0"'
rg -n --sort path --hidden -g '.release-please-manifest.json' -g '.changeset/pre.json' -g '!**/node_modules/**' '"[^"]+"\s*:\s*"[^"]+"' .
L -e '-ldflags[^\n]*-X[^\n]*[Vv]ersion=|--build-arg\s+\w*VERSION\w*='
rg --files . -g 'CHANGELOG.md' -g '!**/node_modules/**' | while IFS= read -r f; do rg -n -m1 --pcre2 '^#{1,3}\s*\[?v?\d+\.\d+\.\d+' "$f" | sed "s|^|$f:|"; done
echo '# 3a publish sites (with 0c BUILD publish!=no: every producer); 3b files that publish with no existence guard; 3c pushes to a version tag'
L "$PUB" | tee "$SCAN/publish.txt"
{ cut -d: -f1 "$SCAN/publish.txt"; rg 'BUILD .*publish=(yes|expr|outputs)|PUSH ' "$SCAN/steps.txt" | cut -d: -f1; } | sort -u | while IFS= read -r f; do
  rg -q --pcre2 '\bnpm\s+view\b[^\n]*version|--skip-existing\b|skip-existing\s*:\s*true|--skip-duplicate\b|\bkeep-existing\b|\bimagetools\s+inspect\b|\bcrane\s+(digest|manifest)\b|\bmanifest\s+inspect\b|\bgh\s+release\s+view\b|\bchangeset\s+publish\b' "$f" || echo "$f: NO-EXISTENCE-GUARD"; done
L '\bdocker\s+push\s+\S+:["\x27]?(\$\{?\{?\s*(env\.)?\w*(VERSION|TAG|ref_name|COMMIT_TAG)\w*|v?\d+\.\d+)|\bbuildx\s+build\b[^\n]*\s-t\s+\S+:["\x27]?\$\{?\w*(VERSION|TAG)\w*[^\n]*--push'
echo '# 4a per-environment build inputs; 4b digest hand-off vs deploy by tag; 4c scans outside GitHub steps (by tag or by digest)'
L -e '--build-arg\s+\w*(ENV|STAGE|PROFILE)\w*=|--build-arg\s+(NEXT_PUBLIC|VITE|REACT_APP|EXPO_PUBLIC)_\w+=|^[^:]+:\d+:\s+(NEXT_PUBLIC|VITE|REACT_APP|EXPO_PUBLIC)_\w+='
rg -n --sort path --pcre2 -g '**/Dockerfile*' -g '**/*.dockerfile' -g '**/Containerfile*' "${X[@]}" '^\s*ARG\s+\w*(ENV|STAGE|PROFILE)\b|^\s*COPY\s+\S*\.env\.(prod|production|staging)\b' .
echo "digest hand-off lines: $(L 'outputs\.digest\b|@sha256:|\bcrane\s+(copy|digest)\b|\bskopeo\s+copy\b|\boras\s+cp\b|\bimagetools\s+create\b' | wc -l | tr -d ' ') · kustomize digest: $(rg -c --pcre2 -g '**/kustomization.{yml,yaml}' "${X[@]}" '^\s+digest\s*:' . | wc -l | tr -d ' ') files · newTag (deploy by tag, security iac-scan 4j): $(rg -n --pcre2 -g '**/kustomization.{yml,yaml}' "${X[@]}" '^\s+newTag\s*:' . | wc -l | tr -d ' ')"
L '\btrivy\b[^\n]*\bimage\b|\bgrype\s|\bdocker\s+scout\s+cves\b' | rg -v '^\./\.github/workflows/' | awk '{ t = $0; sub(/.*(trivy|grype)([:@][^ \t]*)?[ \t]|.*scout[ \t]+cves/, "", t); print $0 ((t ~ /@sha256|[Dd][Ii][Gg][Ee][Ss][Tt]/) ? "  ref=digest" : "  ref=TAG") }'
echo '# 5a verify / sign / attest / attach, classified; 5b scanner and signer floors and pins (THR-SCANNER-FLOOR); 5c SBOM and provenance producers; 5d release assets with no checksum; 5e secret build args (routed)'
L '\bcosign\s+(verify|sign|attest|attach)\b|\bgh\s+attestation\s+verify\b|\bslsa-verifier\b' | awk '{ b = $0; split(b, h, ":"); at = h[1] ":" h[2] ":"
  if (b ~ /cosign[ \t]+verify/) { id = (b ~ /--certificate-identity-regexp/) ? "REGEXP" : (b ~ /--certificate-identity[ =]/) ? "exact" : (b ~ /--key[ =]/) ? "key" : "NONE"
    printf "%s VERIFY tool=cosign identity=%s issuer=%s tlog=%s ref=%s%s\n", at, id, (b ~ /--certificate-oidc-issuer[ =]/ ? "yes" : (id == "key" ? "n/a" : "NO")), (b ~ /insecure-ignore-(tlog|sct)/ ? "IGNORED" : "ok"), (b ~ /@sha256|@\$|[Dd][Ii][Gg][Ee][Ss][Tt]/ ? "digest" : "TAG"), (b ~ /\|\|[ \t]*(true|:)/ ? " MASKED" : "") }
  else if (b ~ /gh[ \t]+attestation[ \t]+verify/) printf "%s VERIFY tool=gh-attestation signer=%s source-ref=%s scope=%s\n", at, (b ~ /--signer-(workflow|repo|digest)|--cert-identity[ =]/ ? "yes" : "NO"), (b ~ /--source-ref/ ? "yes" : "NO"), (b ~ /--repo[ =]|[ \t]-R[ \t]/ ? "repo" : (b ~ /--owner/ ? "OWNER-ONLY" : "?"))
  else if (b ~ /cosign[ \t]+sign[ \t]/) printf "%s SIGN recursive=%s ref=%s\n", at, (b ~ /--recursive/ ? "yes" : "no"), (b ~ /@sha256|@\$|[Dd][Ii][Gg][Ee][Ss][Tt]/ ? "digest" : "TAG")
  else if (b ~ /cosign[ \t]+attest[ \t]/) printf "%s ATTEST type=%s\n", at, (b ~ /--type[ =]slsaprovenance1/ ? "slsaprovenance1" : b ~ /--type[ =]slsaprovenance/ ? "slsaprovenance(v0.2)" : b ~ /--type[ =](cyclonedx|spdx)/ ? "sbom" : "other")
  else if (b ~ /cosign[ \t]+attach/) printf "%s ATTACH (an unsigned blob; deprecated, removed in cosign v4)\n", at
  else print b }'
L 'cosign-release\s*:\s*\S+|\bCOSIGN_VERSION\s*[:=]\s*\S+|sigstore/cosign:v?[\d.]+|\b(aquasec/trivy|anchore/syft|anchore/grype|hadolint/hadolint|rhysd/actionlint)\b[^\s"\x27)]*|aquasecurity/(trivy-action|setup-trivy)@\S+|\bzizmor@\S+' | awk '
  function below(v, f,   a, b, i) { split(v, a, "."); split(f, b, "."); for (i = 1; i <= 3; i++) { if (a[i] + 0 < b[i] + 0) return 1; if (a[i] + 0 > b[i] + 0) return 0 } return 0 }
  function ver(re,   v) { if (!match($0, re)) return ""; v = substr($0, RSTART, RLENGTH); sub(/^[^0-9]*/, "", v); return v }
  { t = ""
    if ($0 ~ /cosign-release|COSIGN_VERSION|sigstore\/cosign:/) { t = "cosign"; f = "3.1.3"; v = ver("(release|VERSION|cosign:)[^0-9]*[0-9]+[.][0-9]+[.][0-9]+") }
    else if ($0 ~ /zizmor@/) { t = "zizmor"; f = "1.28.0"; v = ver("zizmor@v?[0-9]+[.][0-9]+[.][0-9]+") }
    else if ($0 ~ /rhysd\/actionlint/) { t = "actionlint"; f = "1.7.12"; v = ver("actionlint[:/@]v?[0-9]+[.][0-9]+[.][0-9]+") }
    if (t != "") { print $0 "  " t "=" (v == "" ? "?" : v) ((v != "" && below(v, f)) ? "  BELOW-FLOOR(" f ")" : ""); next }
    if ($0 ~ /(aquasec\/trivy|anchore\/(syft|grype)|hadolint\/hadolint):/ && $0 !~ /@sha256:/) { print $0 "  NO-DIGEST-PIN"; next }
    print }'
L '^[^:]+:\d+:\s+sbom\s*:\s*\w+|--sbom[= ]\w+|\bsyft\b|^[^:]+:\d+:\s+provenance\s*:\s*\S+|--provenance[= ]\S+|actions/attest(-build-provenance|-sbom)?@|slsa-github-generator|^[^:]+:\d+:\s+attestations\s*:\s*false'
cut -d: -f1 "$SCAN/publish.txt" | sort -u | while IFS= read -r f; do rg -q --pcre2 '\bgh\s+release\s+(create|upload)\b|softprops/action-gh-release@|\bgoreleaser\b' "$f" && ! rg -q --pcre2 '\bsha256sum\b|\bshasum\b|SHA256SUMS|checksums?\.txt|^\s*checksum\s*:|actions/attest' "$f" && echo "$f: ASSETS-NO-CHECKSUM"; done
rg -n --sort path -U --pcre2 "${CI[@]}" 'build-args\s*:[^\n]*\n(?:[ \t]{8,}[^\n]*\n){0,8}?[ \t]{8,}[^\n]*\$\{\{\s*secrets\.' . | rg ':\s*build-args' | sed 's/$/  SECRET-BUILD-ARG (routed: security iac-scan 2b)/'
echo '# 6 release automation outside GitHub (GitHub rows are RELEASE-BOT in 0c)'
L '\bsemantic-release\b|\brelease-please\b|\bchangeset\s+version\b' | rg -v '^\./\.github/workflows/'
echo '# 7a retention that can delete N-1 (registry lifecycle, package cleanup, Helm history, artifact retention); 7b rollback units: what they redeploy'
rg -n --sort path --pcre2 -g '*.{json,tf,yml,yaml}' "${CI[@]}" "${SH[@]}" "${X[@]}" -g '!**/package.json' '"countNumber"\s*:\s*[1-3]\b|\bcount_number\s*=\s*[1-3]\b|countMoreThan"?\s*:\s*[1-3]\b|\bmin-versions-to-keep\s*:\s*[0-3]\b|\bdelete-only-untagged-versions\s*:\s*true|\bdelete-untagged\b|--history-max[ =][01]\b|\bretention-days\s*:\s*1\b|\bkeep[-_]last\s*[:=]\s*[1-3]\b' . | "${NC[@]}"
L '\brollout\s+undo\b|\bhelm\s+rollback\b|\bargocd\s+app\s+rollback\b|\bset\s+image\b[^\n]*(PREV|[Pp]revious|ROLLBACK)|^[^:]+:\d+:\s*-?-(to|rollback|previous)\)' | rg -v --pcre2 '\b(die|echo|printf|say|warn|fail)\s+["\x27]'
rg --files "${CI[@]}" "${SH[@]}" . | rg -i 'rollback' | sed 's/$/: ROLLBACK-UNIT (read what it redeploys)/'
```

How to read it:
- **0c** is the §4 table for GitHub. `BUILD publish=` is `yes`, `expr` (a `${{ }}` — read when it is true), `outputs` (a push the graph misses) or `no`; `load=yes` is a local image. The `JOB` row's flags are candidates: `REBUILD-AFTER-SCAN` (a build that publishes after a scan in the same job: the scanned image is not the pushed one), `SCAN-BY-TAG` (the scan reads a tag, which can move before deploy), `BUILD-IN-DEPLOY` (a build inside a job `ci-graph.py` marks `deploys=yes`; a job whose only verbs publish — `docker push`, `npm publish` — is `deploys=no publishes=yes deploy-via=publish-verb` and never gets it), `NO-DIGEST-HANDOFF` (the job publishes and nothing in it records a digest), `PUSH-VIA-OUTPUTS`. `RELEASE-BOT token=` is `default(GITHUB_TOKEN)` when the input is absent — the same trap as passing it. A scanner run as a container (`docker run … aquasec/trivy@sha256:… image <ref>`) is a `SCAN` row; its `ref=` reads the scanned reference, never the scanner's own pin.
- **3a plus every 0c `BUILD publish≠no` row is the full producer list.** Two producers that write the same `<repository>:<tag>` (a CI job and a local ship script, two workflows) are the §3/§4 read: which push lands last, and which one was scanned?
- **3b** is per file: one guard anywhere in the file clears it, so read each publish verb against its own guard.
- **5a** rows come from joined lines, so a `cosign verify \` split over four lines is one row with all its flags. `identity=REGEXP` or `NONE`, `issuer=NO`, `tlog=IGNORED`, `ref=TAG`, `MASKED`, `scope=OWNER-ONLY` and `signer=NO` are each a §5 candidate.
- **2** prints every version source; the read groups them by release unit. Declared independent versioning is precedents § 17; a chart's own `version:` versions the chart.

Blind spots, worked around rather than trusted:
- **A publish through an action** other than build-push (`pypa/gh-action-pypi-publish`, `softprops/action-gh-release`, `goreleaser-action`, changesets' `publish:` input) is in 3a; one with no recognisable verb is not. Read every job whose name says release or publish.
- **Verify policies outside CI** (Kyverno `verifyImages`, policy-controller `ClusterImagePolicy`) are not greped here: infrastructure `admission-policy` owns them; §5 asks whether one exists.
- **A version computed at build time** (`git describe`, a tag read in the Dockerfile) leaves no line in grep 2; the release dry run (V221) prints it.

### Measured (2026-10-10)

| Tree | Result |
|---|---|
| Seeded sample (6 GitHub workflows, GitLab, 4 scripts, release-please + changesets + a chart; 30 positives, 15 decoys, 3 routed) | 0.5 s, 0 rg errors; bash 3.2 and zsh print byte-identical output. **30/30 positives surface** in their §: a tag release with no ancestry check (GitHub and GitLab); 4 version-source rows; 5 unguarded publishes including an npm script and a push split over `\` lines (found only after the 0d join); `REBUILD-AFTER-SCAN` + `PUSH-VIA-OUTPUTS` on the `load: true` → scan → `outputs: push=true` job that `ci-graph.py` lists as `publishes=no`; `BUILD-IN-DEPLOY` with `APP_ENV` and `VITE_API_URL` per environment; a script scanning the pushed tag; `identity=REGEXP ref=TAG`, `scope=OWNER-ONLY`, `ATTACH`, cosign 2.4.1 `BELOW-FLOOR`, a trivy image with no digest, an asset with no checksum, `--provenance=false`; 2 release bots on the default token; keep-1 cleanup, ECR `countNumber: 1`, `--history-max 1`, a rollback by tag variable. 3 decoys never appear (a runbook in `docs/`, a fixture workflow, a keep-30 cleanup); the 12 others surface and clear on read, each by one row or precedent (ancestry check, chart version, § 18 ×2, an `npm view` guard, scan-the-pushed-digest + attest, `sign --recursive` by digest, `imagetools create` by digest, exact identity + issuer, `--signer-workflow` + `--source-ref`, `SHA256SUMS`, an App token) |
| `benchmarks/fixtures/*` (16) | 0 rg errors, 0 awk errors. No fixture holds a release workflow, a publish verb, a verify or a retention rule: 11 print only their version inventory (grep 2; vuln-fullstack also its PR-preview `deploys=yes` graph row), 5 print nothing past the headers. A mobile store script (`flutter build appbundle` + `shasum`) is the mobile pack's and prints no row. No FP class to fix |
| Real NestJS + Fastify monorepo (read-only, `git status` clean before and after) | 0.9 s. No release trigger and no version file: §1, §2 `N/A`. 0c: one CI job publishes 3 images by `:<sha>` tag (`publish=expr`, `NO-DIGEST-HANDOFF`); the overlay deploys them by `newTag: <sha>` ×3 (security 4j, counted). 3a found a local ship script's push only through the 0d join (`git archive … \| docker buildx build … \` + `--push` on the next line). That script guards with `imagetools inspect` ("tags are immutable, not rebuilt") and scans the pushed **tag** (4c `ref=TAG`); the CI job has no guard (3b) and pushes the **same** `<repo>:<sha>` tags on the main push the release waits for. Read: two producers of one tag, so the scanned digest can be replaced before the deploy resolves the tag — a §4 candidate, `[report-flagged]` until V223 (`crane digest` before and after that CI run). `--provenance=false`, no signature and no verify anywhere (§5, M). actionlint 1.7.7 below its 1.7.12 floor in CI and in the script, trivy 0.67.2 by tag with no digest (5b). §7: no retention rule; rollback is the deploy script's `--to <sha>`, by tag (N-1 resolves while the registry keeps the tag; the second producer can rewrite it, which corroborates §4) |

## The 3,000-hit path

1. **Intersect** with the producers: keep hits inside a job `ci-graph.py` marks `publishes=yes` or `deploys=yes`, a 0c `BUILD publish≠no` job, a 3a publish site, or a script the release path calls. Dismiss the rest with one read each (a preview image, a test registry) and name them in the coverage block.
2. **Group** by release unit (precedents § 5): one reusable release workflow, one release script, one release tool config, one registry's retention rule.
3. **Rank:** prod-reaching producers first (what a deploy pulls); then published packages; then the rest.
4. **Read the top 30 groups.**
5. **Run the bulk oracle once:** one settings read covers every §1 row of a repository; one release dry run covers §2 for the tool; one `crane digest` per image across build → scan → push → deploy settles every §4 row on it; one `release-security` audit run per image settles §5.
6. **Ledger the rest** as `Live, unreviewed (k groups / n hits — <continuing command>)`. Never mark it `checked`.

## Scans for

Severity follows what the artifact reaches: a prod deploy or a public package first, never the job's name.

| § | Classes | Default severity |
|---|---|---|
| 1 | RL-1 release ref movable: tag-push or release-published publishing with no tag ruleset, no immutable release, no ancestry check | H |
| 2 | RL-2 version source split; changelog behind the release | M |
| 3 | RL-5 non-idempotent release: no existence guard; a re-pushed version tag; two producers of one tag | M (H when the overwritten tag is what deploys) |
| 4 | RL-6 / EP-3 what ships is not what was tested: rebuild after scan, rebuild in deploy, per-environment build inputs, scan by tag, no digest hand-off | H (C on a prod deploy) |
| 5 | RL-7 / CT-R04–R07 provenance and verification: verify that pins no workflow and ref, below-floor tools, attached-not-attested SBOM, no provenance, no checksums, unsigned platforms of an index | H (M with no consumer verify at all) |
| 6 | RL-8 release automation: the release PR opened with `GITHUB_TOKEN` runs no checks | M |
| 7 | DP-9 rollback target retention: N-1 pruned, or reachable only by a tag that can move | H |

### 1. Release ref movable (RL-1)

```
BAD:   on: push: tags: ['v*']   → npm publish / docker push        (anyone with write pushes v9.9.9 from any branch)
       GitLab rules: - if: $CI_COMMIT_TAG   with no protected tag     (a developer tag publishes)
GOOD:  a tag ruleset (creation by the release bot only, no update, no deletion) + immutable releases
       + `git merge-base --is-ancestor "$GITHUB_SHA" origin/main` before publishing
```
**Read the code:** Which 1a triggers publish (3a, 0c)? Does the workflow check that the tagged commit is on the default branch (1b)? Settings read (§ Tool lane): is there a tag ruleset, and who can bypass it? Is the latest release `immutable: true`? Are tags created only by a bot (changesets, release-please), with the ruleset bypass naming that app?

**Finding when** a person with write access can publish from any commit, or move a published tag. A 403 leaves it `UNREADABLE` → Unconfirmed, never cleared. **Proof (V220):** the settings read shows a tag rule and `immutable: true` (A); in a sandbox, a tag pushed from a non-default branch is refused by the workflow (R).

### 2. Version source split; changelog (RL-2)

```
BAD:   apps/api/package.json 2.3.0  ·  .release-please-manifest.json 2.3.1 with linked-versions  ·  Chart.yaml appVersion 2.2.0
       .changeset/pre.json  "mode": "pre"  left on after the beta    ·  CHANGELOG.md head 2.2.0 while 2.3.1 ships
GOOD:  one source (the tool's manifest) writes every other: package.json, appVersion, the image's version label, -ldflags -X
```
**Read the code:** Group grep 2 by release unit. Is independent versioning declared (no `linked-versions`/`fixed`, per-package manifest; precedents § 17)? Does the image tag or `-ldflags` read the same source? Is pre mode intended (a beta branch) or left over? Is the changelog generated (release-please, changesets) or hand-kept?

**Finding when** two artifacts of one release carry different versions, or the changelog names a version the release is not. **Proof (V221):** the tool's dry run (`semantic-release --dry-run --no-ci`, `changeset status --verbose`, `goreleaser check`) prints one version across every output (T).

### 3. Non-idempotent release (RL-5)

```
BAD:   - run: npm publish                     (re-run after a half-failure: E403, but the tag and the image already went)
       docker push ghcr.io/acme/api:${VERSION} (a re-run pushes a new digest under the same version)
       CI images job pushes <repo>:<sha>  AND  a ship script pushes the same <repo>:<sha>   (two producers, last one wins)
GOOD:  npm view "$PKG@$V" version || npm publish · twine upload --skip-existing · goreleaser keep-existing
       docker buildx imagetools inspect "$REF" && skip   — in every producer of that tag, or one producer only
```
**Read the code:** For each 3b file and each 3c line: what happens on the second run of the same commit — red (npm, PyPI refuse a version), silent overwrite (a registry tag), or a no-op? Which earlier steps already ran (a git tag, a GitHub release, a `:latest`)? Do two producers write one tag (3a + 0c)? `changeset publish` skips published versions by design (precedents § 18).

**Finding when** a re-run double-publishes, half-publishes, or replaces a version's digest. **Proof (V222):** a second run against a sandbox registry (Verdaccio, `registry:2` on localhost, TestPyPI) is a no-op with the same digests (R). Never the user's registry.

### 4. What ships is not what was tested (RL-6, EP-3)

```
BAD:   build (load: true) → trivy image-ref: api:scan → build-push-action outputs: …push=true   (scanned ≠ pushed; load: true carries no attestations)
       deploy-prod: docker build -t api:prod --build-arg APP_ENV=production                        (a third build, never tested)
       --build-arg VITE_API_URL=… per environment in a server image                                (two images from one commit)
       ship.sh: push <repo>:<sha>, then trivy <repo>:<sha> by tag, while CI re-pushes the same tag  (the scan read a tag that moved)
GOOD:  build once with push: true (or push-by-digest) → record steps.build.outputs.digest → scan, sign and attest THAT digest
       → promote by digest (kustomize images[].digest, crane copy <src>@<d>, imagetools create … @<d>)
```
**Read the code:**
- The 0c `JOB` flags: is the second build a different image (another context), or a rebuild of the scanned one? Does a `load: true` scan precede a separate push? (Pushing the scanned local ref with `docker push` keeps its content; a second build does not.)
- `BUILD-IN-DEPLOY`: does the deploy job push and deploy this rebuild, or build a throwaway for a smoke test?
- Per-env inputs (4a): a static SPA built per environment by declared, deterministic design is precedents § 20; a server image is not.
- Digest hand-off (4b): does the deploy reference `@sha256:` or a tag? A tag deploy is security 4j; this § records whether the tested digest is the one that tag resolves to.
- Scans by tag (0c `SCAN-BY-TAG`, 4c): can anything write that tag between the scan and the deploy (§3's second producer, a re-run)?

**Finding when** the digest a deploy or consumer pulls is not the digest that was tested and scanned. **Proof (V223):** `crane digest` of the build output equals the scanned digest (the scanner's `.Metadata.RepoDigests` / `.ArtifactName`), the pushed digest, and what staging and prod run (`kubectl get deploy -o jsonpath='{..image}' --kubeconfig=<scratch>` on a throwaway cluster, or the platform API) (B). The `load: true` variant fails first: the scanned image ID and the pushed digest differ.

### 5. Provenance and verification (RL-7, CT-R04–R07)

```
BAD:   cosign verify --certificate-identity-regexp '.*' … api:prod          (any workflow, any repo; and a tag)
       gh attestation verify oci://…:prod --owner acme                     (any repo in the org built it)
       cosign attach sbom …   ·   cosign-release: 'v2.4.1'   ·   aquasec/trivy:0.67.2 (no digest)   ·   --provenance=false
GOOD:  cosign verify --certificate-identity 'https://github.com/O/R/.github/workflows/publish.yml@refs/heads/main' \
         --certificate-oidc-issuer https://token.actions.githubusercontent.com <repo>@<digest>
       gh attestation verify oci://<repo>@<digest> --repo O/R --signer-workflow O/R/.github/workflows/publish.yml \
         --source-ref refs/heads/main --deny-self-hosted-runners
```
**Read the code:**
- Every 5a `VERIFY` row: does it pin **the workflow file and the ref** that may build this artifact, plus the issuer? A valid signature or attestation from the wrong workflow is the TanStack shape (2026-05-11). `--owner` alone accepts any repository of the org [R, gh 2.98.0 help].
- Is the verify by digest, unmasked (`|| true`), with the transparency log on? Is it enforced where it counts (a deploy job that fails, or infrastructure `admission-policy`), or only advisory?
- 5b floors (`THR-SCANNER-FLOOR`): cosign ≥ 3.1.3; trivy, syft, grype, hadolint pinned by version **and** digest. A signer on cosign v3 with a verifier that cannot read v3 bundles or OCI 1.1 referrers blocks deploys or, set to audit mode, passes everything (CT-R07) [R].
- 5c: is provenance produced at all (build-push-action defaults to `mode=min` on private repos and `mode=max` on public ones; its default predicate is SLSA v0.2 unless `version=v1`; `load: true` and the docker exporter produce none) [R, Docker docs read 2026-10-10]? Is the SBOM an attestation or an attached blob? Is a multi-arch index signed with `--recursive`?
- 5d: do release assets ship with `SHA256SUMS` or an attestation (`gh release verify-asset` on an immutable release)?

**Finding when** the verify would accept an artifact from a workflow or ref that should not produce it, a tool in the release path is below its floor, or a shipped artifact carries nothing a consumer could verify. With no verify anywhere and no consumer that could verify, the row is M and names what the first verify should pin. **Proof (V224):** the negative test — in a sandbox, sign a scratch image from another workflow or ref, push it to a scratch registry, and run the project's own verify line against it: it must be **rejected**, and every platform of the index must verify (B). `release-security` runs it (§ Proof).

### 6. Release automation (RL-8)

```
BAD:   googleapis/release-please-action  with: token: ${{ secrets.GITHUB_TOKEN }}   (or no token: the default)
       changesets/action  with no token                                              (the release PR runs no checks)
GOOD:  a GitHub App token (actions/create-github-app-token) or a fine-grained PAT, and the release branch's required checks
```
**Read the code:** Which `RELEASE-BOT` rows use the default or `GITHUB_TOKEN`? A PR opened by `GITHUB_TOKEN` triggers no workflow runs [K: GitHub's documented behaviour, settled by V225]. Does a ruleset require checks on the release PR (then it cannot merge green-less; it stays Pending)? Does semantic-release push to a protected branch through a bypass?

**Finding when** the release PR can merge with no required check having run on it. **Proof (V225):** `gh pr checks <release PR>` lists the required checks as run (A).

### 7. Rollback target retention (DP-9)

```
BAD:   actions/delete-package-versions  min-versions-to-keep: 1     ·   ECR lifecycle countNumber: 1, tagStatus: any
       helm upgrade … --history-max 1                                ·   rollback.sh: set image api=…:${PREVIOUS_TAG}
GOOD:  keep ≥ the N releases a rollback window needs (and every digest a running environment references); roll back by digest
```
**Read the code:** Does each 7a rule delete what the previous release references (untagged digests are often exactly the N-1 images after a tag moves)? What does each 7b unit redeploy — a digest, an immutable tag, or a tag the second producer (§3) can rewrite? Helm `--history-max 0|1` leaves `helm rollback` nothing. `revisionHistoryLimit` is infrastructure's.

**Finding when** `/rollback-deploy` R2 cannot resolve N-1 by digest, or resolves a tag whose digest is no longer the one that ran. **Proof (V226):** `crane manifest <repo>@<N-1 digest>` resolves, and `/rollback-deploy --dry-run` names that digest (B).

## Proof

The oracles are in [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § DevOps. **Scope: settings reads (read-only), registry reads, a sandbox repository the user names, a scratch registry on localhost and `${TMPDIR}` — never a push, tag, delete or sign on the user's registry, and every `kubectl` through an isolated `--kubeconfig=<scratch>`.**

| § | Oracle | Tier | V |
|---|---|---|---|
| 1 | Settings read (tag ruleset, `immutable`) + a non-default-branch tag refused in a sandbox | A + R | V220 |
| 2 | Release dry run prints one version | T | V221 |
| 3 | Second release run against a scratch registry is a no-op, same digests | R | V222 |
| 4 | Digest continuity: build = scanned = pushed = staging = prod | B | V223 |
| 5 | Verify negative test: another workflow's or ref's signature is rejected; every platform verifies (`release-security` audit mode) | B | V224 |
| 6 | `gh pr checks` on the release PR | A | V225 |
| 7 | `crane manifest <repo>@<N-1 digest>` resolves | B | V226 |

**The executor contract (§5 → `release-security`).** When a registry is reachable, §5 calls `release-security` in **audit mode** with: the artifact as `<repo>@<digest>` (from 0c / the deploy, never a tag), the expected identity (`https://github.com/<o>/<r>/.github/workflows/<file>@<ref>`) and issuer, the platforms of the index, and `THR-SCANNER-FLOOR`. It returns one row each — `FLOOR`, `SCAN`, `SBOM`, `SIGN`, `VERIFY+`, `VERIFY-`, `DIGEST` — or `NOT-RUN (<reason>)`. A `VERIFY-` that reports `ACCEPTED` is the V224 failure. A `NOT-RUN` makes §5 `blocked`.

## Output

```
release-integrity-scan — lanes: github-actions (6 workflows; ci-graph.py ruby-psych), gitlab, scripts (4), release-please, changesets
Registry: unreachable (no credential) → B-tier rows written out · settings: UNREADABLE (no token) · security: installed · infrastructure: not installed

Findings: 19 · Unconfirmed: 8 (three rows shown)

1. .github/workflows/build.yml:8                                          [report-with-fix]   high
   §4 RL-6 — job image: build (load: true) → trivy scans api:scan → a second build pushes via `outputs: …push=true`
   (REBUILD-AFTER-SCAN, PUSH-VIA-OUTPUTS; ci-graph lists the job as publishes=no). The pushed digest was never scanned,
   and `load: true` carries no attestations. Proof: V223 written out (scanned image ID ≠ pushed digest). Fix: one
   build-push step with `push: true`, `id: build`; scan `ghcr.io/acme/api@${{ steps.build.outputs.digest }}`; deploy that digest.

2. .github/workflows/cd.yml:21                                            [report-with-fix]   high
   §5 CT-R05 — `cosign verify --certificate-identity-regexp '.*'` on `api:prod` (a tag): any workflow in any repo passes.
   Proof: V224 negative test written out. Fix: `--certificate-identity 'https://github.com/acme/shop/.github/workflows/build.yml@refs/heads/main'`
   + the issuer, by digest (cd.yml:27 already has the right shape for web).

3. .github/workflows/registry-prune.yml:15                                 [report-flagged]    high
   §7 DP-9 — keeps 1 version of api; the N-1 digest the rollback needs is deleted on the next run.
   Unproven link: the registry's version list (UNREADABLE). Settling test: V226 `crane manifest ghcr.io/acme/api@<N-1>`.

Verification: 48 candidates → 19 findings · 8 unconfirmed · 3 hardening · 0 pre-existing · 15 refuted (self-verified) · 3 routed

Class coverage:
  §1  release ref movable          Unconfirmed (2 tag triggers, 2 with no ancestry check; rulesets UNREADABLE)
  §2  version sources              checked (8 sources → 1 split, 1 pre mode left on; chart version refuted § 17)
  §3  idempotence                  checked (12 publish sites → 5 unguarded; § 18 ×2 refuted)
  §4  shipped = tested             checked (4 producer jobs → 1 finding; 1 rebuild-in-deploy unconfirmed; web job refuted)
  §5  provenance / verify          checked (4 verify, 1 sign, 1 attach; 1 finding; release-security: blocked (registry))
  §6  release automation           checked (3 release bots → 2 default-token rows; App token refuted)
  §7  rollback retention           checked (3 rules, 1 rollback unit → 1 flagged; keep-30 refuted)
  routed                           SECRET-BUILD-ARG → security iac-scan 2b · newTag: main → security iac-scan 4j · NPM_TOKEN → security ci-security-scan §6
```

`[report-with-fix]`: the unit, the artifact, the fact and the oracle are in hand, and the fix is local to the unit. `[report-flagged]`: one link is unproven — a settings read, a registry read, a `[K?]` platform fact, a dry run that needed a token. The row names the link and the settling test.

The coverage block lists **all seven** §s on every run: `checked (k hits → m findings)` only when the grep or graph ran on a lane that is present; `N/A (no release trigger)` / `N/A (no publish site)` / `N/A (no version source)` / `N/A (no verify, no signature)` — the last still prints the §5 M row when artifacts ship; `blocked (<reason>)` when a grep, the graph, the registry or the executor failed (a `ci-graph.py` exit 2 makes the GitHub §4 rows `blocked (ci-graph NOT-RUN: <reason>)`); `Unconfirmed (… UNREADABLE …)`; `Live, unreviewed (k groups / n hits)` for a partial review.

## False positives / precedents

The verifier reads [`precedents/devops.md`](../../../../snippets/precedents/devops.md) and [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 4. The ones this skill meets most:
- **§ 17** Declared independent versioning. **§ 18** `changeset publish`, `--skip-existing`, `--skip-duplicate` and goreleaser `keep-existing` are idempotent by design. **§ 19** A per-architecture manifest list is one digest; a platform that cannot pull by digest plus an immutable tag is addressable. **§ 20** A static SPA built per environment when declared and deterministic. **§ 21** An `--ignore-unfixed` PASS means "no fixable High/Critical".
- **§ 41** A tool that errored, parsed nothing or could not reach the registry is NOT-RUN. **§ 44** The `on:` key read as `true`. **§ 1** Security-shaped rows are routed. **§ 5** One finding per unit. **§ 6** A 403 is `UNREADABLE`.

Read-step rules measured on the real repo (2026-10-10), applied with a `file:line`: a producer that guards its own push (`imagetools inspect` → skip) is idempotent only if it is the **only** producer of that tag; a scan by tag is a §4 finding only when something can write that tag between the scan and the deploy; a single CI build with no scan, signature or verify is §5 M, not §4.

Rationalizations to reject:
- "The image has a valid signature / SLSA provenance": from which workflow and ref? (TanStack, 2026-05-11.)
- "We tag by commit SHA, so tags are immutable": a SHA-named tag on GHCR can be re-pushed; only the digest is fixed.
- "The scan passed": on which digest — the one that was pushed, and the one that deploys?
- "Rollback = redeploy the previous tag": a moved tag, or a pruned digest.

## When to run

- On any diff touching a release workflow, a publish or deploy job, a release script or npm script, a release tool's config or manifest, a version file, a verify or signing step, or a registry retention rule.
- After `/dockerize` or `/add-ci` generate a release path, after `release-security` is wired, and before `/rollback-deploy` trusts its R3 ("artifact reference immutable").
- On every whole-repo `/devops-audit`, reporting all seven §s.

## Halt conditions

- **Do not report a critical or high row as confirmed until a separate verifier has refuted it.** That verifier is not the run that found it; it applies [`refute-before-report.md`](../../../../snippets/refute-before-report.md) with `precedents/devops.md`. Under `/devops-audit` that is its verification phase; standalone, run the protocol as a second pass and tag those rows `self-verified`. List the rest as Unconfirmed, Hardening, Pre-existing or Refuted; never drop them.
- **Halt on a finding missing its anchors:** the line, the release unit, the artifact, the fact with its date, and the fix.
- **No "verified" without the identity:** a §5 row that says a verify exists names the identity and issuer it pins, read from the line.
- **No `checked` on a lane whose tool failed:** `ci-graph.py` exit 2, an rg exit 2, a registry or executor `NOT-RUN` are `blocked`.
- **Never push, tag, delete, sign or attest on the user's registry, and never publish a package, to prove a row.** V222 and V224 run against a scratch registry and a sandbox repo; otherwise the row is Unconfirmed with the command written out. Every `kubectl` takes an isolated `--kubeconfig=<scratch>`; no cloud CLI runs on a default profile.
- **No proposed fix may weaken a control to clear a row:** no `--certificate-identity-regexp`, no `--insecure-ignore-tlog`, no removed ancestry check, no `--skip-existing` on a registry where a re-run must fail loudly, no lower retention.
- **Do not print "releases look fine" without the coverage block.** **Do not re-derive a class another skill owns** (§ Boundaries); cross-link it.

## Related

- `release-security` (this pack) is the executor §5 calls (audit mode) and the CI gate the fixes wire; `/devops-audit` dispatches this skill and folds its coverage block into the release rows; `/devops-fix` closes them with V220–V226. `/rollback-deploy` R3 reads §7.
- `@deployment-engineer` judges these rows; `@devops-architect` designs the release path this skill then judges.
- `pipeline-integrity-scan` (publish gating, RL-3), `deploy-safety-scan`, `container-build-scan` (this pack) own the neighbouring classes (§ Boundaries).
- `ci-security-scan` §5–§6 and `iac-scan` 2b / 4j (security), `admission-policy` (infrastructure), each when its pack is installed.

## Sources

Classes RL-1–RL-8, CT-R04–R07 and DP-9, the tool versions and the dated facts (immutable releases GA 2025-10-28; the trivy compromise 2026-03-19; the TanStack postmortem 2026-05-11; cosign 3.1.3 and GHSA-fx35-mq7g-6g98, 2026-08-06; `gh attestation verify` flags from gh 2.98.0 help; build-push-action attestation defaults from Docker's docs read 2026-10-10) come from the devops research catalog and its container/artifact and release/deploy notes (2026-10-10) and the batch-4 devops eval (DV-3). The `ci-graph.py` `publishes=` gap, the `\`-continuation miss and the two-producer read are this skill's own measurements (2026-10-10). Paraphrased; no text reproduced beyond identifiers.
