---
name: idea-discovery-analysis
description: "Orchestrate a full theory-first idea discovery pipeline. Use when the user wants the analysis counterpart of idea-discovery: literature context, proof-oriented idea generation, novelty checking, DeepSeek critique, and an analysis plan instead of an experiment-first workflow."
---

# Idea Discovery Analysis

Run the full analysis-side idea pipeline:

```text
source brief -> Codex subagent idea generation -> parent Codex sanity/novelty checks -> deepseek-agent review -> analysis-plan
```

## Output

Use one canonical report:

```text
idea-analysis-stage/IDEA_DISCOVERY_ANALYSIS_<YYYYMMDD_HHMMSS>.md
idea-analysis-stage/IDEA_DISCOVERY_ANALYSIS.md
```

Detailed plan files may live beside it:

```text
idea-analysis-stage/IDEA_ANALYSIS_REPORT.md
idea-analysis-stage/ANALYSIS_PLAN.md
idea-analysis-stage/reviews/
```

## Pipeline

### Phase 0: Brief and Scope

Read the user request and any reference paper or notes. If the user wants pure experimental ideas, use `idea-discovery` instead. If they want theory, proof, convergence, lower bounds, unification, or RL analysis, continue here.

### Phase 1: Literature Context

Build a lightweight source brief from the user's idea and the main papers they provide or clearly intend to use. Prefer 2-5 anchor sources over a broad literature survey.

For each anchor source, extract only what helps idea generation:

- the problem setting and formal objects;
- the theorem type, assumptions, and proof device;
- the limitation, gap, or boundary regime that could motivate a new idea;
- the closest-prior-work risk it creates for our direction.

If the user provides no papers, do a compact local/web search for a few anchor sources only.

Keep this source brief inside the canonical report unless the caller asks for standalone notes.

### Phase 2: Theory Idea Generation

Invoke `idea-creator-analysis` in composed mode. The generation step belongs to Codex, not DeepSeek. When subagents are available, spawn a Codex-capability subagent on the latest GPT model with `high` or `xhigh` reasoning; prefer `xhigh` for difficult theory-generation cases. If the runtime exposes explicit model names, prefer `gpt-5.5`.

Require candidates to lead with method object, formal target, proof lever, novelty delta, and negative-result value.

Apply the formal sanity gate before accepting a top candidate: boundary regimes must be coherent, constrained RL objects must stay in their correct domains, and nonstandard exact identities must be marked as lemma candidates unless already derived.

Keep a ranked shortlist of at least 3 candidates when the direction is broad enough. The workflow should compare theory shapes before committing to a final plan.

If earlier generated ideas are supplied, treat non-duplication as an acceptance condition. Reject small renames, scheduler/gate variants, or restatements of the same theorem target unless the new candidate has a distinct formal object and proof lever.

### Phase 3: Novelty Check

Run `novelty-check` on the top candidates. For theoretical work, check theorem statements, assumptions, proof techniques, and problem setting, not just algorithm names.

### Phase 4: Independent Critique

Use `deepseek-agent` with `deepseek/deepseek-v4-pro` for adversarial review after Codex has generated and parent Codex has sanity-checked the candidates. DeepSeek is the independent checker, not the primary idea generator. The review brief should ask for:

- whether the idea is genuinely theory-first;
- closest prior work and hidden equivalences;
- likely theorem failure modes;
- whether the idea has top-venue/top-journal value;
- what must be proven before experiments matter.
- whether the idea duplicates any prior generated idea supplied in the brief.

Save the brief and result under `idea-analysis-stage/reviews/`.

### Phase 5: Analysis Plan

Invoke `analysis-plan` for the best surviving idea. The plan must include formal setup, core claim, proof obligations, disproof paths, novelty delta, and acceptance gates.

If the first plan fails the acceptance gates for mathematical coherence, update the report and return to the shortlist with a weaker theorem, diagnostic theorem, or counterexample plan. Do not keep an attractive but false unification as the final idea.

## Rules

- Do not rank ideas by pilot success or GPU feasibility.
- Do not let experiments rescue an idea whose formal object is vague.
- Do not use DeepSeek to create the first candidate set. Use Codex generation first, then DeepSeek critique.
- Do not use Claude-specific agent routing. When an external checker is needed, prefer `deepseek-agent`.
- Preserve public-safety: no private machine paths, account names, unpublished project titles, or local stress-test logs in reusable skill files.
- If the reference paper is local/private, summarize only what is needed in the local output and do not copy its path into reusable artifacts.
