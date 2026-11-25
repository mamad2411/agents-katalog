---
name: test-coverage-audit
description: 'Inventory tests and coverage gaps from evidence without implying permission to change or run them. Use to map what is tested before planning new tests. RU: покрытие тестами, инвентаризация тестов.'
disable-model-invocation: true
---

# Coverage inventory

Identify the requested repository, revision, branch, target behavior and read or execution scope. Inventory the relevant tests, collection rules, runtime dependencies and assertions through supported project interfaces. Distinguish a source file's presence from actual test selection and execution; generated or untracked tests can be absent from ordinary diffs.

Classify a gap as missing assertion, missing execution, missing fixture or environment, uncertain result, or untested integration boundary. Cite the relevant behavior and evidence, distinguish static inspection from measured coverage, and avoid treating coverage percentages as correctness proof. Propose proportionate checks that exercise behavior rather than duplicate implementation.

A request to inventory or propose tests does not itself authorize changing files, launching services or executing the suite. If execution is permitted, record the exact selected scope, runner, results, counts and limitations; distinguish a substituted harness from the sanctioned gate. Preserve unrelated work and report partial or inaccessible scope.
