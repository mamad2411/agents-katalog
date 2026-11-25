---
name: course-builder
description: >-
  Compose a structured, tutor-ready course from YouTube URLs, local documents/notes, and/or a bare
  topic: a course folder in the repo (default courses/{slug}/) with an index (objectives, lesson
  list, concept map), numbered lesson files, a tutor-facing assessment bank (free-recall probes +
  rubrics per concept), and a practicum spec, plus an optional compiled single-file HTML version.
  Honest provenance, no filler, and a bundled checker that must pass before the course is done.
  Use when the user says "build a course", "make a course from these videos", "turn these notes
  into a course", "turn this topic into a course", "create a curriculum/learning path for X", or
  wants material structured so a tutor skill (e.g. teach-me) can quiz them and track progress.
---

# Course Builder

Turn source material into a course a person can study from and a tutor can teach from. The
course is plain Markdown in the user's repo, in a precisely defined folder format
(`references/course-format.md`), so other skills can find it, quiz on it, and track progress
through it without guessing.

Three input doors, freely mixed — a mix makes the richest course:

- **URLs**: YouTube videos (transcripts extracted per video).
- **Documents**: local files or folders — notes, docs, PDFs, code.
- **Topic**: a subject with no sources; built from the repo, the web (if available), and
  honestly labelled general knowledge.

At least one is required.

## What gets written

```
courses/{slug}/            <- default root; the user may name another
  index.md                 course map: objectives, lessons, concept map, provenance
  01-{lesson}.md ...       lessons, prerequisite order
  assessment.md            tutor-facing: one probe + rubric per concept
  99-practicum.md          what a practical task must prove (never a fixed target)
  course.html              optional: compiled single-file reading version
  sources/                 optional: cleaned transcripts captured during the build
  progress.md              RESERVED: tutor / practicum runner (never written here)
  practicum/               RESERVED: practicum attempts (never written here)
```

`progress.md` and a `practicum/` sub-folder in the same course folder are reserved for the tutor
and practicum runner. **This skill never creates, edits, or deletes them** — including when
rebuilding or extending.

Bundled scripts (Python 3 stdlib only), in this skill's `scripts/` folder. Commands in this
skill are written to run **from the repo root** with the skill installed at
`.claude/skills/course-builder/`; for a user-level install substitute
`~/.claude/skills/course-builder/`.

| Script | Purpose |
|---|---|
| `scripts/check_course.py <course-dir>` | Validates the folder against the format. Must print `OK` before the course is done. |
| `scripts/compile_html.py <course-dir>` | Writes `course.html`: one file, inline CSS, no external requests, assessment excluded. |
| `scripts/vtt_to_text.py <file.vtt>` | Cleans auto-caption subtitles into de-duplicated transcript text with `[mm:ss]` markers. |

`examples/spaced-repetition/` is a small complete course that passes the checker — read it
once before writing your first course.

## Procedure

### 0. Scope the build (one question, once)

From the inputs, derive a working title, a slug, and a level. Then confirm in **one** question
(use a structured multiple-choice question tool if available, otherwise one plain message):

- title and slug;
- depth: `intro` (orient a newcomer), `intermediate` (working competence), `advanced`
  (edge cases and trade-offs);
- output root, if the default `courses/` is not obviously right (e.g. the repo already keeps
  learning material elsewhere — then default to that).

Do not re-ask per video or per document. If a video-analysis skill has its own focus questions,
answer them yourself: "frameworks and techniques, detailed". If the session is non-interactive,
pick sensible defaults, state them in the final report, and proceed.

If a course with that slug already exists, this is an **extend**, not a build — see
"Extending an existing course".

### 1. Gather

Follow `references/sources.md`. The essentials:

- **Reuse before re-extraction.** Before extracting a video or re-reading a large doc set,
  check for an earlier extraction of the same source (an existing course's `sources/`, notes
  in the repo naming the video id). Harvest from it instead of paying twice.
- **URLs:** if a video-analysis skill such as `youtube-to-artifact` is installed, use its
  extraction steps per URL (skip its own page output — the course is the output). Otherwise
  extract transcripts directly: `yt-dlp` if on PATH, else the `youtube_transcript_api` Python
  package if importable, else ask the user to paste the transcript. With yt-dlp, request
  `--sub-langs "en,en-orig"` (never a regex) and judge success by the `.vtt` file existing,
  not the exit code. Clean VTT with `scripts/vtt_to_text.py`. Never infer a video's content
  from its title.
- **Documents:** read fully; cite by path; list anything unreadable.
- **Topic:** repo material first, then web search if the tools exist, then general knowledge
  cited as the literal source `model-knowledge`.

Output of this step: for each source, the frameworks, principles, techniques, worked examples
and anti-patterns it contains, with where each came from.

### 2. Plan

Per `references/authoring.md`:

1. 3-6 **observable** course objectives, ids `O1..On`.
2. The concept list: one probe-able idea each, kebab-case ids. Mark the 1-2 threshold concepts.
3. 4-8 lessons (2-12 hard limits), prerequisite-first, 2-4 concepts each, each concept in
   **exactly one** lesson, each lesson serving at least one objective.
4. For each lesson: the sources it draws from. A lesson backed only by `model-knowledge` in a
   course meant to come from the user's material is flagged, not hidden.

Show the plan in a few lines (lessons + one-line goals) as you proceed; the user may redirect.
Do not stop to wait for approval unless the material clearly does not support the requested
course (then say so and ask).

### 3. Write the course files

In `{root}/{slug}/`, exactly as `references/course-format.md` specifies:

1. **Lessons** `01-...md` onward: frontmatter; `Why this matters`, `Core ideas` (one
   ``### Name (`concept-id`)`` per concept), `Worked example`, `Common mistakes`, `Recap`,
   `Check yourself` (questions only, no answers).
2. **`assessment.md`**: one `## concept-id` entry per concept — `lesson`, `weight`, a
   free-recall `probe`, 2-5 `must_include` rubric points, optional `misconceptions` and
   `transfer`. Apply the alignment test to every entry: answer the probe alone as a strong
   learner would; every rubric point must appear in that answer.
3. **`99-practicum.md`**: concepts under test, acceptance criteria (runnable checks beat prose),
   shape of a good task, anti-tasks. **Never a concrete target** — a target fixed now is stale
   when the learner sits down; the practicum runner picks real candidates at that time.
4. **`index.md`** last, when the lesson list and concept map are final: frontmatter (`sources`
   = everything actually read, nothing else), about, objectives, prerequisites, lesson links,
   concept map (`- NN: id, id`), optional concept dependencies, practicum link, and an honest
   **Provenance** section: which lessons came from which sources, reused vs freshly extracted,
   and anything that shipped short.

### 4. Verify (hard gate)

```
python .claude/skills/course-builder/scripts/check_course.py {root}/{slug}
```

Fix every `FAIL` and re-run until it prints `OK`. Then do the read-through in
`references/authoring.md` ("Final read-through"). The checker proves structure, not quality —
both are required.

### 5. Compile HTML (optional, default on)

Unless the user declined it:

```
python .claude/skills/course-builder/scripts/compile_html.py {root}/{slug}
```

`course.html` is derived: regenerate it after any change, never hand-edit it. It leaves out
`assessment.md` so reading the course never spoils the quiz. Open it or report its path; it
works offline and prints cleanly.

### 6. Optional: learning-engine registration

If the engram plugin is installed, register the course as a topic per `references/engram.md`
(register only — never start a study session from a build) and set `engram_topic:` in the
index. If it is not installed, leave `engram_topic: none` and move on.

### 7. Report

Lead with the result, then decisions:

- course title, path, lesson count, concept count, checker `OK` line, HTML path if built;
- what each lesson came from when it varied (reused vs freshly extracted, docs vs video);
- anything that shipped short and why (missing captions, unreadable file, stalled fetch);
- the next step: study it with a tutor skill if one is installed (e.g. `/teach-me {slug}`),
  or read `course.html`.

End in one of these states, and name it:

| State | Meaning |
|---|---|
| `built` | Every source extracted, checker OK |
| `built-short` | Checker OK, but some sources failed — gaps named in Provenance |
| `blocked` | No usable input (every source failed, or nothing given) — no course files written |
| `needs-decision` | The material does not support the requested course; question asked, nothing written |

## Extending an existing course

"Add these videos to my X course" is an extend:

- Read the existing index, lessons and assessment first.
- **Append** new lessons as the next numbers. Never renumber lessons or rename concept ids once a
  `progress.md` exists — that silently breaks the learner's record. If the material demands a
  real restructure, propose a new course with a new slug instead.
- New material that deepens an existing lesson may be added to that lesson (and new concepts to
  its concept-map line), with matching assessment entries.
- Update `sources`, `lessons`, `updated`, the lesson list and Provenance; re-run the checker;
  recompile `course.html` if it exists.
- If two existing courses could be the target, ask which; do not guess.

## Guard rails

- **Never invent provenance.** `sources:` lists only material opened and read in this build.
  Knowledge from training is `model-knowledge`, never an attributed citation.
- **No filler.** When sources run out or an extraction fails, ship the course from what was
  extracted and say so in Provenance. Short and honest beats long and padded.
- **Bounded work.** Retry a failing fetch once, then move on. A course build does not turn into
  an open-ended research project; if the topic needs that, say so and ask.
- **Stay in the course folder.** Writes go to `{root}/{slug}/` only. `progress.md` and
  `practicum/` are never touched. The user's own documents are read, never modified or moved.
- **Format is a contract.** Other skills parse these files. Do not add creative variations to
  headings, frontmatter keys or the concept-map line grammar; put creativity in the teaching.
- **The checker is not optional.** A course that has not printed `OK` is not done, whatever it
  looks like.
