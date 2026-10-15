---
name: writing-social-posts
description: Draft, sequence, and refine social posts — X threads and one-offs, Show HN submissions, LinkedIn posts. Covers launches, progress updates, technical notes, opinions, and amplifying someone else's work. Use when the user asks to write or refine a post, order a thread's posts and media, or check copy before it goes out.
---

# Writing social posts

Posting about work. The steps below run for any post; [By kind](#by-kind) says
what changes between a launch and a progress note. Render mechanics and layout
live in [`IMAGES.md`](IMAGES.md).

Start where the work is. Drafting from scratch runs 0→5. Ordering an existing
thread starts at 2. Refining finished copy runs 3→5. Checking copy that is ready
to go out runs the preservation gate in step 4, then step 5; reopen the wording
only for a verified clarity or correctness defect. After the post is live, run
[Postflight](#6-postflight).

## 0. Audience contract

Fill one line before anything else:

`[speaker/account] -> [primary reader] -> [person or product being discussed]`

It decides the person of the copy. Second person is right only when the
primary reader is the one the post describes; a founder writing to a
professional audience about a product's users writes those users in third
person. Do not assume the reader is the user because the post describes a
product. The Labelme v7.1 LinkedIn draft opened with customer-facing "you"
on a founder post and had to be redone; the contract there was
`founder -> technical LinkedIn readers -> Labelme users`.

Done when the line is written and the person of the draft follows from it.

## 1. Find the exemplar post first

Name a real post that already worked for something comparable, recent, from
someone this audience respects. Copy its **shape** — post order, sentence
lengths, where the link sits — and write your own words into it.

Check the project's own playbook first: if it names a prior post with the
same job, that self-exemplar beats an external one (same audience, same
voice). Otherwise ask the user for the exemplar post; they know whose posts
land with this audience.
Given a status URL, read the post with
`curl -s "https://cdn.syndication.twimg.com/tweet-result?id=<POST_ID>&token=a"` —
`x.com` itself is behind a login wall, and one call returns one post, so a thread
needs every link.

Drafting from a blank page reliably produces copy that reads as generated.
Drafting against a shape does not.

Done when you can point at a specific post and state in one line what structure
you are borrowing.

## 2. One post, one job

Name the single thing this post does before drafting it. Everything that does
not serve that job is load, however true it is.

For a thread, that means one job *per post*, and the order is an **objection
ladder** — each post answers the next objection the reader raises, in the order
they raise it. The git-hunk debut, as a worked example:

| # | asset | objection |
|---|-------|-----------|
| 1 | command table | what even is this? |
| 2 | demo video | looks like work |
| 3 | before/after still | what did that run actually do? |
| 4 | eval table | does it help? |
| 5 | (none) | how do I adopt it? |

For a quote post, treat the caption, attached media, and quoted post as one
composition with one job per layer. Before drafting or reviewing the caption,
inventory the claims the quote and media already carry. Let the quote carry
context it already states, the media carry new evidence, and the caption answer
the next unanswered objection. A self-quote can leave the what and how in the
original post, show the result in a before/after image, and use the caption for
why the change matters: "much easier to keep my bearings with several worktrees
open at once." A label like "before/after" has no job because the image already
says it.

Lead with whatever a practitioner can *get* without pressing play. For a
developer tool that is usually the command surface: it is self-evidently the
pitch, and it is the post people screenshot.

Done when every post or quote-post layer has one job you can state in a few
words, and each answers the next objection the preceding context raises.

## 3. Draft flat

One claim per sentence. State facts and let the reader supply the enthusiasm.
The numbers carry the post; a setup line before them is load.

For a build or progress post, consider a concrete three-to-five-word **theme
line** followed by a blank line and the explanation. It is a title, not another
claim: it lets a reader classify the post at a glance while the body carries the
problem and solution. Use it when it makes the topic faster to scan; skip it
when the opening sentence already does that job.

> Automatic Git worktree hierarchy
>
> I use Herdr with worktrees, but every checkout looked like a separate project.

Done when no sentence needs a second read to find its claim, and cutting any
remaining sentence would lose a fact.

## 4. Refine against the tells

Hunt these tells:

| tell | before → after |
|---|---|
| rhetorical question answering itself | "Does it hold up? Same agent, 8 tasks…" → "Here are the evaluation results. Same agent, 8 tasks…" |
| setup-then-reversal beat | "You don't type these commands. I don't either." → "This is how I use it." |
| symmetric pair restating the image | "Left is what sat in the working tree. Right is what got committed." → "The debug print stayed in the working tree. Everything else got committed." |
| meta commentary on the reader | "the same run as a diff, for anyone who didn't press play" → cut the clause |
| explanatory tail | "version-matched, so the agent always reads the current one" → "version-matched." |
| instructing the reader to work | "The harness is checked in, so rerun it" → "The harness is in the repo." |
| overclaim | "AI agents *can't* hand you reviewable commits" → "*won't*" — nothing stops them, they just avoid it |

Three structural checks beyond the line-level tells:

- **Copy that narrates its own image is load.** The image is labelled already,
  so the sentence carries the fact the picture proves but does not state.
- **A claim belongs in exactly one post.** "You don't type any of it" landed in
  two replies before one got cut, then showed up twice again in the LinkedIn
  draft.
- **A fix propagates across platforms.** `can't` → `won't` was right on X and
  left the LinkedIn copy overclaiming the same fact for an hour.

### Variants change structure, not words

When the user asks for variants, each one changes the job or the shape:
product observation, user narrative, technical mechanism, release-first,
minimal. A set that differs by synonyms prolongs the review without giving
the user a choice; reject it and regenerate.

### Complete is not exhaustive

"Go all in" and "don't hold anything back" mean: do not withhold a strong
fact for a hypothetical later post. They do not override one post, one job.
A fact that is true but off the story weakens it; cut it rather than
parenthesize it.

### Preserve authored roughness

The user's draft and writing samples are the source of truth for voice. Keep
casual lowercase, fragments, parentheticals, uneven rhythm, and asides when they
are clear and characteristic. Separate actual defects from details a copy editor
could polish; changing the latter can make a human post sound generated.

Final review is a **preservation gate**. Change wording only when it misstates a
fact, obscures the claim, or breaks the platform. Offer optional stylistic
alternatives separately. If the user prefers the rougher version, keep it and
limit the remaining review to mechanics.

Detector scores are noise on 60-word posts. Your own ear, read aloud, is the
instrument.

Done when each post has been checked against every tell row, all three
structural checks, and the preservation gate, one at a time.

## 5. Preflight

Mechanical, and worth running every time. Some of it is one `curl` away.

- Every link returns 200.
- Char count per post. Premium raises the ceiling; the fold is still ~280, so
  know which posts get a "show more".
- Alt text on every image.
- Anything the reader is meant to copy exists as **selectable text**, not only
  inside an image.
- Images measured, not eyeballed — see [`IMAGES.md`](IMAGES.md).
- Every claim traceable to something you can link.
- Shipping something installable: the install command resolves to the version
  being announced. Check the registry you publish to, not the tag — for PyPI,
  `curl -s https://pypi.org/pypi/<pkg>/json`.

Run this checklist silently. Report failed or unverifiable items, not every
successful check. When nothing blocks publishing, say the post is ready instead
of reopening settled stylistic choices.

Done when every bullet is checked against the real post, not assumed.

## 6. Postflight

Runs once the user supplies the live URL.

- Read the live copy; the live post is now authoritative over every draft.
- Confirm media rendered and the first comment (if planned) is there.
- Treat the live post as the preferred voice exemplar for future drafts from the
  same author, including its punctuation, capitalization, line length, and list
  style.
- Sync the project's post artifact to the live copy, URL, media, and comment
  when the project's rules authorize recording it.
- Do not reopen settled wording without a verified problem.

Done when the artifact and the live post agree.

## By kind

| kind | shape | opens with | media |
|---|---|---|---|
| launch | thread on the objection ladder | what a practitioner gets, per step 2 | every asset you have |
| launch, LinkedIn | single post: concrete observation or problem → mechanism or user effect → shipped proof | the observation, not the release | one native video or image |
| progress / build-in-public | single post | what changed since last time | one clip or screenshot |
| technical note | single post, or a short thread if it needs a diagram | the finding, setup after | code still, diagram, or none |
| opinion | single post | the claim itself, first line | none — media dilutes a take |
| amplifying someone else | single post | what you took from it | theirs, credited |

A launch is the kind that usually earns a full thread, and the ladder sets its
length. The rest default to one post, and a thread has to argue its way in.

## Voice

Match the author's punctuation and capitalization from their writing samples or
prior posts. Preserve omitted terminal punctuation in short lines and lists when
it is part of their voice. With no author sample, use period rhythm and sentence
case in replies. Use contextual lead phrases on links ("Code:", "Eval
harness:"). The post ends on its last claim — nothing tacked on after it, no
hashtag, thread emoji, or call to action.

## Platform mechanics

- **X** — a link with no media attached unfurls into a card; media suppresses it.
  In a launch thread the main post carries no link and the first reply carries
  the repo. Post a thread in one sitting so latecomers meet it finished.
- **Show HN** — the title must begin with `Show HN:`, which HN's guidelines
  require. Submit the URL alone, then post the prepared first comment
  immediately. Include the limitations section; it reads as confidence.
- **LinkedIn** — standalone, never a thread. Link placement is presentation,
  not a reach hack: one link in the body when click-through to one
  destination is the post's job; the multi-link bundle (release, exact
  install command, download) in the first comment when the body should stay
  on its story. Narrative register is fine here and wrong on X. The "see more" cut falls
  around 140 chars on mobile, so the first two sentences have to carry the whole
  hook; check what survives the cut, not just the total length.
