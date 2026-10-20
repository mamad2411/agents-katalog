---
name: pickup-issue
description: Start work on exactly one issue — read it whole, confirm the verification contract BEFORE writing code, branch, implement, test, verify, and open a PR that closes it with the observation pasted into the evidence section. The step /next hands you. Use when taking an issue off the board. Trigger words — pickup, pick up, pickup-issue, start work, take this issue, claim, work on #12, begin the issue.
---
# Pick up issue (one issue, start to PR)

**Use when:** `/next` handed you an issue, or you are taking one off the board. **Owners:** the issue's lead
`agent` field; `tech-lead-orchestrator` when unassigned.

## Inputs
The issue in full — acceptance criteria, the `REQ-###` it satisfies, security note, declared paths, `deps` —
plus `vantry.yml` and `scripts/verify.sh --status` for the branch you are about to leave.

## Procedure
0. **Is this issue in the ACTIVE sprint? If not, stop.**
   ```bash
   gh issue view <n> --json labels --jq '[.labels[].name] | map(select(startswith("sprint:")))'
   ```
   It must name the sprint marked **ACTIVE** in `docs/planning/sprint-plan.md`. An issue sitting in `Backlog`
   is work nobody has committed to this sprint, and taking it from backlog straight to in-progress and then
   done is how a sprint ends up containing things its goal never covered — `/sprint-review` then reports on a
   scope no one agreed, and the sprint's demo does not match its plan.

   **Moving it is a planning decision, not a step you take on the way past.** If it genuinely belongs in this
   sprint, say so and move it deliberately: set its `sprint` in `scripts/kanban/issues.csv`, re-run
   `bash scripts/kanban/import-kanban.sh --project <n>`, and note in `sprint-plan.md` that the sprint grew and
   why. If it does not belong, it waits for `/refine-backlog`.

   The one exception is a **P0 incident**, where the fix is the plan. Say that it is one, and record it in the
   sprint log so the retro sees what interrupted the sprint.

1. **Read the whole issue,** not the title: acceptance criteria, security note, the paths it declares it will
   touch, and its `deps`. If a dep is not done, stop and go back to `/next` — do not start blocked work.
2. **Confirm the verification contract BEFORE you write code.** Open `vantry.yml` and check `run.smoke` is a
   real command that exercises the software as a user does. If it is empty, define it now — `verify.sh` exits
   **2** on an empty smoke, and discovering that verification is undefined at PR time is far too late.
3. **Branch** `<type>/<ISSUE-ID>-<slug>` off `merge.base` (`feat/`, `fix/`, `chore/`, `docs/`, `test/`,
   `refactor/`). Set the issue **in-progress** on the board (`status:in-progress`) so nobody else takes it.
4. **Implement the smallest change that satisfies the acceptance criteria,** delegating to the surface's
   playbook — `api-endpoint`, `ui-component`, `safe-migration`, `webhook-handler`, `background-job`.
5. **Tests** per `write-tests` — failure modes, and allow+deny for anything touching authorization.
6. **Review gates.** If the issue carries a security note or touches `sensitive_paths`, run `security-review`
   and commit its verdict to `.vantry/reviews/<branch-slug>.security.json` — the judgement travels with the PR.
7. **Verify:** `scripts/verify.sh`, then `scripts/verify.sh --observe "<expected>" "<observed>"`.
8. **Promote the criterion — the step that outlives the issue.** Add one or two lines to `acceptance:` in
   `vantry.yml`, four fields on `" | "`:
   `"AC-7 | REQ-004 | a refund above the original amount is refused | <the command that proves it>"`.
   **Why here and not when the spec was written:** a criterion added at spec time is red until the work lands,
   so every board would start red and the team would learn to ignore the colour. Added on the way out it is
   green on arrival — and `verify.sh` then runs it as its own step `ac:AC-7` on **every** verification, forever.
   A regression on REQ-004 six months from now blocks the push of someone who has never heard of REQ-004.
   Rules: **never `npm test`** or any whole-suite command (`validate-config.sh` refuses a command that re-runs
   `run.test` or `run.smoke`); **at most two lines per issue**; each command proves **one named behaviour** and
   exits non-zero the moment that behaviour breaks. Then re-run `scripts/verify.sh` — the receipt must list your
   criterion with `"status":"pass"`.
9. **Open the PR** with `Closes #NN` and paste that observation into the **"## Verification evidence"** section
   of the template — CI fails a PR whose evidence block is empty. Name the criteria you promoted.

## Guardrails
- **One issue per branch.** Do not start a second issue while the first is awaiting merge — finish or hand off.
- Scope creep is a new issue, not a bigger diff; file it and keep moving.
- Do not merge your own PR when `merge.authority: human` — the bash guard denies `gh pr merge` and it is right.
- Never promote a criterion that is currently failing, and never promote one you cannot name a behaviour for —
  a permanently red `acceptance:` line teaches the whole team to bypass the gate.

## Joining a batch, when the project batches PRs
If `vantry.yml` sets `dispatch.batch_prs` above 1 and `/next` handed you several issues, they share **one
branch and one PR** — one commit per issue, each ending `Closes #<n>`.

What changes for you:
- **Commit per issue, and verify after each.** A batch that is verified only at the end cannot tell you which
  issue broke it.
- **The PR body carries one evidence block per issue** — expected/observed for each, not one summary for all.
  The evidence gate reads the block; a batch with one vague paragraph is a batch nobody reviewed.
- **Never pull a sensitive issue into a batch.** If your issue is `security: yes`, or its `paths` match a
  `sensitive_paths` glob, it leaves the batch and gets its own branch. The security verdict names a branch, and
  a verdict whose scope is four unrelated changes is not a verdict.
- **If one issue in the batch cannot be finished**, take it out — reset its commit onto its own branch — rather
  than holding the others hostage. The minutes you saved are not worth a stalled sprint.

## The CSV is not updated for you
Nothing in this kit writes `status` or `sprint` back into `scripts/kanban/issues.csv` — GitHub is the live
board, and the CSV is the seed that produced it. When you finish an issue, **edit its row yourself** (or accept
that the CSV is a historical record and read status from `gh`). `/standup` and `/next` read the board first and
fall back to the CSV, so a stale CSV misleads only when `gh` is unavailable — which is exactly when you are
least able to check. One line, at the end of the issue:

```bash
awk -F, -v id="$ID" 'BEGIN{OFS=","} $1==id {$9="done"} 1' scripts/kanban/issues.csv > /tmp/k && mv /tmp/k scripts/kanban/issues.csv
```

## Done when
- The issue was **in the ACTIVE sprint** when work started — or it was moved there deliberately, with
  `sprint-plan.md` updated to say the sprint grew and why.
The branch is named `<type>/<ISSUE-ID>-<slug>`; the issue is in-progress on the board; tests cover the failure
modes; `scripts/verify.sh` has written a **pass** receipt matching the current tree whose `acceptance` array
lists the criteria promoted from this issue with `"status":"pass"`; the PR is open with `Closes #NN` and a
non-empty "## Verification evidence" section.
