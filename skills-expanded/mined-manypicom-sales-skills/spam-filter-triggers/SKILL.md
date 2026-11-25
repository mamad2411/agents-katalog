---
name: spam-filter-triggers
description: Identify and remove the content-level things that push a cold email into spam — links, attachments, formatting, phrasing and structure. Use whenever the user mentions spam folder, spam filters, spam words, spam score, emails not landing in the inbox, junk folder, or wants an email checked before sending. Also use when open rates are low despite correct authentication and a warm domain.
---

# Spam Filter Triggers

Modern filters are classifiers trained on behaviour, not keyword lists. The old "never write the word free" advice is mostly folklore, and the sites that score your email out of ten are matching against rules that stopped being decisive years ago.

What actually decides placement, in order:

```
1. Authentication and domain reputation     ~60% of the outcome
2. Recipient behaviour — replies, deletions, complaints
3. List quality — bounces, traps, dormant addresses
4. Content and structure                    ~10% of the outcome
```

So if mail is going to spam, check the first three before rewriting the copy. Content is the smallest lever and the one people reach for first. See `email-deliverability` for the rest.

That said, content does matter at the margin, and the margin is where a lot of cold email sits.

## The things that genuinely hurt

**Links.** The strongest content signal. A first cold email should have zero links, or one at most. Every link is something to evaluate, and links to unknown domains score badly.

- **Never use link shorteners.** bit.ly and similar are heavily associated with spam and obscure the destination.
- **Never use a shared tracking domain.** You inherit every other sender's reputation on it. Use a custom one or turn tracking off.
- **Don't link a calendar in step one.** Save it for after they reply.
- **Check the destination's reputation.** Linking to a domain on a blocklist tanks the message regardless of your own standing.

**Attachments.** Never attach anything to a cold email. PDFs, decks and images in a first message from a stranger are treated as hostile.

**Images and HTML.** A plain-text email from a person looks like a person. An HTML template with a logo, a banner and a styled button looks like marketing and gets filtered like marketing.

- No tracking pixel if you can avoid it. Open tracking inserts a remote image, which is a mild negative and produces unreliable data anyway since Apple Mail Privacy Protection.
- No image-only emails. A message that's mostly image with little text is a classic spam shape.
- No fancy signature. Plain text, name, role, company. No vCard, no banner, no social icons.

**Structure that looks bulk-sent.**

- Identical emails to many recipients in a short window. Personalisation genuinely helps here, mechanically, not just persuasively.
- Sending in a burst rather than staggered.
- Excessive punctuation, all caps, coloured text, multiple exclamation marks.
- A subject line in Title Case, which reads as a newsletter.

**Phrasing.** Individual words rarely trigger anything now, but a cluster of promotional language does shift the classification. What to avoid isn't a word list, it's a register:

> "Act now! Limited time offer! 100% FREE guarantee — click here to claim your risk-free trial!!!"

Nothing in that sentence is banned. The combination is what marks it.

Words worth avoiding in cold outbound because they read as promotional, not because they're on a list: guarantee, risk-free, no obligation, act now, limited time, exclusive deal, click here, buy now, cash bonus, and anything with a percentage increase in the subject line.

## What doesn't matter as much as claimed

- **"Spam words" lists.** Mostly obsolete. You can write "free trial" in a normal sentence.
- **Spam-score tools.** They match against SpamAssassin-style rules, which are one input among many and not the decisive one. A score of 0/10 on a burned domain still lands in junk.
- **Email length.** Short is better for replies, not for filters.
- **The word "unsubscribe".** Required in many contexts, and a one-click unsubscribe header is now a bulk-sender requirement rather than a risk.

## The unsubscribe question

For cold B2B outreach, include a plain-text opt-out line. Not a styled footer, not a marketing-platform unsubscribe block.

> Not the right person, or not interested? Just reply "no" and I'll stop.

This works because it's honest, it's low-friction, and a reply is a positive engagement signal even when it's a no. It also gives someone an alternative to hitting the spam button, which is what you're actually trying to prevent — a complaint costs far more than an opt-out.

For bulk sending, `List-Unsubscribe` and `List-Unsubscribe-Post` headers are now required by the major providers. See `outbound-compliance`.

## Diagnosing placement

Content is the last thing to check, not the first.

1. **Seed test.** Send the exact email to your own Gmail, Outlook, Yahoo and a corporate Microsoft 365 account. Where does it land in each?
2. **Read the raw headers.** `Authentication-Results` tells you whether SPF, DKIM and DMARC passed. Fix any failure before anything else.
3. **Check blocklists** for the sending domain and IP.
4. **Check Google Postmaster Tools** for the domain's reputation as Gmail sees it.
5. **Check the list.** Recent bounces or complaints?
6. **Then** strip the email to plain text with no links and seed test again. If it lands, add elements back one at a time to find the offender.

That last step is the only reliable way to attribute a content problem, and it's usually the links.

Placement differing by provider is informative: Gmail inbox and Outlook junk is common and points at content and authentication rather than at general reputation, because Microsoft weights those differently.

## A pre-send content check

```
[ ] Plain text, no HTML template
[ ] Zero or one link, to a domain you control with good reputation
[ ] No link shortener
[ ] No attachment
[ ] No images, no tracking pixel if avoidable
[ ] Custom tracking domain if tracking at all
[ ] Subject in sentence case, 3-5 words, no punctuation marks
[ ] No exclamation marks anywhere
[ ] Plain-text signature
[ ] Plain-text opt-out line
[ ] Reads like a person wrote it to one person
[ ] Merge fields all have natural fallbacks
```

That last item matters more than it looks. `Hi ,` isn't just embarrassing — a batch of identical malformed emails is exactly the pattern classifiers are built to catch.

## Don't do these

- **Don't rewrite copy to fix a reputation problem.** Diagnose in the right order.
- **Don't trust a spam-score tool** as a placement prediction.
- **Don't use a shared tracking domain.**
- **Don't send image-heavy or template-styled cold email.**
- **Don't attach anything.**
- **Don't remove the opt-out** to avoid giving people the idea. They already have the idea, and the alternative is the spam button.
- **Don't keep sending while placement is bad.** Every message into a junk folder deepens the problem. See `bounce-recovery`.

## Related skills

`email-deliverability`, `spf-dkim-dmarc-setup`, `email-warmup`, `bounce-recovery`, `cold-email-copywriting`, `outbound-compliance`
