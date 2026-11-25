---
name: ftja-keywords
description: Write the keywords for a language the user has started reading postings in — for Stage 1's keyword list and for the Remote check's — and hand them to the user to confirm on the Pipeline tab. Invoke when the user says "/ftja-keywords", "add French keywords", "I added a language", or when `ftja.run_bridge wait` returns {"status": "keywords"} (the Pipeline tab's button).
---

# FTJA keywords for a new language

Two stages of `/ftja-run` read a posting only where one of the user's
keywords appears: Stage 1 (its "Include keywords") and the Remote check.
A posting written in French is caught only by French keywords. So when the
user adds a language under Stage0's readable languages, both keyword lists
have nothing for it, and every posting in that language is dropped unread.
Your job is to write that language's keywords from the ones the user
already has. They confirm them on the page; nothing is added before that.

Every python call uses `venv/bin/python`. **On Windows**, read every `venv/bin/python` as `venv\Scripts\python` (and `venv/bin/pip` as `venv\Scripts\pip`), and run commands in PowerShell. The rules for each system (one shell, time limits, never cutting a command's output short) are in `.claude/skills/ftja-setup/windows.md` and `mac.md`: read the one for this system first. Write the draft files this skill passes with `--file` using your file-writing tool, not PowerShell `>` or `Set-Content`, which do not write plain UTF-8.
Never edit `criteria.json`,
`remote-check.json` or `keywords-request.json` by hand.

## 0. Be in the right folder

Run `pwd` and `git rev-parse --show-toplevel`. Continue only in the user's
existing FTJA folder (it has `criteria.json`). Do not start or restart the
viewer; if it is running it follows your progress by itself.

## 1. Take the request

```
venv/bin/python -m ftja.keywords begin
```

It prints `items`: the lists to fill, each a `target` (`stage1` or
`remote`) and a `language` code. With a request from the page it is what
the user clicked; typed in the chat with no request, it is every gap there
is. The page now shows that you are writing.

- `"nothing_missing": true`: every language the user reads has keywords in
  both lists. Say so and stop.
- From here on, if you cannot finish, run
  `venv/bin/python -m ftja.keywords fail --error "<one plain sentence>"`
  before you stop, so the page does not wait for you.

## 2. Read what the user already has

```
venv/bin/python -m ftja.keywords gaps
```

For `stage1` and `remote` it prints the existing `keywords`, which
language each is recorded in (`keyword_language`; none recorded means the
first language the user reads), and for `remote` the `categories` with
their keywords. For Stage 1 also read `rubric.md`'s Pass and Fail
sections: the keywords exist to find the sentences those rules are about.

## 3. Write the keywords

For each item, write the keywords a posting **in that language** would use
for the same things the existing keywords catch.

- Do not translate word for word. For each existing keyword, ask what it
  is there to find, then give the term or terms postings in that language
  really use for it. One keyword can become several, or none: a tool or
  product name ("Cursor", "LLM") is the same in every language and needs
  no entry here.
- Matching is by whole word, any case. Word forms are only folded the
  English way, so in other languages **list the forms yourself**: singular
  and plural, masculine and feminine where both occur ("basé à", "basée
  à"; "prototype", "prototypes", "prototypage").
- Prefer a phrase when a single word has an everyday meaning in that
  language. An all-capitals keyword (EU, MVP) matches only in capitals.
- Add no place names (countries, cities, regions). If the user's own list
  has some, leave their equivalents out too; that list is theirs to edit.
- The existing keywords keep working on postings in the new language:
  matching does not depend on the posting's language. So a word that
  language's postings use unchanged ("remote", "onboarding", "visa", an
  abbreviation like CET) needs no new entry. Add what is *different* in
  that language.
- A keyword the other list already has in this language (the Remote
  check's French keywords, when you write Stage 1's) can be reused where
  it fits.
- Cover every existing keyword's idea, not just the first few. A list a
  third the size of the original is usually missing things.
- For a `remote` item, also say which category each keyword belongs to
  (`category_of`, by the category `id` from step 2).

Write them as JSON to `.ftja-run/keywords.draft.json` (create `.ftja-run/`
if it is missing):

```json
[{"target": "stage1", "language": "fr", "keywords": ["prototypage", "maquette", "..."]},
 {"target": "remote", "language": "fr", "keywords": ["télétravail", "fuseau horaire", "..."],
  "category_of": {"télétravail": "remote_level", "fuseau horaire": "time_zone"}}]
```

One entry for every item `begin` printed, and only those.

## 4. Hand them to the user

```
venv/bin/python -m ftja.keywords propose --file .ftja-run/keywords.draft.json
```

If it prints `Not accepted: ...`, fix what it names and run it again. Then
delete the file you wrote. The web view opens the keywords for the user to
go through; they are added to the lists when the user confirms there.

## 5. Report

Tell the user, in their language and in two or three lines: which lists
and languages you wrote keywords for, how many each, that the web view has
opened them to confirm (Pipeline tab if their web view is closed), and
that their existing keywords are untouched. If `gaps` showed other
languages or lists still without keywords that this request did not cover,
name them and say they can ask for those the same way.

If you were called from `/ftja-run`'s wait (`{"status": "keywords"}`), go
back to that wait afterwards.
