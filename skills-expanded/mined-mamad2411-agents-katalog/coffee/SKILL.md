---
name: coffee
preferred_activation: coffee
requires: [handoff-check]
description: "Grace-Mar operator cadence and tempo. Primary trigger: coffee. Step 2 = hub A–E only (Steward / Engineer / Historian / Capitalist / Conductor). Standalone Conductor (master name or conductor skill) remains separate from the hub list. Before Step 1, Recent rhythm. Signing-off: same A–E menu; closeout in Step 1. Coffee also acts as the default checkpointed re-entry ritual."
---

# Coffee

**Preferred activation (operator):** say **`coffee`**. Legacy **`hey`** still works as a compatibility alias, but **`coffee`** is the canonical trigger now.

**Signing-off intent** (end of session, wrapping the day, stepping away) uses the **same** **`coffee`** trigger and the **same** **A, B, C, D, E** hub menu. There is **no** separate closeout branch or closeout-only menu item. **Step 1** switches to handoff-weighted output when intent is signing off; **Step 2** is unchanged.

`coffee` is not a startup ceremony. `coffee` is a **repeatable sip of coherence**.

Its purpose is to help the operator become more awake to the actual situation, more coherent about priorities, and more directed about the next move. A coffee session does not need to complete the day's thinking. It only needs to improve orientation enough that action becomes easier.

Multiple `coffee` sessions per day are normal. That is not redundancy; it is the point. Each `coffee` is another sip.

`coffee` is also the default checkpointed re-entry ritual. In a fresh chat, it should resume from the most recent authoritative grace-mar checkpoint on disk, using cadence and handoff state to recover orientation. If more than one plausible checkpoint exists, prefer the latest on-disk authority and surface the ambiguity instead of guessing. This is a checkpoint, not a transfer seal: it restores continuity, but it does not commit, push, or generate a bridge packet.

**Coffee Hub Menu (terminology):** **`coffee` Step 2** fixed **A–E** hub (**Steward / Engineer / Historian / Capitalist / Conductor**) is the **Coffee Hub Menu**. When routing continues into **Conductor**, resolution uses the **Master Selection Menu** (masters **A.–E.** — Toscanini … Bernstein) and then typically the **Conductor Action Menu** (three repo-grounded next moves — [CONDUCTOR-PASS — Conductor action MCQ](../../../docs/skill-work/work-coffee/CONDUCTOR-PASS.md#conductor-action-mcq)). Layer map: [CONDUCTOR-LAYER-MAP.md](../../../docs/skill-work/work-coffee/CONDUCTOR-LAYER-MAP.md).

## Guardrails

- Do not turn `coffee` into a heavy maintenance ritual by default.
- Do not overload each run with every possible obligation or stale thread.
- Prefer a small number of salient next paths over exhaustive review.
- Keep the operator in the position of renewed agency, not procedural burden.
- `coffee` is for orientation; heavier consolidation belongs to `dream`.
- This is read-only planning. Do not merge or stage just because the warmup mentions candidates.
- If integrity fails, surface that before optional improvements.
- **Contextual stewardship:** Agents have no cross-thread institutional memory; authority for the Record is **on-disk files + gated pipeline** — not model recall or chat summary.

## Relation to dream

`coffee` and `dream` form a biological-cognitive pair:
- **`coffee`** = repeated framing dose (many per day)
- **`dream`** = end-of-day consolidation pass (usually once)

`coffee` should feel like a sip. `dream` should feel like sleep. See `.cursor/skills/dream/SKILL.md` § *Cadence choreography* for the day's sequence and data handoff.

<a id="conductor-only-no-coffee"></a>

## Conductor session (outside `coffee` hub menu)

Use this path when the operator wants **Conductor** **without** going through **`coffee` Step 2 hub letter E**.

The **five masters** (**Toscanini**, **Furtwängler**, **Karajan**, **Kleiber**, **Bernstein**) are **not** listed as separate lines on the **`coffee`** hub — hub **E** is the **single** in-`coffee` slot for **Conductor continuation** after **`coffee`** Step 1. Call masters **directly** (this section) when **`coffee`** was not opened or when the operator prefers **`conductor`** / master name **instead** of **`coffee`**.

**Triggers (examples):** master name or prefix (**`toscanini`**, **`karajan`**, **`bernstein`**, **`kleib`**, …), **`conductor`** with optional fragment, or plain language (**"Bernstein pass"**, **"run Kleiber on the notebook"**). If intent is unclear, ask once. **Legacy:** bare **`D`** + fragment still resolves like a conductor turn when the message is clearly conductor-only (no **`coffee`**).

**First-turn activation note:** bare conductor slugs like **`bernstein`** or **`kleiber`** should route straight into Conductor on the first command, not be treated as ambiguity.

**Do not** run `operator_coffee.py`, **do not** paste work-start or closeout **Step 1** output, and **do not** lead with **Recent rhythm** — unless the same message also says **`coffee`** or **`hey`**.

**Standalone Conductor** (no **`coffee`** in this turn): show **`build_conductor_mcq_for_user('grace-mar')`** when the master is **not** yet disambiguated; resolve via `resolve_d_conductor` + [work-cadence-events.md](../../../docs/skill-work/work-cadence/work-cadence-events.md).

**After `conductor=<slug>` resolves** (standalone pick **or** **`coffee` hub E** auto-continue per [**§ Hub E**](#hub-e-auto-continue)): deliver the **short** orientation in [CONDUCTOR-PASS.md](../../../docs/skill-work/work-coffee/CONDUCTOR-PASS.md) and [COFFEE-CADENCE-CONDUCTOR-PROTOCOL.md](../../../docs/skill-work/work-strategy/strategy-notebook/COFFEE-CADENCE-CONDUCTOR-PROTOCOL.md). **Then, always** deliver the **Conductor action MCQ** — **three** **A-C** repo-grounded next moves — per [CONDUCTOR-PASS — Conductor action MCQ](../../../docs/skill-work/work-coffee/CONDUCTOR-PASS.md#conductor-action-mcq) and [conductor skill](../conductor/SKILL.md). **Skip** the action menu **only** if the operator said **"orientation only"** / **"no action menu"** in the same turn.

**Logging:** `log_cadence_event.py --kind coffee_pick -u grace-mar --ok --kv picked=conductor conductor=<slug>` (e.g. `karajan`, `toscanini`). **Legacy** lines may still use `picked=D`; both are fine for rollups. **`coffee` hub letter E** uses **`picked=E conductor=<slug>`** with **`<slug>`** the resolved conductor (**auto-continued** **or** chosen after Masters MCQ) — see [§ Cadence audit](#cadence-audit). **Do not** append a separate **`coffee`** event unless they actually ran `coffee` Step 1.

**Conductor close (optimal loop):** Same as before — [CONDUCTOR-CLOSE-TEMPLATE.md](../../../docs/skill-work/work-strategy/strategy-notebook/CONDUCTOR-CLOSE-TEMPLATE.md) in **`days.md`** / page **Reflection**, or **`coffee_conductor_outcome`** — [CONDUCTOR-IMPROVEMENT-LOOP.md](../../../docs/skill-work/work-strategy/strategy-notebook/CONDUCTOR-IMPROVEMENT-LOOP.md). For auditability, every new outcome line should carry **`conductor=<slug>`** and **`verdict=`**, plus **`notebook_ref=`** or **`falsify=`** (both preferred). If a pass ended without that line, log a repair outcome on the next turn rather than leaving the close implicit.

**After the reply:** return to **normal workflow** unless the operator says **`stay in coffee`** or **`coffee`**.

<a id="hub-e-auto-continue"></a>

**Hub E (`coffee` Step 2) — automatic continuation:** When the operator chooses **E — Conductor** after **`coffee`** Step 1, **`last_logged_conductor`** from cadence (**`coffee_pick`** with **`conductor=`**) is the **default resolved slug**.

- **If a slug exists:** **Continue that master immediately** — short orientation + **Conductor action MCQ** for that slug. **Do not** paste the **Masters MCQ** (`build_conductor_mcq_for_user`) row **unless** the operator asks to switch masters in the same turn (e.g. master name / prefix, “masters”, “pick a card”, “switch”) **or** cadence has **no** qualifying prior conductor.
- **If no slug exists:** Paste **`build_conductor_mcq_for_user('grace-mar')`** **or** prompt once for master name / **`conductor`** — **do not** invent a default.

Optional **one line** after auto-continue prose: *Say a master name or “masters” to open the five-master row instead.*

**Letter-collision:** If both the **coffee hub** and a **Conductor action MCQ** appear in one reply, **label** them — e.g. **`Coffee hub — Reply A–E`** vs **`Conductor action MCQ — Reply A–C (this pass)`** — and never use bare “pick **E**” without naming which menu ([CONDUCTOR-PASS.md](../../../docs/skill-work/work-coffee/CONDUCTOR-PASS.md)).

---

## "Coffee" = start here (two steps)

When the operator begins with **`coffee`** (or clearly the same intent; legacy **`hey`** still counts), treat it as opening a **coffee session**.

### Step 0 — Recent rhythm (before Step 1 scripts)

**Read first** — `operator_coffee.py` appends a new **`coffee`** line at the **end** of a successful run, so the log must be read **before** those commands if the rhythm read is to exclude this session.

1. Open **`docs/skill-work/work-cadence/work-cadence-events.md`**. Below `_(Append below this line.)_`, collect lines matching `- **YYYY-MM-DD HH:MM UTC** — kind (user) …`.
2. Take the **last 4** such lines already in the file. If there are fewer than four, use what exists; if none, **Recent rhythm:** _(no prior events)_ in the reply.
3. **Synthesize in plain prose** — **2–4 short sentences** for a human, **not** a telemetry dump: **do not** lead with a wall of `key=value` pairs. **Companion-facing UX:** label this block **Recent rhythm** (or prose only); **do not** put **dates, UTC, or clock times** in this prose (use order and light anchors like “after dream,” “then bridge,” “earlier today” without timestamps). **Must anchor in specifics** from those four lines — name what actually happened (e.g. **bridge** with **commit refs** if present, **coffee** **work-start** vs **standard**, **coffee_pick** / **conductor** when present, legacy **`thanks`** **park** text when non-empty, **dream** pass/fail or integrity/governance in ordinary words, **harvest** packet vs not). **Avoid** generic process filler that could apply without reading the file. Do **not** paste raw log lines unless they are already very short.

   **Cadence voice:** Follow the **cadence voice principle** ([work-cadence README](../../../docs/skill-work/work-cadence/README.md#cadence-voice-principle-all-rituals)). Lead with *felt* acknowledgment of what was settled or decided, end with the **optimal next direction**. Use **"we"** framing. The operator should feel **seen, grounded, and ready** — not debriefed. Name what was learned or decided, not what was executed. No commit hashes, no process names — warm, direct, future-facing.
4. In the reply, place **Recent rhythm:** at the **top** of Step 1 content (immediately before script output / warmup paste). Same rule for **signing-off** Step 1 (before `operator_coffee.py --mode closeout` or handoff-only flow).

If the file is missing or empty below the anchor, state that under **Recent rhythm** and continue Step 1.

### Step 1 — Automated actions (one flow, two weights)

**Detect intent**

- **Signing off / closeout / end of session / wrapping the day** → use **closeout-weighted Step 1** below.
- Otherwise → **work-start Step 1** (scale with explicit phrases or weekday cadence).

**Work-start Step 1** — run the consolidated coffee script (preferred):

```bash
python3 scripts/operator_coffee.py -u grace-mar                   # work-start (default)
python3 scripts/operator_coffee.py -u grace-mar --mode light      # lighter pass
python3 scripts/operator_coffee.py -u grace-mar --mode minimal    # compact harness only
python3 scripts/operator_coffee.py -u grace-mar --mode reentry    # cold-thread full stack
```

**Signing-off Step 1** — handoff-weighted (same trigger **`coffee`**, not a second ritual name):

```bash
python3 scripts/operator_coffee.py -u grace-mar --mode closeout
```

Or directly: `python3 scripts/operator_handoff_check.py -u grace-mar`. Include the output in your reply. Add a **short paragraph**: what moved today, what is parked, gate + Jiang carryovers, suggested re-entry prompt. Full spec: [`.cursor/skills/handoff-check/SKILL.md`](../handoff-check/SKILL.md).

If the operator **explicitly** wants **both** full warmup **and** signing-off in one message, run work-start then append handoff (rare).

Add `--compact` for shorter harness output. Individual scripts (`operator_daily_warmup.py`, `harness_warmup.py`, `operator_handoff_check.py`, `operator_reentry_stack.py`) are still available.

**Dream handoff:** If `dream` ran overnight, the daily warmup includes a last-dream block from `users/grace-mar/last-dream.json` (**"Last dream (night handoff)"** when there is something to read out, or a **one-line "quiet handoff"** when `integrity` / `governance` / digest counts are clean and there are no followups). A successful dream may add **`last_coffee_echo`**: a single warm line (from the 24h cadence rollup) that ties yesterday’s `coffee` into morning startup—**cadence / runtime only**, not Record. **Signal days** (issues, followups, or non-zero digests) still use the fuller collapsed block. Extra lines (civ-mem summary, coffee 24h rollup) are **off** by default; tune `config/context_budgets/coffee.json` or pass `--show-civ-mem` / `--show-rollup` on `operator_daily_warmup.py`, `operator_coffee.py`, or `operator_reentry_stack.py`. After that block (or alone if the Last dream section is turned off), warmup prints one line **`Dream → coffee menu:`** mapping dream’s suggested execution path to **A / B / C** (**Steward / Engineer / Historian**) — operational hint only; see [dream/SKILL.md](../dream/SKILL.md) § *Five-second closeout*. Approximate paste footprint: `python3 scripts/audit_context_tax.py -u grace-mar`. These files are operator scaffolding, not Record. For full paths / snippets / followups, use **`--verbose-dream`**. When pasting warmup for the operator, prefer **collapsed** unless they ask for detail.

**Step 1 deliverables (work-start):** Warmup brief (priorities, gate, work-politics snapshot where relevant, integrity), branch snapshot, daily brief + intel defer line (path pattern + **menu C — Historian** when ready), optional PH/Jiang line. **No** Polymarket / poll / Massie blocks in Step 1 unless the operator explicitly asked in the same message.

**Memory observability:** `operator_coffee.py` may print a single **`Memory observability:`** line after lane hints when the derived continuity dashboard is `watch`, `stale`, or `missing`. Do not paste the full dashboard into coffee. If the line is absent, treat memory observability as quiet/ok for this run. The dashboard is WORK-derived only; it does not edit MEMORY, the Record, or the gate.

**Step 1 guardrail:** Stay read-only — no merge/stage unless they switch lanes or use a pipeline phrase ("we …").

**Done when:** Script output is pasted in the reply, Recent rhythm is at the top, and the full coffee menu follows immediately.

For cadence tables and explicit phrase definitions (`coffee light`, `coffee minimal`, `coffee survey`): see [menu-reference.md](../../../docs/skill-work/work-coffee/menu-reference.md).

### Multiple coffees per day

The operator may say **`coffee`** **more than once per calendar day** for reorientation. This is normal. Each new `coffee` runs Step 1 again and starts a new **A, B, C, D, E** cycle. If **`coffee`** arrives mid-hub, treat it as a **reorientation restart**: run Step 1 again, then offer a fresh menu.

<a id="coffee-step-2-hub"></a>

### Step 2 — Hub menu (five lines only)

Immediately **after** Step 1 content, output the **hub** menu — **five lines** (**A–E**).

**One option per line:** Each hub letter is **its own line** — **`A.` … `E.`** as **five separate lines**, not multiple letters on one line and not a single paragraph listing A–E. (Sub-menus inside **D** **Capitalist** forks or **Steward** branches are separate from this rule when you open a follow-up.)

**Letter-collision:** The **Symphony masters** disambiguation row (**masters A.–E.**) and the **Conductor action MCQ** (**three actions A-C** for the resolved slug) use **the same letter range** as the hub. When **both** a **coffee hub** menu and a **Conductor action MCQ** could appear in one reply, **label** them explicitly — see [CONDUCTOR-PASS.md](../../../docs/skill-work/work-coffee/CONDUCTOR-PASS.md). **Do not** reuse bare “pick **E**” without naming which menu.

**Do not** append the **masters** **MCQ** row **under** the five hub lines; masters disambiguation belongs to **Conductor** turns ([§ Conductor session (outside `coffee` hub menu)](#conductor-only-no-coffee), [CONDUCTOR-PASS.md](../../../docs/skill-work/work-coffee/CONDUCTOR-PASS.md)). **After hub E is chosen:** when **`last_logged_conductor`** resolves, **skip** the **Masters MCQ** — deliver orientation + **Conductor action MCQ** immediately ([**§ Hub E — automatic continuation**](#hub-e-auto-continue)).

**Do not** add micro-hints, fork shorthand, or F/G/Xavier/Dev tags **under** the hub list.

**Hub menu (example):**

```
A. Steward
B. Engineer
C. Historian
D. Capitalist — <one short line: work-business / grace-gems / commercial angle / bookshelf product or teaching use>
E. Conductor
```

**Hub line E:** **`E — Conductor`** only — **do not** preview **`last_logged_conductor`** in the hub menu copy. **`operator_coffee.py`** Step 1 prints a script section headed like `Coffee hub Step 2 — hub **E**` whose body is **`format_coffee_hub_e_line`** output (label only). Auto-continue behavior is unchanged ([**§ Hub E — automatic continuation**](#hub-e-auto-continue)).

**Filling D — Capitalist:** **work-business**, **grace-gems**, revenue/offers framing; **work-cici** when business/teaching-commercial; one prescribed next step. Bookshelf belongs here only when the use is **commercial / teaching / product packaging**. **Self-knowledge bookshelf quiz** belongs under **C — Historian**.

**Capitalist — bookshelf / product use:**

- Bookshelf may support offer design, teaching angles, grace-gems packaging, course/product framing, or public copy.
- Do **not** use D as the default route for IX-A bookshelf recursion; route that to **C — Historian → B. Bookshelf quiz**.
- **Catalog stance membrane** (`bookshelf-membrane-round.json` + `build_bookshelf_membrane_candidates.py`) remains secondary and scripted: use it only when the operator requests catalog organization or a pressing organizational membrane issue applies.

**Fixed option (Capitalist angle, hub line wording):** may read **Bookshelf product/teaching angle** or **Bookshelf stance membrane (scripted)** when those commercial or catalog intents are live.

**Catalog stance membrane (scripted path only — branch 2 above):**

- Session is **multi-round**: 5–10 MCQs per round when using the scripted stance round artifact.
- After each round, ask continue/stop.
- On stop, produce:
  - `docs/skill-work/work-strategy/history-notebook/research/BOOKSHELF-MEMBRANE-REPORT.md`
  - `docs/skill-work/work-strategy/history-notebook/research/BOOKSHELF-MEMBRANE-CANDIDATE-DRAFTS.md`
- Output is draft-only; no direct writes to `users/grace-mar/recursion-gate.md` unless explicitly requested.

**Write-shaped** work is **not** an extra letter — it defaults under **D** when skill-write/commercial, or when the operator says **`write`** / **`skill-write`** without **`coffee`**. State it plainly in the angle-bracket line; **do not** add a separate “micro-hints” row.

**Filling E — Conductor:** Hub line is **`E — Conductor`** only (no last-master preview). **When the operator picks hub E:** **[`last_logged_conductor`](#hub-e-auto-continue)** **defaults** the session — **orientation + Conductor action MCQ** for that slug **without** interposing the **Masters MCQ**, unless cadence has **no** prior **`coffee_pick` `conductor=`** **or** the operator asks to switch masters (name / “masters” / “pick a card”). **If no slug:** paste **`build_conductor_mcq_for_user`** **or** prompt once — **do not** invent a default master.

**Step 1 context for B / D:** `operator_coffee.py` prints **`Lane context (for hub B / D — Engineer & Capitalist hints)`** — two lines from `scripts/coffee_lane_next_hints.py` (work-cici + work-dev). Use when choosing **B**, **D**, or when wording those lines.

**Step 1 context for hub E:** After lane hints, **`operator_coffee.py`** prints the script block that includes **`format_coffee_hub_e_line`** output — a single **label** line **`E — Conductor`** for Step 2 (no last-master preview on that line).

**Default recommendation line:** Step 1 may print `Session load: … (recommended: X)` and `Recommended default: X — say "go" to accept, or pick another hub letter.` (**A** / **B** / **C**). When present, surface that recommended default once before or after the hub menu. The fixed hub menu still remains five lines only. For **Conductor** emphasis outside the hub, say **once** that **`conductor`** / master name works **without** opening **`coffee`** ([§ Conductor session](#conductor-only-no-coffee)). **Not** micro-hints under the hub list.

**Quick reference (modes):**

- **A. Steward** — **Governance membrane:** **gate** \| **template/boundary** \| **integrity/exports** \| **git/ship**. **Default if the operator says `A` only:** **gate** if pending candidates; else **template/boundary**. **`A integrity`** / **`A git`** / **`A ship`** → that track; **`A both`** / **`A all`** as in [menu-reference — Steward](../../../docs/skill-work/work-coffee/menu-reference.md#ah-table). Gate merges never without companion **approve** + `process_approved_candidates.py`. *(Legacy hub letter **B**.)*

- **B. Engineer** — **work-dev + skills/meta** (not git/ship or full membrane audits — those are **A**): `docs/skill-work/work-dev/` + [work-dev-sources.md](../../../docs/skill-work/work-dev/work-dev-sources.md); **skills / meta** when **`skills`** / **`meta`** with **B**. **work-cici** ops when engineering-shaped. **When hub B is chosen:** After **one short orientation line**, deliver **Engineer next moves** — **3–5 options** labeled **A through E** (**or A–D** if four), **each option its own line**, under an explicit heading such as **`Engineer menu — reply A–E`** — **not** `B1`–`B5` and not unlabeled lists. Each new submenu **restarts letters from A**; disambiguate from the **Coffee hub** with the menu title (same idea as **letter-collision** labeling for Conductor action MCQ vs hub). Each line is a **repo-grounded** plausible next step (work-dev wedge, script, CI, **skills** path) — **enumeration only** until the operator picks. Use Step 1 **`Lane context (for hub B / D)`** and [workspace.md](../../../docs/skill-work/work-dev/workspace.md) § **Next actions** when helpful. **Detail:** [menu-reference § Engineer (B) — detailed scope](../../../docs/skill-work/work-coffee/menu-reference.md#build-b--detailed-scope) *(legacy letter **Build** / old hub **A**).*

- **C. Historian** — Opens exactly three actionable options and nothing else. Do **not** auto-run the daily brief or auto-offer Tri-Frame before this submenu. Output:
  - `Historian menu — reply A–C`
  - `A. Intel — daily brief / current-events watch`
  - `B. Bookshelf quiz — self-knowledge MCQs → IX-A candidates`
  - `C. Notebook synthesis — History Notebook / Predictive History with Tri-Frame lenses`

  **C-A Intel** owns the daily brief path: generator and/or `daily-brief-YYYY-MM-DD.md`, **§1d** / **§1e** / **§1g** / **§1h** (PRC / IRI when load-bearing), optional **KY-4** (Polymarket, polls, Massie X per cadence), and optional **`last30days` frontier check** when the operator wants one fresh, source-dated scan for today's inbox. Do **not** auto-run `last30days` from coffee Step 1 or merely because C-A is opened; offer or run it only when the operator chooses Intel and the frontier is stale / explicitly requested. Output remains a short brief + optional `daily-strategy-inbox.md` one-liner, not a `days.md` / thread / gate edit. **C-B Bookshelf quiz** uses [.cursor/skills/bookshelf-knowledge-mcq-to-gate/SKILL.md](../bookshelf-knowledge-mcq-to-gate/SKILL.md): default **6** source-bound, topic-anchored MCQs from `bookshelf-quiz-anchors.yaml`, with academic inline citations visible to the operator and hidden `self-library-bookshelf` receipts in the gate, **at most two** date-primary stems, strictness default **top2**, and stage candidates only through `recursion-gate.md`; never merge without approval. **C-C Notebook synthesis** owns History Notebook / Predictive History synthesis; Tri-Frame minds **Barnes → Mearsheimer → Mercouris** live here, using [daily-brief-minds-menu.md](../../../docs/skill-work/work-strategy/daily-brief-minds-menu.md) as the lens menu when useful. **Companion survey** still lives under C when invoked by `coffee survey`. *(Legacy hub **C — Strategy (daily brief)**.)*

- **D. Capitalist** — **work-business**, **grace-gems**, revenue/offers; **work-cici** when business/teaching-commercial angle; bookshelf only for commercial / teaching / product packaging or scripted catalog stance membrane; **not** IX-A bookshelf recursion. **One** prescribed next step.

- **E. Conductor** — **`coffee` hub E** **[auto-continues](#hub-e-auto-continue)** **`last_logged_conductor`** (orientation + **Conductor action MCQ**); hub menu line is **Conductor** only. **Not** a substitute for standalone **`conductor`** when **`coffee`** was not invoked.

**Exit / re-offer:** After **A**, **B**, **D**, or **E**, re-offer the full **coffee** hub **A–E** **after** the **current** branch settles — **except:** when **hub E** yielded **orientation + Conductor action MCQ**, **do not** paste **coffee hub** **A–E** in that **same** reply — wait for **Reply A–C** against **Conductor action MCQ** (**label menus** — [§ Letter-collision](#coffee-step-2-hub)); re-offer **coffee hub** on the following turn (or after Conductor closes) unless the operator exited **`coffee`**. After **C**, **exit** to normal workflow unless **`stay in coffee`**. After **A** (Steward), see [menu-reference § Steward follow-up fork](../../../docs/skill-work/work-coffee/menu-reference.md#steward-follow-up-fork-implement-now-vs-later) *(legacy docs may still say **B** for Steward — read **A**).* Synonyms **`A+ship`** / **`EXECUTE`** ≈ **Implement now** on steward track. **Decision-fatigue rule:** after a hub branch opens one submenu, the next assistant turn should execute the selected item, recommend one default, or report the blocker rather than opening another broad menu.

Legacy **A–G** detail tables in [menu-reference.md](../../../docs/skill-work/work-coffee/menu-reference.md) still describe **workloads**; map letters: old **Daily Brief → C-A Intel**, old **self-knowledge bookshelf quiz → C-B Bookshelf quiz**, old **Book / Jiang / Predictive History → C-C Notebook synthesis**, **Build → B**, **Steward → A**, commercial / teaching bookshelf uses → **D**, and **Symphony conductors → E** on hub after **`coffee`**, or **standalone** **`conductor`** / master name without **`coffee`**.

**Done when:** The operator has picked **A–E** (or combo), the selected branch has been executed, and the re-offer or exit rule has been applied.

---

## Session trail (optional)

Sessions begin when the operator says **`coffee`** (optional modifiers). To keep a trail: use **`users/<id>/session-transcript.md`** and/or append dated bullets to **`docs/skill-work/work-*/*-history.md`**. **Not** the gated Record; **not** `self-memory`. See [work-menu-conventions.md](../../../docs/skill-work/work-menu-conventions.md).

<a id="cadence-audit"></a>

## Cadence audit

Each successful coffee run appends one line to `docs/skill-work/work-cadence/work-cadence-events.md` via `scripts/log_cadence_event.py`. This is automatic — no operator action required. The line always includes **`cursor_model=…`** (audit parity with bridge/harvest **Agent surface**): set **`CURSOR_MODEL`** in the environment, or pass **`--cursor-model "…"`** to `operator_coffee.py`, using the model name from the Cursor UI. If unset, **`unknown`**.

**After the operator states their menu letter** (and steward track if **A**), the assistant may append a **`coffee_pick`** cadence line (same file) for rollup:  
`python3 scripts/log_cadence_event.py --kind coffee_pick -u grace-mar --ok --kv picked=A steward=gate --cursor-model "<from Cursor UI>"`  
(`steward=` only when `picked=A`; values: `gate`, `template`, `integrity`, `git`, `both`, or `all`.) For **hub** picks: **`picked=A`..`E`**. **`picked=E`** should include **`conductor=<slug>`** when the Conductor master is resolved. For **Conductor sessions** outside hub letter picks: **`picked=conductor`** with **`conductor=<single-slug>`** — **no** `+` in new logs. Legacy files may still contain **`picked=D`** + `conductor=` or older shapes. **Optional closure after a conductor run:** `python3 scripts/log_cadence_event.py --kind coffee_conductor_outcome -u grace-mar --ok --kv verdict=watch conductor=kleiber notebook_ref=docs/path.md` (see [CONDUCTOR-IMPROVEMENT-LOOP.md](../../../docs/skill-work/work-strategy/strategy-notebook/CONDUCTOR-IMPROVEMENT-LOOP.md) § 3 for `notebook_ref` / `falsify` examples). Optional: `scripts/log_operator_choice.py --context COFFEE --picked A` for `session-transcript.md`.

## Related files

- `docs/skill-work/work-cadence/README.md` — **Cadence choreography** (ordering, handoffs, Step 0 recent rhythm window depths, harvest vs triad)
- `docs/skill-work/work-coffee/README.md` — territory rationale and boundaries
- `docs/skill-work/work-coffee/menu-reference.md` — cadence, survey track, signing-off add-ons; legacy **A–G** workload tables (map to the current coffee Step 2 above)
- `docs/skill-work/work-coffee/work-coffee-history.md` — lane breadcrumbs
- `docs/skill-work/work-cadence/work-cadence-events.md` — per-run cadence telemetry
- `.cursor/skills/dream/SKILL.md` — night-side counterpart
- `.cursor/skills/thanks/SKILL.md` — **`thanks`** **deprecated** for grace-mar workflow; prefer **conductor** or **`coffee` light/minimal`
- `docs/skill-work/work-politics/polling-and-markets.md` — KY-4 polling (**menu C — Historian** / daily brief)
- `docs/skill-work/work-strategy/daily-brief-minds-menu.md` — Tri-Frame **three minds** (Barnes / Mearsheimer / Mercouris) for **C — Historian** second stage
- `docs/skill-work/work-politics/america-first-ky/guardrail-stress-test.md` — messaging discipline
- `.cursor/skills/bookshelf-knowledge-mcq-to-gate/SKILL.md` — **C — Historian / Bookshelf quiz** MCQs toward IX-A / gate staging
