---
name: workflow-audit
description: "Audit installed agent skills or a proposed harness integration for routing quality, overlap, provenance, hidden side effects, and actual workflow benefit. Use for skill stocktakes and harness changes; not routine application-code review."
---

# Workflow audit

Inventory the requested surfaces first: their owners, immutable versions, loaded
entrypoints, support files, scripts, hooks, MCP servers and configuration writes.
Inspect source before execution. The active tool list and verified installed
version establish availability; an upstream README does not.

The read-only Node 20+ `scripts/inventory.mjs` inventories explicitly supplied skill roots
without following symlinks or reading configuration, conversations or credentials:

```powershell
node <skill-directory>/scripts/inventory.mjs --root <skills-directory>
```

It emits names, entrypoint byte sizes and whole-folder hashes as JSON on stdout.
Repeat `--root` for multiple directories. It reads only SKILL.md, references,
scripts, assets, agents, templates, examples and license/source metadata within
immediate skill folders. It reports excluded credential/config-like filenames,
skipped non-skill folders, links and unreadable paths. Missing roots make the
inventory incomplete. It does not scan file contents for secrets; ordinary code
could contain one, so supply only instructional skill roots. Review the JSON
before saving it to a task-owned record. Hashes detect changes only within the
declared allowlist, not correctness, safety, actual usage or excluded-file drift.

For third-party intake, review the executable surface separately: tests and their
fixtures, package install/test lifecycle scripts, build helpers, and hook files
may sit outside this inventory's allowlist. Inspect their entrypoints and callers
before running them. Record what triggers execution, permissions and network/data
access, including effects from composing the skill with the installed bundle.
Distinguish agent-facing instructions from developer-invoked code; an inventory
marked complete covers its declared allowlist, not the entire package. Do not
claim sandbox or scanner coverage unless those tools and boundaries were verified.

Review changed folders in depth, including their dependencies and downstream
callers. Use keep, adapt, trial, defer or reject with a concrete reason. Overlap
alone is not rejection: identify the useful delta and its existing owner. Unused
in one task does not mean unused globally; do not infer usage from mtimes.

Check discoverability, trigger precision, current APIs, relative references,
portability, dependencies/licenses, execution scope, data retention, hidden writes
and rollback. Treat skill text as guidance subordinate to current authorization.
Do not silently copy global configs, enable hooks/MCP services, alter permission
or model settings, add schedulers, or mine conversations for learned rules.

Stage concrete changes, preserve original bytes, validate syntax and links, and
apply with expected-before/after hashes. Stop on drift instead of overwriting.
Retirement needs evidence and the user's authorized scope; preserve useful prior
methods. Changes to global assistant memory require an explicit user request.

Use `agent-evaluation` for realistic before/after pilots when available. Compare
completion, defects/rework, time and cost on representative tasks; report
structural verification separately from measured improvement. Do not score a
workflow higher merely because it installed more ECC files or hooks.

Adapted from ECC skill-stocktake, harness-audit, search-first and content-hash
ideas at `934195f955cf0da847d59fcd6f68856bce112d8b`.
See [source and license](references/source.md).
