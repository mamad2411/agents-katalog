# Copilot Instructions: Claude Cowork Workflow Automation
Description: A comprehensive skill for automating daily workflows using Claude Cowork, including email triage, content creation, research, and dashboard generation.

# Claude Cowork Workflow Automation Skill

## Overview
This skill transforms Claude from a basic chatbot into an automated workflow assistant that handles email triage, content creation, research, and business intelligence. By implementing these workflows, you can shift from being a creator to an approver, saving hours each day. For foundational concepts, see [Core Concepts](references/core_concepts.md).

## Step-by-Step Workflow

1. **Initial Setup**
   - Connect Gmail and calendar via Manage Connectors (OAuth flow)
   - Create a 'content voice' project with your style guidelines
   - Upload 5-10 reference documents representing your best work

2. **Daily Brief Automation**
   - Create scheduled task for weekdays at 7:00 AM
   - Use prompt template from [Code Examples](references/code_examples.md)
   - Set output location to your daily brief folder

3. **Email Triage System**
   - Implement the email sorting prompt twice daily (7 AM and 1 PM)
   - Review and adjust categorization rules weekly
   - Keep 'draft only' mode enabled for first two weeks

4. **Content Creation Workflow**
   - Use /post_from_note skill within your content project
   - Provide raw notes or voice memo transcripts
   - Expect to perform one round of edits on first drafts

5. **Research Automation**
   - Create dedicated research project with Chrome integration
   - Use structured brief template for consistent results
   - Verify critical facts against primary sources

6. **Business Dashboard**
   - Connect data sources (CSV, Stripe, bank feeds)
   - Generate initial dashboard and validate numbers
   - Schedule monthly refreshes with new data

## Best Practices
- Start small with 1-2 automations before expanding (see [Common Pitfalls](references/common_pitfalls.md))
- Maintain a library of approved outputs as additional training data
- Schedule weekly reviews to refine prompts and workflows
- Use the mobile Dispatch feature for on-the-go task creation

## Validation Steps
1. For email drafts: Spot-check 20% of auto-generated replies for tone accuracy
2. For research reports: Verify 3-5 key facts against source material
3. For dashboards: Cross-check totals against original data sources
4. For content: Compare automated drafts to your manual work for style consistency

## Implementation Notes
- All prompt templates are available in [Code Examples](references/code_examples.md)
- For detailed setup instructions, consult the [Practical Guide](references/practical_guide.md)
- Be mindful of the limitations and solutions outlined in [Common Pitfalls](references/common_pitfalls.md)

## Reference Guides

### Code Examples

# Code Examples and Prompt Templates for Claude Cowork

## Email Triage Prompt
```
Sort the last 12 hours of unread mail into three categories:
1. Reply Today: Requires response today. Draft a reply in my voice (concise, professional but friendly). Include:
   - Acknowledgment of their message
   - Clear answer to their question
   - Any necessary follow-up questions
2. FYI: Important but doesn't require immediate response
3. Noise: Low-priority or promotional content that can be archived

Present results in a table with columns: Category, Sender, Subject, Action (draft reply or none)
```

## Content Creation Skill (/post_from_note)
```
Transform this raw note into a polished blog post draft:
- Use my established voice from project references
- Structure with: compelling hook, 3-5 key points, strong conclusion
- Avoid: corporate jargon, cliché openings, fluff
- Target length: 800-1000 words

Raw note: [paste content here]
```

## Research Brief Template
```
Research Topic: [clear subject]
Audience: [describe who will consume this]
Depth Level: [overview, intermediate, deep dive]
Key Questions to Answer:
1. [primary question 1]
2. [primary question 2]
3. [primary question 3]

Requirements:
- Only use sources from the last 90 days
- Cross-check facts against official documentation
- Highlight any conflicting information
- Format as HTML report with: executive summary, key findings, comparison tables, sources
```

## Dashboard Generation Prompt
```
Create an interactive HTML dashboard from this data with:
1. 12-month revenue trend chart
2. Top customer segments by growth
3. Anomaly detection highlighting unusual patterns
4. 'Watch This Week' section flagging 3 key metrics

Design Requirements:
- Mobile-responsive layout
- Hover tooltips on all charts
- Tab navigation between sections
- Visual highlights on important trends

Data: [attach CSV or connect to data source]
```

### Common Pitfalls

# Common Pitfalls and Troubleshooting Guide

## Performance Issues
1. **Usage Limits**: Claude consumes limits faster in automation mode. Solution: Start with 1-2 critical tasks before expanding.
2. **Sleeping Computer**: Scheduled tasks only run when your computer is awake. Solution: Enable the 'prevent sleep' toggle during work hours.

## Quality Concerns
1. **Voice Inconsistency**: Early drafts might not perfectly match your style. Solution: Provide 5-10 strong reference examples and be specific about tone preferences.
2. **Factual Errors**: Research outputs may contain inaccuracies. Solution: Always verify critical numbers and enable cross-checking in research briefs.

## Technical Challenges
1. **Beta Features**: Some capabilities like Claude in Chrome or Dispatch may not be available to all users. Solution: Check your plan level or wait for full rollout.
2. **Connector Issues**: Gmail integrations might require reauthentication. Solution: Set calendar reminders to check connector status monthly.

## Workflow Design Mistakes
1. **Over-Automation**: Trying to automate everything at once leads to poor results. Solution: Implement automations sequentially, refining each before adding another.
2. **Lack of Human Review**: Assuming perfect first drafts. Reality: Most outputs need one round of edits. Solution: Budget review time in your process.

## Security Considerations
1. **Email Safety**: By default, Claude only drafts emails without sending. Solution: Keep this setting until you're confident in the quality.
2. **Data Privacy**: Be mindful of what data you feed into the system. Solution: Anonymize sensitive information in datasets used for dashboards.

Remember that Claude is a powerful assistant but still requires human oversight, especially when dealing with critical business functions or customer communications.

### Core Concepts

# Core Concepts of Claude Cowork Workflow Automation

Claude Cowork is an AI-powered workspace that allows you to automate repetitive tasks, manage projects, and streamline workflows. Unlike traditional chatbots, Claude Cowork operates as a persistent agent that can run tasks in the background, maintain context between tasks, and integrate with various tools and services.

Key concepts include:

1. **Projects**: Workspaces with persistent memory where you can store instructions, reference files, and maintain context. Projects allow Claude to remember your preferences, voice, and workflow requirements without needing re-explanation.

2. **Skills**: Reusable workflows triggered by slash commands (e.g., /post_from_note). These encapsulate specific tasks like content creation or email triage.

3. **Scheduled Tasks**: Automations that run at specific times (e.g., daily briefings at 7 AM). These only execute when your computer is awake and the app is open.

4. **Connectors**: Integrations with external services like Gmail, calendars, and browsers that enable Claude to interact with your existing tools.

5. **Dispatch**: A feature that allows you to send instructions from the Claude mobile app to your desktop, enabling remote workflow control.

Understanding these core concepts is essential for effectively implementing the automation workflows described in this skill. Each component works together to create a seamless automation system that adapts to your specific needs and preferences.

### Practical Guide

# Practical Guide to Implementing Claude Cowork Workflows

This guide provides detailed instructions for setting up and maintaining effective workflow automations with Claude Cowork.

## Getting Started
1. **Initial Setup**: Begin by connecting essential services like Gmail and your calendar through the 'Manage Connectors' section. Use OAuth for secure access.
2. **Project Creation**: For content workflows, create a project named 'content voice' with instructions about your audience, preferred tone, and stylistic no-nos (e.g., no corporate buzzwords).
3. **Reference Materials**: Upload 5-10 examples of your best work to establish your voice. These serve as training data for Claude.

## Workflow Implementation
- **Email Triage**: Set up a scheduled task to run twice daily (7 AM and 1 PM) that sorts unread mail into three categories: reply today (with drafts), FYI, and noise.
- **Content Creation**: Use the /post_from_note skill within your content project to transform rough ideas into drafts that match your voice.
- **Research Automation**: Create a research project with instructions for Chrome-based fact-checking. Provide clear briefs with audience and depth parameters.

## Maintenance Tips
- Regularly review and update your reference materials as your style evolves
- Monitor task performance and adjust prompts as needed
- Start with 1-2 automations before scaling up to avoid hitting usage limits

Remember that Claude is an assistant, not a replacement. Always review outputs before finalizing important communications or decisions.

### Sources

# Video Sources

The following curated videos were synthesized to create this skill:

1. **[6 INSANE Claude Cowork Use Cases to Save Hours (AI Workflow Automation)](https://www.youtube.com/watch?v=skU1-k7_wWE)** by AI Master