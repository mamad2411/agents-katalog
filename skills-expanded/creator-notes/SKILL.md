---
name: creator-notes
description: >
  One private note per creator (how to work with them, reliability, results, deal
  history, next steps), so drafts start from real history. Use for "what do we know
  about <creator>", "update <creator>'s note", "log this call", "import my creators
  from this sheet", and when the inbox learns a fact worth keeping.
---

# Creator notes

One living note per creator: what anyone needs to work with that partner well.
The point is **continuity** - a creator should never have to re-explain their
lead-time needs, and a renewal should never be priced from memory. That is also
the boundary: the note exists to make the working relationship better, not to
build a profile of a person.

Other skills read it: `inbox-auto-draft-workflow` (personalising and pricing
replies), `negotiation-playbook` (Step 0 status quo), `rate-engine` (views, fee
history), `content-reviewer` (code, history).

## ⚠️ Read first: this is third-party personal data

Everything in this note is **personal data about someone who does not work for
you**, stored in your company's systems, readable by colleagues you have not
met, and retained long after the collaboration ends unless someone deletes it.
Treat it accordingly. This section overrides anything else in this file.

### The test that decides what goes in

> **Would you be comfortable if the creator read this note in full, today?**

If the honest answer is no, it does not go in. Not softened — out. That single
test resolves almost every case correctly, and it is a better guide than any
list, because it tracks the thing that actually matters: whether you are
recording something they shared with you, or something you worked out about
them.

### Appropriate to record

- **Professional context.** Channel, niche, formats, cadence, business model,
  their own products or courses, their team or manager, the platforms they are
  live on.
- **Stated working preferences.** "Prefers email to DMs", "needs three weeks'
  lead time", "does not do scripted reads", "publishes Thursdays". These are
  operational facts they told you so you would act on them.
- **Things the creator volunteered, in a professional frame.** They mentioned a
  house move that affects their filming schedule; they said they are taking
  August off; they mentioned they have kids and that school holidays shift
  their capacity. Record **the operational consequence** and, where it helps you
  be a decent person, the minimum context.
- **Commercial history.** Rates, terms, what was agreed, what went well, what
  they pushed back on. Quote their own words where the wording matters.
- **Reliability derived from your own delivery data.** On-time rate, typical
  slip. This is a fact about the collaboration, not about the person.
- **Publicly stated facts**, where relevant to working with them — and **mark
  them as public**, so the next reader knows the source.

### Not appropriate to record

- **Anything inferred rather than told.** If they did not say it, it does not go
  in the note. Deduced marital status, deduced financial pressure, deduced
  age — all out. **Inference about a person is the line.**
- **Health information.** Do not record a diagnosis, a treatment, a pregnancy,
  a mental-health disclosure, or anything about a family member's health — even
  when the creator volunteered it, and even when your intent is kindness. If a
  creator tells you they are unwell and need two extra weeks, the note says
  **"asked for a two-week extension in March; be generous with timelines"**, not
  the reason. The operational fact is what the team needs; the reason is theirs.
- **Anything in a special-category shape:** health, ethnicity, religion,
  political opinion, sexual orientation, trade-union membership, biometric
  data. There is no partnerships use case for any of these, and in most
  jurisdictions recording them carries a materially higher legal bar.
- **Children's details.** No names, no dates of birth, no schools. "Has young
  children, capacity drops in the school holidays" is operationally useful and
  sufficient. A child's name in a company CRM is not.
- **Third-party gossip.** What another creator said about this one, what an
  agency told you off the record, anything you would not say to their face.
- **Speculation about the commercial relationship dressed as fact.** "Probably
  struggling for money so will accept less" is both an inference and the kind of
  sentence that ends a partnership when it leaks. If you have a negotiation
  read, it belongs in the deal thread as an opinion with your name on it, not in
  an evergreen note as background.
- **Screenshots or pasted private messages** beyond the quote you actually need.

### Birthdays and gifting

Gifting is a legitimate relationship practice, and a birthday is the usual
excuse for it. Two conditions: **the creator gave you the date** (they told you,
or they filled it into your onboarding form — not "you found it on a fan wiki"),
and the field is used for that and nothing else. If you cannot source it, leave
the line as an explicit **"not on file — ask if it comes up"** gap rather than
filling it from the internet.

### How it is stored, and for how long

- Notes live in `~/.claude/inbox/creators/`, one file per creator, readable only
  by the user's account. If the team keeps them in a shared CRM instead, that
  company's retention policy and access rules apply.
- In most jurisdictions a creator can ask for a copy of everything you hold on
  them (a subject-access request), and this note is included. **Write every line
  expecting that.**
- **Delete the note when the partnership ends** and there is no live commercial
  reason to keep it. A note on a creator you stopped working with two years ago is
  pure liability with no upside.
- **A deletion or correction request is honoured, not negotiated.**
- **One copy.** Don't mirror notes into other docs, spreadsheets or chats. One
  place to find, one place to delete.

### If you are unsure

Leave it out and say so in your handback: *"the call also covered <topic>; I
have not written it into the note — tell me if you want a line about it."*
The user can always add it. You cannot un-write something a colleague has
already read.


---

## Where notes live

- **Default:** `~/.claude/inbox/creators/<handle>.md` - private files on the user's
  machine. `inbox creator <name|@handle|email|code>` finds one. The folder has an
  `_example-template.md` to copy.
- **Demo mode:** the fictional notes in the demo profile's `creators/` folder
  (`inbox profile-dir`). Never write to them.
- **Team CRM** (if `data-sources.md` names one and Claude can write to it): the
  same sections as one pinned note per contact, first line `PARTNER CONTEXT ::
  <name>` as the retrieval key. Every CRM write needs the user's explicit OK.

## The file format

Front matter (the lookup fields `inbox creator` searches), then sections:

```markdown
---
name: Maya Ortiz
handle: @mayacodes
email: maya@example.com          # plus any manager/agency address
platforms: youtube, tiktok
niche: study productivity
country: US                      # audience country if known
median_views: youtube=41000, tiktok=12000   # with a date in "Results" if you can
promo_code: MAYA30
status: test                     # test | continue | re-onboard | watch | cut | do-not-re-onboard
fee_history: 2 x youtube_integration at 1,160 (2026-10)
# plus the active modules' fields - each module file names its own
---

# Maya Ortiz

## How to work with them
## Release pattern and reliability
## Results so far
## Commercial snapshot
## Pushbacks and sensitivities
## Ideas they shared
## Personal (handle with care)
## Active / next steps          (prune as items close)
```

Keep it tight - a note nobody finishes reading doesn't work. **How to work with
them sits above the commercial snapshot**: the person reading at 9am before a
reply needs that first.

`status` drives renewals in `shapes/money-core.md`: `test` (first deal
running), `continue` (profitable, re-book), `re-onboard` (profitable, gone quiet),
`watch`, `cut` (the rate no longer works - recalibrate), `do-not-re-onboard`.
An exclusivity hold elsewhere is not a decline - note it as temporary with the
date it ends, or the creator gets filed as gone when they're re-approachable.

## Who may write what

| Change | Who decides |
|---|---|
| Facts from a thread during an inbox run: a new go-live date, agreed deliverables, a result they shared, a stated preference | the workflow writes it, and lists the change in the run report |
| A first-time note; an email, fee or status change (a run never makes one, however sure the thread sounds); anything under "Personal" or judgement-shaped | propose it; write only after the user says yes |
| A CRM note | always the user's explicit yes |

---

## Building a first-time note

1. **Read the whole history, not snippets.** Every thread with the creator, full
   bodies (`inbox search "from:<address> OR to:<address>"` finds every thread, read
   or unread). Search every address they've used: manager, agency, the
   whole domain. A keyword search is a locator, not a substitute for reading: the
   message you skip is the one with the paused deliverable, the exclusivity date or
   the boundary they set.
2. **Other sources with signal:** notes the user pastes, a call transcript (prefer
   the transcript over the auto-summary - summaries drop the throwaway line where
   someone explained *why*; speaker labels are often mis-mapped, so check who said
   what), a spreadsheet export, the user's own memory.
3. **Verify before you write.** Names, dates and numbers from a real source. Can't
   confirm -> write `not on file yet - confirm` rather than a guess. A visible gap
   gets filled; an invisible one gets guessed at by the next reader.
4. **Show the draft note, then save** (first-time notes are always approved).

**Importing many creators** ("here's my sheet"): one note per row with the
front-matter fields you can fill, sections left empty, status as the user gives it.
Show a summary table before writing.

## Reliability, honestly measured

On-time rate and typical slip come from comparing the **originally agreed** date
with the actual go-live. Watch the goalpost trap: dates often get revised after a
miss, so "on time versus the current estimate" can make a creator who slipped three
times look perfect. Record the original date when a slip happens ("Oct 3 -> moved
to Nov 5, second move"). Report the median slip, not just the mean.

No data -> write `not measured yet`, never an estimate. A guessed reliability figure
gets quoted back at a creator eventually.

---

## For other skills: reading a note

1. `inbox creator <name|@handle|email|code>` -> path(s).
2. Several matches -> pick by exact handle or email; still ambiguous -> ask or ⚠️.
3. Treat **Active / next steps** as live directives and everything else as
   background. Check dates: results older than the latest video are stale.
4. Act on it; don't copy its contents into other documents.
