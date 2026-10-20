# Notes Garden POC

A notes garden: click to plant a note, Jev (an LLM judge) picks a species and which notes connect (roots).
Being upgraded from an SVG/emoji toy to a 2D PixiJS garden, top-down oblique. Work is split into small PRs.

## Every session: do exactly one PR

1. Read `TRACKER.md`. Take the PR marked "Next up" (or the one the human names). Do not read the whole of `PLAN.md`.
   Read only its sections 1a to 3, and that PR's row: `grep -n "^| <N> |" PLAN.md`.
2. Create branch `pr-<NN>-<slug>` (git may not exist until PR 0).
3. Implement only what that row says. If it needs more than about 300 changed lines, stop and propose a split.
4. Verify: `npm run typecheck` (from PR 0a), `npm run build`, and `npm test` once it exists. Do the row's "Verify" step. For scene PRs, report FPS at `?demo=500`.
5. Update `TRACKER.md`: set status to `review`, fill the branch/PR link, advance "Next up", and append a handoff note (3 lines max).
6. Commit, and open the PR only if the human asks. Then **stop**. Never start the next PR.

If the plan and the code disagree, or a decision is missing, ask. Do not silently redesign.

## Conventions

- TypeScript, `strict`, from PR 0a on (until that PR merges the files are still JS). Avoid `any`. No new dependency without asking.
- `src/domain/` and `src/gen/forms/` are pure: no Pixi, no React, no DOM. Unit-test them with `node --test`.
- The scene (`src/scene/`) is imperative Pixi. React renders DOM UI only, never plants.
- Prefer the shortest working change. Mark deliberate shortcuts with `// ponytail: <ceiling and upgrade path>`.
- Determinism: never `Math.random` in anything that shapes a plant. Use `domain/prng.js` with the note's `seed`.
- Do not touch the old SVG/emoji view except in PR 12, which deletes it.
- Keep `VITE_MOCK=1` for local work. Never commit `.env`, never print `OPENROUTER_API_KEY`.
- Do not refactor unrelated code in a PR.

## Reference

- `PLAN.md`: the plan (stack in 1a, structure in 2, working agreements in 3, PR list in 4).
- `TRACKER.md`: status, decisions, handoff notes.
- Note schema v2 is in `PLAN.md` section 2.
