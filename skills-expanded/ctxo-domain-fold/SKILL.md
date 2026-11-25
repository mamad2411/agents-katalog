---
name: ctxo-domain-fold
description: Use BEFORE changing code under a named domain context, BEFORE finishing a branch, and when adopting or tuning the domain config, to read the context's card, fold behaviour changes back into it and discover the repository's conventions.
---

# Fold domain knowledge with ctxo

## When adopting or tuning the domain config

1. Run `ctxo domain discover` first (a dry run: it writes nothing). It reads the commit subjects, branches, index and tracked files and proposes `domain.rules.trackerPrefixes`, `domain.tests.ruleTraitKeys`, `index.tests` and the characterization and contract test markers (folders, file-name globs, Trait or Category values and custom test attributes). External IDs such as CWE or ISO keys, GitHub `#N` issues and lowercase branch identifiers are evidence only: they need no config.
2. Review the evidence, then either edit `.ctxo/config.yaml` by hand or run `ctxo domain discover --write`, which adds the proposed values and removes none. `--json` prints the same evidence and proposal for a script.
3. A wrong value, once written, stays until you remove it by hand, and discovery (and `ctxo doctor`) proposes it again until the evidence changes. Review before `--write`.
4. Do not reverse-engineer the config keys from ctxo's installed files: the discovery report names each key it proposes.

## Before changing a context's code

1. Find the context that owns the files: the generated path rule for the folder, or `docs/domain/contexts.yaml` (each context lists its `paths` and its `card`).
2. Read the context's card before you edit: its rules, contracts and decisions are the behaviour the code must keep.
3. With the ctxo MCP tools, call `get_domain_context` with the symbol you will change (`symbolId`, or a `path`): it returns the context's card, its rules with their linked tests and code, terms, contracts and decisions. Then call `get_rule` for each rule it lists that your change may affect, to see the tests that pin the rule and the decisions behind it.
4. To find business logic no rule pins yet, call `find_shadow_specs` for the context.

## When behaviour changes

1. Update the card in the same branch as the code: a changed rule, contract or decision goes into the card, not only into the commit message.
2. Rule IDs are permanent. Never reuse or renumber one; retire a rule by marking it, and give a new rule a new ID.

## At branch finish

1. Run `ctxo contexts-touched --since <base>` to list the contexts this branch changed.
2. For each unresolved context, either commit a card update or add `Domain-Unchanged: <id> (reason)` to a commit (an empty commit is fine).
3. The Stop guard blocks once when a commit changed a context without either, so resolve every context before you finish.

<!-- ctxo-skill v0.17 -->
