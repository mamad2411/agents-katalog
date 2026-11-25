---
name: use-personal-data
description: >
  How this project holds data about PEOPLE — names, contacts, documents, health, anything that
  identifies someone — and what may cross the border to a model provider. Load it BEFORE designing
  any table that will hold a person, any support or medical feature, any AI call whose input comes
  from a user's own words. Also load it when the owner says "the data may not leave the country",
  "this is medical", "GDPR", "personal data", "we may not send that to OpenAI". The rule the whole
  skill turns on: the model receives the CASE, never the PERSON — the two are separate tables, and
  they are joined again only on the owner's own server, after the answer comes back.
---

# use-personal-data

> Informational, not binding. **Know a better way for the case in front of you — do it your way and
> say so.** You are trusted with the creative work on this project.

The starter puts a real database on the owner's own machine, and the moment a table starts holding
people rather than products, one question outranks every other design question:

> **What is allowed to leave this server — and what must be rejoined here, after the answer returns?**

Everything below is one answer to that question, applied to the cases that actually come up.

## The structural rule: two tables, one join, and the join happens here

A person and their case are not one row. Split them the day the table is created, not the day a
regulator asks:

| Table | Holds | May it leave the server? |
|---|---|---|
| `<entity>_people` | name, contact, document number, address, date of birth | **never** |
| `<entity>_cases` | `person_id`, the question, the state, the outcome | only pseudonymously, and only the fields the model needs |

The outbound door sends `person_id` — an opaque identifier that means nothing outside this database
— plus the minimum the model must read to be useful. The provider answers keyed by that same
identifier. **The route joins the answer back to the person here**, on the owner's hardware, and
only the joined result reaches the screen.

Both tables are declared in **one place**: the `SCHEMA` constant in `lib/db/index.ts`. Local SQLite
and the remote data service both execute it at startup, so a table added there exists in both
environments without a migration file.

The identifier must be **meaningless**. `p_8f3c…` is an identifier; `ivanov_1978` is personal data
wearing a costume, and an email address is personal data with no costume at all. If the value could
be recognised by someone who never saw your database, it is not pseudonymous.

## Case 1 — the state forbids personal data leaving its borders

The requirement the owner named, and the reason this skill exists. The law does not forbid using a
model; it forbids **exporting the person**. Those are different prohibitions, and the second one is
satisfiable.

What the outbound door sends:

```
{ caseId: "c_41d9…", personRef: "p_8f3c…", question: "…", locale: "ru" }
```

What it must never send: name, contact, document, address, employer, exact date of birth, or the
raw text of anything a person wrote about themselves before it has been read (Case 2).

What comes back is keyed by `caseId`. The route looks the person up locally, composes the reply
with their name in it, and answers. The person's name existed on this server the entire time. From
the provider's side there was a case, and no human being.

**The line to hold in review:** point at the exact object handed to `fetch`. Not the function that
builds it, not the type — the value that goes over the wire. If a name can reach that object through
any branch, the design has not been done yet.

## Case 2 — free text is where the leak actually happens

The hardest case, and the one that defeats a careful schema: **support written by a human**.

A ticket body reads *"I'm Maria Petrova, my insurance card is 4412…, my son's rash started Tuesday."*
The `name` column is clean. The table is split. The identifier is opaque. And the person went abroad
anyway — inside a sentence, in a column nobody classified as personal.

So free text has its own rule: **a field a person composed themselves is untrusted until it has been
read.** Three honest options, in the order they should be considered:

1. **Do not send the body.** Send the structured case instead — category, symptom codes, dates —
   which the interface collected as fields rather than prose. Most support flows can be redesigned
   this way, and the redesign is cheaper than the compliance argument.
2. **Scrub, then send** — strip what a scrubber finds, and mark the record as scrubbed. Understand
   what you bought: a scrubber catches patterns, not the sentence *"my mother works at the school on
   Lenin Street"*. Scrubbing lowers the volume of the leak; it does not close it.
3. **Send it and accept the export.** A legitimate choice in a jurisdiction that permits it, but it
   must be the owner's explicit decision, written down where the next session will find it — not a
   default that arrived because nobody looked at the payload.

Never present option 2 as if it were option 1.

## Case 3 — health data, and why "special category" is not a synonym for "sensitive"

Health, biometrics, religion, ethnicity, sexual life, political opinion and criminal record are a
separate legal class in the EU and most of its imitators: the default is that processing them is
**prohibited**, and permission has to be earned — by explicit consent, or by a professional duty of
care. This inverts the usual habit. Elsewhere you ask "is anything forbidding this?"; here you ask
"what specifically permits this?"

Three consequences for the build, all structural rather than procedural:

- **Consent is a row, not a checkbox.** Store what was consented to, when, in which wording version,
  and how it can be withdrawn. A boolean `agreed = 1` answers none of the questions that get asked
  later, and the questions get asked exactly when the answer matters.
- **Health facts and identity are never in the same table**, even locally. The join above is what
  makes "who has this diagnosis" a query that has to be written deliberately, rather than a column
  anyone reading the table sees by accident.
- **Role gates are per route, and health routes are their own group.** `lib/roles.ts` holds the
  vocabulary, `lib/auth/require-roles.ts` enforces it in the door, and the subgroup `layout.tsx`
  stands in front of the pages. A health feature dropped into an existing group inherits that
  group's audience, which is almost never the audience it should have.

The support scenario the owner named — technical support about a person's health — is Case 1 and
Case 2 and Case 3 at once. That combination is the normal case, not an unlucky one.

## Case 4 — the doors you will forget: vector memory and the knowledge graph

The storage is local. **The ingest is not.**

`lib/fractera/vectors.ts` and `lib/fractera/knowledge.ts` keep their data in the owner's own data
service — and to store it they send the text to the model provider to be embedded or read for
entities. Putting a support ticket into vector memory exports it just as surely as a chat call does,
while looking like a database write.

The knowledge graph is worse on this axis and better on another: loading is where the model reads
**everything**, so a corpus loaded once is a corpus exported once, in full. Asking afterwards is
cheap. Decide what may be loaded before loading anything.

## Case 5 — the four channels nobody classifies

Personal data leaves through more doors than the ones marked "API":

- **Logs.** A route that logs its request body on error has published every field it received. Log
  identifiers and status codes; never the payload.
- **Error text on screen.** A refusal that echoes the input to be helpful — "no patient found for
  Maria Petrova" — puts the name into a screenshot, a support chat, and a bug report. Refusals live
  in `lib/i18n/platform-errors.ts` and are written once, in general terms, on purpose.
- **URLs.** A query string lands in server logs, browser history and any referrer header. Identifiers
  in the path, data in the body — always.
- **Prerender and cache.** The protected layer is static shell plus dynamic holes precisely so a
  person's data is never baked into a prerendered page. Fetching personal data in a server component
  of a cached route bakes one visitor's data into the page every later visitor gets.

## Case 6 — erasure, decided at schema time

Every regime that regulates personal data grants deletion. Whether that is one statement or a week
of work is decided by the schema, months earlier:

- Person in their own table, referenced by opaque id → erasure is one `DELETE`, and the case history
  survives as anonymous statistics, which is usually both legal and desirable.
- Person's name copied into every case row, and into logs, and into the vector store → erasure means
  rewriting all of it, and the copies in the model provider's systems are not yours to delete at all.

The second shape is what a starter's convenience produces by default. Refuse it when you build the
table, because that is the only cheap moment.

## Where these doors are in this project

Three routes reach a model provider, all server-side, and the key never enters a browser
(`lib/openai-key.ts` is the single reader):

| Door | Sends | Watch for |
|---|---|---|
| `app/api/i18n/translate` | the record's fields | translating a person's own words exports them |
| `app/api/transcribe` | recorded speech | a voice is biometric in several regimes, and people say their name out loud |
| `app/api/openai-models` | nothing but the key | safe, listed for completeness |

Anything else that leaves is code somebody adds. Add it as a route with an `@api` line, never as a
`fetch` inside a component: a door that is not a route is a door nobody can review, and the browser
would carry the key.

## When the honest answer is "not here"

Sometimes the requirement is that the model reason **over identified data** — read the medical file
as a whole, with the name — and the law forbids that data leaving. Then pseudonymisation does not
save the design, and saying so early is the service:

- a model running on the owner's own server, or with an in-country provider, or
- the feature without AI on that field, or
- the feature with AI on the non-identifying part only, which is usually most of the value.

Naming the choice is the work. Quietly shipping option four — export it and hope — is the failure
this skill exists to prevent.

## Proof

Types being green proves nothing here; the payload is the only evidence. Prove it the way a
regulator would:

1. Put a recognisable synthetic person in the database — `Zzz Testovich`, `+7 000 000 0000`.
2. Run the feature end to end with the browser's network panel open (Claude's Chrome extension reads
   it — see `use-browser` when that skill exists).
3. Search **every outbound request body** for `Zzz`. One hit is a failed design, not a small bug.
4. Negative control: confirm the same string IS present in the local database and in what the person
   finally sees on screen. If it is absent from both, you did not test the path you think you tested.
