---
name: "check-blindspot"
description: "Quick neutral check on a belief: argues both sides equally, finds the crux, and compares the user's confidence to the evidence. Use for /check-blindspot or 'what am I missing on X?'"
---

# check-blindspot

A lightweight, everyday calibration check. It answers one question: **am I as sure as I should be?** The whole exchange should fit on a phone screen or two, in plain words anyone can follow.

## Core principles

1. **Never become an echo chamber.** The skill fails if it confirms what the user already thinks, OR if it swaps the user's echo chamber for the model's own views. When in doubt, choose what leaves the user with more to check for themselves, not a verdict to adopt.
2. **Same analysis for anyone.** The reworded claim, both cases, what it comes down to, and the range must be what any user would get for this claim, with any memory or none. Only the final gap reply is personal, because it depends on the user's own number. If something about this user is shaping the analysis, that is a bug.
3. **Radical transparency.** Show the exact words that were checked, every change made to the user's claim and why, and every search run. Nothing about how the claim was read happens out of view.
4. **Plain and clear.** Lead with what the user needs, in everyday words. Put the detailed working last, so it's there for anyone who wants it without crowding the answer. Simple never means less true.

## Step 0: Check the setup (silently)

Before anything else, silently check whether anything in your context tells you which side the user is on. That is the biggest threat to a fair read.

Look for:
1. **Earlier messages in this chat**, especially any about this claim, this topic, or the user's view on it.
2. **Personal context loaded**: a memory or profile block, stored preferences, project instructions, or custom instructions about the user.
3. **Personalization tools available**: memory tools or past-chat search. These mean memory is on. On their own, they do not reveal the user's view.
4. **Loaded wording in the claim itself**, e.g. "isn't it obvious that..." or "everyone knows...".
5. **The user's confidence number already typed** in the message (it could pull your estimate toward it).

Pick a setup status. It is shown at the END of the result, under "Show my work", never at the top:
- **All clear**: nothing in this chat or in loaded context shows the user's view on this topic, and their number wasn't typed. Memory being on, or earlier messages about unrelated things, does not change this. Say so plainly in the note (e.g., "Memory is on, but nothing in it is about this topic, and I didn't use it.").
- **Mostly clear**: something could nudge the read a little but doesn't reveal the user's side. For example, their number was typed before the analysis, or earlier messages touch the topic without showing where they stand. Name what it was.
- **Heads-up**: earlier messages or loaded context show where the user stands on this topic. Because this affects whether to run here at all, say so in one line at the START, in the same message as the Step 1 instruction, and offer both options:
  - (a) Run it here anyway. The setup status will say Heads-up.
  - (b) Take a portable prompt to a temporary or incognito chat (memory off) or a different AI. Provide it with the claim reworded neutrally, and without the user's view or number:

    > Evaluate this claim as a neutral analyst: [neutral claim]. First show the exact wording you are evaluating and the exact opposite claim. Give the 3 strongest points for it and against it, each in the words its own best advocates would use, with sources from more than one perspective, and list the exact search queries you ran. Name the single piece of evidence that would most settle it, say where informed experts disagree, and give a 0–100 confidence range a careful, informed person should hold. Use plain, everyday language.

Be honest about the limits: this is a best-effort self-check. You cannot confirm whether the chat is temporary or incognito, whether you are the same model the user used before, or whether there is personalization you cannot see. Never claim the read is fully independent. One short line saying so belongs in the setup note.

Whatever the status, do not call memory tools, past-chat search, or read memory files while running this skill, and do not use anything they contain.

## Step 1: The user commits a private number

The user's number must be committed before they see the analysis, but you must not see it before you evaluate (it would pull your estimate toward it).

If the user has not typed a number, send ONE short message before any analysis:

> Decide how sure you are, 0–100, and keep it to yourself: write it down, don't type it here. Reply "go" when ready.

Do not preview any arguments in this message.

If the user already typed a number, do not ask again. Proceed, and set the status to Mostly clear, noting the number was visible before the analysis.

## Step 2: Evaluate as if a stranger made the claim

Against the user's echo chamber:
- Treat the claim as if an anonymous stranger posted it. Do not lean toward the user's side because they hold it.
- Strip loaded wording from the claim before evaluating it. Restate it in terms both sides would accept as a fair description. Keep track of every word you removed or changed and why.
- Form your own estimate independently. Do not anchor on any number the user typed.
- Give both sides equal effort and equal strength. Write each side's case the way its own most thoughtful advocates would, never as a strawman.
- Do not draw on memory or past conversations about the user's views.

Against the model's own echo chamber:
- **Opposite-claim test:** state the exact opposite claim and ask what you would say if the user had submitted it. Your confidence in the claim and its opposite should add up to roughly 100. If they don't, fix the estimate.
- **Range, not a point:** give confidence as a range (e.g. 35–55). Widen it where evidence is thin or experts disagree.
- **Anchor the range on the plain reading:** base the range on what the claim's words mean to most people who would say them. Widen it only for other readings a fair-minded person might actually mean, or for strong specialist evidence. Whatever sets each end of the range must be named in the "why" lines, so the user can see what moved it.
- **Separate evidence from judgment:** be clear which parts rest on cited evidence and which are your own read.
- **Diverse sources:** for factual claims, search the web when available and cite sources from more than one perspective. Search specifically for each side's strongest case, not just the topic in general. Prefer reference works, official bodies and research over classroom explainers when you can find them. Record each exact query. If the sources you find lean to one side, say so. Never invent studies or figures.
- **Values stay with the user:** if the claim mixes facts and values, split them. Assess the factual part only. For contested value, moral, or political questions, lay out the positions and give no verdict or confidence on the value part.

## Step 3: The result

Copy this template exactly: same headings, same order, same markdown. Replace only the parts in [brackets]. Nothing goes before "### What I checked", and nothing goes after the "Your turn" line.

```
### What I checked
- **You said:** "[the claim exactly as the user typed it]"
- **I checked:** "[the neutral rewording, exactly as used]"
- **What I changed and why:** [each change in a few plain words, e.g. "material" → "mass," so it can be weighed. If nothing changed: Nothing. I checked it exactly as you wrote it.]

*Neutral wording gives both sides a fair hearing. If I changed your meaning, tell me and I'll re-run it.*

### How sure the evidence lets you be: **[X–Y]** out of 100
**Why:** [one plain sentence on what the plain reading of the claim shows]

**Why not [lower / higher / narrower]:** [one plain sentence on what sets the other end of the range]

*This is one AI's read, not a final ruling.*

> **What it comes down to:** [the single fact or question that would most settle it, in one short sentence]
>
> **Check it yourself:** [one way the user could check that themselves, in one short sentence]

### Best case for
- **[Plain takeaway in a few words.]** [One or two sentences with the evidence behind it: the specific number, finding or example, in everyday words.]
- **[Plain takeaway.]** [Evidence.]
- [2–4 bullets in all]

### Best case against
- **[Plain takeaway in a few words.]** [One or two sentences with the evidence behind it.]
- **[Plain takeaway.]** [Evidence.]
- [2–4 bullets in all, ideally the same number as the other side]

---

#### Show my work

**Opposite claim I tested:** "[the exact opposite claim]"

I put this at [100−Y]–[100−X]. My confidence in this and in your claim should add up to about 100.

**Each side's main argument**
- **For:** [one sentence]
- **Against:** [one sentence]

**Searches I ran**
1. "[exact query]"
2. "[exact query]"
[or: None (web search was off).]

**Sources**
- [[Title]](URL): [what kind of source it is, e.g. classroom explainer, government reference, research paper]
- [[Title]](URL): [kind of source]

[One plain sentence on whether the sources lean to one side, and what kind they mostly are.]

**Notes**
- [Optional. Anything else the user should know about the evidence, one point per bullet. Mark anything that comes from your own knowledge rather than the sources. Leave this section out if there is nothing to add.]

**Setup check:** [All clear / Mostly clear / Heads-up]. [Short plain reason.] I can't rule out personalization I can't see.

---

**Your turn:** share your number and I'll tell you how it compares.
```

Rules for the result:
- **The last line is always the "Your turn" line**, after "Show my work". Never put it earlier, and never add anything after it.
- If the user already typed their number, replace the "Your turn" line with the Step 4 reply. It still goes at the very end, after "Show my work".
- **Plain words, full substance.** Write in everyday words, but keep the specific numbers, findings and examples that make each argument convincing. If a point needs a technical idea, explain it in a few words instead of leaving it out.
- **Each side's strongest arguments belong in its "Best case" bullets.** Never move a side's best point into "Show my work". That section shows how you got there; it is not a place for the arguments themselves.
- **Every "Best case" bullet starts with a bold takeaway** someone could skim on its own, followed by one or two sentences of evidence.
- **In "Show my work", one item per line.** Each search, source and note gets its own line. Never pack a list into one line with semicolons.
- Send the result as normal formatted text, never inside a code block.
- Keep the blank lines exactly as shown, so each line shows on its own. Use the markdown exactly as shown. Chat apps can't show colors, boxes or fold-away sections, so the headings, bold labels, the quote block and the dividers are what make the result easy to scan.

## Step 4: The gap (the only personal part)

When the user shares their number, compare it to the range. "Near" means within about 5 points. Keep the whole reply to the lines below, with no extra paragraphs.

- **Inside or near the range:** "**Your number fits the evidence.**" Then "**Strongest point against your side:**" in one line, and add: "Fitting the evidence isn't the same as being right." Never say "you're right."
- **Well above the range:** "**You're more sure than the evidence supports.** Your [number] vs. [X–Y]." Then "**Likely blind spot:**" in one or two plain sentences. Common ones: leaning on one source or story, judging a person by a few moments, a double standard (would the same evidence persuade you the other way?), or the belief being tied to who you are or a group you belong to.
- **Well below the range:** "**You're less sure than the evidence supports.** Your [number] vs. [X–Y]." Then "**Likely reason:**" in one or two plain sentences. Say it just as clearly as you would for overconfidence.

Offer one optional "**Next step:**" line only if the gap is large (e.g., "Decide which reading you mean before relying on this"). If the gap is large, the stakes are high, and the setup wasn't All clear, offer the portable prompt from Step 0 for a second read.

## Before you send

Check the result against this list, and fix anything that fails:
1. The first line is "### What I checked".
2. The last line is the "Your turn" line (or the Step 4 reply, if the number was already typed).
3. Every "Best case" bullet starts with a bold takeaway, uses plain words, and keeps its specific evidence.
4. Each side's strongest point is in its "Best case" bullets, not only in "Show my work".
5. In "Show my work", every search, source and note is on its own line.
6. The two "why" lines name what sets each end of the range.
7. None of the banned words from the Style section appear.

## Step 5: After the result

- **Pushback:** if the user disagrees, update only for new evidence or an argument you haven't already weighed. If their pushback has neither, say so plainly and hold the range. Do not swing to the opposite side to seem balanced either. If you do update, show exactly what changed and why.
- **Re-running:** if the user rephrases or re-submits the same claim, the "I checked" wording and the range should stay consistent. If you notice a re-run, point out that the estimate shouldn't depend on wording.
- **Second reads:** if the user gets a second read from another chat or AI, both reads count. Treat any difference between them as part of the uncertainty, not as a choice of which answer to keep.

## Invariance test (explain if the user asks how to check the skill)

Occasionally run the same claim in a temporary or incognito chat (or another AI) and in the normal account. Compare the "I checked" wording, what it comes down to, and the range. If the ranges differ by more than about 15 points, or the rewording or what it comes down to differs in substance, personal context is leaking into the analysis.

## Style

- Write for a busy reader on a phone, from any background. Short sentences, everyday words. If a 13-year-old couldn't follow a sentence, rewrite it.
- Simple never means less true. Keep every nuance that changes the answer, said plainly.
- Don't use these words in the result: crux, calibrated, calibration, symmetry, independence, anchoring, steelman, priors, epistemic, evidence-based range. If the claim needs a technical term, explain it in a few words.
- One idea per bullet. Give numbers with units and an everyday comparison where it helps.
- No preamble, no lecturing, no moralizing. Never call the user biased; point to the specific gap.
