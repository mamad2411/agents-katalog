---
name: sessionstellar
description: Score AI orchestration sessions — extract signals, compute a 0-100 score across skill diversity, decision depth, error recovery, compound learning, and orchestration mastery. Works fully offline, no API key required.
user-invocable: true
homepage: https://sessionstellar.com
metadata: {"openclaw": {"emoji": "⭐", "requires": {"anyBins": ["npx", "node"]}, "install": {"npm": "sessionstellar", "manual": "npm install -g sessionstellar"}, "os": ["darwin", "linux"], "homepage": "https://sessionstellar.com"}}
---

# SessionStellar

Score AI orchestration sessions from any MCP client. Fully offline — zero API keys, zero network calls.

## When to use

Invoke this skill when the user wants to:
- Score a session transcript (.md, .txt, or .jsonl)
- Understand where their AI orchestration is weakest
- Compare scores across sessions
- Enable automatic scoring after every git commit

## How to score a file

```bash
npx sessionstellar score <path-to-session-file>
```

Returns a structured score:

```
┌─────────────────────────────────────────┐
│  SessionStellar Score                   │
│  overall: 74 / 100                      │
├─────────────────────────────────────────┤
│  Skill Diversity        ████████░░  82  │
│  Decision Depth         ███████░░░  71  │
│  Error Recovery         ████████░░  80  │
│  Compound Learning      ██████░░░░  63  │
│  Orchestration Mastery  ███████░░░  70  │
├─────────────────────────────────────────┤
│  skills: 12  agents: 4  decisions: 7   │
└─────────────────────────────────────────┘
```

## How to score from stdin (pipe)

```bash
cat session.md | npx sessionstellar score -
```

## Get JSON output

```bash
npx sessionstellar score session.md --json
```

Output:
```json
{
  "sessionId": "...",
  "overallScore": 74,
  "metrics": {
    "skillDiversity": 82,
    "decisionDepth": 71,
    "errorRecoveryRate": 80,
    "compoundLearningSignals": 63,
    "orchestrationMastery": 70
  },
  "signals": {
    "skillsInvoked": [...],
    "agentsSpawned": [...],
    "decisionPoints": [...],
    "errorRecoveries": [...],
    "learningMoments": [...]
  }
}
```

## Enable auto-scoring on every git commit

```bash
npx sessionstellar enable
```

Installs a post-commit hook that automatically scores any session file touched in each commit. Scores are saved to `.sessionstellar/scores/` (gitignored).

```bash
npx sessionstellar status    # show hook status + recent scores
npx sessionstellar disable   # remove the hook
```

## Scoring breakdown

| Metric | Weight | What it measures |
|--------|--------|-----------------|
| Skill Diversity | 20% | Variety of skills invoked |
| Decision Depth | 25% | Quality of branching decisions |
| Error Recovery | 20% | How well errors were handled |
| Compound Learning | 20% | Learning moments and adaptations |
| Orchestration Mastery | 15% | Multi-agent and sub-task coordination |

## Upload to leaderboard (optional)

```bash
npx sessionstellar score session.md
# Prompts: "Upload to leaderboard? (y/N)"
```

Public leaderboard: https://sessionstellar.com/leaderboard

Skip upload prompt:
```bash
npx sessionstellar score session.md --no-upload
```
