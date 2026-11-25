---
name: founder-playbook
description: >
  Use when a founder zooms out for whole-company direction — which lifecycle stage am I in (Idea, MVP, Launch, Scale) and the most important thing to do next — rather than one concrete deliverable. Stage-by-stage operating guide for building an AI-native startup, distilled from Anthropic's "The Founder's Playbook" — each stage's goal, exit criteria, failure modes, and how to apply Claude. Triggers on a founder's judgment calls: am I ready to build, launch, scale, or raise; is this real product-market fit or a launch spike that fades; should I pivot or persevere; how to stop being the bottleneck; what moat compounds vs a better-funded incumbent; running an AI-native or solo non-technical startup. For a single artifact instead — pricing model, runway, deck, GTM plan, interview script — route to the matching per-function skill (business-model, finance-accounting, fundraising, growth-analytics, go-to-market, idea-validation).
---

# Founder's Playbook: Building an AI-Native Startup

The map for the shortest path between idea and exit when AI is core infrastructure.
Use it to locate which stage a founder is in, name the goal and the failure mode for
that stage, and apply the right AI surface at the right moment — then hand off to the
deeper per-function skills for execution.

> Distilled from Anthropic's _The Founder's Playbook: Building an AI-Native Startup_.
> This skill is the lifecycle/stage layer; the per-function skills under
> **Related skills** carry the depth.

## The AI-native shift

The founder's job hasn't changed — find a real problem, build something that solves
it, scale it into a company that matters. What changed is the path. AI compresses
quarters into weeks, so the founder role shifts from **individual contributor** to
**orchestrator of agents**. Attention moves up the stack toward the higher-order work:
deciding *what* to build and *why*, and directing the systems that carry it out.

Three areas let a lean startup function like a much larger org:

- **Research / conversational intelligence** — an on-call expert for every domain
  (competitive analysis, market sizing, financial modeling, devil's-advocate analysis).
- **Agentic coding** — the engineer who's always available, never blocked. Plain-language
  intent → generated, tested, debugged, production-grade code.
- **Workflow automation** — an on-demand ops team. Recurring operational tasks (CRM,
  reports, docs, scheduling, compliance) configured to run themselves.

**The bottleneck is no longer what you can build — it's what you choose to build.**
Full mindset, leverage areas, and the closing synthesis: `references/ai-native-founder.md`.

## Choose your surface

| If the task is... | Reach for | Why |
|---|---|---|
| A question, a rewrite, a quick brainstorm | **Chat** | Fast, conversational, no setup |
| Research, analysis, or a finished doc/deck/sheet built from your files & systems | **Claude Cowork** | Folder access, connectors, skills, scheduled runs |
| Writing, testing, or shipping software | **Claude Code** | Codebase access, diffs, git, dev environments |

Same Claude underneath; what changes is the workspace around it.

## Diagnose the stage

| Stage | You're here when... | Guiding question | Read |
|---|---|---|---|
| **Idea** | A problem you can't stop thinking about; nothing validated; no users yet | "Is this worth building?" | `references/idea-stage.md` |
| **MVP** | Validated problem; building the smallest real solution; chasing first PMF evidence | "What exactly should we build first?" | `references/mvp-stage.md` |
| **Launch** | Have a PMF signal; turning traction into a repeatable growth engine and a real company | "Does this business deserve to grow?" | `references/launch-stage.md` |
| **Scale** | Repeatable growth; going thousands→millions of users, one market→many | "Is this sustainable without me in every loop?" | `references/scale-stage.md` |

When unsure, locate the **exit criterion** the founder cannot yet honestly claim — that
names the current stage. Don't let easy building pull execution ahead of the evidence.

## The four stages at a glance

### Idea — research-oriented validation
- **Goal:** assemble evidence a real problem exists and your solution addresses it, *before* building.
- **Exit:** problem-solution fit — yes to all three: problem is real & specific; solution addresses the *revealed* problem; enough signal to justify an MVP.
- **Watch for:** mistaking building for validating · premature scaling · loss of objectivity (AI will confirm whatever you ask it to).
- **Key play:** sharpen the hypothesis until testable, then point AI at *refuting* it. → `references/idea-stage.md`

### MVP — translate a validated problem into a used product
- **Goal:** smallest focused product that real users actually use; build without compounding **agentic technical debt**; invest in persistent context (CLAUDE.md) from day one.
- **Exit:** genuine product-market fit — a specific group returns to it (retention), pays for it (revenue), or refers it (referral).
- **Watch for:** agentic technical debt · false PMF (launch-energy spikes ≠ fit) · zero-friction scope creep · insecure-by-inexperience.
- **Key play:** define architecture + scope *before* building; measurement framework *before* launch. → `references/mvp-stage.md`

### Launch — prove the *business* deserves to grow
- **Goal:** turn early traction into a repeatable, channel-driven growth engine; harden the infrastructure; build the company around the product; stop being the bottleneck.
- **Exit:** (1) growth is repeatable & channel-driven with known CAC/LTV/payback; (2) product handles production workloads; (3) operations run without founder bottlenecks.
- **Watch for:** technical debt coming due · the founder becoming the bottleneck · security/compliance no longer deferrable · expansion before you're ready.
- **Key play:** audit everything routed through you; systematize, delegate, or automate it. → `references/launch-stage.md`

### Scale — make it sustainable beyond the founder
- **Goal:** systematic growth sustained by mature org operations; a defensible moat from accumulated depth (domain expertise, integration depth, proprietary data/workflows).
- **Exit:** a threshold event — sustainable profitability, IPO-readiness, or acquisition. Test: *if a well-funded incumbent copied your product today, would your users stay?*
- **Watch for:** delegating the operational layer (and trusting it) · scaling technical ops *around* the codebase · scaling org functions · building a real GTM function.
- **Key play:** turn domain expertise, user data, and integration depth into compounding lock-in. → `references/scale-stage.md`

## Cross-cutting principles

These hold at every stage — they are what keep AI a force multiplier instead of a source of entropy.

1. **Keep sense-making ahead of building.** Agentic coding builds a flawed premise with
   the same enthusiasm as a great one. The intelligence in the system is yours.
2. **Point AI in the opposite direction.** Using Claude as a structured devil's
   advocate — refute the hypothesis, argue the competitor's case, run the pre-mortem —
   is a core use case at *every* stage, not just the Idea stage.
3. **Prototypes are props; humans are the evidence.** A working prototype is a
   pressure-testing prop for real conversations, never proof the problem is real.
4. **Persistent context compounds.** Specs, architectural decisions, scope docs, and
   CLAUDE.md files are the memory that stops every session from re-deriving (and
   drifting from) the original vision.
5. **Disconfirming evidence is the system working.** Results that don't confirm your
   direction surface *before* you over-invest. That's the signal to adjust, pivot, or
   step back — not failure.
6. **Re-run the research as the hypothesis evolves.** Market sizing and competitive
   mapping are not one-time exercises; repeat them whenever your thinking changes.

## Related skills

This skill diagnoses the stage and the play; route to these for execution:

- **Idea / MVP:** `idea-validation` (customer discovery, PMF), `product` (specs, roadmap), `business-model` (pricing, unit economics)
- **Launch:** `go-to-market`, `growth-analytics` (metrics, experimentation), `customer-success`, `legal-compliance`, `operations`
- **Scale:** `fundraising`, `sales`, `marketing-brand`, `finance-accounting`, plus `go-to-market` again for the dedicated GTM engine
- **Deep dives & evidence:** pair this with your research tools to gather sources and pressure-test assumptions before committing to a direction

## Reference files

- `references/ai-native-founder.md` — the orchestrator mindset, the three leverage areas, surface selection in depth, "same job, new rules"
- `references/idea-stage.md` — validation playbook + exercises
- `references/mvp-stage.md` — build-without-debt playbook, PMF litmus tests, pivot diagnostic + exercises
- `references/launch-stage.md` — growth engine, de-bottlenecking, security/compliance, PM operating system + exercises
- `references/scale-stage.md` — moat-building, enterprise infra, GTM function, lock-in + exercises
- `references/resources.md` — Anthropic docs, founder stories, startup programs (source pointers)
