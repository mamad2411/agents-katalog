---
name: deep-research
description: "Execute autonomous multi-step research using Google Gemini Deep Research Agent. Use for: market analysis, competitive landscaping, literature reviews, technical research, due diligence. Takes 2-10 minutes but produces detailed, cited reports. Costs $2-5 per task."
license: Apache-2.0
metadata:
  author: sanjay3290
  version: "2.0"
---

# Gemini Deep Research Skill

Run autonomous research tasks that plan, search, read, and synthesize information into comprehensive reports.

## Requirements

- Python 3.8+
- httpx: `pip install -r requirements.txt`
- GEMINI_API_KEY environment variable

## Setup

1. Get a Gemini API key from [Google AI Studio](https://aistudio.google.com/)
2. Set the environment variable:
   ```bash
   export GEMINI_API_KEY=your-api-key-here
   ```
   Or create a `.env` file in the skill directory.

## Usage

### Start a research task (async)
```bash
python3 scripts/research.py --query "Research the history of Kubernetes"
# Returns interaction_id immediately
```

### With structured output format
```bash
python3 scripts/research.py --query "Compare Python web frameworks" \
  --format "1. Executive Summary\n2. Comparison Table\n3. Recommendations"
```

### Check status of running research
```bash
python3 scripts/research.py --status <interaction_id>
# Returns: {"status": "running|completed|failed", "result": "...", ...}
```

### Continue from previous research
```bash
python3 scripts/research.py --query "Elaborate on point 2" --continue <interaction_id>
```

### List recent research
```bash
python3 scripts/research.py --list
```

## Output Formats

- **Default**: Human-readable markdown report
- **JSON** (`--json`): Structured data for programmatic use
- **Raw** (`--raw`): Unprocessed API response

## Cost & Time

| Metric | Value |
|--------|-------|
| Time | 2-10 minutes per task |
| Cost | $2-5 per task (varies by complexity) |
| Token usage | ~250k-900k input, ~60k-80k output |

## Best Use Cases

- Market analysis and competitive landscaping
- Technical literature reviews
- Due diligence research
- Historical research and timelines
- Comparative analysis (frameworks, products, technologies)

## Workflow

**Execute step-by-step (do NOT write polling loops):**

```
Step 1: Start research
→ python3 scripts/research.py --query "..." --json
→ Record the interaction_id from output

Step 2: Wait 30 seconds
→ sleep 30

Step 3: Check status
→ python3 scripts/research.py --status <interaction_id> --json

Step 4: Evaluate status:
→ If status == "completed": Output result to user
→ If status == "failed": Report error to user
→ If status == "running": Go back to Step 2
```

## Exit Codes

- **0**: Success
- **1**: Error (API error, config issue)
