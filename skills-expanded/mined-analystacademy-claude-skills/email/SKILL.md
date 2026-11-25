---
name: email
description: Draft emails in the user's voice — direct, human, not generic — based on a voice profile and real samples they fill in below. Use this skill whenever the user asks to write, draft, reply to, or respond to an email; whenever they paste an email and ask how to handle it; and whenever they're working on outbound messages to clients, collaborators, or contacts. Use it even when they don't say "in my voice" — if they're drafting an email, this skill applies.
---

# Email Voice Skill

This skill drafts emails in YOUR voice — short, direct, human-sounding, not "professional generic." To work, it needs a real voice profile based on emails you've actually sent.

The template below is a starting point. **You'll need to fill in your own voice profile and real sample emails before this skill is useful.** Pattern-matching to your real emails is what makes it work — pattern-matching to a generic professional template is exactly what it's trying to avoid.

> **Setup tip:** Before using this skill, fill in the placeholders in this file AND fill in `references/samples.md` with 3–5 real emails you've sent. The more honest the samples (no edits to "polish" them), the better the output.

---

## Your voice profile (fill in once)

### Greetings, by relationship
Most people use 2–3 different greetings depending on who they're writing to. Fill in yours:

- **Professional / newer contact:** [e.g. `Hi [Name],`]
- **Close colleague or active back-and-forth:** [e.g. `[Name],` (no greeting word)]
- **You never use:** [e.g. `Hello,`, `Dear,`, `Greetings,`, `Hi there,`]

### Opening lines
Do you warm up before the substance, or go straight in?

- **In short transactional replies:** [e.g. "Straight to the point. No 'hope you're well.'"]
- **In sales / first-contact / post-meeting follow-ups:** [e.g. "One short warm opener like 'Thanks for reaching out!' is fine, then onto substance."]

### Sign-offs
List the 2–3 sign-offs you actually use, and the contexts:

- **Quick reply with a thank-you / ask:** [e.g. `Thanks!` then your name]
- **Pure transactional reply, no thanks needed:** [e.g. just your name]
- **Developed / sales / post-meeting:** [e.g. `Regards,` then your name]
- **You never use:** [e.g. `Best,`, `Kind regards,`, `Cheers,`, `Sincerely yours,`, `All the best,`]

### Sentence shape
- Do you write declaratively or hedge? [e.g. "Declarative. 'That works.' not 'That should hopefully work for me.'"]
- Do you use contractions? [e.g. "Yes throughout — `I'll`, `won't`, `don't`. Writing them out makes me sound stiff."]
- Do you drop the subject when natural? [e.g. "Yes — 'Don't need to worry about X.' / 'Only thing I need is Y.'"]

### Paragraph shape
- [e.g. "One thought per paragraph. Blank line between each. Most emails are 2–4 paragraphs total."]
- [e.g. "Bullet lists only when content is genuinely list-shaped — not for two or three sentences that could be sentences."]

### Confidence register
[e.g. "I write from a position of running my own show. Direct, not hedged. 'I think maybe we could possibly...' isn't me. Direct AND warm — those aren't in tension."]

### Where humor shows up (if at all)
[e.g. "Mostly in newsletters and casual messages. Rarely in transactional client emails. When in doubt, leave it out — a too-formal email is recoverable; a forced-funny one isn't."]

---

## The two registers

Most people write emails in two distinct registers depending on context. Picking the wrong one is the single biggest mistake to avoid. A draft that's correct in voice but wrong in register will still feel "off" — too cold for a sales inquiry, or too padded for a quick reply between collaborators.

### Register A: Quick / transactional

For ongoing back-and-forth, scheduling, brief logistics, replies between people who already know each other and are actively in something together.

- 2–4 short paragraphs, 1–2 sentences each
- Greeting: short / familiar
- First line goes straight to substance, no warm-up
- No "Thanks for reaching out" — they're already in the conversation
- Almost no list formatting
- Direct, confident, very few hedges

### Register B: Developed / business-development

For first contact or developing prospects, sales inquiries, proposals, post-meeting follow-ups, anything where the user is representing their business to someone newer.

- Longer paragraphs that actually explain things
- Greeting: full ("Hi [Name],")
- A short warm opener IS in voice here ("Thanks for reaching out!", "Great meeting you both!")
- Bulleted lists ARE used when content is genuinely list-shaped (login info, multiple resources, course/option comparisons)
- Closing line is open-door warm, not abrupt: ("Let me know if you have any other questions!" / "happy to answer any additional questions you have")
- Still confident and direct within the longer form — explains plainly, doesn't pad with fluff

### How to pick

Default questions to ask before drafting:
- Is this an ongoing exchange where they already know what's being discussed? → **Register A**
- Did the recipient just reach out cold, or is this a first reply in a new business thread? → **Register B**
- Is this a follow-up after a meeting or call, with proposals/materials attached? → **Register B**
- Is this a pricing / availability / scope question from a prospect? → **Register B**
- Is this a one-line scheduling change or quick logistics check? → **Register A**

When genuinely unsure, ask the user rather than guessing.

---

## Workflow when drafting

1. **Read `references/samples.md` first.** Don't skip this even if you've drafted in this voice before in the conversation — re-anchor each time.
2. **Identify the relationship and situation.** Is this a client, a collaborator they know well, someone new? Reply or fresh send? What's the actual ask or update?
3. **Pick the right register** (A or B, see above).
4. **Draft once, then cut.** First drafts are usually too long. Look at every sentence and ask whether it's pulling weight.
5. **Run the AI-tells check.** Skim `references/avoid-ai-tells.md` and look for any of those patterns in the draft. Strip them out.
6. **Present the draft to the user.** If there are real branching choices — like "soft pushback vs. firm pushback" — offer them as variants. Otherwise just give one draft to send.

---

## Things to actively avoid

These are the things that make an email read as written-by-someone-else (the "AI generic professional" voice). The full reference is in `references/avoid-ai-tells.md`; the highest-frequency offenders are listed here.

**Phrases that don't belong in most personal voices:**
- "I hope this email finds you well" / "Hope you're having a great week"
- "Just wanted to circle back" / "Following up on my last email"
- "Thank you so much for your patience"
- "I'd be more than happy to..." (most people just say "happy to..." without the "I'd be")
- "Please don't hesitate to reach out"
- "Looking forward to hearing from you"
- "I hope that helps!"
- "Of course!" / "Certainly!" / "Absolutely!" as standalone openers
- "Thank you for your time and consideration"

**Words that don't belong** in personal-voice email:
delve, leverage, navigate, ensure, robust, seamless, streamline, foster, cultivate, holistic, comprehensive, valuable insights, key takeaways, crucial, pivotal, underscore (as a verb), align with, showcase, highlight (as a verb)

**Structural tells:**
- Em dashes used in formulaic punched-up parallelisms ("It's not just X — it's Y")
- Negative parallelism ("This isn't about X, it's about Y") — almost always a tell
- Rule of three ("clear, concise, and actionable") — most people write specific singular things, not triplets
- Bulleted lists with bolded inline headers ("**Background:** Lorem ipsum...") — plain bullets for genuine list content are fine; the bold-header pattern is the tell
- "In summary," "In conclusion," or "Overall," at the end of an email — just stop writing
- Title Case Headings inside an email body
- Closing with an unneeded question in Register A — when the next move is already obvious, don't tack on "Does that work for you?"

**Tone tells:**
- Excessive enthusiasm where none is warranted ("Awesome!", "Fantastic!", "Wonderful!")
- Apologizing for things that don't need apology
- Restating what the recipient already said before responding to it ("So just to make sure I understand, you're asking about X...")
- Performative gratitude ("Thank you SO much for taking the time to...")

---

## When in doubt

If a sentence in the draft sounds like it could appear in literally any other professional's email, rewrite it or cut it. Personal voice lives in specificity and brevity. A boring true sentence beats a polished generic one every time.
