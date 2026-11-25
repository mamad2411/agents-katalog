---
name: blueprint-repo-baseline
description: "Find the repository's own gates — install, format check, lint, typecheck, build, test — record them, and prove they all pass before anything is touched."
---

# Green before anything moves

Every later change claims "this behaves the same". That claim is measured against these gates, so they
must be the repository's own, and they must be green on the untouched code. A gate that is already red
cannot tell a regression from the state it was in.

1. **Package manager** from the lockfile: `yarn.lock` → yarn, `pnpm-lock.yaml` → pnpm, `package-lock.json`
   → npm, `bun.lockb`/`bun.lock` → bun. The install command must not rewrite the lockfile:
   `yarn install --frozen-lockfile`, `pnpm install --frozen-lockfile`, `npm ci`, `bun install --frozen-lockfile`.
2. **Gates** from `package.json` scripts, in this order when present: a format CHECK (`format:check`, never a
   script that rewrites files), `lint`, `typecheck`, `build`, `test`. Read what each script runs.
   - Leave out a script that needs a service, a browser download or network the machine may not have
     (`test:e2e` and the like), and write why in the record.
   - Read the CI workflows too: CI is the ground truth these approximate. A gate CI runs and `package.json`
     lacks is worth noting.
3. Write `.blueprint/gates.json`:
   ```json
   {
     "packageManager": "yarn",
     "install": "yarn install --frozen-lockfile",
     "gates": [{ "name": "lint", "command": "yarn lint" }, { "name": "test", "command": "yarn test" }],
     "skipped": [{ "name": "test:e2e", "why": "needs a browser download" }]
   }
   ```
   `name` is the script name exactly as `package.json` has it.
4. Run the install, then every gate, and read each exit code — never the last line of output.
5. If any gate is red on the untouched code, **ask**: it is the person's decision whether to fix it first
   (as its own change) or leave that gate out with a reason. Do not change the repository in this step.

Done when the check passes: every recorded gate exits 0 on the untouched default branch.

## Always

- Read `.blueprint/spec.md` if it exists. It is the agreed plan; do not widen it.
- When you need a decision, ask it through the blueprint question tool and stop. Do not guess.
- Change nothing in the repository in this step.
- Say you are done by stopping; the executor runs the check. Do not claim success yourself.
