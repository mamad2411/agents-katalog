---
name: lifecycle-scan
description: "Lifecycle graph: unreachable and trap states, declared vs built graph, cross-aggregate status, provider events, history."
kind: skill
pack: business
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: lifecycle-scan

## Premise

An entity with a status column has a state machine whether anyone drew it or not. The graph is spread over three kinds of files: the **declaration** (an enum, a string union, a const array, a DB `CHECK` list or enum type), the **declared edges** (a transition table, an FSM library config) and the **writes** (`order.status = 'paid'`, `{ status: 'paid' }` in an update payload, a lowercase multi-line `update orders set status = 'paid' where status = 'pending'` in a template string). A per-line grep sees one of the three, which is how the pack's old probes printed an empty graph — a bare `src` path that exits 2, a case-sensitive single-line `UPDATE .*SET status` that matches nothing — and read it as clean. `scripts/status-graph.py` joins the three per machine and prints the graph, its reachability and terminality, and every write with its guard.

This skill owns research ids LC-1…LC-6, shipped as `BIZ-<id>`: unreachable or stale states, traps and missing terminals, the declared graph against the built one, two aggregates whose statuses disagree, provider events the mapping does not cover, and transitions that leave no history. `@workflow-integrity` judges these rows and keeps the transition matrix.

**Every finding cites the machine and its source `<file:line>` + the state or edge + the write or table row that makes it so (or "none after the written search") + the oracle (a graph diff, a model-based run, a provider replay) or the test that would settle it + the fix in the project's own lifecycle primitive (its transition table, its FSM config, its guarded setter).** A graph row is a candidate. "The lifecycle looks sound" is never printed; the output is the class-coverage block (§ Output). Verification follows [`refute-before-report.md`](../../../../snippets/refute-before-report.md) with [`precedents/business.md`](../../../../snippets/precedents/business.md); the oracles are [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Business, V474–V476 and V482.

## The rule

A candidate is a finding when all four hold:

1. **Reachable.** The writes run in production: a route, a consumer, a webhook, a cron, an admin action. A write under `migrations/` or `seeds/` is kept and tagged; a state reached only there is § 30's question, not a live edge.
2. **Version read.** The FSM library and its direct-write protection come from the lockfile and the config (XState 5, AASM `no_direct_assignment`, django-fsm-2 `protected=True`, viewflow.fsm, statesman, spatie model-states; Spring Statemachine's repository was archived on 2026-07-05). Without a lockfile the row is `UNREAD`.
3. **No existing control, across files.** A transition table every setter consults, an FSM library that owns the writes, a guarded `UPDATE … WHERE status = :from` with the row count checked, a reversal table that declares the way back, an explicit ignore list of provider events, a history insert in the same transaction.
4. **The oracle fired, or the fact is two-ended.** The graph diff, the model-based run or the replay failed on the real code, or the static fact cites both ends: the declared state and the searched-for write; the table row and the setter that skips it; the subscribed event type and the handler that never names it.

## Boundaries

- **An FSM library swallowing an illegal event, a terminal state re-opened through a library, a status write outside the machine when the library offers protection** → backend `state-transition-scan` §1–§2, when the backend pack is installed; it reads this skill's graph (`$OUT/graph/edges.tsv`) as its oracle. Without the pack the rows are listed tagged `fsm library (owner pack backend not installed)`.
- **An unconditional status write that loses a concurrent update** (read-modify-write, no `WHERE status = :from`) → database `transaction-scan` §8; **step skipping by the client, a late provider event re-opening a settled record** → security `logic-race-scan` §3; **a status the client can mass-assign** → security `@api-security-reviewer` (API3). Each when installed, tagged otherwise. §2 here owns whether the graph has a way out, not the race on the write.
- **Consumer dedupe and ordering of provider events** → distributed-systems `messaging-scan` §2, when installed; §5 here owns whether the mapping covers every subscribed type and keeps states monotone.
- **Money moved on a reversal edge** → `ledger-scan` §7 (this pack) conserves it; **the refund share** → `pricing-rule-scan` §9. **The inverse action a user can reach** (cancel, unsubscribe) → `check-business-coverage` (this pack); this skill owns the edges between states, not the existence of the paired verb.

## Read the graph first — `status-graph.py`

The graph is written into the run folder (`$OUT/graph/`: `states.tsv`, `edges.tsv`, `writes.tsv`, `report.txt`), never into the audited repo; the script refuses an `--out` inside a scanned root and exits 2. It reads the lanes below, merges machines by a normalised key (`OrderStatus`, `ORDER_STATUSES`, `order_status`, table `orders` → `order`), prints **set drift** when two sources list different states, prunes const arrays that are subsets of a larger machine (filter lists such as `CONFIRMED_STATUSES`, kept for guards), and groups writes no declaration covers into an **implied** machine (its set is declared nowhere: § 32). A write is attributed by its enum member, then its receiver, table or entity hint, then by which machine declares its literal; a literal many machines declare is **ambiguous** and is read, never counted (§ 33). Its guard is the write's own SQL `WHERE`, or a comparison on the field, an `includes(x.status)`, a transition-table name or a `canTransition`-style call above it in the same function; none is `unguarded` (from `*`).

Exit 0 means the graph was built; exit 2 means it could not be (a missing root, `--out` inside a root, no source file read, writes with no machine) and every § prints `blocked (status-graph exit 2)`, never `checked`. Its `--self-test` covers the TS, Python, Ruby and SQL lanes, XState, AASM and django-fsm, the predicate-vs-write split, the guard window and every exit.

## Adapt to the codebase — the lanes

| Lane | Declaration | Declared edges | Writes the script reads |
|---|---|---|---|
| **TypeScript / JS** — NestJS + MikroORM / Prisma / TypeORM / Drizzle, Express, raw SQL in template strings | `enum XStatus {}`, `type XStatus = 'a' \| 'b'`, `const X_STATUSES = [...] as const` (+ `typeof … [number]`, spreads, enum members), `const XStatus = { A: 'a' } as const`, class-property and `@Property({ default })` defaults | `*TRANSITIONS*` / `*REVERSALS*` / `ALLOWED_*` / `NEXT_*` objects of lists (`[]` = declared terminal); XState `createMachine({ states })` with `target` and `type: 'final'` | `x.status =`, `this._status =`, `{ status: 'paid' }` in create / update payloads (a key inside `where:` / `find…(` / a type union is a predicate), `nativeUpdate(E, { id, status: 'a' }, { status: 'b' })` (the first key guards the second) |
| **Python** — Django + DRF, SQLAlchemy | `class XStatus(models.TextChoices \| Enum \| StrEnum)`; `models.CharField(default=…)` | django-fsm `@transition(source=, target=)`; `transitions` `add_transition` and trigger/source/dest dicts | `obj.status =`, `.update(status='b')` after `.filter(status='a')`, `create(status=…)` |
| **Ruby** — Rails | `enum status: {…}` / `enum :status, […]`; AASM `state :x, initial: true` | AASM `event … transitions from:, to:` | `self.status =`, `update(status: :b)`, `update_column(:status, …)` |
| **PHP** — Laravel | backed `enum XStatus: string { case … }`; spatie state classes | spatie `allowTransition(A::class, B::class)` | `$x->status =`, `'status' => 'b'` in `update([...])` |
| **Java / Kotlin / .NET** — JPA, Spring, EF Core | `enum XStatus { A, B }` | Spring Statemachine `.source(S.A).target(S.B)`; stateless `.Configure(S.A).Permit(t, S.B)` | `setStatus(S.B)`, `x.Status = S.B` |
| **Go** | `type XStatus string` + typed consts | looplab/fsm `{Src: []string{…}, Dst: "…"}` | `o.Status = StatusB` |
| **SQL** (any file, and DDL inside migration code) | `create type x_status as enum`, `check (status in (…))`, `default '…'` | — | `update <t> set status = '<s>' [where status …]`, case-insensitive, multi-line |

Print the lanes the script reported. A lane present in the repo and absent from the script's ledger is read by hand and its § rows say so.

## Pre-flight greps

Run as **one** script from the repo root (bash 3.2-safe). G is the graph; grep **N** feeds §N. Every `rg` names its path (`.` or `"${ROOTS[@]}"`); include globs first, exclusions last, exclusions start with `**/`. Every grep ends in `ck`: rg exit 2 is a **blocked** class, never zero hits. Identifiers are word- and camelCase-bounded.

```bash
ROOTS=(.)   # server code; in a monorepo name the apps: ROOTS=(apps/api/src services/billing). The graph and the greps read the same roots
OUT="${OUT:-$(mktemp -d "${TMPDIR:-/tmp}/lifecycle.XXXXXX")}"; mkdir -p "$OUT/none"
h() { printf '## %s\n' "$1"; }; ck() { [ "$2" -lt 2 ] || echo "$1 BLOCKED (rg exit $2) — the class is blocked, never 0 hits"; }
CODE=(-g '*.{ts,mts,cts,js,mjs,cjs,py,rb,php,java,kt,go,cs}')
X=(-g '!**/node_modules/**' -g '!**/vendor/**' -g '!**/{dist,build,out,target,coverage,.next,.venv,generated,__generated__}/**'
   -g '!**/{test,tests,__tests__,spec,specs,e2e,fixtures,__fixtures__,mocks,__mocks__,testdata,seeds,seeders}/**'
   -g '!**/*.{spec,test,e2e-spec,stories,d}.*' -g '!**/*.test-data.*' -g '!**/*.fixture*.*' -g '!**/test_*.py' -g '!**/*_test.go'
   -g '!**/{migrations,migration,db/migrate}/**' -g '!**/{locales,locale,i18n,translations}/**' -g '!**/{docs,ai,.claude}/**' -g '!**/*.min.*')
M=(-g '**/{migrations,migration,db/migrate}/**' -g '**/*.sql' -g '**/schema.prisma' -g '**/db/schema.rb' -g '!**/node_modules/**' -g '!**/vendor/**')
NC=(rg -v --pcre2 '^[^:]+:\d+:\s*(?://|/\*|\*(?:\s|/|$)|#(?!\[))')   # drops comment-only lines
SG=.claude/skills/lifecycle-scan/scripts/status-graph.py
# 0a the declared graph (§3): a flows file, a state diagram, a lifecycle doc — the first one is passed as --declared
h 0a; rg -l --pcre2 '(?i)stateDiagram|\b\w+\s*(?:→|->|-->)\s*\w+' -g 'ai/business-flows.md' -g '**/docs/**/*.md' -g '**/*{lifecycle,state-machine,workflow,flows}*.md' -g '!**/node_modules/**' . > "$OUT/declared.txt"; ck 0a $?; cat "$OUT/declared.txt"
# G THE GRAPH — §1, §2, §3 directly; writes.tsv feeds §4 and §6
DECL=$(head -1 "$OUT/declared.txt")
if command -v python3 >/dev/null 2>&1 && [ -f "$SG" ]; then python3 -I -B "$SG" "${ROOTS[@]}" --out="$OUT/graph" ${DECL:+--declared="$DECL"} > "$OUT/graph.txt"; echo "G status-graph exit $? → $OUT/graph.txt"
else echo 'G NOT-RUN (python3 or status-graph.py absent): §1–§3 are read by hand from 0b and the writes, and print Live, unreviewed'; fi
# 0b declarations by grep (the cross-check of the script's machine count; the hand lane when G did not run)
h 0b; rg -n --pcre2 '\b(enum|type)\s+\w*(Status|State|Phase|Stage)\b|\b(const|let)\s+[A-Z_]*(STATUS|STATE|PHASE)(ES|S)?\b\s*(:[^=\n]+)?=|class\s+\w*(Status|State)\s*\([^)]*(Choices|Enum)|\benum\s+:?\w*(status|state)\b|\baasm\b|\bcreateMachine\(|@transition\(' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}" > "$OUT/decl.txt"; ck 0b ${PIPESTATUS[0]}; wc -l < "$OUT/decl.txt"
# 4 LC-4 cross-aggregate — files whose writes touch two machines (4a), and which of them open one transaction (4b)
h 4a; awk -F'\t' 'NR>1 && $4!="" && $4!~/,/ {split($1,a,":"); k=a[1]; if (index(m[k], "|"$4"|")==0) {m[k]=m[k]"|"$4"|"; n[k]++}} END {for (k in n) if (n[k]>1) print k"\t"m[k]}' "$OUT/graph/writes.tsv" 2>/dev/null | sort > "$OUT/multi.txt"; cat "$OUT/multi.txt"
F=(); while IFS="$(printf '\t')" read -r f _; do F+=("${ROOTS[0]}/$f"); done < "$OUT/multi.txt"; [ ${#F[@]} -gt 0 ] || F=("$OUT/none")
h 4b; rg -l --pcre2 '\b(transactional|\$transaction|withTransaction|runInTransaction|em\.transactional|atomic\(\)|transaction\.atomic|@Transactional|ActiveRecord::Base\.transaction|DB::transaction)\b' "${F[@]}"; ck 4b $?
# 5 LC-5 provider events — webhook dispatch sites (5a), provider-status maps (5b), declared ignore lists (5c), subscribed types in config (5d)
h 5a; rg -n --pcre2 '(?i)\bcase\s+["\x27](payment_intent|charge|invoice|customer\.subscription|checkout\.session|payout|refund|dispute|order|payment|transaction|subscription)[._][\w.]+["\x27]|\b(event|evt|payload|body|webhook)\w*\.(type|event_?type|event|status)\s*(===?|==)\s*["\x27]\w+[._]\w+' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"; ck 5a ${PIPESTATUS[0]}
h 5b; rg -n --pcre2 '(?i)\b\w*(provider|carrier|psp|gateway|stripe|remote|external|upstream|courier)\w*_?status_?(map|mapping|to_?\w*)\b\s*[:=]|\b(map|to|from)\w*(Provider|Carrier|Gateway|Remote|External|Psp|Courier)\w*Status\w*\s*\(|\bSTATUS_MAP\b|\bstatusMap\b' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"; ck 5b ${PIPESTATUS[0]}
h 5c; rg -n --pcre2 '(?i)\b(ignored|unhandled|skipped|noop|unsupported)_?(events?|event_?types?|statuses)\b\s*[:=]' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"; ck 5c ${PIPESTATUS[0]}
h 5d; rg -n --pcre2 '\benabled_events\b|stripe\s+listen\b[^\n]*--events|\bevents\s*:\s*\[\s*["\x27]\w+\.\w+' -g '**/*.{ts,js,py,rb,php,go,tf,yml,yaml,json,sh}' -g '!**/node_modules/**' -g '!**/{test,tests,__tests__,spec}/**' .; ck 5d $?
# 6 LC-6 history — history tables in the schema (6a); status-writing files with no history / audit insert (6b, the work list)
h 6a; rg -n -i --pcre2 'create\s+table\s+(if\s+not\s+exists\s+)?"?(\w+"?\.)?"?\w*(status_?(history|changes?|log|transitions?)|_history|_transitions|_timeline|_events|audit_?log)\w*' "${M[@]}" .; ck 6a $?
awk -F'\t' 'NR>1 && $8=="" && $5!="ambiguous" {split($1,a,":"); print a[1]}' "$OUT/graph/writes.tsv" 2>/dev/null | sort -u | sed "s|^|${ROOTS[0]}/|" > "$OUT/writers.txt"
F=(); while IFS= read -r f; do F+=("$f"); done < "$OUT/writers.txt"; [ ${#F[@]} -gt 0 ] || F=("$OUT/none")
h 6b; rg --files-without-match --pcre2 '(?i)\b\w*(history|statusChange|status_change|transition_?log|timeline|audit\w*|activity_?log|recordEvent|logTransition)\w*\s*\.?\s*(create|insert|push|add|record|log|save|persist)\w*\s*\(|insert\s+into\s+"?\w*(history|_changes|_transitions|_timeline|audit\w*|_events)' "${F[@]}" > "$OUT/nohistory.txt"; ck 6b $?; wc -l < "$OUT/nohistory.txt"
```

With several roots, `writes.tsv` paths are relative to the root that holds them; run the 4a/6b lines once per root (`ROOTS=(<root>)`) or prefix by hand.

### Measured (2026-10-19)

- **Real repo, read-only** (a NestJS 11 + Fastify + MikroORM 6 + React monorepo, `ROOTS=(apps/api/src)`, run from the repo root with `GIT_OPTIONAL_LOCKS=0`; nothing written into the tree, checked with `find -newer` on a stamp): the script reads 3,725 TypeScript files in about 7.5 s, exit 0. It builds **122 machines**, prunes **63 subset lists**, prints **92** with an edge, a write or a default and puts 30 declaration-only types (filters, view enums) on one line. **414 status writes:** 240 attributed, 132 ambiguous (`'pending'`, `'active'`, `'failed'` are declared by dozens of machines — § 33), 35 grouped into 14 implied machines, 7 written but not declared. The order machine merges a const array and a migration's `CHECK` (21 states) with a forward table and a separate **reversal table** (65 declared edges): the reversal edges out of `cancelled` and the delivered family are a declared way back, not a re-open (§ 29, refuted). The live **§2 candidate** is `awaiting_pickup`: it has no row in the forward table and no outgoing write the script can attribute, while the machine's own comment says a status the table lacks "moves anywhere" — so it is unconstrained rather than trapped; Unconfirmed until V474 shows which edges the setter allows from it. **§1** 41 machines print unreachable states and 49 more states are reached only by an ambiguous write; most are DB-checked vocabularies whose writers sit behind a repository the hint cannot name — read per machine, starting with the money-bearing ones. **§4** 4a 15 files write two attributed machines, 4b 6 of them open a transaction — the other 9 are the read list. **§5** 5a 11 dispatch sites, 5b 7 provider-status maps (carrier statuses), 5c 0 ignore lists, 5d 2 lines — both client realtime subscriptions, not provider webhooks (refuted on reading). **§6** 6a 9 history tables; 6b: 125 of the 126 files with an attributed status write insert no history row themselves — the read decides whether a repository, an ORM subscriber or an audit interceptor writes it. Before: the old `@workflow-integrity` probes printed `rg` exit 2 and 0 hits on this tree.
- **Fixtures** (`benchmarks/fixtures/*`, 24 trees, run from inside each): exit 0 on 22; the two trees with no source file exit 2 (`no source file read`), never an empty clean graph. `backend-defects` gives the XState order machine (`open → paid | cancelled`, `paid → shipped | refunded`, two `final` states) plus 4 unguarded writes to `refunded`, `cancelled` and `paid` from a service, a controller and a webhook — the library-bypass rows are backend `state-transition-scan` §2's seeds, listed here as corroboration. `ds-defects` and `vuln-fullstack` declare no state set for invoices, shipments and orders: their machines print `implied` (§ 32). `feature-refund`'s order machine is implied with every write guarded (`cmp:paid`, `cmp:pending`) — no trap, no unguarded write.
- **Fixture `business-rules`** (2026-10-19, same staging, one run per root): `status-graph.py` exit 0 on both (first run: 118 TS files, 6 machines, 13 writes; 104 Python files, 6 machines, 10 writes — after the integration pass's script fixes: 118 TS files, 5 machines, 10 writes; 104 Python files, 6 machines, 14 writes), about 0.6 s per root. All 12 LC seeds print: `LC-1 unreachable` (`awaiting_review`, `on_hold`), `LC-2 traps: disputed` and `LC-2 no terminal state` (the back office's subscription), `LC-3 declared, not built: delivered→return_requested` and `built, not declared: issued→void`, 4a both two-machine files with 4b empty, 5a the single handled case against 5d's four subscribed types (the graph agrees: payment `failed` and `refunded` unreachable), 5b the carrier map, 6b both writers with no history row. Decoys cleared at the read: `reopen … (ORDER_REVERSALS)` (§ 29), 5c a payout ignore list (§ 22), 6b an audited repair command (§ 21) and a help-article toggle (§ 31). With both roots in one `ROOTS`, 4b/6b print `BLOCKED (rg exit 2)` for the second root, as documented. **Script gaps measured here, fixed the same day** (each with a failing-first self-test case, `--self-test` 32 → 42): `status-graph.py` now reads only the `## <Machine>` section of `--declared`, TS computed enum keys in transition tables, django-fsm `source=[A, B]` lists and map-driven writes (the carrier map's 4 targets); it skips WHERE arguments, response bodies and other receivers' comparisons as guards; and `paid` / `credited` / `approved` are terminal when nothing leaves them (never a reopen source).

## The 3,000-hit path

The graph decides most of a large run. Read `$OUT/graph.txt` machine by machine in this order: machines with a declared table or FSM config (the project's own oracle: § 21, § 29); money-, order-, payment-, subscription- and invoice-bearing machines; machines with unguarded writes; then the rest. Inside a machine: set drift first (one read of both sources), then §2 traps and missing terminals, §1 unreachable states (an ambiguous or migration-only reach is read, not counted), §3 against `--declared`. §4 by file in 4a (one read per file: one transaction, or an outbox, or a saga — which the distributed-systems pack owns); §5 per provider (one read of the handler and the subscribed types); §6 per critical machine (one read of the repository or interceptor that would write history). A group closes only with the reason checked (the table row read, the guard read, the transaction read); remaining groups print `Live, unreviewed (k machines / n writes)` with the command that continues them (`--machine=<key>`).

## Scans for

Severity assumes a production entity that carries money, stock, access or a legal obligation. Grade lower for a low-stakes toggle (§ 31).

| § | Class (`BIZ-` id) | Default severity | Oracle |
|---|---|---|---|
| 1 | LC-1 unreachable state or stale enum value | medium | V474 |
| 2 | LC-2 trap state, or no terminal state | high | V474 |
| 3 | LC-3 declared graph ≠ implemented graph | medium | V474 |
| 4 | LC-4 cross-aggregate status disagreement | high | V475 |
| 5 | LC-5 provider status or event mapping incomplete, or not monotone | high | V476 |
| 6 | LC-6 transitions on a critical entity leave no history | medium | V482 |

### 1. Unreachable state or stale enum value

```
BAD:   ORDER_STATUSES = [..., 'awaiting_review', ...]   // no write, no table row, no default reaches it; a reader still branches on it
GOOD:  every declared state is a target of a table row, a guarded write, an FSM event or the default — or listed as legacy and locked (§ 30)
```
**Read the code:** Is the state the target of any write, including one the script marked ambiguous or tagged `migration`? Does a reader (a report, a filter, a UI tab) branch on it as if rows could enter it? Is it written by an import, a sync from a provider, or a raw SQL path in another service? Does a `set drift` line show the DB accepts a state the code no longer declares, or the reverse? **Finding when** a live reader depends on a state nothing can reach, or a declared set and the DB set disagree on a state a writer uses. **Proof:** V474 — the graph diff: declared states minus reachable states is the expected set (empty, or the documented legacy list).

### 2. Trap state, or no terminal state

```
BAD:   STATUS_TRANSITIONS lacks 'in_review'; the setter throws on any move out of it → orders stuck forever
GOOD:  every non-terminal state has an outgoing edge; terminals are declared ([] in the table, type: 'final', a terminal name)
```
**Read the code:** For each trap the script prints, read the setter: does a state missing from the table mean "locked", "moves anywhere" (the measured monorepo's rule) or a crash? Is there a cron, a provider event or an admin repair that leaves it? For a machine with unguarded writes the trap list is `undetermined`: read the writers and say which states they leave from. Is there at least one terminal state? **Finding when** an entity on a production path can enter a non-terminal state with no way out, or a machine has no terminal state and no documented reason. **Proof:** V474 — reachability over the extracted graph from the initial state: every non-terminal state reaches a terminal one.

### 3. Declared graph ≠ implemented graph

**Read the code:** Which document declares the lifecycle (0a: `ai/business-flows.md`, a state diagram in docs)? For each `LC-3 declared, not built` edge, is the edge implemented under another name (a reversal table, an FSM event)? For each `built, not declared` edge, is it a deliberate admin repair (§ 21) or drift? **Finding when** an edge the business relies on is missing from the code, or the code allows an edge the declared lifecycle forbids on a money- or access-bearing entity. Without a declared graph the § prints `N/A (no declared lifecycle)` and names the missing document as the gap. **Proof:** V474 — the graph diff against the declared edges.

### 4. Cross-aggregate status disagreement

```
BAD:   await payments.markFailed(p); /* crash */ await orders.update(o.id, { status: 'paid' })   // two handlers, two transactions
GOOD:  one transaction for both writes, or an outbox event that the second aggregate consumes idempotently, plus a reconciling sweep
```
**Read the code:** For each 4a file, which two machines does it write, and can a crash, a retry or a concurrent handler leave one written and the other not? Is there a policy that allows the combination ("refund without return" written down: § 27)? Is there a sweep that finds disagreeing pairs? The transaction mechanics and the outbox are database and distributed-systems' classes (§ Boundaries); this § owns whether the two statuses can lie to each other. **Finding when** a reachable sequence leaves two related aggregates in a combination the business forbids (order `paid` with payment `failed`; shipment `delivered` with order `cancelled`). **Proof:** V475 — a model-based run (fast-check `fc.commands`, Hypothesis `RuleBasedStateMachine`) over the real handlers with an invariant on the pair, checked after every step.

### 5. Provider status or event mapping incomplete, or not monotone

```
BAD:   switch (event.type) { case 'payment_intent.succeeded': … }   // subscribed to 6 types; 'payment_intent.payment_failed' falls through → stuck 'pending'
       order.status = mapCarrierStatus(update.status)                  // a late 'in_transit' overwrites 'delivered'
GOOD:  every subscribed type handled or in an explicit ignore list; the mapped state applied only when the graph allows the edge
```
**Read the code:** Which event types is the endpoint subscribed to (5d, the provider dashboard export, the IaC)? Does the handler (5a) name each, or an ignore list (5c, § 22)? For a provider-status map (5b), is the mapped state checked against the graph before it is written, or does a late or duplicate event regress a settled state? Does the handler re-fetch the provider object before deciding (§ 22)? **Finding when** a subscribed event type leaves an entity in a non-terminal state with no handler, or a replay of real events in another order regresses a state. **Proof:** V476 — replay a recorded event sequence duplicated and shuffled (`stripe events resend`, the carrier's sandbox, or a captured fixture) through the real handler: the final state is the same and every intermediate edge is in the graph.

### 6. Transitions leave no history

**Read the code:** For each critical machine (order, payment, subscription, invoice, role, consent), does every write in `writers.txt` insert a history or audit row (actor, from, to, at) in the same transaction — directly, through a repository, an ORM subscriber or an audit interceptor? A low-stakes toggle needs none (§ 31). **Finding when** a transition on a critical entity can happen with no record of who moved it from which state. **Proof:** V482 — fire each transition through its real entry point: exactly one history row per transition, written in the same transaction (a rolled-back transition leaves none).

## Output

```
lifecycle-scan — lanes: typescript (xstate 5.33.3 — pnpm-lock.yaml); python (django-fsm-2 4.x — uv.lock); ruby, php, jvm, go absent
Graph: $OUT/graph/ — status-graph exit 0 · 14 machines shown · 3 subset lists · 211 writes (188 attributed, 17 ambiguous, 6 implied)

Findings: 1 · Unconfirmed: 2 · Hardening: 1

1. src/payments/payment.webhook.ts:41                                    [report-with-fix]  high
   §5 LC-5 — subscribed to payment_intent.payment_failed (infra/stripe.tf:22); the switch has no case and no ignore list;
   V476 failed: replay [created, payment_failed] → payment stays 'pending'. Fix: handle it through the graph's 'failed' edge.
2. src/orders/order-status-machine.ts:14                                 [report-flagged]   high
   §2 LC-2 — 'in_review' has no row in ORDER_TRANSITIONS and no attributed write leaves it. Unproven link: whether
   the setter treats a missing row as locked. Settling: V474 from 'in_review' through updateStatus().
3. src/orders/checkout.service.ts:88                                     [report-flagged]   high
   §4 LC-4 — writes payment 'captured' and order 'paid' in two transactions. Settling: V475 with a crash between them.

Routed: 4 → backend state-transition-scan §2 (status writes outside the machine) · 1 → security logic-race-scan §3 (late event)
Verification: 19 candidates → 1 finding · 2 unconfirmed · 1 hardening · 15 refuted (self-verified; precedents §21, §29, §33)

Class coverage:
  §1 unreachable        checked (6 machines → 0; 3 states reached only by migration writes, legacy list read)
  §2 traps / terminal   checked (14 machines → 1 unconfirmed; 2 undetermined, writers read)
  §3 declared graph     checked (ai/business-flows.md: 2 declared-not-built → 0, both in the reversal table)
  §4 cross-aggregate    checked (4a 5 files, 4b 3 transactional → 1 unconfirmed)
  §5 provider events    checked (5a 9, 5d 6 subscribed → 1 finding)
  §6 history            checked (6a 2 tables; 6b 7 writers → 0: an audit interceptor writes the row)
```

`[report-with-fix]`: the oracle failed on the real path at the installed version and the fix is local to the transition table, the FSM config, the handler or the setter. `[report-flagged]`: one link is unproven (the setter's handling of a missing row, the crash window, the subscribed types); the row names it and the settling oracle. The coverage block lists **all six** §s on every run: `checked (k → m)`, `N/A (<reason>)`, `blocked (status-graph exit 2 | <grep>: rg exit 2)`, `→ <owner> (k)` or `Live, unreviewed (k)`.

## False positives / precedents

The verifier reads [`precedents/business.md`](../../../../snippets/precedents/business.md) and [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 4. The ones this skill meets most:
- § 21 a write inside the FSM library's own transition, an audited admin repair or a migration is not a bypass; § 22 an explicit ignore list of provider events is a mapping, and re-fetching the provider object is the recommended shape.
- § 27 "refund without return" as a written policy is not §4; § 29 a declared reversal table is a way back, not a re-open (a real NestJS + React monorepo keeps one beside its forward table); § 30 legacy states written only by migrations and locked are not §1.
- § 31 low-stakes toggles need no history; § 32 an implied machine is a gap, not yet a defect; § 33 an ambiguous write is evidence for no machine until read.

## When to run

- On any diff that adds or changes a status, state or phase column, an enum or union of states, a transition table or FSM config, a status write, a webhook handler or a provider-status map — `/audit-business`'s lifecycle signal.
- On every whole-repo `/audit-business`, reporting all six §s; before adding a provider, a new status, or an FSM library.

## Halt conditions

- **Do not report a high row as confirmed until a separate verifier has refuted it.** That verifier is not the run that found it, gets the machine's block from `graph.txt`, the `file:line` and the seed — never this run's reasoning — and passes the row through [`refute-before-report.md`](../../../../snippets/refute-before-report.md) §1–§8 with [`precedents/business.md`](../../../../snippets/precedents/business.md). Under `/audit-business` that is `@workflow-integrity` in refute mode, then `@verifier` mode `refute` on every BLOCKER and HIGH; standalone, apply the protocol as a second pass and tag the rows `self-verified`. List the rest as Unconfirmed, Hardening or Refuted; never drop them.
- **Halt before any § when the graph is unread.** `status-graph.py` exit 2, or NOT-RUN, makes §1–§3 `blocked` (or `Live, unreviewed` on the hand lane); never print `checked` over a graph that was not built.
- **Never write into the audited repo:** the graph lives under `$OUT`; the script refuses an `--out` inside a root.
- **No `[report-with-fix]` without the V-oracle failing on the real path** (or a two-ended static fact). A graph row alone is a candidate; an ambiguous or implied machine is never a finding by itself.
- **No proposed fix may hide the class:** never widen a transition table to make a trap disappear, never add a catch-all `default:` that marks unknown provider events handled, never delete a declared state a reader still uses.
- **Business decisions are not code fixes:** whether a terminal state may be re-opened, which provider events matter, and which entity needs history are the owner's call — the row names the decision and stops.
- **Do not grade a class another pack owns** (§ Boundaries). **Do not print "the lifecycle looks sound"** without the coverage block.

## Related

- `/audit-business` dispatches this skill and folds its coverage block into its class ledger; `@workflow-integrity` judges these rows and fills its transition matrix from `edges.tsv`. `ledger-scan` §7 (conservation on reversal edges) and `check-business-coverage` (the inverse a user can reach) are the neighbours in this pack.
- backend `state-transition-scan` §1–§2 reads `$OUT/graph/edges.tsv` as its graph, when the backend pack is installed; database `transaction-scan` §8, security `logic-race-scan` §3, distributed-systems `messaging-scan` §2, when those packs are installed.

## Sources

From the business research (2026-10-19): FSM library behaviour — AASM `no_direct_assignment`, django-fsm-2 `protected=True`, viewflow.fsm, statesman's append-only transitions, spatie model-states v2, looplab/fsm, stateless, XState 5.33.3, Spring Statemachine (repository archived 2026-07-05); provider facts — Stripe webhooks are unordered and duplicated, `stripe events resend`; model-based testing — fast-check 4.10.2 `fc.commands` / `scheduledModelRun`, Hypothesis 6.170.1 `RuleBasedStateMachine`. The real-repo and fixture counts are from read-only runs of the block above and of `status-graph.py`. Paraphrased; no text reproduced beyond identifiers.
