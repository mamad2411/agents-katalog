# Copilot Instructions: Ai Usage Monitoring Dashboard
Description: Build a dashboard to monitor and analyze your AI token usage across different models (Codex, Claude, ChatGPT) to optimize workflows and improve productivity.

# AI Usage Monitoring Dashboard Skill

## Overview
Build a dashboard to track and analyze your AI token usage across different models. This helps you:
- Understand your AI usage patterns
- Identify productivity opportunities
- Compare model effectiveness
- Optimize delegated intelligence

Learn core concepts in [Core Concepts](references/core_concepts.md).

## Step-by-Step Workflow

1. **Set Up Data Collection**
   - For Codex: Use API usage endpoints
   - For Claude/ChatGPT: Implement log parsing or estimation (see [Practical Guide](references/practical_guide.md))

2. **Design Your Dashboard**
   - Choose key metrics (daily tokens, model split, task types)
   - Select visualization style (Tufte-style recommended)
   - Determine time scale (daily + weekly views)

3. **Build Initial Version**
   - Use provided [Code Examples](references/code_examples.md)
   - Start with basic token counts
   - Add model differentiation

4. **Add Advanced Features**
   - Top 10 usage days analysis
   - Same-day activity correlation
   - Token efficiency metrics

5. **Deploy and Iterate**
   - Set up daily auto-refresh
   - Review weekly for insights
   - Continuously add dimensions

## Best Practices

1. **Make It Personal**
   - Track activities you actually do
   - Note what worked/didn't each day

2. **Focus on Growth**
   - Use dashboard to identify underused capabilities
   - Challenge yourself to increase effective token usage

3. **Share Learnings**
   - Contribute insights to community
   - Learn from others' dashboards

## Common Pitfalls

1. **Vanity Metrics**
   - Don't just track total tokens - focus on what they achieved
   - Example: 800M tokens/day only matters if it created value

2. **Model Myopia**
   - Don't compare models without context
   - Example: Claude may use more tokens but produce better results

3. **Data Overload**
   - Start simple, then expand
   - Example: Begin with just Codex before adding other models

## Validation

1. **Sanity Check Estimates**
   - Compare manual calculations to dashboard
   - Spot check high-usage days

2. **Test Insights**
   - Implement one dashboard-inspired change weekly
   - Measure impact on productivity

3. **Peer Review**
   - Share dashboard with colleagues
   - Incorporate feedback

## Continuous Improvement

1. Weekly review sessions
2. Monthly feature additions
3. Quarterly complete redesigns to match evolving usage

## Reference Guides

### Code Examples

# Code Examples and Prompt Templates

## Basic Dashboard Prompt
```
Create a Tufte-style dashboard showing my AI token usage with:
1. GitHub-style bar chart at top showing daily token burn
2. Logarithmic Y-axis to handle large value ranges
3. Color-coded by model (Codex=blue, Claude=green, ChatGPT=purple)
4. Top 10 highest usage days called out with activity notes
5. Same-day usage correlation showing what tasks drove spikes
```

## Claude Usage Estimator Prompt
```
Analyze these Claude chat logs and estimate token usage:
[PASTE LOGS]

Consider:
- Average tokens per character is 0.25
- System messages add 15% overhead
- Long context windows multiply base count by 1.5

Provide:
1. Total estimated tokens
2. Confidence interval
3. Breakdown by conversation
```

## Deployment Script
```python
# Sample Python script to collect Codex usage via API
import openai
from datetime import datetime, timedelta

def get_daily_usage(days_back=30):
    usage = []
    for i in range(days_back):
        date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
        response = openai.Usage.retrieve(date=date)
        usage.append({
            'date': date,
            'tokens': response['usage']['total_tokens'],
            'model': 'codex'
        })
    return usage
```

### Core Concepts

# Core Concepts of AI Usage Monitoring

Token monitoring is the practice of tracking how many tokens you consume when using AI models like Codex, Claude, or ChatGPT. Tokens are the basic units of text that AI models process, and tracking them gives you insights into:

1. **Workflow Efficiency**: See which tasks consume the most tokens and optimize them
2. **Behavior Patterns**: Understand how your AI usage changes over time
3. **Model Comparison**: Compare effectiveness across different AI models
4. **Productivity Gains**: Correlate token usage with output quality

Key metrics to track:
- Daily token consumption
- Token usage by model (Codex vs Claude vs ChatGPT)
- Token usage by task type (research, coding, writing)
- Token efficiency (output quality per token)

Why it matters:
- Studies show higher token usage often correlates with better results
- Helps identify underutilized AI capabilities in your workflow
- Creates accountability for AI usage patterns
- Enables continuous improvement in delegated intelligence

### Practical Guide

# Practical Guide to Building Your Dashboard

## Data Collection Methods

1. **Direct API Access**: For Codex and other models with API access, pull usage data directly
2. **Log Analysis**: Parse chat logs and other artifacts to estimate usage
3. **Approximation**: For models without direct metrics (like Claude chat), use:
   - Character count divided by average tokens per character
   - Comparison with similar tasks in measurable models
   - AI-assisted estimation (have Codex analyze your Claude usage)

## Visualization Principles

Use Tufte-style minimalism for clarity:
- High data-to-ink ratio
- Clear labeling
- Logarithmic scales for wide-ranging data
- Color coding by model/task type

## Implementation Tips

1. Start simple with just token counts
2. Gradually add dimensions (model, task type, time of day)
3. Make it personal - track activities you actually do
4. Update daily for best insights

## Advanced Features
- Top 10 usage days analysis
- Same-day activity correlation
- Model comparison overlays
- Token burn rate alerts

### Sources

# Video Sources

The following curated videos were synthesized to create this skill:

1. **[My Codex Ran 800 Million Tokens in A Day. The Real Story Isn't Cost.](https://www.youtube.com/watch?v=l8BloTSLK6M)** by AI News & Strategy Daily | Nate B Jones