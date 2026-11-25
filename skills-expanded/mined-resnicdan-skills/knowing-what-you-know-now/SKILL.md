---
name: knowing-what-you-know-now
description: Decide whether something already built and working is worth rebuilding the elegant way, knowing everything you now know. Run it when a build works as intended and you want an educated keep / refactor / rebuild call before moving on, not a reflexive rewrite.
disable-model-invocation: true
argument-hint: "[optional: a PR, directory, module, or diff to evaluate]"
---

# Knowing What You Know Now

Run this on something that is **built and working as intended**. Evaluate whatever
target you're pointed at (a PR, a directory, a module, a diff); if none is given,
infer it from the current conversation, and if it's still unclear, ask which build
to evaluate — don't evaluate air.

The job is a judgment call, not a rewrite: **earn the rebuild**. Most of the time
the honest answer is "keep it" or "one targeted refactor" — a full rebuild has to
justify itself. The guiding move is the whiteboard question: *knowing everything
you know now, how would you build it?* The reason an elegant version can exist is
that **the learning is the collateral, not the code** — you now know things about
the problem you didn't when you started. Surfacing that learning, and testing
whether it changes the shape of the solution, is the whole point.

Engineering policy — DRY, test expectations, the effort/risk/maintenance framing,
verification discipline, git hygiene — is governed by your project's conventions
(e.g. your `CLAUDE.md` / `AGENTS.md`) and your agent's standing preferences. Apply
them; don't restate them here.

## Steps

Do them in order. The order matters: first mine the current code for what it
taught you (Step 2), then design from the problem **before** you re-litigate the
code itself (Step 3) — you keep what you learned without inheriting the old shape.

1. **Scope the target.** Pin down exactly what "this build" is and read it — the
   actual code, not a summary. State in one line what it does and what "works as
   intended" means for it (a shipped feature? a working prototype? a spike?). This
   sets the bar: don't hold a spike to production-grade, and note that an untested
   prototype carries more rebuild risk (see Step 5).

2. **Reconstruct the learnings.** This is the leg work — do it thoroughly, it's
   where the value is. Answer: *what do we know now that we didn't when this
   started?* Constraints discovered mid-build, dead ends, edge cases that forced
   detours, the real shape of the problem vs. the assumed one, places where the
   design bent around something. Mine the current code for these: every branch,
   guard, and special case encodes a learning — name it. List them concretely;
   this list is the raw material for everything below, and the requirements the
   blank-slate design must satisfy.

3. **Blank-slate design.** Knowing everything you know now, design the solution
   from a blank slate. Be concrete: name the modules, the data flow, and the main
   path through the system. **Do not reference or reproduce the current
   structure** — design as if writing it fresh, the way an engineer at a whiteboard
   describes a completely different, simpler architecture. Anchoring on the
   existing shape is the failure mode; resist it.

   Two guardrails on that fresh design. It must satisfy **every** learning from
   Step 2 — if it looks cleaner only because it quietly dropped a case, it's
   incomplete, not simpler. And watch the opposite failure: "knowing everything
   now" tempts over-building — extra layers, config, abstraction the problem
   doesn't call for. Simpler means fewer concepts, not more indirection; any
   concept this design adds must earn its place against a Step 2 learning.

4. **Compare.** Put the current build next to the blank-slate design. Where they
   diverge, is the divergence **material** or **cosmetic**? Material = removes a
   class of bugs, drops a dependency, closes a data-consistency hazard, deletes a
   layer or workaround you now know is unnecessary, or cuts complexity by an order
   (O(n²)→O(n), removes an N+1). Cosmetic = naming, layout, style. If the design
   looks dramatically simpler, assume it dropped something until proven otherwise:
   name what it dropped, or show it drops nothing, before crediting the gap as
   material. A material gap should map to a Step 2 learning; one that maps to none
   is suspect. Hold both against the bar: *as complex as necessary, as simple as
   possible.* Be specific — "it could be cleaner" is not a finding.

5. **Verdict — earn the rebuild.** Deliver an educated call, then **stop for
   approval before touching code.** Give all three options ("do nothing" first), each
   with effort / risk / maintenance burden / blast radius, and recommend one. Let
   test coverage set the risk floor: with no tests (common for prototypes and
   spikes) nothing can prove parity, so a rebuild changes behavior with no safety
   net — rate its risk and effort higher (the effort now includes writing a
   characterization suite; see the playbook) and weight the call toward
   keep/refactor.
   - **Keep as-is** — the current build is already the elegant solution, or the
     gap is cosmetic / doesn't justify the cost. Recommend this by default unless
     a rebuild or refactor genuinely beats it.
   - **Refactor in place** — keep the current architecture; make a targeted change
     to capture the design's gains. Covers cleanup (restructuring without changing
     behavior) and hardening (adding a missing edge case or error path the shape
     already accommodates). Choose it when the shape is right but the execution
     isn't done.
   - **Rebuild from learnings** — the blank-slate design is *materially* simpler or
     more robust **and** the gain justifies the cost. Must be earned, not reached
     for reflexively; a material gain on a high-blast-radius or weakly-tested
     surface still leans keep/refactor.

## If a rebuild or refactor is approved

Only after the rebuild/refactor is approved, read `rebuild-playbook.md` and follow
it — it holds the discipline for rebuilding from learnings without copy-pasting the
old code. Until then, this skill ends at the verdict.
