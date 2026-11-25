---
name: deepsearch-truth-deck
description: Condenses a whole market dossier into a short deck of 20 to 30 plain truths, each with one simple sentence, its proof, what it changes for the offer and a visible proof label (measured, estimated, declared, unknown), plus a two-page overview. Use for "résume en 30 points", "les choses essentielles à comprendre sur ma niche", "slides de synthèse", "key takeaways", "executive summary of the research", or "what must I understand about this market". Part of In-depth Deep Search.
---

# Truth deck

Makes a founder understand a market in twenty minutes, without pretending that everything is proven. Every statement shows what it rests on.

Read `../_shared/evidence-protocol.md`, then the whole dossier. Use only what the files support, and keep their source links.

## Rules for a truth

Each truth is one page, and holds:

| Part | Rule |
|---|---|
| **Statement** | One sentence a smart teenager understands. A claim, never a topic |
| **Proof label** | MEASURED, ESTIMATED, DECLARED or UNKNOWN, always visible |
| **Number or quote** | One or two, large. A bar or two if a comparison says it better |
| **The proof** | 2 or 3 sentences |
| **For the offer** | One or two sentences: what this changes for the offer, the marketing or the channel. If a scope gate holds the offer back, call it **For the decision**, and stay on what the fact changes for the decision |
| **Source** | One line, at the bottom |
| **Speaker notes** | Caveats, exact citations, sample sizes, the file to open |

**Be strict with labels.** Never raise a label to look stronger. If the user asks for "proven" facts, and only half the truths are measured, show that split on the first page. It is the most honest and useful number in the deck.

## Choosing the truths

Select what would change a decision, and drop what is merely interesting. Aim for 20 to 30, and cover these:

| Section | What belongs here |
|---|---|
| **Who they are** | How many, how many can pay, the split between segments |
| **Their money** | Income, revenue trend, deals per year, value per deal, when cash arrives |
| **What they know** | Awareness stage, what they search for, who they buy from today |
| **What they feel** | The pains in their words, what disappointed them, what embarrasses them, their identity |
| **The competition** | Who they really compete with, price range, promises against contracts, what nobody combines |
| **The rules** | What is allowed, and the risky structures |
| **Blind spots** | What is unmeasured, who is missing, and the closing truth: has anyone said they would buy? |

Include the surprising ones and the unwelcome ones. A truth that kills a favourite idea stays in.

**End on the test.** The last truth names what is still unknown and the cheapest way to settle it.

## Word rules

- Use the target's vocabulary when writing about them, and keep marketing jargon out.
- Never present a seller's number as a fact. Say who published it.
- Round numbers only when the source allows it, and keep the proof label.
- Check quotes: `python3 "$IDS/scripts/bank.py" check-report 09-truths.md --bank notes/bank.json --corpus notes`.

## Output

**`09-truths.md`**, with this block per truth:

```markdown
## 12 / 30. Almost nobody searches for this solution.  [ESTIMATED]

**Number:** 3 solution queries among 40 suggestions, and no usable Trends curve for the category's name.

**The proof:** <2 or 3 sentences.>

**For the offer:** <1 or 2 sentences.>

*Source: <one line>.*

> Notes: <caveats, sample, file to open.>
```

Open the file with the count: "15 measured, 6 estimated, 6 declared, 3 unknown. Nobody in the target was interviewed."

**A deck.** Build it with the best tool available in the session: a slides artifact, a `.pptx` skill, or HTML. Use one slide per truth. Make the first slide double as the cover if the user capped the page count. Show the label as a pill on every page, using the same shape for the same level, so it can be read without color:

| Level | Style |
|---|---|
| MEASURED | Solid |
| ESTIMATED | Outline |
| DECLARED | Dashed outline |
| UNKNOWN | Accent color, filled |

Check the rendering page by page, or tell the user you did not.

**`00-overview.md`,** at most two pages, conclusion first: who the market is, how many can pay, how they earn and when, demand trend, awareness stage, competition, what they say in their own words, the rules, the verdict with its conditions.

**The first thing to read.** In your final message, point to the 4 or 5 truths that matter most, and say why.

## Done when

- [ ] Each truth has all its parts and a label
- [ ] The proof count sits on the first page
- [ ] Unwelcome truths were kept
- [ ] The deck ends on the unknown and on the test
- [ ] All quotes pass the check
- [ ] Rendering was checked, or the user was told it was not
