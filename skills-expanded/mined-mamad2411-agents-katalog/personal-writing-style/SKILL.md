---
name: personal-writing-style
description: Write PR descriptions, PR messages, inline PR review comments, Slack messages, update comments, RFCs, design docs, and copy-pasteable summaries in Gui's writing style. Use when the user asks to "write a PR message", "write a PR description", "write a PR review comment", "write a Slack message", "draft this update", "write an RFC", "draft a design doc", or similar, especially for recent changes or local diffs. Also invoke automatically before opening a PR on the user's behalf, to write the PR body. PR descriptions use caveman-full terseness; RFCs and docs use full prose (see the Shape sections).
---

# personal-writing-style

Use this skill to write copy that sounds like Gui: practical, direct, a little candid, and ready to paste into a PR description, Slack thread, or design doc.

## When to invoke

Invoke this skill when the user asks for any of these:

- "write a PR message"
- "write a PR description"
- "write a PR review comment"
- "write a Slack message"
- "draft an update"
- "summarise these recent changes"
- "write an RFC" / "draft a design doc" / "write this design up"
- "make this sound like me"
- Any similar request where the output is user-facing engineering prose, not code.

Also invoke this automatically whenever you are about to open or raise a PR on Gui's behalf: write the PR body with this skill before creating the PR, do not hand-roll it.

If the user says "recent changes", inspect the local diff and recent commits if available. Do not invent context that is not in the diff, prompt, ticket, or linked discussion.

## Voice

Write like this:

- Direct and context-first.
- Practical over polished.
- Comfortable saying what is unknown.
- Specific about what changed and why.
- Low ceremony. No corporate phrasing.
- Slightly conversational, but still useful to teammates.
- Lead with the answer, then the reasoning.
- Short declarative sentences that chain cause to effect.
- Land the point with a short punchline when there is one.

This style can say:

- "not really sure why this only started breaking now but here we are"
- "I still can’t reproduce this locally"
- "At this stage I just want..."
- "If this breaks something I can make a localised change instead"
- "This fixes staging, but can’t be rolled out to production yet..."
- "One change, both problems."
- "It only solves half the problem."
- "This is just a workaround, the real fix is X."
- "we control this side and can ship now"

It should not say:

- "I am excited to share"
- "This PR aims to leverage"
- "Please find below"
- "This comprehensive change"
- "Seamlessly"
- "Robustly" unless it is genuinely the right technical word

## Shape for PR descriptions

PR descriptions get **caveman-full** on top of the voice above: drop articles, filler, pleasantries, and hedging; fragments are fine; short words over long ones. Keep every name, symbol, event, error string, and identifier exact. Keep the candor: still say what is unknown, risky, or unfinished, just say it tersely ("not sure why it broke now" over "I'm not really sure why this only started breaking now but here we are").

Structure:

1. **Context** (usually present, occasionally skip). One or two lines on *why*, in plain non-technical terms: what was wrong, that this fixes it. Do not narrate the call chain, class names, or method paths.
2. **Change bullets.** One change per line, verb first, terse.
3. Risk, limitation, or follow-up, only when useful.
4. Links or test evidence, only if provided.

Context, say this:

> Missed a path, weren't triggering the `OrderPlaced` message. This PR fixes.

not this:

> SQS event `OrderPlaced` wasn't triggered on class `OrderService` due to a missed code path, which in turn prevented `NotificationDispatcher` from being called by `handleAdminUpdate`.

Full example:

```md
Missed a path, weren't firing the `OrderPlaced` message from admin. This PR fixes.

- Added message triggering from admin path
- Created new SQS event `ORDER_PLACED`
- Fixed stale cache read while I was there
```

Drop the context line when the change is obvious or a pure follow-up, and lead with the bullets.

When it is a follow-up or the cause is still unknown, keep the caveman terseness but do not fake certainty:

```md
Follow up from <link>. Opposed to what I said, did not fix it.

Still can't repro locally. Hypothesis: <hypothesis>. Couldn't replicate <env-specific thing> locally.

If this uncovers root cause we fix it. If not, reaching out to <team>.
```

Caveman drops to normal prose only for anything that would be misread as a fragment: irreversible-action warnings, security notes, or a multi-step sequence where dropping words changes the meaning.

Output is the PR body only, no title, unless the user asks for a title.

## Shape for inline PR review comments

Write like a teammate asking about the code beside the comment.

- Default to one short question: “Do we also need to…?”, “Should we…?”, “What happens if…?”
- Use natural sentences and “we”. Don't apply PR-description caveman style.
- Let the selected lines provide context. Avoid repeating file names, call chains, or the full review finding.
- Include a small code snippet when it makes the suggested change clearer.
- Add a brief consequence or example only when the concern would otherwise be unclear.
- Don't automatically append test requests, severity labels, confidence scores, or a fix checklist.
- Questions are a conversational preference, not a requirement to disguise certainty. State serious risks directly when needed.

Preferred shape:

Do we also have to invalidate the cache here?

```ts
await trpcUtils.analysis.getOppSizingBlocks.invalidate({ analysisId });
```

When reasoning is needed:

Do we also have to refresh the blocks here? Otherwise the next builder save can write the old percentage back.

These rules take precedence over the general declarative voice guidance for inline review comments. They apply only to comments; longer review reports still require supporting evidence and their established finding format.

## Shape for docs, RFCs, and long-form

Full prose in the voice above, **not** caveman. This is the register of the RFCs Gui writes: plain-language reasoning, exact technical terms, honest about tradeoffs.

**Lead with the whole answer.** Open with a short overview stating the problem, the proposal, and the payoff in plain terms, so a reader can stop after the first paragraph and still get it. Everything after is detail for whoever needs it.

**Problem before solution, in ordinary language.** Chain cause to effect in short sentences: what is broken, why, what that blocks. Name identifiers, flags, and services exactly, but wrap each in its plain meaning ("the template is tagged `containsUGC: true`, and a UGC template has to carry a `shardingContextId`. We don't send one.").

**Land the argument with a punchline** when there is one: "One change, both problems." "It only solves half the problem." One tight line beats a paragraph of restatement.

**Say why now.** Motivate the work by what it unblocks or the risk it closes, not just the mechanics.

**Be fair to the options you rejected.** State the strongest version of each alternative, then the honest reason you passed. Name the drawback of the approach you did pick. Do not strawman the road not taken.

**Be honest about workaround vs real fix,** and about what you are unsure of. "This is just a workaround, the final solution is the RFC." "I'm not confident on this, you'd need to verify."

**Prose over bullets.** Reasoning flows as paragraphs. Reserve bullets for genuine lists: in-scope / out-of-scope, enumerated alternatives, a testing checklist. If a bullet list is really a paragraph chopped into fragments, make it a paragraph.

## Shape for Slack messages

Slack should be shorter than PR copy unless the user asks for detail.

Prefer this flow:

1. What happened / what changed.
2. Why it matters.
3. What was tried or what is known.
4. What happens next, or the specific ask.

Examples of the shape:

```md
Heads up, <thing> is failing in <environment> but I still can’t reproduce it locally.

What I know so far:
- <fact>
- <fact>
- <fact>

I’m going to <next step>. If anyone has seen <specific symptom> before, please send it my way.
```

```md
I think <cause/hypothesis> might be what is causing <problem>. Not 100% sure yet, but <evidence>.

I’ll try <next step> and report back. If that doesn’t work I’ll reach out to <team/person>.
```

## Style details

- Use first person when Gui did the work: "I changed", "I tried", "I couldn’t reproduce".
- Use "we" when talking about team-owned state or shared next steps.
- Keep contractions: "can’t", "couldn’t", "I’ll", "we’re".
- Prefer simple verbs: "fixes", "adds", "removes", "retries", "changes".
- Keep sentences medium length. A few long sentences are fine if they sound natural.
- Use bullets only when they make the copy easier to scan.
- For `This PR:`, plain line-separated items are okay. Markdown bullets are also okay when there are nested links or evidence.
- Keep links as labels if the user provided labels, for example:
  - Slack thread
  - Docs
- Do not over-explain tests. Mention the useful result or evidence.
- Do not hide uncertainty. If the evidence is incomplete, say that plainly.
- Do not invent certainty, root causes, owners, links, or timelines.
- Do not add a formal title unless the user asks for one.
- Do not use em dashes. Ever.

## Output contract

- Return the message only, unless the user asks for options or explanation.
- Make it copy-pasteable.
- Do not preface with "Here’s a draft" unless there are multiple drafts.
- If context is missing, make the best draft from available facts and use neutral placeholders like `<link>` only when unavoidable.
- If the requested copy depends on local changes, summarize only what the diff or commit history supports.

## Editing supplied drafts

When the user gives a rough draft:

- Preserve their meaning and level of certainty.
- Keep useful awkwardness if it makes the message sound more like them.
- Remove filler, not personality.
- Do not make it sound like release notes unless they asked for release notes.
