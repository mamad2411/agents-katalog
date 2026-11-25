---
name: user-documentation
description: Produces documentation for people who did not build the system and do not want to understand it: user guides, manuals, onboarding material, task instructions, help centre articles, FAQs and support-facing troubleshooting. Organised by what the reader is trying to do, in their vocabulary, not by feature. Use whenever the reader is not technical.
license: MIT
metadata:
  category: documentation
  version: 1.0.0
  depends_on: [document-core]
  outputs: [user-guide, task-index, glossary, support-article]
---

# User Documentation

The reader has a task, limited patience, and no interest in the system. They
arrived here because something did not work or was not obvious. Every choice
follows from that.

Governed by `document-core`. This skill adds the task model, the vocabulary
discipline and the specific ways documentation for non-technical readers
fails.

## 1. Tasks, not features

The organising unit is a task the reader can name before reading. Never a
feature, a screen or a module.

| Feature-shaped, wrong | Task-shaped, correct |
|---|---|
| Address management | Change where your order is delivered |
| Notification preferences | Stop receiving emails about someone else's orders |
| Account settings | Change the email address you sign in with |
| Export module | Download your invoices for your accountant |
| Permissions | Let a colleague see your orders without letting them buy |

The test: could the reader have typed this title into a search box before
knowing your product existed? If not, it is a feature name.

A second test, for the whole document: if a feature exists that supports no
task, either the task is missing or the feature is. Both are worth reporting.

## 2. Shape of a task article

```
Title            the task, in the reader's words
One line         what this achieves, and when you would want it
Before you start prerequisites, permissions, and anything irreversible
Steps            numbered, one action each, with what the reader sees
Result           how they know it worked
If it did not    the three or four things that actually go wrong
Related          the task they will want next
```

Rules:

- One task per article. An article covering three tasks is found by nobody
  searching for the second or third.
- One action per step. `Click Save, then enter your address and confirm` is
  three steps, and the reader loses their place in the middle of it.
- Every step says what the reader sees afterwards. Without it, they cannot
  tell a slow step from a failed one.
- Irreversible actions are flagged before the step, never after.
- Five to nine steps. More means the task is too big, or the product is.
- No step depends on a screenshot to be executable.

## 3. Vocabulary

The single largest cause of unusable user documentation is writing in the
system's words.

| Rule | Application |
|---|---|
| Use the reader's noun | invoice, not billing document entity |
| Where the interface has a label, quote it exactly | the button says Confirm, so the document says Confirm |
| Where interface and reader disagree, use both once | your invoices, called Statements in the menu |
| Gloss any unavoidable system term on first use, once | an API key, the password your accounting software uses to connect |
| Never two words for one thing | pick one, put it in the glossary, enforce it by search |
| Never one word for two things | if the product does this, say so and disambiguate every use |

Register: second person, present tense, active, imperative for actions. Not
formal, not familiar. `Select your country` beats both `The user must select
their country` and `Now just pop in your country`.

Banned outright: `simply`, `just`, `easily`, `obviously`, `of course`, `all
you have to do`. They tell a reader for whom it is not simple that the failure
is theirs. When a step is genuinely difficult, say what makes it difficult.

## 4. Screenshots and visuals

| Rule | Reason |
|---|---|
| The text is executable without the image | images break, go stale, and are not read by screen readers |
| An image supports a step, never replaces it | a reader who cannot see it must still be able to act |
| Crop to the relevant control plus enough context to locate it | a full-page screenshot shows nothing |
| Never put instructional text only inside an image | it is unsearchable, untranslatable, inaccessible |
| Caption every image with what it shows | not with what it is |
| Record the product version and date with each image | so staleness is detectable |
| Never show real personal data | use fictional data consistently across the whole document |

Screenshots are the highest-maintenance element in user documentation. Each
one is a promise to update it at the next interface change. Take that promise
consciously.

## 5. Failure content

The reader arrives after something failed. The section most often omitted is
the one they came for.

Per task, cover the three or four failures that actually occur, taken from
support tickets rather than imagined:

```
What they see       the literal message or symptom, so search finds it
Why it happens      in one sentence, without blame
What to do          concrete, and if it needs someone else, who
```

Error message text is quoted exactly, because that is what the reader pastes
into the search box. Paraphrasing it makes the article unfindable at the exact
moment it is needed.

## 6. FAQs

An FAQ is legitimate only for questions that are genuinely asked and belong to
no task. Most FAQs are a place where information went to avoid being
organised.

| Question | Belongs in |
|---|---|
| How do I do X | the task article for X, not the FAQ |
| Why can I not do X | the FAQ, if the answer is a policy or a limit |
| Is X secure, where is my data | the FAQ |
| What does X cost | the FAQ, or pricing |

Each answer is under a hundred words and links to the task article rather than
restating it.

## 7. Support-facing troubleshooting

A separate document from user-facing help, with a different index and a
different register.

```
Indexed by symptom, in the customer's words
Per entry: symptom, confirm it is this, cause, resolution, escalation threshold
Includes what the agent may not tell the customer, marked as internal
```

Never merge the two. The user-facing article must not contain internal
thresholds, workarounds requiring backend access, or known-defect notes.

## 8. Protocol

1. Load `document-core`. Build the audience profile. Set the output language
   to the reader's, from `language.document_output`.
2. List the tasks the reader wants to accomplish, in their words, from support
   tickets and search logs where those exist.
3. Discard every feature that maps to no task, and report it.
4. Fix the vocabulary before writing: one term per concept, in a glossary.
5. Write each task to the shape in section 2.
6. Perform every procedure in the product, in order, as a new user with no
   privileges. Correct what does not match.
7. Add the failure content from real tickets, with exact message text.
8. Have someone unfamiliar complete each task using only the document. Every
   hesitation is a defect in the document.
9. Run the eight-point gate. Add 9 to 11 when the deliverable is paginated.
10. Record the product version, the date and the invalidation trigger.

## 9. Auto-critique

Score 0 to 5: titles are tasks the reader could search for, one task per
article, one action per step, observable result per step, reader vocabulary
throughout, banned reassurance words absent, failure content taken from real
tickets with exact message text, procedures actually performed, text
executable without images, no personal data in examples.

Threshold: no axis below 3, average at least 4.

Automatic failure: a procedure never performed in the product, an article
titled after a feature, or an error message paraphrased rather than quoted.

## 10. Interfaces

- Upstream: `document-core`, `project-brief`, `ui-ux-engineering` for the
  interface labels and states.
- Downstream: `document-design`, `pdf-production`, `self-critique`.
- Related: `technical-writing` for readers who can run commands.
  `client-handover` embeds user documentation in a delivery package.
