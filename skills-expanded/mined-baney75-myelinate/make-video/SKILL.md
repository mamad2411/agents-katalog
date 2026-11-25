---
name: make-video
description: "Use when asked to make a teaching video, animated lesson or explainer to learn a topic, or to turn slides into one. Finding one: find-media. Not app demos, intros or edits."
---

# Make video

A teaching video a learner watches, pauses and answers. You do not draw, animate or judge truth. You write one lesson file. Code does the rest: a checker matches every quote to its source file, recomputes every number, finds sources that disagree and prints numbered fixes. A fixed player turns the file into a narrated, animated video with captions, chapters, sources and questions that wait for an answer.

Paths like `templates/…` and `scripts/…` are relative to this skill's folder, which carries its own copy of every file it names. Other Myelinate skills are siblings (`../find-media/SKILL.md`). If a file is missing from your copy, follow this file: it is enough on its own.

**Stand down when it isn't wanted.** A demo of an app, a vlog edit, a YouTube intro or a trailer is not this skill. To find an existing video, use `find-media`. To learn from a video they already have, use `video`.

Evidence and limits: names before process, narration with few words on screen and short segments follow Mayer's multimedia principles (*Multimedia Learning*, 3rd ed.; see `references/visual-teaching.md`); worked then faded examples follow Renkl et al. (2002) and questions during the video follow retrieval research (Roediger & Karpicke, 2006), both in `references/evidence.md`. No study has tested this player. Never say it raises grades.

## 0. Never

1. **Never invent** a quote, a source, a page number, a timestamp, a web address or a date.
2. **Never narrate a fact that is not in `claims` or `calc`.** Every fact sentence cites an id. A sentence with a number is a fact.
3. **Never write `"verification"`.** Only the checker writes it, signed with a hash of the file. The player shows "Unverified" for any file whose signature does not match.
4. **Never show an answer before its pause.** The checker refuses a pause whose answer is already on screen.
5. **Never deliver while the checker prints `NOT READY`.**
6. **Never for graded work.** A video that solves their homework or a take-home question does the work for them. Use `assignment`, and make the video about a parallel problem instead.
7. **Never a voice like a real person,** and never voice cloning. The credits always say the narration is an AI voice.

## 1. Ask once, then start

Send **one** message. Don't wait for the answer to start drafting.

**For a class**, ask for everything at once:

> To make this match your class, send whatever you have: your notes, the study guide, the slides, the syllabus, the textbook and its edition, past quizzes or exams, which formulas the exam gives you, and any symbols your professor uses. A lecture recording or its transcript helps too. And: what part confuses you most?

**For self-study**, ask: "What do you want to be able to do with this, and how much do you already know?"

If they have nothing, or don't answer, build it anyway from reliable outside sources (a textbook, a university, a government agency, a journal). The badge then says the video was not checked against their course. When their materials arrive, redo steps 3 and 5 against them.

Save each thing they give you as a plain text file in one folder, like `sources/notes.md` or `sources/slides.md`. Copy their text as it came: an uploaded file as is, a PDF through `pdftotext`, a pasted transcript pasted whole. A transcript with timestamps keeps them: lines like `[4:05] words said`. These files are what the checker reads.

If you have to type a source yourself (a photo of a slide, a page you can read but not save), name its file `typed-<name>.md`, like `sources/typed-slide-photo.md`. A quote matched only against your own typing proves nothing, so the badge says so.

If `debrief` or the learner named a question they missed, put it in `learner.target` and make that miss the video's misconception.

## 2. Choose the scope

1. Write 1 to 3 objectives. Each starts with a verb: Explain, Solve, Compare, Predict.
2. Write the one question the video answers.
3. Choose `lessonType`: `"problem"` if the learner must solve problems with steps (math, chemistry calculations, physics); otherwise `"concept"`.
4. **Six minutes or less per file.** For more, make several files, each with `"part": {"n": 1, "of": 3, "series": "<the whole topic>"}`. Each part is its own video with its own question, pauses, recall and practice.

## 3. List the claims first

Before any narration, list every fact the video will state. For **each claim**:

1. Find the line in a source file that says it.
2. Copy that line, letter for letter, into `"quote"`. Never fix its spelling, never shorten it in the middle. 40 words at most.
3. Write the file's name in `"file"`, exactly as it is in your sources folder.
4. Write where it is in `"where"`: the page, slide or section number for the learner's material (`"from": "course"`), the `m:ss` timestamp for a transcript, or the full `https://` address for anything else (`"from": "outside"`, plus `"checked": "YYYY-MM-DD"`, the day you read it). Save an outside page's text as a file too, with a tool that saves the page (a fetch or a download), so its quote can be matched. A page you typed goes in a `typed-` file.
5. A fact that changes over time (a price, a law, a record, a current number) also gets `"changes": true`.
6. **If no line says it, delete the claim.** Or find a reliable outside source and mark it `"from": "outside"`. On screen it shows as *outside your course*.
7. Use the course's own words and symbols. If the professor writes ΔH, write ΔH.

**When two sources disagree** (the checker finds these and tells you):

1. Keep both as claims, each with its own exact quote and file.
2. On the claim that disagrees, set `"status": "conflict"`, `"other": "<the other claim's id>"` and a `"note"` saying what each source says.
3. Add a beat that cites both ids and says it plainly: "Your slides say X. Your textbook says Y. Ask your professor which one the exam uses."
4. If the checker flags a sentence that does not really disagree (it is about something else), copy at least 5 words in a row from that sentence into the claim's `"notConflict": ["..."]`. The badge counts every one you dismiss.

## 4. Every number gets a calc

Never type a computed number by hand. For each one, add a `calc` entry. The checker recomputes it and stops on any slip.

```json
"calc": [
  {"id": "k1", "expr": "(2*90 + 80) / 400", "value": 0.65},
  {"id": "k2", "expr": "1 - k1", "value": 0.35},
  {"id": "k3", "expr": "k1**2 * 200", "value": 84.5, "round": 1}
]
```

- `expr` uses numbers from your quotes, `+ - * / ** ( )`, `sqrt()`, and the ids of earlier calcs.
- `value` is the result you will say; `round` is how many decimal places you say.
- A sentence or screen item that says the number cites the calc id, like `"claims": ["k3"]`.

## 5. Write the scenes

Copy `templates/video-lesson.json` and replace every `<<...>>`. The complete example `examples/video-lesson-sky.json` shows a finished lesson. Build the scenes in this order:

| Scene `role` | What it does |
| --- | --- |
| `intro` | A hook and the question. Show a `title`, then a `question`. |
| `names` | A pause that asks them to predict, then each new word: one `term` per word. |
| `explain` | The idea, one step per sentence. |
| `worked` | **Problem lessons:** solve one problem, one `step` per sentence. |
| `faded` | **Problem lessons:** a similar problem. Show the first steps, then a pause asks for the next step. |
| `example` | **Concept lessons:** apply the idea to one concrete case. |
| `misconception` | Name the common mistake, then correct it. Use `compare`. |
| `summary` | The whole chain in 3 to 5 short `step`s. |

Each beat is **one** of these:

- `{"say": "One short sentence.", "claims": ["c3"], "show": [ ... ]}` for a fact.
- `{"say": "A question, an instruction or a transition.", "talk": true}` for words that state no fact.
- `{"pause": {"ask": "...", "choices": ["...", "..."], "answer": "...", "why": "...", "claims": ["c3"]}}` for a question. Leave out `choices` to have the learner type an answer.

Rules (the checker enforces 1 to 6; check 7 and the predict-first part of 2 yourself):

1. Sentences of 22 words or fewer. Never more than 30.
2. A pause at least every 120 seconds of narration; aim for every 60 to 90. **Ask them to predict before you explain:** the pause comes first, the answer after.
3. The screen shows key words, never the sentence being said. 40 words on screen per scene at most.
4. **Say symbols as words.** The voice reads `say` aloud: write "p squared", "equals", "divided by", "delta H". Put the symbols on screen in an `equation` or `step`.
5. `wpm` from 130 to 160. Use 145.
6. End with `recall` (look away and explain it) and `practice` (one new problem like the one taught).
7. Something appears on screen when the narration names it, in the same beat.

**A word the voice may say wrong** (a name, a technical term) goes in `"pronounce": {"heterozygote": "hetero zygote"}`. Respell with plain words or word parts split by spaces, like "a leel" for allele. Hyphens and capitals made one voice break a word apart. It changes only what the voice reads; the captions keep the real word.

**Mark what to memorize.** A `term`, `equation`, `label` or `step` can carry `"tier": "memorize"` (not given on the exam) or `"tier": "given"` (on the formula sheet). Use it only when their materials say so.

Things you can `show`:

| `type` | Fields | Use it for |
| --- | --- | --- |
| `title` | `text`, `sub` | The opening card |
| `question` | `text` | The question the video answers |
| `term` | `word`, `meaning`, `tier` | A new word, before you use it |
| `label` | `text`, `tier` | One key phrase |
| `equation` | `text`, `claims`, `tier` | Typed math: `x^2`, `v_0`, `\Delta H`, `sqrt(x)`, `->` |
| `step` | `text`, `tier` | One line of a worked solution or a chain; steps stack |
| `arrow` | `from`, `to`, `label` | Cause and effect, input and output |
| `compare` | `left`, `right`, `leftItems`, `rightItems` | Wrong idea and right idea; two cases |
| `table` | `title`, `columns`, `rows`, `claims` | 2 to 5 columns. Start with `"rows": []` to fill it one row per beat |
| `row` | `cells` | Adds one row to the table already on screen in this scene |
| `bars` | `title`, `items` (`{"label", "value"}`), `unit`, `claims` | Compare 2 to 6 amounts |
| `graph` | `title`, `x`, `y`, `points`, `mark`, `claims` | Data. Compute every point; never guess one |
| `quote` | `text`, `claim` | A short exact quotation from a claim |
| `image` | `src`, `alt`, `credit`, `license`, `link` | A licensed figure that teaches; never decoration |
| `highlight` | `target` | Underline something already shown in this scene |

## 6. Run the checker, fix, repeat

<!-- local-tools -->
```sh
python3 scripts/video_check.py lesson.json --sources sources/
```

It prints numbered problems, each with a **Fix:** line. Fix exactly what it says, in order, then run it again. Change only the lines it names and keep every other scene and beat: a lesson with fewer scenes is not a better one. Never stand in for a part with `...`. Repeat until it prints `READY`. Never stop while it prints `NOT READY`. Always give `--sources` when you have any source files: without it, nothing is matched and the badge says *Unverified*.

What it checks: every quote is in the file it names; every timestamp is within 20 seconds of its quote; every calc is right; every number said or shown comes from a cited quote or calc; every cited claim shares key words with its sentence; every sentence in the sources that says the opposite of a claim is flagged in the video.
<!-- /local-tools -->

With no shell, check the file yourself against steps 3 to 5, one rule at a time, and say the checker did not run. The video then shows *Unverified*.

## 7. A second reader checks the explanations

Code can match quotes and numbers. It cannot judge whether an explanation teaches the right idea. Before you deliver:

1. Give a second reader that did not write the lesson (the `key-worker` agent, or the `verify` skill run in a fresh agent or another model) the claims with their quotes, every `say` line with the claims it cites, every `talk` line, all screen text, every pause with its answer, `misconception`, `recall` and the practice problem **without its answer**. It works the problems itself and answers two questions for each sentence: does it say only what its claims' quotes say, and does each `talk` line state no fact?
2. Fix everything it finds. Delete what can't be fixed.
3. Only then add, with its real name and today's date:

```json
"review": {"by": "key-worker agent", "date": "2026-11-22", "result": "pass", "notes": "Worked the 3 pauses and the practice; all match."}
```

4. Run the checker with `--final`. It fails without `--sources` and without a passing review.

If you are the only reader, you are not a second reader: leave `review` out and build **without** `--final` (step 9). The badge then says *Explanations not independently reviewed*. Say so in your reply too. Never write a review that did not happen.

## 8. Narration voice

Read `references/narration.md` before writing the `say` lines: it says how to write for the ear.

The player tries voices in this order and the credits name the one that played:

1. **Recorded clips in the lesson** (best). Make them with one of:
   - **A text-to-speech tool from your host.** Run `python3 scripts/video_check.py lesson.json --audio-plan`. For each line, make speech from its `read` text and save it as `audio/<clip>`. Then add `"audio": {"clips": {"<clip name without .mp3>": "audio/<clip>"}, "voice": {"engine": "<tool>", "name": "<voice>", "disclose": "Narration is an AI voice: <tool> (<voice>)."}}`.
<!-- local-tools -->
   - **A voice engine on this machine:** `python3 scripts/video_voice.py lesson.json` picks the best engine it finds (a command or server the learner names, a local Kokoro or Piper, then Kokoro in a headless browser), makes one clip per line, levels them and writes `audio` into the lesson, with each clip's length. The player times every line to its clip, so run the checker again afterward: the real length can pass 6 minutes. It never installs anything. `--sample 30` makes a 30-second sample first.
   - **Check the clips:** `python3 scripts/voice_check.py lesson.json` transcribes each clip back and checks it says its caption, at 130 to 165 words a minute, at an even loudness, with no long silences, in one voice. Fix what it prints and run it again.
<!-- /local-tools -->
2. **Kokoro in the learner's browser**, when the page may download it. The player offers it on a button. A claude.ai artifact blocks that download, so a video published there needs recorded clips, published as files next to the page.
3. **The browser's built-in voice**, labeled a robotic fallback. Captions show either way.

A changed sentence gets a new clip name, so a stale clip never plays; the checker lists clips that no longer match.

## 9. Build and deliver

<!-- local-tools -->
**With a shell:** `python3 scripts/video_check.py lesson.json --sources sources/ --build video.html` signs the lesson and writes the finished video (it refuses while there are problems). Add `--final` only when step 7 recorded a real review; without one, `--final` refuses. Open it, play the first minute, answer one pause, and look at it at phone width. Then publish it where the learner can open it, or give them the file.
<!-- /local-tools -->

**With files but no shell:** copy `templates/video-player.html` and replace only the JSON between `<script type="application/json" id="lesson">` and `</script>`. Write every `<` inside the JSON as `\u003c`. Never edit the rest of the page. It shows *Unverified*, because only the checker can sign it.

**With no files at all** (this skill was pasted into a chat): give the lesson JSON in one code block, and tell the learner to paste it into the Myelinate video player page (listed in the Myelinate README). Under it, give the same lesson as a read-along script: each chapter title, each sentence, and each pause question with its answer below a line, so they can learn from it right away.

<!-- local-tools -->
**MP4.** When the learner wants a video file and the machine already has Playwright and ffmpeg (never install them for this): `python3 scripts/video_export.py video.html video.mp4`. It renders frame by frame, adds the clips, checks the file with ffprobe and writes a contact sheet of frames. Look at the contact sheet before you send it. The MP4 cannot wait for answers: it shows each pause, holds it, then shows the answer.
<!-- /local-tools -->

## 10. Say exactly what state it is in

End your reply with one line:

- **prepared**: the file is written; the checker did not print READY with `--sources`.
- **checked**: the checker printed READY with `--sources`, so every quote matched and every number was recomputed. No second reader passed the explanations: say so.
- **reviewed**: the checker printed READY with `--sources --final`, so a second reader also passed the explanations.
- **tested**: you also opened the video and played it.

Then: what was checked against the learner's own materials and what was not, and which voice narrates it.

## 11. A small complete example

This is `examples/video-lesson-sky.json` cut down to one claim and two scenes. The full file has 11 claims, 6 scenes, recall and practice, and its source text is in `examples/video-lesson-sky-source.md`. Copy its shape, never its words: your lesson is about your learner's topic, and the checker flags any sky sentence your materials never say.

```json
{
  "format": "myelinate-video/1",
  "title": "Why is the sky blue?",
  "subtitle": "And why sunsets turn red",
  "lessonType": "concept",
  "wpm": 145,
  "learner": {"kind": "self-study", "purpose": "Understand everyday light and color", "level": "Curious adult, no physics background", "materials": []},
  "objectives": ["Explain why air makes the daytime sky look blue", "Use the same idea to explain red sunsets"],
  "question": "If sunlight looks white, why is the sky blue?",
  "claims": [
    {"id": "c3", "text": "Blue light waves are shorter than red light waves.", "from": "outside",
     "source": "NASA Space Place, Why Is the Sky Blue?", "file": "video-lesson-sky-source.md",
     "where": "https://spaceplace.nasa.gov/blue-sky/en/", "checked": "2026-11-22",
     "quote": "Blue light waves are shorter than red light waves."}
  ],
  "scenes": [
    {"id": "s1", "title": "The question", "role": "intro", "beats": [
      {"say": "Look up on a clear afternoon and the sky is blue.", "talk": true,
       "show": [{"type": "title", "text": "Why is the sky blue?", "sub": "And why sunsets turn red"}]},
      {"say": "So where does the blue come from?", "talk": true,
       "show": [{"type": "question", "text": "If sunlight looks white, why is the sky blue?"}]}
    ]},
    {"id": "s2", "title": "Three words first", "role": "names", "beats": [
      {"pause": {"ask": "Predict before you hear it: which color has the shorter waves?", "choices": ["Red", "Blue"], "answer": "Blue",
                 "why": "Blue light waves are shorter than red light waves.", "claims": ["c3"]}},
      {"say": "Each color travels as a wave, and blue waves are shorter than red ones.", "claims": ["c3"],
       "show": [{"type": "term", "word": "Wavelength", "meaning": "Length of one wave. Blue short, red long."}]}
    ]}
  ]
}
```

The pause asks them to predict before the answer is said or shown. The screen then shows *Wavelength* and a ten-word meaning while the voice says the full sentence. The claim's quote is copied exactly from the file it names, and there is no `verification` block: the checker adds that.
