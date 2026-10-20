# Copilot Instructions: Ai Driven Problem Identification And Automation
Description: This skill enables AI agents to autonomously identify business problems, define solutions, and create automation scripts by analyzing user data and workflows.

# AI-Driven Problem Identification and Automation

## Overview
This skill allows AI agents to autonomously identify business problems, define solutions, and create automation scripts by analyzing user data and workflows. The process involves analyzing Slack channels, local files, and other business process descriptors to pinpoint pain points and propose actionable solutions.

## Step-by-Step Workflow
1. **Data Access and Analysis**: Access and analyze user data including Slack channels and local files.
2. **Problem Identification**: Identify potential business problems based on the analysis.
3. **Solution Proposal**: Propose a solution and automation script for the identified problem.
4. **Implementation**: Implement the automation script and ensure it addresses the problem effectively.

## Code Snippets
```python
# Example prompt for problem identification
prompt = "Analyze my Slack channels and local files to identify business problems. Propose a solution and create an automation script."
```

## Best Practices
- Ensure comprehensive data access for accurate problem identification.
- Encourage strategic thinking in problem selection.

## Common Pitfalls
- Narrow problem definitions leading to less impactful solutions.
- Overlooking strategic opportunities in favor of immediate, but less significant, issues.

## Validation and Testing
- Test the automation script in a controlled environment.
- Validate the solution's impact on the identified problem.

For more detailed guidelines and examples, refer to [Core Concepts](references/core_concepts.md), [Practical Guide](references/practical_guide.md), and [Code Examples](references/code_examples.md).

## Reference Guides

### Code Examples

# Code Examples

## Example Prompt for Problem Identification
```python
# Example prompt for problem identification
prompt = "Analyze my Slack channels and local files to identify business problems. Propose a solution and create an automation script."
```

## Example Automation Script
```python
# Example automation script for a identified problem
import os
import slack

# Initialize Slack client
slack_client = slack.WebClient(token=os.environ['SLACK_TOKEN'])

# Function to automate a repetitive task
def automate_task(channel_id, message):
    response = slack_client.chat_postMessage(
        channel=channel_id,
        text=message
    )
    return response

# Example usage
automate_task('C1234567890', 'This is an automated message.')
```

## Example Implementation Script
```python
# Example implementation script
import subprocess

# Function to implement the automation script
def implement_script(script_path):
    result = subprocess.run(['python3', script_path], capture_output=True, text=True)
    return result.stdout

# Example usage
output = implement_script('automation_script.py')
print(output)
```

## Example Validation Script
```python
# Example validation script
import unittest

# Test case for the automation script
class TestAutomationScript(unittest.TestCase):
    def test_automate_task(self):
        # Test the automate_task function
        response = automate_task('C1234567890', 'Test message')
        self.assertEqual(response['ok'], True)

# Run the tests
if __name__ == '__main__':
    unittest.main()
```

These code examples provide practical templates for implementing and validating AI-driven problem identification and automation scripts. Use these examples as a starting point for developing your own solutions.

### Core Concepts

# Core Concepts

## Understanding AI-Driven Problem Identification
AI-driven problem identification involves using artificial intelligence to autonomously detect and define business problems by analyzing various data sources such as Slack channels, local files, and other workflow descriptors. This process leverages AI's ability to process large volumes of data and identify patterns that may not be immediately apparent to human analysts.

## Strategic Thinking in AI
Strategic thinking in AI refers to the ability of AI systems to identify and prioritize problems that offer the most significant leverage or impact. This involves understanding the broader context of the business and selecting problems that, when solved, can lead to substantial improvements in efficiency or effectiveness.

## Automation Scripts
Automation scripts are sequences of instructions that automate repetitive tasks or processes. In the context of AI-driven problem identification, these scripts are designed to address the specific problems identified by the AI, thereby reducing manual effort and increasing operational efficiency.

## Data Analysis
Data analysis is the process of inspecting, cleaning, transforming, and modeling data to discover useful information, suggest conclusions, and support decision-making. In AI-driven problem identification, data analysis is crucial for understanding the current state of business processes and identifying areas for improvement.

## Implementation and Validation
Implementation involves putting the proposed solutions into practice, while validation ensures that these solutions effectively address the identified problems. This step is critical for confirming the accuracy and effectiveness of the AI's problem identification and solution proposal.

By mastering these core concepts, AI agents can effectively identify and solve business problems, leading to improved operational efficiency and strategic advantage.

### Practical Guide

# Practical Guide

## Step-by-Step Workflow
1. **Data Access and Analysis**: Begin by granting the AI access to relevant data sources such as Slack channels and local files. Ensure that the AI has comprehensive access to accurately analyze the data.
2. **Problem Identification**: Use the AI to identify potential business problems based on the data analysis. Encourage the AI to think strategically and prioritize problems that offer the most significant leverage.
3. **Solution Proposal**: Once a problem is identified, the AI should propose a solution and create an automation script to address the problem. Ensure that the solution is practical and feasible.
4. **Implementation**: Implement the automation script in a controlled environment. Monitor the implementation to ensure it addresses the problem effectively.

## Best Practices
- **Comprehensive Data Access**: Ensure the AI has access to all relevant data sources for accurate problem identification.
- **Strategic Thinking**: Encourage the AI to prioritize problems that offer the most significant leverage or impact.
- **Practical Solutions**: Ensure that the proposed solutions are practical and feasible to implement.

## Common Pitfalls
- **Narrow Problem Definitions**: Avoid narrow problem definitions that lead to less impactful solutions. Encourage the AI to think broadly and consider the broader context of the business.
- **Overlooking Strategic Opportunities**: Ensure the AI does not overlook strategic opportunities in favor of immediate, but less significant, issues.

## Validation and Testing
- **Controlled Environment Testing**: Test the automation script in a controlled environment to ensure it functions as intended.
- **Impact Validation**: Validate the solution's impact on the identified problem to confirm its effectiveness.

By following this practical guide, AI agents can effectively identify and solve business problems, leading to improved operational efficiency and strategic advantage.

### Sources

# Video Sources

The following curated videos were synthesized to create this skill:

1. **[Codex vs Fable: Which AI Agent Picked the Better Problem?](https://www.youtube.com/watch?v=uCWKXIyvM_8)** by AI News & Strategy Daily | Nate B Jones