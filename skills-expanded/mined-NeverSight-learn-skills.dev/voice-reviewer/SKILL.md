---
name: voice-reviewer
version: 1.0.0
description: Review content files against a project's voice and style guidelines. Use when reviewing written content (MDX, markdown, copy) for tone, sentence structure, word choice, and bilingual policy compliance before committing. Triggers on "review voice", "check tone", "voice review", "content review", "does this match our voice", or after writing loop/ritual/article content.
user-invocable: false
---

# Voice Reviewer

Review content against the project's voice guidelines. This skill reads the project's voice guide and lint rules, then audits content files for violations.

## How It Works

1. **Find the voice guide**: Look for `docs/brand-voice-guidelines.md`, `.voice-lint.json`, or similar files in the project root.
2. **Read the rules**: Extract sentence limits, forbidden words, tone requirements, bilingual policies, and structural patterns.
3. **Audit the content**: Check each file against every rule.
4. **Report**: List violations with line numbers, the rule violated, and a suggested fix.

## What to Check

### Sentence Structure
- Maximum sentence length (word count per the guide, typically 20-30 words)
- One observation per sentence
- Prefer contractions
- Short to medium sentences

### Forbidden Patterns
- Superlatives (best, top, must-visit, amazing, incredible)
- Exclamation points
- Emojis
- Trend slang (hits different, no cap, lowkey, vibe check as a verb)
- Hashtag energy
- Adjective stacking (cozy, intimate, must-visit spot)
- Expert/authority claims (everyone knows, locals say, the best)

### Tone
- Observational over promotional
- Specific over vague
- Curious before confident
- Human, not performative
- "It felt like..." not "The best..."

### Bilingual Policy (if applicable)
- Check the EN:ES ratio target (e.g., 85:15 for loops, 95:5 for rituals)
- Spanish asides stay under the word limit (typically 6 words max)
- No full content repetition in Spanish
- No Spanish in H1/H2 headings

### Structural Patterns
- Arrival -> Detail -> Shift -> Release arc
- Show instead of tell
- At least one concrete sensory detail per section
- Could this paragraph exist in another city unchanged? (if yes, it needs rewriting)

## Output Format

```markdown
## Voice Review: [filename]

### Violations

1. **Line 23**: "This amazing, must-visit hidden gem is perfect for date night!"
   - **Rule**: No superlatives, no adjective stacking
   - **Fix**: "The place looks quiet until you sit down."

2. **Line 45**: Sentence is 31 words (max: 24)
   - **Rule**: Max sentence length
   - **Fix**: Split into two sentences.

3. **Line 67**: Spanish aside "entonces vamos a intentar algo nuevo juntos" (7 words)
   - **Rule**: Spanish asides max 6 words
   - **Fix**: Trim to "vamos a intentar algo nuevo" (5 words)

### Summary
- 3 violations found
- 0 critical (forbidden terms)
- 2 structural (sentence length, adjective stacking)
- 1 bilingual (Spanish aside too long)
```

## Agentic Workflow & Vibe Coding

- **Iterative Refinement:** Do not expect a perfect voice review on the first pass. Draft the initial review, check if it correctly applies the guidelines without being overly pedantic, isolate any specific misapplication of a rule, and refine the critique. Adjust one rule interpretation at a time.
- **Vibe Coding:** Commit your working review notes or proposed content changes locally before sending final feedback or attempting to rewrite large sections of the document.

## Usage as a Subagent

When dispatching as a subagent, provide:
1. The file(s) to review
2. The path to the voice guide
3. The path to `.voice-lint.json` (if it exists)

The reviewer should read the voice guide first, then audit each file independently.
