---
name: longtail
description: Use when writing or rewriting a blog post, article, newsletter, web or marketing copy, essay, op-ed, email or memo that must read as written by a person, or when the user says a draft sounds like AI, reads like ChatGPT, is slop, or asks to humanize or de-slop it. Not for code, commit messages or fixed templates.
---

# Longtail

AI writing is caught at three layers, and each needs its own fix (the evidence is in `references/science.md`, which is for the user: do not read it while drafting, because knowing which features look human makes every draft use them, and that uniformity is itself the tell):

1. **Structure.** How the piece is built: where the payoff is promised, when the thesis lands, how it ends, who is speaking. Detectable at 98 F1, and rewording does nothing to it.
2. **Style.** Register, sentence complexity, figurative language, rhetorical moves. About 88 F1 on its own. It fails on different documents than structure does, so you have to beat both.
3. **Surface.** Function words, punctuation, sentence-length spread, formatting density. Near 100 F1 on unedited text.

The deepest finding: every model writes into the same few structural configurations, while human pieces are scattered across rare ones. So avoiding a list of bad moves is not enough. A model that avoids them converges on a new common template, and that is just as detectable. This skill therefore **samples the structure from real human writing** with a script, because you cannot be random on your own.

## Pick the mode

- **Web:** blog posts, articles, newsletters, landing and marketing copy. Full recipe below.
- **Essay:** op-eds, personal and blog essays the user authors, and reshaping the user's own drafts. Recipe below, plus `references/essay.md`.
- **Message:** emails, memos, docs, updates. Use the short contract in `references/message.md`, then steps 5, 6 and 8.
- **Quick:** if the user wants speed over rigor, do steps 1 to 3, one cold read, and one surface check, then step 8.
- **Rewrite:** when the user hands you an existing draft, first run a cold read on it as-is. If it was written by a model (cold read above about 60), keep its facts, roll a card and rebuild to the card; rewording alone changes nothing a detector sees. If the user wrote it (cold read under about 40), do not rebuild it: fix only the passages the cold read quotes, in the user's voice, and keep their structure and audience. In testing, rebuilding a person's own paper changed its audience and scored no better.

## Recipe

Every layer gets measured by something other than your own taste. Your taste is what produced the AI shape, so it cannot be the judge.

1. **Material.** List the specifics you actually have: the user's facts, numbers, names, quotes, incidents, opinions. If the user is there, ask for missing ones, and ask for exact quotes and raw notes rather than summaries; texture you do not have cannot be faked. Never invent quotes, statistics, named people, customers, studies or first-hand experience ("we see this constantly"). Opinions are fine without a source; events and habits are not.

2. **Roll the shape.** Run:
   `python3 <skill_dir>/scripts/shape.py --mode web --words <target> --has <flags>`
   where `<flags>` lists what the material really contains: `quotes` (named people and their views), `data` (real numbers), `story` (an incident or first-hand experience), `news` (something new to announce), `steps` (a real procedure). The script draws the skeleton of a real human post that fits your material, perturbs it, prints a **shape card** and saves it to a file (it prints the path). If Bash is unavailable, use `references/fallback-shapes.md`.
   Use the card as given. Re-roll once only if the card cannot fit the material (for example it asks for an interview and you have no interviewee). Do not re-roll because another shape feels more natural; the natural shape is the AI shape.

3. **Plan, then draft to the card.** The card is the only source of structure and style decisions, and its PRIORITY block is binding. Before writing prose, write a paragraph plan: one line per paragraph saying its job. The plan must put the opening the card asks for in paragraph 1, put the first statement of the main claim exactly where the card says (early, middle, end or never), include no preview paragraph unless the card asks for one, make the last paragraph do exactly what the card's ending line says with nothing after it, and use the card's heading count. Then write the draft from the plan.
   Current Opus models make the same moves in almost every draft no matter what they are told: the claim and a preview in the first paragraphs, a wrap-up at the end, arguing against common advice or a "myth", old-way-versus-new-way framing, and escalating the stakes. Human writers from the same material did most of these in fewer than half their posts. Make these moves only when the card asks for them; when it says not to, leave them out even if the brief's angle invites them (state the company's view plainly, without a strawman). Where the card and the user's brief disagree about length or product mentions, the brief wins. Keep the user's facts exact.

Do steps 4, 5 and 6 in this order. Structure first, because it moves paragraphs; surface last, because every rewrite moves those numbers.

4. **Structure check (loop).** Save the draft to a file. Annotate it with `references/rubric.md` as a strict outside reader (quote evidence where the rubric asks), save the answers as JSON, and run:
   `python3 <skill_dir>/scripts/structure.py check <answers.json> --card <card path>`
   It reports a structural P(AI) and every PRIORITY-level card line the draft broke. Rebuild the broken parts (move or delete paragraphs, rewrite the opening or ending) and re-check until no card lines are broken and P(AI) is below 0.50, for at most two more rounds. If you have an Agent or Task tool, use it: give a subagent only `references/rubric.md` and the draft file path and have it write the JSON; it annotates more honestly than the writer. This step is required.

5. **Cold read.** Follow `references/cold-read.md`: a fresh subagent (Agent or Task tool) reads only the draft and quotes what sounds machine-written; you rebuild those passages without changing the plan. Then read `references/defaults.md` sections C and D once and fix what remains. The giveaway that survives everything else is polish: aphorisms, paragraphs ending on a quotable line, tidy callbacks, explaining why every detail matters, announced caveats. Leave some things raw.

6. **Surface check (loop, last).** Run:
   `python3 <skill_dir>/scripts/stylo.py check <draft.md>`
   It scores the draft with a built-in detector trained on pre-2022 human business posts versus current model drafts, and names the signals to fix. Half of human posts score under 0.20 and nine in ten under 0.40. Rewrite and re-check until P(AI) is below 0.40, for at most four rounds; if it plateaus above that, stop and deliver rather than contorting the prose. Edits here are sentence-level only: never add or remove paragraphs, never add a wrap-up or preview. Fix by rewriting sentences (join short ones, restore the field's real vocabulary, use infinitives, add parenthetical asides, stop rotating synonyms), never by stuffing words. The biggest current-model tells are not the famous ones: too many short sentences, the word "one", too few "to" constructions, plain short words, varied synonyms, and zero dashes, parentheses or exclamation marks. Pre-2022 people used all of those.
   If the user gave a writing sample or has a saved style profile, their voice wins: build their profile with `stylo.py profile <samples> --out /tmp/voice.json`, check with `--ref /tmp/voice.json`, and keep their punctuation rules (never add dashes for a user who bans them).

7. **Done gate.** You are not finished until shape.py, structure.py and stylo.py have each run at least once on this piece, and a cold read has happened. If any has not, do it now. In quick mode, structure.py may be skipped.
   Then do a truth pass. The human-sounding voice tempts invented texture, and in testing skill-guided drafts carried more unsupported claims than plain ones. List every number, name, quote, event and first-person experience claim ("we've seen", "in our experience", "most teams we talk to") in the draft. Anything not in the user's material gets cut or turned into a plainly stated opinion ("we think").

8. **Deliver** only what the user asked for. The card, the checks and any list of missing material stay out of the piece. If material is missing and the user is present, list it after the piece under "Missing material". Never leave `[NEED]`, `[LINK]` or bracket placeholders in the prose unless the user asked for them.

## Rules that override everything

- The user's own voice, sample or saved style profile beats this skill's defaults, including punctuation rules.
- Honor the requested length. If none is given, the card's length is a good default.
- Do not trade detectability for truth. A human-looking piece with invented facts is worse than an AI-looking true one.
- In essay mode, keep what the genre requires (see `references/essay.md`).

## Why the card and not a checklist

A checklist tells you what not to do, and you then pick the most likely remaining option, which is the same for every run. That is how a "humanized" skill ends up with ten posts that all open on a concrete object, all push back on one piece of common advice, and all end on a resource link. The card gives each piece a different, real human configuration, so a batch of drafts can spread out the way a batch of human posts does. Rarity is what separates human from AI in the data. In testing, the model's own habits still pulled drafts back together (see step 3), so treat the card as binding, not as inspiration.

## Limits

Tested on company blog posts (11 held-out briefs). Against detectors trained on ordinary AI text it does well: a surface detector flagged 0 of 11 drafts (11 of 11 plain or humanspeak drafts) and a structural detector flagged 1 of 11. It does not beat a detector trained on this skill's own output (AUC about 0.8 to 0.95), and a strong model reading carefully still identified every draft. Essay and message modes had only a two-essay smoke test. The surface detector was trained on business blogs and over-flags other genres (a student's own course paper scored 0.72), so outside blog writing check against the user's voice profile instead, and treat a single-document structure score as rough (repeat annotations of one paper ranged from 0.62 to 0.88). Details: `references/science.md`. If the environment variable `LONGTAIL_LOG` is set, the scripts append their output to that file for auditing.
