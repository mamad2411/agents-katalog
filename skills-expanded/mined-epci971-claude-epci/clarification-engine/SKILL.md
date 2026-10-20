---
name: epci:clarification-engine
description: >-
  Generates smart clarification questions based on context and requirement gaps.
  Uses progressive disclosure to avoid overwhelming users.
  Use when: analyzing vague requirements, identifying missing information,
  generating targeted questions, or cleaning up voice input.
  Internal component for EPCI v6.0.
user-invocable: false
allowed-tools: AskUserQuestion
---

# Clarification Engine

Internal component for smart clarification and gap analysis.

## Overview

Ask the right questions at the right time:
- Identify gaps in requirements
- Avoid unnecessary questions
- Progressive disclosure (max 3 at once)
- Context-aware suggestions with defaults

## API

| Function | Description | Input | Output |
|----------|-------------|-------|--------|
| `analyze_gaps(input)` | Find missing information | raw input | Gap list |
| `generate_questions(gaps)` | Create targeted questions | gaps[] | Question list |
| `prioritize(questions)` | Order by importance | questions[] | Sorted questions |
| `clean_voice_input(text)` | Clean dictation artifacts | raw text | Cleaned text |

## Question Categories

| Category | When Used | Example |
|----------|-----------|---------|
| `scope` | Unclear boundaries | "Should this work offline?" |
| `behavior` | Missing edge cases | "What happens on timeout?" |
| `technical` | Implementation choices | "Preferred auth method?" |
| `priority` | Feature ordering | "Must-have vs nice-to-have?" |
| `constraint` | Limitations unclear | "Performance requirements?" |

## Question Format

```json
{
  "category": "scope",
  "question": "Should this feature work offline?",
  "suggestions": [
    "Yes, full offline support",
    "No, online only",
    "Partial - cache last data"
  ],
  "importance": "high | medium | low",
  "default": "No, online only"
}
```

## Progressive Disclosure Rules

1. **Max 3 questions** per interaction
2. **Critical first** - block only on must-knows
3. **Smart defaults** - suggest most common choice
4. **Skip option** - allow "use defaults" path
5. **Defer non-critical** - ask during implementation if needed

## Usage

Invoked automatically by skills:

```
# Called by /brainstorm for iterative clarification
gaps = clarification.analyze_gaps(user_input)
questions = clarification.generate_questions(gaps)
# Returns: [{ question: "...", suggestions: [...], default: "..." }]

# Called by /spec for gap filling
clarification.prioritize(all_questions)
# Returns: top 3 questions sorted by importance

# Called by any skill for voice input cleaning
clarification.clean_voice_input(raw_dictation)
# Returns: cleaned, structured text
```

## Voice Input Cleaning

Handles common dictation artifacts:

| Input | Output |
|-------|--------|
| "uh like create a um button" | "create a button" |
| "period new line" | ".\n" |
| "quote hello quote" | '"hello"' |
| "comma space" | ", " |

## Integration with AskUserQuestion

Questions are formatted for Claude's tool:

```yaml
AskUserQuestion:
  questions:
    - question: "Should this work offline?"
      header: "Scope"
      options:
        - label: "Yes, full offline"
          description: "Cache all data locally"
        - label: "No, online only (Recommended)"
          description: "Simpler implementation"
```

## Limitations

This component does NOT:
- Store question history
- Learn from user preferences (see project-memory)
- Support multi-language questions
