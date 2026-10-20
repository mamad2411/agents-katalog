---
name: voice-architect
description: >
  This skill should be used when the user asks to "build a voice profile,"
  "extract [person]'s voice," "create a voice file," "how does [person] write,"
  "do the voice interview," "voice architect for [name]," "import a voice profile,"
  or any request to capture an author's authentic writing voice through structured
  interview. Also trigger when the editorial-forge skill reaches Phase 3 (voice
  extraction). This skill works for ANY author — it extracts voice from the human
  through interview, never applies a preset voice. The resulting voice profile
  is per-project but can be imported into other projects via drag-and-drop.
version: 0.1.0
---

# Voice Architect

Build an author's voice profile through structured interview. The profile captures how they argue, their sentence rhythm, vocabulary, emotional patterns, and what they'd never say — everything needed to generate prose that sounds like THEM, not like AI.

## Core Principle

Voice is not style. Style is mechanics (sentence length, punctuation, word choice). Voice is the person — their origin story, their patterns of thought, how they fight, what they refuse to say. This interview extracts both.

## The Interview: 8 Questions

Ask ONE question at a time. Wait for the full answer before proceeding. These questions may take hours or days to answer — save state after each.

### Question 1: Origin Story
"How did you come to this work? Not your resume — the moment you knew this was your thing."

**What to extract**: The emotional entry point. Where conviction comes from. Whether they lead with stories or credentials.

### Question 2: The Pattern
"What do you see that others miss? What pattern have you noticed over years that most people in your field haven't caught yet?"

**What to extract**: Intellectual signature. How they synthesize. Whether they think in systems, narratives, or data.

### Question 3: How You Argue
"When you're making a case to someone who disagrees, how do you do it? Stories first? Data first? Do you get loud or get quiet?"

**What to extract**: Argument structure. Rhetorical instincts. Whether they're deductive, narrative, Socratic, or confrontational.

### Question 4: What You Hate
"What's the thing in your field that makes you genuinely angry? The practice, the phrase, the mindset that you'd burn if you could?"

**What to extract**: Emotional triggers. Where conviction turns to heat. The forbidden territory they patrol.

### Question 5: How You Explain
"Pick something complex in your domain. Explain it to me like I'm smart but from a different field."

**What to extract**: Teaching style. Metaphor preferences. How they simplify without dumbing down. Technical vocabulary comfort.

### Question 6: Your Reader
"When you picture someone reading your work and thinking 'they get it' — who is that person and what specifically did you say that landed?"

**What to extract**: Who they write FOR. What "landing" feels like to them. Their theory of impact.

### Question 7: The Line You Won't Cross
"What's the popular advice in your space that you refuse to give? Why?"

**What to extract**: Intellectual boundaries. Where they diverge from consensus. The contrarian positions they hold with conviction.

### Question 8: Your Natural Register
"Do you write like you talk? More formal? Less? What's the closest published thing to how you actually sound?"

**What to extract**: Self-awareness about register. The gap (or lack of gap) between spoken and written voice. Reference points for calibration.

## After the Interview

### Analysis

After all 8 answers are collected, analyze for:

1. **Argument style**: Deductive (premise → conclusion), Narrative (story → insight), Socratic (question → discovery), Confrontational (challenge → proof), or hybrid
2. **Sentence rhythm**: Short and punchy? Long and layered? Alternating? Fragments for emphasis?
3. **Vocabulary register**: Technical depth, jargon comfort, metaphor density
4. **Emotional patterns**: Where they get heated, where they pull back, what triggers conviction vs. caution
5. **Teaching mode**: Analogies? Step-by-step? Examples first? Theory first?
6. **Forbidden territory**: Phrases, structures, tones that would never come from this person

### Voice Profile Generation

Generate the voice profile document:

```markdown
# Voice Profile: [Author Name]
## Created: [date]
## Last validated: [date]
## Project: [project name]

### How They Argue
[Analysis of argument style with examples from interview answers]

### Sentence Rhythm
[Observed patterns: length, variation, fragment usage, paragraph style]

### Vocabulary & Register
[Technical depth, jargon comfort, metaphor preferences, words they use vs. avoid]

### Emotional Patterns
[Where they get heated, where they pull back, what triggers conviction]

### Teaching Mode
[How they explain complex things, metaphor style, simplification approach]

### Forbidden Patterns
[Phrases, structures, or tones that would never come from this author]
[Include specific examples: "This author would never say 'It's worth noting that...'"]

### "Sounds Like Me" Samples
[3-5 short passages the author confirmed as authentic to their voice]
[Drawn from interview answers — the parts where they were most themselves]

### Anti-Detection Markers
[Specific checklist items calibrated to THIS author's natural style]
- [ ] Contraction rate: [X]% (based on observed patterns)
- [ ] Sentence length range: [X]-[Y] words typical
- [ ] Fragment usage: [frequency and purpose]
- [ ] Paragraph length: [typical range]
- [ ] Technical vocabulary depth: [level]
- [ ] Emotional vocabulary: [patterns]
- [ ] Conjunction starters: [frequency]
- [ ] Metaphor density: [low/medium/high]
```

### Validation

Present the voice profile to the author: "Does this sound like you? What's wrong? What's missing?"

Iterate until the author confirms. Log each iteration in the authorship record.

## Importing Voice Profiles

When a voice profile file is found in a project's `voice-profiles/` directory that wasn't created during this project's interview:

1. Detect the import (file exists but no corresponding `voice_interview_answer` decisions in the authorship record)
2. Ask: "I found an existing voice profile for [name]. Use it as-is, or re-interview to update?"
3. If as-is: Log a `voice_profile_imported` decision in the authorship record
4. If re-interview: Run the full 8-question interview, noting where answers diverge from the imported profile
5. Either way, validate the profile against the current project's content type

## State Persistence

After each interview answer:
1. Write the answer to `voice-profiles/[author-name]-raw-qa.md`
2. Log a `voice_interview_answer` decision in the authorship record
3. Update the manifest: `pending_question` with the next question and context
4. Update `progress.voice_profile` to `in_progress`

After profile generation and validation:
1. Write the profile to `voice-profiles/[author-name].md`
2. Log `voice_profile_generated` and `voice_profile_validated`
3. Update `progress.voice_profile` to `complete`
4. Clear `pending_question`

## What Voice Architect Does NOT Do

- Does not apply any preset voice (MoxyWolf, brand guidelines, etc.) unless the author explicitly requests it
- Does not generate prose — it only builds the profile. Prose generation happens in Editorial Forge Phase 4.
- Does not skip questions or batch them. Each question builds on previous answers.
- Does not assume voice is static. If an author's voice evolves, re-interview and update the profile.
