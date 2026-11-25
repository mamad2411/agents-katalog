---
name: spam-nuke
description: "Use when the user wants to report spam email, cold outreach, robocalls, spam texts or phishing through every legitimate channel. Maps the sender's supply chain (mailboxes, sending platform, domains, carrier, blocklists, regulators) and files with each layer's official channel, using whatever tools you have: email, browser, shell, phone. Triggers: 'nuke this spammer', 'report spam', 'do something about these spam calls', 'file FCC complaints', 'report this phishing'."
---

# Spam Nuke

Trace a spammer's whole supply chain and report them to every layer of it, using only the **official channels** built to receive these reports: abuse desks, blocklists, carrier traceback, regulators. Nothing here is a hack, a gray area or vigilantism. The internet already has an immune system; it's under-used because reporting is tedious. You make it cheap.

## Why: a dark forest for spammers

Spam runs on an asymmetry. Sending costs almost nothing, and fighting back costs the recipient an hour of header-reading, WHOIS lookups and web forms. So almost nobody fights back, and the expected cost of hitting any one inbox is roughly zero.

An agent removes the recipient's cost. Spammers can't tell which inboxes have an agent behind them, so every message becomes a lottery ticket for an expensive event: a suspended mailbox tenant, a terminated sending account, the brand domain on a blocklist, a traceback that cuts off their voice carrier, or a regulator file with their name on it.

    expected cost per message = P(recipient is armed) × cost of a full-stack response

More armed recipients raise P. Hitting the whole stack instead of one throwaway address raises the cost. When the product gets high enough, the rational strategy for senders is Liu Cixin's dark forest: don't reveal yourself. In practice that means only contacting people who opted in.

Two consequences shape how you work:
1. **Hit what's expensive to replace.** A sender address takes minutes to replace, a warmed mailbox weeks, and a brand domain's reputation months. A voice carrier's network access is existential. Report everywhere, but put effort into the expensive layers.
2. **Precision is the weapon.** These systems weigh reports by reliability. One wrong report against a sender the user actually signed up with does more damage to the deterrent than ten missed spammers. Hence the ground rules below.

The full reasoning and every layer in depth, with sources, is in `references/supply-chain.md`. Read it before your first run.

## The supply chain at a glance

| Layer | What it is to them | Official channel | What a report costs them |
|---|---|---|---|
| **Lead data** | The vendor that sold your address (Apollo, ZoomInfo, …) | GDPR Art. 17/21, CCPA deletion, CA [DROP](https://privacy.ca.gov/drop/) | Removes you from *every future* buyer's list; the most durable win for the user |
| **Sending domains** | Lookalikes (`getacme.co`) that shield the brand | Registrar abuse (ICANN RAA §3.18), Spamhaus DBL/SURBL/URIBL | Weeks of warmup wasted per burned domain |
| **Mailboxes** | Google Workspace / Microsoft 365 seats, warmed for weeks | `abuse@<sending-domain>` (Google monitors it on every Workspace domain), `abuse@outlook.com`, "Report spam" | Seat or whole-tenant suspension; each complaint is a big fraction of a low-volume inbox's traffic (Gmail wants under 0.1%) |
| **Sending platform** | Sequencer (Instantly, Smartlead, lemlist, Apollo…) or ESP (SendGrid, Mailgun, SES…) | Platform abuse / trust & safety | Account termination: campaigns, lists and prepaid plan gone. ESP rules are stricter than the law |
| **Brand domain** | The real domain in links and signature | Spamhaus DBL, SURBL, URIBL (they match body links) | Months: hurts *all* their mail, including invoices and customer replies |
| **Hosting / CDN** | Landing page, DNS | Host abuse contact | Low for spam, high for phishing; high if they run their own SMTP on a VPS |
| **Payment rails** | Merchant account behind a scam storefront | Processor fraud report, card dispute | The chokepoint for scam and affiliate spam; irrelevant for B2B SaaS |
| **The company** | Legal exposure | FTC, state AG, EU DPA, ICO, CASL, ACMA, PDPC | Aggregated into enforcement; per-message penalties |
| **Voice carrier** (calls) | VoIP provider that put the call on the network | FTC/FCC complaints → Industry Traceback Group | Removal from the FCC Robocall Mitigation Database means every US carrier must refuse its traffic |
| **Caller-ID numbers** (calls) | Rented or spoofed numbers | DoNotCall.gov (published daily to carriers) | "Spam Likely" labels → answer rate collapses → number burned |
| **Messaging platform** (texts) | Twilio, Bandwidth, Telnyx… (find via carrier lookup) | Platform abuse; 7726 to the carrier | Campaign or number suspension; carriers penalize the platform |

## Use whatever tools you have

This skill doesn't assume particular tools. Use the best one you have for each step:

| Step | Good tools | Fallback |
|---|---|---|
| Get the evidence | Mail access (Gmail/Outlook API, IMAP, an email MCP) to pull the raw message; call log / voicemail / SMS access (phone integration, messaging bridge) | Ask the user for "Show original" output, screenshots or a call-log export |
| Recon | Shell: `dig`, `whois`, the bundled scripts | Web lookups: lookup.icann.org, abuse.net, MXToolbox, a CNAME lookup site |
| Email reports | Send from the user's own mailbox, original attached as `message/rfc822` | Write the email out in full for the user to send |
| Web-form complaints (FTC, FCC, Spamhaus, regulators) | Browser automation | A pre-filled field-by-field draft |
| Phone-only channels (7726, ScamShield app, Report Junk) | Do it if you control the phone | A ready list of messages and numbers for the user |

If you can't reach a channel, write the filled-in draft and put it on the user's checklist. Don't skip a channel without saying so.

## Ground rules

1. **Confirm it's unsolicited before reporting.** Search the user's mailbox, contacts and accounts for earlier correspondence, signups, purchases or a newsletter they joined. If they opted in, unsubscribe instead and stop. **The Spam folder is not proof:** in testing, about a third of a real Spam folder was retail newsletters, event venues and charities the user had probably signed up for, sitting next to genuine spam.
2. **Only claim what the evidence shows, under the law that actually applies.** In the US, unsolicited email is *not* illegal by itself: CAN-SPAM is an opt-out law. UK law allows compliant B2B email to corporate addresses. Cite a violation only when the message shows it: forged or misleading headers, a deceptive subject, no postal address, no working opt-out, mail after an opt-out, a call to a Do Not Call number, or a robocall without consent. Platform policies are often stricter than the law (most email platforms ban purchased lists), so "unsolicited, no prior relationship" is a valid *abuse-desk* complaint even when it isn't a legal violation. Never invent or embellish. Government forms are filed in the user's name, and many ask them to confirm the information is true.
3. **One report per channel per incident.** Combine related messages into one report per recipient, and check the ledger first (see "Finish with a record"). Volume doesn't help: these systems aggregate across reporters, so duplicates only add noise and cost you credibility.
4. **Don't engage with scams.** With scams, phishing and robocalls, never reply, click body links, load images, "press 9 to be removed" or call back; that only confirms a live target. The one exception is a **real, identifiable company**: there, the official opt-out (`List-Unsubscribe`, or a one-line removal request) is allowed and useful, because continued mail after 10 business days is a clear CAN-SPAM violation (see the opt-out tactic in `references/supply-chain.md`). Never retaliate beyond reporting: no hacking, DoS, signup-bombing or prompt-injection replies to AI spambots.
5. **Report as the user, honestly.** Use the user's real name and contact details, and disclose that an AI agent prepared the report for them (template in `references/report-formats.md`).
6. **The user sets how much you decide alone.** There are three modes, really careful → a bit careful (the default) → sicko mode (see below). Analysis is always read-only. What changes between modes is when filing needs the user's OK.

## Modes: really careful → a bit careful → sicko mode

**First run** (no ledger yet): before anything else, state the three choices in one line each and ask which one they want:

> How hands-on do you want to be? **🧐 Really careful:** you approve every report word for word. **🙂 A bit careful:** I show spam in batches of 10, most certain first, and report them unless you say otherwise. **😈 Sicko mode:** I sweep everything and file it all, then send you a digest.

Later runs: use the mode recorded in the ledger, or the user's words ("be careful", "just do it", "sicko mode", "go ham"). If the user doesn't pick, or just says "go", use **a bit careful**.

**Same in every mode:** ground rules 1–5. Check the user didn't sign up, claim only what the evidence shows, file one report per channel per incident, never engage scams, and disclose that an agent prepared each report. Never report a sender the user has a relationship with. Never file a lawsuit or send a legal threat.

| | 🧐 **Really careful** | 🙂 **A bit careful** (default) | 😈 **Sicko mode** |
|---|---|---|---|
| **What needs the user's OK** | Every outgoing report, shown word for word | Nothing per item. Batches of 10, most-likely-spam first, one-line blurb each; **reported by default** unless the user excludes them ("skip 3 7", "unsub 5") | Nothing. Pre-authorized, with a digest afterwards |
| **Scope** | Only the emails or calls the user pointed at | Those, or a sweep of the Spam folder or voicemail | The whole Spam folder and voicemail, and new spam as it arrives if you have a scheduler |
| **Triage** | Nothing skipped automatically; risks are flagged on the card | Prior relationship, newsletter or retail signals, or LOW confidence → "probably subscribed: unsubscribe instead?" list | Same filters. Anything that isn't high-confidence B/C/C2/D goes to a review queue, not filed |
| **Channels** | Platform-embedded abuse links, platform or ESP abuse desk, mailbox provider, "Report spam" | + blocklists, registrar, host, Reply-To inbox provider, data-deletion requests | + regulators (spam@uce.gov, ReportFraud, FTC/FCC for calls, national regulators), SpamCop, automatic escalation for repeat offenders (state AG, second-tier providers), California DROP |
| **Opt-out tactic** (identifiable companies) | Off | Ask per company | On for category B |
| **Legal** | Never | Never | Prepare evidence packets for TCPA / state email laws; still never file |
| **Volume guard** | n/a | n/a | At most ~50 outbound report emails a day from the user's account, spaced out, so their own mailbox doesn't get flagged for bulk-forwarding spam. Web forms: one per incident |
| **Afterwards** | Ledger | Ledger | Ledger + a digest: what was filed and where, what got queued for review, what was skipped and why |

**A bit careful: the batch view.** Run `python3 scripts/triage.py --prior prior.json [--ids ids.json] [--page N] *.eml`. Build `prior.json` first by searching the user's mailbox: for each sender domain, count mail outside Spam and mail the user sent to it. The script then:
- **sorts by how likely each email is to be spam** (a 0–100 heuristic with reasons: impersonation, forged domains, a Reply-To on another domain, hacked-host scams, scam/phishing/predatory-academic wording, cold-email sequencers; minus for compliant newsletters, personal one-off senders and retail wording);
- shows **10 at a time**, each with a one-line blurb: category, score, sender, subject, an **open** link, why it looks like spam, and where it would be reported;
- ends each batch with: *"I'll report all N unless you say otherwise: `skip 3 7`, `unsub 5` (you signed up), `details 2` (full card), or `stop`."* Any reply that doesn't exclude an item counts as yes for it, e.g. "go" or just "skip 4". The next batch follows.
- lists, after the last batch, what it is **not** reporting by default: "unsure" items (score under 40) and anything the user has had mail with (offered as `unsub` instead). `report N` moves one up.

Silence is not consent: if nobody replies (e.g. an unattended scheduled run), nothing is filed in this mode. Scores only set the order and the default. The ground rules still apply to every item, and the user's reply is the final call.

**Review card** (really careful, or `details N`): run `python3 scripts/parse-headers.py --card [--gmail-id ID] message.eml` and add the recon results. Each card has:
- subject, sender, a link to open the original, and a ~200-character intro so the user can recognise it at a glance;
- what was found at each layer and the reports you'd file;
- prior-relationship evidence;
- your category call and confidence;
- the choice: report / skip / unsubscribe instead.

Group emails from the same operation (shared sending account or Reply-To) into one card. In **really careful** mode, also show the exact text of each outgoing report before it goes. Open every review and every batch with:

> ⚠️ Every report goes out in your name to real abuse teams. Reporting mail you actually signed up for, or a real contact, is a false positive: it wastes their time, weakens genuine reports, and can hurt a legitimate sender. If unsure, skip it or unsubscribe instead.

**Trust ladder.** Earn autonomy rather than assuming it. After a clean run, where the user approved essentially everything you proposed and flagged no false positives (~20+ cards), offer to move up one level. If the user flags a false positive, or a provider replies that a report was mistaken, drop down a level, note what went wrong in the ledger, and tighten the triage rule that let it through. Record the current level in the ledger so it persists between runs.

## Triage first

- **A. Marketing they signed up for:** unsubscribe and stop.
- **B. Cold outreach from a real, identifiable company:** follow the Email workflow, and send the official opt-out once if no opt-out has been sent yet.
- **C. Anonymous or deceptive commercial spam:** follow the Email workflow and don't engage.
- **C2. Sent from a hacked legitimate site** (an old domain unrelated to the pitch, sent from a shared-hosting server per `X-AntiAbuse`, with replies going to a freemail address): the domain owner is a *victim*. Report it to the host as a compromised account, quoting the `X-AntiAbuse` lines. Report the freemail Reply-To to its provider (e.g. the Gmail abuse form). Don't blocklist-report the victim's domain as a spammer.
- **D. Phishing, fraud or impersonation:** follow the Email workflow, prioritizing takedowns: the client's "Report phishing" button, `reportphishing@apwg.org`, Google Safe Browsing, the registrar and host, and the impersonated brand's security contact. Use IC3 or the police only if money or credentials were lost.
- **E. Spam calls, robocalls or voicemail:** follow the Calls workflow.
- **F. Spam texts:** follow the Texts workflow.

## Email workflow

**1. Get the raw message.** Full headers matter. Gmail API: `users.messages.get` with `format=raw`, or ⋮ → Show original → Download original. Outlook: View message source. Apple Mail: Save As → Raw Message Source. Pasted headers are second-best; the sender's domain alone is the minimum.

**2. Identify the stack.** Run `python3 scripts/parse-headers.py message.eml` (`--no-dns` skips lookups). It reports:
- **★ Platform-provided abuse channels:** sending platforms often embed their own abuse channel in the message. Examples: Instantly's `X-Mail-Abuse-Inquiries` (a per-message report URL), Mailchimp's `X-Report-Abuse` (with account and campaign IDs), HubSpot's `X-Report-Abuse-To`, cPanel's `X-AntiAbuse` (names the exact server and account), and `Feedback-ID` (identifies the sending account at SES, Alibaba and others). These are the most precise official channels there are. Use them first, and quote the IDs in every other report.
- **Verified sending server:** the hop your own mail server recorded. Everything below it in the `Received` chain is the sender's own claim and can be forged. Don't report IPs or hostnames that appear only in the forged part.
- **Sending service:** the mailbox provider (Google Workspace / Microsoft 365 / Gmail / Outlook), the ESP fingerprint (including Alibaba Cloud DirectMail and Net263), and the **sequencer** behind tracking links (resolved via CNAME: Instantly, Smartlead, lemlist, …).
- **Reply-To mismatch:** operations rotate sending domains but keep one reply inbox. A different Reply-To domain is usually the operation's **persistent asset**, so recon it and report it. If it's a freemail inbox (Gmail, Outlook, Tuta, QQ), the parser prints where to report the address.
- **Link hosts and brand domain:** the domain in links and signature, as opposed to the (often lookalike) sending domain. They get different reports.
- **Payload hosted on a legitimate platform** (Google Cloud Storage, Firebase, Azure Blob, R2/Pages, GitHub Pages, …): report the **exact URL** to that platform's abuse channel and Safe Browsing. The platform is not the spammer's brand.
- **Flags:** a display name impersonating the recipient, or a From domain on a TLD that doesn't exist (forged). Never report a forged or spoofed domain; check DMARC/DKIM alignment and report the authenticated domains instead.
- **Company confidence:** if it's LOW/UNKNOWN, or the domains disagree, investigate before filing with a regulator.

**3. Map the supply chain.** Run `bash scripts/recon.sh <domain>` for the sending domain, the brand domain and the Reply-To domain. It reports the registrar and its abuse contact, **domain age** (rotating sending domains are typically months old while the Reply-To or brand domain is older), MX (Workspace/M365/263…), the host's IP owner, SPF includes (other sending platforms), DKIM, CNAMEs and **current blocklist status**. For IPs, run `bash scripts/check-lists.sh <ip>…`. An obvious spammer that isn't listed anywhere is exactly where a blocklist report adds new evidence. Confirm each abuse address on abuse.net or the provider's own abuse page; `references/report-targets.md` is a starting point, not the final word.

**4. File, most expensive layer first** (see the table above):
- **Sending platform:** the platform-provided channel from step 2 if there is one (e.g. Instantly's per-message report link), otherwise the ESP's or sequencer's abuse desk.
- **Mailboxes:** `abuse@<sending-domain>` for Google Workspace, or `abuse@outlook.com`. Plus "Report spam" / move to Spam in the user's client.
- **Brand and sending domains:** Spamhaus (submission portal), SURBL, URIBL. Include the body link domains.
- **Lead data:** deletion requests to the likely vendors, and DROP for California residents.
- **Regulators**, chosen by where the user and sender are and by which violations are actually present. US: forward to `spam@uce.gov`, plus ReportFraud.ftc.gov for deceptive mail. EU: the data protection authority. UK: ICO (individuals only). Canada: Spam Reporting Centre. Australia: forward to `report@submit.spam.acma.gov.au`. Singapore: PDPC.
- **Registrar and host:** the full report for phishing; a brief one otherwise.
- **SpamCop**, if the user has an account, and **AbuseIPDB** for IPs that are actually abusive (not Google's or Microsoft's shared IPs).

Templates are in `references/report-formats.md` and endpoints in `references/report-targets.md`.

## Calls workflow (robocalls and voicemail)

**1. Gather, per call:** the caller-ID number (report it even if it may be spoofed), the user's number, the date and time, any callback number, the **company or product named** (the seller is the most actionable detail), and the voicemail transcript or recording.

**2. Clean the list.** Remove duplicates and group by caller and by seller. Leave out the user's contacts, businesses they actually deal with, calls they returned, and anything that looks wanted (appointments, deliveries, 2FA). List anything ambiguous for the user rather than reporting it. Check whether the user's number is on the Do Not Call Registry and since when, because that changes what's illegal.

**3. File the reports (US):**
- **FTC:** [DoNotCall.gov → Report Unwanted Calls](https://www.donotcall.gov/report.html) (no money lost) or ReportFraud.ftc.gov (money lost). Include the number that received the call, the caller ID, any callback number, the date/time, whether it was a recording, and the seller's name. Reported numbers go to carriers and call-blocking partners every business day.
- **FCC:** [consumercomplaints.fcc.gov](https://consumercomplaints.fcc.gov) → Phone → "Unwanted calls/texts" → "All other unwanted calls/messages". International numbers go in Additional Information. These complaints help decide which campaigns get traced back to the originating carrier. Never file twice for the same call. For a repeat caller, one complaint listing every date and time is stronger than many copies; where the form allows only one call per complaint, file one per distinct call event.
- **Voice provider:** run a carrier lookup on the caller ID. If it's a real (not spoofed) VoIP or CPaaS number, report it to that provider's abuse desk too.
- **Do Not Call Registry:** register the number if it isn't (the confirmation email must be clicked within 72h).
- **Carrier:** block and report in the phone's or carrier's spam-call tool.
- **State attorney general:** for repeat offenders, especially when the seller is identifiable.

**Elsewhere:** Canada: CRTC National Do Not Call List complaint. UK: TPS, then the ICO nuisance-calls form. Australia: ACMA / Do Not Call Register. Singapore: the ScamShield app (answered calls only), plus the PDPC DNC complaint form for telemarketing. Other countries: the national telecom regulator. Details are in `references/report-targets.md`.

## Texts workflow

- **Forward to 7726 ("SPAM")** from the receiving phone (most US, UK and Canadian carriers), and use "Report Junk" (Apple Messages) or "Report spam" (Google Messages).
- **Carrier lookup on the sender:** if it's a CPaaS number (Twilio, Bandwidth, Telnyx, …), report to that platform. Twilio: [twilio.com/en-us/help/abuse](https://www.twilio.com/en-us/help/abuse) or `stopspam@twilio.com`.
- **Links in the text:** report to the registrar and Google Safe Browsing, and to the shortener's abuse page if a shortener was used.
- **Regulators:** US: the FCC form above (texts use the same sub-issue), plus ReportFraud.ftc.gov for scams. Canada: Spam Reporting Centre (CASL covers SMS). Australia: forward to 0429 999 888. Singapore: the ScamShield app, plus the PDPC DNC form for telemarketing.
- If you can't send from the user's phone, give them the exact messages and numbers to forward.

## Optional: legal escalation (the user decides)

Some laws let recipients sue directly. This is the most expensive outcome for a spammer, and the user's call alone. Prepare the evidence; don't file, send demand letters or threaten anything without explicit instruction. It isn't legal advice; check current law.

- **TCPA (US calls/texts):** generally $500 per violation, up to $1,500 if willful. It covers robocalls or prerecorded messages to cell phones without prior express consent (written consent for telemarketing), and more than one telemarketing call in 12 months to a number on the Do Not Call Registry. Small claims court is common.
- **California B&P §17529.5:** $1,000 per email for falsified or untraceable header information or materially misleading subject lines, for email sent to a California address.
- **Washington CEMA (RCW 19.190):** $500 per email to Washington residents for misrepresented origin or false or misleading subject-line information.

To support this, keep the raw `.eml` files, voicemail audio, call-log screenshots with timestamps, the DNC registration date, opt-out dates and the seller's identity. The ledger below is the backbone of that record.

## Finish with a record

Keep a **ledger** that persists across incidents (e.g. `spam-nuke-ledger.csv` in the user's notes or your workspace). Columns: date, mode, sender identifiers (sending domain, brand domain, phone number, seller), layer, channel, what was filed, confirmation or ticket number, status, opt-out date, and user decision (approved / skipped / unsubscribed / flagged false positive). The decision column is what the trust ladder reads. Before filing, check it:
- **Same incident already reported:** don't refile.
- **Same sender again after earlier reports or an opt-out:** escalate. Cite the earlier report dates and the opt-out, add the state AG or a provider you skipped, and follow up on open tickets. A documented repeat offender is much stronger evidence than a first-time one.

Save confirmation emails and screenshots alongside the ledger. Re-check in about two weeks, including `check-lists.sh` on the same domains and IPs: a new listing is one of the few visible success signals.

**What to tell the user:** abuse desks rarely reply, and the FTC and FCC don't resolve individual complaints. Success looks like the mail or calls stopping, a domain appearing on a blocklist, a number getting labeled, or a ticket closed with action taken. Report what you filed, what's waiting on the user, and what you deliberately skipped and why. Don't claim the spammer was "nuked" without evidence.

## Files

| File | Purpose |
|---|---|
| `references/supply-chain.md` | **Read first.** Each layer of the email, call and text supply chain: what it is, its official channel, what a report does, what it costs the sender, and where reports don't bite. Includes the dark-forest reasoning and sources. |
| `references/report-targets.md` | Directory of abuse contacts, blocklists and regulators (email, phishing, calls, texts), including sequencer CNAME fingerprints. |
| `references/report-formats.md` | Report templates: platform abuse (ARF-style), mailbox provider, registrar, host, FTC, GDPR, opt-out, data deletion, phone complaints. |
| `scripts/parse-headers.py` | Header analysis: verified sending server (trust boundary), mailbox provider, ESP and sequencer fingerprints, Reply-To mismatch, brand vs sending domain, payloads on abused platforms, phishing flags, authentication results, company confidence score. Python 3 standard library; uses `dig` if available. |
| `scripts/recon.sh` | DNS/WHOIS supply-chain map for a domain: registrar, abuse contact, domain age, MX provider, host, SPF platforms, DKIM, blocklist status. Needs `dig` and `whois`; runs on macOS bash 3.2 and Linux. |
| `scripts/triage.py` | "A bit careful" batch view: spam-likelihood ranking with reasons, batches of 10, one-line blurbs with open links, report-by-default wording, unsure / probably-subscribed list. Uses `parse-headers.py`. |
| `scripts/check-lists.sh` | Read-only blocklist status for domains (Spamhaus DBL, SURBL, URIBL) and IPs (Spamhaus ZEN, SpamCop). Distinguishes "not listed" from "query refused". Use it before filing and again ~2 weeks later. |
