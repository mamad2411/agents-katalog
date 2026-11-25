---
name: write-site-narrative
description: How to agree on what a website says before building it, by grilling the person one question at a time (in the style of Matt Pocock's grill-me) until there is a shared story, writing it to context-v/narratives/, getting it signed off, and then developing the site's content from it. Use at the start of every new site or redesign, before the mood board, brand kit or any code; whenever someone says "narrative", "messaging", "positioning", "what should the site say", "help me figure out my website", "grill me", or is new and doesn't know where to start; and when content needs writing for pages that don't have any. Encodes the decision tree a site's story walks down, the one-question-with-a-recommendation interview, the narrative document shape, the sign-off gate, and the narrative-to-content step.
---

# Write the site's narrative, then its content

We agree on what a site says before anyone builds it. The agreement lives in
`context-v/narratives/<Site>-Narrative.md`: the story the site has to tell, the
*why* and the *feeling*, written before the *what to build*. The spec, the mood
board, the brand kit and every page's copy come from it.

Building first and finding the message later is the most expensive order: every
page gets rewritten once the story settles. Agents are especially prone to it,
because writing plausible copy is easy and asking hard questions isn't.

## 1. Grill, one question at a time

The interview follows Matt Pocock's
[grill-me](https://www.aihero.dev/5-agent-skills-i-use-every-day) discipline:

> Interview me relentlessly about every aspect of this plan until we reach a
> shared understanding. Walk down each branch of the design tree, resolving
> dependencies between decisions one-by-one. For each question, provide your
> recommended answer.
>
> Ask the questions one at a time.
>
> If a question can be answered by exploring the codebase, explore the
> codebase instead.

Applied to a site's story:

- **One question per message.** Never a list. A beginner faced with eight
  questions answers the easy two.
- **Every question comes with your recommended answer** and one line of why.
  This is what makes it work for people who've never done this: reacting to a
  suggestion is far easier than inventing from nothing. Make the
  recommendation specific enough to be wrong.
- **Look before you ask.** An existing site, a README, a pitch deck, a
  LinkedIn page, the person's old posts: read them and ask "I found X, is that
  still true?" instead of asking from scratch.
- **Relentless means following up.** A vague answer ("we help people") gets a
  sharper follow-up ("which people, doing what, the week before they'd find
  you?"). Move on only when the branch is settled.
- **Use their words.** Quote the person back to themselves. The narrative is
  their story in their language, tightened, not yours.
- **Keep a running tally** so they can see progress: "Settled: audience,
  promise. Next: proof."

## 2. The tree to walk

Settle these in order; later branches depend on earlier ones. Skip any the
files already answer.

1. **What it is.** In one sentence a stranger would understand. What is it not?
2. **Who it's for.** The one reader the site is really for, then any second
   reader. If there are two (investors and founders, parents and kids), the
   site may need two voices; name both.
3. **Their moment.** What is that reader doing, feeling or stuck on the day
   they land here?
4. **The promise.** What changes for them, in their terms?
5. **Why believe it.** Proof: numbers, names, history, work, people, a story.
6. **Why this one.** What's different from the alternatives they'd otherwise pick?
7. **The feeling.** How the reader should feel in the first five seconds. Three
   words they'd use about it afterwards, and three they never should.
8. **What it should never say or look like.**
9. **What they do next.** The one action the site asks for, and the second.
10. **What's on it.** The pages or sections the story needs, and what each one
    has to make the reader believe.

Stop grilling when every branch has an answer the person agrees with. Say so:
"I think we have it. I'll write it up."

## 3. Write the narrative

Write `context-v/narratives/<Site-Name>-Narrative.md` (create the folder if
needed; add an `index.md` if the repo indexes its context-v folders). Use the
`context-vigilance` frontmatter baseline with `type: Narratives`,
`status: Draft`, and the person in `authors`.

Sections, in their words wherever possible:

- **Why Care?** The situation and what the site's job is, in a paragraph.
  End with the job in bold, one sentence.
- **Who <it> is.** The authoritative description and its defining traits.
- **The voices.** One subsection per reader: the story told to them, and a
  one-line takeaway in italics.
- **The feeling.** The five-second feeling, words to use, words to avoid.
- **What's on the site.** Each page or section, and what it must make the reader believe.
- **Open questions.** Anything the grilling didn't settle.

`sites/learnstart-site/context-v/narratives/LearnStart-Site-Narrative.md` in
astro-knots is the reference.

## 4. Get it signed off

Ask the person to read it and say "signed off" or what to change. Iterate.
When they sign off, set `status: Signed-Off`. Nothing downstream (mood board,
brand kit, spec, pages) starts before that; if they want to keep going while
unsure, note what's unsettled under *Open questions* and carry on knowingly.

When the story changes later, change the narrative first, then the pages.

## 5. Develop the content

Content is written from the signed-off narrative, not invented page by page.

1. List the pages from *What's on the site*. For each, write what it must make
   the reader believe (one line), and the sections that get it there.
2. Draft the copy as Markdown in the site's content collections
   (`src/content/<collection>/`), rendered through LFM (see
   `lossless-flavored-markdown`). Copy in Markdown is copy a person can edit;
   copy hard-coded in components isn't.
3. Draft in the voice the narrative named, with real specifics from the
   grilling. Where a fact is missing, leave a visible `TODO:` rather than
   inventing one. Never make up numbers, names, quotes or testimonials.
4. Grill again where the draft exposes a gap ("the About page needs a founding
   story; what happened?").
5. Have the person read each page in the browser, not in the file.

Long-running content (articles, guides, a knowledge base) gets its own
collection from the start, so the site can grow into it.

## Anti-patterns

- **The questionnaire.** A list of questions in one message, with no recommendations.
- **Accepting the first vague answer.** The narrative inherits the vagueness.
- **Ghost-writing.** Polished copy in your voice that the person can't defend.
- **Building on a Draft.** The pages get rewritten when the story settles.
- **Invented proof.** Placeholder testimonials and stats ship more often than anyone intends.
