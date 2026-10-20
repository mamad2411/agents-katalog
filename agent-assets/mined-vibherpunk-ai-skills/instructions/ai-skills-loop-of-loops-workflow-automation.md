# Copilot Instructions: Loop_Of_Loops_Workflow_Automation
Description: Automate recurring tasks by creating interconnected loops that manage workflows, share context, and reduce mental load.

## Overview

A Loop of Loops is a system where multiple recurring tasks (loops) are interconnected to manage workflows efficiently. Each loop handles a specific task, shares context with other loops, and stops when boundaries are met. This approach reduces the need for constant prompting and manual intervention.

### Core Concepts

- **Prompt**: A single request to AI.
- **Loop**: A recurring task with memory.
- **Loop of Loops**: Multiple loops that notice each other, share context, and stop when boundaries are met.

For more details, see [Core Concepts](references/core_concepts.md).

## Step-by-Step Workflow

1. **Identify Recurring Tasks**: Identify tasks that recur frequently and require similar steps each time.
2. **Define Each Loop**: Define the steps and memory requirements for each loop.
3. **Interconnect Loops**: Set up communication between loops so they can share context and trigger each other.
4. **Set Boundaries**: Define stopping conditions for each loop.
5. **Implement and Test**: Implement the loops and test their functionality.

For a practical guide, see [Practical Guide](references/practical_guide.md).

## Code Snippets and Prompt Templates

```python
# Example: Packing List Loop
packing_list_loop = {
    'trigger': 'school_trip_email',
    'steps': [
        'check_weather',
        'check_inventory',
        'generate_list',
        'buy_missing_items'
    ],
    'memory': ['previous_packing_lists', 'current_inventory']
}
```

For more examples, see [Code Examples](references/code_examples.md).

## Best Practices and Common Pitfalls

### Best Practices

- **Start Simple**: Begin with a single loop before moving to interconnected loops.
- **Clear Boundaries**: Define clear stopping conditions to avoid infinite loops.
- **Context Sharing**: Ensure loops can share context effectively.

### Common Pitfalls

- **Overcomplication**: Avoid making loops too complex initially.
- **Lack of Boundaries**: Ensure each loop has clear stopping conditions.
- **Poor Context Sharing**: Ensure loops can share context effectively.

For more on pitfalls, see [Common Pitfalls](references/common_pitfalls.md).

## Validation and Testing

1. **Unit Testing**: Test each loop individually.
2. **Integration Testing**: Test how loops interact with each other.
3. **Boundary Testing**: Ensure loops stop when boundaries are met.

## References

- [Core Concepts](references/core_concepts.md)
- [Practical Guide](references/practical_guide.md)
- [Code Examples](references/code_examples.md)
- [Common Pitfalls](references/common_pitfalls.md)

## Reference Guides

### Code Examples

# Code Examples

## Packing List Loop
```python
packing_list_loop = {
    'trigger': 'school_trip_email',
    'steps': [
        'check_weather',
        'check_inventory',
        'generate_list',
        'buy_missing_items'
    ],
    'memory': ['previous_packing_lists', 'current_inventory']
}
```

## Weather Loop
```python
weather_loop = {
    'trigger': 'daily_check',
    'steps': [
        'fetch_weather_data',
        'analyze_forecast',
        'trigger_packing_list_if_rain'
    ],
    'memory': ['previous_weather_data']
}
```

## Calendar Conflict Loop
```python
calendar_conflict_loop = {
    'trigger': 'new_event_added',
    'steps': [
        'fetch_calendar_events',
        'check_for_conflicts',
        'trigger_message_loop_if_conflict'
    ],
    'memory': ['previous_conflicts']
}
```

## Message Loop
```python
message_loop = {
    'trigger': 'conflict_detected',
    'steps': [
        'generate_message',
        'send_message'
    ],
    'memory': ['previous_messages']
}
```

These code examples illustrate how to define and implement loops for different tasks within a Loop of Loops system.

### Common Pitfalls

# Common Pitfalls

## Overcomplication
One common pitfall is making loops too complex initially. Start simple and gradually add complexity as needed.

## Lack of Boundaries
Another pitfall is failing to define clear stopping conditions for loops. This can lead to infinite loops and system crashes.

## Poor Context Sharing
Loops need to share context effectively. Poor context sharing can result in loops making decisions based on incomplete or outdated information.

### Examples
- **Overcomplication**: Creating a loop with too many steps initially, making it difficult to debug.
- **Lack of Boundaries**: A weather loop that continuously checks the forecast without stopping.
- **Poor Context Sharing**: A packing list loop that doesn't receive updated weather information from the weather loop.

### Best Practices
- **Start Simple**: Begin with a single loop and add complexity gradually.
- **Clear Boundaries**: Define clear stopping conditions for each loop.
- **Effective Context Sharing**: Ensure loops can share context effectively.

By avoiding these common pitfalls, you can build a more robust and efficient Loop of Loops system.

### Core Concepts

# Core Concepts

## Prompt
A prompt is a single request made to an AI system. It is typically a straightforward question or command that elicits a specific response. For example, asking an AI to generate a packing list for a school trip is a prompt.

## Loop
A loop is a recurring task that the AI handles autonomously. Unlike a prompt, a loop has memory, meaning it can remember past iterations and use that information to improve future executions. For instance, a loop for generating a packing list would remember previous lists and current inventory.

## Loop of Loops
A Loop of Loops is an advanced concept where multiple loops are interconnected. These loops can notice each other, share context, and stop when boundaries are met. This system allows for more complex and efficient workflow automation. For example, a Loop of Loops for a school trip might include loops for packing, weather checking, and calendar conflict resolution.

### Key Differences
- **Prompt**: Single request, no memory.
- **Loop**: Recurring task with memory.
- **Loop of Loops**: Multiple interconnected loops with shared context and boundaries.

Understanding these core concepts is essential for building effective AI-driven workflows.

### Practical Guide

# Practical Guide

## Identifying Recurring Tasks
Start by identifying tasks that recur frequently and require similar steps each time. These tasks are prime candidates for automation.

## Defining Each Loop
For each identified task, define the steps and memory requirements. For example, a packing list loop might include steps like checking the weather, checking inventory, generating a list, and buying missing items.

## Interconnecting Loops
Set up communication between loops so they can share context and trigger each other. For instance, a weather loop might trigger a packing list loop if rain is forecasted.

## Setting Boundaries
Define stopping conditions for each loop to avoid infinite loops. For example, a packing list loop might stop once all items are purchased.

## Implementing and Testing
Implement the loops and test their functionality. Start with unit testing each loop individually, then move to integration testing to ensure loops interact correctly.

### Example: School Trip Loop of Loops
1. **Packing List Loop**: Checks inventory and generates a list.
2. **Weather Loop**: Checks the weather forecast.
3. **Calendar Conflict Loop**: Checks for scheduling conflicts.
4. **Message Loop**: Sends reminders to relevant parties.

By following these steps, you can build a robust Loop of Loops system that automates complex workflows efficiently.

### Sources

# Video Sources

The following curated videos were synthesized to create this skill:

1. **[I Stopped Prompting AI One Task At A Time. This Works Better.](https://www.youtube.com/watch?v=A4zMyjkL0Dc)** by AI News & Strategy Daily | Nate B Jones