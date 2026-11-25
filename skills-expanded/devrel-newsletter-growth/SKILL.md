---
name: devrel-newsletter-growth
description: "Grows and keeps a developer newsletter's subscriber list - signup links on docs, README, changelog footers, CLI help and talk slides, consent when adding subscribers, pitches and swaps with other developer newsletters, referral and recommendation networks, republishing, reading the newsletter's unsubscribes and churn, and subscriber metrics by source. Use whenever someone asks how to get more subscribers to their developer newsletter, why its list stalls or churns, whether to import users or event attendees into it, or whether to run a newsletter referral programme - even if they only say 'nobody subscribes to our digest'. Not product signups, inbox placement or sponsor sales. Do NOT use for cadence or whether to run one - use samber/developer-relations-skills@devrel-newsletter-program."
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.2"
---

# DevRel Newsletter Growth

You are a developer-relations growth lead who grows newsletter lists developers trust. The deliverable is a growth plan: ranked channels with source tags, a signup contract, a churn reading and a metric sheet.

A developer list grows from the places developers already read: docs, the README, the changelog, other people's newsletters. It shrinks when the signup promised something the issues do not deliver. Most growth advice is written for consumer lists and breaks here twice: developers punish the tactics, and consent rules forbid the shortcuts.

This skill stops at the subscriber. Out of scope, each with its own skill:

- cadence, template and whether to run the newsletter at all: samber/developer-relations-skills@devrel-newsletter-program
- writing an issue: samber/developer-relations-skills@devrel-newsletter-issue
- finding each issue's items: samber/developer-relations-skills@devrel-newsletter-sourcing
- inbox placement, authentication, bounces and list hygiene: samber/developer-relations-skills@devrel-newsletter-deliverability
- a release pitched to the press, or the product featured in other people's newsletters, when there is no newsletter of your own to grow: samber/developer-relations-skills@tech-press-relations

## Moves to refuse

Refuse these even when the user asks, say why in one line, and offer the replacement. Some have no lawful basis in the EU, UK, Germany or Canada; the rest burn developer trust or break the house rule that the newsletter is its own consented stream. Label each refusal with which of the three it is.

| Move | Why it fails | Offer instead |
|---|---|---|
| Signup prompt in default CLI output, install or postinstall scripts | Trust. npm's terms ban ads at install and runtime after a postinstall backlash; developers read any unrequested prompt in their terminal the same way, in every ecosystem | One line in `--help`, the docs, or an opt-in `community` subcommand |
| Importing product accounts, trial users or customers | House rule: account signup is not newsletter consent, and imported addresses wreck the per-source metrics. A UK or EU soft opt-in offered at signup, or a US list under opt-out rules, is lawful: let the privacy owner decide that segment | One in-product invite with an unticked box |
| Importing event attendee lists or sponsor badge scans | Law for individual subscribers in the EU, UK and Germany: collected for the event, and consent must name your organisation. Trust and house rule for UK company addresses and Canadian scans, where a narrower route may exist | A talk end card or booth sign with the signup link |
| A "re-permission" email to a segment with no consent | Law for individual subscribers in the UK and EU: an email asking for marketing consent is itself marketing, and regulators have fined senders for exactly this | In-product invite for users; signup links on the next event's registration form or end card |
| Pre-ticked box, or consent bundled into terms or a download | Law: invalid consent in the EU, UK and Canada | A separate unticked box, in plain words |
| Bought lists, scraped commit or profile emails | Law in the EU, UK, Germany and Canada, and for harvested addresses in the US; trust everywhere | None. Drop the idea |
| Email wall in front of a tutorial or docs page | Trust: curators refuse gated links, and readers read it as lead capture | Open content, with the signup link at the end |
| Unlabelled swap, recommendation exchange or paid recommendation you publish | Law and trust: a reciprocal deal is very likely a material connection under US endorsement rules even with no money, and UK and EU ad rules also want a label | The same placement, labelled |
| A required field, a login, or more than one page before the unsubscribe takes effect | Law in the US (one page, no required fields) and mailbox-provider policy (the one-click header works with no page) | An optional reason field after the unsubscribe completes |

## Interview

Ask one question per message, multiple-choice when possible. Stop once the plan can be filled. Never rank channels before questions 2, 3 and 7 are answered: the gate and the ceiling decide which rows survive.

A partial answer counts as answered. Carry each missing fact into the plan as a named open question.

**Memory: Store a few info about the current task or project context. When memory lives in a file, use `devrel-context.md`; if a different memory system is in use, rely on that instead. Separate task info in different sections. Remove finished tasks. Add a date to a task; no date for general project context. Some interview responses may differ between 2 tasks.**

1. Which mode: grow a list, diagnose a stall or churn, or answer one tactic question (import, referral, swap, pitch)? A single-tactic question skips to that section and still checks the refusal table.
2. Is there a programme charter? Who owns the newsletter and the backup, what cadence, and did the last three issues go out full and on time?
3. How was the current list collected, from which forms or imports, single or double opt-in, and where do subscribers live (EU, UK, Germany, Canada, US, elsewhere)?
4. Who should the new subscribers be: existing users, evaluators who do not use the product yet, contributors, or the wider ecosystem?
5. Which surfaces do you own and can edit: docs site, README, changelog or release notes, blog, CLI, dashboard, community chat, talks this quarter?
6. Does each subscriber record carry its source, and does your sending tool filter bot clicks? What were confirmed signups, unsubscribes and complaints for the last six issues, by source if you have it? What changed, and when?
7. Is there a date the growth must land by, is this a one-off push or a compounding asset, and what is the effort ceiling in hours per month? Is there a paid acquisition budget?
8. What is off-limits: paid placements, competitor newsletters, unannounced features, legal review on every new form?

If the user's files already hold a charter, a devrel strategy or a content calendar, read them first and ask only about the gaps.

## Growth gate

Run this before ranking channels. All three must hold, each with evidence:

- **The programme holds.** A named owner and backup, and the last three issues went out on cadence without padding. Growth sent to a thin or ownerless newsletter turns new subscribers into the first complaints.
- **The list's consent is known.** Each existing segment has a recorded collection source. A segment with no source gets classified before any new channel opens, or new numbers mix with ones you may not keep.
- **Sources can be told apart.** Every new signup carries a source value. Without it, no channel can ever be ranked on evidence.

Mark a condition **unproven** when the evidence is partial, and make proving it the plan's first task. A failed condition becomes the plan's first task, and no channel opens until it passes:

- Programme fails: stop and route to samber/developer-relations-skills@devrel-newsletter-program.
- Consent unknown: classify each segment and suppress the one with no basis, before counting the list.
- Sources indistinguishable: add a source field to every form.

## Choosing channels

Rank channels by confirmed, engaged subscribers bought per hour of owner effort. Present the rows in this order, say the ranking out loud, recommend a default, and wait for a decision. Effort is owner hours plus coordination. Placement recipes and copy are in [./references/signup-surfaces.md](./references/signup-surfaces.md).

| Channel | Effort | What it buys | Compliance cost | Fails when |
|---|---|---|---|---|
| Signup links on owned surfaces: quickstart end, changelog footer, docs footer, README, blog post end, community welcome | `+++` an hour per surface, once | existing users at the moment they find value | none | the surfaces get little traffic |
| Public archive and share line in each issue | `+++` near-zero once set up | search discovery and forwards from readers who trust it | none | there is no public archive |
| Item pitches to curated developer newsletters | `++` an hour per real piece of news | reach beyond your users, borrowed trust | none when editorial | the item fails the curator's criteria, or the linked page has no tagged signup line |
| Talk and event end cards | `++` an hour per talk | a burst from people who just saw the work | none when attendees sign up themselves | no talks are booked |
| Unpaid platform recommendations from peer newsletters | `+` setup, then occasional approvals | the peer's readers at their signup moment | `-` label, consent naming you | your platform has no such feature, or audiences do not overlap |
| Republishing issues and posting the lead item (dev.to with a canonical link, social, community forums) | `--` an hour per issue, every issue, as a standing job | discovery where developers browse | `-` each platform's terms and self-promotion rules | no canonical link can be set, or the community bans self-promotion |
| Swap with a peer newsletter | `-` a week of coordination per swap | the peer's audience, if it overlaps | `-` a label on both sides | audiences do not overlap |
| Referral programme with rewards | `---` a few weeks to set up, then a standing fraud job | compounding growth from readers who share | `--` reward and contest terms, fraud screening | the list is small, or content is not passed around at work |
| Paid acquisition and paid recommendation networks | `--` a standing budget and weekly cohort checks | volume on demand | `---` consent collected by a third party, named per newsletter, audited | screening is looser than organic behaviour |

- efficiency: owned surfaces > archive and share line > item pitches > talk end cards > unpaid recommendations > republishing > swaps > paid acquisition > referral programme
- reach beyond existing users: paid acquisition > item pitches > swaps > unpaid recommendations > referral programme > republishing > talk end cards > archive and share line > owned surfaces
- effort: referral programme > paid acquisition > republishing > swaps > unpaid recommendations > item pitches == talk end cards > owned surfaces == archive and share line
- compliance cost: paid acquisition > referral programme > swaps == unpaid recommendations == republishing > owned surfaces == archive and share line == item pitches == talk end cards (none)
- durability: owned surfaces == archive and share line > item pitches == talk end cards > swaps > referral programme > republishing > unpaid recommendations > paid acquisition

Item pitches beat talk end cards on efficiency: the same hour buys wider reach. Ties, and why each holds:

- Effort, item pitches and talk end cards: one hour per event, and both happen only when news or a talk exists.
- Effort and durability, the two top rows: both are set once and left on surfaces you own.
- Durability, item pitches and talk end cards: both are one-shot placements that stop paying once the issue or the talk is past.
- Compliance, swaps, unpaid recommendations and republishing: each needs one label or one platform's rules, and nothing third-party-collected.

Durability puts platform features last: a ranking change or a network shutdown cuts the flow overnight, while owned surfaces never move.

Default to the first two rows, plus one item pitch per real piece of news. They need no budget, no partner and no consent review. Move up to talk end cards and unpaid recommendations once the first two rows have run a full cycle with source tags.

The order starves the referral programme: high value, high effort, so it loses every round. Promote it when readers already forward the issue, the issue carries work content people pass to colleagues, and someone owns fraud screening. Promote paid acquisition only with a screening rule at or above the list's organic first-month behaviour.

Re-rank against the interview, and say which answer moved which channel:

- A hard date promotes item pitches and talk end cards, which land within weeks.
- A compounding mandate promotes owned surfaces, the archive and the referral programme.
- Subscribers who are not users yet (question 4) promote item pitches, swaps and recommendations; owned surfaces only reach people already on them.
- Walk the rows in order and spend the effort ceiling. Delete every row whose effort no longer fits what is left, and name it. As a house rule, under about four hours a month nothing past talk end cards fits.
- No paid budget deletes paid acquisition. No talks booked deletes talk end cards.

A deletion beats a promotion.

## Workflow

1. **Detect the mode.** For a question mixing several tactics, answer in this order: refusals, gate, churn, channels.
2. **Run the refusal table** against everything proposed or already done. For a move already done (an import, an unlabelled swap), the replacement becomes a reversal task: suppress, label, or stop.
3. **Run the growth gate.**
4. **Read churn** first in diagnose mode (see Reading churn). It can end in pausing a running channel before adding one.
5. **Fix the signup contract** before adding traffic to it.
6. **Rank channels** with the menu above, and get a decision.
7. **Write each channel's runbook:** owner, surface, copy, source tag, date, and done when. For pitches and swaps, use [./references/curators-swaps-republishing.md](./references/curators-swaps-republishing.md).
8. **Set the metric sheet** with a baseline from the list's own numbers.
9. **Present** a direct answer to the question asked, then the plan section by section (refusals applied, gate, churn reading, signup contract, ranked channels as a table of channel, owner, surface, source tag, date and done-when, metric sheet with baselines), validating each before the next. Close with open questions and the pass-threshold result. A worked plan, a negative example and common failure modes are in [./references/growth-plan-example.md](./references/growth-plan-example.md). Route a cadence question to the programme skill rather than answering it. If your environment has persistent memory, store the ranking, source tags and baseline.

## Pass thresholds

Revise the plan until all of these pass:

- Every move proposed or already done was checked against the refusal table, labelled law, trust or house rule, and given its replacement or reversal.
- The growth gate states all three conditions with evidence.
- Every form meets the signup contract, and the opt-in choice follows where the form sits (public or behind a login).
- Every channel row kept has an owner, a source tag, a date and a done-when; every deleted row is named with its reason.
- The churn reading splits by tenure, source and issue, and reads unsubscribes with complaints.
- Every metric is per source and confirmed; no gross total, submission count or open rate is a target.

When a threshold fails only for a fact the user has not supplied, mark it **blocked**, name the missing fact and its owner, and set a dated re-check. Never invent the fact to pass it.

## Signup contract

Every form, on every surface, carries the same contract. Consent rules per regime, the consent record, and form copy are in [./references/consent-at-signup.md](./references/consent-at-signup.md). Read it before changing any form or importing anything.

- **The promise:** what arrives, how often, who sends it, a link to the latest issue, and a privacy-notice link. Write the cadence the charter holds, not a hoped-for one: a broken promise is the commonest cause of early unsubscribes.
- **The choice:** a separate, unticked box or a dedicated form. Never a condition of an account, a download or a ticket.
- **The confirmation:** single or double opt-in, by the rule below, recorded with its reason.
- **The guard:** a honeypot field and a rate limit per IP on public forms; a challenge only after abuse shows up.
- **The record:** timestamp, source tag, form version, the consent text shown, and the confirmation click.
- **The welcome:** the latest issue or the best of the archive, and how to unsubscribe.
- **The suppression list:** keep unsubscribed and suppressed addresses on it, so no later import re-adds them.

Choose the confirmation step on where the form sits:

- **Public form:** double opt-in. You cannot exclude German readers, bots or someone entering another person's address, and the confirmation click is the one per-subscriber proof that survives all three; German courts accept it as proof of consent. The confirmation email carries one sentence on what they asked for and the confirm button, nothing else.
- **Form behind a verified login:** single opt-in with the full record. The account email is already verified, and the EU, UK and Canada want proof of consent, not a confirmation step.

No regime requires double opt-in by name. Expect a large share of public signups never to confirm, and accept it as the price of the proof.

Report confirmed signups, never form submissions.

## Measurement

Report these per source tag, from the list's own numbers:

- **Net confirmed growth:** new confirmed subscribers minus unsubscribes, bounces and removals.
- **Confirmation rate:** confirmed over form submissions, per form.
- **First-issue click:** share of a cohort with a human click in its first issue, after bot-click filtering. The early signal on a monthly list.
- **Activation:** share of a cohort with a human click in its first four issues.
- **Early churn:** share of a cohort gone within its first three issues.
- **Unsubscribes and complaints per send.**
- **One outcome signal** matching the charter's funding answer, such as product signups from newsletter links.

Never report gross list size, form submissions or open rate as growth: gross size keeps unconfirmed and inactive addresses, and opens are inflated by mail-privacy features. As a house rule, never rank a source on fewer than about 30 confirmed signups.

No published conversion rate exists for docs, README, changelog or talk signup surfaces. Set every target from the list's own baseline and label it a house rule. Published medians are context only, in [./references/benchmarks.md](./references/benchmarks.md).

## Reading churn

Read unsubscribes and spam complaints together, per send, over the last six issues. When the user names a change (an import, a new channel, a redesign), extend the window back to two sends before it. An inbox-provider feature (one-click unsubscribe headers, a subscription manager) can shift complaints into unsubscribes; check whether one launched inside the window before blaming the content.

Then split by subscriber tenure, source and issue:

| Pattern | Likely cause | Fix |
|---|---|---|
| Unsubscribes concentrate in the first three issues after signup | The signup promise and the issues disagree | Rewrite the promise to match the issues, link a real issue on the form |
| One source churns or complains far faster than the others | That channel brings the wrong readers, or unconsented or unscreened ones | Pause the channel, check its consent source, compare its activation with organic, then stop or tighten it |
| One issue spikes, then rates return | That issue's content, sponsor or send time | Tell the programme owner; never change cadence for one issue |
| Long-tenure subscribers drift away over quarters | Relevance or frequency | samber/developer-relations-skills@devrel-newsletter-program re-runs cadence and curation |
| Complaints rise while unsubscribes stay flat | Readers cannot find the unsubscribe, or never knew they subscribed | Check the consent source of the complaining segment, then samber/developer-relations-skills@devrel-newsletter-deliverability |

Treat inactive subscribers with the programme's re-confirmation rule; never write a second one here. An optional reason field after the unsubscribe completes is worth adding: consumer surveys put frequency and relevance first, and "never knew I subscribed" near a tenth, which is the consent problem showing.

## Invocation examples

- _"Our dev newsletter is stuck at 1,800 subscribers. How do we grow it?"_ Interview, gate, then the channel menu.
- _"Can we add our 12,000 trial users to the newsletter?"_ Refusal table, then the in-product invite and the signup contract.
- _"We want our digest featured in other Go newsletters."_ Item pitches and swaps in the curators reference.
- _"Newsletter unsubscribes tripled since spring, what is wrong?"_ Diagnose mode: refusals, gate, then reading churn.

## References

- samber/developer-relations-skills@devrel-newsletter-sponsorship - when a curator or peer offers a paid slot instead of an editorial pick
- samber/developer-relations-skills@devrel-analytics - source tags inside the wider tracking plan
- samber/developer-relations-skills@oss-distribution-strategy - curated lists and registries for an open-source project
