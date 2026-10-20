---
name: ai-agents-patterns
description: "When to activate: AI agents, LLM agents, ReAct, LangChain agents, tool use, memory, multi-agent, CrewAI, AutoGen, agent orchestration"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: ml-ai
  language: python
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---
# AI Agents Patterns

## ReAct Agent Loop (from scratch)

```python
from anthropic import Anthropic

client = Anthropic()

SYSTEM = """You are a helpful assistant with access to tools.
Use the following format:
Thought: reason about what to do
Action: tool_name
Action Input: input to the tool
Observation: result of the tool
... (repeat as needed)
Final Answer: your final response"""

def react_agent(question: str, tools: dict[str, callable], max_steps: int = 10) -> str:
    messages = [{"role": "user", "content": question}]
    for _ in range(max_steps):
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1024,
            system=SYSTEM,
            messages=messages,
            stop_sequences=["Observation:"],
        )
        text = response.content[0].text
        messages.append({"role": "assistant", "content": text})
        if "Final Answer:" in text:
            return text.split("Final Answer:")[-1].strip()
        if "Action:" in text and "Action Input:" in text:
            action = text.split("Action:")[1].split("\n")[0].strip()
            action_input = text.split("Action Input:")[1].split("\n")[0].strip()
            result = tools.get(action, lambda x: f"Unknown tool: {action}")(action_input)
            messages.append({"role": "user", "content": f"Observation: {result}"})
    return "Max steps reached"
```

## LangChain Tool Use

```python
from langchain_anthropic import ChatAnthropic
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain.tools import tool
from langchain_core.prompts import ChatPromptTemplate

@tool
def search_web(query: str) -> str:
    """Search the web for current information."""
    # integrate with search API
    return f"Search results for: {query}"

@tool
def run_python(code: str) -> str:
    """Execute Python code and return output."""
    import io, contextlib
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        exec(code, {})
    return buf.getvalue()

tools = [search_web, run_python]
llm = ChatAnthropic(model="claude-sonnet-4-6")
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

agent = create_tool_calling_agent(llm, tools, prompt)
executor = AgentExecutor(agent=agent, tools=tools, verbose=True, max_iterations=10)
result = executor.invoke({"input": "What is the latest Python version and write a hello world?"})
```

## Memory Types

```python
from langchain.memory import (
    ConversationBufferMemory,
    ConversationSummaryMemory,
    VectorStoreRetrieverMemory,
)
from langchain_community.vectorstores import FAISS
from langchain_anthropic import ChatAnthropic

llm = ChatAnthropic(model="claude-haiku-4-5-20251001")

# 1. Buffer memory (last N exchanges)
buffer_memory = ConversationBufferMemory(k=5, return_messages=True)

# 2. Summary memory (compresses old history)
summary_memory = ConversationSummaryMemory(llm=llm, return_messages=True)

# 3. Vector memory (semantic retrieval from history)
vectorstore = FAISS.from_texts([""], embedding=embeddings)
vector_memory = VectorStoreRetrieverMemory(
    retriever=vectorstore.as_retriever(search_kwargs={"k": 3})
)
```

## Multi-Agent with CrewAI

```python
from crewai import Agent, Task, Crew, Process

researcher = Agent(
    role="Research Analyst",
    goal="Find accurate, up-to-date information",
    backstory="Expert at web research and data synthesis",
    tools=[search_web],
    llm="claude-sonnet-4-6",
    verbose=True,
)

writer = Agent(
    role="Technical Writer",
    goal="Write clear, structured reports",
    backstory="Expert at turning research into readable documents",
    llm="claude-sonnet-4-6",
)

research_task = Task(
    description="Research {topic} and compile key findings",
    expected_output="Bullet-point summary with sources",
    agent=researcher,
)

writing_task = Task(
    description="Write a 500-word report based on the research",
    expected_output="Formatted markdown report",
    agent=writer,
    context=[research_task],
)

crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, writing_task],
    process=Process.sequential,
    verbose=True,
)
result = crew.kickoff(inputs={"topic": "quantum computing trends 2025"})
```

## Agent Evaluation

```python
from langsmith import Client, traceable

client = Client()

@traceable(name="agent-run")
def run_agent(question: str) -> str:
    return executor.invoke({"input": question})["output"]

# Define evaluation dataset
examples = [
    {"input": "What is 2+2?", "expected": "4"},
    {"input": "Capital of France?", "expected": "Paris"},
]

dataset = client.create_dataset("agent-eval")
for ex in examples:
    client.create_example(inputs={"input": ex["input"]},
                          outputs={"output": ex["expected"]},
                          dataset_id=dataset.id)

def correctness_evaluator(run, example):
    score = 1.0 if example.outputs["output"].lower() in run.outputs["output"].lower() else 0.0
    return {"key": "correctness", "score": score}

results = client.run_on_dataset(
    dataset_name="agent-eval",
    llm_or_chain_factory=run_agent,
    evaluators=[correctness_evaluator],
)
```

## Key Patterns

- **Tool descriptions are prompts**: write them precisely — the LLM reads them to decide which tool to call
- **Max iterations**: always cap agent loops (10-20 steps) to prevent infinite loops
- **Parallel tool calls**: use `claude-sonnet-4-6` tool_use with multiple tools in one response for speed
- **Structured output**: use `response_format` or Pydantic models to prevent hallucinated tool args
- **Observability**: instrument every agent run with LangSmith or similar for debugging
