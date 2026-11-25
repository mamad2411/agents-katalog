---
name: receiving-code-review
description: Code review reception methodology - technical rigor and verification, not performative agreement. Use when receiving code review feedback, before implementing suggestions.
category: engineering
exposure: standard
---

# Code Review Reception

## Overview

When receiving code review feedback, require technical rigor and verification, not performative agreement or blind implementation.

**Core principle:** Evaluate feedback on technical merit, not social pressure.

## The Iron Law

```
NO IMPLEMENTATION WITHOUT TECHNICAL VERIFICATION FIRST
```

Don't implement suggestions just because a reviewer said so. Verify they're technically correct.

## When to Use

- Receiving code review feedback
- PR comments requiring changes
- Architecture review suggestions
- Any external technical feedback

## The Process

### Step 1: Understand the Feedback

1. **Read the feedback completely** — don't skim
2. **Identify the concern** — what specific issue is raised?
3. **Check if it's factual** — is the reviewer correct about the code?
4. **Check if it's opinion** — is this a preference or a real issue?

### Step 2: Evaluate Technical Merit

**For each piece of feedback:**

1. **Verify the claim** — does the code actually have this issue?
2. **Check the suggestion** — would the proposed fix actually help?
3. **Consider trade-offs** — what are the costs of the change?
4. **Look for alternatives** — is there a better way to address the concern?

**Red flags in feedback:**
- "I think this might be..." (uncertain)
- "You should probably..." (unsure)
- "This feels wrong..." (subjective)
- "Best practice says..." (without citation)

### Step 3: Respond Technically

**If feedback is correct:**
```
"You're right, [specific issue]. I'll fix it by [specific approach]."
```

**If feedback is incorrect:**
```
"I see the concern, but [technical reason why current approach is correct].
Here's the evidence: [specific code/data/test results]."
```

**If feedback is ambiguous:**
```
"I'm not sure I understand the concern. Could you clarify [specific aspect]?
Currently, the code does [what it actually does]."
```

### Step 4: Implement or Push Back

**Implement when:**
- Feedback identifies a real bug
- Feedback suggests a genuinely better approach
- Feedback addresses a legitimate concern about maintainability, performance, or security

**Push back when:**
- Feedback is based on incorrect understanding of the code
- Feedback suggests a worse approach (verify with benchmarks/tests)
- Feedback is purely stylistic with no technical benefit
- Feedback would introduce new bugs or complexity

## Anti-Patterns

| Anti-Pattern | Reality |
|--------------|---------|
| "The reviewer said it, so it must be right" | Reviewers make mistakes too |
| "I'll just implement it to avoid conflict" | Technical debt from social pressure |
| "They have more experience" | Experience doesn't guarantee correctness |
| "It's easier to just do it" | Easier ≠ better |
| "I don't want to seem difficult" | Technical rigor > social comfort |

## Response Templates

### Accepting Feedback
```
Good catch. The [specific issue] is real. I'll fix it by [approach].
```

### Questioning Feedback
```
I see the concern about [issue]. However, [technical reason].
The current approach works because [evidence].
Could you clarify what specific problem you're seeing?
```

### Requesting Evidence
```
I'd like to verify this. Can you point me to:
- The specific code that has this issue?
- A test case that demonstrates the problem?
- Documentation that supports this approach?
```

### Explaining Trade-offs
```
I considered [suggested approach], but chose [current approach] because:
- [trade-off 1]
- [trade-off 2]

The tests show [evidence]. Would you like me to add a comment explaining the reasoning?
```

## Quick Reference

```
1. Read feedback completely
2. Verify technical claims
3. Evaluate trade-offs
4. Respond with evidence
5. Implement or push back (with reason)
```

## Integration with Our Workflow

- **After code review:** Invoke this skill
- **If implementing:** Use `test-driven-development` for changes
- **If pushing back:** Provide technical evidence
- **After changes:** Use `verification-before-completion` skill
