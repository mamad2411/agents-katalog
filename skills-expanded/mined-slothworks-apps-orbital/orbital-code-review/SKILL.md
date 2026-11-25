---
name: orbital-code-review
description: Review a change in the Orbital repo — the local branch against main, or a GitHub PR by number or URL — by fanning it out to focused review agents (feature, reuse, security, phone, sessions, robustness, ui, performance, ship), then verifying and merging what they find; the feature review is posted to the PR.
argument-hint: "[pr-number-or-url]"
---

# Orbital review

One procedure for two inputs: with no argument it reviews the current
branch against `main`; with a PR number or URL it reviews that PR. The
agents are the same either way; only where the diff and the intent come
from differs.

The agents check what CI does not: the rules that live in the `CLAUDE.md`
files, the ADRs under `docs/decisions` and `docs/why-orbital.md`. Do not
ask them to repeat what CI already enforces (typecheck, lint, tests,
`check-versions.mjs`, gitleaks, attribution).

## 1. Scope

| | Local branch | Pull request |
|---|---|---|
| Files | `git diff --name-only main...HEAD` | `gh pr diff <n> --name-only` |
| Diff | `git diff main...HEAD` | `gh pr diff <n>` |
| Intent | `git log main..HEAD`, the spec or plan it names | `gh pr view <n> --json title,body,labels` |

Include uncommitted changes in a local review (`git diff HEAD` on top) and
say so in the report. Note which workspaces the change reaches.

## 2. Understand the change

Read the diff and the intent and write one paragraph: what the change does,
for whom, and why. Every agent gets this paragraph, so none of them has to
guess what the change is for. If the intent cannot be found, say so in the
paragraph rather than inventing one.

## 3. Pick the agents

| Agent | Spawn when |
|---|---|
| `review-feature` | the change adds or alters a feature the user sees; not for a fix or a refactor |
| `review-reuse` | always, unless the change only deletes or moves code |
| `review-phone` | the change adds or alters a feature, a route, a WS message, or anything in `shared/` |
| `review-ship` | always |
| `review-security` | `server/` (`api/`, `remote/`, `files/`, `auth/`, `runner/`, `terminal/`, `git/`, `mcp/`, `media/`, `images/`), `relay/`, `shared/src/remote`, `desktop/`, `web/src/mobile` |
| `review-sessions` | `server/src/` `transcript/`, `watcher/`, `indexer/`, `runner/`, `harness/`, `rewind/`, `claudeDirs/`, `limits/`, `models/`, `media/`, `walkthrough/` — any server code that reads a transcript — or the message types they feed to `web/` |
| `review-robustness` | non-trivial logic in `server/`, `relay/`, `desktop/`, or stateful code in `web/` (stores, socket, transport); any migration under `server/drizzle` or the relay store |
| `review-ui` | `web/src` (including `web/src/mobile`), `site/` |
| `review-performance` | `web/src/map/`, `web/src/store/`, transcript rendering, `server/src/` `watcher/`, `indexer/`, `transcript/`, `api/hub.ts`, `files/`, `media/`, `walkthrough/` |

A change that touches only `docs/` gets `review-ship` alone.

## 4. Run them in parallel

Spawn every picked agent in one message. Each gets:

- the intent paragraph,
- the changed file list,
- the diff (or, for a large one, the command to produce it),
- whether this is a local or a PR review (and the PR number),
- for a PR, the path of a worktree checked out at its head
  (`git fetch origin <branch>` and `git worktree add --detach .claude/worktrees/pr<n>-review origin/<branch>`),
  so the agent reads the code as the PR has it; remove it after the review,
- this rule: report what the change introduces. A problem that was already
  there is reported only if the change makes it worse, the finding says it
  was there before, and its severity follows what the change added.

Each agent returns findings in this shape, and nothing else:

```
- file: <path>:<line>
  claim: <one sentence: what is wrong>
  scenario: <concrete inputs or state → the wrong result>
  severity: must-fix | should-fix | recommendation
```

`review-ship` returns a checklist instead (see its definition).
`review-feature` returns a `verdict:` line before its findings; give it the
PR description and the feature's spec as well.
`review-phone` also returns its OTA-or-native verdict; pass it to
`review-ship` only if `review-ship` has not run yet — otherwise reconcile
the two yourself in step 5.

## 5. Verify

Agents over-report. Before anything reaches the user, check each finding
in the code yourself:

- open the cited line and confirm the claim;
- confirm the scenario can actually happen (who calls this, with what);
- merge duplicates found by several agents;
- lower the severity of a finding about something the change did not
  introduce, if the agent did not already;
- drop a finding with no concrete scenario, or one that contradicts an
  ADR in force, unless the change itself contradicts that ADR.

`review-ui` lists design values with no canvas source rather than judging
them. Subagents cannot reach the design canvas; if the list is not empty,
compare those values against Claude Design through `DesignSync` yourself,
or name them in the report as unchecked.

## 6. Report

In the language of the conversation. Number findings across the groups so
they can be referred to.

```markdown
## Review: <PR #n — title | branch vs main — short description>

<the intent paragraph>

**Feature:** <review-feature's verdict, if it ran>

### Must fix
1. **path:line** — claim. Scenario.

### Should fix
2. …

### Recommendations
3. …

### Ready to ship
- [ ] versions: <app → proposed bump, reason>
- [ ] changelog: …
- [ ] documents: …
- [ ] tests: …
- [ ] PR: …

Agents run: <list>; findings dropped in verification: <count>.
```

Leave out an empty group. The proposed bumps are proposals: the decision
goes through AskUserQuestion, as the root `CLAUDE.md` → Versions says.

## 7. Post the feature review

When `review-feature` ran and the change has a PR — the one under review,
or an open PR for the local branch (`gh pr view --json number,url`) — post
its verified result to that PR as one comment:

```markdown
## ORBITAL FEATURE REVIEW

**Verdict:** <fits | fits in Labs | questionable — why>

<its verified findings, numbered, plain words; or "No findings.">

<sub>Reviewed at <short SHA of the PR head>. Updated on every run of `/orbital-code-review`.</sub>
```

Keep one such comment per PR. Find an earlier one by its heading
(`gh api repos/{owner}/{repo}/issues/<n>/comments`, a body starting with
`## ORBITAL FEATURE REVIEW`) and edit it
(`gh api -X PATCH repos/{owner}/{repo}/issues/comments/<id> -f body=…`);
post a new one (`gh pr comment <n> --body …`) only when there is none.
Without a PR, say in the report that the feature review will be posted
once the PR is open and the review runs on it.

Nothing else is posted to the PR, and nothing is fixed unless the user
asks.
