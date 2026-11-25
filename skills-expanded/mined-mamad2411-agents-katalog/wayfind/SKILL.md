---
name: wayfind
description: >
  goalforge-internal — use entry commands; do not auto-trigger Chart a foggy, multi-session effort into a decision map BEFORE goalforge-capture
  — when the work is too big to spec yet, spans multiple sessions, and needs a
  decision map before anyone can write a real spec. Triggers: "chart this foggy
  effort", "multi-session decision map", "too big to spec yet", "map the unknowns
  before we plan". Establishes <PLANS_ROOT>/<effort>/wayfind/ (map.md pointer-index +
  one-decision-per-ticket files), drives a frontier-computed work loop across
  sessions, and graduates the converged map into goalforge-capture. SKIP when the
  effort is one session and already clear — a single well-understood feature goes
  straight to goalforge-capture with no map. SKIP for a bounded one-off edit, and
  for anything already past spec (that is the SDD chain, not wayfind).
argument-hint: "<effort-slug> [chart]"
metadata:
  skill-kind: preference
  version: 0.3.0
---

# Wayfind

A situational **pre-spec on-ramp** positioned BEFORE `goalforge-capture`. It runs
entirely on existing machinery — `plans/` folders, OKF-ish frontmatter,
`depends_on` edges, the dispatch matrix, and the `interview` plugin / `prototype` /
`research-analyst` skills. No new tracker, no parallel conventions, **no new
handoff mode**. Three phases, one command (`/wayfind`).

Use wayfind ONLY when an effort is too big/foggy for one session. **No-fog early
exit:** if charting surfaces no real fog, build no map — hand the loose idea
straight to `goalforge-capture`.

## Artifact layout

```
<PLANS_ROOT>/<effort-slug>/
  wayfind/
    map.md                     # pointer-index only
    ticket-NN-<slug>.md        # one decision per file, NN zero-padded, assigned at create
    findings/
      ticket-NN.md             # research/prototype outputs (linked from ticket resolution)
      quiz-back.md             # exit-gate record (questions, answers, gaps) — authoritative store
      blind-spot-NN.md         # blind-spot pass record (candidates, why_blind_spot, triage) — authoritative store
  overview.md                  # written LATER by goalforge-capture on graduation
```

The same `<effort-slug>` becomes the feature slug — **graduation is in-place**.
`map.md` is a **pointer-index**: decision bodies live in tickets/findings, never
in the map.

Resolve `<PLANS_ROOT>` per `${CLAUDE_PLUGIN_ROOT}/references/schema.md`
§PLANS_ROOT resolution: env `SDD_PLANS_DIR` → project git-root `plans/` →
global `~/.claude/plans/`. Wayfind cites that rule, never its own convention.

**Auto-phase (`/wayfind <effort-slug>`):** no `wayfind/` map present → **chart**;
map present → **work** (work offers graduate when the frontier script reports
`converged: true`). `/wayfind <effort-slug> chart` forces a re-chart / add-tickets pass.

**Discovery (`/wayfind` with NO slug)** — the session-resume entry point: run
`bash ${CLAUDE_PLUGIN_ROOT}/skills/wayfind/scripts/wayfind-status.sh <PLANS_ROOT>` and present the
active efforts it lists (slug, `open` count, `frontier`) to pick from; the pick
continues into the auto-phase above. Read-only; `frontier`/`converged`/`stale_claims`
pass through verbatim from the sibling frontier script; `open` is counted directly
from ticket files with `status: open` (the arrays are no disjoint partition). stdout `{"efforts": [{"slug", "status": working|charting, "frontier",
"open", "converged", "stale_claims"}]}`; exit 0 in every valid state (zero
efforts → `{"efforts": []}`), exit 2 only on a missing `<PLANS_ROOT>`; a
malformed effort degrades to `{"slug", "error"}` and never hides the rest.

---

## chart flow

Establish `<PLANS_ROOT>/<effort-slug>/wayfind/` from a foggy effort
description (or a graduating idea).

**1. Write `map.md`** (frontmatter verbatim from the Interface Contract):

```yaml
type: wayfind-map
status: charting | working      # convergence is COMPUTED by the frontier script, never stored
destination: "<one-line pinned scope>"
created: YYYY-MM-DD
context_pointers: []            # paths/globs the blind-spot pass sweeps (set at chart, editable)
references: []                  # provenance; bridges into the graduated feature's sources[]
```

`references[]` uses the CANONICAL typed shape — cited, never re-invented:
`~/.claude/skills/idea/references/provenance-mapping.md` (`id` / `type` /
`locator` required, `note` / `retrieved` optional; `type` from
`url|file|spec|paper|repo|session|conversation|image|video`). A bare `- <string>`
entry stays legal and reads as `{locator: <string>}` — legacy prose entries carry
over LOSSILY (id/type/note/retrieved dropped), not unexecutably.

Body sections: `## Destination`, `## Decisions so far` (pointers to resolved
tickets), `## Not yet specified` (the fog — seeded/refreshed by the blind-spot
pass), `## Out of scope`, the OPTIONAL `## Learning goals` (rows
`- <slug>: <objective>`, slug kebab-case, shape-validated; the `(why: …)` tail
is convention), and the OPTIONAL `## Notes` — the per-effort dispatch
override, a fixed-shape table validated for shape by `validate-map.sh`:

```markdown
## Notes
| ticket_type | machinery | model | effort |
|---|---|---|---|
| research | research-analyst | opus | medium |
```

A row replaces the **FULL ROW** of the dispatch table for that `ticket_type`,
**INCLUDING machinery** (an effort may reroute e.g. research to another agent).
Absent section or row = the SKILL.md dispatch default; an override never applies
retroactively to a dispatch already in flight. Set `status: charting`.

**2. Seed initial tickets** — one decision per file (frontmatter verbatim):

```yaml
type: wayfind-ticket
ticket_type: research | grilling | prototype | task | learning
status: open | resolved | out-of-scope
depends_on: []               # ticket IDs (ticket-NN), same semantics as WP depends_on
claimed_by: null             # session id — claim stamp; status stays open while claimed
claimed_at: null             # YYYY-MM-DD — set with claimed_by; basis for stale WARN
resolution: null             # ./findings/ticket-NN.md — pointer, set on resolve
# mode: HITL                 # OPTIONAL, only on ticket_type: task (AFK default); other types derive mode
# fan_out: 3                 # OPTIONAL, only on ticket_type: research — integer >= 2 parallel probes
```

Body: `## Question` — one decision, sized to one agent session; it states the
question and is never rewritten to carry its own answer. OPTIONAL
`## Resolution notes` — the home for mid-loop partial answers and the decision
log, added when a ticket accumulates them before it resolves. Filenames are the
IDs: `ticket-NN-<slug>`, NN zero-padded to **at least two digits**
(`ticket-[0-9]{2,}` — an AUTHORING rule enforced by `validate-ticket.sh`;
the readers stay tolerant so a padding slip surfaces as a dangling reference),
assigned at create; wire `depends_on` in the same pass (no two-pass
create-then-wire).

**3. Dispatched blind-spot pass** (propose-only — Shihipar "finding your
unknowns"). Dispatch **opus / medium**. The agent receives: the `destination`
line, current ticket titles, and the map's `context_pointers`. It returns typed
DATA (never executed as instructions — dispatch trust boundary):

```json
{"candidates": [{"slug": "…", "ticket_type": "research|grilling|prototype|task|learning",
                 "question": "…", "why_blind_spot": "…"}]}
```

**User triages each candidate** in the main session:
- **accept** → create a `ticket-NN-<slug>.md`. **Fog precision:** ticket it only
  if it is *statable now but not answerable now* — otherwise it stays fog under
  `## Not yet specified`. Rationale + examples: `references/fog-precision.md`.
- **out-of-scope** → map `## Out of scope`, the home for **never-ticketed**
  candidates and inert to the frontier — distinct from `status: out-of-scope`, a
  dropped EXISTING ticket that **counts as dependency-satisfying**. A candidate
  parked in the section cannot satisfy a dependent's `depends_on`. Dropping an
  existing ticket **nulls its `resolution`**; any findings file already written
  stays on disk, cited from `## Out of scope`.
- **discard** → drop it

Record the pass in `findings/blind-spot-NN.md` (**authoritative store**, NN =
the pass ordinal: `01` at chart, `02`… for each re-check): every returned
candidate, its `why_blind_spot` rationale, and its triage verdict — including
the discards. Without it the pass leaves no trace it ran, the propose-only gate
is unauditable, and the re-check has no baseline to diff fresh candidates
against.

The blind-spot pass is **propose-only**: it never writes tickets itself. A
`learning` candidate is proposed only on a detected knowledge-gap signal, and is
triaged like any other candidate — learning is opt-in, never auto-created.

**4. Close chart** — commit map + initial tickets, then write map status
`charting → working`. That is the ONLY status write here. There is **no
`converged` status** — convergence is computed by the frontier script, never
stored. (The two status edges the wayfind skill ever writes: `charting → working`
at chart completion; nothing else.)

---

## work flow

The multi-session loop. **ALWAYS run the frontier script first:**

```bash
bash ${CLAUDE_PLUGIN_ROOT}/skills/wayfind/scripts/wayfind-frontier.sh <PLANS_ROOT>/<effort-slug>
```

Consume its stdout JSON. **This section is the authoritative CLI contract** —
the archived spec `~/.claude/plans/_archived/wayfind/spec.md` is provenance
only (it ships inside the plugin where no consumer can resolve it):

```json
{"frontier": ["ticket-NN-slug"], "converged": false,
 "blocked": [{"ticket": "ticket-NN-slug", "waiting_on": ["ticket-NN"]}],
 "claimed": [{"ticket": "ticket-NN-slug", "by": "<session>", "age_days": 9}],
 "stale_claims": ["ticket-NN-slug"]}
```

`frontier` = open tickets with all `depends_on` satisfied and `claimed_by` null
(a dependency is satisfied when `resolved` OR `out-of-scope`); `claimed` = open
tickets with `claimed_by` set; `converged` = zero open tickets; `stale_claims` =
**open-ticket** claims older than 7 days (a resolved ticket never reports
claimed or stale) (WARN on stderr, never auto-reset); `blocked` is
human-diagnostic-only (no automation consumes it). Exit 0 in any valid state;
exit 2 fail-close (missing dir, no `wayfind/`, zero tickets, duplicate ticket
NN, dangling `depends_on`, or malformed frontmatter — naming the file); exit 1
is `--self-test`-only. Read-only, sole computer of convergence (Constraints).

**Pick** the next unclaimed `frontier` ticket. If `frontier` is empty while
`converged` is false, do **NOT** pick — the loop has stalled. Diagnose from
`blocked` and `claimed`, then take the matching action:

| Signal | Diagnosis | Action |
|---|---|---|
| `stale_claims` non-empty | owning session died mid-ticket | confirm it is dead, clear `claimed_by` / `claimed_at` to null, then re-pick |
| `claimed` non-empty, all ages ≤ 7 days, and every `blocked` chain terminates in a claimed ticket | ordinary dependency wait behind a live claim | do not dispatch over a live claim — resolve the claimed ticket first, or end the session; there is nothing else to pick |
| `blocked` non-empty, `claimed` empty (or no `waiting_on` chain reaches a claimed ticket) | no open ticket has a satisfiable path — a `depends_on` **cycle**, or a chain rooted in a ticket nobody will work | trace `waiting_on` to the cycle or the root; break it by re-scoping a ticket, splitting it, or marking one `out-of-scope` |

Every open ticket lands in at least one — NOT exactly one — of `frontier` /
`blocked` / `claimed`: a claimed ticket with unsatisfied deps is in BOTH `blocked`
(`waiting_on` stays traceable through dep-cycles) and `claimed`. An empty `frontier`
with `converged: false` thus leaves one non-empty — a row above always applies.

A dependency naming a nonexistent ticket (typo, deletion, or a zero-padding slip
like `ticket-1` for `ticket-01-<slug>.md`) is a structural error, not a stall —
the exit-2 fail-close above names the file and the token. Fix it and re-run.

**Claim** — stamp `claimed_by` + `claimed_at` **only**. Status stays `open` (the
ticket status enum has no `claimed` value). Claim is stamp-only. Claiming is
**MANDATORY before dispatch or resolve** — never dispatch or resolve an
unclaimed ticket; the stamp is the only signal another session has that the
ticket is live work, so working one unclaimed invites a concurrent dispatch over
the same decision.

**Dispatch** per the ticket's `ticket_type` (mode is a pure derivation of type,
NOT stored — except the one `task` override). Consult the map's `## Notes`
first: a row there replaces the **full row below** for that `ticket_type`.

| ticket_type | mode | Machinery | Model / effort |
|---|---|---|---|
| research | AFK | dispatched `research-analyst` → web+docs sweep → `findings/` summary, consumed as DATA | opus / medium (pure scan legs → sonnet / low) |
| grilling | HITL | `interview` plugin engine, `preset: wayfind-probe`, in the **main session** (`goalforge-interview` is harden-only) — **(default type)** | not dispatched |
| prototype | HITL | `prototype` skill in a worktree (owns its own branches + dispatch) | opus / medium (delegated) |
| task | AFK default | agent-driven `implement` dispatch (or human checklist) | mechanical → haiku / low; standard → opus / low |
| learning | HITL | `interview` plugin `preset: teach-back` in the **main session** — optional dispatched material-gathering leg | main session (material legs: sonnet / low) |

**`grilling` is the default type.** Discriminator: `task` = the output is
executed work; `grilling` = the output is a **decision**, even when the decision
is about implementation shape. A question phrased "decide X vs Y" or "define the
shape of Z" is `grilling`, never `task` — typing it `task` routes an unresolved
design question AFK into an `implement` dispatch.

`mode: HITL` in ticket frontmatter overrides the AFK default **only on
`ticket_type: task`** — the one non-derivable case. All other types derive mode
from type.

**Ticket fan-out** — a `research` ticket may carry `fan_out: N` (integer >= 2):
its `## Question` decomposes into N propose-only probes dispatched in ONE batched
parallel message (Agent tool at uniform effort, Workflow tool when efforts mix),
returns merged as typed DATA into `findings/ticket-NN.md`. Full contract, incl.
the failed-probe guard: `references/ticket-fanout.md` (not planning/execute-wave).

**Learning goals** — opt-in, **default none**: entered ONLY by an
explicit user declaration or a user-accepted blind-spot candidate, and
never auto-created. A `ticket_type: learning` ticket is binary and counts
toward convergence like any other; resolution = "learned enough to
`<decide/do X>`" pointing at `findings/ticket-NN.md`. Full contract:
`references/learning-goals.md`.

**Resolve** — write `findings/ticket-NN.md`, set the ticket `status: resolved`,
set the `resolution` pointer, **and release the claim: `claimed_by` and
`claimed_at` back to `null`**. Resolving without releasing leaves a claim stamp
on a done ticket, which ages into a false stale signal. A dependency counts as
satisfied when `resolved` OR `out-of-scope`.

For `ticket_type: grilling` **only**, that findings file carries a REQUIRED
`## Q&A resolution-notes` section — questions asked, answers in the user's
terms, the decision, and confidence at stop. AUTHORING rule: no validator, no
template; distinct from the OPTIONAL ticket-body `## Resolution notes` above.

**Mid-loop fog moves:** surface new tickets when a resolution exposes fresh unknowns;
graduate map `## Not yet specified` fog into real tickets; re-scope when a resolution
invalidates an already-resolved decision. **No pre-slicing** — never split a ticket
into sub-tickets before it is picked. **One ticket per session** is the DEFAULT,
excepted only by `ticket_type: research` tickets (AFK + non-conflicting, a property
of the type) and trivially-coupled ones. No machine check.

**End the session** — BEFORE committing, run all three validators from
`${CLAUDE_PLUGIN_ROOT}/skills/wayfind/scripts/` and **FIX every failure before committing**
(BLOCK-by-instruction; wayfind ships no hook): `validate-map.sh
<effort>/wayfind/map.md`, `validate-ticket.sh` on every `ticket-NN-*.md`, and
`validate-linkage.sh <effort>` (resolved ↔ map-pointer ↔ findings agreement;
read-only, and never a computer of convergence). Then commit map + tickets in a
**consistent state**. The map IS the resume point — no wayfind handoff mode. A generic `session`-mode
handoff is used only when ONE ticket's resolution is mid-flight and needs
conversational context (e.g. an interrupted grilling).

---

## graduate flow

Entered from work when the frontier script reports `converged: true`. A
**strictly ordered, gated** sequence — each gate can ABORT the graduation, at
which point the map is simply `working` again (no status unwind needed).

1. **Precondition** — frontier script reports `converged: true` (zero open
   tickets; an in-flight claim keeps a ticket open, so it blocks convergence by
   construction).

2. **Blind-spot re-check** (dispatched, propose-only — same opus/medium
   contract as chart). Fresh candidates → user triage. **Any accepted candidate
   becomes a new ticket and ABORTS graduate** (map is `working` again).

3. **Quiz-back gate** (HITL, main session — never dispatched). `preset: quiz-back`
   over the map's decisions; record questions/answers/gaps →
   `findings/quiz-back.md` (authoritative store). A surfaced gap either becomes a
   new ticket (**ABORT**) or a recorded **accepted-risk** (proceed).

4. **User confirms transfer** (the human stays in the loop at the chain
   boundary).

5. **Exit-transfer** — compose a **graduation brief** (destination line, resolved
   decisions, scope bullets, references) and invoke `goalforge-capture` with it as
   the free-text intent, passing map `references[]` for `sources[]` plus a
   `wayfind-<effort-slug>` self-link entry. **Scope discriminator:** a resolved
   `task` ticket becomes a scope bullet ONLY when its resolution is a
   **decision about future work**; one whose resolution IS the executed work is
   reported as **completed work**, never as scope. Concrete invocation brief:
   `references/graduation-brief.md`. **Before** invoking `goalforge-capture`, run
   `adr-write` for each decision that passes its three-condition gate (adr-write
   refuses the rest). Graduation ENDS at goalforge-capture's `overview.md`
   (status: draft) — spec/decompose proceed through the normal SDD chain; carried
   task tickets are consumed by `goalforge-decompose` from the spec, not wayfind.

6. **`wayfind/` stays in place** as provenance.

---

## Constraints (inline)

- **Frontier script is read-only** and the **sole computer of convergence** —
  SKILL.md never re-implements frontier logic; `goalforge-frontier.sh` is never
  modified (wayfind ships a sibling).
- **No new handoff mode** — the map is the resume point.
- **`map.md` is a pointer-index** — decision bodies live in tickets/findings.
- **Blind-spot pass is propose-only** — it never writes tickets itself; the user
  triages every candidate.
- **Claim is stamp-only** (`claimed_by` + `claimed_at`); status stays `open`.
- **Grilling and quiz-back run HITL in the main session**, never dispatched.

## Gotchas

- **An uncommitted claim is invisible to parallel sessions.** The claim stamp
  only synchronizes once it reaches the shared git state — a stamp sitting in
  your working tree protects nothing, and a parallel session can resolve the
  same ticket while you dispatch over it (live failure 2026-08-20: base-map
  ticket-41 resolved by one session while another, holding only a local claim,
  dispatched a duplicate research agent). On a map worked by concurrent
  sessions, COMMIT the claim stamp immediately after claiming — do not batch it
  into the end-of-session commit — and immediately before claiming, re-read the
  ticket file and check `git log` freshness for the map: a same-day parallel
  resolution may postdate the frontier output you are holding.

- **A stale claim is not a free ticket.** `claimed_by` + `claimed_at` are
  stamp-only and the ticket status stays `open`, so a claimed ticket is excluded
  from `frontier` while still counting against `converged`. A session that dies
  mid-ticket therefore silently stalls the whole loop: the frontier script emits
  the ticket under `stale_claims` (WARN on stderr past 7 days) and **never
  auto-resets it**. Do not treat a stale claim as unclaimed and dispatch over it
  — confirm the owning session is dead, then clear `claimed_by` / `claimed_at`
  explicitly before re-picking it. Clearing the stamp is the whole remedy:
  "resolve the ticket" is not an alternative, because Resolve itself releases
  the claim. Only OPEN tickets are reported under `claimed` / `stale_claims`, so
  a stale claim always means live work that stalled — never a leftover stamp on
  something already done.

- **`converged: true` is not "no fog left".** Convergence counts open tickets only —
  fog in map `## Not yet specified`, or never ticketed at all, is invisible to the
  frontier script. Fog is therefore worked CONTINUOUSLY by the mid-loop fog moves, and
  the graduate gates (blind-spot re-check, HITL quiz-back) are the LAST net, not the
  only one. Relabelling a real gap an "accepted risk" ships fog into `goalforge-capture`.

- **End every session in a consistent commit state.** The map IS the resume
  point — there is no wayfind handoff mode — so a half-committed map/ticket set
  is the resume point being wrong. Commit `map.md`, the ticket files, and
  `findings/` together: a committed `resolution:` pointer to an uncommitted
  `findings/ticket-NN.md`, a committed claim stamp with no findings, or a
  `status: resolved` ticket whose map pointer was not updated all leave the next
  session computing a frontier from a state that never existed.

## Dependencies

Dispatch targets wayfind reaches for, and what it does when one is absent. A
missing dependency **degrades, never blocks** — wayfind ships no vendored copy
of any of them.

| Target | Kind | Availability | Degrade path |
|---|---|---|---|
| `research-analyst` | agent | dotfiles `agents/research-analyst.md`; NOT shipped with the plugin | dispatch a general-purpose agent with an explicit research brief |
| `interview` | plugin skill | cogwright marketplace (source: elicitforge); NOT shipped with this plugin | one-question-at-a-time `AskUserQuestion` loop in the main session |
| `adr-write` | skill (private child of the `knowledge-write` router) | dotfiles; NOT shipped with the plugin | skip the ADR gate; log the skipped decisions in the graduation brief |
| `prototype` | skill | in-package co-tenant | always available |
| `goalforge-capture` | skill | in-package chain stage | always available |
