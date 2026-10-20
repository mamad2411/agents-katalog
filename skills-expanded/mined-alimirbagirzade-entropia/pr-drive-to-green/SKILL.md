---
name: pr-drive-to-green
description: Drive an Entropia pull request from red CI to merged without the maintainer babysitting it. Use this whenever you have opened a PR, pushed to one, subscribed to one, or been woken by a CI-failure or review event on this repo — and whenever the user says anything like "otomatik fix", "kendi düzeltsin", "yeşile getir", "merge et", "babysit the PR", "drive it to green", or asks why a PR is stuck. Encodes which failures may be auto-fixed, which must never be touched (ratchets and baselines), how to bring main in (rebase, never the Update-branch button), and when to stop and hand back to a human.
---

# Drive a PR to green — and know what you are forbidden to touch

The maintainer's ask is: "I give a prompt, code gets written, and if it breaks it fixes
itself and merges." That is achievable, but only because this repo's gates are honest. The
moment a fixer starts editing the files that *record* what is allowed, every gate becomes a
rubber stamp and the automation is worse than doing nothing.

So the whole skill reduces to one judgement, applied per failure:

> **Is this a broken *thing*, or a gate reporting that a decision was made?**
> Fix the first. Never edit the second — report it.

## Reuse what already exists

This repo already ships the diagnosis and fix machinery; do not reinvent it.

- **`entropia-triage`** — read-only diagnosis. Turns a symptom into a scope (files +
  symbols) and names the adjudicated invariants at risk. Writes nothing.
- **`entropia-scoped-fix`** — applies one bounded change under the layer pattern, with its
  test. Refuses to widen its own scope.
- **`/entropia-maintenance:merge-check <PR>`** — the five pre-merge gates CI does not cover
  (docs record deletion, base freshness, generated-file drift, the 0-job fake-green trap,
  and evidence for any "landed/closed" claim).

These live in `plugins/entropia-maintenance/` and load **only when the plugin is
installed**. Check your own tool inventory rather than assuming: if `entropia-triage` is not
in your agent list, the plugin is not loaded in this session — which is the normal state for
remote containers, where installation needs an approval prompt nobody can answer. When it is
absent, do the same work inline and follow the same order; the sequence matters more than
the packaging.

## The cost model you are optimising against

`Backend — lint, type, test` takes **~48 minutes** (measured; it has run as long as 85). The
ruleset on `main` (`20765617`) requires **16 checks** and `strict: true`, so the branch must
also be current with main at merge time. Every push restarts that clock.

The practical consequence: **guessing is extremely expensive.** One wrong push costs an
hour. Reproduce locally before pushing whenever the failure is reproducible locally — that
is minutes instead of an hour, and it is the difference between this loop being useful and
being a slow random walk.

## Loop

1. **Read the actual failing job log.** Not the check name, not the summary — the log. A
   check called `Backend — lint, type, test` fails for lint, type *and* test reasons, and
   those need different responses.
2. **Classify the failure** (three tiers below).
3. **Tier 1, or a Tier 2 you have proven** → fix, verify locally, push. **Tier 3** → stop,
   report, do not push.
4. **After pushing**, expect a fresh ~48-minute cycle. Do not poll with `sleep`; PR events
   wake you. Arm a fallback check-in (`send_later`, ~60 min) anyway, because CI *success*
   and merge-conflict transitions are not reliably delivered by webhook.
5. **When green**: confirm the PR is not a draft and auto-merge is armed. It lands itself.
6. **Stop** when the PR is merged or closed. Not before.

## Tier 1 — mechanical, fix without asking

These are *derived* artefacts. A human hand-writing them is the bug; regenerating is the
intended workflow.

| Failure | Fix |
|---|---|
| `generate_repository_facts.py --check` fails — artefacts stale | Run it **without** `--check` (`cd backend && uv run python ../scripts/generate_repository_facts.py --root ..`) and commit the result. Adding tests changes collection counts, so a test-adding PR legitimately needs this. |
| `openapi_export --check` fails | Run the generator; never hand-edit `docs/openapi.json`. |
| New `docs/audit/*.md` or `docs/implementation/*.md` without its `doc-status` banner | Insert the exact 5-line `historical` banner as the first lines. Every file under those globs is `historical`; only the newest kickoff is `current`. |
| A newer `docs/ADIM<n>…KICKOFF.md` exists while an older one is still `current` | Promote the highest-numbered, demote the rest. The rule is deterministic. |
| `ruff format --check` fails | `uv run ruff format .` |
| Branch behind main / `mergeable_state: behind` | **Rebase** — see below. |
| PR is still a draft but the intent was to merge | Undraft, then arm auto-merge (that order). |

## Tier 2 — a real defect in code this session wrote

Fix it if — and only if — you can state the failure in one sentence and the fix is small and
provably right: a type error, a wrong import, an off-by-one, a test asserting the old shape
after you deliberately changed that shape.

Two things separate a fix from a cover-up:

- **Reproduce locally first.** `cd backend && uv run pytest <file>::<test> -q --no-cov` — the
  `--no-cov` matters, because a single-file run measures ~4% of the package and the
  `--cov-fail-under=90` gate then reports a false red. Never pipe pytest to `tail`; the exit
  code becomes `tail`'s. Write output to a file and read `$?` separately.
- **Ask what the test was defending.** If it fails because the behaviour genuinely changed
  and that change *is* the point of the PR, re-align the test to the new behaviour and say
  so in the commit message. If the behaviour changed and that was **not** the point of the
  PR, you have found a regression — fix the code, not the test.

When you cannot tell which of those two it is, treat it as Tier 3 and say so.

## Tier 3 — never auto-fix; stop and report

These files and numbers *are* decisions. Editing them to go green converts a finding into a
silence that nobody will ever see again.

**Ratchet and baseline files:**

- `backend/tests/unit/engine_golden_digests.json` — 50 scenarios. A moved digest means the
  engine **re-priced** something. That is precisely the class of defect #550/#551/#552 were;
  refreshing it to get green ships a financial change nobody reviewed.
- `docs/audit/acceptance_coverage_baseline.json` — raising a ceiling "closes" debt by
  redefining it. The point of the ratchet is that it only moves down.
- `docs/performance/baseline_ci.json`, `docs/performance/query_budgets.json` — widening a
  band silences a returning N+1.
- `frontend/e2e/a11y-baseline.json`, `frontend/e2e/lighthouse-baseline.json`,
  `frontend/e2e/screenshots/baseline/` — the standing rule is *don't update the baseline,
  narrow the selector*.
- Coverage floors: `--cov-fail-under=90` in `backend/pyproject.toml`, the thresholds in
  `frontend/vite.config.ts`. Lower the number and the gate stops meaning anything.

> **Do not pattern-match on the word "baseline".** `domain/create_package/baseline.py`,
> `domain/capability/baseline.py` and `domain/manual/baseline.py` are ordinary production
> source and are perfectly normal to edit. The forbidden set is the list above, not a glob.

**Also Tier 3, for the same reason:**

- A `strict=True` xfail that starts passing (`XPASS`). That is the product changing. Remove
  the decorator only in the commit that intentionally fixed what it tracked.
- Any product decision — the STOP-GATEs in
  `docs/implementation/closure_design_financial_research_2026-08-13.md`, the unsigned entries
  in `docs/decisions/`. No amount of CI pressure turns an unsigned decision into a signed one.
- A failure that reproduces on `main` too. Say so once in the thread — "red on `<check>`,
  also failing on the base branch, will re-run when it recovers" — and act on the recovery
  notice. That is the one legitimate "not mine", and it is still not silent.

## Bringing main in

Rebase, then `git push --force-with-lease`. Do **not** use the server-side "Update branch"
button, and do not merge main into the branch:

- On a docs PR, a server-side merge once **silently dropped a `PROJECT_HISTORY.md` record**
  and **no CI gate caught it** — nothing in CI reads `docs/`.
- A heading rename inside a merge looks like record deletion to `docs-history-guard`.

If the rebase conflicts, **stop**. Resolving a conflict decides whose intent wins; that is a
human's call, not a fixer's. Report which hunks conflicted.

After any rebase that touches `docs/`, re-run the documentation-truth gate before pushing —
main may have moved the `current`/`historical` classification underneath you:

```
cd backend && uv run python ../scripts/generate_repository_facts.py --root .. --check
```

Push only on `exit 0` **and** the literal `documentation-truth gate OK` line.

## Merging

Prefer **auto-merge** over waiting and merging by hand: 48 minutes plus a `strict` ruleset
means a hand-merge window is usually stale by the time you reach it.

- Auto-merge does **not** survive a draft conversion. Undraft first, arm it second, then
  verify the ordering rather than assuming it.
- Direct self-merge through the CLI is blocked by a guard hook by design. That is not an
  obstacle to route around — auto-merge is the sanctioned path, and `merge-check` is the
  five-gate review that CI does not perform.

> **Guard-hook trap worth knowing:** `guard-git.sh` matches patterns against the *entire*
> Bash command string, fail-closed. A heredoc that merely quotes a blocked phrase is blocked
> too. When you need to write such text into a file, use the Write tool instead of a shell
> heredoc.

## Loop guard, and when to hand back

Push at most **two** corrective rounds for the same failing check. If a third round would be
for that same check, the diagnosis is wrong rather than the fix — stop and report what you
tried and what the log actually says.

Hand back when: the failure is Tier 3; a rebase conflicts; the same check fails three times;
the fix needs a product decision; or the PR needs an approval you cannot give.

## Reporting

Do not narrate each round. Report when a round **resolves** the failure, hits a real
blocker, or raises a question. Two things are always safe to skip silently: an event echoing
your own comment, and a duplicate of one you already handled.

State outcomes as measurements, never predictions — "22 checks, 0 failures, `Backend` 48 min"
rather than "CI should pass". If you did not run something, say you did not run it.
