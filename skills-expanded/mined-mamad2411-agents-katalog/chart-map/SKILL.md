---
name: chart-map
description: >-
  Chart a Decision map for an effort too big for one agent session — name the
  destination, grill breadth-first to separate real decision tickets from fog,
  create the map and its tickets behind a dry-run gate, fire the research
  subagents, then STOP. Use when the user has a loose, foggy, multi-session
  idea — "this is huge, where do we even start", "plan this migration", "chart
  this", "make a decision map", "map out this initiative", "too big for one
  session" — and the route to the goal is not visible yet. Do NOT use for a
  well-scoped single-session design (that is grill-then-plan / sp-grill-with-doc),
  and do NOT use to continue a map that already exists (that is work-map). If
  the opening grill surfaces no fog, this skill stops and says a map is not
  needed.
argument-hint: "<loose idea — e.g. 'migrate billing to the new provider'>"
effort: high
---

# chart-map

Chart the way; don't charge at the goal. The output is a **Decision map** — one
item indexing the whole effort — plus child **Decision tickets**: questions whose
resolution is a *decision*, each sized to one session.

**Plan, don't do.** Charting creates the map and hand-resolves nothing (ADR
0041). One charting run is one session, and it ends at Step 5.

Emit this diagram once, at the start, so the user can see the whole run:

```
CHART A DECISION MAP — one session, then stop
─────────────────────────────────────────────

  ① PREFLIGHT — ask which backend
  │   local docs/decision-map/<slug>/
  │   or GitHub issues + sub-issues
  │   name it BEFORE any charting
  ▼
  ② DESTINATION  (HITL — the human answers)
  │   what does arriving look like?
  │   one or two sentences, one line, first
  ▼
  ③ FRONTIER — breadth-first, never deep
  │   HITL too: you ask, the human answers
  │   can you STATE the question now?
  │     yes → ticket · no → fog
  │     past the destination → out of scope
  │
  │   no fog anywhere? ■ STOP — no map
  │      needed; hand to grill-then-plan
  ▼
  ④ GATE — dry run first, always
  │   create · skip (exists) · merge
  │   show every label → get a yes → --real
  ▼
  ⑤ RESEARCH subagents, in parallel
  │   findings posted back with `resolve`
  ▼
  ⑥ LINT — run the check, report it
  │   exit 0 clean · exit 3 findings
  ▼
  ■ STOP — report the `frontier`, hand off
     charting hand-resolves nothing
```

## Step 0 — Preflight: name the backend before you chart

**Two backends exist. Ask which one, before anything else happens** — even if
the user never mentioned a tracker. Someone who expected their map on a shared
board needs to learn where it lands **here**, not after spending a session
charting.

| backend | where the map lives | how it is shared | needs |
|---|---|---|---|
| **local markdown** (default) | `docs/decision-map/<slug>/` in this repo | by committing the repo | nothing |
| **GitHub Issues** | an issue per map, a **sub-issue** per ticket, native `blocked-by` dependencies | the repo's issue tracker — visible to anyone with access | `gh auth status` passing, and a repo you may write issues to |

Default to **local** and say so; only use GitHub if the user asks for a board or
names a repo. Azure DevOps is **not** available (ADR 0059 — its half of the
marker probe has never been run). If ADO specifically is a hard requirement,
stop and say decision-map cannot do that yet.

Do **not** offer to install `ado-backlog` or `github-backlog` in either case —
neither plugin can drive a decision map, so offering them would be a false
promise. `github-backlog` in particular is a *findings-to-issues* pipeline, not
a decision map; the two write different things to the same tracker.

Then fix these two, and use them for every command from Step 1 down:

| | local | GitHub |
|---|---|---|
| **`<ops>`** | `${CLAUDE_SKILL_DIR}/scripts/local_map_ops.py` | `${CLAUDE_SKILL_DIR}/scripts/github_map_ops.py` |
| **extra flag on every call** | *none* — `--root` defaults to `docs/decision-map` | **`--repo <owner>/<repo>`, always.** It is never inferred from the git remote: this writes issues |

Run `<ops>` with `python`, from the repo root, so a local map lands at its
ADR-0042 default location. Everything from Step 1 down is backend-neutral — the
subcommands, the flags, the JSON shapes and the gate are identical on both
(ADR 0062); only `<ops>` and that one flag change.

**On GitHub, two limits are hard and worth knowing before you grill breadth-first:**
a map cannot exceed **100 tickets** (GitHub's sub-issue ceiling) and a ticket
cannot be blocked by more than **50** others. `chart` checks both before it
writes anything rather than failing partway.

**Contract** — every subcommand, flag and JSON shape used below is fixed by
`references/data-contracts.md`. Where this skill and the
contract disagree, the contract wins.

The map is repo docs, so it is committed through **assisted git** — offer the
commit, never make it automatically.

## Step 1 — Name the destination

Run a short grilling exchange (load `sp-grill-with-doc` the way your harness loads
skills, if it is available; otherwise ask directly, one question at a time):
**what does reaching the end look like?** A written spec, a locked decision, a
change made in place?

One or two sentences. The destination is what every ticket is measured against,
and what makes "out of scope" decidable. Write it down before any ticket exists.

It is stored as a **single line** — the tool collapses any line break to a
space, in `title` and `destination` alike, so that a stray newline can
never truncate the value or inject a heading into the map document. Write it as prose,
not as a bulleted list or a paragraph break. (`notes` is different: it is a
**list** region now, one bullet per entry, and each bullet is flattened the
same way — ADR 0101.)

### The HITL guard — it governs this step and Step 2 both

Naming the destination is itself a HITL grilling exchange, and so is the
breadth-first grill that follows. **An agent that answers its own grilling
questions has broken the type.** A map charted that way is fiction: every
ticket on it is measured against a destination the human never actually agreed
to, and the whole effort then runs off it.

The line is *who supplies the answer*, not who does the work:

- **Explore for yourself** the factual questions — what the code does today,
  which services exist, what the repo has already decided. Reading is not
  asking, and the more you find out, the sharper your questions get.
- **Ask the human** every preference, trade-off, scope and destination
  question. One at a time.
- **Never pose a question and answer it in the same breath.** Your own
  recommended answer is a recommendation, never an accepted answer: offer it,
  then wait for the human to accept, reject or reshape it. Silence is not
  acceptance, and neither is a plausible-sounding default.

If the human is not available to answer, stop and say so rather than charting
alone.

## Step 2 — Map the frontier, breadth-first

Grill again, this time breadth-first: fan out across the whole space, never deep
on one thread. Depth is what the individual sessions are for.

The HITL guard above applies here too. The *classification* below is yours to
make — but the answers that feed it come from the human, not from you.

For each area, apply one test — **can you *state* the question precisely, right
now?** Not answer it. State it.

| Verdict | When | What you record |
|---|---|---|
| **Ticket** | you can state the question precisely now, even if it is blocked | a typed ticket (below) |
| **Fog** | you cannot phrase it sharply yet | one line under "Not yet specified" |
| **Out of scope** | it lies past the destination | one line under "Out of scope" |

Do not pre-slice fog into ticket-sized pieces. Fog that is left as fog graduates
into real tickets later, once an earlier decision has sharpened it.

### Ask what ships first (ADR 0100)

Once every ticket on this pass is named, ask one more question — in the
user's own terms, not the tool's: **"what do you want to be able to demo
first?"**, not "how do you want to group these tickets?". One question, and
it is skippable — say plainly that skipping it costs nothing, because the
grouping can be declared later from `work-map` once the map exists to group.
Keep it short: at most two options, and lead with your own recommendation
before asking — the framing every HITL question in these two skills should
use, and the one the HITL guard above already requires (a recommendation is
offered, never accepted on the human's behalf).

The answer becomes the map's first **milestone** in Step 3's input — which
ticket keys ship in that first increment. Everything else stays unassigned
until a later session groups it; that is a legal, unfinished state, not a gap
to fill now.

Type every ticket — the type picks its resolver and its mode (ADR 0038):

| Type | Mode | Resolved by |
|---|---|---|
| `research` | AFK | a research subagent, fired at chart time (Step 4) |
| `prototype` | HITL | a cheap artifact the user reacts to |
| `grilling` | HITL | a live grilling exchange — the default |
| `task` | either | doing the thing that unblocks a decision |

**If this step surfaces no fog at all, stop.** The way is already clear and the
whole journey fits one session, so a map would be overhead. Say that plainly and
point the user at `grill-then-plan` instead.

## Step 3 — Create the map (gated)

Build a `map_input.json` in a scratch working directory. These JSON files are
working files, never a store — the map itself is the source of truth.

```json
{
  "target": { "slug": "billing-migration" },
  "map": {
    "title": "Decision map - migrate billing to the new provider",
    "destination": "<the destination from Step 1, as one line>",
    "notes": ["<a skill every session should consult>", "<a standing preference>"],
    "notYetSpecified": ["<fog line>"],
    "outOfScope": ["<ruled-out line>"],
    "milestones": [
      { "slug": "mvp", "label": "demo the search page",
        "members": ["provider-choice"] }
    ]
  },
  "tickets": [
    { "key": "provider-choice", "title": "Provider - which one do we commit to?",
      "type": "grilling", "question": "<the decision this resolves>",
      "blocks": ["cutover-order"] },
    { "key": "cutover-order", "title": "Cutover order - big bang or per-tenant ramp?",
      "type": "grilling", "question": "<the decision this resolves>" }
  ]
}
```

- `slug` and every ticket `key` are lowercase-kebab, must match
  `[A-Za-z0-9][A-Za-z0-9_-]*`, and **must not contain `--`**.
- `milestones` is optional; each entry is `{slug, label, members}`, in the
  order you want them to ship — order is the list's own order, not the
  tickets' key order. A milestone `slug` follows the same rule as a ticket
  `key` (no `--`). A ticket belongs to **at most one** milestone, and a
  ticket in none is legal: it means "not yet scheduled", not an error.
- A later `chart` on the same map only **appends** a milestone that is
  entirely new and **unions** a new member into one that already exists. A
  member the map already places in a *different* milestone, a different
  relative order of two milestones that both already exist, or a changed
  `label` are each reported under `divergence` and left unapplied — the same
  contract as `title` / `destination`. Edit the milestones region
  by hand to move a ticket, reorder the list, or change a label.
- `blocks` is **downstream** — the tickets this one holds up. Readers see the
  upstream `blockedBy` instead; do not confuse the two.
- **Every `blocks` target must already exist**, either in this same input's
  `tickets[]` or on the map on disk. Naming one that exists in neither is a
  validation error: the run exits `2` and writes nothing. That is why the
  template above carries `cutover-order` as well as the ticket that blocks it.
- `mapType` / `ticketType` in the contract are Azure DevOps work-item types.
  They have no effect on the local backend — leave them out.

### The create-class gate (never skip it)

**1. Dry run.** `chart` is dry-run by default; `--real` is what writes.

```
python "<ops>" chart --input <workdir>/map_input.json
```

The plan lands twice: as JSON on **stdout** (machine-readable) and as a human
rendering on **stderr**. Show the user the stderr rendering.

**2. Read the labels — they are what the user is approving.** Every item the run
would touch appears exactly once, with one of four actions:

| Action | What it means for that item |
|---|---|
| `create` | it does not exist yet and will be created |
| `skip (exists)` | it exists and **nothing** will be written to it |
| `merge` | it exists and will be modified **in place, additively** — added to, never overwritten |
| `OVERWRITE` | `--force` only: it exists and will be fully rewritten, discarding its recorded state |

Every `merge` carries a `detail` naming exactly what it gains. A **ticket**
merge reads `unions blockedBy: <key>` — and that is the only thing a ticket
merge ever does. A **map-body** merge counts the lines,
`adds 2 fog lines, 1 out-of-scope line`; when it adds none but still rewrites a
region it says so instead — `normalises the map body's list regions (no new
lines)`, which is what you see after a hand edit left a region empty or ragged
and the run is only restoring the tool-owned `- (none)` placeholder. Read those
details out; then add the part the count cannot convey: it is a **union**, so it
can add lines but never removes or reorders the ones already there, and a fog
line the input omits stays on the map.

On a first chart every line is `create`. On a later chart most lines are
`skip (exists)` — that is the design, not a failure: **`chart` is additive** (ADR
0054/0055). It adds what is absent and never removes, reorders or overwrites
what is there, so re-running the identical input is a byte-identical no-op, and
a partially-failed chart is resumable by simply re-running it. If you see an
`OVERWRITE` line and did not deliberately pass `--force`, stop and investigate.

**3. Ask for explicit approval. Never create without it.** The approval is for
the plan you just showed — if the input changes at all, re-run the dry run and
show the new plan.

**Carry the end-of-session commit offer in this same ask, on local.** In the
same message, ask whether to commit the new `docs/decision-map/<slug>/` folder
once the session ends, alongside any repo docs it produced -- so the session
pauses once, here, instead of twice. This does not weaken assisted git: a
bundled offer is still an explicit offer the user answers, and nothing is
committed without that yes. On GitHub there is nothing to commit for the map
itself, but any repo docs still need the same ask.

**4. On approval, re-run with `--real`:**

```
python "<ops>" chart --input <workdir>/map_input.json --output <workdir>/map.json --real
```

Keep the returned `map.json` as this session's working file. Show the user the
map's name and its path, and the tickets by name — never a wall of bare keys.
The script wires the **blocking edges** itself, in a second pass once every
ticket exists. There are no parent links to wire: on the local backend
containment *is* the directory — a ticket belongs to this map because it sits in
that map's tickets — and the map document holds no index of open tickets, only
the "Decisions so far" list that `resolve` projects from the closed ones. Each
created ticket also carries a generated **position diagram** below `## Question`,
written and maintained by the script rather than by you (ADR 0063/0064).

**5. Check `divergence` in the result.** A non-empty list means the input asked
for something an additive run deliberately did **not** apply — most often a
changed `title` / `destination` on a map that already exists. Report
every line. The fix is to edit the map document by hand, never to reach for `--force`.
`notes` is not on that list on any map carrying the notes region: there it is a
list region that **unions** like the fog lines (ADR 0101), so a later `chart`
should carry only NEW note lines. (On a legacy map that predates the region,
`notes` is still a scalar and still diverges.) An
existing note restated in any other shape — the bullets joined into one string,
or pasted back with their `- ` prefixes — is a new line to the union, so it is
appended, silently, with no `divergence` to catch it.

**On failure:** a known, actionable failure exits `2` with one line on stderr
and **empty stdout**. That line names the field to fix. Correct
`map_input.json`, re-run the dry run, and re-approve.

**The gate will not remove a graduated fog line.** If this chart turns a line
that already sits under "Not yet specified" into a real ticket, union never
deletes, so the line is still sitting there. Delete it by hand from between the
`decision-map:fog` marker comments in the map document, leaving the markers themselves
alone — otherwise the map keeps advertising fog that is now a real ticket, and
the list slowly becomes a log of questions already answered.

### `--force` is an escape hatch, never a remedy

`--force` is **destructive**: on every item the plan labels `OVERWRITE` it
discards the recorded resolution, the claim and the blocking edges. Its exact
blast radius — which items it reaches, and what survives on each — is tabulated
in `references/data-contracts.md`. Read it there and quote
it; do not paraphrase it loosely.

Do **not** suggest `--force` because a re-chart printed `skip (exists)`, because
the map looks stale, or because a run half-failed. Additive `chart` already
covers all three, and `--force` is never required to add a ticket or an edge.
Offer it only when the user explicitly asks for an existing map to be rewritten
from a new input — and only after showing the `--force` dry run's `OVERWRITE`
lines and naming, per line, what will be destroyed. The plan will not name it
for you: an `OVERWRITE` entry carries `detail: null`, so you have to work each
line's cost out of the contract's `--force` table and say it out loud yourself.

## Step 4 — Fire the research subagents

Every `research` ticket is AFK, and they are the one exception to
one-ticket-per-session. For each one just created:

1. Dispatch a research subagent — all of them in parallel, the way your harness
   runs subagents. Give it that ticket's Question verbatim plus the destination
   line for context, and ask for raw markdown findings, not a polished summary.
2. Write each set of findings to a scratch file and post it onto its ticket:

```
python "<ops>" resolve --map <slug> --ticket <key> --gist "<one-line answer>" --body-file <workdir>/findings-<key>.md
```

`resolve` records the resolution, closes the ticket, and re-projects the map's
"Decisions so far" index.

**Escalation (ADR 0038).** If a research question can only be answered from a
live system — a real schema, a real org's data, the actual code — do not answer
it from outside knowledge. Leave the ticket **open** and note on it that it
should be resolved via `study-design-verify` in its own session:

```
python "<ops>" comment --map <slug> --ticket <key> --body-file <workdir>/note-<key>.md
```

## Step 5 — Stop

**Run the check on the map you just made** (ADR 0067). `lint` reads it and writes
nothing — exit `0` clean, exit `3` with findings:

```
python "<ops>" lint --map <slug>
```

A fresh chart should be clean. If it is not, an input that passed the gate still
produced a broken map — a blocking cycle is the one the gate cannot see, because
each edge is valid on its own. Fix it before reporting a map the next session
will trip over.

**Read the frontier before you report it.** The split you are about to show
answers "what can the next session pick up", and `map.json` cannot answer that:
its `blockedBy` deliberately lists **every** recorded blocker, open or closed.
Step 4 has just produced exactly the state that trips this up — a `research`
ticket you resolved may have been blocking something, and in `map.json` that
something still looks blocked. `frontier.json` counts only the **open**
blockers, which is the whole point of it:

```
python "<ops>" frontier --map <slug>
```

Its three buckets — `frontier`, `blocked`, `claimed` — are what you report.
`map.json` stays the full picture; the frontier is the answer to "what is
takeable".

Report, in this order:

- **any `lint` finding**, errors first — and say explicitly when it came back
  clean;
- the map's name and path;
- the **frontier** tickets **by name** — what the next session can pick up;
- the **blocked** tickets by name, each with the open blocker still holding it;
- what the research subagents resolved, one gist each;
- the fog lines still unspecified;
- what was ruled out of scope.

One line per bullet, no filler, around ten lines in total -- group rather than
itemize when a bullet would otherwise run to a list of its own.

On **local**, offer to commit the new `docs/decision-map/<slug>/` folder
(assisted git — offer, never automatic). On **GitHub** there is nothing to
commit: the map is already live in the tracker the moment `--real` returned, so
give the map issue's URL instead and say that anyone with repo access can see it
now. If the Step 3 gate already carried this offer and the user approved it
there, commit now without asking a second time -- the yes you are holding *is*
that explicit offer, answered.

Then suggest `/decision-map:work` for the next session, and **stop**. Do not
claim a ticket, do not resolve one, do not start the first decision. Charting is
one session's work, and the map — not this conversation — carries the state from
here on.

Fog graduates into new tickets later through this same Step 3 gate, driven from
`work-map`: `chart` is one operation serving both acts (ADR 0057).
