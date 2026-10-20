# Copilot Instructions: Optimizing Ai Agents To Reduce Hallucinations And Improve Efficiency
Description: This skill teaches AI agents how to optimize their performance by reducing hallucinations, minimizing token waste, and improving accuracy through five key techniques: semantic tool selection, GraphRAG, multi-agent validation, neuro-symbolic guardians, and runtime guardians.

### Overview
AI agents often hallucinate or waste tokens due to inefficient tool selection, unstructured data retrieval, and lack of validation mechanisms. This skill introduces five techniques to address these issues:
1. **Semantic Tool Selection**: Filters tools based on relevance to reduce token usage.
2. **GraphRAG**: Replaces text retrieval with structured graph queries for precise answers.
3. **Multi-Agent Validation**: Adds a validation layer to catch errors before responses reach users.
4. **Neuro-Symbolic Guardians**: Enforces rules in code to prevent agents from bypassing constraints.
5. **Runtime Guardians**: Allows agents to self-correct and complete tasks without hard stops.

For detailed explanations of each technique, refer to [Core Concepts](references/core_concepts.md).

### Step-by-Step Workflow
1. **Semantic Tool Selection**:
   - Create a vector database of tools.
   - Use semantic search to filter relevant tools for each query.
   - Reduce token usage by sending only the most relevant tools.
   Example: [Code Examples](references/code_examples.md).

2. **GraphRAG**:
   - Build a knowledge graph from documents.
   - Use Cypher queries to retrieve structured data.
   - Replace text retrieval with graph queries for precise answers.
   Example: [Practical Guide](references/practical_guide.md).

3. **Multi-Agent Validation**:
   - Implement a swarm of agents: executor, validator, and critic.
   - Validate responses before they reach users.
   - Catch hallucinations and errors early.
   Example: [Common Pitfalls](references/common_pitfalls.md).

4. **Neuro-Symbolic Guardians**:
   - Write rules in Python code using hooks.
   - Intercept tool calls to enforce constraints.
   - Prevent agents from bypassing rules.
   Example: [Code Examples](references/code_examples.md).

5. **Runtime Guardians**:
   - Use agent control to steer agents when rules are soft.
   - Allow agents to self-correct and complete tasks.
   - Avoid hard stops and improve user experience.
   Example: [Practical Guide](references/practical_guide.md).

### Best Practices
- **Semantic Tool Selection**: Always filter tools based on relevance to minimize token usage.
- **GraphRAG**: Use structured queries for precise answers, especially for aggregations and counts.
- **Multi-Agent Validation**: Implement a validation layer to catch errors before responses reach users.
- **Neuro-Symbolic Guardians**: Enforce rules in code, not in prompts, to ensure compliance.
- **Runtime Guardians**: Use steering rules to allow agents to self-correct and complete tasks.

### Common Pitfalls
- **Semantic Tool Selection**: Sending all tools in every query wastes tokens and increases costs.
- **GraphRAG**: Relying on text retrieval for structured queries leads to inaccurate answers.
- **Multi-Agent Validation**: Single agents may generate false success responses without validation.
- **Neuro-Symbolic Guardians**: Rules in prompts are suggestions, not constraints.
- **Runtime Guardians**: Hard stops can frustrate users; use steering rules instead.

### Validation and Testing
- **Semantic Tool Selection**: Compare token usage and accuracy before and after filtering tools.
- **GraphRAG**: Test queries for aggregations and counts to ensure precise answers.
- **Multi-Agent Validation**: Compare responses from single agents and swarms to catch hallucinations.
- **Neuro-Symbolic Guardians**: Test rule enforcement by attempting to bypass constraints.
- **Runtime Guardians**: Verify that agents self-correct and complete tasks without hard stops.

For more detailed validation steps, refer to [Practical Guide](references/practical_guide.md).

## Reference Guides

### Code Examples

### Code Examples

#### Semantic Tool Selection
```python
from sentence_transformers import SentenceTransformer
from faiss import IndexFlatL2

# Create embeddings for tools
tool_embeddings = SentenceTransformer('all-MiniLM-L6-v2').encode(tool_descriptions)

# Build a vector index
index = IndexFlatL2(tool_embeddings.shape[1])
index.add(tool_embeddings)

# Search for relevant tools
query_embedding = SentenceTransformer('all-MiniLM-L6-v2').encode(query)
_, indices = index.search(query_embedding, k=3)
relevant_tools = [tools[i] for i in indices[0]]
```

#### GraphRAG
```python
from neo4j import GraphDatabase

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))

# Execute a Cypher query
with driver.session() as session:
    result = session.run("MATCH (h:Hotel) WHERE h.city = 'Paris' RETURN AVG(h.rating) AS avg_rating")
    avg_rating = result.single()['avg_rating']
```

#### Multi-Agent Validation
```python
from swarms import Swarm

# Create a swarm of agents
swarm = Swarm([executor_agent, validator_agent, critic_agent])

# Execute a query
response = swarm.execute("Book a hotel in Paris")
```

#### Neuro-Symbolic Guardians
```python
from strands import Agent, Hook

# Define a rule hook
def booking_rule_hook(params):
    if params['guests'] > 10:
        raise ValueError("Maximum guest limit exceeded")

# Register the hook
agent = Agent()
agent.register_hook(Hook.BEFORE_TOOL_CALL, booking_rule_hook)
```

#### Runtime Guardians
```python
from agent_control import AgentControl

# Define steering rules
rules = [
    {"name": "steer_max_guests", "action": "reduce_guests", "condition": "guests > 10"},
    {"name": "deny_no_payment", "action": "block", "condition": "payment is None"}
]

# Register rules
agent_control = AgentControl(rules)
agent_control.register()
```

For more detailed explanations, refer to [Core Concepts](references/core_concepts.md).

### Common Pitfalls

### Common Pitfalls

#### Semantic Tool Selection
- **Pitfall**: Sending all tools in every query wastes tokens and increases costs.
- **Solution**: Filter tools based on relevance using semantic search.

#### GraphRAG
- **Pitfall**: Relying on text retrieval for structured queries leads to inaccurate answers.
- **Solution**: Use structured graph queries for precise answers.

#### Multi-Agent Validation
- **Pitfall**: Single agents may generate false success responses without validation.
- **Solution**: Implement a swarm of agents to validate responses.

#### Neuro-Symbolic Guardians
- **Pitfall**: Rules in prompts are suggestions, not constraints.
- **Solution**: Enforce rules in code using hooks.

#### Runtime Guardians
- **Pitfall**: Hard stops can frustrate users.
- **Solution**: Use steering rules to allow agents to self-correct and complete tasks.

For practical examples of how to avoid these pitfalls, refer to [Practical Guide](references/practical_guide.md).

### Core Concepts

### Core Concepts

#### Semantic Tool Selection
Semantic tool selection involves filtering tools based on their relevance to a specific query. This reduces token usage by sending only the most relevant tools to the model. For example, a travel agent with 29 tools can reduce token usage from thousands to fewer than 300 by filtering tools.

#### GraphRAG
GraphRAG replaces text retrieval with structured graph queries. Instead of retrieving text chunks, it builds a knowledge graph from documents and uses Cypher queries to retrieve precise answers. This is especially useful for aggregations, counts, and multi-hop reasoning.

#### Multi-Agent Validation
Multi-agent validation adds a validation layer to catch errors before responses reach users. A swarm of agents (executor, validator, and critic) ensures that responses are accurate and free from hallucinations.

#### Neuro-Symbolic Guardians
Neuro-symbolic guardians enforce rules in code, not in prompts. This ensures that agents cannot bypass constraints. Rules are enforced using hooks that intercept tool calls before they execute.

#### Runtime Guardians
Runtime guardians allow agents to self-correct and complete tasks without hard stops. Steering rules enable agents to adjust and keep going, improving user experience.

For detailed code examples, refer to [Code Examples](references/code_examples.md).

### Practical Guide

### Practical Guide

#### Semantic Tool Selection
1. Create a vector database of tools.
2. Use semantic search to filter relevant tools for each query.
3. Reduce token usage by sending only the most relevant tools.

#### GraphRAG
1. Build a knowledge graph from documents.
2. Use Cypher queries to retrieve structured data.
3. Replace text retrieval with graph queries for precise answers.

#### Multi-Agent Validation
1. Implement a swarm of agents: executor, validator, and critic.
2. Validate responses before they reach users.
3. Catch hallucinations and errors early.

#### Neuro-Symbolic Guardians
1. Write rules in Python code using hooks.
2. Intercept tool calls to enforce constraints.
3. Prevent agents from bypassing rules.

#### Runtime Guardians
1. Use agent control to steer agents when rules are soft.
2. Allow agents to self-correct and complete tasks.
3. Avoid hard stops and improve user experience.

For common pitfalls and how to avoid them, refer to [Common Pitfalls](references/common_pitfalls.md).

### Sources

# Video Sources

The following curated videos were synthesized to create this skill:

1. **[Stop AI Agent Hallucinations: 5 Techniques + Production Patterns - Elizabeth Fuentes, AWS](https://www.youtube.com/watch?v=vJukHCIv7Ck)** by AI Engineer