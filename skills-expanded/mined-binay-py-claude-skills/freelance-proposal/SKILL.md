---
name: freelance-proposal
description: Write Upwork proposals, Fiverr gig descriptions and cold client emails that get replies, built only from the freelancer's real work, then score them with proposal-lint (generic openers like "Dear Hiring Manager / I am writing to", AI-isms like leverage/seamless/delve, placeholders left in, I-focused pitch, no proof, no question, ignoring the job post, wrong length, weak 200-character preview). Use when the user pastes a job post, asks for a proposal, cover letter, gig description, or client outreach message.
---

# freelance-proposal

## Hard rule: never invent experience
Only use projects, numbers, links and skills the user actually has. Ask for, or read, a portfolio file (e.g. `portfolio.md` with project, link, stack and one result each). If nothing relevant exists, say so honestly and offer a small paid test task or a quick free sample instead of faking it. Invented experience gets accounts banned and loses clients.

## Workflow
1. Read the job post. Pull out: the real problem, stack/platform, deadline, budget, and anything unusual they mention (that's what proves you read it).
2. Pick the **one** most relevant real project as proof (link + one concrete result).
3. Write it in this shape (Upwork 80–200 words, Fiverr gig intro 40–160, cold email 50–150):
   - **Line 1 (the preview, ~200 chars shown in the Upwork list):** their problem or the outcome, in their words. Never a greeting, never "I am…".
   - **Proof:** "I built the same thing for X: <link>" plus one number if real.
   - **Plan:** 2–3 short steps specific to their post.
   - **Logistics:** timeline and price, if the post invites it.
   - **One specific question**, then a next step ("Can start tomorrow").
4. Save it to a file and run the linter, with the job post for relevance:
   ```
   node scripts/proposal-lint.mjs proposal.txt --job job.txt [--platform upwork|fiverr|email]
   ```
   Fix every ✘ and ! item and re-run until it scores **≥ 85**. Show the user the final text and the score. Never send it for them.
5. Offer a second variant with a different hook (outcome-first vs problem-first) so they can choose.

## Fiverr gig descriptions
Same rules, plus: first sentence = who it's for and the result ("Local clinics: a mobile site patients can book from in one tap"); then what's included per package, delivery time, what you need from the buyer, and 1–2 real portfolio links if Fiverr allows them in that field. No keyword stuffing.

## Tone
Plain words, short sentences, contractions are fine. No "delve, leverage, seamless, robust, cutting-edge, tailored, elevate, top-notch, go above and beyond, perfect fit". No em-dash chains. Write like a busy expert texting a client, not a cover letter.
