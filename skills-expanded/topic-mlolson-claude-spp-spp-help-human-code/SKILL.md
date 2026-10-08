---
name: spp-help-human-code
description: Help a human complete a coding task
---

# SPP Help Human Code Skill

Guide a human through completing a coding task themselves. Use this skill when the SPP ratio is unhealthy (too much AI-written code) and the human needs to write code to improve their ratio. Be a mentor for your human friend, help them stay sharp and learn programming.

## When to Use

- When blocked from writing code by SPP write hook.
- When `spp status` shows the human ratio is below target
- When the human wants to practice writing code themselves
- When teaching mode is appropriate


## Steps

1. **Describe the high level goal**: Explain what we are trying to accomplish at a high level.

2. **Offer code pointers to relevant files**: Show the user which files they need to modify, and which lines, and what they need to do there. You may include code snippets on trickier algorithms or parts that require more arcane syntax knowledge.

3. **Provide test instructions**: Tell the user how they can test their change and verify correctness.

4. **Ask if the user wants more help**: If they want more help, provide guidance including code snippets or other in more depth hand holding.

5. **Offer to review the user's code**: After they are done writing code, review it using standard best practices for code review.

6. **Important: Do not commit user's code with 'Co-Authored-By: Claude'** If the user asks you to commit their code, make sure not to include the 'Co-Authored-By: Claude' note in the commit message. Otherwise, SPP will track the commit as written by Claude and not the human.