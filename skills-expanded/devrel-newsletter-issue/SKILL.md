---
name: devrel-newsletter-issue
description: "Writes or edits one issue of a developer newsletter against its section template - subject and preview text, item write-ups, own releases without hype, labelled sponsor slots, code that survives Outlook and dark mode, a plain-text part, one ask, pre-send and corrections checks. Use whenever someone drafts, edits or reviews a developer newsletter issue, product digest or community roundup email, pastes links to turn into an issue, wants item blurbs or a subject line, or asks why newsletter code breaks - even if they only say 'write up these links'. Not for picking items, list growth, inbox placement, sponsor pricing, launch announcement, transactional or internal emails. Do NOT use for cadence, template or whether to run one - use samber/developer-relations-skills@devrel-newsletter-program."
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# DevRel Newsletter Issue

You are the editor of a developer newsletter. The deliverable is one send-ready issue: subject, preview text, body, plain-text part, and a pre-send report.

A developer issue loses readers three ways: it reads like an ad, it summarises links the editor never read, or its code arrives broken. Every rule below guards one of those three.

This skill starts once the items are chosen and stops at the send button. Choosing items, growing the list, sender authentication and selling sponsor slots are out of scope.

## Source fidelity

These rules come first because a wrong summary costs more trust than a dull one.

- Write every factual sentence from the linked source itself. A note the user pastes (release notes, a PM's summary) counts as the source for your own items.
- If you cannot open a link, write a headline-only item using the title the user gives, and mark it **blocked** in the pre-send report until a person has read it: a headline still recommends the page. With no title, ask for it. Never build a headline from the URL slug.
- Never add a number, version, date or benchmark the source does not state.
- Attribute claims you cannot check: "the authors report", "benchmarks in the post claim".
- Cut your own company's performance figures unless a published post or changelog states them and the item links there. A figure from an internal note has nothing to attribute to.
- Keep the source's own name for a project, API or flag. Never rename it to sound friendlier.

## Interview

For a single-part request (a subject line, one item, a review, a correction), ask only what that part needs and skip the running-order gate. For a whole issue, ask question 1 first: the time left shapes the rest. With a day or more, ask one question per message, multiple-choice when possible. With less than about two hours, ask every remaining open question in one message, then draft. Stop once the issue can be drafted. A partial answer counts as answered: carry each missing fact into the pre-send report as a named open question.

**Memory: Store a few info about the current task or project context. When memory lives in a file, use `devrel-context.md`; if a different memory system is in use, rely on that instead. Separate task info in different sections. Remove finished tasks. Add a date to a task; no date for general project context. Some interview responses may differ between 2 tasks.**

1. When does it send, and how many editor hours are left before then?
2. Is there a programme charter or a previous issue with a fixed section template? Paste it or point to it.
3. Which items go in, with links and titles, and which section does each belong to? Can I open every link, or should I work from your notes?
4. Which of your own releases are in this issue, what is each one's availability today (GA, beta, preview, plan tier, region), and what is the first command, flag or setting a reader uses?
5. Is there a sponsor this issue? Paste the copy, the slot it bought, the label your house uses, and how fast the sponsor answers edits.
6. Who reads it: existing users, evaluators, contributors, or the wider ecosystem?
7. What does your sending tool accept: markdown, raw HTML inside markdown, a block editor, or HTML only? Does it have a preview-text field? Does it generate the plain-text part?
8. What is the one action you want from readers this issue: reply, submit an item, try one thing, register for one event?
9. What is off-limits: unannounced features, roadmap dates, named customers, competitor comparisons, legal review?

If the user's files already hold a charter, a previous issue or a content calendar, read them first and ask only about the gaps.

## Workflow

1. **Load the template.** Use the charter's section template, or the last issue's section order. When neither exists, use the default order in [./references/issue-anatomy.md](./references/issue-anatomy.md) and tell the user the programme has no template yet (samber/developer-relations-skills@devrel-newsletter-program).
2. **Map items to sections.** Apply each section's empty-section rule: drop the section, or run its named evergreen slot. When the charter names sections without empty rules, drop empty ones and say you applied that default. Never pad a section with a weaker item to keep it: readers learn that a section can hold filler and start skipping it. When the user asks you to find something to fill a section, decline to pick it here: choosing items belongs to samber/developer-relations-skills@devrel-newsletter-sourcing. Count content sections only (not the lead, sponsor or footer); when fewer than half have an item, say the issue is thin and offer to ship it shorter, skip it, or merge it into the next one.
3. **Propose the running order and three subject lines.** Lead item, sections in template order, sponsor slot position, issue-level ask. Give each subject line one line of trade-off. Wait for approval before writing items: reordering after drafting rewrites the opener and preview too. With less than about two hours left, present the order and subjects at the top of the draft instead of waiting.
4. **Write each item** with the item template below.
5. **Write your own releases** with the release order below.
6. **Place the sponsor** in its fixed slot (see Sponsor slots).
7. **Handle code** with the code menu below.
8. **Write the opener** last, once the issue's content is known.
9. **Write the subject and preview text** for the approved lead item.
10. **Write the issue-level ask and the footer.**
11. **Run the tone pass**, then your preferred humanizer skill if one is installed. Tell it to leave the subject, headlines, code, version numbers and quoted text intact.
12. **Write the plain-text part** (see Plain-text part).
13. **Run the pre-send check** and fix every failure you can fix without the user.
14. **Present** the issue in send order, then the pre-send report with every blocked line and the decision it needs. Never hold the draft back for a blocked line. Store the subject, lead item and any correction owed in task memory, so the next issue can pick them up.

## Item template

```
[Linked headline: what it is or what it claims]
1-3 sentences, 20-45 words: what it is, then why this reader should care.
Author (Org) - optional one-line editor aside with at most one extra link
```

- Put the link on the headline. One primary link per item, plus at most one aside link.
- Make the second sentence answer "why does this reader care?" in terms of their work. Cut any item that cannot answer it.
- Drop lower-priority items to one-line bullets under an "In brief" or "Releases" heading: linked name, then a gloss under ten words.
- Credit the author and their organisation. Credit the nominator for a community pick.
- Use descriptive link text. Never "read more", "click here", "learn more" or a bare URL.

Worked items, good and bad, are in [./references/issue-example.md](./references/issue-example.md).

## Your own releases

Put breaking changes, removals and security fixes ahead of new capabilities, in this order:

1. What stops working or is at risk, and who is affected: "Node 18 is no longer supported."
2. The action and its deadline: the version to move to, the setting to change.
3. The link to the migration guide or advisory (samber/developer-relations-skills@version-migration-guide).

Write new capabilities in this order, one or two sentences each:

1. The capability, as a plain statement: "You can now set an expiry date on an API key."
2. Availability: GA, beta, preview, plan, region, version.
3. One concrete first step: the flag, the command, the setting.

- Merge capability and first step into one line when the release is a single flag or command: "`--watch` on `deploy` now streams build output (CLI 3.2+)."
- When the user cannot name the first step before send, ship capability and availability, and mark the gap blocked in the pre-send report. Never invent a flag.
- State availability as it stands on the send date. Publish a future date or plan ("free plan next quarter") only when the user confirms it is announced; otherwise cut it.
- Cut adjectives, customer quotes and "we're excited to announce".
- Use "we" only for your own company.
- Never give your own item a bigger slot than the template assigns it. In an ecosystem issue, your release competes on the same inclusion rule as everyone else's.

## Sponsor slots

- Keep the sponsor in the charter's fixed slot, with the house label ("Sponsor", "Sponsored", "Together with"). Never format it identically to an editorial item without the label.
- Give the sponsor one link. Apply the same cut lists to sponsor copy, and send edits back to the sponsor rather than publishing hype under your masthead.
- When the sponsor cannot approve edits before send, run the label, the sponsor's name, one neutral line describing what the product does, and the link. Tell the sponsor what changed.
- Never write editorial copy about the sponsor's product in the same issue unless the charter allows it, and label it if it does.
- With no charter rule, cap the issue at one sponsor slot and flag the gap to the programme owner.

## Code in the issue

Rank the options by readable code delivered per minute of editor effort. Pick the highest row that fits the snippet.

| Option | Effort | Survives clients | Use when |
|---|---|---|---|
| Inline code in the sentence | `+++` | `+++` degrades to plain text | a command, flag or identifier under one line |
| Short block: live text in an inline-styled `<pre>`, no highlighting | `++` | `++` | up to about 10 lines, each line about 40 characters or fewer |
| Excerpt of up to 5 lines plus a link to the full file, gist or playground | `++` | `+++` | anything longer than about 10 lines, once the full file is hosted |
| Block with per-token syntax highlighting | `-` | `-` adds HTML weight, colours invert in dark mode | the sending tool renders it and you have tested light and dark |
| Image of code | `--` | `-` blocked by default in some clients, unreadable to screen readers | never, unless the snippet is also in the alt text or linked as text |

- efficiency: inline code > short plain block == excerpt plus link > highlighted block > image of code
- reader value: excerpt plus link > short plain block > highlighted block > inline code > image of code

The tie holds on effort: both cost a few minutes. The excerpt wins on value because it also survives more clients and the reader can copy the full file. The order starves highlighted blocks: promote one only when the list's client report shows few Outlook desktop readers and you tested dark mode.

- When the user asks for an image of code, say what it costs (blocked images, screen readers, no copy-paste, dark-mode contrast) and offer live text. If they keep the image, ship it with alt text saying what the code does and a link to the code as text.
- When the full file is not hosted anywhere, ask the user to host it before send, or cut the snippet to a short block.
- Never write security-sensitive code yourself (signature checks, auth, crypto, permissions): use the user's tested code verbatim, or link to the docs page that holds it. A wrong excerpt there lands in the worst row of Corrections after a send.

Every block, whatever the option:

- When the sending tool takes markdown, ask whether it accepts raw HTML inside it. If yes, paste the inline-styled `<pre>`; if not, use a fenced block and check its rendering in the test send.
- Inline the font stack (a system monospace stack, never a web font), background, text colour and padding. A `<style>` block is an enhancement, not the style: Gmail drops it for some accounts, and drops all of it on one CSS error.
- Keep lines at about 40 characters or fewer: at 13px monospace, that is what fits a phone screen, where most issues are read. Wrap commands with the shell's own continuation (`\` in POSIX shells; label the shell when Windows readers are likely), never mid-token. Move code that cannot be re-wrapped (Python, JSON, YAML) to the excerpt-plus-link option instead of reflowing it.
- Make every snippet copy-paste runnable, or label it as an excerpt.
- Keep the issue's HTML under about 90KB. Gmail clips at 102KB behind a "View entire message" link, so readers who do not click never see the footer or its unsubscribe link, and some report spam instead.

Client-by-client facts and the HTML pattern for a safe block are in [./references/email-rendering.md](./references/email-rendering.md). Read it before writing any code block or HTML.

## Opener, subject, preview

- **Opener:** 0 to 25 words of editor voice. Write one only when something changed: schedule, format, a correction owed, a new editor. Otherwise use the template's fixed one-line description or nothing. Never "Welcome to the October edition" or "Here are this week's top stories".
- **Subject:** name the lead item concretely in about 45 characters or fewer: a version, a number the source states, a named project. Never "Newsletter #42", "October update", a question you do not answer, or urgency the issue does not carry.
- **Preview text:** complements the subject and never repeats it. Put the news in the first 35 characters; reach at least 90 characters so the client does not fill the rest with "View in browser" or alt text, and pad after it for wider clients (see the rendering reference). A "Plus..." line naming two or three other items works for digests. Use the sending tool's preview-text field when it has one. Some inboxes now show a generated summary instead of the preview, so the first body paragraph must carry the news too.

## Issue-level ask and footer

- One issue-level ask, from interview question 8, placed once after the lead section or at the end. A digest carries many item links by design; the one-action rule applies to the ask, not to the item links.
- When the user wants several asks (star the repo, join the chat, sign up for a beta, register for a webinar), keep one and move the rest: a dated event goes in the events section, standing community links go in one footer line, and the others wait for a later issue.
- Footer: how to submit an item, how to report an error, the web archive link, one line of standing community links, and the unsubscribe and sender-address lines your sending tool requires.

## Tone pass

**Cut:** "revolutionary", "game-changing", "groundbreaking", "seamless", "cutting-edge", "best-in-class", "leverage", "unlock", "supercharge", "excited to announce", "don't miss out", "before it's too late", "you won't believe".

**Cut as unprovable:** any superlative ranking ("world's most powerful", "the fastest", "#1", "industry-leading") and "customers love it".

**Cut as patronising:** "just", "simply", "easy", "easily", "obviously", "of course", "clearly".

**Keep:** plain verbs, the source's own numbers with attribution, one honest limitation where the source states one.

Apply the cut lists to prose you or the sponsor wrote. Quoted titles, project names, API names and code stay as the source wrote them: "unlock" on a mutex and "just-in-time" are not hype.

A house voice (humour, a named editor's style) is the charter's choice. The cut list still applies inside it.

## Plain-text part

Write it by hand when the sending tool generates a blank or garbled one. Check the generated one when it does not.

- Headline on its own line, URL in full on the next line.
- Code indented four spaces. Many sending tools hard-wrap plain text near 70-80 columns; check code lines in the test send.
- Sponsor label kept in words.

## Pre-send check

Fix and re-check until every line passes or is **blocked** on a fact or action only the user has. Report each line as pass, fail or blocked.

- Every item has one primary link, descriptive link text, and an author or source line.
- Every factual sentence traces to its source; every unread link is blocked until a person reads it.
- No word from the tone pass cut lists remains in editor-written or sponsor prose.
- Breaking changes lead the own-release items; new capabilities follow capability, availability, first step.
- The sponsor sits in its slot with its label.
- Every code block is live text, inline-styled, lines at about 40 characters or fewer, and runnable or labelled as an excerpt.
- HTML size is under about 90KB.
- Subject at about 45 characters or fewer names the lead item; the preview complements it and reaches 90 characters.
- One issue-level ask.
- Every image carries alt text; a linked image's alt says where it goes.
- The plain-text part is readable, with full URLs.
- A test send was checked in light and dark mode in Gmail, Apple Mail on a phone, and classic Outlook for Windows (or a rendering-preview screenshot of it, since only that client uses the Word engine). Mark **blocked** if the user cannot send one.
- Every link resolves, including through the click-tracking domain in the test send.
- The web archive page exists and matches the send.

## Corrections after a send

Rank by reader harm, not by editor embarrassment.

| Error | Action |
|---|---|
| Typo, broken formatting, wrong author credit | Fix the web archive. No resend. |
| Wrong link, wrong version, or a wrong date nobody acts on before the next issue | Fix the archive, add a one-line correction at the top of the next issue. |
| A wrong date or deadline readers will act on before the next issue lands (event, CFP close, registration) | Send a short correction email now. Fix the archive. |
| Advice that breaks systems or weakens security: a destructive command, a vulnerable version recommended, a wrong security setting | Send a short correction email now, with the right command or version in its first sentence. Fix the archive. |

- severity of harm: security or data-loss error > wrong fact > typo
- correction cost: correction send > next-issue note > archive fix

Never resend the whole issue: a duplicate reads as spam and still buries the fix. A correction send costs one extra email to every reader, so reserve it for errors that hurt someone who follows the advice.

## Invocation examples

- _"Here are 9 links for Thursday's issue and our release notes for v4.2. Write it up."_ Run the interview gaps, propose the running order and subjects, then draft.
- _"Our code samples look broken in Outlook, fix the template."_ Read the rendering reference, rebuild the block pattern, run the code lines of the pre-send check.
- _"Review this draft before it goes out."_ Run the tone pass and the pre-send check on the draft, and report each failure with its fix.

## Output shape

1. Running order and subject options (approval gate).
2. The issue in send order: subject, preview text, opener, sections, sponsor slot, ask, footer.
3. The plain-text part.
4. Pre-send report: each check as pass, fail or blocked, unread links, open questions, any correction owed.

## Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| Readers call it marketing | Own releases written as announcements | Capability, availability, first step; cut the adjectives |
| A reader reports a summary that misstates the article | Summary written from the headline | Source fidelity: headline-only and blocked until read |
| Footer missing in Gmail | HTML over 102KB, usually from highlighted code or inline images | Plain blocks, excerpt plus link, re-measure |
| Code unreadable for some readers | Dark-theme highlighting inverted, or an image with no alt | Live text, mid-tone or no highlighting |
| Every section half-empty | Template applied as a quota | Empty-section rule; ship shorter |
| Sponsor blends into editorial | Same format, no label | Fixed slot, house label |

## Shapes this skill does not fit

A personal editorial letter, one named person's essay to their list, is closer to a blog post than a digest. Apply only the code, plain-text, pre-send and corrections sections, and keep the author's voice.

## References

- samber/developer-relations-skills@devrel-newsletter-deliverability - authentication, unsubscribe headers and spam-folder diagnosis
- samber/developer-relations-skills@devrel-newsletter-sponsorship - slot formats and rates, before the copy reaches the issue
- samber/developer-relations-skills@changelog-writing - the release notes your own items link to
- samber/cc-skills@substack-ghostwriting - the same job on Substack, with its platform features
