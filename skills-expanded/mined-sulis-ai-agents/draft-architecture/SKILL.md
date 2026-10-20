---
name: draft-architecture
description: "Turns a requirements document into a technical blueprint."
---

# Blueprint — Greenfield Technical Design

When invoked, produce a Technical Design Document and supporting ADRs for a
project, driven by the upstream SRD specification.

If arguments are provided, treat them as the path to the spec folder (e.g.
`/sulis:draft-architecture .specifications/payments-service`). If no path is provided,
use the most recently modified folder in `.specifications/`.

If no SRD specification exists, stop and tell the user — refer them to
`srd:requirements-analyst`. **Do not invent requirements.**

---

## Required Reading (load before drafting)

These standards shape the TDD + the new contract artifacts (step 3.5):

<!-- VERIFICATION_QUESTIONS source: plugins/sulis/references/standards/VERIFICATION_QUESTIONS.md v1.0.0 -->

- `../../references/standards/VERIFICATION_QUESTIONS.md` — the canonical
  20-question set (foundational Q1-Q4 + per-integration Q5-Q13 + per-kind
  Q14-Q20) and the seven-row kind→adapter table. The TDD this skill
  produces MUST carry a populated `## Verification Plan` section
  (literal heading per ADR-001) with six subsections referencing
  questions by ID, never inlining them. The engineering-architect agent
  is the one that walks the questions; this skill is the orchestrator
  that ensures the resulting TDD section is present and that **P-VER**
  is invoked against the TDD before stage completion (FR-002, FR-009).
  Cross-reference: [`ADR-001`](../../../../.architecture/verification-by-design/adrs/ADR-001-section-name-verification-plan.md)
  fixes the section name; [`decompose-validation-rubric.md`](../../references/decompose-validation-rubric.md)
  §Phase 9 hosts the P-VER check.
- `../../references/standards/CONTRACT_FIRST_STANDARD.md` — the **data
  contract** seam discipline (two-axis model, three-category error model,
  stubs include error/empty cases, transport binding).
- `../../references/standards/UX_VISUAL_DESIGN_STANDARD.md` — the **visual
  contract** (Identity/Visual/Experience/Governance layers + the agentic-
  interface principles for AI surfaces); produced as a design-time artifact
  per UXD-14.
- `../../references/standards/WP_BACKEND_STANDARD.md` — backend patterns
  the TDD's backend components implement (ports & adapters, repository,
  handler, in-memory adapter first, etc.).
- `../../references/standards/WP_FRONTEND_STANDARD.md` — frontend patterns
  the TDD's user-facing components implement (component tiers, typed client,
  loading/error/empty, design tokens, agentic UX).
- `../../references/standards/WORK_PACKAGE_STANDARD.md` — the `kind:` enum
  (incl. `kind: contract`) and the cross-kind decomposition WP-08.5 that
  `plan-work` will apply to the TDD this skill produces.

---

## Inputs You Read

**Read in this order. Context index first — it constrains everything else.**

| File | Why |
|---|---|
| `.context/{project}/INDEX.md` (sulis-context v0.1.0+) | **Read first.** Authoritative sources to reference (not restate); External ADR Registry's highest ADR number (so new ADRs start at N+1); Known Gaps (your licence to add new artifacts). Apply Respect-Don't-Restate to everything that follows. |
| Authoritative sources listed in the index | Load on demand when their topic is touched by your TDD work |
| `SRD.md` | Functional requirements, use cases, business rules, per-use-case Negative Requirements → Form pillar (and seeds Armor) |
| `NFR.md` | Non-functional requirements → drives Armor pillar + pattern selection |
| `MISUSE_CASES.md` (SRD v1.11.0+) | Abuse cases, misuse flows, **System Response (REQUIRED)** for each → seeds Armor primitives (rate limits, audit logging, replay protection, integrity guards) and shapes the TDD's security boundary |
| `PRIMITIVE_TREE.jsonld` | Structural decomposition of building blocks → component inventory |
| `GLOSSARY.md` | Locked vocabulary from SRD Phase 3.5 Disambiguation Sweep — use preferred terms exactly in the TDD and ADRs |
| `.architecture/{project}/probe-raw/synthesis.json` → `reserved_vocabulary_hint` | YAML kinds in use + universally K8s/Sulis-reserved words. Feeds the Reserved-Vocabulary Sweep at step 7. If the field is missing, the probe is older than v0.9.1 — recommend re-running. |
| `diagrams/*.md` | Sequence, process, data-flow diagrams → integration design |
| `EXPLORATION_JOURNAL.md` `## Deferred to SEA` (if present) | Architecture-and-implementation content parked by SRD mid-session — treat as additional design intent from the user |
| `HANDOVER.md` (if present) | Suggested implementation sequence → may inform WP ordering |
| `HANDOFF_TO_SEA.md` (if present, instead of SRD.md) | SRD took the Early Handover path — user arrived with predominantly technical content. Read it as the sole upstream context; fill business-intent gaps by asking the user, not by inventing. |

Read all of them. If any are missing, list them and ask the user how to
proceed before writing anything.

**Context index is required reading when present.** If `.context/{project}/INDEX.md`
exists and you do not read it, you will produce TDD content that restates or
contradicts existing authoritative sources. The auto-suggest in the agent's Phase 0
check should have either loaded the index or surfaced the "continue without context"
override before you got here — but if you somehow find yourself in blueprint with no
loaded index on a non-trivial codebase, stop and surface that.

**MISUSE_CASES.md is required reading when present.** Each MUC's System Response
becomes Armor input. Skipping it means you write a TDD that addresses the happy
path but not the adversarial path SRD already specified.

---

## Outputs You Write

```
.architecture/{project}/
├── ARCH.yaml
├── TDD.md
├── service-specs/
│   ├── {service-name}.servicespec.yaml   # one per service introduced/modified — emitted in step 10
│   └── ...
└── adrs/
    ├── ADR-001-{slug}.md
    └── ...

.brain/instances/product-development/
└── decision/
    └── {ulid}.jsonld          # one per ADR — emitted in step 9
```

Every ADR has a paired structured **Decision** entity under
`.brain/instances/`. The `.md` is the human view; the `.jsonld` is the
machine-readable spine — what tooling, cross-references, and the
golden-thread query layer read. Pairing is one CLI call per ADR (see
step 9).

**Every service the design introduces or modifies has a paired
ServiceSpec manifest** under `service-specs/` (see step 10). The
manifest is the platform's contract for that service — operations,
errors, entities, bindings, permissions — and is what the platform's
service-registration apply pipeline (SPEC-006) reads. The TDD describes
*what to build*; the ServiceSpec describes *what the built service
exposes to AI agents and SDKs*. Without it, the design has no machine-
readable service contract and downstream — agent integration, SDK
generation, MCP routing, the cockpit's service view — has nothing to
bind to. This is the third design-stage structured deliverable
alongside the visual contract (`UX_VISUAL_DESIGN_STANDARD`, #45) and
the data contract (`CONTRACT_FIRST_STANDARD`, #48).

### `ARCH.yaml`

```yaml
id: ARCH-001
title: Payments Service Architecture
status: designed                 # draft | designed | decomposed | implemented | verified
sourced_from: ../../.specifications/payments-service/SPEC.yaml
created: 2026-05-12
pillars:
  form: covered
  armor: covered
  proof: covered
```

### `TDD.md` — Required Sections

The TDD has a fixed structure. Each section maps to MECE-3 pillars. See
`references/tdd-template.md` for the full template; the headline structure is:

1. **Overview** — one-paragraph summary of what is being designed and why.
2. **Source Specification** — link to `SRD.md`, `NFR.md`, key requirements.
3. **Form — Structural Design**
   - Component inventory (from `PRIMITIVE_TREE.jsonld`)
   - Module boundaries and dependency graph
   - Ports (interfaces in the domain)
   - Adapters (implementations in infrastructure)
   - Composition root layout
4. **Armor — Operational Hardening**
   - External dependency table — every cross-process call lists timeout, retry policy, circuit-breaker config
   - Security boundary — what's authenticated, authorised, encrypted (mTLS, TLS, at-rest)
   - Secrets — where they live, how they rotate
   - Observability — trace coverage, log structure, metrics (RED per operation, USE per resource)
5. **Proof — Verification Protocol**
   - Contract tests per port
   - Integration tests against real adapters (testcontainers, ephemeral DBs)
   - Chaos assertions per resiliency primitive
6. **Trade-offs** — patterns chosen, alternatives rejected, with one-line reasons
7. **Open questions** — anything the SRD does not specify that the architecture needs
8. **Canonical Identifiers** *(if any cross-WP identifiers are foreseen)* — when the design foresees parallel WPs cross-referencing a shared identifier (ULID, slug, version literal, namespace, `dna:*:*` shape), pre-mint that identifier here OR author a paired `ADR-NN-canonical-identifiers.md`. Document the minting recipe (e.g. `SHA256(name) → Crockford base32`) so a future regenerate produces the same value. Without this, parallel-dispatched executors each invent their own value and they diverge — anchor case CH-01KSZ4 release-train wave-1 tenant ULID. `/sulis:plan-work` step 7c + Decompose Validation Rubric Phase 8 are the downstream gates that catch a missing canonical source.
9. **`## Verification Plan`** *(MUST — verbatim heading per ADR-001)* — the design-time commitment to how this work will be verified. The six required subsections, in order: (1) "What user-observable behaviour are we verifying?" — populated from the foundational Q1-Q4; (2) "Verification environment(s)" — local / staging / ephemeral / production-shadow; (3) "Bootstrap-from-zero case" — what verification looks like before any data exists (the anchor failure mode for the release-train + discovery dogfood incidents that motivated this change); (4) "Per-integration verification strategy" — per-touched-integration verdict against Q5-Q13 (real / recorded / simulated / none-with-justification); (5) "Per-kind verification adapter" — the one-liner from the seven-row table in `references/standards/VERIFICATION_QUESTIONS.md` for this change's `kind:`; (6) "Infrastructure needs surfaced (deferred)" — entries that ADR-005's slice-end auto-draft picks up to create follow-on changes. The engineering-architect agent populates this section from the canonical's question set; this skill's Workflow step (after pillar coverage) invokes **P-VER** against the produced TDD before stage completion.

### ADRs

Emit one ADR per non-trivial decision. "Non-trivial" means: the decision
affects more than one component, locks in a technology choice, or rejects
a viable alternative.

**ADR numbering (MUST):** If `.context/{project}/INDEX.md` exists and contains
an External ADR Registry with `Highest ADR number: ADR-N`, your new ADRs MUST
start at `ADR-{N+1}`. Reading the index's External ADR Registry section gives
you this number directly. Do not start at ADR-001 unconditionally — that
collides with the existing registry and produces ambiguous references.

**Before writing each ADR, check the External ADR Registry for an existing
ADR on the same topic.** If one exists:

- If your decision **aligns** with the existing ADR: don't write a new ADR.
  Reference the existing one in your TDD instead.
- If your decision **extends** the existing ADR: write a new ADR with
  `extends: external:ADR-NN` in frontmatter, and explain in Context what's
  new.
- If your decision **supersedes** the existing ADR: write a new ADR with
  `supersedes: external:ADR-NN` in frontmatter. Surface the supersession to
  the user before finalising — the team owns its existing decisions, and you
  shouldn't quietly overrule them.

ADR file format:

```markdown
---
id: ADR-023
title: Use PostgreSQL with logical replication for the order store
status: accepted              # proposed | accepted | superseded
date: 2026-05-14
deciders: [iain]
supersedes: external:ADR-007  # optional — when overriding an existing ADR
extends: external:ADR-012     # optional — when extending an existing ADR
---

## Context
{What forced the decision; constraints from NFR/SRD; existing system shape.
If extending or superseding, reference the existing ADR by path.}

## Decision
{One paragraph stating the choice in active voice.}

## Options Considered
- PostgreSQL with logical replication — chosen
- DynamoDB — rejected because {reason}
- MySQL — rejected because {reason}

## Consequences
- Positive: {what becomes easier}
- Negative: {what becomes harder; what new operational concerns appear}
- Neutral: {what stays the same}
```

---

## Workflow

0. **Load the context index (if present).** Read `.context/{project}/INDEX.md` first.
   Parse Authoritative Sources, External ADR Registry, Conventions & Standards,
   Patterns Library, Known Gaps. Hold these in working memory — every subsequent
   step respects what you found. If the index is missing and the codebase has
   signals of existing architecture material, stop and recommend
   `/sulis:discover-context` (the agent's Phase 0 check should have done this
   already — if you got here without an index on a non-trivial codebase, surface
   that).
1. **Discover** — locate the spec folder; read all inputs in the table above; report what's missing. If `HANDOFF_TO_SEA.md` is present and `SRD.md` is absent, read the handoff file first and ask the user for any business intent it doesn't capture before proceeding.
2. **Inventory** — parse `PRIMITIVE_TREE.jsonld` for components. List them. Map each to a TDD section.
3. **Compute SIZING.md (MUST).** Per `references/right-sizing.md`:
   - **If `.architecture/{project}/SIZING.md` already exists and is current**
     (all source artifact mtimes are older than SIZING.md's `Generated`
     timestamp): read it, honour the recorded tier, skip to step 4.
   - **Otherwise**, compute sFPC + ASR + per-pillar coverage:
     - sFPC: count ILF (PRIMITIVE_TREE domain-entity + data-store nodes) +
       EIF (integration nodes) + EI/EO/EQ (use cases classified by whether
       their flow mutates / derives / retrieves)
     - ASR: count NFRs + integrations + MUCs + cross-cutting policies +
       hard data constraints
     - Pillar coverage: from `.context/{project}/INDEX.md` Authoritative
       Sources — judge whether Form, Armor, Proof are fully / partially /
       uncovered for the work in scope
     - Tier: from the table in the standard (take higher of sFPC-tier and
       ASR-tier; promote to XL on multi-bounded-context)
   
   **Decide the tier, record it, announce its meaning, and proceed
   (decide-and-report).** The tier is a deterministically-computed
   engineering call the agent owns — a non-technical founder cannot ratify
   "sFPC ≈ 31, ASR ≈ 56, Tier XL", so do NOT put the raw numbers to them as a
   confirm-or-override gate (that's the permission-theatre AAF-08 forbids).
   Write the full sFPC + ASR + pillar breakdown into `SIZING.md` (the
   artifact + technical-mode carry the numbers); then announce to the founder,
   in plain English, only what the tier *means for them* — the size of the
   build — and proceed:

   > "This is a {small / medium / large / very large} build — roughly {N}
   > pieces of work, so I'll size the design to match. Shout if you'd rather
   > start with a smaller first version."

   The founder can redirect the size *after* (down to a spike; up for a
   growth-projection / junior-team / regulatory context) — the override never
   needs pre-asking. Record the tier (computed, or founder-redirected) and
   write `.architecture/{project}/SIZING.md` per the schema in
   `references/right-sizing.md`.

   **Scope posture (MUST — see the Sulis body "Scope Posture").** The tier
   sizes *how much design rigour* the work warrants — it does **not** license
   shrinking the *scope delivered*. Default to designing the **full coherent
   scope** of what's asked; a large tier means "design it properly," not
   "deliver less." The "smaller first version" above is a *founder-initiated*
   redirect, never the agent's reflex. If the scope is genuinely too big to
   hold in one go, **you** propose a phased plan (phase 1 a real go; the rest
   captured to the backlog) — never hand the slicing to the founder.

   (Operator-facing invocations — `--raw` / `/sulis:jargon on` — may still see
   the full sFPC/ASR proposal; founder-mode gets the plain size sentence.)
3.5. **Define the contracts (MUST when cross-kind or user-facing).** Before
   pillar design, identify the **producer/consumer seams** in the proposed
   architecture and the **user-facing surfaces**. For each, produce a
   contract artifact as a design-time deliverable — the same way the TDD is.

   **(a) Data contracts** — per
   [`CONTRACT_FIRST_STANDARD.md`](../../references/standards/CONTRACT_FIRST_STANDARD.md).
   For every backend↔frontend seam (or tool↔caller seam) in the TDD, produce
   a schema sketch:
   - **operations** (named units the seam exposes)
   - **input + output types** (named, reusable; not inline-per-endpoint)
   - **the three error categories** (Protocol / Expected / Internal per CF-03)
     mapped to the chosen transport (HTTP statuses / NDJSON event types /
     subprocess exit codes / library exceptions)
   - **example stubs** covering **happy + error + empty** cases (CF-04)
   - **the transport binding** (HTTP/REST + OpenAPI 3.1 for web seams;
     JSON-RPC/MCP for agent tools; subprocess+NDJSON for streaming local
     pipes; library for in-process)
   - **operational + founder-facing semantics per operation (CF-10)** — not
     only schemas: **auth/permissions**, **audience** (admin/operator vs
     founder), a **plain-language guide** (what it does, when to use,
     prerequisites, next steps), and **error fixes** (cause + user/developer
     action). These are the ServiceSpec dimensions; where the project
     produces ServiceSpecs, that IS the contract. MUST for any contract a
     founder reviews — it is what makes the contract founder-reviewable
     (rendered by the cockpit preview, #85), not just engineer-integratable.

   Write the contract sketch to `.architecture/{project}/contracts/{seam}.md`
   (or `.yaml`/`.json` if you can already commit to OpenAPI/JSON Schema at
   this stage). `plan-work` will emit a `kind: contract` WP from it (WP-08.5)
   so the build conforms.

   **(b) Visual contract (MUST for any user-facing surface)** — per
   [`UX_VISUAL_DESIGN_STANDARD.md`](../../references/standards/UX_VISUAL_DESIGN_STANDARD.md).
   This is a **hard gate** (#45): if the TDD has any user-facing surface, the
   visual contract is mandatory and `plan-work` cannot emit frontend WPs
   without it (the toolchain enforces this — see below).

   **Dispatch the `ux-designer` specialist — do NOT produce the visual contract
   inline (MUST).** The visual contract is owned by the `ux-designer` agent the
   way the SRD is owned by the requirements-analyst: it runs the inspiration
   probe, produces the real-token HTML mockup, takes the accessibility
   decisions, and **facilitates the founder's sign-off** (the most founder-
   facing review there is). Hand it the surface + the project's design instance:

   ```
   Agent({
     subagent_type: "sulis:ux-designer",
     description: "Design the {surface} screen + get your sign-off",
     prompt: "Produce the visual contract for {surface} (part of the {project}
              design). Read the TDD's user-facing surface description + the
              project's design instance. Run the inspiration probe, produce the
              real-token mockup at contracts/visual/{surface}.html, verify
              accessibility, and facilitate sign-off. Return the visual-contract
              WP fields (mockup path, inspiration, signed_off_at, provenance)."
   })
   ```

   The architect's job here is to **identify the surface(s)** + hand off; the
   `ux-designer` owns the contract. The detail below (the four layers + the
   Mobbin probe + the mockup) is that agent's contract — kept here as the spec
   it produces against (and as the fallback if `ux-designer` is unavailable, in
   which case produce it inline per the steps below and note the deviation).

   **If the surface renders inside an AI client (MCP App / Artifact), write an
   ADR for the rendering path (MUST).** Choosing Artifact vs MCP App vs MCP-UI
   `externalUrl` is an **architecture** decision — driven by data-connection +
   durability, not styling — so it belongs in an ADR, not buried in a WP. See
   [`mcp-ui-surface-patterns.md`](../../references/mcp-ui-surface-patterns.md)
   for the decision rule + the `ui://` contract shape. (Ephemeral Artifact for
   in-session output with no live data; MCP App for a durable, data-connected,
   reusable surface; `externalUrl` to embed an existing web app.)

   **(i) The contract record + mockup.** Cover the four layers' essentials:
   - **Identity** (referenced — not re-articulated here) — point at the
     project's identity artifacts; flag if missing.
   - **Visual** — the token tiers the surface will consume (semantic +
     component tokens, not raw values); brand traits → measurable visual
     parameters; the structural profile (navigation / layout / density /
     elevation).
   - **Experience** — the HIG sections needed (the surface's components +
     their variants/states/focus + the three UI states loading/empty/error);
     accessibility decisions taken at design time (AA contrast on the
     chosen token pairs; keyboard model; colour-independence check); if
     the surface is AI-facing, the agentic-interface principles in play
     (UXD-10: outcome-oriented, human-in-the-loop gates, transparency).
   - **Governance** — provenance label on the artifact.

   **Run the Mobbin inspiration probe FIRST (UXD-15 — gated on MCP
   availability).** Before producing the mockup, search Mobbin for real-world
   patterns matching this surface so the mockup is grounded in what's been
   shipped, not invented in isolation. Strict scope: **structural patterns
   are transferable; visual choices are NOT** — our tokens, type stack, and
   identity stay authoritative (UXD-15).

   1. **Detect availability.** Probe the Mobbin MCP (e.g.
      `mcp__plugin_honest_mobbin__search_screens` if connected via the honest
      plugin, or a sulis-native equivalent). If unavailable or unauthenticated:
      log one line ("Mobbin: MCP unavailable, skipping inspiration probe —
      mockup will proceed without external references."), set
      `inspiration: none` on the visual-contract WP, and continue. **Never
      fabricate references** — no MCP = no `_mobbin-context.md`.
   2. **Query.** Compose a search from the surface description (e.g.
      "settings screen with org switcher") + the change intent. Cap results
      to ~6; keep 2–3 most relevant.
   3. **Capture per reference.** App name, Mobbin URL, 2–4 *structural*
      observations (transferable — section ordering, density, spacing rhythm,
      micro-interaction beats) and the *visual* observations explicitly marked
      NOT transferable (our tokens authoritative).
   4. **Synthesise.** Write a 2–4 line paragraph extracting the cross-cutting
      structural patterns the mockup should consider folding in.
   5. **Worked-example carve-out.** If the project's own design-instance
      `reference/` or `examples/` already covers this surface tightly, log
      "Worked example covers this surface; skipping Mobbin probe" and skip.
   6. **Persist** the probe output to
      `.architecture/{project}/contracts/visual/_mobbin-context.md`. Because
      `.architecture/` travels with the change branch (#42), the research is
      durable and discoverable — `review` can later verify the shipped surface
      honoured the inspiration cited here. The visual-contract WP's
      `inspiration:` frontmatter field cites the relative path so the link
      is explicit.

   **(b.ii) Produce the real-token HTML mockup** at
   `.architecture/{project}/contracts/visual/<surface>.html` — composed
   page(s), the product's actual design-instance tokens (never invented hex),
   and **the webfonts its type tokens reference actually loaded** (L-13: a
   mockup whose fonts don't load passed "tokens match" while the founder saw
   no brand — sign-off is *visual*, not value-equality). The mockup's
   **structure** may reflect the Mobbin synthesis (section ordering, density,
   spacing rhythm); the mockup's **visual identity** stays bound to the
   design instance — never embed Mobbin screenshots and never adopt their
   palettes/type stacks. Note the perceptual delta vs the current surface so
   the founder can see what changes.

   **(b.iii) The visual-contract WP.** Emit a WP with frontmatter:
   ```yaml
   kind: contract
   contract_type: visual          # marks it as the visual-contract WP
   mockup: contracts/visual/<surface>.html
   inspiration: contracts/visual/_mobbin-context.md   # or "none" if MCP unavailable
   signed_off_at:                 # EMPTY until the founder signs off
   provenance: draft              # → production-approved on sign-off
   ```
   `plan-work` makes every `kind: frontend` WP carry `visual_contract: <this
   WP id>` and `dependsOn` it; the WP only reaches `done` once `signed_off_at`
   is set + `provenance: production-approved` (enforced at `wpx-index
   flip-status`). So no frontend WP is dispatchable until the founder has
   signed off the rendered mockup.

   Identity/brand *values* (palette, type, look-and-feel) remain
   founder-owned — if absent, STOP, surface as the first Open Question, and
   route to the design flow rather than inventing them.

   **(c) Platform contract (MUST for any gated third-party touch)** — per
   [`PLATFORM_CONTRACT_STANDARD.md`](../../references/standards/PLATFORM_CONTRACT_STANDARD.md).
   The fourth design-stage contract: where the data contract governs the
   backend↔frontend seam and the visual contract governs the user-facing
   surface, the **platform contract** governs the seam between this design and
   a *third-party platform* it integrates with (GitHub Actions, Stripe, an
   email provider, a cloud API). It is our outside-in, evidence-grounded record
   of how that platform actually behaves — every rule bound to the platform's
   own documentation, the load-bearing ones confirmed by a probe — so we
   conform to the platform's real contract instead of assuming it and
   discovering the gap at runtime (the failure that drove #137).

   **Gate the touch by what it does to the platform (ADR-001):**
   - **write / deploy touch → hard-gate.** Design does not proceed until a
     Platform Contract covering the platform exists at
     `plugins/sulis/references/platform-contracts/{platform}.md` (or is produced
     now via the harness step below). The block is founder-readable — name the
     platform and the file to produce, no internal IDs:
     *"This change writes to {platform}. I need a Platform Contract for it first
     — I'll ground one against {platform}'s own docs before we build."*
   - **read-only touch → soft-recommend.** Note that a lightweight contract is
     advisable; do not block.
   - **escalation override:** a read-only touch that *informs a write/deploy
     decision* may be escalated to hard-gated with a one-line note;
     de-escalation requires a superseding ADR (ADR-001).

   **Produce the contract by running the faithful-generation-harness — do NOT
   hand-author it (FR-003 / ADR-004):**
   1. Dispatch the harness via `/sulis-brain:execute-workflow` (the
      `faithful-generation-harness` Workflow) against the platform's **official
      documentation as the closed manifest**. The harness binds every generated
      claim to a source, flags inferences, and refuses on ungrounded claims.
   2. Land the harness's committed claim→source binding table **as the contract
      body** — one binding becomes one claim entry; flagged inferences become
      `inferred: true` entries — per the step→artifact mapping in ADR-004 (do
      not restate the harness's internal steps here).
   3. Record the harness-run reference (`run_id`) in the produced contract's
      front matter (the provenance P-PLAT checks; A-8), and add the contract's
      row to `platform-contracts/INDEX.md`.
   4. **Cross-repo handling (OAQ-1 / ADR-004):** the harness is an `existing`
      sibling-repo Workflow. If the sibling repo is unresolvable, **emit a
      BLOCKER** — do **not** fall back to hand-authoring a contract. A
      hand-authored contract would carry no grounded provenance and defeat the
      whole mechanism.

   **(d) Verification scenarios (MUST for any user-facing or behavioural
   change)** — define the change's `Scenario` entities up front, as living
   graph entities (NOT a change-dir file). A `Scenario` is a reusable,
   founder-legible verification case: it **`verifies → Requirement[]`**,
   **`exercises → Design`**, and **`journey → Workflow`** (a graph of IDEF0
   `Step`s — e.g. *sign up → log in → see dashboard*). Each Step carries its
   `mechanism` (`deterministic` → a command the runner runs; `human` → a manual
   checklist item), `input_artifacts` (the needs/credentials — a missing one
   becomes a `deferred:<need>` at run time), and `preconditions`/`postconditions`
   (the asserts). These are the cases the testable-state DoD gate runs against a
   standing app (`sulis-verify-acceptance`) so "done" means *the app is
   testable*, not *merged*. Author them so a non-technical founder can read the
   title + steps and run them. (A change with no user-facing or behavioural
   surface — pure docs/infra — is exempt; log `scenarios: exempt — <reason>`.)

   **(e) Single-kind non-visual work + `--prototype` changes are exempt** from
   the visual-contract step (the gate honours a `prototype: true` WP and a
   logged `visual_contract: exempt — <reason>`). A change that touches **no**
   third-party platform is likewise exempt from the platform-contract gate.

4. **Select patterns** — for each NFR, pick patterns from `references/architecture-patterns.md`. Surface trade-offs explicitly. Skip pattern selection for any pillar marked "fully covered" in the sizing announcement; reference the authoritative source instead.
5. **Translate misuse cases** — for each MUC in `MISUSE_CASES.md`, translate its `System Response (REQUIRED)` into one or more Armor-pillar primitives in the TDD. Cross-reference: every MUC ID must appear in the TDD's Armor section. See `references/hardening-deltas.md` for the MUC → delta/primitive translation pattern (the same translation applies to greenfield TDD entries).
6. **Cover all three pillars at tier-appropriate depth.** For every component, ensure Form, Armor, and Proof are addressed. Per the sizing decision:
   - Fully covered pillar → one line + reference to the authoritative source
   - Partially covered pillar → section addresses only the gap
   - Uncovered pillar → full tier-sized section per `references/right-sizing.md`
   If you cannot address one pillar for a component, flag it in Open Questions; do not silently skip.
7. **Reserved-Vocabulary Sweep (MUST).** Before naming abstract types, classes, registries, or dispatch keys in the TDD, run this check. It catches polysemy collisions between proposed design vocabulary and infrastructure-coded vocabulary already in use in the repo. The kind/Kind collision (a generative-pipeline abstract sharing a name with the Sulis YAML discriminator) is the canonical failure mode this step exists to prevent.

   a. **Load reserved words.** Read `.architecture/{project}/probe-raw/synthesis.json`'s `reserved_vocabulary_hint` block (emitted by `/sulis:analyse-codebase` v0.9.1+). It contains:
   - `yaml_kinds_in_use` — every value seen in `apiVersion: <x>` / `kind: <y>` pairs across the repo (Sulis kinds, k8s sub-kinds, Argo, Flux). These are reserved because re-using one of these names imports its dispatch shape.
   - `infrastructure_reserved` — universally K8s/Sulis-coded words (`kind`, `apiVersion`, `metadata`, `spec`, `status`, `apply`, `reconcile`, `manifest`, `resource`).
   
   If the hint is missing (older probe output), recompute it on the fly by reading `1_16_deployment.json` directly, or surface the gap and recommend re-running `/sulis:analyse-codebase`.
   
   Also load `GLOSSARY.md` (if present) — its preferred-terms list is already a vocabulary lock.

   b. **List proposed abstracts.** Enumerate every new abstract type, class, registry, or dispatch concept the TDD will introduce. For tier-S this is usually 3-8; for tier-XL it can be 20+.

   c. **Score each proposed abstract against the reserved set.** For every proposed abstract `P`:
   - If `P` does not appear in `yaml_kinds_in_use` or `infrastructure_reserved` and is not flagged in GLOSSARY: proceed.
   - If `P` matches (case-insensitive) any reserved word: trigger the lifecycle check below.

   d. **4-cell lifecycle check.** For each colliding name, fill this table — for both the existing manifest resource and the proposed abstract:

   | Question | Manifest resource `kind: X` | Proposed abstract `X` |
   |---|---|---|
   | Does it persist (DB/repo-stored)? | yes/no | yes/no |
   | Does it converge (drift-reconciled)? | yes/no | yes/no |
   | Does it have a natural key? | yes/no | yes/no |
   | What does `apply -f X.yaml` mean? | bring resource into desired state / invoke a pipeline / N/A | … |
   | Delete semantics? | convergent / explicit-only / N/A | … |

   e. **Decision rule (MUST):**
   - **All five cells match** → proceed; the shared name reflects shared semantics. Note in the TDD that the dispatch is intentionally shared.
   - **Any cell diverges** → BLOCK. The agent MUST do one of:
     1. **Rename the proposed abstract.** Pick a name that anchors on what's distinct (e.g. Kind → Recipe because the abstract is "instructions for producing", not "type of thing"). Update GLOSSARY.md with a "Where else this word appears" note on the old term.
     2. **Write an ADR justifying the shared dispatch.** Cite the lifecycle differences explicitly; explain why the runtime path is genuinely the same despite different semantics. This is the rare case (e.g. when the new abstract is genuinely a new manifest resource).
   - **Do not proceed to TDD draft until the table is filled and the decision recorded** for every collision.

   f. **Report the sweep result in the TDD's "Open Questions" or "Design Decisions" section.** Even when no collisions were found, the report demonstrates the check ran: "Reserved-Vocabulary Sweep: {N} proposed abstracts checked against {M} reserved words; no collisions found."

8. **Draft TDD** — write `TDD.md` following the template. Use GLOSSARY.md's preferred terms exactly. Apply Respect-Don't-Restate throughout.

8.5. **Walk the journey (MUST for any user-facing / behavioural change).**
   Before the design is "done" and hands off to `plan-work`, walk each
   verification `Scenario`'s journey **outside-in, hop-by-hop, against the
   actual code + the TDD you just drafted.** This is the design-stage forcing
   function that catches "a hop of the round-trip was never built" *here*, not
   after deploys — the failure mode behind four green-but-broken login
   attempts (the consumption half of the journey didn't exist). It is the
   mechanical form of Outside-In (OI) + Work-Backwards: the design isn't
   complete until the *whole* user round-trip is built-or-planned.

   **(a) Pull the journey's COMPLETE scenario set — not just what you're
   building.** A journey is a `Workflow`; each `Scenario` carries
   `journey → dna:workflow:<ulid>`. Enumerate the full set:

   ```
   python3 -c "import sys; sys.path.insert(0,'<SCRIPTS_DIR>'); \
     from _brain_query import find_scenarios_for_journey; \
     print([s['id'] for s in find_scenarios_for_journey('<base-dir>', '<journey-workflow-id>')])"
   ```

   (`find_scenarios_for_journey` / `find_scenarios_verifying` —
   `plugins/sulis/scripts/_brain_query.py`.)

   **(b) For each Scenario, walk its journey Steps in order** — the user's
   first action → every hop → the final observable result (e.g. *click sign-in
   → redirect → callback → token → session → stay-signed-in → an authenticated
   call returning real data*). For **every hop**, name the component that
   handles it and assert it **exists** — cite the file + function in the
   codebase, OR a TDD component / WP-to-be that will build it. A hop with
   neither an existing component nor a planned one is a **GAP**.

   **Sharper "exists" for a host-rendered / integration hop (MUST).** When a hop
   crosses a seam into a host or platform you don't control — a host-rendered
   surface (MCP App / OpenAI App / figma-plugin / browser-extension), or any
   third-party protocol round-trip — "exists" is **NOT** satisfied by a serving
   endpoint, rendering HTML, or a passing unit test. It requires: (1) the
   protocol binding cited in code on **both** sides of the seam (e.g. for
   MCP-Apps: server `_meta.ui.resourceUri` + the host's accepted MIME; client the
   ext-apps runtime `app.connect`/`ontoolresult`/`callServerTool`/`openLink`),
   **and** (2) the round-trip **observed — or attested via
   `sulis-attest-scenario` — in the real host**, planned as the hop's proof. A
   surface that serves but isn't bound, or whose buttons only flip local state,
   is a **GAP**, not "exists." See
   [`mcp-ui-surface-patterns.md`](../../references/mcp-ui-surface-patterns.md)
   § "Done = wired + legible" for the full gate (incl. the legibility metadata:
   `title` + one-line `description` + `icon`, not a technical `name` alone).

   **(c) Classify every scenario in the set** (so ALL are checked even when
   only some are built): **covered-this-change** (its gaps become WPs) /
   **already-green** (confirm via `find_passing_testresults_for_scenario(<id>)`
   — a passing TestResult back-links it) / **GAP → WP** / **explicitly
   out-of-scope (RECORDED, never silently dropped)**.

   **(d) Write the walk to TDD.md** as a `## Journey Walk` section: per
   scenario, a hop-by-hop table `hop | component (path) | status
   (exists / planned-WP / GAP)`, plus the scenario-set classification.

   **(e) GATE (MUST).** The design is not complete — `plan-work` does not
   start — until *every hop of every in-scope Scenario* is **exists** or
   **planned-WP**, and every journey scenario is classified. A bare `GAP`
   (a hop neither built nor planned) blocks design completion; turn it into a
   planned WP or an explicit, recorded out-of-scope decision. **For a
   host-rendered / integration hop, "exists" means the sharper bar above
   (binding both sides + real-host round-trip), not a serving endpoint** — an
   unbound surface that merely serves is a GAP that blocks here. (Pure docs/infra
   change with no user-facing surface: exempt — log `journey-walk: exempt —
   <reason>`, mirroring the scenario-authoring exemption in step 3d.)

   **(f) SECOND PASS — walk the TOOL surface (MUST for any change with a tool
   surface).** Steps (a)–(e) above walk the **UI** surface — the human
   consumer's path. Now run the *same procedure a second time* over the **tool**
   surface — the machine consumer's path (the API / SDK / MCP operations the
   change exposes). This is the second pass of ADR-003: not a new walk
   mechanism, the *same* outside-in, hop-by-hop existence check applied to the
   machine consumer.

   - **Source of operations:** the walk's tool operations are drawn from the
     **interface-contract section** (`## Interface Contract` / ServiceSpec,
     FR-18). Per FR-19 every walked operation MUST appear in the contract — the
     walk is a *subset* of the contract, never inventing an operation the
     contract never declared. (`plan-work`'s WP-013 enforces walk ⊆ contract
     mechanically; here you draw *from* the contract.)
   - **The sharper "exists" bar for a tool hop (FR-09 / NFR-S02, MUST).** A tool
     operation is **exists** only when **BOTH** are cited: (1) the **handler**
     (the file + function that serves the operation) **AND** (2) its
     **ServiceSpec binding** (the `bindings:` entry — host/basePath/method/auth —
     that wires the handler into the contract). A handler that merely *serves* —
     with no binding — is a **GAP**, never exists. This is the **generalisation
     of the host-rendered bar** in (b): the same "wired, not just serving"
     discipline, applied to every tool operation (so the false-EXISTS bypass is
     closed on the machine path too, MUC-02). A planned WP for a still-unbuilt
     operation is **planned-WP**.

   **(g) Write the SECOND table + GATE (MUST).** Write a **second**
   `## Journey Walk` table for the tool surface alongside the UI one — **both
   tables persist** in the document (NFR-D02). The same gate applies: a bare
   `GAP` in *either* table (UI or tool) blocks design completion. Mechanise the
   check with the walk scripts:

   ```
   # Drive each surface (writes a `## Journey Walk` section per surface):
   python3 <SCRIPTS_DIR>/_drive_journey_walk.py --fixture <walk> --surface ui   --out DESIGN.md
   python3 <SCRIPTS_DIR>/_drive_journey_walk.py --fixture <walk> --surface tool --out tool-walk.md
   #   (append the tool section into the document so both tables persist)

   # Assert both tables present + no bare GAP on the tool surface:
   python3 <SCRIPTS_DIR>/_assert_walk_table.py --surface tool --require-two-tables --no-bare-gap DESIGN.md
   python3 <SCRIPTS_DIR>/_assert_walk_table.py --surface ui   --no-bare-gap DESIGN.md

   # Assert the tool walk is a SUBSET of the interface contract (FR-19): every
   # walked operation must be declared in the §7.6 contract — a walked op the
   # contract never declared is OperationNotInContract (add it to the contract
   # first). Exempt when there is no tool surface (no tool walk ⇒ passes).
   python3 <SCRIPTS_DIR>/_assert_walk_subset_of_contract.py DESIGN.md
   ```

   The tool pass adds **≤ 1 agent turn** over the single-surface walk (NFR-S01)
   — it reuses the contract operations as its source, so the agent doesn't
   re-derive the path. (A change with **no** tool surface is exempt from the
   second pass — log `tool-walk: exempt — no tool surface`, mirroring the (e)
   UI exemption.)

   **(h) Cover every flow on both surfaces; an undrivable tool scenario is
   recorded deferred, never skipped (MUST).** Every UC flow (main / alternate /
   exception) maps to ≥ 1 verifiable scenario on the appropriate surface (FR-10)
   — check it with `_assert_flow_scenario_map.py`. When a tool scenario cannot be
   driven in this environment (no dev-tier endpoint / credential — the
   `tool-drive-sandbox` deferred infrastructure need), it is **recorded
   deferred** via `_drive_scenario.py` (a visible deferred record, NFR-R02),
   never a silent skip and never a fake green:

   ```
   python3 <SCRIPTS_DIR>/_assert_flow_scenario_map.py <flow-map.json>
   python3 <SCRIPTS_DIR>/_drive_scenario.py --scenario <scenario.json> --out <record.json>
   #   exit 0 = observed; exit 3 = recorded deferred (NOT a pass); never a skip
   ```

9. **Extract ADRs** — for each non-trivial decision in the TDD, factor it out into an ADR file. The TDD references the ADR by ID. **Before writing each ADR**, check the External ADR Registry — if an existing ADR covers the same decision, reference it instead. New ADR numbering starts at one past the registry's highest. Do not write ADRs to fill a quota.

    **After writing each ADR file (MUST)**, emit the paired Decision entity through the Brain↔OS port:

    ```
    plugins/sulis/scripts/sulis-emit-decision --from-adr <path-to-adr>
    ```

    For a **business decision** (a BDR — a non-technical, business-level choice) pass `--from-bdr` (or `--kind bdr`) so it is recorded with `kind: bdr`, distinct from a technical ADR (`kind: adr`, the default):

    ```
    plugins/sulis/scripts/sulis-emit-decision --from-adr <path-to-bdr> --from-bdr
    ```

    This persists a validated structured Decision instance under `.brain/instances/product-development/decision/{ulid}.jsonld` — the machine-readable spine of which the `.md` is the human view. The emitter parses `## Context` / `## Decision` / `## Options Considered` (with `## Alternatives Considered` synonym) / `## Consequences` from the body, plus `title` + `status` from frontmatter (translated to entity `state`); the `kind` discriminator (`adr`/`bdr`) is supplied by the flag, not the markdown (absent reads as `adr`). **Each emitted Decision gets its own freshly-minted ULID `@id`**, so a change that produces more than one decision records every one distinctly — there is no `@id` collision when a single change emits two ADRs (or an ADR plus a BDR). **Validation is real**: a malformed ADR is rejected at write (no partial persistence). Skipping this step leaves the Brain↔OS graph incomplete for downstream tooling — the cockpit's golden-thread view, lineage queries, and the Storage Service substrate (Track 2) all read instances, not the `.md`.
10. **Emit a ServiceSpec manifest for every service the design introduces or modifies (MUST).** The third design-stage structured deliverable — alongside the visual contract (`UX_VISUAL_DESIGN_STANDARD`, #45) and the data contract (`CONTRACT_FIRST_STANDARD`, #48). Without it, the design has no machine-readable service contract and downstream — agent integration, SDK generation, MCP routing, the cockpit's service view — has nothing to bind to.

    Write one manifest per service to `.architecture/{project}/service-specs/{service-name}.servicespec.yaml`. Format follows the platform's **SPEC-006 / Service Registration** spec (the canonical contract every Sulis service registers via). Each manifest declares at minimum:

    - **operations** — every endpoint the service exposes. Each operation MUST carry a `description` (what it does) and a `user_guide` (whenToUse / prerequisites / nextSteps) so an AI agent can decide when to call it without reading docs.
    - **errors** — the error catalog. Each error MUST carry `httpStatus`, `user_action` (how a human caller fixes it), `developer_action` (how an integrator fixes it), and `retryable`. No bare codes.
    - **entities** — the Brain-graph nouns this service handles. **Reference compiled entity schemas by id** (e.g. `dna:entity:order`) rather than re-declaring shapes — the marketplace's vendored Brain compile outputs at `plugins/sulis/brain/compiled/` are the source of truth. (When the SPEC-006 entities-block shape stabilises, Slice 3 will emit this block automatically from the Brain compiler.)
    - **bindings** — per operation: host/basePath/method/auth so the SDK and MCP runtime can route calls without guessing.
    - **permissions** — every operation's permission, **structurally namespaced** per SPEC-006's namespacing convention (no bare names).

    **The Lovable Test bar applies**: a spec is complete only if an AI agent could build a working integration against it *with no human docs*. Hold this bar by hand for now; the decompose-validation rubric will mechanically enforce it once Slice 2 ships (a new P7 phase parses the manifest and runs the Lovable Test checks).

    For services the design *modifies* rather than introduces: update the existing manifest in place; do not branch it. The manifest is single-source-of-truth across the lifecycle (design → implementation → registration → SDK / MCP / agent consumption), so divergence at any point is a bug.

    For services that are explicitly bridge handlers over an existing system (BYOS per SPEC-006), call this out in the manifest's metadata and produce the bridge-side contract in the same shape — the registration substrate is identical for BWS and BYOS.

10.5. **Invoke P-VER on the produced TDD + WP set (MUST).** Once the TDD,
    ADRs, and ServiceSpec manifests are written, run the P-VER rubric
    check from
    [`plugins/sulis/references/decompose-validation-rubric.md`](../../references/decompose-validation-rubric.md)
    §Phase 9 against the produced artifacts. P-VER asserts: (a) the
    TDD's `## Verification Plan` section is present per ADR-001's
    literal heading; (b) all six required subsections per
    [`VERIFICATION_QUESTIONS.md`](../../references/standards/VERIFICATION_QUESTIONS.md)
    are populated with substantive content (the placeholder block-list
    per MUC-001 — 30-char minimum); (c) every named integration
    carries an `existing` / `deferred` / `out-of-scope` classification
    (MUC-002 defence); (d) the canonical HTML-comment annotation
    resolves to a live file at a current version (MUC-003 + MUC-004);
    (e) the change's `kind:` value maps to an adapter row in the
    seven-row table (MUC-007); and (f) every WP carries the
    `verification:` frontmatter field per ADR-003.

    **Failure semantics (FR-009).** A P-VER failure halts the design
    pass and surfaces the failure-mode name + the missing piece. The
    common failure modes during draft-architecture are: missing
    Verification Plan section, placeholder content in a subsection,
    unclassified integration. Fix in-line where possible (P-VER PASS
    is the gate that lets `/sulis:plan-work` start). If the failure
    points at an SRD↔TDD contradiction (e.g., the SRD specifies an
    integration that the TDD did not surface), the engineering-architect
    agent's responsibility is to surface the contradiction back to the
    founder; this skill's responsibility is to render the contradiction
    plainly.

11. **Sizing self-check (MUST).** Before writing, review your draft against the tier targets:
    - Total TDD length > 1.5× tier target? → write a "Why is this big?" paragraph or refactor
    - Any section restates content from an authoritative source? → refactor to a reference
    - ADR count > tier maximum? → write an "ADR rationale" paragraph or remove the marginal ones
    - Any pillar marked "fully covered" but actually contains content? → refactor to reference-only
12. **Write `ARCH.yaml`** — link back to the source SPEC.
13. **Append a Sizing Report appendix to TDD.md (MUST).** Add this as the last
    section, cross-referencing the full SIZING.md:

    ```markdown
    ## Sizing Report
    
    See `SIZING.md` for the full sFPC + ASR breakdown. Highlights:
    
    - Tier: {S/M/L/XL} ({computed | user-overridden})
    - TDD length: {N} lines (target: {range})
    - ADRs produced: {N} (target: {range})
    - Pillar coverage applied: Form={covered|gap-filled|full}; Armor={...}; Proof={...}
    - Authoritative sources referenced: {count, listed in SIZING.md}
    - Sections that referenced rather than restated: {list}
    - Circuit breakers triggered: {none | list}
    - Reserved-Vocabulary Sweep: {N} abstracts checked / {M} collisions / {K} renames / {L} shared-dispatch ADRs
    ```
    
    Full breakdown stays in SIZING.md to avoid duplication.
14. **Report** — summarise what was produced, what patterns were chosen, what open questions remain, which misuse cases drove which Armor primitives, the Sizing Report headlines, **and the list of ServiceSpec manifests written (one per service introduced/modified)**.

15. **Emit Design + Decision entities to the brain (MUST).** After the
    TDD + ADRs are written to disk, populate the brain graph so downstream
    tools (`run-all`, the DoD verifier, the dashboard, cross-change design
    queries) can see what was decided. The TDD's `satisfies` array auto-
    resolves to the Requirement entities `specify` emitted (same
    deterministic ULID seed `req:{srd_path}:{fr_id}`); each ADR becomes
    one Decision entity.
    
    Resolve `$SCRIPTS_DIR` once at the start of the skill (the same
    resolver pattern other skills use; see `../change/SKILL.md`), then:
    
    ```bash
    # Design entity from TDD (cross-references Requirements + Decisions)
    "$SCRIPTS_DIR/sulis-emit-design" \
      --from-tdd ".architecture/{project}/TDD.md" \
      --repo-root "$(git rev-parse --show-toplevel)" \
      --state draft
    
    # One Decision per ADR file
    for adr in .architecture/{project}/adrs/ADR-*.md; do
      "$SCRIPTS_DIR/sulis-emit-decision" \
        --from-adr "$adr" \
        --repo-root "$(git rev-parse --show-toplevel)"
    done
    ```
    
    Best-effort: each call emits `{"ok": false, "error": ...}` on failure
    (brain unavailable, schemas missing, validation reject — e.g. an ADR
    with no `## Decision` section). The TDD + ADR files have already
    persisted on disk; brain emission is a side-effect and never blocks
    the blueprint step from completing. Don't narrate the emissions to
    the founder (FE-09) — the brain simply stays current.

15.5. **Resolve verification scenarios to the real Design (MUST when the
    change authored scenarios at specify).** `/sulis:specify` writes each
    scenario's `exercises` as a *synthetic Design placeholder* (no Design
    existed yet). Now the real Design is emitted, so re-point them — capture
    the Design id from the emit above (its envelope's `data.entities[].id`),
    then for each of the change's durable scenario bundles
    (`{worktree}/.changes/{primitive}-{slug}.scenarios.jsonld`):

    ```bash
    "$SCRIPTS_DIR/sulis-resolve-scenario-design" \
      --scenarios "{worktree}/.changes/{primitive}-{slug}.scenarios.jsonld" \
      --design "<dna:design:… from the emit above>" \
      --emit --repo-root "$(git rev-parse --show-toplevel)"
    ```

    A change produces one Design that all its scenarios exercise, so
    re-pointing every scenario in the bundle is unambiguous (it uses the REAL
    emitted id, not a path-recomputed one, so it can't drift). Best-effort +
    no narration (FE-09): skip silently if the change authored no scenarios
    bundle (a non-user-facing change, or specify wrote none).

After the blueprint is accepted, the user typically runs `/sulis:plan-work`
next.

---

## Adapting Depth

Depth is governed primarily by the tier detected in step 3 of the workflow.
The modes below are user-facing overrides — they apply on top of tier
detection, not instead of it.

- **Quick** ("draft a TDD shape") — produce a tier-skeleton only. Each
  pillar gets one paragraph + bullet placeholders. Useful for early
  alignment before full detail. ~30 minutes.
- **Full** (default) — complete TDD sized to the detected tier and
  addressable scope. ADRs for genuinely non-trivial decisions (not as a
  quota).
- **Audit-mode** ("compare proposed TDD to MECE-3") — read an existing TDD,
  score it against the three pillars, return a gap list. No new TDD
  produced.
- **Manual tier override** — accepted at step 3 of the workflow. Up-tier
  for growth-projection / junior-team / regulatory contexts; down-tier for
  spike / POC / pair-programmed contexts. Recorded in the Sizing Report.

See `references/right-sizing.md` for the full sizing standard, including
when to up- or down-tier manually.

---

## Gotchas

- **No SRD, no TDD — except for Early Handover.** If `SRD.md` does not exist and `HANDOFF_TO_SEA.md` does not exist, the skill blocks. Refer the user back to `srd:requirements-analyst`. Do not invent requirements. If `HANDOFF_TO_SEA.md` exists, you may proceed with a lightweight TDD provided you record the absent SRD as an explicit gap in the first ADR.
- **No NFR, no Armor.** The NFRs determine which resiliency and security patterns are needed. If `NFR.md` is missing or thin, surface that as the first Open Question — do not pick patterns by guesswork.
- **No MISUSE_CASES.md when one is expected.** If `SRD.md` exists but `MISUSE_CASES.md` does not, the SRD was produced by a pre-v1.11.0 facilitation or the adversarial sweep was skipped. Note this in the TDD's Open Questions: "Adversarial spec absent — Armor primitives derived from NFR only. Recommend the user re-run `requirements-analyst` for the misuse-case sweep, or accept the gap."
- **One ADR per decision.** Resist bundling. "Why we chose PostgreSQL" and "Why we chose logical replication" are two ADRs if both decisions had viable alternatives.
- **TDD is design, not implementation.** No code in the TDD beyond illustrative type signatures. Implementation lives in Work Packages.
- **Cross-reference the PRIMITIVE_TREE.** Every node in the tree should map to at least one TDD component. Nodes that don't map are gaps — flag them.
- **Cross-reference MISUSE_CASES.md.** Every MUC should map to at least one Armor primitive in the TDD. MUCs that don't map are gaps — flag them.
- **Use the locked vocabulary.** Use only the preferred terms from `GLOSSARY.md` — do not introduce synonyms or use forms the glossary marks as deprecated.
- **Reserved-Vocabulary Sweep is non-optional.** Step 7 catches polysemy collisions between proposed design vocabulary and YAML kind values already used as dispatch keys in the project's infrastructure. The canonical failure it prevents: a new abstract called `Kind` for content generation that shares a name with the Sulis YAML discriminator (`apiVersion: sulis.io/v1, kind: Workload`) — same dispatch shape, opposite lifecycle (one persists and converges, the other is a one-shot pipeline invocation). The sweep table forces lifecycle differences visible *before* TDD authorship, when renames cost minutes rather than days. If the probe synthesis is missing the `reserved_vocabulary_hint` block, re-run `/sulis:analyse-codebase` (v0.9.1+) before drafting.
- **Respect, Don't Restate (MUST).** If `.context/{project}/INDEX.md` exists and lists authoritative sources, your TDD references those sources for topics they already cover — it does not reproduce or paraphrase their content. The most common SEA failure mode is generating a 600+ line TDD that re-derives Clean Architecture, then writing 10 ADRs that overlap with the project's existing registry. The context index is the antidote. Read it, respect it, surface contradictions instead of silently overruling them.
- **New ADRs start past the highest external ADR.** Check the External ADR Registry in the context index. If it shows `Highest ADR number: ADR-22`, your first new ADR is ADR-23. Starting at ADR-1 collides with the existing registry and creates ambiguous references.
- **Size to addressable scope, not to the template (MUST).** The "Full" TDD template is a maximum, not a target. A 4-NFR change does not deserve a 600-line TDD. Compute the tier (S/M/L/XL) in step 3 of the workflow, then *shrink* the target by per-pillar coverage from the context index. A tier-L project with rich existing coverage may justifiably produce a 200-line TDD. See `references/right-sizing.md`. The Sizing Report you append to TDD.md makes this calibration visible.
- **ADRs are not a quota.** They emerge when a decision affects more than one component, locks a technology choice, or rejects a viable alternative — AND no existing ADR covers it. A tier-L project where the team has already made all the major decisions may justifiably produce zero new ADRs. Resist the urge to write ADRs for "we used X" when X was the obvious choice.
- **Chaos tests need a named NFR or MUC.** Each chaos test in the Proof section must defend a specific NFR or MUC. A chaos test for "what happens when the cache is down" without a corresponding NFR or MUC is testing imagination, not requirements — drop it.

---

## See Also

- `references/tdd-template.md` — full TDD section structure with prompts
- `references/architecture-patterns.md` — pattern catalogue (plugin root)
- `references/mece-3-architecture.md` — the three pillars (plugin root)
