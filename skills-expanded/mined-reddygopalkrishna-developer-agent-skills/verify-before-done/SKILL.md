---
name: verify-before-done
description: Proves a code change works before calling it done by finding and running the project's build, typecheck, lint and tests, reading the output and fixing failures, plus a browser check for UI changes. Use when finishing any coding task, before saying a change is complete, fixed or working, before handing work back for review, or when the user asks to verify, check or test a change.
license: MIT
---

# Verify Before Done

"Done" means you ran the project's own checks on the final code and saw them pass. Never say a change works, is fixed, or is complete based on reading the code. Report what you ran and what it printed.

## When to use

- At the end of every coding task, before telling the user it is finished.
- After fixing a bug, before saying it is fixed.
- When the user asks "does it work?", "verify this", "run the checks".

Not for: designing a test suite (use the test-strategy skill) or writing new unit tests (use the unit-testing skill). This skill runs what exists and checks the result.

## Workflow

1. **Find the checks the project actually uses.** CI config is the source of truth, because it is what gates merges. Look in this order:
   - CI files: `.github/workflows/*.yml`, `.gitlab-ci.yml`, `azure-pipelines.yml`, `Jenkinsfile`, `.circleci/config.yml`.
   - Task runners: `package.json` scripts, `Makefile`, `justfile`, `Taskfile.yml`, `tox.ini`, `noxfile.py`.
   - Project docs: README, CONTRIBUTING, any agent instructions file.
   - If none of these exist, use the ecosystem defaults in the table below.
2. **Get a baseline when you can.** Before changing code, run the checks once. Failures that exist before your change are not yours, but you must report them. If you only start verifying at the end, say which failures you could not attribute.
3. **Run the checks on the final code, in this order**, stopping to fix as you go:
   1. Install or restore dependencies if the lockfile changed.
   2. Build / compile.
   3. Typecheck.
   4. Lint and format check (use check mode, such as `prettier --check` or `ruff format --check`, not write mode, unless the project expects auto-fix).
   5. Tests: run the tests closest to your change first for fast feedback, then the full suite or the CI test command.
4. **Read the output, not just the exit code.** Note the counts (passed, failed, skipped). Look for new warnings, deprecation notices you introduced, and tests that were skipped or did not run at all. "0 tests ran" is a failure, not a pass.
5. **Fix failures caused by your change, then rerun the failed step and everything after it.** Repeat until clean. If a failure is pre-existing or unrelated, leave it alone and report it with the evidence.
6. **For UI or web changes, check in a browser** (next section). Backend-only, library and CLI changes skip this step.
7. **Report** using the template below.

## Default commands by ecosystem

Use these only when the project defines nothing of its own.

| Ecosystem | Build | Typecheck | Lint | Test |
| --- | --- | --- | --- | --- |
| JS/TS (npm, pnpm, yarn) | `npm run build` | `npx tsc --noEmit` | `npm run lint` | `npm test` |
| Python | `python -m build` (packages only) | `mypy .` or `pyright` | `ruff check .` | `pytest` |
| Go | `go build ./...` | (part of build) | `go vet ./...` | `go test ./...` |
| Rust | `cargo build` | (part of build) | `cargo clippy --all-targets` | `cargo test` |
| Java / Kotlin (Maven) | `mvn -q compile` | (part of build) | project plugins | `mvn test` or `mvn verify` |
| Java / Kotlin (Gradle) | `./gradlew build` | (part of build) | project plugins | `./gradlew test` |
| C# / .NET | `dotnet build` | (part of build) | `dotnet format --verify-no-changes` | `dotnet test` |

Only run a tool the project already has installed or configured. Don't add a new linter or type checker as part of verifying.

## Browser check for UI changes

A green test suite does not prove a page renders. For any change to markup, styles, client code, routing or a frontend build config:

1. **Start the dev server** the project uses (for example `npm run dev`), in the background, and wait until it reports it is ready.
2. **Use whatever browser tool you have**: a built-in browser, or a browser automation MCP server such as Chrome DevTools MCP or Playwright MCP. Then check:
   - [ ] The changed page loads with no error overlay and no blank screen.
   - [ ] The console has no new errors (warnings are worth a note).
   - [ ] Network requests the page makes succeed: no new 4xx/5xx responses, no failed asset loads.
   - [ ] The key flow you changed works end to end: click the button, submit the form, see the result.
   - [ ] The layout holds at a narrow mobile width (about 375 px) and at desktop width.
   - [ ] Take a screenshot as evidence if the tool supports it.
3. **If you have no browser tool**, run the project's existing end-to-end tests (Playwright, Cypress, Selenium) if it has them. If not, give the user a short manual checklist: the URL to open, what to click, what they should see. Mention that they can add a browser MCP server so this can be checked automatically next time.
4. **Stop the dev server** when you are done.

## Rules

- **No proof, no claim.** If you could not run a check (missing tool, no network, needs secrets), say exactly which check and why. Never round "I couldn't run it" up to "it works".
- **Never make checks pass by weakening them.** Don't skip or delete tests, loosen assertions, add `@ts-ignore` / `# type: ignore` / `eslint-disable`, raise timeouts blindly, or commit with `--no-verify`. If a check is truly wrong, explain why and ask the user.
- **Don't fix unrelated failures silently.** Report them. Fixing them is a separate task the user can approve.
- **Verify the final state.** Any edit after your last check run means the checks must run again.
- **Don't touch shared environments.** Verification runs locally or in CI. Never deploy, migrate a shared database, or call production services to verify, unless the user explicitly asks.

## Report template

```markdown
Verification
- Build: `npm run build` — passed
- Typecheck: `npx tsc --noEmit` — passed
- Lint: `npm run lint` — passed (0 warnings)
- Tests: `npm test` — 214 passed, 0 failed, 2 skipped (skipped before my change)
- Browser: /settings loads, no console errors, save flow works, layout OK at 375 px
- Not verified: e2e suite (needs staging credentials)
- Pre-existing failures: `api/orders.test.ts` "refund rounding" fails on main too
```

## Anti-patterns

- **"This should work."** Reasoning about code is not verification. Run it.
- **Exit code only.** A test command that found no tests, or a build that printed errors and exited 0, looks green.
- **Partial runs reported as full.** Running one test file and saying "tests pass".
- **Fix, then don't rerun.** The last edit broke something the earlier run would have caught.
- **Browser skipped for UI work** because unit tests passed.
- **Green by deletion.** Removing the failing test instead of fixing the code.

## Done when

- Every check the project's CI runs has been run locally on the final code, or listed as not run with a reason.
- All failures caused by the change are fixed; pre-existing ones are reported with evidence.
- UI changes were checked in a browser, by e2e tests, or with a manual checklist given to the user.
- The user got a report listing each command and its result.
