---
name: modeling-repair-regression
description: Targeted repair/regression coordinator. After a confirmed defect is fixed by its owner, rerun the smallest affected downstream checks and behavior comparisons.
---

# Targeted repair and regression

Use route_back evidence to identify the owner and minimum scope. Do not mix correctness repair with score chasing. After a code fix, require before/after hashes and behavior comparison; after a Paper fix, rerun only affected citation/formula/abstract/visual checks.
