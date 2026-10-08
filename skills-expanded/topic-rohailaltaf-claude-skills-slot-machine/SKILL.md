---
name: slot-machine
description: Surprise MVP generator - conceive a novel idea and build a polished MVP without spoiling the surprise
user-invocable: true
disable-model-invocation: true
allowed-tools: *
---

# Slot Machine

A surprise MVP generator that conceives a novel, niche idea and builds it from scratch. The user doesn't know what they're getting until it's done - like pulling a slot machine lever and seeing what comes out.

## When to Use

- User invokes `/slot-machine`
- User asks you to "surprise me with an app"
- User wants you to build something novel without specifying what

## Core Principles

### The Surprise Element
- **Never reveal the idea upfront** - The user should discover what you built only after it's complete
- **No spoilers during development** - Keep commit messages, file names, and progress updates vague
- **Build the suspense** - Use playful, mysterious language while coding

### Idea Selection

Ultrathink. Use the current timestamp (seconds) as a random seed throughout this process.

1. This can either be a web app or a cool interactive visual experience. 

2. List 50 industries/niches - but make them specific, not generic. Not "healthcare" but "traveling nurses" or "pediatric dentists." Not "education" but "homeschool parents" or "ESL tutors."

3. Use your timestamp seed to pick ONE. Don't pick what feels "best" - use the randomness.

4. List 20 problems people in that niche face. Be specific to their daily reality.

5. Use your timestamp seed again to pick ONE problem. Not the most obvious one - the random one.

6. Design a solution. The app should be something people would pay for.

7. Consider the vast spectrum of human experience. Lots of niches out there. 

**Forced variety rules:**
- If the idea feels "safe" or "obvious" → re-roll
- Prefer weird, specific niches over broad ones
- It's okay to consider unglamourous industries equally as well


### Technical Constraints

**Use web technologies only:**
- Next.js, React, Node.js, P5 (if needed)
- Tailwind CSS for styling
- SQLite if persistence is needed (via better-sqlite3 or similar)

**Keep it simple:**
- No authentication required
- No external API keys needed (or use free, no-signup APIs)
- No caching layers, logging frameworks, or infrastructure complexity
- No native dependencies that require Xcode, build tools, etc.
- **No real payment infrastructure** - Use placeholder buttons/modals for pricing and checkout (e.g., "Coming soon" or mock upgrade flows). The user can ask you to implement real payments later if they pursue the idea.

**Polish the UX:**
- The interface should feel complete and intentional
- Smooth interactions, good visual design
- Mobile-responsive if applicable
- Clear affordances - user should know how to use it immediately

## Process

### 1. Spin the Wheel
Internally conceive a novel idea. Do NOT share this with the user. Simply announce:

> "Spinning the slot machine... I've got something fun in mind. Let me build it for you."

### 2. Build in Stealth Mode
Create the MVP while keeping the mystery alive:
- Use vague progress updates: "Setting up the foundation...", "Adding the magic...", "Polishing the experience..."
- Keep file and folder names non-descriptive if possible, or use the project name generically
- Don't describe features as you build them

### 3. The Reveal
Once complete, unveil what you built:
- Give it a proper name
- Explain what it does and why it's interesting
- Show the user how to run it

### 4. Launch Offer
Ask the user if they'd like you to run the app for them, or provide clear instructions:

```
npm install
npm run dev
```

Then open the provided localhost URL.

## Example Flow

**User:** `/slot-machine`

**Assistant:** "Spinning the slot machine... I've got something in mind. Let me build it."

*[Creates project, builds features with vague updates]*

"Setting up the foundation..."
"Adding the core experience..."
"Making it feel right..."
"Final touches..."

**Assistant:** "Done! I built you **[Name]** - [one sentence hook explaining what it does and why it's interesting].

Would you like me to run it for you?

To run manually:
```
cd [project-name]
npm install
npm run dev
```
Then open http://localhost:3000"

## What NOT to Do

- Don't ask the user what they want - the surprise IS the point
- Don't reveal the idea before it's built
- Don't require complex setup or external tools
- Don't leave the MVP feeling unfinished or rough
- Don't implement real payment infrastructure (Stripe, etc.) - use tasteful placeholders
- Don't use placeholder content for the core experience - only for payment flows
