---
name: sr-policy-check
description: The last check before anything goes live. Walks a post, caption or script through disclosure and policy questions in plain order: sponsorship, gifts and affiliate links (US FTC, India's ASCI, EU rules), platform paid-partnership and realistic-AI labels, reposted or unoriginal material, music and footage rights, health, money and result claims, testimonials, and use of other people's faces or voices. Use before posting anything sponsored, AI-assisted, reposted or making a claim. A checklist with sourced facts, not legal advice.
license: MIT
compatibility: Any agent that loads Agent Skills. The facts lookup needs Python 3.9+; the checklist works without it.
metadata:
  author: Raj Bharti
  version: "0.1.2"
  family: showrunner
---

# Policy check

This is the last gate before a human presses post. It catches the problems that get a post removed, a channel limited or a creator in trouble. It is a checklist backed by sourced facts. It is **not legal advice**. For a paid deal, read the brand's contract, and for anything large ask a lawyer.

## Ask first

- Is any of this paid, gifted, free product, affiliate, or from a company you have a relationship with?
- Where does the audience live, and where do you live? (US, India and EU rules differ.)
- Is there realistic AI-generated or AI-altered video, audio, voices or faces in it?
- Whose footage, music, images, faces and words are in it?
- Does it claim anything about health, money, results or guarantees?

## Run the list

Work through `references/checklist.md` top to bottom. For each row, answer PASS, FIX or ASK (ask the person). Look up the facts with `facts_search topic=policy` and say each fact's status and age.

The rows that matter most:

1. **Material connection.** Payment, free product, a commission or a relationship needs a clear disclosure. The US FTC requires it (`general.ftc_disclosure`, official). India's ASCI requires a visible label on paid or incentivised promotion (`general.asci_disclosure`). In the EU, hiding the commercial nature of content is a prohibited unfair commercial practice (`general.eu_hidden_ads`).
2. **Use the platform label as well.** Instagram has a paid partnership label for branded content (`instagram.paid_partnership`). Add your own words too, placed where they cannot be missed: in the first line or spoken at the start, not buried in a pile of hashtags.
3. **Realistic AI content.** YouTube asks creators to disclose realistic altered or synthetic content with the AI use setting when uploading in Studio (`youtube.ai_disclosure`). TikTok requires realistic AI-generated content to be labelled (`tiktok.ai_label`). For other platforms, ask the person to check the in-app setting, because the database holds no fact for them.
4. **Originality.** YouTube, Instagram and Facebook each announced changes favouring original content over reposts in 2026 (`general.originality_trend`). A repost with nothing added is a risk. Add commentary, analysis or your own footage.
5. **Music, footage, images.** The database has no verified facts on music licensing. Use the platform's own licensed library or media you own or have a licence for, and say so if unsure.
6. **Claims.** Do not promise results ("guaranteed", "you will make"). Show what happened to you, with the numbers, and say it was one case. Be careful with health and money advice.
7. **Testimonials and reviews.** Real ones only, with permission. Never write or invent a review.
8. **People.** Permission before featuring an identifiable person, and extra care with children. Do not use an AI voice or face that imitates a real person.

## Output

A short table:

```
Item | Result | Fix
Sponsorship disclosure | FIX | Add the paid partnership label and say it in the first line.
```

End with one line: ready to post, or fix these first.

## Gate

`human`. The person decides and posts. If anything is marked ASK or unsure, stop and ask.

## Do not

- Hide a sponsorship, or say "not sponsored" when it is.
- Present an AI-made realistic clip as real footage.
- Invent a result, a review or a testimonial.
- Tell the person it is legal advice or that a post is safe. Say what the checklist found and what you could not check.
