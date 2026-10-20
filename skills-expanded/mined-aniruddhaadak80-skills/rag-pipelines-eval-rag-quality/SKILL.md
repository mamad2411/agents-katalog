---
name: rag-pipelines-eval-rag-quality
description: "Score groundedness, relevance, and completeness with judge prompts plus deterministic checks wired into CI."
---
# Evaluate RAG answer quality automatically

> Score groundedness, relevance, and completeness with judge prompts plus deterministic checks wired into CI.

**Track:** 🤖 AI Engineering · **Domain:** RAG Pipelines · **Level:** advanced · **~45 min**

**Who this is for:** AI Engineers, ML Engineers, LLM App Developers, Agent Builders

## When to Use This Skill

Score groundedness, relevance, and completeness with judge prompts plus deterministic checks wired into CI.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Freeze 30-100 test questions with known-good source passages
2. Run deterministic checks first: citation present, answer not empty, no refusal
3. Use an LLM judge with rubric scores 1-5 for groundedness and relevance
4. Swap judge models occasionally; if two judges disagree widely, fix the rubric
5. Log every eval artifact: question, chunks used, answer, scores, cost, latency
6. Block merges when groundedness average drops more than 0.3 below baseline

## Common Pitfalls

- Judging with the same model that generated the answer, inflating scores
- Evals only run manually, drifting from production reality

## Success Signals

- Groundedness average 4.3+ of 5
- Eval suite runtime under 10 minutes

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill rag-pipelines-eval-rag-quality
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill rag-pipelines-eval-rag-quality -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills