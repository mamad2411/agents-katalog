# Neo4j Agent Memory

Automatically use the tools for Neo4j Agent Memory Service to store messages and retrieve information from prior (relevant) conversations. Every user message and every assistant response should be persisted, and every new conversation should begin with a search for relevant prior context.

## Conversation Lifecycle

### Step 1 - Create a conversation (once, at conversation start)

At the start of every conversation, create a session:

```
memory_create_conversation(user_id="<user_id or empty>")
→ returns conversation_id (a UUID)
```

Keep this `conversation_id` consistent for every tool call throughout the conversation - never create a new one mid-conversation.

If you know the user's name or identifier, pass it as `user_id`. If not, omit it and update later if the user introduces themselves.

### Step 2 - Search memory before your first response

Before responding to the user's first message, search for relevant past context:

```
memory_search_entities(query=<user's first message or key terms>)
```

Use what you find to inform your response naturally - don't announce that you searched. If relevant past context surfaces, weave it in as you would with your own memory.

### Step 3 - Store the first message

Immediately after your memory search, store the user's first message to anchor the conversation:

```
memory_add_messages(
  conversation_id=<conversation_id>,
  messages=[{role: "user", content: <user's first message>}]
)
```

This links the message to the conversation node in Neo4j and triggers async entity extraction.

### Step 4 - Store every exchange throughout the conversation

After each exchange, store both turns together:

```
memory_add_messages(
  conversation_id=<conversation_id>,
  messages=[
    {role: "user", content: <message>},
    {role: "assistant", content: <your response>}
  ]
)
```

Message storage automatically extracts entities and generates embeddings - no extra steps needed.

### Step 5 - Store entities and facts as they arise

When a clear entity (person, organization, location, object, event) is stated or strongly implied, store it:

```
memory_add_entity(name=<entity name>, type=<type>, description=<description>)
```

Types: `person`, `organization`, `location`, `concept`, `tool`, `custom`.

Keep entities atomic - one entity per call.

### Step 6 - Look up entities when they're mentioned

Whenever a person, organization, location, object, or event comes up, check existing knowledge before responding:

```
memory_search_entities(query=<name>, type=<type>)
```

If results are found and you need more detail:

```
memory_get_entity(entity_id=<id from search results>)
```

To see all conversations where an entity has appeared:

```
memory_get_entity_history(entity_id=<id>)
```

Use what you find to give a richer, more contextual response. If nothing is found, respond normally - don't mention the lookup.

### Step 7 - Record reasoning traces after complex tasks

When you complete something that involved multiple steps or tools, record it:

```
memory_record_step(
  conversation_id=<conversation_id>,
  reasoning=<your reasoning process>,
  action_taken=<what you decided to do>,
  result=<outcome>
)
→ returns step_id
```

For each tool you invoked during that reasoning:

```
memory_record_tool_call(
  step_id=<step_id>,
  tool_name=<name>,
  input=<parameters>,
  output=<result>,
  status="completed",
  duration_ms=<time>
)
```

To retrieve full reasoning traces later:

```
memory_get_trace(conversation_id=<conversation_id>)
memory_explain_decision(step_id=<step_id>)
```

## Resuming a Known Session

If the user references a past conversation and you have a conversation_id, retrieve that history:

```
memory_get_context(conversation_id=<known_id>)
```

This returns the three-tier context: reflections (high-level insights), observations (compressed summaries), and recent messages.

If no conversation_id is available but the user references past context, search entities:

```
memory_search_entities(query=<what they're referencing>)
```

## What Is Worth Storing

Apply the same judgment you would with your own memory - not everything needs to be stored.

**Always store:**
- User's name, role, and goals (as entities)
- Decisions made and their rationale
- Facts the user states about themselves, their work, or their domain
- Any entity (person, org, place, object, event) discussed in meaningful context
- Outcomes of complex tasks (as reasoning traces)

**Use judgment:**
- Casual small talk - only if it reveals something meaningful about the user
- Corrections the user makes - always worth storing as an entity or fact
- Intermediate reasoning steps - only if the approach is novel or reusable

**Don't store:**
- Greetings, filler, pleasantries
- Information the user is clearly just passing through, not asserting
- Duplicates of information already in memory

## Tone and Transparency

- **Work silently** - don't narrate memory operations ("I'm now searching your memory…")
- **Surface naturally** - use retrieved context the way you'd use your own recollection
- **Acknowledge when relevant** - if past context is materially shaping your response, briefly mentioning it is fine: "Based on what you told me before about X…"
- **Never confabulate** - if memory returns nothing, say so honestly if the user asks; don't invent recollections

## Entity Types (POLE+O)

| Type | Subtypes | Examples |
|---|---|---|
| `person` | individual, suspect, witness, victim, officer | People, personas |
| `organization` | company, ngo, government, criminal | Companies, agencies |
| `location` | address, city, country, premise, virtual | Places, addresses |
| `object` | vehicle, phone, document, device, weapon | Physical and digital items |
| `event` | meeting, transaction, incident, communication | Incidents, meetings |

## Tool Reference

| Tool | Purpose |
|---|---|
| `memory_create_conversation` | Start a new session, returns conversation_id |
| `memory_add_messages` | Add messages to a conversation in bulk (triggers entity extraction) |
| `memory_get_context` | Get reflections + observations + recent messages |
| `memory_search_messages` | Semantic search within a conversation |
| `memory_search_entities` | Search entities across all conversations |
| `memory_get_entity` | Get entity details and relationships |
| `memory_add_entity` | Store a new entity |
| `memory_get_entity_history` | Cross-conversation history for an entity |
| `memory_record_step` | Record a reasoning step |
| `memory_record_tool_call` | Record a tool invocation within a step |
| `memory_get_trace` | Get full reasoning trace for a conversation |
| `memory_explain_decision` | Explain a specific reasoning step |
