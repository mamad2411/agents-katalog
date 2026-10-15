---
name: document-what-shipped
description: 'Write and publish ONE documentation page about something that already ships - a user manual, a process and flow page, a release note, a runbook, or a rules page - with every fact measured on the running system, to any destination: an Azure DevOps wiki, a GitHub wiki, a repo docs folder, or a plain markdown folder. Slash-only. Not for a single bug write-up (post-mortem), not a full SA and D document (sa-doc), not a status message (management-talk).'
disable-model-invocation: true
---

# Document what shipped

A decided design is not a shipped one. That sentence is the whole skill, and it is in the name
because it is the thing a session forgets at exactly the wrong moment - when a decision record,
a plan or an ADR describes the behaviour so clearly that reading the running system feels like
a formality.

It is not a formality. The draft this method replaced said the reject link *"asks for a reason
from a short list and closes the quote as lost"*. True in the decision record. Untrue in the
product: the link opened a page saying an Agent would be in touch, and closed nothing. Two more
claims in the same draft were false the same way, and one claim written by the agent doing the
measuring was false too - *"nothing notifies the Agent"*, written after reading the C# only,
while a CRM workflow had been sending that email all along, 16 seconds after the press.

So the deliverable is not a document. It is **one page whose every sentence a person can check**,
plus the record that says how each sentence was checked.

```
  ONE RUN = ONE PAGE
  ─────────────────────────────────────────────────────────────
  ⓪ FOUR ANSWERS      type · reader · system+environment · destination
  │                   any one missing → ask, do not assume
  ▼
  ① SHOT LIST         numbered pictures the page needs
  │                   gate opens ONLY on files, or a plain "no images"
  ▼
  ② FACT LEDGER       every fact × three places · live journey first
  │                   no place answers it → it is NOT BUILT, not a sentence
  ▼
  ③ DRAFT             one page, one spine, holes visible
  ▼
  ④ SNAPSHOT          live page + version token, before any write
  ▼
  ⑤ HAND OVER         and STOP. Only the owner says publish
  ▼
  ⑥ PUBLISH           If-Match / fast-forward · read back · probe
  ▼
  ⑦ PROVE IT          resolve EVERY link · publish record · one ticket comment
```

---

## ⓪ Four answers before anything is read

Ask all four at the start, in one message, and wait. Each one changes what gets measured, so
guessing any of them means measuring twice - and the second pass happens after a draft exists,
which is when measurement gets skipped.

| answer needed | how to ask it | if it is missing |
|---|---|---|
| **Which type of page?** | offer the five spines by the reader's question, plus *other* | ask. Never infer from the request wording |
| **Who reads it?** | propose from the type and destination: *"Reader: management, on the GlassHull wiki. Correct?"* | ask |
| **Which system, which environment?** | name the product and the environment you will measure | **stop.** See ① below |
| **Where does it get published?** | name the destination and the parent page | ask |

Read `references/page-spines.md` for the five spines and their sections, and
`references/register.md` once the reader is named.

**An unnamed environment stops the run.** Not a caveat banner - a stop, with a question. In this
repo the trunk carries 390 of the tree's frontend and api files while the delivery ref that was
actually deployed carries 753, so "the code" is not one thing and a page written from the wrong
one describes a product that does not exist. A manual whose subject cannot be identified cannot be
re-checked by anybody, including you next month.

**The type may be one the five spines do not cover.** Then take *other*: ask for the reader's
question, propose a spine from it, and at the end of the run **write that spine into
`references/page-spines.md`** marked unproven. A type answered once should never be improvised
twice.

---

## ① The shot list, before the draft exists

Hand over a numbered list of the pictures the page intends to show - one row per step, saying what
each picture must contain. "Do you have screenshots?" is not answerable; this is.

```
  1. the Send dialog, showing the voyage list and the Send button
  2. the email as the customer receives it, showing one button per voyage
  3. the confirm page, showing the vessel and the departure date
```

**The gate opens only on an explicit answer.** Files handed over, or a plain *"no images"* /
*"the diagram is enough"*. Silence, "later", "maybe", and simply moving on to another instruction
all leave it closed - ask once more. An absent answer is not a decline.

**Once the files are handed over, read them through `read-picture`.** Load the `read-picture`
skill via your harness's mechanism, asking kind `on-screen-text` for the words this page will
quote - button labels, page titles, status names. It answers from the project's picture record
when that picture has already been read for the same question, and opens the image when it has
not. Carry its not-re-checked flag into ② - a row whose bytes could not be confirmed is not
evidence for a sentence on a published page.

**A diagram may replace a picture, and it does not replace what the picture proved.** A screenshot
is evidence the thing exists and carries the exact words on the button; a diagram shows order,
branch and state, and proves nothing about what shipped. So when a step is covered by a diagram
instead:

- quote its on-screen names - button labels, page titles, status words - from the **measurement**,
  never from memory, because the picture that would have caught a wrong label is not there;
- make sure the diagram actually carries **that step**, not merely sits near it.

**A step with neither stays a visible hole in the draft**, written as a line on the page:
`> Screenshot needed: the Send dialog showing the voyage list.` Recording the gap in a side file
is what happened before, and no reader of a wiki opens the side file - a thin section reads as a
complete one.

---

## ② The fact ledger - every fact, three places

For each fact the page will state, read all three places that can answer it:

| place | what it answers | how it lies |
|---|---|---|
| **authored code** | what we wrote | it is silent about everything the platform does for us |
| **the platform's own automation** | workflows, plug-ins, triggers, jobs, rules, integrations | a sweep of one storage column misses a whole family - reading only classic definitions missed 129 cloud flows whose definition lives elsewhere |
| **a live observation** | *does this ship* | it is a sample. One run does not prove the second branch |

Every fact. Not only the ones that look doubtful - the false claims all looked correct to their
author. Where a place cannot answer a fact (a button label has no automation behind it), write
**not applicable**; never skip it silently, because a skipped place and an absent place look the
same in a week.

Two mechanisms keep this affordable, and without them the run stalls before the draft:

1. **Plan one live journey and take it end to end first.** Yesterday a single real quote proved
   about ten facts in one pass - the link, the confirm page, the won quote, the booking in
   Planning, the notification email at 16 seconds, the second press, the log row. Read the code
   and the automation *against what the journey produced*, not before it.
2. **Cache platform state, decide from a fresh read.** Save each live query with its result count
   and newest modified date, so staleness costs one cheap call next time. A cache orients; it never
   decides. Re-pull any fact in the session that puts it on the page.

The ledger is one row per fact - the fact, the places that answered, the date - and it is what
makes the page auditable without re-reading the system.

**A fact no place answers is not a sentence.** It goes on the *not built yet* list, in the page's
own words, or it is dropped. An entire reject flow went that way and the page is better for saying
so.

---

## ③ Draft one page

One run publishes **one** page. A companion page is a second run, with its own shot list and its
own measurement pass - and by then the first page exists, so the link between them is written
against a path that has been read rather than guessed.

Follow the chosen spine from `references/page-spines.md`. Three things belong on every page
whatever the spine:

- **The provenance line**, in the reader's words: *"live on the development environment since
  20 August 2026, proven on a real quote"*. Where and when and proven-or-not is what a reader can
  act on. The ref, the build number and the queries go in the record - a branch name on a
  management page is noise that goes stale one deploy later while the sentence around it still
  reads as current.
- **A *not built yet* section**, when anything decided is unbuilt. Name it plainly, including what
  the reader should do instead until it ships.
- **The exact on-screen words**, kept as the product spells them - button labels, page titles,
  status names. Everything else obeys `references/register.md`, which bans identifiers the chosen
  reader cannot act on.

**No credential reaches the page.** A signed accept link is a credential for the quote it names.
It stays out of the page, out of the record, and out of the commit. This one does not bend for any
reader.

Write the draft into the run's record folder: the repo's existing home for such records if it has
one, otherwise `docs/published/<date>-<page-slug>/`. Ask only when two candidates exist. The
folder lives in the repo you run in, even when the product lives elsewhere.

---

## ④ Snapshot, then edit where the page came from

Before any write to a page that exists, fetch it live into `<page>-before.md` **with its version
token** - the `ETag` in an API page store, the commit in a git file store. This is not extra work:
it is the generator's input, it proves the anchors still match what the destination serves right
now, and it is what turns a bad publish into one restore command. Record the token; the write
replays it (`If-Match`, or a non-fast-forward push refusal) so a concurrent edit is refused rather
than overwritten.

Then edit **where the page came from** - the publish record names its origin:

| origin | how to edit it |
|---|---|
| a generator script | change the **script**, re-run it, and never touch its output |
| a person | one surgical edit, with an assert that the anchor text appears exactly **once** |
| unknown | treat as a person's page |

`scripts/anchored_edit.py` carries the four habits that make either safe: find a place by its own
text, assert the text is unique, apply edits from the bottom of the file upward so earlier edits
cannot move later anchors, and probe the result.

**Then read the produced prose.** Asserts prove an anchor matched; they cannot prove a sentence
reads. A patch that replaced one line of a two-line sentence passed every assert and published
*"the Agent clears it with Add Booking, and the quote-list marker and the Agent clears it with
Add Booking"*.

---

## ⑤ Hand over, and stop

The run stops at the draft. Publishing is the only step other people see and it cannot be undone
quietly - a wiki push is live the instant it lands. Hand over five things, so the decision is one
glance:

1. the page title and the full destination path the write will use;
2. the parent page to be edited, and the single line to be added there;
3. the attachment names, when there are images;
4. what the draft deliberately leaves out - the not-built list, and any fact no place answered;
5. the internal links that cannot be checked yet, because they only resolve once the page exists.

Then wait. **Only the owner saying *publish* starts ⑥.** Not a passing "looks good", not a green
check.

**A task that names the destination is not authorisation to publish.** "Put it in `wiki/` as
`Customer-accept.md`, and the parent must link to it" describes the write; it does not approve it.
The same is true of a deadline, of a path handed over in the brief, and of a destination you were
given credentials for. Measured in this skill's own test: an agent following this method read a
named destination file as pre-approval and published without being asked. Write the hand-over,
then wait for the word.

**Count the hand-over's numbers off the draft**, never from memory - how many holes, how many
links, how many unobserved claims. The same test produced a report claiming six screenshot holes
on a page carrying three.

---

## ⑥ Publish

Read `references/destinations.md` and answer its eight questions for this destination **before**
the first write. If the destination is not one of the measured adapters, discover it live, publish,
and write the measured recipe back into that file in the same run - an adapter is measured or it
does not exist.

The protocol is the same in both families:

1. re-fetch the live page and compare it against the before-snapshot. Different? Re-run the
   generator against the new content; do not merge by hand;
2. write, carrying the version token;
3. read the page back and check a probe list - sentences that must be present, and sentences that
   must be **gone**;
4. edit the parent so the new page is reachable. A page nothing links to is not published, it is
   uploaded. One-way navigation was the default failure.

Mermaid fences differ per destination (`::: mermaid` on an Azure DevOps wiki, a triple-backtick
fence on GitHub). The fence belongs to the destination, not to the writer.

**Parse every diagram before the write.** `scripts/check_mermaid.py` does it, and nothing else in
this method can: the read-back probes check sentences, the link check checks links, and a diagram
that does not parse renders as an error box while both pass. Measured 2026-08-21 - a sequence
diagram published on 20 August contained

    CRM-->>Portal: Quote closes; chosen schedule recorded

and had never rendered once. A **semicolon terminates a statement** in mermaid, so the tail became a
new statement and the parser demanded an arrow. Two runs went past it, both with every assert green,
because no assert either run made was about the diagram. A `#` in a label fails the same way.

The same run found the diagram was *also* factually wrong - one branch covered both a customer
accepting and a customer rejecting, then flowed into "create booking", so it told readers a
rejection creates a booking. Fixing only the parse error would have left a diagram that renders and
lies, which is worse than one that fails loudly. **When a diagram fails to parse, re-read what it
claims before you fix the syntax** - a diagram nobody could render is a diagram nobody proofread.

---

## ⑦ Prove it, then record it

**Resolve every internal link on every page you touched, against the live destination.** Not the
new page only - the parent too. This is `scripts/check_links.py`, and it is the step that has
caught the most: a dead link looks exactly like a page that was never created, and a parent that
links to none of its children looks exactly like a parent that does.

Then write, in this order:

- the **publish record** beside the draft: version token before and after, size change, the probes
  checked, the link-check result, and the page's origin so the next edit knows where to go;
- **one comment on the ticket**, when the task came from one: the page link, the token before and
  after, what is still not built, and the link-check result. After the publish, never before - a
  comment written at draft time claims a published page while the page is still a file on disk;
- **commit** the record folder in the same run. An uncommitted record dies with the session, and
  the next run re-pays the whole fact gate.

---

## What this skill refuses

- **To publish without the owner saying so.** Draft, record, hand over the paths, stop.
- **To document unbuilt behaviour as working**, however clearly a decision record describes it.
  It goes on the not-built list or it is left out.
- **To trust a document about the product** - including its own earlier draft, and including its
  own summary of what it measured an hour ago.
- **To hand-edit a page a generator produced**, or hand-merge when the generator can be re-run.
- **To put a credential on a page**, in a record, or in a commit. A signed link is a credential.
- **To publish a diagram nobody parsed.** It renders as an error box and every other gate passes.
- **To write a page whose environment nobody can name.**

## Red flags - stop and go back a phase

| thought | what it means |
|---|---|
| "The ADR describes this precisely, I can write from it" | you are documenting a decision, not a product. Go to ② |
| "The code clearly does not do X" | code silence is not product silence. Read the platform automation and the live record |
| "There are no screenshots, I will describe it in words" | ① is closed. Ask, or take a plain "no images" first |
| "One page plus a diagram page is tidier" | two pages is two runs. ③ |
| "The asserts passed, publish it" | asserts do not read sentences. ④ |
| "The link is obviously right" | the last obviously-right link answered *Page does not exist*. ⑦ |
| "The diagram looks correct" | nothing in review renders it. Parse it - ⑥ - then re-read what it claims |
| "The brief already told me where to put it" | that is the path, not the permission. ⑤ |
| "I will record it all at the end" | an interrupted session leaves the round trips paid and nothing to show. Write each fact as it is measured |

---

## Related skills

- `management-talk` - the tone rules for a management reader. Use its register section; ignore its
  channel shapes, because this output is a durable page, not a message.
- `guide-and-verify` - the sibling for work a person must do by hand in a console. Same
  measure-before-and-after habit, different deliverable.
- `post-mortem` - one fixed bug, engineer readers. If that is the request, this is the wrong skill.
- `sa-doc` - a full SA and D document from one validated model. Also not this.
