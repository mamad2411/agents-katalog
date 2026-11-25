---
name: write-in-your-voice
description: "Build a working voice for a person from how they actually speak, then draft in it: assemble a tiered source bank from their speech (recordings, transcripts, dictations), compose drafts from their own sentences, and gate the result on shape, not just words. Use when setting up AI drafting for a founder, creator, or executive, when drafts keep coming back 'not my voice,' or when a voice profile built from published posts is not working."
version: 1.2.6
---

# <img src="assets/icons/mic-01.svg" width="20" height="20" alt="" /> Write in Your Voice

A voice cannot be learned from text the person never wrote or said. This skill builds the evidence base first (a source bank cut from the person's speech), then drafts from it under a procedure, then checks the draft's shape. It exists because the obvious approach (feed the model the person's published posts and a style description) fails in a specific, repeatable way, documented in the case study in `references/`.

## The principle

Published is not the same as theirs. If any of a person's published posts were ghostwritten or AI-generated, training on them teaches the model its own voice back to itself, and the loop is invisible because the output looks plausible. Speech is the ground truth: recordings and transcripts of the person actually talking carry their cadence, sentence habits, and judgment moves. Everything else is a weaker source, in a fixed order, and the weakest source (published posts) is quarantined in writing.

## What a run returns

State which run you are doing; each has a defined output.

- **Build run** returns the bank: a tiered file (spoken passages, dictated explanations, approved texts, quarantined published posts), each passage tagged with date, source, and format, plus a coverage note naming the subjects and formats the bank does not cover.
- **Draft run** returns the source passages it composed from (quoted), the draft, and the gate results (word gate, shape gate, grammar check). If no source covers the move, it returns the dictation prompt instead of a draft, and says why.
- **Review run** (grading an existing draft) returns the gate results with the failing lines quoted, and a verdict: send back to sources, or ready for the person's approval. This skill never publishes; the person approves the exact final text.

## Procedure A — Build the source bank

Full detail in `references/source-bank-process.md`; the worked example (a production build, with its failure) is `references/worked-example-the-bank-build.md`.

1. <img src="assets/icons/search-01.svg" width="20" height="20" alt="" /> **Gather speech, not posts.** Meeting and call transcripts with speaker diarization, transcripts of the person's own videos (most-watched first; they are the most audience-tested), and voice notes. Target 100,000+ words of the person's own speech before cutting anything.
2. **Purge other voices.** Diarization mislabels speakers. Drop whole blocks where someone else does most of the talking (customer interviews, panels), then filter passages that read like another person. Prefer sources where the person is the only speaker: hosted videos, solo talks, webinars they lead.
3. **Cut passages where the person is doing the moves.** Slice the speech into 60–180 word passages. Score for judgment markers (I think, the problem is, most people, nobody, because), concrete numbers, questions, and first-person density. Penalize housekeeping: intros, scheduling, logistics, filler, raw list recitation. Tag each kept passage with date, source, and format.
4. **Layer the bank in a fixed order, and give it a header that carries the rules.** Tier 1: spoken passages. Tier 2: dictated explanations, verbatim. Tier 3: texts the person personally approved. Tier 4, quarantined: published posts, labeled contaminated in the file itself. A published post counts as a voice source only when the person identifies that specific post as their own words. The bank header also records the person's **channel conventions**: the register rules per channel (for example, a lowercase raw register for short-form story posts, capitalization restored for professional channels, how formal their email is), so any drafter working from the bank picks them up instead of defaulting to standard capitalization everywhere.
5. **Wire the bank into drafting.** Procedure B is not optional garnish; a bank that is not wired into drafting is an archive.
6. **Maintain it and measure it.** Refresh on a fixed cadence (new speech into tier 1, dictations into tier 2, approvals into tier 3, new posts into tier 4 only). Keep a kill-rate ledger: drafts presented vs drafts the person rejected on voice, week over week. If the kill rate is not falling, the bank or the procedure is wrong, not the person's taste.

## Procedure B — Draft from the bank

1. **Source first.** Pull 2–3 passages on the same move or subject as the piece, from tier 1 or tier 2 where they exist. Quote them in the working notes. If you cannot quote any, check tier 3 before concluding you have no material (step 4).
2. **Compose from the sources.** The load-bearing lines (the opening, the explanation, the close) must trace to source sentences, tightened at most. Structure (a hook-first order like AIDA) is applied to their sentences; it never generates replacements for them. New connective text stays minimal and plain.
3. **No source, no draft.** If no source in tiers 1–3 covers the move, the deliverable is a dictation prompt, not a composed draft: "Tell it like you're warning a friend: what's the moment this is for, what's the dumbest way people handle that moment, and what do you do instead?" Drafting first and voice-checking afterward is the banned path; it is how voice systems produce plausible text the person rejects on sight.
4. **Respect the hierarchy at drafting time, including the tier 3 rule.** Spoken passages outrank dictated explanations, which outrank approved texts. Tier 3 (approved texts) may source a draft when no spoken or dictated passage covers the move — the control case is a launch built from the person's own published product text, which they approved and which leads with the material itself. A tier-3-sourced draft must say so in its return ("sourced from approved text, not speech"), because the cadence will read as the person's written voice, not their spoken one; if the spoken cadence is what the piece needs, the answer is the dictation prompt, not tier 3. Apply the target channel's convention from the bank header (Procedure A, step 4) as you compose. Chat messages the person wrote to their tools or team are process language: usable for facts and opinions, never for cadence. Published posts are not a cadence source at all unless individually verified (tier 4 rule).

## Calls on sibling skills

This skill does not run alone; the playbook is one playbook, and a skill calls the siblings its work needs, by name, at the step that needs them. The calls are steps, not suggestions:

- **At drafting, call comms** — purpose and audience are set before voice is applied; a piece in the right voice aimed at the wrong reader is still wrong.

- **When the piece is a public post, call stop-the-scroll** — the opening must earn the second line, in the subject's own voice, under that skill's tests.

## The gates

- **Word gate.** Build a working vocabulary from the person's spoken corpus (the words they actually use, counted) plus a never-use list (words they have rejected or never say). Check every draft against it mechanically if you can; a script beats a judgment call. **Account for every flag in the run's return: rewrite it away, or justify it in one line** (a source name, a quoted term, the person's verbatim phrase). No unexamined flags. **A justification counts only when it traces to the person's own attested speech** — their verbatim phrase, their corpus, a term they were quoting. A skill's own house terms never justify a flag: structural labels and method vocabulary are the skill talking about its own process, not the person's words. When the only defense of a flagged word is the skill's own terminology, the flag stands and the word is rewritten into the person's plain words. A count of justified flags is not a failure — the approved draft in the case study carries more flags than the rejected one — but one unjustified flag is. Necessary, and nowhere near sufficient: see the case study, where the rejected draft scored cleaner on the word gate than the approved one.
- **Shape gate.** Four checks on the exact final text. (1) Parallelism scan: flag mirrored sentence pairs and balanced two-part constructions; people explain in a line, they do not argue in balanced pairs unless that is genuinely their habit on tape. (2) Press-release test: could the opening line run unchanged in a company announcement or a news summary? Openings in a real voice are a reaction, a receipt, a question, or a verdict. (3) Read-aloud check: read the draft next to two bank passages chosen for the piece type and compare person, sentence-length pattern, and cadence. Default to tier 1 spoken passages; for a launch, the strongest anchor is the source behind the most recent approved launch (often a tier 2 dictation), whatever tier it sits in. If it does not sound like the same person, it goes back to the sources, not to another polish pass. (4) Numbers check: every figure is written the way the person says it out loud, rounded to the spoken form ("more than 304,000 emails," "$307 billion," "about 3 in 4"); a raw precise count (304,174) or a decimal abbreviation ($307.0B) fails. Exact figures live in the source material; the draft carries the number as speech.
- **Grammar check.** Beside the word gate, on the exact final text: subject-verb agreement, articles, punctuation, hyphenation, parallelism. Account for every finding exactly as word-gate flags are accounted for — fixed, or justified in one line in the run's return; a draft is not finished with an unexamined grammar finding. The standing justification is the person's own usage: where the bank shows a pattern is theirs — a fragment habit, a dropped article in their attested cadence — it is their voice, not an error, and the check must not correct them into standard prose. What the check exists to catch is what the person would call a mistake themselves: the agreement slip, the wrong article, the broken parallel.
- **Priority rule.** The voice outranks task-level register assumptions. A house style, a "launch register," a format copied from a previous package: all of these are defaults that yield to the voice on any conflict. The only override is the person naming the exception for that specific piece.
- **Writing pass.** After the gates above, run the called-in writing pass on the exact final text: the work-humanizer skill in rewrite mode as a final register check, then the writing-styles skill's plain rules. This step calls two sibling skills; it is a procedure, not a style reminder. The pass is subordinate to the priority rule: any change that fights the source bank loses, because the person's own sentences outrank the pass, always. Facts and figures never change in the pass. The draft is not finished until the pass has run.

## Guardrails

- The bank holds other people's speech too, before the purge. Purge on build, keep the bank private, and never quote another speaker's words as the person's.
- Never invent first-person experience, opinions, outcomes, or endorsements for the person. The bank is the evidence base; a position with no source in it does not go in the draft.
- Caption and diarization errors survive filtering. The bank teaches cadence and sentence habits, not quotable wording; anything quoted publicly as the person's exact words needs their own check.
- The person approves the exact final text before anything ships. Praise is not approval, and any edit after approval needs a fresh look by the person.

## Limits and boundaries

- A bank built from one context (sales calls) will not carry a different one (a keynote). Coverage gaps are handled by dictation, not by composing harder.
- This skill builds and uses a voice for drafting. It does not decide what the person should say: topic selection, claims, and strategy belong to the person's other processes (or their judgment).
- Style transfer to a different person requires a different bank. There are no shortcuts through someone else's passages.
- The method assumes the person talks on the record somewhere: calls, videos, voice notes. A person with no recorded speech can dictate the tier 2 material directly; expect a thinner bank and more dictation prompts.

## Sources

This skill is a method, not a summary of a book. It was built in production, on the author's own content operation, and its evidence is the build record: the bank statistics, the rejected and approved drafts graded side by side, and the kill-rate ledger described in `references/`. The dictation-prompt pattern and the hook-first structure (AIDA) are long-standing public practice in direct response and sales writing, used here as structure applied to the person's own sentences.
