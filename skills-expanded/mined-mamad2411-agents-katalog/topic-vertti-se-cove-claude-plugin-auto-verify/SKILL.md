# Auto-Verify Skill (Software Engineering)

This skill suggests using `/verify` for software engineering tasks that would benefit from systematic verification.

## Design Philosophy

**Be minimal and non-eager.** Users invoke `/verify` when they want it. This skill only suggests verification in specific high-value scenarios where the user might not realize verification would help.

## When to Suggest Verification

Only suggest `/verify` when the user's question involves **ALL** of these:
1. **Significant complexity** - Not a trivial fix or simple question
2. **High risk of subtle bugs** - Async patterns, state management, security
3. **Verifiable claims** - There are specific behaviors that can be tested

### Good Candidates

**Complex code patterns with known pitfalls:**
- React hooks with async behavior (useEffect, useCallback + async)
- Debouncing/throttling implementations
- Race condition scenarios
- Caching strategies
- Authentication/authorization flows

**Security-sensitive operations:**
- Input validation and sanitization
- Token handling and session management
- Password hashing and credential storage
- Encryption/decryption implementations
- Access control and permission checks

**Complex async patterns:**
- Promise chains with error handling
- Concurrent operations with shared state
- Retry logic with backoff strategies
- Streaming and chunked data processing
- WebSocket or real-time connection handling

**Financial and critical operations:**
- Payment processing logic
- Inventory or balance calculations
- Audit logging implementations
- Data migration scripts
- Rate limiting implementations

**Architectural decisions with significant tradeoffs:**
- State management approach (Redux vs alternatives)
- Microservices vs monolith
- Database schema design
- API design patterns

**Bug investigations where the cause is uncertain:**
- "I think the bug is X but not sure"
- Intermittent failures
- Production issues with incomplete information

## When NOT to Suggest

**Do NOT suggest verification for:**
- Simple questions ("How do I center a div?")
- Trivial fixes (typos, simple renames)
- Documentation lookups
- Exploratory coding ("Let's experiment with this approach")
- Clear requirements with obvious implementation
- Time-sensitive requests

## Suggested Response Format

When you do suggest verification, be brief and non-pushy:

```
This [type of task] has some subtle edge cases that `/verify` could catch.
Would you like me to use it, or should I proceed directly?
```

**Examples:**

- "Debouncing has some cleanup gotchas. `/verify` could catch those, or I can proceed directly."
- "Token refresh flows are tricky. Want `/verify` to double-check the implementation?"
- "This architectural decision has significant tradeoffs. `/verify` would evaluate them systematically."

## Important Notes

- **Never auto-invoke** - Only suggest, let user decide
- **Acknowledge if declined** - "Got it, proceeding directly"
- **Don't repeat** - If user declines once, don't suggest again for similar questions
- **Trust the user** - They know when they want thorough verification vs quick answers
