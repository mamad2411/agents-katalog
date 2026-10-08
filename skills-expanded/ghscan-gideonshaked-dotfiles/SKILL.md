---
name: responding-to-code-review
description: "House style for answering code review feedback: every reviewer point quoted verbatim with the reply beneath it, consolidated into one comment. Covers PR reviews, inline threads, and review feedback given anywhere else."
when_to_use: "Use whenever review feedback is going to get a reply, in whatever words it arrives: address the review comments, reply to the reviewer, handle the feedback on a PR, fix what they flagged, what should I say back. A pasted review body, a PR link, or `gh pr view` output showing comments is the same trigger. Use it once the changes a review asked for are made, because reporting back is the deliverable and the reply is what the reviewer sees. Use it again when a reviewer answers on a thread already replied to. Use it for feedback that is not a formal PR review at all: an inline thread, a Slack message, a verbal list, or the findings of a code-review tool. Reach for it as soon as review feedback is in play, not only at the moment of writing the comment."
argument-hint: "[PR number, review, or comment to respond to]"
---

# Responding to code review

Respond to the review feedback point by point: `$ARGUMENTS`

Every reviewer point gets quoted verbatim in a blockquote, with your response directly beneath it. This anchors each answer to the exact comment it addresses, so the reviewer can see at a glance that nothing was dropped and can check each response against what they actually wrote. One consolidated comment, never a scatter of separate replies.

This is the house style for all review responses. Follow it whether the feedback is a formal PR review, an inline thread, a Slack message, or a verbal list.

## Scope: this skill writes the comment, not the fixes

The deliverable is the response comment. This skill governs how you write it, not how you carry out the work the reviewer asked for. Making the fixes, adding the tests, running the suite, tracing a claim to verify it: those happen separately, before you write, through whatever tools or skills the task needs. This skill assumes that work is done (or that you have a truthful position on why it is not) and turns it into a point-by-point reply. Do not treat invoking it as the moment to start fixing; treat it as the moment to report.

## The rule

- Copy each reviewer point verbatim into a Markdown blockquote (`>`), then put your response directly beneath that quote.
- Do this for every point: every sub-bullet, every nit, every low-priority item. No point is too small to quote.
- Consolidate everything into a single comment. Never paraphrase a point away, and never post many separate comments.
- Be honest. If something was not addressed, quote it and say so plainly rather than skipping it.

## Step 1: Gather every point

Pull the complete feedback before writing anything. Miss a point and the quote-and-respond structure silently drops it, which is the exact failure this style exists to prevent.

- For a PR review, read the review body AND every inline comment AND any reply threads. A GitHub review is often a summary body plus separate inline comments on specific lines.
- Fetch them with the tools, do not work from memory:
  - `gh pr view <n> --json reviews --jq '.reviews[] | {author: .author.login, state, body}'`
  - `gh api repos/<owner>/<repo>/pulls/<n>/comments` for inline line comments
  - `gh api repos/<owner>/<repo>/pulls/<n>/reviews/<id>/comments` for one review's inline comments
- List every distinct point, grouped as the reviewer grouped them (severity headers, numbered findings). Preserve their order and their grouping.

## Step 2: Precondition, the work is done and verified

This step is not part of writing the comment. It is the precondition the comment reports on. Do it before you write (through other skills or tools), so every response is true when posted.

- Trace the actual code path before claiming anything about behavior. Do not assert a fix works, or that a finding is a non-issue, without checking the specific conditions.
- Make the fixes, add the tests, run the suite and the linter. Note the commit hash for each change so responses can cite it.
- If you disagree with a point, verify your counter-position against the code first, then say so with the evidence.
- If a point turns out to be a non-issue, prove it (query the data, read the history) rather than dismissing it.

Once this is settled, the rest of the skill is purely about composing the reply.

## Step 3: Draft one consolidated comment

Structure the comment to mirror the review:

1. A one or two line preamble: thank the reviewer, state where the changes live (commit hashes), and give the headline result (for example "all blockers addressed, suite green at N tests").
2. The reviewer's own section headers (for example "Must address", "Medium", "Low", "Nits"), so your comment reads alongside theirs.
3. Under each header, one quote-and-respond block per point, in the reviewer's order.

Keep the whole thing in one comment. If the review had a "bottom line" or intro line worth acknowledging, quote and answer that too.

## Step 4: Write each response

Beneath each quoted point, state what you did in plain, specific terms:

- What changed, and where. Name the function, file, or test. Cite the commit.
- If you followed the reviewer's suggested fix, say so. If you deviated, say what you did instead and why.
- If you added a test, say what it now covers.
- Keep it tight. The reviewer wrote the context already; you are reporting the resolution, not re-explaining the problem.

Match the prose to house style: plain English, active voice, no marketing language, no em-dashes.

## Step 5: Be honest about gaps

The point of anchoring each response to a verbatim quote is that gaps become visible. Do not let that push you into hiding them.

- If you did not address a point, quote it and say so, with the reason and whether it is a follow-up.
- If you found a related problem while fixing, disclose it under the relevant point rather than burying it.
- If you are deferring something, say when or under what condition it lands.
- Never claim done what is not done. A reviewer who catches one inflated "fixed" distrusts the whole comment.

## Step 6: Post one comment

- Write the comment body to a temp file, then post with `gh pr comment <n> --body-file <path>`. Writing to a file avoids shell-escaping breakage from backticks, quotes, and newlines in the body.
- Post exactly one comment. Do not fire off a separate reply per inline thread.
- After posting, confirm the URL and report it.

## Format template

The reference shape, data-agnostic:

```markdown
Thanks for the review. Everything below is in <commit>; <headline result>. Responding to each point inline.

## <reviewer's section header, e.g. Must address>

> <reviewer point 1, verbatim, including their own bold/italic/links>

<your response: what changed, where, which commit; or why not, honestly>

> <reviewer point 2, verbatim>

<your response>

## <next reviewer section header>

> <sub-bullet or nit, verbatim>

<your response>
```

## Worked example

A real response, abbreviated:

```markdown
Thanks for the fast re-review, and for verifying #1 against the real migration history. Everything below is in `06d4636`; the suite is green (193 tests, was 185). Responding to each point inline.

## 🟡 Recommend fixing before merge

> **`notion.py:289`, `page_id_from_ref` returns the wrong id for a database-view URL.** It strips all dashes then takes the last 32-hex match [...] Fix: `path = ref.split("?")[0]` before stripping dashes.

Fixed exactly as suggested: `path = ref.split("?", 1)[0]` before the dash strip, so only the path is scanned and the `?v=` view id can't win. Added a focused `test_page_id_from_ref_ignores_database_view_id` regression, and the existing test now uses a real 32-hex `?v=` (the 3-hex one masked it).

## 🟢 Nice-to-have

> **`config.py:79` reads all three secrets eagerly** [...] This is fine as-is.

Left as-is on purpose, agreeing with your read: the loud failure is the desired behavior. If we ever want to narrow the blast radius I'll take the `include_gmail` opt-in route rather than a try/except.
```

Note what the example does: quotes the reviewer's own emphasis and code spans verbatim, cites the commit, states the deviation (`split("?", 1)` vs the suggested `split("?")`), and on the second point agrees and defers a change with a named alternative rather than silently doing nothing.

## Anti-patterns to avoid

| Anti-pattern | Why it is bad | Do this instead |
|---|---|---|
| Paraphrasing the reviewer's point | Loses their exact wording, hides what you skipped | Quote verbatim in a blockquote |
| One comment per inline thread | Noisy, hard to review as a whole | One consolidated comment |
| Skipping nits and low-priority items | Reads as ignoring feedback | Quote and respond to every point |
| "Done" / "Fixed" with no specifics | Reviewer cannot verify, distrust grows | Name the change, file, and commit |
| Claiming a fix you did not verify | Inflated claims poison the whole comment | Trace the code, run the tests, then claim |
| Silently omitting an unaddressed point | The gap is invisible and looks deliberate | Quote it and say you did not address it, with the reason |
| Re-explaining the problem back | Wastes the reviewer's time | Report the resolution; they wrote the context |
