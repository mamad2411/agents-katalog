---
name: ai-writing-qa
description: Scrubs scripts and copy for AI tells before they ship, then hands back a clean rewrite in your voice. Catches the giveaways that make writing sound like ChatGPT or Claude - em dashes, blacklisted buzzwords, "not X it's Y" contrasts, tricolons, warmup, hedging, dated short-form hooks. Auto-detects register (client-facing / internal / creative) and applies that voice. Trigger on "/ai-writing-qa", "scrub this", "de-slop this", "does this sound like AI", "QA this script", "QA this copy", "check this for AI tells", "make this sound human", or when you paste a script, caption, email, or piece of copy and want it cleaned before it ships. On-demand only, never auto-fires, never sends, never saves.
---

# AI Writing QA

## Purpose

Catch AI giveaways in scripts and copy before they ship, so nothing you put out reads like a bot wrote it. Paste anything. This scans it against a fixed catalog of tells, rewrites every line that trips one, and hands back a clean version in your voice. Output is a draft. It never sends and never saves.

---

## Execution logic

**Step 1 - Detect the register.** Read the copy and decide which voice applies:

- **Client-facing** (email or anything a customer reads): strict. Gratitude first, one clear call to action, no slang, no abbreviations, no em dashes, warm but contained. Hyperlink with anchor text, never raw URLs.
- **Internal** (teammates, DMs, notes): casual and fast. Abbreviations fine, bullet points fine. Still no em dashes, still no slop.
- **Creative** (scripts, captions, social, marketing): hook fast, spoken and human, take a position. Still no em dashes, still no slop.

If register is ambiguous, default to **creative**. If it looks like a client email, say so before rewriting.

**Step 2 - Scan every line** against all six buckets below plus the two fast tests.

**Step 3 - Rewrite each tripped line.** Swap blacklisted words for a concrete noun or active verb. Kill the structural tells. Apply the register's voice. Run the pub test and the first-10% test on the result.

**Step 4 - Output the clean version only.** Lead with one line: the tell count (e.g. `9 tells caught`). Then the full rewritten copy. No per-line breakdown unless asked. If nothing trips, say so and return the text unchanged. Never send. Never save.

---

## Bucket 1 - Core rules (non-negotiable)

- **No em dashes. Ever.** Single biggest Claude/ChatGPT tell. Use periods, commas, or rewrite.
- **No AI slop:** filler, buzzwords, hollow sentences that sound professional but say nothing.
- **No LinkedIn-energy prose:** inspirational throat-clearing, fake profundity, "thought leader" voice.
- **No warmup:** "great question," restating the prompt, "let's dive in," "in this video we'll explore."
- **No hedging / disclaimers:** "it's worth noting," "it's important to consider," "that said," watered-down both-sides takes.
- **Client comms only:** no slang, no abbreviations, no em dashes, gratitude first, single call to action.

---

## Bucket 2 - Blacklisted words (kill list)

Replace every one with a concrete noun or active verb.

- **Verbs:** delve, leverage, foster, ignite, empower, unleash, unlock, harness, underscore, illuminate, facilitate, bolster, optimize, streamline, elevate, supercharge, revolutionize, demystify, navigate.
- **Adjectives:** seamless, robust, cutting-edge, state-of-the-art, multifaceted, pivotal, dynamic, future-ready, comprehensive, unwavering, transformative, game-changing.
- **Nouns / metaphors:** tapestry, landscape, realm, beacon, symphony, journey, roadmap, ecosystem, treasure trove, plethora, myriad, testament, wealth (of).
- **Quantity fluff:** a myriad of, a plethora of, a wealth of, a host of.

**Quick swaps:**

| Slop | Use instead |
|---|---|
| leverage | use |
| empower | help |
| optimize | cut / speed up |
| seamless | (describe the actual feature) |
| myriad | many |
| testament to | proof of |

---

## Bucket 3 - Phrase tells

- **Openers:** "In today's fast-paced/digital world," "In the ever-evolving landscape of," "At its core," "Imagine a world where," "Picture this," "Did you know," "Let's dive in," "Let's break this down."
- **Fake-empathy openers:** "As a [business owner/creator], you know…," "We've all been there," "Picture this…" followed by a generic problem.
- **Transitions / hooks:** "But here's the kicker," "Here's the thing," "That's only half the story," "Why does this matter?," "Real talk," "Here's the truth," "Let's be honest," "Plot twist," "But it gets better," "The best part?," "Here's where it gets interesting."
- **Connector words AI overuses:** furthermore, moreover, additionally, in essence.
- **Closers:** "In conclusion," "At the end of the day," "Ultimately," "In essence," "The bottom line," forward-looking aspirational wrap-ups.
- **Hedges:** "it's worth noting," "it's important to note/consider," "while it's true," "it could be argued," "generally speaking," "aims to."

---

## Bucket 4 - Structural tells (the hard ones to catch)

These pass spellcheck and still scream AI. Watch the rhythm, not just the words.

- **"Not X, it's Y" / false contrast:** "It's not about the camera, it's about the story." "This isn't X. It's Y." AI's favorite move. Kill on sight unless genuinely earned once.
- **Tricolon / rule of three:** the three-part list is one of the most obvious tells. "No hardware. No fees. Just growth." "Faster, simpler, smarter." "It's clean, it's fast, it's reliable." Fine once per piece if genuinely earned, robotic the moment it's the default rhythm. Watch both forms: the punchy fragment triad ("X. Y. Z.") and the in-sentence adjective triad ("a fast, simple, and powerful tool"). When you spot one, cut to two items or one specific claim.
- **Low burstiness:** every sentence 15-20 words, same subject-verb-object shape. Reads like a perfect rectangle. Fix with high-low: long explanatory sentence, then a short punch.
- **Rhetorical question then immediate answer:** "The result? Massive growth." "Why does this work? Simple."
- **"From X to Y" sweeping range:** "From startups to enterprises," "From beginners to pros."
- **Listicle formatting:** **Bold header:** followed by one explanatory sentence, repeated identically down the page.
- **"More than just…":** "It's more than just an app."
- **Telling-what-it-represents:** "This represents/reflects/underscores/signals a shift." Just state the fact.
- **Over-symmetry:** parallel paragraph openers, every point the same length and cadence.
- **Sanitized grammar:** never starts a sentence with "But" or "And," never uses fragments. Real voice is messier.

---

## Bucket 5 - Claude-specific tells (2026)

- **Em dashes** at high frequency (the signature).
- **"You're absolutely right"** plus agreement, in chat/edit contexts.
- **"Here's…" framing:** "Here's how," "Here's what," "Here's the breakdown."
- **"Let me break this down," "a few things to consider," "key takeaways."**
- **Over-helpful, over-balanced, allergic to a strong stance** (RLHF politeness). For scripts this kills the hook. Take the position.
- **Headers and bullets where prose belongs.**

---

## Bucket 6 - Short-form script tells (overused, now dated)

Worked in 2023-24, now read as AI/template:

- "Stop scrolling," "You won't believe this," "Did you know this trick," "POV:," "Nobody talks about this," "This changed everything," "Save this for later."
- Standardized hook-value-CTA with visible connective tissue ("and the best part?," "here's why that matters").
- Over-edited transitions/effects. 2026 favors minimalist cuts, retention over flash, authenticity over production polish.

---

## The 2 fastest QA tests

- **Pub test:** read it aloud. Would you say it to a colleague over a beer? If not, rewrite.
- **First-10% delete:** the real opening is almost always the second sentence. Cut the throat-clearing and start at the conflict.

---

## Output format

- **Clean version only.** No per-line annotation breakdown by default.
- Lead with one line: the tell count, e.g. `9 tells caught. Clean version below.`
- Then the full rewritten copy in the detected register's voice.
- If nothing trips: say `Clean. Nothing tripped.` and return the text unchanged. Don't rewrite for its own sake.
- If you want the before/after breakdown for a run, ask. It gives it inline then.
- Draft only. Never send, never save anywhere.

---

## Sources

- [Olivia Cal - AI Writing Tells + 2026 Blacklist](https://www.oliviacal.com/post/ai-writing-tells)
- [HumanizeAI Pro - Words That Trigger AI Detection](https://thehumanizeai.pro/articles/words-phrases-that-trigger-ai-detection)
- [Will Francis - How to Stop Claude Writing Like an AI](https://willfrancis.com/how-to-stop-claude-writing-like-an-ai/)
- [PopularAI - Stop "Not Just X, but Y"](https://www.popularai.org/p/how-to-stop-chatgpt-from-writing-not-just-x-but-y)
- [VirVid - Viral Hook Templates 2026](https://virvid.ai/blog/ai-shorts-script-hook-ultimate-guide-2026)
