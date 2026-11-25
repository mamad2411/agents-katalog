---
name: ai-insight
description: Gain self-knowledge from vault data. Analyzes your notes across mindset, cognitive models, exploration frameworks, and key influences. Use when you want to understand yourself better, get a self-knowledge report, inner conflicts, values clarification, MBTI analysis, CBT/ACT insights, or /ai-insight.
---

# AI Insight Skill

Generates a comprehensive self-knowledge report by analyzing your Obsidian vault. Surfaces insights across four dimensions: Core Mindset, Cognitive Models, Exploration Frameworks, and Key Influences.

## Analysis Dimensions

### 1. Core Mindset and Analysis
- (a) Inner conflicts — recurring tensions and dilemmas
- (b) Values and what you see as valuable
- (c) MBTI analysis (inferential from writing patterns)
- (d) CBT and ACT therapy lenses
- (e) Positives every day — strengths and wins
- (f) Action guide — concrete next steps

### 2. Cognitive Models
- (a) Reverse thinking (Charlie Munger)
- (b) Second-order thinking
- (c) Anti-intuitive insights
- (d) Major contradictions (主要矛盾)
- (e) Value clarification (价值澄清)

### 3. Exploration Frameworks
- (a) The Soul Question
- (b) Mind Topic Extend
- (c) Resource digging
- (d) Blind spot exploration (盲区探索)
- (e) Friend's perspective (朋友视角)
- (f) Director's perspective (导演视角)
- (g) The question that occurs again and again

### 4. Key Influences and Figures
- (a) Charlie Munger — mental models, inversion
- (b) Aristotle — virtue ethics, phronesis
- (c) Seneca — Stoicism, memento mori
- (d) Tasha Eurich — self-awareness
- (e) Fuli Flywheel (复利飞轮) — compound growth

## Usage

```bash
# Full AI Insight report (default: 90 days)
python3 _scripts/ai_insight.py

# Focus on one dimension
python3 _scripts/ai_insight.py --focus mindset
python3 _scripts/ai_insight.py --focus cognitive
python3 _scripts/ai_insight.py --focus exploration
python3 _scripts/ai_insight.py --focus influences

# Deeper look (6 months)
python3 _scripts/ai_insight.py --days 180

# Exclude PARA (Projects/Areas/Resources)
python3 _scripts/ai_insight.py --no-para

# Print only, don't save
python3 _scripts/ai_insight.py --no-save

# Custom output path
python3 _scripts/ai_insight.py --output "Atlas/My Insight - 2026-02.md"
```

## Output

`Atlas/AI Insight - YYYY-MM-DD.md` — comprehensive self-knowledge report with:
- Evidence-based analysis citing [[wikilinks]] to source notes
- Actionable recommendations
- Constructive, empowering tone

## Notes

- Default lookback: 90 days (longer than concept extract for deeper self-knowledge)
- Collects from Sources, Atlas, Maps, Inbox, and PARA (Projects, Areas, Resources)
- Use `--focus` to emphasize one dimension when time or tokens are limited
- Synthesis notes (weekly, daily, self-reflection) are prioritized
