---
name: multi-turn-conversation-design
version: 1.0.0
min_mindforge_version: 10.0.4
status: stable
triggers: multi-turn conversation, conversation state, context carryover, clarification strategy, conversation repair, intent disambiguation, dialogue management, turn-taking, conversation memory, slot filling, conversation flow, dialogue state tracking
---

# Skill — Multi-Turn Conversation Design (Dialogue State Management)

## When this skill activates
When designing conversational interfaces, building dialogue systems, implementing
multi-step user interactions, or troubleshooting conversation flow issues. Use for
chatbots, voice assistants, multi-step forms, or any interface where information
is gathered across multiple exchanges.

Core principle: **Continuity over repetition** — a well-designed conversation feels
like talking to someone with a good memory. Never re-ask what was already provided.
Never lose context between turns. Never make the user repeat themselves.

## Mandatory actions when this skill is active

### Dialogue State Tracking

1. **State schema (track at every turn):**
   ```json
   {
     "conversation_id": "uuid",
     "turn_number": 5,
     "current_intent": "book_flight",
     "confidence": 0.92,
     "slots": {
       "origin": {"value": "SFO", "confirmed": true, "source": "turn_2"},
       "destination": {"value": "JFK", "confirmed": true, "source": "turn_3"},
       "date": {"value": null, "confirmed": false, "source": null},
       "passengers": {"value": 1, "confirmed": false, "source": "assumed_default"}
     },
     "pending_clarifications": ["date"],
     "conversation_history": ["summary of prior turns"],
     "user_preferences": {"prefers_direct_flights": true}
   }
   ```

   Rules:
   - State is updated after EVERY turn (never stale)
   - Each slot tracks: value, whether confirmed by user, and which turn provided it
   - Assumed values are marked as unconfirmed (verify before critical actions)
   - History is summarized (not raw) to stay within context limits

### Context Carryover

2. **Explicit reference to prior context:**
   ```
   Good (references prior turn):
   "You mentioned you're flying from SFO. What date works for you?"

   Bad (no reference, feels disconnected):
   "What date would you like to fly?"

   Good (acknowledges what's known):
   "I have SFO to JFK for 1 passenger. I just need your travel date."

   Bad (re-asks known information):
   "Where are you flying from?"
   ```

   Rules:
   - Start responses by acknowledging what you already know
   - Reference specific prior statements: "Earlier you said X..."
   - Summarize collected information periodically (every 3-4 turns)
   - If context window is exhausted: summarize and explicitly note what's carried forward
   - Never assume context persists implicitly — make carryover visible

### Clarification Strategy

3. **When to clarify (confidence-based):**
   ```
   Confidence >= 0.9: Proceed without clarification
   Confidence 0.7-0.9: Proceed but confirm ("I'll book SFO to JFK — is that right?")
   Confidence 0.5-0.7: Ask targeted question with options
   Confidence < 0.5: Ask open-ended clarification

   Clarification types (from most to least specific):
   1. Binary confirmation: "Did you mean San Francisco?"
   2. Multiple choice: "Did you mean SFO, SJC, or OAK?"
   3. Constrained question: "Which airport in the Bay Area?"
   4. Open question: "Where are you flying from?" (last resort)
   ```

   Rules:
   - Always prefer more specific clarification formats (binary > choice > open)
   - Limit choices to 3-5 options maximum
   - Never ask two clarification questions in one turn (one at a time)
   - If user answers a different question than asked: accept the new info, don't force the original question
   - After 2 failed clarification attempts on same slot: offer to skip or use default

### Conversation Repair

4. **Detecting and recovering from misunderstanding:**
   ```
   Misunderstanding signals:
   - User contradicts a prior agent response
   - User repeats their question with different phrasing
   - User says "no", "that's not what I meant", "wrong"
   - User provides information that conflicts with current state

   Repair protocol:
   1. Acknowledge the misunderstanding explicitly
      "I misunderstood — let me correct that."
   2. State what you incorrectly assumed
      "I thought you meant [X], but you're saying [Y]."
   3. Update state with correct information
   4. Confirm the correction
      "Got it — [Y], not [X]. Is that right?"
   5. Continue from the corrected state
   ```

   Rules:
   - Never argue with the user about what they meant
   - Repair immediately (don't wait for the user to notice the error)
   - After repair: replay any downstream logic that depended on the wrong value
   - Track repair frequency (high repair rate = poor understanding, needs model improvement)

### Slot Filling

5. **Multi-turn information gathering:**
   ```
   Slot filling strategy:
   1. Identify all required slots for the current intent
   2. Check which are already filled (from prior turns or user profile)
   3. Ask for unfilled slots in natural priority order (most important first)
   4. One slot per turn (don't overwhelm)
   5. Allow user to provide multiple slots in one message (parse and fill all)
   6. Confirm all slots before executing action

   Example flow:
   Turn 1: User: "I want to book a flight"
           → Intent: book_flight, all slots empty
   Turn 2: Agent: "Where are you flying from?"
           → User: "SFO to JFK next Tuesday"
           → Fill: origin=SFO, destination=JFK, date=next_tuesday
   Turn 3: Agent: "SFO to JFK next Tuesday for 1 passenger. Shall I search?"
           → Confirm all slots, offer to proceed
   ```

   Rules:
   - Never re-ask a filled slot (check state first)
   - If user provides extra info: accept and fill (don't say "I didn't ask that yet")
   - Required slots must be confirmed before executing actions
   - Optional slots get defaults (stated explicitly: "I'll assume 1 passenger unless you say otherwise")

### Intent Disambiguation

6. **Handling ambiguous or multi-intent messages:**
   ```
   Single intent (clear):
   "Book me a flight to NYC" → book_flight

   Ambiguous intent (clarify):
   "I need to go to NYC" → travel? meeting? moving? → "Are you looking to book a flight?"

   Multi-intent (handle sequentially):
   "Book a flight and a hotel" → [book_flight, book_hotel]
   → "Let's start with the flight. Where are you flying from?"
   → Complete flight, then: "Now let's find you a hotel."
   ```

   Rules:
   - Handle one intent at a time (queue others, don't drop them)
   - When disambiguating: offer the most likely interpretation first
   - Track which intents are pending (never lose a queued intent)
   - If intents are independent: handle in order mentioned
   - If intents are dependent: handle the dependency first

### Conversation Flow Design

7. **Turn structure:**
   ```
   Every agent turn should contain:
   1. Acknowledgment: what you understood from the user's message
   2. Progress indicator: what's done, what remains
   3. Next action: what you need from the user OR what you're doing next

   Pattern:
   "[Acknowledge]. [Progress]. [Next step]."
   "Got it, SFO to JFK. I just need your travel date. When are you flying?"
   ```

   Rules:
   - Keep agent turns concise (2-3 sentences for information gathering)
   - Never end a turn without a clear next step (question, confirmation, or action)
   - Use progressive disclosure (don't dump all information at once)
   - Match formality to user's tone (mirror their communication style)

## Self-check before task completion

Before marking a task done when this skill was active:

- [ ] Is dialogue state tracked and updated every turn (intent, slots, confidence)?
- [ ] Does every agent response reference prior context (no disconnected turns)?
- [ ] Is clarification strategy confidence-based (specific at high confidence, open at low)?
- [ ] Is there a repair protocol for misunderstandings (acknowledge, correct, confirm)?
- [ ] Does slot filling never re-ask already-provided information?
- [ ] Are multi-intent messages handled sequentially (queued, not dropped)?
- [ ] Does every agent turn have: acknowledgment, progress, next step?
- [ ] Are assumed/default values explicitly stated and marked unconfirmed?
