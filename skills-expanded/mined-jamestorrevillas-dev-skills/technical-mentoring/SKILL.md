---
name: technical-mentoring
description: Use this skill when mentoring junior developers, conducting code walkthroughs, transferring knowledge, onboarding new team members, or giving technical guidance to less experienced developers. Trigger on keywords: mentor, mentoring, junior developer, teach, knowledge transfer, code walkthrough, explain to junior, help teammate, onboarding developer.
---

# Technical Mentoring

## Core Principle

**Your goal is to make yourself unnecessary.**

A good mentor builds independence, not dependency. Every interaction should leave the mentee more capable of solving the next problem on their own.

---

## The Mentoring Spectrum

```
TELL ←————————————————————————→ GUIDE
"Here's the answer"              "What do you think the problem is?"
```

Default to the right side. Move left only when:
- They're truly blocked and time is critical
- The concept is foundational and needs direct explanation
- Safety or correctness is at risk

---

## The Socratic Approach to Code Review

Instead of:
```
❌ "This is wrong, change it to X"
```

Try:
```
✅ "What happens if this value is null?"
✅ "What's the time complexity of this approach?"
✅ "What would happen under high load here?"
```

This builds reasoning skills, not just fixes the current bug.

---

## Explaining Technical Concepts

### The 4-Step Teaching Pattern
1. **Why it matters** — connect to something they already care about
2. **Simple analogy** — link to something familiar
3. **Minimal working example** — smallest possible illustration
4. **Common mistake** — the gotcha that trips everyone up

### Calibrating Explanation Depth
- Too simple → they don't learn anything new
- Too complex → they lose the thread
- Ask first: "What's your current understanding of X?"
- Adapt to their answer

---

## Code Walkthrough Structure

When walking someone through your code:
```
1. Start with WHY — what problem does this solve?
2. Show the data flow — input → process → output
3. Explain non-obvious decisions — "I chose X here because..."
4. Point out what you'd do differently now — models growth mindset
5. Invite questions at each step
```

---

## Giving Feedback on Junior Code

### The Feedback Ladder
1. **Acknowledge** — find something genuinely good first
2. **Question** — ask before telling ("What was your thinking here?")
3. **Suggest** — "One approach I've used is..." not "You should..."
4. **Teach** — explain the principle behind the suggestion
5. **Verify** — "Does that make sense? What questions do you have?"

### Feedback Anti-Patterns
- Rewriting their code entirely — kills ownership and learning
- Fixing without explaining — they'll make the same mistake next time
- Being vague — "make this cleaner" without showing how
- Only criticizing — not noticing what they did well

---

## Tracking Mentee Growth

Periodically check in:
```
"What's one thing you can do now that you couldn't 3 months ago?"
"What's still confusing or intimidating?"
"What kind of support is most helpful from me?"
```

Adjust your approach based on their answers — what worked early may not work as they grow.
