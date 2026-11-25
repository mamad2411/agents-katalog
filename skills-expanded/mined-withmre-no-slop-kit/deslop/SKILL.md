---
name: deslop
description: Removes what sounds AI-generated from French or English text. Review mode rewrites a text while keeping the author's ideas and examples, then shows what was removed and why. Writing mode applies the same rules silently to new text. Use when I ask to proofread, reread, humanize or « désloper » a text, and whenever writing copy meant for publication (site copy, article, LinkedIn post, newsletter, email, README, product description, interface text).
---

# Deslop

## 1. Two modes

- **Review**: I give you a text (pasted, or a file path) or ask to reread one. Rewrite it under the contract of section 2 and report as in section 8.
- **Writing**: you write new text meant for a reader. Apply every rule silently, follow section 6, and don't mention the rules or add a report unless I ask for one.

If my request includes instructions (a light pass only, a target channel, a length), follow them over the defaults.

## 2. Contract (review mode)

- Keep every idea, example, figure, name and the author's stance. Change the form only.
- Add nothing: no new idea, no new example, no new argument, no conclusion. The result is usually shorter, never longer.
- Keep the register (tu or vous, familiar or formal), the person (je, nous, on) and the author's deliberate quirks: a recurring expression, a joke, a regional word, a chosen anglicism.
- If a fix would change the meaning, leave the sentence and flag it.
- Don't silently correct facts. Flag anything that looks wrong, and any claim with no source (« les études montrent », « de nombreux experts »).

## 3. Load the catalogue

Detect the text's language and read the matching file in this skill's folder: `fr.md` for French, `en.md` for English. Mixed text: read both.

## 4. Two kinds of rules

Absolute. Remove every instance, no exception:

- Em dash and en dash used as punctuation.
- « Ce n'est pas X, c'est Y » and all its variants (« It's not X, it's Y » in English).
- Emoji, unless I asked for them.
- The banned words and phrases of the catalogue.
- Leftovers from a generator (« Voici une version révisée », « Bien sûr ! », placeholders like `[Votre nom]` or `[Insérer]`, Markdown symbols in a plain-text channel). The kit's own `[À FOURNIR : ...]` marker is the exception: it stays, and gets listed in your reply.
- Invented specifics: a figure, a quote, an anecdote or a source that nobody gave you.

Frequency. A human text has a list now and then, a bold word, a group of three, a colon. What signs a machine is repetition. Fix until these patterns stop repeating, and keep the occurrences that carry meaning:

- Three sentences in a row of about the same length.
- Three or more short declarative sentences in a row, each one standing alone. Connect the thoughts the way people do: because, but, so, which, a subordinate clause, a semicolon.
- Every paragraph built the same way (claim, explanation, example, wrap-up), or ending on a transition or a summary. Some paragraphs can just stop.
- Groups of three by reflex, in lists and inside sentences.
- The hedging seesaw: a claim, then its counterpoint given equal weight, then a vague middle. Take the position the text supports, and give the counterpoint one sentence at most.
- Bold, colons or bullets on every line.

## 5. Don't swap one tic for another

The classic failures of a rewrite:

- Every em dash turned into a colon. Vary: comma, period, parentheses, a semicolon, or rebuild the sentence.
- Every triplet cut to a pair. Now everything comes in twos.
- Every long sentence chopped into fragments. Staccato is a tic too.
- Every hedge replaced by a confident punchline.
- Synonyms swapped word for word while the structure stays robotic. Change the structure.

## 6. Writing mode

- Specific beats general, using only what you know: the real number, the real name, the real step, the real date. « Trois clics entre la connexion et le premier devis » says more than « une expérience fluide ».
- When the text needs a specific you don't have (a figure, a client name, a moment), ask for it or leave a visible `[À FOURNIR : ...]`. Honest vagueness beats invented precision.
- A hypothetical is labeled as one (« imaginons », « suppose »), never told as something that happened.
- Match the person's voice when you have samples of it (their previous texts, messages, posts): sentence length, humor, words they use, words they would never use.
- Default voice when nothing is known: direct, slightly informal, active verbs, trusts the reader, doesn't over-explain. In English, use contractions.
- Fit the channel: no headings in an email or a social post, no Markdown in plain text, a LinkedIn post that doesn't look like a template.

## 7. Procedure

1. Read the whole text once. Identify its channel and the author's voice before changing anything.
2. List the patterns present and their frequency.
3. Rewrite, structure first, then sentences, then words.
4. Read the result as if aloud. Any sentence you can't say in one breath gets cut or split.
5. Compare with the original: every idea, example and figure is still there.
6. Generic test: could this text have been written for anyone, about anything similar? If yes, point to where a detail only the author knows would change that, and ask for it. Don't invent it.
7. Final check: no em dash, no en dash, no banned word, no invented specific, no new tic from section 5.

## 8. Output (review mode)

Write the report in the language of the conversation, with the labels of that language: in French « Ce que j'ai retiré », Avant, Après, Pourquoi, « Laissé tel quel », « Marqueurs : N avant, N après »; in English "What I removed", Before, After, Why, "Left as is", "Markers: N before, N after". The French labels below stand for both.

1. The rewritten text, complete, ready to paste.
2. « Ce que j'ai retiré » (What I removed): a table with columns Avant, Après, Pourquoi (Before, After, Why). One row per kind of fix, grouping repeats (« 6 tirets cadratins remplacés par des virgules, des points ou des parenthèses »). Quote short excerpts only.
3. « Laissé tel quel » (Left as is), only if needed: sentences kept because a fix would change the meaning, doubtful facts, unsourced claims, places where a specific detail from the author is missing.
4. One line: « Marqueurs : N avant, N après » (Markers: N before, N after).

Nothing else: no introduction, no comment on the quality of the text.
