# Working on PHOENIX

- Read [CONTRIB.md](CONTRIB.md) and inspect the current Git state before changing files. Keep
  unrelated work intact; use feature branches from `dev`. Publishing, pushing and merging need
  explicit authorization.
- Use GitHub issues for bugs, substantial tasks, feature requests and ideas. Search before opening
  an issue; link dedicated branches/PRs to it. Small bounded fixes may share a misc branch from dev.
  Follow the label and completion rules in CONTRIB.md: requests/ideas need acceptance before becoming
  tasks; close fully verified implementation tickets after merging to `dev`, with a PR/commit link.
  Reconcile issue checklists and closures at merge checkpoints, not after local implementation.
  An idea in the backlog is not authorization to implement it. Record player-visible changes in
  [CHANGELOG.md](CHANGELOG.md), under Unreleased until a release is actually published.
- Work sequentially, one accepted ticket per cycle: ticket → implementation → changelog → commit
  and PR → wait for all required CI to pass (fix failures) → merge into `dev` and verify issue
  completion → next ticket. Do not start the next implementation while the current PR awaits CI
  or merge; start its branch from the updated `dev` to avoid overlapping work and merge conflicts.
  Release publication remains separately authorized.
- Request Copilot PR review for substantial architecture changes, larger features, medium-to-high
  complexity work, or concrete unresolved concerns. Small, understood changes do not need a routine
  Copilot review; required CI and our own verification still apply. Assess findings against real
  invariants rather than implementing every suggestion automatically.
- Keep changes with their owner. Control Deck is a separate dependency, not source to copy into
  PHOENIX. Bundled in-game Copilot profiles live in `resources/copilots/`, not in this file.
- Use [.agents/skills/codebase-audit/SKILL.md](.agents/skills/codebase-audit/SKILL.md) for systematic
  complexity, defensive-programming and maintainability audits. Ordinary edits do not require a
  whole-codebase audit.
- For UI work read [.agents/skills/phoenix-ui/SKILL.md](.agents/skills/phoenix-ui/SKILL.md); for
  release/CI work read [.agents/skills/phoenix-release/SKILL.md](.agents/skills/phoenix-release/SKILL.md).
  Read actual installed versions and the relevant owner before using version-sensitive APIs.
  For React APIs and upgrades, use the source and compatibility checks in [docs/react.md](docs/react.md).
- Run focused regression tests and `npm run check` for code changes. Report unverified behavior;
  production typechecks do not typecheck every test, and CI is not proof of real Elite input.
- If available, `.context/index.md` and `.context/codex-handoff.md` provide local working context.
  Keep `.context` ignored; never force-add it or put player data and credentials in tracked files.
