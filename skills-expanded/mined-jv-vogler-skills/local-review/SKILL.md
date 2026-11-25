---
name: local-review
description: >
  Use when reviewing a pull request or branch locally without posting to
  GitHub — the user says "review PR #N", "review this PR locally", "check
  this branch's changes", "review my diff", asks whether a PR matches its
  ticket or does what the task asked, or wants review comments written to a
  file to read, filter, and copy before publishing anything.
---

# Local PR review

Review a PR against what its ticket asked for, verify every finding by
running code, and write it all to a local scratchfile — never to GitHub.

## Flow

1. **Target** — first that applies: given PR number (`gh pr view/diff <N>`);
   current branch's open PR (`gh pr view`); local diff vs base
   (`git diff <base>...HEAD`). Say which you used.
2. **Spec** — find a ticket reference anywhere: branch name, PR title, PR
   description. Teams differ; there is no fixed pattern. Fetch the ticket via
   the Jira/Atlassian MCP tools. MCP missing or ticket unreachable → the PR
   description becomes the spec. Neither exists → infer intent from the code
   and say so in the overview. Beyond ticket-hunting, the PR description is
   not review input — judge the changes, not the pitch.
3. **Big picture** — establish what the project does and what the touched
   area is for: README, CLAUDE.md, directory layout, the modules around the
   change. A diff can be locally correct and still wrong for the system.
4. **What changed** — describe the change at business level: "fixes the
   duplicate image on the product page", never "renamed a to b, added an if".
   No code in the overview.
5. **Scope check** — ticket vs changes: matches / misses pieces / does
   unrelated extras. Fundamental mismatch (solves a different problem) →
   stop and ask whether to review anyway. Anything less → record it in the
   overview's verdict line, keep going.
6. **Find problems** — correctness (edge cases, wrong data, unhandled
   errors, races) and design (should this exist in this shape, consistency
   with sibling code, silent breaking changes). Ground every candidate in
   code you actually read: open the definitions the diff calls, check the
   data model, compare with siblings.
7. **Verify** — every finding gets tested before it's written up, as you go
   or in one batch at the end, whichever is cheaper. Prefer a failing test
   that reproduces the bug — include it in the comment; it's the most useful
   artifact you can hand the author. When a test can't capture it, run the
   app and interact with it. Testing needs the PR's code: work in place if
   already on the branch with a clean tree, otherwise a temporary git
   worktree. Delete temp tests and worktrees after. Genuinely impractical to
   test (network, third parties)? High-confidence inference is acceptable —
   hedge honestly in the comment and mark the proof line. Discard whatever
   fails verification: a killed false positive is the system working.
8. **Write** — fill the template below.
9. **Humanize** — run the prose through the **`writing:humanize`** skill. No
   fake-personal voice in either direction ("I really like this PR…"):
   genuine strengths go under _Quality points_ as factual bullets; the user
   writes their own compliments from them.

## Comment format

Comments are grouped by file: one `##` per file, one `###` per comment under
it, so the user can fold each file and each handled comment while working
through the list. The `###` heading is `Lines N-M — plain-language title`.
Everything between the heading and the proof line is the pasteable comment.

A comment is, in order:

1. The alert block: tier + the consequence in a few words.
2. One paragraph, at most two sentences: what breaks and what it costs,
   consequence first, in terms a non-engineer could follow.
3. At most one evidence block — a ```diff fix, a small table, or
   input → expected vs got. It shows what the paragraph claims; it never
   restates the paragraph.

### Lines 41-48 — retried webhooks silently drop orders

> [!WARNING]
> **Should-fix** — orders can disappear with no trace

When the payment provider retries a webhook, the second save fails and the error is swallowed — the order is lost and nothing is logged.

```diff
-  } catch (e) {}
+  } catch (e) { logger.error(e); throw e; }
```

_Verified: test double-firing the webhook — order row gone, no log line._

Match that example's length and density. Hard limits:

- **Budget: pasteable prose ≤ 500 characters per comment** (alert text +
  paragraph + any bullet text). Count it, don't eyeball it.
- **Named exception — incident risk:** a warning about data loss, a security
  hole, or breaking prod keeps whatever length it needs. Cut explanation,
  never warnings.
- **Mandatory cut pass:** draft the comment, then cut half of it; only the
  cut version lands in the file. First drafts calibrate to "thorough".
- **Never hard-wrap prose anywhere in the file.** GitHub renders every
  newline inside a comment as a line break, so one paragraph = one line;
  let the editor soft-wrap.

Never include in a comment:

- The code restated in words, or anything the diff makes obvious.
- Background the author already has — they wrote the PR.
- How you found the problem.
- A second fix option. Pick the best one; if the choice genuinely belongs to
  the author, name the options in one sentence.
- The same fact as both prose and bullets.

Other rules:

- Bullets over prose whenever they're easier to scan and end up shorter;
  they count toward the budget.
- Fixes as ```diff blocks whenever concrete — GitHub renders them red/green.
- Other files referenced → markdown links with relative paths.
- Backtick every identifier, column, and path.
- Below the comment, a proof line for the user's triage (not pasted):
  _Verified: <how>_ or _Inferred: <why still confident>_.

## Severity

| Tier       | Alert        | Bar                                               |
| ---------- | ------------ | ------------------------------------------------- |
| Blocker    | `[!CAUTION]` | breaks prod, loses data, security hole            |
| Should-fix | `[!WARNING]` | real bug or trap; fix before or right after merge |
| Suggestion | `[!TIP]`     | improves the change; author's call                |
| Nitpick    | `[!NOTE]`    | style or taste; fine to ignore                    |

Tier + a few-word reason on the alert's first line. Torn between tiers →
pick the lower.

## Output template

Write `<repo-root>/pr-<N>-review-notes.md` (no PR: `review-notes-<branch>.md`).
Keep the `##`/`###` levels — they fold.

```markdown
# PR #<N> — <TICKET-KEY>: review notes

Scratch file — not for committing. One ## per file, one ### per comment; paste the block under it.

## Overview

<Business-level description, 2-5 sentences. No code.>

_Verdict: <one italic line — does what the ticket asked / misses X / also does unrelated Y>_

**Ticket:** <one line — what it asks for>

## Quality points

<At most 3 bullets, each a fact the author can't already see: something you verified beyond what CI runs, or a non-obvious decision that's right. CI results, linter output, and praise adjectives never qualify. Nothing qualifies → delete this section.>

## `path/to/file.ext`

### Lines N-M — <plain-language title>

<alert block, paragraph, evidence — the pasteable comment>

_Verified/Inferred: …_

## Related findings (pre-existing, not this PR)

<Same format. Optional follow-ups — never review feedback on this PR.>
```

## Don't

- Post anything to GitHub (`gh pr review`, `gh pr comment`) unless asked
  afterward.
- Invent findings. A clean PR gets no file-level `##` sections and an honest
  _Quality points_ list (or none) — that's a valid, complete review.
- Leave traces: temp tests deleted, worktrees removed, the user's branch and
  uncommitted work untouched.
