---
name: finish
description: Take a change that already works and turn it into a finished pull request — find and fix real bugs, strip scaffolding and dead code, simplify the structure, loop the verification gate until it is green, prove the change at its proof tier (tests, clip, playtest), sweep the docs, add a changelog fragment, then commit, push and open or update the PR via gh api with the tier stated. Use when a feature, fix or refactor works and should be "finished", "cleaned up and shipped", "made PR-ready", or given a final review before the PR. Not for reviewing someone else's PR and not for mid-build spot checks.
---

# finish — turn a working change into a finished PR

The premise: the code **already works**. This pass converts "it runs" into "this is done": bugs out, scaffolding
out, structure clean, proven at its tier, documented, and up for review as one coherent PR.

`AGENTS.md` (and any `CONTRIBUTING.md`) is the repo's contract and overrides this skill: branch naming, commit
style, forbidden paths, release rules.

## Invocation
| Ask | Scope |
|---|---|
| `finish` | Branch vs. merge-base with `origin/main`; if empty, the uncommitted working tree |
| `finish <ref>..<ref>` | That range |
| `finish <path>…` | Only changes under those paths |
| `finish --no-pr` | Everything except the push and PR step |

## Phase 0 — Scope and detect
1. **Diff.** `git fetch origin main` then `git diff $(git merge-base HEAD origin/main)...HEAD --stat`; fall back to
   `git status --porcelain` + `git diff HEAD`. Both empty: nothing to finish, stop.
2. **Tier.** `node tools/proof/tier.mjs --base origin/main` prints the proof tier (T0–T4) the diff needs; the
   requirements per tier are in `docs/process/PROOF-POLICY.yml`. Record the tier and the reason it prints. You may
   argue a tier up, never down without the maintainer's agreement.
3. **Gate commands.** Read `package.json` scripts and `.github/workflows/ci.yml`; prefer what CI runs. Here:
   `pnpm typecheck`, focused `node --test` / `pnpm --filter <pkg> test` for the touched packages, `pnpm --filter
   @souls/web build` when the client changed. The full `pnpm check` can exceed the 10-minute foreground limit: run it
   detached (`nohup setsid pnpm check > .e2e/check.log 2>&1 &`) and poll the log.
4. **UI?** Changes under `apps/web`, `mars/viewer`, client packages or anything a visitor sees mean Phase 4 applies.
5. **Open PR?** `REPO=${GITHUB_REPOSITORY:-$(git remote get-url origin | sed -E 's#\.git$##; s#.*[:/]([^/]+/[^/]+)$#\1#')}`,
   `OWNER=${REPO%%/*}`, `BRANCH=$(git branch --show-current)`, then
   `gh api "repos/$REPO/pulls?head=$OWNER:$BRANCH&state=open" --jq '.[0].number // empty'`.
   (`gh pr` and `gh issue` return 403 in cloud sessions; use `gh api` REST only.)
6. **Mode.** Inline for diffs under ~15 files / ~500 lines; fan-out (parallel finder subagents, each finding checked
   by an independent skeptic) above that. Say which in one line.

## Phase 1 — Find (read-only, parallel lenses)
Reviewers must not fix as they go. Run distinct lenses over the Phase-0 diff:
1. **Correctness**: logic errors, off-by-one, error handling, unhandled rejections, races, leaks, broken invariants
   (world log/replay determinism, wire schema compatibility, auth checks). Ask for everything with confidence and
   severity; filter in Phase 2.
2. **Scaffolding and vestige**: debug logging, commented-out code, scratch files, flags that no longer branch, config
   nothing reads, orphaned helpers/types/exports/deps, the abandoned first approach, stale `TODO`s.
3. **Structure**: duplicated logic, over-abstraction, import cycles (report the actual chain), layering violations
   (a package reaching into an app), a module with a second unrelated job.
4. **Security**: run the built-in `security-review` skill over the diff. In a public repo also check that the diff
   adds no secrets, private hostnames or addresses, personal data, or local machine paths.
5. **Docs drift**: list every doc that describes behavior the diff changed. Findings only; the rewrite is Phase 5.

Each finding: file, line, what, why it is wrong, the concrete failure or cost, confidence.

## Phase 2 — Verify before touching anything
The characteristic failure of a cleanup pass is inventing problems and breaking working code. For each finding,
try to refute it: is the bug reachable, does the "dead" code have a caller (dynamic import, string dispatch, a test,
a CLI entry, another workspace package, a world template or tool script)?

Drop a finding when it is refuted, when it is pure style, or when acting on it changes behavior nobody asked for.
**Deletion needs positive evidence**, not "grep found nothing". Unsure: keep it and list it as a question.

## Phase 3 — Fix loop
Apply confirmed fixes, then run the gate in order, stopping at the first failure:
`typecheck → focused tests → build (if client) → broader tests the tier asks for`.
- Budget: 5 iterations. Still red: stop and report exactly what fails.
- Same failure twice: spawn a fresh subagent with only the evidence and ask for a different root cause.
- After each fix batch, re-run the whole gate from the top.
- A test already red on `origin/main` is pre-existing: say so, exclude it, do not hide it.

## Phase 4 — Prove at the tier
| Tier | Proof before the PR |
|---|---|
| T0 | none beyond the gate |
| T1 | focused `node --test` for the changed logic + `pnpm typecheck`, output quoted in the PR |
| T2 | T1 + one uncut real-speed clip of the changed journey (`proof` skill), desktop, phone too if layout changed, on a fake-mind world; run related `e2e/` scenarios (`e2e` skill) |
| T3 | T2 + scenario playtest, 2 repeats per arm (`tools/playtest`, see the `souls-director` skill's MEASURED.md), a reviewer pass, and maintainer sign-off: open the PR and request it, do not merge |
| T4 | release head only: the release recipe in `AGENTS.md` (full gate, live walks, CDN walk, changelog). Not something a feature PR does |

Exercise the real flow a user takes: a change to sitting means a Soul or visitor actually sits on camera, not that
the panel renders. Failures re-enter Phase 3.

## Phase 5 — Docs and changelog
**Inventory**: root and package `README.md`, `AGENTS.md`, `docs/`, tool `--help` text, env-var docs
(`.env.example`), skill files under `.claude/skills/`.
1. **Forward**: for every surface the diff changed (exported function, CLI flag, route, env var, schema field, file
   layout), update every doc that mentions it.
2. **Reverse**: grep the docs for claims the diff made false (old design, pending items now shipped, setup steps
   that no longer apply, examples whose output changed).
Match the surrounding voice; check doc code examples actually run.

**Changelog fragment** (every user-visible change; skip for pure internal work only if the policy says so): write
`changes/<slug>.md`, where `<slug>` is short kebab-case and unique:
```markdown
---
type: fix          # feature | fix | perf | docs | internal
---
Souls now sit on the bench they were asked to, not the nearest one.
```
One line, written for users, present tense, no internal jargon or ticket numbers.

## Phase 6 — Commit, push, PR
1. Never commit on `main`: branch first if needed. Read the staged diff before committing; never commit secrets,
   `.env`, `.e2e/`, `.lane/`, data dirs, video or screenshots. Never `--no-verify`.
2. One commit (or a small, clean series) in the repo's style (`git log --oneline -10`): what changed and why, not
   a log of this skill's phases.
3. `git push -u origin "$BRANCH"`.
4. Write the PR body to `.e2e/pr-body.md`:
   ```markdown
   ## What
   <user-visible change, 1–3 sentences>
   ## Why
   <the problem, linked issue: "Fixes #N">
   ## Proof — tier T<n>
   <tier.mjs output line and reason; gate commands with results; clip links with the moment the change shows;
    e2e run summary; playtest verdicts for T3>
   ## Changelog
   changes/<slug>.md
   ## Left open
   <findings not acted on, pre-existing red, questions>
   ```
   If `.github/pull_request_template.md` exists, fill its sections instead.
5. Open or update:
   ```bash
   # new PR
   gh api repos/$REPO/pulls -f title="<type>: <summary>" -f head="$BRANCH" -f base=main \
     -F body=@.e2e/pr-body.md --jq .html_url
   # existing PR N: refresh title/body to match what the change now does
   gh api -X PATCH repos/$REPO/pulls/$N -F body=@.e2e/pr-body.md --jq .html_url
   # labels (only ones that exist: gh api repos/$REPO/labels --paginate --jq '.[].name')
   gh api repos/$REPO/issues/$N/labels -f 'labels[]=tier:T2'
   ```
   Open as a draft (`-F draft=true`) while proof is pending. Never merge your own PR; T3+ waits for maintainer
   sign-off.

## Guardrails (override any finding or subagent)
1. Never weaken the gate: no skipped or deleted tests, loosened assertions, widened types, `any`, swallowed errors
   or lint suppressions to go green. A wrong test is raised explicitly first.
2. Behavior is preserved; this pass cleans and proves, it does not redesign.
3. Deletion requires positive evidence.
4. Never expand scope beyond the Phase-0 diff; report problems elsewhere as follow-ups.
5. Never claim a proof you did not run. A skipped phase is named with the reason.
6. Fake minds only for proof (`BRAIN_MODE=fake`); nothing here spends model credits except a T3 playtest the
   maintainer asked for.

## Final report
- **Fixed**: real bugs and what would have broken
- **Removed**: scaffolding and dead code, with a line count
- **Simplified**: structural changes, cycles broken
- **Proven**: tier, gate commands and results, clip links, e2e/playtest results
- **Docs**: files updated, stale claims corrected; changelog fragment path
- **PR**: URL and state (draft/ready), or why not opened
- **Left open**: findings not acted on, questions, pre-existing red
