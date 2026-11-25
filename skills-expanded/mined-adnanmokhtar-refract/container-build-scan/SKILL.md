---
name: container-build-scan
description: "Dockerfiles that build green and fail later: PID 1, stage-chain user, cache order, lockfile, healthcheck, size."
kind: skill
pack: devops
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: container-build-scan

## Premise

A Dockerfile that builds is not a Dockerfile that ships correctly. These all build green; each was measured on 2026-10-10 (docker engine 29.5.2, buildx 0.37.1, hadolint 2.15.1):
- a `RUN <<EOF` heredoc whose first command fails, with no `set -e`: the build exits 0;
- `USER ${APP_USER}` where `APP_USER` is a global `ARG` the stage never redeclares: it expands empty, the image runs as **root**, and the build exits 0;
- `pnpm install` on a drifted lockfile rewrites the lockfile and installs, **even with `ENV CI=true`** in the stage (pnpm 9.15.9); only `--frozen-lockfile` fails;
- a `HEALTHCHECK` that calls `curl` on `node:22-bookworm-slim`, which ships neither curl nor wget, so every compose service gated on it waits forever;
- shell-form `CMD` on a dash base keeps `sh` as PID 1: `docker stop` takes 10.2 s and exits 137 (devops research, measured on node:22).

The linters do not close this gap. hadolint 2.15.1 reports one `DL1000` and **nothing else** for a file with `EXPOSE 127.0.0.1:8080:8080`, or with a heredoc terminator followed directly by the next instruction. `docker build --check` errors out, with every warning hidden, when one base cannot be resolved, and it runs only the rules of the frontend `# syntax=` names. This skill reads the **shipped** stage through the `FROM <stage>` chain, joins it with the build invocation and the manifests, and proves each finding with a built-image oracle.

It owns `ownership.json` row `container-build` (§1–§10). `@deployment-engineer` (this pack) judges its rows. It replaces `dockerfile-lint` and keeps that skill's FROM classifier, its "every check reads the final stage" rule, its HEALTHCHECK-per-runtime judgement, the `.dockerignore` check and `docker history`.

**Every finding cites `<Dockerfile:line>` + the stage it judges (the shipped stage, or the builder for a build-time class) + the base and its family + the invocation that ships it (CI `file:`/`target:`, compose `build:`, bake) + the oracle and its tier + the fix in the Dockerfile's own syntax.** A pre-flight row is a candidate; none is a finding. "The Dockerfile looks fine" is never printed; the output is the class-coverage block (§ Output). Verification follows [`refute-before-report.md`](../../../../snippets/refute-before-report.md) with [`precedents/devops.md`](../../../../snippets/precedents/devops.md) (containers § 29–40, tools § 41–46); the oracles are [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § DevOps, V231, V235–V240, V242 and V243.

## The rule

A candidate is a finding when all four hold (the seven gates as `precedents/devops.md` § Reading the seven gates applies them to images):

1. **The stage ships** (gates 1, 7). The stage is the last `FROM`, or the `--target` / compose `build.target` / bake `target` that an invocation in pre-flight 0a names. Runtime classes (§1, §2, §6, §8) are judged on that stage only; builder stages count only for build-time classes (§3–§5, §7 libc and CGO) (precedents § 38). A Dockerfile no invocation builds is Hardening.
2. **The event happens** (gate 2). A SIGTERM on every rollout, a source edit, a lockfile drift, a health gate in compose/Swarm/ECS, an arm64 node, a rebuild of the same commit, a pod with `runAsNonRoot: true`.
3. **No control already covers it** (gate 4). `tini` / `docker run --init` / compose `init: true`; a handler in the app; a prune before the copy; a bump bot (precedents § 31); an orchestrator probe instead of HEALTHCHECK (§ 29); a pod `runAsUser`; a per-file `.dockerignore`.
4. **The oracle fired, or both ends are cited** (gate 6). The built-image oracle (B) ran on a scratch build, or the static trace names both ends (the instruction and the invocation or manifest that makes it matter), and the row is `[report-flagged]`.

## Boundaries

- **Security owns the attacker-path claims about the image, when the security pack is installed** — `iac-scan` §1: the final stage running as root (its severity), secret `ARG`/`ENV` and secret files, `ADD <url>` / `curl | sh` / unpinned build-time fetches, TLS verification disabled (CT-D20), and an untagged, `:latest` or floating base read as "whoever moves the tag changes what ships". **Devops owns correctness:** the stage-chain resolution itself (§1 supplies the awk; both packs print the same verdicts), CT-D14, and base pinning for **reproducibility and rollback** (§7, §10). One line carrying both claims is one finding per `<file:line>`, credited to the owner whose claim is more severe; the other corroborates (the batch-4 devops eval's tie-break; `precedents/devops.md` § 1 routes the attacker half). Without the security pack, pre-flight R prints those rows tagged `security-class (owner pack not installed)` at this skill's severity, never at security's.
- **Shutdown is split three ways.** PID 1 and signal delivery are §2 here (infrastructure hands K-PID1 to this skill). The app's handler and drain number are `deploy-safety-scan` §5 (this pack). `preStop`, `terminationGracePeriodSeconds` and `THR-SHUTDOWN-GRACE` arithmetic are infrastructure `k8s-availability-scan` §7 when that pack is installed; the telemetry flush is observability's.
- **Image CVEs, SBOM and signing** → `release-security` (this pack, the runner). **Scanned digest = pushed digest, rebuild-after-scan** → `release-integrity-scan` §4. **CI layer cache** (`cache-from`/`cache-to`, `mode=max`, `scope=`) → `pipeline-cache-scan` §2. **A masked hadolint job in CI** → `pipeline-integrity-scan` §1.
- **Manifest fields** (probes, `securityContext`, `readOnlyRootFilesystem`) → infrastructure; §1 reads `runAsNonRoot`/`runAsUser` only to join CT-D14. **Compose** `depends_on`, `healthcheck:`, `init:`, `stop_grace_period` → `compose-scan` (this pack).

## Adapt to the codebase — the stack lanes

Discover every Dockerfile and invocation (pre-flight 0a); never assume `./Dockerfile` or a context. Print the lanes you ran in the header.

| Lane | Lockfile-enforced install (§4) | PID 1 (§2) | HEALTHCHECK binary (§6) | Runtime content (§8) · libc (§7) |
|---|---|---|---|---|
| **Node** | `npm ci`, `pnpm install --frozen-lockfile`, `yarn install --immutable` (berry) / `--frozen-lockfile` (classic) | exec-form `node`, a handler or `tini`; never `npm start` | `node -e "fetch(…)"` on slim; busybox `wget` on alpine | `pnpm deploy --prod`, `npm ci --omit=dev`, `npm prune --omit=dev` before the copy · native addons (`sharp`, `bcrypt`, Prisma engines) must be built on the runtime's libc |
| **Python** | `pip install --require-hashes -r`, `uv sync --locked`, `poetry install` after a committed lock | gunicorn/uvicorn exec form (server-managed SIGTERM) | `python -c "urllib.request…"` | a venv copied whole; wheels built on the runtime's libc |
| **Go** | `go mod download` + `-mod=readonly` | the static binary, exec form | `["/app", "healthcheck"]` (precedents § 30) | `CGO_ENABLED=0` into `scratch`/`distroless/static`; `GOOS`/`GOARCH` from `TARGETOS`/`TARGETARCH` |
| **JVM** | Gradle/Maven wrapper with a lock or BOM | `java` exec form; `--start-period` for warm-up | `curl`/`wget` only if the chain installs it (read the base); the app's own health endpoint | the jar only, not the build tree |
| **Static / nginx** | the build stage's lane | the base's (`STOPSIGNAL SIGQUIT`, precedents § 36) | busybox `wget` on alpine | `dist/` only; `nginx-unprivileged` runs as 101 (§ 33) |

A shared base stage used by N services is **one finding with N call sites** (precedents § 5).

## Tool lane and ledger

| Lane | Command and pin | Trap that makes a clean result false (precedents § 41) |
|---|---|---|
| BuildKit checks | `docker build --check -f <file> <ctx>` (buildx ≥ 0.15); `# check=error=true` in a scratch copy for a gate | An unresolvable base → `ERROR: … failed to resolve source metadata`, no warnings printed, exit 1 like a violation: NOT-RUN [V]. A local-only base resolves on the `docker` driver [V]. The rules are the `# syntax=` frontend's: on one file, `docker/dockerfile:1.6`–`1.8` ran 2 rules and missed `SecretsUsedInArgOrEnv`, `1.10` and the bundled frontend ran 3 [V]. Print the frontend |
| hadolint | `hadolint/hadolint:v2.15.1@sha256:32dac941…` (digest read 2026-10-10), `-f json --failure-threshold warning`, stdin | `DL1000` = that file was not scanned: `EXPOSE ip:port:port`; a heredoc terminator followed directly by an instruction (a blank line after `EOF` parses) [V]. Default threshold `info` fails on DL3066 alone. `THR-SCANNER-FLOOR` |
| checkov | `checkov --framework dockerfile` when installed (to enable: `pipx install checkov==3.3.26`) (`CKV2_DOCKER_*` only) | `CKV_DOCKER_4` flags `ADD --checksum`; not installed → NOT-INSTALLED with the command |
| Built image (B) | `docker image inspect`, `container-structure-test` 1.22.1 (`--platform` set), `dive` 0.13.1, `diffoci` 0.1.8, `crane config` | cst defaults to amd64; trivy image-config with 0 targets exits 0; Docker Desktop not sharing `/private/tmp` → use stdin or the socket |

Every B-tier run uses a scratch tag (`cbs-<n>:probe`), never pushes, and removes what it built. No daemon → `blocked (no docker)` with the command written out.

## Pre-flight

Run as **one** script from the repo root (bash 3.2 and zsh print the same rows). Grep **N** feeds **§N**; 0 is the inventory; R lists the security-routed rows. Every `rg` names its path; an rg exit 2 is a failed grep, never zero hits. `--iglob` matters: `api.Dockerfile` and `Containerfile` are real names, and `Dockerfile.dockerignore` must not be read as a Dockerfile. Nothing is written inside the repo: the awk programs, facts and tool output go to `$SCAN`. The docker lane (9) reads each context and writes nothing.

```bash
X=(-g '!**/{node_modules,vendor,dist,build,out,target,.venv,venv,coverage,.next,.turbo,generated}/**'
   -g '!**/{test,tests,__tests__,spec,e2e,fixtures,__fixtures__,mocks,__mocks__,testdata,examples}/**' -g '!**/{docs,ai,.claude,.git}/**')
DF=(--hidden --iglob 'Dockerfile*' --iglob '*.dockerfile' --iglob 'Containerfile*' --iglob '*.containerfile' --iglob '!*.dockerignore'
    --iglob '!**/{node_modules,vendor,dist,build,out,target,.venv,venv,coverage,.next,.turbo,generated}/**'
    --iglob '!**/{test,tests,__tests__,spec,e2e,fixtures,__fixtures__,mocks,__mocks__,testdata,examples}/**' --iglob '!**/{docs,ai,.claude,.git}/**')   # X as --iglob: every --iglob is matched after every -g, so the exclusions must be --iglob too
NC=(rg -v --pcre2 '^[^:]+:\d+:\s*#')   # drops comment-only hit lines
SCAN="${SCAN:-$(mktemp -d "${TMPDIR:-/tmp}/container-build.XXXXXX")}"; echo "SCAN=$SCAN"
echo '# 0a inventory: Dockerfiles; ignore files; build invocations (context, file, target) in CI, compose, bake, scripts'
rg --files "${DF[@]}" . | sort > "$SCAN/df.txt"; cat "$SCAN/df.txt"
rg --files --hidden -g '.dockerignore' -g '*.dockerignore' -g '.containerignore' "${X[@]}" . | sort
rg -n --hidden --pcre2 -g '.github/workflows/*.{yml,yaml}' -g '**/.gitlab-ci*.yml' -g '*compose*.{yml,yaml}' -g '**/docker-bake.{hcl,json}' -g '**/Makefile' -g '*.sh' "${X[@]}" \
  '^\s*-?\s*(context|dockerfile|file|target)\s*[:=]|\bdocker\s+(buildx\s+)?build\b[^\n]*\s(-f|--file|--target)\b|\bbake\b' . | "${NC[@]}"
cat > "$SCAN/chain.awk" <<'AWK'
# §1 the shipped stage's effective USER through FROM <stage> (the same chain security iac-scan §1 grep 2a resolves); -v T=<stage> for --target
function lc(s) { return tolower(s) }
toupper($1) == "ARG" && !n { next }
toupper($1) == "FROM" { n++; ref = ""; nm = ""
  for (i = 2; i <= NF; i++) { if ($i ~ /^--/) continue; if (ref == "") { ref = $i; continue } if (toupper($i) == "AS" && i < NF) nm = lc($(i + 1)) }
  par[n] = ref; line[n] = FNR; if (nm != "") idx[nm] = n; next }
toupper($1) == "ARG" && n { for (i = 2; i <= NF; i++) { split($i, a, "="); dec[n, a[1]] = 1; dv[n, a[1]] = a[2] } }; toupper($1) == "USER" && n { usr[n] = $2; set[n] = 1; ul[n] = FNR }
END { if (!n) exit; f = (T != "" && (lc(T) in idx)) ? idx[lc(T)] : n; s = f; h = 0
  while (!set[s] && (lc(par[s]) in idx) && h++ < 50) s = idx[lc(par[s])]
  at = FILENAME ":" (set[s] ? ul[s] : line[f]) ": shipped stage (FROM line " line[f] (T != "" ? ", target " T : "") ")"
  if (!set[s]) { print at " sets no USER; base " par[s] " -> INHERIT-EXTERNAL (read: crane config " par[s] " | jq -r .config.User)"; exit }
  u = usr[s]; v = (u ~ /^(root|0)(:|$)/) ? "ROOT" : "non-root"
  if (u ~ /\$/) { k = u; gsub(/[${}]/, "", k); sub(/:.*/, "", k)
    if ((s, k) in dec) v = "ARG-DRIVEN default=" (dv[s, k] == "" ? "<none>" : dv[s, k]) ((dv[s, k] == "" || dv[s, k] ~ /^(root|0)(:|$)/) ? " -> ROOT unless every caller passes --build-arg" : " -> read the callers' --build-arg")
    else v = "ARG-DRIVEN " k " is not declared in this stage -> expands empty -> ROOT" }
  else if (v != "ROOT" && u !~ /^[0-9]+(:[0-9]+)?$/) v = "non-root NAMED (CT-D14: runAsNonRoot cannot verify it)"
  print at " user=" u " -> " v (s != f ? " [inherited from the stage at line " line[s] "]" : "") }
AWK
cat > "$SCAN/facts.awk" <<'AWK'
# §2-§8 facts: logical lines (continuations joined, heredoc bodies held), per-stage state, the shipped stage resolved through FROM <stage>
function lc(s) { return tolower(s) }; function out(c, l, m) { printf "%s:%d: %s %s\n", FILENAME, l, c, m }
function fam(r) { r = lc(r); if (r == "scratch") return "scratch"; if (r ~ /distroless\/static|static-debian|chainguard\/static/) return "static"
  if (r ~ /distroless|chainguard|cgr\.dev|wolfi/) return "distroless"; if (r ~ /alpine/) return "alpine"; if (r ~ /slim|minimal|micro/) return "slim"; return "full" }
function libc(f) { return f == "alpine" ? "musl" : (f == "scratch" || f == "static") ? "none" : "glibc" }
function unq(s,   o, q) { o = ""; while (match(s, /'[^']*'|"[^"]*"/)) { q = substr(s, RSTART, RLENGTH); o = o substr(s, 1, RSTART - 1) ((q ~ /[ \t]\|[ \t]/) ? q : "''"); s = substr(s, RSTART + RLENGTH) } return o s }   # a quoted span is data (`sed 's|a|b|'`) unless it holds a spaced pipe (`sh -c 'x | y'`)
function pin(r, l,   v) { if (lc(r) == "scratch") return; if (r ~ /\$/) v = "ARG-DRIVEN"; else if (r ~ /@sha256:/) v = "digest"; else if (r ~ /:latest$/) v = "LATEST"
  else if (r !~ /:[^\/]*$/) v = "UNTAGGED"; else if (r ~ /:[^:\/]*[0-9]+\.[0-9]+/) v = "version"; else v = "floating"; out("BASE", l, r " pin=" v) }
BEGIN { g["TARGETOS"] = g["TARGETARCH"] = g["TARGETPLATFORM"] = g["BUILDPLATFORM"] = 1 }
hd { if ($0 ~ ("^[ \t]*" hw "[ \t]*$")) { hd = 0; if (hk == "RUN" && hc > 1 && !he) out("HEREDOC-NO-E", hl, hc " commands, no set -e: only the last exit counts") }
     else if ($0 ~ /^#!/) { if ($0 ~ /[ \t]-[a-z]*e/) he = 1 } else if ($0 !~ /^[ \t]*(#.*)?$/) { hc++; if (hc == 1 && $0 ~ /set[ \t]+-[a-z]*e|errexit/) he = 1 }
     next }
{ if (cont) { if ($0 ~ /^[ \t]*#/) next; buf = buf " " $0 } else { if ($0 ~ /^[ \t]*(#|$)/) next; buf = $0; L = FNR }
  if (buf ~ /\\[ \t]*$/) { sub(/\\[ \t]*$/, "", buf); cont = 1; next }
  cont = 0; $0 = buf; I = toupper($1); r = $0; sub(/^[ \t]*[A-Za-z]+[ \t]+/, "", r); while (r ~ /^--[^ \t]+[ \t]+/) sub(/^--[^ \t]+[ \t]+/, "", r) }
(I == "RUN" || I == "COPY" || I == "ADD") && match($0, /<<-?[ \t]*["']?[A-Za-z_][A-Za-z0-9_]*/) { hw = substr($0, RSTART, RLENGTH); sub(/^<<-?[ \t]*["']?/, "", hw)
  hd = 1; hk = I; hl = L; hc = 0; he = ($0 ~ /set[ \t]+-[a-z]*e/) }
I == "FROM" { n++; ref = ""; nm = ""; pf = ""
  for (i = 2; i <= NF; i++) { if ($i ~ /^--platform=/) { pf = substr($i, 12); continue } if ($i ~ /^--/) continue; if (ref == "") { ref = $i; continue } if (toupper($i) == "AS" && i < NF) nm = lc($(i + 1)) }
  fl[n] = L; sn[n] = (nm != "" ? nm : "#" n); if (nm != "") idx[nm] = n
  if (lc(ref) in idx) { pst[n] = idx[lc(ref)]; base[n] = base[pst[n]]; fm[n] = fm[pst[n]] } else { pst[n] = 0; base[n] = ref; fm[n] = fam(ref); pin(ref, L) }
  if (pf != "" && pf !~ /\$/) out("PLATFORM-CONST", L, "--platform=" pf); if (pf ~ /BUILDPLATFORM/) bp[n] = 1
  next }
!n { if (I == "ARG") { split($2, a, "="); g[a[1]] = 1 } next }; I == "ARG" { for (i = 2; i <= NF; i++) { split($i, a, "="); dec[n, a[1]] = 1 } next }
{ for (k in g) if (!((n, k) in dec) && $0 ~ ("[$][{]?" k "([^A-Za-z0-9_]|$)")) { ok = 0; st = n; h = 0; while (st && h++ < 50) { if ((st, k) in envd) ok = 1; st = pst[st] }
    if (!ok) out("ARG-SCOPE", L, k " is a global ARG not redeclared in this stage: it expands empty") } }
I == "ENV" { for (i = 2; i <= NF; i++) if ($i ~ /=/) { split($i, a, "="); envd[n, a[1]] = 1; if (a[1] == "PORT") port[n] = a[2]; if (a[1] == "CGO_ENABLED" && a[2] == "0") cg0[n] = 1 } else if (i == 2) envd[n, $2] = 1 }
I == "WORKDIR" { wd[n] = $2; if ($2 !~ /^[\/$]/) out("WORKDIR-RELATIVE", L, $2) }
I == "SHELL" && /pipefail/ { pfs[n] = 1 }; I == "EXPOSE" { ex[n] = ex[n] " " $2 }; I == "STOPSIGNAL" { sig[n] = $2 }
I == "CMD" || I == "ENTRYPOINT" || I == "HEALTHCHECK" { if (++cnt[n, I] == 2) out("DUP-" I, L, "only the last " I " of a stage counts") }
I == "CMD" { cmd[n] = r; cl[n] = L }; I == "ENTRYPOINT" { ep[n] = r; el[n] = L }; I == "HEALTHCHECK" { hcx[n] = r; hcl[n] = L }
I == "COPY" || I == "ADD" { fr = ""; src = ""; for (i = 2; i < NF; i++) { if ($i ~ /^--from=/) fr = lc(substr($i, 8)); else if ($i !~ /^--/) src = src " " $i }
  if (fr == "" && src ~ / \.\/?( |$)/ && !cp[n]) cp[n] = L; if (fr != "") { cf[n] = cf[n] " " fr; cfs[n, fr] = cfs[n, fr] src; cfl[n, fr] = L } }
I == "RUN" { s = r; if (s ~ /^cd[ \t]/) out("RUN-CD", L, "cd in RUN (use WORKDIR)")
  t = unq(s); gsub(/\|[ \t]*grep[ \t]+-[A-Za-z]*q[A-Za-z]*/, "", t)
  if (t !~ /^\[/ && t ~ /[^|]\|[^|]/ && t !~ /pipefail/) { st = n; h = 0; ok = 0; while (st && h++ < 50) { if (pfs[st]) ok = 1; st = pst[st] } if (!ok) out("PIPE-NO-PIPEFAIL", L, "a failing producer is masked by /bin/sh -c") }
  ins = (s ~ /(^|[ \t;&|(])(npm[ \t]+(ci|install|i)|pnpm[ \t]+(install|i)|yarn[ \t]+install|pip[0-9.]*[ \t]+install|uv[ \t]+sync|poetry[ \t]+install|bundle[ \t]+install|composer[ \t]+install|go[ \t]+mod[ \t]+download|cargo[ \t]+(build|fetch))([ \t;&|]|$)/ || s ~ /(^|[ \t;&])yarn[ \t]*($|&&|;)/) && s !~ /[ \t](-g|--global|--offline)([ \t]|$)/
  if (ins) { dep[n] = 1; if (s ~ /npm|pnpm|yarn/) js[n] = 1; if (cp[n] && !lo[n]) { lo[n] = 1; out("LAYER-ORDER", L, "dependency install after COPY . . at line " cp[n]) } }
  if (s ~ /--omit[= ]dev|--prod(uction)?([ \t=]|$)|npm[ \t]+prune|pnpm[ \t]+deploy|--only[= ]prod/) prn[n] = 1
  if (s ~ /(npm|pnpm|yarn)[ \t]+(run[ \t]+)?build|(^|[ \t])(tsc|nest[ \t]+build|vite[ \t]+build)([ \t]|$)|mvn[ \t].*package|gradle[ \t].*(build|assemble)/) bld[n] = 1
  if (s ~ /go[ \t]+build/) { gob[n] = L; if (s ~ /CGO_ENABLED=0/) cg0[n] = 1; if (s ~ /GOARCH/) gar[n] = 1 }
  if (s ~ /(apt-get|apt|apk|dnf|yum|microdnf)[ \t].*(install|add)[ \t].*(build-essential|gcc|g\+\+|[ \t]make|[ \t]git|-dev([ \t]|$)|alpine-sdk|cmake)/) tl[n] = L
  if (s ~ /(apt-get|apt|apk|dnf|yum)[ \t].*(install|add)[^&;|]*curl/) cu[n] = 1; if (s ~ /(apt-get|apt|apk|dnf|yum)[ \t].*(install|add)[^&;|]*wget/) wg[n] = 1
  if (s ~ /ch(own|mod)[ \t]+-[A-Za-z]*R/) chr[n] = L
  if (s ~ /apt(-get)?[ \t]+([^ \t]+[ \t]+)*update([ \t;&]|$)/ && s !~ /apt(-get)?[ \t]+([^ \t]+[ \t]+)*(install|upgrade|dist-upgrade)([ \t]|$)/) out("APT-UPDATE-ALONE", L, "apt-get update with no install in the same RUN: a later install reuses this layer's stale index (no --check or hadolint rule fires on it, §9)") }
END { if (!n) exit; S = (T != "" && (lc(T) in idx)) ? idx[lc(T)] : n; b = base[S]; f = fm[S]; st = S; h = 0
  while (st && h++ < 50) { if (e == "" && ep[st] != "") { e = ep[st]; eL = el[st] } if (!cst && c == "" && cmd[st] != "") { c = cmd[st]; cL = cl[st] } if (e != "" && c == "") cst = 1
    if (hv == "" && hcx[st] != "") { hv = hcx[st]; hL = hcl[st] } if (sg == "" && sig[st] != "") sg = sig[st]; if (pt == "" && port[st] != "") pt = port[st]; exs = exs ex[st]
    if (cu[st]) cuS = 1; if (wg[st]) wgS = 1; if (tl[st] && !tL) tL = tl[st]; if (chr[st] && !chL) chL = chr[st]; chain[st] = 1; st = pst[st] }
  out("SHIPPED", fl[S], "stage " sn[S] " base=" b " family=" f (T != "" ? " (target " T ")" : ""))
  x = (e != "") ? e : c; xl = (e != "") ? eL : cL
  if (x == "") out("PID1-INHERITED", fl[S], "no CMD/ENTRYPOINT in the chain: read crane config " b " | jq .config.Entrypoint,.config.Cmd")
  else if (x !~ /^\[/) out("PID1-SHELL-FORM", xl, "/bin/sh -c " x " on " f (f == "alpine" ? " (ash tail-execs one command: precedents § 35)" : " (sh stays PID 1)"))
  else { x1 = x; sub(/^\[[ \t]*"/, "", x1); sub(/".*/, "", x1)
    if (x1 ~ /(^|\/)(tini|dumb-init|catatonit|s6-svscan|init)$/) out("PID1-INIT", xl, x1 " reaps and forwards; the app still needs a handler")
    else if (x1 ~ /(^|\/)(npm|npx|yarn|pnpm|bun)$/) out("PID1-PKG-MANAGER", xl, x1 " is PID 1")
    else if (x1 ~ /(^|\/)(ba|da)?sh$/ && x ~ /"-c"/) out("PID1-SH-C", xl, (x ~ /exec[ \t]/ ? "exec present: read it" : "no exec: sh stays PID 1"))
    else if (x1 ~ /\.sh$/) out("PID1-SCRIPT", xl, x1)
    else if (x1 ~ /(^|\/)(su|sudo)$/) out("PID1-SU", xl, x1 " forks the app")
    else out("PID1-EXEC", xl, x1 " is PID 1 with no init: its handler is deploy-safety-scan §5") }
  if (sg != "") out("STOPSIGNAL", xl ? xl : fl[S], sg)
  if (hv == "") out("HC-NONE", fl[S], "(precedents § 29: a nit on Kubernetes-only images)")
  else if (hv !~ /^NONE/) { y = hv; sub(/^.*CMD[ \t]+/, "", y); hb = y; sub(/^\[[ \t]*"/, "", hb); sub(/[" \t].*/, "", hb); sub(/.*\//, "", hb)
    if ((hb == "curl" && !cuS && f != "full") || (hb == "wget" && !wgS && f != "full" && f != "alpine")) out("HC-BINARY", hL, hb " is not in a " f " base and the chain never installs it")
    if (match(hv, /(localhost|127\.0\.0\.1|0\.0\.0\.0):[0-9]+/)) { hp = substr(hv, RSTART, RLENGTH); sub(/.*:/, "", hp)
      if ((exs != "" && index(exs " ", " " hp " ") == 0 && index(exs, " " hp "/") == 0) || (pt != "" && pt != hp)) out("HC-PORT", hL, "probes " hp "; EXPOSE" exs (pt != "" ? " PORT=" pt : "")) } }
  for (st = 1; st <= n; st++) { if (gob[st] && !cg0[st] && libc(f) != libc(fm[st])) out("GO-CGO", gob[st], "CGO default on " fm[st] " (" libc(fm[st]) ") -> " f " (" libc(f) ")")
    if (bp[st] && gob[st] && !gar[st]) out("GO-NO-TARGETARCH", gob[st], "$BUILDPLATFORM builder without GOOS/GOARCH")
    if (bp[st] && dep[st] && !gob[st]) out("BUILDPLATFORM-NATIVE", fl[st], "dependency install on the build platform: native artefacts")
    if (!chain[st]) continue; m = split(cf[st], fs, " ")
    for (j = 1; j <= m; j++) { X = fs[j]; if (!(X in idx) || seen[st, X]++) continue; xi = idx[X]
      rt = (cfs[st, X] ~ /(node_modules|site-packages|venv|\/usr\/local\/lib|vendor|\.so)(\/| |$)/ || index(cfs[st, X] " ", " " wd[xi] " ") || index(cfs[st, X] " ", " / "))
      if (rt && dep[xi] && !gob[xi] && libc(fm[xi]) != libc(fm[st]) && libc(fm[st]) != "none") out("LIBC-MISMATCH", cfl[st, X], "stage " X " (" fm[xi] ", " libc(fm[xi]) ") installs deps -> " fm[st] " (" libc(fm[st]) ")")
      if (cfs[st, X] ~ /node_modules\/?( |$)/ && js[xi] && !prn[xi]) out("RESIDUE", cfl[st, X], "node_modules from stage " X ", which never prunes dev dependencies") } }
  if (js[S] && bld[S] && !prn[S]) out("DEV-DEPS-SHIP", fl[S], "the shipped stage installs and builds with no prune")
  if (tL) out("BUILD-TOOLS", tL, "compilers or git in the shipped chain"); if (chL) out("CHOWN-R", chL, "recursive chown/chmod duplicates every byte into a new layer (COPY --chown)") }
AWK
echo '# 1a stage chain (shipped stage = last FROM; re-run with -v T=<stage> for each target 0a printed)'
while IFS= read -r f; do awk -f "$SCAN/chain.awk" "$f"; done < "$SCAN/df.txt"
echo '# 1b CT-D14: workloads with runAsNonRoot: true and no runAsUser (join their images with the NAMED rows above)'
NR_AWK='function f() { if (nr && !ru) printf "%s:%d: NONROOT-NO-UID %s%s\n", FILENAME, dl, kd, im; nr = ru = 0; im = ""; kd = "" }
  FNR == 1 || /^---/ { f(); dl = FNR } /^kind:/ { kd = $2 } /runAsNonRoot:[ \t]*true/ { nr = 1 } /runAsUser:[ \t]*[0-9]/ { ru = 1 }
  /^[ \t]*-?[ \t]*image:/ { x = $0; sub(/.*image:[ \t]*/, "", x); im = im " " x } END { f() }'
{ rg -l --pcre2 -g '*.{yml,yaml}' "${X[@]}" '^\s*runAsNonRoot:\s*true' .; find "$SCAN" -maxdepth 1 -name 'render-*.yaml'; } | while IFS= read -r m; do awk "$NR_AWK" "$m"; done
echo '# 2-8 facts per file (shipped stage first; build-time rows from every stage)'
while IFS= read -r f; do awk -f "$SCAN/facts.awk" "$f"; done < "$SCAN/df.txt" > "$SCAN/facts.txt"; rg -v ': (HC-NONE|PID1-EXEC) ' "$SCAN/facts.txt"
echo "HC-NONE in $(grep -c ': HC-NONE ' "$SCAN/facts.txt") files: a finding only where these gate on health (precedents § 29):"
rg -n --hidden --pcre2 -g '*compose*.{yml,yaml}' -g '*task-def*.json' -g '*taskdef*.json' "${X[@]}" 'condition:\s*service_healthy|"healthCheck"\s*:|^\s*deploy:\s*$' . | "${NC[@]}"
echo "PID1-EXEC in $(grep -c ': PID1-EXEC ' "$SCAN/facts.txt") files: the app is PID 1 with no init; its handler is deploy-safety-scan §5 (rows in $SCAN/facts.txt)"
echo '# 2b entrypoint scripts: every exit path must exec the app'
rg -N 'PID1-SCRIPT' "$SCAN/facts.txt" | while IFS= read -r row; do f=${row%%:*}; s=${row##* }; p=$(rg --files "$(dirname "$f")" -g "${s##*/}" | head -1)
  if [ -z "$p" ]; then echo "$f: entrypoint $s not under $(dirname "$f"): read the context"; elif rg -q '^\s*exec\s' "$p"; then echo "$p: exec present (read every exit path)"; else echo "$p: NO-EXEC"; fi; done
echo '# 3b ignore file per Dockerfile: <file>.dockerignore beside it wins, else the CONTEXT ROOT one (a .dockerignore beside a root-context Dockerfile is ignored)'
IGN() { m=""; rg -q --pcre2 '^\s*(\*\*/)?/?\.git(/|/\*\*)?\s*$' "$1" || m="$m .git"; rg -q --pcre2 '^\s*(\*\*/)?/?\.env(\*|\.\*)?\s*$' "$1" || m="$m .env"
  [ "$2" = js ] && { rg -q --pcre2 '^\s*(\*\*/)?/?node_modules(/|/\*\*)?\s*$' "$1" || m="$m node_modules"; }; echo "${m:- none}"; }
while IFS= read -r f; do d=$(dirname "$f"); j=""; rg -q -i --pcre2 '^\s*(COPY|ADD)\s+(?![^\n]*--from=)' "$f" || { echo "$f: copies nothing from its context"; continue; }; rg -q '\b(npm|pnpm|yarn)\b' "$f" && j=js
  if [ -f "$f.dockerignore" ]; then echo "$f: per-file ignore lacks:$(IGN "$f.dockerignore" $j)"; continue; fi
  a="ctx=$d: $([ -f "$d/.dockerignore" ] && echo "lacks:$(IGN "$d/.dockerignore" $j)" || echo NONE)"; [ "$d" = . ] || a="$a | ctx=.: $([ -f .dockerignore ] && echo "lacks:$(IGN .dockerignore $j)" || echo NONE)"; echo "$f: $a"; done < "$SCAN/df.txt"
echo '# 4 lockfile not enforced inside the build (CI auto-freeze does not reach RUN; ENV CI=true did not freeze pnpm 9.15.9 either)'
rg -n --pcre2 "${DF[@]}" '\b(npm\s+(i|install)\b(?!\s+(-g|--global)\b)|pnpm\s+(i|install)\b(?![^\n]*--frozen-lockfile)|yarn(\s+install)?\s*(&&|;|\\|$)(?![^\n]*--(frozen-lockfile|immutable))|pip3?\s+install\b(?=[^\n]*\s(-r|--requirement)\b|[^\n]*\s\.(\s|$))(?![^\n]*(--require-hashes|\s-c\s|--constraint))|uv\s+sync\b(?![^\n]*--(locked|frozen))|cargo\s+(build|install)\b(?![^\n]*--locked)|bundle\s+install\b(?![^\n]*--(frozen|deployment))|go\s+build\b[^\n]*-mod=mod)' . | "${NC[@]}"
echo '# R routed to security iac-scan §1 when installed (secret ARG/ENV, TLS verification off, curl|sh, ADD URL): listed, never posted here'
rg -n -i --pcre2 "${DF[@]}" '^\s*(ARG|ENV)\s+\w*(SECRET|TOKEN|PASSW(OR)?D|API_?KEY|PRIVATE_?KEY|ACCESS_?KEY|CREDENTIAL)\w*|curl\b[^\n]*\s(-k|--insecure)\b|--no-check-certificate|NODE_TLS_REJECT_UNAUTHORIZED\s*=?\s*["\x27]?0|strict-ssl\s+false|--trusted-host|--allow-untrusted|GIT_SSL_NO_VERIFY|\b(curl|wget)\b[^|\n]*\|\s*(sudo\s+)?(ba|z|da)?sh\b|^\s*ADD\s+(--\S+\s+)*https?://' . | "${NC[@]}"
echo '# 7 bump bot for base images (precedents § 31) and runtime versions to read against the release schedule'
rg -n --hidden --pcre2 -g '.github/dependabot.y*ml' -g '{renovate,.renovaterc}*' -g '.github/renovate*' '^\s*-?\s*package-ecosystem:\s*["\x27]?docker|^\s*directory:|"(docker|dockerfile)"|\bextends\b' . | "${NC[@]}"
echo '# 9 build-check lane (T): docker build --check + hadolint per file; a parse error or an unresolved base is NOT-RUN for that file'
HL="hadolint/hadolint:v2.15.1@sha256:32dac94127fd60b7b7e3fbfc65e1383b9b5e25c9bfd7b8536de7a539fe68a12d"
if docker info >/dev/null 2>&1; then while IFS= read -r f; do docker build --check -f "$f" "$(dirname "$f")" > "$SCAN/check.out" 2>&1; rc=$?
    if rg -q 'Check complete' "$SCAN/check.out"; then echo "$f: check rc=$rc $(rg -o 'WARNING: \w+' -r '$0' "$SCAN/check.out" | sed 's/WARNING: //' | sort | uniq -c | awk '{printf "%s%s ", $2, ($1 > 1 ? "x" $1 : "")}')"
    else echo "$f: check NOT-RUN $(rg -m1 -o 'ERROR: .{0,100}' "$SCAN/check.out")"; fi
    docker image inspect "$HL" >/dev/null 2>&1 || { echo "$f: hadolint NOT-RUN (image not local — to enable: docker pull $HL)"; continue; }
    docker run --pull=never --rm -i "$HL" hadolint -f json --failure-threshold warning - < "$f" > "$SCAN/hl.json"; rc=$?
    if rg -q '"DL1000"' "$SCAN/hl.json"; then echo "$f: hadolint NOT-RUN (parse error at line $(rg -o '"line":(\d+)' -r '$1' "$SCAN/hl.json" | head -1))"
    else echo "$f: hadolint rc=$rc $(rg -o '"code":"(DL\d+|SC\d+)","column":\d+,"file":"[^"]*","level":"(error|warning)"' -r '$1' "$SCAN/hl.json" | sort -u | tr '\n' ' ')"; fi
  done < "$SCAN/df.txt"; else echo '9: blocked (no docker daemon): docker build --check -f <file> <ctx>; docker run --rm -i <HL> hadolint -f json --failure-threshold warning - < <file>'; fi
echo '# 10 reproducibility claims (only a claim makes §10 a finding) and the recorded size baseline'
rg -n -i --pcre2 --hidden -g '*.{md,yml,yaml,hcl,json}' --iglob 'Dockerfile*' --iglob '!**/{node_modules,vendor,fixtures,testdata,.claude,.opencode,.cursor,.git,ai}/**' '\breproducible[- ](builds?|images?|containers?)\b|\bSLSA\b[^\n]*\b(L|level\s*)3\b|SOURCE_DATE_EPOCH|rewrite-timestamp' . | "${NC[@]}"
rg -n -i --pcre2 -g '**/runbooks/docker.md' '\b\d+(\.\d+)?\s*(MB|GB|MiB|GiB)\b' .
```

How to read it:
- **1a** is the stage chain. `INHERIT-EXTERNAL` needs `crane config` (precedents § 33); `ARG-DRIVEN` needs the default and every caller's `--build-arg`; `NAMED` matters only joined with a **1b** row for the same image. For every target 0a prints, re-run `awk -v T=<stage> -f "$SCAN/chain.awk" <file>` and the same for `facts.awk`.
- **2–8** print the shipped stage (`SHIPPED`) and its facts. `HC-NONE` and `PID1-EXEC` are counted, not listed: they are findings only where something gates on health (§6) or no handler exists (`deploy-safety-scan` §5).
- **3b** names the ignore file per context: a `<file>.dockerignore` beside the Dockerfile wins over the context root's, and a `.dockerignore` beside a Dockerfile built from the repo root is never read [V 2026-10-10]. 0a's `context:` decides which half of the row applies.

Blind spots, worked around rather than trusted:
- **The base's own config** (USER, ENTRYPOINT, CMD, STOPSIGNAL, HEALTHCHECK) is invisible to a grep: read `crane config <ref>`, or `docker image inspect` on a pulled scratch copy.
- **Entrypoint scripts outside the Dockerfile's directory** (a context at the repo root): 2b says so; read the copied script.
- **Bake, Earthly, Buildpacks, ko, Jib, Nix** produce images without a Dockerfile, or with a generated one: list them as `N/A (no Dockerfile: <builder>)`.

### Measured (2026-10-10)

| Tree | Result |
|---|---|
| Seeded sample: 21 Dockerfiles (incl. `worker.Dockerfile`, a `Containerfile`), compose with a `build.target`, a Deployment, a dependabot `docker` entry; 39 positives, 19 decoys, 5 routed | Static lanes 2.0 s, whole script with the docker lane 12.5 s, 0 rg or awk errors; bash 3.2 and zsh identical. **39/39 positives surface** in their §. The 3 copies under `tests/fixtures/`, `docs/examples/` and `node_modules/` and the `Dockerfile.dockerignore` never appear. The rest surface and clear on read, each by one row or precedent: inherited `USER 10001` read as non-root with `-v T=runtime` (the old final-user awk said ROOT), `nginx-unprivileged` and `distroless:nonroot` (§ 33), alpine shell form (§ 35), `exec "$@"` entrypoint, busybox `wget` on alpine, manifest-first `COPY . .` (§ 34), a pruned `node_modules`, a static `dist/` into nginx, `CGO_ENABLED=0` with `TARGETARCH`, a floating tag with a bump bot (§ 31). One fact flipped: `VOLUME /data` followed by a write in a later `RUN` **keeps** the write under BuildKit (the classic-builder class does not apply) [V] |
| `benchmarks/fixtures/*` (16) | 7 Dockerfiles in 3 fixtures, 0 rg errors, `--check` 7/7 ran, hadolint 7/7 parsed. Candidates: 5 `NAMED` users with no `runAsNonRoot` manifest (info), 2 `pip install` without hashes, a `chown -R` after `COPY . .`, `git` in a shipped stage (Refuted on read: the theme-install feature needs it), `node:20-bookworm` for the EOL read. A `# syntax=docker/dockerfile:1.6` file passed `--check` clean while the bundled frontend reports 2 `SecretsUsedInArgOrEnv` (security's rows). One FP class fixed before shipping: `RESIDUE` fired on `node_modules/.prisma` (a generated client); it now needs the whole `node_modules` |
| Real NestJS + Fastify monorepo (3 Dockerfiles, read-only, `git status` clean before and after) | 4.2 s. 0 findings. `USER node` (`NAMED`) is cleared by `runAsUser: 1000` on every workload (1b empty); `tini` as PID 1; manifest-first `--frozen-lockfile` installs; the edge image's final stage sets no USER over an ARG-driven external base (security's row, mitigated by the pod's `runAsUser`); `--check` 3/3 clean; hadolint DL3008 (§ 32), DL3025 on a shell-form HEALTHCHECK, DL4006 on a pipe into `grep -q`. Three FP classes fixed before shipping: a static `dist/` copied into nginx read as a libc mismatch; a pipe into `grep -q` read as masked; the §10 claim grep matched 35 lines of agent tooling and prose ("reproducible" alone) — 0 after excluding `.opencode`/`.claude`/`ai` and requiring "reproducible build/image" |

## The 3,000-hit path

1. **Intersect** with 0a: keep rows in a Dockerfile an invocation builds, and in the stage it ships. Dismiss the rest with one read each and name them in the coverage block.
2. **Group** by shared base stage, by base image, and by stack lane (precedents § 5).
3. **Rank:** images that reach prod first; then §2 and §1 (every rollout pays them); then the rest.
4. **Read the top 30 groups.**
5. **Run the bulk oracle once:** one `--check` + hadolint pass settles every §5/§9 row; one V231 stop per base family and PID 1 shape settles §2 for every image sharing it; one `crane config` per external base settles every `INHERIT-EXTERNAL` and `PID1-INHERITED` row.
6. **Ledger the rest** as `Live, unreviewed (k groups / n hits — <continuing command>)`. Never mark it `checked`.

## Scans for

| § | Classes | Default severity |
|---|---|---|
| 1 | Effective user through the stage chain; CT-D14 named USER × `runAsNonRoot` | M (a ROOT verdict is security's severity) |
| 2 | CT-D03 PID 1 and signal delivery | M–H (L: alpine single command) |
| 3 | CT-D01 layer-order cache bust; the context's ignore file | L–M |
| 4 | CT-D17 lockfile not enforced inside the build | M–H |
| 5 | CT-D04–D07 RUN correctness: heredoc without `set -e`, pipe without pipefail, ARG scope, `RUN cd`, relative WORKDIR | M (L: `cd`, WORKDIR) |
| 6 | CT-D09 HEALTHCHECK broken (binary, port) | M where something gates on it; nit on Kubernetes-only images |
| 7 | CT-D10 base freshness and pin; CT-D11 platform; CT-D12/D18 libc and CGO | M (H: EOL, or a binary that will not start) |
| 8 | CT-D16 builder residue and dev dependencies; CT-D15 ownership; build tools in the runtime | L–M |
| 9 | Build-check lane: CT-D08 duplicate CMD, CT-D02/D13/D19/D21–D23 rule ids | L–M |
| 10 | CT-P01–P05 reproducibility (only when claimed); CT-R10 size vs baseline | L–M (H when SLSA L3 is claimed) |

### 1. Effective user through the stage chain (CT-D14)

```
BAD:   ARG APP_USER=app / FROM alpine / USER ${APP_USER}        (global ARG, never redeclared: expands empty → root, build exit 0)
       USER node  ×  Deployment securityContext.runAsNonRoot: true, no runAsUser   (kubelet: CreateContainerConfigError)
GOOD:  FROM base AS runtime  where base ends USER 10001  (inherited) · ARG APP_USER=10001 inside the stage · USER 10001:10001
```
**Read the code:** Which stage ships (0a target)? Does the verdict hold under `-v T=<stage>`? For `INHERIT-EXTERNAL`, what does `crane config <ref> | jq -r .config.User` print (precedents § 33: `node` official is root, `nginx-unprivileged` 101, distroless `:nonroot` 65532)? For `NAMED`, does a 1b workload run this image, and does the pod or container set `runAsUser`? For `ARG-DRIVEN`, what do CI `build-args` and compose `build.args` pass?

**Finding when** the kubelet would refuse the pod (a `NAMED` user × a 1b row for that image), or the chain resolves to a user the author did not write (an `ARG` that expands empty, a `--target` that ships a root debug stage). A ROOT verdict is posted by security `iac-scan` §1 when installed; this § corroborates with the chain line. A numeric `USER` is the fix, not a named one (precedents § 37). **Proof (V235):** on a scratch build, `docker image inspect -f '{{.Config.User}}'` is non-empty, not `root`/`0`/`0:*`, numeric where `runAsNonRoot` applies; container-structure-test `metadataTest.user`; a `runAsNonRoot` server dry run through an isolated `--kubeconfig=<scratch>` admits the pod.

### 2. PID 1 and signal delivery (CT-D03)

```
BAD:   CMD node dist/main.js  on node:22-bookworm-slim     (sh -c stays PID 1: docker stop 10.2 s → 137)
       CMD ["pnpm", "start"] · CMD ["sh", "-c", "node migrate.js && node server.js"] · ENTRYPOINT ["./entrypoint.sh"] with no exec
GOOD:  ENTRYPOINT ["tini", "--"] + CMD ["node", "dist/main.js"] · an entrypoint whose every exit path is exec "$@"
```
**Read the code:** Which `PID1-*` row, on which base family (precedents § 35: alpine's ash tail-execs one command)? For `PID1-SCRIPT`, does 2b say `NO-EXEC`, and does every branch end in `exec`? For `PID1-INHERITED`, what are the base's Entrypoint/Cmd? Is `STOPSIGNAL SIGQUIT` the server's graceful signal (precedents § 36)? Does the orchestrator add an init (`docker run --init`, compose `init: true`)? Is there a handler behind the exec (`deploy-safety-scan` §5)?

**Finding when** the measured stop reaches the timeout (exit 137): the app never sees SIGTERM, so every rollout drops in-flight work. **Proof (V231):** `proof-oracles.md` § Stop timing on a scratch build of the real base: `docker stop -t 10` returns under 10 s with an exit other than 137, and an in-flight request completes.

### 3. Layer order and the context's ignore file (CT-D01)

```
BAD:   COPY . .  then  RUN npm ci                  (every source edit re-runs the install)
       Dockerfile.dockerignore beside the Dockerfile lists only node_modules   (it wins: the root ignore is not read; .git busts every build)
GOOD:  COPY package.json package-lock.json ./ · RUN npm ci · COPY . .   with .git, .env*, node_modules ignored in the file that applies
```
**Read the code:** Are the manifests already copied first in the stage (precedents § 34)? Is it `pnpm fetch` + `pnpm install --offline` after the copy (the documented pattern), or a `RUN --mount=type=bind` install? Which context does 0a give, so which ignore file applies (3b)? Does the context hold a host `node_modules` that a `COPY . .` lays over the installed one?

**Finding when** a source edit re-runs the dependency install, or the applied ignore file lets `.git` or a host `node_modules` into the context. `.env` in the context is security's (a secret file). **Proof (V236):** touch one source file and rebuild with `--progress=plain`: the install step prints `CACHED`.

### 4. Lockfile not enforced inside the build (CT-D17)

```
BAD:   RUN corepack enable && pnpm install        (a drifted lock is rewritten and installed; ENV CI=true did not stop it, pnpm 9.15.9)
       RUN npm install · RUN pip install -r requirements.txt (no hashes) · RUN uv sync
GOOD:  RUN pnpm install --frozen-lockfile · npm ci · pip install --require-hashes -r requirements.txt · uv sync --locked
```
**Read the code:** Is the flag on a continuation line the grep did not see? Is the project's own config frozen (`.yarnrc.yml` `enableImmutableInstalls: true`)? Is the `pip install .` installing a package whose dependencies come from a hashed lock? Do not clear a row because CI sets `CI=true`: the runner's environment does not reach `RUN`, and in the stage it did not freeze pnpm [V].

**Finding when** the image can contain dependency versions the tested lockfile does not. **Proof (V236):** mutate the lockfile by one version on a scratch copy: the build must fail.

### 5. RUN correctness (CT-D04–D07)

```
BAD:   RUN <<EOF / python manage.py collectstatic / python manage.py check / EOF     (the first failure is ignored)
       RUN curl -fsSL https://x/tool.tgz | tar xz   (a failed download exits 0 under /bin/sh)
       ARG PY_VERSION=3.12 / FROM python:${PY_VERSION}-slim / RUN echo "$PY_VERSION"   (empty inside the stage)
GOOD:  RUN <<EOF / set -eu / … / EOF · SHELL ["/bin/bash", "-o", "pipefail", "-c"] · ARG PY_VERSION redeclared after FROM
```
**Read the code:** Does the heredoc's first command set `-e`, or its shebang? Is the pipe's consumer a condition (`grep -q`, already dropped by the awk)? Is the `ARG-SCOPE` name set by `ENV` in this stage or its parent? `docker build --check` `UndefinedVar` sees `ENV`, `COPY`, `USER` uses but not `RUN` (devops research, measured); the awk reads all of them.

**Finding when** a failing step builds green or a variable expands empty where it chooses a version, a user or a path. **Proof (V237):** a seeded failing line inside the heredoc or the pipe's producer fails the build; `--check` and hadolint report 0 kept rule ids after the fix.

### 6. HEALTHCHECK broken (CT-D09)

```
BAD:   HEALTHCHECK CMD curl -fsS http://localhost:3000/health  on node:22-bookworm-slim   (no curl, no wget [V]: never healthy)
       EXPOSE 3000 · HEALTHCHECK CMD wget -qO- http://localhost:8080/health                (probes the wrong port)
GOOD:  HEALTHCHECK --start-period=20s CMD node -e "fetch('http://localhost:'+(process.env.PORT||3000)+'/health').then(r=>process.exit(r.ok?0:1)).catch(()=>process.exit(1))"
```
**Read the code:** Does compose (`condition: service_healthy`), Swarm or ECS gate on this image (the HC-NONE grep)? A Kubernetes-only image ignores HEALTHCHECK (precedents § 29); distroless and scratch need an exec-form self-check (§ 30). Does the chain install the binary? Does the probe path exist in the app? Does a JVM need `--start-period`?

**Finding when** the container can never turn healthy where something gates on it. **Proof (V238):** `docker inspect -f '{{.State.Health.Status}}'` is `healthy` within start-period + interval × retries on a scratch run.

### 7. Base, platform and libc (CT-D10–D12, D18)

```
BAD:   FROM node:16-alpine (EOL) · FROM --platform=linux/amd64 golang AS build · go build (CGO default on Debian) → FROM alpine
       FROM node:22-alpine AS build (npm ci, musl) → COPY --from=build /app/node_modules → FROM node:22-bookworm-slim (glibc)
GOOD:  a supported line with a bump bot (precedents § 31) · CGO_ENABLED=0 GOOS=$TARGETOS GOARCH=$TARGETARCH · one libc for build and runtime
```
**Read the code:** For each `BASE` row, is the runtime line still supported? Read the runtime's published schedule and date it in the row. Does a bump bot cover the directory (§ 31)? A floating tag with a bot is not a finding; a digest pin with no bot rots. Do the copied dependencies hold native code (`binding.gyp`, `prebuilds/`, `*.node`, `.so`)? Is the cluster mixed-arch?

**Finding when** the base is past end of life, a binary or addon will not load on the runtime's libc or arch, or a constant `--platform` builds the wrong arch. **The security split:** a `LATEST`/`UNTAGGED`/floating base as tag mutability is security `iac-scan` §1's row; this § posts the same line only for reproducibility and rollback (a rebuild of the same commit ships a different base), corroborating. **Proof (V239):** `docker run --platform linux/<arch> <img> <smoke>` succeeds for each published platform, and `docker buildx imagetools inspect` lists them.

### 8. Builder residue and runtime content (CT-D15, D16)

```
BAD:   COPY --from=build /app/node_modules ./node_modules   where build ran `npm ci` with no prune
       single stage: pnpm install + pnpm build + CMD   (dev dependencies ship) · apt-get install build-essential git in the shipped stage
       COPY . .  then  RUN chown -R node:node /app       (every byte stored twice)
GOOD:  npm ci --omit=dev / pnpm deploy --prod before the copy · COPY --chown=10001:10001 · build tools only in the builder
```
**Read the code:** Is the prune before the copy (or in the runtime stage)? Is the tool needed at runtime (a comment, a feature that shells out)? `VOLUME` followed by a write is **not** a finding under BuildKit (the write is kept [V]); it is a candidate only on a legacy builder `[K?]`.

**Finding when** builder residue, dev dependencies or compilers ship, or ownership doubles the layer. **Proof (V240):** container-structure-test file and command tests (`--platform` set) find no dev dependency or build tool in the runtime image; `docker history` shows the layer sizes.

### 9. The build-check lane (CT-D02, D08, D13, D19, D21–D23)

```
BAD:   CMD ["node", "worker.js"] / CMD ["node", "server.js"]   (only the last counts)
       a file hadolint did not parse, reported as "hadolint: 0 findings"
       RUN apt-get update   (alone; the install is a later RUN that reuses this cached index)
GOOD:  one CMD per stage · hadolint DL1000 → that file NOT-RUN in the ledger, the fix re-parses it
       RUN apt-get update && apt-get install -y --no-install-recommends … (one RUN)
```
**Read the code:** Map each rule id to its §: DL3025/`JSONArgsRecommended` → §2; DL3000/`WorkdirRelativePath`, DL3003, DL4006, `UndefinedVar`, `UndefinedArgInFrom` → §5; DL3029/`FromPlatformFlagConstDisallowed` → §7; DL3066 → §1; DL4003/`MultipleInstructionsDisallowed` → here. A lone `apt-get update` fires no `--check` or hadolint rule, so the awk prints `APT-UPDATE-ALONE` for it whether this lane ran or not. DL3008/DL3018 pins are not findings unless reproducibility is claimed (precedents § 32). DL3002, DL3006, DL3007, DL3064, `SecretsUsedInArgOrEnv` → security. A tool that did not parse or resolve is NOT-RUN (§ 41).

**Finding when** a kept rule fires on a shipped Dockerfile. **Proof (V237):** `--check` with `# check=error=true` and hadolint `--failure-threshold warning` report 0 kept rule ids.

### 10. Reproducibility and size (CT-P01–P05, CT-R10)

```
BAD:   README: "reproducible builds, SLSA Build L3"  ·  FROM golang:1.26-bookworm (tag) · no SOURCE_DATE_EPOCH · no rewrite-timestamp
       api image 260 MB against a recorded 180 MB baseline with no dependency change
GOOD:  base by digest + a bot · SOURCE_DATE_EPOCH + --output type=image,rewrite-timestamp=true · the baseline in ai/runbooks/docker.md
```
**Read the code:** Does the repo **claim** reproducibility (grep 10)? Without a claim, these are Hardening. What does the BuildKit version and compatibility version say? Did the dependency set change since the baseline (`/dockerize` Phase 7)?

**Finding when** a claimed-reproducible build differs between two builds of one commit, or the size grows past `THR-IMAGE-GROWTH` (20 %, a proposal: measure the repo's own size history before relying on it) with no dependency change (precedents § 39). **Proof:** V242 — two `--no-cache` builds with one `SOURCE_DATE_EPOCH` give an empty `diffoci diff --semantic`. V243 — `docker image inspect -f '{{.Size}}'` and `dive` stay within `THR-IMAGE-GROWTH` of the baseline.

## Proof

The oracles are in [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § DevOps. **Scope: scratch builds with throwaway tags, `${TMPDIR}`, and a throwaway kind cluster through an isolated `--kubeconfig=<scratch>` — never the user's registry, default kube context or cloud profile. Nothing is pushed.**

| § | Oracle | Tier | V |
|---|---|---|---|
| 1 | Image-config user + cst `metadataTest.user` + a `runAsNonRoot` dry run | B | V235 |
| 2 | Stop timing on the real base; an in-flight request completes | B | V231 |
| 3, 4 | Touch a source file → install `CACHED`; mutated lockfile → build fails | B | V236 |
| 5, 9 | `--check` (`check=error=true`) + hadolint threshold: 0 kept rule ids; a seeded failing line fails the build | T + B | V237 |
| 6 | `.State.Health.Status` = healthy within the window | B | V238 |
| 7 | Per-platform smoke; `imagetools inspect` platform list | B | V239 |
| 8 | container-structure-test file and command tests | B | V240 |
| 10 | Rebuild diff (`diffoci --semantic`); size vs baseline | B | V242, V243 |

## Output

```
container-build-scan — 21 Dockerfiles (19 built by an invocation) · lanes: node, python, go, static · frontend: bundled (3 files pin docker/dockerfile:1.6)
Tools: --check 20/21 ran (1 NOT-RUN: base unresolved) · hadolint 19/21 parsed (2 NOT-RUN: DL1000) · checkov NOT-INSTALLED · docker: yes · security: installed

1. services/api/Dockerfile:15                                             [report-with-fix]   high
   §2 CT-D03 — shell-form `CMD node dist/main.js` on node:22-bookworm-slim: sh stays PID 1. Proof: V231 on a
   scratch build, docker stop 10.2 s, exit 137. Fix: `CMD ["node", "dist/main.js"]` behind `ENTRYPOINT ["tini", "--"]`.

2. services/api/Dockerfile:13                                             [report-with-fix]   medium
   §6 CT-D09 — HEALTHCHECK calls curl; the base ships neither curl nor wget, and docker-compose.yml:17 gates edge on
   `service_healthy`. Proof: V238 status `unhealthy` after 120 s. Fix: the `node -e "fetch(…)"` check (GOOD shape).

3. services/worker/worker.Dockerfile:4                                    [report-flagged]    medium
   §4 CT-D17 — `pnpm install` without --frozen-lockfile in the image CI builds (.github/workflows/build.yml:14).
   Unproven link: no scratch build with a mutated lock. Settling test: V236 lock probe.

Verification: 64 candidates → 3 findings · 4 unconfirmed · 9 hardening · 0 pre-existing · 41 refuted (self-verified) · 7 routed

Class coverage:
  §1  stage-chain user / CT-D14     checked (21 chains → 1 CT-D14 finding; 2 ROOT routed to security; 3 INHERIT-EXTERNAL refuted § 33)
  §2  PID 1                         checked (8 PID1 rows → 1 finding, 2 unconfirmed; alpine shell form refuted § 35)
  §3  layer order / ignore file     checked (1 LAYER-ORDER, 2 ignore rows → hardening)
  §4  lockfile in the build         checked (3 hits → 1 unconfirmed, 2 hardening)
  §5  RUN correctness               checked (6 rows → 1 unconfirmed; RUN cd, WORKDIR → hardening)
  §6  HEALTHCHECK                   checked (2 rows → 1 finding; HC-NONE ×18 refuted § 29 except 1 gated image)
  §7  base / platform / libc        checked (EOL read 2026-10-10: 1 unconfirmed; floating + bot refuted § 31)
  §8  runtime content               checked (4 rows → 2 hardening; VOLUME write refuted [V BuildKit])
  §9  build-check lane              Live, unreviewed (2 files NOT-RUN under hadolint: DL1000)
  §10 reproducibility / size        checked (1 claim → 1 unconfirmed: V242 needs two builds; size: blocked (no baseline build))
  R   routed                        ARG NPM_TOKEN, curl -k, wget --no-check-certificate, FROM node (untagged), USER 0:0 → security iac-scan §1
```

`[report-with-fix]`: the stage, the invocation that ships it, the base fact and the oracle are in hand, and the fix is local to the Dockerfile. `[report-flagged]`: one link is unproven — no scratch build, a base config not read, a target not resolved, a tool NOT-RUN. The row names the link and the settling test.

The coverage block lists **all ten** §s and the R lane on every run: `checked (k hits → m findings)` only when the lane ran on a present surface; `N/A (no Dockerfile)`; `blocked (<reason>)` for a failed grep or a NOT-RUN tool on the files it owns; `Unconfirmed (…)` when only a B-tier run can decide; `Live, unreviewed (k groups / n hits)` for a partial review.

## False positives / precedents

The verifier reads [`precedents/devops.md`](../../../../snippets/precedents/devops.md) and [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 4. The ones this skill meets most:
- **§ 29** No HEALTHCHECK on a Kubernetes-only image. **§ 30** Distroless and scratch self-checks. **§ 31** A floating minor tag with a bump bot. **§ 32** DL3008/DL3018 pins.
- **§ 33** Read the base's user before `INHERIT-EXTERNAL` counts. **§ 34** `COPY . .` after a manifest-first install. **§ 35** Shell form on alpine. **§ 36** `STOPSIGNAL SIGQUIT`.
- **§ 37** A numeric USER is the k8s-verifiable form. **§ 38** Builder stages count only for build-time classes. **§ 39** Size against the baseline. **§ 40** A dev-only compose file (for the §6 gate join).
- **§ 41** A tool that errored, parsed nothing or could not resolve a base is NOT-RUN. **§ 5** One finding per shared base stage. §§ 42–46 (Helm, the GitHub shell, YAML loaders, `act`) do not arise here.

Read-step rules measured on 2026-10-10, applied with a `file:line`: a pipe into `grep -q` is a condition, not a masked producer; a static `dist/` copied across libcs is not a libc mismatch; `node_modules/.prisma` is a generated client, not the dev tree; a pod `runAsUser` clears CT-D14; `ENV CI=true` does not freeze pnpm 9.15.9.

Rationalizations to reject:
- "It built, so the Dockerfile is fine": a heredoc, an empty ARG and an unfrozen lockfile all build green.
- "Exec form, so signals work": with no handler and no init, PID 1 ignores SIGTERM for 10 s, then 137.
- "hadolint is clean": did it parse the file (`DL1000`)?
- "We set CI=true": it did not freeze pnpm inside the build.

## When to run

- On any diff touching a Dockerfile or Containerfile, an ignore file, an entrypoint script, a build invocation (CI `build-push-action`, compose `build:`, bake), or a lockfile an image installs from.
- From `/dockerize` Phase 6 on the Dockerfile it generated, before its smoke test; after a base-image bump; after a `/devops-fix` on a container row.
- On every whole-repo `/devops-audit`, reporting all ten §s.

## Halt conditions

- **Do not report a critical or high row as confirmed until a separate verifier has refuted it.** That verifier is not the run that found it; it applies [`refute-before-report.md`](../../../../snippets/refute-before-report.md) with `precedents/devops.md`. Under `/devops-audit` that is its verification phase; standalone, run the protocol as a second pass and tag those rows `self-verified`. List the rest as Unconfirmed, Hardening, Pre-existing or Refuted; never drop them.
- **Halt on a finding missing its anchors:** the line, the stage, the base and family, the invocation that ships it, and the fix.
- **No runtime verdict from a builder stage**, and no shipped-stage verdict without the target 0a names.
- **No `checked` on a file a tool did not read:** hadolint `DL1000`, an unresolved base under `--check`, an rg exit 2 are `blocked`.
- **Never push, tag over, or pull-by-credentials against the user's registry; never use the default kube context.** B-tier runs build scratch tags and remove them; the CT-D14 dry run uses an isolated `--kubeconfig=<scratch>`.
- **No proposed fix may weaken a control to clear a row:** no `# hadolint ignore=`, `# check=skip=`, deleted HEALTHCHECK, `USER root`, or `CI=false`.
- **Do not print "the Dockerfile looks fine" without the coverage block.** **Do not re-derive a class another skill owns** (§ Boundaries); cross-link it.

## Related

- `/devops-audit` dispatches this skill on a Dockerfile or ignore-file signal and folds its coverage block into the container rows; `/devops-fix` closes them with V231–V243. `/dockerize` runs it in Phase 6 and records the size baseline in Phase 7.
- `@deployment-engineer` judges these rows; `@devops-architect` designs the images this skill then judges.
- `deploy-safety-scan` §5 (handler and drain), `compose-scan`, `release-integrity-scan`, `release-security`, `pipeline-cache-scan` §2 and `pipeline-integrity-scan` §1 (this pack) own the neighbouring classes.
- `iac-scan` §1 (security; root, secrets, fetches, tag mutability) and `k8s-availability-scan` §7 (infrastructure; grace arithmetic), each when its pack is installed.

## Sources

Classes and tool behaviour from the devops research catalog's containers notes (CT-D/CT-P/CT-R taxonomy, the `--check`/hadolint/trivy/checkov matrix and the node:22 stop-timing matrix, measured 2026-10-10) and the batch-4 devops eval (DV-5, the stage-chain awk verified 6/6). This skill's own measurements on 2026-10-10 (docker engine 29.5.2, buildx 0.37.1, hadolint 2.15.1, pnpm 9.15.9 via corepack): the heredoc, empty-ARG USER, pnpm `CI=true`, curl/wget presence, `VOLUME` write, ignore-file precedence, `--check` resolution and frontend-version, and hadolint `DL1000` probes, all on scratch images removed afterwards. Paraphrased; no text reproduced beyond identifiers.
