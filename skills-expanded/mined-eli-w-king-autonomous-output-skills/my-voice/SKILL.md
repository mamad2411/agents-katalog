---
name: my-voice
description: "My voice: write anything the user will send, post, or say as themselves so it sounds like them. Use when the user says 'write it like how I would say it', 'in my voice', 'make it sound like me', 'how I'd say it', 'draft a message/reply/post for me', 'rewrite this as me', 'less like AI', or asks for an email, a Slack or Teams message, a LinkedIn post or comment reply, an event invite or description, a bio, a team update, feedback request, announcement, reply, PR or issue description, notes for engineers, a PM summary, a design rationale, UI copy, or a script they will read out loud. Covers the user's core voice (plain, direct, warm, honest about status, concrete, human not robotic, no marketing tone or AI slop, no em or en dashes), channel patterns, copyediting their drafts without changing their wording, and length rules. Reads local private writing samples when present. Kept current by the weekly skill miner from the user's own edits, approvals, and corrections."
---

# My voice

Write the way the user writes when they send something to their team, not the way an assistant
writes. When this skill applies, every sentence should pass the test "would they have typed this?".

**Before drafting, read the samples if they exist:**
`~/.copilot/skill-miner/private/voice-samples.md` holds verbatim examples of the user's own writing
and of drafts they approved, plus their exact copy feedback. It contains internal names and links, so
it is never published: a private copy keeps it the same on each of the user's machines, and it stays
out of this repo. Imitate its rhythm and structure; never copy its facts into something else, and
never put it in a public repo or a post. No samples yet? Build them from the user's own sent Teams
messages and email, read only: [voice from Work IQ](references/voice-from-workiq.md).

**Then read examples of the same kind** when there are any: the other items in the plan, the docs
the text will sit next to, or recent announcements that landed well. Match their tone, vocabulary,
length, and format.

## Core voice

1. **Say the thing first.** Lead with the news, the change, or the ask. Context comes after, briefly.
   Skip the filler around it: no warm-up pleasantries ("how are you doing"), no asides explaining
   what the reader can already see, and no filler closers ("so just let me know"). A simple warm
   line ("I hope you and your family are well") is fine. Write for what this reader knows and cares
   about: leave out your other projects they don't know, private plans (like who you will pass the
   work to), and caveats or process details they don't need.
2. **Short, plain sentences.** One idea per sentence. No run-ons; sentences end cleanly. Use the
   words a person would say out loud. Short is not choppy: write full sentences that flow, not
   fragments split by periods, and not comma chains either.
3. **First person, team voice.** "I" for the user's own work and asks ("send feedback my way"),
   "we" for the team's work and decisions ("we're exploring a few ideas"), "you" to the reader.
   Shared work sounds collaborative, never "I did all this". Replies to collaborators end with an
   open invitation ("Any questions for me?") rather than a filler closer.
4. **Warm and upbeat, never hype.** Friendly openers and closers ("Hi all!", "Thanks!"), real
   enthusiasm when it fits, and no marketing language: no "seamless", "powerful", "robust",
   "unlock", "elevate", "game changer", or superlatives the facts do not support. If it reads like
   a launch blog, it is "too markety"; use straightforward bullets instead. If it reads as AI
   generated (slogan rhythm, frills, decoration, polished filler), it is "AI slop": strip it back to
   simple sentences that are quick to read. The specific tells (puffed-up importance, "serves as",
   "not just X, it's Y", trailing "-ing" verdicts, chatbot leftovers) and how to fix the vagueness
   under them are in [AI tells](references/ai-tells.md). Frame things for the reader as
   encouragement and opportunity ("a chance to learn a new way to work"), never as pressure to keep
   up, blame, a sales pitch, or a backhanded compliment; a simple "congrats" beats praise with a
   catch, and a deadline reads as a friendly reminder, never a threat.
5. **Honest about status.** Call unfinished work what it is ("still a WIP", "a first pass", "close
   but still a work in progress") and name the open question instead of hiding it.
6. **Concrete.** Name the feature, the setting, the branch, the link, the date. Show an example
   instead of describing one ("Instead of X, we could say Y"). When pitching or announcing, name the
   specific things people will see or get (an overnight run that ends in a demo video, many agents
   working in parallel) instead of abstract or "woo woo" claims, and give each claim or perk the
   context an outsider needs to feel it.
7. **No em or en dashes.** Use periods, commas, colons, or parentheses, and mix them: a draft that
   is only periods and commas, with every sentence about the same length, reads as AI too.
8. **No process narration.** Do not mention how the work was produced ("we recorded a demo", "an
   agent drafted this", "I used X to..."). The only exception is an attribution the user asks for.
9. **Respect the requested length.** "Shorter" means cut it roughly in half; "one paragraph" means
   one paragraph. Labels are about three words; bullets are one or two sentences. When unsure, go
   shorter and simpler: "simplify" and "make it shorter" are the most common copy notes.
10. **Keep their wording.** When editing the user's draft, fix typos, punctuation, capitalization,
    spacing, duplicated words, and its/it's or their/there/they're, but keep their phrasing and
    order unless they ask for a rewrite.
11. **Human, not robot.** Write for a person who was not in the room: full sentences in the
    reader's terms, and no robot speak (version numbers, build or capture details, internal step or
    process labels) or jargon: say what a technique does in plain words instead of naming it.
    Describe what happens for the reader, not what the system is doing.

## Patterns by channel

**Team update (Slack or Teams post).** A short headline with an exclamation point ("Site
revisions!"), then one short paragraph on what changed and why. Optional "Things to look for:" as
two or three bullets. One line on what is still a WIP. A clear ask. Links on their own lines with
plain labels ("v1:", "Original, for comparison:").

**Feedback request on a design.** "Hi all! We've put together a first pass at <thing>,
prioritizing <goal>." Then "We're exploring a few ideas:" with short bullets, one bolded question
they most want answered, a concrete before and after example, where to try it (branch, link, or
steps), and the timeline in bold ("Please leave feedback in this thread by <date>."). End with
"Thanks!".

**Announcement or how-to (for example a setting of the week).** One emoji plus a title line, then
one paragraph of imperative steps ("Add ..., then start ..."), a call to action ("Try it out by
..."), and who to contact ("Send any feedback my way or to @<teammate>"). An optional playful
sign-off line only when the user asks for one.

**Quick reply.** One or two upbeat sentences ("Let's use the same component!"), then the link or
code location on its own line.

**Sharing work for feedback (a DM or group chat).** One or two casual lines that tie it to what you
discussed and ask what they think ("Hey, what do you think of this so far?"), then a short list of
what changed, with the link, PR or video attached. A small feature idea for a reviewer is one line
("Hey, I think ...") with the PR and the video.

**Email to outside partners, senior leaders, or academics.** Warm but more formal than team chat,
never super casual. Address people by name (or by title where that is the custom), thank or
congratulate them simply, lead with the update and the key details, answer their questions in short
bullets, offer to answer questions or share more materials, and sign off with a first name. Keep it
specific and short: a generic, long draft misses. With senior leaders, be grateful and succinct;
with partner teams, sound confident rather than deferential.

**Event invite or announcement (email, Slack or Teams post, LinkedIn).** The news first (who is
hosting what, and with whom), then a framing sentence or a question hook, about three short bullets
that start with a verb and name what people will see or learn, a friendly invitation with any perk
stated precisely, and the sign-up link last. A social post that links to the event page leaves the
date, place, and headcount to that page; an invite email still gives the date and place. LinkedIn
posts stay short and credit the co-hosts, so they never read as all about the user. For an
independent event, never imply the employer's partnership or sponsorship: the user speaks for their
team, and company names and logos stay understated.

**Design rationale or status write-up.** A one-line framing sentence, then bullets that start with
"Users can ..." (one or two sentences each), each followed by why it is better, in first person ("I
think this design also makes it much clearer which ..."). End with the next step ("I've launched a
quick study to test these assumptions.").

**Notes for engineers.** Straightforward bullets of concrete call-outs, one change each ("Removed
<word> from the tab title", "Added a lock next to locked options"). Include settings and branches.
Respect the requested count.

**PM or leadership summary.** A few plain bullets about decisions and what the prototype shows.
High level, no implementation detail, still not markety.

**PR or issue description.** What changed and why in two or three sentences, before and after
images, how to try it, and anything still open. No narration of how it was built.

**UI copy (labels, descriptions, headlines).** Labels in about three words. Descriptions in full
sentences a newcomer understands. Never make it sound like the user is responsible for the product
working ("Keep each task separate" puts the burden on them). "Learn more" links go where the design
puts them (end of the sentence or on their own line), consistently.

**Something they will say out loud** (a script, a talk track, a voice-over). Conversational and
first person, contractions, short spoken sentences ("So here's what we changed."), honest asides
("I'm not fully sold on this one yet"), and generous thanks.

## How to deliver

- Before handing it over, run the final pass at the end of [AI tells](references/ai-tells.md).
- Put the full text in the chat as a ready-to-paste code block, one block per channel (email,
  Slack, Teams), every time, even when you also saved it as a draft or sent it; the user should
  never have to ask "what is the draft?". Write a `.txt` on the Desktop only when asked, and open it
  only when the user is at the Mac and asked for it; during unattended or overnight runs, leave it
  closed (or use `open -g`) and mention it in the final report.
- Offer at most one alternative, and only when the choice is real (for example shorter versus with
  examples).
- "Start over" means a new draft with a different structure and format, not a reword of the
  rejected one.
- Never send or post as the user unless they explicitly asked you to in this conversation; when you
  do, follow `autonomous-computer-use` for exactly-once sends.

## How this stays accurate

The weekly skill miner reads the user's own messages, their edits to drafts, and what they
approved, and updates the rules above. Only text written for other people counts as voice evidence:
the user's quick prompts to agents are casual and often dictated, so their typos and lowercase are
not the voice. The miner also refreshes the private samples file: it keeps the most representative
recent examples, and only text the user wrote or approved, never other people's words. If the user
corrects your draft, follow the correction now; the miner will pick it up.
