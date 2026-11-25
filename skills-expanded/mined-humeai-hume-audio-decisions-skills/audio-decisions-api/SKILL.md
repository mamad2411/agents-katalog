---
name: audio-decisions-api
description: Build with the Hume Audio Decisions API, which answers questions about audio with probabilities that estimate how human raters would answer. Covers deciding whether a question suits the API, choosing which audio each request covers (speakers, windows, turns, long recordings, live audio), writing questions, reading and combining answers, and checking results. Use when a developer wants to analyze recordings or live audio with the Audio Decisions API, for bulk files, real-time apps or anything in between, or asks what the API can and can't answer.
license: MIT
---

# Hume Audio Decisions API

The Hume Audio Decisions API listens to an audio file and answers questions you ask about it. You send one MP3 or WAV file, optional `context` text, and a set of questions. For each question it returns probabilities that estimate the share of human raters who would give each answer. It returns no transcript, reply or explanation.

Use the official SDKs: `pip install hume-audio-decisions` for Python, or `npm install @humeai/audio-decisions` for TypeScript.

Every integration comes down to two decisions:

1. **Which units of audio** each request covers: whose voice, how much time, and how fast you need the answer.
2. **Which questions** to ask of each unit.

The rest (reading answers, combining them, checking them) follows from those two. This skill walks through both, then how to read and check what comes back.

**Freshness:** written in November 2026 for the first release of the API. Where the [API reference](https://dev.hume.ai/audio-decisions/reference) differs, the reference wins. Details that may change are collected in [references/api-reference.md](references/api-reference.md).

## Step 0: Check that the question suits the API

The API is good at **listening questions**: something a group of people could answer by listening to the clip, without having to reason it through. It works best when you supply the possible answers.

| The question is… | Do this |
| --- | --- |
| How something sounds (tone, emotion conveyed, accent, quality, background) | Ask the API |
| Which of several things was said or meant, with the options supplied (intent, request type, a word from a list) | Ask the API as a `choice` |
| When something happens | Ask the API as a `span` question, and confirm what it finds (see Step 1) |
| Open-ended output: a transcript, a summary, a free topic label | Use speech-to-text and an LLM |
| Counting (speakers, turns, seconds) or exact timestamps | Use speaker separation (diarization), voice activity detection or signal processing |
| An outcome that needs reasoning ("Is this call escalating?", "Will this caller buy?") | Break it into listening questions plus other signals: [references/breaking-down-questions.md](references/breaking-down-questions.md) |

What the API does well, under which conditions, and what is still unproven: [references/capabilities.md](references/capabilities.md). Read it before promising a capability to anyone.

## Step 1: Choose the units of audio

A **unit** is the stretch of audio one request covers. Each request is answered on its own, with no memory of earlier requests, so the unit has to contain everything the answer depends on.

Work through four things:

**Whose voice?**
- Stereo recording with one speaker per channel: send the channel for the person you're asking about. The API mixes the channels into one track, so a mixed call lets the other speaker's voice leak into the answer. For a WAV whose first channel is the person, the SDKs' `downmix_strategy="first_channel"` does this for you.
- Mono recording with several speakers: either separate speakers in your own code (diarization) and send their turns, or keep the mix and name the person in the question and in `context` ("the caller"). Overlapping speech stays hard either way.

**How much time?** Choose it by what you need from the answer:

| You need to know | Unit |
| --- | --- |
| *Whether* something happens in a turn or a call | The turn, or the whole file |
| *How* a known moment sounds (a reply, a greeting) | A window centred on the moment, at least 5 s long |
| *Where* or *how often* something happens, and it's frequent or missing one is costly | Overlapping windows, at least twice as long as the longest expected event |
| *Where* something happens, and it's rare in long audio | A `span` question on the turn or chunk, then confirm each span with a `noul` question on a window around it |
| An overall impression of a recording longer than 5 minutes | Chunks of up to 5 minutes, cut and sent by the SDKs' `create_chunked`, answers combined in your code |
| Answers *while someone is talking* | Rolling windows (see the real-time recipe) |

The API refuses clips shorter than 1 second (`audio_too_short`), but most questions need at least 5 seconds of audio, so pad a short moment with the audio around it rather than sending it alone. A few questions, such as which language is spoken or whether someone laughs, hold up at 1 second; each [use case](https://dev.hume.ai/audio-decisions/docs/use-cases) shows its recommended minimum.

**How fast do you need answers?** After the fact, use turns, whole files or chunks. During a conversation, send independent rolling windows. This gives an answer per window, not continuous monitoring or exact event timing. The recipe, including window length, hop size and smoothing, is in [references/audio-units.md](references/audio-units.md#real-time).

**What stays in the audio?** Trim silences for questions about the speech. Keep them for questions about pace, pauses or timing.

Recipes for each of these (channel extraction, window sizing, cutting at silences, merging overlapping hits, long recordings, real time): [references/audio-units.md](references/audio-units.md).

## Step 2: Write the questions for each unit

| Type | Asks | Answer |
| --- | --- | --- |
| `noul` | Yes or no | The share of raters who'd say yes |
| `choice` | Which one of several options you supply | The likeliest option, `confidence`, and a probability per option |
| `score` | How much, on an ordered scale you supply | The mean level (from 0), `confidence`, and a probability per level |
| `span` | When an event happens | Time ranges in milliseconds, each with a probability |

Rules that matter most:

- **Supply the options.** Closed choices (these five languages, these four intents, these sound types) work far better than open questions. Add "None of these" or "Unclear" when many clips won't fit any option.
- **One property per question, name the person, keep it neutral.** "Does the agent sound warm and professional?" is two questions. Ask "How patient does the agent sound?", not "Isn't the agent impatient?".
- **Say what counts as yes.** A `noul` question's optional `criteria` says what counts as `true` and as `false`.
- **Use `context` for what a rater needs to know:** the setting, who is speaking, a transcript or earlier turns, the line being judged, or a list of candidates. Don't use it to ask the question.
- **Match the question to the unit.** An event question on a long recording gets diluted. A trait question on a single short window is noisy.
- **Treat `span` as a way to find candidates,** not a measurement. Confirm each span with a `noul` question on a window of at least 5 s around it.
- **Send all the questions for one unit in one request,** in the same order every time. Questions in a request are answered in one model inference, so adding, removing or reordering questions can change the answers.
- **Ask what you need.** Requests are billed in input tokens, which grow with the audio's length, the `context` and the number of questions. `decisions.input_tokens` (`inputTokens` in TypeScript) counts a request before you send it.
- **Gates and follow-ups belong in your code.** Ask a cheap question on everything, then more questions only where it says yes.

Full guidance with worked wording, options, scales and `context` examples: [references/question-design.md](references/question-design.md).

## Step 3: Read and combine the answers

- **Probabilities are rater shares.** A `noul` of 0.5 means raters would split, not that the model is unsure. `confidence` measures how much raters would agree, not how certain the model is.
- **Choose thresholds on your own labelled clips,** never 0.5 by default. Thresholds tuned for other models don't carry over.
- **Use a middle band for review.** Send clips whose answers fall between two thresholds (for example 0.3–0.7) to a person instead of deciding automatically.
- **Combine across units in your code:** mean, maximum, "any window above the threshold", "N windows in a row", or per speaker across turns. Say in your results that answers are per unit.
- **Store the answers yourself.** The run endpoints return a run's status and request, not its answers.
- **Expect model updates.** The model can change without an API version change, so answers for the same audio can shift. Re-run your labelled clips after updates and re-check thresholds.

## Step 4: Check before relying on it

A question you haven't checked is a guess. At minimum:

- **Known-answer clips** from both ends: an obviously frustrated caller and an obviously calm one. Make them from the same kind of audio you'll analyze. Synthetic voices make most questions look easy, so test on real recordings.
- **A control:** silence, noise, or a clip where the property is clearly absent.
- **The same property in two wordings** should agree.
- **Listen** to the highest-, lowest- and middle-scoring clips.
- **For questions built from parts** (Step 0), check each part moves the way you expect, then check the combined result against your labels.

## Rules

- Read the API key from the `HUME_API_KEY` environment variable. Never hard-code, print or commit it.
- Don't present an unproven capability as validated. Say what you checked, on how many clips, and with which thresholds.
- Accent, perceived age and perceived sex are raters' perceptions, not facts about a person. Use them to route or support, never to screen people.
- Don't use the API for identity verification, detecting minors, or judging hidden feelings or sincerity.

## Files

| File | What's in it |
| --- | --- |
| [references/audio-units.md](references/audio-units.md) | Speakers and channels, window sizing, spans vs windows, long recordings, the real-time recipe, audio preparation commands |
| [references/question-design.md](references/question-design.md) | Question types in detail, wording, options, scales, `context`, example questions by area |
| [references/capabilities.md](references/capabilities.md) | What generally works, what works under conditions, what's unproven and how to build it, what not to use the API for |
| [references/breaking-down-questions.md](references/breaking-down-questions.md) | Turning an outcome question into listening questions plus other signals, with worked examples |
| [references/api-reference.md](references/api-reference.md) | Endpoints, request and response, counting input tokens, SDKs and their audio helpers, runs, errors, limits, what the first release leaves out and how to work around it |
| [examples/bulk-review.md](examples/bulk-review.md) | Many recordings, some over 5 minutes, answers combined per file and exported (Python) |
| [examples/realtime-mic.md](examples/realtime-mic.md) | Live microphone input with rolling windows in the browser (TypeScript) |
| [examples/call-escalation.md](examples/call-escalation.md) | A stereo support call, per-turn questions plus a transcript, built up into "is this call getting heated?" |
