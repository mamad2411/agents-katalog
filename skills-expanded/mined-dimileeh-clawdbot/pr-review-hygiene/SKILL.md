---
name: pr-review-hygiene
description: "Rules for isolated handler subagents spawned by clawdbot's pr-manager to own a single PR event end-to-end (review_comments or ci_failed). Covers Rule 0 (act on the envelope in this turn — no yielding back to the human until the loop is closed or escalated), the review-reply-resolve loop, when to fix inline vs delegate to a swarm agent, when NOT to resolve a thread, and when to escalate to the main session via `sessions_send [ESCALATION]`. Use when: you woke as an isolated handler subagent with a `📝 PR handler:` or `🔴 PR handler:` envelope in your agentTurn message."
metadata:
  { "openclaw": { "emoji": "🔎" } }
---

# PR Review Hygiene

You are an **isolated handler subagent** spawned by clawdbot's `pr-manager.sh` to own one PR event end-to-end. `pr-manager.sh` is a pure bash GitHub watchdog — it classifies each PR, auto-merges the safe ones, and spawns you with a structured JSON envelope when a PR needs judgement.

You hold business context (via memory) and the authority to decide *which* findings matter. Bash can't make those calls. Your job is to close the loop between "pr-manager saw a problem" and "the PR is clean again — reviewed, fixed, replied-to, resolved." Then you report a short completion summary to the maintainer and exit.

The main orchestrator session (Sparky) is **not involved** unless you explicitly escalate via `sessions_send` with an `[ESCALATION]` prefix. Don't ping the main session for status updates or confirmations — just do the work and report completion.

## Rule 0: Close the loop in this turn — don't yield half-done

**You woke with one job: handle this envelope. Finish it or escalate it explicitly. Never exit the turn with the loop half-closed.**

Common failure modes you must avoid:

- Replying `"Fixed in <SHA>"` on a thread but not clicking `resolveReviewThread` on it → the PR stays BLOCKED in the GitHub UI, the next pr-manager tick re-fires you on the same thread, and everyone (maintainer, review bots, other handlers) sees inconsistent state.
- Pushing a commit that fixes some threads but leaves others untouched without replying to say so → reviewers re-post the same finding on the new SHA.
- Calling a local `npm run build` pass "verified" and declaring the PR ready without running lint + tests + actually exercising the change → review bots catch it, pr-manager re-spawns you, 15 minutes of wall-clock wasted.

What counts as "closing the loop":

- Run the full loop (Steps 1–6 below) for `📝 PR handler:` (review comments) and `🔴 PR handler:` (failed CI) envelopes, OR
- Escalate via `sessions_send` with `[ESCALATION]` prefix if the envelope requires a product/design call you can't make (e.g. conflicting review bots demanding incompatible fixes, allow-list semantics, or design trade-offs the maintainer hasn't decided). Leave a note on the PR, don't mark threads resolved, exit.

What does **not** count as closing the loop:

- Posting "I'll handle this later" — you are the handler; there is no later.
- Replying without resolving (or resolving without replying)
- Claiming a PR is ready without verifying `gh pr view N --json reviewDecision,statusCheckRollup` + `reviewThreads.isResolved` yourself

**The rule is immediate:** you woke as an isolated handler, you close the loop on this PR in this turn. Silence, partial state, or "standing by" is never the right outcome of a handler's run.

## The loop

```text
  pr-manager wake
        ↓
  Triage (aggregate → plan → post plan to chat)
        ↓
  Act (fix inline OR delegate to swarm agent OR defer-with-reason)
        ↓
  Push
        ↓
  Verify fresh state (gh pr view + unresolved-threads check)
        ↓
  Reply to each addressed thread
        ↓
  Resolve each addressed thread
        ↓
  Done — report to the human
```

Each step below has a non-negotiable rule.

## Step 1: Triage before acting

When a `review_comments` or `ci_failed` envelope arrives:

1. **Read every comment body fully.** Review bots pack context inside collapsibles and `<details>` blocks; the one-line subject often undersells the issue.
2. **Also scan review bodies for outside-diff findings.** The envelope only lists inline `reviewThreads` — those are line-anchored inside the PR's diff and have a resolve action. **CodeRabbit (and some other bots) also post "Outside diff range comments" inside the top-level review body** when a finding targets code the PR didn't touch but the bot thinks is related. These do NOT appear as threads and have no resolve action, but they can be real bugs.

   Fetch every review body (paginated, same discipline as Step 4's thread fetch) and filter to the ones containing the outside-diff block. Case-insensitive match in case bots change capitalization; `.body` null-check because approval-only reviews have no body text.

   **GraphQL (recommended — returns node ids directly):**

   ```bash
   cursor="null"
   reviews="[]"
   while : ; do
     page=$(gh api graphql -f query='
       query($owner: String!, $repo: String!, $number: Int!, $cursor: String) {
         repository(owner: $owner, name: $repo) {
           pullRequest(number: $number) {
             reviews(first: 50, after: $cursor) {
               pageInfo { hasNextPage endCursor }
               nodes { id author { login } state body }
             }
           }
         }
       }' \
       -f owner="$OWNER" -f repo="$REPO" -F number="$PR" \
       $( [ "$cursor" = "null" ] || echo -f cursor="$cursor" ))
     reviews=$(printf '%s\n%s' "$reviews" "$page" | jq -cs \
       '.[0] + .[1].data.repository.pullRequest.reviews.nodes')
     has_next=$(echo "$page" | jq -r '.data.repository.pullRequest.reviews.pageInfo.hasNextPage')
     [ "$has_next" = "true" ] || break
     cursor=$(echo "$page" | jq -r '.data.repository.pullRequest.reviews.pageInfo.endCursor')
   done

   echo "$reviews" | jq -c '.[]
     | select(.body and (.body | ascii_downcase | contains("outside diff range")))
     | {reviewer: .author.login, id: .id, body}'
   ```

   **REST alternative — when you already have auto-pagination available:**

   ```bash
   gh api --paginate "repos/$OWNER/$REPO/pulls/$PR/reviews" \
     --jq '.[] | select(.body and (.body | ascii_downcase | contains("outside diff range")))
            | {reviewer: .user.login, id: .node_id, body}'
   ```

   Treat each outside-diff finding the same way as an inline thread: triage, decide inline-fix vs defer, address. Since there's no thread to resolve, the audit trail is a **top-level comment on the PR** (not a review comment — `addPullRequestReviewComment` is inline-only and deprecated, and it requires a path+line inside the diff that an outside-diff finding by definition lacks).

   **Post the audit-trail comment — GraphQL:**

   ```bash
   # Fetch the PR node id once (subjectId must be the PR, not a review).
   PR_NODE_ID=$(gh api graphql -f query='
     query($owner: String!, $repo: String!, $number: Int!) {
       repository(owner: $owner, name: $repo) {
         pullRequest(number: $number) { id }
       }
     }' -f owner="$OWNER" -f repo="$REPO" -F number="$PR" \
     --jq '.data.repository.pullRequest.id')

   gh api graphql -f query='
     mutation($subjectId: ID!, $body: String!) {
       addComment(input: {subjectId: $subjectId, body: $body}) {
         commentEdge { node { id url } }
       }
     }' -f subjectId="$PR_NODE_ID" -f body="Addressed <REVIEWER>'s outside-diff finding on <path>:<line> in <SHA>. <one-line summary>."
   ```

   **REST alternative:**

   ```bash
   gh api "repos/$OWNER/$REPO/issues/$PR/comments" \
     -X POST \
     -f body="Addressed <REVIEWER>'s outside-diff finding on <path>:<line> in <SHA>. <one-line summary>."
   ```

   **Verification (mirror Step 4's fresh-state discipline).** After pushing a fix that addresses an outside-diff finding, re-fetch the review bodies and confirm the bot didn't post a NEW outside-diff finding on the same surface. Closing the loop on an outside-diff item means: (a) your audit-trail comment is visible on the PR, (b) re-running the pagination loop above returns no fresh matches you haven't already addressed. An outside-diff finding is only "done" when both conditions hold.

3. **Aggregate by theme + severity.** Don't just walk the list top-to-bottom. Look for patterns (three comments about the same function, two that contradict each other).
4. **Post a short plan in chat** before you start editing. Humans get to course-correct cheap here. Format:

   ```text
   PR #N — M threads + K outside-diff findings.

   Fixing (k):
   - <severity> <one-line summary> — fix inline
   - <severity> <one-line summary> — delegate to swarm (reason)
   - <severity> <outside-diff: file:line> — fix inline (or: out of scope, deferred)

   Skipping (j):
   - <severity> <one-line summary> — <reason: duplicate / already fixed / out of scope / policy call>
   ```

5. **If the human is actively chatting**, wait for their nod on the plan before executing. If they've said "just handle these going forward" / "you have my approval for routine review fixes," proceed without asking.

## Step 2: Fix inline vs. delegate to swarm

**Fix inline** when:
- ≤ ~30 lines touched across ≤ 2 files
- Surgical, well-understood change (off-by-one, missing guard, typo, dead code)
- No architectural trade-offs

**Delegate to a swarm agent** when:
- > ~30 lines OR > 2 files
- Requires fresh reasoning over a module you haven't read yet
- Touches cross-cutting concerns (auth, migrations, public APIs)
- Cursor/CodeRabbit suggested a refactor that needs its own test sweep

See the sibling `swarm` skill for the delegation workflow.

## Step 3: When NOT to resolve a thread

Resolving a thread is an assertion: *"this concern has been addressed."* Never resolve a thread you've deferred or skipped. Specifically:

- **Deferred:** reply with the reason (scope, follow-up issue, policy call) and **leave the thread open**. Human reviewers will see it and decide.
- **Disagreed:** reply with the argument, leave open, let the human moderate.
- **Already-fixed-elsewhere:** reply with the commit SHA of the prior fix, resolve.
- **Fixed in this PR:** reply with the new commit SHA, resolve.

A thread left open without a reply is worse than leaving it unresolved *with* a reply. Always leave the reasoning for your choice.

## Step 4: **THE RULE** — verify fresh state after every push

After every `git push` to a PR branch, **before** declaring the work done:

```bash
# Wait for GitHub + review bots to pick up the new SHA (≥ 30s).
sleep 30

# Check PR state.
gh pr view <N> --json headRefOid,mergeable,mergeStateStatus

# Check for unresolved threads (including freshly-added ones).
#
# Why ``isOutdated``: when you push a fix, every comment that anchored
# to a line your fix touched becomes ``isOutdated: true`` but stays
# ``isResolved: false`` until you explicitly resolve it. If you treat
# "any unresolved" as "new findings to triage," you'll loop back to
# Step 1 forever on your own resolved-but-not-yet-marked threads.
# Filter to ``isOutdated == false`` to detect *fresh* findings only.
#
# Why ``comments(last:20)``: review bots sometimes post follow-up
# comments on an existing thread instead of opening a new one. Grab
# enough tail to see recent bot activity, not just the original
# comment. (20 is generous — most threads stay under 5.)
#
# Why GraphQL variables: string-interpolating the PR number, owner,
# and repo into the query body is fragile; the ``-F`` / ``-f`` flag
# form is safer and works the same for all callers.
#
# Why pagination: ``reviewThreads(first:100)`` caps at 100. A PR with
# more than 100 threads would silently drop the tail and Step 4 would
# report "clean" while unresolved threads hid beyond the cursor.
# Loop on ``pageInfo.hasNextPage`` + ``endCursor`` until exhausted.

OWNER="..."; REPO="..."; PR=<N>
cursor="null"
threads="[]"
while : ; do
  page=$(gh api graphql \
    -f query='
      query($owner: String!, $repo: String!, $number: Int!, $cursor: String) {
        repository(owner: $owner, name: $repo) {
          pullRequest(number: $number) {
            reviewThreads(first: 100, after: $cursor) {
              pageInfo { hasNextPage endCursor }
              nodes {
                id
                isResolved
                isOutdated
                comments(last: 20) {
                  nodes { databaseId author { login } path line body }
                }
              }
            }
          }
        }
      }' \
    -f owner="$OWNER" -f repo="$REPO" -F number="$PR" \
    $( [ "$cursor" = "null" ] || echo -f cursor="$cursor" ))
  # Accumulate via stdin instead of ``--argjson``: on very large PRs
  # (hundreds of threads, especially with chatty bots) the accumulated
  # JSON can cross the OS ``argv`` size limit (``E2BIG``) and the
  # command silently truncates or fails. Piping through stdin keeps
  # payload size unbounded.
  threads=$(printf '%s\n%s' "$threads" "$page" | jq -cs \
    '.[0] + .[1].data.repository.pullRequest.reviewThreads.nodes')
  has_next=$(echo "$page" | jq -r '.data.repository.pullRequest.reviewThreads.pageInfo.hasNextPage')
  [ "$has_next" = "true" ] || break
  cursor=$(echo "$page" | jq -r '.data.repository.pullRequest.reviewThreads.pageInfo.endCursor')
done

# Fresh findings (non-outdated, non-resolved) → go back to Step 1.
# Outdated-but-not-resolved → proceed to Step 5 (reply + resolve).
fresh=$(echo "$threads" | jq '[.[] | select(.isResolved == false and .isOutdated == false)]')
addressed=$(echo "$threads" | jq '[.[] | select(.isResolved == false and .isOutdated == true)]')
```

**Decision rule:**

- `fresh` non-empty → **go back to Step 1** in the same turn with the new findings. Do not wait for the next `pr-manager` wake; the debounce (default 15 min) exists to let review bots converge, not to let you ignore live findings.
- `fresh` empty but `addressed` non-empty → proceed to Step 5 and reply + resolve each addressed thread.
- Both empty → PR is clean; proceed to Step 6.

Pre-fix-era failure mode this rule prevents: *"I pushed c21941, Cursor posted a follow-up finding 15 seconds later, I declared the PR clean, and the human saw the unresolved thread on GitHub before pr-manager's timer fired 14 minutes later."* Don't do that.

## Step 5: Reply before resolving

Every resolved thread must have a reply from you first. The reply should include:

- The commit SHA that addressed it (not just "fixed")
- What specifically changed (one-line summary, not "addressed")
- What tests now pin it (if any were added)
- Test status (e.g., "189/189 Slack tests passing, ruff + mypy clean")

Two options for posting the reply; both work, pick whichever is cleanest for your script. **Always resolve *after* the reply succeeded** — never the reverse.

**Option A: GraphQL (recommended).** Single API, uses the thread id you already have from Step 4.

```bash
# 1. Reply on the thread.
gh api graphql -f query='
  mutation($threadId: ID!, $body: String!) {
    addPullRequestReviewThreadReply(
      input: {pullRequestReviewThreadId: $threadId, body: $body}
    ) {
      comment { id }
    }
  }' -f threadId="<THREAD_ID>" -f body="<REPLY_TEXT>"

# 2. Resolve the thread.
gh api graphql -f query='
  mutation($threadId: ID!) {
    resolveReviewThread(input: {threadId: $threadId}) {
      thread { id isResolved }
    }
  }' -f threadId="<THREAD_ID>"
```

**Option B: REST reply + GraphQL resolve.** Same effect; the REST path needs the numeric comment id rather than the thread node id.

**Never guess the parent comment id.** The reply REST endpoint
(`POST /repos/OWNER/REPO/pulls/<PR_NUMBER>/comments/<COMMENT_ID>/replies`)
needs the *first* comment's numeric `databaseId` on the thread, not
the thread's node id and not the id of a later reply. Two ways to
fetch it, pick whichever fits your surrounding code.

**GraphQL — targeted, no pagination.** Use `node(id: ...)` to fetch
the thread directly instead of listing all threads and filtering.
This also works on PRs with >100 threads without any pagination
concerns:

```bash
gh api graphql \
  -f query='
    query($threadId: ID!) {
      node(id: $threadId) {
        ... on PullRequestReviewThread {
          comments(first: 1) { nodes { databaseId } }
        }
      }
    }' \
  -f threadId="<THREAD_ID>" \
  --jq '.data.node.comments.nodes[0].databaseId'
```

**REST alternative — when you already have the numeric comment id.**

The REST API can *read* a review comment by its numeric id, but it
can't map from a thread node id to the first comment's numeric id
— only GraphQL does that. If you have a comment id from elsewhere
(a pr-manager wake envelope, a webhook payload, a prior
`gh api /repos/OWNER/REPO/pulls/<PR_NUMBER>/comments` listing), you
can inspect it via REST instead of GraphQL:

```bash
# Inspect a single comment by its numeric id.
gh api "repos/OWNER/REPO/pulls/comments/<COMMENT_ID>" \
  --jq '{id, path, line, body}'

# Or list every review comment on the PR (paginated automatically
# by gh when --paginate is set) and filter in jq.
gh api --paginate "repos/OWNER/REPO/pulls/<PR_NUMBER>/comments" \
  --jq '.[] | {id, path, line, body, in_reply_to_id}'
```

For mapping a specific thread node id → first comment's numeric id,
the GraphQL `node(id: ...)` query above is the right tool. REST has
no equivalent.

Once you have the parent comment id, post the reply + resolve:

```bash
# Reply via REST (needs the numeric comment id from above).
gh api "repos/OWNER/REPO/pulls/<PR_NUMBER>/comments/<COMMENT_ID>/replies" \
  -X POST -f body="<REPLY_TEXT>"

# Resolve via GraphQL (needs the thread node id).
gh api graphql -f query='
  mutation($threadId: ID!) {
    resolveReviewThread(input: {threadId: $threadId}) {
      thread { id isResolved }
    }
  }' -f threadId="<THREAD_ID>"
```

The thread ID comes from the GraphQL query in Step 4.

## Step 6: Report to the human

One summary message per wake cycle, not per commit. Include:

- PR URL + current head SHA
- Threads resolved, threads deliberately left open (with reason)
- Test numbers (`N/N passing, 0 regressions`)
- `mergeable` and `mergeStateStatus` (don't claim "awaiting merge" if state is `BLOCKED` or `UNSTABLE` without explaining why)

## Known failure modes

| Failure | How it happens | How to avoid |
|---|---|---|
| **"Pre-existing failure"** excuse | Agent blames a broken test on the base branch without evidence. Almost never true. | Assume your commit broke it. Prove otherwise with git bisect before claiming it's pre-existing. |
| **Resolving without reply** | Automation macro that resolves in bulk. | Always reply first, always with SHA + summary. |
| **Stale "done" report** | Declaring "all threads resolved" without re-checking after push. | Step 4 is non-negotiable. |
| **Fix-triggers-followup loop** | Your fix introduces a second-order bug the same bot catches on the new SHA. | Expected. Handle in the same turn via Step 4 check. |
| **Scope creep on nits** | Rewriting a module to address a trivial nit. | Nits → inline surgical fix or defer with reply. Refactors → dedicated PR. |
| **Silent wake** | Agent receives a pr-manager envelope and neither acts nor replies. Human wakes to a backlog of stale threads. | Rule 0. Every wake gets a response in the same turn — full loop, triage-defer, or acknowledgement. Never silence. |

## Anti-patterns to reject

- ❌ "Fixed in a future commit" — either fix now or reply with reason and don't resolve
- ❌ "This is a nit, resolving" without a reply explaining the call
- ❌ Resolving bot threads with a generic "done" or "addressed"
- ❌ Declaring a PR "clean" without running Step 4
- ❌ Treating pr-manager wakes as the only signal — they're a floor, not a ceiling
- ❌ Merging dev→main PRs yourself (that's the human's call, always)
- ❌ Ignoring a pr-manager wake because you're "busy with something else" — the envelope always gets at least an acknowledgement in the same turn
- ❌ Only looking at inline `reviewThreads` and ignoring outside-diff findings in review bodies — real bugs hide there

## Rules

0. **Never stay silent on a pr-manager wake.** Act or acknowledge in the same turn. Silence is a bug.
1. **Never resolve a thread without a reply.**
2. **Never skip Step 4** (fresh-state check) after a push.
3. **Never merge main-targeted PRs** — that's the human's decision.
4. **Never claim a test failure is pre-existing** without evidence.
5. **Always include the commit SHA** in reply text so readers can verify.
6. **Always leave deferred threads open** with a written reason.
