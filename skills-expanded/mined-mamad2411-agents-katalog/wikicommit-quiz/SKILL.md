---
name: wikicommit-quiz
description: Generate a quiz from wiki content, with adjustable difficulty
---

# wikicommit-quiz

A `wikicommit-ask`-derived skill that generates a difficulty-adjustable quiz from the content of `.wikicommit/entity/` and outputs it into the conversation. When `--topic` is given, gathering related pages is delegated to the shared script `.wikicommit/scripts/search_index.py` (the same call used by p3-006 `wikicommit-search`). It never writes to the filesystem.

## Usage

```
/wikicommit-quiz [--topic <keyword>] [--difficulty=easy|medium|hard]
```

- `--topic <keyword>`: if given, generate the quiz from pages related to that keyword (if omitted, sample randomly from the whole wiki)
- `--difficulty`: one of `easy` / `medium` / `hard` (default `medium`)

## Processing Flow

### Step 1: Gather Target Pages

Branches depending on whether `--topic` is given.

#### With `--topic`

```bash
python .wikicommit/scripts/search_index.py query "$(cat <<'EOF'
<topic>
EOF
)" --limit 10
```

Pass the topic through a quote-delimited heredoc (`docs/DesignDoc-skills.md` §11.7), not a plain double-quote embedding — `--topic` is free-form user text with no upstream validation, and a plain `"<topic>"` embedding would let shell metacharacters (`` ` ``, `$(...)`) in it be evaluated by the shell when this command line is assembled, regardless of the downstream script (Issue #398).

On exit code `1` (failure, with an `ERROR:` line printed), display that error message as-is to the user and stop (e.g. SQLite doesn't support trigram, or `.wikicommit/entity/` doesn't exist).

Collect the `MATCH:` lines (`path` / `title` / `type` / `lang` / `review_status`). If the `hits` value in the `SUMMARY: query="...", hits=<N>` line is `0`, display "No pages related to \"<topic>\" were found" and stop.

#### Without `--topic`

1. Read `.wikicommit/config.yml` and get `translation.primary_lang`. If `.wikicommit/config.yml` doesn't exist, display an error, guide the user to run `/wikicommit-init`, and stop.
2. Scan `.wikicommit/entity/<primary_lang>/**/*.md` and build a list excluding `index.md` and pages with `status: removed`.
3. Randomly sample 5–10 pages from the list (not scripted, since this isn't deterministic — the agent performs the random selection).
4. If fewer than 5 target pages exist, proceed with however many exist. If there are zero, display "No pages available to generate a quiz from" and stop.

### Step 2: Fetch Page Content

Read each page gathered in step 1 with the Read tool and add its body (excluding frontmatter) to the LLM's context.

### Step 3: Generate the Quiz

Vary the question format based on `--difficulty`. **Do not include claims in the quiz or explanations that aren't in the gathered body content** (hallucination prevention).

- `easy`: one Q&A per page, asking about the `title` and basic facts of a single page. One question per page.
- `medium`: multiple-choice (4 options) questions spanning connections across multiple pages. Build incorrect options from within the gathered body content as well.
- `hard`: free-response questions about relationships and chronology between pages connected via WikiLink. If no WikiLink (`[[Type/slug]]`) is found among the gathered pages, switch to questions about chronology within a gathered page (dates, the order of events).

Aim for around 3–5 questions depending on the number of gathered pages (`easy` is one question per page, but if there are more than 5 gathered pages, narrow it down to a representative 5). Prepare the full question/answer/source set up front, but do not reveal it yet — questions are presented one at a time (Step 4).

### Step 4: Present One Question at a Time

This is a self-test: the user must not see the correct answer before answering. Output only the current question — never the answer or the grounding page path — then wait for the user's response before continuing.

```
Q1. <question text>
(medium only)
  A. ...
  B. ...
  C. ...
  D. ...
```

Never write to a file.

### Step 5: Interactive Grading and Progression

When the user answers the current question, grade it and reveal, for the first time, whether it's correct, an explanation (quoting the relevant part of the grounding page), and the grounding page path. If incorrect, also show the correct answer.

```
✅ Correct! (or ❌ Incorrect. Correct answer: <correct answer>)
<explanation quoting the relevant part of the grounding page>
Source: .wikicommit/entity/ja/Person/yamada-taro.md
```

Then present the next question (back to Step 4's format) until all prepared questions have been asked. After the last question, show a final score summary (e.g. `3/5 correct`) and end.

## Notes

- Never write to the filesystem (including `.wikicommit/exports/`), and never commit or create a PR against `main` or any branch
- Do not write to `.wikicommit/schema/`
- Do not include claims in the quiz or explanations that aren't in a gathered page's body content (hallucination prevention; see step 3)
- This skill itself has no side effects. However, when `--topic` is given, the `search_index.py` call automatically runs `build` if the index file (`.wikicommit/.cache/search_index.sqlite3`, not tracked by Git) doesn't exist
