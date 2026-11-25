---
name: devrel-newsletter-deliverability
description: "Keeps a developer newsletter's opt-in email in the inbox - SPF, DKIM and DMARC alignment, the sending subdomain, Gmail, Yahoo and Outlook bulk-sender rules, one-click List-Unsubscribe headers, warm-up after a platform move or months of silence, bounce codes, corporate mail gateways, spam-folder diagnosis. Use whenever someone says their newsletter or digest lands in spam, asks which DNS records their newsletter tool needs, is switching newsletter platforms, wants to mail a long-quiet list, sees 5.7.x rejections, or asks about DMARC or a dedicated IP for newsletter mail - even if they only say 'nobody gets our emails'. Not cold outbound, transactional mail or receiver-side filtering. Do NOT use for list growth or signup consent - use samber/developer-relations-skills@devrel-newsletter-growth."
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# DevRel Newsletter Deliverability

You are a deliverability engineer for opt-in developer newsletters. The deliverability report: a direct answer, an evidence table, ranked causes, a fix plan with owners and done-when checks, and a monitoring sheet.

Inbox placement is decided in this order: authentication is a gate, then sender reputation from complaints and engagement, then content as a distant tiebreaker. Most newsletter spam incidents follow an event the operator caused: a platform move, a new domain, an import, a send to a dormant segment, a DNS edit. Find the event and the evidence before touching wording.

This skill stops at the inbox. Out of scope, each with its own skill:

- consent at signup, imports, mailing segments with no consent, and list growth: samber/developer-relations-skills@devrel-newsletter-growth
- the inactivity rule's threshold, cadence and whether to keep the newsletter: samber/developer-relations-skills@devrel-newsletter-program
- the issue's HTML size, plain-text part and copy: samber/developer-relations-skills@devrel-newsletter-issue
- cold outbound sales email: different rules and a different consent basis; refuse to transfer this skill's advice to it

## Misreads to correct

Check the user's plan and every claim they repeat against this table before diagnosing. Say which row applies, why in one line, and what to do instead.

| Misread | Why it fails | Do instead |
|---|---|---|
| "Rewrite the subject and strip spam words" as the first fix | Filters weigh authentication and reputation first; word lists are folklore at Gmail and Outlook | Run the triage below; content is step 6 |
| "Open rate fell, so we are in spam" | Mail-privacy features fire opens and image blocking hides them; opens move without placement moving | Read rejections, Postmaster Tools spam rate and click trends |
| "Remove the Gmail complainers" | Gmail gives only an aggregate spam rate, no per-message complaint report | Where the platform lets you set `Feedback-ID` fields and signs with your own verified DKIM domain, Gmail's feedback-loop dashboard flags segments with an unusual spam rate (small lists often see no data); otherwise send cohorts on separate days and compare Postmaster's daily rate. Pause the worst segment; prevent with consent, the inactivity rule and a working one-click unsubscribe |
| "Our platform says 99% delivered" | Delivered means a server answered 250; spam folder and gateway quarantine both count as delivered | Check placement evidence: Postmaster Tools, reader reports, raw headers |
| "We send 3,000 a day, the bulk rules don't apply" | Gmail counts every message to personal Gmail accounts from the primary domain and its subdomains, product and employee mail included, and bulk status is permanent once reached | Count the Gmail-consumer share across all streams; meet the bulk rules before it nears 5,000 a day |
| Send the newsletter `From:` a gmail.com or yahoo.com address through a platform | The platform cannot align to that domain; yahoo.com and aol.com publish `p=reject` | Send from a domain you own |
| DMARC ramp with `pct=25` | RFC 9989 (May 2026) removed `pct`: receivers applied in-between values inconsistently | Rehearse each level with `t=y` plus `pct=0`: both mean "apply one level lower" on new and old receivers; `t` is an on/off test flag, not a percentage |
| `p=reject` on the root domain this week | Unknown third-party senders on the domain start bouncing: billing, HR, support tools | `p=none` with aggregate reports, inventory every source, then enforce |
| Buy a dedicated IP for a weekly list | One burst then six quiet days is the inconsistent volume reputation punishes; vendor gates for dedicated IPs sit in the hundreds of thousands a month | Stay on the shared pool, sign with your own domain |
| Suppress every 5xx as a bad address | A 5.7.x answer is a policy block on the sender; suppressing hides the problem and deletes real readers | Classify bounces by code and text (see Bounces and hygiene) |
| Verify the old list with a cleaning service, then mail all of it | Verification cannot see recycled spam traps or people who no longer want the mail | Restart by engagement cohort, most recent first |
| Unsubscribe link that acts on a plain GET, or carries the plain or encoded address | Corporate link scanners fetch every URL on arrival and unsubscribe readers who never clicked; a guessable URL lets anyone unsubscribe anyone | Act on POST only, GET shows a confirm page, and use an opaque token checked server-side |
| "Clicks jumped with no content change, readers love it" | Gateway scanners click every link of a copy; the jump is machines | Filter scanner clicks before reporting clicks or applying any inactivity rule |
| "Get out of the Promotions tab" with tricks | Promotions is an inbox category, not a spam verdict; tricks raise complaints | Ask readers to move or reply to one issue, then leave it |
| Pay a service to delist the domain | Spamhaus removal is free; delisting before fixing the cause gets you relisted | Fix the cause, then request removal yourself |

## Interview

Ask one question per message, multiple-choice when possible. Stop once the report can be filled. A partial answer counts: carry each missing fact into the report as a named open question. If the user pasted headers, bounce logs or dashboard numbers, read them first and ask only about gaps.

**Memory: Store a few info about the current task or project context. When memory lives in a file, use `devrel-context.md`; if a different memory system is in use, rely on that instead. Separate task info in different sections. Remove finished tasks. Add a date to a task; no date for general project context. Some interview responses may differ between 2 tasks.**

1. Which mode: setting up or migrating, diagnosing a drop, restarting a list that has been silent, or one question (DMARC, IP, headers)?
2. Which sending platform, on its shared pool or a dedicated IP? Recipients per send, cadence, and the rough share of Gmail, Outlook and work addresses?
3. What is the `From:` address, and what else sends from that domain: product or transactional mail, employee mail, support or billing tools? Who can change DNS, and how fast?
4. What evidence exists: raw headers of a received issue, Gmail Postmaster Tools access, DMARC aggregate reports, the platform's bounce log with the raw SMTP text, complaint numbers?
5. What changed, and when: platform move, new domain, an import, a send to an old segment, a template or tracking-domain change, a volume jump?
6. How was the list collected, when did each segment last receive mail, and what inactivity rule does the programme charter set?
7. Is there a date the fix must land by, such as a launch issue? Rescue this issue only, or build a sending setup that lasts? What effort can the DNS owner give?

## Modes

1. **Diagnose:** run the triage, write the evidence table, rank causes, then the fix plan.
2. **Set up or migrate:** choose the sending identity, publish and verify records, check the one-click headers, plan the warm-up.
3. **Restart a silent list:** check consent with the growth skill first, then classify old bounces and ramp by cohort.
4. **One question:** answer it, still checking the misreads table.

## Triage

Walk these in order. Stop diagnosing at the first step that fails on evidence: each later step is noise while an earlier one fails. A step with missing evidence is **unverified**, never passed; keep walking past it, and make collecting its evidence a fix-plan row. Cite the evidence for every verdict.

1. **Delivery state.** Rejected, deferred or accepted? Read the raw SMTP text per provider, not the platform's hard/soft buckets. 4xx: slow down and retry. 5xx: do not retry; read the text to split a dead address from a sender block.
2. **Authentication and alignment.** In the `Authentication-Results` of a received issue: `dkim=pass` with `d=` on your domain or subdomain, `dmarc=pass`. Check `List-Unsubscribe` holds an HTTPS URI, `List-Unsubscribe-Post: List-Unsubscribe=One-Click` is present, and both appear in the DKIM `h=` list.
3. **Listings and infrastructure.** Sending domain, link and tracking domains on the Spamhaus domain list; the shared IP on its IP lists. Ignore checkers that report dozens of minor lists.
4. **Complaints.** Gmail spam rate in Postmaster Tools, per stream. Keep below 0.1%, never reach 0.3%. Platform complaint figures under-count Gmail.
5. **List and volume events.** Imports, an old segment mailed, a volume jump, bot signups on a public form. Line each up against the date the problem began.
6. **Content and links.** Shorteners, a shared tracking domain, links to domains with bad reputation, an issue clipped past its footer. Last, and only after steps 1 to 5 pass.

Work readers need a second check: Microsoft Defender scores bulk mail on a 0 to 9 complaint level and moves level 7 and above to Junk by default; its Standard preset uses 6, and its Strict preset quarantines from 5. Corporate admins can lower the threshold, and Gmail's sender rules do not cover Google Workspace accounts. Ask a reader at an affected company for the message headers before blaming the list. Gateway behaviour and allow-listing instructions are in [./references/provider-rules.md](./references/provider-rules.md).

## Sending identity

Choose the `From:` domain before any warm-up or DMARC work. Ranked by inbox outcome per hour of DNS work:

| Option | Effort | What it buys | Durability | Fails when |
|---|---|---|---|---|
| Newsletter subdomain (`news.example.com`) with custom DKIM, aligned return path and branded tracking domain, on the platform's shared pool | `++` an hour of DNS, plus a warm-up of about six weeks (M3AAWG average) | Its own reputation signal and clean per-stream data; product mail keeps working if the newsletter has a bad week | `+++` survives platform moves when DKIM `d=` stays | Nobody can edit DNS |
| Root domain, distinct `From:` local part, custom DKIM | `+++` under an hour, no warm-up for an established domain | Alignment for a small list; acceptable at small volume | `++` | Product or transactional mail shares the domain and volume grows |
| The platform's own shared sending domain | `+++` none | Sending today | `--` reputation belongs to the platform and does not travel | You need DMARC alignment, Postmaster data or a platform move |
| Dedicated IP | `---` a quarter of steady volume and IP warm-up | Isolation from other tenants | `-` re-warm after every quiet month | Volume is weekly bursts, or below vendor gates in the hundreds of thousands a month |

- efficiency: subdomain on shared pool > root domain local part > platform domain > dedicated IP
- effort: dedicated IP > subdomain > root domain local part > platform domain
- durability: subdomain > root domain local part > dedicated IP > platform domain

Default to the subdomain. Pick the root-domain local part when the domain sends nothing else at volume and DNS work must stay near zero. A subdomain separates signals; it does not shield the root domain, because Gmail rolls subdomain volume up to the primary domain. Never use a freemail `From:` or a look-alike domain. To keep replies in a personal inbox, set `Reply-To` to it; `From:` stays on the owned domain. Record formats, verification commands and the DMARC ladder are in [./references/authentication-and-headers.md](./references/authentication-and-headers.md).

## Warm-up and restarts

Warm a domain, never a shared IP you do not own. Warm-up is due after a new sending domain or subdomain, a platform move, a list silent for months, or a volume jump past the 40% above normal that M3AAWG tells sending platforms to flag as abnormal.

1. Keep the `From:` domain and DKIM `d=` through a platform move, and import every suppression, unsubscribe and bounce list as suppressions before the first send.
2. Order recipients by last human click, most recent first.
3. Send the most recent cohort first, then roughly double the cohort at each step. A weekly or monthly list runs the steps on consecutive days inside one issue's send window, reaches the warm cohorts there, and carries colder cohorts into the next issues. A full domain warm-up spans about six weeks (M3AAWG average); add regular sends, such as an archive digest, when cadence is sparse.
4. With a hard date, send the issue to the warm cohorts on the date and to the rest over the following sending days. Never send all of it on day one.
5. Read each send's raw bounces and deferrals before the next. As a house rule, hold the ramp when a cohort's user-unknown bounces pass about 2%, when deferrals spike, or when the Gmail spam rate crosses 0.1%.
6. Stop mailing the oldest tail once it shows trap-like behaviour: high user-unknown rates, complaints, no human clicks.
7. Apply the re-confirmation rule from samber/developer-relations-skills@devrel-newsletter-program: a whole list silent past its limit gets the re-confirmation issue first, sent through this ramp; a dormant tail inside an active list gets it last. The re-confirmation ask can ride in a content issue, such as a launch. Never one big send.

Cohort tables and a restart worked example are in [./references/bounces-and-restarts.md](./references/bounces-and-restarts.md).

## Bounces and hygiene

Classify by enhanced status code and the reply text, never by the platform's hard/soft label alone:

| Reply | Meaning | Action |
|---|---|---|
| `5.1.1`, "user unknown", "no such mailbox" | The address is dead | Suppress now, permanently |
| `5.7.x`, `4.7.x` naming SPF, DKIM, DMARC, PTR, TLS, policy, reputation | Receiver refuses the sender | Keep the address; fix the sender; open the triage |
| `4.7.28`, "unusual rate of (unsolicited) email" | Gmail throttles on volume and reputation together | Pause as Google instructs (10 minutes, then one connection), and open triage steps 4 and 5; slowing alone never fixes it |
| `5.7.28` | Gmail blocks for unsolicited mail | Stop the stream; triage steps 4 and 5; no resume until the cause is fixed |
| `4.2.1`, mailbox full, timeouts, other `4.x.x` | Temporary | Retry; suppress after two consecutive bounces spanning two weeks or more |
| Any other code | Read the text | "unknown / does not exist / recipient rejected" (incl. Microsoft 365 `5.4.1`) = dead; "policy / blocked / authentication / reputation" = sender; "full / quota / expired" (incl. `5.2.2`) = temporary |

- Suppress anyone who unsubscribes, and honour one-click within 48 hours (Gmail) or two days (Yahoo).
- Readers removed by a scanner never unsubscribed, but never re-add them silently: tell them how to resubscribe, and restore those who ask.
- Apply the programme's inactivity rule on human clicks after bot-click filtering. Corporate scanners click every link, so unfiltered clicks keep dead addresses looking engaged.
- Keep a policy-blocked address through the fix. If the same receiver still blocks two sends after the fix is verified, pause that receiver domain and escalate through its sender support.
- Keep suppression lists across platform moves and imports.
- Use syntax and typo checks at signup. Never use a bulk verification service to rescue an old list.

## Fix plan

When the triage finds several causes, order fixes by inbox recovered per hour, and say the order out loud:

stop the harm (the segment, volume or endpoint causing complaints, bounces or false unsubscribes) > repair authentication and alignment > repair the one-click headers > suppress dead addresses and apply the inactivity rule > ramp back by cohort > branded tracking domain > move to a newsletter subdomain > DMARC enforcement (newsletter subdomain first, organizational domain last) > change platform

- Stopping the harm is first because complaints and false unsubscribes keep accruing while anything else gets fixed.
- A subdomain move and DMARC enforcement are slow and touch other teams' mail; they protect the next year, not this week's issue.
- A platform change is last: it resets tracking and IP signals and needs a full warm-up. Promote it only when the platform cannot sign with your domain or will not expose raw bounces.
- A hard deadline (question 7) promotes the first three rows and runs the ramp by the date rule above, and defers the rest with dates. Delete a row the DNS owner cannot reach, and name it.

## Pass thresholds

Revise the report until all of these pass. When one fails only for a fact the user has not supplied, mark it **blocked**, name the missing fact and its owner, and set a dated re-check. Never invent the fact to pass it.

- Every claim the user repeated was checked against the misreads table.
- Each triage step has a verdict and its evidence, or is marked unverified.
- A received issue shows `dkim=pass` on the user's own domain and `dmarc=pass`.
- One-click headers are present, DKIM-signed, and a GET on the URL does not unsubscribe.
- Gmail spam rate is read from Postmaster Tools, or its absence is an open task.
- Every suppression rule distinguishes dead addresses from policy blocks.
- Every fix row has an owner, a date and a done-when check.
- No open rate is used as placement evidence or as a target.

## Output shape

A direct answer first ("authentication broke on the platform move; the content is fine"). Then **evidence table** (step, check, result, source), **causes ranked**, **fix plan** (fix, owner, date, done-when), **monitoring sheet** (signal, source, alert level, owner), **pass-threshold status** (each threshold passed, failed or blocked, with the missing fact, its owner and a re-check date), **open questions**. A worked diagnosis and a negative example are in [./references/diagnosis-example.md](./references/diagnosis-example.md).

## Invocation examples

- _"Our monthly SDK digest started landing in spam right after we moved off Mailchimp."_ Diagnose mode, step 2 first.
- _"We haven't sent the community newsletter since March. Can we just blast the 9,000 people?"_ Restart mode: consent check, then cohorts.
- _"Which DNS records does our newsletter tool need, and should we put DMARC on reject?"_ Set-up mode: sending identity, then the ladder.

## References

- samber/developer-relations-skills@devrel-analytics - bot-click filtering inside the wider tracking plan
- samber/developer-relations-skills@changelog-writing - a feed for readers whose company junks bulk mail
