---
name: artifact-review
description: OUTPUT IS ALWAYS A `.html` FILE (never `.md`, never plain markdown). Use this skill whenever the user asks for a code review writeup, PR review, annotated diff, "review this patch", "give feedback on this change", "leave inline comments on this PR", "summarize what's wrong with this code", or any reviewer-side artifact that pairs concrete diff hunks with human commentary, suggestions, and approve/request-changes verdicts as a polished HTML document. This is the reviewer-side companion to `artifact-report`'s PR writeup (which is author-side). Pair with `artifact-css` for the underlying design system. Do NOT use for casual one-line feedback or for purely conversational review chats — only when an HTML artifact with annotated diffs is the deliverable.
---

# artifact-review

> ## OUTPUT CONTRACT
>
> **Produces ONE `.html` file. Not markdown. Not `.md`. Not plain text.**
>
> Annotated reviews are HTML artifacts. Diff hunks render as `<div class="diff">` + `<div class="diff-row">` — never as ` ```diff ` code fences. Review comments render as `<aside class="note review-comment">` — never as markdown blockquotes. The file extension is `.html`, always.
>
> Use the template in `templates/`. Inline `artifact.css` inside `<style>` (Mode B — single-file portable) or `<link>` to it.

---

The reviewer-side artifact for code reviews. The goal: a developer who can't open the PR in GitHub still sees, on this page, every diff hunk that matters and every comment the reviewer left, in order, with enough context to act.

Read `artifact-css/SKILL.md` first for the full OUTPUT CONTRACT, the design system, and the page skeleton. This skill uses the library's `.diff` system and adds inline comment threading. **No jQuery required** — review artifacts are static.

## When to reach for this skill

- The user pasted a PR URL or a patch and asked for a review.
- The user wants to capture review feedback that will be sent over email / Slack / a thread rather than left on the PR itself.
- The reviewer has already left comments on a PR and wants a polished writeup summarizing the verdict + the top issues.

If the user wants a PR description from the author's side, use `artifact-report`'s PR writeup template instead.

## One template, three modes

`templates/annotated-review.html` covers all three review postures. Pick one in the verdict block and edit accordingly.

| Verdict | Eyebrow chip | Meaning |
|---|---|---|
| Approve | `.badge-success` "approve" | Ship as-is. Comments are nits or future work. |
| Request changes | `.badge-danger` "changes requested" | Must address before merge. Reviewer commits to re-review. |
| Comment | `.badge-info` "comment" | Reviewer has thoughts but isn't gating. Author decides. |

## Anatomy of an annotated review

Built from six blocks. Use this order.

1. **Header.** Eyebrow with repo path + PR number in mono (`acme/billing · PR #247`), h1 with the PR title (not the reviewer's verdict — that goes in the verdict block), `.lead` paragraph with one sentence on what this PR does in the reviewer's own words. NOT a copy of the author's description — the reviewer's restatement is the test for whether they understood it.
2. **Verdict block.** A `.callout` with the verdict badge inline next to the heading. Two or three sentences: what the reviewer would want changed before merge, what they think is good, and any condition for approval. If approve, name the most important nit. If changes requested, name the must-fix.
3. **Summary scorecard.** A `.kv-strip` with five cells: scope (LOC changed) · risk (`.badge-warn`/`-danger`/`-info`) · test coverage stance · backwards-compat impact · rollout safety. These are the dimensions reviewers actually score. Tabular figures so the page reads as a report card.
4. **Top issues.** A `.highlights` list of the three to five most important things. Each item starts with a `<strong>` verb (Fix / Reconsider / Ask / Confirm) and ends with a link-style anchor `#h-N` to the diff hunk below. This is the section the reviewer would copy-paste into Slack.
5. **Annotated diffs.** A series of `.review-hunk` blocks, each containing:
   - `.file-label` with the file path in mono.
   - A `.hunk-anchor` (id like `h-1`, `h-2`) so top-issues can link to it.
   - The `.diff` block with `.diff-row.hunk`, `.diff-row.ctx`, `.diff-row.add`, `.diff-row.del` rows.
   - One or more `.review-comment` cards directly under the diff — the reviewer's annotation. Each comment has a reviewer avatar, a line reference (`L42-45`), a severity chip (`must-fix` / `should-fix` / `nit` / `praise`), the comment prose, and an optional suggested replacement in a small `.code-block`.
6. **What was not reviewed.** A short list. Files skipped, behaviors not exercised, edge cases the reviewer trusts the author on. Naming this is a courtesy to the author — they know what to defend in follow-up review.

End the page with a meta line: reviewer name + timestamp + re-review commitment ("happy to re-review within 4h once the must-fix items are addressed").

## The review-comment primitive

The library does not ship a dedicated `.review-comment` class because the visual is built from existing primitives. Use this exact markup:

```html
<aside class="note note-info review-comment">
  <div class="row-between mb-1">
    <div class="row" style="gap:8px;align-items:center;">
      <span class="avatar avatar-sm">{{INITIALS}}</span>
      <span class="mono small">{{REVIEWER}} on L{{LINES}}</span>
    </div>
    <span class="badge badge-warn">should-fix</span>
  </div>
  <p class="mb-1">{{COMMENT_PROSE}}</p>
  <pre class="code-block"><code><span class="cm">// suggested</span>
{{SUGGESTED_REPLACEMENT}}</code></pre>
</aside>
```

Severity chips and `.note` color pair as follows:

| Severity | `.note` variant | `.badge` variant |
|---|---|---|
| must-fix | `.note-danger` | `.badge-danger` |
| should-fix | `.note-warn` | `.badge-warn` |
| nit | `.note-info` | `.badge-info` |
| praise | `.note-success` | `.badge-success` |

A review with no `praise` notes is a review the author will skim defensively. Drop in at least one when you can.

## Voice and density rules

1. **Concrete, not categorical.** "This function will deadlock if `userId` is the same as `actorId`" beats "potential concurrency concern".
2. **Suggest a fix in code, not in prose.** A four-line suggested replacement is worth a paragraph of "you could refactor this to…".
3. **Severity is for the author, not the reviewer.** Mark nits as nits. Don't mark a nit as must-fix because you feel strongly. Severity inflation kills review velocity.
4. **Praise specifically.** "Clean separation of the validator from the transformer" beats "nice work". Vague praise is patronizing.
5. **Time-box yourself in the verdict.** "I'll re-review within 4h" is a real commitment. Don't dangle the author.
6. **No "what about X" without a hunk.** If the question doesn't anchor to a line, it belongs in the "what was not reviewed" block, not in the diff annotations.

## Common mistakes

- **Wall-of-text comments under a one-line diff.** If the comment is longer than the changed code, the reviewer is restructuring the PR. Suggest a follow-up PR instead.
- **All comments tagged must-fix.** This is severity inflation. Pick the two or three real must-fixes and downgrade the rest.
- **Verdict that contradicts the comments.** "Approve" with three `must-fix` notes makes the document incoherent. Either change the verdict to "request changes" or downgrade the severities.
- **Diff hunks copied verbatim without curation.** A review is not a re-pasted patch. Show only the hunks the reviewer is annotating. Use `.diff-row.hunk` rows to elide skipped context.
- **No "what was not reviewed" block.** Without it, the author can't tell where to put their post-merge attention.

## After the artifact

Always offer two derivatives:

1. A plain-text Slack-paste version: title · verdict · three-line "what I'd want changed" · re-review window.
2. A copy-pasteable list of inline comments formatted for GitHub PR review (one comment per file/line). Useful when the user wants to commit the review to the actual PR after generating the artifact.
