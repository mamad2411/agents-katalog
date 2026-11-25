# Per-PR agent prompt

Every PR agent gets this same prompt with `<REPO>`, `<PR>`, and `<OUTDIR>` filled in. Do not paraphrase it per PR — labels from divergent prompts cannot be summed into one table.

The refute pass at the bottom is a second, separate agent on the same PR.

---

## Pass 1 — judge

You are auditing one pull request to measure how well several AI code reviewers performed on it. You are not reviewing the PR for its author, and you have no stake in any reviewer looking good.

**Repo:** `<REPO>`  **PR:** `<PR>`  **Write your result to:** `<OUTDIR>/<PR>.json`

### Step 1 — cold review, before you look at any reviewer's output

Do this first. If you read the bots first you will anchor on their framing and stop finding what all of them missed, which is the most valuable thing this audit produces.

```bash
gh pr diff <PR> --repo <REPO>
gh api repos/<REPO>/pulls/<PR>/files --paginate
```

Check out the repo at the reviewed commit if you need to read surrounding code or run anything. Read the call sites, not just the diff.

Record every defect you find. A defect is a **reachable wrong output or a violated contract that this PR introduces**: an input and a resulting behavior you can state concretely. Not a style preference, not a missing test with no current wrong output, not a pre-existing issue the PR merely touches.

Rate each on:

- `severity`: `blocking` (data loss, money movement, auth bypass, outage, security exposure) · `major` (wrong output on a real path) · `minor` (degraded but usable) · `nit` (style, naming, polish)
- `class`: `correctness` · `race` · `authz` · `data-money` · `perf` · `error-handling` · `api-contract` · `tests` · `style` · `other`

### Step 2 — now read the reviewers

```bash
node <SKILL_DIR>/scripts/fetch-pr-reviews.mjs --repo <REPO> --pr <PR> \
  --only "<REVIEWER_LIST>" --out /tmp/rv/raw/<PR>.json
```

The `reviewedCommit` on each finding is the commit that reviewer actually saw. **Judge every finding against that commit, never against the current head.** GitHub re-anchors comment lines as a PR evolves, so a comment can appear to point at code the reviewer never read, and a bug that was real at PR-open is often already fixed by the time a later reviewer runs.

**Enumerate summary-comment findings individually.** Several reviewers publish most of their findings in one long summary comment rather than as inline comments, and some publish the same finding in both places. Every distinct claim in a summary body is its own finding instance and must appear in `instances`, exactly as an inline comment would — labelled, severity-rated, and mapped to a defect. Recording one reviewer's inline comments while collapsing another's summary into a single entry is the single largest scoring error available in this pass: it inflates the inline-commenting reviewer's unique catches and deletes the other's yield and its false-positive denominator at the same time. When a summary restates an inline comment, keep the inline instance and mark the summary one `duplicateOf` it — do not drop it.

**A reviewer reacting to another reviewer's finding is not a discovery.** Threads sometimes contain a human pasting one reviewer's review into another's thread, or a reviewer replying to a comment already on the PR. Credit `foundBy` only for findings a reviewer published independently, before or without sight of the other's. Check timestamps before crediting.

```bash
git fetch origin <reviewedCommit> && git show <reviewedCommit>:<path>
```

Two traps in that command:

- **If the fetch fails, stop.** After a force-push the object is unreachable, and on fork PRs the intermediate commits are never published. The `&&` short-circuits silently and you end up reading the working tree — which means a finding that was real when the reviewer wrote it, and fixed by head, gets labelled `incorrect`. That penalty lands hardest on whichever reviewer ran earliest. Label the instance `unverified`, say why, and never judge against head as a substitute.
- **`side: "LEFT"` means the comment points at the base file, not the head file.** `git show <commit>:<path>` gives you the RIGHT side. For a LEFT-side comment read the pre-image instead, or you will judge unrelated code. A finding with `scope: "file"` is file-scoped and legitimately has no line — that is not a parse failure.

Label every finding instance:

- `confirmed` — the code at that commit contains the reachable wrong output or violated contract the finding describes
- `below_bar` — the mechanism is real but produces no material harm: polish, a speculative test request, a product choice. Real, just not worth a reviewer's comment
- `incorrect` — the code, tests, dependency behavior, or an explicit repo contract disproves the claim
- `unverified` — proving it needs external state you cannot reach (a live provider response, production data). Use sparingly; try to resolve it first
- `drifted` — the finding was published for a different code state and cannot be compared at this head
- `out_of_scope` — the claim belongs to a category excluded by the defect definition frozen in the run manifest

Keep `below_bar` and `incorrect` strictly apart. One is a cautious reviewer, the other is a hallucinating one, and collapsing them punishes both equally.

**`below_bar` versus a `confirmed` finding at `nit` severity** is the highest-leverage boundary in this pass — it moves a finding between the precision numerator and the noise count, the two headline numbers — and it is easy to apply inconsistently. Use one test: **does the finding name a concrete wrong output or violated contract?** If yes, it is `confirmed`, and `nit` severity if the harm is trivial. If it names no wrong output at all — a naming preference, a speculative test request, a product opinion, a "consider extracting this" — it is `below_bar`, whatever its severity would have been. Apply this identically across reviewers; drift here silently reorders the scorecard.

**Re-rate severity yourself.** Reviewers rarely invent a bug; they routinely over-rate one. Record what the reviewer claimed *and* what you judge. A real bug labelled critical that is really a nit still counts as found — at nit severity.

### Step 3 — reconcile into defects

Merge every confirmed finding and every cold-review defect into one deduplicated defect list.

- Findings from different reviewers describing **the same mechanism** are one defect, however differently worded. This is where the biggest errors hide: an over-merge erases a reviewer's unique catch, an under-merge invents one. When two findings touch the same line but describe different wrong outputs, they are two defects.
- **The same test applies within one reviewer's own output, and it is easy to forget.** A reviewer that files six comments about one broken predicate must not become six defects while a reviewer that said the same thing once becomes one. Apply this test both ways: **two findings are one defect if a single corrected line, predicate, guard, or config value resolves both.** They are two defects if fixing one leaves the other reachable. Name that single fix when you merge.
- A reviewer re-posting the same unfixed mechanism on a later head is `duplicateOf` the first instance, not a new finding.
- A summary comment restating an inline finding is `duplicateOf` the inline one.
- Genuinely different residual defects after an attempted fix are separate defects, because they exist on different code.
- Set `foundBy` to every reviewer with a confirmed instance mapping to that defect. A defect only you found gets `foundBy: []`.
- Set `actioned` from the evidence: a follow-up commit fixing it, or the author replying that they will. `null` if unclear.

### The presence interval — this drives the headline metric

Scoring asks: *of the defects that were live in code at a commit this reviewer actually reviewed, how many did it find?* That requires knowing when each defect existed, so record two fields per defect:

- **`introducedAt`** — the earliest commit in this PR whose code contains the mechanism. **Not the commit where a reviewer happened to raise it.** Check the earlier commits explicitly: if the code is byte-identical at an earlier reviewed commit, the defect was introduced there. Pinning a defect late silently excuses every reviewer that ran earlier from a miss it actually had.
- **`fixedAt`** — the commit that resolves it, or `null` if it is still live at head. A reviewer that only reviewed commits after the fix never had the chance to catch it.

Copy `commitOrder` **verbatim** from the raw file. Do not rebuild it from `commits`: on a rebased or force-pushed PR the sha a reviewer actually read is often no longer reachable from the head, and `commits` does not contain it. `fetch-pr-reviews.mjs` resolves those by sha and places them in `commitOrder` by committer date; rebuilding the list from `commits` drops them, which makes every finding on those commits unplaceable and records the reviewer that published it as having missed it. Any commit it could not resolve at all is in `unresolvableCommits` — mark defects pinned there `presenceAmbiguous: true`.

**Write every sha as the full 40 characters, exactly as the raw file gives them.** Every metric in this audit joins on these strings. A short sha copied out of `git log --oneline` is resolved against `commitOrder` where it can be, and where it cannot the defect is dropped from scoring and reported as a corpus bug — it does not quietly become a miss for anyone. A PR with no `commitOrder` is excluded from the report entirely.

Use `reviewersByCommit` from the raw file as-is. It records who ran against each commit. Note that some reviewers edit one summary comment in place on every round instead of posting a new one; `fetch-pr-reviews.mjs` already folds the commits such a body claims to have reviewed into this map, so do not second-guess it downward.

### Step 4 — write the file

```json
{
  "repo": "<REPO>",
  "pr": 973,
  "url": "https://github.com/<REPO>/pull/973",
  "createdAt": "2026-08-10T14:02:00Z",
  "reviewEvents": [
    {
      "reviewer": "some-reviewer[bot]",
      "reviewedCommit": "abc123",
      "verdict": "issues_found",
      "submittedAt": "2026-08-10T14:19:00Z",
      "minutesToReview": 17
    }
  ],
  "reviewersByCommit": { "abc123": ["some-reviewer[bot]", "other-reviewer[bot]"] },
  "commitOrder": ["abc123", "def456", "ghi789"],
  "defects": [
    {
      "id": "d1",
      "title": "Refund path releases the row lock before the ledger write commits",
      "commit": "abc123",
      "introducedAt": "abc123",
      "fixedAt": "ghi789",
      "severity": "blocking",
      "class": "data-money",
      "evidence": "services/refund.ts:214 — two concurrent refunds on one payment both pass the balance check and both write",
      "discoveredBy": "reviewer",
      "foundBy": ["some-reviewer[bot]"],
      "actioned": true
    }
  ],
  "instances": [
    {
      "id": "inline-2481930",
      "reviewer": "some-reviewer[bot]",
      "reviewedCommit": "abc123",
      "label": "confirmed",
      "defectId": "d1",
      "claimedSeverity": "major",
      "auditedSeverity": "blocking",
      "class": "data-money",
      "runtimeVerified": false,
      "duplicateOf": null,
      "note": "reproduced with two concurrent calls against the test fixture"
    }
  ],
  "notes": "Reviewer B first ran against def456, three commits later; its findings are not comparable on abc123."
}
```

`verdict` is `clear` when the reviewer explicitly said it found nothing, otherwise `issues_found`. `runtimeVerified` is true only when the reviewer showed evidence it executed something — a command, its output, a reproduction — not when it merely asserts confidence.

Return only the path you wrote. Do not summarize the PR.

---

## Pass 2 — targeted skeptic

You are a second auditor. Another agent labelled this PR; your job is to **break its labels**, not to agree with them.

Read `<OUTDIR>/<PR>.json` for the claims, then work from the code at each `reviewedCommit` — not from the first agent's reasoning. When you are genuinely uncertain, overturn.

Attack, in order:

1. **Every `incorrect` and `below_bar` label.** Did the first agent dismiss a real bug? Construct the concrete input and wrong output that would make it `confirmed`. Being unable to is what justifies the label.
2. **Every defect with a single reviewer in `foundBy`.** Uniqueness claims carry the whole argument. Did another reviewer describe the same mechanism in different words, in a summary comment, or on an adjacent line? If so it is shared, and the merge was missed. Equally: was the second reviewer merely reacting to the first's published comment? Then it is not shared.
3. **Every defect with `foundBy: []`.** Is it real, is it reachable, and is it actually *introduced by this PR* rather than pre-existing? These inflate "everyone missed it," which is the report's most quoted number.
4. **Every `blocking` and `major` severity.** State the concrete harm. If you cannot, drop it a rank. Do not rate a defect **above** the severity the reviewer itself claimed without stating why the reviewer under-rated it — an unexplained upgrade quietly flatters that reviewer's severity accuracy.
5. **Every merge, and every failure to merge.** Two findings merged into one defect erase a reviewer's catch — check that they truly describe the same wrong output. Then check the reverse, which the first pass is not warned about: several defects credited to **one** reviewer that a single corrected line, predicate, or guard would resolve together are one defect, not several. Collapse them and name the fix.
6. **Every `introducedAt`.** Read the code at the earlier commits. If the mechanism is already present at an earlier reviewed commit, move `introducedAt` back. A late pin removes the defect from the opportunity set of every reviewer that ran earlier, which is the largest single distortion available to this pass. Check `fixedAt` the same way.

Rewrite `<OUTDIR>/<PR>.json` with the reconciled labels and append a `skeptic` object. It records `status` as `upheld`, `revised`, `rejected`, or `not_run`, plus a `changes` array (`{"target": "...", "from": "...", "to": "...", "why": "...", "commit": "<full sha>", "path": "...", "line": 1}`). A material negative claim with `not_run` cannot enter a headline count. Return the skeptic object.

**Change a label only when you can state the evidence that forces the change.** Record `refuteChanges: []` when the first pass was right — that is a real result and it must be reportable. Do not manufacture an overturn to look diligent: an agent that changes labels to satisfy a quota destroys the one signal this pass exists to produce, which is whether the first pass can be trusted. If you find yourself with no evidence either way, say so in `refuteNotes` and leave the label alone.

Every change must name the file and line you read, at the commit you read it at. When every targeted claim survives, use `status: "upheld"` with an empty `changes` array. Do not manufacture an overturn.

---

## Pass 3 — human engagement

A third, separate agent per PR.

You are recording **what the humans on this PR actually did with each reviewer's findings.** This is the
strongest available evidence of whether a finding was worth publishing: an author who fixes code, or argues
back with reasoning, has engaged with it. A finding nobody ever responded to and nobody acted on delivered
little value however technically correct it was.

**Raw reviewer dump (bodies + human replies):** the `--out` file from `fetch-pr-reviews.mjs`
**Audit labels:** `<OUTDIR>/<PR>.json`
**Write your result to:** `<ENGAGEMENTDIR>/<PR>.json`

## The asymmetry you must not flatten

Reviewers publish findings in two places:

- **inline review comments** — these open a thread, so a human can reply to them directly
- **summary comments** — a single long comment listing many findings; a human *cannot* reply to an
  individual item in it

A reviewer that files most of its findings in summaries will look ignored if you only count threaded replies.
So for **every** finding record `replyable`: `true` for inline, `false` for summary-only. Then judge
engagement from **all** available evidence, not just threads:

- a threaded human reply to that specific comment (`humanReplies[]`)
- a human comment elsewhere on the PR that clearly addresses that finding (`humanComments[]` — top-level
  issue comments and human review bodies; this is the only channel by which a person can answer a
  summary-only finding, so check it before recording `none` against a summary reviewer)
- the thread being **resolved** (`resolved: true`) — the cheapest strong `accepted` signal — or **hidden**
  as outdated or off-topic (`minimized`, `minimizedReason`), which is a strong `rejected` signal
- reactions on the comment (`reactions.up` / `reactions.down`)
- **a later commit that changes the code the finding pointed at** — this counts as engagement even with
  total silence, and it is the only signal available for summary-only findings

Where these disagree, prefer words over code motion: an actively-developed file changes for reasons that
have nothing to do with the finding. Say which signal you used in `evidence`.

## For every finding instance in the audit file, classify `outcome`

- `fixed` — the code changed in response. Verify in the diff between commits; do not take "Fixed in abc123"
  at face value, authors sometimes believe a fix landed when the mechanism survives. If they claimed a fix
  and the mechanism survives, use `fixed_claimed_not_real` and say what survived.
- `accepted` — a human agreed in words but the code did not change in this PR
- `rejected` — a human disputed it and did not change the code. Record their reason in `humanReason`. This
  is the most valuable label in the pass: it is a domain expert telling you the finding was not worth making.
- `discussed` — substantive human engagement, outcome genuinely unclear
- `none` — no human words, no code change traceable to it

Also set `humanWords: true` when a person wrote anything about the finding (as opposed to code merely
changing), and set `authorIsBot` from the raw file's `authorType` field (`"Bot"`) rather than guessing from
the login — an agent author accepting a finding is weaker evidence than a human engineer doing so, and on
repos where agents open most PRs this distinction carries the entire engagement section.

Include `repo` in your output so outcomes cannot attach to a same-numbered PR in another repo.

**Write an entry for every non-duplicate instance, including the ones nothing happened to.** A missing
entry is counted as `none` and reported as a data problem; a pass that only records findings which got a
response drives "silently ignored" toward zero and makes every reviewer look engaged with.

## Output

```json
{
  "pr": 0,
  "authorIsBot": false,
  "findings": [
    {"instanceId": "inline-123", "reviewer": "x[bot]", "replyable": true,
     "outcome": "rejected", "humanWords": true,
     "humanReason": "the starvation is real but reserving capacity per account fixes it more cheaply",
     "evidence": "reeceengle reply on the thread; no code change to findDrainCandidates through head"}
  ]
}
```

Include an entry for **every** non-duplicate instance in the audit file's `instances[]`, inline and summary
alike. The count must match. Return only the path you wrote.
