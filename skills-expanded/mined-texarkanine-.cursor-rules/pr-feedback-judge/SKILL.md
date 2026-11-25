---
name: "pr-feedback-judge"
description: "Invoke with /pr-feedback-judge"
disable-model-invocation: true
---

# PR Feedback Judge

Evaluate one or more pieces of GitHub PR review feedback against the standard "valid? worth fixing? in scope for this PR?" rubric and emit a per-item verdict with an explicit disposition.

**Access requirements.** Prefers the `gh` CLI for direct, batched fetches. Falls back to a registered GitHub MCP server. Requires one or the other — anonymous public access is not supported. Judging also depends on reaching the code under review when the claim leaves the hunk or an outdated anchor must be resolved; see [Reading the Code Under Review](#reading-the-code-under-review).

## ⚠️ Load-bearing instruction: fetch first, never judge from the URL alone

**Always fetch the actual comment text and consider it before forming any opinion.** Do not improvise a verdict from the URL slug or the file path alone. The reviewer's actual words — and the diff hunk they were anchored to — MUST be retrieved and considered before you judge. Check whether the anchor still describes the current code before treating a line number as trustworthy. Fetch first, then evaluate. Every time.

## URL shape → GitHub endpoint

Classify each input URL by its fragment, then dispatch. Each shape **fetches material**; only [actionable findings](#what-becomes-an-item) become Items.

| URL fragment | Shape | API path (under `https://api.github.com`) | Fetches |
|---|---|---|---|
| (none) — `…/pull/N` | Whole PR | `/repos/{o}/{r}/pulls/{N}/comments` + `/repos/{o}/{r}/issues/{N}/comments` + `/repos/{o}/{r}/pulls/{N}/reviews` (all paginated) | All inlines (incl. anchor fields), conversation comments, and review bodies — then filter to findings |
| `#pullrequestreview-<rid>` | PR review | `/repos/{o}/{r}/pulls/{N}/reviews/<rid>` + `/repos/{o}/{r}/pulls/{N}/reviews/<rid>/comments` | That review's body + its inlines (incl. anchor fields) — then filter to findings |
| `#discussion_r<cid>` | Inline review comment | `/repos/{o}/{r}/pulls/comments/<cid>` | Single inline (incl. `diff_hunk`, `path`, `in_reply_to_id`, and anchor fields) — then filter |
| `#issuecomment-<cid>` | Conversation comment | `/repos/{o}/{r}/issues/comments/<cid>` (+ that author's reviews/inlines on the PR — see below) | Linked comment as context; resolve the author's review findings on the PR |

If a URL doesn't match any of these shapes: emit "could not classify URL: `<url>`" for that item and continue with the rest. Do not crash, do not guess.

### Author resolution for `#issuecomment-…`

Bot (and human) "review" posts often land as conversation comments that are mostly summary. When the user passes `#issuecomment-<cid>`:

1. Fetch that comment; note `user.login`.
2. **Read the body for orientation** — overview, confidence, file lists, walkthroughs. Do **not** turn orientation prose into Items.
3. Fetch that author's review artifacts on the same PR: their rows in `pulls/{N}/comments` and `pulls/{N}/reviews` (filter client-side by user).
4. Build Items only from [actionable findings](#what-becomes-an-item) in those artifacts (and from distinct findings stated in the linked body that are not already covered by an inline).

Same rule when a whole-PR fetch includes such a conversation comment: use it as context for that author; do not emit an Item for the summary itself.

## Anchor State

Every inline carries an `anchor` value — computed by the T1 `--jq` projection, or derived locally under T2:

| Value | When | Consequence for judgment |
|---|---|---|
| `current` | `line` is non-null | Read current code at `line` only when the code source is verified at the PR head SHA |
| `outdated` | `subject_type` is `line` and `line` is null | Do not read current code at any line number. Locate the referenced text by searching the current file for the content of `diff_hunk`. Require exactly one match; if zero or many, report the anchor unresolved and do not judge against a guessed occurrence |
| `file` | `subject_type` is `file` | A null `line` is expected; it carries no staleness meaning |

Derivation when no `--jq` runs: `file` if `subject_type == "file"`; else `outdated` if `line == null`; else `current`.

`original_line` and `original_commit_id` address the historical blob the reviewer saw. Retain them for reporting. Never use them to index current code.

## What becomes an Item

An **actionable finding** is a concrete claim about the PR's code, tests, docs, config, or behavior that asks for a change, raises a defect, or poses a substantive question about the diff.

**Read but do not Item-ize** (no per-item block, no triage row, no "nothing to address about the flowchart" verdicts):

- Walkthroughs, change stacks, confidence scores, file overviews, mermaid/flow diagrams, pre-merge dashboards, finishing-touch checklists
- Rate-limit / billing / "could not start a review" notices
- Coverage or CI status with no concrete claim about the diff
- Pure acknowledgments or chatter ("LGTM", "works on my machine", "ship it", "thanks")
- Empty review entries (empty body and no inlines)
- Summary rollups that only restate inlines already in the Item set — prefer the inline; never double-count

**Human (or bot) review body with real findings and few/no inlines:** emit **one Item per distinct finding** in the body. A single undifferentiated blob of feedback → one Item for that blob.

**Linked URL that yields zero findings after filtering:** one line — `no actionable findings in <url> (summary/context only)` — then continue. Do not invent Items to fill the rubric.

Anchor state is not a filter. An outdated anchor whose finding still stands is still an Item. Anchor state informs the verdict, never item-ness.

## Reading the Code Under Review

Default: judge from `diff_hunk` plus the reviewer's text. Escalate only when the claim reaches outside the hunk, or an outdated anchor must be resolved by locating that content in the current file.

Choose the first sufficient rung. Declare which rung you used.

1. **At the PR head.** Obtain the PR head with `gh api "repos/{o}/{r}/pulls/{N}" --jq .head.sha` (or equivalent). If `git rev-parse HEAD` equals that SHA, read against that commit — `git show HEAD:{path}`, `git ls-tree HEAD`, `git grep {pattern} HEAD` — not the working tree (a dirty tree is not PR-head evidence). This is the only rung where a `current` `line` can be trusted verbatim. Do not use a comment's `commit_id` as a stand-in for the PR head.
2. **In the repository, off-head.** From `git remote -v`, pick the remote whose URL matches `{o}/{r}`; if none matches, fall through to rung 3. Then `git fetch {remote} pull/{N}/head` (additive: sets `FETCH_HEAD`, does not touch the index, working tree, or any branch). Read against the ref — `git show FETCH_HEAD:{path}`, `git ls-tree FETCH_HEAD`, `git grep {pattern} FETCH_HEAD`. All read-only; no checkout. Materialize a worktree only to run something (`git worktree add --detach` into `mktemp -d`), then `git worktree remove`.
3. **Not in the repository.** Fetch only needed files raw: `gh api "repos/{o}/{r}/contents/{path}?ref={sha}" -H "Accept: application/vnd.github.raw"`.
4. **Clone, last resort.** Only when a prior rung cannot answer — tree-wide search when objects are not local, or running tests. Tree-wide search is not a reason to clone when rung 2 applies. Check `gh api repos/{o}/{r} --jq .size` first (KB). Above tolerance, stay on raw fetches and say why. When cloning: `--filter=blob:none --depth 1 --single-branch` into `mktemp -d`.

When no code source is reachable, or an outdated anchor is unresolved, state that the verdict rests on `diff_hunk` alone.

## Tier Detection Order

Evaluate tiers in this exact order. Use the first one available; do not fall through to a lower tier if a higher one is present.

### T1 — `gh` CLI

Detection:

```bash
command -v gh >/dev/null 2>&1 && gh auth status >/dev/null 2>&1
```

If both succeed, use `gh api` for all fetches. T1 wins on efficiency: it has direct O(1) endpoints for both single-comment URL shapes and composes naturally with batched shell pipelines.

Project every comment and review fetch to the fields below. Measured: inlines drop from ~20.5 KB to ~15.1 KB per page on a busy PR; do not strip the anchor fields to chase a tighter filter — those fields are what staleness detection needs. The projection also computes `anchor` so classification arrives in the data rather than as a per-item derivation.

For the current diff use `gh pr diff {N} -R {o}/{r}` (works outside any checkout) or `gh api repos/{o}/{r}/pulls/{N} -H "Accept: application/vnd.github.diff"`. Never fetch bare `pulls/{N}` JSON for diff purposes. Never use the `application/vnd.github.patch` media type.

Per-shape invocation recipes:

```bash
# Whole PR (paginated). Inline projection retains every field the anchor model needs — do not strip them.
gh api --paginate "repos/{o}/{r}/pulls/{N}/comments" \
  --jq '.[] | {id, user:{login:.user.login}, path, subject_type, line, original_line, commit_id, original_commit_id, side, in_reply_to_id, body, diff_hunk, anchor:(if .subject_type=="file" then "file" elif .line==null then "outdated" else "current" end)}'
gh api --paginate "repos/{o}/{r}/issues/{N}/comments" \
  --jq '.[] | {id, user:{login:.user.login}, body}'
gh api --paginate "repos/{o}/{r}/pulls/{N}/reviews" \
  --jq '.[] | {id, user:{login:.user.login}, state, body}'

# Specific PR review
gh api "repos/{o}/{r}/pulls/{N}/reviews/{rid}" \
  --jq '{id, user:{login:.user.login}, state, body}'
gh api --paginate "repos/{o}/{r}/pulls/{N}/reviews/{rid}/comments" \
  --jq '.[] | {id, user:{login:.user.login}, path, subject_type, line, original_line, commit_id, original_commit_id, side, in_reply_to_id, body, diff_hunk, anchor:(if .subject_type=="file" then "file" elif .line==null then "outdated" else "current" end)}'

# Single inline review comment (direct, O(1))
gh api "repos/{o}/{r}/pulls/comments/{cid}" \
  --jq '{id, user:{login:.user.login}, path, subject_type, line, original_line, commit_id, original_commit_id, side, in_reply_to_id, body, diff_hunk, anchor:(if .subject_type=="file" then "file" elif .line==null then "outdated" else "current" end)}'

# Single conversation comment (direct, O(1))
gh api "repos/{o}/{r}/issues/comments/{cid}" \
  --jq '{id, user:{login:.user.login}, body}'
```

### T2 — GitHub MCP Server

Detection: scan the harness's **registered-MCP-servers list** (the same block of MCP metadata exposed to you at invocation time) for any server whose **name, identifier, or description** contains `github` (case-insensitive substring). If one matches, use its read-only PR/issue tools.

Once a GitHub MCP is detected, read its tool schemas at runtime and pick the tool that matches each URL shape. Filter locally to the same fields the T1 projection keeps, and derive `anchor` with the rule under [Anchor State](#anchor-state).

### No tier available — fail loudly

If neither T1 nor T2 is available, emit verbatim:

> Cannot fetch GitHub data. Install [GitHub CLI](https://cli.github.com/) and run `gh auth login`, or register a GitHub MCP server with your harness.

Do not attempt anonymous `curl`. Do not scrape HTML. Do not pre-fetch the URL via any other path. Stop and surface the message.

## Intro Block

Emit the following block verbatim before evaluating any items:

> Evaluating each piece of PR feedback. I'll fetch the actual comment text first — never judging from the URL alone — then for each item answer three questions and state the disposition.
>
> 1. **Valid?** Is the reviewer technically right about the code? Why or why not?
> 2. **Worth fixing?** Is the issue real and severe enough to act on at all? Why or why not?
> 3. **In scope for this PR?** Should it be fixed on this branch, deferred to a follow-up, dismissed, or already satisfied on the current head? Why or why not?
>
> The three answers compose into a disposition. Feedback can be valid but not worth fixing, valid and worth fixing but out of scope for *this* PR, or valid when written and already satisfied by the current head — I'll spell each one out.

## Per-Item Block

```markdown
### Item N — [link to comment](url) by @author

**Where**: `path/to/file.ts:L42` · anchor: current|outdated|file · code: <rung or "diff_hunk only">
(or "(conversation comment)" / "(review body)" when there is no line anchor)

**Reviewer's point** *(quoted or paraphrased)*:
> …

**1. Valid?** ✅ / ❌ — …

**2. Worth fixing?** ✅ / ❌ — …

**3. In scope for this PR?** ✅ / ❌ / 🕒 follow-up — …

**Disposition**: fix in this PR | already addressed | defer to follow-up | dismiss with acknowledgment | dismiss
```

Disposition vocabulary is fixed (5 values). Pick exactly one per item. Use the emoji set ✅ / ❌ / 🕒 only.

- `already addressed` means the finding was valid when written and the current PR head already satisfies it. It requires code evidence from the ladder; an outdated anchor alone never justifies it. Question 1 is judged as of when the comment was written; `already addressed` resolves question 3 (mark ✅ and say the head already satisfies it).

## Conditional Triage Table

If — and only if — the total number of items to evaluate is greater than 5 (e.g., a whole-PR URL on a busy PR), emit a compact triage table **before** the per-item blocks:

```markdown
| # | Item | Author | Disposition |
|---|---|---|---|
| 1 | [discussion_r123](url) | @reviewer | fix in this PR |
| 2 | [discussion_r456](url) | @reviewer | already addressed |
| 3 | [discussion_r789](url) | @reviewer | dismiss |
```

For 5 or fewer items, skip the table — the per-item blocks alone are clearer at that scale.

## Tail Block

> N items evaluated · X to fix in this PR · A already addressed · Y deferred · Z dismissed.

## Orchestration walkthrough

For each invocation:

1. **Classify each URL** against the shape table. Emit "could not classify" for any that don't match and continue.
2. **Detect tier** (T1 → T2 → fail). Pick the first available. If none, emit the failure message and stop.
3. **Fetch.** Issue the per-shape calls for each classified URL, using the projections under T1 (or the T2 local filter). For `#issuecomment-…`, also fetch that author's inlines and reviews on the PR (author resolution above).
   - **Batch-fetch discipline (specific to this step):** if you end up with **3 or more structurally-identical `gh api` calls** in one invocation (e.g., the user gave you multiple `#discussion_r…` URLs all hitting `pulls/comments/<cid>`), issue them as **one batched shell pipeline**, not a sequential loop of tool calls. Example:

     ```bash
     for cid in 123 456 789; do
       gh api "repos/Texarkanine/a16n/pulls/comments/${cid}" \
         --jq '{id, user:{login:.user.login}, path, subject_type, line, original_line, commit_id, original_commit_id, side, in_reply_to_id, body, diff_hunk, anchor:(if .subject_type=="file" then "file" elif .line==null then "outdated" else "current" end)}'
     done | jq -s '.'
     ```

     For T2 (MCP), batching is per-tool — make the minimum number of distinct MCP calls (e.g., one `get_review_comments` for the whole PR, then filter locally to all the requested `cid`s).
4. **Resolve reply context.** If a fetched inline comment has a non-null `in_reply_to_id`, make one extra call to fetch the parent thread (cheap — single comment). The parent provides the context the reviewer was responding to.
5. **Gate and escalate.** For each inline, note its `anchor`. Decide whether code beyond `diff_hunk` is needed. If so, obtain the PR `head.sha` (see rung 1), select and declare a rung from [Reading the Code Under Review](#reading-the-code-under-review).
6. **Filter to actionable findings.** Apply [What becomes an Item](#what-becomes-an-item). Summaries and walkthroughs are context only. Prefer inlines over summary echoes. If a user-supplied URL yields nothing actionable, emit the one-line note.
7. **Render.** Emit the intro, then (if items > 5) the triage table, then per-item blocks in input order, then the tail. Only findings get numbers.

## Failure modes

- **Malformed / unclassifiable URL** → "could not classify URL: `<url>`" for that item; continue with the rest.
- **T1 hits a 404** → "Got 404 fetching `<url>`. Either the PR is private and your `gh` auth doesn't cover it, the comment was deleted, or the URL is malformed. Cannot evaluate this item." Continue with the rest.
- **No tier available** → see the failure message in the tier-detection section above. Stop.
- **`gh` rate-limit error** → surface `gh`'s message verbatim. Do not retry blindly. Stop.
- **Unreachable code source** → degrade to hunk-only judgment and say so in the Item's `code:` field and the verdict prose. Do not invent file contents.
- **Unresolved outdated anchor** → zero or many `diff_hunk` matches in the current file → same as hunk-only: say the anchor is unresolved; do not pick an occurrence at random.
- **Oversized repository** → when the size check rules out a clone, stay on raw fetches and state that reason. Do not clone anyway.
- **Foreign repository** → when the operator cannot push, author-action dispositions (`fix in this PR`, `defer to follow-up`) are inapplicable — say so and prefer dismiss-family wording or "not actionable by this operator." `already addressed` still applies: it is a factual claim about the current head, not a prescription for the author to act.
