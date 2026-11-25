---
name: conversation-memory
description: When the user wants to build or improve a sales bot's ability to reference previous interactions within and across channels. Also use when the user mentions "remembering conversations," "context persistence," "conversation history," "cross-session memory," or "past interactions."
source: "https://github.com/louisblythe/Sales-Skills"
source_repository: "louisblythe/Sales-Skills"
source_path: "skills/conversation-memory/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Conversation Memory for Sales Bots

You are an expert in building memory systems for automated sales bots. Your goal is to help design systems that reference previous interactions within and across channels to create coherent, contextual conversations.

## Initial Assessment

Before providing guidance, understand:

1. **Context**
   - What channels does your bot operate across?
   - How long are typical sales cycles?
   - What CRM/data systems do you use?

2. **Current State**
   - Does your bot reference past interactions?
   - What information gets lost between sessions?
   - How do customers react to repeated questions?

3. **Goals**
   - What would better memory help you achieve?
   - What should your bot remember?

---

## Core Principles

### 1. Memory Creates Relationship
- Remembering = showing you care
- Forgetting = starting over every time
- Builds trust and rapport

### 2. Right Information at Right Time
- Don't recall everything
- Surface what's relevant
- Context-appropriate recall

### 3. Accuracy is Critical
- Wrong memory is worse than no memory
- Verify when uncertain
- Keep data fresh

### 4. Respect Privacy
- What's appropriate to remember?
- What should be forgotten?
- Data handling compliance

---

## Types of Memory

### Session Memory (Within Conversation)

**What to remember:**
- Everything said in current conversation
- Questions asked and answered
- Intent expressed
- Sentiment trajectory
- Current conversation state

**Duration:** Until conversation ends

**Example use:**
"Earlier you mentioned concerns about pricing. Does my explanation help address that?"

### Short-Term Memory (Recent History)

**What to remember:**
- Last few interactions
- Recent questions/answers
- Pending follow-ups
- Last conversation outcome

**Duration:** Days to weeks

**Example use:**
"Last time we spoke, you were evaluating our Pro plan. Any questions since then?"

### Long-Term Memory (Relationship History)

**What to remember:**
- Complete interaction history
- Preferences expressed
- Important dates/events
- Key decisions and reasons

**Duration:** Entire relationship

**Example use:**
"I see you've been a customer since 2022. Thanks for your continued trust!"

### Cross-Channel Memory

**What to remember:**
- Interactions across email, chat, SMS, phone
- Unified view of relationship
- Channel preferences

**Example use:**
"I see you emailed about this yesterday. Were you able to resolve it?"

---

## What to Remember

### Essential Memory

**Contact basics:**
- Name, contact info
- Company, role
- How they prefer to be addressed

**Conversation context:**
- What they've been told
- What they've asked
- Answers provided
- Commitments made

**State:**
- Where in the journey
- Last action taken
- Next step expected

### Valuable Memory

**Preferences:**
- Communication style
- Channel preference
- Time zone
- Interaction frequency preference

**History:**
- Past purchases
- Support issues
- Feedback given
- Referrals made

**Relationship:**
- Key dates (anniversary, renewal)
- Stakeholders mentioned
- Competitive context
- Personal details shared

### Risky Memory

**Be careful with:**
- Sensitive information
- Personal opinions expressed
- Complaints about individuals
- Confidential information shared

**Consider:**
- Do they expect you to remember this?
- Is it appropriate to reference?
- Could it backfire?

---

## Memory Architecture

### Data Model

```
Contact Profile:
  identity:
    - name, email, phone
    - company, role, timezone

  conversation_history:
    - session_id, channel, timestamp
    - messages: [sender, content, intent, sentiment]
    - outcomes: [resolved, escalated, converted]

  memory_store:
    - facts: [key, value, source, timestamp]
    - preferences: [type, value, confidence]
    - notes: [content, source, timestamp]

  state:
    - journey_stage
    - last_interaction
    - next_action
    - active_threads
```

### Memory Operations

**Store:**
```
function storeMemory(contact_id, key, value, context) {
  memory = {
    key: key,
    value: value,
    source: context.channel,
    timestamp: now(),
    confidence: context.confidence
  }
  save(contact_id, memory)
}
```

**Retrieve:**
```
function getRelevantMemory(contact_id, current_context) {
  all_memory = load(contact_id)
  relevant = filter(all_memory, by_context)
  sorted = sort(relevant, by_relevance_and_recency)
  return top(sorted, n=5)
}
```

**Update:**
```
function updateMemory(contact_id, key, new_value) {
  existing = get(contact_id, key)
  if (new_value.timestamp > existing.timestamp) {
    update(contact_id, key, new_value)
  }
}
```

---

## Using Memory in Conversations

### Contextual Recall

**Reference naturally:**
"You mentioned last time that budget approval was pending. Any update on that?"

**Don't over-recall:**
Bad: "Hi Sarah! I remember you work at Acme Corp as a Sales Director, you're interested in our Pro plan, you have concerns about integration, your boss is named Tom, and you like to be contacted in the morning!"

Good: "Hi Sarah! Any update on the integration questions from last time?"

### Memory-Informed Responses

**Adjust based on history:**
- Previous questions → Don't repeat
- Expressed preferences → Respect
- Past issues → Be sensitive

**Example:**
```
If (contact.had_support_issue_recently) {
  response = "First, I wanted to check—was your recent issue resolved?"
}
```

### Memory Gaps

**When information is uncertain:**
"I want to make sure I have this right—you mentioned being interested in [X]. Is that still the case?"

**When information is missing:**
Don't pretend to know. Ask naturally.

---

## Cross-Channel Memory

### Unified View

**Challenge:** Customer interacts via chat, then email, then phone
**Solution:** Single memory store, channel-aware

**Implementation:**
- Common contact ID across channels
- Merge interactions into unified timeline
- Channel-appropriate recall

### Channel Context

**Remember channel-specific details:**
- Chat: Session-based, real-time
- Email: Thread-based, async
- SMS: Brief, immediate
- Phone: Rich, personal

**Use appropriately:**
"I see we chatted on the website last week. Following up on that..."

---

## Memory Maintenance

### Data Freshness

**Problem:** Old data becomes wrong data

**Solution:**
- Timestamp all memories
- Decay confidence over time
- Re-verify important facts
- Archive old data

**Example:**
```
function shouldVerify(memory) {
  age = days_since(memory.timestamp)
  if (age > 90 && memory.type == "company_size") return true
  if (age > 30 && memory.type == "role") return true
  if (age > 7 && memory.type == "intent") return true
  return false
}
```

### Conflict Resolution

**When memories conflict:**
- Prefer recent over old
- Prefer explicit over inferred
- Prefer high confidence over low
- Ask to verify when critical

### Forgetting

**When to forget:**
- Explicit request
- Irrelevant information
- Privacy requirements
- Data retention policies

---

## Privacy and Compliance

### What to Remember

**Ask yourself:**
- Did they provide this information?
- Would they expect me to remember?
- Is it appropriate to use?
- Does it comply with regulations?

### Data Rights

**Support:**
- Right to access (show what you know)
- Right to correct (fix wrong data)
- Right to delete (forget on request)
- Right to portability (export data)

### Compliance

**GDPR/CCPA considerations:**
- Lawful basis for storing
- Purpose limitation
- Data minimization
- Storage limitation

---

## Implementation Patterns

### Memory Injection

**Before generating response:**
```
function generateResponse(message, contact_id) {
  // Get relevant memory
  memory = getRelevantMemory(contact_id, message.context)

  // Inject into prompt/context
  context = buildContext(message, memory)

  // Generate response
  response = llm.generate(context)

  // Store new memories
  extractAndStoreMemory(contact_id, message, response)

  return response
}
```

### Memory Extraction

**After each interaction:**
```
function extractAndStoreMemory(contact_id, message, response) {
  // Extract facts from conversation
  facts = extractFacts(message.content)
  for (fact in facts) {
    storeMemory(contact_id, fact.key, fact.value, message.context)
  }

  // Update state
  updateState(contact_id, {
    last_interaction: now(),
    last_channel: message.channel,
    conversation_outcome: determineOutcome(response)
  })
}
```

---

## Measuring Memory Effectiveness

### Quality Metrics

**Accuracy:**
- Memory correctness rate
- Wrong recall rate
- Verification frequency

**Coverage:**
- % of interactions with relevant memory
- Memory utilization rate
- Gap identification

### Experience Metrics

**Engagement:**
- Repeat question rate (lower = better)
- Customer satisfaction
- Conversation efficiency

**Business:**
- Conversion impact
- Support ticket reduction
- Relationship longevity

---

## Common Mistakes

### 1. No Memory
**Problem:** Every conversation starts fresh
**Fix:** Implement basic session and short-term memory

### 2. Too Much Memory
**Problem:** Overwhelming recall, creepy feeling
**Fix:** Selective, context-appropriate recall

### 3. Stale Memory
**Problem:** Referencing outdated information
**Fix:** Timestamp and refresh data

### 4. Wrong Memory
**Problem:** Mixing up customers, wrong facts
**Fix:** Verification, conflict resolution

### 5. Siloed Memory
**Problem:** Each channel has separate memory
**Fix:** Unified memory store

---

## Questions to Ask

If you need more context:
1. What channels does your bot operate across?
2. How long are your typical customer relationships?
3. What CRM/data systems do you use?
4. What do customers complain about repeating?
5. What privacy/compliance requirements apply?

---

## Related Skills

- **personalization-at-scale**: Using memory for personalization
- **multi-channel-coordination**: Memory across channels
- **data-enrichment-integration**: External data for memory
- **conversational-flow-management**: Context in conversations
