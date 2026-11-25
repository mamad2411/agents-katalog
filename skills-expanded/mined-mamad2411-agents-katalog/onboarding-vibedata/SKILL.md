---
name: onboarding-vibedata
description: Prepare or refresh a data-engineering repository for VibeData while preserving existing code and conventions.
disable-model-invocation: true
---

# Onboarding VibeData

Invoke explicitly with `/vibedata-repo-skills:onboarding-vibedata` in Claude Code or `$onboarding-vibedata` in Codex.

Prepare reusable repository context. Keep customer conventions and application behavior. A normal source/model task uses existing context; it does not start onboarding.

## Workflow

1. **Inspect.** Resolve this installed directory as `skill_root` and the customer repository as `repo_root`. Run `python3 "<skill_root>/scripts/inspect_repo.py" --root "<repo_root>"`. Read discovered instructions, maps, conventions and representative code as text. For selected Studio/DuckDB, check [Domain readiness](references/studio-duckdb.md). Use [brownfield](references/brownfield.md) for an existing implementation or partial context, or [greenfield](references/greenfield.md) for an empty implementation. Record evidence-backed `C-n` conventions and confirmation states; do not ask again about established decisions. Done when mode, ownership and gaps are known without application execution.
2. **Reconcile.** Follow the [artifact contract](references/artifact-contract.md) for canonical instructions, preservation and mapped destinations. Reuse existing conventions before defaults. Require a preservation ledger when merging, moving or replacing existing instructions. Present actual conflicts with sources and effects. Done when retained destinations are known and pending decisions identify their dependent writes.
3. **Propose.** State context changes. For compatibility changes, custom-path workarounds or runtime limitations, read [compatibility](references/compatibility.md). Preserve typed review IDs/text through triage; keep edit approval separate. Emit procedure skills only for confirmed procedures. Done when each diff has an input revision, disposition and readiness effect.
4. **Apply.** Merge independent context and approved changes into live artifacts. Preserve human edits and map extensions. If a write is denied, keep its proposed path blocked; an alternate location requires an explicit compatibility decision. Continue other writable artifacts. Done when the artifact contract is complete or each missing item has a specific blocker.
5. **Verify.** Follow the [verification contract](references/artifact-contract.md#verification) for checks, selected-runtime loading, rehearsals and authorized execution. Write [the report](templates/onboarding-report.md): Changes, Checks, Blockers. Separate context, runtime loading, sandbox execution, persistent Domain state and conditional Studio lifecycle. Done when each has evidence or a named gap, preservation is checked, and unchanged reruns leave artifact bytes unchanged.

Onboarding does not authorize production data writes, application conversion, unrelated repair, provisioning, commits, pushes or publication. Authentication failures stop the affected operation; record the login/refresh action without substituting a provider.
