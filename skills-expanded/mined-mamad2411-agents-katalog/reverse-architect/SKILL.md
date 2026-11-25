---
name: reverse-architect
description: Reverse-engineer any software project's design from high-level purpose down to component interactions, producing a knowledge map that enables either contributing to the project or rebuilding your own version in a different tech stack. Use when asked to "understand this codebase", "explain how this project works", "map this architecture", "write docs for this repo", "prepare to contribute", or "rebuild this in my own stack".
---

# Reverse Architect

Expert assistant for reverse-engineering the *design* of an existing software project — not just reading its code, but reconstructing the reasoning behind it. The output is a layered knowledge map that takes a reader from "why does this exist?" all the way down to "how do these components talk to each other?", deep enough to support two end goals: **contributing** to the project, or **rebuilding** a personal version in a preferred tech stack.

## Core Philosophy

Every analysis is driven by one root question:

> **"If I had to rebuild this from an empty folder, what is the minimum I'd need to understand — and in what order — so that every line I write has a reason?"**

This question is deliberately symmetric. A contributor and a rebuilder need the *same map*; they just stop at different layers and act on it differently. The contributor uses the map to make a small, safe change without breaking an invariant. The rebuilder uses the same map to decide what is load-bearing (must keep) versus what is an accidental implementation choice (free to swap).

The skill works **outside-in and static-to-dynamic**: start from human purpose, descend through structure, then animate the structure by tracing data through it. Understanding is never assumed — each step ends with a **Decision Point**, a sentence the agent must be able to complete before moving deeper. If it cannot complete the sentence, it has skimmed, not understood, and must go back.

**Anti-patterns to avoid:**

- Listing files and folders without explaining *why each boundary exists*
- Reciting the tech stack as a dependency dump instead of grouping it *by the concern each library serves*
- Drawing static box diagrams instead of tracing *data in motion*
- Jumping to "here's how to change it" before the invariants are mapped
- Treating every dependency as essential — failing to separate load-bearing walls from decoration

---

## Thinking Process

When activated, follow these seven steps in order. Steps 1–6 build understanding identically for both end goals; Step 7 forks into the track the user needs.

### Step 1: Find the Pain & the Promise (Why Does This Exist?)

**Goal:** State, in one plain-language sentence, the human problem this project solves — before reading architecture.

**Key Questions to Ask:**
- What does a person do *manually and painfully* without this tool?
- Who is the user, and what is the exact moment they reach for it?
- What is the *promise* — the one outcome that, if removed, makes the whole project pointless?

**Thinking Framework:**
- "Without this, [person] would have to _____."
- "The single most important thing this must get right is _____. Everything else is supporting cast."
- Resist reading the code until you can answer these. If you can't, the code will be noise.

**Actions:**
1. Read the README's first paragraph and the top-level docs — but only for *intent*, not mechanics.
2. State the purpose in one sentence containing no library names.
3. Identify the one promise that defines success.

**Decision Point:** You can complete:
- "This project exists so that [person] does not have to [painful thing], and it succeeds if and only if [the promise]."

**Example (Plannotator):** "This exists so that an engineer does not have to blindly approve an AI agent's plan in a terminal — it succeeds if and only if the user can review, annotate, and approve/deny a plan in a real UI, and that decision flows back to the agent."

---

### Step 2: Map the Topography (What Are the Boundaries, and Why?)

**Goal:** Draw the project's module/package boundaries as a dependency graph, and explain why each boundary exists — what would break if two modules merged.

**Key Questions to Ask:**
- What are the top-level units (packages, apps, services), and which depend on which?
- Which units are *leaves* (pure logic, no internal deps) and which are *roots* (deployables)?
- Why is each boundary drawn here? What single responsibility does it protect?

**Thinking Framework — Leaves to Roots:**
```
Pure-logic leaves (no internal deps, easy to test)
  → Shared infrastructure (servers, UI kits — depend on leaves)
    → Composition layer (app shells — wire infrastructure together)
      → Deployables (the apps users actually run)
```
- "This boundary exists so that [unit A] can change without forcing [unit B] to change."
- A boundary that protects nothing is accidental complexity — note it.

**Actions:**
1. Read the workspace/build manifest (`package.json` workspaces, `go.mod`, `Cargo.toml`, etc.) to find the units.
2. Read each unit's manifest to extract internal dependencies only.
3. Draw the dependency graph as ASCII, ordered leaves → roots.
4. Build a one-line single-responsibility table for each unit.

**Decision Point:** You can complete:
- "The dependency graph flows [leaves] → [infra] → [apps]; the load-bearing boundary is [X] because it isolates [responsibility]."

**Example (Plannotator):** `shared` + `ai` (pure leaves) → `server` + `ui` (infrastructure) → `editor` + `review-editor` (app shells) → `apps/hook`, `apps/opencode-plugin`, etc. The `shared` boundary exists so the same storage/diff/VCS logic runs unchanged under both the Bun server and the Node-based Pi server.

---

### Step 3: Inventory the Tech Stack by Concern

**Goal:** Map the technology choices grouped by the *concern* each one serves, with a note on what could replace it. This is the bridge between "what they used" and "what I'd use."

**Key Questions to Ask:**
- For each concern (UI, parsing, storage, networking, build, etc.), which library owns it?
- *Why* this library — what property made it the choice (performance, ergonomics, ecosystem)?
- Is this choice load-bearing (tied to the promise) or swappable (incidental)?

**Thinking Framework — The Concern Table:**

| Concern | Library chosen | Why this one | Swappable? |
|---------|---------------|--------------|------------|
| UI rendering | … | … | yes/no + with what |
| Data parsing | … | … | … |
| Persistence | … | … | … |
| Transport/server | … | … | … |
| Build/packaging | … | … | … |

- "If I were rebuilding, I could replace [X] with [Y] and lose only [Z]."
- A library that appears in many units is structural; one that appears in one unit is local.

**Actions:**
1. Read the dependency lists from Step 2's manifests.
2. Cluster dependencies by concern, not alphabetically.
3. For each concern, name the owner library and a plausible substitute.

**Decision Point:** You can complete:
- "The stack divides into [N] concerns; the load-bearing choices are [list] because they directly enable the promise; the rest are swappable."

**Example (Plannotator):** UI = React 19 + Tailwind 4; markdown render = `marked`, HTML→MD = `turndown`; plan diff = `diff` npm; **code-review diff = `@pierre/diffs` (load-bearing — its shadow-DOM renderer is the heart of the review UI)**; text annotation = `web-highlighter` (load-bearing); transport = `Bun.serve` (swappable — Pi proves it, using `node:http`); build = Vite + `vite-plugin-singlefile`.

---

### Step 4: Trace the Core Flows End-to-End (Animate the Structure)

**Goal:** For each primary user flow, trace data from the triggering event to the final resolution, naming every component it passes through. This turns the static graph from Step 2 into living behavior.

**Key Questions to Ask:**
- What are the 2–4 *primary* flows (the things users actually do)?
- For each: what triggers it, what transforms the data, where is it stored, how does the result get back?
- At each hop: *what is lost or could break here?*

**Thinking Framework — Follow the Data:**
```
Trigger (user action / external event)
  → Who receives it first?
    → How is the payload parsed / validated?
      → Which component transforms it?
        → Where does it rest (storage / state)?
          → How is the result rendered / returned?
            → How does the loop close (response to trigger)?
```

**Actions:**
1. Identify the entry point of each flow (CLI arg, route, hook, event handler).
2. Trace it hop-by-hop through the units from Step 2; cite `file:line` for each hop.
3. Draw one ASCII sequence diagram per flow — one flow, one diagram.
4. At each hop, ask "what is lost here?" and note blind spots.

**Decision Point:** For each flow you can complete:
- "Flow [name] starts at [entry], passes through [components in order], rests at [storage/state], and closes by [return path]."

**Example (Plannotator) — Plan Review flow:** Claude `ExitPlanMode` → `PermissionRequest` hook spawns the `plannotator` CLI → `apps/hook/server/index.ts` reads stdin JSON, extracts `tool_input.plan` → `startPlannotatorServer` saves history + computes previous-version diff + `Bun.serve` → browser fetches `/api/plan`, parses to blocks, renders `Viewer` → user approves/denies → `waitForDecision` resolves → CLI prints `{hookSpecificOutput:{decision:{behavior}}}` to stdout → agent acts.

---

### Step 5: Extract the Data Model & Contracts

**Goal:** Identify the 3–5 core data types and the contracts (APIs, message formats, protocols) by which components communicate. These are what a rebuild must preserve and a contribution must not violate.

**Key Questions to Ask:**
- What are the central nouns (the types every flow touches)?
- What is the API surface / message schema between the major boundaries?
- Which fields are essential to the promise vs. incidental conveniences?

**Thinking Framework — Nouns and Contracts:**
- The *nouns* are the types that appear in multiple flows (Step 4). Find their definition file.
- The *contracts* are the serialized boundaries: HTTP endpoints, stdout protocols, IPC messages, file formats.
- "Component A and Component B agree on [contract]; if I change it, both must change together."

**Actions:**
1. Read the central type-definition file(s); list the core types with their key fields.
2. Enumerate the API/protocol surface (endpoints, message shapes, exit formats).
3. Mark each contract as essential or incidental relative to the promise.

**Decision Point:** You can complete:
- "The core nouns are [types]; the load-bearing contracts are [list]; a rebuild must honor [essential ones] but may redesign [incidental ones]."

**Example (Plannotator):** Core nouns = `Annotation` (`{id, type, originalText, text?, diffContext?, startMeta/endMeta}`) and `Block` (`{id, type, content, level?, startLine}`). Contracts = the `/api/*` HTTP surface (`/api/plan`, `/api/approve`, `/api/deny`, `/api/diff`, `/api/feedback`) **plus the stdout hook protocol** (`{hookSpecificOutput:{decision:{behavior:'allow'|'deny'}}}`) — the latter is the load-bearing contract with Claude Code itself.

---

### Step 6: Find the Seams & Invariants (The Rules You Must Not Break)

**Goal:** Locate the extension points (seams) and the invariants — the implicit rules that keep the system correct. This is the step that separates a safe contributor from a dangerous one, and a faithful rebuild from a broken one.

**Key Questions to Ask:**
- Where is the system *designed* to be extended (plugin points, provider registries, mirrored implementations)?
- What rules are enforced by convention rather than the compiler (build order, mirrored runtimes, "update both places")?
- What would silently break if a newcomer didn't know the rule?

**Thinking Framework — Hunt for Hidden Rules:**
- Look for *mirrored* code (two implementations of the same API) — changing one means changing both.
- Look for *build-order* dependencies (artifact A is copied into B) — wrong order ships stale output.
- Look for *boundary bridges* (shadow DOM, FFI, serialization) — fragile crossing points.
- Look in `AGENTS.md` / `CONTRIBUTING.md` / build scripts for "you must" / "always" / "don't" language.

**Actions:**
1. Identify each seam and how it is meant to be extended.
2. List each invariant as an explicit rule plus the consequence of breaking it.
3. Map each invariant back to the components it constrains.

**Decision Point:** You can complete:
- "To extend this safely I must respect [invariants]; the most dangerous one is [X] because breaking it fails [silently/loudly]."

**Example (Plannotator):** Seam = the AI provider registry (`@plannotator/ai`) and the dual server runtimes. Invariants: (1) **every server endpoint must be implemented in *both* the Bun server and the Pi `node:http` server** — they mirror each other via `vendor.sh`; (2) **build order**: `apps/review` must build before `build:hook` or the hook ships stale HTML; (3) the `@pierre/diffs` theme is bridged into a shadow DOM via `unsafeCSS` — a fragile boundary.

---

### Step 7: Fork — Choose Your Track

**Goal:** Route the now-complete knowledge map into the deliverable the user actually needs.

**Decision Matrix:**

| User intent | Track | Reference file |
|-------------|-------|----------------|
| "I want to contribute / fix / add a feature" | **Contribution Track** | `references/contribution-track.md` |
| "I want to build my own version in [stack]" | **Rebuild Track** | `references/rebuild-track.md` |
| Unsure / both | Present the shared map, then ask which track | both |

**Contribution Track (summary):** Map the change surface onto Step 2's graph, run the change against Step 6's invariant checklist, find the smallest safe change, and verify it (tests + the project's typecheck/build order). Read `references/contribution-track.md` for the full checklist.

**Rebuild Track (summary):** Use Step 3's concern table to build a substitution matrix (original → your choice → what you lose), derive a parity checklist from Step 5's essential contracts, strip away the accidental complexity, and sequence the build leaves-first per Step 2's graph. Read `references/rebuild-track.md` for the full template.

**Decision Point:** You have produced the track-specific deliverable, and the user can act on it without re-reading the whole codebase.

---

## Source Discipline

Ground every structural claim in the repository itself, in this priority order:

| Priority | Source | Use for |
|----------|--------|---------|
| 1 | Build/workspace manifests (`package.json`, `go.mod`, etc.) | Boundaries + dependency graph (Step 2) |
| 2 | Type-definition + schema files | Data model + contracts (Step 5) |
| 3 | Entry points (CLI, routes, handlers) | Flow tracing (Step 4) |
| 4 | `AGENTS.md` / `CONTRIBUTING.md` / build scripts | Invariants (Step 6) |
| 5 | README / docs | Purpose only (Step 1) — never trust docs for mechanics |

**Rules:** Cite `file:line` for every flow hop and contract. When docs and code disagree, the code wins — note the drift. Use the `task`/explore tooling for open-ended search; use direct reads for specific files.

---

## Present Results to User

Assemble the knowledge map using `references/output-template.md`, presented top-down:

1. **The one-sentence purpose** (Step 1) — pain + promise.
2. **Topography diagram** (Step 2) — ASCII dependency graph, leaves → roots.
3. **Core-flow diagram(s)** (Step 4) — one ASCII sequence per primary flow.
4. **Data-model & contracts table** (Step 5) — core nouns + the API/protocol surface.
5. **Seams & invariants** (Step 6) — the rules, each with its breakage consequence.
6. **The chosen track's deliverable** (Step 7).

Always end with the **load-bearing-walls statement**:
> "The essential complexity of this project is [X] — that is what any version must preserve. Everything else ([list]) is a swappable implementation choice."

This single sentence is the payoff: it is simultaneously the contributor's "don't break this" and the rebuilder's "keep this, swap the rest."

---

## Troubleshooting

**"The project is huge — where do I start?"**
- Do Steps 1–2 fully first; they bound the problem. Then ask the user which *flow* matters most and deep-trace only that one in Step 4.

**"There's no README / docs."**
- Skip to Step 2 (manifests never lie). Infer purpose from the entry points and the primary flow, then state it as a hypothesis for the user to confirm.

**"Two parts of the code look identical."**
- That is almost always a mirrored-implementation invariant (Step 6). Confirm whether a script generates one from the other, and flag "change both" as a rule.

**"The user wants me to just start coding the rebuild."**
- Resist until Steps 1, 2, 5, and 6 are done. The load-bearing-walls statement is what prevents rebuilding accidental complexity. A rebuild without it is just a slower copy.
