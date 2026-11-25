---
name: newsletter-draft
description: Draft a newsletter issue from an episode — subject-line options, preview text, one core idea developed, and a clear CTA.
metadata: { "openclaw": { "emoji": "✉️" } }
---

# Newsletter Draft

Writes a full newsletter issue built around **one** idea from an episode — not a link dump. Great newsletters teach a single thing and then point to the full episode for people who want more. This skill produces the subject lines, the preview text, and the body, in the sender's voice.

## When to use (trigger phrases)

Use this skill when the user says:

- "write the newsletter for this episode"
- "draft this week's email"
- "turn this episode into a newsletter issue"
- "I need subject lines and a body from this"
- "email version of the episode"

## How it works

1. **Read the transcript and show notes.** Reuse `show-notes` output if it exists — the takeaways and pull quotes are your raw material.
2. **Pick the ONE core idea.** An episode has many threads; a good issue has one. Choose the through-line most useful to the reader (usually the strongest contrarian take or the most actionable framework) and build the whole email around it. Everything else becomes a one-line "also in this episode."
3. **Write subject lines (3–5 options).** Keep them ~30–50 characters (mobile truncates hard). Alternate two levers: **curiosity** ("The 90-day death zone") and **benefit/specificity** ("A retention fix you can ship this week"). No `RE:`/`FWD:` fakery, no all-caps, no false urgency — that trains readers to ignore you and trips spam filters.
4. **Write the preview / preheader text.** One sentence that extends the subject line (this shows in the inbox next to it). Don't repeat the subject; add to it.
5. **Structure the body:**
   - **Hook** (1–3 sentences): open on the idea's tension, not "In this week's episode…".
   - **The idea, developed** (2–4 short sections): explain it, ground it in the guest's story or example, and give the reader the takeaway they can use. Short paragraphs, plenty of whitespace — most people read on a phone.
   - **CTA to the episode:** one clear ask with a timestamp deep-link ("Dr. Chen breaks down the three fixes at 21:05 → [link]"). One primary CTA, not five.
   - **Sign-off + optional PS.** The PS is the second-most-read line in any email — use it for a soft secondary CTA (reply, reshare, the one link).
6. **Match the sender's voice.** Ask for a past issue or a one-line description. Newsletters live and die on a consistent, human voice.
7. **Save as a draft file.** Write it where the user keeps drafts. This skill does **not** send.

## Output

```markdown
Subject line options:
1. The 90-day death zone
2. Your churn problem is (probably) a lie
3. A retention fix you can ship this week

Preview text: Most apps don't die from a bad product. They die in session one.

---

Most founders think they have a churn problem.

They almost never do. They have a first-session problem — and the two need
completely different fixes.

I talked to Dr. Chen this week about the "90-day death zone," the window where
most consumer apps quietly lose the users they spent so much to acquire. Her
reframe stuck with me:

> "You don't have a churn problem, you have an empty-state problem. Nobody
> leaves a product that's already full of their stuff."

The fix isn't more features. It's making session one leave something behind:

- **Shorten time-to-value** — get them to the "oh, nice" moment faster.
- **Kill the empty state** — seed the account so it never looks abandoned.
- **Earn the first notification** — one that's actually worth the tap.

She walks through all three (with the D30 numbers) starting at 21:05.

→ Listen to the full episode: [link]

— Ryan

PS. If you know a founder staring at a scary retention chart, forward this.
```

## Notes

- **This skill drafts; it does not send.** Sending requires an email tool you configure — Resend, your ESP's API, Beehiiv, ConvertKit, Substack. OpenClaw won't push to your list on its own, and you should always eyeball an issue before it goes out.
- **One idea per issue.** The urge to include everything is the most common way newsletters get boring. Cut ruthlessly; the episode link carries the rest.
- **Subject-line honesty is deliverability.** Clickbait and fake-urgency subjects raise unsubscribes and spam reports, which quietly wreck your inbox placement for everyone on the list.
- If the user runs A/B subject tests, give them two genuinely different angles (curiosity vs. benefit), not two rewordings of the same line.
- Keep links to one primary CTA; extra links dilute clicks and can hurt deliverability.
