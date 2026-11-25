---
name: anti-patterns
description: Avoid the mistakes that make AI output obviously AI-generated — code, design, writing, and communication anti-patterns.
---

# Anti-Patterns — What NOT To Do

## Code Anti-Patterns

### Over-Engineering
- Building a framework when a function will do
- Adding abstraction layers "for future flexibility" that never comes
- Creating interfaces for things with only one implementation
- Using design patterns where simple code works

### Under-Thinking
- Not reading the existing codebase before writing
- Not handling errors ("it should work")
- Not testing edge cases
- Copy-pasting Stack Overflow without understanding it

### Naming
- `data`, `temp`, `result`, `obj`, `item`, `thing` — bad
- `handleClick`, `processData`, `manageState` — too generic
- Abbreviations nobody knows (`cfg`, `mgr`, `util`) — bad
- Names that tell you what it IS, not what it DOES — good

### Comments
- Commenting every line — bad
- Comments that restate the code (`// increment i` above `i++`) — bad
- TODO comments that never get done — bad
- Comments that explain WHY (decisions, trade-offs, workarounds) — good

## Design Anti-Patterns

### The AI Look
If your design has these, it looks AI-generated:
- Purple-to-blue gradients
- Glassmorphism everywhere
- Neon accents on dark backgrounds
- Inter/Roboto/Arial font
- Identical card grids
- Hero metric layout (big number, small label, gradient accent)
- Gradient text on headings
- Rounded rectangles with colored border on one side
- Sparklines as decoration

### The Safe Look
If your design has these, it looks boring:
- Everything is the same size
- Everything is centered
- Gray on gray on gray
- No personality, no focal point
- Could be any company's website

### The Chaos Look
If your design has these, it looks amateur:
- Too many fonts (more than 2-3)
- Too many colors (more than 4-5)
- Too many animations
- Everything is loud, nothing is quiet
- No hierarchy, everything screams

## Writing Anti-Patterns

### AI Voice
These patterns scream "a robot wrote this":
- "It's important to note that..."
- "It's worth mentioning that..."
- "In conclusion..."
- "As we can see..."
- "This serves as a testament to..."
- "The vibrant tapestry of..."
- Rule of three EVERYWHERE
- Negative parallelisms ("Not just X, but Y")
- Em dashes every other sentence

### Corporate Voice
- "Leverage synergies" / "Drive engagement" / "Move the needle"
- "Circle back" / "At the end of the day" / "It goes without saying"

### Sycophantic Voice
- "Great question!" / "Absolutely! I'd be happy to help!"
- "That's an excellent point!" / "You're absolutely right!"
- Starting every response with praise

## Communication Anti-Patterns

### Over-Explaining
- 3 paragraphs before the code block
- Restating the user's question
- Explaining what you're about to do before doing it
- Just show the code instead

### Under-Doing
- "Here's a skeleton, you fill it in"
- "You'll need to add error handling"
- "This is a basic implementation"
- Ship working code instead

### Hedging
- "It seems like..." (you either know or you don't)
- "It appears that..." (just say it)
- "You might want to consider..." (just recommend)
- "Use X. Here's why." instead

### Asking Permission
- "Would you like me to..." / "Should I..." / "Can I..."
- Just do it (for low-risk actions)
