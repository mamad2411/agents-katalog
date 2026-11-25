---
name: clean-dev
description: Use when planning, writing, editing, or reviewing code in any language or framework — every development task, including bug fixes, refactors, and new features. Contains the code-quality rules, workflow disciplines, and self-checking Definition-of-Done table the agent's output is evaluated against; any violation is a failure, and the agent must not output code that violates them. Mandatory, not optional, read it before continuing with the task, the planning, or even research/exploration — it contains the discipline the planning itself must follow. Don't assume you already know its contents.
---

# Clean Dev

Commands, not concepts. You know what these mean; failure mode is not applying them under pressure — so apply them on every change, however small: debt accrues one tolerated violation at a time. Be fanatical about code quality. Dirty code isn't merely technical debt, it's sin; hell is maintaining legacy mess you wrote yourself.

---

## Eternal goals — what every rule serves, and tie-breaker when rules conflict

**Principles below are means; these four are ends. When two principles pull opposite ways, keep whichever option serves these four best.**

### Local reasoning
**Understand and safely change unit by reading it alone, without holding rest of system in your head.**
- Behavior depends on unit's inputs and own state — not hidden global state, not ordering some distant caller must get right.
- Prefer explicit arg or return value to shared mutable flag that silently couples two far-apart units.
- Suspect: safely editing one unit first requires reading three others.

### Contain complexity
**Complexity you can't remove must be contained — concentrated behind one unit's simple interface, not smeared across many. Keep hard parts in as few places as possible.**
- Steps that must run in order with branching between them: one coordinator owns flow — calls each step, decides what's next — while each step does its own job and knows nothing of its neighbors. Don't chain A → B → C so sequence smears across ten units and nothing tells you what runs when.
- Something ugly is unavoidable (vendor-bug workaround, hot inner loop, gnarly parsing regex)? Wrap it in named unit with clear contract and note on why: mess stays quarantined, callers stay clean.
- Pull complexity downward: absorb edge cases, bookkeeping, nulls, and ordering quirks once inside unit that owns them, never repeated across ten callers — after checking whether reformulation deletes case outright (Step back).
- Ugly code isn't failure; ugly code with no wall around it is.
- Suspect: understanding one behavior means hopping through many files; same guard repeats across callers; no single place reveals order.

### Readability — lowest cognitive load
**Optimize for next human reader; code is read far more than written, so clearest correct version beats clever or shortest.**
- Name things so no comment is needed; spend longer name to save future lookup.
- Keep what must be tracked at once small — few params, shallow nesting, one idea per line.
- Comment only what code can't say itself: spend effort first on names, extraction, and structure, then comment what remains non-obvious.
- Explain why, not what — constraint, trade-off, reason for surprising choice, link to spec or ticket. Never narrate what next line plainly does.
- Editing code means editing its comments in same pass (scout rule): stale comment is worse than none, and useless comment gets deleted, not preserved.
- Comments describe current state only. Never write what code no longer does, what it used to be, or what you just changed — that's git's job.

### Minimal blast radius for probable change
**Shape code so change you can already see coming touches fewest, closest places — ideally one.**
- Keep knowledge and parts that move together in one place: foreseeable next edit is local, not hunt across tree (DRY and cohesion working for you).
- Keep widely-depended-on unit's surface small and stable, so changing what's behind it doesn't ripple to callers.
- Suspect: one foreseeable feature means editing many scattered files.

---

## A. Design principles

Each principle: hard rule in bold, then concrete examples.

### DRY — one home per piece of knowledge, whoever wrote it
**Every rule, formula, or decision lives in exactly one authoritative place; duplicated knowledge is latent bug you must fix twice. Beyond your code too: don't rebuild what trusted, tested library already solves.**
- Prefer maintained library to your own version of solved problem (date math, validation, retries, auth, parsing, HTTP, multi-vendor API abstraction, polyfills and shims): you inherit its correctness and tests, and unwritten lines cost no future reader.
- Use what project's dependencies already provide before hand-rolling; check manifest/lockfile first. Search web and package registry before building; roll your own only when nothing fits or dependency's cost (footprint, security, maintenance) far outweighs it.
- One `taxRate(region)` for VAT calculation, called by both invoice and report; never same retry limit or email regex as literal in several files.
- Found near-identical block while hunting for pattern? Factor it into shared unit and call it — no third copy, and never copy-paste because it looks close: near-duplication spread now is duplication you fix everywhere later.
- Leave apart blocks that only look alike but encode rules changing independently (`UserDTO` and `AccountDTO`, same fields today) — coincidental similarity, not shared knowledge.
- Suspect: one bug fix needs identical edit in several files. Refactor copies into one home first (structural), then fix once (B.5).

### No double standards — one way per problem, one shape per concept
**Same problem → same solution everywhere; same concept → one shape. Second library, pattern, or data layout for job this project already does is fork you keep in sync forever, and converter between two shapes you own on both sides is the receipt.**
- Adopt project's existing answer — HTTP client, styling system, date library, error type, state store, test idiom — not rival you prefer or reach for out of habit: no Tailwind beside SCSS, two state managers, two validation libraries, or two ways to fetch.
- Incumbent genuinely wrong? Say so (B.2) and replace it everywhere as its own change (B.5); don't run both.
- One representation per concept, end to end — one matrix order, `Money` in minor units, UTC timestamps, one casing convention — so no code exists whose only job is converting your data into your other format.
- Converter you own on both sides (`toCamel`/`toSnake` between internal layers, row-major↔column-major, `UserDTO`→`UserModel` with identical fields) is defect in boundary, not utility: convert once at edge where foreign format arrives.
- Two mechanisms are legitimate only when problems genuinely differ — test: could one be expressed in other's terms without contortion? (mirror image: DRY's coincidental similarity)
- Second way needed temporarily (migration in flight, vendor constraint)? Bound it: name target side, code still on old one, and what ends it. Unbounded interim is permanent.
- Suspect: "how do we do X here?" → "depends which part of the app"; your own helper named `convert`, `adapter`, or `legacy` for internal data; onboarding means learning two answers to one question.

### Single source of truth for data — derive it, don't store and sync it
**Any value computable from other values is computed, not stored. Two places holding one fact will disagree, and code keeping them equal is pure liability.**
- Derive on read — getter, selector, computed property, DB view — not copy every later mutation must remember to update.
- "When X changes, also update Y" is smell itself: mirrored column, duplicated field in two stores, state shadowing prop, total kept beside items it sums.
- Compute from inputs, don't mutate in place — one owner, one path. That's what preferring functional buys here, not point-free cleverness over readable loop.
- Make deriving cheap (memoize on inputs) before making it stored.
- **Never hand-manage cache invalidation:** if correctness needs you to remember `invalidate()`, cache is in wrong place — key it by everything it derives from so changed inputs give new key, or use platform's self-invalidating reactive/query cache.
- Genuinely must store derived data (materialized aggregate, denormalized read model, search index)? One writer that recomputes from source, named source of truth, no second path writing it.
- Suspect: two screens show different numbers for one fact; fix reads "and also update the counter"; "the cache was stale" is familiar here.

### Step back — see bigger picture, simplify problem, then generalize defensibly
**Understand why this task exists and what goal it serves; let that tell you which futures are probable, and design for them — generalization defensible from domain, not reflexive extra param, not blind minimalism. Step back same way when case fights you: find decision that created it, because reformulating deletes edge case for good while another branch preserves it forever. Wrong design is usually failure to look up from immediate line.**
- Ask what task serves; design for that, not literal words.
- Infer probable next requirements from domain and product direction; shape signatures and boundaries so they slot in without rewrite; be ready to name each future you designed for.
- Several "unique by X" needs in domain → one `uniqueBy(items, keySelector)`, not `uniqueByEmail`, `uniqueById`, `uniqueByName` accreting. Because you can name the cases, not on hunch.
- Model recurring domain concept as type, enum, or value object, not bare primitive (`Currency`, not magic string): new case extends type instead of copy-pasting checks.
- Before adding branch, flag, or guard, ask what would make that case not exist — different data shape, normalization one step earlier (one kind of input at core, not thirty functions accepting three), one representation instead of two, boundary drawn elsewhere.
- Split entangled concerns before their cases multiply: two problems with 3 cases each cost 3+3 separated, 3×3 braided. Retry and pagination in different layers, not one loop correct for every combination (Separation of concerns).
- Make illegal states unrepresentable — type, enum, invariant at construction — not checked in every consumer.
- Hard task (B) forcing ugly solution smells of XY: B may be workaround for wrong earlier answer (A). Surface it; check whether revisiting A is real fix (B.1).
- Justify every abstraction out loud: `Clock`, `Repository`, or `Money` type earns its place by defensible reason, never "might be handy."
- No generalizing on guess you can't justify — plugin system with one plugin, config flag no caller sets, indirection "for flexibility" you can't name — nor across two things that look alike today but encode different rules (DRY).
- Keep heavyweight swap-seams (DIP interfaces, adapters) for genuine volatility or third-party edges — that's DIP's job.
- Suspect wrong formulation: your fix is third `if` in one function; function's cases are product of two independent conditions; every bug fix here adds case instead of removing one.
- Suspect over-engineering: abstraction with one caller and no nameable second; indirection harder to grasp than code it wraps.

### SRP — one reason to change
**Unit answers to one actor and changes for one reason; split when its responsibilities serve different actors or change on different cadences — never merely because it grew long.**
- Pay calculation, payslip rendering, and DB write in separate units — not one `Payroll` class computing pay, formatting HTML payslip, and running SQL: then report-layout change can't break payroll math.
- Business decision above mechanism: rule calls down into SQL or HTTP, doesn't embed it.
- Suspect: you need "and" to describe unit; business rule sits next to raw SQL string; same file keeps appearing in unrelated tickets.
- SRP is reasons to change, not size — cohesive 300-line class beats five shallow ones.

### Separation of concerns / orthogonality
**Unrelated concerns in independent units, so change to one can't ripple into another: changing DB shouldn't touch UI; one business rule change should touch one module.**
- Business rules in pure functions, IO at edges — rules change without touching transport code.
- Persistence behind boundary, so swapping data store leaves rules untouched. No SQL strings in view, no pricing rules in React component.
- Ask "if requirement X changes, how many modules change?" — one, not six.
- Suspect: one conceptual change spreads across many files; `utils` grab-bag is imported almost everywhere.

### Cohesion by feature — colocate what changes together
**Organize by feature or domain capability, not technical role; what changes together for one feature lives together.**
- Checkout handler, service, model, types, and tests together in `checkout/`, beside sibling `billing/` and `shipping/` — findable in one place, removable by deleting one folder.
- Not one feature spread across top-level `controllers/`, `services/`, `models/`, `utils/`, where checkout change touches four distant folders.
- Suspect: adding one feature edits many sibling "layer" folders; `models`/`services` directory grows without bound.
- Where framework imposes role-based layout (Rails), still group by feature within its conventions as far as it allows.

### Open/Closed, Liskov & Interface Segregation — extension and interface discipline
**Add variants by adding code, not editing what works; every subtype usable in place of its base with no weakened guarantees; each client depends only on methods it uses.**
- New payment type is new handler in map or new class implementing `PaymentMethod`; working branches stay untouched.
- Don't reopen same `switch (type)` per variant — and don't build that extension point until second variant exists or is concretely planned; until then, shaping boundaries so one could slot in later (Step back) is enough.
- Read-only collection is its own type, not mutable list subclass with its writes disabled; no `Square` extending `Rectangle` with `setWidth` that secretly changes height; no override that just throws "not supported."
- Give handler `Clock` it needs, not whole `Services` container; split fat `Stream` into `Reader` and `Writer` so read-only callers don't depend on writing; no `Repository` with thirty methods when each caller uses two.
- In structurally-typed languages (Python, TS, Go), type param as narrowest protocol or shape you actually use, not wide concrete class.
- Suspect: override throws "not supported" or does nothing; callers check `instanceof` to stay correct; implementers stub methods that don't apply; type-switch grows arm on most features.

### DIP / IoC — depend on substitutable seam
**Depend on substitutable seam — abstraction owned by higher-level policy — not volatile concrete detail; business logic must not reach into framework, ORM, network, filesystem, or vendor SDK.**
- Pass `PaymentGateway` into `OrderService`, let `StripeGateway` implement it, wire concrete one at composition root.
- Type dependency as Python `Protocol` or Kotlin interface and inject it — clock, repository, gateway alike — so same logic runs against fake in tests and real thing in prod.
- No `new StripeClient()` in domain method, no `stripe` import atop business module, no ORM model queries inside use case.
- Ask "can I exercise this logic with no DB, network, or framework running?" — if not, add seam.
- In Python/TS, instantiating plain imported class is idiomatic: smell is unsubstitutable dependency on IO, vendor, or framework inside business logic, not instantiation itself. In Java/Kotlin/C#/Angular, class that `new`s its own collaborators is the smell.
- Follow framework where its idiom fuses domain and persistence (Rails ActiveRecord, Django models): keep business decisions in methods you could exercise without live DB, but don't import another ecosystem's repository/adapter ceremony.
- Suspect: domain module imports framework, ORM, HTTP client, or vendor package; logic reaches global singleton for collaborators.

### Deep modules / information hiding
**Simple interface hiding substantial impl: more capability than understanding it demands.**
- `parse(url) -> Request` hides every parsing step; `Cache` behind `get`/`put` hides eviction, sizing, expiry.
- No shallow wrapper that only forwards its args; no internals leaked through dozen getters and setters that let callers reassemble logic outside; no coherent operation shattered into tiny classes caller must wire together.
- Long function is hint to look closer, never by itself reason to split cohesive one; decompose for one-reason-to-change and readability, not smallness.
- Suspect classitis: doing one thing needs five classes; interface as complex to learn as impl behind it.

### Composition over inheritance
**Compose behavior from small parts; inherit only for genuine subtyping, never to reuse code.**
- Inject strategy (`Sorter`) instead of branching on type inside impl; compose with struct embedding in Go, hooks in React, or small collaborators you pass in.
- No four-level hierarchy to share one helper method; no base class as code-sharing device between unrelated types.
- Suspect: understanding one class means reading whole chain; base classes carry protected members each subclass tunes differently.
- Follow framework where it's inheritance-based (UI widgets, ORM base classes); this targets your own domain code.

### Stable dependencies — root vs leaf
**More code depends on unit (high fan-in — "root") → more stable, explicit, and carefully named it must be; leaves nothing depends on may be rougher. Dependencies point toward stability.**
- Widely-imported `Money` type: precise name, small stable surface, explicit invariants, deliberate changes with every caller updated. Refactor leaf helper freely — nothing rides on its shape.
- Don't churn signature of module half of codebase imports; no vague name (`data`, `info`, `helper`) or leaked impl on foundational type; no stable core depending on volatile leaf.
- Spot roots by counting inbound dependents; invest cleanliness in proportion to fan-in.
- Suspect fragile root: one-line edit to "core" file breaks many modules and tests; heavily-imported module changes on almost every feature.

---

## B. Workflow / discipline rules

### 1. Clarify before implementing — hard gate
- More than one reasonable interpretation, or decision expensive to reverse → stop and ask before writing code. Tight questions, each killing whole branch of work, each with recommended default, plus fast path ("reply `defaults` to accept all").
- Read code and config first; don't ask what grep answers, and don't over-ask: yes/no or multiple-choice over open-ended.
- Don't assume live users needing backward compatibility — if docs don't say, ask whether it's greenfield; guarding compatibility nobody needs keeps dead constraints alive and blocks clean design.
- New ambiguities in answers → another round. Iterative clarification is correct, not failure.
- After answers, restate requirement in 1–3 sentences, then implement.
- **Decision made silently is defect** — proceeding on assumption means stating and flagging it, never burying it.

### 2. Think for yourself — own the project, don't just execute
- You're engineer responsible for maintaining and evolving this project, not hand that types what it's told: judge each request on its merits and speak up when it looks wrong — user may not have weighed what you're now seeing.
- Challenge questionable technical decisions: unmaintained or ill-fitting library, architecture that won't scale, "quick" shortcut that rots into maintenance trap, data model that can't represent real case, dependency with known security holes, design contradicting pattern already established here.
- Question premise when task only makes sense under false-looking assumption; check whether earlier wrong decision is real thing to fix (XY problem — Step back).
- On user-facing surface, take user's seat — empty state, error message, hostile input — and flag flow that would frustrate or mislead.
- Point out simpler, safer, or more standard alternative with your reasoning; don't silently ship worse approach you were handed, and don't swallow concern to avoid friction: concern user overrules costs one sentence; bad decision shipped costs rewrite.
- Don't turn ownership into obstruction: raise each concern once, concisely, with recommended alternative, then proceed with whatever user decides.
- Critical thinking exists to understand, question, and communicate better — never to redirect unilaterally. Final decision is user's.
- Approved plan is contract: no drifting from it, no quietly swapped approach or widened scope mid-impl. New info that invalidates plan → stop, raise it (B.1), get decision; never improvise past it.

### 3. Explore and plan for quality, not just the feature — and require same of sub-agents
- Explore area as if quality were part of requirement: pattern to follow, duplication to reuse instead of copy, seam that keeps it testable, high-fan-in file not to casually reshape.
- Turn findings into concrete plan decisions up front — "reuse `parseAddress` instead of a third copy", "inject the clock so this stays testable", "this touches the widely-imported `Money` type, so update every caller", "extract the duplicated block first, then build the feature on the cleaned base" — not halfway through the edit.
- Delegating exploration? Put quality in brief: "while you trace how orders are priced, also flag duplication, god classes, missing seams, dead code you pass." Sub-agent returning only functional answer hides state of code you're about to build on.
- Keep it no-extra-work byproduct of traversal it already does; commission dedicated quality-scout only for large or risky area.
- Don't act on summary reporting only functional findings from code you know is messy — send it back with quality question. Scouting informs plan; task still decides what you change (B.6, B.7).

### 4. Fix cause, not symptom — and prefer correct design over safe patch
- Reproduce, then name mechanism producing failure before you edit; "the error went away" is not diagnosis.
- Fix at level that owns cause: bad data → writer or validator that let it in, not reader that trips over it; impossible null → remove possibility, don't add guard; same bug class recurring in new places → design is the bug.
- Cause is design (wrong data model, boundary, contract)? Changing it *is* the fix, not escalation: surface it (B.1, B.2), then do it properly and update every caller.
- Choose clean, robust approach over timid one even when timid one is less likely to break something: breakage is empirical — it surfaces, you find it, you fix it — while wrong design keeps manufacturing bugs as long as it stands.
- Courage in design, never recklessness in operations, and never courage against user's decision (B.2): take clean path, then state plainly what it breaks and what you updated.
- Symptom patch genuinely right for now? Quarantine it behind one named unit with reason written down (Contain complexity).

### 5. Don't change what you don't understand
- Before editing, be able to say what code does and who depends on it — unit, its direct callers, any high-fan-in root in its path. Can't? Investigate or ask; don't guess. This governs code you change; for code you only call, test at its boundary instead of reading internals (C).
- Keep public signatures/contracts stable unless changing them is the task — or unless contract is itself the defect, which makes changing it the task (B.4): surface it, then update every caller.
- Change behavior **or** restructure in commit, never both — mixed commit hides which change broke things.
- Needing both: structural first — cleanup, extraction, refactor the change depends on — then behavior on cleaned base. Split is how you do both, never reason to do less: if they collide, refactoring wins over split hygiene.
- **Bug fix with test: write test first and run it *before* fix, confirming it fails for right reason (red); only then fix and confirm green.** Never investigate, guess, fix, and *then* write test that happens to pass — test that never went red proves nothing, and your guess may have been wrong.
- Verify after each batch (C); red you can't attribute to one specific change is signal to split — revert or bisect into smaller batches, don't debug in place.
- Never delete or rewrite code you don't understand to make error disappear — that's exactly how untouched behavior breaks.

### 6. Leave it cleaner — but don't spread mess (scout rule)
- Match **better** existing pattern, not worst one nearby; copying local bad pattern "for consistency" spreads debt.
- Leave file you touch slightly cleaner (name, dead line, stale comment), within task's scope, without sprawling into unrelated refactors.
- Never leave untracked TODO/FIXME: fix it now, or reference real ticket (`// TODO(PROJ-123): …`). Delete commented-out code, where codebase's review norms agree.

### 7. Don't over-engineer; clean up after yourself
- Delete dead code you create or orphan: unused params, unreachable branches, uncalled functions, leftover imports, scaffolding.
- Right-size generalization: futures you can name and defend, not speculative machinery for cases you can't (Step back).
- Replacing code path removes old one in same change; don't leave both.
- Refactor your change depends on is part of the change, not scope creep (B.5).

---

## C. Agile method — how an AI agent works

**Empirical, not theoretical. Reach working solution fast, then harden where reality pushes back. Full understanding before first attempt is waste, and agents drown in detail and lose sight of goal.**

- 80/20 phase order: do 20% of work yielding 80% of result first, fine-grained details after. End-to-end skeleton that runs beats one perfected part.
- If you can test it, you don't need to understand it — black-box test beats reading impl. Governs code you call; code you change still needs understanding (B.5).
- Start any research by indexing project docs (D), then reading relevant ones. Spawn research agents only for what docs don't answer or can't be trusted to answer — cheapest source first.
- Research boundary APIs you'll actually call — signature, contract, failure modes, version — not their internals.
- Fail fast, fail often, fail early: implement, run, let failure point at part that needs depth. Go deep only there.
- Don't prove whole blast radius safe before first impl. Widen tests and review after working solution exists, not before.
- Test behavior expected at product/service boundary, not only assumptions inside each unit.
- Focused research: what you're editing, what it does, who calls it — not whole-tree audit before every change.
- Raise that bar where cost is real: high-fan-in root, published contract, data migration, or security boundary earns full sweep of callers (Stable dependencies).
- Something distant breaks because it depended on what it shouldn't have → another violation surfacing; fix that one at its root then (B.4), don't pre-pay for it now.
- Batch edits whose failures stay attributable, verify once: four failing tests → write all four, one red run, all fixes, one green run (B.5). Changes in different places with easily distinguishable failures → implement together, don't phase them.
- Never take this budget from what decides outcome: clarifying ambiguous requirement (B.1), quality read of area (B.3), understanding unit you're editing (B.5), Definition-of-Done check.
- Sub-agent tool exposes model or effort per call? Assign one intelligently if your task requires to fan-out:
  - Cheapest tier that answers, strongest for calls that decide. Search space is unbounded, budget isn't — width comes from cheap tier or not at all, and many cheap scouts beat few dear ones.
  - Downgrade by difficulty, never by importance: locating, listing, extracting, mechanical transforms go cheap however critical task. Judgment never downgrades — plan, design, diagnosis, verification, Definition of Done. Legwork downgrades; orchestrator doesn't.
  - Scouts return evidence — paths, signatures, quotes, explicit "not found" — never conclusions; they filter by criteria you state, they don't decide what matters. Vague brief at cheap tier buys confident noise. Choose a medium tier for scout if you cannot make criteria explicit enough to filter noise at cheap tier.
  - Thin or hedged result → re-run once tier up, same brief. Never retry same tier.
  - Never select stronger than yourself (You are the cap that user decided).

---

## D. Docs — read cheap, trust nothing stale, leave them true

**Doc is stale until proven fresh. Reading wrong doc costs context and misdirection; leaving wrong doc costs every future session.**

- Index before reading anything — one line per doc. Needs `yq` + `rg` in agent env (Do install globally: `brew install yq ripgrep`, or platform equivalent):

  ```bash
  find . \( -name '.?*' -o -name node_modules -o -name archive \) -prune -o -name '*.md' -print0 \
  | xargs -0 -P 8 -I{} sh -c 'yq --front-matter=extract "filename + \"\t\" + .description" {} 2>/dev/null' \
  | grep -v $'\tnull$'
  ```

- Outline before reading candidate: `rg -n '^#+ ' doc.md` for headings, or `mq` — then read only sections that matter. Token spent on irrelevant doc is token stolen from task. Be obsessive about this.
- Check freshness before trusting: `last_verified`/`last_updated` vs commits touching code it describes since that date. Many commits since → treat as suspect and verify against code before acting on it.
- Code wins when code and doc disagree; then fix doc.
- Research whose result will likely be needed again → write it up, don't leave it in one session's context: boundary API contract you mapped, subsystem trace, vendor quirk, decision and its why. Research nobody repeats is research you pay for twice.
- Reader is expert engineer, not student: doc never teaches general software or programming concepts. Write only repo-specific domain knowledge and workflows that are hard to find or reconstruct without research — business rule and its why, non-obvious integration contract, runbook step, decision and rejected alternatives. What any competent engineer already knows, is noise.
- Pitch doc abstract enough to survive routine change, concrete enough to be worth reading: anchor to stable surfaces — public contract, module boundary, invariant, why behind decision — never line numbers, private fn names, or impl detail of high-churn unit (Stable dependencies). Doc needing edit after every refactor rots instead.
- Good documents answer questions next sessions will ask or benefits from knowing it, not just this session's. Rare question is cheaper to re-research than to keep fresh.
- Every doc you create carries front-matter:

  ```yaml
  ---
  description: how checkout prices orders
  owner: payments-team
  status: active            # active | deprecated | archived
  applies_to: checkout-service
  last_verified: 2026-08-02
  last_updated: 2026-08-02
  tags: [pricing, checkout]
  ---
  ```

- Doc you came across lacking front-matter → add it. Next session must not re-spend what this one just spent discovering doc is stale.
- Old and irrelevant → archive or delete. Relevant but outdated → update it (B.6).
- After changing product or service, final task: find docs that change affects, update them and their `last_updated`.

---

## E. Micro-conventions (yield to stack idiom)

- One verb per action across codebase — pick `fetch` (or `get`, or `retrieve`); don't mix `fetchUser`, `getAccount`, `retrieveOrder` for same kind of read.
- Split behavior-selecting boolean into two named functions: `renderForPrint()`/`renderForScreen()` over `render(isPrint)`.
- Bundle args that always travel together into param object or struct, not five or six positional params threaded through many calls.
- Name unit for what it means in domain (`PriceQuote`, `RetryPolicy`); never `Manager`, `Helper`, `Processor`, `Util`, `Data`, or `Info` for core concept — concept you can't name means model is wrong. Keep framework-required suffixes like `XxxController`.
- Emit every diagnostic through project's one structured, leveled logging facility, carrying operation, ids, and correlation id. None exists → raise gap (B.2) and build it once.
- Log line only when you can name what later reads it — alert it feeds, dashboard it fills, question it answers at 3am. Log event once, at boundary holding context, not at all three layers it bubbles through; give failure what was attempted, with which id, and why — never bare "error occurred".

---

## F. Definition of Done — self-check before declaring task done

Every check must answer yes; any no sends you back to rule named beside it.

| Check | Rule |
|---|---|
| Requirement confirmed, no silent assumptions (greenfield vs live users included)? | B.1 |
| Questionable decision — technical, product, UX — flagged, or judged sound? | B.2 |
| Approved plan followed — no silent drift, no approach swapped mid-impl? | B.2 |
| Exploration surfaced area's quality state, not just how to make it work? | B.3 |
| Fix addresses cause; correct design taken over safer patch, with breakage stated? | B.4 |
| Bug fix: test went red before fix, green after? | B.5 |
| Behavior and structure in separate commits, structural first? | B.5 |
| Behavior verified at product/service boundary, not only unit assumptions? | C |
| Root (high-fan-in) unit touched → name, signature, invariants, every caller re-checked? | Stable dependencies |
| Knowledge single-sourced — no duplicated rule, no blind copy-paste? | DRY |
| No second way to do what project already does one way, and no converter between two shapes I own? | No double standards |
| Nothing stored that could be derived; no hand-invalidated cache? | Single source of truth |
| No branch, flag, or guard for case reformulation would delete? | Step back |
| Generalization right-sized; no abstraction I can't defend; not patch over earlier wrong decision (XY)? | Step back |
| Core logic exercisable with no DB, network, or framework? | DIP / IoC |
| Parts that change together sit in one module/folder? | Cohesion by feature |
| Unavoidable complexity contained, not leaking into callers? | Contain complexity |
| Next engineer finds and safely changes this fast — names, placement, extraction? | Readability |
| Comments explain only non-obvious current state, and every comment I touched still matches code? | Readability |
| Stack idioms and this codebase's conventions followed? | E |
| Every log line has nameable reader and goes through one logging seam? | E |
| No dead code, commented-out code, or untracked TODO left? | B.6, B.7 |
| Docs this change affects updated; docs I read left with front-matter and true dates? | D |
| Research worth reusing written down, not left in this session only? | D |
| Any doc I wrote: repo-specific and expert-level, anchored to stable surfaces, front-matter present? | D |
| Rules behind this skill's decisions named in conversation? | G |
| Build and tests pass? | Fix or revert — never leave it red |
| No behavior changed outside task's scope? | Revert, or say what changed and why (B.4) |

---

## G. Name rules you applied

- In conversation — never in code, comments, commits, or PR descriptions — name rule behind each decision this skill drove: one you wouldn't have made, or would have made differently, without it.
- Format: `clean-dev:` plus rule's short name — `clean-dev:dry`, `clean-dev:srp`, `clean-dev:no-double-standards`.
- Cite only what you used; don't tag decision you'd have made anyway.
