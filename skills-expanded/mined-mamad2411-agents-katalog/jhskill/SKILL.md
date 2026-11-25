---
name: jhskill
description: |
  姜胡说 SkillHub 根入口。Use when installing or invoking the packaged Jiang Hushuo / 姜胡说 skill bundle for ordinary people making money and growing. Defaults to IMA knowledge base "姜胡说Ai知识库｜普通人赚钱与成长" and routes users to $jhs, $jhs-ima, $jhs-learning-map, $jhs-content, $jhs-writing, or $jhs-practice.
---

# jhskill

This is the SkillHub root entry for the Jiang Hushuo skill bundle.

Use `$jhs` as the main router. Use `$jhs-ima` for source-backed retrieval from the default IMA knowledge base:

```text
姜胡说Ai知识库｜普通人赚钱与成长
```

Available workflows:

- `$jhs`: route the user's task
- `$jhs-ima`: search and verify from IMA
- `$jhs-learning-map`: build learning paths
- `$jhs-content`: generate topics and short-form content
- `$jhs-writing`: draft essays and scripts
- `$jhs-practice`: turn concepts into practice plans

Do not expose internal IDs or private source paths. Use the bundled quarterly atom library under `知识库/原子库/YYYY-Qn.jsonl` only as abstract methodology, not as exact source text.
