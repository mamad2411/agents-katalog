---
name: create-contact-list-from-image-or-spreadsheet
description: Turn a roster — a phone photo of a printed sign-in sheet, a screenshot, a PDF, a CSV, or a spreadsheet — into a verified contact CSV, importable vCards for iPhone and Android, and a comma-separated E.164 number list ready to paste into Messages. Use whenever the user drops a photo of a list of people and wants it "parsed", whenever they say "make contact cards", "generate vCards", "get these into my phone", "make a WhatsApp group from this", "I need everyone's numbers", "turn this roster into a CSV"; whenever an event/cohort/conference/class/retreat roster needs to become a group chat; whenever numbers need normalizing to E.164. Encodes the band-crop transcription discipline that makes photo OCR trustworthy (EXIF auto-orient, overlapping full-res bands — never read digits off a downscaled overview), the E.164-always rule, the name-prefix trick that survives WhatsApp's names-only picker search, the one-vCard-format-covers-both-platforms fact, the flag-don't-fix verification pass, and the hard reality that WhatsApp has no bulk-add — invite links are the fallback.
---

# Create Contact List from Image or Spreadsheet

> **The one thing to remember: never transcribe phone digits off a downscaled
> overview image.** A 1400px view of a full page is legible enough to *look*
> right and wrong often enough to poison a whole roster. Crop the table into
> overlapping full-resolution bands and read each one. See
> [Transcription](#transcription-the-part-that-actually-goes-wrong).

## When to use this skill

- The user drops a photo of a printed roster, sign-in sheet, or attendee list
  and asks for it "parsed"
- "Make contact cards", "generate vCards", "get these people into my phone"
- "I want to start a WhatsApp group with everyone from X"
- An event / cohort / class / retreat / conference list needs to become a
  group chat, a CRM import, or a broadcast list
- A spreadsheet of people needs numbers normalized to E.164
- Any time the deliverable is *"these humans, in my address book, fast"*

## Why this exists

Two failure modes, both expensive and both silent:

1. **Bad digits.** OCR from a photo is confidently wrong about `0/8`, `1/7`,
   `3/8`, `5/6`. A single wrong digit means a stranger gets added to a private
   group chat. The band-crop discipline below is the cheap fix.
2. **The wrong artifact.** Producing a beautiful CSV when what the user needed
   was 33 contacts in their phone in the next ten minutes. The output set here
   is ordered by *time-to-usefulness*, not by tidiness.

## The pipeline

```
image/PDF/sheet  →  transcribe  →  roster.tsv  →  build-contacts.py  →  deliverables
                    (bands)        (source of      (mechanical)
                                    truth)
```

Keep `roster.tsv` as the durable intermediate. Everything else is regenerable
from it, which means a transcription correction is a one-line edit plus a
re-run — not a hand-patch across six files.

## Transcription: the part that actually goes wrong

### 1. Normalize the image first

HEIC from an iPhone is not directly readable, and **EXIF orientation lies** —
a 5712×4284 "landscape" file is often a portrait photo. Auto-orient before
computing any crop box, or every offset will be wrong.

```bash
sips -s format jpeg -s formatOptions high IMG_1234.heic --out full.jpg
magick full.jpg -auto-orient oriented.jpg
magick identify oriented.jpg     # trust THIS width/height, not the HEIC's
```

### 2. Read the overview once — for structure only

Downscale to ~1400px and read it to learn the **column layout, row count, and
where the table starts and ends**. Do not harvest digits from it.

```bash
sips -Z 1400 oriented.jpg --out overview.jpg
```

### 3. Crop into overlapping full-res bands, then read

Estimate the table box from the overview's proportions, then slice it into
horizontal bands with **deliberate overlap** so no row is bisected at a
boundary. Upscale and sharpen — the model reads crisp large glyphs far better
than small ones.

```bash
# crop WxH+X+Y, 760px tall bands stepping 690px → 70px of overlap
for i in 0 1 2 3 4 5; do
  y=$((820 + i*690))
  magick oriented.jpg -crop 3250x760+450+${y} +repage \
    -resize 1900x -sharpen 0x1 band_$i.jpg
done
```

Then `Read` each band in order. The overlap gives a free consistency check:
the last row of band N reappears as the first row of band N+1, so a
misread there is self-revealing.

### 4. Preserve what the sheet actually says

Transcribe **verbatim**. `Hollly` with three L's stays `Hollly`. A blank phone
cell stays blank. An enrollment date in the wrong year stays wrong. You are
producing a faithful record plus a flag list — not a corrected roster. Silent
"helpful" fixes are how a typo becomes permanent and untraceable.

## Build the deliverables

`scripts/build-contacts.py` does the mechanical half. Input is any delimited
file with a header row; it matches columns case-insensitively against aliases
(`first`/`last`/`name`/`mobile` and friends) and folds every other column into
the vCard `NOTE` and the master CSV.

```bash
python3 scripts/build-contacts.py \
  --input roster.tsv \
  --out ~/Downloads/LV236-BananaLove \
  --group  "LV236-BananaLove" \
  --org    "ChoiceCenter LV236 - BananaLove" \
  --event  "ChoiceCenter Discovery, Las Vegas LV236, Aug 27-30 2026" \
  --prefix "LV236 "
```

It emits, and prints a verification summary:

| Output | Why it exists |
|---|---|
| `<group>-roster.csv` | Master spreadsheet — every column, plus E.164 |
| `<group>-ALL.vcf` | **All contacts in one vCard 3.0 file** — one tap to import |
| `<group>-ALL-cleannames.vcf` | Same, without the name prefix |
| `vcards/` | Individual `.vcf` files (iOS fallback when a big multi-card file balks) |
| `vcards-cleannames/` | Individual files, unprefixed |
| `google-contacts-import.csv` | Google Contacts format — creates the label on import |
| `numbers.txt` | Comma-separated E.164, ready to paste into a Messages To: field |

### E.164, always

Store every number as `+1XXXXXXXXXX`. This is what makes WhatsApp, Signal, and
iOS reliably match a saved contact to a messaging account. `(805) 455-1379` in
a `TEL` field works *sometimes*, which is worse than never.

### One vCard format covers both platforms

**vCard 3.0** is read natively by iOS Contacts, Android/Google Contacts,
macOS, and Outlook. When a user asks for "two formats if necessary", the
correct answer is that it isn't necessary — say so rather than shipping a
vCard 4.0 twin that adds no reach. The Google CSV is included not as a second
format but as a genuinely better *bulk path* on Android/desktop, because it can
create the contact **label** in the same import.

### The name prefix, and why it is not cosmetic

WhatsApp's "New Group" participant picker **searches contact names only** — not
company, not notes, not labels. Prefixing every card `LV236 Art Kalayjian`
means the user types `LV236` once and the whole cohort appears together.
Without it they hunt 33 names one at a time through a picker.

Always ship the `-cleannames` variant alongside and explain the tradeoff: the
prefix is fast, the clean names keep the address book tidy. Let the user pick;
default to prefixed when the stated goal is speed.

## Verify before anyone gets messaged

The script prints these; **surface all of them to the user, fix none of them**:

- **Rows with no number** — kept in the CSV, excluded from vCards and
  `numbers.txt`. Name them explicitly so the user can chase it down.
- **Duplicate numbers** — two people sharing a number is sometimes real (a
  couple, a participant who is also staff) and sometimes a printing artifact.
  The user knows which; you don't.
- **Non-standard digit counts** — anything that isn't 10 digits in the default
  region. Almost always a transcription slip.
- **Odd spellings and out-of-range dates** — flag them in prose. `Hollly`,
  a lone `2025` date in a sheet of `2026` dates.

Then **cross-check the derived files against each other, once, at generation
time** — before the user has touched anything:

```bash
diff <(tr ',' '\n' < numbers.txt | grep .) \
     <(grep '^TEL' <group>-ALL.vcf | sed 's/.*://' | tr -d '\r')
```

A disagreement *at that moment* means one of the two was written by a broken
command. **After** the user has the files, this check means nothing — see below.

## `numbers.txt` is a consumable, not a record

Once handed over, the number list is a **working surface**. The user pastes
numbers into a To: field and deletes each one as it lands, so the file empties
as they make progress. A `numbers.txt` that has gone blank is not corruption —
it is a **finished job**, and the leftover commas are the tally.

This has two hard consequences:

- **Never regenerate an output file the user has already been given** without
  asking. Re-running the builder over a half-consumed list destroys the only
  record of where they were. If a file looks wrong after handoff, *ask what
  they've been doing with it* before diagnosing it as broken.
- **Never diagnose a changed artifact as a defect** when a human has had their
  hands in it. "This file is empty" and "this file is done" look identical from
  the outside.

Lean into it rather than fighting it. A flat comma-separated list is a good
delivery format precisely *because* it can be eaten one number at a time. When
the batch is large enough that the user will work through it in sittings, offer
a `numbers-checklist.txt` — one number per line, easy to delete or check off —
alongside the single-line paste version.

## Getting the group live (WhatsApp)

**There is no supported bulk-add.** WhatsApp's picker only offers people already
in the phone's address book. Chrome extensions that claim otherwise require full
access to the user's WhatsApp Web session and carry ban risk — **do not
recommend them.** The vCard import *is* the bulk step.

1. Import the combined `.vcf` (AirDrop/email on iOS; Google Contacts →
   *Fix & manage* → *Import from file* on Android).
2. New Group → search the prefix → select all → name → Create.
3. Group info → **Invite via link** → Copy. Get this immediately.
4. Post the first message, then **pin it** so late joiners land on it.
5. **Mop up.** Anyone whose group privacy is "My Contacts" and who doesn't have
   the organizer saved **cannot be added directly** — WhatsApp offers a private
   invite instead, and that invite **expires in 3 days**. SMS them the link.

Group cap is **1,024**, so cohort-sized lists are never the constraint.

**When speed matters more than completeness:** create the group with 3–4 people,
grab the invite link, and SMS it to everyone at once by pasting `numbers.txt`
into the Messages To: field. Self-serve joining sidesteps every privacy setting
and all the "who got added" bookkeeping. It's opt-in, so expect 60–80% in the
first hour rather than everyone instantly. Doing both is the belt-and-suspenders
version.

Also draft the first message. The user asked for a group, which means they have
something to say — handing over an empty group is half the job.

## Privacy

A roster is dozens of people's personal mobile numbers, and they did not consent
to being in a git repo.

- Write deliverables **outside any git repo** — `~/Downloads/<group>/` is the
  default. Never the working tree, never `context-v/`, never a scratch dir
  inside a project.
- Never commit the output. Say so in the generated `README.md`.
- Tell the user to delete the folder once the group is up.
- Real roster data belongs nowhere in this skill directory. The worked example
  in this file is deliberately abbreviated and the numbers are not reproduced.

## Gotchas

- **`ls` may be aliased to `eza`** in this environment; `ls -la <dir> | wc -l`
  can fail on flag parsing. Use `find <dir> -name '*.vcf' | wc -l`.
- **PIL is often absent** even where `python3` exists. ImageMagick (`magick`)
  and macOS `sips` are the reliable pair for image work here.
- **Python 3.11** rejects same-quote nesting inside f-strings. Build filename
  stems with `%` formatting rather than nested f-strings.
- **`sips -Z` respects EXIF orientation, raw pixel dimensions do not.** Always
  `magick identify` the auto-oriented file before computing crop offsets.
- **vCard escaping is real.** Commas and semicolons in `NOTE`/`ORG` must be
  backslash-escaped or the card silently truncates in some importers.
- **A photo of a screen** (rather than paper) adds moiré. Try
  `-despeckle` before `-sharpen`, and lean harder on the overlap check.

## Related

- [[prep-images-for-embed]] — the other half of the image-handling story, for
  images destined for publication rather than data extraction
- [[lossless-crm-interface-guidelines]] — when the roster should land in Twenty
  rather than (or as well as) a phone address book
- [[context-vigilance]] — where the durable `roster.tsv` belongs if the cohort
  becomes an ongoing project rather than a one-off
