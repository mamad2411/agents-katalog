# Copilot Instructions: Building Live Artifacts With Claude
Description: This skill enables you to create personalized dashboards with live data pulled from multiple software sources using Claude's live artifacts feature. It covers setup, best practices, pitfalls, and validation steps.

## Overview
Live artifacts in Claude allow you to build personalized dashboards that pull live data from multiple software sources. These dashboards automatically refresh with up-to-date data and can provide AI-driven insights. This skill will guide you through the process of creating these dashboards, avoiding common pitfalls, and validating their effectiveness.

## Step-by-Step Workflow
1. **Define the Purpose of Your Dashboard**: Clearly articulate what you want the dashboard to achieve. For example, a marketing dashboard might track conversions across different offers.
2. **Identify Data Sources**: Determine which software connectors (e.g., YouTube, Bitly, Posthog) you need to pull data from.
3. **Specify Data Requirements**: Define what specific data you need from each connector to avoid unnecessary scope creep.
4. **Set AI Interpretation Rules**: Decide how AI should interpret the data, such as providing strategic insights or prioritizing tasks.
5. **Build the Artifact**: Use Claude's built-in tool to create the live artifact by describing your requirements and connecting the necessary data sources.
6. **Test and Validate**: Ensure the dashboard updates correctly and provides the expected insights.

## Code/Prompt Templates
```markdown
**Prompt Template for Building a Live Artifact**
1. What is the purpose of this dashboard?
2. Which connectors should pull data?
3. What specific data do you need from each connector?
4. How should AI interpret the data?
5. What brand guidelines should it follow?
6. What actions should the artifact take?
7. What should this dashboard not do?
```

## Best Practices
- **Scope Narrowly**: Focus on specific use cases to avoid creating overly broad and slow dashboards.
- **Clear Communication**: Clearly communicate your requirements to Claude to avoid hard-coded dashboards that are not useful.
- **Regular Updates**: Ensure the dashboard refreshes regularly to provide up-to-date insights.

## Common Pitfalls
- **Overloading Data**: Pulling data from too many connectors can slow down the dashboard.
- **Unclear Requirements**: Failing to clearly define what you need can result in a dashboard that doesn't meet your needs.
- **Ignoring AI Interpretation**: Not setting rules for AI interpretation can lead to less useful insights.

## Validation Steps
1. **Check Data Accuracy**: Ensure the data pulled from each connector is accurate and up-to-date.
2. **Test AI Insights**: Verify that the AI provides meaningful and actionable insights.
3. **Monitor Performance**: Ensure the dashboard performs well and refreshes quickly.

For more detailed guidance, refer to the [Core Concepts](references/core_concepts.md), [Practical Guide](references/practical_guide.md), and [Code Examples](references/code_examples.md).

## Reference Guides

### Code Examples

## Code Examples
Here are some concrete examples of prompts and code snippets to help you build live artifacts with Claude.

### Prompt Template
```markdown
**Prompt Template for Building a Live Artifact**
1. What is the purpose of this dashboard?
2. Which connectors should pull data?
3. What specific data do you need from each connector?
4. How should AI interpret the data?
5. What brand guidelines should it follow?
6. What actions should the artifact take?
7. What should this dashboard not do?
```

### Example Prompt
```markdown
**Example Prompt for a Marketing Dashboard**
1. Purpose: Track conversions across different offers.
2. Connectors: YouTube, Bitly, Posthog.
3. Data: Conversions based on YouTube videos for three main offers.
4. AI Interpretation: Provide insights on which offers are performing best.
5. Brand Guidelines: Use company colors and logo.
6. Actions: None.
7. What Not to Do: Do not include data from unrelated campaigns.
```

### Example Code
```markdown
**Example Code for Building a Live Artifact**
1. Describe the purpose of the dashboard.
2. List the connectors and data requirements.
3. Define AI interpretation rules.
4. Specify brand guidelines.
5. Outline any actions the artifact should take.
6. Define what the dashboard should not do.
```

For more detailed guidance on core concepts and practical applications, refer to the [Core Concepts](references/core_concepts.md) and [Practical Guide](references/practical_guide.md).

### Core Concepts

## Core Concepts
Live artifacts in Claude are a powerful feature that allows you to create personalized dashboards that pull live data from multiple software sources. These dashboards automatically refresh with up-to-date data and can provide AI-driven insights. The key advantage of live artifacts is that you only need to build the dashboard once, and it will continuously update with fresh data.

### Key Features
- **Automatic Refresh**: Dashboards update automatically whenever opened or refreshed.
- **Multiple Connectors**: Pull data from various software sources into a single dashboard.
- **AI Insights**: AI interprets the data to provide strategic insights and prioritize tasks.

### Use Cases
- **Marketing Dashboards**: Track conversions across different offers.
- **Business Intelligence**: Monitor key business metrics and get strategic insights.
- **Sales Dashboards**: Track proposals and deals in your CRM.

For more detailed examples and practical applications, refer to the [Practical Guide](references/practical_guide.md).

### Practical Guide

## Practical Guide
Creating effective live artifacts with Claude involves several steps and best practices to ensure your dashboards are useful and efficient.

### Step-by-Step Instructions
1. **Define the Purpose**: Clearly articulate what you want the dashboard to achieve.
2. **Identify Data Sources**: Determine which software connectors you need to pull data from.
3. **Specify Data Requirements**: Define what specific data you need from each connector.
4. **Set AI Interpretation Rules**: Decide how AI should interpret the data.
5. **Build the Artifact**: Use Claude's built-in tool to create the live artifact.
6. **Test and Validate**: Ensure the dashboard updates correctly and provides the expected insights.

### Best Practices
- **Scope Narrowly**: Focus on specific use cases to avoid creating overly broad and slow dashboards.
- **Clear Communication**: Clearly communicate your requirements to Claude.
- **Regular Updates**: Ensure the dashboard refreshes regularly to provide up-to-date insights.

### Common Pitfalls
- **Overloading Data**: Pulling data from too many connectors can slow down the dashboard.
- **Unclear Requirements**: Failing to clearly define what you need can result in a dashboard that doesn't meet your needs.
- **Ignoring AI Interpretation**: Not setting rules for AI interpretation can lead to less useful insights.

For more detailed code examples, refer to the [Code Examples](references/code_examples.md).

### Sources

# Video Sources

The following curated videos were synthesized to create this skill:

1. **[Live Artifacts Just 10x'd Claude Cowork (Real Use Cases)](https://www.youtube.com/watch?v=PwLqKIGA25c)** by Ben AI