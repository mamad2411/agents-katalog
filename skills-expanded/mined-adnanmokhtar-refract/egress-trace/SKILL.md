---
name: egress-trace
description: "Egress paths from config (origin vs CDN host, byte proxying, region parity, public hairpins) plus a flow-log lane."
kind: skill
pack: finops
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: egress-trace

## Premise

Data transfer is the cost line with no owner: it appears in no application metric, it is attached to no resource anyone provisioned, and it is billed on a dimension — bytes crossing a boundary — that nobody holds in their head while writing code. Two halves of it are readable at different times:

- **From config and code, always.** Four decisions fix where bytes leave: the host a public URL points at (origin or CDN), whether object bytes stream through the application, which region each client and endpoint names, and whether services call each other by a public hostname. None of them needs a flow log (§ 1–§ 4).
- **From flow logs, when the user supplies them.** Which component pair actually moved how many bytes across which boundary (§ 5). Without logs this lane prints `NOT-RUN (no flow logs)` and the four static classes still run. The skill used to refuse the whole pack lane without flow logs, which silently dropped the four static classes; that halt is gone.

**Every finding cites the URL builder, handler, client or env line `<file:line>` + the boundary it crosses (origin → internet, pod → internet, region → region, public LB hairpin) + the oracle.** A flow-lane finding cites the component pair and the bytes. Verification follows [`refute-before-report.md`](../../../../snippets/refute-before-report.md) with [`precedents/finops.md`](../../../../snippets/precedents/finops.md); the oracles are [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § FinOps, V587–V588.

| § | Class | What is wrong | Lane | Oracle |
|---|---|---|---|---|
| 1 | EG-1 | public objects served from the origin host, not the CDN host | static | **V587** |
| 2 | EG-2 | object bytes proxied through application pods | static | **V587** |
| 3 | EG-3 | a cross-region data path in config | static | **V588** |
| 4 | EG-4 | service-to-service through a public hostname | static | **V588** |
| 5 | EG-flow | transfer attributed by boundary and component pair | flow logs | arithmetic (bytes reconcile to the transfer line) |

## The rule

1. **The path runs in production** (gate 1): the deployed env file or render, a route that serves real traffic.
2. **The bytes are real** (gate 2): public media, downloads at volume, a hot path between regions. Private, low-volume downloads on presigned or redirect URLs are fine (precedents § 22).
3. **Nothing already routes them cheaply** (gate 4): the CDN host is what the URL builder returns, a redirect to a signed URL replaces streaming, the endpoint is the VPC or cluster name.
4. **The proof holds** (gate 6): V587/V588 fails first, or the two-ended trace (the URL builder and the env value it reads; the handler and the stream it returns).

## Boundaries

- **NAT gateways, gateway endpoints and cross-AZ traffic** are infrastructure `iac-cost-scan` § 1–§ 2 (COST-01/02, N4) when that pack is installed; § 5 here attributes their bytes when flow logs exist, and never re-counts the gateways.
- **`Cache-Control` on assets, image weight, payload size** → performance `caching-scan` § 6 and its request-path classes. A CDN host with uncacheable responses is theirs; § 1 asks only which host serves.
- **Telemetry shipped across a boundary at full volume** → observability (`log-signal-scan`, `trace-propagation-scan` § 9, `telemetry-config-scan`); `candidate-pricing` prices their bytes.
- **Who may download a private file** → security. § 2 keeps per-request authorisation; it changes only who carries the bytes.
- **The availability argument for a cross-region topology** belongs to the design (`@cost-architect`, and the infrastructure pack's DR classes); this skill prices it and never recommends co-location without naming the trade.

## Pre-flight

Run as **one** script from the repo root (bash 3.2-safe). Grep **N** feeds §N. Every `rg` names its path; include globs first, exclusions last; `.env*` files are read on purpose (hidden), docs and runbooks are not (they describe, the env files decide). Every grep ends in `ck`: rg exit 2 is a **blocked** class. An empty `ROOTS` stops the script.

```bash
ROOTS=(.)   # monorepo: name the service roots, the env files and the deploy folder
[ -n "${ROOTS[0]:-}" ] || { echo "ROOTS empty — every § blocked (an unset path makes rg search the cwd)"; exit 2; }
OUT="${OUT:-$(mktemp -d "${TMPDIR:-/tmp}/finops-egress.XXXXXX")}"; mkdir -p "$OUT/none"
h() { printf '## %s\n' "$1"; }; ck() { [ "$2" -lt 2 ] || echo "$1 BLOCKED (rg exit $2) — the class is blocked, never 0 hits"; }
X=(-g '!**/node_modules/**' -g '!**/vendor/**' -g '!**/{dist,build,out,target,coverage,.next,.turbo,.venv,venv,.terraform}/**'
   -g '!**/{test,tests,__tests__,spec,e2e,fixtures,__fixtures__,mocks,__mocks__,testdata,examples}/**' -g '!**/*.{spec,test,e2e-spec,stories}.*'
   -g '!**/*.test-data.*' -g '!**/{migrations,locales,i18n,translations}/**' -g '!**/{.git,.claude,docs}/**' -g '!**/ai/**' -g '!**/*.md')
CODE=(-g '*.{ts,mts,cts,js,mjs,cjs,py,go,java,kt,rb,php,cs}' "${X[@]}")
CFG=(--hidden -g '*.{tf,tofu,tfvars,yaml,yml,toml,ini,properties,json}' -g '*.env' -g '*.env.*' -g '.env*' "${X[@]}" -g '!**/{package,package-lock,tsconfig,composer,openapi}*.json' -g '!**/*.lock' -g '!**/pnpm-lock.yaml' -g '!**/.github/**')
# 1 EG-1 public base URLs and object hosts (1a: origin host vs CDN host), presigned GETs handed out (1b)
h 1a; rg -n --pcre2 '\b\w*(PUBLIC|CDN|ASSET|MEDIA|STATIC|FILES?)_?(BASE_)?(URL|HOST|DOMAIN)\b\s*[:=]|\b[\w.-]+\.(digitaloceanspaces\.com|s3[.-][\w.-]*amazonaws\.com|storage\.googleapis\.com|blob\.core\.windows\.net|r2\.(dev|cloudflarestorage\.com)|cloudfront\.net|b-cdn\.net)\b' "${CODE[@]}" "${CFG[@]}" "${ROOTS[@]}"; ck 1a $?
h 1b; rg -n --pcre2 '\bgetSignedUrl\s*\(|\bgenerate_presigned_url\s*\(|\bpresigned(Get|Put)Object\s*\(|\bcreatePresignedPost\b|\bPresignGetObject\b|\bgenerate_signed_url\s*\(|\bgenerateSasUrl\s*\(' "${CODE[@]}" "${ROOTS[@]}"; ck 1b $?
# 2 EG-2 object bytes through the app: the object read (2a) and the response that streams it (2b) — the pair in one handler is the read
h 2a; rg -n --pcre2 '\bnew\s+GetObjectCommand\s*\(|\.get_object\s*\(|\.getObject\s*\(|\bfGetObject\s*\(|\bdownload_(file|fileobj)\s*\(|\.download_as_(bytes|string)\s*\(|\bdownloadToBuffer\s*\(' "${CODE[@]}" "${ROOTS[@]}"; ck 2a $?
h 2b; rg -n --pcre2 '\bnew\s+StreamableFile\s*\(|\b(res|reply|response)\.(pipe|sendFile|download)\s*\(|\.pipe\(\s*(res|reply|response)\b|\.send\(\s*[\w.]*(stream|Stream|Body)\s*\)|\b(StreamingResponse|FileResponse)\s*\(|\bsend_file\s*\(|\bio\.Copy\(\s*w\b|\bc\.(Stream|DataFromReader)\s*\(' "${CODE[@]}" "${ROOTS[@]}"; ck 2b $?
# 3 EG-3 region values per file (3a, distinct values counted) — a mismatch is a join across files, never one line
h 3a; rg -o -n --pcre2 '(?i)\b(region|region_name|location|aws_?region|aws_default_region|s3_region|spaces_region|do_region)\b["\x27]?\s*[:=]\s*["\x27]?\K(?!<|\$|\{)[a-z]{2}-[a-z]+-\d\b|(?i)\b(region|location)\b["\x27]?\s*[:=]\s*["\x27]?\K(?!<|\$|\{)(nyc[1-3]|sfo[1-3]|ams[23]|sgp1|lon1|fra1|tor1|blr1|syd1|atl1)\b|\bhttps?://(\w[\w-]*\.)?\K(nyc[1-3]|sfo[1-3]|ams[23]|sgp1|lon1|fra1|tor1|blr1|syd1|atl1)(?=\.(cdn\.)?digitaloceanspaces\.com)|\.s3[.-]\K[a-z]{2}-[a-z]+-\d(?=\.amazonaws\.com)' "${CODE[@]}" "${CFG[@]}" "${ROOTS[@]}" | awk -F: '{print $NF}' | sort | uniq -c | sort -rn; ck 3a ${PIPESTATUS[0]}
# 4 EG-4 public hostnames (4a: ingress hosts, saved) used as a service-to-service target in config or code (4b)
h 4a; rg -o --no-filename -N --pcre2 '^\s*-?\s*host:\s*["\x27]?\K[a-z0-9][\w-]*(\.[\w-]+)*\.[a-z]{2,}(?=["\x27]?\s*$)|^\s*-?\s*hosts:\s*\[\s*["\x27]?\K[a-z0-9][\w.-]*\.[a-z]{2,}|\bHost\(`\K[^`]+(?=`\))' -g '*.{yaml,yml,toml}' "${X[@]}" "${ROOTS[@]}" | rg -v --pcre2 '\.(internal|local|svc|cluster\.local|localhost|test|invalid)$|^(localhost|example\.(com|net|org))$' | sort -u | tee "$OUT/hosts.txt"; ck 4a ${PIPESTATUS[0]}
[ -s "$OUT/hosts.txt" ] || echo "__no_public_host__" > "$OUT/hosts.txt"
h 4b; rg -n -F -f "$OUT/hosts.txt" "${CODE[@]}" "${CFG[@]}" -g '!**/{scripts,seeds,web,frontend,client}/**' "${ROOTS[@]}" | rg -i --pcre2 '^[^:]+:\d+:\s*(-\s*)?(value|url|endpoint|base_?url|\w*_(URL|HOST|ENDPOINT)|target)["\x27]?\s*[:=]' | rg -v --pcre2 '^[^:]*(ingress|httproute|gateway|certificate|dns|cors|csp)[^:]*:'; ck 4b ${PIPESTATUS[0]}
```

**The joins are reads.** § 1: the URL builder → the env variable it reads → that variable's value in the **deployed** env file or render → origin host or CDN host, per area (public media vs private downloads). § 2: a 2a read and a 2b response in the same handler, or a store `open()` whose stream a controller returns — trace the stream to the reply. § 3: the distinct regions 3a prints, then the file of the odd one out: a commented example, a test config or a DR replica is not EG-3 (precedents § 24). § 4: each 4b line's variable name decides it — a link-building origin (`PUBLIC_ORIGIN`, email links) and an external probe are not calls (§ 23).

## § 5 — the flow-log lane (runtime; only on the user's `--flow-logs=<path>`)

Inputs the user hands over: flow logs (AWS VPC default format v2, or a provider equivalent mapped to the same fields), an inventory TSV `cidr<TAB>component<TAB>zone`, and the transfer line of the bill (`bill-lane.py summary --by sku` on the export, filtered to transfer usage types). The helper sums bytes per component pair and boundary, and states what it could not map:

```bash
cat > "$OUT/flow.py" <<'PY'
import ipaddress, sys, collections
# usage: flow.py <inventory.tsv: cidr<TAB>label<TAB>zone> <flow-log files (AWS default v2 format)...>
inv = []
for line in open(sys.argv[1]):
    if line.strip() and not line.startswith('#'):
        cidr, label, zone = line.rstrip('\n').split('\t')[:3]
        inv.append((ipaddress.ip_network(cidr, strict=False), label, zone))
inv.sort(key=lambda r: -r[0].prefixlen)
def who(ip):
    a = ipaddress.ip_address(ip)
    for net, label, zone in inv:
        if a in net:
            return label, zone
    return ('internet' if a.is_global else 'unmapped'), '-'
pairs, total, bad = collections.Counter(), 0, 0
for path in sys.argv[2:]:
    for line in open(path):
        f = line.split()
        if len(f) < 14 or f[0] == 'version' or f[13] != 'OK' or f[12] != 'ACCEPT':
            bad += f[0] != 'version'
            continue
        (s, sz), (d, dz) = who(f[3]), who(f[4])
        boundary = 'internet' if 'internet' in (s, d) else ('same-zone' if sz == dz else ('cross-zone' if '-' not in (sz, dz) else 'unmapped'))
        pairs[(s, d, boundary)] += int(f[9]); total += int(f[9])
for (s, d, b), n in pairs.most_common(20):
    print(f"{n:>15} B  {100 * n / max(total, 1):5.1f}%  {s} -> {d}  [{b}]")
print(f"total {total} B · rows skipped (REJECT, NODATA, malformed): {bad} · unmapped share: {100 * sum(n for (s, d, b), n in pairs.items() if 'unmapped' in (s, d)) / max(total, 1):.1f}%")
PY
[ -n "${FLOW_LOGS:-}" ] && [ -n "${INVENTORY:-}" ] && python3 -I "$OUT/flow.py" "$INVENTORY" "$FLOW_LOGS"/* || echo "§5 NOT-RUN (no flow logs or no inventory)"
```

Then, per top pair: the **mechanism** (a chatty pair split across zones; replicas or caches read across a boundary; a managed service reached through a per-GB gateway where a private endpoint exists — infrastructure's row, bytes here; replication whose recovery objective does not need it; telemetry or backups shipped out at full volume; CDN misses from cache-busting or short TTLs); the **bytes the fix removes**; and the **trade** (co-location gives up availability; say so). The window is whole weeks: replication and backup traffic is weekly or monthly, so a day misses the largest lines. Transfer belongs to a **pair**, not a resource: attribution by one side's tag is arbitrary. Gateways bill per GB processed on top of transfer. Cross-zone transfer is often billed in both directions. CDN egress and origin egress are different lines: a better hit rate moves bytes between them more than it removes them. Bytes the inventory cannot map are reported as **unattributed transfer** with their share — a telemetry gap, not a rounding error. A managed service that bills transfer inside its own line with no breakdown is said so, never assigned to a pair.

**Measured 2026-10-19** (rg 14, Python 3 stdlib; offline). `flow.py` on a synthetic four-line log (one cross-zone app→db flow, one internet flow, one same-zone, one NODATA) printed 87.3 % cross-zone, 12.2 % internet, 0.5 % same-zone, 1 skipped row; no real flow log exists in any fixture or in the real repo, so § 5 is NOT-RUN there. The 28 fixtures: 1a 2 (`infra-ops` DNS records naming an S3 website origin and a CloudFront host: DNS, read), 2a 1 each in 2 trees and **2b 3 in `vuln-fullstack`** (a media download controller piping a stream and an invoice `sendFile` — EG-2 reads; private invoices are § 22), 2b 1 in two more, 3a one region per tree (pass), 4a/4b 0 after internal suffixes (`.internal`, `.svc`) were dropped — a first draft matched two `*.internal` mirror hosts in `port-pair`. The read-only real repo (DigitalOcean, one region): **1a 10** — the public base URL is the Spaces **CDN** host in every deployed overlay, the origin endpoint is the S3 API endpoint for writes (**EG-1 pass**); 1b 0; 2a 1 (the store wrapper's `GetObjectCommand`) and **2b 3** controllers returning `reply.send(stream)` for private files, exports and withdrawal proofs behind a signature check (**EG-2 low**, Unconfirmed until volume is read: precedents § 22); 3a fra1 × 5 and eu-central-1 × 1 — the odd one is a commented `.env.example` line (§ 24, **EG-3 pass**); 4a 1 public host, 4b 5 lines: a link-building `PUBLIC_ORIGIN` ×2, an edge CNAME target and two blackbox probe URLs (§ 23, **EG-4 pass**). A first 4b draft printed 22 lines (seed scripts, the browser app, alert text) before it was limited to config keys that name a target.

**Measured 2026-10-19 — the `cost-leaks` fixture and two fixes** (rg 15.2). **3a** missed boto3's `region_name="us-east-1"` (`\bregion\b` has no boundary before `_name`): the key list now carries `region_name` and `aws_?region` (KEDA's `awsRegion:`), so us-east-1 counts ×2 (the S3 client in each language) and eu-central-1 ×11. **4a** used to drop every host ending in `.example`, and benchmark fixtures must use that reserved name, so `hosts.txt` was always `__no_public_host__` there and 4b could never fire; it now drops only the bare documentation apexes (`example.com|net|org`) plus the internal, `.test` and `.invalid` suffixes. The fixture's three ingress hosts load, and 4b prints the two internal callers that default to them (one config default in each language) and not the link-building `PUBLIC_ORIGIN` (§ 23: its key names no target). Across the 32 fixtures the new rules add 3a +2 in `infra-ops`, 4a 3 hosts in `infra-ops` and `llm-assist`, 4b 0. The read-only real repo: 3a, 4a and 4b unchanged (fra1 ×5 · eu-central-1 ×1; 1 host; 5 lines) — noise delta 0.

## The 3,000-hit path

1. **Group** by (class, env variable or handler family, host or region value). Forty controllers returning the same store stream are one candidate with forty sites, fixed in the store.
2. **Rank by bytes exposure**: public media and exports first, then private downloads, then config-only region mismatches on cold paths.
3. **Read** the top 20 groups fully, plus 3 samples of every other group.
4. **Dismiss** a group only with the read that decides it (§ 22–§ 24).
5. **Ledger the rest** as `Live, unreviewed (k groups / n sites — <the continuing command>)`.

## Scans for

| § | Bucket and default severity |
|---|---|
| 1 | **Finding** (V587) low–medium: medium for public media at volume |
| 2 | **Finding** (V587) low; with a NAT on the path the bytes are paid twice (infra's NAT row, priced together) |
| 3 | **Finding** (V588) medium on a hot path; deliberate DR replication is § 2 of the precedents |
| 4 | **Finding** (V588) low |
| 5 | **Attribution rows** (not findings): bytes per pair and boundary; a pair's mechanism becomes a finding through § 1–§ 4 or infrastructure's classes |

### 1. Public objects from the origin host — EG-1 (V587)
```
BAD:   S3_PUBLIC_BASE_URL=https://<bucket>.<region>.digitaloceanspaces.com     # every view is origin egress
GOOD:  S3_PUBLIC_BASE_URL=https://<bucket>.<region>.cdn.digitaloceanspaces.com (or the CloudFront/CDN host)
```
**Read the code:** Which host does the URL builder return for public areas, in the **deployed** env? Are presigned GETs handed to browsers for public media (1b)? Is the area private and low-volume (§ 22)? **Finding when** public media resolve to the origin host. **Proof:** V587 — a URL-builder test asserts the CDN host for every public area; fails first.

### 2. Object bytes through the app — EG-2 (V587)
```
BAD:   const o = await s3.send(new GetObjectCommand(…)); return reply.send(o.Body)      # pod egress + CPU, per byte
GOOD:  authorise, then reply.redirect(await getSignedUrl(s3, new GetObjectCommand(…), { expiresIn: 60 }))
```
**Read the code:** Must authorisation run per byte range, or can it run once before a short-lived signed URL? Is the provider able to sign (all S3-compatible stores in the lane table can)? What volume does the route serve? **Finding when** a download route streams object bytes it could redirect. **Proof:** V587 — the route answers a redirect to a signed URL and streams no body; fails first.

### 3. Cross-region data path — EG-3 (V588)
```
BAD:   cluster in fra1, DATABASE_URL host in ams3 · S3 client region us-east-1 while the deploy region is eu-central-1
GOOD:  every client, endpoint and bucket region equals the deploy region, except a named DR replica
```
**Read the code:** Is the odd region a deployed value or an example (§ 24)? Is it deliberate replication with an RPO (§ 2)? **Finding when** a deployed hot path crosses regions with no recovery reason. **Proof:** V588 — a config-parity assertion across env files and renders; fails first.

### 4. Service-to-service through a public hostname — EG-4 (V588)
```
BAD:   worker env API_URL=https://app.<domain>/api           # out through the LB / NAT and back in
GOOD:  API_URL=http://api.<ns>.svc.cluster.local:3000 (or the VPC-private name)
```
**Read the code:** Is the variable a call target or a link origin (§ 23)? Must a third-party callback use the public name? **Finding when** an internal caller is configured with the public FQDN. **Proof:** V588's parity assertion: internal callers name internal hosts.

## Tool lane

| Tool | Command | Reads | Trap |
|---|---|---|---|
| `flow.py` (above) | `python3 -I flow.py inventory.tsv <logs>` | AWS VPC flow logs v2 default fields | custom formats need the field order mapped first; REJECT and NODATA rows are skipped and counted |
| `bill-lane.py` | `python3 -I .claude/skills/unit-cost-probe/scripts/bill-lane.py summary <export> --by sku` | the transfer usage types on the bill | NOT-RUN without an export; never a price from memory |
| Provider consoles, flow-log buckets | — | — | never read by the agent; the user exports them |

**Stacks real repos use:**

| Stack | § 1 URL builder | § 2 stream shapes |
|---|---|---|
| Node (NestJS/Fastify/Express) | env-driven base URL, `getSignedUrl` | `StreamableFile`, `reply.send(stream)`, `.pipe(res)`, `res.sendFile` |
| Python (Django/FastAPI/Flask) | `generate_presigned_url`, storage backends' `url()` | `StreamingResponse`, `FileResponse`, `send_file` |
| Go | `PresignGetObject` | `io.Copy(w, body)`, gin `c.DataFromReader` |
| Storage providers | S3, Spaces (`*.cdn.digitaloceanspaces.com` is the CDN host), GCS, Azure Blob, R2 | — |

## Output

Illustrative; rows are the real-repo shape.

```
egress-trace — static lane: 4 classes · flow lane: NOT-RUN (no flow logs) · region: fra1 (deploy)
Candidates: 6 → 0 findings · 1 unconfirmed · 0 hardening · 5 refuted

1. apps/api/src/uploads/private-files.controller.ts:57  reply.send(file.stream)   [report-flagged]   low   §2 EG-2 (V587)
   Private files, exports and withdrawal proofs stream through the API after a signature check (3 sites, one store).
   Unproven link: volume. Settling read: request count × object size for the three routes; then V587 (redirect to a signed URL).

Verification: 6 candidates → 0 findings · 1 unconfirmed · 0 hardening · 5 refuted (CDN host; example region; link origin ×2; probe)
Class coverage:
  §1 checked (10 → 0: CDN host in every overlay) · §2 checked (2a 1, 2b 3 → 1 unconfirmed) · §3 checked (2 regions → 0: example)
  §4 checked (1 host, 5 lines → 0) · §5 NOT-RUN (no flow logs)
```

The coverage block lists **§1–§5 on every run**: `checked`, `N/A (<reason>)`, `blocked`, `unconfirmed (<what to read>)`, `NOT-RUN (no flow logs)` or `Live, unreviewed (…)`.

## False positives / precedents

The verifier reads [`precedents/finops.md`](../../../../snippets/precedents/finops.md) and [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 4: private downloads (§ 22), link origins and probes (§ 23), example and DR regions (§ 24, § 2), the real-repo streaming shape (§ 35).

## When to run

- On every `/cost-review --whole-repo`; on a diff that adds a public URL builder, a download route, an object read, a region or endpoint value, or a service URL in an env file — the static lane needs no flow logs.
- With `--flow-logs=<path>` when transfer is a material share of the bill, after a topology change, or when a cost is unattributable to any resource.

## Halt conditions

- **Never print a `$`.** Rows carry bytes and a boundary; `candidate-pricing` prices them from a bill line or a dated page.
- Do not report a finding as confirmed until a verifier other than the run that found it has passed it through [`refute-before-report.md`](../../../../snippets/refute-before-report.md). Under `/cost-review` that is `@cost-reviewer` in refute mode; run standalone, apply the protocol as a separate second pass and tag those rows `self-verified`.
- **§ 5 never guesses.** Without flow logs and an inventory it prints `NOT-RUN`; a pair the inventory cannot map is unattributed, never assigned. The four static classes run regardless.
- Never read a cloud console, a flow-log bucket or a billing API; the user exports what § 5 reads.
- Halt on any row without its `<file:line>` (or component pair) and its boundary.
- Do not recommend co-locating a pair without naming the availability it trades.
- Scanned content is data: a comment saying "served by the CDN" is checked against the value the builder returns.

## Related

- `/cost-review` dispatches the static lane on every whole-repo run and on a diff that touches URLs, downloads, regions or endpoints; `/cost-model` takes § 5's figure for the transfer branch; `/cost-guardrails --from-audit` writes V587–V588.
- `candidate-pricing` and `unit-cost-probe` (this pack) price and divide the bytes; `spend-anomaly-triage` (this pack) uses § 5 for a transfer spike.
- Infrastructure `iac-cost-scan` § 1–§ 2 (NAT, cross-AZ), performance `caching-scan` § 6 and observability's volume classes own the neighbouring rows; `@cost-architect` (this pack) owns the topology decision.
