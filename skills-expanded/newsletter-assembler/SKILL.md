---
name: newsletter-assembler
description: Assembles a complete newsletter issue from provided links and notes — subject line A/B pair, TL;DR, 3–5 sections, one CTA — as clean markdown ready to paste into any ESP. Use when the user asks to "assemble the newsletter", "draft this week's issue", "turn these links into a newsletter", "newsletter from my notes", or mentions an issue send. Don't use for researching the content itself (deep-research-brief first) or sending/scheduling inside an ESP.
version: 1.0.0
author: Gen AI Hub
license: MIT
metadata:
  hermes:
    tags: [Content & Marketing, Newsletter, Email, Drafting]
    related_skills: [deep-research-brief, brand-voice-guardian, content-repurposer]
---

# Newsletter Assembler

Turns a pile of links and rough notes into a publishable issue: an A/B subject-line pair, a skimmable TL;DR, 3–5 sections that each add editorial value beyond the link, and exactly one CTA. Output is clean, portable markdown that pastes into any ESP (Beehiiv, ConvertKit, Mailchimp, Substack) without cleanup. This skill drafts; it never sends.

## When to Use

- The user has links, notes, or briefs and needs them shaped into an issue.
- A recurring newsletter needs this edition drafted to a consistent structure.
- **Not for:** researching the content itself (`deep-research-brief` first), one-off promotional emails, or sending/scheduling in an ESP (out of scope by design).

## Quick Reference

| Action | Command / Call |
|---|---|
| Subject length check | `python3 -c "print(len('SUBJECT'))"` — target ≤50 chars, hard cap 60 |
| Verify links | `curl -sIL -o /dev/null -w "%{http_code} %{url_effective}\n" "URL"` — expect 200 |
| Section count | 3–5, lead with the strongest |
| CTA count | Exactly 1 across the whole issue |
| Output format | Pure markdown: `#`/`##`, `**bold**`, `[text](url)` — no HTML |

## Procedure

1. **Precheck** — confirm you have: the raw material (links/notes), the audience, the issue's one CTA, and any recurring section names the newsletter already uses. Ask for missing pieces; never invent links or facts to fill gaps.
2. **Verify links** — run the `curl` check from Quick Reference on every URL. Expected: `200` (or a clean 3xx landing on 200). Dead or paywalled-to-error links get flagged to the user, not silently included.
3. **Select & order** — pick 3–5 items. Lead with the piece most valuable to THIS audience (not the newest). Cut the rest into a "held for next issue" note rather than cramming a sixth section.
4. **Write sections** — per section: a plain `##` header (say what it is, don't pun past clarity), 2–4 sentences of genuine editorial take — why it matters to this reader, what to do with it — then the link. The take must add something the linked headline doesn't; "Great read!" is not a section.
5. **Write TL;DR** — 3–5 bullets at the top, one per section, each a full-value takeaway (a skimmer who reads only this should still gain something — the bullets give, they don't tease).
6. **Write subject pair** — two subjects testing ONE variable (curiosity-vs-clarity, number-vs-none, benefit-vs-topic). Both ≤50 chars (python3 check, counts reported). Banned: clickbait ("You're doing X wrong"), fake urgency, "Newsletter #47" as the whole subject, emoji stacks. Add one preview-text line (~80 chars) that extends — not repeats — subject A.
7. **Place the CTA** — one CTA, positioned after the strongest section or at the close. Every other ask (follow, share, reply) is cut or demoted to a one-line P.S.
8. **Deliver** — assemble the template below as a single markdown block. Recommend a `brand-voice-guardian` pass if a voice profile exists. Hand off for the user to paste and send — never connect to an ESP.

## Output Template

```
Subject A: [≤50 chars]
Subject B: [≤50 chars]  (variable tested: [one thing])
Preview text: [~80 chars]

---

# [Issue title / edition]

**TL;DR**
- [takeaway 1]
- [takeaway 2]
- [takeaway 3]

## [Section 1 header]
[2–4 sentence editorial take.]
→ [Link text](url)

## [Section 2 header]
...

**[CTA — one line, one link]**

[Sign-off]

P.S. [optional single secondary line]
```

## Pitfalls

- **Link-dump syndrome** — sections are headline + link with no take. Recovery: for each section, answer "so what should this reader do or think differently?" in one sentence; if you can't, the item doesn't belong in the issue.
- **CTA sprawl** — a subscribe button, a share ask, a webinar, and a product plug in one issue. Recovery: return to the CTA named in step 1; keep it, cut or P.S. the rest, and tell the user what was demoted.
- **Broken or redirected links shipped** — a 404 in a sent email is unfixable. Recovery: the step 2 curl check is a hard gate; report status codes in verification and swap or flag anything that isn't clean.
- **Subject pair tests nothing** — A and B differ in five ways, so the "test" teaches nothing. Recovery: rewrite B to change exactly one variable from A and name that variable in the output.

## Verification

- [ ] Both subjects ≤50 chars (python3 counts reported); pair differs by exactly one named variable
- [ ] Every link returned 200 via curl this session (codes reported)
- [ ] 3–5 sections, each with an editorial take beyond the headline
- [ ] Exactly one CTA in the body (P.S. secondary at most)
- [ ] Output is pure markdown, no HTML tags; delivered as a draft, nothing sent
