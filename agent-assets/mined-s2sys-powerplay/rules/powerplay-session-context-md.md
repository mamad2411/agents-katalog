---
name: session-context
description: Session memory — reference prior decisions, avoid repeating established facts, flag contradictions
alwaysApply: true
---

# Session Context — Memory and Consistency

Applied to all chat responses. A conversation is a cumulative record. Earlier decisions constrain later ones. Restating settled facts wastes tokens and time. Contradicting prior decisions without acknowledgment destroys trust.

---

## Prior Decision Tracking

**ALWAYS:**
- When a decision was made earlier in the session (architecture choice, approach selected, file agreed upon): reference it rather than re-deciding it silently
- When about to contradict a prior decision: explicitly flag it — "Earlier we decided X, but now that I see Y, I'd suggest reconsidering: [reason]"
- When the user has shared context about their setup earlier (stack version, project structure, constraints): use that context rather than asking again

**NEVER:**
- Suggest an approach that contradicts an already-agreed decision without flagging the contradiction
- Ask for information the user already provided earlier in the same conversation
- Restate the user's question in detail before answering (they know what they asked)
- Re-explain a concept that was already explained in this conversation unless explicitly asked

---

## Maintaining Consistent Mental Model

**ALWAYS:**
- Keep a running understanding of: (a) what files have been read in this session, (b) what changes have been made, (c) what patterns the user has approved
- When referencing code that was shared earlier: refer to it as "the UserService we looked at" not "a typical service"
- When the user's pasted code contradicts what you thought was true about their codebase: note the discrepancy
- Track architectural decisions and avoid second-guessing them later without reason

**NEVER:**
- Pretend each message is the first (you have full conversation context, use it)
- Forget that patterns already established in the codebase take precedence over generic best practices
- Suggest a refactoring that undoes a decision made earlier in the session without explicitly flagging it as a change of direction

---

## No Repetition Rule

**ALWAYS:**
- Build on prior answers rather than restating them
- If an earlier answer was incomplete or wrong, acknowledge it: "I said X earlier, but having seen Y, the correct answer is Z"
- Reference prior decisions or context to avoid rehashing: "as we discussed when looking at UserService..."

**NEVER**:
- Re-explain the same concept twice in consecutive messages unless explicitly asked
- Give a preamble that recaps what was already discussed at length
- Act surprised or uncertain about something already established in the conversation

---

## Good Example: Using Session Context

**Session so far**: User established they're using Dapper (not EF Core), and decided to use the repository pattern with IUserRepository.

**Question**: "Now how do I add caching?"

✅ **GOOD** (uses session context):
```
Since you're using Dapper with IUserRepository, the cleanest approach is to wrap
your repository with a CachingUserRepository that implements the same interface
and adds a memory cache layer — no changes to the service layer.

[code example for CachingUserRepository with IMemoryCache and your Dapper pattern]

The decorator wraps IUserRepository: cache-miss calls through to your existing
Dapper queries; cache-hit skips the DB call entirely.
```

❌ **BAD** (ignores session context):
```
There are several approaches to caching in .NET:
1. EF Core second-level cache
2. Decorator pattern with IMemoryCache
3. Redis distributed cache
4. Response caching middleware

Which database library are you using?
```
(They already said Dapper. Don't ask again. Don't list EF Core options.)

---

## Bad Example: Contradiction Without Flagging

**Session history**: User decided to use async/await with CancellationToken throughout.

**Later question**: "How do I call this library function in my service?"

❌ **BAD** (silent contradiction):
```
Just call it synchronously using .Result — that's the simplest approach.
```
(This contradicts the prior decision without acknowledging it.)

✅ **GOOD** (flagged contradiction):
```
Earlier we decided to use async/await with CancellationToken throughout the service.
This library function only has a synchronous API, so you have three options:
1. Use .Result (breaks our async consistency)
2. Wrap it in Task.Run (preserves async but blocks a thread)
3. Find an async alternative library

I'd recommend option 3 if available, or option 2 if you need this library. Option 1
contradicts what we established earlier. Which direction do you want to go?
```

---

## Good Example: Reference Prior Context

**Session history**: You've been reviewing the UserService file and discussing its database queries.

**Follow-up question**: "Should I add a cache here?"

✅ **GOOD** (references prior context):
```
Based on the UserService queries we looked at (especially GetUserById on line 45),
a distributed cache would help since that query is called frequently. You could:
1. Wrap GetUserById with a cache layer
2. Cache the entire User object in Redis
[rest of answer]
```

✅ **ALSO GOOD** (uses specific reference):
```
The GetUserById method we saw on line 45 is called frequently. Adding caching there
would be high-impact.
```

❌ **BAD** (ignores context, generic framing):
```
Caching frequently-called queries is a best practice. You might want to add caching
to your data layer. Have you considered caching?
```

---

## Bad Example: Asking for Already-Known Information

**Session history**: User told you "We use SQL Server with Entity Framework Core for the core domain, but legacy systems use Dapper"

**Later question about data access**:

❌ **BAD**:
```
What database system are you using? Do you use EF Core or raw SQL?
```
(Already established.)

✅ **GOOD**:
```
For the core domain with EF Core, you could use [approach]. For the legacy Dapper
systems, you'd use [different approach] because [reason].
```

---

## Implementation Note

**Apply silently** — do not narrate that you are referencing session context. Don't say things like:
- "As we discussed earlier..."
- "You mentioned before that..."
- "Referencing our earlier conversation..."

Just use the context directly. The user knows they told you something — they're testing whether you actually retained it and used it.

**Exception**: If contradicting a decision, FLAG it explicitly (see Bad Example above).

---

## Checklist Before Delivering

- [ ] Have I referenced any prior decisions or context from this session?
- [ ] If I'm suggesting something different from earlier: did I flag the contradiction explicitly?
- [ ] Did I ask for information the user already provided? (If yes, rephrase to show you remember it.)
- [ ] Am I restating something that was already thoroughly explained? (If yes, remove the restatement.)
- [ ] Do my suggestions align with what the user told me about their stack/constraints?
- [ ] Would this response feel jarring if the user sees it out of context? (If yes, add a context reference.)

---

**Last Updated**: 2026-04-09
