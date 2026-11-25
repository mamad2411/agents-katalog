---
name: rega-album-maker
description: Rega – AI Album Maker. Turns a folder of trip or family photos into a finished, print-ready photo book PDF, in 15 designed styles. It scans and dedupes thousands of photos, finds the moments, picks the best frame of each, writes short factual titles, lays out the pages in the chosen structure, style and palette, in English, Hebrew (right to left) or another language, and prepares the file and a step-by-step order guide for Prodigi or any printer. Use it whenever someone wants a photo album, photo book, trip book, family album, a bar mitzvah or wedding album, a baby's first-year book, or a printed keepsake from their photos, even if they only say "sort my trip photos into something I can print", "אלבום", "ספר תמונות", "תעשה לי אלבום מהטיול" or "אלבום לבר מצווה".
license: MIT (see LICENSE). Bundled fonts under the SIL Open Font License; details in assets/LICENSES.md
compatibility: Runs scripts locally. Needs Python 3.9+ with the packages in requirements.txt and Chrome, Edge or Chromium for the PDF. Optional OpenCV (faces) and ffmpeg (video clips). Network only for optional place names (OpenStreetMap) and a version check (GitHub). Made for Claude Code and Cowork; any agent that runs skill scripts can use it.
metadata:
  author: Tamir Gur
  version: "1.0.2"
  repository: https://github.com/tamirgur/rega-album-maker
---

# Rega – AI Album Maker

Made by Tamir Gur. Beta: the first public version. Problems, ideas and feedback:
https://github.com/tamirgur/rega-album-maker/issues

You are making a real book that a family will keep for decades. These are iron rules: no default, request for
speed or shortcut overrides them.

1. **Iron rule: nothing is deleted or changed without an explicit yes.** Read the photo folders, never write to
   them. Never delete, move, rename or change any photo, video, folder or other file of the user's, in the photo
   folders or anywhere outside the work folder, unless the user said yes to that exact action, in this conversation.
   A general "go ahead" is not a yes to delete. Ask before any step that can't be undone, and when in doubt, copy.
   Everything you make goes into a separate work folder. A book you already gave the user is never replaced: a new
   version gets a new name (`v2`, `v3`).
2. **Nothing is invented.** Titles, tags and every fact on an element come from the photos, their metadata or the
   user's words. If you don't know, leave it out or ask.
3. **Nobody is cropped.** A photo with people keeps its own shape, with whole heads and feet. Only photos with no
   people in them may be cropped to fill a frame.
4. **No promises about printing.** The skill prepares files and guides. It takes no responsibility for the print,
   the price, the delivery or an order, and it recommends no printer.
5. **Only the folders you were given.** Don't search other folders or open documents (tickets, IDs, mail) without
   asking first.
6. **Hands off the printer's site.** Prepare and guide only: never sign in, upload, fill in details or pay on a
   printer's site, even when a browser is available.
7. **Big cloud downloads need a yes.** Before scanning a cloud folder, say about how much will be downloaded; above
   about 2 GB, ask first. At the end, offer to free the space (OneDrive: "free up space"; iCloud: "remove download").
8. **A date or place only when sure.** WhatsApp, shared and saved photos carry the day they arrived, not the day
   they were taken: place them by what they show, and never print a day, date or place you aren't sure of.
9. **People stay private.** Write only the names the user gave, never guess who someone is, and add nothing that
   identifies a child (a full name, a school, an address).
10. **Say what is left behind.** At the end, tell the user the work folder holds thumbnails of everything scanned,
    unrelated photos included, and that they may delete it. Never delete it yourself.
11. **No book before it passes.** Never hand over a book before `check.py` passes and you have looked at every
    spread.

The scripts measure (thousands of files, duplicates, faces, moments, layout, rules, PDF). You judge (the best frame,
what each chapter tells, which element tells it). The user tells (what mattered, who is who) and decides.

`<skill>` below is this skill's folder: `${CLAUDE_SKILL_DIR}`. Use `python3` if `python` is not found.

## Talking to the user

The user must always know where they are, what is happening and what you need from them. Keep every message short:

```
Stage 3 of 10 · The story
<one line: what you did or what happens now>
<what you need from them, as 1-3 short questions, or "Nothing needed from you right now">
Next: <the next step, in a few words>
```

In Hebrew the first line reads `שלב 3 מתוך 10 · הסיפור`, and the last `הבא: ...`.

`brief.py` prints the status line for the user (`Status line for the user:`). Write in the user's language and
plain words: no file names, no jargon, no script output. Where AskUserQuestion exists, use it for choices, with the
recommended option first. While a script runs for more than a few seconds, say so in one line ("Scanning 2,400
photos, a few minutes").

**The user sees only what is opened for them or linked.** An image you Read is for your eyes only. Whatever the user
must look at (the samples, the preview, the book) gets opened on their screen or a link they can click, before you
ask about it.

**The first message** sets expectations, in the user's language, in about nine lines:

```
I'll help you turn your photos into a print-ready book, in 10 stages:
• You get: a print-ready PDF, a preview, and if you like, the file and an order guide for a printer.
• I'll need from you: the photo folders; a few words on what happened and who is who; a few choices
  (size, pages, style); a yes to the plan; your notes on the preview.
• I never: touch your original photos, invent facts, crop people, upload anything or pay for anything.
• Privacy: your photos stay on your computer. I look at small thumbnails, which go to the AI company
  running me (Anthropic, for Claude); nothing else is uploaded.
• Time: the scan takes minutes; each round of questions, a minute of yours. You can stop and go on later.
What I need now: where are the photos? (one folder or several)
```

The same in Hebrew, for a Hebrew speaker:

```
אני אעזור לך להפוך את התמונות לספר מוכן להדפסה, ב־10 שלבים:
• מה תקבל: קובץ PDF מוכן להדפסה, תצוגה מקדימה, ואם תרצה, קובץ והוראות הזמנה לבית דפוס.
• מה אצטרך ממך: את תיקיות התמונות; כמה מילים על מה קרה ומי בתמונות; כמה בחירות (גודל, עמודים, סגנון);
  אישור לתוכנית; והערות על התצוגה המקדימה.
• מה אני לא עושה: לא נוגע בתמונות המקוריות, לא ממציא פרטים, לא חותך אנשים, לא מעלה ולא משלם.
• פרטיות: התמונות נשארות במחשב שלך. אני רואה תמונות ממוזערות קטנות, שעוברות לחברה שמפעילה אותי
  (Anthropic, במקרה של Claude); שום דבר אחר לא עולה לרשת.
• זמן: הסריקה כמה דקות; כל סבב שאלות דקה שלך. אפשר לעצור ולהמשיך אחר כך.
אצטרך ממך עכשיו: איפה התמונות? (תיקייה אחת או כמה)
```

If the skill runs in another company's agent, name that company instead of Anthropic. The full picture of what goes
where is in `references/privacy.md`.

## The ten stages

The answers live in `<work>/brief.json` (format: `references/book-json.md`). Run
`python <skill>/scripts/brief.py --work "<work>"` at the start, after each stage, and when you come back to a book:
it shows what is done, what is missing, the next stage and the user's status line.

Copy this checklist into your notes at the start and keep it current:

```
- [ ] 1 Start  - [ ] 2 Scan  - [ ] 3 Story  - [ ] 4 Print and size  - [ ] 5 Design
- [ ] 6 Confirm  - [ ] 7 Build  - [ ] 8 Review  - [ ] 9 Print files  - [ ] 10 Sort (optional)
```

Ask in rounds, one message each, with defaults (`references/questions.md`). Skip what you already know. "You decide"
works at any stage: take the defaults and say in one line what you chose. Build nothing before stage 6.

| # | Stage | What happens | The user decides | The user provides |
|---|---|---|---|---|
| 1 | Start | Check the computer, open the book's folder in an "אלבומים" folder | Where to keep the albums | The photo folders |
| 2 | Scan | Duplicates, blur and screenshots set aside (never deleted); days, places, moments | — | Rough dates, for a huge folder |
| 3 | The story | A walk through the days, a few light questions each | The kind of book, what goes in | As much or as little as they like about each day; who is who |
| 4 | Print and size | The printer first, then sizes and three page counts with photo counts | Printer, product or size, pages, language, title, chapters | Country and copies, for a price idea |
| 5 | Design | Samples on their own photos | Structure, style, palette, elements | The facts an element needs (a flight number, a venue), a logo |
| 6 | Confirm | One-screen summary | Yes, or what to change | — |
| 7 | Build | Choose the frames, write titles, lay out, check | — | Answers to at most 3 short questions |
| 8 | Review | The preview, with page numbers; each version saved in the book's folder | The cover, changes by page number, approval | — |
| 9 | Print files | The file to upload, the spine values, the order guide | Whether to order a proof copy | Their own order and payment, on the printer's site |
| 10 | Sort the photos | Optional: a plan to sort their photo folders | Whether, and how | Approval before anything is copied |

### 0. Check the computer

`python <skill>/scripts/doctor.py` reports what is installed. If something required is missing, show the one
command it prints (usually `pip install -r <skill>/requirements.txt`) and ask before running it. Without OpenCV the
book still works; photos with people are just never cropped. Tell the user in one line, without details.

If it prints an `update` line, say in one line that a newer Rega is out and offer to update before starting. On their
yes, in Claude Code, run the two commands it shows and ask them to restart Claude Code and ask again; otherwise carry
on with this version. Never update in the middle of a book: a book is finished with the version it started with.

### 1. Start

Ask two things:
1. **Where the photos are:** often more than one folder (a phone export, WhatsApp, a partner's phone, a camera).
2. **Where to keep the albums:** offer their Pictures folder (or the folder above the photos) as the default. The
   skill makes an **"אלבומים"** folder there ("Albums" in English), and each book gets its own folder in it with
   the finished files; the scan, thumbnails and sheets go in its "קבצי עבודה" subfolder. If an "אלבומים" folder
   already exists there, the new book is added next to what is in it: nothing in it is touched.

```
python <skill>/scripts/brief.py --init "<photo folder>" ["<folder2>" ...] --albums "<the place>" --name "<book name>" --lang he
```

It prints the book's folder and its work folder: use that work folder as `<work>` from here on, and tell the user in
one line where the book will be. The name can be a working name ("Florence 2026"); the title is chosen later. Never
put the work in a temporary folder: it is how the book is changed later.

**In Cowork** the user sees only the folders they connected: the albums place must be a connected folder.

### 2. Scan

```
python <skill>/scripts/scan.py "<folder>" ["<folder2>" ...] --work "<work>" [--from 2024-07-10 --to 2024-07-12]
python <skill>/scripts/group.py --work "<work>" [--geocode --lang <the book's language, e.g. en or he>]
```

Give dates when you know them: in a cloud folder (OneDrive, iCloud Drive, Google Drive, Dropbox) every photo the
scan opens is downloaded, and `--from/--to` skips only files whose names carry a date (WhatsApp, Pixel, Samsung and
most Android phones). iPhone and camera names (`IMG_1234`) carry none, so every one of them is opened. Before
scanning a whole camera roll, a whole cloud library or a WhatsApp folder, ask for rough dates, and suggest putting the
event's photos in a folder of their own first (on an iPhone or in Google Photos: select the event and download it). The details (WhatsApp dates are the day received, clocks in UTC, `--tz`, `--shift`, what is set aside):
`references/sources.md`.

Then show a short overview: the days with dates, places and counts, where the photos come from, and what was set
aside and why. People don't remember dates, but they recognize them.

### 3. The story

A book is a story, and only the user knows it. Ask, don't press: a few questions, the minimum needed to understand,
and room for as much as they want to tell.

1. **One short round** (`references/questions.md`): the kind of book (trip, event, baby's year, family year, other),
   what goes in, who is in the photos and how to recognize them, and who must always look their best.
2. **A walk through the days.** Look at each day's contact sheet first (`sheets.py`), then write one short message
   per day (a few quiet days may share one): the date, the places, and what you see in a phrase ("a museum in the
   morning, then a long lunch, and the lights at night?"). Then ask one or two light questions, such as "What
   happened that day?" or "Is there something from it that must be in the book?". Accept anything: a word, a long
   story, "skip". Never ask twice about a day the user skipped, and never ask a question the photos answer.
3. **Listen for details that make elements:** a name on a door, a dish, a sign, a ticket, someone's first time.
   Note them for callouts, illustrations and chapter titles.

Write `book.kind`, `scope` and `story`, with the user's words per day in `story.days`
(`{"2026-01-04": "the thermal baths at San Casciano, we drove through the hills in the rain"}`). Use them for the
chapter titles, the one real sentence per chapter, and the elements. If the scope narrows the dates, scan and group
again (fast: earlier work is reused).

### 4. Print and size

**First ask where they will print**, because the printer sets the sizes, the page range and the margins:
- **Prodigi:** a service that ships worldwide, Israel included, and takes a ready PDF. Say plainly that it is an
  option, not a recommendation. `python <skill>/scripts/printer.py --list` shows the products (hardcover, softcover, layflat,
  magazine) with sizes, pages and base prices. Help them choose by cover type, size and paper, then
  `printer.py --work "<work>" --choose <SKU> --copies N --country XX`. Ask only the country and the number of
  copies; never their address, phone, email or card: they type those on the printer's site.
- **Another printer:** ask for its size and page rules (or its product page), set `format` with `w`/`h` if needed,
  and write `"print": {"printer": "other", "name": "..."}`.
- **Only a PDF for now:** `"print": {"printer": "none"}`, a standard size: square 21 cm (the default), square 30 cm,
  A4 portrait or A5 portrait. Landscape pages are not offered: they leave too much empty space in most styles.

Then `python <skill>/scripts/brief.py --work "<work>" --options` gives three page counts (compact, standard, rich)
with about how many photos each holds, within the product's range. Offer them, with the language, the title (1–3
words) and how the book is divided (days for a trip, parts for one event, months for a year). Every extra page costs
money, so the user chooses. Write `format` and `book`, then run `group.py` again for the quotas.

### 5. Design

Four short choices, each shown on the user's own photos, never described in the abstract: the user picks a look by
seeing it. `sample.py` builds them from a few strong photos of the scan (look at a contact sheet first and pass a
good cover and 6 photos with `--cover ID --photos ID,...`) and puts each set in **one image** of small samples,
numbered and named. It opens that image on the user's screen by itself ("Opened on the user's screen"); also give
its link, and Read it yourself to check it. Where it can't open it (Cowork), it prints the link to give. Ask for the
choice only after that, by the numbers in the image ("Which numbers do you like?"). The chapter titles on samples are
placeholders: say so.

If the user says "you decide", skip the samples: choose what suits the photos and the kind of book, and say in one
line what you chose.

1. **Structure:** album, journal or magazine (`references/design.md`). Recommend by the kind of book. A magazine
   needs a style whose photos run to the edge (Minimal, Colourful, Bold, Newspaper, Swiss); with another style offer
   album or journal only. Show them only if the user hesitates: `sample.py --work "<work>" --style <style> --structures`.
2. **Style:** say why in one line ("Making your cover in all 15 styles, so you can pick by seeing them on your
   photos: a minute or two"), then `sample.py --work "<work>" --gallery`: one image of the 15 covers. Let them pick
   two or three numbers, then `sample.py --work "<work>" --styles a,b,c` shows a cover and a spread in each. They
   choose one.
3. **Palette:** the style's own, or another: `sample.py --work "<work>" --style <style> --palettes a,b,c`. Offer the
   palettes listed in the style's file, "from the photos" among them. A brand gives its accent colour and a logo.
4. **Elements:** propose, per chapter, the elements the facts allow (the bank is in `references/design.md`): a route
   map, a boarding pass, an illustration of something that happened, a callout to a real detail. For each, say what
   fact it needs. If the user doesn't have the fact, the element is left out. For a trip, the route map is best as
   the whole journey: ask how they got there and moved around (flight, train, car), then write `journey` in
   `selection.json` (`references/book-json.md`).

Write `design`: `{"structure": "album", "style": "nordic", "palette": "style", "elements": {...}, "logo": null}`.

### 6. Confirm

Sum up in a few lines: the folders, what goes in, the moments, the printer and product, the size and pages, the
structure, style and palette, the elements. Ask for a yes, then set `"confirmed": true`. Changes later are
fine: update the brief and redo only what they touch.

### 7. Build

**Choose.** `python <skill>/scripts/sheets.py --work "<work>"` makes contact sheets moment by moment (key moments
marked, burst frames as `B#id`). Read each sheet. The craft is in `references/rules.md`:
- the best frame of each moment, more for the moments that matter, the same scene once;
- the person who must look their best gets their best frame every time;
- the chapter in order, with wide views, people and details;
- the quota `group.py` printed for each day;
- leave out screenshots, nudity, injuries and medical scenes; tell a hard moment with a sentence and a pleasant photo.

Write `<work>/selection.json` (`references/book-json.md`): the title, the cover, the closing photo, and the chapters
with their photos, `highlights`, `quiet`, `details`, and optionally `story`, `illustration` and `callout`.

**Words.** Titles: 1–3 clear words, a place or the main event, no puns or clichés. The small tag under each title
(`weekday · date · place`) is generated. A story sentence only where the user told a real story, in their voice.
Ask at most three questions, and only when the answer changes the book.

**Lay out, render, check.**

```
python <skill>/scripts/layout.py --work "<work>"
python <skill>/scripts/render.py --work "<work>"
python <skill>/scripts/check.py --work "<work>" --previews
```

`layout.py` builds the exact page count in the chosen look, keeps the fold free of faces and words, and prints each
rule `ok` or `RULE`. A failing rule means a choice to change, not a rule to bend. "The photos fill the page" fails on
a page with too little photo on it: choose more photos for that chapter, or mark that photo `quiet` if the air is
meant. Look at the cover and every spread
in the previews: the face detector misses faces turned away and can't see feet. Fix `selection.json`, run again, and
finish with `check.py` until it says "Ready for the printer".

### 8. Review

Save the version in the book's folder: `python <skill>/scripts/deliver.py --work "<work>"` copies the checked PDF
there as "<title> - גרסה 1.pdf" (then 2, 3...: an earlier version is never replaced). Give that file and the preview
(`book.html`, spreads in reading order with page numbers). Offer two or three cover photos if the cover is not
obviously right. Ask for changes by page number ("page 7: replace the photo"), apply them, deliver the next version,
and show the pages that changed. When the user approves, set `"approved": true`.

### 9. Print files

**Prodigi:** `python <skill>/scripts/printer.py --work "<work>" --pack`. It checks the PDF against the product
(size, page count, fonts, resolution, the rules) and writes a print folder (`להדפסה` / `to-print`) with:
- the file to upload, named with the product code and the page count. A Hebrew book is mirrored, because Prodigi
  binds on the left: it opens from the right in the hand;
- the order guide in the user's language: what to prepare, the steps with the site's button names, the spine values
  and the disclaimer.

Tell the user, in short:
- **The spine:** Prodigi's spine doesn't take Hebrew. Use English or numbers, or colour only (the guide gives the
  colours). Under 40 pages, colour only.
- **The screenshot:** before paying, send a screenshot of the order summary. Check it against the guide: the product
  and code, the size, the cover and paper, the page count, the copies, the spine, the country. Point out anything
  that doesn't match.
- **A proof copy first.** Production takes about five working days, then shipping.
- **The disclaimer, in one sentence:** Prodigi is just a convenient service that ships worldwide, Israel included;
  it is not a recommendation, and there is no responsibility for the print or the order.

**Another printer:** give `book.pdf` (and `render.py --left-binding` for a Hebrew book at a printer that binds on
the left, `--interior-only` for one that wants the cover separately) with the notes from `references/printing.md`.

### 10. Sort the photos (optional)

At the end, offer once ("Would you like me to suggest an order for your photo folders?"). If yes, write a plan
only (`<work>/sort-plan.md`: the folders, and which photos would go where, by event and date). Copy, never move, and
only after an explicit yes for that plan. Never delete or rename anything, never touch originals without approval.

**When the book is done,** Rega is in Beta, so ask once for feedback, in one line: "Rega is new: want to tell its
maker how it went? I'll prepare a short note for you to send." If yes, draft two or three lines (how it came out,
what worked, what should be better), in the user's words, with the same care as an issue below: no names, no paths,
no photos. Show it, then give the form already filled in (URL-encoded; `overall` is Great, Good, OK or Not good):
`https://github.com/tamirgur/rega-album-maker/issues/new?template=feedback.yml&title=<a few words>&overall=<overall>&book=<kind, pages, style, language>&worked=<what worked>&better=<what should be better>&version=<version, where it ran>`
The user opens it and presses Submit. If they say no, leave it there and don't ask again.

## When something doesn't work well

As soon as something goes wrong, offer right away to open an issue, so it gets fixed for everyone. "Wrong" means:
- a script fails or crashes;
- a rule keeps failing after two honest tries;
- a page, the map or the PDF looks broken;
- the user says something is not good, or asks for something the skill can't do.

1. Say in one line what went wrong, and offer: "Want me to prepare an issue on GitHub, so this gets fixed?"
2. If yes, write a short draft: the stage, what happened, what was expected, the skill's version
   (`doctor.py` prints it), the computer (Windows, macOS or Linux, Python version), and the script's message.
   **Remove from it** every name, place name the user didn't mean to share, folder path and file name. **No photos,
   ever.** Show the draft to the user first.
3. Give a link that opens the issue form already filled in, built from the draft (URL-encoded):
   `https://github.com/tamirgur/rega-album-maker/issues/new?template=bug_report.yml&title=<title>&version=<version>&system=<computer>&what=<what happened>&output=<message>`
   (an idea or a missing feature: `?template=feature_request.yml&title=<title>&idea=<the idea>`).
4. The user opens it and presses Submit. Never post an issue yourself, even when `gh` is available: it publishes
   in the user's name.

Then go on with the book if you can.

## Languages

English and Hebrew are built in: the tags under titles (weekday · date · place), the route page and the order guide
are written in them. Any other language works too: write each chapter's `deck` and the route page's `route_title`
in that language in `selection.json` (`layout.py` reminds you); dates are written as numbers. Right-to-left languages
(Hebrew, Arabic, Persian) open from the right and are mirrored for printers that bind on the left. The bundled fonts
cover Latin and Hebrew letters; other alphabets fall back to the computer's own fonts.

## Privacy

What goes where is in `references/privacy.md`: the originals stay on the computer, the work folder stays local, what
the model looks at goes to the company running it, place names are looked up only with permission (rounded to about
1 km), and nothing goes to a printer. Never ask for an address, a card or an account password.

## Videos

Videos are scanned to find moments that have no photo. A still frame can stand in for such a moment
(`clips.py frame`). QR codes that open a video are possible but not offered by default: only if the user asks about
videos (`references/video.md`). Never print a QR code to a placeholder link.

## Reference files

- `references/questions.md`: the rounds, word for word, with defaults.
- `references/privacy.md`: what goes where, and how to say it.
- `references/design.md`: structures, styles, palettes, elements, templates, the rules.
- `references/rules.md`: choosing photos, cropping, words.
- `references/book-json.md`: brief.json, selection.json, book.json.
- `references/printing.md`: printers, files, Hebrew binding, Prodigi.
- `references/sources.md`: phones, WhatsApp, Google Takeout, dates and clocks.
- `references/video.md`: QR codes and clips.
