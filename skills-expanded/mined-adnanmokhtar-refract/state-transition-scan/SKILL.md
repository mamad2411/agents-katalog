---
name: state-transition-scan
description: "State machines: an illegal event answered as success, a terminal state re-opened — FSM-library semantics, read-only."
kind: skill
pack: backend
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: state-transition-scan

## Premise

A state-machine library looks like the guard a workflow needs: the states are declared, the transitions are declared, an illegal event cannot happen. Several libraries are configured, or default, to make an illegal event **quiet**. Python `transitions` with `ignore_invalid_triggers=True` answers `refund()` from `pending` with `False` and no exception, and a failed `conditions=` guard does the same; python-statemachine with `allow_event_without_transition=True` returns `None`; an XState v5 actor ignores an event its current state does not handle, and every event after a final state; AASM with `whiny_transitions: false` returns `false`; looplab/fsm returns an error the caller drops. None of that is a bug while the caller checks the answer. It becomes one when the handler **carries on** — answers "refunded", calls the PSP, sends the email — after an event the graph forbids. The second shape re-opens what the graph says is final: a wildcard source (`source='*'`), an AASM event with no `from:`, a job or webhook path writing the status around the machine. This skill finds both in the library configuration and the code that drives it, and proves each with the **(state × event) matrix and a side-effect counter** through every entry point. Read-only: it never edits code.

Backend owns **FSM-library transition semantics** (eval § 4.1): what the library does with an illegal event and whether a terminal state can be left. It is the detector of the `workflow-transitions` row of `ownership.json` (`state-transition-scan §1–§2`, fixer `/backend-fix`); the **owner and judge of the state graph stay `business/agents/workflow-integrity`**, which supplies the graph this skill reads. It owns `/backend-audit`'s transition rows (`state-transition-scan §1–§2`); `@api-reviewer` (this pack) judges them in refute mode.

**Every finding cites the machine configuration or the call `<file:line>` + the library and version + the graph row it breaks (the illegal pair or the terminal state, with the graph's source) + the entry point that sends the event (HTTP, job, webhook, admin) + what happens after it (the status code and the side effects counted) + the oracle that showed it, or the pair that would settle it + the fix in the project's own machine.** A grep hit is a candidate. "Transitions look guarded" is never printed; the output is the class-coverage block (§ Output). Verification follows [`refute-before-report.md`](../../../../snippets/refute-before-report.md) with [`precedents/backend.md`](../../../../snippets/precedents/backend.md). The oracles are [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Backend: V350 (state × event, property S4) and V357 (the version pair rule).

## The rule

A candidate is a finding when all four hold — `precedents/backend.md` § Reading the seven gates for backend, applied to transitions.

1. **Part A holds: the machine drives a server-side aggregate.** It is constructed in a request handler, a use case, a job, a consumer or an admin action that a deployed process runs, and its state is persisted. A front-end statechart that ignores unknown events is the contract, not a defect (B-R5); `ROOTS` are server and worker code, and `.tsx`/`.jsx`/`.vue`/`.svelte` files are excluded.
2. **Part B holds at the installed version.** The library version comes from the lockfile (F1); the swallow behaviour is version-specific (V357). Without a lockfile the version is `UNREAD` and the row is Unconfirmed.
3. **Nothing already controls it**, across files: the handler checks the trigger's return value, `can()`, `may_<event>?` or the post-event state before it responds or acts (B-R5); a status predicate on the write (`UPDATE … WHERE status = 'paid'` with the row count checked); a re-open path the graph declares, behind an audited admin action.
4. **The oracle fired, or the fact is two-ended.** V350 through the real entry point (tier U) shows an illegal pair answered 2xx or followed by a side effect, or a terminal state left; or the static fact cites both ends (tier S: the swallow setting or wildcard source, and the handler line that acts after the event without checking it). Without one, the row is `[report-flagged]` / Unconfirmed with the pair written out.

## Boundaries

One class, one owner. A neighbour that sees the same `file:line` lists it as corroboration (`precedents/backend.md` § Owned elsewhere). Each routed row prints `→ <pack> <skill> §n (k)` and is never graded here; without the owner's pack the hits are listed tagged `<class> (owner pack <x> not installed)`, never at the owner's severity.
- **The graph itself** — which states exist, which are terminal, unreachable states, traps — → business `lifecycle-scan` (`lifecycle-graph`, judged by `@workflow-integrity`), when the business pack is installed; this skill reads the graph that skill's `status-graph.py` wrote (`$OUT/graph/edges.tsv` and `states.tsv` of the same run, or a same-day `/audit-business` run folder) and never re-derives it, else `ai/business-flows.md`, else the machine's own final states (an inferred terminal state makes the row Unconfirmed).
- **A transition decided in memory and persisted with no status predicate or version** (BS-03: `can()` then a whole-entity `save()`; AASM `requires_lock` off) and **a stale copy written back across an await** (BS-05, non-value field) → database `transaction-scan` §8 (V5), when the database pack is installed. **Callbacks with side effects before the commit** (BS-04: AASM `after_commit` fires only on bang events, Rails `after_save` mailers) → its §1 (V8).
- **Step skipping, a status taken from the request, a late provider event re-opening a settled record, and check-then-act on a value field** (BS-05) → security `logic-race-scan` §3 and §5, when the security pack is installed. A status write that bypasses no library machine is security's and database's, not this skill's.
- **A hand-written `switch` on a status with a silent `default`, or "many writers, no transition table"** → code-quality `correctness-smell-scan` §5.
- **Repeated keys on non-HTTP paths** (BS-06) → security `logic-race-scan` §2; **aggregation after rounding** (BS-07) → code-quality `correctness-smell-scan` §4.
- Same pack: **a job or webhook that fires the event** is read through `job-lifecycle-scan`'s inventory; **the status code an illegal transition answers** (409 vs 422 vs 500) is `edge-error-scan` §2's mapping once the library raises.

## Adapt to the codebase — the lanes

Read the library **with its version** (F1) and every machine definition (grep 0) first. `[V]` rows were run or read in the backend research labs (§ Sources); `[K]` are vendor docs; a library below with no row has an unread default — read its installed source before asserting.

| Library | Illegal event, by default | The swallow setting (§1) | Re-open shape (§2) | Control |
|---|---|---|---|---|
| **transitions** 0.9.3 (Python) | raises `MachineError` [V] | `ignore_invalid_triggers=True` → the trigger returns `False`, state unchanged; a failed `conditions=` guard also returns `False` with no exception [V] | `source='*'` re-opens a terminal state [V] | `if not order.refund(): raise Conflict` |
| **python-statemachine** 3.2.2 | raises `TransitionNotAllowed` [V] | `allow_event_without_transition=True` → `send()` returns `None` [V] | `final=True` states; a wildcard source if the version offers one — read it | the default, or the result checked |
| **XState** 5.33.2 | ignored without error; `can()` is `false`; events after a final state are ignored (`status: 'done'`) [V] | the default itself, on a server actor | a root-level `on` handler — read whether final states accept it | `snapshot.can(event)` before `send`, or the post-send state asserted |
| **AASM** (Ruby) | raises `AASM::InvalidTransition` [K] | `whiny_transitions: false` → the event returns `false` [V README] | an event whose `transitions` have no `from:` accept any state [K] | `may_<event>?`, the bang event's exception |
| **looplab/fsm** (Go) | `Event` returns `InvalidEventError`, `NoTransitionError` or `CanceledError` [V source] | the error dropped (a bare call, `_ =`) | a `Src` list that names a terminal state | `if err := f.Event(ctx, e); err != nil { … }` |
| **Spring Statemachine** | `sendEvent` reports `DENIED` in its result [K?]; the repository was **archived on 2026-07-05** (its README: no longer maintained; patched 3.2.x / 4.0.x builds are sold commercially) — last core release 2025-06-29 [V] (business research § 0.9, read 2026-10-19) | the result never read | — | read the `StateMachineEventResult` |
| **.NET Stateless** | throws `InvalidOperationException` [K] | `OnUnhandledTrigger(…)` that does not throw | — | — |

django-fsm, Symfony Workflow, spatie/laravel-model-states and qmuntal/stateless are recognised by F1 and grep 0; their defaults were not read by the research — a verdict states the installed version and the behaviour read from its source. **Opt-in direct-write protection decides 2c:** AASM `no_direct_assignment: true`, django-fsm-2 `FSMField(protected=True)` and viewflow's `fsm` state descriptor make a plain status assignment outside the machine raise, so a 2c write on a model that sets one is not a §2 row (it fails loudly; read the option on that model before rating). Without the option, the write bypasses the machine's guard (business research § 0.9, read 2026-10-19; not run in the lab).

## Tool lane and ledger

Each tool prints `ran` / `blocked (<why>)` / `NOT-RUN (<why>)` in the output header.

| Tool | Command | Covers | Limits |
|---|---|---|---|
| **The (state × event) matrix with side-effect counters** (V350) | for every pair from the graph, put the aggregate in the state (fixture rows), send the event through each entry point that can fire it (HTTP via the real bootstrap, the registered job, the webhook handler, the admin action), count effects (rows, enqueues, provider-stub calls, emails) — not just the state | §1, §2 | needs the graph (business pack or `ai/business-flows.md`) and a scratch database in a container; `NOT-RUN` without them, never PASS |
| **Property S4** (V350) | `fc.commands` / Hypothesis `RuleBasedStateMachine` / jqwik `ActionChain` against a transition-table model: `(ok, state)` matches the model after every step, terminal states accept nothing, effect counts match | §1, §2 | written per fix and shown to fail on the pre-fix code first |

## Pre-flight greps

Run as **one** script from the repo root (bash 3.2-safe). Grep **N** feeds detector **§N**; F1 and grep 0 are the gates every § reads first. Every `rg` names its path — `.` or `"${ROOTS[@]}"`; include globs come **first**, exclusions last, and exclusions start with `**/`. Any `rg` exit 2 is a failed grep, never zero hits. A block question ("this file sends an event and never asks `can()`") is answered at the **file** with `--files-without-match`, never by `-A<n> | rg -v`.

```bash
ROOTS=(.)   # server and worker code (never a UI app: front-end statecharts that ignore events are the contract, B-R5); in a monorepo: ROOTS=(apps/api apps/worker)
SCAN="${SCAN:-$(mktemp -d "${TMPDIR:-/tmp}/st.XXXXXX")}"; mkdir -p "$SCAN"
CODE=(-g '*.{ts,mts,cts,js,mjs,cjs,py,java,kt,cs,go,php,rb}')
X=(-g '!**/node_modules/**' -g '!**/vendor/**' -g '!**/{dist,build,out,target,coverage,.next,.venv,venv,generated,__generated__}/**'
   -g '!**/{test,tests,__tests__,spec,specs,e2e,fixtures,__fixtures__,mocks,__mocks__,testdata}/**'
   -g '!**/*.{spec,test,e2e-spec,stories}.*' -g '!**/test_*.py' -g '!**/*_test.go' -g '!**/*.d.ts' -g '!**/*.min.*'
   -g '!**/{migrations,migration,db/migrate,seeders,seeds}/**' -g '!**/{locales,locale,i18n,translations}/**' -g '!**/{docs,ai,.claude}/**'
   -g '!**/*.{tsx,jsx,vue,svelte}')
NC=(rg -v --pcre2 '^[^:]+:\d+:\s*(?://|/\*|\*(?:\s|/|$)|#(?!\[))')   # drops comment-only lines
# F1 state-machine libraries with versions — ranges from manifests; exact versions from the lockfile (gate 3; V357). None → §1 and §2 are N/A; the routed rows still print
rg -n --no-heading --pcre2 '"(xstate|@xstate/\w+|javascript-state-machine|typescript-fsm|robot3|fsm-as-promised|@stately/\w+)"\s*:\s*"[^"]+"' -g '**/package.json' -g '!**/node_modules/**' .
rg -n --no-heading -i --pcre2 '^\s*["\x27]?(transitions|python-statemachine|django-fsm(?:-2)?|viewflow)\b\s*[=<>~!^]|gem\s+["\x27](?:aasm|state_machines(?:-activerecord)?|statesman|workflow)["\x27]|"(?:symfony/workflow|spatie/laravel-model-states|winzou/state-machine)"\s*:|github\.com/(?:looplab/fsm|qmuntal/stateless)\s+v|spring-statemachine-\w+|<PackageReference Include="Stateless"' -g '**/{pyproject.toml,requirements*.txt,Pipfile,Gemfile,composer.json,go.mod,pom.xml,build.gradle*,*.csproj}' -g '!**/node_modules/**' .
# 0 THE MACHINES — every library machine definition (the graph's source in code) and the declared graph (business pack: ai/business-flows.md, @workflow-integrity)
M='\bcreateMachine\s*\(|\bsetup\s*\(\s*\{[^\n]*\bactors\b|\bnew\s+StateMachine\s*\(|\bMachine\s*\(\s*(?:model\s*=|self\b|\w+\s*,\s*states)|\bclass\s+\w+\s*\(\s*(?:\w+\.)?StateMachine\s*\)|\binclude\s+AASM\b|\baasm\b[^\n]*\bdo\b|\bstate_machine\s*(?::\w+\s*,\s*)?(?:initial:|do\b)|\bfsm\.NewFSM\s*\(|\bstateless\.NewStateMachine\s*\(|@EnableStateMachine(?:Factory)?\b|\bStateMachineBuilder\b|\bFSMField\s*\(|@transition\s*\(|\bStateMachine<\w+\s*,\s*\w+>|\bnew\s+StateMachine<'
rg -l --null --pcre2 "$M" "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" > "$SCAN/machines"
echo "0 machine files: $(tr -cd '\0' < "$SCAN/machines" | wc -c | tr -d ' ') · declared graph: $(ls ai/business-flows.md 2>/dev/null || echo 'none (terminal states come from the machine definitions)')"
xargs -0 -r rg -n --no-heading --pcre2 "$M" < "$SCAN/machines" | "${NC[@]}" | head -40
xargs -0 -r rg -n --no-heading --pcre2 '\btype\s*:\s*["\x27]final["\x27]|\bfinal\s*=\s*True\b|\bState\s*\([^)\n]*\bfinal\s*=\s*True|\.end\s*\(\s*\w+|\bterminal\b' < "$SCAN/machines" | "${NC[@]}" | sed 's/^/0 terminal: /' | head -20   # declared final states; otherwise the graph decides
# 1 an illegal event answered as success: swallow settings (1a); XState send in a server file that never asks can() (1b); a Go FSM error dropped (1c);
#   Spring Statemachine sendEvent result ignored (1d); python guarded triggers and unchecked trigger calls in machine files (1e — read whether the result is used)
rg -n --no-heading --pcre2 '\bignore_invalid_triggers\s*=\s*True\b|["\x27]ignore_invalid_triggers["\x27]\s*:\s*True\b|\ballow_event_without_transition\s*=\s*True\b|\bwhiny_transitions:\s*false\b|\bwhiny_persistence:\s*false\b|\bOnUnhandledTrigger(?:Async)?\s*\(' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}" | sed 's/^/1a /'
rg -l --null --pcre2 'from\s+["\x27]xstate["\x27]|require\(\s*["\x27]xstate["\x27]\s*\)' -g '*.{ts,mts,cts,js,mjs,cjs}' "${X[@]}" "${ROOTS[@]}" | xargs -0 -r rg --files-without-match --null --pcre2 '\.can\s*\(' | xargs -0 -r rg -H -n --no-heading --pcre2 '\.send\s*\(\s*(?:\{\s*type\s*:|["\x27]\w+["\x27])' | "${NC[@]}" | sed 's/^/1b /'
rg -l --null --pcre2 'github\.com/(?:looplab/fsm|qmuntal/stateless)' -g '*.go' "${X[@]}" "${ROOTS[@]}" | xargs -0 -r rg -H -n --no-heading --pcre2 '^\s*(?:_\s*=\s*)?[\w.]+\.(?:Event\s*\(\s*\w+\s*,|Fire(?:Ctx)?\s*\()[^\n]*\)\s*$' | "${NC[@]}" | sed 's/^/1c /'
rg -n --no-heading --pcre2 '^\s*[\w.]*[sS]tate[mM]achine\w*\.sendEvent(?:s|Collect)?\s*\([^\n]*\)\s*(?:\.subscribe\s*\(\s*\))?\s*;\s*$' -g '*.{java,kt}' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}" | sed 's/^/1d /'
xargs -0 -r rg -n --no-heading --pcre2 '["\x27]?conditions["\x27]?\s*[=:]|\bunless\s*=|^\s*(?:self\.)?\w+\.(?!save\b|update\b|delete\b|get\b|set\b|add\w*\b|send\b)\w+\s*\(\s*\)\s*$' -g '*.py' < "$SCAN/machines" | "${NC[@]}" | sed 's/^/1e /' | head -40
# 2 a terminal state re-opened: wildcard sources (2a); AASM transitions with no from: (2b); direct status writes on job, webhook, consumer and admin paths in
#   files that touch a library-driven aggregate — a write that bypasses the machine's guard (2c, read against the graph's terminal states)
#   2c's assignment starts a statement (line start, after ; { ) => else then do): `x.state = 'run'` inside SQL text in a template string is a predicate, not a write
rg -n --no-heading --pcre2 '["\x27]source["\x27]\s*:\s*["\x27]\*["\x27]|\bsource\s*=\s*["\x27]\*["\x27]|\badd_transition\s*\(\s*(?:trigger\s*=\s*)?["\x27]\w+["\x27]\s*,\s*(?:source\s*=\s*)?["\x27]\*["\x27]|\bfrom_\.any\s*\(|\bsource\s*=\s*\[?\s*["\x27]\*["\x27]' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}" | sed 's/^/2a /'
rg -n --no-heading --pcre2 '^\s*transitions\s+(?:(?!\bfrom:)[^\n#])*\bto:' -g '*.rb' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}" | sed 's/^/2b /'
ST='(?:^\s*|[;{)]\s*|=>\s*|\b(?:else|then|do)\s+)(?:this\.|self\.|@)?[\w$]+(?:[!?]?\.[\w$]+|\[[^\]\n]+\])*[!?]?\.(?:status|state)\s*=(?!=)|\bset_?[sS]tatus\s*\(|\bupdate!?\s*\(\s*(?:status|state):|\.update\w*\s*\([^)]*["\x27]?(?:status|state)["\x27]?\s*[:=]|\bUPDATE\s+\w+\s+SET\s+(?:status|state)\b'
rg --files "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | rg --pcre2 '(?i)(?:jobs?|workers?|processors?|consumers?|webhooks?|listeners?|subscribers?|handlers?|tasks?|cron|admin)' | tr '\n' '\0' > "$SCAN/paths"
echo "2c status writes on non-HTTP and admin paths: $(xargs -0 -r rg -c --no-heading --pcre2 "$ST" < "$SCAN/paths" | awk -F: '{s+=$NF} END {print s+0}') in $(xargs -0 -r rg -l --pcre2 "$ST" < "$SCAN/paths" | wc -l | tr -d ' ') files (rows only where the aggregate has a machine in grep 0)"
xargs -0 -r rg -n --no-heading --pcre2 "$ST" < "$SCAN/paths" | "${NC[@]}" | head -30 | sed 's/^/2c /'
# R routed rows — counted here, graded by their owners (§ Boundaries)
echo "R → database transaction-scan §8: $(rg -l --null --pcre2 '\.can\s*\(|\bmay_\w+\?|\bcan_\w+\s*\(|\bcan_proceed\s*\(|\.(?:may|is)\w*\s*\(\s*["\x27]\w+["\x27]\s*\)' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | xargs -0 -r rg -l --pcre2 '\.save!?\b|\.save\s*\(\s*\)|\.flush\s*\(|\brepository\.save\s*\(|\.persist(?:AndFlush)?\s*\(' | wc -l | tr -d ' ') files decide a transition then save the whole entity (lost update without a status predicate or version)"
echo "R → security logic-race-scan §3: $(rg -c --no-heading --pcre2 '\.(?:status|state)\s*=\s*(?:req|request|ctx\.request|body|dto|params|input)\.(?:body\.)?(?:status|state)\b|\b(?:update|create|save|patch|set)\w*\s*\([^)\n]*\b(?:status|state)\s*:\s*(?:req|request|ctx\.request|body|dto|params|input)\.(?:body\.)?(?:status|state)\b|\brequest\.data\[["\x27](?:status|state)["\x27]\]|\bparams\[:(?:status|state)\]|\.permit\([^)]*:(?:status|state)\b' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | awk -F: '{s+=$NF} END {print s+0}') status writes taken from input (step skipping; a late provider event re-opening a settled row) · §5: value-field check-then-act"
echo "R → code-quality correctness-smell-scan §5: $(rg -c --no-heading --pcre2 '\bswitch\s*\(\s*[\w.]*\b(?:status|state)\s*\)|\bmatch\s+[\w.]*\b(?:status|state)\s*:|\bwhen\s+[\w.]*\b(?:status|state)\s*$|\bcase\s+[\w.@]*\b(?:status|state)\s*$' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | awk -F: '{s+=$NF} END {print s+0}') hand-written switches on a status (non-exhaustive, silent default)"
```

Two blind spots are structural. **The result checked one call away** — a helper that wraps `send()` and asserts the post-state, a base aggregate whose `apply(event)` throws on `False` — is not in the file: read the helper before keeping a 1b or 1e row. **A machine built from data** (states and transitions loaded from a table or a JSON file) is not a definition grep 0 can parse: read the loader and the data, and quote both.

### Measured (2026-10-14)

- **Real repo, read-only, full tree** (the NestJS 11 monorepo of `job-lifecycle-scan`; `ROOTS=(apps/api/src)`): 0.5 s, 13 lines, 0 `rg` errors, 0 files written into the tree. F1: **no state-machine library** in any manifest; grep 0: **0 machine files** — the domain's transitions are hand-written methods on aggregates — and the declared-graph file (`ai/business-flows.md`) is present for the business pack. §1 and §2 are therefore `N/A (no FSM library)`. 2c prints 6 status writes in 4 files on job, consumer and admin paths (two consumers' ledger rows, a tasks port and its use case); with no library machine none are this skill's rows. The first full-tree run printed 8 lines in 5 files: the other 2 were SQL text inside a template string in the outbox's claim query (`… ${claim}.state = 'run' or …`, a predicate), so 2c's assignment now has to start a statement (line start, or after `;`, `{`, `)`, `=>`, `else`, `then`, `do`). Routed: database §8 0, security §3 **4** (ports that assign `row.status = input.status`), code-quality §5 2. An earlier run on `ROOTS=(apps/api)` over an older partial copy printed 6 writes in 4 files.
- **Fixtures** (`benchmarks/fixtures/*`, 18 roots): 0 `rg` errors; **no root uses a state-machine library**, so §1/§2 print `N/A` everywhere; 2c lists 3 writes in 2 files (`brittle-suite`) and 3 in 1 file (`node-api`), all hand-written → routed. The `backend-defects` fixture (a later build item) seeds `transitions.Machine(…, ignore_invalid_triggers=True)` followed by a refund call.
- **Research lab B** (the scripts that measured the library defaults): `py/sm.py` — 1a 3 (the setting, plus two `print` lines that echo it: read), 1e 1 (a `conditions=` guard), 2a 2 (`source='*'`); `node/x.mjs` — its XState machine in grep 0 and its final state in the terminal line, 1b quiet (the script asks `can()`). A first 1c draft matched every `.Event(x)` in a Go module cache; 1c now reads only files that import looplab/fsm or qmuntal/stateless.
- **Paired samples** (scratch, Python, Ruby, TypeScript, Go): every POS line hit (1a ×3, 1b, 1c, 1e, 2a ×2, 2b); every NEG line stayed quiet — the default `Machine(…)`, an XState handler that asks `can()` first, a Go call whose error is checked, an AASM transition with `from:`.

## The 3,000-hit path

ST is machine-first: a repo has a handful of machines, and each machine's configuration decides most rows. Read **every** grep 0 definition whole and print its graph (states, terminal states, transitions, guards) before any per-site grep. Then group: §1 by machine (one swallow setting is one finding with the N entry points that drive it as its sites, P5); §2 by terminal state (one row per state that can be left, with every path that leaves it); 2c by aggregate — only aggregates that have a machine are read, the rest print their routed count. A partial review prints `Live, unreviewed (k groups / n hits)`, never `checked`.

## Scans for

| § | Class (research id) | Default severity | Oracle |
|---|---|---|---|
| 1 | an illegal event answered as success (BS-01) | high; **blocker** when the handler continues to a money effect (the `/backend-audit` floor) | V350 |
| 2 | a terminal state re-opened (BS-02) | high | V350 |

### 1. An illegal event answered as success

```
BAD:   Machine(model=order, …, ignore_invalid_triggers=True); order.refund(); psp.refund(order.id); return {"refunded": True}
       actor.send({ type: 'REFUND' }); await psp.refund(id); res.json({ refunded: true })     // XState: ignored in `pending`, no error
       aasm whiny_transitions: false  →  order.refund; Mailer.refunded(order).deliver_later   ·   fsm.Event(ctx, "refund")  (error dropped)
GOOD:  if not order.refund(): raise Conflict("illegal transition")      ·  if (!actor.getSnapshot().can({ type: 'REFUND' })) return res.status(409).end()
       the library default that raises, mapped to 409/422 by the edge (edge-error-scan §2)
```
**Read the code:** for each 1a setting, which entry points send events to this machine (HTTP, job, webhook, admin — the job and webhook inventory is `job-lifecycle-scan`'s grep 0)? After the event, does the code read the answer — the return value, `can()`, `may_<event>?`, the post-event state — **before** it responds or acts? Does a guard (`conditions=`, `unless=`) return `False` where the caller expects an exception (1e)? Which pairs does the graph forbid, and what effect follows each one? **Finding when** an illegal pair answers 2xx or is followed by any side effect. **Proof:** V350 — every (state × event) pair from the graph through every entry point: an illegal pair answers 409/422 (or a typed error) **and** the effect counters stay at zero.

### 2. A terminal state re-opened

```
BAD:   add_transition('reopen', '*', 'open')  ·  {'trigger': 'reset', 'source': '*', 'dest': 'pending'}
       event :reopen do transitions to: :pending end                 # AASM: no from: → any state, refunded included
       a webhook handler setting order.status = 'paid' on a row the machine already moved to 'refunded'
GOOD:  explicit sources that exclude terminal states · an audited admin re-open the graph declares · the write goes through the machine
```
**Read the code:** which states does the graph mark terminal (the business pack's `lifecycle-scan` graph — `status-graph.py`'s `states.tsv` — then `ai/business-flows.md`, or the machine's own `final` markers — inferred ones make the row Unconfirmed)? Does a wildcard source or a `from:`-less transition include them? For a 2c write on a job, webhook or admin path: is the aggregate driven by a machine in grep 0 — then the write bypasses the machine's guard and is this §; with no machine it is security §3's (§ Boundaries). **Finding when** any entry point moves an aggregate out of a terminal state outside a re-open path the graph declares. **Proof:** V350 — (terminal state × every event) through HTTP, job and webhook: no state change and no effect.

## Proof

V350 of `proof-oracles.md` § Backend through the project's real entry points — the app the bootstrap builds for HTTP, the registered processor for jobs, the webhook handler with a signed payload, the admin action — against a scratch database on the production engine: every (state × event) pair from the graph, effects **counted** (rows written, jobs enqueued, provider-stub calls, emails), not just the final state. Property S4 is the generalisation a fix keeps: written against a transition-table model and shown to fail on the pre-fix code first. The control: a UI statechart and a handler that checks `can()` stay quiet (B-R5). A matrix that did not run is `NOT-RUN`, never PASS; a unit test of the machine alone proves nothing about what the handler does next.

## Output

```
state-transition-scan — lanes: none (no FSM library in any manifest)
Machines: 0 · graph: ai/business-flows.md present (the business pack's; no library machine to read it against)
Tools: (state × event) matrix N/A (no library machine) · property S4 N/A

Findings: 0 · Unconfirmed: 0

Class coverage:
  §1 illegal event → success   N/A (no FSM library; transitions are hand-written aggregate methods)
  §2 terminal state re-opened  N/A (no FSM library) · 2c 6 status writes in 4 files on job, consumer and admin paths → routed
  routed                       → database transaction-scan §8 (0) · → security logic-race-scan §3 (4) · → code-quality correctness-smell-scan §5 (2)
```

On a repo with a machine (the paired-sample run), a row reads:

```
1. py/app/fsm.py:3 (Machine(…, ignore_invalid_triggers=True)) · py/app/fsm.py:9–10                    [report-flagged]  high
   §1 — transitions (version UNREAD): order.refund() from 'pending' returns False; the next line calls psp.refund() without reading it.
   Pair: pending × refund through the caller's entry point → expect a refusal and 0 PSP calls. Fix: drop ignore_invalid_triggers,
   or raise on False. Settling: V350.
```

`[report-with-fix]`: V350 failed through the real entry point on the installed library version and the fix is local to the project's machine or the handler that drives it. `[report-flagged]`: one link is unproven (no matrix run, the version `UNREAD`, the graph inferred); the row names the pair that would settle it. The coverage block lists **both** §s and the routed rows on every run: `checked (k → m)`, `N/A (<reason>)`, `blocked (<grep or tool>)`, `→ <owner> (k)` or `Live, unreviewed (k groups / n hits)`. A missing line is printed by `/backend-audit` as `not run`.

## False positives / precedents

The verifier reads [`precedents/backend.md`](../../../../snippets/precedents/backend.md) and [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 4. The ones this skill meets most:
- **B-R5** state-machine "ignore" settings in a UI statechart, or in server code that checks `can()` or the return value before it responds — the row flips back only when the handler **continues** to a side effect.
- **B-G3** a lifecycle field written by a generic update instead of an action endpoint (the security and API reading of the same write).
- **P1** the illegal pair comes from a graph source (the business pack's graph, `ai/business-flows.md`, the machine), never from intuition; **P3** "an attacker can skip a step" goes to security; **P5** one swallow setting is one finding with its entry points as sites.

Shapes this skill must not report: an XState machine in a front-end app; a test that drives the machine to prove an illegal event is refused; a declared, audited admin re-open; a `False` return that the next line turns into a 409.

## When to run

- On any diff that touches a machine definition or its options, a handler or job that sends events to one, a status write on a job, webhook or admin path, or the library version — `/backend-audit`'s "a state-machine file" signal.
- On every whole-repo `/backend-audit`, reporting both §s (N/A with a reason when there is no library); after `@workflow-integrity` redraws a graph; before upgrading the library across a major (V357).

## Halt conditions

- **Do not report a high row as confirmed until a separate verifier has refuted it.** That verifier is not the run that found it, gets part A (the machine, where it is constructed and the entry points), part B (the library and version), the pair and the graph source — never this run's reasoning — and passes the row through [`refute-before-report.md`](../../../../snippets/refute-before-report.md) with `precedents/backend.md`. Under `/backend-audit` that is `@api-reviewer` in refute mode, then `@verifier` mode `refute` on every BLOCKER and HIGH; standalone, apply the protocol as a second pass and tag the rows `self-verified`. List the rest as Unconfirmed, Hardening or Refuted; never drop them.
- **Halt before any § when grep 0 is unread.** A verdict on a `send()` without the machine it drives and the graph it breaks is invalid.
- **Halt on any finding missing its anchors:** the configuration or call `file:line`, the library and version, the illegal pair or terminal state with its graph source, the entry point, the effect that follows, the fix in the project's own machine.
- **No `[report-with-fix]` without V350 through the real entry points** with effects counted (or a two-ended static fact). A unit test of the machine alone is not one.
- **No proposed fix may hide the class:** never catch the library's exception and answer 200, never add the terminal state as a source to make a test pass, never delete a guard because it returns `False`.
- **Do not grade a class another pack owns** (§ Boundaries); route it with a count. **Do not print "transitions look guarded"** without the coverage block; a § whose grep did not run is `blocked`, never `checked`.

## Related

- `/backend-audit` dispatches this skill and folds its coverage block into its transition ledger rows; `/backend-fix` closes findings failing-first through the real entry points and re-runs this detector.
- business `@workflow-integrity` draws and judges the graph (the `workflow-transitions` owner); `job-lifecycle-scan` (this pack) inventories the jobs and webhooks that fire events; `edge-error-scan` §2 maps the library's exception to a status; `@api-reviewer` judges these rows.
- database `transaction-scan` §1/§8, security `logic-race-scan` §2/§3/§5, code-quality `correctness-smell-scan` §4/§5 — when those packs are installed.

## Sources

Library behaviour tagged `[V]` was run in backend research lab B on 2026-10-14: transitions 0.9.3 (the default `MachineError`; `ignore_invalid_triggers=True` and a failed `conditions` guard returning `False`; `source='*'` re-opening a terminal state) and python-statemachine 3.2.2 (`TransitionNotAllowed`; `allow_event_without_transition=True` returning `None`) in `py/sm.py`, XState 5.33.2 (an unhandled event ignored, `can()` false, events after a final state ignored) in `node/x.mjs`; AASM `whiny_transitions` and `requires_lock` from its README, looplab/fsm's error types from its source, the Spring Statemachine release date from its repository (backend research notes B § 2). `[K]`/`[K?]`: AASM without `from:`, Spring Statemachine's result type, .NET Stateless. The real-repo, fixture and lab counts are from read-only runs of the block above on 2026-10-14 (batch-5 eval § 2.6 and § 5.7). Paraphrased; no text reproduced beyond identifiers.
