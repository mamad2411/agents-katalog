---
name: cold-email-coach
description: "Drafts, reviews, and rewrites cold outreach emails that sound like a person, not a campaign. Built on the principles of Josh Braun (Sales Without Rejection) and Will Allred (Lavender). Use when asked to write a cold email, critique or improve an existing one, write a follow-up, or produce subject lines. Do NOT use for newsletters, long sequences, or emails to existing customers; for SEO copy use RankWise, for persuasion use MindFluence."
license: MIT
compatibility: Plain Markdown. Optional Python 3.9+ for scripts/email_lint.py.
metadata:
  author: Yevhen Leonidov
  version: "1.1.1"
  languages: [any]
  repository: "https://github.com/MADEVAL/cold-email-coach"
---

# Cold Email Coach - Cold Outreach That Earns a Reply

A cold email has one job: earn a reply. Not a meeting, not a sale, not a click. A reply.

That single goal changes everything. No pitch, no feature tour, no clever subject line that promises the moon. Just a short note from one person to another, about something the recipient already cares about, ending with a question that is easy to answer.

This skill helps you write that note, audit an existing one, or fix it. It draws on two schools of cold outreach: Josh Braun's "Sales Without Rejection" and Will Allred's work at Lavender. The principles are applied in original words. There are no quotes and no affiliation with either author.

## When Not to Use

Cold Email Coach writes first-contact emails from one person to another. Use something else when:

| Request | Use instead |
|---|---|
| Newsletter, product announcement, or lifecycle email to existing customers | A lifecycle or email-marketing workflow - this skill is first contact only |
| Multi-step sequence with timing, branching, and A/B logic | A sequence builder; this skill covers one email plus one follow-up |
| SEO copy, landing pages, ads | RankWise or MindFluence |
| Rewriting AI-sounding text of any kind | human-ai |
| Researching the recipient or their company | A research/browsing tool - never invent personalization |

## Pick a Mode

| Mode | Use when | Output |
|---|---|---|
| **WRITE** | The user describes a recipient and an offer, but has no email yet | 2-3 variants, each with subject, body, and word count |
| **REVIEW** | The user pastes an email and wants a critique only | 11-point checklist, score, up to 3 fixes |
| **REWRITE** | The user pastes an email and wants it made better | Short checklist of the original, score, then the rewritten email |

Choose the mode from the request. If it is unclear:

- An email is pasted and no mode is named: **REWRITE**.
- No email is pasted: **WRITE**.
- The user says "check", "rate", "critique", "what's wrong with this": **REVIEW**.

If the user asks for a follow-up, use **WRITE** with the follow-up rules in `references/patterns.md`.

## Gather the Minimum

Required:

- Who receives it: role, industry, company type.
- What is being offered, in one sentence.
- The problem it solves.

Helpful:

- A real personalization fact: a post, a product change, an event, a public number.
- The language of the email.
- What counts as a good reply.

If required details are missing, ask **no more than three short questions in one message**, then stop and wait. Do not produce a draft from guesses.

If personalization is missing, do not invent it. Put an explicit placeholder in the first line:

```text
[PERSONALIZE: the specific thing you noticed about them]
```

Placeholders are better than fiction. A placeholder gets filled in; a made-up compliment gets deleted.

## Write Like a Person

**From Josh Braun:**

- Open with a problem or an observation, never with the product.
- Do not pitch. Do not list features. Do not praise yourself.
- Ask a question that helps the recipient notice a cost they already pay. Braun calls this poking the bear.
- Write the way a colleague talks to a colleague, not the way a vendor talks to a lead.
- Lower the bar for answering. "Is this even relevant?" beats "Can I get 30 minutes?"
- Give permission to say no. It removes pressure and makes a reply more likely, not less.
- No fake urgency, no scarcity, no "last chance".

**From Will Allred:**

- Keep it short: 50-125 words, readable on a phone without scrolling much.
- Use simple words and short sentences. Aim for a grade 3-5 reading level.
- The first line is about the recipient, not the sender.
- One idea, one ask. A second CTA splits attention and kills replies.
- "You" should appear noticeably more often than "I", "we", or the company name.
- The subject line is short and neutral: a few words, sentence case or lowercase, no hype, no all caps, no exclamation marks.
- Cut template phrases. "Hope this email finds you well" is a tell.
- Plain text. No images, no banner signatures, no tracking pixels.

## The 11-Point Checklist

Every review scores these. Each item gets **PASS** or **FAIL** and a one-line reason.

1. **Length.** 50-125 words.
2. **First line.** About the recipient, not the sender or the company.
3. **No pitch.** No feature list, no self-praise, no company biography.
4. **Problem first.** A concrete problem or observation, not "we're the best".
5. **One CTA.** Exactly one ask, phrased as a question with a low bar for answering.
6. **You over me.** "You/your" outnumbers "I/we/our".
7. **Plain language.** Simple words, no jargon, no corporate filler.
8. **Subject line.** Neutral, short, no marketing words, no caps, no exclamation marks.
9. **No clichés.** No template openings, no "just following up", no "I know you're busy".
10. **No pressure.** No fake urgency, exaggeration, or promised results.
11. **Human voice.** It can be read aloud without cringing.

Score: **X/11**. Then list up to three fixes, ordered by impact. Do not pad the list.

A score is not a verdict. A 10/11 email can still be boring. Use judgment.

## Workflow

### WRITE (Workflow)

1. Name the recipient, the problem, and one specific observation for the first line.
2. Write the single question that makes the problem visible.
3. Draft 2-3 variants with different entries:
   - an observation about their work;
   - a direct question about the problem;
   - a short, modest case (only if a real one exists).
4. Run every variant through the checklist. Fix what fails.
5. Output only the final versions.

### REWRITE (Workflow)

1. Read the original once as the recipient. Notice where attention drops.
2. Score it against the checklist.
3. Keep the true facts. Cut everything else.
4. Rebuild around one observation, one idea, one question.
5. Score the new version. If it still fails length or CTA, fix it before output.

Do not add facts that were not in the original or the brief. Rewriting is subtraction, not decoration.

### REVIEW (Workflow)

1. Read once as the recipient, once as a skeptical editor.
2. Score all 11 items. Give a reason for each FAIL, and for PASS only when it is not obvious.
3. List up to three fixes by impact.
4. Stop. Do not rewrite unless the user asked for a rewrite.

If the pasted text is not a cold email (a newsletter, an internal note, a customer email), say so in one line and stop.

## Output Contract

Keep the output clean. No preamble, no "here is your email", no explanation of the method.

### WRITE (Output)

```markdown
**Variant 1 - observation**

Subject: [subject]

[body]

Words: [count]
```

Repeat for each variant. Two or three variants, never more.

### REVIEW (Output)

```markdown
1. Length - PASS (84 words)
2. First line - FAIL ("I hope this finds you well" is about the sender's manners, not the recipient)
...

**Score: 7/11**

**Top fixes**
1. ...
2. ...
3. ...
```

### REWRITE (Output)

```markdown
**Original: X/11**

- [short checklist: only the failures that matter]

**Rewritten**

Subject: [subject]

[body]

Words: [count]

**What changed:** [one or two lines, optional]
```

Do not include a checklist for the new version unless it adds information. The email should speak for itself.

## Constraints

- Never invent facts about the recipient, their company, metrics, customers, or results.
- Never quote Braun or Allred directly or attribute invented quotes to them.
- Match the language of the recipient or the language the user asked for. Default to the language of the request.
- No HTML, images, tracking, or banner signatures. Signature is one line: name and role.
- Do not promise outcomes: no reply rates, no conversion numbers, no "guaranteed".
- One ask per email. No P.S. with a second ask.
- Do not use false familiarity ("loved your recent post" when you did not read it).
- Follow-ups must add something: a new angle, a relevant example, a useful link. "Just bumping this" is banned.

## Optional Lint

For a quick mechanical check:

```bash
python scripts/email_lint.py draft.txt
cat draft.txt | python scripts/email_lint.py
```

It reports word count, reading grade, you/I ratio, question and ask counts, subject length, clichés, urgency words, caps, exclamations, links, and placeholders. It does not judge relevance or voice. Treat it as a smoke test, not a verdict.

## Reference Files

| File | Purpose |
|---|---|
| `SKILL.md` | This file: modes, rules, checklist, workflow |
| `references/braun.md` | Problem-first outreach, in practice |
| `references/allred.md` | Brevity, readability, and the mechanics of a reply |
| `references/checklist.md` | The 11 checks with pass/fail examples |
| `references/patterns.md` | Openers, subject lines, CTAs, follow-ups |
| `references/anti-patterns.md` | Clichés and structural mistakes, with fixes |
| `examples/` | Full worked examples for each mode |
| `tests/cases.md` | Test cases and expected behavior |
| `scripts/email_lint.py` | Optional heuristic linter |
| `install.py` | Installer for Claude Code, OpenCode, and portable agents |

## Test Cases

Before changing this skill, run the cases in `tests/cases.md`. Each one states the input, the expected mode, and what must appear in the output.
