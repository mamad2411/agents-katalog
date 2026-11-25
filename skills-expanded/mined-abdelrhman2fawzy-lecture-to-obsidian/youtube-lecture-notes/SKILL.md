---
name: youtube-lecture-notes
description: Turn a YouTube lecture (URL or pasted transcript) into an Obsidian study note with LaTeX math, callouts, timestamp links, board equations read from video frames, honest confidence markers, and review questions that can go to a spaced-repetition queue. Use when the user shares a lecture link or transcript and wants notes, or asks to resolve the ❓ markers in an existing lecture note.
---

# YouTube lecture → Obsidian note

The user reviews and edits a ready-made note instead of writing notes while
watching. Accuracy beats completeness: never present a guess as lecture
content.

Scripts live in `scripts/` next to this file. Run them with `python3 -I`
(`python` on Windows). Use a fresh temporary folder per video as WORKDIR.
Python standard library only; external tools are yt-dlp (required), ffmpeg
and deno/node (for frames).

## 0. Settings

Run `scripts/config.py show`. Keys are explained in
[references/config.md](references/config.md). Then:

- `vault` empty → `scripts/config.py vaults`. One vault: use it. Several:
  ask once which one, then offer to save it with
  `scripts/config.py set vault "<path>"`. None: ask where notes should go.
- First run on this machine, or a tool fails → `scripts/doctor.py` and pass
  on its fix lines.
- `note_language: auto` → write in the language the user writes to you in.
  Keep technical terms and symbols as the lecturer uses them.

## 1. Get the transcript

- Pasted transcript → use it; skip to step 3.
- URL → `scripts/fetch_transcript.py URL WORKDIR --lang "<sub_langs>"`.
  It ignores playlist parameters, prefers manual subtitles over
  auto-captions, and writes `meta.json` (title, duration, chapters,
  description, `subs_lang`) plus a cleaned, minute-stamped `transcript.txt`.
  With no track in `sub_langs`, it takes the lecture's own language instead
  of YouTube's machine translation. If YouTube asks to sign in, retry with
  `--cookies-from-browser chrome`.
- Check the description in `meta.json` for slides or PDF notes. When they are
  reachable they are a better source for equations than frames.
- No shell, no network, or no subtitles → say so plainly and ask the user to
  paste the transcript (YouTube: "Show transcript", copy). Never write
  lecture content from the title or from memory.

## 2. Learner context (only if `study_records_dir` is set)

Search that folder for the lecture's main topics (a few keywords, not the
whole history) and collect at most four relevant facts: an open gap, a
recorded misconception, an overdue review item, an earlier note on the same
idea. These feed the "For you" callout in step 3. With nothing relevant,
skip the callout. Never invent learner history.

## 3. Write the note

Read the whole transcript first. Lectures over about an hour: write it in
~30-minute chunks, then merge and renumber.

Follow [references/note-format.md](references/note-format.md): file name,
frontmatter, summary, timestamped `##` sections, callouts, worked examples,
in-class exercises, wikilinks to notes that already exist in the vault, and
the review questions section.

**Translate.** The whole note is in the note language. Translate anything in
another language: a foreign-language transcript (`subs_lang` differs), passages
where the lecturer switches language, slides, frames, and the video title in
the H1 (keep the exact title in frontmatter `title`). Translate the meaning,
not word by word. Leave math, code, symbols and names as they are. On a
term's first use, give the original in parentheses, e.g. *eigenvalue
(Eigenwert)*, so the user can match it to the audio. A phrase you cannot
translate with confidence gets `[❓ check term, mm:ss]`. Never translate a
quotation silently: mark it `(translated)`.

Mark every piece of math with its confidence tier:

| Tier | Marker | Use when |
|---|---|---|
| heard or seen | none, or `[🖼 from frame, mm:ss]` | said clearly, or read from a frame or slide |
| reconstructed | `[🔁 reconstructed from spoken arithmetic, mm:ss]` | rebuilt from spoken steps **and every step checks** |
| unknown | `[❓ check equation, mm:ss]` / `[❓ check term, mm:ss]` | anything else. Do not guess |

- The lecturer says one thing and means or writes another → a
  `> [!warning] Lecturer slip` callout with the correct version.
- No theorems, proofs or examples that are not in the lecture. Helpful extras
  go in `> [!question] Suggestion (not from the lecture)`, or nowhere.
- Fix misspelled names and terms only when confident; otherwise mark `❓`.

## 4. Resolve board content from frames

Skip if `frames.enabled` is false, or doctor reports no ffmpeg or JS runtime.

Collect every `[❓ ...]` timestamp and run
`scripts/grab_frames.py URL WORKDIR/frames <mm:ss> ... --offsets 0,30,60 --height <frames.height>`
(add `--delete-video` unless `frames.keep_video`). Writing usually lags
speech, so check later offsets too. For a finished result, grab the end of
the segment. Read the images:

- Replace a marker only with what the frame clearly shows, tagged
  `[🖼 from frame, mm:ss]`.
- Re-check spoken and reconstructed values against the board. Frames catch
  your own transcription errors.
- Unreadable or missing → keep the `❓`.

For an existing note ("resolve the markers in …"), do only this step and
step 5.

## 5. Validate

`scripts/validate_note.py NOTE.md --duration <seconds>` checks frontmatter,
that `open_markers` matches the `❓` count, timestamp links (same video,
in order, within the duration), balanced `$`/`$$`, and the review questions.
Fix and rerun until it prints `OK`.

## 6. Series index

If the note has a `course`, create or update `<notes_dir>/<course> - index.md`
with one line per episode, in order:
`- [[<note>|epNN]] · <one-line summary> · <status>`. Add
`Previous: [[…]] · Next: [[…]]` under the H1 of neighbouring episodes.

## 7. Integrations (each only if configured)

- `material_log` → `scripts/log_material.py NOTE.md` adds one line to the
  configured log, in the configured section. A note is study material, not
  proof of learning: don't record progress or mastery from it.
- Review queue → propose 3–6 questions covering the core ideas with
  `scripts/export_review_questions.py NOTE.md --topic <topic> --prefix "<label>" --only 1,4,…`
  (a dry run). Show the batch. Run again with `--apply` **only after the user
  confirms**. Destinations are in [references/config.md](references/config.md).
- `tutor_skill` → offer a short quiz on the lecture with that skill.

## 8. Sharing on GitHub (only when asked)

Obsidian callouts, wikilinks and `$$` blocks render poorly on GitHub. When the
user wants to publish a note there, run `scripts/export_github.py NOTE.md`. It
writes `NOTE.github.md` and leaves the vault note unchanged.

## 9. Finish (2–4 lines)

Say where the note is, how many markers frames resolved, which `❓` remain
(with timestamps), and the proposed review batch if any. Don't recap the
steps.
