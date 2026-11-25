# Agent Tutor Skill

A cognitive science-based AI tutor for [Claude Code](https://claude.ai/code) that won't let you fake understanding.

Implements a full teaching loop, concept-level mastery tracking with FSRS spaced repetition, learning profile diagnostics, zero-hint quizzes, and source-aware teaching from PDFs, docs, code, and URLs.

## Why This Exists

AI makes learning feel easy. That's the problem.

| Cognitive Trap | What Happens | How This Skill Fixes It |
|---|---|---|
| **Fluency Illusion** | Clear explanations feel like understanding | Forces you to explain back and apply |
| **Zero Retrieval Practice** | AI answers remove the need to remember | Tests recall before re-teaching |
| **No Desirable Difficulty** | AI removes productive struggle | Socratic method, transfer tests |
| **Forgetting Architecture** | Every conversation starts fresh | Persistent tracking + FSRS scheduling |

> Based on research by Roediger & Karpicke (retrieval practice), Robert Bjork (desirable difficulties), and Hermann Ebbinghaus (forgetting curve).

## Install

```bash
npx skills add Bhala-Srinivash/agent-tutor-skill
```

## Usage

```
/learn                    # Start a learning session
"teach me Kubernetes"     # Learn a specific topic
"quiz me on React hooks"  # Test your knowledge
"what's due for review"   # Check spaced repetition schedule
"learning dashboard"      # See progress overview
```

## How It Works

### Teaching Loop
Every concept follows: **Explain → Example → Check → Evaluate → Practice**

You can't say "I get it" without proving it. The tutor asks you to explain back, apply to new scenarios, and transfer to unfamiliar contexts.

### FSRS Spaced Repetition
Unlike fixed intervals (3→7→14→30→90 days), FSRS adapts per concept:
- Easy concepts get longer breaks faster
- Hard concepts get reviewed more often
- Intervals personalize based on your recall history

### Source-Aware Teaching
Point it at any source material:
- PDFs, docs, markdown files
- URLs and web pages
- Codebases and source code

It teaches FROM the material, not just from general knowledge.

### Persistent Tracking

```
~/.learn/
├── profile.md                     # Your learning preferences (global)
└── topics/
    ├── kubernetes/
    │   ├── knowledge-base.md      # Concept map + FSRS + session log
    │   └── concepts/
    │       ├── networking.md      # Per-area tracking
    │       └── storage.md
    └── react/
        └── ...
```

## Features

- **Learning profile diagnostic** — Identifies your learning style, analogy domain, confusion tolerance
- **Teaching loop** — Explain → Example → Check → Evaluate → Practice
- **Zero-hint quizzes** — 4-question rounds with plausible distractors
- **FSRS spaced repetition** — Adaptive intervals based on recall quality
- **Concept-level tracking** — Mastery badges (🟥🟨🟩🟦⬜) per concept
- **Error notes** — Tracks specific misconceptions for targeted re-teaching
- **Sequencing protocol** — Ensures prerequisites before advancing
- **Source-aware** — Reads PDFs, docs, URLs, and code to teach from
- **Multi-language** — All content in your detected language
- **Platform-agnostic** — Plain markdown files, works anywhere

## Credits

- **Pedagogical framework**: [Mia Kiraki](https://robotsatemyhomework.substack.com/p/the-ai-tutor-i-built-in-claude-that) — "The AI tutor I built in Claude that won't let you fake understanding" (ROBOTS ATE MY HOMEWORK, Feb 2026)
- **Concept tracking & quiz engine**: Inspired by [tutor-skills](https://github.com/RoundTable02/tutor-skills) by RoundTable02
- **Spaced repetition**: [FSRS algorithm](https://github.com/open-spaced-repetition) by open-spaced-repetition
- **Cognitive science**: Roediger & Karpicke, Robert Bjork, Hermann Ebbinghaus

## License

MIT
