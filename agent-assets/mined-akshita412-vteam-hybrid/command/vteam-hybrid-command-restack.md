<!-- agent-notes: { ctx: "tech stack reevaluation workflow", deps: [CLAUDE.md, docs/adrs/], state: active, last: "archie@2026-02-12" } -->
Reconsider and update the project's tech stack: $ARGUMENTS

The user wants to re-evaluate some or all of the current tech stack choices. Follow these steps:

## 1. Understand the Current Stack

- Read `CLAUDE.md` to understand the current tech stack and conventions.
- Read all ADRs in `docs/adrs/` to understand past decisions and their rationale.
- Read `pyproject.toml`, `package.json`, `Cargo.toml`, or whatever build config exists to see actual dependencies.
- Summarize the current stack to the user: language, framework, key libraries, build tools, test tools, CI/CD.

## 2. Identify What to Reconsider

Ask the user what's motivating the change. Common reasons include:
- A dependency is abandoned or has security issues
- Performance isn't meeting needs
- Developer experience is poor
- Requirements have changed (e.g., now need mobile support, now need real-time)
- A better alternative has emerged
- Scaling concerns

If the user gave specific arguments (via $ARGUMENTS), focus on those areas. Otherwise, walk through each layer of the stack and ask if they want to reconsider it.

## 3. Research Alternatives

For each area being reconsidered:
- Present 2-4 realistic alternatives with pros/cons relative to the current choice
- Consider migration cost — how much code would need to change?
- Consider ecosystem compatibility — does the alternative play well with the rest of the stack?
- Flag any choices that would require a near-complete rewrite vs. incremental migration

## 4. Make Decisions

For each change the user wants to make:
- Create a new ADR documenting the decision to switch (this supersedes the original ADR)
- In the ADR, document: why the original choice is being replaced, what the new choice is, migration strategy, and risks

## 5. Execute the Migration (if requested)

If the user wants to proceed with changes now (not just evaluate):
- Create a migration plan in `docs/plans/`
- Update dependencies
- Update build configs, CI pipelines, and scripts
- Update imports and code to use new libraries/frameworks
- Update `CLAUDE.md` with the new stack details
- Update `README.md` setup instructions
- Run the test suite after each significant change to catch regressions early

If the migration is large, suggest breaking it into phases.

## 6. Verify

Run the full test suite and build to confirm everything still works. Fix any issues before declaring done.

## 7. Summary

Tell the user:
- What was changed and why (reference the new ADRs)
- What was kept and why
- Any follow-up work needed
- Updated commands for dev/build/test if they changed
