# 生产可用 publish-artifact 技能 实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 把 `skills/publish-artifact/` 重写为生产可用、全英文、纯 bash+curl 的独立技能：env 配置 + 缺配置引导、`--json/--version/--dry-run/--verify`、瞬时失败重试、规范退出码、可移植。

**Architecture:** 三个自包含文件——`publish.sh`(CLI 全部逻辑)、`test.sh`(自测)、`SKILL.md`(Claude Code 技能说明)。无外部依赖（无 python/jq）、无对仓库其它文件的引用。

**Tech Stack:** bash（3.2 兼容）+ curl。对接 IPFS Cluster REST `/add`（经 token 写入口）。

## Global Constraints

- **纯 bash + curl**：禁止 python、jq、其它运行时。
- **全英文**：`publish.sh`/`test.sh` 注释与输出、`SKILL.md` 正文全英文。
- **完全自包含**：三个文件不引用 `docs/`、`../`、仓库其它路径。
- **bash 3.2 兼容**：可用数组、`${var#prefix}`、`read -r -d ''`、`$(( ))`；禁用 `mapfile`/`readarray`/`${var,,}`。
- **配置 = 3 个 env**：`IPFS_PUBLISH_ENDPOINT`、`IPFS_PUBLISH_TOKEN`、`IPFS_BASE_URL`；不落配置文件。
- **退出码**：0 成功 / 1 发布失败 / 2 未配置(引导) / 3 用法错误 / 4 目标不存在 / 5 缺依赖。
- **强制** `cid-version=1`；默认 `expire-in=168h`，`--permanent` 省略。
- **stdout**：默认仅一行链接；`--json` 一个 JSON 对象；诊断全走 stderr。
- **重试**：curl 非0 / HTTP 5xx / 000 → 退避重试至多 3 次；4xx（含 401）不重试。
- 提交信息中文（约定式前缀英文）；**不带** `Claude-Session:` trailer。

## 已验证事实（实现可依赖）

- IPFS Cluster REST `POST <endpoint>/add`：单文件返回一行 JSON `{"name":...,"cid":"...","size":...}`；目录（`wrap-with-directory=true`、各文件 filename 取相对站点根路径）逐条返回，其中 `"name":""` 那行的 `cid` 是站点根。
- 单文件链接 `<BASE>/artifact/<cid>`；目录链接 `<BASE>/artifact/<root>/`。
- 本地实测：`make up` 起栈，`.env` 有 `IPFS_PUBLISH_TOKEN`；本机写入口 `http://127.0.0.1:9097`、读 `http://127.0.0.1:8088`。

## 文件结构

- `skills/publish-artifact/test.sh` — 自测（先写，TDD）。
- `skills/publish-artifact/publish.sh` — CLI 全部逻辑（重写）。
- `skills/publish-artifact/SKILL.md` — 英文、自包含技能说明。

---

### Task 1: test.sh（英文自包含，5 条断言）

**Files:**
- Modify(重写): `skills/publish-artifact/test.sh`

**Interfaces:**
- Consumes: `./publish.sh`（同目录）、3 个 env、可达部署。
- Produces: 退出码 0 当且仅当 5 条断言全过；末尾打印 `PASS=N FAIL=M`。

- [ ] **Step 1: 写测试（会先失败，因 publish.sh 尚未支持 --json/--dry-run/退出码2）**

覆盖 `skills/publish-artifact/test.sh` 为：

```bash
#!/usr/bin/env bash
# Self-contained behavior test for the publish-artifact skill.
# Pure bash + curl (no python, no jq). NOTE: intentionally no `set -e`
# so that assertions on non-zero exits work.
# Requires: the 3 env vars set + a reachable deployment (for publish assertions).
set -uo pipefail
HERE=$(cd "$(dirname "$0")" && pwd)
PUB="$HERE/publish.sh"
PASS=0; FAIL=0
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"; echo "PASS=$PASS FAIL=$FAIL"' EXIT
ok(){ echo "PASS: $1"; PASS=$((PASS+1)); }
ng(){ echo "FAIL: $1"; FAIL=$((FAIL+1)); }
# Poll a URL until it serves 200 (replication across gateways is asynchronous).
get200(){ for _ in $(seq 1 20); do [ "$(curl -s -o /dev/null -w '%{http_code}' "$1")" = "200" ] && return 0; sleep 1; done; return 1; }

# 5) missing config -> exit 2 + onboarding (needs no cluster; run first)
out=$(env -u IPFS_PUBLISH_TOKEN "$PUB" "$tmp/none.html" 2>&1); rc=$?
if [ "$rc" = 2 ] && printf '%s' "$out" | grep -q 'not configured'; then ok "missing config -> exit 2 + onboarding"; else ng "missing config (rc=$rc)"; fi

# remaining assertions need config + reachable deployment
: "${IPFS_PUBLISH_ENDPOINT:?set IPFS_PUBLISH_ENDPOINT}"
: "${IPFS_PUBLISH_TOKEN:?set IPFS_PUBLISH_TOKEN}"
: "${IPFS_BASE_URL:?set IPFS_BASE_URL}"

# 4) --dry-run exits 0 and does not upload
printf '<!doctype html><meta charset=utf-8><h1>DRY</h1>' > "$tmp/dry.html"
out=$("$PUB" --dry-run "$tmp/dry.html" 2>&1); rc=$?
if [ "$rc" = 0 ] && printf '%s' "$out" | grep -q 'dry-run'; then ok "--dry-run exits 0, no upload"; else ng "--dry-run (rc=$rc)"; fi

# 1) single file publishes and renders
printf '<!doctype html><meta charset=utf-8><h1>SMOKE_OK</h1>' > "$tmp/page.html"
link=$("$PUB" "$tmp/page.html")
if get200 "$link" && curl -fsS "$link" 2>/dev/null | grep -q 'SMOKE_OK'; then ok "single-file renders"; else ng "single-file renders (link=$link)"; fi

# 3) --json contains cid + link
j=$("$PUB" --json "$tmp/page.html")
if printf '%s' "$j" | grep -q '"cid"' && printf '%s' "$j" | grep -q '"link"'; then ok "--json has cid+link"; else ng "--json ($j)"; fi

# 2) directory (relative asset) renders
mkdir -p "$tmp/site/css"
printf '<!doctype html><meta charset=utf-8><link rel=stylesheet href="./css/app.css"><h1>SMOKE_DIR</h1>' > "$tmp/site/index.html"
printf 'h1{color:green}' > "$tmp/site/css/app.css"
dlink=$("$PUB" "$tmp/site")
if get200 "${dlink}index.html" && get200 "${dlink}css/app.css"; then ok "dir index+css render"; else ng "dir render (dlink=$dlink)"; fi

[ "$FAIL" -eq 0 ]
```

```bash
chmod +x skills/publish-artifact/test.sh
```

- [ ] **Step 2: 起栈 + 配置 env，运行测试确认「未支持」项失败**

Run:
```bash
make up
export IPFS_PUBLISH_ENDPOINT=http://127.0.0.1:9097
export IPFS_PUBLISH_TOKEN=$(grep '^IPFS_PUBLISH_TOKEN=' .env | cut -d= -f2)
export IPFS_BASE_URL=http://127.0.0.1:8088
# 等三 peer 成形
for i in $(seq 1 90); do curl -fsS -X POST http://localhost:9095/api/v0/version >/dev/null 2>&1 && break; sleep 1; done
for i in $(seq 1 60); do n=$(docker exec cl-cluster0 ipfs-cluster-ctl --enc=json peers ls 2>/dev/null | grep -o '"peername"' | wc -l | tr -d ' '); [ "${n:-0}" -ge 3 ] && break; sleep 1; done
./skills/publish-artifact/test.sh; echo "exit=$?"
```
Expected: 有 FAIL（旧 publish.sh 不支持 `--dry-run`/`--json`、缺配置退出码非 2），`exit != 0`。这证明测试有效。

- [ ] **Step 3: Commit**

```bash
git add skills/publish-artifact/test.sh
git commit -m "test: 发布技能自测重写为 5 条断言(含 --json/--dry-run/缺配置引导)"
```

---

### Task 2: publish.sh（英文重写，通过全部 5 条断言）

**Files:**
- Modify(重写): `skills/publish-artifact/publish.sh`
- Test: `skills/publish-artifact/test.sh`（Task 1）

**Interfaces:**
- Consumes: 3 个 env、`curl`。
- Produces: CLI `publish.sh [options] <file|dir>`；默认 stdout 一行链接，`--json` 输出 `{"cid","link","kind","expires_in"}`；退出码见 Global Constraints。

- [ ] **Step 1: 重写 publish.sh**

覆盖 `skills/publish-artifact/publish.sh` 为：

```bash
#!/usr/bin/env bash
# publish-artifact: publish an HTML file or a directory (multi-asset site) to a
# private IPFS Cluster and print an immutable, shareable link.
# Pure bash + curl. No python, no jq. Config via 3 env vars (see --help).
set -euo pipefail

VERSION="1.0.0"
# exit codes: 0 ok | 1 publish failed | 2 not configured | 3 usage | 4 target missing | 5 dependency

usage() {
  cat >&2 <<'EOF'
publish-artifact - publish HTML to a private IPFS Cluster, get an immutable link.

Usage: publish.sh [options] <file.html | dir/>

Options:
  --json            print a JSON object instead of just the link
  --expire-in DUR   auto-unpin after DUR (default 168h); e.g. 24h, 720h
  --permanent       keep forever (omit expiry); use sparingly
  --verify          after publishing, GET the link and report status (stderr)
  --dry-run         validate config + target and print the planned request; no upload
  --version         print version and exit
  -h, --help        show this help and exit

Configuration (3 environment variables):
  IPFS_PUBLISH_ENDPOINT   token write ingress, e.g. https://pages-publish.example.com
                          (internal / same host: http://127.0.0.1:9097)
  IPFS_PUBLISH_TOKEN      Bearer token for the write ingress (ask your cluster operator)
  IPFS_BASE_URL           read/share base, e.g. https://pages.example.com
EOF
}

onboarding() {
  cat >&2 <<'EOF'
publish-artifact is not configured. Set these 3 environment variables:

  export IPFS_PUBLISH_ENDPOINT="https://pages-publish.example.com"  # token write ingress
  export IPFS_PUBLISH_TOKEN="<ask your cluster operator>"           # Bearer token
  export IPFS_BASE_URL="https://pages.example.com"                  # read/share base

  # internal / same-host agents may use the loopback ingress instead:
  # export IPFS_PUBLISH_ENDPOINT="http://127.0.0.1:9097"

To persist, add the exports to your shell profile (~/.zshrc or ~/.bashrc),
then open a new shell. Verify with:  publish.sh --help
EOF
}

die() { echo "error: $1" >&2; exit "${2:-1}"; }

# require bash (arrays, read -d)
[ -n "${BASH_VERSION:-}" ] || { echo "error: run with bash, not sh (bash arrays required)" >&2; exit 5; }

# parse args (--help/--version need no config)
JSON=0; PERMANENT=0; VERIFY=0; DRYRUN=0; EXPIRE="168h"; TARGET=""
while [ $# -gt 0 ]; do
  case "$1" in
    --json)      JSON=1; shift ;;
    --permanent) PERMANENT=1; shift ;;
    --expire-in) [ $# -ge 2 ] || die "--expire-in needs a value" 3; EXPIRE="$2"; shift 2 ;;
    --verify)    VERIFY=1; shift ;;
    --dry-run)   DRYRUN=1; shift ;;
    --version)   echo "publish-artifact $VERSION"; exit 0 ;;
    -h|--help)   usage; exit 0 ;;
    --)          shift; [ $# -eq 0 ] || TARGET="$1"; break ;;
    -*)          echo "error: unknown option: $1" >&2; usage; exit 3 ;;
    *)           [ -z "$TARGET" ] || die "only one target allowed" 3; TARGET="$1"; shift ;;
  esac
done

# dependency check
command -v curl >/dev/null 2>&1 || { echo "error: curl not found (required)" >&2; exit 5; }

# config check (friendly onboarding, not a bare error)
if [ -z "${IPFS_PUBLISH_ENDPOINT:-}" ] || [ -z "${IPFS_PUBLISH_TOKEN:-}" ] || [ -z "${IPFS_BASE_URL:-}" ]; then
  onboarding; exit 2
fi

# target check
[ -n "$TARGET" ] || { echo "error: no target given" >&2; usage; exit 3; }
[ -e "$TARGET" ] || die "target not found: $TARGET" 4

ENDPOINT="${IPFS_PUBLISH_ENDPOINT%/}"
BASE="${IPFS_BASE_URL%/}"
ADD_URL="$ENDPOINT/add"
Q="cid-version=1"
[ "$PERMANENT" -eq 1 ] || Q="$Q&expire-in=$EXPIRE"

# build curl form args + determine kind
form=()
if [ -d "$TARGET" ]; then
  KIND=dir
  Q="$Q&wrap-with-directory=true"
  [ -e "$TARGET/index.html" ] || echo "warn: no index.html at directory root; link will show a listing" >&2
  nfiles=0
  while IFS= read -r -d '' f; do
    rel="${f#"$TARGET"/}"
    form+=(-F "file=@$f;filename=$rel")
    nfiles=$((nfiles+1))
  done < <(find "$TARGET" -type f -print0)
  [ "$nfiles" -gt 0 ] || die "directory has no files: $TARGET" 4
else
  KIND=file
  form+=(-F "file=@$TARGET;filename=$(basename "$TARGET")")
  nfiles=1
fi

# dry-run: validate + preview, no upload
if [ "$DRYRUN" -eq 1 ]; then
  {
    echo "dry-run (no upload):"
    echo "  request : POST $ADD_URL?$Q"
    echo "  kind    : $KIND"
    echo "  files   : $nfiles"
    echo "  expires : $([ "$PERMANENT" -eq 1 ] && echo permanent || echo "$EXPIRE")"
  } >&2
  exit 0
fi

# upload with retry (transient failures only)
AUTH="Authorization: Bearer $IPFS_PUBLISH_TOKEN"
attempt=0
while :; do
  attempt=$((attempt+1))
  resp=$(curl -sS -H "$AUTH" -X POST "${form[@]}" -w $'\n%{http_code}' "$ADD_URL?$Q" 2>/dev/null) && rc=0 || rc=$?
  http=$(printf '%s' "$resp" | tail -1)
  body=$(printf '%s' "$resp" | sed '$d')
  if [ "$rc" -eq 0 ] && printf '%s' "$http" | grep -q '^2'; then break; fi
  if printf '%s' "$http" | grep -qE '^4'; then
    echo "error: publish rejected (HTTP $http): $body" >&2; exit 1
  fi
  if [ "$attempt" -ge 3 ]; then
    echo "error: publish failed after $attempt attempts (HTTP ${http:-none}, curl rc $rc): $body" >&2; exit 1
  fi
  sleep $((2 ** (attempt - 1)))
done

# parse cid (whitespace-tolerant); dir -> the wrap-root line (name == "")
if [ "$KIND" = dir ]; then
  cid=$(printf '%s' "$body" | grep -E '"name":[[:space:]]*""' | grep -oE '"cid":[[:space:]]*"[^"]*"' | head -1 | sed 's/.*"\([^"]*\)"$/\1/')
  link="$BASE/artifact/$cid/"
else
  cid=$(printf '%s' "$body" | grep -oE '"cid":[[:space:]]*"[^"]*"' | head -1 | sed 's/.*"\([^"]*\)"$/\1/')
  link="$BASE/artifact/$cid"
fi
[ -n "$cid" ] || die "could not parse CID from response: $body" 1

# optional verify
if [ "$VERIFY" -eq 1 ]; then
  code=$(curl -s -o /dev/null -w '%{http_code}' "$link" || true)
  echo "verify: GET $link -> $code" >&2
fi

# output
if [ "$JSON" -eq 1 ]; then
  if [ "$PERMANENT" -eq 1 ]; then exp=null; else exp=$(printf '"%s"' "$EXPIRE"); fi
  printf '{"cid":"%s","link":"%s","kind":"%s","expires_in":%s}\n' "$cid" "$link" "$KIND" "$exp"
else
  echo "$link"
fi
```

```bash
chmod +x skills/publish-artifact/publish.sh
```

- [ ] **Step 2: 运行测试确认全过**

Run（沿用 Task 1 已 export 的 3 个 env 与已起的栈；未起则重复 Task 1 Step 2 的起栈+export）：
```bash
./skills/publish-artifact/test.sh; echo "exit=$?"
```
Expected: `PASS=5 FAIL=0`，`exit=0`。

- [ ] **Step 3: 手验退出码与 --version/--help（无需集群）**

Run:
```bash
env -u IPFS_PUBLISH_TOKEN ./skills/publish-artifact/publish.sh x.html >/dev/null 2>&1; echo "missing-config exit=$?  (want 2)"
./skills/publish-artifact/publish.sh --version                                  # want: publish-artifact 1.0.0
./skills/publish-artifact/publish.sh --bogus >/dev/null 2>&1; echo "bad-opt exit=$?  (want 3)"
./skills/publish-artifact/publish.sh nonexist.html >/dev/null 2>&1; echo "missing-target exit=$? (注意: 无 env 时先返回2；有 env 时才 4)"
```
Expected: missing-config `2`；`--version` 打印 `publish-artifact 1.0.0`；bad-opt `3`。

- [ ] **Step 4: Commit**

```bash
git add skills/publish-artifact/publish.sh
git commit -m "feat: publish.sh 生产化(英文/env引导/--json/--dry-run/--version/重试/退出码/可移植)"
```

---

### Task 3: SKILL.md（英文、自包含、Claude 配置引导）

**Files:**
- Modify(重写): `skills/publish-artifact/SKILL.md`

**Interfaces:**
- Consumes: 同目录 `publish.sh`（退出码 2 = 未配置）。
- Produces: Claude Code 技能说明；无对仓库其它路径的引用。

- [ ] **Step 1: 重写 SKILL.md（全英文，含 Claude 配置引导 + 边界注记）**

覆盖 `skills/publish-artifact/SKILL.md` 为：

````markdown
---
name: publish-artifact
description: Publish an HTML file or a directory (multi-asset site) to a private IPFS Cluster and get back an immutable, shareable link. Use when the user/agent says things like "publish this page / publish to pages / 发布到 pages / give me a share link / host this HTML / host this artifact". Each publish is a new immutable snapshot (new CID/link); default auto-expires after 1 week. Requires 3 env vars pointing at a deployed cluster; guide the user to set them on first use.
---

# Publish Artifact to a private IPFS Cluster

Publish agent-generated HTML as a content-addressed, immutable snapshot and return a shareable link. Similar to Claude Artifacts, but every publish is a new immutable link (edit = new link; old versions stay reachable).

Pure `bash` + `curl` — no python, no jq. Ships as three files: `publish.sh`, `test.sh`, `SKILL.md`.

## First run / configuration

The tool needs 3 environment variables:

- `IPFS_PUBLISH_ENDPOINT` — token write ingress, e.g. `https://pages-publish.example.com` (internal/same host: `http://127.0.0.1:9097`)
- `IPFS_PUBLISH_TOKEN` — Bearer token for the write ingress (ask the cluster operator)
- `IPFS_BASE_URL` — read/share base, e.g. `https://pages.example.com`

**If `publish.sh` exits with code 2 ("not configured"), do NOT just fail.** Ask the user for these three values, then set them for the session:

```bash
export IPFS_PUBLISH_ENDPOINT="…"
export IPFS_PUBLISH_TOKEN="…"
export IPFS_BASE_URL="…"
```

Tell the user they can persist these by adding the exports to `~/.zshrc` or `~/.bashrc`. Then retry the publish.

## Usage

```bash
./publish.sh page.html            # single file -> https://pages.example.com/artifact/<cid>
./publish.sh ./site               # directory (index.html + relative assets) -> …/artifact/<dirCID>/
./publish.sh --json page.html     # JSON: {"cid","link","kind","expires_in"}
./publish.sh --expire-in 24h x.html
./publish.sh --permanent x.html   # no expiry (use sparingly)
./publish.sh --verify x.html      # GET the link after publishing (status to stderr)
./publish.sh --dry-run ./site     # validate + preview the request, no upload
./publish.sh --help
```

Default stdout is a single link line (easy to capture); `--json` prints one JSON object; diagnostics go to stderr.

## Behavior & constraints

- **Immutable snapshots**: each publish is a new CID/link; no in-place update.
- **Default 1-week expiry**: auto-unpinned after `--expire-in` (default 168h); `--permanent` keeps it forever (use sparingly).
- **Directory**: files are added with paths relative to the directory root + `wrap-with-directory`; the root should contain `index.html` (else the link shows a listing).
- **No delete**: the tool does not unpublish (no ownership model); cleanup is via expiry or an operator using `ipfs-cluster-ctl`.
- **CIDv1** enforced.

## Edge cases

- Requires **bash** (not `sh`) and **curl**; exits 5 if missing.
- Symlinked files inside a directory are skipped (`find -type f`).
- Very large directories (thousands of files) may hit the OS argument-length limit.
- For external publishing use the HTTPS write ingress (token stays encrypted in transit); avoid plain `http://<ip>:9097` over the public internet.

## Self-test

```bash
# needs the 3 env vars set + a reachable deployment
./test.sh
```

## Install / distribute

Copy this `publish-artifact/` directory into the user's `~/.claude/skills/` or a project's `skills/` (Claude Code auto-discovers it); or use `publish.sh` as a plain CLI (`chmod +x`, only needs bash + curl).
````

- [ ] **Step 2: 校验自包含 + frontmatter**

Run:
```bash
grep -nE 'docs/|\.\./|SINGLE_HOST|CLUSTER_CTL|CLOUDFLARE|report\.py' skills/publish-artifact/SKILL.md && echo "⚠️ 有外部引用" || echo "自包含 ✓"
head -4 skills/publish-artifact/SKILL.md    # 确认 frontmatter name+description 在
```
Expected: 输出「自包含 ✓」；frontmatter 首行 `---`、含 `name:` 与 `description:`。

- [ ] **Step 3: Commit**

```bash
git add skills/publish-artifact/SKILL.md
git commit -m "docs: SKILL.md 英文化+自包含+首次使用配置引导(去除对仓库 docs 的引用)"
```

---

## Self-Review

**1. Spec coverage:**
- 全英文 → Task 2/3（publish.sh/SKILL.md 全英文）、Task 1（test.sh 英文）。✓
- 零 python/jq、纯 bash+curl → Task 2（解析用 grep/sed；JSON 用 printf）。✓
- 自包含（无外部引用）→ Task 3 Step 2 显式校验。✓
- env-only 配置 + 缺配置引导(码2) → Task 2 `onboarding()`+config check；Task 1 断言5。✓
- SKILL.md 指示 Claude 问用户并 export → Task 3「First run / configuration」。✓
- `--json/--version/--dry-run/--verify/--expire-in/--permanent` → Task 2 参数解析全覆盖；Task 1 断言3/4。✓
- 重试(3次退避，4xx不重试) → Task 2 上传循环。✓
- 退出码 0/1/2/3/4/5 → Task 2；Task 2 Step 3 手验。✓
- bash3.2兼容/依赖检查/空白容忍解析/find -print0/不用 date-stat → Task 2 实现。✓
- test.sh 5 条断言 → Task 1。✓

**2. Placeholder scan:** 无 TBD/TODO；所有脚本/文档为完整内容；`pages.example.com`/`<ask…>` 为示例占位，非待补。✓

**3. Type/name consistency:** 变量 `JSON/PERMANENT/VERIFY/DRYRUN/EXPIRE/TARGET/KIND/form/cid/link`、退出码、`--json` 键 `cid/link/kind/expires_in` 在 Task 1(断言)与 Task 2(实现) 间一致；env 名三者一致。✓
