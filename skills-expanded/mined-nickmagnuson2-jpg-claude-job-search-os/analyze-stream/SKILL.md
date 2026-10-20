---
name: analyze-stream
description: Analyze a long recorded livestream, conference session, podcast, or workshop (45 min to many hours) for Nick. Downloads the audio, transcribes it with local Whisper in overlapping segments, reviews transcription anomalies, extracts evidence per chunk, synthesizes insights against Nick's goals and systems, and runs an adversarial verification pass before anything is reported. Use when Nick shares a stream or recording link, says "analyze this livestream", "run the pipeline on day 2", or a recording email arrives for an event he registered for.
argument-hint: <url or "day N of <event>"> [stream_type] [focus]
user-invocable: true
allowed-tools: Read(*), Grep(*), Glob(*), Write(output/**), Write(data/source-transcripts/**), Bash, Task, mcp__exa__web_search_exa, mcp__exa__web_fetch_exa, WebFetch, mcp__claude_ai_Gmail__search_threads, mcp__claude_ai_Gmail__get_thread
---

# /analyze-stream

Deterministic steps run through `tools/stream_pipeline.py` and `tools/stream_validate.py`. LLM steps run through the Agent tool with the prompts below. Every command prefixes `PYTHONIOENCODING=utf-8`.

**Custody rule.** The source audio (m4a) is kept. Only WAVs are deleted (`clean-wav`). Never delete the m4a unless Nick asks for that specific file.

**Profile guard.** Before synthesis, confirm `data/profile.md` and `data/goals.md` exist with real content.

## Parameters

| Name | Values |
|---|---|
| `slug` | lowercase-hyphens, e.g. `event-name-day2` |
| `date` | stream date, `YYYY-MM-DD` |
| `stream_type` | `vendor_demo`, `conference_talk`, `podcast`, `workshop`. `panel` is not supported: run as `conference_talk` and state in section 3 that speaker disagreements were not analyzed |
| `incentive` | who benefits from the audience believing it |
| `agenda` | optional session list; used as labels only, never as boundaries |

## Step 0: Discover the recording

Check, and write down what each returned, before saying a recording does not exist:
1. The URL Nick gave.
2. Gmail: `search_threads` for the event name and "recording" in the last 7 days.
3. The event page (Luma or vendor).
4. The host's X account.

## Step 1: Acquire and transcribe

```bash
PYTHONIOENCODING=utf-8 python3 tools/stream_pipeline.py acquire "<url>" --slug <slug> --date <date>
PYTHONIOENCODING=utf-8 python3 tools/stream_pipeline.py transcribe --slug <slug> --date <date>
```
`acquire` tries without cookies. On HTTP 402/403, tell Nick and ask before retrying with browser cookies. `transcribe` runs in the background for long streams (about 25 min per 9 h on the current machine; segmented timing is still being measured). Report `failed` segments and `seam_recovered_cues` from its output.

## Step 2: Review anomalies

```bash
PYTHONIOENCODING=utf-8 python3 tools/stream_pipeline.py validate --slug <slug> --date <date>
```
For each anomaly, read the printed context and decide:
- `hold_screen`: a break or hold slide (repeated "Thank you." or "Bye." at a fixed cadence, bounded by "we'll be right back" and "we are back").
- `redo`: a loop or gap over real speech. Then run `validate` again.
- `accept`: real repeated speech. Always add `--note`.

```bash
PYTHONIOENCODING=utf-8 python3 tools/stream_pipeline.py dispose --slug <slug> --date <date> --id A3 --as hold_screen
```
Show Nick the anomaly list with dispositions in the final report.

## Step 3: Chunk

```bash
PYTHONIOENCODING=utf-8 python3 tools/stream_pipeline.py chunk --slug <slug> --date <date>
```
It refuses while any anomaly is undisposed.

## Step 4: Extract (one goal-blind pass, parallel)

One Agent per chunk, `model: sonnet`, all launched in one message. The prompt receives the chunk path and stream parameters only. **Do not include Nick's goals, profile, or CLAUDE.md.**

Prompt template:

> You are an evidence extractor for a livestream transcript. Record faithfully what was SAID, not what is useful.
> Stream: <name, date, one-line description>. stream_type: <type>. incentive: <incentive>. Transcript: Whisper, no speaker labels, names may be misspelled.
> Read `<repo>/data/source-transcripts/<date>-<slug>/chunks/chunk-NN.txt` in full (in pieces if long). Extract only items whose timestamp is inside the core window in the header; `[overlap]` lines are context.
> Write ONE JSON file to `.../forms/chunk-NN.json` with keys: `chunk_id`, `segment_summary`, `segments[{ts_start,label}]`, `speakers_inferred[{name,basis}]`, `claims[{ts,quote,speaker,kind: capability|metric|opinion|roadmap|pricing|security}]`, `demos[{ts_start,ts_end,what_was_attempted,outcome: worked|partial|failed|unclear,evidence_quote,evidence_ts}]`, `friction[{ts,quote,what_went_wrong}]`, `numbers[{ts,quote,value,self_reported}]`, `techniques[{ts,quote,pattern}]`, `audience_questions[{ts,question_quote,answer_summary,answered_directly}]`, `open_threads[]`.
> Rules: quotes are copied character for character from one line or contiguous lines joined by a space, never edited (no dropped filler words, no expanded contractions); `ts` is the first quoted line's timestamp; name a speaker only when the transcript establishes it; record friction and failures even if laughed off; a demo "worked" only if the transcript establishes completion; record every number as self-reported unless a source is cited.
> Before finishing, run `PYTHONIOENCODING=utf-8 python3 tools/stream_validate.py form <form path> --chunk <chunk path>` and fix any failures it lists.
> Final reply: one line `chunk-NN: claims=N demos=N friction=N numbers=N techniques=N questions=N`.

After all return, run `stream_validate.py form` on every form yourself. The external run is the only authoritative one. Report totals and failure reasons.

## Step 5: Synthesize

One Agent, `model: opus`. Inputs: all forms (items with `verified: false` may not be cited), raw chunks, `CLAUDE.md`, `data/goals.md`, `data/professional-identity.md`, prior analyses found by grepping `output/analysis/` for the subject name, stream parameters.

Required in the prompt:
- Read the forms, then do a **goal-aware retrieval pass over the raw chunks** for themes that matter to Nick and for findings that span chunks. Forms alone miss cross-chunk findings.
- Before recommending any build, check whether the repo already does it.
- **Every quoted string is followed on the same line by an evidence tag**: `[transcript H:MM:SS]` or `[file relative/path.md]`. Quotes are verbatim from the tagged source.
- A person's name not spoken on stream is followed by `(from the agenda)` in the same sentence.
- Discount rules for the `stream_type` (vendor_demo: unscripted failures and conceded gaps weigh more than scripted wins; metrics are self-reported; a pre-made example is not live output).
- Sections: 1 Verdict; 2 What the stream was (segments with times); 3 Evidence discount; 4 Capability shown vs claimed (table); 5 Systems insights (target file or skill, effort, confidence tag); 6 Search and wisdom insights (confidence tag); 7 Where it does NOT fit (non-empty); 8 Next actions or "nothing to build"; 9 Coverage note.
- Confidence tags `(strong)`, `(lean)`, `(unsure)` on every item in 5 and 6. No em dashes. Plain literal language. No compensation, family, health, or therapy content. No inferred role titles for Nick.
- Output path: `output/analysis/MMDDYY-<slug>.md`, with `Last updated:` header.

Then run:
```bash
PYTHONIOENCODING=utf-8 python3 tools/stream_validate.py doc output/analysis/MMDDYY-<slug>.md --transcript data/source-transcripts/<date>-<slug>.vtt
```
Fix every failure (tag, quote, timestamp, name, em dash) before Step 6.

## Step 6: Adversarial verify

One Agent, `model: opus`. Inputs: the doc and the raw chunks. **Do not give it the forms.** It checks every item in sections 1, 4, 5, and 6 for:
- a quote taken out of context (a question, a joke, a hypothetical);
- two quotes that answer different questions presented as a contradiction;
- absence claims ("never", "no presenter"): it must search all chunks and list which;
- pattern sentences contradicted by the doc's own tables;
- names and attributions not established by the transcript;
- a pre-made example presented as live output;
- timing (mid-stream decisions presented as end-of-stream conclusions).

It writes `output/analysis/MMDDYY-<slug>-verify.md` with a ledger table `| ID | Claim | Verdict (KEEP/SOFTEN/DROP/FIX-FACT) | Evidence (ts + verbatim quote) | Required change |`, an absence-claims table, a names table, and counts.

## Step 7: Apply and report

1. Spot-check the 3 to 5 highest-impact verdicts against the transcript yourself.
2. Apply every SOFTEN, DROP, and FIX-FACT. Re-run `stream_validate.py doc`.
3. Add a one-line verification note under the doc header with the verdict counts.
4. `clean-wav`.
5. Report to Nick: verdict, top insights with confidence tags, what verification changed, anomaly dispositions, cost (agent count, tokens if known), and any tuning observations for `output/analysis/091626-stream-pipeline-hand-run-learnings.md` (append new L# entries with measurements).

## Known limits

- Quote and name checks prove presence in the declared source, not that the quote supports the claim. That is Step 6's job, and its recall is unmeasured.
- Whisper mishears proper nouns; exact matching cannot catch that.
- A name made only of ordinary dictionary words is not checked.
- Panel streams: disagreements are not analyzed.
