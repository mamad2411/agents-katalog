---
name: quickstart-verify
description: "Run a doc's setup steps in a disposable, offline container pinned to the repo's versions, never on the host; static pre-pass otherwise."
kind: skill
pack: documentation
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: quickstart-verify

## Premise

A setup section that reads correctly does not prove a newcomer can follow it. The maintainer's machine already has the tool the prerequisites forgot, the database the migrate step assumes is running, the `.env` nobody said to create. Naive execution of more than 600 tutorials succeeded for 26% of code blocks, and no tutorial ran every step (Docable, FSE 2020); "commands not mentioned" is the top install failure (Installamatic). This skill stops trusting the prose and **runs the documented steps, in order, as written, in a container that has none of that warm state**.

It owns **DS-1, the setup sequence fails in a clean environment**, in four §s: §1 a missing prerequisite, §2 a renamed or missing command, §3 a wrong order or an assumed warm state, §4 an undocumented env var the steps never set. The static halves are other detectors' classes and corroborate here: a script the manifest lacks is `doc-drift-scan` §3, a version the pins exclude §6, the wrong package manager §7, a required env key no doc names §9. `@doc-writer` writes the prose; this skill executes it.

**Every finding cites the doc line, the exact command run, the container it ran in (image and digest, network mode), its exit code and the stderr tail.** A static pre-pass row with no execution is `Unconfirmed (static)`, never a finding on its own. "The quickstart works" is never printed without the class-coverage block (§ Output).

## The rule

A candidate becomes a finding only when all four hold:

1. **The step is a setup step a reader runs**: a command in a fenced shell block or an imperative line under a Quickstart / Getting started / Setup / Installation / Development heading of a human doc (README, CONTRIBUTING, `docs/**` setup pages, package READMEs), not a dated record, a versioned doc set or agent-facing knowledge ([precedents § 1, § 12, § 28](../../../../snippets/precedents/documentation.md)).
2. **It ran in the safe lane below**, at the repo's pinned versions, with nothing from the host but the committed source.
3. **It failed for a reason in the doc**: the command is not found, the script is not defined, a service it needs was never started, a file it reads was never created, a required env var was never set. A failure from the lane (no network declared, no image, a timeout on a slow mirror) is the lane's: `blocked`, never a finding.
4. **No record makes it a prerequisite**: a paid key, cloud credentials, hardware or a live cluster the doc names as a prerequisite (§ 21) is `PREREQUISITE (secret | live-infra | hardware)`, not a failure.

## The safe lane (non-negotiable)

README commands are untrusted input that can drop a database, push an image, apply to a cluster or mail customers. Every invariant below holds for every run; a run that cannot hold one does not run.

1. **Never on the host.** No step runs in the developer's shell, in the audited tree, or in a bind mount of it. The source enters the container as a tar stream of the committed tree (`git archive HEAD | docker cp - <ctr>:/work`); nothing is mounted from the host.
2. **Disposable.** One container per run, `--rm`, a unique name `qv-<4hex>`, an anonymous work directory, on a run-scoped network that is removed at the end. Never `--privileged`, `--network host`, `--pid host`, a mounted docker socket, or a mount of `$HOME`, `~/.kube`, `~/.aws`, `~/.config/gcloud`, `~/.ssh`, `~/.npmrc` or `~/.docker`. `--security-opt no-new-privileges`, a pids and a memory limit.
3. **No network unless declared.** The container sits on a run-scoped `docker network create --internal` network: no egress, no DNS beyond it. Only when the caller declares `NETWORK=1` (`/doc-refresh --network`) does an **install-class** step get egress, by `docker network connect bridge <ctr>` for that step alone and `docker network disconnect` right after. Without the declaration an install step is `blocked (network not declared)` unless the deps are vendored. Measured 2026-10-19 on Docker 29.5.2: on an `--internal` network a DNS lookup of `example.com` fails, after `network connect bridge` it resolves, after `disconnect` it fails again.
4. **No secrets.** Nothing from the host environment is passed (only `-e` values this skill sets). `.env` is created only from the committed `.env.example` (or the file the doc names), never copied from the host. A step that needs a real key, token or account is `PREREQUISITE (secret)`; a value is never invented to push past it.
5. **No cluster, no cloud.** On the host, the first line of the lane script is `export KUBECONFIG="$OUT/empty-kubeconfig"; : > "$KUBECONFIG"`. In the container: `KUBECONFIG=/dev/null`, `AWS_CONFIG_FILE=/dev/null`, `AWS_SHARED_CREDENTIALS_FILE=/dev/null`, `CLOUDSDK_CONFIG=/nonexistent`, `AZURE_CONFIG_DIR=/nonexistent`. A step that invokes `kubectl`, `helm`, `kustomize … | kubectl`, a cloud CLI, `terraform apply`, `pulumi up` or a deploy CLI is never run: `PREREQUISITE (live-infra)`.
6. **Nothing leaves.** A publish step (`npm publish`, `docker push`, `git push`, `twine upload`, `cargo publish`, `gh release`) is never run: `SKIPPED (publishes)`. A step whose URL is not `localhost`, `127.0.0.1` or a compose service name is never run: `PREREQUISITE (external service)`. A destructive step against anything but the container's own files is never run.
7. **Telemetry off**: `CI=true DO_NOT_TRACK=1 NEXT_TELEMETRY_DISABLED=1 NUXT_TELEMETRY_DISABLED=1 ASTRO_TELEMETRY_DISABLED=1 GATSBY_TELEMETRY_DISABLED=1 STORYBOOK_DISABLE_TELEMETRY=1 DOTNET_CLI_TELEMETRY_OPTOUT=1 HOMEBREW_NO_ANALYTICS=1 TURBO_TELEMETRY_DISABLED=1 REDOCLY_TELEMETRY=off` (precedents § 34).
8. **A time budget per step**, enforced inside the container with `timeout` (15 min for install, 5 min otherwise; macOS has no `timeout` on the host, so the budget never runs host-side). A timeout is `blocked (timeout)`, never a pass.
9. **Pinned, never guessed.** The image comes from the repo: `.devcontainer/devcontainer.json` `image`, else the runtime pin (`.nvmrc` / `engines` / `.tool-versions` / `.python-version` / `requires-python` / `go.mod` `go` / `rust-toolchain(.toml)`) mapped to the official image, else the Dockerfile's first `FROM`. No pin is `blocked (no runtime pin)`. An image that is not local is pulled only under `NETWORK=1`; otherwise `blocked (image not local)`.
10. **No daemon, no run.** With no container runtime the lane is `blocked (no container runtime)` and the static pre-pass stands; a warm-host run is forbidden, and this skill never starts a VM (colima, Docker Desktop, podman machine) on its own.
11. **The write check**: `find . -newer "$OUT/stamp"` on the audited tree prints nothing.

Compose services a step brings up (`docker compose up -d db`) are never run through a nested docker. When the service has an `image:` the runner starts it as a sibling container on the same internal network with the service name as its alias (no `build:`, no host ports, no volumes, non-secret `environment:` only); a `build:` service is `PREREQUISITE (service build)`.

## Lanes

| Stack | Pin → image | Install-class steps | Notes |
|---|---|---|---|
| Node / TS | `.nvmrc`, `engines.node`, `volta` → `node:<v>-bookworm-slim`; `packageManager` via corepack | `pnpm install`, `npm ci`, `yarn install`, `bun install` | `corepack enable` needs the registry under `NETWORK=1`; `--frozen-lockfile` is the doc's choice, not the runner's |
| Python | `.python-version`, `requires-python` → `python:<x.y>-slim` | `pip install`, `uv sync`, `poetry install`, `pdm install` | a step using `uv` or `poetry` with neither listed as a prerequisite is §1 |
| Go | `go.mod` `go` line → `golang:<x.y>` | `go mod download` | `GOFLAGS=-mod=mod` only if the doc says so |
| Rust | `rust-toolchain(.toml)` → `rust:<v>` | `cargo fetch`, `cargo build` | caches stay in the container |
| JVM / .NET / PHP / Ruby | `.java-version`, `global.json`, `composer.json` `php`, `.ruby-version` → the official image | `./gradlew build`, `dotnet restore`, `composer install`, `bundle install` | a Gradle wrapper download needs `NETWORK=1` |
| devcontainer | `.devcontainer/devcontainer.json` `image` | as the stack | a devcontainer with `build:` or features is `checked · partial`: the lane uses its base image |
| Nix | `flake.nix` / `shell.nix` | `nix develop` | `checked · partial` [K?]: needs a Nix image and the network |

A lane marked partial prints `checked · partial` in the coverage block, never plain `checked`.

## Pre-flight

Run as **one** script from the repo root (bash 3.2-safe). Part 1, the static pre-pass, always runs; part 2, the container lane, runs unless `NO_EXEC=1` (`/doc-refresh --no-exec`). `DOCS` overrides the setup docs.

```bash
export KUBECONFIG="${TMPDIR:-/tmp}/qv-empty-kubeconfig"; : > "$KUBECONFIG"
DC="${DC:-.claude/skills/doc-drift-scan/scripts/doc-claims.py}"; NETWORK="${NETWORK:-}"; NO_EXEC="${NO_EXEC:-}"
OUT="$(mktemp -d "${TMPDIR:-/tmp}/quickstart.XXXXXX")"; export GIT_OPTIONAL_LOCKS=0 CI=true DO_NOT_TRACK=1; : > "$OUT/stamp"
ck() { [ "$2" -lt 2 ] || echo "$1 BLOCKED (rg exit $2) — never 0 hits"; }
DOCS="${DOCS:-$(rg --files -g '{README,CONTRIBUTING,INSTALL,DEVELOPMENT,SETUP,GETTING_STARTED}*.md' -g 'docs/**/{setup,getting-started,installation,install,development,quickstart}*.md' -g '!**/node_modules/**' -g '!docs/v[0-9]*/**' . | tr '\n' ',' | sed 's/,$//')}"; echo "setup docs: ${DOCS:-none}"
# 1a. The steps: every shell command under a setup heading, in order, classified (never executed here).
python3 -I - "$DOCS" > "$OUT/steps.tsv" <<'PY'
import re, sys
H = re.compile(r'^(#{1,4})\s+(.*)$'); F = re.compile(r'^\s*(`{3,}|~{3,})\s*([\w-]*)')
SETUP = re.compile(r'(?i)quick ?start|getting started|set ?up|install|development|local|running|prerequisite|requirement')
K = [('live-infra', r'^(kubectl|helm|kustomize|aws|gcloud|az|terraform|pulumi|flyctl|vercel|netlify|heroku|doctl|eksctl)\b'),
     ('publish', r'^(npm|pnpm|yarn) publish|^docker (push|buildx .*--push)|^git push|^twine upload|^cargo publish|^gh release'),
     ('service', r'^docker[- ]compose\b.*\bup\b|^docker run\b'), ('env', r'^(cp|copy)\s+\S*\.env|^export\s+\w+=|^\w+=\S* *$'),
     ('install', r'^(pnpm|npm|yarn|bun) (i|install|ci)\b|^(pip|pip3) install|^uv (sync|pip)|^poetry install|^pdm install|^go mod download|^cargo (fetch|build)|^bundle install|^composer install|^dotnet restore|^corepack '),
     ('external', r'https?://(?!localhost|127\.0\.0\.1|0\.0\.0\.0)'), ('destructive', r'\brm -rf /|\bdrop (database|table)\b|--force\b|\bprune\b'),
     ('migrate', r'migrat|seed|db:'), ('smoke', r'^(curl|wget|http|open)\b')]
for doc in [d for d in sys.argv[1].split(',') if d]:
    lv, on, inf, buf = 0, False, False, ''
    for n, line in enumerate(open(doc, encoding='utf-8', errors='replace'), 1):
        m, f = H.match(line), F.match(line)
        if m and not inf:
            l = len(m.group(1)); on = bool(SETUP.search(m.group(2))) or (on and l > lv); lv = l if SETUP.search(m.group(2)) else lv
        elif f:
            inf = not inf; sh = f.group(2) in ('', 'bash', 'sh', 'shell', 'zsh', 'console', 'terminal')
        elif inf and on and sh and line.strip() and not line.lstrip().startswith('#'):
            c = re.sub(r'^\s*[$>] ', '', line.rstrip('\n')).strip(); buf += c[:-1] + ' ' if c.endswith('\\') else c
            if not c.endswith('\\'):
                for part in [p.strip() for p in re.split(r'\s*&&\s*', buf) if p.strip()]:
                    kind = next((k for k, r in K if re.search(r, part, re.I)), 'run')
                    print('%s\t%d\t%s\t%s' % (doc, n, kind, part))
                buf = ''
PY
echo "steps: $(wc -l < "$OUT/steps.tsv" | tr -d ' ')"; cut -f3 "$OUT/steps.tsv" | sort | uniq -c
# 1b. Corroboration: the drift lanes on the same docs (scripts §2, versions and tools §1, env §4).
[ -f "$DC" ] && { python3 -I "$DC" . --lanes=scripts,flags,paths,versions,tools,env --docs="$DOCS" > "$OUT/claims.tsv" 2> "$OUT/ledger.txt"; echo "doc-claims exit $? (0 clean · 1 candidates · 2 BLOCKED)"; cut -f3,5,6,7 "$OUT/claims.tsv"; } || echo "corroboration UNVERIFIED (doc-drift-scan not installed)"
# 1c. Tools the steps call that the prerequisites never name (§1), and the services they assume (§3).
cut -f4 "$OUT/steps.tsv" | awk '{print $1}' | sort | uniq -c | sort -rn       # every tool a step calls: each must be in the image or in the doc's prerequisites
awk -F'\t' '$3=="service"&&!s[$1]{s[$1]=1; if(e[$1]) print "§3 candidate (static): " e[$1] " runs before " $1 ":" $2 " starts the service"} ($3=="migrate"||$3=="run")&&!s[$1]&&!e[$1]{e[$1]=$1":"$2" "$4}' "$OUT/steps.tsv"
python3 -I - "$OUT/steps.tsv" <<'PY'
import re, sys
BUILTIN = {'cd', 'cp', 'copy', 'export', 'echo', 'cat', 'mkdir', 'ls', 'source', '.', 'set', 'mv', 'sh', 'bash', 'curl', 'open'}
steps = [l.rstrip('\n').split('\t') for l in open(sys.argv[1]) if l.strip()]
prose = {d: re.sub(r'(?ms)^\s*(`{3,}|~{3,}).*?^\s*\1', '', open(d, encoding='utf-8', errors='replace').read()).lower() for d in {s[0] for s in steps}}
seen, first_env = set(), {}
for d, n, k, c in steps:
    tool = c.split()[0]
    if k == 'env' and d not in first_env: first_env[d] = int(n)
    if tool in BUILTIN or (d, tool) in seen: continue
    seen.add((d, tool))
    if not re.search(r'\b' + re.escape(tool.lower()) + r'\b', prose[d]): print('§1 candidate (static): %s:%s `%s` — the doc never names `%s` outside a fence' % (d, n, c, tool))
for d, n, k, c in steps:
    if k in ('migrate', 'run') and d in first_env and int(n) < first_env[d]: print('§3 candidate (static): %s:%s `%s` runs before %s:%d creates the env file' % (d, n, c, d, first_env[d]))
PY
rg -n --pcre2 '^\s*(?:services:|\s{2}\w[\w-]*:\s*$)|\b(?:DATABASE_URL|REDIS_URL|AMQP_URL)\b' -g 'docker-compose*.{yml,yaml}' -g 'compose*.{yml,yaml}' -g '.env.example' . | head -20; ck 1c $?
# 2. The container lane (skipped with NO_EXEC=1; blocked with no runtime, no pin, or an image that is not local without NETWORK=1).
if [ -n "$NO_EXEC" ]; then echo "container lane NOT-RUN (--no-exec)"; elif ! docker info >/dev/null 2>&1; then echo "container lane blocked (no container runtime)"; else
  IMG=""; [ -f .devcontainer/devcontainer.json ] && IMG=$(python3 -I -c 'import json,re;t=re.sub(r"(?m)^\s*//.*$","",open(".devcontainer/devcontainer.json").read());print(json.loads(t).get("image",""))' 2>/dev/null)
  [ -z "$IMG" ] && [ -f .nvmrc ] && IMG="node:$(tr -d 'v \n' < .nvmrc)-bookworm-slim"
  [ -z "$IMG" ] && [ -f .python-version ] && IMG="python:$(cut -d. -f1,2 .python-version | tr -d '\n')-slim"
  [ -z "$IMG" ] && [ -f go.mod ] && IMG="golang:$(awk '/^go /{print $2; exit}' go.mod)"
  [ -z "$IMG" ] && [ -f Dockerfile ] && IMG=$(awk 'toupper($1)=="FROM"{print $2; exit}' Dockerfile)
  if [ -z "$IMG" ]; then echo "container lane blocked (no runtime pin: the image is never guessed)"
  elif ! docker image inspect "$IMG" >/dev/null 2>&1 && { [ -z "$NETWORK" ] || ! docker pull -q "$IMG" >/dev/null; }; then echo "container lane blocked (image $IMG not local; pulling needs NETWORK=1)"
  else CTR="qv-$(python3 -I -c 'import secrets;print(secrets.token_hex(2))')"; NET="$CTR-net"; docker network create --internal "$NET" >/dev/null
    docker run -d --rm --name "$CTR" --network "$NET" --security-opt no-new-privileges --pids-limit 512 --memory 4g -w /work \
      -e CI=true -e DO_NOT_TRACK=1 -e NEXT_TELEMETRY_DISABLED=1 -e TURBO_TELEMETRY_DISABLED=1 -e STORYBOOK_DISABLE_TELEMETRY=1 -e DOTNET_CLI_TELEMETRY_OPTOUT=1 -e REDOCLY_TELEMETRY=off \
      -e KUBECONFIG=/dev/null -e AWS_CONFIG_FILE=/dev/null -e AWS_SHARED_CREDENTIALS_FILE=/dev/null -e CLOUDSDK_CONFIG=/nonexistent -e AZURE_CONFIG_DIR=/nonexistent \
      --entrypoint sleep "$IMG" 7200 > /dev/null && docker exec "$CTR" sh -c 'mkdir -p /work /tmp/qv && echo /work > /tmp/qv/cwd && : > /tmp/qv/env && command -v timeout' > /dev/null || { echo "container lane blocked (container did not start, or no timeout in $IMG)"; : > "$OUT/steps.tsv"; }
    git archive HEAD | docker cp - "$CTR":/work; echo "container $CTR on $IMG ($(docker image inspect -f '{{index .RepoDigests 0}}' "$IMG" 2>/dev/null)), network internal"
    T0=$(date +%s); i=0; svc=""; while IFS="$(printf '\t')" read -r doc line kind cmd; do i=$((i+1))
      case "$kind" in service) svc="$cmd"; echo "step $i $doc:$line PREREQUISITE (service — start each compose image: as a sibling on $NET, never nested docker): $cmd"; continue;; live-infra) echo "step $i $doc:$line PREREQUISITE (live-infra): $cmd"; continue;; publish) echo "step $i SKIPPED (publishes): $cmd"; continue;; external|destructive) echo "step $i $doc:$line PREREQUISITE ($kind): $cmd"; continue;; esac
      B=300; [ "$kind" = install ] && B=900
      if [ "$kind" = install ]; then [ -n "$NETWORK" ] && docker network connect bridge "$CTR" || { echo "step $i $doc:$line blocked (network not declared): $cmd"; continue; }; fi
      docker exec "$CTR" timeout "$B" sh -c 'cd "$(cat /tmp/qv/cwd)"; . /tmp/qv/env; '"$cmd"'; rc=$?; pwd > /tmp/qv/cwd; export -p > /tmp/qv/env; exit $rc' > "$OUT/step$i.out" 2> "$OUT/step$i.err"; rc=$?
      [ "$kind" = install ] && [ -n "$NETWORK" ] && docker network disconnect bridge "$CTR"
      if [ $rc -ne 0 ] && [ $rc -ne 124 ] && [ -n "$svc" ] && grep -qiE 'ECONNREFUSED|connection refused|could not connect|getaddrinfo|ENOTFOUND' "$OUT/step$i.err"; then echo "step $i $doc:$line blocked (service from '$svc' not started in the lane): $cmd"; break; fi
      case $rc in 0) echo "step $i $doc:$line PASS ($kind): $cmd";; 124) echo "step $i $doc:$line blocked (timeout ${B}s): $cmd";; *) echo "step $i $doc:$line FAIL exit $rc ($kind): $cmd — $(tail -2 "$OUT/step$i.err" | tr '\n' ' ')"; break;; esac
    done < "$OUT/steps.tsv"; echo "elapsed $(( $(date +%s) - T0 ))s"
    docker stop "$CTR" > /dev/null; docker network rm "$NET" > /dev/null; fi; fi
find . -newer "$OUT/stamp" -type f -not -path './.git/*' -not -path './node_modules/*' | head -3; echo "write check done (empty = nothing written)"
```

A `run` step that starts a server is started detached (`docker exec -d`), and the next `smoke` step (the doc's own `curl http://localhost:<port>/…`) is retried for up to its budget; an image without `curl` uses its runtime (`node -e "fetch(…)"`, `python3 -c "urllib.request…"`). Each `cd` and `export` a step makes carries to the next through `/tmp/qv/cwd` and `/tmp/qv/env`, as it would in the reader's shell.

## Measured

Measured 2026-10-19. The isolation itself, on Docker 29.5.2 (colima): a `python:3.10` container on an `--internal` network failed a DNS lookup of `example.com` (exit 1), resolved it after `docker network connect bridge` (exit 0) and failed again after `disconnect`; `timeout` was present at `/usr/bin/timeout`; the container and network were removed and no `qv-*` object remained. On the seeded `benchmarks/fixtures/doc-drift` copy (history staged, write check empty): 8 setup docs, 19 steps (4 install, 3 env, 2 service, 4 migrate, 6 run); the static pre-pass printed 7 candidates — both DS-1 seeds (README `docker compose …` with Docker named nowhere in the prose, §1; CONTRIBUTING `db:migrate` before the step that creates `.env`, §3), the two DS-3 lines `doc-drift-scan` §7 already owns (`npm install`, `yarn start:dev`), and three §1 rows read as Hardening (`pnpm add` in a consumer README, `make`, `pip`); the corroboration lanes printed 12 drift rows on the setup docs. The container lane printed `blocked (image node:22-bookworm-slim not local; pulling needs NETWORK=1)`: no image was pulled and no step ran, so both seeds stay `Unconfirmed (static)` and the audit is GO-UNVERIFIED on SETUP RUNS, as designed. The first extractor missed DS-1 §3 when the warm-state step was a migrate before `cp .env.example` with no `.env` in its own text; the order check now compares every migrate and run step with the doc's first env step.

## The 3,000-row path

A monorepo with forty package READMEs has forty setup sections, most of them copies.
1. **Primary first.** The root README and CONTRIBUTING quickstart run in the container; package READMEs get the static pre-pass and run only when they carry a distinct sequence.
2. **Group by failing command.** One renamed script that breaks twelve READMEs is one finding with twelve sites (`doc-claims.py --claim=<command>` lists them).
3. **Stop at the first hard failure** of a sequence: everything after it is `not reached`, never FAIL.
4. **Close a group with one checked reason** (`9 PREREQUISITE (live-infra): kubectl steps in deploy READMEs, § 19`), and ledger the rest `Live, unreviewed (k sections)`.

## Scans for

| § | Class | Static pre-pass | Container lane | Finding when | Default (primary) | Oracle |
|---|---|---|---|---|---|---|
| 1 | DS-1 missing prerequisite | a tool or runtime a step calls that the prerequisites never name; a pin the doc's runtime claim excludes (corroborated by `doc-drift-scan` §6) | exit 127 `command not found`, a version check failing | the clean image lacks what the step needs and the doc never says to install it | HIGH | V437 |
| 2 | DS-1 renamed or missing command | `doc-drift-scan` §3 / §4 rows on the setup docs | `Missing script`, `No rule to make target`, an unknown flag | the command the doc gives does not exist where it runs | HIGH | V437 |
| 3 | DS-1 wrong order or warm state | a migrate or seed step before the service it needs; a step reading `.env` before the step that creates it; build before install | a connection refused, a missing file a later step creates | the sequence fails as written and passes reordered | HIGH | V437 |
| 4 | DS-1 undocumented env | a required schema key no setup step sets (corroborated by `doc-drift-scan` §9) | the app exits on a missing variable | boot fails on a variable the steps never set and `.env.example` does not carry | HIGH | V437 |

On a secondary surface (an internal how-to, a package README nobody links) each row is one step lower.

### 1. Missing prerequisite

```
BAD:   README.md:18   pnpm install            (prerequisites list Node 22 only; corepack not enabled: "pnpm: not found", exit 127)
       CONTRIBUTING.md:30   uv sync           (prerequisites name pip; uv is never mentioned)
GOOD:  "Prerequisites: Node 22, `corepack enable` (pnpm 10)" · "Install uv (https://docs.astral.sh/uv/)"
```
**Read the docs and the run:** Is the missing tool part of the official image (the image is the reader's best case, so a tool the image lacks is one a newcomer lacks)? Does the doc point at a devcontainer that installs it? Is it a system package the doc mentions further down (an order problem, §3)? **Finding when** the step fails because a tool the doc never asks for is absent. **Proof:** V437, the step's exit and stderr, then the same step passing once the prerequisite is added in a fresh container.

### 2. Renamed or missing command

```
BAD:   README.md:24   pnpm dev:all    → ERR_PNPM_NO_SCRIPT  Missing script: dev:all    (package.json: dev, dev:api, dev:web)
GOOD:  pnpm dev
```
**Read the docs and the run:** Does the step run where the doc runs it (a preceding `cd`, a `--filter`)? Is the `doc-drift-scan` §3 row for the same line already a finding (then this is its execution proof, one finding)? **Finding when** the command is not defined where it runs. **Proof:** V437 plus V434.

### 3. Wrong order or assumed warm state

```
BAD:   README.md:30   pnpm db:migrate         README.md:34   docker compose up -d db      (connection refused at :30)
GOOD:  start the database first, then migrate
```
**Read the docs and the run:** Would the step pass on a warm machine (a database already running, a `.env` from last month)? That is this class exactly. Is the order platform-branched ("on macOS…")? Run the branch the image matches; never flag the other. **Finding when** the sequence fails as written and the same steps pass reordered in a fresh container. **Proof:** V437, both runs recorded.

### 4. Undocumented env

```
BAD:   apps/api boots → "PAYMENTS_WEBHOOK_SECRET: Required"     (env.schema.ts: z.string(); no step sets it; .env.example lacks it)
GOOD:  .env.example carries it with a dev value or a comment, and the setup says to copy the file
```
**Read the docs and the run:** Is the variable a secret (then the doc must name it as a prerequisite, § 21, and the row is `PREREQUISITE (secret)` once it does)? Is it set by the compose file the doc runs? **Finding when** boot fails on a variable no step and no example provides. **Proof:** V437; corroborate with `doc-drift-scan` §9 and backend `env-diff` when the backend pack is installed.

## Output

```
quickstart-verify — README.md § Quickstart · 7 steps · image node:22-bookworm-slim (sha256:…) · network internal (NETWORK not declared)

Step  Doc line        Kind      Command                          Result
1     README.md:18    install   corepack enable && pnpm install  blocked (network not declared)
2     README.md:22    env       cp .env.example .env              PASS
3     README.md:24    run       pnpm dev:all                      FAIL exit 1 — Missing script: dev:all
4–7                                                                 not reached
Time to first green: never (blocked at step 1, failed at step 3)

Findings: 1 · Unconfirmed: 2
1. README.md:24   [report-with-fix]  HIGH · DS-1 §2   `pnpm dev:all` — container exit 1 (Missing script); doc-drift-scan §3 row 3fa91c02d1. Fix: `pnpm dev`.
2. README.md:30   [report-flagged]   HIGH · DS-1 §3   Unconfirmed (static): `pnpm db:migrate` precedes `docker compose up -d db` (:34). Settles: NETWORK=1 run.
3. README.md:18   [report-flagged]   HIGH · DS-1 §1   Unconfirmed (static): pnpm used, prerequisites name Node only. Settles: NETWORK=1 run.

Class coverage:
  §1 missing prerequisite   checked · static (7 steps → 1 Unconfirmed); container blocked at step 1 (network not declared)
  §2 renamed command        checked (container step 3 → 1)
  §3 order / warm state     checked · static (1 Unconfirmed)
  §4 undocumented env       not reached (boot step 6 not reached)
  lane                      container ran (node:22-bookworm-slim, internal network, 3 of 7 steps) · PREREQUISITE 0 · SKIPPED 0
```

`[report-with-fix]`: the step ran in the safe lane and failed for a reason in the doc; the fix is a setup-doc edit (or the code, when the doc is the contract, § 16). `[report-flagged]`: the static pre-pass found it and the container did not reach it, or one link (a prerequisite, a platform branch) is unproven; the row names the run that settles it. Every run prints **all four** §s and the lane line as `checked`, `checked · static`, `not reached`, `N/A (no setup section)`, `blocked (<reason>)` or `NOT-RUN (--no-exec)`; a static-only pass is never PASS.

## Precedents

The verifier reads [`precedents/documentation.md`](../../../../snippets/precedents/documentation.md) and [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 4. The ones this skill meets most: § 6 placeholders in a step that must run, § 16 the doc is the contract, § 19 live infra and third-party CLIs, § 21 secrets, paid accounts and hardware, § 33 NOT-RUN is never PASS, § 34 telemetry. The oracle is [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Documentation, V437.

## When to run

- On every whole-repo `/doc-refresh --audit` (the static pre-pass always; the container lane unless `--no-exec`).
- On a diff that edits a setup section, a runtime pin, a manifest script, the env schema, `.env.example` or the compose file.
- Before a release, and when onboarding a contributor: the root quickstart, end to end, with `NETWORK=1`.

## Halt conditions

- Do not report a HIGH or BLOCKER row as confirmed until a verifier other than the run that found it has passed it through [`refute-before-report.md`](../../../../snippets/refute-before-report.md); under `/doc-refresh --audit` that is `@verifier` in refute mode. Run standalone, apply the protocol as a separate second pass, tag those rows `self-verified`, and keep the rest Unconfirmed, Hardening or Refuted. Never drop them.
- **Never run a doc's command on the host**, in the audited tree, or with a host mount; never pass host environment, credentials, a kubeconfig or a docker socket into the container; never start a VM to get a daemon. If an invariant of the safe lane cannot hold, the lane is `blocked`, and the static pre-pass is the result.
- Never run a live-infra, publish, external-URL or destructive step; never invent a secret to get past a step.
- Halt on any finding without the doc line, the command, the image, the network mode, the exit code and the stderr tail; a static row is `Unconfirmed (static)`.
- Never edit the repo: the setup patch is printed, never applied (`/doc-refresh --from-audit` applies it, failing first). The write check must print nothing; tear down the container and its network every run.
- Do not print "the quickstart works" without the class-coverage block.

## Related

- `doc-drift-scan` (this pack) — owns the static classes this skill corroborates (§3 scripts, §4 flags, §6 versions, §7 tools, §9 env) and the engine whose `--claim` lists every doc carrying the same command; `doc-sample-scan` compiles fenced code samples, which this skill never runs.
- `/doc-refresh` — runs this skill in its runnable gate (default mode) and its audit; `--from-audit` closes DS-1 findings by re-running the failing step in a fresh container.
- `@doc-writer` — writes the setup prose; this skill proves it.
- Code-quality `smoke-verify` (when installed) — the same leap for code: a green suite does not prove the app boots.
