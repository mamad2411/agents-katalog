---
name: fine-tuning-adaptation-dataset-prep-sft
description: "Clean, deduplicate, and balance instruction-response pairs so fine-tuning learns behavior rather than noise."
---
# Prepare supervised fine-tuning datasets

> Clean, deduplicate, and balance instruction-response pairs so fine-tuning learns behavior rather than noise.

**Track:** 🤖 AI Engineering · **Domain:** Fine-tuning & Adaptation · **Level:** advanced · **~60 min**

**Who this is for:** AI Engineers, ML Engineers, LLM App Developers, Agent Builders

## When to Use This Skill

Clean, deduplicate, and balance instruction-response pairs so fine-tuning learns behavior rather than noise.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Define the target behavior as 5 crisp capability statements before collecting data
2. Deduplicate near-identical pairs; duplicates amplify artifacts
3. Balance coverage across capabilities, lengths, and difficulty tiers
4. Hold out 3% as an untouched eval split mirroring real traffic
5. Scrub PII and secrets with automated scans plus human spot checks
6. Start LoRA-scale: 500-2000 high-quality pairs beat 50k scraped ones

## Common Pitfalls

- Training on outputs of the same model you are tuning, compounding errors
- Response style inconsistent across contributors

## Success Signals

- Eval-split win-rate vs base model above 70%
- Zero PII findings in pre-flight scan

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill fine-tuning-adaptation-dataset-prep-sft
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill fine-tuning-adaptation-dataset-prep-sft -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills