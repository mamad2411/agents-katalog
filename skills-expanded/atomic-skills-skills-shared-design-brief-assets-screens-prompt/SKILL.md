# Asset — Screens prompt skeleton (consumes the inherited DS)

Skeleton for the **second** prompt: per-screen specs handed to the design agent. It consumes
the **inherited DS** by name and never redefines it. Emit in the output language (pt-BR or the
install-configured language). One screen block per screen in the coverage ledger — **no screen
left out**.

---

## App-shell / navigation contract (emit BEFORE the per-screen blocks)

Brief the app **as a whole** before any single screen. The screens are not islands — each is a
**content-component mounted in the shell container**, and the agent needs the frame before it can
place a screen inside it. Emit:

- **The shell** — the persistent frame every shell-bearing route sits in (the brand/identity
  surface, the global nav, any global actions).
- **The navigation graph** — who leads to whom: the entry points, which screen reaches which,
  the **active nav item per screen**, and the **sub-page / back pattern** (which routes are
  destinations vs. drill-downs that return to a parent).
- **Route classes** — which routes are **pre-login**, which are **focused / shell-less** (a flow
  that intentionally drops the chrome), and which are **shell-bearing**.
- **Per-platform shell** — how the shell differs on **mobile** (e.g. a bottom tab bar) vs.
  **desktop** (e.g. a side rail). Per-platform treatments are **expected and fine**; consistency
  means the **same SYSTEM** (vocabulary / hierarchy / brand), **not the same widget**.

**Core surfaces get nav PARITY.** Do not demote a core destination to a secondary slot just
because it happens to be a verb (an action the product is built around) rather than a noun — a
core is a core in the graph regardless of how the user names it.

## R9 preamble (emit verbatim at the top — in the output language; pt-BR shown, translate if the install language differs)

There are **two distinct authorities**, not one all-binding bucket — the preamble keeps them
apart so layer-2 is never frozen as if it were layer-3:

> Há **duas autoridades distintas** neste briefing — não um carimbo único de "tudo vinculante":
> — **Forma visual** (widget, cor, formato, espaçamento): é **sua** para decidir — não prescrevemos.
> — **Filosofia / o que fica oculto / quem decide** (camada 3): **requisito de produto vinculante**, não negociável.
> — **Comportamento de interação** (camada 2): é a **calibração atual** do app — a **banda comportamental vincula** (ex.: "a cadência é da ordem de segundos"), mas o **valor exato é o que o app faz hoje (~8s), melhorável por você dentro da banda**, nunca um número congelado.
> Consumimos o **Design System existente** pelo nome semântico e nunca o redefinimos. Se uma tela precisa de algo que o DS não tem, **pare e sinalize** — não improvise.

## Per-screen block — the 8 mandatory sections (§4)

For **each** screen, emit all eight; sections 4 and 5 are mandatory whenever the screen has
interaction:

1. **Purpose** — the person's goal on this screen.
2. **Visible information** — what must be on screen, with **real fixtures** (see the
   fixtures recipe). Each screen-state gets a real, **state-aware** set (cardinality + edge
   rows) **pulled from a real source** (the skill's fixtures step, R8) — a few inline examples are **not**
   fixtures. Show the texture: how little (or how much) text there really is at the moment of
   decision.
3. **What the person needs to do** — intents, not widgets.
4. **Interaction model** *(mandatory when interactive)* — describe by behavioural attributes,
   never by widget, with the **concrete values mined from the code (R2)**, expressed as
   **current calibration, not a frozen requirement**: state the **behavioural band that binds**
   (e.g. "pace on the order of seconds") **and** the **exact mined value as the current app's
   calibration** (e.g. ~8s), improvable by the design agent within that band — never the bare
   value as a hard requirement. This holds for **every quantitative value alike — timings,
   counts, lengths**: a count (steps in a flow, items in a list) is the **current shape,
   improvable** ("a first-run explainer of a few steps today"), never a frozen number —
   **unless** a product invariant corroborates it, which routes it to a §5 R6 guardrail, not a
   bare count:
   - *gesture class* (fast / deliberate / typing), *latency* (instant / sub-second /
     deliberate), *effort* (one hand / thumb), *text density* (very short / verbose),
     *timings* (pace in seconds, default timers — as cadence, not raw ms), *counts* (how many levels/items/steps — band-pinned as current calibration, not a frozen number, unless a product invariant corroborates → §5),
     *triggers* (only after X), *reversibility* (forgives an accidental touch),
     *parity* (mobile-gesture ↔ desktop-keyboard, equally fast),
     *navigation density* (how many destinations are reachable in one gesture; whether the set
     is always-visible or invoked on demand — a reach/effort attribute, **never** a nav widget).
   - **Forbidden vocabulary (R4):** never name a widget, a layout container, or a visual-hierarchy
     knob — those are layer-1 form, the design agent's to choose. The ban covers **PT and EN
     synonyms alike**:
     - *widgets / containers:* button/botão, list/lista, tab/aba, bar/barra, card-UI,
       heatmap (mapa / mapa-de-atividade), chip/pílula, modal, badge/selo, sidebar/menu-lateral,
       bottom-nav/navegação-inferior, anchor-nav/âncora, collapsible-nav/recolher-expandir,
       banner, strip/faixa/tira, grid/grade/coluna-como-layout, skeleton.
     - *visual form / hierarchy:* colour/cor, border/borda, shadow/sombra, spacing/espaçamento,
       opacity/opacidade, prominence/proeminência, emphasis/destaque.

     Naming any of them is contamination. **Three sharpening rules:**
     - **If the DS already owns the widget**, reference it by its **DS semantic name** or its
       **behavioural essence** — never re-describe its form or its container.
     - **Divergence notes (R3) obey R4 too:** describe a gap by **reach / parity**, never by a
       nav widget's name or position.
     - **Never prescribe prominence / emphasis.** State importance as a fact — *"the primary
       action"* — and leave the visual weight to the agent.

     **Literal copy too:** do not prescribe the exact button/label words — substitute the
     **literal copy** with its **speech-act (ato-de-fala)** (what the words make the person do
     or understand) and treat the exact words as **texture, a mutable content lane** (see the
     fixtures recipe's copy lane), never a binding requirement.
5. **Philosophy / guardrails** *(mandatory)* — the **human × system** axis (which decision is
   human judgement, which is the system's technical/hidden call), **what stays hidden**, and
   the **forbidden anti-pattern named** for risky screens (R6). A system decision must never
   surface as a user choice. **Do not emit an R5/R6 guardrail for a system that has no backend** —
   a guardrail around a non-existent system legitimises an invention; route the missing system to
   the **feature-reality gate** first, then brief it only if it's real.
6. **Flow** — the moment-to-moment sequence.
7. **States** — a per-screen **6-state ledger** over {empty, loading, error, offline, first-time,
   populated}: account for **each** state explicitly — either **specify it** or write
   *"<state> — not applicable (reason: …)"*. **Silent omission is forbidden** — an omitted state
   is indistinguishable from a forgotten one. Every **specified** state, in **mobile and desktop**,
   **light and dark**.
8. **Constraints** — usability (one hand, instant, forgives error, etc.).

## Omission audit before closing each screen (R3)

Ask, per screen: *"If I omit this parameter (timing, count, length, modality,
what-stays-hidden), would a reasonable agent fill it with something that contradicts the
product?"* If yes, **state the parameter**. Silence is permitted **only** about visual form.

## Catalog / collection / discovery screens

Brief discovery by an **information model**, never a flat category list. Name the **axes** and
their **roles**:

- **navigation** — a **closed ~N list** (the small, finite set the product organises around);
- **facets** — attributes that **cross** the navigation axis (a thing can carry several);
- **free-tail tags** — the open, long-tail labels.

Mark each axis **public vs. private** (catalog-visible vs. only-mine). Every **user collection**
needs a **"see all" surface**, and brief it **by the TARGET scale** — today's fixture is the
**empty / seed state, not the ceiling**, so the layout must hold the realistic full set. A user's
own collection gets its own **"my-state" per-item vocabulary** (progress, ownership, recency),
**distinct** from a public catalog's **social-proof vocabulary** (popularity, ratings, who-else).

## Hub vs. dashboard · desktop · comprehension · tracking-completeness

- **Hub ≠ dashboard.** An **action-hub** drives **motivation / status** (what to do next, where
  the person stands); an **analysis-dashboard** drives **analysis / metrics**. Brief the screen
  as the one it is — don't dress a hub as a metrics board or vice-versa.
- **Desktop is its own layout** for hub / dashboard screens — a **horizontal hero, two columns, a
  rail** — **not** a stretched mobile column.
- **Teach the product's distinctions.** When a product invariant names **discrete levels / senses**
  (a small set of directional or graded states), **define what each one means** and require the
  design to **teach the distinction**, not just label it.
- **Every number gets a gloss.** On data screens, give each metric its **user-meaning**
  (translate internal jargon into what it means for the person); no bare number ships without its
  one-line gloss.
- **Tracking / passive screens — "done" includes the full interaction inventory:** every status
  item is **tappable to its detail**; every **initiable action** has a **cancel / discard**; every
  **user-controllable number** has an **input**; **silent saves** get a **light confirmation**;
  every **list** has an **empty state**; copy is **honest** — **no fake affordances** in the mocks.

## De-induction rule (R7) — substitute, never delete

When removing a widget/gesture label, replace it with its behavioural essence; never delete
the essence along with the label. "swipe" → "a single fast gesture reachable with the thumb".

## Consume the inherited DS (not redefine)

Reference tokens/components by semantic name from the DS. Do **not** restate colour, radius,
shadow, spacing or any component. Fork the **base template** from the DS prompt as the shell.
If a screen needs something the DS lacks → **stop and signal**, do not improvise.

---

## Gold example (the bar to hit) — "how a card is answered"

**Shallow (the failure — do NOT generate like this):**
> *"Rate how well you remembered, on a short scale — didn't / almost / remembered."*

**Correct (behaviour + parameters + guardrails, no widget — generate like this):**
> **Interaction model.** Each card is **very short** (a few lines). The cadence is in
> **seconds**: the person thinks, and a **soft time limit of a few seconds** (in the current
> app, ~8s) reveals the back on its own. After reveal, the person expresses recall in a
> **single fast gesture reachable with the thumb**, **instant**, that **forgives an accidental
> touch**; on desktop equally fast **without a mouse**. There are **~3 human expressions**
> (didn't / almost / remembered); an "easy" is **inferred** from the human action of **revealing
> early by an explicit gesture** (vs. letting the soft limit reveal it) — the direction is
> *revealed-before-the-limit → confident* — not a 4th option to weigh. The whole act
> (think→reveal→answer→next) lasts **a few seconds**.
>
> *Caution:* a system-inferred outcome must **name the human action it reads** (the trigger,
> mined from the code) **and the direction** of the inference — never a vague "readiness".
>
> **Philosophy / guardrails (binding).** The person judges **memory**, never the **schedule**.
> The interval/scheduling (e.g. FSRS) is the **system's** and **does not appear**. **Forbidden:**
> showing "+N days", technical labels ("Hard/Good/Easy"), or turning the answer into an option
> picker with intervals. No number on the answering path.

Zero mention of colour/widget, yet the agent can no longer derive the button-with-days. That
is the quality target.
