---
name: storyboard-builder
description: Generate detailed storyboards for eLearning courses from design documents or content outlines. Use when creating storyboards for Articulate Rise, Articulate Storyline, screen-by-screen specifications, or preparing content for development.
allowed-tools: Read, Write, Edit, Grep, Glob, AskUserQuestion
model: claude-opus-4-5-20251101
user-invocable: true
---

# Storyboard Builder

Generate detailed, development-ready storyboards from your design documents or content outlines.

## What This Skill Does

Transform high-level design documents into detailed storyboards that:

- Specify **screen-by-screen content** for developers
- Define **interactions and navigation** for each screen
- Include **narration scripts** if audio is used
- Describe **visual elements** and layout
- Note **accessibility requirements** per screen
- Provide **developer notes** for implementation

## When to Use This Skill

Use after design document is approved and before development begins:

```
Discovery → Design Document → [STORYBOARD] → Development → QA → Launch
```

## How to Use This Skill

### Option 1: Full Guided Process
Say: "Help me create a storyboard for [project/module]" or invoke `/storyboard-builder`

I'll interview you about:
1. Design document/content outline
2. Level of detail needed
3. Interaction types to include
4. Output format preferences

### Option 2: Build from Design Document
Share your design document and say:
"Create a storyboard for Module 2 based on this design document"

### Option 3: Quick Single Screen
Use the `/storyboard-screen` command for individual screens:
`/storyboard-screen "identify safety hazards" drag-drop`

---

## Interview Process

### Phase 1: Input Gathering
- What's the source document? (design doc, content outline, SME notes)
- Which module/section are we storyboarding?
- What are the learning objectives for this section?

### Phase 2: Format & Detail Level
- **High-level storyboard**: Screen flow with key content (for client review)
- **Production storyboard**: Full detail for developers
- **Output format**: Word-style table or visual/Miro-ready format?

### Phase 3: Interaction Planning
- What interaction types will be used?
- See [interaction-patterns.md](interaction-patterns.md) for options
- Are there branching scenarios?

### Phase 4: Media & Accessibility
- Will there be narration? (need scripts)
- Video content? (need descriptions)
- Accessibility requirements? (WCAG level)

---

## Storyboard Formats

### Format 1: Word/Document Style
Traditional table-based format for detailed specifications.

**Best for:**
- Client/SME review
- Detailed developer handoff
- Compliance documentation

See [storyboard-template-word.md](storyboard-template-word.md)

### Format 2: Visual/Card Style
Card-based format designed for Miro transfer or visual review.

**Best for:**
- Quick visualization
- Miro board population
- Collaborative review sessions

See [storyboard-template-visual.md](storyboard-template-visual.md)

---

## Screen Types

### Title/Intro Screen
- Course/module title
- Overview or hook
- Navigation instructions

### Content Screen
- Instructional content
- Supporting visuals
- Key takeaways

### Interaction Screen
- Practice activity
- User input required
- Feedback provided

### Scenario Screen
- Situation presented
- Decision point
- Consequences shown

### Knowledge Check
- Assessment question
- Answer options
- Feedback per option

### Summary Screen
- Key points recap
- Resources/job aids
- Next steps

### Completion Screen
- Congratulations
- Certificate (if applicable)
- Return to LMS

---

## Output Structure

For each screen, the storyboard includes:

```markdown
## Screen [Number]: [Title]

### Screen Info
| Field | Value |
|-------|-------|
| Screen ID | [Unique ID] |
| Screen Type | [Title/Content/Interaction/etc.] |
| Duration | [Estimated time] |
| Objective | [Which objective this supports] |

### On-Screen Text
[Exact text that appears on screen]

### Narration Script
[Audio narration - if applicable]

### Visual Description
[Description of images, graphics, animations]

### Interaction
| Element | Details |
|---------|---------|
| Type | [Click, drag-drop, etc.] |
| Instructions | [What learner does] |
| Feedback - Correct | [What happens] |
| Feedback - Incorrect | [What happens] |

### Navigation
| Action | Result |
|--------|--------|
| Next | [Screen X] |
| Back | [Screen Y] |
| Menu | [Available/Not] |

### Accessibility Notes
- Alt text: [For images]
- Captions: [For audio/video]
- Keyboard: [Navigation notes]

### Developer Notes
[Technical implementation notes]
```

---

## Interaction Reference

For detailed interaction patterns and when to use them, see:
- [interaction-patterns.md](interaction-patterns.md) - Full interaction reference

Common interactions:
- **Click to reveal** - Progressive disclosure
- **Tabs/Accordion** - Organize chunked content
- **Drag and drop** - Matching, sorting, categorization
- **Hotspots** - Explore images/diagrams
- **Sliders** - Show ranges or progressions
- **Branching** - Scenario-based decisions
- **Fill in blank** - Recall practice
- **Multiple choice** - Knowledge check

---

## Accessibility Checklist

Every storyboard should address accessibility. See:
- [accessibility-checklist.md](accessibility-checklist.md) - Full checklist

Quick checks per screen:
- [ ] Alt text for all images
- [ ] Captions for audio/video
- [ ] Color not sole indicator
- [ ] Keyboard accessible
- [ ] Clear focus indicators
- [ ] Readable text sizes
- [ ] Sufficient contrast

---

## Tips for Better Storyboards

### Be Specific
- "Image of diverse team in meeting" not "team image"
- Exact button labels, not "button to continue"
- Specific feedback text, not "feedback appears"

### Think Like a Developer
- What needs to be built?
- What are the edge cases?
- What happens if...?

### Consider the Learner
- Is the flow logical?
- Are instructions clear?
- Is feedback helpful?

### Plan for Accessibility
- Note accessibility requirements per screen
- Don't leave it for QA to catch

### Version Control
- Number screens consistently
- Track revisions
- Note what changed

---

## Examples

See [examples/sample-storyboard.md](examples/sample-storyboard.md) for a complete storyboard example.

---

## Related Commands & Skills

- `/storyboard-screen` - Quick single screen generation
- `/accessibility-review` - Review storyboard for accessibility
- `/objectives` - Generate objectives for screens
- `design-document` - Create the design doc first

---

## Getting Started

Ready to create a storyboard? Tell me:

1. **What module/section?** (name and learning objectives)
2. **What's your source?** (design doc, outline, or describe the content)
3. **What format?** (Word-style tables or visual cards)
4. **What tool?** (Rise, Storyline, or both)

Or share your design document and I'll help you build the storyboard from there.
