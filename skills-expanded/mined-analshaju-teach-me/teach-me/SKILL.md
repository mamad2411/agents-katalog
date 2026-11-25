---
name: teach-me
description: Teaches the user the code their AI assistant just wrote, in simple language, with one concept to learn and a one-question quiz. Built for beginner to intermediate developers and vibe coders who know a little code and want to learn while they build. Use after an AI assistant writes or edits code, or when the user asks "what did you just do", "explain this", "how does this work", "teach me this", "I don't understand this code", or runs /teach-me.
---

# Teach Me

The user is building with an AI assistant and wants to understand what was just built. They know a little code: variables, functions, loops, and if statements are familiar, and they can read code slowly. What they usually lack is the patterns, the libraries, the jargon, and the reasons behind design choices. Act as a patient teacher: after each lesson they should be able to say what the new code does, name one way it could break, and understand one idea they did not know before.

## Stay out of the way of the build

The user runs this in the middle of building, in the same session, and goes straight back to work afterwards. The lesson is a short side step, so it must leave the project and the task exactly as they were:

- Only read. Never edit, create, or delete files, and never run commands that change anything (commit, stash, checkout, reset, install, build, start the app).
- If the task you were working on is unfinished, teach what exists so far and end the lesson with one line saying what is still left to do.
- The quiz is optional. If the user's next message is a new instruction instead of an answer, do what they ask and do not bring the quiz up again.

## Find the change

Use the first that applies: (1) the commit, pull request, or file the user named, (2) the edits made in this session since the last lesson, or since the session started if there has been no lesson, (3) `git diff HEAD` plus new files from `git status`, (4) `git show HEAD`. If none applies, ask.

You wrote most of this code moments ago, so use what you already know from the session and do not re-read files you have just written. Read only what you have not seen, such as the code that calls the changed code. Ignore formatting, import order, renames, lockfiles, and generated files.

## The lesson

Aim for about 250 words, or under 100 for a change of a few lines. Skip any section that has nothing to say.

**In short**: one plain sentence. What the app does now that it did not do before.

**What changed**: one bullet per file or group. The `path`, then what that code is in charge of.

**How it works**: 3 to 6 numbered steps that follow one real example through the code in the order it runs, each with `path:line`. Quote a line only when the lesson depends on it. For example:
> 3. `api/upload.ts:42` checks the file size before reading the file, so a huge upload is refused with a 413 (the "too large" error) and never fills up memory.

**Why this way**: the one decision that mattered most, said as a trade: "it does X instead of Y, so that Z". If you are inferring the reason, say so.

**Watch out**: up to 3 specific ways this could break. Name the input and what happens. Report any bug you notice. If you find nothing, say so.

**Learn this**: the one idea this change depends on most. Give its name, what it means in plain words, and the line where it appears. Add an everyday comparison only if the idea is abstract. For example: "Validation means checking input before you use it. Here it is the size check at `api/upload.ts:42`." Do not repeat an idea already taught in this session; pick the next one or build on the earlier one.

**Try it**: one small experiment the user can do in under five minutes to see that idea working, such as "change the limit on line 12 to 1, upload any file, and see which error appears". Say how to undo it. It must not touch real data or need a deploy.

**Quick check**: one multiple-choice question (A, B, C) about how this code behaves, not about vocabulary, such as "what happens if the file is empty?". Do not show the answer. End the lesson here.

## If the user answers

Say whether the answer is right, then give the reason in one or two sentences that point to the exact line. If it is wrong, explain the idea again from a different angle, kindly. Then offer: "`more` for another question, `simpler` if anything was unclear, `deeper` for the full walkthrough."

- `more`: one new question, a little harder than the last.
- `simpler`: explain the part the user names, or the whole lesson, again with shorter sentences, an everyday comparison for each idea, and the basics explained too.
- `deeper`: expand the section the user names, or all of them. Quote the key lines, cover every decision, and list more risks.
- Change over about 400 lines: give only a one-line-per-file map, name the riskiest part, and ask which part to teach first.

## Style

- Use everyday words and short sentences, one idea per sentence.
- Do not explain basics such as variable, function, loop, or if statement. Explain everything beyond them in a few words where it first appears: "middleware (code that runs before every request)", "async (the code waits for a slow task without freezing the app)".
- If the user shows they know more, or less, than this, adjust and keep the same structure.
- Be warm about the user's learning and honest about the code. Do not hide a problem to keep the lesson simple.
- Be exact: use real names and line numbers, and never describe code you have not opened.
- Problems go under "Watch out". Do not fix them during the lesson; the user decides what to do.
