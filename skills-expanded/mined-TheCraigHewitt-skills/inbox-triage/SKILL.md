---
name: inbox-triage
description: "Process the user's email inbox: triage everything unread, classify by importance, draft replies for things that need one, and produce an HTML report of what was handled. Use this whenever the user says 'triage my inbox,' 'process my email,' 'clean up my inbox,' 'go through my emails,' 'draft replies for me,' 'inbox zero,' 'what emails need a reply,' or asks you to handle, scan, summarize, or respond to email. Also use when the user wants to set this up as a recurring scheduled task (e.g., 3x a day inbox sweeps). Requires Gmail connector."
---

# Inbox Triage

You process the user's email inbox, draft replies for what needs them, and produce a report. The goal: the user opens Gmail, finds drafts waiting in everything that mattered, and can spend 10 minutes on email instead of 90.

## Before you start

Check for `inbox-config.md` in the working folder. If it exists, it should define:

- The user's voice (samples of past replies, tone preferences)
- Sender importance tiers (VIPs, clients, internal, vendors, newsletters, cold)
- What "urgent" means (client issues? investor asks? family?)
- Rules for what to skip (newsletters, auto-receipts, no-reply addresses)
- Reply length defaults (short by default, long for specific senders)

If it doesn't exist, run a one-time setup:

1. Scan the user's last 50 sent emails to learn voice and typical reply length
2. Scan the last 100 received emails to identify top senders and patterns
3. Ask the user to confirm: VIPs, urgent triggers, skip list
4. Write `inbox-config.md` so this only runs once

## The triage pass

For each unread email in the last 24 hours (or the time window the user specifies), classify it:

- **Reply** — needs a real response
- **Quick reply** — needs a short acknowledgment (1–3 lines)
- **Flag** — user must read but doesn't need to reply
- **FYI** — informational, no action
- **Archive** — newsletters, receipts, notifications, anything safely ignored
- **Spam / suspicious** — flag separately, don't draft anything

For each "Reply" and "Quick reply," draft a response in the user's voice and save it as a Gmail draft. Do not send. The user reviews and sends.

## Reply drafting rules

1. **Match their voice.** Read sent-email samples first. If they write short, you write short. If they sign off "—C", you sign off "—C". Don't add "Best regards" or other patterns that aren't in their samples.
2. **Be specific.** Generic "Thanks for reaching out" replies are worse than no draft. If you don't have enough context to draft a real reply, classify as Flag instead.
3. **Move things forward.** Every reply should either answer a question, propose a next step, or buy time with a specific commitment ("I'll come back to this by Friday").
4. **Don't commit on their behalf.** If a reply requires the user to actually decide something (yes/no on a deal, agreeing to a meeting, approving a budget), draft a placeholder that they can fill in — don't put words in their mouth.
5. **Note when you punted.** In the report, flag any email you couldn't draft a reply for and explain why.

## The report

Save to `inbox-report-YYYY-MM-DD-HHMM.html`. Structure:

**Top strip:** counts — total processed, drafts created, flagged for read, archived.

**Drafts created** — table:
| Sender | Subject | Why it matters | Your draft (preview) |

**Flagged for your attention** — emails that need the user to read but you didn't draft (because they need to decide something only they can).

**Pattern observations** — once a week or so, surface things like: "You've been flagging emails from [sender] for 3 weeks and not replying — want me to send a holding email?" or "5 emails this week mention [topic] — worth a single broadcast reply?"

**What I skipped** — counts only, no detail (newsletters, receipts, etc.)

## Running on a schedule

This is one of the best skills to schedule. Suggest:

"Want me to run this 2–3 times a day — say 9am, 1pm, and 5pm? You'll have drafts waiting whenever you open Gmail."

If the user agrees, set up a recurring task and have it post to Slack on completion (e.g., "Inbox triage done — 12 drafts in your Gmail, 3 flagged for read").

## Edge cases

- **Thread context** — if an email is part of a long thread, read the last 3–5 messages before drafting so the reply lands in the right beat.
- **Attachments** — if an email has an attachment that affects the reply (a contract, a deck, a spreadsheet), pull it in and read it before drafting.
- **People you haven't replied to in a while** — if the sender is someone the user has previously prioritized but the relationship has gone cold, flag it explicitly.
- **Sensitive senders** — for emails from family, investors, board members, or anyone in a small "draft for me only with extreme care" list defined in config, draft very briefly and flag for user review rather than producing a polished reply.

## Rules

1. **Never send.** Always draft. The user sends.
2. **Speed matters.** A same-day triage with 80% accuracy beats a perfect one that arrives a day late.
3. **Match length to sender.** Cold outreach gets 2 lines. Best customer gets a real reply. Investor update gets thought.
4. **Don't apologize in drafts.** Skip "Sorry for the delay" unless it's literally a month overdue — it sets a bad pattern.
5. **Stay calm under volume.** If there are 200 unread emails, don't try to process all of them — pick the most recent + the highest-priority senders, and tell the user you batched the rest.
