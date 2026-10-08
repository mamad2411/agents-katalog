---
name: meta-learning
description: Continuous learning and improvement system for paracle_meta. Use when you need to record feedback, track quality metrics, or improve generation templates over time.
license: Apache-2.0
compatibility: Python 3.10+
metadata:
  author: paracle-team
  version: "1.0.0"
  category: quality
  level: advanced
  display_name: "Meta Learning"
  tags:
    - learning
    - feedback
    - improvement
    - quality
    - metrics
  capabilities:
    - record-feedback
    - track-quality
    - evolve-templates
    - analyze-patterns
allowed-tools: Read Write Bash(python:*)
---

# Meta Learning Skill

## Overview

This skill enables continuous improvement of the paracle_meta generation system through feedback collection, quality tracking, and template evolution.

## When to Use

Use this skill when you need to:
- Record feedback on generated artifacts
- Track generation quality over time
- Improve templates based on patterns
- Analyze common generation issues

## Feedback Collection

### Recording Feedback

```python
from paracle_meta import MetaAgent

async with MetaAgent() as meta:
    # Generate an artifact
    result = await meta.generate_agent(
        name="TestAgent",
        description="A test agent"
    )

    # Record feedback
    await meta.record_feedback(
        artifact_id=result.id,
        rating=4,  # 1-5 scale
        feedback="Good structure, but needs more examples",
        tags=["documentation", "examples"]
    )
```

### Feedback Categories

- **Quality** (1-5): Overall generation quality
- **Accuracy** (1-5): How well it matches the request
- **Completeness** (1-5): Are all necessary parts included
- **Usability** (1-5): How easy is it to use the output

### Detailed Feedback

```python
await meta.record_feedback(
    artifact_id=result.id,
    ratings={
        "quality": 4,
        "accuracy": 5,
        "completeness": 3,
        "usability": 4
    },
    improvements=[
        "Add more edge case handling",
        "Include integration examples"
    ],
    issues=[
        "Missing error handling section"
    ]
)
```

## Quality Tracking

### View Generation Stats

```python
from paracle_meta import LearningEngine

engine = LearningEngine()

# Get overall stats
stats = await engine.get_stats()
print(f"Total generations: {stats.total}")
print(f"Average quality: {stats.avg_quality:.2f}")
print(f"Success rate: {stats.success_rate:.1%}")

# Stats by artifact type
agent_stats = await engine.get_stats(artifact_type="agent")
workflow_stats = await engine.get_stats(artifact_type="workflow")
```

### Quality Trends

```python
# Get quality over time
trends = await engine.get_quality_trends(
    period="7d",  # Last 7 days
    artifact_type="agent"
)

for day, score in trends.items():
    print(f"{day}: {score:.2f}")
```

## Template Evolution

### Automatic Improvement

The learning system automatically:
1. Identifies common patterns in high-rated generations
2. Detects recurring issues in low-rated ones
3. Updates templates to incorporate improvements

```python
# Trigger template evolution
evolution_result = await engine.evolve_templates(
    artifact_type="agent",
    min_samples=10,  # Minimum feedback samples needed
    threshold=0.8    # Quality threshold for pattern extraction
)

print(f"Templates updated: {len(evolution_result.updates)}")
for update in evolution_result.updates:
    print(f"  - {update.template}: {update.change}")
```

### Manual Template Updates

```python
from paracle_meta import TemplateLibrary

library = TemplateLibrary()

# Get current template
template = library.get("agent_generation")

# Update template
library.update(
    "agent_generation",
    additions=["Include error handling section"],
    removals=["Deprecated pattern X"]
)
```

## Best Practices Database

### Recording Best Practices

```python
from paracle_meta import BestPracticesDatabase

db = BestPracticesDatabase()

# Add a best practice
await db.add(
    category="agent_design",
    practice="Always include fallback behavior",
    rationale="Improves reliability in production",
    examples=["...", "..."],
    tags=["reliability", "production"]
)
```

### Querying Best Practices

```python
# Get practices for a category
practices = await db.get(category="agent_design")

# Search by tags
security_practices = await db.search(tags=["security"])

# Get recommendations for a generation
recommendations = await db.recommend(
    artifact_type="agent",
    context={"domain": "security", "complexity": "high"}
)
```

## Cost Tracking

### Monitor Generation Costs

```python
from paracle_meta import CostOptimizer

optimizer = CostOptimizer()

# Get cost summary
costs = await optimizer.get_costs(period="30d")
print(f"Total cost: ${costs.total:.2f}")
print(f"By provider:")
for provider, cost in costs.by_provider.items():
    print(f"  {provider}: ${cost:.2f}")
```

### Cost Optimization

```python
# Get optimization recommendations
recommendations = await optimizer.optimize()
for rec in recommendations:
    print(f"- {rec.suggestion}")
    print(f"  Potential savings: ${rec.savings:.2f}/month")
```

## CLI Integration

```bash
# View learning stats (future)
paracle meta stats

# Show quality trends
paracle meta trends --period=7d

# Evolve templates
paracle meta evolve --artifact=agent

# Export feedback data
paracle meta export-feedback --format=json
```

## Storage

Learning data is stored in:
- `.parac/memory/data/meta_learning.db` (SQLite)
- `.parac/memory/data/meta_costs.db` (cost tracking)
- `.parac/memory/data/best_practices.db` (best practices)
- `.parac/memory/data/meta_templates.db` (template versions)

## Related Skills

- [meta-generation](../meta-generation/): Generate artifacts
- [performance-optimization](../performance-optimization/): Optimize generation
- [technical-documentation](../technical-documentation/): Document improvements
