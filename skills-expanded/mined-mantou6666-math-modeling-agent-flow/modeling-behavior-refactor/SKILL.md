---
name: modeling-behavior-refactor
description: Contestant-scale code simplification. Simplify unnecessary engineering structure while preserving mathematical/numerical behavior; any executable hash change requires result/evaluator regression.
---

# Contestant-scale code simplification

Compare baseline and current executable hashes. Simplify only unnecessary engineering structure. Preserve mathematical kernels, formal evaluator, numerical stability and performance-critical vectorization. After changes, compare official Result IDs/values, feasibility, key intermediates and independent evaluator outputs within declared tolerance. No freeze/state-machine dependency is required.
