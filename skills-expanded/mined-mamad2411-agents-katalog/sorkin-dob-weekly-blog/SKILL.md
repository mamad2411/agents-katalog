---
name: sorkin-dob-weekly-blog
description: Transform weekly STIG+CMMC research into narrative-driven blog posts using Aaron Sorkin's Desire-Obstacle-Battle storytelling framework with MoxyWolf brand voice. Use when Dorian provides weekly research structured in acts with bracketed citations that needs conversion to publication-ready blog content for STIGViewer's technical audience. Creates visceral, human-authentic prose that engages readers emotionally while maintaining technical precision.
---

# Sorkin DOB Weekly Blog

## Overview

Transform Dorian's weekly STIG+CMMC2 research into compelling narrative blogs that apply Aaron Sorkin's Desire-Obstacle-Battle (DOB) storytelling framework with MoxyWolf's brand voice.

**Provenance gate.** Before publishing, route every statistic and factual claim through citation verification (the research-pipeline citation-verifier or an equivalent source-and-date check). No unverified claim ships; flag what can't be verified rather than printing it.

**Sorkin's DOB Framework:**
- **Desire**: What the character wants (win contracts, prove security, sustain trust)
- **Obstacle**: What stands in their way (regulatory complexity, scale problems, technical barriers)
- **Battle**: The conflict when desire meets obstacle (the struggle playing out in the ecosystem)

**This skill transforms**: "Here's what changed" → "Here's what you're fighting for, what's blocking you, and the battle you're in"

## Workflow

### Step 1: Analyze Research Structure

Dorian's research typically arrives as:
- Five-act narrative already outlined
- Bracketed citation numbers [1][2][3]
- Source list at end with URLs
- Act-based headers describing story beats

**Identify DOB elements:**
- Acts I-II = Desire and emerging obstacle
- Acts II-III = Obstacle becomes urgent
- Acts IV-V = Battle intensifies toward new paradigm (don't resolve it)

### Step 2: Apply MoxyWolf Voice

Transform analytical prose into human-authentic voice using these **mandatory elements**:

**Voice Requirements:**
- Use contractions in 80%+ of opportunities ("doesn't," "can't," "it's")
- Vary sentence length aggressively (4-word fragments to 40-word buildups)
- Use fragments deliberately for emphasis
- Start sentences with And, But, Or
- Break topic-sentence patterns
- Replace abstract claims with specific, visceral details
- Always use typographer's quotes: "curly" not "straight"
- Use spaced en-dashes " – " sparingly, never em dashes (—)

**Forbidden Phrases** (AI tells - never use):
- "It's worth noting that..."
- "It's important to understand..."
- "In today's rapidly changing..."
- "At its core..."
- "Moving forward..."
- "In order to..." (use "to")
- "Furthermore," "Additionally," "Moreover" (use And, or delete)

### Step 3: Sharpen Character Stakes

Transform observations into visceral experience.

❌ Avoid: "Contractors faced challenges with manual evidence collection."

✅ Use: "Picture a CISO three weeks before audit, staring at 320 controls and a spreadsheet that hasn't updated since June. The POA&M they submitted six months ago? Already obsolete. The assessor arrives in 18 days."

**Technique**: Use second-person perspective or specific scenarios that put readers inside the experience.

### Step 4: Embed Citations Invisibly

Transform bracketed citations into natural narrative authority with proper in-text citations.

❌ Avoid: "Articles argue automation is 'the only scalable path'.[11]"

✅ Use: "Fortra (2026) isn't being subtle about it: automation is 'the only scalable path' to CMMC Level 2. Manual evidence collection can't scale to 220,000 contractors racing toward the same certification deadline."

**Citation Format:**
Use (Author/Organization, Year) format integrated naturally into prose:
- "Steel Patriot Partners (2024) describes STIGs as..."
- "According to the Federal Register (2024), CMMC 2.0 requires..."
- "DoD's audit (Wiley Law, 2024) flagged weaknesses..."
- "Companies like Accorian (2024) and Integris IT (2024) have been blunt..."

**Technique:**
- Always include (Author/Organization, Year) for factual claims
- Weave citations into sentence structure naturally
- Place citation after the entity name or at end of claim
- Use direct quotes only when exact phrasing matters (keep under 15 words for copyright compliance)
- Include full source list at end with titles and URLs

See `references/examples.md` for detailed before/after transformations.

### Step 5: Structure Narrative Arc

**Opening** (Desire established):
- Show world before the shift
- What everyone wants
- 2-3 paragraphs maximum
- End with emerging tension

**Rising Action** (Obstacle emerges):
- Old methods stop working
- Stakes become urgent
- Show pressure building
- Use concrete examples and numbers

**Battle Intensifies** (Confrontation):
- Ecosystem reorganizes itself
- New solutions emerge but fight isn't over
- Show both promise and remaining challenges

**Ending** (Unresolved tension):
- DO NOT resolve cleanly
- Leave readers mid-battle with choice to make
- Frame ongoing struggle
- End with dramatic tension

❌ Avoid: "Organizations that adopt automation will succeed."
✅ Use: "The question isn't whether automation wins. It's whether your organization figures that out before your competitor does – and before DoD makes the decision for you."

### Step 6: Polish for Human Authenticity

Run anti-AI detection checklist:

- [ ] Contractions used in 80%+ of opportunities
- [ ] No forbidden phrases
- [ ] No formulaic transitions (Furthermore, Additionally, Moreover)
- [ ] Sentence length varies dramatically (4-word and 40-word sentences present)
- [ ] At least one fragment per section
- [ ] Parallelism broken (not everything in threes)
- [ ] Specific examples replace abstract claims
- [ ] Paragraphs vary in length (including single-sentence paragraphs)
- [ ] Sentences start with And, But, or Or in each section
- [ ] No topic-sentence pattern for 3+ consecutive paragraphs
- [ ] Typographer's quotes throughout
- [ ] Spaced en-dashes only, no em dashes

## Output Format

### Blog Post Structure

```markdown
# [Stakes-Driven Headline]

[Opening hook – 2-3 paragraphs establishing desire and tension]

## [Thematic section break - not "Act I"]

[Rising action – obstacle becomes clear]

## [Thematic section break]

[Battle intensifies – ecosystem shifts]

[Ending – unresolved tension, dramatic question]

---

**Sources**

[Full citation list with titles and URLs]
```

**DO NOT** use "Act I, Act II" headers in published blog.
**DO NOT** include bracketed citation numbers in body text.
**DO** include complete source list at end with descriptive titles and full URLs.

### Headline Formula

Capture DOB tension in headline:

❌ Avoid: "CMMC 2.0 Updates for 2026"
❌ Avoid: "How STIG Automation Helps CMMC Compliance"

✅ Use: "The Audit That Outgrew the Checklist: When Paperwork Stopped Being Enough"
✅ Use: "From Passing Audits to Proving Trust: The STIG Automation Reckoning"
✅ Use: "220,000 Contractors, 200 Assessors, One Deadline: Why Manual Evidence Just Died"

**Formula**: [Vivid situation] + [Stakes/tension] or [Old world] vs [New reality]

## Execution Checklist

Before delivery, verify:

**Structure:**
- [ ] Clear DOB arc (desire → obstacle → battle)
- [ ] Opens with visceral hook, not abstract overview
- [ ] Builds tension through middle
- [ ] Ends with unresolved dramatic question
- [ ] No "Act I/II/III" headers in final version
- [ ] Thematic section breaks flow naturally

**Voice:**
- [ ] MoxyWolf brand voice throughout
- [ ] 80%+ contractions
- [ ] No AI tell phrases
- [ ] Sentence length varies dramatically
- [ ] Specific examples, not abstract claims
- [ ] Fragments used deliberately
- [ ] Typographer's quotes throughout

**Citations:**
- [ ] No bracketed numbers in body text
- [ ] In-text citations use (Author/Organization, Year) format
- [ ] Every factual claim has proper citation
- [ ] Citations woven naturally into prose (not interrupting flow)
- [ ] Direct quotes under 15 words (copyright compliance)
- [ ] Full source list at end with titles and URLs
- [ ] Attributions feel organic to narrative

**Impact:**
- [ ] Stakes are visceral and immediate
- [ ] Reader can feel pressure/tension
- [ ] Technical audience respects precision
- [ ] Ending leaves them mid-battle with decision
- [ ] Could be read aloud and sound natural

## Common Pitfalls

**❌ Leaving citations as [1][2][3]**: Transform into natural attributions

**❌ Resolving the tension**: Sorkin doesn't wrap neatly. Neither should you. Leave readers mid-battle.

**❌ Using AI transitions**: "Furthermore," "Additionally," "Moreover" are tells. Use And, But, or delete.

**❌ Abstract language**: "Organizations face challenges" → "You're the CISO staring at 320 controls and 18 days until audit"

**❌ Topic sentences everywhere**: Break the pattern. Build to points. Bury them. Mix it up.

**❌ Clean parallelism**: Make one item longer, one shorter, one a fragment

**❌ Hedging**: "This might potentially help" → "This changes everything"

**❌ Neat endings**: Don't end with resolution. End with "The question is whether you figure it out before your competitor does."

## Resources

See `references/examples.md` for detailed before/after transformation examples showing:
- Opening hook transformation
- Embedding citations organically
- Making stakes visceral
- Creating unresolved dramatic endings

## Success Criteria

A successful transformation:
1. Feels like a story, not a report
2. Puts reader in scene with visceral, specific details
3. Creates tension that builds through piece
4. Sounds human when read aloud (contractions, natural rhythm, varied sentences)
5. Respects audience intelligence with technical precision
6. Leaves them thinking with unresolved dramatic question
7. Passes AI detection test (no forbidden phrases, authentic voice)
8. Maintains MoxyWolf brand (bold but precise, structured but wild)
