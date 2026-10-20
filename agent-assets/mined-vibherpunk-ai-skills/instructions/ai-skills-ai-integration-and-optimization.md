# Copilot Instructions: Ai Integration And Optimization
Description: A comprehensive skill for integrating and optimizing AI agents using Microsoft Foundry, focusing on knowledge grounding, retrieval systems, and agent optimization.

## Overview
This skill focuses on integrating and optimizing AI agents using Microsoft Foundry. It covers three main areas: knowledge grounding, retrieval systems, and agent optimization. The goal is to enable agents to effectively utilize intrinsic, extrinsic, and learned knowledge to perform tasks efficiently.

## Step-by-Step Workflow
1. **Set Up Knowledge Grounding**: Create a knowledge base in Microsoft Foundry to ground your agents on relevant data. This includes unstructured data (PDFs, images), structured data (parquet tables), and web data.
2. **Configure Retrieval Systems**: Choose between simple vector search and more sophisticated retrieval systems. Use Foundry IQ to manage retrieval workflows, balancing latency and quality.
3. **Optimize Agents**: Use the agent optimizer in Foundry to evaluate and improve agent performance. Generate evaluation tasks, run optimization, and apply the best configuration.

## Code Snippets
```python
# Example: Creating a Knowledge Base in Foundry
from foundry import KnowledgeBase

kb = KnowledgeBase(name='MovieData', unstructured_data='blob://movies.pdf', structured_data='parquet://movie_stats.parquet', web_data=True)
kb.save()
```

## Best Practices
- **Knowledge Grounding**: Ensure your knowledge base includes diverse data sources to provide comprehensive grounding.
- **Retrieval Systems**: Combine methods (e.g., vector search, lexical retrieval) for better results.
- **Agent Optimization**: Regularly evaluate and optimize agents to capture learned knowledge and improve performance.

## Common Pitfalls
- **Incomplete Knowledge Grounding**: Avoid grounding agents on limited data sources, which can lead to incomplete or inaccurate responses.
- **Over-Reliance on Single Retrieval Method**: Using only vector search can result in suboptimal retrieval. Combine methods for better performance.
- **Neglecting Agent Optimization**: Failing to optimize agents can lead to stagnant performance. Regularly evaluate and optimize to capture learned knowledge.

## Validation and Testing
- **Knowledge Grounding**: Test the knowledge base by querying it with various tasks to ensure comprehensive grounding.
- **Retrieval Systems**: Evaluate retrieval performance using metrics like recall and answer completeness.
- **Agent Optimization**: Compare baseline and optimized agent performance using task adherence metrics.

For more details, refer to the following references:
- [Core Concepts](references/core_concepts.md)
- [Practical Guide](references/practical_guide.md)
- [Code Examples](references/code_examples.md)
- [Common Pitfalls](references/common_pitfalls.md)

## Reference Guides

### Code Examples

## Code Examples
### Creating a Knowledge Base
```python
from foundry import KnowledgeBase

kb = KnowledgeBase(name='MovieData', unstructured_data='blob://movies.pdf', structured_data='parquet://movie_stats.parquet', web_data=True)
kb.save()
```

### Configuring Retrieval Systems
```python
from foundry import RetrievalSystem

rs = RetrievalSystem(knowledge_base='MovieData', methods=['vector_search', 'lexical_retrieval'], latency_quality_balance='medium')
rs.configure()
```

### Optimizing Agents
```python
from foundry import AgentOptimizer

optimizer = AgentOptimizer(agent='MovieAgent')
optimizer.generate_evaluation_tasks()
optimizer.run_optimization()
optimizer.apply_best_configuration()
```

### Best Practices
- **Code Readability**: Ensure your code is well-commented and easy to understand.
- **Modular Design**: Use modular design to make your code reusable and maintainable.
- **Error Handling**: Implement robust error handling to manage unexpected issues.

### Common Pitfalls

## Common Pitfalls
### Incomplete Knowledge Grounding
**Issue**: Grounding agents on limited data sources can lead to incomplete or inaccurate responses.
**Solution**: Ensure your knowledge base includes diverse data sources (unstructured, structured, web).

### Over-Reliance on Single Retrieval Method
**Issue**: Using only vector search can result in suboptimal retrieval performance.
**Solution**: Combine multiple retrieval methods (e.g., vector search, lexical retrieval) for better results.

### Neglecting Agent Optimization
**Issue**: Failing to optimize agents can lead to stagnant performance.
**Solution**: Regularly evaluate and optimize agents to capture learned knowledge and improve performance.

### Poor Configuration Management
**Issue**: Poorly managed configurations can lead to inconsistent agent behavior.
**Solution**: Externalize configurations (instructions, tool definitions, skills) for easy management and optimization.

### Token Inefficiency
**Issue**: Inefficient use of tokens can lead to higher costs and slower performance.
**Solution**: Carefully evaluate retrieval systems to ensure information-dense answers with fewer tokens.

### Core Concepts

## Core Concepts
### Intrinsic Knowledge
Intrinsic knowledge refers to the knowledge embedded within AI models through training data. This includes the parametric memory of models, which allows them to perform tasks based on learned patterns.

### Extrinsic Knowledge
Extrinsic knowledge involves external data sources that agents can access to enhance their understanding. This includes documents, emails, chat threads, and data warehouses.

### Learned Knowledge
Learned knowledge is the result of continuous improvement through observation and reflection. Agents can capture unique organizational processes and optimize their performance over time.

### Knowledge Grounding
Knowledge grounding involves connecting agents to relevant data sources to ensure they have the necessary context to perform tasks. This includes unstructured data (PDFs, images), structured data (parquet tables), and web data.

### Retrieval Systems
Retrieval systems are used to fetch relevant information from knowledge bases. These systems can range from simple vector search to more sophisticated methods combining multiple retrieval techniques.

### Agent Optimization
Agent optimization involves evaluating and improving agent performance using tools like the agent optimizer in Microsoft Foundry. This process captures learned knowledge and enhances agent capabilities.

### Practical Guide

## Practical Guide
### Setting Up Knowledge Grounding
1. **Create a Knowledge Base**: Use Microsoft Foundry to create a knowledge base that includes unstructured, structured, and web data.
2. **Configure Data Sources**: Specify the sources of data (e.g., blob storage for PDFs, parquet tables for structured data).
3. **Save and Connect**: Save the knowledge base and connect it to your agents.

### Configuring Retrieval Systems
1. **Choose Retrieval Methods**: Decide between simple vector search and combined methods for better retrieval performance.
2. **Balance Latency and Quality**: Configure the retrieval system to balance between response time and the quality of retrieved information.
3. **Evaluate Performance**: Use metrics like recall and answer completeness to assess retrieval effectiveness.

### Optimizing Agents
1. **Generate Evaluation Tasks**: Create tasks to evaluate agent performance based on traces and instructions.
2. **Run Optimization**: Use the agent optimizer to generate and evaluate candidate configurations.
3. **Apply Best Configuration**: Deploy the optimized configuration to improve agent performance.

### Best Practices
- **Diverse Data Sources**: Ensure your knowledge base includes a variety of data sources for comprehensive grounding.
- **Combined Retrieval Methods**: Use a combination of retrieval techniques for better results.
- **Regular Optimization**: Continuously evaluate and optimize agents to capture learned knowledge and improve performance.

### Sources

# Video Sources

The following curated videos were synthesized to create this skill:

1. **[On AI and Knowledge — Pablo Castro, Distinguished Engineer & CVP for AI Knowledge, Microsoft](https://www.youtube.com/watch?v=RGSFUqzqErE)** by AI Engineer