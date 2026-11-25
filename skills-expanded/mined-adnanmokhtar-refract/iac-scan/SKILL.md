---
name: iac-scan
description: "Infrastructure files as attack surface — Dockerfiles, compose, Kubernetes, Terraform, CI workflows and reverse-proxy configs: root containers, exposed ports and dashboards, secrets in images or env, wildcard IAM, public buckets, script injection in CI, missing TLS and headers at the edge."
kind: skill
pack: security
allowed-tools: [Read, Grep, Glob, Bash, Write]
---

# Skill: iac-scan

## Premise

A container that runs as root, a database port published on every interface, a CI token with `write-all`, an nginx `alias` one slash short — each is exploitable while every line of application code is correct. This skill is the security pack's entry point for the files that decide **where the code runs, who can reach it and with what privilege**. It runs regardless of which other packs are installed; the devops and infrastructure packs add depth (§ Related) when present.

Like `sast-scan`, it has two halves:

1. **A tool ledger** — each IaC scanner that applies is **RAN** (version, exit code, files read, hits, output path), **SKIPPED** (`n/a` only when grep 1 proves the file type is absent), or **NOT-INSTALLED** (the exact install command, printed for the user — the audit never installs, downloads or pulls a scanner). A scanner that did not run is a `COVERAGE:` gap for `/security-audit`, never a pass.
2. **The detectors below, run as greps plus a read, whatever the scanners said.** The scanners are not a superset of them. On this skill's own vulnerable sample (2026-10-01: checkov 3.3.21, trivy 0.74.0, hadolint 2.15.1, kube-linter 0.8.3, zizmor 1.30.1, gixy-ng 0.2.55, semgrep 1.178.0), every item here passed every scanner that read its file:
   - a multi-stage Dockerfile whose `USER` is set only in the builder stage (hadolint, checkov, trivy);
   - `COPY .env` into the image;
   - `0.0.0.0/0` on port 5432 (checkov, trivy);
   - a compose file with no top-level `version:` key (semgrep `p/docker-compose`);
   - `eval "$CI_COMMIT_MESSAGE"` in GitLab CI (checkov);
   - a committed `kind: Secret`, a plain-text `DB_PASSWORD` env value, and a Grafana Ingress with no auth;
   - nginx `autoindex on` and `Access-Control-Allow-Origin *` with credentials (gixy-ng).

**Every finding cites `<file:line>`** (for a manifest, `<file:line>` plus the field path, e.g. `spec.template.spec.containers[0].securityContext.privileged`) **+ the failing condition + what it exposes to whom + the fix + severity**. A scanner rule id alone is not a finding.

**Out of scope, on purpose:** checks that are operations, not security — `HEALTHCHECK`, probes, resource requests/limits, replicas, PDBs, log retention, bucket versioning, Multi-AZ. Scanners emit them in bulk; triage marks them `ops — out of scope` and moves on. The **value** of a leaked secret is `secret-scan-method`'s (rotation first); this skill owns the fact that the secret is **in a deployable file**. Image CVEs, SBOM and signing are the devops pack's `release-security` skill's — § 1 dispatches it when that pack is installed. What the running edge actually serves is `/security-live-scan`'s.

## Adapt to the codebase

| Surface | Scanner lane (installed tools and already-local images only) | Install for later | Suppression to inventory |
|---|---|---|---|
| **Dockerfile** | `docker run --pull=never --rm -i "hadolint/hadolint:v2.15.1@$HADOLINT_DIGEST" hadolint -f json --failure-threshold warning - < <file>`; `trivy config`; `checkov --framework dockerfile` | `brew install hadolint trivy` (or `docker pull` the pinned image) · `pipx install checkov` | `# hadolint ignore=DL####` · `.hadolint.yaml` · `#checkov:skip=` · `#trivy:ignore:` |
| **Compose** | semgrep `p/docker-compose` — matches only files with a top-level `version:` key; checkov and trivy do not read compose. **Greps are the primary lane.** | — | `# nosemgrep` |
| **Kubernetes** (raw, Helm, Kustomize) | render first: `helm template <chart> -f <values> > "$SCAN/rendered.yaml"` / `kubectl kustomize <dir> > …`; then `trivy config`, `checkov`, `kube-linter lint --add-all-built-in`; `kubescape scan <path> --format json --output … --keep-local` as an alternative | `brew install kube-linter kubescape helm` | `ignore-check.kube-linter.io/<check>` · `checkov.io/skip<N>` annotations · `#trivy:ignore:` |
| **Terraform / CloudFormation** | `checkov -d`; `trivy config` (tfsec's successor) | as above | `#checkov:skip=` · `#trivy:ignore:` / legacy `#tfsec:ignore:` · `.trivyignore` |
| **Pulumi** | no scanner reads Pulumi programs; grep 5c on the program, then `pulumi preview --json` read as a plan | — | — |
| **GitHub Actions** (and the other five CI platforms) | `ci-security-scan` owns the lane and its ledger (zizmor ≥ 1.28, poutine, octoscan, actionlint); this skill runs `zizmor --offline --persona=auditor --format json .github/workflows` (installed, ≥ 1.28) for its own row; semgrep `p/github-actions` | `brew install zizmor actionlint` | `# zizmor: ignore[<audit>]` · `zizmor.yml` · `.github/actionlint.yaml` |
| **GitLab CI** | `checkov --framework gitlab_ci` — zero failures on the sample that held `eval "$CI_COMMIT_MESSAGE"`; **greps are the primary lane** | — | — |
| **nginx** | `gixy -f json <conf>` (gixy-ng, the maintained fork of yandex/gixy); semgrep `p/nginx` | `pipx install gixy-ng` | `--skips` in the project's own invocation |
| **Caddy, Apache, Traefik** | no maintained static scanner — **greps are the primary lane** | — | — |
| **`.env` files** | `git ls-files` + grep 8 | — | `.gitignore` · `.dockerignore` |

A semgrep pass over the IaC rulesets (`p/dockerfile p/docker-compose p/kubernetes p/terraform p/github-actions p/nginx`) is part of this skill, not `sast-scan`'s.

## Pre-flight greps

Run from the repo root. Every command excludes vendored and generated trees and names its path (`.`, `"$SCAN"`) explicitly — with no path and a non-terminal stdin (an agent harness, a CI step), `rg` searches stdin and waits forever. Rendered and extracted files go to `$SCAN`, never into the repo.

```bash
X=(-g '!**/node_modules/**' -g '!**/vendor/**' -g '!**/dist/**' -g '!**/build/**' -g '!**/.terraform/**')
SCAN="$(mktemp -d "${TMPDIR:-/tmp}/iac-scan.XXXXXX")"

# 1. Inventory — which surfaces exist (decides every SKIPPED n/a in the ledger).
rg --files . --hidden "${X[@]}" -g '!.git/**' | rg --pcre2 -i '(^|/)(Dockerfile[^/]*|[^/]+\.dockerfile|(docker-)?compose[^/]*\.ya?ml|[^/]+\.tf|[^/]+\.tfvars|Chart\.yaml|kustomization\.ya?ml|Pulumi[^/]*\.ya?ml|\.gitlab-ci\.yml|[^/]*nginx[^/]*\.conf|Caddyfile|[^/]+\.caddy(file)?|httpd\.conf|apache2?\.conf|\.htaccess|traefik[^/]*\.(ya?ml|toml)|\.env[^/]*|\.dockerignore)$|\.github/workflows/[^/]+\.ya?ml$|(^|/)(conf\.d|sites-(available|enabled))/'
rg -l --pcre2 -g '*.y*ml' "${X[@]}" '^kind:\s*(Deployment|StatefulSet|DaemonSet|Pod|Job|CronJob|Service|Ingress|IngressRoute|HTTPRoute|Role|ClusterRole|RoleBinding|ClusterRoleBinding|Secret|NetworkPolicy|ServiceAccount)\b' .
rg -l -g '*.y*ml' -g '*.json' -g '*.template' "${X[@]}" 'AWSTemplateFormatVersion|Type:\s*"?AWS::' .
rg -l --pcre2 -g '*.conf' -g '*.nginx' -g '*.conf.template' "${X[@]}" '^\s*(server_name|proxy_pass|listen|location)\s' .
#  e. Edge config embedded in YAML — a ConfigMap key (`Caddyfile: |`, `nginx.conf: |`) or an ingress snippet annotation.
#     Grep 7 globs file names and cannot see it: each block is copied to "$SCAN/edge" with the source's line numbers kept.
E='^\s*-?\s*"?(Caddyfile|[\w.-]+\.(conf|caddy|caddyfile)|nginx\.ingress\.kubernetes\.io/(server|configuration|stream)-snippet)"?\s*:\s*[|>]'
mkdir -p "$SCAN/edge"; rg -l --pcre2 -g '*.y*ml' "${X[@]}" "$E" . | while IFS= read -r f; do awk 'b { if ($0 ~ /^[ \t]*$/) { print ""; next } match($0, /^ */); if (RLENGTH > k) { print substr($0, k + 1); next } b = 0 }
  /^ *(- +)?"?(Caddyfile|[A-Za-z0-9_.-]+\.(conf|caddy|caddyfile)|nginx\.ingress\.kubernetes\.io\/(server|configuration|stream)-snippet)"? *: *[|>]/ { match($0, /^ */); k = RLENGTH; b = 1 }
  { print "" }' "$f" > "$SCAN/edge/$(echo "${f#./}" | sed 's#/#__#g').conf"; echo "$f"; done
#  f. Render every Kustomize dir (Helm: `helm template <chart> -f <values> > "$SCAN/rendered-<chart>.yaml"`); grep 4 reads both.
#     Offline render, never a cluster: an empty kubeconfig first. No kubectl and no kustomize → NOT-RENDERED (§ 3 Unrendered).
export KUBECONFIG="$SCAN/empty-kubeconfig"; : > "$KUBECONFIG"
rg --files . -g 'kustomization.y*ml' "${X[@]}" | while IFS= read -r k; do d="$(dirname "$k")"; o="$SCAN/rendered-$(echo "${d#./}" | tr '/' '_').yaml"
  if command -v kubectl >/dev/null; then kubectl kustomize "$d" > "$o" && echo "$d"; elif command -v kustomize >/dev/null; then kustomize build "$d" > "$o" && echo "$d"; else echo "NOT-RENDERED $d"; fi; done
#  g. No Terraform / Pulumi / CloudFormation found above → the provisioning commands in runbooks and scripts are the plan § 4 reads.
#     -U: a `create secret` split over `\` lines prints whole (each `--from-literal` key), `kubectl -n ns create` included.
rg -n -U --pcre2 -g '*.md' -g '*.sh' "${X[@]}" '^\s*(\$\s+)?(doctl|aws|gcloud|az|gsutil|s3cmd)\s+[\w-]+\s+[\w-]+|kubectl\b[^\n]*?\bcreate\s+secret\b(?:[^\n]*\\\n)*[^\n]*--from-literal' .

# 2. Dockerfile (§ 1) — final-stage user, build secrets, secret files copied in, unverified downloads (pipe or `<(curl …)`),
#    floating bases, then build-time module fetches with no version (`xcaddy --with mod`, `go install …@latest`, `npm i -g x`).
#  a. The final stage's effective USER through the stage chain (`FROM <stage>` inherits it); root:*/0:* are ROOT; a chain
#     that ends at an external base with no USER prints INHERIT-EXTERNAL — read the base's user before rating it.
rg --files . -g 'Dockerfile*' -g '*.dockerfile' "${X[@]}" | while IFS= read -r f; do awk 'toupper($1) == "FROM" { n++; r = ""; m = ""; c = 0
    for (i = 2; i <= NF; i++) { if ($i ~ /^--/) continue; if (r == "") { r = $i; continue } if (toupper($i) == "AS" && i < NF) m = tolower($(i + 1)) }
    par[n] = r; ln[n] = FNR; if (m != "") idx[m] = n; next } toupper($1) == "USER" && n { usr[n] = $2; set[n] = 1 } toupper($1) ~ /^(CMD|ENTRYPOINT)$/ { c = FNR }
  END { if (!n) exit; s = n; h = 0; while (!set[s] && (tolower(par[s]) in idx) && h++ < 50) s = idx[tolower(par[s])]; at = FILENAME ":" (c ? c : ln[n]) ": final stage (FROM line " ln[n] ")"
    if (!set[s]) { print at " sets no USER; base " par[s] " -> INHERIT-EXTERNAL (read: crane config " par[s] " | jq -r .config.User)"; exit }
    v = (usr[s] ~ /^(root|0)(:|$)/) ? "ROOT" : (usr[s] ~ /\$/ ? "ARG-DRIVEN (resolve the default)" : "")
    if (v != "") print at " user " usr[s] " -> " v (s != n ? " [inherited from the stage at line " ln[s] "]" : "") }' "$f"; done
rg -n --pcre2 -i -g 'Dockerfile*' -g '*.dockerfile' "${X[@]}" '^\s*(ARG|ENV)\s+\w*(SECRET|TOKEN|PASSW(OR)?D|API_?KEY|PRIVATE_?KEY|ACCESS_?KEY|CREDENTIAL)\w*' .
rg -n --pcre2 -i -g 'Dockerfile*' -g '*.dockerfile' "${X[@]}" '^\s*(COPY|ADD)\s+(--\S+\s+)*[^\n]*(\.env\b|\.pem\b|\.key\b|\.p12\b|\.pfx\b|id_rsa|id_ed25519|\.npmrc|\.pypirc|\.netrc|credentials)' .
rg -n --pcre2 -i -g 'Dockerfile*' -g '*.dockerfile' "${X[@]}" '^\s*ADD\s+(--\S+\s+)*https?://' .
rg -n --pcre2 -i --hidden -g 'Dockerfile*' -g '*.dockerfile' -g '*.sh' -g '*.y*ml' "${X[@]}" '\b(curl|wget)\b[^|\n]*\|\s*(sudo\s+)?(ba|z|da|k)?sh\b|\b((ba|z|da|k)?sh|source|\.)\s+<\(\s*(curl|wget)\b' .
rg -n --pcre2 -i -g 'Dockerfile*' -g '*.dockerfile' "${X[@]}" '^\s*FROM\s+(--\S+\s+)*[^\s:@]+(:latest)?(\s|$)' .
rg -n --pcre2 -g 'Dockerfile*' -g '*.dockerfile' -g '*.sh' "${X[@]}" '(?:--with\s+[^\s@=\\]+(?=\s|$))|\bgo\s+(install|get)\s+\S+@(latest|master|main)\b|\b(npm|pnpm|yarn)\s+(i|install|add)\s+(-g|--global)\s+(@[\w.-]+/)?[\w.-]+(?=\s|$)' .

# 3. Compose (§ 2) — ports without a loopback host IP, literal/default passwords, host-level privilege.
rg -n --pcre2 -g '*compose*.y*ml' "${X[@]}" '^\s*-\s*[\x22\x27]?(?!127\.0\.0\.1:|localhost:|\[::1\]:)[\d.\[\]:]*\d+:\d+' .
rg -n --pcre2 -i -g '*compose*.y*ml' "${X[@]}" '\w*(PASSWORD|_PASS|_PWD)\w*[\x22\x27]?\s*[:=]\s*[\x22\x27]?(?!\$\{)[^\s\x22\x27]+|ALLOW_EMPTY_PASSWORD|HOST_AUTH_METHOD[\x22\x27]?\s*[:=]\s*[\x22\x27]?trust' .
rg -n --pcre2 -g '*compose*.y*ml' "${X[@]}" '^\s*(privileged:\s*true|network_mode:\s*[\x22\x27]?host|pid:\s*[\x22\x27]?host|ipc:\s*[\x22\x27]?host|cap_add:|userns_mode:\s*[\x22\x27]?host)|(/var)?/run/docker\.sock|seccomp[:=]unconfined|apparmor[:=]unconfined|label[:=]disable' .

# 4. Kubernetes (§ 3) — the source tree AND the rendered output from 1f (a field set only by an overlay exists only there).
K=(-g '*.y*ml' "${X[@]}" -g '!*compose*.y*ml')
rg -n --pcre2 "${K[@]}" '^\s*(privileged:\s*true|allowPrivilegeEscalation:\s*true|runAsNonRoot:\s*false|runAsUser:\s*0\s*$|host(Network|PID|IPC):\s*true|hostPath:|readOnlyRootFilesystem:\s*false|automountServiceAccountToken:\s*true)|\b(SYS_ADMIN|NET_ADMIN|SYS_PTRACE|SYS_MODULE|DAC_READ_SEARCH|BPF)\b|^\s*add:\s*\[?\s*[\x22\x27]?ALL\b' . "$SCAN"
#  b. Per DOCUMENT, not per file: a workload with no runAsNonRoot: true — rendered output plus raw manifests that are not patches.
awk 'function f() { if (w && !ok) print fn ":" s ": " w " " n " has no runAsNonRoot: true"; w = n = ""; ok = 0 } FNR == 1 || /^---/ { f() }
  /^kind: *(Deployment|StatefulSet|DaemonSet|Pod|Job|CronJob|ReplicaSet) *$/ { w = $2; fn = FILENAME; s = FNR }
  /^(metadata: *\{ *| +)name: / && w && n == "" { x = $0; sub(/.*name: */, "", x); sub(/[,} ].*/, "", x); n = x }
  /runAsNonRoot: *true/ { ok = 1 } END { f() }' $(ls "$SCAN"/rendered-*.yaml 2>/dev/null) $(rg -l --pcre2 "${K[@]}" -g '!*patch*' '^kind:\s*(Deployment|StatefulSet|DaemonSet|Pod|Job|CronJob)\b' .) /dev/null
rg -n -U --pcre2 "${K[@]}" -e '-\s*name:\s*[\x22\x27]?\w*(PASSWORD|PASSWD|SECRET|TOKEN|API_?KEY|PRIVATE_?KEY|CREDENTIAL)\w*[\x22\x27]?\s*\n\s*value:\s*\S+' .
rg -n "${K[@]}" '^kind:\s*Secret\b' .
rg -l "${K[@]}" '^kind:\s*NetworkPolicy\b' . || echo "no NetworkPolicy in repo"
rg -n --pcre2 "${K[@]}" '^\s*type:\s*[\x22\x27]?(LoadBalancer|NodePort)\b|^\s*externalIPs:' .
rg -n -i --pcre2 "${K[@]}" '^\s*-?\s*host:\s*[\x22\x27]?[\w.-]*(grafana|kibana|prometheus|alertmanager|dashboard|argo|rabbitmq|pgadmin|adminer|phpmyadmin|jaeger|flower|traefik|consul|vault|minio|admin)[\w.-]*' .
rg -n -i "${K[@]}" 'auth-(url|type|signin|secret)|(whitelist|allowlist)-source-range|oauth2-proxy|forwardAuth|basicAuth|router\.middlewares' . || echo "no edge auth annotations in repo"
rg -n --pcre2 "${K[@]}" '^\s*-?\s*(verbs|resources|apiGroups):\s*\[[^\]]*[\x22\x27]\*[\x22\x27]|^\s*-\s*[\x22\x27]\*[\x22\x27]\s*$|name:\s*cluster-admin\b' .
#  j. Images deployed by tag, not digest (kustomize newTag too) — read with § 5's who-can-push-that-tag.
rg -n --pcre2 "${K[@]}" '^\s*(-\s*)?image:\s*[\x22\x27]?(?![^\s\x22\x27]*@sha256:)[^\s\x22\x27{]+|^\s*newTag:' .
#  k. NetworkPolicy rules wider than they read: peers with no `ports:` (every port), or `ports:` with no peers (every source).
rg -l "${K[@]}" '^kind:\s*NetworkPolicy\b' . "$SCAN" | xargs -r awk 'function f() { if (r && t && !p) print rf ":" r ": " d " rule names peers but no ports"; if (r && p && !t) print rf ":" r ": " d " rule names ports but no peers"; r = 0 }
  FNR == 1 { f(); np = 0; li = -1 }   # flush the previous file: a rule pending at EOF keeps its own file name
  /^---/ { f(); np = 0; li = -1; next } /^kind: *NetworkPolicy/ { np = 1 }
  np && /^ *(ingress|egress): *$/ { f(); match($0, /^ */); li = RLENGTH; ri = -1; d = $1; sub(/:$/, "", d); next }
  np && li >= 0 && /^ *[^ #]/ { match($0, /^ */); n = RLENGTH; if (n < li || (n == li && $0 !~ /^ *- /)) { f(); li = -1; next }
    if ($0 ~ /^ *- /) { if (ri < 0) ri = n; if (n == ri) { f(); r = FNR; rf = FILENAME; p = 0; t = 0; s = substr($0, n + 3) } else s = "" } else s = (n == ri + 2) ? substr($0, n + 1) : ""
    if (s ~ /^(from|to):/) t = 1; if (s ~ /^ports:/) p = 1 } END { f() }'
#  l. Observability backends with auth off (Loki, Prometheus admin API, anonymous Grafana) — chart values included.
rg -n --pcre2 "${K[@]}" 'auth_enabled:\s*false|--web\.enable-admin-api|enableAdminAPI:\s*true|GF_AUTH_ANONYMOUS_ENABLED\W+true|anonymous:\s*\{?\s*enabled:\s*true|disable_login_form\W+true' .
#  m. Migration and backup jobs — whose DB role and which bucket each one uses (§ 3, § 4).
rg -n --pcre2 -i "${K[@]}" '^(?!\s*#)[^\n]*?(\bname:\s*[\x22\x27]?([\w-]*migrat[\w-]*[\x22\x27]?\s*$|\w*BACKUP\w*(URI|URL|BUCKET|DEST\w*|TARGET)\b)|\b(migration:(up|run)|db:migrate|migrate\s+(deploy|up)|alembic\s+upgrade|flyway\s+migrate|liquibase\s+update|pg_dump(all)?|mysqldump|mongodump)\b)' .
#  n. NetworkPolicy ipBlock width, with or without `ports:` (4k reads only peers vs ports): a peer CIDR of /20 or wider
#     (IPv6 /64 or wider) — usually the VPC, the node range, a whole RFC 1918 block or the VPN, all of which bypass the edge.
rg -l "${K[@]}" '^kind:\s*NetworkPolicy\b' . "$SCAN" | xargs -r rg -H -n --pcre2 '^\s*-?\s*cidr:\s*[\x22\x27]?(?:\d{1,3}(?:\.\d{1,3}){3}/(?:[0-9]|1\d|20)|[0-9a-fA-F:]+/(?:[0-9]|[1-5]\d|6[0-4]))[\x22\x27]?\s*(?:#.*)?$'

# 5. Terraform / CloudFormation / bucket policies (§ 4): (a) public data + public DBs, a policy with Principal "*",
#    (b) world-open ingress, (c) Pulumi programs, (d) wildcard IAM, (e) encryption / IMDS / TLS floor, (f) literal passwords.
T=(-g '*.tf' -g '*.tfvars' -g '*.y*ml' -g '*.json' -g '*.template' "${X[@]}" -g '!*compose*' -g '!package*.json')
rg -n --pcre2 "${T[@]}" '\b(acl\s*=\s*"public-read(-write)?"|AccessControl:\s*PublicRead(Write)?|(block_public_acls|block_public_policy|ignore_public_acls|restrict_public_buckets)\s*=\s*false|"?(allUsers|allAuthenticatedUsers)"?|container_access_type\s*=\s*"(blob|container)"|allow_nested_items_to_be_public\s*=\s*true|publicly_accessible\s*=\s*true|PubliclyAccessible:\s*true)|[\x22\x27]?Principal[\x22\x27]?\s*[:=]\s*(\{\s*[\x22\x27]?AWS[\x22\x27]?\s*[:=]\s*)?\[?\s*[\x22\x27]\*[\x22\x27]' .
rg -n --pcre2 "${T[@]}" '\b(cidr_blocks|ipv6_cidr_blocks|CidrIpv6|CidrIp|source_ranges|source_address_prefix(es)?|cidrBlocks)\b[^\n]*(0\.0\.0\.0/0|::/0|[\x22\x27]\*[\x22\x27]|Internet)' .
rg --files . -g 'Pulumi.y*ml' | xargs -n1 dirname | sort -u | xargs -r -I{} rg -n --pcre2 -g '*.{ts,js,py,go,cs,java,yaml,yml}' -g '!**/node_modules/**' \
  '\b(acl|cannedAcl|publiclyAccessible|publicly_accessible|PubliclyAccessible|httpTokens|http_tokens|HttpTokens|storageEncrypted|storage_encrypted|StorageEncrypted|encrypted)\b\s*[:=]\s*[\x22\x27]?(public-read(-write)?|[Tt]rue|optional|[Ff]alse)\b|\b(cidrBlocks|cidr_blocks|CidrBlocks)\b[^\n]*0\.0\.0\.0/0|[\x22\x27]?\b(Action|Resource)[\x22\x27]?\s*:\s*[\x22\x27]\*[\x22\x27]|\b(allUsers|allAuthenticatedUsers)\b' {}
rg -n --pcre2 "${T[@]}" '[\x22\x27]?\b(Action|actions)[\x22\x27]?\s*[:=]\s*\[?\s*[\x22\x27](\*|[a-z0-9-]+:\*)[\x22\x27]|[\x22\x27]?\bResource[\x22\x27]?\s*[:=]\s*\[?\s*[\x22\x27]\*[\x22\x27]|\bNotAction\b|roles/(owner|editor)\b|role_definition_name\s*=\s*"(Owner|Contributor)"' .
rg -n --pcre2 "${T[@]}" '\b(http_tokens\s*=\s*"optional"|HttpTokens:\s*optional|(storage_)?encrypted\s*=\s*false|StorageEncrypted:\s*false|enable_https_traffic_only\s*=\s*false|min_tls_version\s*=\s*"TLS1_[01]")' .
rg -n --pcre2 -g '*.tf' -g '*.tfvars' "${X[@]}" '^\s*(password|master_password|admin_password|secret)\s*=\s*"[^"$]+' .
#  g. The registry form of 4j — tags anyone with push can overwrite: ECR `MUTABLE` (also the default when the attribute is
#     absent; the awk lists those), CloudFormation `ImageTagMutability: MUTABLE`, Artifact Registry `immutable_tags = false`.
rg -n --pcre2 "${T[@]}" 'image_tag_mutability\s*=\s*"MUTABLE(_WITH_EXCLUSION)?"|ImageTagMutability:\s*[\x22\x27]?MUTABLE|immutable_tags\s*=\s*false' .
rg -l -g '*.tf' "${X[@]}" 'resource\s+"aws_ecr_repository"' . | xargs -r awk 'function f() { if (r && !m) print at ": aws_ecr_repository with no image_tag_mutability (the default is MUTABLE)"; r = 0 }
  FNR == 1 || /^resource / { f() } /^resource +"aws_ecr_repository"/ { r = 1; m = 0; at = FILENAME ":" FNR } r && /image_tag_mutability/ { m = 1 } END { f() }'
#  h. Dangling DNS (D1): a declared record whose literal target is a third-party name someone else can claim once it is
#     released. Read whether that bucket, app or site is declared and owned here; CloudFront and ELB targets are not claimable.
rg -n --pcre2 -g '*.zone' "${T[@]}" '\b(records|alias|value|target|cname|content)\b[^\n]*[\x22\x27][\w.-]+\.(s3-website[.-][\w.-]+\.amazonaws\.com|s3\.amazonaws\.com|herokuapp\.com|herokudns\.com|azurewebsites\.net|cloudapp\.(net|azure\.com)|trafficmanager\.net|blob\.core\.windows\.net|azureedge\.net|azurefd\.net|github\.io|elasticbeanstalk\.com|netlify\.app|pages\.dev|vercel\.app|fly\.dev|surge\.sh|ghost\.io|myshopify\.com|readthedocs\.io|bitbucket\.io|wpengine\.com|pantheonsite\.io|web\.app|firebaseapp\.com)\.?[\x22\x27]' .

# 6. CI (§ 5) — the candidate list `ci-security-scan` judges; its pre-flight is the full set on six platforms.
W=(--hidden -g '**/.github/workflows/*.y*ml' -g '**/action.y*ml')
#  a. Privileged and comment triggers (a permission key such as `issues: write` is excluded).
EXT='^(on:\s*\[?[^\n#]*?\b|\s{2}-?\s*)(pull_request_target|workflow_run|issue_comment|pull_request_review_comment|pull_request_review|discussion_comment|discussion|issues)\b(?!\s*:\s*(write|read|none)\b)'
rg -n --pcre2 "${W[@]}" "$EXT" .
#  b. Every way PR code reaches the runner, in those files only: head/merge refs, refs/pull/, the head repo, gh pr checkout, git fetch pull/.
rg -l --null --pcre2 "${W[@]}" "$EXT" . | xargs -0 -r rg -H -n --pcre2 'ref:\s*[\x22\x27]?\$\{\{\s*github\.(event\.pull_request\.head\.(sha|ref)|head_ref|event\.workflow_run\.head_(sha|branch))|refs/pull/|\bpull/\$\{\{|allow-unsafe-pr-checkout:\s*true|\bgh\s+pr\s+checkout\b|\bgit\s+fetch\b[^\n]*\bpull/|\bmerge_commit_sha\b|repository:\s*[\x22\x27]?\$\{\{\s*github\.event\.(pull_request\.head\.repo|workflow_run\.head_repository)\.full_name'
#  c. Each tainted expression on its own line (-o); integer, enum, boolean and comparison expressions are filtered out.
INJ='\$\{\{(?:(?!\}\}).)*?(?:\bgithub\.event\s*\[|\bgithub\.event\.(?:issue|pull_request|comment|review|review_comment|discussion|discussion_comment|head_commit|commits|pages|workflow_run|inputs|release|merge_group|check_run|check_suite|deployment|client_payload)\b|\bgithub\.head_ref\b|(?<![\w.])inputs\.|(?<![\w.])env\.|\bsteps\.[\w-]+\.outputs\.|\bneeds\.[\w-]+\.outputs\.|(?<![\w.])matrix\.)(?:(?!\}\}).)*\}\}'
rg -n -o --pcre2 "${W[@]}" "$INJ" . | rg -v --pcre2 ':\$\{\{\s*github\.event\.[\w.]+\.(?:number|id|run_number|run_attempt|conclusion|fork|draft|merged)\s*\}\}$|:\$\{\{(?:(?!&&|\|\|)[^}])*(?:==|!=)(?:(?!&&|\|\|)[^}])*\}\}$'
#  d. Non-SHA `uses:`; e. write scopes in every form, flow-map included; f. files with no permissions block; g. secrets in logs; h. self-hosted.
rg -n --pcre2 "${W[@]}" '^\s*-?\s*uses:\s*(?!\./|docker://)[^@\s]+@(?![0-9a-f]{40}\b)\S+' .
rg -n --pcre2 "${W[@]}" 'permissions:\s*write-all|\b(contents|packages|id-token|actions|pull-requests|deployments|security-events|statuses|checks|issues|attestations|pages|discussions|repository-projects)\s*:\s*write\b' .
rg --files-without-match "${W[@]}" '^\s*permissions:' .
rg -n --pcre2 "${W[@]}" '\b(echo|printf|cat)\b[^\n]*\$\{\{\s*secrets\.|\bset\s+-[a-z]*x|ACTIONS_STEP_DEBUG|\bprintenv\b|toJSON\(\s*secrets\s*\)' .
rg -n --pcre2 "${W[@]}" 'runs-on:\s*\[?[^\n]*\bself-hosted\b' .
#  i. Every actions/checkout without `persist-credentials: false` — the default leaves the token in .git/config for later steps.
rg -l "${W[@]}" 'actions/checkout@' . | xargs -r awk 'function f() { if (c && !k) print cf ":" c ": checkout keeps its token in .git/config"; c = 0 } FNR == 1 { f() }
  /^ *[^ #]/ { match($0, /^ */); if (c && (RLENGTH < i || (RLENGTH == i && /^ *- /))) f() } /persist-credentials: *false/ { k = 1 }
  /uses: *actions\/checkout@/ { f(); c = FNR; cf = FILENAME; k = 0; match($0, /^ */); i = /^ *- / ? RLENGTH : RLENGTH - 2 } END { f() }'
#  j. Job containers, service images and `docker://` steps with no digest (a flow-map `container: { image: x }` is a read).
rg -n --pcre2 "${W[@]}" '^\s*(container|image)\s*:\s*[\x22\x27]?(?!\$\{\{)(?![^\n]*@sha256:)[\w./-]+(:[\w.-]+)?[\x22\x27]?\s*$|\buses\s*:\s*[\x22\x27]?docker://(?![^\n]*@sha256:)' .
G=(--hidden -g '.gitlab-ci.yml' -g '*.gitlab-ci.yml' -g '**/.gitlab/**/*.y*ml')
rg -n --pcre2 "${G[@]}" '\b(eval|sh\s+-c|bash\s+-c)\b[^\n]*\$\{?CI_(MERGE_REQUEST_\w+|COMMIT_(MESSAGE|TITLE|DESCRIPTION|BRANCH|REF_NAME|TAG_MESSAGE)|EXTERNAL_PULL_REQUEST_\w+)|\$\{?CI_(MERGE_REQUEST_(TITLE|DESCRIPTION|SOURCE_BRANCH_NAME)|COMMIT_(MESSAGE|TITLE|DESCRIPTION|BRANCH|REF_NAME))\b' .
rg -n --pcre2 "${G[@]}" '^\s*-?\s*(remote|project):|^\s*image:\s*[\x22\x27]?[^\s:@\x22\x27]+(:latest)?[\x22\x27]?\s*$|\becho\s+[\x22\x27]?\$\{?\w*(TOKEN|SECRET|PASSWORD|KEY)\w*' .

# 7. Edge config (§ 6) — nginx, Caddy, Apache, Traefik; every command also reads the blocks 1e extracted to "$SCAN/edge".
N=(--hidden -g '*.conf' -g '*.nginx' -g '*.conf.template' -g 'Caddyfile*' -g '*.caddy' -g '*.caddyfile' -g '.htaccess' -g 'traefik*.y*ml' -g 'traefik*.toml' -g '*compose*.y*ml' "${X[@]}" -g '!.git/**')
rg -n --pcre2 "${N[@]}" '^\s*(autoindex\s+on|server_tokens\s+on|ssl_protocols\s[^;]*\b(SSLv[23]|TLSv1(\.1)?)(?![.\d])|ssl_ciphers\s[^;]*(?<![!\w])(RC4|3?DES|MD5|EXPORT|NULL)\b|client_max_body_size\s+0\s*;|add_header\s+Access-Control-Allow-(Origin\s+[\x22\x27]?(\*|\$http_origin)|Credentials\s+[\x22\x27]?true)|file_server\s+browse|Options\s+[^\n]*(?<!-)\bIndexes|ServerTokens\s+(Full|OS)|ServerSignature\s+On|TraceEnable\s+On|SSLProtocol\s+[^\n]*\ball\b(?![^\n]*-TLSv1\b)|admin\s+[\d.]*0\.0\.0\.0:\d+)|--api\.insecure(=true)?|\binsecure:\s*true|exposedByDefault[:=]\s*true' . "$SCAN/edge"
rg -n -U --pcre2 "${N[@]}" 'location\s+[^\s{]*[^/\s{]\s*\{[^}]*?\balias\s+[^;]*/\s*;' . "$SCAN/edge"
rg -n --pcre2 "${N[@]}" '^\s*(proxy_pass|reverse_proxy)\s[^\n]*(127\.0\.0\.1|localhost|admin|internal|:(2019|8080|9000|9090|15672|5601|3000)\b)' . "$SCAN/edge"
rg -l --pcre2 "${N[@]}" 'listen\s[^;]*\b443\b|ssl_certificate\s' . "$SCAN/edge" | xargs -r rg --files-without-match 'Strict-Transport-Security'
#  e. Client-IP derivation, edge to app — what every per-IP throttle keys on (CDN → LB → proxy → app, one trusted hop each).
rg -n --pcre2 "${X[@]}" -g '!*.md' -g '!**/*.{test,spec}.*' -g '!**/{test,tests,__tests__}/**' 'trusted_proxies|client_ip_headers|real_ip_header|set_real_ip_from|use-forwarded-headers|compute-full-forwarded-for|enable-real-ip|forwarded-for-header|proxy-real-ip-cidr|use-proxy-protocol|\bproxy_protocol\b|externalTrafficPolicy|\btrust[_ ]proxy\b|trustProxy|TRUST_PROXY\w*|ProxyFix|FORWARDED_ALLOW_IPS|forwarded_allow_ips|KnownProxies|ForwardedHeaders|RemoteIpValve|CF-Connecting-IP|True-Client-IP' . "$SCAN/edge"
#  f. Shared state the edge holds a credential for (certificate storage) — compare its host and secret with the app's.
rg -n -A6 --pcre2 "${N[@]}" '^\s*storage\s+(redis|consul|postgres\w*|s3|dynamodb|etcd)\b' . "$SCAN/edge"
#     Then the manifests: a Secret an edge workload (Caddy, nginx, Traefik, Envoy, HAProxy, a gateway) reads that an app workload also reads.
rg -l --sort path --pcre2 "${K[@]}" '^\s*(-\s*)?(secretKeyRef|secretRef)\s*:|^\s*secretName\s*:' . "$SCAN" | xargs -r awk 'function f() { if (w != "") for (s in cur) { if (!index(us[s], " " w " ")) { us[s] = us[s] " " w " "; at[s] = at[s] " " cur[s]; n[s]++ } if (e) ed[s] = ed[s] " " w } split("", cur); w = ""; e = 0; k = 0; p = 0 }
  FNR == 1 || /^---/ { f() } /^kind: *(Deployment|StatefulSet|DaemonSet|Pod|Job|CronJob|ReplicaSet) *$/ { k = 1 }
  k && w == "" && /^  name: / { w = $2; gsub(/[\042\047]/, "", w); if (w ~ /caddy|nginx|traefik|envoy|haproxy|ingress|gateway|edge|proxy/) e = 1 }
  k && /^ +(- +)?image: / && /caddy|nginx|traefik|envoy|haproxy|ingress-controller|gateway/ { e = 1 }
  k && /secretName: / { x = $0; sub(/.*secretName: */, "", x); gsub(/[\042\047 ]/, "", x); cur[x] = FILENAME ":" FNR; next }
  k && /(secretKeyRef|secretRef): *\{/ { x = $0; sub(/.*name: */, "", x); sub(/[,} ].*/, "", x); gsub(/[\042\047]/, "", x); if (x != "") cur[x] = FILENAME ":" FNR; next }
  k && /(secretKeyRef|secretRef): *$/ { p = 1; next } p && /^ +name: / { x = $0; sub(/.*name: */, "", x); gsub(/[\042\047 ]/, "", x); cur[x] = FILENAME ":" FNR; p = 0; next }
  p && !/^ +(key|optional): / { p = 0 }
  END { f(); for (s in ed) if (n[s] > 1) { m = split(substr(at[s], 2), a, " "); for (i = 1; i <= m; i++) print a[i] ": Secret " s " read by edge" ed[s] " and by:" us[s] "-> one credential across trust zones" } }'
#     And by VALUE (runbook-created Secrets, names differ): datastore keys grouped by user across `create secret` blocks;
#     a password-only Redis/Valkey key is the `default` user. Two Secrets on one user → read each mount and the host.
rg -l --pcre2 -g '*.md' -g '*.sh' "${X[@]}" 'kubectl\b[^\n]*?\bcreate\s+secret\b' . | xargs -r awk '/kubectl[^#]*create +secret +[a-z-]+ +[^ \\]+/ { s = $0; sub(/.*create +secret +[a-z-]+ +/, "", s); sub(/[ \\`\042\047].*/, "", s); b = 1 }
  b { t = $0; while (match(t, /--from-literal=[A-Za-z0-9_.-]+=(\042[^\042]*\042|\047[^\047]*\047|[^ ]*)/)) { kv = substr(t, RSTART + 15, RLENGTH - 15); t = substr(t, RSTART + RLENGTH)
    k = kv; sub(/=.*/, "", k); v = substr(kv, length(k) + 2); f = ""
    if (k ~ /REDIS|VALKEY|CACHE|QUEUE|MEMCACHE/ || v ~ /rediss?:\/\//) f = "redis"; else if (k ~ /DATABASE|POSTGRES|PG_|MYSQL|MONGO|DSN/ || v ~ /(postgres(ql)?|mysql|mongodb(\+srv)?):\/\//) f = "db"; else if (k ~ /RABBIT|AMQP|NATS|KAFKA|BROKER/ || v ~ /amqps?:\/\//) f = "broker"
    if (f == "") continue; u = "?"
    if (match(v, /:\/\/[^\/@ ]*@/)) { u = substr(v, RSTART + 3, RLENGTH - 4); sub(/:.*/, "", u) } else if (k ~ /PASS(WORD)?/) u = (f == "redis" ? "default" : "?"); else if (v ~ /:\/\//) continue
    r = f " user " u; row[r] = row[r] "\n  " s " " k " " FILENAME ":" FNR; if (!index(sec[r], " " s " ")) { sec[r] = sec[r] " " s " "; n[r]++ } }
    if ($0 !~ /\\[ \t]*$/) b = 0 }
  END { for (r in n) if (n[r] > 1 && r !~ / [?]$/) print r " in " n[r] " Secrets -> one credential across trust zones?" row[r] }'
#  g. Snippet-enabled ingress-nginx: snippet annotations, and the controller flags that allow them (often only in a runbook).
rg -n --pcre2 "${X[@]}" -g '!*.md' 'nginx\.ingress\.kubernetes\.io/(server|configuration|stream)-snippet|allow-?[sS]nippet-?[aA]nnotations|annotations-risk-level' .
#  h. A shared cache that can serve one user's response to another (E4): a proxy cache switched on, response headers it is
#     told to ignore, a Caddy / Souin `cache` handler; the nginx files that cache with no `proxy_no_cache` / `proxy_cache_bypass`
#     anywhere; CDN cache behaviours (read which header and cookie the policy keys on).
rg -n --pcre2 "${N[@]}" '^\s*proxy_cache\s+(?!off\b)\w+|^\s*proxy_ignore_headers\s[^;]*\b(Set-Cookie|Cache-Control|Vary)\b|^\s*(cache|souin)\s*\{?\s*$' . "$SCAN/edge"
rg -l --pcre2 "${N[@]}" '^\s*proxy_cache\s+(?!off\b)\w+' . "$SCAN/edge" | xargs -r rg --files-without-match --pcre2 '^\s*proxy_(no_cache|cache_bypass)\s'
rg -n --pcre2 "${T[@]}" '\b(cache_policy_id|forwarded_values|query_string_cache_keys)\b' .

# 8. Env files that ship (§ 7).
git ls-files | rg --pcre2 '(^|/)\.env(\.(?!example$|sample$|template$|dist$|defaults$)[^/]+)?$'
rg -n --hidden --pcre2 -g '.env.example' -g '.env.sample' -g '.env.template' -g '.env.dist' -g '*.env.example' \
  '^\s*\w*(PASSWORD|SECRET|TOKEN|_KEY|DATABASE_URL|DSN|CONNECTION_STRING)\w*\s*=\s*(?![\x22\x27]{0,2}\s*$|[\x22\x27]?(<|your|change|xxx|example|dummy|placeholder|\$\{))\S+' .
rg -n -i --pcre2 -g 'Dockerfile*' -g '*.dockerfile' "${X[@]}" '^\s*(COPY|ADD)\s+(--\S+\s+)*\.\s' .; rg -n --hidden --pcre2 -g '.dockerignore' "${X[@]}" '^\s*(\*\*/|/)?\.env(\*|\.\*)?\s*$' . || echo "no .dockerignore entry for .env"
```

Every grep produces candidates only. A finding needs a hit plus a read of the enclosing block — the service's image, the resource's `from_port`, the step's trigger, the location's auth — to establish what it exposes.

## Scans for

Then the scanners. All output goes to the pre-flight's `$SCAN`, never into the repo:

```bash
checkov -d . --skip-path node_modules --skip-path vendor -o json -o sarif --output-file-path "$SCAN/checkov" --quiet --compact
trivy config --skip-dirs node_modules --skip-dirs vendor --format json --output "$SCAN/trivy-config.json" .
for f in $(rg --files . -g 'Dockerfile*' -g '*.dockerfile' -g '!**/node_modules/**'); do
  docker run --pull=never --rm -i "hadolint/hadolint:v2.15.1@$HADOLINT_DIGEST" hadolint -f json --failure-threshold warning - < "$f" > "$SCAN/hadolint-$(echo "$f" | tr '/' '_').json"; done
zizmor --offline --persona=auditor --format json .github/workflows > "$SCAN/zizmor.json" 2> "$SCAN/zizmor.err"; echo "zizmor exit $? (3 = no inputs → NOT-RUN)"
actionlint -format '{{json .}}' > "$SCAN/actionlint.json"
MANIFESTS=("$SCAN"/rendered-*.yaml)   # 1f's output; with nothing to render, the manifest dir
NGINX_CONF=nginx.conf           # each nginx config the repo ships — a copy in $SCAN with absolute `include`s rewritten to repo paths
kube-linter lint --add-all-built-in --exclude schema-validation --format json "${MANIFESTS[@]}" > "$SCAN/kube-linter.json"
gixy -f json "$NGINX_CONF" > "$SCAN/gixy.json"
semgrep scan --metrics=off --config p/dockerfile --config p/docker-compose --config p/kubernetes --config p/terraform \
  --config p/github-actions --config p/nginx --exclude node_modules --exclude vendor --json-output="$SCAN/semgrep-iac.json" > /dev/null
```

Each command above runs only when its binary is installed; absent → the ledger row reads `NOT-INSTALLED` with the "Install for later" command, and the greps still run. **The audit never downloads a scanner** (no `uvx`, `pipx run`, `npx -y`, or `docker pull`). A scanner image that is **already local** (`docker image inspect <image>` succeeds) may stand in for an absent binary, with `--pull=never`, fed through **stdin, not a bind mount** (§ False positives):
- trivy: `tar -cf - --exclude node_modules --exclude .git . | docker run --pull=never --rm -i --entrypoint sh "aquasec/trivy:0.75.0@$TRIVY_DIGEST" -c 'mkdir /src && tar -xf - -C /src && trivy config --quiet --format json /src' > "$SCAN/trivy-config.json"`.
- kube-linter: `docker run --pull=never --rm -i stackrox/kube-linter lint --add-all-built-in --exclude schema-validation --format json - < <file>`. The image has no shell; stdin works.
- actionlint: `docker run --pull=never --rm -i "rhysd/actionlint:1.7.12@$ACTIONLINT_DIGEST" -format '{{json .}}' - < <workflow>`, one file per run.

Scanners are supply chain too: the 2026-03 trivy-action compromise force-moved 76 of 77 tags. Every image above runs by version **and** digest, never `:latest`. Record each `*_DIGEST` once (`crane digest <image>:<version>`) in the ledger. A different digest under the same version is a stop, not an update. zizmor below 1.28 is refused (1.27.0 logged GitHub credentials, GHSA-f42p-wjw5-97qh).
- semgrep, checkov, zizmor, gixy-ng: no local stand-in; NOT-INSTALLED (`pipx install semgrep` / `pipx install checkov` / `brew install zizmor` / `pipx install gixy-ng`).

Read each output's file or target count before calling the row RAN. **A scanner that scanned 0 files is NOT-RUN, whatever its exit code.**

### 1. Dockerfile — what the shipped image runs as and carries

Flag: the **final** stage's effective user is root — `USER root` / `root:*` / `0` / `0:*`, set in it or inherited through `FROM <stage>` (grep 2a resolves the chain; a final `FROM builder` takes the builder's `USER`) — or it sets none over an external base (`INHERIT-EXTERNAL`: `crane config <ref> | jq -r .config.User` settles it); a secret-named `ARG` / `ENV` (both persist in the image config and history); `COPY` / `ADD` of `.env`, keys, `.npmrc`, `.netrc`; `ADD https://…` or `curl … | sh` (code fetched with no integrity check); an untagged or `:latest` base. `HEALTHCHECK` is ops — skip it.

```
BAD:   FROM node:22 AS build
       USER node                       # builder only
       FROM node:22-slim               # final stage: no USER → root
       ARG NPM_TOKEN                   # recoverable from the image config
       COPY . .                        # .env rides along: no .dockerignore entry
GOOD:  FROM node:22.11-slim@sha256:<digest>
       RUN --mount=type=secret,id=npm_token NPM_TOKEN="$(cat /run/secrets/npm_token)" npm ci
       COPY --chown=node:node dist/ ./dist/
       USER node                       # after the LAST FROM
```
**Unpinned build-time module fetches** are the same class as `curl | sh`, and no scanner flags them. Examples: `xcaddy build --with <module>` with no `@version`, `go install …@latest`, and `npm i -g <pkg>` with no version. Each compiles whatever upstream published last into the shipped binary. That matters most for an edge proxy, which sees every request in plaintext and holds the DNS and storage credentials. The Go checksum database guarantees everyone gets the same bytes, not that the bytes are benign. Fix: `--with <module>@vX.Y.Z`, or a vendored `go.mod`/`go.sum` built with `GOFLAGS=-mod=readonly`. **Before rating a root final stage high**, read the base image's own user (`docker image inspect -f '{{.Config.User}}' <base>`, or the vendor's docs). `nginx-unprivileged` runs as 101. Also read the pod's `runAsUser` / `runAsNonRoot`, since either one mitigates it.

Severity: secret file or secret build-arg in a pushed image **critical** (hand the value to `secret-scan-method`); root final stage **high** (mitigated by the base's `USER` or the pod's securityContext → hardening); `curl | sh`, `bash <(curl …)` / `ADD` URL **high**; unpinned build-time module into an internet-facing binary **medium**; floating base **medium**. A02 / A08:2025 · CWE-250, 522, 538, 494, 829.

When the devops pack is installed, also dispatch its `container-build-scan` skill (stage chain, PID 1, lockfile, HEALTHCHECK, `--check`/hadolint lane, `docker history`) and `release-security` (image CVEs, SBOM, signature). Without it, this detector reports the Dockerfile only, and the ledger says `built image: not scanned`.

### 2. Compose — what the host exposes and hands to containers

Flag: a published port with no `127.0.0.1:` host IP on a database, cache, queue, search or admin UI (read the service's `image:`); `privileged: true`; `/var/run/docker.sock` mounted (root on the host); `network_mode` / `pid` / `ipc: host`; `cap_add`; a literal or default password (`POSTGRES_PASSWORD: postgres`, `HOST_AUTH_METHOD=trust`, `ALLOW_EMPTY_PASSWORD`). Missing resource limits are ops — skip.

```
BAD:   db:    { image: postgres:16, ports: ["5432:5432"], environment: { POSTGRES_PASSWORD: postgres } }
       api:   { volumes: ["/var/run/docker.sock:/var/run/docker.sock"] }
GOOD:  db:    { image: postgres:16, expose: ["5432"], environment: { POSTGRES_PASSWORD_FILE: /run/secrets/db_pw }, secrets: [db_pw] }
       admin: { ports: ["127.0.0.1:5050:80"] }          # loopback only; reach it over SSH / VPN
```
Docker's published ports are inserted ahead of the host firewall's rules, so `ufw deny 5432` does not close `"5432:5432"`. Severity: docker.sock or privileged **critical**; DB/admin port on all interfaces **high**, **critical** with a default password on it. **Dev-only stacks** (a compose file or kind config that only developers run, holding no production data) drop one level: **high** with a default password, **medium** without. They stay Unconfirmed until a probe from a second host on the LAN connects. The same rule covers a kind `extraPortMappings` entry with no `listenAddress: 127.0.0.1`. A02 / A07:2025 · CWE-668, 250, 1393.

### 3. Kubernetes — pod privilege, secrets in manifests, exposure, RBAC

Flag on the **rendered** manifests: `privileged`, `allowPrivilegeEscalation: true`, `runAsUser: 0` or no `runAsNonRoot: true`, `hostPath`, `hostNetwork` / `hostPID` / `hostIPC`, added capabilities (`SYS_ADMIN`, `NET_ADMIN`, `ALL`), `readOnlyRootFilesystem: false`. Flag a secret-named env var with a literal `value:`, and a committed `kind: Secret` with `data` / `stringData` — base64 is encoding, not encryption. Flag no `NetworkPolicy` anywhere, a `LoadBalancer` / `NodePort` Service in front of an internal, admin or database workload, a dashboard Ingress (Grafana, Kibana, Argo CD, pgAdmin …) with no auth annotation or middleware, and RBAC `*` in `verbs` / `resources` / `apiGroups` or a `cluster-admin` binding.

```
BAD:   securityContext: { privileged: true, runAsUser: 0 }
       env: [{ name: DB_PASSWORD, value: "hunter2" }]
       kind: Service · type: LoadBalancer · name: internal-admin
GOOD:  securityContext: { runAsNonRoot: true, allowPrivilegeEscalation: false, readOnlyRootFilesystem: true,
                          capabilities: { drop: ["ALL"] }, seccompProfile: { type: RuntimeDefault } }
       env: [{ name: DB_PASSWORD, valueFrom: { secretKeyRef: { name: db, key: password } } }]   # Secret from ESO / Sealed Secrets, not git
       type: ClusterIP, reached through an authenticated Ingress
```
Severity: privileged, `hostPath: /`, `hostPID`, cluster-admin to a workload, or an unauthenticated admin Ingress **critical**; plain secret in git, internal Service on a LoadBalancer, RBAC wildcard **high**; no NetworkPolicy, capabilities, writable root FS **medium**. A01 / A02:2025 · CWE-250, 269, 306, 312, 668.

**Blast radius: what one compromised pod or token reaches.** No scanner reports these. Read greps 4j–4m and 7f:
- **Deploy by mutable tag** (4j): an `image:` or kustomize `newTag:` with no `@sha256:` digest. Whoever can re-push that tag replaces what the next node pull runs (autoscale, node replacement, `rollout restart`). That includes any default-branch workflow, a third-party action inside it (§ 5), and any `packages: write` token. Fix: kustomize `digest:`, filled by CI from the build step's digest output; keep the sha as a label. The registry form is grep 5g: a repository whose tags can be overwritten (ECR `MUTABLE`, the default when the attribute is absent) lets a re-push replace even a tag nobody moves on purpose; fix: `IMMUTABLE`.
- **A NetworkPolicy rule wider than its comment** (4k). Peers with no `ports:` reach every port of the selected pods. `ports:` with no `from:` opens that port to every source, which bypasses the edge's rate limit and path blocks. Grep 4n adds width: an `ipBlock` of /20 or wider is usually the whole VPC, the node range, an RFC 1918 block or the VPN, and it admits every pod and host in it **whether or not the rule names ports** (read the `except:` list and what the CIDR is). No policy governs a pod's own loopback ([`finding-verification.md`](../../../../snippets/finding-verification.md) § 4 NET1–NET2). Fix: a namespace or pod selector for the real client, plus its port. Add an observability backend with auth off (4l: Loki `auth_enabled: false`, the Prometheus admin API, anonymous Grafana), and a peer reads every log line and can silence alerts.
- **One credential across trust zones** (7f, then read). The internet-facing edge holds the password of the app's cache or queue, for example certificate storage in the app's Redis with no storage encryption key. Edge code execution then writes the app's auth state (permission cache, OTPs, session revocations). App code execution reads every private key the edge stored. The manifest half is 7f's join: a Secret an edge workload reads that an app workload also reads (the same Valkey, Redis or RabbitMQ user on both sides of the trust boundary). Secrets created by a runbook usually carry different names, so the name join stays silent: 7f's value join groups each `--from-literal` datastore key by its user (a password-only Redis or Valkey key is the `default` user) and prints a user that appears in two Secrets. Trace each key to its source line (the `doctl databases connection … Password`, the `user:…@host` URL), confirm the same datastore host, then read which workload mounts each Secret. Fix: a separate store, or an ACL user scoped to the edge's key prefix in its own Secret, plus the storage backend's encryption key.
- **Migrations run as the runtime DB role** (4m). Compare the migration Job's credential with the Deployment's. When they match, the request-serving role owns every table and can run `ALTER TABLE … NO FORCE ROW LEVEL SECURITY` or `DROP POLICY`, so RLS stops being a backstop against SQL execution. A backup Job holding the admin credential when a read-only role suffices is the same defect. Fix: an owner role for migrations only, DML grants for the runtime role, and one secret per Job holding only its `DATABASE_URL`.

**Unrendered.** When 1f prints `NOT-RENDERED` (no kubectl, no kustomize), 4b, 4j, 4k and 7f see only the source tree, and a field an overlay sets or removes is invisible. Apply each overlay's `patches:` / `images:` entries to its base by hand for the workloads those greps name, and mark those four rows `partial (unrendered)` in the coverage block, never clean.

Chain severity: each of these is **medium** alone. Raise it to **high** when the same report has a reachable way in. That can be an internet-facing tier built from unpinned code (§ 1, § 5), a CI job that can push the deployed tag, or a pod with no egress policy. Name the chain in both rows.

When the infrastructure pack is installed, dispatch `@k8s-reviewer` for the full manifest review and the `admission-policy` skill to enforce these fields at admission. Without it, this detector covers the security fields above and the ledger says `manifest review: security fields only`.

### 4. Terraform / CloudFormation / Pulumi — cloud exposure and privilege

Flag: public object storage (S3 `public-read` ACL or public-access-block `false`, GCS `allUsers` / `allAuthenticatedUsers`, Azure `container_access_type` blob/container); ingress from `0.0.0.0/0` / `::/0` to SSH, RDP, a database, cache or admin port (read `from_port` / `to_port` — 80/443 on a public load balancer is intended); a publicly accessible database; IAM `Action "*"` / `service:*` / `Resource "*"` / `NotAction`, GCP `roles/owner|editor`, Azure `Owner` / `Contributor` on an app identity; unencrypted storage or a TLS floor below 1.2; IMDSv1 (`http_tokens = "optional"`); a literal password in `.tf` / `.tfvars`; a container registry with mutable tags (5g, the registry form of § 3's 4j); **dangling DNS** (5h, D1): a CNAME, alias or record whose literal target is a third-party name (an S3 website bucket, a Heroku app, an Azure site, GitHub Pages) that nothing in the repo declares, so whoever claims that name serves the subdomain. Read whether the target is a resource reference whose lifecycle the record follows; a literal CloudFront or ELB target is not claimable. Severity **high** (cookies scoped to the parent domain, phishing on a trusted name); `/security-live-scan` settles it with `dig` and the target's NXDOMAIN / `NoSuchBucket`. When the infrastructure pack is installed, `dns-tls-lifecycle-scan` § 7 defers to this row.

```
BAD:   resource "aws_security_group" "db" { ingress { from_port = 5432, to_port = 5432, cidr_blocks = ["0.0.0.0/0"] } }
       policy = jsonencode({ Statement = [{ Effect = "Allow", Action = "*", Resource = "*" }] })
       metadata_options { http_tokens = "optional" }
GOOD:  ingress { from_port = 5432, to_port = 5432, security_groups = [aws_security_group.app.id] }
       Action = ["s3:GetObject"], Resource = ["${aws_s3_bucket.uploads.arn}/*"]
       metadata_options { http_tokens = "required", http_put_response_hop_limit = 1 }
```
IMDSv1 is the SSRF amplifier — when `ssrf-scan` § 6 has any user-URL fetch on that instance, raise it to **critical**. Severity otherwise: public bucket holding user data or world-open DB port **critical**; `*:*` IAM, public RDS, SSH from anywhere **high**; unencrypted storage, TLS floor **medium**. A01 / A02 / A04:2025 · CWE-732, 284, 269, 311, 326, 798.

**Bucket policies and storage keys.** A standalone policy JSON with `"Principal": "*"` (grep 5a) makes the bucket public even with no Terraform. Map its `Resource` prefix to what the app writes under it by reading the storage module's key layout. A "public assets" prefix that also holds chat media or legacy uploads is serving user data. Also flag DB dumps written to the app's own bucket (compare 4m's backup target with the app's bucket). And flag an app key that can change bucket policy; a runbook that applies policies with the app's key proves it. App code execution then reads every tenant's dump, or makes `private/` public. Fix: backups in their own bucket with a key only the backup Job holds; a limited-access app key with no policy rights; policies applied with an operator key. Severity **medium**, chained per § 3.

**No IaC.** When grep 1 finds no Terraform, Pulumi or CloudFormation, the provisioning runbook is the plan (1g). Read which key applies policies, the firewall rules, `--from-literal` secrets (they land in shell history), and which cluster each credential points at. **Helm values for upstream charts** with no vendored chart: diff each values file against `helm show values <chart>` for auth, password and service-type defaults.

Pulumi programs are code — grep 5c reads them; when a stack is configured, `pulumi preview --json` is the plan to read. When the infrastructure pack is installed, dispatch `/audit-iam` for usage-based IAM analysis (dead permissions, entitlement chains), `tf-plan-review` for the pre-apply plan and `network-exposure-audit` for the running footprint. Without it, these findings stand on the declared code alone.

### 5. CI workflows — dispatched to `ci-security-scan`

Every CI attacker-path class on GitHub Actions, GitLab CI, CircleCI, Bitbucket, Azure Pipelines and Jenkins belongs to the security pack's [`ci-security-scan`](../ci-security-scan/SKILL.md) skill. That covers a privileged trigger running untrusted code, expression injection, AI agents in CI, pinning × privilege, cache and artifact trust, credentials and OIDC, gates, and runners. Dispatch it whenever grep 1 finds a CI file. Grep 6 here is its candidate list:
- 6a / 6b: privileged triggers and every PR-code checkout form;
- 6c: one tainted expression per line, the bracket form included;
- 6e: every write scope;
- 6j: images with no digest.

That skill owns the severity (reach × the job's capability), the `ci-graph.py --check=pin-priv` join, the tool ledger and the § 4 CI precedents of [`finding-verification.md`](../../../../snippets/finding-verification.md). This detector's coverage row is that skill's class-coverage block. A CI hit is never rated here.

### 6. Edge config — nginx, Caddy, Apache, Traefik

Flag:
- Protocols below TLS 1.2 or weak ciphers (RC4, 3DES, NULL, EXPORT, MD5).
- A 443 server with no `Strict-Transport-Security`. An `add_header` inside a `location` drops every server-level `add_header`, so headers set once at the top can vanish on exactly the routes that matter.
- `autoindex on`, Caddy `file_server browse`, Apache `Options Indexes`.
- `server_tokens on`, `ServerTokens Full`, `ServerSignature On`.
- The alias traversal: a `location /x` with no trailing slash over an `alias /y/;` that has one, so `/x../` walks out of `/y/`.
- `proxy_pass` / `reverse_proxy` to an internal admin, metrics or management port with no `auth_basic`, `auth_request`, `allow`/`deny`, `basicauth` or `forward_auth`.
- `client_max_body_size 0` (unlimited). Absent means nginx's 1 MiB default, which is not a finding; check that upload routes raise it in their own `location`.
- `Access-Control-Allow-Origin *` with `Allow-Credentials true`. Browsers refuse that pair, and the usual "fix" is to reflect `$http_origin`, which is the real hole.
- Traefik `api.insecure` / an unauthenticated dashboard / `exposedByDefault: true`, and Caddy `admin 0.0.0.0:<port>`.
- **Snippet-enabled ingress-nginx** (7g). With `allowSnippetAnnotations=true` and `annotations-risk-level=Critical`, anyone who can create an Ingress in any namespace can inject nginx config. That config can read the controller's ServiceAccount token, which lists Secrets cluster-wide (CVE-2021-25742, CVE-2023-5044). An admission webhook reachable from every pod is the CVE-2025-1974 class. The Kubernetes project has retired ingress-nginx (best-effort maintenance ended March 2026). Fix: move the snippet logic into the edge proxy and drop snippets; meanwhile, a NetworkPolicy admitting only the API server to the admission port.
- **A shared cache serving one user's response to another** (7h, E4). An nginx `proxy_cache` on an authenticated route (`/me`, `/account`, an API that reads `Authorization` or a session cookie) with no `proxy_no_cache` / `proxy_cache_bypass` on those headers, `proxy_ignore_headers Set-Cookie Cache-Control` (the upstream's `private` / `no-store` is thrown away), a Caddy or Souin `cache` handler in front of an account route, or a CDN behaviour whose cache policy keys on neither the auth header nor the session cookie. The next caller gets the previous caller's profile. **Read:** which route the cache sits on, whether the upstream answers per identity, and what the key holds. Severity **high**; **critical** for tokens or payment data. Fix: no shared cache on authenticated routes, or bypass and no-store on the identity headers. Proof (the settling run): two identities request the same URL through the edge in turn, and the second response must not carry the first one's data; until it runs, the row is `[report-flagged]`. When the infrastructure pack is installed, `edge-reliability-scan` § 4 defers to this row.
- **Client-IP derivation behind a CDN** (7e). Every per-IP throttle keys on it. Behind a CDN, three values are the CDN's egress address: the proxy's `remote_host`, the `X-Forwarded-For` it forwards, and the app's `req.ip`. That holds unless the proxy trusts the CDN's ranges and reads its header (Caddy `trusted_proxies` + `client_ip_headers`; nginx `set_real_ip_from` + `real_ip_header`), and the app trusts exactly the hops in front of it. Otherwise an attacker spreads a login brute-force across egress IPs, and one noisy client locks out everyone behind the same PoP. A PROXY-protocol `allow` range wider than the load balancer lets any pod claim any client IP. Severity **medium**.

Edge config embedded in YAML (a Caddyfile in a ConfigMap, a `server-snippet` annotation) is invisible to grep 7's file globs, and a run that skips it reports "Caddy N/A". Grep 1e copies each block to `$SCAN/edge` with the source's line numbers. A hit at `$SCAN/edge/deploy__k8s__edge.yaml.conf:88` is `deploy/k8s/edge.yaml:88`.

```
BAD:   location /static { alias /var/www/static/; }          # GET /static../app/.env
       location /admin/ { proxy_pass http://127.0.0.1:9000/; }
GOOD:  location /static/ { alias /var/www/static/; }
       location /admin/ { auth_request /_oauth; allow 10.0.0.0/8; deny all; proxy_pass http://127.0.0.1:9000/; }
```
Severity: alias traversal, unauthenticated admin proxy, Caddy admin API exposed **critical**; TLS < 1.2, reflected-origin CORS with credentials, directory listing over app files **high**; missing HSTS / headers **medium**; version disclosure **low**. A01 / A02 / A04:2025 · CWE-22, 306, 326, 942, 548, 319, 200.

The deployed edge can differ from the repo. `/security-live-scan` checks what the running host actually serves. When the infrastructure pack is installed, its `network-exposure-audit` skill covers the load balancer and firewall layer.

### 7. Env files that ship

Flag: a real `.env` tracked by git (it is in every clone and every fork); an `.env.example` holding real hosts or credentials; an image that carries `.env` (`COPY .env`, or `COPY . .` with no `.dockerignore` entry); a web root or static mount that contains it.

```
BAD:   git ls-files → .env                           .env.example: DATABASE_URL=postgres://app:realpass@prod-db.internal/app
GOOD:  .env in .gitignore and .dockerignore          .env.example: DATABASE_URL=postgres://user:<password>@localhost:5432/app
```
Severity: tracked `.env` with live values **critical** — `secret-scan-method` owns the value and the rotation; an example file with real values **high**; image-carried `.env` **critical** (`release-security` for the published image when the devops pack is installed). A `.env` reachable over HTTP is `data-exposure-scan`'s exposed-file finding — dispatch it. A02:2025 · CWE-538, 312.

### Triage of scanner hits

Each scanner hit lands as one of: a **finding** (merged into the detector above whose class it is, deduped by `<file:line>`, carrying both rule ids); `ops — out of scope`; or a **false positive with a cited reason** (intended public listener, a value from a secrets manager, a chart value overridden in the env's values file at `<file:line>`). Every suppression comment or ignore-file entry above is listed for `/security-audit` § Phase 6 — Validate with the triage of the hit it hides.

## Output

```
iac-scan — <repo>@<sha>          scratch: /tmp/iac-scan.Q7x2 (outside the repo)

Tool ledger
  checkov 3.3.21        RAN            exit 1 · 12 files · terraform, kubernetes, dockerfile, github_actions · 91 failed → 64 ops, 18 merged, 9 FP
  trivy config 0.74.0   RAN            exit 0 · 7 targets · 65 misconfigs → 38 ops, 27 merged
  hadolint 2.15.1       RAN            2 Dockerfiles · 7 hits → 2 merged
  zizmor 1.30.1         RAN            exit 14 · --persona=auditor · 2 workflows parsed of 2 · 15 hits → 6 merged
  kube-linter 0.8.3     RAN            --add-all-built-in · rendered chart · 27 hits → 8 merged
  gixy-ng 0.2.55        RAN            1 nginx config · 6 hits → 5 merged
  actionlint            NOT-INSTALLED  blocked — brew install actionlint  (or docker pull the pinned rhysd/actionlint:1.7.12 image; it then runs locally on stdin)

Findings: 6

1. deploy/nginx/site.conf:10                         critical  [report-with-fix]
   location /static (no trailing slash) + alias /var/www/static/; → GET /static../app/.env reads outside the root.
   gixy alias_traversal · A01:2025 · CWE-22
   Fix: `location /static/ { alias /var/www/static/; }`.

2. .github/workflows/pr.yml:3,12,19                  critical  [report-with-fix]
   pull_request_target + checkout of github.event.pull_request.head.sha + `npm ci && npm test` → fork PR code runs
   with write-all token and repo secrets. zizmor dangerous-triggers, semgrep pull-request-target-code-checkout · A08:2025 · CWE-829
   Fix: trigger on pull_request; if a privileged step is needed, split it into a workflow_run job that never executes PR code.

3. docker-compose.yml:14,12                          critical  [report-with-fix]
   db publishes "5432:5432" on all interfaces with POSTGRES_PASSWORD: postgres. Docker's rules bypass ufw.
   grep 3 (no scanner reads compose without `version:`) · A07:2025 · CWE-1393, 668
   Fix: drop `ports:` (use `expose:`) or bind 127.0.0.1; password from a compose secret.

4. Dockerfile.worker:6                               high      [report-with-fix]
   final stage (FROM line 4) has no USER — `USER app` (line 2) belongs to the build stage; CMD runs as root.
   hadolint, checkov and trivy all passed it.
   grep 2 · A02:2025 · CWE-250      Fix: `USER app` after the last FROM (create the user in that stage).

5. k8s/api.yaml:53         kind: Secret data.key     high      [report-with-fix]
   committed Secret; base64 only. Value → secret-scan-method (rotate first).   A02:2025 · CWE-312
   Fix: External Secrets / Sealed Secrets; remove from git history after rotation.

6. infra/main.tf:51  aws_instance.web                high      [report-flagged]
   metadata_options.http_tokens = "optional" (IMDSv1). No user-URL fetch found on this host by ssrf-scan → stays high.
   checkov CKV_AWS_79, trivy AWS-0028 · A01:2025 · CWE-918      Fix: http_tokens = "required", hop limit 1.

Suppressions: 1 — infra/main.tf:57 `#checkov:skip=CKV_AWS_3:legacy volume` hides encrypted = false on aws_ebs_volume.data.

Class coverage
  ### 1 Dockerfile        checked (9 hits → 3 findings)
  ### 2 Compose           checked (7 hits → 2 findings)
  ### 3 Kubernetes        checked (14 hits → 5 findings)
  ### 4 Terraform/CFN     checked (19 hits → 6 findings); Pulumi N/A (no Pulumi.yaml)
  ### 5 CI workflows      checked (11 hits → 4 findings) — actionlint blocked (not installed)
  ### 6 Edge config       checked (10 hits → 5 findings); Apache/Traefik N/A (no config files)
  ### 7 Env files         checked (3 hits → 2 findings)
```

## False positives / gotchas

Measured on the sample described in § Premise:

- **Three scanners read the wrong stage.** hadolint's root check fires only on an explicit `USER root`; checkov's `CKV_DOCKER_3` and trivy's `DS-0002` pass a multi-stage file whose only `USER` is in the builder. Grep 2's awk is the check of record.
- **semgrep `p/docker-compose` matches only files with a top-level `version:` key.** The Compose Specification made that key obsolete, so a modern compose file scans clean. Checkov and trivy do not read compose at all.
- **"World-open port" checks are SSH/RDP-shaped.** checkov `CKV_AWS_24` and trivy `AWS-0107` cover 22/3389; `0.0.0.0/0` on 5432 or 3306 passed both. Read every `cidr_blocks` hit's port range.
- **A parse error or an empty input is NOT-RUN, never a pass.** hadolint 2.15.1 skips a whole file on one line it cannot parse, reporting one `DL1000` and nothing else: an `EXPOSE ip:port:port`, or a heredoc terminator followed directly by the next instruction (a blank line after `EOF` parses). A `DL1000` makes that file NOT-RUN, never clean. `docker build --check` (when a run uses it) applies only the rules of the frontend the file's `# syntax=` line names: `docker/dockerfile:1.6`–`1.8` miss `SecretsUsedInArgOrEnv`, which `1.10` and the bundled frontend run — print the frontend beside the result (devops `container-build-scan` § Tool lane and ledger, measured 2026-10-10). zizmor exit 3 means no inputs were collected; `--format=sarif` and `--no-exit-codes` force exit 0. hadolint's default `info` threshold buries the signal; the commands carry `--failure-threshold warning`.
- **zizmor's default persona hides findings.** `self-hosted-runner`, `excessive-permissions` on `write-all` and secret interpolation surfaced only with `--persona=auditor`. A workflow it cannot parse is skipped with a `WARN … failed to parse input` on stderr while the other files still produce results — read `zizmor.err` and count parsed files. Exit codes 11–14 mean findings at that maximum severity, not a crash.
- **kube-linter's defaults omit `wildcard-in-rules`, `exposed-services` and `non-isolated-pod`.** `--add-all-built-in` turns them on, along with label and ordering noise (`required-label-owner`, `sorted-keys`) to triage as ops. Offline, it also emits one `schema-validation` error per object, which is why the commands above carry `--exclude schema-validation` (88 → 63 reports on a 25-object render).
- **kubescape with no path argument scans the cluster in your current kube context**, not the repo. Always pass the path, and `--keep-local`.
- **Helm templates are not manifests.** Grep and scan the `helm template` output with the environment's values file. A field set only in `values-prod.yaml` is invisible in the chart source.
- **Docker one-shots can scan nothing, and exit 0.** Measured 2026-10-02 on macOS Docker Desktop, trivy 0.74.0, `-v "$PWD:/src:ro"` from a `/private/tmp` checkout: it logged `Detected config files num=0`, returned 0 targets and exited 0. The same tree piped in as a tarball gave 2 targets and 17 failures. Feed containers through stdin (§ Scans one-shots), or mount a directory Docker shares, and read the target count. A scanner that scanned 0 files is **NOT-RUN**.
- **checkov `--framework github_actions` can parse nothing.** 3.3.21 read 0 resources from a valid 350-line workflow, with both `-d` and `-f`, and reported `passed 0 failed 0`. A GHA run with a resource count of 0 is NOT-RUN; zizmor and actionlint are the lane.
- **gixy-ng silently skips an absolute `include`** (`include /etc/nginx/conf.d/…` logs only a WARNING), so its `add_header` analysis runs without the headers file. Copy the config to `$SCAN` with each include rewritten to its repo path, and scan the copy.
- **gixy-ng has `--fix`, and it rewrites the config in place.** Never pass it here.
- **checkov's raw count is mostly ops.** On the sample, 42 Terraform failures across 9 resources were largely logging, versioning, replication and Multi-AZ. Report the triaged set, not the raw number.
- **The final-stage awk was wrong both ways** until grep 2a resolved the stage chain. It reported ROOT for a final `FROM base` whose `USER node` sat in `base`, and it passed `USER 0:0` and `USER root:root`. Measured 2026-10-10 on nine cases (no USER, builder-only USER, an inherited non-root USER, an inherited `root`, `0:0`, `root:root`, `USER ${ARG}`, numeric non-root, a mixed-case stage name): 9 of 9 correct. The seeded `vuln-fullstack` root image still prints at its `CMD` line, and a real repo's edge image prints `INHERIT-EXTERNAL` for its `caddy:${RUNTIME_TAG}` base, as before.
- **Measured: grep 6 against the old greps** (a seeded six-platform CI sample, 2026-10-10). 6c keeps 10 of 10 injection seeds, including the bracket form, where the old grep missed 5. 6b finds 8 of 8 PR-code checkouts, where the old one found 2. 6e finds 15 write-scope lines, including a flow-map block, where the old one found 10. 6j finds 3 of 3 undigested images, and neither digest decoy.
- **Measured: greps 4n, 5g, 5h, 7f's join and 7h, and `*.caddy` in the edge globs** (2026-10-10, ripgrep 15.2.0, `/bin/bash` 3.2.57, the pre-flight copied verbatim into staged copies of `benchmarks/fixtures/infra-ops` and `vuln-fullstack`). On `infra-ops` the security rows printed went from 4 of 12 to **12 of 12**: 4n both ipBlocks (`10.40.0.0/16` with no ports, `10.0.0.0/8` with ports; one line per render as well), 5g the ECR `MUTABLE` repository (its `IMMUTABLE` sibling and the absent-attribute awk stay quiet), 5h the S3-website and Heroku records (the CloudFront CNAME decoy is not printed), 7f the Caddy `storage redis` block in an imported `shop.caddy` (unread while the globs knew only `Caddyfile*`) and the join's two `valkey-app` sites, 7h the nginx `/api/me` cache (and its file, which has no bypass) and the Caddy `cache` handler. New unseeded lines: 1 (a CloudFront `cache_policy_id`, read as context). `vuln-fullstack`: the same 37 lines as before; every seeded IaC and CI defect still prints.
- **`0.0.0.0/0` on 80/443 of a public load balancer, and a `LoadBalancer` Service for the public ingress controller, are intended.** Note them, do not file them.
- **Measured on a real NestJS + React monorepo** (2026-10-15): its runbooks create every Secret with `kubectl -n <ns> create secret … \` and one `--from-literal` per continuation line. The old 1g matched none of the 8 commands (it needed `create` right after `kubectl` and the literal on the same line); the `-U` form prints all 8 with their keys. The value join prints one group: the cache's `default` user in 3 Secrets (the app's `REDIS_URL`, the edge's certificate-storage password and an exporter's), which the name join missed because the three names differ. 1f rendered 3 Kustomize dirs offline with an empty kubeconfig. Fixtures: 1g 1 → 1, the value join 0; after seeding `infra-ops` (IO-SEC-FLa, IO-SEC-VKc and decoys IO-DECOY-33/34, 2026-10-15) 1g prints the seed block and not the `--from-file` decoy, and the value join prints one group (`api-sessions` + `traefik-ratelimit`) and not the decoy. Grep 4k flushes a rule pending at a file's end under that file's own name (it was printed under the next file's name when `rg -l` order changed).
- **Measured on a real repo** (Kustomize base + one overlay, a Caddy edge in a ConfigMap, GitHub Actions; 2026-10). The old greps saw none of the Caddy edge or the ingress snippet: 0 files, so § 6 would have read "Caddy N/A". Grep 1e now extracts 2 embedded configs. Its storage backend appears only in the extracted copy, and 7a–7d read it too. On source, 4b flagged 7 files, 5 of them kustomize patches. Per document, on the render plus non-patch manifests, it flags 3 workloads, all local-dev. Grep 8c's false "no .dockerignore entry" is gone. 8b went from 5 hits to 1 (the four `KEY=""` lines). New detectors on the same repo: 2e went from 0 to 2 (`bash <(curl …)` in CI and a release script); 2g found 3 (unpinned `xcaddy --with`), 4j 13, 4k 2 rules (+2 rendered copies), 4l 2, 4m 8, 5a 1 (`"Principal": "*"`), and 6i 5 checkouts (zizmor `artipacked` found the same 5). The seeded IaC and CI defects in `benchmarks/fixtures/vuln-fullstack` are all still hit.

## When to run

- On any diff touching a Dockerfile, compose file, Kubernetes manifest or chart, Terraform / CloudFormation / Pulumi, a CI workflow, a reverse-proxy config or an `.env*` file. `/security-audit` § Phase 2 — Organize dispatches it on that signal, and on every whole-repo run that holds any of them.
- Before the first deploy of a new service, before making a repo public (self-hosted runners, tracked `.env`), and after any change to a scanner's ignore file.

## Halt conditions

- Do not report a critical or high row as confirmed until a verifier other than the run that found it has passed it through [`finding-verification.md`](../../../../snippets/finding-verification.md). Under `/security-audit` that happens in Phase 4; run standalone, it applies the protocol as a separate second pass, tags those rows `self-verified`, and lists the rest as Unconfirmed, Hardening or Refuted — never drops them.
- Halt on a finding without `<file:line>` (plus the field path for a manifest), the failing condition, what it exposes, the fix and a severity.
- Halt on a ledger that omits a surface grep 1 found, or that marks a scanner RAN without its file count. A scanner that read zero files did not run.
- Do not report a scanner rule id as a finding before reading the block. Do not file ops-only checks as security findings.
- Do not run any tool that writes into the repo (`gixy --fix`, `checkov --download-external-modules` into the tree, `helm dependency update`) without asking. Do not install globally without asking. Do not write scan output inside the repo.
- Do not rotate, scrub or print a secret value — hand it to `secret-scan-method`.

## Related

- `/security-audit` — dispatches this skill in § Phase 2 — Organize; its § Class coverage ledger takes this skill's coverage block as the "Container, orchestration, cloud IAM, CI, reverse-proxy config" row, and § Phase 6 — Validate rates the suppression list.
- `sast-scan` — owns semgrep on application code; this skill runs the IaC rulesets. `secret-scan-method` — owns every secret value and its rotation. `ssrf-scan` — § 6 there is the code half of the IMDSv1 finding. `data-exposure-scan` — an `.env` or backup reachable over HTTP.
- `/security-live-scan` — what the running edge actually serves (TLS handshake, headers, exposed paths); this skill reads the config that should produce it.
- `ci-security-scan` (same pack) — every CI attacker-path class on six platforms (§ 5). devops pack, when installed — `container-build-scan` and `release-security` (§ 1, § 7); `@ci-reviewer` judges delivery-integrity rows through `ci-security-scan`'s boundary.
- infrastructure pack, when installed — `@k8s-reviewer` and `admission-policy` (§ 3); `/audit-iam`, `tf-plan-review` and `network-exposure-audit` (§ 4, § 6).
- `@security-auditor` — its A02 rows (S3 public, `hostNetwork`, privileged containers) are the surface pass this skill executes; its A03 build-integrity row is `release-security`'s.
