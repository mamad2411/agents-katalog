---
name: research-first
description: Makes research a blocking phase before any bot or project is designed or built. Use when the user says "build me a bot", "make a project", "can you build X", when starting a new repository or feature whose design depends on external facts (APIs, pricing, limits, schemas, platform rules), or whenever the honest answer would be "I don't have enough information yet". Produces a Discovery Contract with primary sources and a preflight gate instead of guessing, and enforces a question budget so intent questions do not crowd out facts that could simply be fetched.
---

# Research-first

Findable facts are collection tasks, not questions. This skill is the protocol that makes
that binding.

## Before anything else: where am I?

The project is the **current working directory**. If the cwd is not the project the
operator means - the kit's own repo, a parent folder holding several projects, an
unrelated checkout - **ask which project**, and wait. Never search the filesystem for the
one you think was meant, never infer it from a name, never look it up on a remote.

Signals that you are in the wrong place: no `AGENTS.md`, no `research/` directory, or a
`research/` corpus plainly about something else.

## Which machine is this?

```
node "$HOME/.agents/fetchproof/bin/doctor.mjs"
```

A **collector** produces the corpus, using Firecrawl with its key or an explicitly chosen
keyless route (ADR-0095). A **builder** consumes a corpus and
must not collect: `research.mjs` and `decompose.mjs` refuse there (exit 2) rather than
fall back on another transport. A page fetched by hand is not evidence in this kit.

On a builder, the first command is `node "$HOME/.agents/fetchproof/bin/handoff.mjs"`.

## The sequence

```
decompose -> contract -> prior -> collect -> gate -> brief
```

1. **Decompose.** `node "$HOME/.agents/fetchproof/bin/decompose.mjs"` (it maps the project's own topic; `--topic` only while the project is untitled)
   drafts `research/MAP.md`, seeded with nine universal dimensions: access model, auth,
   rate limits, ToS/legality, schema stability, freshness, cost at volume, runtime
   limits, and **output obtainability** - the load-bearing one. If the data your "done"
   depends on cannot be obtained, the project dies in phase 1, not phase 2.

   Statuses arrive blank. Mark each row COVERED (cite the U-## rows), DISMISSED (reason
   required), or GAP. Dismissing is fine; omitting is not.

2. **Contract.** Write `## Build intent` in `research/DISCOVERY.md`, then enumerate the
   blocking unknowns FROM the map. A fact blocks the build when a wrong guess changes the
   design.

3. **Register your prior.** `node "$HOME/.agents/fetchproof/bin/prior.mjs" "<what you expect>"`.
   Write two things: what you expect the evidence to say, and what you know you cannot know
   yet. Optional - and **this is the only moment it is possible**, because it is chained
   into the ledger ahead of the first page and refused afterwards.

   Being wrong is the point. A prediction that the corpus demolishes is the clearest
   evidence the research was worth doing; one you reconstruct afterwards is worth nothing,
   which is exactly why the order is fixed by a hash rather than by memory. Nothing grades
   it (ADR-0039).

4. **Collect.** `node "$HOME/.agents/fetchproof/bin/research.mjs"`. Prefer the page that
   *owns* the fact - official docs, the repo, the pricing page, the statute - over any
   write-up about it. Firecrawl collection spends credits; chosen keyless pages still
   use the planned page allowance. Plan the queries first.

5. **Rewrite the findings.** The `Finding` cell arrives auto-extracted. Turn it into a
   real claim with the number or quote that proves it, and keep `Raw` pointing at the
   cached page. For a Git builder request, the collector records this review and the
   unknown closure; the builder reports review-only gaps in prose (ADR-0150).

6. **Gate.** `node "$HOME/.agents/fetchproof/bin/preflight.mjs"`. **Do not build until it
   prints PASS.**

7. **Brief.** `node "$HOME/.agents/fetchproof/bin/brief.mjs"` drafts the phase-1 -> phase-2
   handoff. Answer the two sections the corpus cannot fill.

Before building, check the intact handoff, PASS, classified MAP, rewritten Findings,
and an authored brief with both judged sections answered. `brief.mjs --state` reports
the state and judged sections; it does not establish currency by itself. A stamped
brief needs current inputs; authored unstamped briefs retain approval with currency
unknown (ADR-0138). Approval has no machine-role predicate. ADR-0052's local review and
re-packaging of a received package remains available without collecting.

## The question budget

At most **three** questions, once, up front, and only about intent: what the user
actually wants, which accounts or budget they have, who the audience is, what "done"
means. A question whose answer is in public documentation is a research task.

**Never answer "insufficient info" and stop.** Either produce evidence, or name the
single missing fact and go collect it.

## Honest gaps

A fact that is genuinely unreachable - login-walled, private, paywalled - is marked
`KNOWN-UNKNOWN`, with the day-one verification step written into the `Evidence` cell. An
honest, labeled gap is fine. An unlabeled gap is the failure mode this protocol exists to
prevent.

## Source quality

`P` primary/official carries the design. `S` secondary is context. `L` lead-only -
forums, video, blogs - is a hint, never proof. Never invent a citation. Record
contradictions and say which side you trust and why; never average them.
