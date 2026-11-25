---
name: compose-scan
description: "Compose stacks that start wrong: depends_on, healthchecks, overrides."
kind: skill
pack: devops
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: compose-scan

## Premise

A compose file that `docker compose config` accepts is not a stack that starts correctly on the host that runs it. Each of these was measured on 2026-10-10 with Compose v5.1.4 (`docker:29.5.2-cli` over engine 29.5.2):
- `depends_on: [db]` expands to `condition: service_started`. An app that probes Postgres the moment it starts exits 2; the same app behind `condition: service_healthy` exits 0.
- `condition: service_healthy` on a service with no healthcheck (or `healthcheck: { disable: true }`) makes `docker compose up` exit 1: `dependency failed to start: container … has no healthcheck configured`.
- `test: ["CMD", "redis-cli ping"]` is one argv word: the exec fails and the container is `unhealthy` forever. `curl` in a healthcheck on `redis:7-alpine` is `/bin/sh: curl: not found`.
- `image: api:${TAG}` with `TAG` unset renders `image: 'api:'` with only a warning, and `ports: ["${API_PORT}:3000"]` renders **no published port** (an ephemeral one), with `config` still exiting 0.
- `docker compose up` with no `-f` merges an override file into the base: ports and volumes **append** (the debug port and the `./src` bind mount both arrive), `command` is replaced. Every one of `compose.override.yaml`, `compose.override.yml` and `docker-compose.override.yml` paired with every base name.
- `restart: always` on a one-shot migrator restarted it 6 times in 8 s. `deploy.replicas: 2` and `deploy.restart_policy` are honoured outside Swarm.
- A Postgres service with no named volume lost its table across `down` + `up`: the image's `VOLUME` became a new anonymous volume, and the old one was left dangling.
- `container_name:` and a fixed host port each make `--scale 2` fail (`port is already allocated` left one container in `created`).

No linter reports these. hadolint, checkov and trivy do not read compose; semgrep `p/docker-compose` matches only files with a top-level `version:` key (security `iac-scan`, gotchas). This skill reads the stack **the way the host loads it**: it finds every invocation, rebuilds each file set with `docker compose config --format json`, and joins the normalised model (long-form `depends_on`, merged overrides, resolved profiles) with the raw lines.

It owns `ownership.json` row `compose-reliability` (§1–§7). `@deployment-engineer` (this pack) judges its rows.

**Every finding cites `<file:line>` + the file set it was read in (the invocation that loads it) + the service and its partner (dependency, image, volume) + the oracle and its tier + the fix in compose syntax.** A pre-flight row is a candidate; none is a finding. "The compose file looks fine" is never printed; the output is the class-coverage block (§ Output). Verification follows [`refute-before-report.md`](../../../../snippets/refute-before-report.md) with [`precedents/devops.md`](../../../../snippets/precedents/devops.md) (containers and compose § 29–40, tools § 41–46); the oracles are [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § DevOps, V241 (§1, §3–§7), V238 (§2) and V231 (§7).

## The rule

A candidate is a finding when all four hold (the seven gates as `precedents/devops.md` § Reading the seven gates applies them to compose):

1. **The file set is the one a host loads** (gates 1, 7). A deploy script, CI job, systemd unit or playbook runs `docker compose … up` on a server with this set (pre-flight 0b). A set only a developer loads drops one level for §1, §3 and §5 (precedents § 40); a set nothing loads is Hardening.
2. **The event happens** (gate 2). A cold start, a host reboot, `down` + `up` during an upgrade, `--scale`, a deploy with an unset variable, a one-shot that exits.
3. **No control already covers it** (gate 4). The app retries its connection with backoff; the image defines a `HEALTHCHECK` (`docker image inspect`); the host's `.env` or the CI step sets the variable; the deploy passes `-f`; the data lives outside the container.
4. **The oracle fired, or both ends are cited** (gate 6). `docker compose config` on the host's file set (T), `up --wait` or a cold start in a scratch project (R), or a static trace naming both ends (the line and the invocation that loads it), which keeps the row `[report-flagged]`.

## Boundaries

- **Security owns exposure and secrets, when the security pack is installed** — `iac-scan` §2: published ports without `127.0.0.1` on a database, cache or admin UI, `privileged`, `docker.sock`, host namespaces, `cap_add`, literal or default passwords; `iac-scan` §7 and `secret-scan-method`: secret values in `environment:`, `.env` or `env_file`. Pre-flight R lists those lines and never posts them. Devops owns whether the stack **starts, stays up and keeps its data**. One line carrying both claims (an override that publishes `9229` on every interface) is one finding per `<file:line>`, credited to the more severe owner; the other corroborates. Without the security pack, R rows print `security-class (owner pack not installed)` at this skill's severity.
- **Images** (PID 1, a Dockerfile `HEALTHCHECK`, the shipped user) → `container-build-scan` (this pack). §2 here judges the compose `healthcheck:`; §7 reads `init: true` only to join `container-build-scan` §2's PID 1 row.
- **Migration topology** (`--scale app=3` running one migration N times) → `deploy-safety-scan` §1 (V227); the app's drain number → `deploy-safety-scan` §5. §7 compares `stop_grace_period` against that number.
- **Kubernetes** manifests generated from compose (kompose) are read rendered by infrastructure; Swarm `docker stack deploy` is a lane below, not a separate skill.

## Adapt to the codebase — the engine lanes

Discover every compose file and invocation (pre-flight 0a, 0b); never assume `./docker-compose.yml`. Print the lane in the header.

| Lane | Which files load | `depends_on` | `deploy:` keys | Tool |
|---|---|---|---|---|
| **Compose v2+ plugin** (v5.1.4 measured) | `compose.yaml` preferred over `docker-compose.yml` ("Found multiple config files" warning); any override name auto-merges; `-f` or `COMPOSE_FILE` replaces the default set [V] | short form = `service_started`; long form `condition`, `required` (2.20.0), `restart` (2.17.0) | `replicas`, `restart_policy` honoured [V]; unsupported keys ignored | `docker compose config` / `--variables` / `--profiles` |
| **CLI image** (no plugin, daemon present) | as above, through `docker:29.5.2-cli` with the repo mounted read-only | as above | as above | the same commands, run in the container |
| **Swarm** (`docker stack deploy -c`) | only the `-c` files; no override auto-load | ignored by Swarm `[K?]`: read the stack's own retry | Swarm semantics | `docker stack config` `[K?]` |
| **Legacy `docker-compose` v1** | v1 rules; `version:` selects the schema | v1 short form | ignored without `--compatibility` `[K?]` | upgrade first: v1 is unsupported |

A shared `extends:` base or `include:`d file used by N stacks is **one finding with N call sites** (precedents § 5).

## Tool lane and ledger

| Lane | Command and pin | Trap that makes a clean result false (precedents § 41) |
|---|---|---|
| Model | `docker compose config --no-interpolate --format json` per file set, `jq` over it | `${VAR:?}` unset makes plain `config` exit 1 for the **whole** set (measured): the model lane uses `--no-interpolate`, and the interpolation rows come from `config -q` and `config --variables`. A set whose `config` fails prints `NOT-RUN <error>`, never clean |
| Variables | `docker compose config --variables` | A variable used both with and without `:?` is reported either way between runs (measured); the raw-line row is the stable one |
| CLI image | `docker:29.5.2-cli@sha256:9ba8e32b…` (digest read 2026-10-10) | Docker Desktop or colima not sharing the repo path → `no configuration file provided`: NOT-RUN, mount a shared path |
| Runtime (R) | `docker compose -p cs-probe up -d --wait --wait-timeout 60` in a scratch copy, then `down -v` | `--wait` exits **1** when any selected service exits, even with 0 (a one-shot with no dependent, measured): select the long-running services, or make the one-shot a `service_completed_successfully` dependency (then `--wait` exits 0, measured) |

Every R run uses a scratch project name (`-p cs-probe`), placeholder values for required variables, never the host's `.env` with real credentials, and `down -v` afterwards. No daemon → `blocked (no docker)` with the command written out.

## Pre-flight

Run as **one** script from the repo root; bash 3.2, bash 5 and zsh print the same rows. Grep **N** and model rows starting `N` feed **§N**; 0 is the inventory; R lists the security-routed rows. Every `rg` names its path; an rg exit 2 is a failed grep, never zero hits. Nothing is written inside the repo: the jq program and the models go to `$SCAN`, and the CLI image mounts the repo read-only.

```bash
[ -n "${ZSH_VERSION:-}" ] && setopt shwordsplit nonomatch   # the compose argv below is split on spaces in bash and zsh alike
X=(-g '!**/{node_modules,vendor,dist,build,out,target,.venv,venv,coverage,.next,.turbo,generated}/**'
   -g '!**/{test,tests,__tests__,spec,e2e,fixtures,__fixtures__,mocks,__mocks__,testdata,examples}/**' -g '!**/{docs,ai,.claude,.git}/**')
CMP=(--sort path --hidden -g '*compose*.{yml,yaml}' "${X[@]}")
INV=(--hidden -g '*.sh' -g '**/Makefile' -g '**/package.json' -g '.github/workflows/*.{yml,yaml}' -g '**/.gitlab-ci*.yml' -g '**/Jenkinsfile*'
     -g '**/*.service' -g '**/{ansible,playbooks,roles}/**/*.{yml,yaml}' -g '**/Procfile' -g '**/justfile' -g '**/Taskfile*.yml' "${X[@]}")
NC=(rg -v --pcre2 '^[^:]+:\d+:\s*#')   # drops comment-only hit lines
SCAN="${SCAN:-$(mktemp -d "${TMPDIR:-/tmp}/compose-scan.XXXXXX")}"; echo "SCAN=$SCAN"
echo '# 0a compose files (canonical names auto-load an override; any other name loads only through -f)'
rg --files "${CMP[@]}" . | sort | tee "$SCAN/cf.txt"
echo '# 0b invocations: which files and profiles each one loads (no -f / COMPOSE_FILE = the canonical file + every override in its directory)'
rg -n --pcre2 "${INV[@]}" '\bdocker[ -]compose\b[^\n]*?\s(up|pull|run|create|start|restart|deploy|config)\b|\bdocker\s+stack\s+deploy\b|\bCOMPOSE_(FILE|PROFILES)\s*[=:]' . | "${NC[@]}" | sort > "$SCAN/inv.txt"
awk '{ f = ($0 ~ /[ \t](-f|--file)[ =]|COMPOSE_FILE/) ? "files=explicit" : "files=DEFAULT(+override)"; p = ($0 ~ /--profile|COMPOSE_PROFILES/) ? "profiles=set" : "profiles=none"
       w = ($0 ~ /--wait/) ? "wait=yes" : "wait=no"; print f, p, w, "::", $0 }' "$SCAN/inv.txt"
echo '# 0c override files (each auto-merges into a DEFAULT invocation run in its directory; measured: any override name pairs with any base name)'
rg -N --pcre2 '(^|/)(docker-)?compose\.override\.ya?ml$' "$SCAN/cf.txt"
echo '# 0d compose engine: plugin, else the CLI image over the daemon, else static only'
DCI="docker:29.5.2-cli@sha256:9ba8e32bfc35a2c7ae2feb1e3241b2778ae21dee80f4dcd31d04e1cfdea86ea2"
if docker compose version >/dev/null 2>&1; then DC="docker compose"; elif docker image inspect "$DCI" >/dev/null 2>&1; then DC="docker run --pull=never --rm -v ${PWD}:${PWD}:ro -w ${PWD} $DCI docker compose"
else DC=""; echo "model lane: NOT-RUN (no compose plugin, and the CLI image is not local — to enable: docker pull $DCI): static greps only, every row [report-flagged]"; fi
[ -n "$DC" ] && echo "model lane: $($DC version --short 2>&1 | head -1) via ${DC%% compose*}"
cat > "$SCAN/model.jq" <<'JQ'
def oneshot($n; $v): ($n + " " + ([$v.command // [] | if type == "array" then .[] else . end] | join(" "))) | test("migrat|seed|(^|[^a-z])init([^a-z]|$)|setup|bootstrap|alembic|flyway|liquibase"; "i");
def stateful: test("(^|/)(postgres|postgis|mysql|mariadb|mongo|redis|valkey|keydb|rabbitmq|elasticsearch|opensearch|minio|clickhouse|cassandra|neo4j|influxdb|meilisearch|qdrant|kafka|zookeeper)([:@]|$)"; "i");
def reps($v): ($v.deploy.replicas // $v.scale // 1);
.services as $S | $S | to_entries[] | .key as $s | .value as $v |
( ($v.depends_on // {}) | to_entries[] | .key as $t | .value.condition as $c | $S[$t] as $tv |
  if $tv == null then "1 DEP-UNDEFINED \($s) -> \($t) (a profile or another file: read config --profiles)"
  elif $c == "service_started" and oneshot($t; $tv) then "1 DEP-ONESHOT-STARTED \($s) -> \($t) (a one-shot: service_completed_successfully)"
  elif $c == "service_started" then "1 DEP-STARTED \($s) -> \($t) target-healthcheck=\(if $tv.healthcheck == null then "none" elif $tv.healthcheck.disable then "disabled" else "yes" end)"
  elif $c == "service_healthy" and $tv.healthcheck == null then "1 DEP-HEALTHY-NO-HC \($s) -> \($t) (up fails unless the image has a HEALTHCHECK)"
  elif $c == "service_healthy" and $tv.healthcheck.disable == true then "1 DEP-HEALTHY-HC-DISABLED \($s) -> \($t) (up fails: no healthcheck)"
  else empty end ),
( ($v.healthcheck.test // null) as $x | if $x == null then empty
  elif ($x | type) == "array" and $x[0] == "CMD" and (($x[1] // "") | test(" ")) then "2 HC-CMD-ONE-STRING \($s): \($x | tojson) (exec of one argv word: never healthy)"
  else ((if ($x | type) == "array" then (if $x[0] == "CMD" then $x[1] elif $x[0] == "CMD-SHELL" then ($x[1] | split(" ")[0]) else "" end) else ($x | split(" ")[0]) end) as $b
    | if $b == "curl" or $b == "wget" then "2 HC-BINARY \($s): \($b) in \($v.image // "build:")" else empty end) end ),
( if ($v.restart // "" | test("always|unless-stopped")) and oneshot($s; $v) then "7 RESTART-ONESHOT \($s): restart=\($v.restart) re-runs it forever"
  elif $v.restart == null and $v.deploy.restart_policy == null and ($v.profiles // []) == [] and (oneshot($s; $v) | not) then "7 RESTART-NONE \($s)" else empty end ),
( $v.stop_grace_period // empty | select(test("^[0-9]+s$") and (rtrimstr("s") | tonumber) < 10) | "7 GRACE-SHORT \($s): stop_grace_period=\(.) (default 10s): compare the app drain (deploy-safety-scan §5)" ),
( if $v.container_name and reps($v) > 1 then "6 CN-SCALED \($s): container_name with replicas=\(reps($v))" elif $v.container_name then "6 CN \($s)" else empty end ),
( if reps($v) > 1 and ([$v.ports[]? | objects | select((.published // "") | test("^[0-9]+$"))] | length) > 0 then "6 PORT-SCALED \($s): fixed host port with replicas=\(reps($v))" else empty end ),
( $v.image // empty | if test("\\$\\{[A-Za-z_][A-Za-z0-9_]*\\}") then "3 IMAGE-VAR-NODEFAULT \($s): \(.)" elif test("\\$|@sha256:") then empty
  elif test(":latest$") then "5 IMAGE-LATEST \($s): \(.)" elif (test(":[^/]+$") | not) then "5 IMAGE-UNTAGGED \($s): \(.)" else empty end ),
( if ($v.image // "" | stateful) and ([$v.volumes[]? | select(.type == "volume" and .source != null or .type == "bind")] | length) == 0 then "6 STATEFUL-ANON \($s): \($v.image) keeps its data in an anonymous volume (down + up loses it)" else empty end ),
( $v.volumes[]? | select(.type == "bind" and (.target | test("^/(app|code|src|usr/src/app|srv/app|var/www/html|home/node/app)(/src)?/?$"))) | "4 BIND-CODE \($s): \(.source) -> \(.target) (source tree over the image's code)" ),
( if $v.profiles then "4 PROFILE \($s): \($v.profiles | join(","))" else empty end ),
( $v.env_file[]? | "3 ENV-FILE \($s): \(.path) required=\(.required // true)" ),
( if $v.links then "6 LINKS \($s): \($v.links | join(","))" else empty end )
JQ
SETS="$SCAN/sets.txt"; : > "$SETS"
rg -N --pcre2 '(^|/)(compose|docker-compose)\.ya?ml$' "$SCAN/cf.txt" | while IFS= read -r f; do d=$(dirname "$f"); grep -qx "D $d" "$SETS" || echo "D $d" >> "$SETS"; done
rg -o --pcre2 '(\s(-f|--file)[ =]\S+)+' -r '$0' "$SCAN/inv.txt" | sed -E 's/^[^:]+:[0-9]+://; s/--file[ =]/-f /g; s/["\x27]//g' | sort -u | sed 's/^ */F /' >> "$SETS"
echo '# 1-7 model rows per file set (D = a DEFAULT invocation in that directory; F = an -f set an invocation names); § number first'
if [ -n "$DC" ]; then while read -r k a; do
  if [ "$k" = D ]; then o="--project-directory $a"; else o="$a"; fi
  if [ "$k" = F ]; then h="invocations: $(grep -cF -e "$a" "$SCAN/inv.txt"), with --profile: $(rg -F -- "$a" "$SCAN/inv.txt" | grep -cE -e "--profile|COMPOSE_PROFILES")"; else h="DEFAULT invocations: 0b rows whose working dir is $a"; fi
  echo "## set $k $a ($h)"; $DC $o config --no-interpolate --format json > "$SCAN/m.json" 2> "$SCAN/m.err" || { echo "NOT-RUN $(head -c 200 "$SCAN/m.err")"; continue; }
  jq -r -f "$SCAN/model.jq" "$SCAN/m.json" | awk '/ RESTART-NONE / { r = r " " $3; next } { print } END { if (r != "") print "7 RESTART-NONE (a finding only on a host-deployed set):" r }'
  $DC $o config -q 2>&1 | rg -o --pcre2 'The "\w+" variable is not set|attribute `version` is obsolete|env file \S+ not found|required variable \w+ is missing|Found multiple config files' | sort | uniq -c | sed 's/^/  config: /'
  $DC $o config --variables 2>/dev/null | awk 'NR > 1 && $2 == "false" && NF == 2 { print "3 VAR-NODEFAULT " $1 }'
  if [ "$k" = D ] && ls "$a"/*compose.override.y*ml >/dev/null 2>&1; then b=$(ls "$a"/compose.y*ml "$a"/docker-compose.y*ml 2>/dev/null | head -1)
    $DC -f "$b" config --no-interpolate --format json > "$SCAN/b.json" 2>/dev/null && jq -r --slurpfile B "$SCAN/b.json" '.services | to_entries[] | .key as $s | ($B[0].services[$s] // null) as $o |
      if $o == null then "4 OVERRIDE-ADDS service \($s)" else ((.value.ports // []) - ($o.ports // []) | .[] | "4 OVERRIDE-ADDS port \($s): \(tojson)"), ((.value.volumes // []) - ($o.volumes // []) | .[] | "4 OVERRIDE-ADDS volume \($s): \(.source) -> \(.target)"),
        (if .value.command != $o.command then "4 OVERRIDE-ADDS command \($s): \(.value.command | tojson)" else empty end) end' "$SCAN/m.json"; fi
done < "$SETS"; fi
echo '# 1-7 static lane (raw files: line numbers for the model rows; the only lane when the model lane is blocked)'
rg -n -A3 --pcre2 "${CMP[@]}" '^\s*depends_on:\s*(\[|$)|^\s*condition:\s*service_started\b' . | "${NC[@]}"
rg -n --pcre2 "${CMP[@]}" '^\s*test:\s*\[\s*["\x27]CMD["\x27]\s*,\s*["\x27][^"\x27]*\s[^"\x27]*["\x27]|^\s*test:[^\n]*\b(curl|wget)\b|^\s*disable:\s*true' . | "${NC[@]}"
rg -n --pcre2 "${CMP[@]}" '(?<!\$)\$\{[A-Za-z_]\w*\}|(?<![\$\w])\$[A-Za-z_]\w*' . | "${NC[@]}"
rg -n --pcre2 "${CMP[@]}" '^\s*image:\s*["\x27]?(?![^\n]*\$)(?![^\n]*@sha256:)([\w.-]+/)*[\w.-]+(:latest)?["\x27]?\s*$' . | "${NC[@]}"
rg -n --pcre2 "${CMP[@]}" '^version:|^\s*links:|^\s*container_name:|^\s*replicas:\s*([2-9]|\d{2,})|!reset|!override' . | "${NC[@]}"
rg -n --pcre2 "${CMP[@]}" '^\s*restart:\s*["\x27]?(always|unless-stopped)|^\s*stop_grace_period:|^\s*init:\s*true|^\s*profiles:' . | "${NC[@]}"
echo '# R routed to security iac-scan §2 when installed (published ports without 127.0.0.1, literal passwords, host privilege, docker.sock): listed, never posted here'
rg -n --pcre2 "${CMP[@]}" '^\s*-\s*[\x22\x27]?(?!127\.0\.0\.1:|localhost:|\[::1\]:)[\d.\[\]:]*\d+:\d+|^\s*published:\s*[\x22\x27]?\d' . | "${NC[@]}"
rg -n --pcre2 -i "${CMP[@]}" '\w*(PASSWORD|_PASS|_PWD)\w*[\x22\x27]?\s*[:=]\s*[\x22\x27]?(?!\$\{)[^\s\x22\x27]+|ALLOW_EMPTY_PASSWORD|HOST_AUTH_METHOD[\x22\x27]?\s*[:=]\s*[\x22\x27]?trust' . | "${NC[@]}"
rg -n --pcre2 "${CMP[@]}" '^\s*(privileged:\s*true|network_mode:\s*[\x22\x27]?host|pid:\s*[\x22\x27]?host|cap_add:)|/var/run/docker\.sock|/run/docker\.sock' . | "${NC[@]}"
```

How to read it:
- **0b** decides gate 1. `files=DEFAULT(+override)` loads the canonical file **and** every override in the working directory the command runs in (`cd /srv/app && docker compose up -d` inside an `ssh` string: map `/srv/app` to the repo directory it is deployed from). `files=explicit` loads only its `-f` list. A `package.json` or `Makefile` target a developer runs is dev-only (precedents § 40).
- **Sets.** `D <dir>` is the default set of a directory; `F -f …` is a set an invocation names. A row in a `D` set with an override (`OVERRIDE-ADDS`) and a DEFAULT invocation on a server is §4's finding. A row only in an `F` set no server loads is Hardening.
- **The static lane** gives the line numbers the model rows lack (`rg -n` the service name), and is the only lane without a daemon: then every row is `[report-flagged]` and §4's merge is read by hand (sequences append; `command` replaces; `!reset` clears).

Blind spots, worked around rather than trusted:
- **Host-side files**: the server's `.env`, `COMPOSE_FILE`, `COMPOSE_PROFILES` and override files that are not in the repo. Read the deploy script and the provisioning (Ansible, cloud-init); otherwise the §3/§4 row stays `[report-flagged]` with `unknown host env`.
- **`include:`, `extends:` and remote `-f`** (a URL or an OCI artifact) are resolved by `config` only when reachable; a failure is NOT-RUN for that set.
- **The image's own `HEALTHCHECK`** satisfies `service_healthy` with no compose `healthcheck:`: read `docker image inspect -f '{{json .Config.Healthcheck}}' <img>` before a `DEP-HEALTHY-NO-HC` row counts.

### Measured (2026-10-10)

| Tree | Result |
|---|---|
| Seeded sample: 6 compose files (base, override, prod, a profiled stack, a dev file, a legacy `docker-compose.yml` with `version:`), 6 invocations (ssh deploy script, CI deploy over ssh, an `-f` deploy, a profile deploy, two `package.json` scripts), copies under `tests/fixtures/`, `docs/` and `node_modules/`; 31 positives, 12 decoys, 3 routed | 7 s with the model lane (~1 s per set through the CLI image), 0 rg or jq errors; bash 3.2 and zsh identical apart from the `--variables` ordering quirk. **31/31 positives surface** in their §, including the `!reset []` in the prod file that leaves Postgres on an anonymous volume (visible only in the merged model). The copies never appear. Decoys clear on read: `${TAG:?…}`, `${LOG_LEVEL:-info}`, `$$HOME`, a digest-pinned image, `service_healthy` on a service with a healthcheck, the explicit `-f` deploy, the dev file (precedents § 40) |
| `benchmarks/fixtures/*` (3 of 16 hold compose) | obs-defects 52 lines: 7 `VAR-NODEFAULT` on credentials (`${API_DATABASE_URL}` and kin, no default and no `:?`), 11 `restart: unless-stopped`, config bind mounts. slow-marketplace 36: 6 `DEP-STARTED` with no target healthcheck, `STATEFUL-ANON` redis, `POSTGRES_PASSWORD:?` making plain `config` fail (the `--no-interpolate` lane kept running). vuln-fullstack 22: 1 `DEP-STARTED`, R rows (`5432:5432`, `POSTGRES_PASSWORD: postgres`: security's seeds). One FP class fixed before shipping: every bind mount printed (config files, log dirs); `BIND-CODE` now fires only on a code target (`/app`, `/src`, …) |
| Real NestJS + Fastify monorepo (one dev compose, read-only, `git status` clean before and after) | 3 s. 0 findings. 2 `CN` rows (Hardening: a dev stack nothing scales), 3 R rows routed (published DB and cache ports, a literal dev password). Both healthchecks correct (`CMD-SHELL pg_isready`, `["CMD", "redis-cli", "ping"]`), named volumes on both stateful services, the only invocation a `package.json` script (dev-only, precedents § 40) |

## The 3,000-hit path

1. **Intersect** with 0b: keep rows in a set a server loads. Dismiss dev-only and unloaded sets with one read each, and name them in the coverage block.
2. **Group** by file set, then by shared `extends:` base or `include:`d file (precedents § 5).
3. **Rank:** host-deployed sets first; then §6 data loss and §1/§2 start-up (every boot pays them); then the rest.
4. **Read the top 30 groups.**
5. **Run the bulk oracle once:** one `config` + `--variables` per set settles §3–§6; one `up --wait` of the host set in a scratch project settles §1, §2 and §7 for every service in it.
6. **Ledger the rest** as `Live, unreviewed (k groups / n hits — <continuing command>)`. Never mark it `checked`.

## Scans for

| § | Classes | Default severity |
|---|---|---|
| 1 | CT-C01 `depends_on` without health or completion gating | M (L dev-only) |
| 2 | CT-C02 healthcheck missing, disabled under a gate, or never healthy | M |
| 3 | CT-C03 interpolation drift; `env_file` the host may lack | M (L dev-only) |
| 4 | CT-C04 which files and profiles production loads: override auto-merge, profiles never started, source bind mounts | M (H: a debugger or source tree on a prod host) |
| 5 | CT-C05 untagged or `:latest` images | M (L dev-only) |
| 6 | CT-C06 spec semantics: anonymous volumes on stateful services, scaling blockers, legacy keys | L (H: a database on an anonymous volume in a host set; M: a scale blocker on a replicated service) |
| 7 | CT-C07 restart and stop semantics | L–M |

### 1. depends_on without gating (CT-C01)

```
BAD:   api: { depends_on: [db] }                                   (= service_started: api boots before Postgres accepts connections)
       worker: { depends_on: { migrate: { condition: service_started } } }   (the worker runs while the migration is half-applied)
       edge: { depends_on: { queue: { condition: service_healthy } } } · queue: { healthcheck: { disable: true } }   (up exits 1)
GOOD:  depends_on: { db: { condition: service_healthy } } + a db healthcheck · migrate: { condition: service_completed_successfully }
```
**Read the code:** Does the dependent retry its connection with backoff (a TypeORM/Prisma/SQLAlchemy retry option, a `wait-for` loop in the entrypoint)? Is the target a one-shot (`DEP-ONESHOT-STARTED`)? For `DEP-HEALTHY-NO-HC`, does the image define a `HEALTHCHECK`? Is the set dev-only (precedents § 40)?

**Finding when** a cold start of the host set boots a service before its dependency accepts work and nothing retries, or `up` cannot start at all. **Proof (V241):** in a scratch project, `docker compose up -d --wait` on the host set exits 0 and the dependent's first connection succeeds; before the fix the dependent exits or crash-loops (measured: exit 2 with the short form, 0 with `service_healthy`).

### 2. Healthcheck missing, disabled or never healthy (CT-C02)

```
BAD:   test: ["CMD", "redis-cli ping"]                      (one argv word: exec fails, unhealthy forever)
       test: ["CMD", "curl", "-f", "http://localhost:5432"] on postgres   (no curl; and Postgres speaks no HTTP)
       test: curl -fsS http://localhost:3000/health         (a string is CMD-SHELL; curl absent on node:22-bookworm-slim)
GOOD:  ["CMD-SHELL", "pg_isready -U $$POSTGRES_USER"] · ["CMD", "redis-cli", "ping"] · node -e "fetch(…)" on slim bases
```
**Read the code:** Is the binary in the image (`docker run --rm --entrypoint sh <img> -c 'command -v curl'`)? Does the probe speak the service's protocol and port? Does anything gate on it (§1 `service_healthy`, `up --wait`, an autoheal container)? A compose healthcheck replaces the image's `HEALTHCHECK`; `disable: true` removes it.

**Finding when** the service can never turn healthy, or a gate waits on a healthcheck that does not exist. **Proof (V238):** `docker inspect -f '{{.State.Health.Status}}'` is `healthy` within `start_period` + `interval` × `retries` in a scratch run (measured: the one-word CMD and the missing curl both `unhealthy` in 7 s; `["CMD", "redis-cli", "ping"]` `healthy`).

### 3. Interpolation drift and env files (CT-C03)

```
BAD:   image: ghcr.io/acme/api:${TAG}          (unset → 'ghcr.io/acme/api:' with a warning)
       ports: ["${API_PORT}:3000"]             (unset → an ephemeral host port; the proxy upstream misses it)
       DATABASE_URL: ${API_DATABASE_URL}       (unset → the app boots with an empty URL)
GOOD:  ${TAG:?TAG required} · ${API_PORT:-3000} · env_file: [{ path: .env.production, required: true }] provisioned on the host
```
**Read the code:** Who sets the variable on the host: the project `.env` (interpolation only), the deploy step's environment, `--env-file`? The shell wins over `.env`. `env_file:` sets the **container** environment, not interpolation. Is the `ENV-FILE` gitignored by design and provisioned by the deploy? `$$` is a literal `$`.

**Finding when** the host invocation can render an empty image tag, port or credential with only a warning. Secret **values** in these files are security's (§ Boundaries). **Proof (V241):** `docker compose config -q` with the host's variable source prints no `variable is not set` warning, and `config --variables` shows each used variable `REQUIRED true` or with a default.

### 4. What production actually loads (CT-C04)

```
BAD:   ssh prod 'cd /srv/shop && docker compose up -d'   with compose.override.yaml beside compose.yaml
         → api gets 9229 published, ./src bind-mounted over /app/src, and node --inspect (OVERRIDE-ADDS ×3)
       scheduler: { profiles: [jobs] }  ·  deploy.sh: docker compose -f stack/compose.yaml up -d   (scheduler never starts)
GOOD:  docker compose -f compose.yaml -f compose.prod.yaml up -d --wait · the override renamed compose.dev.yaml · --profile jobs in every host invocation
```
**Read the code:** Which working directory does each DEFAULT invocation run in, and does the deployed checkout carry the override (is it in `.dockerignore`/`rsync --exclude`, or gitignored)? Is `COMPOSE_FILE` set in the host `.env`? For a profiled service: is it meant to run on the host (a scheduler) or only on demand (`docker compose run`)? A `depends_on` into an inactive profile fails `config` loudly (measured), so the silent case is a profiled service nothing depends on.

**Finding when** a host invocation loads dev-only content (a debug port, a source bind mount, a dev command or service), or never starts a service production needs. **Proof (V241):** `docker compose config --services` and `--volumes` on the host invocation's exact file set list only production services and volumes; `OVERRIDE-ADDS` is empty for it.

### 5. Untagged or :latest images (CT-C05)

```
BAD:   image: redis · image: postgres:latest      (in the prod file: pull_policy missing pulls latest on every new host)
GOOD:  image: postgres:16.4-bookworm with a bump bot (precedents § 31) · or @sha256:<digest> with a bot
```
**Read the code:** Does Dependabot (`docker-compose` ecosystem) or Renovate cover the file? Is `pull_policy` set? Under the default `missing` policy a `:latest` image is pulled again (Compose docs, *Services*, fetched 2026-10-10). The tag-mutability claim ("whoever moves the tag changes what runs") is security's when installed; this § posts the same line for **reproducibility and rollback**: two hosts deployed a day apart run different databases.

**Finding when** a host set can start a different image than the one tested. **Proof (V241):** `docker compose config --images` on the host set prints a tag with a version or a digest for every service.

### 6. Spec semantics: volumes, scaling, legacy keys (CT-C06)

```
BAD:   db: { image: postgres:16 }                      (no volume: down + up lost the table, measured)
       volumes: !reset []  in compose.prod.yaml        (the merge drops the base file's named volume)
       reports: { container_name: reports, ports: ["8081:8080"], deploy: { replicas: 2 } }   (scale fails both ways)
       version: "3.8" · links: [db]
GOOD:  volumes: [pgdata:/var/lib/postgresql/data] + a top-level volume · expose: instead of a fixed host port on replicas · drop version:/links:
```
**Read the code:** For `STATEFUL-ANON`: does the service hold durable data (a database, a queue with persistent messages), or is it a pure cache the app rebuilds (Hardening)? For a scale blocker: is the service replicated (`deploy.replicas`, `--scale` in 0b)? `version:` is obsolete (Compose warns and ignores it); `links:` still implies a start dependency.

**Finding when** routine `down` + `up` loses durable data, or the declared replica count cannot start. **Proof (V241):** in a scratch project, write a row, `down`, `up`, and read it back; `up --scale <svc>=2` starts two containers. `config --volumes` lists a named volume for each stateful service.

### 7. Restart and stop semantics (CT-C07)

```
BAD:   migrate: { command: [node, dist/migrate.js], restart: always }   (re-runs the migration forever: 6 restarts in 8 s)
       api: { stop_grace_period: 2s }  with a 25 s drain               (SIGKILL mid-request)
       worker: no restart:  in a host-deployed set                     (stays down after a crash or a reboot)
GOOD:  migrate: restart: "no" + dependents on service_completed_successfully · stop_grace_period ≥ drain + margin · restart: unless-stopped
```
**Read the code:** Is the service a one-shot? What is the app's drain (`deploy-safety-scan` §5)? Is the stack host-deployed (`RESTART-NONE` matters only there)? Does `container-build-scan` §2 report the image's PID 1 with no handler, so `init: true` is the compose-side fix?

**Finding when** a one-shot loops, a stop kills in-flight work, or a long-running host service stays down. **Proof:** V231 — `docker compose stop -t <grace>` returns before the grace with an exit other than 137 and an in-flight request completes; V241 — after `up -d`, `docker inspect -f '{{.RestartCount}}'` on the one-shot stays 0.

## Proof

The oracles are in [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § DevOps. **Scope: a scratch copy of the repo, a scratch project name (`-p cs-probe`), placeholder variables, `${TMPDIR}`, and `down -v` afterwards — never the user's hosts, `.env` with real credentials, or registries.**

| § | Oracle | Tier | V |
|---|---|---|---|
| 3, 4, 5, 6 | `docker compose config` (`-q`, `--variables`, `--services`, `--volumes`, `--images`) on the host invocation's file set: no warning, only production services and volumes, versioned images | T | V241 |
| 1, 6, 7 | `up -d --wait` on the long-running services of the host set exits 0; cold-start, `down` + `up` and `--scale` probes in a scratch project | R | V241 |
| 2 | `.State.Health.Status` = healthy within the window | R | V238 |
| 7 | `docker compose stop` timing; an in-flight request completes | R | V231 |

## Output

```
compose-scan — 6 compose files, 6 sets (3 host-loaded) · model: Compose v5.1.4 via docker:29.5.2-cli · security: installed

1. docker-compose.override.yml:4                                    [report-with-fix]   high
   §4 CT-C04 — scripts/remote-deploy.sh:3 runs `docker compose up -d` (DEFAULT) in /srv/shop, so the override merges:
   api publishes 9229, runs `node --inspect`, and ./src is bind-mounted over /app/src. Proof: config --services
   on the DEFAULT set lists mailhog; on `-f docker-compose.yml -f docker-compose.prod.yml` it does not (T). Fix: deploy with
   the explicit -f set; rename the override compose.dev.yaml. The 0.0.0.0:9229 exposure → security iac-scan §2.

2. docker-compose.prod.yml:6                                          [report-with-fix]   high
   §6 CT-C06 — `volumes: !reset []` drops pgdata from db in the host set: Postgres runs on an anonymous volume.
   Proof: write, down, up → `relation "keep" does not exist` (R, scratch project). Fix: drop the !reset.

3. docker-compose.yml:25                                              [report-flagged]    medium
   §1 CT-C01 — worker starts on `migrate` with service_started. Unproven link: whether the worker retries.
   Settling test: V241 cold start with a slow migration; worker log shows no schema error.

Verification: 41 candidates → 2 findings · 6 unconfirmed · 9 hardening · 0 pre-existing · 21 refuted (self-verified) · 3 routed

Class coverage:
  §1  depends_on gating          checked (5 rows → 1 unconfirmed; dev set refuted § 40)
  §2  healthchecks               checked (4 rows → 2 unconfirmed: image read pending)
  §3  interpolation / env files  checked (4 rows → 1 unconfirmed: host env unknown)
  §4  what production loads      checked (2 DEFAULT host invocations → 1 finding; profile row → hardening)
  §5  image tags                 checked (3 rows → 1 unconfirmed; floating + bot refuted § 31)
  §6  volumes / scale / legacy   checked (8 rows → 1 finding; redis cache refuted on read)
  §7  restart / stop             checked (3 rows → 1 unconfirmed: drain read from deploy-safety-scan §5)
  R   routed                     5432:5432, POSTGRES_PASSWORD literal, docker.sock → security iac-scan §2
```

`[report-with-fix]`: the host invocation, the set and the oracle are in hand, and the fix is local to the compose files or the invocation. `[report-flagged]`: one link is unproven — the host's env or working directory, the image's own healthcheck, the app's retry, a model lane that did not run. The row names the link and the settling test.

The coverage block lists **all seven** §s and the R lane on every run: `checked (k rows → m findings)` only when the lane ran on a present surface; `N/A (no compose file)`; `blocked (<reason>)` for a set whose `config` failed or a missing daemon; `Live, unreviewed (k groups / n rows)` for a partial review.

## False positives / precedents

The verifier reads [`precedents/devops.md`](../../../../snippets/precedents/devops.md) and [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 4. The ones this skill meets most:
- **§ 40** A dev-only compose file drops one level for §1, §3 and §5; it flips back when a server loads it.
- **§ 29** No HEALTHCHECK on a Kubernetes-only image is a nit — but a compose `service_healthy` gate is exactly where it is not.
- **§ 31** A floating minor tag with a bump bot. **§ 5** One finding per shared base or included file. **§ 41** A `config` that errored is NOT-RUN.

Read-step rules measured on 2026-10-10, applied with a `file:line`: a `depends_on` into an inactive profile is a loud `config` error, not a silent skip; a PR-only or `package.json` invocation is dev-only; Redis used purely as a cache on an anonymous volume is Hardening; an image `HEALTHCHECK` satisfies `service_healthy`.

Rationalizations to reject:
- "`docker compose config` is clean": with which file set, and with the host's variables?
- "It has `depends_on`": the short form waits for nothing.
- "We have a healthcheck": does its binary exist in the image?
- "The override is only for dev": who deletes it from the host checkout?

## When to run

- On any diff touching a compose file, an override, a `.env.example` the stack interpolates, or a script, workflow or unit that runs `docker compose`.
- After `/dockerize` writes a compose file; after a `/devops-fix` on a compose row.
- On every whole-repo `/devops-audit`, reporting all seven §s.

## Halt conditions

- **Do not report a critical or high row as confirmed until a separate verifier has refuted it.** That verifier is not the run that found it; it applies [`refute-before-report.md`](../../../../snippets/refute-before-report.md) with `precedents/devops.md`. Under `/devops-audit` that is its verification phase; standalone, run the protocol as a second pass and tag those rows `self-verified`. List the rest as Unconfirmed, Hardening, Pre-existing or Refuted; never drop them.
- **Halt on a finding missing its anchors:** the line, the file set and the invocation that loads it, the service and its partner, and the fix.
- **No `checked` on a set whose `config` failed**, and no model-lane verdict when the lane was blocked (static rows stay `[report-flagged]`).
- **Never run `up` against the user's host, a real `.env` or a production project name.** R-tier runs use `-p cs-probe` in a scratch copy and end with `down -v`.
- **No proposed fix may weaken a control to clear a row:** no `required: false` on a real dependency, no deleted healthcheck, no `restart: "no"` on a long-running service.
- **Do not print "the compose file looks fine" without the coverage block.** **Do not re-derive a class another skill owns** (§ Boundaries); cross-link it.

## Related

- `/devops-audit` dispatches this skill on a compose-file signal and folds its coverage block into the compose rows; `/devops-fix` closes them with V231, V238 and V241. `/dockerize` runs it on the compose file it writes.
- `@deployment-engineer` judges these rows.
- `container-build-scan` (images), `deploy-safety-scan` §1 and §5 (migration topology, drain) in this pack own the neighbouring classes.
- `iac-scan` §2 and §7 and `secret-scan-method` (security; exposure, privilege, secret values), when that pack is installed.

## Sources

Compose semantics measured on 2026-10-10 (Compose v5.1.4 in `docker:29.5.2-cli`, engine 29.5.2) on scratch projects removed afterwards: short-form expansion, `service_healthy` without a healthcheck, override pairing and merge, profiles, `container_name` and fixed-port scaling, `restart: always` on a one-shot, `deploy.restart_policy` and `replicas` outside Swarm, `--wait` with a one-shot, anonymous-volume data loss, `env_file` and `:?` errors, `--variables`. Cross-checked against docs.docker.com (*Services*, *Merge*, *Profiles*, *Interpolation*, *Environment variable precedence*, *docker compose up/config/down*, *Dockerfile reference* healthcheck defaults), fetched 2026-10-10. Classes from the devops research catalog's containers notes (CT-C01–C08) and the batch-4 devops eval (DV-6). Paraphrased; no text reproduced beyond identifiers.
