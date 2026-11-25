---
name: council
description: Ask the same question to three models from different families (GPT, Kimi, DeepSeek by default), read-only and in parallel, then judge the answers blind. Use for design decisions, risky trade-offs, root-cause hypotheses and reviews where one model's view is not enough. Needs the orchestra skill's scripts.
---

# Council

One model can be confidently wrong. Three models from different families are wrong in different ways,
and the differences are where the useful information is.

## Run it

1. Write the question to a file. Include the evidence (code excerpts, logs, constraints) and say what a good
   answer looks like: a recommendation, the main risk, and what would change the recommendation.
2. Run:

```bash
../orchestra/scripts/mmo-council --question q.md --outdir council/ -C <repo>
# custom panel:
../orchestra/scripts/mmo-council --question q.md --outdir council/ \
  --lane codex:gpt-6-astra --lane deepseek:deepseek/deepseek-v4-pro --lane kimi:kimi-code/k3.1-pro
```

3. Read `council/answer-A.md`, `answer-B.md`, ... **before** opening `key.txt`. The letters are shuffled,
   so you judge the reasoning and not the brand.
4. Check `status.txt`. A lane marked FAILED (including `model`, a rejected model id) is not an answer and not a vote. If fewer than two lanes answered,
   say so and do not call it a council.

## Judge it

- Write down where they agree, where they disagree, and which claims you can check.
- Check the checkable claims yourself (run the code, read the file, look up the API).
- Agreement is a hint, not proof: models share training data and blind spots.
- A single dissent with a concrete, checkable argument beats a majority with none.
- Your final answer is your own synthesis. Do not paste a panelist's answer as the result.
- Tell the user which models answered, which failed, and where the panel split.
