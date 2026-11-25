---
name: usage-monitor-workflow
description: Run the usage-monitor delivery workflow end to end — issue with a short plan, plan in docs/planos, worktree, strict TDD (red before green, recorded), local tests, PR with auto-merge, CI incident count, cleanup and a test-case comment on the issue. Implementation is delegated to subagents (backend-dev, frontend-dev, prototype-dev) that run red to green in their worktree, while the session plans, validates and commits. Use for EVERY request that changes the repository, even when the user does not mention the workflow.
allowed-tools: Bash(node .claude/skills/orchestrate/setup/agentes.mjs *), Bash(node .claude/skills/orchestrate/portal/emit.mjs *)
---

# Usage Monitor Workflow

Agents:
!`node .claude/skills/orchestrate/setup/agentes.mjs verificar || true`

The "Fluxo de trabalho" section of `CLAUDE.md` is the rule; this skill is how to execute it. It applies to every request
that changes a versioned file. A question that only asks for an explanation is answered in chat, outside the flow.
No step waits for approval: the `CLAUDE.md` rule is the authorization for commit, push, PR and merge.

## 0. First run: configure the agents for this project

If the `Agents:` block above says `PENDENTE`, the project has no agents configured yet. Do this before planning. If it
says `CONFIGURADO`, skip to section 1.

1. Show the user the detected stack and commands from the block (they come from manifests only; commands marked
   `convenção` are the ecosystem default, not verified in this project).
2. Ask which option they want, with `AskUserQuestion`:
   - **Install for this project (recommended)**: `node .claude/skills/orchestrate/setup/agentes.mjs instalar` writes the
     five agents to `.claude/agents/` from the templates in `.claude/skills/orchestrate/agents/`, each with a
     `Project context` section (stack, commands, rule files). It never overwrites an existing agent.
   - **Use the generic agents**: `node .claude/skills/orchestrate/setup/agentes.mjs dispensar` records the choice and
     stops asking.
3. After installing, read each generated agent and fix what the manifests could not tell: conventions, forbidden
   paths, the real test command if the detected one is a `convenção`. Take the rules from the project's `CLAUDE.md` or
   `AGENTS.md` if present; do not invent any.
4. If the new agents are not available to delegate to, tell the user to restart the session (or reload with `/agents`)
   and run the same request again.

## Who does what (#513)

The session is the Neferpitou orchestrator. Models, effort and tools live only in `.claude/agents/`; this list names the
agent, never the model. Rules against context leakage: `CLAUDE.md`, "Orquestração e agentes".

- **Neferpitou (main session)**: issue, both plans, briefings, worktree, validation, commits, push, PR, merge, cleanup
  and the issue comment. Never writes production code or tests.
- **Implementing agent** (`backend-dev`, `frontend-dev`, `prototype-dev`): red → green, and the fix of a red CI, in the
  worktree named in the prompt.
- **`test-runner`**: step 5 (local tests, test report, diff coverage) and step 7 (watch the CI run, `--log-failed`,
  `ci-incidents.mjs`).
- **`explorer`**: broad search in any step, read-only.

The roles are mandatory, not advice (#515): it is the user's explicit request to use these subagents. Never run the
step 5 or step 7 commands in the main session; call the `test-runner` agent with them.

## Route: work by agent

Subagents run the model and effort set in their frontmatter in `.claude/agents/`: implementers and `test-runner` on
haiku with high effort (`test-runner` since #532), `explorer` without `effort` (#513). Delegate without `model` or
`effort`, except the
escalation in "Validate and send back".

| Work | Agent |
|---|---|
| Sweeps, locating code, gathering facts | `explorer` |
| Tests, typecheck, build, smoke, CI | `test-runner` |
| Back-end code | `backend-dev` |
| Front-end code | `frontend-dev` |
| Prototype, tooling, video, audio | `prototype-dev` |
| Planning, judging, integrating, shared contracts, dependencies, commits | Neferpitou (main session) |

Sonnet enters only by escalation. Never pass `model` in advance, nor because a task looks hard. Haiku costs 5x more above
100K prompt tokens: a large task becomes several small tasks, not one long agent.

Edit directly only a pinpoint tweak to one known file. A long command that needs no judgement (a render, for example)
runs in the background in the main session: it costs no agent tokens.

## Delegate without inflating context

Split only when it pays off: evaluate the demand before opening agents. A small or sequential task goes to one agent.
Parallelism needs several truly independent tasks, never a target number of agents: every return costs one orchestrator
turn with the whole context.

A delegation prompt has at most 12 lines, in this format:

```text
Task <ID>. Briefing: <path>, section <n>.
Edit only: <paths>.
Acceptance: <command that exits 0, or verifiable criteria>.
Return: the agent's standard format.
```

The directory of the prompt is the worktree path. Forbidden in the prompt: conversation summary, another agent's return,
file contents the agent can read, the reason behind the request. Point to a path, do not paste text. Never the
conversation, never a fork. A red verdict comes back as the failing assertion lines; Neferpitou decides the fix.

- At most 4 simultaneous agents. Agents always in the background when there is other work to do.
- Parallel code tasks go in `isolation: "worktree"`. Exception: artefacts in exclusive folders with no shared test suite
  may use the same checkout, because no agent runs or reads another's work.

## Validate and send back

No delivery is accepted on the agent's own report. Check every criterion with your own evidence: diff, execution,
screenshot or a frame extracted from the video.

Run the `emit.mjs` commands from the main checkout, each with `--sessao ${CLAUDE_SESSION_ID}`. The log of rejections and
limits is located from the repo root through `raizRepo()`, so run it from the main checkout and keep the counts in one
place. Register the task on its first call, then give the verdict:

```bash
node .claude/skills/orchestrate/portal/emit.mjs tarefa --sessao ${CLAUDE_SESSION_ID} --id <ID> --titulo "<title>" --dono <agent> --estado andamento
node .claude/skills/orchestrate/portal/emit.mjs veredito --sessao ${CLAUDE_SESSION_ID} --tarefa <ID> --resultado aprovada --texto "Criteria checked."
```

Rejected: `--resultado devolvida`. The command prints the count and the action; follow the printed action, never memory.
Only delivery defects reject: a `BLOQUEADA` return and a usage-limit interruption do not count. Never fix it in the
agent's place. Returns (`devolvida`) and CI incidents are separate counts.

- **`devolver ao mesmo agente`** (return to the same agent): `SendMessage` to the same agent, which keeps its context. The
  first line is `<ID> devolvida: <defect>`. The message carries only the failed criterion, the evidence and the expected
  result. Never resend the briefing. Verdict and `SendMessage` go out in the same turn: each orchestrator turn resends
  the whole session context.
- **`escalar para sonnet high`** (3rd rejection on haiku): run `emit.mjs escalada` and open a new agent of the same type
  with `model: "sonnet"` and `effort: "high"`, because `SendMessage` cannot change the model. No `isolation`: the work
  continues in the path where haiku stopped, which the prompt points to with the open defect. Never paste haiku's
  history.
- **`parar e reportar ao dono do produto`** (3rd rejection on sonnet): stop and report to the user what failed.

```bash
node .claude/skills/orchestrate/portal/emit.mjs escalada --sessao ${CLAUDE_SESSION_ID} --tarefa <ID>
```

`emit.mjs escalada` refuses a task below the limit. Limits live in `LIMITE_REPROVACOES` in
`.claude/skills/orchestrate/portal/emit.mjs` (haiku 3, sonnet 3).

## Prototype gate (visual work)

1. Generate the prototypes in `prototipos/<entrega>/`, one agent per prototype, with genuinely different directions.
2. Open each `prototipos/<entrega>/index.html` in a real browser and validate it there. Give the user those paths.
3. Stop and ask the user to choose. No final version before the choice.

Visual options follow the `usage-monitor-visual-options` skill; the design system is the source for tokens and components.

### Design system

The design system is `docs/design-system/`. Never read it yourself: `explorer` does it, to keep the whole system out of the
main context.

1. Before planning any visual task, delegate to `explorer` with the standard prompt format. Task: locate, in
   `docs/design-system/`, the tokens (colors, type, spacing), the components with their props and usage rules, and any
   written guidelines. Return `file:line` pointers, at most 20 lines. `explorer` is read-only and cannot write files.
2. Write the return to a briefing file (`prototipos/design-system.md`): pointers plus the few values that decide the
   work. Shared specification goes in a briefing, never in the prompt.
3. Every visual task points to that briefing and names the design-system files the agent must read. Prototypes use the
   existing tokens and components only.
4. A new token, component or rule: list what is missing and ask permission first.

If the explorer finds nothing usable in `docs/design-system/`, stop and tell the user; do not invent a design system.

## 1. Issue (always)

Use the issue the user gave. Without one, create it — the first line is mandatory (`CLAUDE.md`, "Convenções"):

```bash
gh issue create --title "<what>" --body-file <scratchpad>/issue.md
```

Body: `🤖 Escrito por Claude Code, a pedido de @edilsonvilarinho`, then the plan in **at most 15 lines**: **O quê**,
**Atividades** (A01, A02… one line each), **Onde**, **Validação**, **Fora** (what is deliberately left out).

In chat, the plan for the user is at most one paragraph. Every chat report stays within 15 lines.

## 2. Plan in `docs/planos/` (activity A01)

`docs/planos/<subject>-<issue>-execucao.md`, modeled on `fluxo-automatizado-496-execucao.md`: provenance (model,
tool, date, branch, commit identity), **Objetivo**, **Fatos confirmados** (each with the command that measured it),
**Decisões**, **Atividades**, **Ponto de situação** (one row per activity, written in that activity's commit, with the
command and its result — never the intention), **Problemas em aberto e riscos**. A01 commits the plan alone.

## 3. Worktree and branch

```bash
git fetch origin
git worktree add .claude/worktrees/<slug> -b <type>/issue-<n>-<slug> origin/main
```

Never commit on `main` (the ruleset rejects the push anyway). Commit identity, passed per command and never written
to the config — the same thing the `usage-monitor-commit-push` script does since #498:

```bash
git -c user.name=claude -c user.email=claude@anthropic.com commit -F <message>
```

Conventional Commits in English, trailers from the conversation's attribution reminder. One activity, one commit:
test, code, docs and the plan row together.

## 4. TDD — every activity that changes behavior

The implementing agent does this and returns the literal lines; Neferpitou rejects a delivery without them.

1. **Red.** Write the test for the behavior first: the contract (route, body, published state, text, decision), as
   the neighboring tests do. Run the narrowest command and confirm it fails **on the assertion, for the expected
   reason**. A compile error is not red: add the minimal stub so the test compiles and fails on what it asserts.
2. **Green.** Write the least production code that makes it pass. Run the same command.
3. **Refactor** with the test green; run it again.
4. **Record** in the activity's plan row: the agent returns the red command and the failure line (`expected …,
   actual …`), then the green command and its count. Neferpitou copies both into the row. A delivery without them is
   returned: a row without the red run is an activity that did not follow TDD.

A bug fix starts with a test that reproduces the bug (red), never with the fix. A test that only executes code without
asserting behavior does not count (`cobertura-95-execucao.md`, "Decisões").

Without a test harness (Actions YAML, `docs/`, design system, skill text), the row says so and names what validated
it (parse, a real run, real data). That is the only exception.

## 5. Local tests before the PR

`test-runner` runs these commands. The full suite is the CI's job: the PR runs it on every push and `ci-ok` blocks the
merge if it fails (decision of the owner, #619 — running it locally too doubled the wait). Locally run only the **slice
of what changed**, by test class:

| Changed | Command |
|---|---|
| `src/**` | `gradlew.bat desktopTest --tests "<classes of the changed files>" --tests "*ArchitectureRulesTest*"` |
| Gradle files, `commonMain` domain/data shared by many screens | `gradlew.bat allTests` (the slice cannot be named) |
| `server/**` | `cd server && npm test` (`npm run test:coverage` for coverage) |
| `tools/ci/**` | `node --test "tools/ci/test/*.test.mjs"` |

`ArchitectureRulesTest` always goes in the slice: it is the only check of file/function size and layering, and it is
cheap. The test report of the `usage-monitor-test-report` skill is produced by the CI's `test-report` job; run it
locally only when asked.

Diff coverage before opening the PR (advisory in CI, floor 90%), on the same slice:

```bash
gradlew.bat desktopTest --tests "<slice>" --tests "*ArchitectureRulesTest*" koverXmlReport -Pcoverage
node tools/ci/diff-coverage.mjs --base origin/main --kover build/reports/kover/report.xml
node tools/ci/diff-coverage.mjs --base origin/main --lcov server/coverage/lcov.info
```

Below 90%: write the missing tests (TDD) or justify each uncovered line in the plan row. A red CI caused by a test
outside the slice counts as an incident like any other (section 7).

## 6. PR with auto-merge

```bash
git push -u origin <branch>
gh pr create --title "<conventional title> (#<n>)" --body-file <scratchpad>/pr.md
gh pr merge --auto --merge <pr>
```

Body: `Closes #<n>`, what changed, **platforms tested** (`CLAUDE.md`, "CI e testes"; window host changes say the
#342 risk), test plan with the commands run, footer from the attribution reminder. The `main` ruleset requires
`ci-ok`; GitHub merges by itself when it passes and deletes the remote branch. Never `--admin`.

## 7. CI and the incident stop

Watch the `CI` run of the head commit, not `gh pr checks --watch`: right after a push the CI run sits queued behind
the `concurrency` cancel with no check registered yet, and `gh pr checks --watch` returns as soon as the checks it
sees (the skipped `Dependabot auto-merge` job) are done — measured on PR #497.

```bash
gh run list --branch <branch> --workflow ci.yml --limit 1 --json databaseId,headSha
gh run watch <run-id> --exit-status
gh run view <run-id> --log-failed        # on red
node tools/ci/ci-incidents.mjs            # count after every red run
node tools/ci/ci-incidents.mjs --local "<what failed>"   # local test failure after the PR is open
```

The red goes back to the implementing agent: it reproduces the failure with a test, then fixes it (TDD), and Neferpitou
commits and pushes. Exit code 3 from `ci-incidents.mjs` is the 4th incident: run
`gh pr merge --disable-auto <pr>`, stop touching the branch, and hand back to the user the diagnosis of each failure,
what was tried and the branch state.

## 8. After the merge

First take **every** session's working directory out of the worktree, each in its own tool: the PowerShell tool keeps
its directory between calls, and a process whose current directory is inside the folder makes the removal exit 255 with
`Permission denied`, after dropping the registration and the content, leaving the empty folder (#500, measured: PR #499
cleanup, and reproduced with `Start-Process pwsh -WorkingDirectory <wt>`). A `cd` inside the same Bash command does
not release the PowerShell session.

```powershell
Set-Location <repo root>          # PowerShell tool, in its own call
```

```bash
cd <repo root>                    # Bash tool, in its own call
gh pr view <pr> --json state,mergedAt,mergeCommit
git -c core.longpaths=true worktree remove .claude/worktrees/<slug>
git branch -D <branch>
git fetch --prune
git pull --ff-only                # local main, always (#509)
```

The local `main` is always brought up to the merge: without the pull it stays behind `origin/main` (11 commits after
PR #508, measured). `--ff-only` never creates a local merge; if it fails, report why instead of forcing.

`core.longpaths` is mandatory on Windows: `server/node_modules` (after `npm ci`) passes 260 characters, and without it
`git worktree remove` exits 255 with `Filename too long`, drops the registration and leaves the folder half deleted
(#498, measured). It goes per command, never into the user's config.

If the removal still fails and `git worktree list` no longer shows the worktree, run `git worktree prune`, list what is
left in the folder, and delete it only if it is empty or holds nothing but this branch's ignored files
(`node_modules`, `build`): `Remove-Item -LiteralPath '\\?\<absolute path>' -Recurse -Force`. Another process holding the
folder (editor, file explorer) gives the same `Permission denied`; close it first.

Then comment on the issue with the test cases created — **at most 20 lines**, first line
`🤖 Escrito por Claude Code, a pedido de @edilsonvilarinho`:

```bash
gh issue comment <n> --body-file <scratchpad>/tests.md
```

Content: one line per test file or group — what behavior each case asserts (not the method name alone), the red →
green evidence of the key cases, totals (tests added, suite count), diff coverage result, and what stayed without a
test and why. Close the issue if `Closes #<n>` did not.

Finally tell the user, within 15 lines: PR, merge commit, CI run, incidents, and the issue comment link.
