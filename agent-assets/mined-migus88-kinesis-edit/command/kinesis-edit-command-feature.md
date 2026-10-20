---
description: Drive a feature end-to-end from a GitHub issue ID or description — resolve the issue, branch an isolated git worktree off origin/main, research and clarify inside it, implement, open a PR
argument-hint: <issue-number | issue-url | feature description>
---

# /feature — issue to PR, end to end

Input: `$ARGUMENTS` — either a GitHub issue reference (`123`, `#123`, or an issue URL) or a free-text feature description. If empty, ask the user what to build before doing anything else.

## Operating principles

- **Worktree isolation.** All implementation happens in a dedicated git worktree under `.claude/worktrees/`, branched from `origin/main` (phase 3). The shared checkout is never switched or dirtied, so multiple `/feature` sessions can run concurrently.
- **Stay lean.** You are the orchestrator: hold decisions, plans, and diffs under review — not file contents. Delegate reading, exploring, and code-writing to subagents (Agent tool). Do not pull whole source files into your own context when a subagent summary will do.
- **But read the seams yourself.** Lean is not blind. Before fanning out, read the few files that define the contract the agents will share: the composition root they all merge into, the base type they derive from, the file whose conventions they must match. Skip it and each agent invents its own answer to the same question, with the integration pass paying for all of them.
- **Read by reading list, never end-to-end.** The two biggest module docs — `docs/app/design-system.md` and `docs/app/keyboard-editor.md`, ~1 200 dense lines each — are tens of thousands of tokens apiece, so a fan-out where every agent opens both spends more on paging docs than on writing the feature. Phase 4 therefore produces a reading list of **`path:startLine-endLine` ranges**, and every agent — implementers and reviewers alike — reads *those ranges*, via `Read`'s `offset`/`limit`. Reading either doc end to end is a defect, not diligence: CLAUDE.md's "read `design-system.md` before writing any view or style" means the sections that govern your view, and the reading list is what names them.
- **Contracts live in the repo, not in prompts.** When more than two agents work on one subsystem, have the first agent commit the shared convention as an artifact — a base type, a header comment, a doc section — and tell the rest to *read* it. Pasting a convention into N prompts guarantees drift: the copies go stale as the work teaches you things, and later agents get instructions the code has outgrown.
- **Name the traps, not the principle.** Agents working in parallel make the *same* mistake in parallel. A principle ("make state precedence explicit") produced an identical defect in four files at once; the enumerated list of qualifiers that actually recur would have prevented all four. Spell out the failure modes you know as a checklist — a principle is what you write when you don't yet know them.
- **Settle mechanically what a command can settle.** Findings — from a review agent, an implementer's self-check, or your own reading — fall in two classes. **Mechanical:** a `grep`, a build or one filtered test settles it outright ("names a token that isn't defined", "calls a method that doesn't exist"). **Judgment:** no command decides it ("breaks the design law that absent features aren't rendered", "leaves the profile half-saved"). Run the command for the first class; spend agents only on the second. This holds in **both modes** — it is what the standard path's review agent should do, and what gates the ultracode verifier fan-out in phase 6. The guard against dressing a judgment finding as a mechanical one: you must be able to state, *before* running the check, which output means confirmed and which means refuted; if you cannot, it is a judgment finding. A check that comes back **confirming** also skips the fan-out and goes straight to the fix list — a definitive answer needs no second opinion either.
- **One PR is one reviewable change.** Generation time scales with the size of the diff; *verification does not* — a build and a test run cost a fraction of writing the code. A feature that runs for hours is almost always one scoped too large, not one checked too thoroughly; the longest here landed a hundred-plus files at once. Size is the decision with the hours riding on it, and phase 4 is where it gets made, before any code exists.
- **Docs before source.** This repo is documented agent-first: subagents read `docs/app/` (and `specs/` for domain questions) before opening source files — through the reading list, per above.
- **Documentation is part of the feature, not an afterthought.** Per CLAUDE.md, every change ships with its documentation: the module's agent-first doc in `docs/app/` (create it if the module is new), CLAUDE.md (new modules, changed commands), README.md when user-facing behavior changes. A feature without its doc updates is incomplete and must not reach the PR phase.
- **Unit tests are part of the feature, not an afterthought.** Per CLAUDE.md's testing rules, every change ships with unit tests for the behavior it adds and maintains the tests of the code it touches. The full suite must pass before the PR phase.
- **Ultracode.** If a system-reminder says ultracode is enabled for this session, orchestrate research and implementation with the Workflow tool as described in phase 6. Otherwise use individual subagents and skip the heavy machinery.

## Phase 1 — Sync

`git fetch --prune origin`. Do **not** check out or pull `main`, and do not require a clean shared checkout — the shared checkout is never touched; the feature branches from `origin/main` inside its own worktree in phase 3. Independent of phase 2: issue both in one batch.

## Phase 2 — Resolve the input, and get an issue number

You need an issue number `N` before phase 3, because the branch and worktree are named for it.

- Issue reference → `gh issue view <n> --json number,title,body,labels`. Its content is the starting spec. Add `,comments` only when resuming a prior run on this issue — phase 5 posts full specs as comments, so a re-fetch otherwise drags every earlier spec back into context. If the lookup fails, tell the user and ask whether the input was meant as a description instead.
- Free text → **create the issue now**, with the user's description as the body and a title you propose: `gh issue create --title "…" --body "…"`. Capture the new number. The refined spec is posted as a comment in phase 5, exactly as for an issue that already existed — creating it early costs nothing and is what lets research run against a current tree.

## Phase 3 — Worktree

Before research, not after. The shared checkout is **routinely several merges behind** `origin/main`, and research against a stale tree is worse than none: subagents cannot tell a stale tree from a current one, so they report confidently either way and the errors surface only at integration. Two research passes have already been thrown away to this, having proposed rebuilding things that already existed on `main`.

1. Determine the primary checkout's root: the first `worktree` line of `git worktree list --porcelain`. Do not use `--show-toplevel` — the session may already be inside another worktree.
2. Create the worktree and its branch from `origin/main`:
   `git worktree add "<root>/.claude/worktrees/feature-N-short-slug" -b feature/N-short-slug origin/main`
   If the branch or worktree already exists (a previous run for the same issue), don't fight it: ask the user whether to resume in the existing worktree as-is or delete and recreate it.
3. Switch the session into it: EnterWorktree with `path: "<root>/.claude/worktrees/feature-N-short-slug"`. Every subsequent phase — researching, implementing, testing, committing, pushing — runs inside the worktree.

## Phase 4 — Research and clarify

Runs **inside the worktree from phase 3**, so every agent reads the tree the feature will actually be built on. Re-fetch before each new wave of agents; the repo can move under you mid-feature.

1. Delegate codebase research to an Explore agent: which modules/files the feature touches, existing patterns to follow, relevant constraints from `specs/`. Point it at `docs/app/README.md` first — it routes a question to the right module doc, which is cheaper than searching for it. You receive a summary, not file dumps. Tell agents to locate code by **symbol name, not line number**.
2. Have that agent finish with the **reading list** the previous principle describes: for each implementer, the `docs/app/` and `specs/` ranges it actually needs, as `path:startLine-endLine` (it has `grep -n '^#'` for free — headings alone are not enough, because an agent handed a heading opens the file to find it). The research agent pays the paging cost once and hands down pointers.
3. Ask the user clarifying questions with AskUserQuestion — one batched call, max 4 questions, and only questions whose answers change the implementation (scope, behavior, UX trade-offs). Skip entirely if the issue is unambiguous.
4. Write a short spec: problem, approach, acceptance criteria, affected modules, required unit tests (what new behavior gets tested, which existing tests need updating), **the screens whose rendered frames phase 7 will check** — name them now, or the visual gate arrives with nothing planned for it — and required doc updates. Per CLAUDE.md's documentation rules that is the **module's own `docs/app/` doc**; a new module also needs its row in `docs/app/README.md`. CLAUDE.md and README are touched only for genuinely repo-wide changes, never to describe what the feature does.
5. **Write the spec and the reading list to a file; give agents the path, not the text.** Pasting them into N prompts and re-pasting on every fix round costs more each round than the file did once, and the copies drift as the work teaches you things. Put it **outside the worktree** (the session scratchpad is the obvious home): phase 6 runs `git add -A`, which would otherwise stage your working notes into the feature's diff. The durable copy is the phase-5 issue comment.
6. **Size the spec before committing to it.** Estimate the files it implies. Past the point where one reviewer could hold the whole change in their head — a couple of dozen files is a fair rule of thumb — stop and put a split to the user: independently shippable issues in dependency order, with your recommendation for what lands first. Here it costs one message; at phase 7 the diff is already too big to review and every remaining option is bad.

## Phase 5 — Record the spec on the issue

Post the refined spec as a comment on issue `N` (`gh issue comment <n> --body …`) — for an issue that already existed and for one you created in phase 2 alike. Use `gh issue edit` only if the body is empty or wrong (typically the stub you just wrote).

If phase 4 ended in a split, this is where the follow-up issues get created, and the worktree from phase 3 continues with whichever piece lands first.

## Phase 6 — Implement

**Standard mode:** delegate to one or more general-purpose agents. Give each the **path** to the phase-4 spec file and its own reading-list ranges. Their instructions must include: follow `docs/guides/Coding Conventions.md`, keep classes small (SOLID), write unit tests for everything they implement and maintain the existing tests they touch, and update `docs/app/`, CLAUDE.md, and README as part of the change.

**Review by stat, not by bulk.** `git add -A` first so newly created files count, then read `git diff HEAD --stat`. That, plus each agent's acceptance-criteria self-check below, tells you where to look; pull a file's full text only when the stat, a self-check or a review agent gives you a reason to. Reading a feature-sized diff in full spends the orchestrator's context on what it least needs verbatim, surfaces nothing a review agent reading the same diff would miss, and makes you pay again on every iteration. This does not contradict *read the seams*: that is a handful of dense files chosen deliberately before the work starts; this is bulk arriving after it.

**Fanning out.** Give each agent **strict file ownership** and keep the shared merge points (the composition root, the file every bridge lands in) for yourself — agents that cannot collide need no sequencing. Prefer: one agent establishes the contract and the exemplar, the rest run concurrently against it, then one integration agent owns every cross-cutting edit. Tell each that a build error in a file it does not own belongs to a sibling and must be reported, not fixed.

**Every implementation agent self-checks against the acceptance criteria.** Its report must state, per criterion, whether it is covered, deliberately absent, or not done — not a bare claim of completion. A later review agent then *verifies* that self-check, settling mechanically whatever a command settles. If a review pass is the first place a defect appears, the criteria never reached the agent that could have honoured them cheaply, and you have bought an extra round.

**And it verifies before it reports — scaled to what it touched.** Phase 7 is not where a compile error should first surface; that costs a round-trip to a fresh agent which must rebuild the context the last one had. But "run the suite" is two very different instructions here (measured 2026-08, Apple silicon):

| project | tests | duration |
|---|---|---|
| `KinesisEdit.Core.Tests` | 3 491 | **0.7 s** |
| `KinesisEdit.Tests` (headless Skia, one UI thread) | 3 715 | **3 m 7 s** |

So: an agent working only in `KinesisEdit.Core` runs `dotnet test src/KinesisEdit.Core.Tests` at every checkpoint — at under a second there is never a reason to skip or defer it. An agent that touched the app layer runs `dotnet build src/KinesisEdit.sln` for the compile answer and, while iterating, only its own area (`dotnet test src/KinesisEdit.Tests --filter FullyQualifiedName~<area> --no-build` — measured at ~20 s for a typical area, against 3 m 7 s unfiltered). **The unfiltered app suite is not an agent's job**: it runs once, in phase 7, after the last edit. N concurrent agents each running it in the same worktree pay three minutes apiece *and* contend for the same `obj/bin`. Either way the agent reports having built — one that reports without building has reported nothing you can act on.

**Ultracode mode:** orchestrate with the Workflow tool:

1. **Design** — only if the solution space is genuinely wide: 2–3 independent design attempts from different angles, a judge scores them, synthesize from the winner.
2. **Implement** — one agent per independent module; use worktree isolation only if agents would edit the same files concurrently.
3. **Adversarial review** — finder agents sweep the diff along separate dimensions (correctness vs. the spec, edge cases, conventions/doc compliance). Each finding carries the check that would settle it, per *settle mechanically* above: findings a command decides are decided by running it, and **only judgment findings reach the refuting verifiers** — the convention/doc dimension is nearly all mechanical, and it is the dimension a large diff generates the most hits on. Only confirmed findings get fixed. **Cap it at two rounds.** Loop-until-dry over a feature-sized diff can cost more than the implementation did, and by round three the yield is mostly restatement. If a third round still looks warranted, the real problem is upstream — the spec under-specified something (see *Name the traps*) — so say that to the user instead of buying another sweep.

## Phase 7 — Verify

**Cheapest gate first.** Gates 2 and 3 are a `grep` and a `--stat`; gates 5 and 6 are minutes. A missing doc found after the suite ran wastes the run, because the fix invalidates it.

1. **Re-sync gate.** `git fetch origin`, then merge `origin/main` into the branch. A feature that ran for several rounds has probably been overtaken by a merge; resolving that now is far cheaper than after the PR is open. **A textually clean auto-merge is not a correct one** — git merges by region, not by meaning — so inspect the files both sides touched.
2. **Documentation gate.** Confirm the diff includes the doc updates identified in phase 4 — the `docs/app/` doc of every touched module, a new row in `docs/app/README.md` for a new one. Check the reverse too: a feature's behavior is described in its module's doc and **nowhere else**, so a diff that adds a sentence about this feature to CLAUDE.md or README.md is wrong and that sentence belongs in `docs/app/` instead.
3. **Test-coverage gate.** Confirm the diff includes the unit tests identified in phase 4: new tests for the behavior added, updates to the existing tests of any code touched. (Vacuous when gate 4 finds no compiled change — a change with no behavior owes no tests.)
4. **Blast-radius check — decide what a run can tell you, before starting one.** `origin/main` is the tree this branch was cut from and is taken as green, so a run is informative only where the compiled tree now differs from it:

   ```sh
   git diff origin/main --stat -- src/ global.json .editorconfig
   ```

   - **Empty** → the branch is docs-only (or command-only): the source the tests compile is byte-identical to a tree already known green, so the suite cannot distinguish this branch from `main` and there is nothing for it to catch. Say so in the PR body — *"no compiled file changed; source is identical to `origin/main`"* — and skip gates 5 and 6.
   - **Only `src/KinesisEdit.Core*`** → `dotnet test src/KinesisEdit.Core.Tests` (0.7 s) **is** gate 6 in full; nothing there renders, so gate 5 does not apply.
   - **Anything in the app layer** → gates 5 and 6 over the whole solution.

   **The trap is reasoning about the diff instead of running that command.** A merge from `origin/main` really does add source and tests to the branch — but they arrive *from* the tree already taken as green, so they add nothing to verify. "The merge pulled in a thousand lines of new source" is a true sentence and the wrong conclusion. The same question applies again after every fix round: a fix confined to Core does not re-earn the three-minute app suite.

5. **Visual gate (any change that alters what a screen looks like)** — before the suite, because a wrong frame means a fix and a fix invalidates the run. Per CLAUDE.md's testing rules, a green suite is not evidence the screen is right. Build once (`dotnet build src/KinesisEdit.sln`), then capture the screens named in the phase-4 spec, offscreen, in both theme variants, and look at the frames yourself — not the control in isolation, which is what the agent already asserted about. **One process for all of them**; booting per frame pays the startup again each time. **Do not re-derive the harness** — `Design/ViewSceneFactory.cs` already builds any view over a realistic view model and `Headless/ThemedHost.cs` shows it under a chosen variant and captures the frame. The throwaway part is only the few lines that pick the scenes, wait out the fade-in in *real* time and write the PNGs; read `docs/app/design-system.md` § *Rendered-frame capture* first, which owns the timing details and both traps that cost real time to rediscover. Delete that driver before committing.
6. **Unit-test gate (hard requirement).** With the build from gate 5 already done: `dotnet test src/KinesisEdit.sln --no-build`. Every test must pass before a PR is created — fix failures and rerun until green. Never open a PR with a failing suite; if a failure genuinely cannot be resolved, stop and report it to the user instead of proceeding.

## Phase 8 — Pull request

1. Delete the throwaway capture driver if one is still on disk, commit with a clear imperative message, and push: `git push -u origin HEAD`.
2. `gh pr create --title "…" --body "…"` (always pass the flags — the bare command drops into interactive mode). Body contains: what/why summary, notable decisions, test evidence, **any deliberate deviation from `docs/design/` with its reason, any behaviour that visibly changed, and what remains open**, and `Closes #N`. A reviewer should not have to discover a deviation by reading the diff.

Finish by reporting to the user: the issue link, the PR link, the worktree path, and a 3–5 sentence summary of what was built and any open questions. Remind the user that the worktree stays until the PR is merged: they can tell you when it merges and you'll remove it (phase 9), or run `/clean-worktree` periodically to sweep up merged worktrees.

## Phase 9 — Post-merge cleanup (deferred)

The worktree outlives the PR creation. When the user reports the merge — possibly much later in the session:

1. Verify: `gh pr view feature/N-short-slug --json state` — proceed only if the state is `MERGED`; otherwise report the actual state and stop.
2. Leave the worktree first (a worktree cannot be removed while the session is inside it): ExitWorktree with `action: "keep"`.
3. `git worktree remove <path>` — if removal is blocked only by disposable untracked files (build output and the like), retry with `--force`.
4. `git branch -D feature/N-short-slug` (`-D` because squash/rebase merges are not ancestors of `main`; the merge was already verified in step 1), then `git fetch --prune`.

If the session ends before the merge, that's fine — `/clean-worktree` removes merged worktrees on its next run.
