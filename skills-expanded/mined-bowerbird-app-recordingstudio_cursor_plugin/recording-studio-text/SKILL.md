---
name: recording-studio-text
description: Write fun, clear, short product text for Recording Studio screens, buttons, flashes, and mail. Use when adding titles, labels, empty states, errors, tooltips, popovers, admin widget extra info, or any copy people will read. Give the app personality without filling the screen or using expert/AI jargon.
---

# Recording Studio text

Write like a sharp marketer: **personality, then clarity**. The product should feel human and a little playful. It should never feel like a whitepaper or a chatbot.

People came to do a job. Help them do it. Do not fill the screen with words.

## Voice

Warm, light, and plain. A short wink is fine. A lecture is not.

Think “Move this folder” or “Invite your team” — not “Relocate the selected recordable in the hierarchy.” The first is friendly. The second is a gem talking to itself.

Titles name the job. Subtitles add one spark of context, or they stay empty. Buttons are verbs: Save, Move, Invite, Close.

Personality lives in **short lines** — a title, an empty state, a flash. It does not live in paragraphs of brand voice.

## Little text, better design

Do not pad a page to make it look finished. White space is fine. A clear form beats a wall of help text.

If something is hard to understand, **fix the design first** (`recording-studio-ui`): one action, a better label, a sensible default. Copy is the backup, not the product.

When you really must explain something complex:

1. Split it into parts.
2. Use scannable headings.
3. Put **one short paragraph** under each heading (a blog post, not a brochure).

Even then, ask whether a simpler screen would make the explanation unnecessary.

## Extra info, off the main line

Keep the thing people see **simple**. Put the extra explanation behind a Flatpack **tooltip**, **popover**, or similar additional-info control — only when the visible label is not obvious.

A table column titled “Last seen” might need a tooltip. A column titled “Name” does not. Do not decorate every cell with a hint.

In **Recording Studio Admin**, widgets take an extra-info param. Use it the same way: a clear number or title on the card, and a sentence of “what is this?” in that extra-info slot.

Before you ship a view, look at it as someone **new to this page**. What would make them pause? Add just enough extra info to make that obvious — then stop.

## Everyday words, not expert talk

If only a domain expert would say it, do not put it on the screen. Same for AI-speak: words that sound smart and mean little.

Skip filler like *leverage, utilize, robust, seamless, unlock, empower, streamline, holistic, delve*. Skip gem talk like *recording, recordable, actor, root, capability, grant*.

Say workspace, folder, page, site, people, access — the words a teammate would use at lunch.

Staff admin screens can be a little more precise. They still should not say “recordable,” and they still should not drone.

## Errors and empty states

Be human. Say what happened. Say what to do next. Do not blame. Do not dump class names.

Good: “You don’t have access to this workspace. Ask someone to invite you.”  
Poor: “Accessible role check failed on the root recording.”  
Also poor: a three-paragraph apology.

A playful empty state is great: “Nothing here yet. Add a page to get going.” Keep it to a line or two.

## Do not

- Cover the page in explanation when a simpler layout would do.
- Tooltip every label. Only hint when a newcomer would be stuck.
- Stack witty intros on top of the actual action.
- Use expert or AI phrasing to sound more serious.
- Repeat the title in the subtitle.
- Write a different voice in each gem. Same spark, same shortness.

Page shape: `recording-studio-ui`. Components: `recording-studio-flatpack` (`Tooltip`, `Popover` — not custom hover hacks).
