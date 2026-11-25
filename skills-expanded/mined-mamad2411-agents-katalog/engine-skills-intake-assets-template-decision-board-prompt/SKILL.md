# Decision Board Handoff Prompt — scaffold

The orchestrator fills this to dispatch the **Decision Board** render subagent at Outcomes (Phase 5). The board is the wave's **interactive decision surface**: it presents the trusted triage findings + the decisions to make, and collects steering answers/votes via widgets that copy a clean JSON payload back.

**This template IS the repeatability contract** (`¶INV_BOARD_HANDOFF_IS_FIXED_PRESENTATION_IS_FREE`): it pins **WHAT every wave must surface** and the **three mechanical contracts that cannot drift** (embed the widget kit; emit the payload schema; render panel marks as the kit reads them). **HOW it looks is the render agent's creative call** (load `Skill(artifact-design)`).

**The handoff is structured but NON-LOSSY** (`¶INV_HANDOFF_STRUCTURED_NOT_LOSSY`): each finding is a fixed-field envelope, but the FULL triage reports + working doc travel with it (pointers below), and the agent **presents from the full sources, not a digest**. The orchestrator organizes + points; it never compresses facts away.

**Trust the curation** (`¶INV_BOARD_TRUSTS_ORCHESTRATOR_CURATION`): the questions/options below were surfaced by the orchestrator. Present them faithfully; do NOT re-investigate whether they are the right questions — that is the wave's job, taken as given. Your only verification is presentational: real evidence, faithful captions, honest provenance (`¶INV_PROVE_FAITHFUL_PRESENTATION`).

Save the filled prompt to `builds/<wave-slug>-decision-board-handoff.md`; dispatch. The subagent writes `builds/<wave-slug>_DECISION_BOARD.html`; the orchestrator runs the integrity pass + publishes.

---

## Fill this

**Wave**
- **Project + domain goal**: […] · **Wave slug** `<wave-slug>` · **Wave** `<project> wave <n>`
- **Directions + Ticketing Strategy in force** (verbatim): […]
- **The wave ranking** (`¶INV_RANKING_WITH_PROOFS`): the ordered "pull first, and why" list — carry the **number behind each call** (blast-radius / corroboration / consolidation breadth) with its proof-pointers.

**Full sources that travel with this handoff** (present FROM these — pointers, not digests)
- **Triage reports**: `builds/inbox-triage-<id>.md` … (one per triaged item — the render agent reads them for the facts)
- **Working doc**: `INTAKE.md` `<path>` (the cross-scope understanding, root-cause map, dependency graph)
- **Origin comments / entity links**: […app URLs + FIN-keys + comment deep-links per item]

**The findings to decide — one envelope per finding** (fixed fields; content stays rich)
For EACH decision-open finding:
- **`id`**: `<origin-comment-id | FIN-key | op-id>` (this becomes `data-fb-item`)
- **Problem** (crisp, one sentence) + **the number behind the call** (its blast-radius / corroboration evidence)
- **Priority / rank** (from the wave ranking)
- **The steering read** (from triage, FULL — legitimacy/confidence + still-open questions + what-to-measure-next; `¶INV_STEERING_NOT_SOLUTIONS` — options to react to, not manufactured solutions)
- **The options to offer** (orchestrator-polished from triage's suggestions): 3–5 `{key, label}` — e.g. `{needs-research, "Needs more research"}` · `{seems-like-a-ticket, "Seems like a ticket"}` · `{fold-into:FIN-1234, "Fold into FIN-1234"}` · `{measure:extraction-count, "Measure the extraction-failure count first"}`. Keys are stable machine ids (the payload carries keys, never labels).
- **Evidence pointers**: the triage report path + origin comment + entity app-URLs (render the real evidence — DB counts, screenshots, quoted log lines — never prose where you could show the artifact).
- **Provenance**: `trusted-upstream` (the triage verdict) vs `checked-here` (something confirmed for the presentation).
- **`also_worth_surfacing`** (overflow): anything that doesn't fit a field above — never drop it for lack of a slot.

**The consolidation ops to decide** (each an approve/reject widget)
For EACH proposed merge / supersede / connect / milestone-move: the op + **its reasoning** + **the evidence the destination already owns the problem** + the affected FIN-keys. `id` = op id.

**Carry the destination's own premise, not a one-line summary of it.** A merge is the highest-stakes operation on this board and the one a human confirm demonstrably fails to audit — the human confirms the *action*, not the *reasoning* behind it. Anyone ruling on it (a teammate, or a panel expert who cannot open the ticket) needs enough to actually judge: what the destination ticket claims the problem IS, and why this item is a facet of that rather than a neighbour of it. Prefer **under-merging to one wrong merge** — two tickets that should have been one costs a little duplication; one merge that buries a real problem costs the system's credibility, and those are not symmetric.

**The stray tickets to adopt/cancel** (each an adopt-or-cancel widget; `¶INV_ADOPT_OR_CANCEL_STRAYS`)
For EACH stray (a non-Inbox ticket lacking wave-provenance): the ticket + its triage finding + the **candidate target milestone** (for adopt) + the **cancel rationale** (if the recommendation is cancel). `id` = FIN-key.

**The panel's votes** (only when a `/council` poll ran this wave — omit the whole block otherwise)
The council run's `votes[]` verbatim, plus the run's `rosterVersion` and `report_path`. Per vote: `item` · `key` · `lens` · `icon` · `weight` (1–5) · `why` · `alternative` · `thinGrounds`. Render these as panel marks per Mechanical contract 3 — **one mark per expert, never an aggregate**. Hand them over unedited: the render agent presents the panel's read, it does not summarise, average, or filter it, and an expert that flagged thin grounds must still appear as having done so.

**The dependency / root-cause graph**
The problem map to render as a diagram (nodes = problems/solutions; edges = stands-on / blocked-by / unlocks). Source: `INTAKE.md`'s dependency graph. Real nodes only.

---

## Mechanical contracts (these cannot drift — the kit reference, the payload, and the panel-mark markup are fixed)

**1. Reference the shared widget kit — do NOT inline it.** Write exactly these two lines, with the token verbatim:
- `<link rel="stylesheet" href="__FB_KIT_BASE__/board-widgets.v2.css">` (in `<head>`)
- `<script src="__FB_KIT_BASE__/board-widgets.v2.js"></script>` (at end of body)

`__FB_KIT_BASE__` is substituted by `publish-s3.sh` at publish time, when the bucket, region and prefix are all known — do not compute a URL yourself, and do not inline the files as a "safer" fallback. **An unpublished board is meant to look broken**: the unresolved token is the signal, and a plausible-looking wrong URL would not be.

*Why this is not inlining any more, since it reads like a regression:* an inlined kit meant a published board carried the kit it was built with **forever** and could never receive a fix. The kit now lives at one versioned address (`publish-kit.sh`), so republishing it reaches every board pointing at that major. The version tracks the payload version the kit emits, so a breaking payload change mints v3 at a new key and leaves v2 boards working.

**The trade, stated so nobody reverses it by accident**: a board is no longer a single file that works anywhere. It works **from the S3 host**. Opened from disk it renders and does not function. That was accepted deliberately in exchange for updatability.

**2. Widget markup** — wire each decision with `data-fb-*` attributes; the kit reads them and emits the payload in `PAYLOAD_SCHEMA.md`:
- Board metadata (once, e.g. on `<body>`): `data-fb-board="<wave-slug>" data-fb-wave="<project> wave <n>"`
- A steering widget (multi-select): a container `data-fb-item="<id>" data-fb-kind="steer"`, with one option row per choice and an optional `<textarea class="fb-note" data-fb-note>`. **Every option carries a one-line description** — the option keys are terse machine ids and the labels are short, so a picker with labels alone is a picker that gets guessed at. Put the *why-you'd-pick-this* on the row, not in a tooltip:
  ```html
  <label class="fb-opt">
    <input type="checkbox" data-fb-key="do-it-now">
    <span class="fb-opt-body">
      <span class="fb-opt-label">Do it now</span>
      <span class="fb-opt-desc">The four numbers are one query; every wave that runs first turns the baseline into a reconstruction.</span>
    </span>
    <span class="fb-panel"><!-- panel marks, if any --></span>
  </label>
  ```
  The description is the orchestrator's, drawn from the triage steering read — not invented by the render agent (`¶INV_BOARD_TRUSTS_ORCHESTRATOR_CURATION`). If the handoff gave an option no description, render the label alone rather than writing one.
- A consolidation widget: `data-fb-item="<op-id>" data-fb-kind="consolidation"` with two radios `<input type="radio" name="<op-id>" data-fb-key="approve">` / `data-fb-key="reject"`.
- An adopt-cancel widget: `data-fb-item="<FIN-key>" data-fb-kind="adopt-cancel"` with radios `data-fb-key="adopt"` / `data-fb-key="cancel"`, a `<select data-fb-field="milestone">…</select>` (adopt target), and `<input data-fb-field="reason">` (cancel reason).
- A copy bar (or let the kit auto-inject one): a `<button data-fb-copy>Copy answers</button>`, a `<input data-fb-voter>` for the voter name, a `<span data-fb-copied></span>`, and a `<pre data-fb-payload></pre>` (the always-visible payload, so copy works even if the clipboard API is blocked).

**3. Panel marks** (only when the orchestrator's handoff carries panel votes — omit entirely otherwise). One mark per expert per option, rendered **directly on the option picker**, never collapsed behind a control and never in a separate block. Each mark is a **focusable control** (`<button type="button">`), not a `<span>`:
- `data-fb-panel="<item-id>"` `data-fb-panel-key="<option-key>"` `data-fb-panel-lens="<persona name>"` `data-fb-panel-icon="<persona icon>"` `data-fb-panel-kind="<itemKind>"` `data-fb-panel-weight="1..5"` `data-fb-panel-why="<one line>"` `data-fb-panel-alt="<alternative, may be empty>"` `data-fb-panel-thin="true|false"`.
- Board-level, once: `data-fb-panel-roster="<rosterVersion>"` `data-fb-panel-report="<report path>"`.
- The mark's visible content is the **persona icon**; classes `fb-mark fb-mark-council` inside a `fb-markwrap`, with the expert's `why` in a sibling `.fb-mark-note`. The kit toggles `data-fb-panel-open` on click; the CSS also reveals on `:hover` and `:focus-visible`.
- **Marks are position-independent** — the item id lives on the attribute, so place them wherever the layout wants. But *always visible on the picker* is a decided constraint, not a preference: a reader must see the panel's read at the moment they choose.
- **Never render a count.** One mark per expert. An aggregate flattens a 3–2 split into "3 for this one" and hides the more informative outcome.
- **Never give a panel mark the same visual weight as a human's.** Icons are the council namespace; initials (`fb-mark-human`) are the human one. They must be distinguishable at a glance and by form, not by shade.

Design the widgets to look like whatever fits your layout — the kit only reads the `data-fb-*` attributes.

**Restyling: override the `--fb-*` variables, don't fight the kit.** The kit owns what must *work* (geometry, hit targets, focus, reachability, and the states that carry meaning — checked, conviction, thin-grounds); you own what must look *good*. The seam is a set of custom properties on `:root` — `--fb-fg`, `--fb-muted`, `--fb-border`, `--fb-surface`, `--fb-accent`, `--fb-council`, `--fb-human`, `--fb-note-bg`, `--fb-radius`, `--fb-shadow`, `--fb-mark-size` — each with a light and dark default. Override them in your `<style>` to restyle the whole widget set coherently. You may also override kit rules outright, but **do not remove** the reachability behaviours (focus reveal, click toggle) or the state distinctions: those are the parts a reader depends on, not decoration.

## Presentation (yours — load `Skill(artifact-design)`)
- **Required coverage** (present all, in whatever structure reads best): thesis line · `/prove` scope block (*evidence shows / out of scope / **rests on trusted upstream triage***) · **a "where the signals came from & how" provenance section** (per-channel counts of what drained this wave, how items were drained + triaged, the Directions in force) · ranked candidates each with the number behind the call + its steering widget · consolidation ops as approve/reject with reasoning + evidence · stray adopt/cancel widgets · the dependency graph · a closing "nothing is executed — these are decisions" note (`¶INV_INTAKE_DISPATCHES_NEVER_EXECUTES`). **When the handoff carries panel votes, also required**: a **legend** naming each seated expert's icon and lens, stating plainly that this is an AI panel's advisory read — one layer further from authority than a teammate's vote — and telling the reader that hovering, focusing or tapping a mark shows that expert's reasoning. A mark whose reasoning a reader cannot reach is a judgement delivered at a decision point with its audit trail hidden, which is worse than showing no panel at all; the reachability is not a nicety to trade away for a tidier layout.
- **Same-origin only**, theme-aware (light+dark), responsive. Honest `<title>` + favicon. The kit arrives from the board's own host (contract 1); **everything else stays inline** — no CDN, no external font, no remote image, no fetch. The property being preserved is *no cross-origin request*, which is what the integrity pass verifies; "one file" was the old means to it, not the goal.

## Optional sections — a palette the ORCHESTRATOR picks from when filling this handoff
Deciding *what to surface* is a curation call the orchestrator owns (`¶INV_BOARD_TRUSTS_ORCHESTRATOR_CURATION`); the render agent is free in *how to present*, never in *whether to include*. So **you (the orchestrator), when you fill this handoff, name which of the sections below to include for THIS wave** — drawn from the real working-doc / triage data — and hand the agent that selected set. The agent then renders the required coverage **plus your selected optional sections**, and does NOT add or drop sections on its own. Omit a section by not selecting it — never leave the inclusion call to the render pass, or a Contested / One-way-doors section can be silently dropped with the integrity pass none the wiser. (The required coverage above always appears; these are additive.)
- **Numbers at a glance** — a stat strip: ingested · triaged · ripe · filed-candidates · merges · strays · total blast-radius (orgs/claims/users).
- **What changed since last wave** — new signal vs carried-over items, re-opened (un-resolved) threads, and any `## Directions` / Ticketing-Strategy change that re-opens prior judgments.
- **Contested / needs-alignment** — items where triage disagreed with the reporter, corroboration is split, or a `not-a-problem` call is doubtful. The ones that most need a human (and the vote).
- **Quick wins** — low-effort / high-leverage items to pull first (the 20/80 node), called out from the ranking.
- **Blocked / waiting-on** — items blocked on a decision or an external answer; name **who to ask** (from the project's `## Stakeholders`).
- **Stakeholder callouts** — per-item "who should weigh in", so the right person votes rather than the loudest.
- **Cross-cutting themes** — the root-cause clusters behind the dependency graph, if the graph alone doesn't make them legible.
- **Aging / staleness** — items marinating across several waves, nomination-rejections, rot made visible (honest, not just flattering volume).
- **Open questions for the room** — the still-unresolved questions triage surfaced, framed for discussion (pairs with the steering widgets).
- **Risk / one-way doors** — decisions that are hard to reverse (a cancel, a merge that loses a framing) flagged before they're confirmed.
- **What we're NOT doing** — explicit non-goals / out-of-scope-per-Directions parked items, surfaced so they're visible, not silently dropped.
- **Confidence & provenance legend** — a key for `trusted-upstream` vs `checked-here` and `[DB-confirmed]`/`[inferred]`/`[needs-source]`, if the board leans on those tags.

## Output contract
- WRITE the HTML to `builds/<wave-slug>_DECISION_BOARD.html` with the `__FB_KIT_BASE__` token **unresolved** — publish substitutes it. Leaving the composed file as authored is deliberate: a re-publish to a different bucket then resolves afresh instead of inheriting the first one's URL. Notebook-log every ~5 tool calls via `engine log <session log path>`.
- RETURN a tight manifest: decisions surfaced (N candidates · M consolidations · K strays), the provenance counts (trusted-upstream / checked-here), any asset that failed, and the HTML path. Do NOT dump the HTML/base64.

## Integrity pass + publish (orchestrator, after the subagent returns)
- **Integrity pass** (`¶INV_PROVE_FAITHFUL_PRESENTATION`): open the load-bearing renders yourself; confirm captions match assets, nothing oversells, provenance is honest, the scope block is unburied, **the kit reference resolves same-origin to the published versioned object and the board issues no cross-origin request** (this replaces the old "everything is inline, therefore nothing is fetched" reasoning — the property is unchanged, what you verify is not), and every widget's `data-fb-key` matches the option keys you authored (so the payload tallies correctly). **When a panel ran, also check**: every `data-fb-panel-key` matches an option key you authored (a mark on a key that doesn't exist is a vote for nothing); the mark count equals the vote count you handed over (no expert silently dropped, none invented); every mark is focusable and its `why` reachable without hover; and the legend is present. Then open the board and confirm the panel's marks read as **advisory** rather than as a verdict — that judgement is yours and no attribute check can make it. Direct a targeted edit if anything is off.
- **Publish the kit first, then the board**: `~/.claude/engine/skills/prove/assets/publish-kit.sh` (idempotent — it republishes the same versioned key, which is how a fix reaches existing boards), then `~/.claude/engine/skills/prove/assets/publish-s3.sh builds/<wave-slug>_DECISION_BOARD.html <wave-slug>-decisions` → capture the public URL. Order matters on a first publish: a board pointing at a kit that isn't there yet is a board with no behaviour.
- **Then open the published URL and confirm the widgets actually respond.** The kit is no longer inside the file, so "the HTML looks right" no longer implies it works — that inference was free under inlining and is not any more. Check a checkbox and watch the payload box populate; if the kit 404'd, this is the only place it shows. The Decision Board is **offered** (default yes), not silent. If `PROVE_S3_BUCKET` is unset, keep the `builds/` file + poke the user; never fabricate a URL.
