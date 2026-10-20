# Copilot Instructions: Agentic Ai Framework Selection
Description: A comprehensive skill for selecting the appropriate agentic AI framework based on the type of system you aim to build, including linear workflows, autonomous agents, role-based systems, production orchestration, and rapid prototyping.

## Overview
Agentic AI frameworks are essential tools for building complex AI systems that involve planning, acting, and iterating. These frameworks provide predefined architectures, integration tools, task management capabilities, and communication protocols to simplify the development process. The choice of framework depends on the type of agentic AI system you are building, such as linear workflows, autonomous agents, role-based systems, production orchestration, or rapid prototyping.

For a deeper understanding of core concepts, refer to [Core Concepts](references/core_concepts.md).

## Step-by-Step Workflow
1. **Identify the Type of System**: Determine whether your system is a linear workflow, autonomous agent, role-based system, production orchestration, or rapid prototyping.
2. **Select the Appropriate Framework**:
   - **Linear Workflows**: Use LangChain or LlamaIndex.
   - **Autonomous Agents**: Use AutoGen, Baby AGI, or CrewAI.
   - **Role-Based Systems**: Use CrewAI or AutoGen with structured roles.
   - **Production Orchestration**: Use Agent Framework (Semantic Kernel + AutoGen) or LangGraph.
   - **Rapid Prototyping**: Use LangFlow or Flowise.
3. **Implement the Framework**: Follow the framework's documentation to set up and configure your system.
4. **Test and Validate**: Ensure the system performs as expected and meets the requirements.

For detailed implementation steps and code examples, refer to [Practical Guide](references/practical_guide.md) and [Code Examples](references/code_examples.md).

## Best Practices
- **Understand Your Requirements**: Clearly define the problem and the type of system needed.
- **Leverage Framework Features**: Utilize predefined functions and tools provided by the framework.
- **Monitor and Iterate**: Continuously monitor the system's performance and make necessary adjustments.

## Common Pitfalls
- **Choosing the Wrong Framework**: Selecting a framework not suited for your system type can lead to inefficiencies.
- **Overcomplicating the System**: Avoid adding unnecessary complexity by sticking to the framework's strengths.

For more insights on best practices and pitfalls, refer to [Common Pitfalls](references/common_pitfalls.md).

## Validation Steps
1. **Functional Testing**: Ensure all components work as intended.
2. **Performance Testing**: Verify the system handles the expected load.
3. **User Testing**: Gather feedback from end-users to refine the system.

## References
- [Core Concepts](references/core_concepts.md)
- [Practical Guide](references/practical_guide.md)
- [Code Examples](references/code_examples.md)
- [Common Pitfalls](references/common_pitfalls.md)

## Reference Guides

### Code Examples

# Code Examples
This document provides concrete code snippets and prompt templates for implementing agentic AI frameworks.

## Linear Workflows with LangChain
```python
from langchain import LLMChain, PromptTemplate

# Define the prompt template
prompt_template = PromptTemplate(
    input_variables=['question'],
    template='Answer the following question: {question}'
)

# Create the LLM chain
chain = LLMChain(llm=llm, prompt=prompt_template)

# Run the chain
response = chain.run('What is the capital of France?')
print(response)
```

## Autonomous Agents with AutoGen
```python
from autogen import AssistantAgent, UserProxyAgent

# Create the assistant agent
assistant = AssistantAgent('assistant')

# Create the user proxy agent
user_proxy = UserProxyAgent('user_proxy')

# Initiate the conversation
user_proxy.initiate_chat(assistant, message='Plan a trip to Paris.')
```

## Role-Based Systems with CrewAI
```python
from crewai import Agent, Task, Crew

# Define the agents
researcher = Agent(role='Researcher', goal='Find relevant information')
writer = Agent(role='Writer', goal='Write an article')

# Define the tasks
task1 = Task(description='Research the topic', agent=researcher)
task2 = Task(description='Write the article', agent=writer)

# Create the crew
crew = Crew(agents=[researcher, writer], tasks=[task1, task2])

# Run the crew
crew.kickoff()
```

These code examples demonstrate how to implement different types of agentic AI systems using various frameworks.

### Common Pitfalls

# Common Pitfalls
When working with agentic AI frameworks, there are several common pitfalls to avoid.

## Choosing the Wrong Framework
Selecting a framework not suited for your system type can lead to inefficiencies. For example, using LangChain for a role-based system may not provide the necessary structure.

## Overcomplicating the System
Adding unnecessary complexity can make the system harder to manage. Stick to the framework's strengths and avoid over-engineering.

## Ignoring Integration Requirements
Failing to consider integration with existing systems can lead to compatibility issues. Ensure the framework supports the necessary APIs and databases.

## Lack of Testing
Skipping thorough testing can result in unexpected behavior. Conduct functional, performance, and user testing to ensure the system meets expectations.

## Best Practices
- **Understand Your Requirements**: Clearly define the problem and the type of system needed.
- **Leverage Framework Features**: Utilize predefined functions and tools provided by the framework.
- **Monitor and Iterate**: Continuously monitor the system's performance and make necessary adjustments.

By avoiding these common pitfalls, you can build more effective and efficient agentic AI systems.

### Core Concepts

# Core Concepts
Agentic AI frameworks are toolkits designed to build complex AI systems that involve planning, acting, and iterating. These frameworks provide predefined architectures, integration tools, task management capabilities, and communication protocols to simplify the development process.

## Types of Agentic AI Systems
1. **Linear Workflows**: Systems where tasks progress in a step-by-step fashion, such as customer support agents.
2. **Autonomous Agents**: Systems where AI agents collaborate to achieve a common goal, such as AI coding assistants.
3. **Role-Based Systems**: Systems where agents have defined roles and operate within constraints, such as content generation agents.
4. **Production Orchestration**: Systems integrated with real-world applications, such as AI operations agents.
5. **Rapid Prototyping**: Systems designed for quick validation of ideas, such as drag-and-drop workflow builders.

## Key Features of Frameworks
- **Predefined Architectures**: Simplify the design process.
- **Integration Tools**: Facilitate connections with databases and APIs.
- **Task Management**: Help manage complex workflows.
- **Communication Protocols**: Enable agents to interact effectively.

Understanding these core concepts is crucial for selecting the right framework for your AI system.

### Practical Guide

# Practical Guide
This guide provides detailed steps for selecting and implementing the appropriate agentic AI framework based on your system type.

## Step-by-Step Implementation
1. **Identify the System Type**: Determine whether your system is a linear workflow, autonomous agent, role-based system, production orchestration, or rapid prototyping.
2. **Select the Framework**:
   - **Linear Workflows**: LangChain or LlamaIndex.
   - **Autonomous Agents**: AutoGen, Baby AGI, or CrewAI.
   - **Role-Based Systems**: CrewAI or AutoGen with structured roles.
   - **Production Orchestration**: Agent Framework (Semantic Kernel + AutoGen) or LangGraph.
   - **Rapid Prototyping**: LangFlow or Flowise.
3. **Set Up the Framework**: Follow the framework's documentation to install and configure the necessary components.
4. **Develop the System**: Implement the workflows, agent interactions, and integrations as per your requirements.
5. **Test the System**: Conduct functional, performance, and user testing to ensure the system meets expectations.

## Tips for Success
- **Start Simple**: Begin with basic functionalities and gradually add complexity.
- **Leverage Documentation**: Utilize the framework's documentation and community resources.
- **Iterate and Improve**: Continuously refine the system based on feedback and performance metrics.

By following this practical guide, you can effectively implement the right agentic AI framework for your project.

### Sources

# Video Sources

The following curated videos were synthesized to create this skill:

1. **[Agentic AI Frameworks Explained: Workflows, Multi-Agent, & Production](https://www.youtube.com/watch?v=ZVPlLaehjLk)** by IBM Technology