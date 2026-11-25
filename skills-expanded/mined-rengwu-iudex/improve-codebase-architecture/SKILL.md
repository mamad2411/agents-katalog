---
name: improve-codebase-architecture
description: Find deepening opportunities in a codebase, informed by the domain language in .context/ and the decisions in .context/adr/. Use when the user wants to improve architecture, find refactoring opportunities, consolidate tightly-coupled modules, or make a codebase more testable and AI-navigable.
---

# Improve Codebase Architecture

Surface architectural friction and propose **deepening opportunities** — refactors that turn shallow modules into deep ones. The aim is testability and AI-navigability.

This skill is a *source* of work that feeds the iudex funnel: a chosen deepening can be sliced into iudex tickets via **to-issues**, or recorded as an ADR in `.context/adr/` when the decision is to leave it as-is.

## Glossary

Use these terms exactly in every suggestion. Consistent language is the point — don't drift into "component," "service," "API," or "boundary."

- **Module** — anything with an interface and an implementation (function, class, package, slice). Deliberately scale-agnostic. _Avoid_: unit, component, service.
- **Interface** — everything a caller must know to use the module correctly: the type signature, but also invariants, ordering constraints, error modes, required configuration, performance characteristics. _Avoid_: API, signature (too narrow).
- **Implementation** — what's inside a module, its body of code. Distinct from **Adapter**: a thing can be a small adapter with a large implementation (a Postgres repo) or a large adapter with a small implementation (an in-memory fake). Reach for "adapter" when the seam is the topic; "implementation" otherwise.
- **Depth** — leverage at the interface: the amount of behaviour a caller (or test) can exercise per unit of interface they have to learn. **Deep** = a lot of behaviour behind a small interface. **Shallow** = interface nearly as complex as the implementation.
- **Seam** (from Michael Feathers) — a place where you can alter behaviour without editing in that place; the *location* at which a module's interface lives. _Avoid_: boundary (overloaded with DDD's bounded context).
- **Adapter** — a concrete thing satisfying an interface at a seam. Describes *role* (what slot it fills), not substance (what's inside).
- **Leverage** — what callers get from depth: more capability per unit of interface they have to learn. One implementation pays back across N call sites and M tests.
- **Locality** — what maintainers get from depth: change, bugs, knowledge, and verification concentrate at one place rather than spreading across callers. Fix once, fixed everywhere.

Key principles:

- **Depth is a property of the interface, not the implementation.** A deep module can be internally composed of small, mockable, swappable parts — they just aren't part of the interface. A module can have **internal seams** (private to its implementation, used by its own tests) as well as the **external seam** at its interface.
- **Deletion test**: imagine deleting the module. If complexity vanishes, it was a pass-through. If complexity reappears across N callers, it was earning its keep.
- **The interface is the test surface.** Callers and tests cross the same seam. If you want to test *past* the interface, the module is probably the wrong shape.
- **One adapter = hypothetical seam. Two adapters = real seam.** Don't introduce a seam unless something actually varies across it.

Rejected framings: depth as a ratio of implementation-lines to interface-lines (rewards padding) — use depth-as-leverage instead; "interface" as just the TypeScript `interface` keyword or a class's public methods (too narrow); "boundary" (say **seam** or **interface**).

This skill is _informed_ by the project's domain model. The domain language gives names to good seams; ADRs record decisions the skill should not re-litigate. The domain glossary is every top-level `*.md` in `.context/`; ADRs live in `.context/adr/`. `.context/` is tracked project documentation.

## Process

### 1. Explore

Read the project's domain glossary (top-level `*.md` in `.context/`) and any ADRs in `.context/adr/` for the area you're touching first.

Then use the Agent tool with `subagent_type=Explore` to walk the codebase. Don't follow rigid heuristics — explore organically and note where you experience friction:

- Where does understanding one concept require bouncing between many small modules?
- Where are modules **shallow** — interface nearly as complex as the implementation?
- Where have pure functions been extracted just for testability, but the real bugs hide in how they're called (no **locality**)?
- Where do tightly-coupled modules leak across their seams?
- Which parts of the codebase are untested, or hard to test through their current interface?

Apply the **deletion test** to anything you suspect is shallow: would deleting it concentrate complexity, or just move it? A "yes, concentrates" is the signal you want.

### 2. Present candidates as an HTML report

Write a self-contained HTML file to the OS temp directory so nothing lands in the repo. Resolve the temp dir from `$TMPDIR`, falling back to `/tmp` (or `%TEMP%` on Windows), and write to `<tmpdir>/architecture-review-<timestamp>.html` so each run gets a fresh file. Open it for the user — `xdg-open <path>` on Linux, `open <path>` on macOS, `start <path>` on Windows — and tell them the absolute path.

The report uses **Tailwind via CDN** for layout and styling, and **Mermaid via CDN** for diagrams where a graph/flow/sequence reliably communicates the structure. Mix Mermaid with hand-crafted CSS/SVG visuals — use Mermaid when relationships are graph-shaped (call graphs, dependencies, sequences), and hand-built divs/SVG when you want something more editorial (mass diagrams, cross-sections, collapse animations). Each candidate gets a **before/after visualisation**. Be visual.

For each candidate, render a card with:

- **Files** — which files/modules are involved (monospaced, `font-mono text-sm`)
- **Problem** — one sentence; why the current architecture causes friction
- **Solution** — one sentence; what changes
- **Wins** — bullets, ≤6 words each, named in glossary terms ("locality: bugs concentrate in one module", "leverage: one interface, N call sites")
- **Before / After diagram** — side-by-side, custom-drawn, illustrating the shallowness and the deepening (the centrepiece)
- **Recommendation strength** — `Strong` (emerald), `Worth exploring` (amber), `Speculative` (slate), rendered as a badge
- **Dependency-category tag** — `in-process`, `local-substitutable`, `ports & adapters`, or `mock` (see Deepening, below)
- **ADR callout** (if applicable) — one amber-tinted line

End the report with a **Top recommendation** section: which candidate you'd tackle first and why.

**Use the domain vocabulary from `.context/` for the domain, and the Glossary above for the architecture.** If the glossary defines "Order," talk about "the Order intake module" — not "the FooBarHandler," and not "the Order service."

**ADR conflicts**: if a candidate contradicts an existing ADR, only surface it when the friction is real enough to warrant revisiting the ADR. Mark it clearly in the card (e.g. _"contradicts ADR-0007 — but worth reopening because…"_). Don't list every theoretical refactor an ADR forbids.

See the **HTML report format** section below for the full scaffold, diagram patterns, and styling.

Do NOT propose interfaces yet. After the file is written, ask the user: "Which of these would you like to explore?"

### 3. Grilling loop

Once the user picks a candidate, drop into a grilling conversation. Walk the design tree with them — constraints, dependencies, the shape of the deepened module, what sits behind the seam, what tests survive. Ask questions one at a time, recommending an answer for each.

Side effects happen inline as decisions crystallize:

- **Naming a deepened module after a concept not in the glossary?** Add the term to `.context/glossary.md` (or the relevant per-context file). Keep definitions tight (one or two sentences, what it IS not what it does), be opinionated about the canonical word and list rejected synonyms under `_Avoid_`. Create the file lazily if it doesn't exist.
- **Sharpening a fuzzy term during the conversation?** Update the glossary right there.
- **User rejects the candidate with a load-bearing reason?** Offer an ADR, framed as: _"Want me to record this as an ADR so future architecture reviews don't re-suggest it?"_ Only offer when the reason would actually be needed by a future explorer to avoid re-suggesting the same thing — skip ephemeral reasons ("not worth it right now") and self-evident ones. Write it to `.context/adr/NNNN-slug.md` (scan the directory for the highest number and increment); a single paragraph stating what was decided and why is enough.
- **User commits to the deepening?** It's now work to schedule. Hand the agreed design to **to-issues** to slice it into iudex tickets (or to **to-prd** first if it's large enough to warrant a written spec).
- **Want to explore alternative interfaces for the deepened module?** See **Interface design** below.

---

## Reference: Deepening

How to deepen a cluster of shallow modules safely, given its dependencies. When assessing a candidate, classify its dependencies — the category determines how the deepened module is tested across its seam.

1. **In-process** — pure computation, in-memory state, no I/O. Always deepenable: merge the modules and test through the new interface directly. No adapter needed.
2. **Local-substitutable** — dependencies with local test stand-ins (PGLite for Postgres, in-memory filesystem). Deepenable if the stand-in exists; the deepened module is tested with the stand-in running in the suite. The seam is internal; no port at the module's external interface.
3. **Remote but owned (Ports & Adapters)** — your own services across a network boundary. Define a **port** (interface) at the seam. The deep module owns the logic; the transport is injected as an **adapter**. Tests use an in-memory adapter; production uses an HTTP/gRPC/queue adapter. Recommendation shape: *"Define a port at the seam, implement an HTTP adapter for production and an in-memory adapter for testing, so the logic sits in one deep module even though it's deployed across a network."*
4. **True external (Mock)** — third-party services (Stripe, Twilio) you don't control. The deepened module takes the external dependency as an injected port; tests provide a mock adapter.

Seam discipline:

- **One adapter = hypothetical seam. Two adapters = real one.** Don't introduce a port unless at least two adapters are justified (typically production + test). A single-adapter seam is just indirection.
- **Internal seams vs external seams.** Don't expose internal seams through the interface just because tests use them.

Testing strategy — replace, don't layer:

- Old unit tests on shallow modules become waste once tests at the deepened module's interface exist — delete them.
- Write new tests at the deepened module's interface. The **interface is the test surface**.
- Tests assert on observable outcomes through the interface, not internal state, and survive internal refactors.

## Reference: Interface design (design it twice)

When the user wants to explore alternative interfaces for a chosen candidate, use this parallel sub-agent pattern. Based on "Design It Twice" (Ousterhout) — your first idea is unlikely to be the best.

1. **Frame the problem space.** Before spawning sub-agents, write a user-facing explanation: the constraints any new interface must satisfy, the dependencies it relies on and their category (above), and a rough illustrative code sketch to ground the constraints (not a proposal). Show it to the user, then immediately proceed — they read while the sub-agents work.
2. **Spawn 3+ sub-agents in parallel** (Agent tool). Each must produce a **radically different** interface. Prompt each with a separate technical brief (file paths, coupling details, dependency category, what sits behind the seam) plus the architecture Glossary above and the project's domain vocabulary from `.context/`. Give each a different constraint:
   - Agent 1: "Minimize the interface — 1–3 entry points max. Maximise leverage per entry point."
   - Agent 2: "Maximise flexibility — support many use cases and extension."
   - Agent 3: "Optimise for the most common caller — make the default case trivial."
   - Agent 4 (if applicable): "Design around ports & adapters for cross-seam dependencies."
   Each sub-agent outputs: the interface (types, methods, params, invariants, ordering, error modes); a usage example; what the implementation hides behind the seam; dependency strategy and adapters; trade-offs (where leverage is high, where thin).
3. **Present and compare.** Present designs sequentially, then compare in prose by **depth**, **locality**, and **seam placement**. Give your own opinionated recommendation; propose a hybrid if elements combine well.

## Reference: HTML report format

A single self-contained HTML file in the OS temp dir. Tailwind and Mermaid both from CDNs.

Scaffold:

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>Architecture review — {{repo name}}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script type="module">
      import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs";
      mermaid.initialize({ startOnLoad: true, theme: "neutral", securityLevel: "loose" });
    </script>
    <style>
      .seam { stroke-dasharray: 4 4; }
      .leak { stroke: #dc2626; }
      .deep { background: linear-gradient(135deg, #0f172a, #1e293b); }
    </style>
  </head>
  <body class="bg-stone-50 text-slate-900 font-sans">
    <main class="max-w-5xl mx-auto px-6 py-12 space-y-12">
      <header>...</header>
      <section id="candidates" class="space-y-10">...</section>
      <section id="top-recommendation">...</section>
    </main>
  </body>
</html>
```

**Header**: repo name, date, and a compact legend (solid box = module, dashed line = seam, red arrow = leakage, thick dark box = deep module). No intro paragraph — straight into candidates.

**Diagram patterns** (pick what fits; mix them — don't make every diagram look the same):

- **Mermaid graph** — the workhorse for dependencies / call flow. Use a `flowchart`/`graph` for "X calls Y calls Z, and look at the mess." Style with `classDef` to colour leakage edges red and the deep module dark. Sequence diagrams suit "before: 6 round-trips; after: 1."

  ```html
  <div class="rounded-lg border border-slate-200 bg-white p-4">
    <pre class="mermaid">
      flowchart LR
        A[OrderHandler] --> B[OrderValidator]
        B --> C[OrderRepo]
        C -.leak.-> D[PricingClient]
        classDef leak stroke:#dc2626,stroke-width:2px;
        class C,D leak
    </pre>
  </div>
  ```

- **Hand-built boxes-and-arrows** — modules as `<div>`s with borders; arrows as inline SVG `<line>`/`<path>` over a relative container. Reach for this when the "after" should feel like one thick-bordered deep module with greyed-out internals.
- **Cross-section** — stack horizontal bands (`h-12 border-l-4`) to show layers a call passes through. Before: 6 thin layers doing nothing. After: 1 thick band.
- **Mass diagram** — two rectangles per module (interface surface vs implementation). Before: interface rectangle nearly as tall as implementation (shallow). After: short interface, tall implementation (deep).
- **Call-graph collapse** — before: a tree of nested call boxes. After: collapsed into one box, now-internal calls faded inside.

**Style guidance**: lean editorial, not corporate-dashboard. Generous whitespace; serif optional for headings (`font-serif` with stone/slate). Colour sparingly — one accent (emerald or indigo) plus red for leakage, amber for warnings. Keep diagrams ~320px tall so before/after sits side by side. `text-xs uppercase tracking-wider` for module labels inside diagrams. The only scripts are the Tailwind CDN and Mermaid ESM import; otherwise static.

**Top recommendation section**: one larger card — candidate name, one sentence on why, anchor link to its card.

**Tone**: plain English, concise, architectural nouns/verbs straight from the Glossary. **Use exactly**: module, interface, implementation, depth, deep, shallow, seam, adapter, leverage, locality. **Never substitute**: component/service/unit (for module), API/signature (for interface), boundary (for seam), layer/wrapper (for module). Don't write "easier to maintain" or "cleaner code" — those aren't glossary terms. No hedging or throat-clearing. If a sentence could be a bullet, make it a bullet; if a bullet could be cut, cut it.
