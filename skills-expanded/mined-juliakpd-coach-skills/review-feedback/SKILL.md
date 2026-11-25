---
name: review-feedback
description: Turn a completed review's findings into feedback a colleague can act on — the reviewer picks what they stand behind, then it produces plain-language wording and 2-3 ranked delivery options. Use after context-review or any review that produced a findings document.
---

# Skill: Review → feedback

A review produces findings **for the reviewer**. Feedback is a different artifact for a different
audience: the person who wrote the thing. This skill does the translation.

Run it after a review skill has produced a findings document. Do not run the two together — the
reviewer needs to decide what they actually believe before anything is worded for sending.

## Guardrails
- **The reviewer owns the feedback, not the agent.** Never produce a sendable draft before they
  have picked which findings survive. They are putting their name on this with a colleague.
- **Read-only toward the reviewed repo.** This skill writes feedback documents. It does not open
  PRs, post comments, or push. A human sends.
- **No invented authority.** If a finding was a judgment call, it says so in the feedback. Do not
  launder an opinion into a verdict.

## Step 1 — separate what's tested from what's judged
Go through the findings and sort each into one of three buckets. Show the reviewer the sorted list
and ask them to confirm or move items. Do not skip to wording.

- **Verified** — checked against the files. "This path is referenced in 6 places and doesn't exist"
  is verifiable; say how it was checked so it can be re-checked.
- **Judgment** — a defensible opinion with no test behind it. Most longevity and structure findings
  live here. Mark them as opinion in the feedback; that is what makes the feedback trustworthy.
- **Dropped** — findings the reviewer doesn't stand behind, or that Step 0 of the review invalidated
  (e.g. a layer-mismatched privacy flag). Record these with a one-line reason. Being explicit about
  what was considered and rejected is a large part of why feedback gets taken seriously.

## Step 2 — check the premise before sending
- Does the reviewer understand what the repo is **for**? If not, that is the first thing to send —
  as a question, not a finding. Structural criticism built on a guessed purpose will be wrong and
  will read as careless.
- Would the author be surprised by any finding in a way that means the reviewer misread something?
  Name the assumption in the feedback so they can correct it cheaply.

## Step 3 — rank by what the author should do first
Order by *cost of not fixing it*, not by how interesting the finding is. Group into:
- **Would fix now** — cheap, clear payoff.
- **Worth deciding** — a real trade-off; present the options, don't prescribe.
- **Noted, not blocking** — say it once, don't argue for it.

Three to five items total. A long list reads as an audit and gets defended against rather than used.

## Step 4 — rewrite in the author's language
Strip the reviewing vocabulary. "Altitude", "progressive disclosure", "always-on budget",
"provenance" mean nothing to someone who didn't read the skill. Say what breaks and when.

- Bad: *"Progressive disclosure is violated; always-on context is unbounded."*
- Good: *"Every rule loads every time, so it'll get slower and noisier as you add notes. Worth
  splitting the rarely-needed ones out."*

Describe behavior and consequence. Attribute to the file, never to the person: "this file says X",
not "you did X".

## Step 5 — produce the delivery options
Give the reviewer **2–3 ranked options** with a recommendation and the trade-off, not a survey:

- **PR with inline comments** — best when findings are file-specific and small. Highest signal,
  lands where the fix happens. Costs the most to prepare.
- **One issue with a prioritized list** — best when findings are structural or need discussion
  before anyone edits. Easiest for the author to triage and reply to.
- **Message + the review document attached** — best when the relationship is informal, the repo is
  someone's WIP, or the reviewer wants a conversation before anything formal. Lowest friction,
  easiest to ignore.

Say which one fits *these* findings and why.

## Step 6 — the method block (always include)
Feedback that doesn't say how it was produced is hard to trust and impossible to re-run. Close with:

- What was reviewed (repo, commit/date) and with what skill.
- What was actually checked versus judged — carry the Step 1 buckets through.
- **What was not verified**, plainly. Missing linters or CI mean integrity claims are judgment;
  say so rather than letting confident wording imply testing that didn't happen.
- That an AI-assisted review produced the draft and a human reviewed it. Do not hide this — it is
  also what makes the approach shareable with others later.

## Output
Write to `reviews/<repo>-feedback-<date>.md`:
1. **The question(s)** for the author, if purpose was unclear — first, before criticism.
2. **Would fix now / Worth deciding / Noted** — the ranked items in plain language.
3. **Considered and dropped** — with reasons.
4. **Delivery options** — ranked, with the recommendation.
5. **Method block.**

Keep it shorter than the review it came from. If it isn't shorter, it hasn't been translated.
