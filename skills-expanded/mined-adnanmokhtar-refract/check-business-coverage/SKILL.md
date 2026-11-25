---
name: check-business-coverage
description: "Business cycles: forward action with no inverse, API-only inverse, send without resend, unsubscribe, erasure, dead ends."
kind: skill
pack: business
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: check-business-coverage

## Premise

Half-cycles ship for a structural reason: the forward action is the feature and the inverse is "the edge case". Demos walk forward, tickets are filed against forward, and the inverse drops below the line every sprint — subscribe with no cancel, invite with no revoke, an export with no status, a marketing mail with no one-click unsubscribe, an account with no deletion, an expired link with no way to ask for another. The cost lands where nobody measures it: support, a store review, a regulator, a job queue full of retries ([`missing-counterparts.md`](../../ai-patterns/missing-counterparts.md) § What half-cycles actually cost).

This skill owns research ids CY-1…CY-6, shipped as `BIZ-<id>`. It used to be a walk with matrices and no probe, and it halted when `ai/business-flows.md` was absent while its own input line said "scan the codebase if missing". It now builds the inventory from the routes (the flows file is optional: it adds declared cycles, it does not gate the run), pairs every forward route with its inverse by resource, and keeps the walk — roles, error recovery — as a lane that runs only with `--live`. `@business-auditor` judges these rows and owns the walk.

**Every finding cites the forward site `<file:line>` (the route, the handler) + the inverse searched for and where ("none after the written search: routes under `/invites`, the settings UI, the account page") + the role that has the forward action + the oracle (a route-pair diff, an end-to-end inverse, a captured raw message) or the test that would settle it + the fix in the project's own routing and UI idiom.** "Every forward has an inverse" is never printed; the output is the class-coverage block (§ Output). Verification follows [`refute-before-report.md`](../../../../snippets/refute-before-report.md) with [`precedents/business.md`](../../../../snippets/precedents/business.md); the oracles are [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Business, V478, V483 and V484.

## The rule

A candidate is a finding when all four hold:

1. **Reachable.** The forward action is served on a production surface and a real role can take it (a route mounted under the real prefix, a screen in the route table, a handler a consumer calls).
2. **The inventory is read, not assumed.** The routes come from a route table the run built (§ Read the inventory first); a framework the inventory did not cover is read by hand and its rows say so.
3. **No existing control, across surfaces.** The inverse under another verb (archive, close, void), a provider-hosted portal the app links to (§ 39), an admin inverse for an admin forward (§ 40), an ESP that injects the unsubscribe headers (§ 38), an asynchronous deletion request with an SLA (§ 23).
4. **The oracle fired, or the fact is two-ended.** The route-pair diff lists the pair and the written search found no inverse; or the end-to-end inverse failed; or the raw message lacks the header pair.

## Boundaries

- **The screen-level error, empty and loading states** → ui-ux `ui-state-scan`, when installed; §6 here owns the *business-cycle* dead end (an expired link with no way to request another, a declined card with no other payment path), not the component's error state. Without the pack, screen states are tagged `ui state (owner pack ui-ux not installed)`.
- **In-app account deletion for mobile apps** → mobile `store-compliance-scan` G7 (§ 42); **a route nobody calls** in general → product `feature-surface-scan` §2. Each when installed, tagged otherwise.
- **Who may take an inverse** (authorization on cancel, refund, revoke) → security, when installed; **the legality of the state edge the inverse takes** → `lifecycle-scan` (this pack); **records the inverse must not erase** → `ledger-scan` §8 (this pack).
- **The experience of a flow** — discoverability, guidance, clicks-to-find — is `@business-auditor`'s walk (`--live`); this skill owns whether each forward action has its inverse, resend, status and exit.

## Read the inventory first — routes, inverses, the declared cycles

Written into the run folder (`$OUT/routes.tsv`: `METHOD<TAB>path<TAB>site`, `$OUT/pairs.txt`), never into the audited repo. Sources, in order:
1. **product `surface-map.py --inventory`**, when the product pack is installed: served routes for Nest, Express/Fastify/Koa/Hono, Next, SvelteKit, FastAPI/Flask, Django/DRF, Rails, Laravel and Go, with global prefixes and versions resolved — its `ROUTE` rows are this skill's table.
2. **backend `dto-types.py --routes`**, when the backend pack is installed (NestJS mounts only).
3. **The per-framework greps** below (grep 0c): one line per decorator or route call. Without a prefix join, pair by controller file by hand and print §1–§2 `Live, unreviewed` for the rest.

`ai/business-flows.md` and `ai/users-and-personas.md`, when present, add declared cycles and roles; when absent, the run says so and continues on the routes.

## Adapt to the codebase — the lanes

| Lane | Forward / inverse shapes | Inverse that is not a DELETE (decoy) | Mail and erasure |
|---|---|---|---|
| **TypeScript** — NestJS, Express / Fastify, Next route handlers | `@Post()` on a collection with `@Get(':id')`; `router.post('/invites')`; `POST /x/:id/start` | `POST /x/:id/archive`, `/cancel`, `/close`, `/void`; a soft-delete flag | nodemailer / SES / SendGrid / Resend / Postmark calls; `DELETE /me`, `/account` |
| **Python** — Django + DRF, FastAPI | `ModelViewSet` gives create and destroy unless `http_method_names` or the mixins drop one; `@router.post` | `@action(detail=True, methods=['post'])` named `cancel`, `revoke` | `send_mail`, `EmailMessage(headers=…)`; Django `User.delete()` views |
| **Ruby** — Rails | `resources :invites, only: [:create]` (the `only:` list is the read) | `member { post :cancel }` | ActionMailer `headers['List-Unsubscribe']` |
| **PHP** — Laravel | `Route::post`, `Route::apiResource(...)->only([...])` | `Route::post('{x}/cancel')` | `Mailable::headers()` |
| **JVM / Go / .NET** | `@PostMapping` / `@DeleteMapping`; chi / gin / echo verbs; `[HttpPost]` / `[HttpDelete]` | an action endpoint | the mail client's header API |
| **Providers** | Stripe Checkout / subscriptions; app-store subscriptions | Stripe Customer Portal (cancel, update card), store subscription management — inverses when linked (§ 39) | an ESP that adds `List-Unsubscribe` itself (§ 38) |

## Pre-flight greps

Run as **one** script from the repo root (bash 3.2-safe). Grep **N** feeds §N; grep 0 builds the inventory. Every `rg` names its path; include globs first, exclusions last; exclusions start with `**/`. Every grep ends in `ck`: rg exit 2 is a **blocked** class, never zero hits.

```bash
ROOTS=(.)     # server code: ROOTS=(apps/api/src services/accounts)
WEB=(.)       # client code that would hold the inverse's entry point: WEB=(apps/web/src apps/admin/src)
OUT="${OUT:-$(mktemp -d "${TMPDIR:-/tmp}/cycles.XXXXXX")}"; mkdir -p "$OUT/none"
h() { printf '## %s\n' "$1"; }; ck() { [ "$2" -lt 2 ] || echo "$1 BLOCKED (rg exit $2) — the class is blocked, never 0 hits"; }
CODE=(-g '*.{ts,tsx,mts,cts,js,jsx,mjs,cjs,py,rb,php,java,kt,go,cs,vue,svelte}')
X=(-g '!**/node_modules/**' -g '!**/vendor/**' -g '!**/{dist,build,out,target,coverage,.next,.venv,generated,__generated__}/**'
   -g '!**/{test,tests,__tests__,spec,specs,e2e,fixtures,__fixtures__,mocks,__mocks__,testdata,seeds,seeders}/**'
   -g '!**/*.{spec,test,e2e-spec,stories,d}.*' -g '!**/*.test-data.*' -g '!**/*.fixture*.*' -g '!**/test_*.py' -g '!**/*_test.go'
   -g '!**/{migrations,migration,db/migrate}/**' -g '!**/{locales,locale,i18n,translations}/**' -g '!**/{docs,ai,.claude}/**' -g '!**/*.min.*')
NC=(rg -v --pcre2 '^[^:]+:\d+:\s*(?://|/\*|\*(?:\s|/|$)|#(?!\[))')
SM=.claude/skills/feature-surface-scan/scripts/surface-map.py      # product pack
DT=.claude/skills/validation-boundary-scan/scripts/dto-types.py    # backend pack
# 0a the route table: surface-map (multi-framework) → dto-types (Nest) → greps (0c, hand-paired)
if command -v python3 >/dev/null 2>&1 && [ -f "$SM" ]; then python3 -I -B "$SM" . --inventory --classes=2 > "$OUT/sm.tsv" 2> "$OUT/sm.err"; echo "0a surface-map exit $?"
  awk -F'\t' '/^# ROUTE/{f=1;next} /^# /{f=0} f{print $2"\t"$4"\t"$5}' "$OUT/sm.tsv" > "$OUT/routes.tsv"
elif command -v python3 >/dev/null 2>&1 && [ -f "$DT" ]; then python3 -I -B "$DT" --routes > "$OUT/dt.tsv" 2>/dev/null; echo "0a dto-types --routes exit $? (Nest only; read its columns into routes.tsv)"
else echo '0a NOT-RUN (no route inventory script): grep 0c lists the decorators; §1–§2 are paired by hand per controller'; : > "$OUT/routes.tsv"; fi
h 0a; wc -l < "$OUT/routes.tsv"
# 0b the pairing: every POST that creates on a CRUD collection or names a forward verb, and the inverse looked for under the same resource
python3 -I - "$OUT/routes.tsv" > "$OUT/pairs.txt" <<'PY'
import re, sys, collections
INV = {'create': 'delete|remove|destroy|archive|cancel|close|deactivate|void|revoke', 'add': 'remove|delete|unlink|detach',
       'invite': 'revoke|cancel|delete|uninvite|remove', 'invites': 'revoke|cancel|delete|uninvite|remove', 'subscribe': 'unsubscribe|cancel',
       'enable': 'disable|deactivate|turn-off', 'connect': 'disconnect|unlink|revoke|remove', 'share': 'unshare|revoke|remove',
       'start': 'stop|cancel|pause|abort|end', 'follow': 'unfollow', 'block': 'unblock', 'pin': 'unpin', 'schedule': 'unschedule|cancel',
       'grant': 'revoke|remove', 'attach': 'detach|remove', 'link': 'unlink|disconnect', 'publish': 'unpublish|archive|withdraw',
       'lock': 'unlock', 'activate': 'deactivate|suspend|disable', 'enroll': 'unenroll|disable|remove', 'archive': 'unarchive|restore',
       'hold': 'release|cancel', 'reserve': 'release|cancel', 'assign': 'unassign|reassign|release', 'suspend': 'resume|reactivate|unsuspend',
       'pause': 'resume|unpause', 'register': 'delete|deactivate|unregister', 'join': 'leave', 'install': 'uninstall|remove'}
DEL_OK = {'create', 'add', 'invite', 'invites', 'connect', 'share', 'link', 'attach', 'register', 'install', 'subscribe', 'enroll'}
P = re.compile(r'^[:{<*]|^\[')
rows = [l.rstrip('\n').split('\t') for l in open(sys.argv[1]) if l.count('\t') >= 1]
rows = [(r[0].upper(), r[1], r[2] if len(r) > 2 else '') for r in rows if r[0].upper() in ('GET', 'POST', 'PUT', 'PATCH', 'DELETE')]
segs = lambda p: [s for s in p.strip('/').split('/') if s and not P.match(s)]
items = {'/'.join(segs('/'.join(p.strip('/').split('/')[:-1]))) for _, p, _ in rows if p.strip('/') and P.match(p.strip('/').split('/')[-1])}
fam = collections.defaultdict(list)
for m, p, s in rows:
    for i in range(1, len(segs(p)) + 1):
        fam['/'.join(segs(p)[:i])].append((m, p))
checked, miss = 0, []
for m, p, site in rows:
    s = segs(p)
    if m != 'POST' or not s: continue
    last = s[-1].lower(); raw = p.rstrip('/').split('/')[-1]
    verb = last if last in INV else ('create' if not P.match(raw) and '/'.join(s) in items else None)
    if not verb: continue
    res = '/'.join(s[:-1]) if last in INV else '/'.join(s); checked += 1
    inv = re.compile(r'(?:^|[-_/])(?:' + INV[verb] + r')(?:$|[-_/])', re.I)
    ok = any(inv.search(segs(q)[-1]) for _, q in fam[res] if segs(q)) or (verb in DEL_OK and any(x == 'DELETE' for x, _ in fam[res]))
    if not ok: miss.append('%s\tPOST %s\t%s' % (verb, p, site))
print('CY-1 forward routes %d · no inverse under the same resource %d' % (checked, len(miss)))
print('\n'.join(miss))
PY
echo "0b pairing exit $?"; head -1 "$OUT/pairs.txt"
# 0c the hand lane: route decorators and calls per framework (also the cross-check of 0a's count)
h 0c; rg -n --pcre2 '@(Post|Delete|Put|Patch)\(|@(Post|Delete|Put|Patch)Mapping\(|\b(router|app|fastify|server|r)\.(post|delete|put|patch)\(\s*["\x27`]|@\w+\.(post|delete|put|patch)\(\s*["\x27]|\bRoute::(post|delete|put|patch|resource|apiResource)\(|^\s*resources?\s+:\w+|\.(POST|DELETE|PUT|PATCH)\(\s*"/|\[Http(Post|Delete|Put|Patch)' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}" | wc -l; ck 0c ${PIPESTATUS[0]}
h 0d; rg -l --pcre2 '\b(cycles?|forward|inverse|counterparts?)\b' -g 'ai/business-flows.md' -g 'ai/users-and-personas.md' -g '!**/node_modules/**' .; ck 0d $?
# 2 CY-2 inverse routes in the API (2a) and, per inverse path, a reference in the client roots (2b: none = API-only)
grep -iE $'^(DELETE\t|POST\t[^\t]*/(cancel|revoke|unsubscribe|disable|disconnect|deactivate|remove|unlink|leave|archive|close)\\b)' "$OUT/routes.tsv" > "$OUT/inverse.tsv"; h 2a; wc -l < "$OUT/inverse.tsv"
h 2b; while IFS="$(printf '\t')" read -r m p s; do seg=$(printf '%s' "$p" | tr '/' '\n' | grep -v '^[:{<*[]' | grep -v '^$' | tail -2 | paste -sd'\t' -); [ -n "$seg" ] || continue; a=${seg%%$(printf '\t')*}; b=${seg##*$(printf '\t')}; pat="$a"; [ "$a" = "$b" ] || pat="$a/[^\"'\x60\\s]{0,80}$b"; rg -q --pcre2 "$pat" "${CODE[@]}" "${X[@]}" "${WEB[@]}" 2>/dev/null || printf '%s %s\t%s\tno client reference to %s\n' "$m" "$p" "$s" "$pat"; done < "$OUT/inverse.tsv" > "$OUT/apionly.txt"; wc -l < "$OUT/apionly.txt"
# 3 CY-3 sends (3a) vs resends (3b); user-started async work (3c) — is there a status route or screen?
h 3a; rg -n --pcre2 '(?i)\b(send|email|mail|deliver)\w*(invite|invitation|verification|verify|otp|code|magic_?link|reset|confirmation|receipt|activation)\w*\s*\(' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"; ck 3a ${PIPESTATUS[0]}
h 3b; rg -n --pcre2 '(?i)\bre_?send\w*' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}" | wc -l; ck 3b ${PIPESTATUS[0]}
h 3c; rg -n --pcre2 '(?i)\b(queue|\w+Queue)\.add\(\s*["\x27]\w*(export|import|report|bulk|sync|generate|upload)\w*|\b(enqueue|dispatch|apply_async|perform_later|delay)\w*\([^)\n]*(export|import|report|bulk)' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"; ck 3c ${PIPESTATUS[0]}
# 4 CY-4 marketing senders (4a: files that send mail and name marketing) and the RFC 8058 header pair (4b)
rg -l --pcre2 '(?i)\b(newsletter|marketing|campaign|promotional|drip|broadcast)\w*|\b\w*digest_?(e?mail|send)\w*|\bweekly_?digest\b' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" > "$OUT/mkt.txt"; ck 4 $?
F=(); while IFS= read -r f; do F+=("$f"); done < "$OUT/mkt.txt"; [ ${#F[@]} -gt 0 ] || F=("$OUT/none")
h 4a; rg -l --pcre2 '(?i)\b(sendMail|sendEmail|send_mail|send_mass_mail|mailer|transporter\.send|ses\.send\w*|sgMail|resend\.emails|postmark|mailgun|nodemailer|ActionMailer|Mailable|EmailMessage)\b' "${F[@]}"; ck 4a $?
h 4b; rg -n --pcre2 '(?i)List-Unsubscribe(-Post)?|List-Unsubscribe=One-Click|\bunsubscribe_?(url|link|token)\b' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"; ck 4b ${PIPESTATUS[0]}
# 5 CY-5 web account deletion and data export routes and handlers (server and client)
h 5; rg -n --pcre2 '(?i)["\x27/](delete|erase|close|deactivate)[-_/]?(my[-_]?)?(account|me|user|profile|data)\b|\bgdpr\w*|\bdata[-_]?export\b|\bexport[-_]?(my[-_]?)?(data|account)\b|\bdownload[-_]?my[-_]?data\b|\btakeout\b|\bportability\b|\bright[-_]?to[-_]?(erasure|be[-_]?forgotten)\b' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" "${WEB[@]}" | "${NC[@]}"; ck 5 ${PIPESTATUS[0]}
# 6 CY-6 dead ends — expired / invalid / used tokens, links and codes (is there a request-new path?) and declined payments
h 6; rg -n --pcre2 '(?i)\b(expired|invalid|used|declined|insufficient)\w*[^\n]{0,40}\b(token|link|code|invite|otp|reset|card|payment)\w*' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}" | wc -l; ck 6 ${PIPESTATUS[0]}
```

**The walk lane (`--live=<url>` only).** With a non-production URL and the roles' test credentials, `@business-auditor` walks each §1 pair, each §6 error path and the role matrix (owner, member, viewer, another tenant, anonymous) through the UI, recording `Reachable @ <screen → click path>`, `MISSING (searched: …)`, `PARTIAL (<why>)` or `NOT WALKED (<no role / no env>)`. Without `--live`, every walk row prints `NOT WALKED (no --live)` and stays in the denominator: an audit that reached 12 of 50 cycles reports on 12.

### Measured (2026-10-19)

- **Real repo, read-only** (a NestJS 11 + Fastify + MikroORM 6 + React monorepo; server `ROOTS=(apps/api/src)`, client `WEB=(apps/web/src)`; product's `surface-map.py` in about 21 s; nothing written into the tree, checked with `find -newer`): 0a **1,310** served routes, 0c 714 decorator lines (the hand lane would have to pair those by controller). The pairing's first draft treated every POST whose last segment is not a parameter as a creation and listed **282** "creates" with no inverse — commands (`/confirm`, `/recalculate`, `/extract`) are not resources (§ 41). Restricted to POSTs on a CRUD collection (one with an item route `/x/:id`) plus named forward verbs, 0b checks **99** forward routes and lists **21** with no inverse under the same resource (10 creates, 3 links, 2 registers, 2 joins, 2 assigns, a start, an activate) — the read list: admin-created collections with no delete, store-connection `link` routes whose disconnect lives under another prefix, `register` routes whose account deletion exists elsewhere. **§2** 2a 115 inverse routes; the first draft searched the client for the inverse's last two literal segments joined by `/` and missed every path with a parameter between them (24 "API-only"); with the parameter allowed between, **3** remain — one is an OAuth token-revocation endpoint called by machine clients (product precedent § 1, refuted). **§3** 3a 5 send sites, 3b 4 resend lines, 3c 10 user-started async jobs. **§4** 0 marketing mail senders once the first draft's `digest` stopped matching `crypto.digest('hex')`: `N/A (no marketing mail)`; customer messages go out over a chat channel this skill does not cover (named on the lane line). **§5** 8 lines: a per-customer data-export route with its client action; account erasure runs through a pseudonymising port (`ledger-scan` §8 corroborates). **§6** 11 expired / invalid / declined lines — read for a request-new path per token kind.
- **Fixtures** (`benchmarks/fixtures/*`, 24 trees, product's `surface-map.py` as the inventory): 0 `rg` errors. `half-built-crm` (FastAPI + Jinja): 0b checks 3 forward routes and lists `POST /api/deals` and `POST /api/tasks` with no inverse — exactly its seeded asymmetries (deals with no update or delete; the task delete reachable only through a bulk route nobody serves, which product `feature-surface-scan` §1 owns). `backend-defects` lists `POST /products` and an OAuth client `register`; `vuln-fullstack` an `install` and a `register`; `port-pair` a stock `reserve` on both sides of its port (the release is a job, § 23 reads it). Trees with no route inventory print 0 forward routes and §1–§2 `N/A (no served routes)`.
- **Fixture `business-rules`** (2026-10-19, same staging, `WEB=(apps/web/src)`, product's `surface-map.py`): 0.94 s; 0a 22 served routes (19 Nest, 3 DRF — each ViewSet's `@action(methods=…)` route with its method; the first run read 6 `ANY` routes, a collection and an item per `router.register`), 0c 13. All 12 CY seeds print: 0b pairs both TS forward routes with no inverse (an invite, a carrier connection) beside two rows the read closes (an irrevocable payout, § 23; an export command, § 41); 2b both API-only inverses; 3a the one-shot verification mail (3b 0 resends) and 3c an export with no status; 4a both marketing senders with 4b 0 header lines; 5 the support-only account closure and an erase-only privacy endpoint; 6 counts the two dead ends. surface-map now gives DRF routes their methods (ModelViewSet and mixin actions, `@action(detail=, methods=, url_path=)`, APIView and generic-view method defs, `@api_view`), so 0b and 2a can pair DRF routes; the fixture's CY-1 and CY-2 seeds are TypeScript, and its three back-office actions are neither forward nor inverse verbs (0b and 2a unchanged).

## The 3,000-hit path

The pairing decides most of a large run. Read `pairs.txt` grouped by resource (one read of the controller per resource closes every route in it) in this order: account, subscription, payment and invite resources (legal and money exposure first); then user-created resources; admin-only resources last (§ 40). For §2 read `apionly.txt` per resource: a provider portal link (§ 39) or an admin screen closes it once. §3–§6 group by sender, job type and token kind. A group closes only with the reason checked (the inverse found under another verb, the portal link read, the ESP setting read); remaining groups print `Live, unreviewed (k resources / n routes)`.

## Scans for

Severity assumes a self-serve product with real users. Critical only for a legal obligation unmet on a reachable path (consent withdrawal, erasure) with the regulation cited.

| § | Class (`BIZ-` id) | Default severity | Oracle |
|---|---|---|---|
| 1 | CY-1 forward action without an inverse | high | V478 |
| 2 | CY-2 inverse exists in the API with no UI entry point for the forward's role | high | V478 |
| 3 | CY-3 send without resend; user-started async work without a status surface | medium | V478 |
| 4 | CY-4 marketing mail without one-click unsubscribe (RFC 8058 header pair) | high | V483 |
| 5 | CY-5 web account deletion or data export missing (GDPR Art. 17 / Art. 20) | high | V484 |
| 6 | CY-6 error path with no recovery (dead end) | medium | V478 |

### 1. Forward action without an inverse

```
BAD:   POST /team/invites            → no DELETE /team/invites/:id, no /revoke, no /cancel; the screen lists pending invites with no action
GOOD:  POST /team/invites  ·  POST /team/invites/:id/revoke  ·  a Revoke item in the pending-invites row menu
```
**Read the code:** For each `pairs.txt` row, is the inverse there under another verb or prefix (archive, close, void, a soft-delete flag on PATCH)? Is the POST a command rather than a resource (§ 41)? Is the action irrevocable by policy (signed, filed, paid out: § 23)? Is the inverse a provider portal the app links to (§ 39)? **Finding when** a user can create, subscribe, invite, connect, share or start something durable and the same role has no inverse in the system — only a support ticket or a database edit. **Proof:** V478 — the route-pair diff for the resource, then an end-to-end test that runs forward → inverse through the real routes and checks the state is undone.

### 2. Inverse in the API with no UI entry point

**Read the code:** For each `apionly.txt` row, is the inverse called by a client the 2b search did not cover (a mobile app, an admin app, a generated client with the path in a constant)? Which role has the forward action, and does that role's UI reach the inverse (§ 40)? **Finding when** an end user can take the forward action in the UI and the inverse exists only in the API or the admin panel. **Proof:** V478 — a UI test as the forward's role: the inverse's entry point is reachable from the screen that shows the resource.

### 3. Send without resend; async work without a status

**Read the code:** For each 3a send (invite, verification, reset, OTP, receipt), is there a resend path for the recipient (3b), rate-limited, that does not require re-entering data? For each 3c job a user starts (export, import, bulk action), is there a status route or screen, and a notification when it ends? **Finding when** a user who did not receive the message, or whose job is running, has no way to act but to repeat the forward action. **Proof:** V478 — the end-to-end path: send, simulate non-delivery, resend; start a job, poll the status surface to its end state.

### 4. Marketing mail without one-click unsubscribe

```
BAD:   transporter.sendMail({ to, subject: 'This week at Acme', html })        // a campaign with no List-Unsubscribe headers
GOOD:  headers: { 'List-Unsubscribe': '<https://acme.example/u/abc>', 'List-Unsubscribe-Post': 'List-Unsubscribe=One-Click' }
       + a POST endpoint that unsubscribes without a login
```
**Read the code:** Is the message marketing (a campaign, a newsletter, a promotion) or transactional (a receipt, a reset — no unsubscribe needed)? Does the sender set both headers of RFC 8058, and does the POST endpoint unsubscribe without authentication? Does the ESP inject them itself (§ 38 — read its dated docs or a captured raw message)? **Finding when** marketing mail leaves without the header pair, or the one-click endpoint requires a login. **Proof:** V483 — capture a raw message from the real sender (a test transport) and assert both headers; POST to the URL without a session and assert the subscription is gone.

### 5. Web account deletion or data export missing

**Read the code:** Can a signed-in user delete their account (or request deletion with a stated SLA: § 23) from the web app, and export their data in a machine-readable form? Does deletion keep records of fact under a legal obligation and pseudonymise the rest (`ledger-scan` §8, § 17)? Mobile apps' in-app deletion is mobile G7 (§ 42). **Finding when** the product processes personal data and the web path to erase or export it is missing or support-only. Cite GDPR Art. 17 / Art. 20 for a product serving the EU; without a jurisdiction the row is `[report-flagged]`. **Proof:** V484 — end to end: request export → a file with the user's data; request deletion → login refused, PII gone from mutable tables, records of fact intact.

### 6. Error path with no recovery

**Read the code:** For each token kind in grep 6 (invite, reset, verification, magic link, OTP), does the expired or used path offer a request-new action? For a declined or insufficient payment, is another method or a retry offered? The screen's error component is ui-ux's (§ Boundaries); this § owns whether the *cycle* has an exit. **Finding when** a reachable error leaves the user with no action but contacting support. The walk lane (`--live`) confirms the screen; without it the row is `[report-flagged]`. **Proof:** V478 — drive the error (expire the token, decline the test card) and assert a recovery action completes the cycle.

## Output

```
check-business-coverage — inventory: product surface-map.py (1,310 routes, nest); declared cycles: ai/business-flows.md absent (routes only)
Walk: NOT WALKED (no --live) — 14 pairs, 6 error paths, 5 roles stay in the denominator

Findings: 1 · Unconfirmed: 2 · Hardening: 3

1. src/team/team.controller.ts:192                                        [report-with-fix]  high
   §1 CY-1 — POST /team/invites; no revoke, cancel or DELETE under /team/invites (searched: routes, team settings screen).
   V478 failed: invite → no route undoes it; the pending invite stays redeemable. Fix: POST /team/invites/:id/revoke + row action.
2. src/partners/partners.controller.ts:411                                 [report-flagged]   high
   §1 CY-1 — POST /connected-stores/<provider>/link; the disconnect may live under /stores/:id. Settling: V478 forward → inverse.
3. src/auth/auth.controller.ts:538                                        [report-flagged]   high
   §5 CY-5 — POST /auth/register; account deletion found only as an admin erasure port. Settling: V484 as the user.

Routed: 2 → ui-ux ui-state-scan (error states) · 1 → product feature-surface-scan §2 (an uncalled route)
Verification: 22 candidates → 1 finding · 2 unconfirmed · 3 hardening · 16 refuted (self-verified; precedents §23, §40, §41)

Class coverage:
  §1 forward / inverse   checked (102 forward routes → 22 read → 1 finding, 1 unconfirmed)
  §2 API-only inverse    checked (2a 41 inverse routes, 2b 3 with no client reference → 0: admin app, § 40)
  §3 resend / status     checked (3a 5, 3b 19; 3c 10 jobs → 0: an export status screen covers all)
  §4 unsubscribe         N/A (no marketing mail sender)
  §5 erasure / export    checked (5: 8 lines → 1 unconfirmed)
  §6 dead ends           checked (29 lines → 0 static; walk NOT WALKED)
```

`[report-with-fix]`: the oracle failed on the real routes and the fix is local to the controller and the screen that shows the resource. `[report-flagged]`: one link is unproven (the inverse under another prefix, the client the search did not cover, the jurisdiction); the row names it and the settling oracle. The coverage block lists **all six** §s on every run: `checked (k → m)`, `N/A (<reason>)`, `blocked (<grep>: rg exit 2)`, `→ <owner> (k)`, `Live, unreviewed (k)` or, for walk rows, `NOT WALKED (<reason>)`.

## False positives / precedents

The verifier reads [`precedents/business.md`](../../../../snippets/precedents/business.md) and [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 4. The ones this skill meets most:
- § 23 irrevocable actions need no inverse, a legal hold blocks deletion on purpose, an asynchronous deletion request with an SLA is an inverse; § 41 a command POST is not a resource, and archive, close and soft-delete are inverses of create.
- § 38 an ESP that injects the unsubscribe headers; § 39 a provider-hosted portal linked from the app; § 40 an admin inverse for an admin forward; § 42 mobile store deletion is mobile's.

## When to run

- On any diff that adds a create, invite, subscribe, connect, share or start route, a mail sender, a token-based flow, a user-started job, or an account or data route — `/audit-business`'s cycle signal.
- On every whole-repo `/audit-business`, reporting all six §s; before an external audit (GDPR, a store review) or a launch.

## Halt conditions

- **Do not report a high row as confirmed until a separate verifier has refuted it.** That verifier is not the run that found it, gets the pair, the written search and the role — never this run's reasoning — and passes the row through [`refute-before-report.md`](../../../../snippets/refute-before-report.md) §1–§8 with [`precedents/business.md`](../../../../snippets/precedents/business.md). Under `/audit-business` that is `@business-auditor` in refute mode, then `@verifier` mode `refute` on every BLOCKER and HIGH; standalone, apply the protocol as a second pass and tag the rows `self-verified`. List the rest as Unconfirmed, Hardening or Refuted; never drop them.
- **Refuse "inverse missing" without the written search**: the routes under the resource, the client roots, the settings and account screens. "I did not find it" is not "it is not there".
- **Refuse a bare checkmark.** Every pair carries the path that makes it true, or `MISSING (searched: …)`, `PARTIAL (<why>)`, `NOT WALKED (<reason>)`.
- **Refuse "critical" without naming the regulation or policy** (GDPR article, RFC 8058, a store guideline) and the jurisdiction it applies in.
- **Never walk a production environment;** the walk lane needs `--live` with a non-production URL and test credentials, else every walk row is `NOT WALKED`.
- **Business decisions are not code fixes:** whether an action is irrevocable, which role owns an inverse, and a deletion SLA are the owner's call — the row names the decision and stops.
- **Do not grade a class another pack owns** (§ Boundaries). **Do not print "every forward has an inverse"** without the coverage block.

## Related

- `/audit-business` dispatches this skill and folds its coverage block into its class ledger; `@business-auditor` judges these rows and runs the walk. [`missing-counterparts.md`](../../ai-patterns/missing-counterparts.md) is the forward / inverse / completion / recovery table this skill pairs against; `lifecycle-scan` (the edge the inverse takes) and `ledger-scan` §8 (what deletion must keep) are the neighbours in this pack.
- product `feature-surface-scan` (`surface-map.py`, the route table), backend `dto-types.py --routes`, ui-ux `ui-state-scan`, mobile `store-compliance-scan` G7, when those packs are installed.

## Sources

From the business research (2026-10-19): RFC 8058 one-click unsubscribe (`List-Unsubscribe` + `List-Unsubscribe-Post: List-Unsubscribe=One-Click`), GDPR Art. 7(3), 17 and 20 (gdpr-info.eu, read 2026-10-19), App Store Review Guideline 5.1.1(v) for in-app deletion (owned by the mobile pack); the cycle classes CY-1…CY-6 and the pack's own forward / inverse tables. The real-repo and fixture counts are from read-only runs of the block above and of product's `surface-map.py`. Paraphrased; no text reproduced beyond identifiers.
