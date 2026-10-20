# Copilot Instructions: Ai Agent Workflow Automation With Google Gemini
Description: Implement autonomous AI agents using Google Gemini's Spark feature to automate multi-step workflows, handle multimodal inputs, and execute scheduled tasks.

# AI Agent Workflow Automation with Google Gemini

## Overview
This skill enables you to implement autonomous AI agents using Google Gemini's Spark feature. These agents can handle complex workflows by breaking them into parallelizable sub-tasks, process multimodal inputs through the Omni model, and execute scheduled actions via heartbeats. Key capabilities include:
- Autonomous task execution with sub-agent coordination
- Multimodal (text+image+video) processing and generation
- Context-aware desktop integration with speech filtering
- Recurring task automation

For foundational concepts, see [Core Concepts](references/core_concepts.md).

## Step-by-Step Workflow
1. **Agent Initialization**
   - Access Spark through the Gemini app's beta features
   - Define your primary task objective (e.g., "Prepare my daily work briefing")
   - Specify whether the task should recur (set heartbeat parameters)

2. **Task Decomposition**
   - Let the agent automatically determine sub-tasks or manually specify them
   - Example for daily briefing:
     1. Check calendar appointments
     2. Scan unread emails
     3. Review task list
     4. Compile weather/commute info

3. **Multimodal Processing**
   - When working with mixed media:
     1. Upload all source files
     2. Provide clear instructions for how to combine them
     3. Specify output format requirements
   - Detailed examples in [Code Examples](references/code_examples.md)

4. **Execution Monitoring**
   - Review the agent's proposed action plan before execution
   - Monitor initial runs to verify:
     - All sub-tasks are completed
     - Output quality meets expectations
     - Timing aligns with requirements

5. **Optimization**
   - Refine prompts based on initial results
   - Add conditional logic where needed
   - Adjust scheduling as necessary

## Best Practices
1. **Prompt Design**
   - Be specific about desired outcomes
   - Include examples when possible
   - For complex tasks, break instructions into logical sections

2. **Error Handling**
   - Anticipate common failure points:
     - Missing context
     - Ambiguous instructions
     - Media format incompatibilities
   - Build in verification steps for critical tasks

3. **Security**
   - Limit agent access to sensitive data
   - Review actions before execution in high-stakes scenarios
   - More implementation guidance in [Practical Guide](references/practical_guide.md)

## Common Pitfalls
1. **Overly Broad Tasks**
   - Bad: "Manage my entire workday"
   - Good: "Prepare a prioritized task list based on today's calendar"

2. **Ignoring Context Limits**
   - Agents may lose track in very long conversations
   - Solution: Break extremely complex workflows into separate agent instances

3. **Scheduling Conflicts**
   - Heartbeats may overlap with system maintenance
   - Solution: Stagger execution times for multiple agents

## Validation Steps
1. **Functional Testing**
   - Verify all sub-tasks complete successfully
   - Check output quality against requirements

2. **Performance Testing**
   - Measure execution time for time-sensitive workflows
   - Test with peak loads (e.g., processing many emails)

3. **User Acceptance**
   - Have end-users review outputs
   - Adjust based on feedback

## Implementation Example
```python
# Sample workflow for content creation agent
content_agent = {
    "trigger": "when new blog topic requested",
    "steps": [
        "Research trending subtopics",
        "Draft outline with 3 main sections",
        "Generate 2 supporting images per section",
        "Compile into Google Doc with headers"
    ],
    "output": {
        "format": "Google Doc",
        "review_required": True
    }
}
```
For complete code templates, see [Code Examples](references/code_examples.md).

## Reference Guides

### Code Examples

# Code and Prompt Examples for Gemini Agents

## Basic Spark Agent Initialization
```python
# Example API call to initialize a Spark agent
def create_spark_agent(task_description, schedule=None):
    agent_config = {
        "task": task_description,
        "subtasks": "auto",  # Allow agent to determine subtasks
        "output_format": "concise_report",
    }
    if schedule:
        agent_config["schedule"] = {
            "frequency": schedule["frequency"],
            "time": schedule["time"]
        }
    # This would call Gemini's API in practice
    return agent_config

# Example usage:
daily_brief_agent = create_spark_agent(
    "Prepare my daily briefing including calendar, emails, and pending tasks",
    schedule={"frequency": "daily", "time": "08:00"}
)
```

## Multimodal Processing Prompt
```
PROMPT TEMPLATE:
Combine these inputs to create a [DESIRED OUTPUT]:
1. [MEDIA TYPE 1]: [DESCRIPTION/PATH]
2. [MEDIA TYPE 2]: [DESCRIPTION/PATH]
3. [TEXT INSTRUCTIONS]: [SPECIFIC REQUIREMENTS]

EXAMPLE:
Combine these inputs to create a marketing poster:
1. Video: /content/product_demo.mp4
2. Images: /brand/logo.png, /photos/team.jpg
3. Text instructions: Use the logo in top right, extract key frames from video to show product features, include team photo with caption 'Meet the makers', use brand colors #FF5733 and #333333
```

## Voice Command Patterns
```
Effective voice command structure:
1. [Action verb] + [object] + [parameters]
   Example: "Schedule meeting with engineering team tomorrow at 2pm for 1 hour"

2. [Context] + [request]
   Example: "Regarding the quarterly report draft, add charts from these figures"

3. [Multi-step instruction]
   Example: "First analyze this spreadsheet for trends, then create a summary presentation with 3 slides"
```

## Scheduled Task Configuration
```json
{
  "agent_type": "recurring",
  "name": "Morning Briefing",
  "trigger": {
    "type": "scheduled",
    "time": "08:00",
    "days": ["mon", "tue", "wed", "thu", "fri"]
  },
  "tasks": [
    "Check calendar for today's appointments",
    "Scan unread emails for urgent items",
    "Review pending tasks from yesterday"
  ],
  "output": {
    "format": "bulleted_list",
    "delivery": "app_notification"
  }
}
```

### Core Concepts

# Core Concepts of Gemini AI Agents

## Autonomous Agents
Google Gemini's Spark feature introduces true autonomous agents capable of executing multi-step workflows. Unlike traditional chatbots that handle single requests, these agents can spin off sub-agents (referred to as 'minions') to accomplish complex tasks. For example, when asked to prepare a daily brief, Spark can autonomously check your calendar, review emails, and compile pending tasks without manual intervention.

## Omni Model
The Omni model enables multimodal processing, allowing the agent to handle any combination of text, images, and videos simultaneously. This 'anything-to-anything' capability means you can input a video, several images, and a text prompt together, and the agent will produce a combined output. For instance, you could merge a personal video with a styled photo to create a new media output.

## Scheduled Actions (Heartbeats)
Spark agents support recurring tasks through scheduled actions called 'heartbeats'. These allow you to set up routines like daily briefings that automatically run at specified times (e.g., every morning at 8 AM). The system handles the repetition without requiring manual re-triggering.

## Contextual Awareness
When used with desktop integration, agents gain access to local files and screen content, enabling context-aware assistance. The voice interface includes real-time speech filtering that removes filler words ('um', 'uh') and self-corrections, producing clean text output from natural speech.

### Practical Guide

# Practical Guide to Implementing Gemini Agents

## Setting Up Spark Agents
1. Access the Spark beta tab in your Gemini app (requires Google AI Ultra access)
2. Start with simple workflows like daily briefings before progressing to complex automations
3. Clearly define the end goal of your workflow (e.g., 'Prepare me for tomorrow's meetings')

## Designing Effective Workflows
- Break down complex tasks into logical sub-tasks that agents can parallelize
- Example workflow for content creation:
  1. Research trending topics
  2. Draft outline
  3. Generate supporting images
  4. Compile final document
- Use natural language prompts that specify both the task and desired output format

## Multimodal Processing Best Practices
- When combining media types, provide clear instructions about how they should interact
- Example prompt: 'Use this video of my presentation and these three logo images to create a branded recap clip with captions highlighting key points'
- For style transfers, provide both the source media and clear style references

## Scheduling Recurring Tasks
- Set clear time triggers (e.g., 'Every weekday at 7:30 AM')
- Include conditional logic where appropriate (e.g., 'Only check for new emails if I have meetings scheduled')
- Monitor initial runs to verify timing and output quality

## Voice Interface Tips
- Speak naturally; the system automatically filters filler words
- Use clear command phrases when directing actions (e.g., 'Add this to my task list')
- For complex instructions, pause between distinct thoughts to help the agent parse intent

### Sources

# Video Sources

The following curated videos were synthesized to create this skill:

1. **[Google Gemini’s Biggest Update Yet: AI Agents, Omni AI, and Smart Glasses](https://www.youtube.com/watch?v=GiqyqBKmAfA)** by Kevin Stratvert