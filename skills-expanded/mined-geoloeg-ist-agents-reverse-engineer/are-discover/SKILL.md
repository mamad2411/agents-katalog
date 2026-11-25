---
name: are-discover
description: Discover files in codebase
disable-model-invocation: true
---

List files that would be analyzed for documentation.

<execution>
## STRICT RULES - VIOLATION IS FORBIDDEN

1. Run ONLY this exact command: `npx agents-reverse-engineer@$VERSION discover $ARGUMENTS`
2. DO NOT add ANY flags the user did not explicitly type
3. If user typed nothing after `/are-discover`, run with ZERO flags

## Steps

1. **Read version**: Read `.claude/ARE-VERSION` → store as `$VERSION`. Show the user: `agents-reverse-engineer v$VERSION`

2. **Run the discover command in the background** using `run_in_background: true`:
   ```bash
   npx agents-reverse-engineer@$VERSION discover $ARGUMENTS
   ```

3. **Monitor progress** by polling the latest progress log:
   - Wait ~10 seconds (use `sleep 10` in Bash), then use **Glob** to find the latest `.agents-reverse-engineer/progress-*.log` file, and **Read** it (use the `offset` parameter to read only the last ~20 lines for long files)
   - Show the user a brief progress update
   - Check whether the background task has completed using `TaskOutput` with `block: false`
   - Repeat until the background task finishes
   - **Important**: Keep polling even if no progress log exists yet (the command takes a few seconds to start writing)

4. **On completion**, read the full background task output and report number of files found.

6. **Review plan and suggest exclusions**:
   - Read `.agents-reverse-engineer/GENERATION-PLAN.md` and `.agents-reverse-engineer/config.yaml`
   - Scan the Phase 1 file list and classify files into these categories:
     - **Test/spec files**: matches like `*.test.*`, `*.spec.*`, `__tests__/**`, `__mocks__/**`, `*.stories.*`, `*.story.*`
     - **CI/CD configs**: `.github/workflows/*.yml`, `.gitlab-ci.yml`, `Jenkinsfile`, `.circleci/**`, `.travis.yml`
     - **Tool configs**: `.eslintrc*`, `.prettierrc*`, `jest.config.*`, `.editorconfig`, `babel.config.*`, `webpack.config.*`, `vite.config.*`, `rollup.config.*`, `tsconfig*.json`, `.lintstagedrc*`, `.huskyrc*`, `.stylelintrc*`, `commitlint.config.*`
     - **Migration files**: paths containing `migrations/` or matching `*.migration.*`
     - **Fixture/snapshot files**: `__snapshots__/**`, `*.fixture.*`, `fixtures/**`, `test-data/**`, `testdata/**`
     - **Type declarations**: `*.d.ts` (not source code, auto-generated or ambient)
     - **Docker/infra**: `Dockerfile*`, `docker-compose*`, `*.Dockerfile`, `k8s/**`, `terraform/**`, `helm/**`
   - For each category, count how many files from the plan match and list up to 3 example filenames
   - **Skip categories with zero matches** — only present categories that have files in the plan
   - Also skip patterns that are already in the current `config.yaml` exclude list
   - Present the findings in a summary table showing category, file count, example files, and proposed glob patterns
   - Ask the user which categories to exclude using `AskUserQuestion` with `multiSelect: true`
   - For accepted categories, use the **Edit** tool to append the corresponding glob patterns to the `exclude.patterns` array in `.agents-reverse-engineer/config.yaml`
   - After editing, briefly confirm what was added
</execution>
