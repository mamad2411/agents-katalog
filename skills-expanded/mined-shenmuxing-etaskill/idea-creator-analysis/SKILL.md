---
name: idea-creator-analysis
description: Generate and rank theory-first or proof-oriented research ideas. Use when the user wants non-experimental research ideas, theoretical methods, proof programs, theorem candidates, impossibility results, convergence/sample-complexity analyses, or "analysis" variants of idea creation.
---

# Idea Creator Analysis

Generate publishable theory-first research ideas from a direction, paper, or open problem. Treat experiments as optional evidence, not the ranking backbone.

This skill uses Codex as the idea generator. When subagents are available, spawn a Codex-capability subagent on the latest GPT model with `high` or `xhigh` reasoning for the generation pass. DeepSeek is reserved for later independent critique, novelty skepticism, and proof-route stress testing; do not use DeepSeek to generate the candidate set.

## Output

Write a timestamped report first, then copy it to the fixed name:

```text
idea-analysis-stage/IDEA_ANALYSIS_REPORT_<YYYYMMDD_HHMMSS>.md
idea-analysis-stage/IDEA_ANALYSIS_REPORT.md
```

The report is the single human-facing artifact unless the caller passes a different composed report path.

For subagent generation briefs, use:

```text
idea-analysis-stage/codex-idea-generation-brief.md
```

## Workflow

1. **Load the brief.** Read the user's direction and any cited local files. If a reference paper is provided, extract its core lemma pattern, proof device, assumptions, and stated limitations before searching elsewhere.
2. **Map the analysis landscape.** Search local notes first, then recent literature. For every cited paper, record what theorem type it proves, which assumptions it needs, and which proof technique carries the result.
3. **Prepare the Codex generation brief.** Use `scripts/new_codex_idea_prompt.ps1` when a filesystem brief is useful. Include the source brief, known prior ideas to avoid, the relevant analysis lenses from `references/analysis-lenses.md`, and the candidate schema below.
4. **Generate through Codex analysis lenses.** If subagents are available, spawn one Codex-capability subagent on the latest GPT model with `high` or `xhigh` reasoning and ask it to generate the full candidate set from the brief. If subagents are unavailable, run the same brief in the parent Codex thread and record that fallback in the report.
5. **Keep a real candidate set.** Generate 6-10 candidates before selecting. Do not let the first plausible theorem become the final answer.
6. **Normalize candidates.** Each candidate must specify a theorem target or formal diagnostic object, not only an intuition.
7. **Run a formal sanity gate.** Before ranking, check each candidate against `references/formal-sanity-gate.md`. Drop or weaken candidates whose central theorem depends on an unproved exact identity, invalid boundary case, circular proof lever, or treating constrained RL occupancy measures as an unconstrained simplex.
8. **Mechanically filter.** Drop only candidates that are logically malformed, duplicate, require unavailable definitions, contradict the supplied facts, or repeat known prior outputs. Do not discard ideas merely because they are hard.
9. **Ask for independent critique.** Use `deepseek-agent` with `deepseek/deepseek-v4-pro` for novelty skepticism, proof-route stress testing, and reviewer-style objections after the Codex generation pass. Do not ask DeepSeek to invent replacement ideas unless the task is explicitly a critique-driven repair.
10. **Rank by theory value.** Use `references/analysis-rubric.md`. Top ideas should be capable of becoming a theorem, counterexample, unifying principle, lower bound, or proof technique with top-venue/top-journal value.
11. **Prepare next-step handoff.** For the top 2-3 ideas, invoke or recommend `analysis-plan` to turn them into claims, assumptions, proof obligations, and validation gates. Pick one final idea only after comparing the shortlist.

## Codex Subagent Generation Contract

When subagents are available:

1. Spawn exactly one generation subagent unless the caller explicitly asks for parallel generation.
2. Select the latest GPT-family Codex-capability model exposed by the runtime. If the runtime supports explicit model override, prefer `gpt-5.5`.
3. Set reasoning to `xhigh` for difficult theory generation, or `high` when latency must be controlled.
4. Pass only the generation brief, source summaries, public/local excerpts needed for reasoning, and known prior ideas to avoid.
5. Ask the subagent for 6-10 candidates, ranked shortlist, duplicate-risk notes, and one recommended idea.
6. Parent Codex must run the formal sanity gate, duplicate check, and DeepSeek critique before final ranking.

Do not spawn a DeepSeek-backed generator for this phase. DeepSeek's role begins after Codex has produced candidates.

## Candidate Schema

Use this schema for every surviving idea:

```markdown
### Idea N: <plain title>
- **Research object**: theorem / counterexample / impossibility / convergence analysis / sample-complexity bound / unification / diagnostic principle.
- **Method in 2-4 steps**: what we define, compare, prove, or disprove.
- **Formal target**: the statement shape, including assumptions and conclusion.
- **Proof lever**: the core lemma, decomposition, coupling, potential function, variational identity, or reduction expected to carry the result.
- **Sanity checks**: boundary cases, constrained-domain issues, and which equalities are proved facts versus lemma candidates.
- **Why it matters**: what belief in the field would change if true or false.
- **Closest prior work**: verified or marked `[UNVERIFIED]`.
- **Main risk**: false, already known, too assumption-heavy, or technically blocked.
- **Validation plan**: proof obligations first; optional simulations only if they test a mathematical claim.
```

## Rules

- Lead with the method object, not with a hypothesis or promised application.
- Prefer ideas where a negative result, impossibility theorem, or counterexample is still publishable.
- Treat experiments as sanity checks for formal claims, not as the primary acceptance signal.
- Never present a speculative algebraic identity as established. If the key step is uncertain, state it as a lemma candidate, list the exact derivation obligation, and rank the idea lower unless the failure mode is itself publishable.
- Check boundary regimes before claiming unification. If a theorem claims to cover two limits, the formula must remain meaningful in both limits or explicitly use separate corollaries.
- Check the new candidate against prior generated ideas supplied by the caller. If it is a rename or small variant, mark it duplicate and choose another candidate.
- Keep local private paths, unpublished project names, and one-off stress-test details out of reports that may be promoted.
- Use `deepseek-agent` before final ranking when an external critique is feasible. Save the brief and result under `idea-analysis-stage/reviews/`.

## Related Skills

```text
idea-creator-analysis -> ranked theory/proof ideas
analysis-plan         -> proof obligations and research plan for the selected idea
idea-discovery-analysis -> full pipeline orchestration
novelty-check         -> literature novelty verification for top candidates
deepseek-agent        -> preferred independent critique and proof-route stress test
```
