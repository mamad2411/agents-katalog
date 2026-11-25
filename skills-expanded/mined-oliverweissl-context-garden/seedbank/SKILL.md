---
name: seedbank
description: Maintain a small, generated AGENTS.md of repository facts (build commands, conventions, invariants, past mistakes) that were rediscovered often or were costly to get wrong. Use at task start to check cached facts, and at task end to log and promote what you had to dig for.
allowed-tools: Bash(${CLAUDE_SKILL_DIR}/bin/seedbank *), Bash("${CLAUDE_SKILL_DIR}/bin/seedbank" *)
---

# seedbank

!`"${CLAUDE_SKILL_DIR}/bin/seedbank" mode --banner`

Agents that do not expand the line above (e.g. Codex): run
`<this-skill-dir>/bin/seedbank mode --banner` first and follow it.

Offline fact store + profiler. It counts rediscoveries and mistake cost;
you supply the fact text and decide what to promote. Nothing is promoted
just because it was seen once; promotion is always a deliberate `promote` call. Formulas: `references/scoring.md`.

`seedbank` is not on `PATH`: always run it as `<this-skill-dir>/bin/seedbank`. State
lives in `<git repo root>/.seedbank/`.

1. **Start:** read `AGENTS.md`. If it answers your question, skip
   re-discovery.
2. **While working**, log only "how does this repo work" discoveries, not
   every file you touch (with the plugin hook, Read/Grep/Glob and
   read-only Bash such as cat/sed/grep/rg/find are logged automatically):
   ```
   bin/seedbank observe run --scope <topic> -- <command...>
   bin/seedbank observe mistake "<rule you broke>" --scope invariants [--source <file>]
   bin/seedbank observe fact "<invariant>" --scope invariants
   ```
3. **End:** `bin/seedbank candidates`, then
   ```
   bin/seedbank promote <key> --representation "<compact text>" --tier hot [--critical]
   bin/seedbank promote <key> --tier warm --scope <topic>
   bin/seedbank compile
   ```
   A correctness/safety invariant is always worth promoting: use
   `--critical` so it's protected from budget-based eviction.
   Promote refuses a fact contradicting one in the same scope; re-run with
   `--replace <id>` or `--force`. `compile` rewrites only the region
   between `<!-- seedbank:begin -->`/`<!-- seedbank:end -->` and excludes
   stale facts (source changed since promotion) instead of serving them as
   still true; `--critical` facts stay, marked "(source changed — verify)".
   With the plugin, a Stop hook reminds you once per session when this
   session produced candidates; hand the curation to the `gardener` agent
   to keep it out of your context, or do step 3 yourself.
4. Existing hand-written `AGENTS.md`/`CLAUDE.md`: `bin/seedbank import <path>`.
5. Sharing facts: `bin/seedbank export --out f.json`; the recipient runs
   `bin/seedbank import f.json` (refused unless the repo fingerprint matches).

Hook setup, tiers, what to commit: `references/guide.md`.
Full CLI: `references/schema.md`.
