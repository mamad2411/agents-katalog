---
name: read-picture
description: 'Answer one named question about one or more picture files, and record the answer so no run and no other skill re-reads the same image to reach the same sentence. Use when another skill or the user hands over screenshots, ticket attachments or exported images together with a specific question about them - the exact words on a control, or what an annotated picture requires. Not for generating or editing images, and not a full transcription: it answers the question it was given and records nothing else.'
---

# Read a picture

The answer to a question about a picture is a measurement, and this repo throws exactly
one class of measurement away: the one that came from looking. A ticket whose description
is a single annotated screenshot decided that a hardcoded label was a requirement rather
than a bug — and every later run re-downloaded and re-read that same picture to learn the
same sentence.

So this skill reads the picture **once per question**, writes the answer down, and hands
rows back. It is a reader, not a store: the caller passes paths and a question, and gets
facts (ADR 0135).

```
  ONE CALL = ONE QUESTION, N PICTURES
  ──────────────────────────────────────────────
  ① THE QUESTION      a kind from the named set
  │                   plus the caller's detail
  ▼
  ② LOOK IT UP      hash the bytes, ask the record
  │                   hit / candidates / no-answer
  ▼
  ③ READ ON A MISS    open the picture, answer ONLY
  │                   the question, append one line
  ▼
  ④ HAND BACK       rows, plus hit and miss counts
                      and any not-re-checked flag
```

## ① Take the question as a kind, plus detail

The record is keyed on the picture's bytes **and** the question, so the question has to be
a name from a set rather than free prose — two skills phrasing the same need differently
would otherwise never share an answer, and nothing would report the miss (ADR 0138).

```bash
python "${CLAUDE_SKILL_DIR}/scripts/picture-record.py" kinds
```

The set and what each kind means live in
`references/picture-record-contract.md`. Read it before choosing.

**If no kind fits, take `other` — and add the new kind to that contract's table in this
same change.** A question answered once should never be improvised twice.

Under the kind, state the caller's **detail**: what specifically is being asked ("the words
on the primary button in the Send dialog"). The detail is part of the key.

## ② Look it up before opening anything

```bash
python "${CLAUDE_SKILL_DIR}/scripts/picture-record.py" lookup \
    --file "<image path>" --kind <kind> --detail "<detail>" --json
```

Three outcomes, and only one of them lets you skip looking:

| outcome | what to do |
|---|---|
| `hit` | Use the stored answer. Do not open the picture. |
| `candidates` | Rows exist for this picture and kind, but none answers *this* detail. **Read the candidates, then default to opening the picture.** |
| `no-answer` | Open the picture. |

**A near-miss is a miss.** A stored row about the page title does not answer a question
about the confirm button. Serving it anyway manufactures the failure
`generating-test-cases` names — a value that is genuinely sourced but is the *class*
rather than the *instance*, which slips the source check precisely because it looks
verified. When the candidate does not plainly cover what was asked, read the picture.

**When the bytes are gone** — a temp download that was cleaned up, an attachment nobody
can re-fetch — look up by source instead of by file:

```bash
python "${CLAUDE_SKILL_DIR}/scripts/picture-record.py" lookup \
    --source "<url or original path>" --kind <kind> --detail "<detail>" --json
```

That result comes back with `bytes_verified: false`. **Carry that flag to the caller.** A
row nobody can re-check looks exactly like one verified a minute ago, and the caller about
to quote it onto a published page has to be able to see the difference (ADR 0139).

## ③ On a miss, read the picture and answer only what was asked

Open the image and answer the question. Then record it:

```bash
python "${CLAUDE_SKILL_DIR}/scripts/picture-record.py" append \
    --file "<image path>" --kind <kind> --detail "<detail>" \
    --answer "<the answer>" --asked-by "<calling skill>"
```

**When the bytes came from somewhere that will not last** - a ticket attachment
downloaded to a temp path, the case `ticket-trace` hits on every run - pass `--source`
too, so the record keeps the durable identity rather than a path that is gone by
tomorrow. `--file` still supplies the bytes to hash; `--source` supplies what the row
is found by later:

```bash
python "${CLAUDE_SKILL_DIR}/scripts/picture-record.py" append \
    --file "<temp download path>" --source "<the ADO attachment URL>" \
    --source-kind ado-attachment \
    --kind requirement --detail "<detail>" \
    --answer "<the answer>" --asked-by "ticket-trace"
```

**Record only the answer.** Not the customer name that happened to be on screen, not the
quote number, not the rest of the window. A picture of a running system carries more than
the thing being asked about, and this file is committed (ADR 0137).

**No credential reaches the record.** A signed link is a credential for the record it
names. It stays out of the answer, out of the record and out of the commit — this one does
not bend for any caller.

**Quote on-screen words exactly as the product spells them.** The whole value of a picture
over a diagram is that it carries the real label, so "Send quote" is not "Send".

## ④ Hand back rows, counts, and any flag

Return to the caller, per picture: the kind, the detail, the answer, and whether it was a
hit, a fresh read, or a flagged row. Then the run's counts — how many hits, how many
candidates-only, how many read fresh, how many not re-checked.

The counts are not decoration. A run where every call is a miss says the kind set no
longer fits the questions being asked, and that is the signal to extend the set rather
than keep paying.

## What this skill refuses

- **To answer a question it was not asked**, or to transcribe a picture in full.
- **To serve a near-miss row as a hit.** When in doubt, open the picture.
- **To put a credential, a customer identifier, or anything else it merely saw into the
  record.**
- **To present a `bytes_verified: false` row as verified.**
- **To hand back an answer with no picture and no row.** `no-answer` is the honest result,
  and the caller decides what to do about it.

## Red flags — stop and go back a step

| thought | what it means |
|---|---|
| "There is a row for this image, close enough" | Check the detail. A near-miss is a miss — ② |
| "I will transcribe everything so future callers are covered" | The first caller cannot know what a later one needs, and this file is committed — ③ |
| "The file is missing, I will answer from the row" | You may, but the flag travels with it — ② |
| "No kind fits, I will write my own phrasing" | Take `other` and add it to the contract — ① |
| "I will record the counts at the end" | Nothing else reports a hit that did not happen — ④ |

## Related skills

- `document-what-shipped` — asks `on-screen-text` for the words a page will quote.
- `ticket-trace` — asks `requirement` of an annotated screenshot that may *be* the spec.
- `references/picture-record-contract.md` — the row schema and the kind set.
