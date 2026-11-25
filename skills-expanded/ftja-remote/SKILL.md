---
name: ftja-remote
description: Draft (or redraft) the Remote check's setup for the user to confirm — the remote-work keywords, the categories the model answers, and which answers pass or fail — from where they live, where they want to work, their time zone and their work permit. Invoke when the user says "/ftja-remote", "set up the remote check", "write the remote setup", or when `ftja.run_bridge wait` returns {"status": "remote"} (the Pipeline tab's button).
---

# FTJA remote check setup

The Remote check is an optional stage of `/ftja-run`, between the code
filter and Stage 1. A cheap model reads only the title and the sentences
around the user's remote keywords, and answers a few questions (the
"categories") by picking from a fixed list of answers. Code then applies
the rule the user set for each answer. Your job here is to write a good
first version of that setup for this user. They edit it afterwards on the
Pipeline tab, so write something sensible and complete, not something
cautious and empty.

Every python call uses `venv/bin/python`. **On Windows**, read every `venv/bin/python` as `venv\Scripts\python` (and `venv/bin/pip` as `venv\Scripts\pip`), and run commands in PowerShell. The rules for each system (one shell, time limits, never cutting a command's output short) are in `.agents/skills/ftja-setup/windows.md` and `mac.md`: read the one for this system first. Write the draft files this skill passes with `--file` using your file-writing tool, not PowerShell `>` or `Set-Content`, which do not write plain UTF-8.
Never edit `remote-check.json`,
`remote-request.json` or `criteria.json` by hand; the commands below write
them.

## 0. Be in the right folder

Run `pwd` and `git rev-parse --show-toplevel`. Continue only in the user's
existing FTJA folder (it has `criteria.json`). If the session is not
attached to it, attach it as `/ftja-run` step 0a describes. Do not start
or restart the viewer for this; if it is running it will show your
progress by itself.

## 1. Work out the user's situation

The setup is written for four facts about the user: where they live, which
countries or regions they want to work in, their time zone, and what work
permit they hold.

```
venv/bin/python -m ftja.remote request
```

First tell the viewer you have started, so the page shows that the draft
is being written:

```
venv/bin/python -m ftja.remote begin
```

Then settle the four facts, in this order of trust:

1. `answers` in the request that are not empty: the user typed or
   confirmed these on the page. Use them as they are.
2. For each one that is empty, work it out yourself, without asking:
   `profile/summary.md` (where they live, citizenship, visa or permit, the
   places they say they want to work), then `criteria.json`'s `locations`
   (where their searches look is where they want to work), then the usual
   time zone of where they live.
3. What you still cannot tell, leave empty. Do not invent a work permit.

Do not ask the user in the chat: they confirm or correct all four on the
page before anything is used. The one exception is when you cannot tell
where they live at all and the request did not come from the page
(`status` was `none`): then ask that one question.

From here on, if you cannot finish, run
`venv/bin/python -m ftja.remote fail --error "<one plain sentence>"` before
you stop, so the page does not wait for you.

## 2. Read what is there

- `criteria.json` → `languages`: the languages the user reads postings in
  (ISO codes; empty means any, then use English plus the main language of
  where they live). Keywords are written in **each** of these languages.
- `venv/bin/python -m ftja.remote show`: the current setup. If `saved` is
  false, what it prints is the general built-in setup: use it as a list of
  ideas and write a fresh one. If `saved` is
  true the user already has one: keep every category you do not recognise
  as one of the five below (they added it), and keep the `id` of every
  category and answer that still exists, even if you reword it.

## 2b. Only a language is missing? That is another skill

`show` also prints `languages_without_keywords`: languages the user reads
postings in that the draft (or, with no draft, the saved setup) has no
keyword for. If that list is not empty and the request did not come from
the page's setup button (`status` was `none`, `drafted` or `done`), the
user most likely wants just those keywords: stop here and follow the
`ftja-keywords` skill (`.agents/skills/ftja-keywords/SKILL.md`) instead. It
adds a language's keywords without touching the rest.

## 3. Write the setup

Write it as JSON to `.ftja-run/remote-check.draft.json` (create `.ftja-run/`
if it is missing):

```json
{"languages": ["en", "fr"],
 "keyword_language": {"remote": "en", "télétravail": "fr", "à distance": "fr"},
 "drop_without_keywords": true,
 "guidance": "<two or three sentences for the model, see below>",
 "profile": {"residence": "...", "work_countries": "...", "time_zone": "...", "work_permit": "..."},
 "categories": [
   {"id": "remote_level", "label": "Remote level",
    "question": "How remote is the role itself?",
    "keywords": ["remote", "work from home", "hybrid", "..."],
    "options": [{"id": "fully_remote", "label": "Fully remote", "rule": "pass"},
                {"id": "hybrid", "label": "Hybrid: regular office days", "rule": "fail"},
                {"id": "on_site", "label": "On-site", "rule": "fail"}],
    "unknown": "pass"}]}
```

**Categories.** Write these five, with these ids, wording the labels for
this user:

1. `remote_level` — how remote the role is. Answers: fully remote (pass),
   hybrid with regular office days (fail), on-site (fail).
2. `work_location` — from where the person may work. Answers, named for
   this user: anywhere (pass); a region or list that includes where they
   live or want to work, e.g. "Includes France or the EU" (pass); only
   places that leave those out, e.g. "Only outside the EU" (fail).
3. `work_authorization` — the right to work. Answers: asks for a right to
   work the user holds (pass); asks for one they do not hold and offers no
   sponsorship (fail); offers visa sponsorship or relocation (pass). Leave
   this category out if the user gave no work permit.
4. `time_zone` — working hours. Answers: any hours (pass); hours that
   overlap with the user's time zone, named (pass); hours far from it,
   named, e.g. "US Pacific hours only" (fail). Leave it out if the user
   gave no time zone.
5. `onsite_duties` — presence asked for besides regular office days.
   Answers: none (pass); occasional — onboarding, team gatherings, some
   travel (pass); frequent — regular on-site weeks or heavy travel (pass:
   the user decides once they have seen real postings).

An answer's rule `fail` rules a posting out; `pass` means it is fine with
the user.

**How a posting is decided.** A posting that gives an answer marked
`fail` (with its sentence) fails. Otherwise the model judges the sentences
against all of the answers, fine and failing alike, and passes a posting
only when one of them says the role is worked in a way that suits the
user; it has to show that sentence. A posting that says nothing about
remote work therefore fails. An answer marked `pass` does not pass a
posting by itself; it tells the model what is fine with the user. So mark
`fail` on exactly the things that rule a posting out for this user.

**"Not stated".** A category's answer is `?` when the posting does not
say. That is reported and decides nothing; there is no rule to set for it
(write `"unknown": "pass"`). Always write `drop_without_keywords` as true.

**Answers.** Two to four per category, each a state a posting can plainly
be in, none overlapping. The label is what the user reads on every job
and what the model chooses from, so it must be understandable alone.

**Keywords.** They decide which sentences the model sees, and a posting
with none of them is dropped without a model call. So:

- Be broad. Include the direct words (remote, hybrid, on-site, work from
  home, home office) and the indirect ones that tell how remote a job
  really is: onboarding, offsite, retreat, team gathering, travel, in
  person, headquarters, time zone, working hours, overlap, work from
  anywhere, relocation, work permit, visa, sponsorship. A sentence like
  "you can work where you feel at home" has to be caught by something:
  add the phrases people actually write.
- Write each of them in **every** language the user reads, not only
  English: someone who reads English and French gets both sets (French:
  télétravail, à distance, présentiel, sur site, déplacements, fuseau
  horaire, ...). Use the wording postings in that language really use,
  not a word-for-word translation.
- `languages` lists those language codes, and `keyword_language` says
  which language every keyword is in (an abbreviation used in all of them,
  like EU or CET, goes under the first). The page shows the user the
  keywords one language at a time, to confirm before the categories.
- **No place names**: no countries, cities or regions (not France, Paris,
  Europe). Where a role may be done from is said in the sentence around a
  remote keyword, and a place name would match nearly every posting.
  Abbreviations of regions used as hiring scopes (EU, EMEA) are fine.
- Matching is by whole word and word stem, any case: `remote` also finds
  "remotely", `gathering` also finds "gather requirements". Prefer a
  phrase when a single word has an everyday meaning: `team gathering`,
  not `gathering`; `distributed team`, not `distributed`; never `global`,
  `country`, `location`, `office` or `work` alone. An all-capitals keyword
  (EU, WFH, CET) matches only in capitals; leave out an abbreviation that
  means something else in a language the user reads (in French postings
  "CET" is a savings account, compte épargne temps).
- Put each keyword in the one category it informs most (listing it twice
  changes nothing). A keyword of any category gets the posting read.
- Keep keywords that matched nothing in the measurement below: a small
  scrape says little about a rare phrase.

**Guidance.** Two or three sentences the model reads above the questions:
that it judges the role and not the company, what does not count as an
office day (travel, an onboarding week, occasional gatherings), that steps
of the hiring process (an on-site interview) say nothing about the job, and
anything the user's answers make important.

## 4. Measure before saving

```
venv/bin/python -m ftja.remote coverage --file .ftja-run/remote-check.draft.json
```

With no model call, it counts how many postings of the newest scrape in
this folder have at least one of your keywords (`with_a_keyword` of
`postings`), which keywords catch the most (`by_keyword`) and which never
matched. If there is no scrape yet (`postings` is 0), skip this step.

- A single everyday word near the top that hits a large share of all
  postings is probably matching something else. Read two or three of its
  hits if you are unsure, replace it with a phrase, and measure again.
- Do not chase a low number: catching most postings is acceptable, missing
  a remote one is not.

## 5. Hand the draft to the user

```
venv/bin/python -m ftja.remote save --file .ftja-run/remote-check.draft.json
```

It checks the setup and stores it as a **draft**. If it prints `Not
saved: ...`, fix what it names and run it again. Then delete the file you
wrote. Nothing is in use yet: the Pipeline tab now walks the user through
the draft one step at a time (their situation first, then each category),
and it becomes their setup when they confirm at the end. What they correct
there is kept as they typed it; the categories are theirs to adjust in the
steps that follow.

## 6. Report

Tell the user, in their language and briefly:

- that the web view has opened the draft for them to go through (it opens
  by itself; if their web view is closed, it is on the Pipeline tab under
  **Remote check**, "Review and confirm"), and that it is not in use until
  they confirm it there;
- the situation you assumed for them, saying which parts you worked out
  yourself rather than were told;
- for each category, which answers rule a posting out;
- that a posting which says nothing about remote work does not pass, that
  "not stated" in a category is only information, and that a posting with
  none of the keywords is dropped without being read;
- how many keywords, in which languages, and the coverage numbers if you
  measured;
- that they can change any name, keyword, answer or rule while they go
  through it, and again later;
- if `criteria.json`'s `stages.remote` is not true: that the check is
  still switched off, and the switch is on that same section. Do not
  switch it on yourself.

If you were called from `/ftja-run`'s wait (`{"status": "remote"}`), go
back to that wait afterwards.
