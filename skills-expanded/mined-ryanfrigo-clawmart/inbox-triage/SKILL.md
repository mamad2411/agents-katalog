---
name: inbox-triage
description: Sort the inbox into urgent / reply / read-later / ignore and draft the replies you would actually send.
metadata: { "openclaw": { "emoji": "📥" } }
---

# Inbox Triage

Turn a full inbox into four clean buckets and a stack of ready-to-send drafts. The point isn't to read your mail for you — it's to make the "what needs me?" decision instantly and to pre-write the boring replies so you just approve and send.

## When to use (trigger phrases)

Use this skill when the user says:

- "triage my inbox" / "go through my email"
- "what emails need a reply?"
- "clean up my inbox" / "sort my mail"
- "draft replies to the ones that need me"

## How it works

1. **Pull recent mail** via the configured email tool (`himalaya envelope list`, Gmail, or IMAP). Default window: unread from the last 48h, or everything since the last triage. Cap at ~50 to stay fast; process newest first.
2. **For each message, extract the signals** that drive the decision:
   - Sender, and whether the user is in **To** (asked directly) vs **CC** (kept informed).
   - The explicit **ask** — a question, a request, an approval, a sign-off.
   - Any **deadline** ("by Friday", "EOD", "before the call").
   - **Thread state** — is this a reply the user owes, or a fresh thread?
   - **VIP match** against the configured `vipSenders` list (investors, key customers, boss, legal).
3. **Classify with a rubric** (in priority order — first match wins):
   - **🔴 Urgent** — a VIP or counterparty with an explicit ask due within ~48h, OR anything that blocks someone else, OR money / legal / security / access. Needs action today.
   - **🟡 Reply** — a direct question or request to the user, no hard deadline. Owed but not on fire.
   - **🔵 Read-later** — FYI, CC-only, newsletters worth keeping, long reads, receipts to file.
   - **⚪ Ignore** — marketing, automated notifications, social, cold pitches. Candidates for archive.
4. **Draft replies** for the Urgent and Reply buckets. Write in the user's voice: match their tone samples from config, keep it short, mirror the sender's formality. Get to the point in the first line. Where the reply requires a decision only the user can make, write the draft up to that point and flag the decision explicitly rather than inventing an answer.
5. **Never auto-send.** Every draft is a draft. The only write action allowed without per-item approval is archiving the **Ignore** bucket — and only if the user has opted in via `autoArchiveIgnore`.
6. **Return a triage report** grouped by bucket, each item one line of rationale, with the draft attached for actionable ones.

## Output

Example triage report:

```
Triaged 23 emails (last 48h). 2 urgent, 4 need a reply, 9 read-later, 8 ignore.

🔴 URGENT (2)
  • Sarah @ Acme — "Redlined MSA — need it back to sign this week"
    → Direct ask, VIP, deadline. Draft:
      "Sarah — thanks. One change on §7 (liability cap); otherwise good to
       sign. Redline attached. Can send a clean copy today if that works."
  • AWS — "Action required: root access key exposed"
    → Security. Draft asks IT to rotate; flagged for you to confirm the key.

🟡 REPLY (4)
  • Marcus — asking for the launch date. Draft: "Targeting the 14th, will
    confirm Weds after the design review."
  • Recruiter (candidate intro) — Draft: polite "yes, Thursday works."
  • ... (2 more, drafts attached)

🔵 READ-LATER (9)
  Lenny's newsletter, 3 CC-only threads, Stripe receipt, 2 long docs...

⚪ IGNORE (8) — LinkedIn digests, 4 cold pitches, 3 promos.
  [Archive all 8?  y/n]
```

## Notes

- **Requires an email tool** connected to OpenClaw (`himalaya` with an IMAP/SMTP config, Gmail, etc.). This skill supplies the judgment and the drafts; the tool does the reading and sending.
- **Configure your voice.** Drop 2-3 real sent emails as tone samples and a `vipSenders` list into `openclaw.json.example`. Good drafts depend on this — without samples, expect generic-but-safe wording.
- **Signature & footer** come from your email tool's config, not this skill.
- **Drafts only.** Sending is always a separate, explicit user action. Auto-archive is opt-in and limited to the Ignore bucket; it never deletes.
- **Don't over-trust the classifier on edge cases.** A quiet FYI from your boss can be urgent; when a message is ambiguous between Reply and Urgent, round up and let the user downgrade.
- **Privacy.** Email content is sensitive; keep processing local to the user's OpenClaw session and never forward it anywhere the user didn't ask.
