---
name: presentation-content
description: |
  Creates compelling presentation content including outlines, slide content, speaker notes,
  and pitch decks. Uses storytelling frameworks and persuasion principles. Use this skill
  for PPT content, webinar scripts, training materials, sales presentations, and any
  slide-based content needs.
allowed-tools:
  - Bash
  - Read
  - Write
  - Glob
  - Grep
  - AskUserQuestion
---

# Presentation Content Skill

> **QUICK REFERENCE**
> - **Output folder**: `output/content/presentations/`
> - **File naming**: `YYYY-MM-DD_topic_presentation.md`
> - **Sample script**: `scripts/samples/sample_presentation_content.py`
> - **Run with**: `.venv\Scripts\python.exe scripts/samples/sample_presentation_content.py`
> - **Types**: Pitch decks, webinar scripts, training materials, sales presentations
> - **References**: Check `references/` folder for brand voice and examples
> - **Python**: ALWAYS use `.venv\Scripts\python.exe` (never bare `python`)

Creates compelling, engaging presentation content that captures attention and drives action.

## Scope of This Skill

**This skill handles:**
- Presentation outlines and structure
- Slide content and headlines
- Speaker notes
- Pitch deck content
- Webinar scripts
- Training presentation content
- Sales deck content
- Conference talk outlines
- Workshop materials

**NOT handled by this skill:**
- Editing PPTX files → Use `local-pptx-editor`
- Visual design → Creates content, not design
- Video editing → Creates scripts only

## Presentation Types & Frameworks

### 1. Pitch Decks

**Framework: Problem-Solution-Traction**

```
Slides:
1. Title + Hook
2. Problem (Pain Point)
3. Solution (Your Product)
4. Market Opportunity
5. Product Demo/Features
6. Business Model
7. Traction/Metrics
8. Competition
9. Team
10. Ask/Next Steps
```

### 2. Sales Presentations

**Framework: SPIN (Situation-Problem-Implication-Need)**

```
Slides:
1. Title + Agenda
2. Understand Their Situation
3. Problem Identification
4. Implications of Problem
5. Solution Overview
6. Features → Benefits
7. Case Study/Results
8. Pricing/Options
9. Implementation
10. Next Steps
```

### 3. Educational/Training

**Framework: Tell-Show-Do-Review**

```
Slides:
1. Title + Objectives
2. Why This Matters
3. Concept Overview (Tell)
4. Example/Demo (Show)
5-8. Step-by-Step (Do)
9. Common Mistakes
10. Summary + Action Items
```

### 4. Conference Talks

**Framework: Story Arc**

```
Slides:
1. Hook (Bold Statement/Question)
2. Context (Why You, Why Now)
3. The Challenge
4. The Journey/Discovery
5-8. Key Insights
9. Transformation/Results
10. Call to Action + Resources
```

### 5. Quarterly Business Reviews

**Framework: Review-Analyze-Plan**

```
Slides:
1. Executive Summary
2. Key Metrics Overview
3. Goals vs. Actual
4. Wins & Successes
5. Challenges & Learnings
6. Market/Competitive Update
7. Next Quarter Goals
8. Resource Needs
9. Risks & Mitigations
10. Discussion/Q&A
```

## Slide Content Principles

### The Rule of Three
- 3 main points per presentation section
- 3 bullet points per slide maximum
- 3 supporting examples for key claims

### Headline Writing
Every slide title should be a **takeaway**, not a label:

```
BAD: "Market Analysis"
GOOD: "Market Growing 40% YoY, $2B Opportunity"

BAD: "Our Solution"
GOOD: "Cut Processing Time from 2 Hours to 2 Minutes"

BAD: "Team"
GOOD: "25 Years Combined Industry Experience"
```

### Visual + Verbal Balance
- Slides are visual aids, NOT scripts
- One idea per slide
- Minimal text, maximum impact
- Speaker notes for details

## 3-Mode Workflow

### MODE 1: PLAN

1. **Understand Presentation Goals**
   ```
   - Purpose: Inform, persuade, train?
   - Audience: Who are they?
   - Duration: How long?
   - Format: In-person, virtual, recorded?
   - Outcome: What should they do/feel after?
   ```

2. **Check References**
   ```bash
   # Check presentation examples
   ls references/examples/presentations/

   # Analyze presentation patterns
   python scripts/content/analyze_presentations.py \
     --folder references/examples/presentations/ \
     --output output/analysis/ppt_patterns.json
   ```

3. **Select Framework**
   - Match to presentation type
   - Adapt to audience needs
   - Plan slide count

4. **Document Plan**
   ```markdown
   ## Presentation Plan

   ### Overview
   - Type: [Pitch/Sales/Training/etc.]
   - Audience: [Description]
   - Duration: [X minutes]
   - Slides: [X slides]

   ### Framework
   [Framework name and structure]

   ### Key Messages
   1. [Message 1]
   2. [Message 2]
   3. [Message 3]

   ### Call to Action
   [What you want them to do]
   ```

### MODE 2: CLARIFY

**Essential Questions:**
- "What's the presentation about?"
- "Who is the audience?"
- "How much time do you have?"
- "What's the one thing you want them to remember?"

**Context Questions:**
- "What do they already know?"
- "What objections might they have?"
- "What's in it for them?"

**Style Questions:**
- "Formal or conversational?"
- "Data-heavy or story-driven?"
- "Any must-include content?"

### MODE 3: IMPLEMENT

1. **Create Outline**
   ```bash
   python scripts/content/generate_outline.py \
     --type pitch-deck \
     --topic "Product Launch" \
     --slides 12 \
     --output output/content/presentations/
   ```

2. **Write Slide Content**
   - Headlines (takeaway statements)
   - Bullet points (3 max per slide)
   - Speaker notes (detailed)

3. **Save Output**
   ```
   output/content/presentations/
   ├── [date]_[topic]/
   │   ├── outline.md
   │   ├── slides_content.md
   │   ├── speaker_notes.md
   │   └── handout.md
   ```

## Output Format

### Full Presentation Document

```markdown
# [Presentation Title]

## Slide 1: [Headline as Takeaway]

**Visual**: [Description of visual element]

**Bullet Points**:
- Point 1
- Point 2
- Point 3

**Speaker Notes**:
[What to say - detailed talking points]

---

## Slide 2: [Headline as Takeaway]
...
```

### Slide-by-Slide Format

```markdown
---
SLIDE 1
---
HEADLINE: [Takeaway statement]
CONTENT:
• [Bullet 1]
• [Bullet 2]
• [Bullet 3]
VISUAL: [Suggested image/chart]
NOTES: [Speaking points]
TRANSITION: [How to lead into next slide]

---
SLIDE 2
---
...
```

## Presentation Templates

### Pitch Deck Template

```markdown
# [Company Name] Pitch Deck

## Slide 1: Title
HEADLINE: [Company Tagline]
VISUAL: Logo + compelling image
NOTES: Introduce yourself, set the hook

## Slide 2: The Problem
HEADLINE: [Problem statement as pain point]
CONTENT:
• [Stat showing problem magnitude]
• [Who experiences this]
• [Current solutions failing]
VISUAL: Image representing frustration
NOTES: Build empathy, make it relatable

## Slide 3: The Solution
HEADLINE: [Product name] [does what]
CONTENT:
• [Core feature 1 → benefit]
• [Core feature 2 → benefit]
• [Core feature 3 → benefit]
VISUAL: Product screenshot or demo
NOTES: Keep high-level, save demo for later

## Slide 4: Market Opportunity
HEADLINE: $[X]B Market Growing [X]% YoY
CONTENT:
• TAM: [Total market]
• SAM: [Serviceable market]
• Target: [Initial focus]
VISUAL: Market size chart
NOTES: Show the opportunity is real and big

## Slide 5: Business Model
HEADLINE: [How You Make Money]
CONTENT:
• [Revenue stream 1]
• [Revenue stream 2]
• [Pricing model]
VISUAL: Pricing table or revenue flow
NOTES: Simple, clear, believable

## Slide 6: Traction
HEADLINE: [Key Metric] and Growing
CONTENT:
• [Users/Revenue/Growth metric]
• [Customer logos or names]
• [Key milestone achieved]
VISUAL: Growth chart
NOTES: Show momentum

## Slide 7: Competition
HEADLINE: We Win on [Key Differentiator]
CONTENT:
• [Feature comparison matrix]
VISUAL: Competitive positioning chart
NOTES: Acknowledge competition, show differentiation

## Slide 8: Team
HEADLINE: [Years] Combined [Industry] Experience
CONTENT:
• [Founder 1 - relevant credential]
• [Founder 2 - relevant credential]
• [Key team member]
VISUAL: Team photos
NOTES: Why you're the team to do this

## Slide 9: The Ask
HEADLINE: Raising $[X] to [Achieve Milestone]
CONTENT:
• [Use of funds breakdown]
• [What you'll achieve]
• [Timeline]
VISUAL: Milestone roadmap
NOTES: Clear, specific, achievable

## Slide 10: Thank You + Contact
HEADLINE: Let's [Build the Future/Change X] Together
CONTENT:
• [Contact email]
• [LinkedIn/Website]
VISUAL: Contact info + logo
NOTES: Clear next step
```

### Training Presentation Template

```markdown
# [Training Topic]

## Slide 1: Welcome
HEADLINE: [What They'll Learn to Do]
CONTENT:
• By the end, you'll be able to:
  - [Objective 1]
  - [Objective 2]
  - [Objective 3]

## Slide 2: Why This Matters
HEADLINE: [Impact/Benefit of This Skill]
CONTENT:
• [Business impact]
• [Personal benefit]
• [Consequence of not knowing]

## Slide 3: Concept Overview
HEADLINE: [The Core Framework/Concept]
CONTENT:
• [Definition]
• [Key principle 1]
• [Key principle 2]
VISUAL: Framework diagram

## Slides 4-7: Step-by-Step
HEADLINE: Step [X]: [Action]
CONTENT:
• [How to do it]
• [Common mistake to avoid]
• [Tip for success]
VISUAL: Screenshot or example

## Slide 8: Practice Exercise
HEADLINE: Your Turn: [Exercise Name]
CONTENT:
• [Instructions]
• [Time allocated]
• [What success looks like]

## Slide 9: Common Mistakes
HEADLINE: Avoid These [X] Pitfalls
CONTENT:
• [Mistake 1] → [Instead, do this]
• [Mistake 2] → [Instead, do this]
• [Mistake 3] → [Instead, do this]

## Slide 10: Summary + Next Steps
HEADLINE: Key Takeaways
CONTENT:
• [Takeaway 1]
• [Takeaway 2]
• [Takeaway 3]
• Next step: [Action item]
```

## Example Interactions

### "Create a pitch deck for my startup"
```
[PLAN]
- Pitch deck format
- 10-12 slides
- Investor audience

[CLARIFY]
- "What problem does your startup solve?"
- "What's your business model?"
- "Any traction or metrics to share?"
- "How much are you raising?"

[IMPLEMENT]
- Create full pitch deck outline
- Write all slide content
- Include speaker notes
- Save to output folder
```

### "I need a sales presentation"
```
[PLAN]
- Sales presentation format
- SPIN framework
- 10-15 slides

[CLARIFY]
- "What are you selling?"
- "Who's the buyer (role, company size)?"
- "What objections do you typically face?"
- "Any case studies to include?"

[IMPLEMENT]
- Create SPIN-structured deck
- Focus on their problems → your solution
- Include case study slide
- Strong close with next steps
```

### "Help me outline a conference talk"
```
[PLAN]
- Conference talk format
- Story arc framework
- 20-30 slides for 30 min

[CLARIFY]
- "What's the topic?"
- "Who's the audience?"
- "What's the one big idea?"
- "Any personal story to share?"

[IMPLEMENT]
- Create compelling narrative arc
- Hook opening
- Build to transformation
- End with clear CTA
```

## Speaker Notes Best Practices

- **Opening**: Write your first 2-3 sentences verbatim
- **Transitions**: Note how each slide connects to the next
- **Key points**: Bullet what to emphasize
- **Timing**: Estimate time per slide
- **Questions**: Anticipate what audience might ask
- **Stories**: Script any anecdotes briefly

## Output Files

Presentation content saved to:
- `output/content/presentations/[project]/outline.md` - Structure
- `output/content/presentations/[project]/slides.md` - Full content
- `output/content/presentations/[project]/notes.md` - Speaker notes
- `output/content/presentations/[project]/handout.md` - Leave-behind

## Quality Checklist

Before finalizing:
- [ ] Clear takeaway headline on every slide
- [ ] Maximum 3 bullet points per slide
- [ ] One idea per slide
- [ ] Opening hooks attention
- [ ] Closing has clear CTA
- [ ] Speaker notes provide context
- [ ] Follows chosen framework
- [ ] Appropriate for time limit
- [ ] Audience-appropriate language
