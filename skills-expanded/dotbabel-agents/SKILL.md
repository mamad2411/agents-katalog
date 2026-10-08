# Repository Guidelines

## Project Structure & Module Organization

This repository is a dual-purpose checkout: the published `@dotbabel/dotbabel` package and a personal Claude Code configuration. Core Node implementation lives in `plugins/dotbabel/src/*.mjs`; CLI entrypoints live in `plugins/dotbabel/bin/`. Shell helpers, hooks, and templates sit under `plugins/dotbabel/{scripts,hooks,templates}`. Tests live in `plugins/dotbabel/tests/` and mix Vitest, Bats, and shell harnesses. Shared content for consumers is kept in `commands/`, `skills/`, `agents/`, `schemas/`, `docs/`, and `examples/`.

## Build, Test, and Development Commands

Run `npm ci` first. Use `npm test` for the Vitest suite and `npm run coverage` for coverage output. Run `npx bats plugins/dotbabel/tests/bats/` for shell integration coverage and `bash plugins/dotbabel/tests/test_validate_settings.sh` for settings validation. `npm run lint` checks Markdown/JSON/YAML formatting and exported JSDoc coverage; `npm run shellcheck` lints shell scripts. `npm run dogfood` runs the packaged validators against this repo, and `npm run build-plugin` builds the distributable plugin.

## Coding Style & Naming Conventions

Target Node 20+ and keep source in ESM `.mjs` files. Follow `.editorconfig`: UTF-8, LF, final newline, and 2-space indentation; `Makefile` is the only tab-indented exception. Prettier governs Markdown/JSON/YAML formatting (`npm run format`) with `printWidth: 100` and double quotes. Name CLI bins `dotbabel-*`, keep tests as `*.test.mjs` or `*.bats`, and add JSDoc to every exported symbol under `plugins/dotbabel/src/`. Avoid adding new runtime dependencies without a strong justification.

## Testing Guidelines

Keep unit tests in `plugins/dotbabel/tests/**/*.test.mjs`. Use Bats for cross-shell or CLI regression scenarios and plain `.sh` harnesses where needed. Coverage thresholds are enforced in Vitest: 85% lines, 85% functions, 80% branches, and 85% statements. For bug fixes, add a failing regression test first and make it pass in the same change.

## Commit & Pull Request Guidelines

Follow conventional commits such as `feat(handoff): ...`, `fix(cli): ...`, `test(sync): ...`, and `chore(main): ...`. Prefer a dedicated worktree like `.claude/worktrees/my-change` instead of editing in the main checkout. PRs must include `## Summary` and `## Test plan`. If you touch protected paths such as `plugins/dotbabel/src/**`, `plugins/dotbabel/bin/**`, `README.md`, or `.github/workflows/**`, include either `## Spec ID` or `## No-spec rationale`. Record the exact verification commands you ran, and do not use `--no-verify` or amend published commits.

## Universal rule floor

<!-- dotbabel:rule-floor:begin -->
<!-- AUTO-GENERATED FROM CLAUDE.md by dotbabel-generate-instructions. Do not edit. -->

## Local filesystem conventions

- All projects live at `$HOME/projects/`. Do not search the home directory or default locations.
- Global dotbabel config lives wherever you cloned `dotbabel` and is symlinked into `your CLI's user-scope config dir`. Edit files in the clone, not `your CLI's user-scope config dir` directly.

## Disk hygiene

- The Windows C: drive on this machine is small. The WSL virtual disk only grows; it never shrinks on its own. Every gigabyte you write inside the distro stays allocated on C: until a manual compact.
- After you run containerized tests (testcontainers), run `docker volume prune -f`. Anonymous test volumes leak ~70 MB per run and are the main growth driver.
- Keep large artifacts, datasets, and clones on `/mnt/wsl/storage`, not on the distro disk.
- Do not download large toolchains or browser bundles (Playwright browsers, Go module trees) unless the task needs them. Prefer existing installed versions.
- Cleanup is automated on the Windows side: scheduled tasks `WSL Weekly Maintenance` and `WSL Monthly Compact` run `C:\WSL\wsl-maintenance.ps1` (log: `C:\WSL\maintenance.log`). Do not build ad-hoc cleanup scripts; extend that one.

## Code Changes

- Before proposing fixes, **read the relevant source files**. Use `Grep` + `Glob` + `Read` to locate current behavior.
- Cite `file:line` references in every analysis. Claims without citations are not grounded.
- Do not propose edits until the analysis is confirmed against real code. "The file is probably named X" is not grounding — open it.
- When unsure, invoke the `/ground-first` skill to enforce the read-first discipline.
- **Surface assumptions before coding.** If a request has multiple valid interpretations, list them explicitly. In interactive sessions, ask before picking one. In autonomous/headless mode, state the chosen interpretation and proceed. "Make it faster" → clarify which dimension (latency, throughput, perceived UX) before writing code.
- **Surgical orphan cleanup.** When your changes make an import or variable unused, remove it. Remove a function only after verifying it is not part of a public/exported API and has no remaining references (use a repo-wide search); otherwise keep it or deprecate it. Don't remove pre-existing dead code your changes didn't create — mention it instead.

## Root Cause Before Fix

- For any bug or data discrepancy, perform a grounded audit (read the actual code paths, check deployment state, verify data sources) BEFORE proposing a fix or plan. Do not accept the first plausible hypothesis.
- State evidence (file:line, log snippet, commit sha) for each claim in the diagnosis.
- Present at least two candidate root causes with evidence for and against each before settling on one.
- **Do not write code until the user approves the audit.** In interactive sessions, wait for explicit sign-off. In autonomous/headless mode, emit the audit and state the chosen root cause before proceeding.

## Testing

- Run the project's **full** test suite locally before merging any PR that modifies a file matching `critical_paths` (see the `quality` key in `.dotbabel.json`) or anything consumed by downstream consumers.
- Never claim a test failure is "pre-existing" without proving it. Required proof:
  ```bash
  git stash && <test-command> ; git stash pop
  ```
  If the failure survives the stash, it's pre-existing. If it disappears, your change introduced it.
- Detect the test runner from the project, don't guess:
  - `Makefile` with a `test` target → `make test`
  - `package.json` → `npm test` (or `pnpm test` / `yarn test` based on the lockfile)
  - `go.mod` → `go test ./...`
  - `pyproject.toml` → `pytest` or `uv run pytest`
- Partial test subsets are fine for iteration. Full suite is required before pushing or merging.

## TDD and verification

- **Always follow TDD for new features:** write tests first (positive, negative, boundary), then implement until tests pass.
- **For bug fixes:** write a failing test that reproduces the issue, fix, then verify.
- **Transform vague tasks into verifiable goals before starting.** "Fix the bug" → "write a test that reproduces it, then make it pass." For multi-step tasks, emit a concise plan with explicit verification at each step: `Step → verify: [check]`. Default to 5 bullets or fewer; exceed that only when the task is genuinely complex.
- **When editing Go files, run `gofmt -w <file>` immediately after editing.** Never leave Go files with formatting issues.
- **When reporting status or roadmap progress, verify each item against actual code or config before marking it complete.** Do not assume completion — show the evidence.

## Test Plan Verification

- Run every command in the test plan verbatim, in order. Paste the **last 10 lines of output** for each.
- If any command was skipped or inferred rather than run, say so explicitly. Never claim completion based on partial runs.

## Version control discipline

- **Never push to `main` (or any branch) without explicit user instruction.** Commit locally and wait for the user to say "push".
- **Never merge a PR without explicit user instruction.** Do not use `--auto`, `gh pr merge`, or any merge path unless the user says "merge" for that specific PR.
- **Never force-push, force-rebase, or `git reset --hard` a branch that is not yours.** If conflict resolution is ambiguous, stop and ask.
- **Never undo or revert another session's committed work.** Prior session commits are authoritative. If a merge conflict arises with prior session work, stop and ask.
- Before pushing any commit, review staged files for sensitive content (.env, credentials, API keys). Use `.gitignore` proactively.
- Prefer new commits over `--amend`. Never pass `--no-verify` or `--no-gpg-sign` unless the user explicitly asks.

## Worktree discipline (for any non-trivial change)

- **Default to git worktrees for anything non-trivial.** New features, bug fixes, code reviews, refactors, and spec work belong in a fresh worktree under `.claude/worktrees/<slug>/`, branched from the latest `origin/main` (run `git fetch origin main` first).
- The main checkout is effectively read-only for agentic work unless the user says "do it on main" for this specific task. A one-line typo fix they want committed directly is fine; anything larger is not.
- Never use `gh pr checkout`, `git checkout <other-branch>`, `git switch`, or `git stash` in the main checkout as a way to swap contexts; those operations silently corrupt any concurrent session editing the same checkout.
- **Respect other sessions' worktrees and branches.** Multiple agents and humans work concurrently. Before creating a worktree, run `git worktree list` and scan for anything that looks active (recent HEAD, branch name matching your intent). Never remove, rename, or force-overwrite a worktree you did not create in this session.
- **Clean up your own worktree when the work lands.** After the PR merges, or after you abandon the task, remove the worktree you created in this session: `git worktree remove .claude/worktrees/<slug>` from the main checkout, then `git worktree prune`. This deletes only the checkout directory — the branch and its commits survive. Do it before you end the task. No other session will do it for you, because the rule above forbids them from touching a worktree they did not create.
- **Never remove a worktree that holds content living nowhere else.** Run `git status --porcelain` first. Uncommitted edits to tracked files, and untracked files absent from `origin/main`, are destroyed by removal — commit them to the branch or ask the user before you remove. Regenerated exports, coverage output, build artifacts, and `test-results/` are safe to discard.

## Worktree & Sandbox Conventions

- Before starting work in a worktree, verify it is clean (`git status`) and not already claimed by a concurrent headless worker (check for lockfiles/PID files).
- Use `$CLAUDE_PROJECT_DIR` in hooks and scripts rather than relative paths.
- When sandbox blocks writes to `/tmp` or the worktree path, emit results to stdout as a fallback and flag the limitation explicitly.

## PR Conventions

- Create PR bodies via `gh pr create --body-file <file>`, not heredoc. Heredocs mangle backticks and break the required Spec ID block.
- Required sections in every PR body:
  - `## Summary` — 1–3 bullets describing the change.
  - `## Test plan` — bulleted markdown checklist.
  - `## Spec ID` heading followed by the spec id — if the project uses spec IDs (check for `specs/` or `docs/specs/`). Must be an H2 heading; `dotbabel-check-spec-coverage` extracts it via H2 regex.
- **The `## Spec ID` section must contain nothing but the id(s).** The extractor captures everything from that heading to the next H2 heading _or the end of the body_, then splits it on whitespace and treats every token as a spec id. Anything trailing — a generated-by footer, a sign-off, a link — is parsed as unknown spec ids and fails the gate. Put `## Spec ID` last with nothing after it, or follow it with another H2. `## No-spec rationale` is exempt — its body is only checked for non-emptiness, never tokenized — so prose and trailing content are safe there.
- Never merge a PR with failing CI without explicit user approval.

## Shell & Scripting

- Use `bash` (not `zsh`) for monitor scripts, loops, and anything using `read`, `$?`, or `$status`. `zsh` makes `status` read-only and breaks scripts silently.
- Avoid reserved variable names: `status`, `path`, `pwd`, `prompt`, `HISTFILE`. Prefer `result`, `workdir`, `current_status`.
- Before long-running work, verify session sanity:
  - `pwd` exists (sessions die silently on deleted worktrees).
  - `git status` is clean (or intentionally dirty) — no unexpected locks.
  - The branch is what you expect.
- Prefer `gh <cmd> --body-file` or `--json` + `--jq` over shell-interpolated strings.

## Deploy discipline

- **Never deploy to production without explicit user instruction.** Use the project's sanctioned deploy command (e.g. `/ship`, not direct `vercel --prod` or `flyctl deploy`).
- **When designated as autonomous** (batch task, pipeline, overnight run), do not stop for permission at intermediate steps. Execute fully. Only pause for genuinely destructive or irreversible actions.
- **Autonomous dry-run contract.** Before invoking any command that writes to production data, emit a one-block plan: exact command, every flag with a justification, expected scope, estimated runtime. Then execute without further prompts. Never pass `--force` without explicit user authorization for the specific run.

## Implementation vs Spec

- When the user asks for an implementation, a fix, a PR, or "just do X" — **cap planning at a 5-bullet sketch, then edit**. Do not spin up spec docs.
- Use `/spec` only when the user explicitly asks for a spec, design doc, RFC, or says "let's spec this out."
- If a task genuinely needs a plan longer than 5 bullets, write it inline in the response — don't create a planning file unless asked.

## Headless Mode

For recurring sweeps (Dependabot, cron, CI-triggered agents), use headless mode to skip tool-approval prompts.

## AI code quality floor

Use the resolved project policy. `dotbabel quality` measures it with the tools the repository already has. It never installs a checker.

- Run `dotbabel quality explain` before a policy-sensitive change. Add `--rule <id>` for one rule.
- Run `dotbabel quality detect` to see the components, the selected tools, and the trust state. It executes no project command.
- Run `dotbabel quality check --profile fast` while you edit. Run `--profile pr --base <ref>` before a pull request. Keep `--profile deep` for a scheduled audit.
- Add `--path <glob>` to narrow a run to one package. Add `--all` to check the whole repository instead of a diff.
- Read the exit code. `0` is no error verdict. `1` is a policy failure. `2` is a missing tool, report, base, or trust. `64` is invalid usage. Never report `2` as a pass.
- Set project policy in the repository `.dotbabel.json` under the `quality` key. Do not lower a shipped threshold to make a check pass.
- Trust project commands by their exact repository path. Pass `--allow-project-commands` for one CI run only.
- Resolve an ambiguous tool choice in configuration. Do not guess, and do not install a missing tool.
- Simplify control flow before splitting a function. Split a file only when each result has one coherent responsibility.
- Add tests for behavior and failure boundaries. Reject assertion-free or implementation-coupled coverage padding.
- Do not add abstractions only to reduce local metrics. Remove obsolete code instead of moving it.
- Do not replace a safe `unknown` value with a cast. Narrow or validate untrusted data before use.
- Treat each new suppression as a review finding. Keep each exception narrow, temporary, and justified.
- Exclude generated and vendor code only with file evidence. Do not exclude difficult code for convenience.
- Use changed-code checks and no-regression rules in legacy repositories. Report improvements that remain above a target.
- Report unsupported, unavailable, and not-configured measurements. Never claim that an unsupported metric passed.

## Communication

**Hard caps. Not aspirational — enforced.**

- Default response is ≤3 sentences. Prose, not bullets. No headers.
- Never restate the question. Never preface with "Let me…", "I'll…", "Here's…", "Looking at…", "Based on…". Start with the answer.
- Never summarize what you just did at end-of-turn. The diff and tool output already show it. One line max if a follow-up genuinely matters; otherwise zero lines.
- No bullet lists unless the answer is genuinely ≥3 peer items. Two items = a sentence with "and".
- No headers (`##`, `###`) in chat responses. Headers belong in files, not conversation.
- Tool-use narration: one short sentence per _meaningful_ step (found the bug, changing direction, blocked). Silent for routine reads/greps.
- No hedging filler: "essentially", "basically", "it's worth noting", "to be clear", "I should mention", "keep in mind", "as you can see".
- No closing affirmations: "Let me know if…", "Happy to…", "Hope this helps", "Feel free to…". Just stop.
- Code answers: show the code. Skip the prose explanation unless asked. If the user wants the reasoning they'll ask.
- When in doubt: cut it. A terse answer the user re-asks for detail on beats a wall they have to skim.

**Length rubric.** Simple factual question → one sentence. Code change → the diff + ≤1 line of context. Investigation result → ≤3 sentences + file:line. Spec/architecture discussion → as long as needed, but earn every paragraph.

## Language: ASD-STE100 Simplified Technical English

**Write all chat output to the user in ASD-STE100 Simplified Technical English (STE).** This rule applies to every AI agent that reads this rule floor.

- Use approved STE words where the dictionary permits. Use one word for one meaning.
- Write short sentences. Use a maximum of 20 words in an instruction. Use a maximum of 25 words in a description.
- Use the active voice. Use the present tense where possible.
- Give one instruction in each sentence. Start each instruction with a verb.
- Write paragraphs with a maximum of 6 sentences.
- Do not use idioms, slang, or Latin abbreviations such as "e.g." and "i.e.".
- Use the articles "a", "an", and "the". Do not remove them.
- Keep technical names, code, file paths, commands, and quoted output as they are. STE does not change code.
- Put safety warnings before the instruction they apply to.
- The Communication hard caps stay in effect. STE controls the style; the caps control the length.

## Protected paths (dogfood)

This repository governs itself with `@dotbabel/dotbabel`. The authoritative
list of protected paths lives in `docs/repo-facts.json` and every entry must
be documented in every rule-floor file listed in
`docs/repo-facts.json:rule_floor_files`; `dotbabel-check-instruction-drift`
enforces this invariant.

- `CLAUDE.md` — canonical rule-floor source.
- `README.md` — top-level public README.
- `AGENTS.md` — project-scoped instructions for Codex / Copilot / OpenCode CLI.
- `GEMINI.md` — project-scoped instructions for Gemini / Antigravity CLI.
- `.github/workflows/**` — CI pipelines.
- `.github/copilot-instructions.md` — project-scoped instructions for GitHub Copilot.
- `.claude/**` — skill manifest, settings, hooks.
- `docs/repo-facts.json` — the facts source of truth.
- `docs/specs/**/spec.json` — spec metadata governed by the spec-anchored workflow.
- `plugins/dotbabel/src/**` — the npm package's source of truth.
- `plugins/dotbabel/bin/**` — the shipped bin entrypoints.
- `plugins/dotbabel/templates/**` — scaffolding templates consumers install (includes `plugins/dotbabel/templates/cli-instructions/**`, the user-scope rule-floor templates generated by `dotbabel-generate-instructions`).

Any PR touching one of these paths must carry either `Spec ID: dotbabel-core`
or a `## No-spec rationale` section in its body.

The rule-floor block (between `<!-- dotbabel:rule-floor:begin -->` and `<!-- dotbabel:rule-floor:end -->` markers) in `AGENTS.md`, `GEMINI.md`, and `.github/copilot-instructions.md` is **auto-generated from this file** by `dotbabel-generate-instructions`. Edit the rule floor here in `CLAUDE.md`; re-run the generator (`npx dotbabel-generate-instructions` or `dotbabel sync`) to fan it out. Hand-editing the block in a host file will be reverted by the next regen and is detected by `dotbabel-check-instruction-drift`.

## Skills, Commands, and Discovery

Do not maintain static command or skill tables in instruction files. When editing
this dotbabel repository, the authoritative inventory is generated from artifact
frontmatter:

```bash
node plugins/dotbabel/bin/dotbabel-index.mjs --check
node plugins/dotbabel/bin/dotbabel-list.mjs --type skill
node plugins/dotbabel/bin/dotbabel-list.mjs --type command
node plugins/dotbabel/bin/dotbabel-search.mjs <query>
node plugins/dotbabel/bin/dotbabel-show.mjs <id> --type skill
```

<!-- dotbabel:rule-floor:end -->
