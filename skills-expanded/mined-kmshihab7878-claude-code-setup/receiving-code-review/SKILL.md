---
name: Receiving Code Review
description: Guidance for evaluating review feedback, applying valid changes, and responding with evidence.
---

# Receiving Code Review

> Technical rigor over social performance. Verify before implementing. Push back with evidence.

## Triggers

- Reviewer feedback received on a PR or code change
- User provides review comments to address
- `/review` output has REQUEST CHANGES or NEEDS DISCUSSION items

## Principles

### 1. Technical Rigor Over Social Performance

- Do not implement suggestions just to be agreeable
- Evaluate every suggestion on technical merit
- If a suggestion would make the code worse, push back with evidence
- "Thank you for the feedback" is nice but irrelevant — focus on the code

### 2. Verify Suggestions Before Implementing

Before applying ANY review suggestion:

```
1. READ the suggestion carefully — what exactly is being asked?
2. UNDERSTAND the rationale — why does the reviewer want this change?
3. VERIFY the suggestion is correct:
   - Does it actually fix the issue described?
   - Does it introduce new problems?
   - Is it consistent with project conventions?
4. If valid: implement, run tests, confirm improvement
5. If invalid: respond with evidence why, not opinion
```

### 3. Push Back on YAGNI

If a reviewer suggests adding:
- Extra abstraction layers "for future flexibility"
- Premature optimization without profiling data
- Error handling for impossible states
- Configuration for things that will never change

Push back with:
```
"This adds complexity without current need. The simpler version:
- Has fewer lines to maintain
- Is easier to understand
- Can be refactored later IF the need arises
- [Specific evidence why the current approach is sufficient]"
```

## Response Protocol

For each review comment, respond with ONE of:

| Response | When | Action |
|----------|------|--------|
| **Accepted** | Suggestion is correct and improves the code | Implement, test, confirm |
| **Accepted with modification** | Core idea is good but implementation differs | Implement your version, explain why |
| **Declined with evidence** | Suggestion would make code worse | Explain with evidence, propose alternative |
| **Needs discussion** | Trade-off isn't clear, need more context | Ask specific clarifying questions |

## After Addressing All Comments

1. Run the full test suite — ensure nothing broke
2. Show the diff of all changes made in response to review
3. Summarize: N accepted, M declined (with reasons), K modified
4. Push updated code
5. Comment on PR summarizing changes

## Integration

- Review comments come from `/review` output or PR feedback
- Changes follow `test-driven-development` where applicable
- Final verification uses `verification-before-completion`
- Updated code pushed via `branch-finishing` Option 2 workflow
