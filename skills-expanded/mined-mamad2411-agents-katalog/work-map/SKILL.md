---
name: work-map
description: >-
  Work one session of an existing Decision map — load it, show the frontier
  (open, unblocked, unclaimed tickets) by name, claim exactly ONE, resolve it
  with the matching arc skill (grilling / prototype / research / task), record
  the answer on the ticket, graduate any fog it cleared through the dry-run
  gate, then STOP. This is also the skill that graduates fog on its own, when a
  map has nothing takeable left but fog remains. Use when a map already exists
  and the user says "continue
  the map", "next decision", "work the decision map", names a ticket on it, or
  comes back to a charted effort. Do NOT use to create a map or to add the
  first tickets to a foggy idea (that is chart-map), and do NOT use for a
  single-session design with no map behind it (that is grill-then-plan /
  sp-grill-with-doc). Never resolves more than one HITL ticket in a session.
argument-hint: "[map slug, or a ticket name on it — optional]"
effort: high
---

# work-map

One session, one decision. The **map — not this conversation — is the state
carrier**: everything that gets decided is written onto a ticket before the
session ends, so the next session can start cold from the map and lose nothing.

Emit this diagram once, at the start, so the user can see the whole run:

```
WORK A DECISION MAP — one decision, then stop
─────────────────────────────────────────────

  ① PREFLIGHT
  │   which backend holds THIS map?
  │   local docs/decision-map/<slug>/
  │   or GitHub issues (needs --repo)
  ▼
  ② FRONTIER
  │   read the map, then list the frontier
  │   BY NAME — never a wall of bare ids
  │
  │   nothing open, no fog? ■ the map is done
  ▼
  ③ CLAIM — one ticket, immediately
  │   the pick IS the approval; claim first,
  │   before any work, so others skip it
  ▼
  ④ RESOLVE by type
  │   grilling · prototype · research · task
  ▼
  ⑤ RECORD
  │   repo doc? gist + link
  │   no repo doc? the body IS the record
  ▼
  ⑥ FOG — graduate through the chart gate
  │   dry run → labels → a yes → --real
  ▼
  ⑦ LINT — run the check, report it
  │   exit 0 clean · exit 3 findings
  ▼
  ■ STOP — one HITL ticket per session
     wanting "just one more" = the edge
```

## Step 0 — Preflight: name the backend before you work

**Two backends exist, and a map lives in exactly one of them.** Work out which
before anything else happens — a session that reads the wrong backend reports an
empty or missing map and looks like a finished effort.

| backend | where the map lives | how to tell |
|---|---|---|
| **local markdown** (default) | `docs/decision-map/<slug>/` | the directory exists in this repo |
| **GitHub Issues** | an issue labelled `decision-map:map`, one **sub-issue** per ticket | the user names a repo or a board, or no local directory exists |

Azure DevOps is **not** available (ADR 0059). If ADO specifically is a hard
requirement, stop and say decision-map cannot do that yet. Do **not** offer
`ado-backlog` or `github-backlog` — neither can drive a decision map.

Then fix these two, and use them for every command from Step 1 down:

| | local | GitHub |
|---|---|---|
| **`<ops>`** | `${CLAUDE_SKILL_DIR}/scripts/local_map_ops.py` | `${CLAUDE_SKILL_DIR}/scripts/github_map_ops.py` |
| **extra flag on every call** | *none* — `--root` defaults to `docs/decision-map` | **`--repo <owner>/<repo>`, always** |
| **what `--map` takes** | the slug | the map's **issue number** *or* its slug |

Run `<ops>` with `python`, from the repo root. Everything from Step 1 down is
backend-neutral — the subcommands, flags, JSON shapes and gates are identical on
both (ADR 0062); only `<ops>` and that one flag change.

On GitHub the map is a shared tracker, so two things follow that do not apply
locally: **a claim is visible to everyone immediately** (which is the point —
claim before working, so a parallel session skips the ticket), and every write
lands in an issue's timeline, which is why `block` and an additive `chart` do not
re-write an edge that already exists.

**Contract** — every subcommand, flag and JSON shape used below is fixed by
`references/data-contracts.md`. Where this skill and the
contract disagree, the contract wins.

The map and any repo docs a resolution produces are committed through
**assisted git** — offer the commit at the end, never make it automatically.

## Step 1 — Load the map, show the frontier

If the user did not name a map, list the maps and ask which one — on local they
are the directories under `docs/decision-map/`; on GitHub they are the issues
labelled `decision-map:map`. If there is no map at all, this is the wrong skill:
point at `/decision-map:chart`.

**Read the map first**, and read it before the frontier:

```
python "<ops>" read --map <slug>
```

A map that does not exist fails here — exit `2`, one line on stderr, empty
stdout. `frontier` fails the same way now (ADR 0061 made it assert the map
exists), so this is no longer the *only* guard against mistaking a missing map
for a finished one. Read first anyway: `read` is what gives you the destination,
every ticket's status and every gist, and the frontier alone tells you none of
that.

**Check for orphaned artifacts before showing the frontier.** This runs in **two
directions**, and the second one is the one that actually catches drift.

*Artifact exists, map does not know* — run `git status` and look for uncommitted or
untracked repo docs — an ADR, a spec, a CONTEXT.md edit — that name a ticket on this
map. A session that produced the artifact and then ended before Step 4 recorded it
leaves the decision **real but the map ignorant of it**, and usually leaves the ticket
`claimed` too. The map is the state carrier; an orphaned ADR is that carrier having
failed. Report what you find alongside the frontier — but do **not** record it
yourself without asking, because the claiming session may still be live.

*Map says closed, artifact does not exist* — **`lint` checks this; do not audit it by
hand.** It reports `closed-without-artifact` for every closed ticket of a type that owes
a durable artifact whose resolution names none. This half was prose in an earlier
revision, which was the wrong shape: the failure it exists to catch IS a complete
instruction being skipped in silence, so the remedy could not be another instruction
(ADR 0091).

```
python "<ops>" lint --map <slug>
```

A closed `grilling` ticket with no ADR is the **more common** failure and the more
expensive one, because nothing about the map's state looks wrong — the frontier is
clean, the destination looks nearer, and the reasoning is gone. Measured on one real
map: **8 closed `grilling` tickets, 1 ADR, 0 glossary terms**, while a sibling feature
run straight through `grill-then-plan` produced 14 ADRs and edited the glossary in
nearly every commit. On a tracker backend the rule needs the resolution body, so it
comes back under `notChecked` rather than passing quietly.

Report the findings as one line with the ticket keys, then **stop and ask**, and be
honest about the cost of the repair: an ADR written long after the code shipped tends to
record **what the code does** rather than **what was decided and what was rejected**, and
a confident ADR documenting the implementation is worse than none, because a later reader
trusts it. When the user does want them, draft from the ticket's own body — the question,
the `Confirming exchange`, the user's own words — never from the code.

`read` returns the map's `id` / `name` / `url` / `destination`, every ticket,
and now the ordered **`milestones`** list too — `{slug, label, members}` per
entry, in map order (ADR 0099). Milestones is the one region `read` *does*
report; the fog list, the out-of-scope list and the notes are the three that
still do not come back from `read` at all. Those three live only in the map
**document**, each between its own marker pair — `decision-map:fog`,
`decision-map:scope`, and now `decision-map:notes` too (ADR 0101 turned the
old bare `## Notes` paragraph into an append-only bullet region, the same
shape as fog and scope) — so **open it and read them**. You need the fog list
in Step 5, and again in Step 6's report — but not this same copy of it: Step 5
changes that region twice (the gate's merge adds lines, your hand edit deletes
the graduated one), and `frontier` carries no fog to refresh it. **Re-read the
map document in Step 6**; treat what you read here as good only until Step 5
writes:

- local: the file `docs/decision-map/<slug>/map.md`
- GitHub: the map **issue body** — `read`'s `map.url` links straight to it, or
  `gh issue view <number> --repo <owner>/<repo> --json body`

The regions are byte-identical in both, which is what lets one flow read either
(ADR 0062).

("Decisions so far" you do not need to read: it is a projection of the closed
tickets, and `read` returns each one's `status` and `gist` already.)

```
python "<ops>" frontier --map <slug>
```

Present it as prose, in this order:

- the **destination** line, verbatim — it is what every choice below is
  measured against;
- **decisions so far**, one gist each — the closed tickets in `read`'s output,
  the same lines the map document indexes;
- the **frontier, grouped by milestone** (ADR 0099): walk `frontier.json`'s
  `milestones` list in the order it gives them — that order is the map's own
  declared plan, not something a session chooses — and under each show its
  progress (`<closed>/<total>` closed) plus its takeable tickets by name, one
  line each with its type, never a wall of bare ids. **Each milestone carries
  its own blocked and claimed lines too**, not just its takeable ones: with one
  global blocked line a reader cannot tell whether the second milestone is
  stalled or simply untouched, and cannot see another session's claims sitting
  in a later group. Collapse them rather than itemizing — `2 blocked on
  <blocker name>`, `1 claimed by <session>` — so the group stays two or three
  lines. Every entry in all three buckets carries a `milestone` field, so no
  extra call is needed. After every milestone, list any ticket whose
  `milestone` is `null` as a final **unassigned** tail — takeable, blocked and
  claimed the same way, with no progress count, because there is no milestone
  for it to count against. `read` is what carries milestone *membership*
  (`map.json`'s `milestones[].members`); `frontier` is what carries
  *progress* and each ticket's own `milestone` field. The three buckets
  themselves stay key-ascending exactly as before (ADR 0062) — the grouping
  comes from walking the `milestones` list, not from re-sorting a bucket. On
  an unmilestoned map `milestones` is `[]`, so there is nothing to group and
  this collapses back to the flat list it replaces: takeable by name, then one
  line of **blocked** (`<name> — waiting on <blocker name>`) and one line of
  **claimed**, if any — another session is holding those.

One line per item, no filler: aim to keep the whole presentation around ten
lines, and on a map large enough to blow past that, group rather than itemize --
"four tickets blocked on `<name>`" beats four lines that each say it once.

A ticket sits in exactly one bucket, and the order is fixed by the contract:
**claimed** beats **blocked** beats **frontier**. So a claimed ticket does not
show its blockers here, and a blocked ticket lists only its *open* blockers — a
blocker that has closed is no longer a reason, which is precisely how resolving
one decision releases the next.

If the frontier is empty, go to Step 6 — the answer is either "the map is
done", "everything left is blocked or claimed", or "that was the wrong slug",
and Step 6 tells them apart.

### Offer milestones once, only on a big unmilestoned map (ADR 0100)

If `frontier.json`'s `milestones` is empty and more than five tickets came
back open, offer **one line**: "this map has no milestones; want to group
what ships first before picking?" Ask it once per session, never repeat it,
and a decline changes nothing — go straight to Step 2 either way. Below that
threshold, skip the offer outright: a small map does not need an ordering
layer, and milestones must never become a toll a session pays just to pick up
one ticket.

## Step 2 — Choose one, and claim it before you work

If the user named a ticket, use it — **unless it came back under `claimed`**,
which is the one case where you stop and ask first (below). Otherwise
recommend by the **two-level rule** (ADR 0099): first find the **earliest
incomplete milestone that has something takeable** — walk `frontier.json`'s
`milestones` list in order, skipping any milestone that is `complete` or
whose frontier tickets are none, and take the first one that has at least
one — then, inside it, apply the existing heuristic and recommend whichever
of its frontier tickets unblocks the most. Recommend an **unassigned**
ticket (`milestone: null`) only once every milestone is either `complete` or
blocked — i.e. the walk above found nothing takeable anywhere. Say the
reason in one line either way — the ordering was decided once, on the map,
so this session does not re-derive it.

**Before claiming, check the bucket the ticket came from.** Claim only what
`frontier` listed under `frontier`. A ticket under `claimed` is another
session's work: there is no tool backstop, so a second `claim` exits `0` and
silently replaces the first assignee, and the two sessions then resolve the same
decision two different ways with no trace that it happened. Ask the user whether
that session is still live, and say plainly that taking it over means the other
session's answer will land on a ticket you have already changed. On the local
backend the claim records whatever `--user` you passed, and an anonymous
claim (the bare default) names nobody, so the files cannot tell you who
holds it. Always pass a real `--user`, as the command below does; for a claim
already holding an anonymous value, only the user can identify it.

**Taking over a `claimed` ticket does not stop the other session.** There is no
lock: the user telling you to proceed settles who *should* own it, not who is
still writing. Expect the other session to keep resolving and to keep charting
— so re-read the map before every write (Step 5), and treat a second resolution
appearing on your ticket as evidence it was live, not as your own duplicate.

Then, the moment the user picks or accepts, **claim it — before any work at
all**:

```
python "<ops>" claim --map <slug> --ticket <key> --user "<purpose>-<HHMM>"
```

The pick itself is the approval; this is a lifecycle write, not a create, so it
needs no separate dialog (ADR 0039). Claiming first is the concurrency
handshake: a session that starts a minute later sees the ticket under `claimed`
and picks something else. Work first and claim later, and you have no handshake
at all.

**Claim before you IMPLEMENT, not only before you decide.** The ticket is the
unit of work in both phases. A session that resolves one ticket and then starts
building another ticket's content without claiming it has dropped the handshake
exactly where two sessions collide hardest: the source tree. Seen 2026-08-02,
`nav-registry-seam` sat open and unclaimed while two sessions each built the
whole nav registry, caught only because one noticed an export that had not
existed twenty minutes earlier. Note a claim does not lock files; for genuine
isolation give each session its own git worktree.

**A claim you cannot finish must be released.** There is no `unclaim`
subcommand, but `claim --user ""` does release one: it sets `assignee:` back
to empty and the ticket returns to the frontier. The catch is quoting — on
Windows PowerShell an empty string is dropped before argparse sees it, so the
command fails there. Under bash it works. If you are on PowerShell, or you
would rather not rely on shell quoting, clear the value by hand instead — so
if you end the session holding a ticket you did not resolve (the escalation in
Step 3 is the usual reason), edit:

```
local:   docs/decision-map/<slug>/tickets/<key>.md   →   frontmatter `assignee:`
GitHub:  the ticket issue                            →   unassign yourself
```

That is a legitimate edit in both: `assignee:` is ordinary frontmatter rather
than a tool-owned marker region, and a GitHub assignee is a native field the UI
exists to change. Clearing it puts the ticket straight back on the frontier.
Skipping it quarantines the ticket permanently, because every future session is
told above not to claim over `claimed`.

## Step 3 — Resolve it, by type

The ticket's `type` picks the resolver and the mode (ADR 0038). The ticket's
**Question** is the scope: if resolving reveals the question was wrong, do not
silently widen it — re-scope out loud, and record the re-scope in the
resolution. It is the exit condition too: the moment the Question is answerable,
stop grilling and go record it (Step 4). Questions that sit past it belong to
other tickets, or to fog -- breadth was chart-map's job, and it is already done.

| Type | Mode | How you resolve it |
|---|---|---|
| `grilling` | HITL | Load `dev-workflows:sp-grill-with-doc` the way your harness loads skills — or `dev-workflows:grill-then-plan` when this ticket's outcome is meant to be a written plan, and ONLY then: its Step 6 hand-off to `sp-writing-plans` is mandatory and terminal, and its Step 0 warns (non-blocking) rather than gates on the upstream superpowers plugin, so loading it for a decision-only ticket yields a spec plus an implementation plan per ticket where the map wanted one answer. **If the ticket is fix-shaped and the cause is not yet verified, verify the cause first with `debug-mantra`: never plan a fix on an unverified cause** (ADR 0003/0011). **Pose every question in the user's terms** - name the screen, what they press, and what they would observe; when two or more paths are in play put them in a small table, and make the stake concrete ("you save it under a parent record, you delete that parent later, it disappears"). An answer that comes back as a question ("what do you mean?", "which step of the app is this?") is a framing failure: re-pose it rather than explaining it at greater length. |
| `prototype` | HITL | Produce the cheap artifact through the ui-mockup mechanism — before the first render, read `references/ui-mockup.md` **as bundled with the dev-workflows plugin** (in this repo, `plugins/dev-workflows/references/ui-mockup.md`; once installed it sits inside that plugin's own directory, wherever your harness put it — the plugin-root path every other file reference in this skill uses points at decision-map, so it cannot address another plugin's file). A Claude Design design-system home is preferred per ADR 0032; a rendered artifact, then a self-contained local `.html`, are fallbacks 2 and 3, used only when the ones above are unavailable. The user reacts to the artifact; their reaction is the decision. Link the artifact onto the ticket with `comment`. |
| `research` | AFK | Normally already resolved by the chart-time subagents. If it is still open: dispatch a research subagent now, the way your harness runs them, and record its findings with `--body-file` in Step 4. |
| `task` | either | Do the thing if you can do it unattended; otherwise hand the user a **precise** checklist and wait. Record what was done, and the facts later tickets depend on — a task ticket's value to the map is the facts it leaves behind. |

**HITL means the human answers.** Preference, trade-off and scope questions go
to the user, one at a time. Your own recommended answer is a recommendation,
never an accepted answer — do not resolve a ticket on it. Silence is not
acceptance, and neither is a plausible-sounding default.

**Frame every question in the user's terms, whatever the ticket's `type`** — name the
screen, what they press, what they would observe. Restate where the session has got to
*immediately before* asking: a frame set at session open goes stale across a long
technical middle. And when a plan, ADR or standing rule already names a route, say so
and justify any deviation rather than offering a neutral menu. This is not grilling-only
— a `task` ticket's blocking question (which branch, which environment) fails the same
way. An answer that comes back as a question is a framing failure: re-pose it, do not
explain it at greater length.

If the human is not available to answer, stop and say so rather than resolving
alone. A decision recorded without them is worse than an open ticket: the map
presents it as settled, and the next session builds on it without knowing
nobody agreed to it. Release the claim (above) so the ticket goes back on the
frontier.

**Research escalation (ADR 0038).** If the question can only be answered from a
live system — a real schema, a real org's data, the actual running code — do
not answer it from outside knowledge. Leave the ticket **open**, note on it that
it needs `study-design-verify` in its own session, and pick something else or
stop:

```
python "<ops>" comment --map <slug> --ticket <key> --body-file <workdir>/note-<key>.md
```

**Then release the claim** — clear the ticket's `assignee:` frontmatter by hand,
exactly as Step 2 describes. You could not have avoided claiming it: you learn
that a question needs live-system grounding *here*, in Step 3, and by then the
claim has already happened, because claiming first is the handshake you must not
skip. An escalated ticket left claimed is a ticket no future session will pick
up.

The same `comment` call is how a prototype artifact's link, or any note that is
not the answer, lands on a ticket.

## Step 4 — Record the resolution (ADR 0036)

When the user confirms the answer, or the unattended work completes, write it
onto the ticket **in the same turn**. An answer that lives only in this
conversation is lost the moment the session ends.

There are two shapes, and which one you use depends on whether repo docs exist:

**1. The resolution produced repo docs** — an ADR, a CONTEXT.md term, a spec.
Those stay **canonical**. The ticket only gists, links and *pictures* them; it
never restates them:

```
python "<ops>" resolve --map <slug> --ticket <key> --gist "<one line>" --link <adr-path-or-url> --body-file <workdir>/body-<key>.md
```

**2. There is no repo doc** — research findings, task facts. Then the
resolution body **is** the record:

```
python "<ops>" resolve --map <slug> --ticket <key> --gist "<one line>" --body-file <workdir>/body-<key>.md
```

Both shapes pass `--body-file`, and for the same reason: it is the **only** slot
a diagram can go in. `resolve` renders the block as gist, then a `Detail:` line
for `--link`, then the body file — so with `--link` alone there is literally
nowhere for a picture to land, and the ADR-backed path is the common one.

`--gist` is required either way (without it: exit `2`, one line on stderr). It
is flattened to a single line and it is what the map's index shows, so make it
**one sentence that answers the question** — not one paragraph, and not a topic.
`resolve` warns on stderr past 200 characters and records it anyway; the warning
means the map index is now unreadable, not that the answer was rejected. Detail
belongs in `--body-file` or behind `--link`, never in the gist.

**The resolution body opens with one Mermaid diagram of the ANSWER** (ADR 0065)
— the first block of the `--body-file`, above any prose in it. It shows the
structure the decision creates, not the options weighed and not the process
followed. A reader who opens a closed ticket should see what was decided before
reading a word of prose. ("Opens with" is about the body: the gist and the
`Detail:` line are rendered above it, and both are one line.)

Match the diagram to the ticket's own `type`:

| `type` | diagram | what it shows |
|---|---|---|
| `grilling` | `flowchart TD` | the chosen shape and what it displaces |
| `research` | `graph TD`, or `erDiagram` for a real data model | the structure that was found |
| `prototype` | `sequenceDiagram` if the answer is a call order, else `graph TD` | the seam that was built |
| `task` | `graph TD` | before → after |

A ticket whose answer is an ADR draws its own diagram anyway, and it is **not** a
copy of the ADR's. The subjects differ: the ADR draws *chosen versus rejected*
(diagram convention, Rule 3); the ticket draws *what the chosen answer changes*.
Two diagrams with two subjects cannot drift into contradicting each other; two
copies of one diagram will. That is why shape 1 carries a `--body-file` even
when the ADR holds every word of the reasoning — the body file may be nothing
but the diagram.

This is separate from the **position diagram** the ops script generates below
`## Question` — that one is the ticket's place in the map, and you never author
or edit it.

Shape 1's body file holds the diagram at minimum; add prose to it when there is
a confirming exchange worth keeping alongside the ADR. **Quote the user's
confirming words in the body**: the close rides the conversation's own approval,
so the quote is the audit trail that makes that safe (ADR 0039).

One call does all of it: `resolve` writes the resolution block, closes the
ticket, and re-projects the map's "Decisions so far" index from every closed
ticket. There is no second call, and no map edit to remember.

**On local it is idempotent — re-resolving replaces the previous resolution
block. On GitHub it is NOT: the resolution is an issue comment, so a second
`resolve` posts a SECOND `## Resolution` comment** (the ticket's gist markers
and the map index do get replaced either way). **Count the gist yourself before
the first call** — a `--gist` past ~200 characters is warned about only *after*
it has been recorded, and re-resolving to shorten it leaves two resolutions on
the timeline. Seen 2026-08-10: ticket #16 of `claude-model-router` carries four,
two from each of two concurrent sessions.

**A measured gate must name the ref it was measured on.** A route count, a test
tally or a file count is true of one commit, and a resolution stating it bare is
read as describing the trunk forever. Write "24 paths on `main` (ba323d8)", never
"24 paths". On one map `carve-core-api` recorded "20 paths with ZERO module
routes" — correct for its branch, false on the trunk one merge later — and three
canonical docs plus four tickets had to be amended once a later session ran it.

**It must name its SEARCH SCOPE and the repo set it swept, too.** "0 hits" is not a
measurement; "0 hits in `*.cs` across 26 refs" is. An unscoped zero reads as "the thing is
not even specified", and the same grep over `*.md` will contradict it. Worse, a zero
measured in ONE repo says nothing when the product is split across sibling repos — seen
2026-08-19: a map recorded a feature "absent on all seven refs" while nine sibling repos on
the same disk held the CRM plugins, the Dataverse solution and three per-feature React
controls, one of them a plugin writing to the very record the new code would create.
Enumerate the siblings before writing any "not built" gist.

**If the ticket's subject is runnable, RUN it.** A compile gate and a route table
cannot see a wrong runbook. That same map had 24 closed tickets, every one gated
on `tsc` / `dotnet build` / a route diff, and the first session to open a browser
found the demo script wrong in six ways — a branch that had never existed, the
wrong repo count, and every nav-item count off by one.

### When a CLOSED ticket's recorded fact turns out to be false

You will find these — a later session runs what an earlier one only reasoned
about. Do **not** re-`resolve` the old ticket to overwrite its gist: the
resolution is the audit trail of what was verified *then*, and its numbers are
usually correct for the ref they were taken on. Instead:

1. `comment` the correction onto that ticket, naming both the old claim's true
   scope and the new measurement.
2. Amend the **canonical doc** the gist links (the ADR) with a dated amendment
   that *scopes* the original rather than deleting it.
3. Carry the correction in **your** ticket's resolution too, so the map's newest
   entry holds the truth.

Overwriting the old gist loses the fact that the claim was ever believed, which
is precisely what explains how the downstream work went wrong.

## Step 5 — Graduate the fog (through the same gate as charting)

Now ask what the answer changed:

- Did it make a "Not yet specified" line sharp enough to **state as a
  question**? That fog graduates into a ticket. (Can you only gesture at it
  still? Then it stays fog — do not pre-slice fog into ticket-sized pieces.)
- Did it put something **past the destination**? Close that ticket and add one
  line under "Out of scope".
- Did it reveal a new blocking relationship?
- Did it sharpen the **milestone** plan — a group that should now exist, or a
  ticket that clearly belongs in one that already does?

Graduating fog is an **additive `chart`** — one operation serves both acts, so
there is no separate subcommand (ADR 0057). Build a `map_input.json` in your
scratch working directory containing **only the new tickets**, plus, for an
edge onto a ticket that already exists, that edge in the new ticket's `blocks`:

```json
{
  "target": { "slug": "<the existing map's slug>" },
  "map": {
    "title": "<unchanged>", "destination": "<unchanged>",
    "notes": ["<any NEW note line>"],
    "notYetSpecified": ["<any NEW fog line>"],
    "outOfScope": ["<anything newly ruled out>"],
    "milestones": [
      { "slug": "<a NEW group, or one already on the map>", "label": "<optional>",
        "members": ["relevance-metric"] }
    ]
  },
  "tickets": [
    { "key": "relevance-metric", "title": "Relevance metric - what do we measure against?",
      "type": "grilling", "question": "<the decision this resolves>",
      "blocks": ["rollout-order"] }
  ]
}
```

- Repeat `title` / `destination` **unchanged**. An additive run does
  not apply a differing scalar — it reports it under `divergence` and leaves it
  alone. To change one, edit the map document by hand.
- `notes` is **not** one of those any more (ADR 0101): on any map carrying the
  notes region it is a list that unions exactly like `notYetSpecified`, so pass
  **only new lines** and omit the key when there are none. Do not restate what
  is already there in any other shape — a string holding the existing notes
  joined together, or the rendered bullets pasted back, is a *new* line to the
  union, so it is appended and there is no `divergence` to catch it. Repeating
  the exact same list is a harmless no-op, but there is no reason to.
- `milestones` is the same optional field chart-map's Step 3 fills in — a
  resolution can sharpen the plan just as easily as a fog line, so include it
  here whenever the answer named a group that should now exist, or made clear
  which milestone a ticket belongs in. A brand-new group appears in the plan
  as `adds 1 milestone line`; a ticket joining one that already exists as
  `adds 1 ticket to an existing milestone`, which is worded differently
  because that one **edits** the stored milestone line instead of adding a
  line. **Moving** a ticket between milestones is different:
  additive means union, never move, so `chart` reports a member already
  claimed by a different milestone under `divergence` rather than applying
  it. A move is a **hand edit** of the milestones region instead — the same
  shape as deleting a graduated fog line, below — with `lint` as the check
  afterwards.
- `blocks` is **downstream** — the tickets this one holds up. Readers see the
  upstream `blockedBy`. An edge may name a ticket that already exists without
  re-listing it in `tickets[]` (ADR 0058), but the target must exist **either in
  this input or already on the map**: naming one that exists in neither is a
  validation error, and the run exits `2` naming the ticket and the bad target.
- Keys are lowercase-kebab, must match `[A-Za-z0-9][A-Za-z0-9_-]*`, and **must
  not contain `--`**.

### The create-class gate (never skip it)

**1. Dry run.** `chart` is dry-run by default; `--real` is what writes.

```
python "<ops>" chart --input <workdir>/map_input.json
```

The plan lands twice: JSON on **stdout**, a human rendering on **stderr**. Show
the user the stderr rendering.

**2. Read the labels — they are what the user is approving.**

| Action | What it means for that item |
|---|---|
| `create` | it does not exist yet and will be created |
| `skip (exists)` | it exists and **nothing** will be written to it |
| `merge` | it exists and will be modified **in place, additively** — the map body gaining fog / out-of-scope lines, or a ticket gaining one `blockedBy` entry |
| `OVERWRITE` | `--force` only: it exists and will be fully rewritten, discarding its recorded state |

A graduation run should read almost entirely `create` (the new tickets) and
`merge` (the map body, and any existing ticket gaining an edge). Every `merge`
names what it adds in its `detail` — `adds 2 fog lines, 1 out-of-scope line` on
the map body, `unions blockedBy: <key>` on a ticket — so read those out. There
is a third shape: `normalises the map body's list regions (no new lines)`, a
rewrite that adds nothing. Expect it on the run *after* you delete a graduated
fog line by hand and the region is left empty — the run is restoring the
tool-owned `- (none)` placeholder, nothing more. **A
`merge` on an existing ticket adds exactly one `blockedBy` entry and changes
nothing else**: its status, assignee, gist and resolution block are untouched
(ADR 0058). If you see an `OVERWRITE` line and did not deliberately pass
`--force`, stop and investigate.

**Re-read the map before you approve — the Step 1 snapshot is stale.** `read`
and `frontier` describe the map as it was when you ran them, and a parallel
session can create tickets, resolve them or comment *after* that. On GitHub the
tell is cheap: issue numbers are sequential, so a ticket numbered higher than
the highest you saw in Step 1 was written by someone else while you worked.
Re-run `read` immediately before `--real` and diff the ticket list against your
Step 1 copy. If something new appeared, check whether your graduation duplicates
it BEFORE creating — `lint` reports the map clean either way. Seen 2026-08-10 on
`claude-model-router`: `gate-rearm-scope` (#17) and `effort-ratchet-persistence`
(#18) are the same question, charted 8 minutes apart by two sessions that had
each resolved the same ticket.

**3. Ask for explicit approval. Never create without it.** The approval is for
the plan you just showed — if the input changes at all, re-run the dry run.

**Carry the end-of-session commit offer in this same ask, on local.** In the
same message, ask whether to commit `docs/decision-map/<slug>/` and any repo
docs this session produced, once the session ends -- so the session pauses once,
here, instead of twice. This does not weaken assisted git: a bundled offer is
still an explicit offer the user answers, and nothing is committed without that
yes. On GitHub there is nothing to commit for the map itself, but any repo docs
still need the same ask.

**4. On approval, re-run with `--real`:**

```
python "<ops>" chart --input <workdir>/map_input.json --output <workdir>/map.json --real
```

**5. Check `divergence` in the result** and report every line. The fix is a
hand edit of the map document, never `--force`.

**`--force` is never the remedy here.** It discards recorded resolutions,
claims and blocking edges on everything it rewrites — on a map you are working,
that is the session history you just wrote. Additive `chart` already adds
tickets, edges, fog lines and scope lines; nothing in graduation needs
`--force`. Its exact blast radius is tabulated in
`references/data-contracts.md`.

**Two things the gate will not do for you:**

- **The graduated fog line is not removed.** Union never deletes, so the line
  you just turned into a ticket is still sitting under "Not yet specified".
  Delete it by hand from between the `decision-map:fog` marker comments in
  the map document, leaving the markers themselves alone — otherwise the map keeps
  advertising fog that is now a real ticket.
- **An edge between two tickets that both already exist needs no create at
  all.** That is `block`, a lifecycle write with no gate:

```
python "<ops>" block --map <slug> --ticket <blocked-key> --blocked-by <blocker-key>
```

Then re-run `frontier --map <slug>` and show the result. A graduated ticket
that blocks an existing one pushes that ticket off the frontier into `blocked`
— seeing that happen is how you know the edge was actually wired.

## Step 6 — Stop

**The cap counts HITL tickets: one per session** (ADR 0041). Grilling and
prototype tickets are always HITL, and so is any task ticket that needed the
user. **Research is AFK and does not count** — subagents run in parallel, so
dispatching several and recording their findings is one session's work whether
they were fired at chart time or picked up here. The line is the user's
attention, not the ticket count: the moment a ticket needs their judgement, that
is this session's one, and you stop after it. If the ticket you claimed turned
out to be research that resolved without them, you may go back to Step 1 and
take one more.

The pull to do "just one more" past that line is not stamina, it is a
**signal** — name it out loud rather than acting on it. Either the frontier is
genuinely small and the map is nearly done, or this session is overreaching and
the next decision deserves a fresh, un-anchored session. The cap is what keeps
the map, rather than a long conversation, holding the state.

**If the user directs work past the cap, the claim discipline does not lapse.**
The cap is theirs to override -- a deadline, a follow-on they want now -- and
their instruction wins; do not argue it. What must NOT lapse is Step 2: every
additional ticket you touch gets **claimed before you implement it**, and
**resolved before the session ends**. Working on past the cap *without* claiming
is the worst of both -- past the attention budget AND off the map, so the code
lands in git while the reasoning that produced it does not. Seen 2026-08-02: after
resolving one ticket the session drove two more (`frontend-relocation`,
`monorepo-import-api`) to completion, unclaimed and unrecorded, and only the user
asking "which ticket are we on?" surfaced it. The tell is cheap -- if you cannot
name the ticket you are on, you are off the map.

**Run the check before you report** (ADR 0067). `lint` reads the map as it now
stands and writes nothing — exit `0` clean, exit `3` with findings:

```
python "<ops>" lint --map <slug>
```

It catches what a session most plausibly just broke: the graduated fog line
Step 5 told you to delete by hand, an edge left dangling by a hand-edited
`assignee:`, a resolution recorded without its diagram, or a milestone move
gone wrong — a line the hand edit left unparsable, a slug declared more than
once, a ticket key listed more than once (in two milestones, or twice on one
line), or a milestone naming a ticket that is not
on this map (`milestone-line-unparsable`, `milestone-duplicate-slug`,
`milestone-duplicate-member`, `milestone-unknown-ticket` — the same four
rules a mistyped hand-edited move above can trip). Report every finding
alongside the rest of the report, and fix the **errors** before you stop; a
warning is the user's call. Do not skip it because the session felt clean —
"felt clean" is the only signal you have otherwise, and it is the one `lint`
exists to replace.

Re-run the frontier so the report describes the map as it now stands, not as it
looked when the session opened:

```
python "<ops>" frontier --map <slug>
```

**And re-read the fog region of the map document** — `frontier` does not carry it, and
the copy you read in Step 1 is stale the moment Step 5 runs: the gate's merge
appended any new fog lines and your hand edit removed the graduated one.
Reporting the Step 1 copy tells the user the map still asks a question they just
answered.

Report, in this order:

- **any `lint` finding**, errors first — and say explicitly when it came back
  clean, so the user knows the check ran;
- the ticket you resolved, **by name**, with its gist and the link if there is
  one;
- what that released — the tickets that moved onto the frontier;
- what graduated out of the fog, and anything newly out of scope;
- the frontier for next time, **by name**;
- the fog lines still unspecified.

Same discipline as the Step 1 frontier: one line per bullet, no filler, around
ten lines in total -- group rather than itemize when a bullet would otherwise run
to a list of its own.

Offer to commit any repo docs the resolution produced — an ADR written during a
grilling ticket is exactly the file that gets orphaned when only the map is
committed — **plus, on local, `docs/decision-map/<slug>/` itself**. On GitHub the
map needs no commit (it is already live in the tracker), but the repo docs still
do, and that is the half most easily forgotten when the map is not a file.
Assisted git: offer, never automatic. If the Step 5 gate already carried this
offer and the user approved it there, commit now without asking a second time --
the yes you are holding *is* that explicit offer, answered. If there was no
graduation this session, no gate ran and no offer rode along with it, so this is
the ask, exactly as before.

Then suggest `/decision-map:work` for the next session, and stop.

### When the frontier came back empty

Three different situations, and they need different answers:

- **Nothing open and no fog left** — the map is done. Say the way is clear, and
  hand off to `sp-writing-plans` (or whatever the destination line
  named). decision-map plans; it does not build.
- **Nothing open but fog remains** — this session's work is **graduation, and
  it happens here**. Do not send the user to `/decision-map:chart`: that skill
  charts a map that does not exist yet, and this one does. Take the sharpest fog
  line, grill it just far enough to *state* it as a question, and run Step 5's
  gate on it — the gate is the same additive `chart` whether or not a resolution
  came before it, and a session that opens a map, finds nothing takeable and
  graduates one fog line into a real ticket has done exactly one session's work.
  If nothing sharpens, say so and stop: fog that will not state itself is
  waiting on a decision that has not been made yet.
- **Everything left is blocked or claimed** — another session is holding the
  unblocked work, or a blocker is still open under someone else's claim.
  Nothing to pick up; say who holds what and stop. If a `claimed` ticket looks
  abandoned, releasing it is the hand edit in Step 2, and it is the user's call.
