---
name: got-it
description: Schelling point coordination game where players converge on a shared word. Use when someone initiates the "got it" game, when managing active game state in Discord/Telegram channels, or when responding to "got it" messages during gameplay.
---

# Got It Game

A Schelling point coordination game where players attempt to converge on the same word through iterative guessing.

## Game Rules

1. **Starting**: Game begins when 2 players say "got it" in the channel
2. **Revealing**: Both players reveal a word (any word)
3. **Win Condition**: If words match → everyone wins, game ends
4. **Next Round**: If words differ → new round starts, wait for 2 new "got it" messages
5. **Convergence Strategy**: Each round, players choose a word "between" the previous two words, aiming to find a Schelling point where both players meet

## State Management

Game state is stored in `~/.openclaw/workspace/got-it-state.json`. See `references/state-schema.md` for full schema.

**Load state** at the start of every interaction to check if a game is active.

**Save state** after every state change (new "got it", reveal, round transition).

## Game Flow

### 1. Game Initiation

When someone says "got it" in a channel:

1. Load or create state file
2. Check if this is first "got it" of a round
3. If first: Record player and wait for second
4. If second: Transition to revealing state and prompt both players to reveal

**Response when first player says "got it":**
```
🎯 Got one! Waiting for one more to "got it"...
```

**Response when second player says "got it":**
```
🎯 Two players ready! @player1 and @player2, reveal your words!

Round {N} {context_if_not_first_round}
```

If not first round, include context:
```
Previous words: "{word1}" vs "{word2}"
Find the Schelling point between them!
```

### 2. Word Revelation

When a player who said "got it" posts a word:

1. Record their word in state
2. Wait for second player's word
3. When both revealed: Check if words match

**If words match:**
```
🎊 CONVERGENCE! Both said "{word}"!

Everyone wins! Game complete in {N} rounds.
🎯 {summary_of_journey}
```

**If words don't match:**
```
Round {N}: "{word1}" vs "{word2}"

🔄 New round! Who's got it?
```

### 3. Agent Participation

When participating as a player:

1. **Delay before "got it"**: Wait 5 seconds after detecting "waiting for got it" state before saying "got it" (give humans priority)
2. **Delay before reveal**: When in revealing state and agent is one of the two players, **wait for the other player to reveal their word first** before revealing. Do NOT reveal immediately after prompting players.
3. **Reveal Strategy**: When revealing, use Schelling point reasoning:
   - Round 1: Choose highly salient, universal concepts (e.g., "water", "love", "home")
   - Round 2+: Choose the most obvious conceptual midpoint between the two previous words
   - Prefer: Common nouns, concrete objects, basic emotions, universal experiences
   - Avoid: Obscure references, proper nouns, technical terms

### 4. State Cleanup

Delete state file when:
- Game completes (words match)
- 24+ hours since `lastActivity` (abandoned game)

## Schelling Point Strategy

**Round 1 (no previous words):**
Choose from highly salient universal concepts:
- Basic elements: water, fire, earth, air
- Universal emotions: love, fear, joy
- Basic needs: food, home, family
- Fundamental concepts: time, life, death

**Round 2+ (converging):**

Given previous words W1 and W2, choose the most obvious bridge concept:

Examples:
- "hot" & "cold" → "warm" or "temperature"
- "cat" & "dog" → "pet" or "animal"  
- "night" & "day" → "time" or "dusk"
- "love" & "hate" → "emotion" or "passion"

**Selection heuristics:**
1. Superordinate category (cat/dog → animal)
2. Midpoint on a spectrum (hot/cold → warm)
3. Common context (fork/knife → table, meal)
4. Obvious associations shared by both (sun/moon → sky, light)

**Avoid:**
- Obscure connections only you see
- Wordplay or puns (not universal)
- Abstract philosophy (too subjective)
- Multiple degrees of separation

## Message Detection

Detect "got it" by checking if message:
- Exactly matches "got it" (case-insensitive)
- Matches "got it" with punctuation: "got it!", "got it?"
- Variants: "Got it.", "GOT IT"

Do NOT match:
- "I got it working" (conversational usage)
- "You got it right" (different context)

Use exact phrase matching to avoid false positives.

## Example Gameplay

**Round 1:**
```
Alice: got it
Bot: 🎯 Got one! Waiting for one more...
Bob: got it
Bot: 🎯 Two players ready! @Alice and @Bob, reveal your words! Round 1
Alice: tree
Bob: water
Bot: Round 1: "tree" vs "water"
     🔄 New round! Who's got it?
```

**Round 2:**
```
Carol: got it
Alice: got it  
Bot: 🎯 Two players ready! @Carol and @Alice, reveal your words!
     Previous words: "tree" vs "water"
     Find the Schelling point between them!
Carol: nature
Alice: plant
Bot: Round 2: "nature" vs "plant"
     🔄 New round! Who's got it?
```

**Round 3:**
```
Bob: got it
Carol: got it
Bot: 🎯 Two players ready! @Bob and @Carol, reveal your words!
     Previous words: "nature" vs "plant"  
     Find the Schelling point between them!
Bob: nature
Carol: nature
Bot: 🎊 CONVERGENCE! Both said "nature"!
     
     Everyone wins! Game complete in 3 rounds.
     🎯 tree vs water → nature vs plant → NATURE!
```

## Error Handling

**Player reveals when not in revealing state:**
Ignore (might be regular conversation)

**Same player says "got it" twice in one round:**
Ignore duplicate, don't count twice

**Player who didn't say "got it" tries to reveal:**
Politely note only the two players can reveal this round

**Channel confusion (game in multiple channels):**
State includes `channelId` — only respond to game in the active channel
