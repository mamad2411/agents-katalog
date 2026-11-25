---
name: research-spike-run
description: 'Run a scoped feasibility experiment and report evidence before committing to an implementation. Use when a design or feasibility question needs a bounded experiment. RU: спайк, проверка осуществимости.'
disable-model-invocation: true
---

# Feasibility spike

Use when an unresolved design or feasibility question benefits from a bounded experiment. Define the question, success signal, alternative hypotheses, time and resource budget, scope and allowed side effects before starting. If documentation or source inspection can answer the question, start there. Select the smallest practical experiment and preserve inputs and existing user work.

Record observations, failure boundaries and sample limitations; separate a proof of concept from a production-ready implementation. Recommend a next step only to the extent the experiment supports it. Explicitly identify reusable findings and outstanding risks.

Temporary or experimental files are still user data: discard or overwrite them only under the applicable authorization and after protecting unrelated work. A spike does not authorize dependency installation, external publication, destructive cleanup or production changes by implication.
