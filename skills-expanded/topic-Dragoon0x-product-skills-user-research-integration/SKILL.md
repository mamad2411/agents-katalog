---
name: user-research-integration
description: "Turn user research into product decisions, not just reports. Covers when to research, what methods to use, and how to act on findings. Use when product direction feels disconnected from users, research exists but isn't informing decisions, or you're building on assumptions."
---

# User Research Integration

Turn research into decisions, not slide decks that nobody reads.

## How to use

- `/user-research-integration` Apply research integration constraints to this conversation.
- `/user-research-integration <question>` Design a research approach for the described question.

## Constraints

### When to Research
- MUST research before building when: the problem is unclear, the solution is novel, or the stakes are high
- SHOULD research during building when: usability is uncertain or you're choosing between approaches
- MUST research after building when: adoption is lower than expected or metrics tell a confusing story
- NEVER research to validate a decision that's already been made. That's confirmation bias with extra steps.
- NEVER research when the answer is obvious and you're just delaying the decision

### Method Selection
- User interviews: for understanding problems, motivations, and context. Not for asking what features to build.
- Usability testing: for evaluating whether a solution works. 5 users finds 80% of issues.
- Surveys: for quantifying things you already understand qualitatively. NEVER use as primary discovery.
- Data analysis: for understanding what users do. Pair with qualitative to understand why.
- MUST match method to question. "Do users understand this flow?" needs usability testing, not a survey.

### Acting on Findings
- MUST connect every research finding to a specific product decision or action
- SHOULD present findings as "here's what we learned and here's what it means for what we build"
- MUST prioritize findings by impact on user outcomes, not by how surprising they are
- NEVER let research sit in a doc — synthesize it into the next sprint planning or roadmap review
- SHOULD share raw research (clips, quotes) with the team, not just synthesized takeaways

### Research Quality
- MUST recruit participants who match your target users, not convenience samples
- MUST ask about past behavior, not hypothetical future behavior
- NEVER ask "would you use this?" — people are terrible at predicting their own behavior
- SHOULD watch what users do, not just listen to what they say
- MUST distinguish between what one user said and a pattern across multiple users

### Anti-Patterns
- Research Theater: doing research to check a box without intending to change anything
- The Survey Default: surveying when you should be interviewing
- Confirmation Research: designing research to validate what you've already decided
- Research as Delay: researching endlessly to avoid making a decision
- The Report Graveyard: thorough research that never makes it into product decisions
