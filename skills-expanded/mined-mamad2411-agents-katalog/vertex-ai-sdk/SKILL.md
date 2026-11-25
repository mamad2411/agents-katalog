---
name: vertex-ai-sdk
version: "1.0"
description: >
  Vertex AI SDK patterns for configuring Gemini models including generation parameters, safety settings, streaming responses, and function calling.
  PROACTIVELY activate for: (1) model configuration and temperature settings, (2) safety controls and streaming implementation, (3) Vertex AI endpoint selection and function calling.
  Triggers: "gemini config", "model parameters", "streaming response"
core-integration:
  techniques:
    primary: ["structured_decomposition"]
    secondary: []
  contracts:
    input: "none"
    output: "none"
  patterns: "none"
  rubrics: "none"
---

# Vertex AI SDK: Gemini Model Configuration and Usage

## Core Principles

The Vertex AI SDK provides Python interfaces for Gemini models with fine-grained control over generation behavior, safety, and response characteristics. Proper configuration is critical for production-grade agents.

## Model Initialization (Required Pattern)

### Basic Client Setup

```python
from google import genai
from google.genai import types
import os

# Initialize Vertex AI client
client = genai.Client(
    vertexai=True,
    project=os.getenv("GOOGLE_CLOUD_PROJECT"),
    location=os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
)

# Reuse client instance across requests
MODEL_ID = "gemini-2.0-flash-exp"
```

**Best Practice**: Initialize client once and reuse. Creating new clients for every request adds unnecessary overhead.

### Model Selection Guide

| Model | Use Case | Speed | Cost | Context Window |
|-------|----------|-------|------|----------------|
| `gemini-2.0-flash-exp` | Fast responses, production agents | Fastest | Lowest | 1M tokens |
| `gemini-1.5-pro` | Complex reasoning, analysis | Medium | Medium | 2M tokens |
| `gemini-1.5-flash` | Balanced performance | Fast | Low | 1M tokens |

## Generation Parameters (Configuration Pattern)

### Core Parameters

```python
from google.genai import types

# Create generation configuration
config = types.GenerateContentConfig(
    temperature=0.7,        # Randomness (0.0 = deterministic, 2.0 = creative)
    top_p=0.95,            # Nucleus sampling threshold
    top_k=40,              # Top-k sampling (limits token pool)
    max_output_tokens=2048, # Maximum response length
    candidate_count=1,      # Number of responses to generate
    stop_sequences=["END"]  # Optional: Stop generation at these tokens
)

# Use config with model
response = await client.aio.models.generate_content(
    model=MODEL_ID,
    contents="Explain quantum computing",
    config=config
)
```

### Parameter Guidelines

**Temperature** (Controls randomness):
- `0.0-0.3`: Deterministic, factual responses (documentation, data extraction)
- `0.4-0.7`: Balanced creativity (general conversation, analysis)
- `0.8-1.2`: Creative writing (stories, brainstorming)
- `1.3-2.0`: Maximum creativity (experimental, art)

**Top-P** (Nucleus sampling):
- `0.9-0.95`: Recommended for most use cases
- `0.8-0.89`: More focused, less diverse outputs
- `0.96-1.0`: Maximum diversity

**Top-K** (Token pool size):
- `1-10`: Very focused (not recommended)
- `20-50`: Balanced (recommended)
- `100+`: Very diverse

**Max Output Tokens**:
- Set based on expected response length
- `512`: Short responses (summaries, answers)
- `2048`: Medium responses (explanations, code)
- `8192`: Long responses (essays, documentation)

## Safety Settings (Required Pattern)

### Comprehensive Safety Configuration

```python
from google.genai.types import (
    HarmCategory,
    HarmBlockThreshold,
    SafetySetting
)

# Define safety settings
safety_settings = [
    SafetySetting(
        category=HarmCategory.HARM_CATEGORY_HATE_SPEECH,
        threshold=HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
    ),
    SafetySetting(
        category=HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
        threshold=HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
    ),
    SafetySetting(
        category=HarmCategory.HARM_CATEGORY_HARASSMENT,
        threshold=HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
    ),
    SafetySetting(
        category=HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
        threshold=HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
    )
]

# Apply to generation config
config = types.GenerateContentConfig(
    temperature=0.7,
    safety_settings=safety_settings
)
```

### Harm Categories

| Category | Description | When to Block |
|----------|-------------|---------------|
| `HATE_SPEECH` | Content promoting hate based on protected characteristics | Always |
| `DANGEROUS_CONTENT` | Instructions for harmful activities | Always |
| `HARASSMENT` | Content intended to bully, intimidate, or threaten | Always |
| `SEXUALLY_EXPLICIT` | Sexual content | Application-dependent |

### Threshold Levels

| Threshold | Effect | Use Case |
|-----------|--------|----------|
| `BLOCK_NONE` | No blocking | Internal testing only |
| `BLOCK_ONLY_HIGH` | Block high-confidence harmful content | Liberal applications |
| `BLOCK_MEDIUM_AND_ABOVE` | Block medium+ confidence (RECOMMENDED) | Production |
| `BLOCK_LOW_AND_ABOVE` | Block low+ confidence | Conservative applications |

## Streaming Responses (Production Pattern)

### Async Streaming Implementation

```python
async def stream_response(prompt: str) -> None:
    """
    Generate streaming response with real-time output.

    Args:
        prompt: User prompt for the model
    """
    client = genai.Client(vertexai=True)

    # Use generate_content_stream for streaming
    async for chunk in client.aio.models.generate_content_stream(
        model=MODEL_ID,
        contents=prompt,
        config=types.GenerateContentConfig(temperature=0.7)
    ):
        # Process each chunk as it arrives
        if chunk.text:
            print(chunk.text, end="", flush=True)

    print()  # Newline after complete response
```

### Streaming with Error Handling

```python
import asyncio
from typing import AsyncIterator

async def safe_stream_response(
    prompt: str,
    timeout: float = 30.0
) -> AsyncIterator[str]:
    """
    Stream response with timeout and error handling.

    Args:
        prompt: User prompt
        timeout: Maximum time to wait for complete response

    Yields:
        Text chunks from the model
    """
    client = genai.Client(vertexai=True)

    try:
        stream = client.aio.models.generate_content_stream(
            model=MODEL_ID,
            contents=prompt
        )

        # Apply timeout to entire stream
        async for chunk in asyncio.wait_for(stream, timeout=timeout):
            if chunk.text:
                yield chunk.text

    except asyncio.TimeoutError:
        yield "\n[Response timed out]"
    except Exception as e:
        yield f"\n[Error: {str(e)}]"

# Usage
async for text in safe_stream_response("Explain AI"):
    print(text, end="", flush=True)
```

**Why Streaming?**
- Reduces perceived latency (first token arrives faster)
- Enables real-time UX (typing effect)
- Allows early termination if needed
- Better for long responses

## Function Calling (Integration Pattern)

### Basic Function Calling

```python
from pydantic import BaseModel, ConfigDict, Field

# Define tool schema
class CalculatorInput(BaseModel):
    """Calculator tool input."""
    model_config = ConfigDict(strict=True)

    operation: str = Field(description="Math operation: add, subtract, multiply, divide")
    a: float = Field(description="First number")
    b: float = Field(description="Second number")

# Create function declaration
calculator_function = types.FunctionDeclaration(
    name="calculator",
    description="Perform basic math operations",
    parameters=CalculatorInput.model_json_schema()
)

# Create tool
calculator_tool = types.Tool(
    function_declarations=[calculator_function]
)

# Use with model
response = await client.aio.models.generate_content(
    model=MODEL_ID,
    contents="What is 15 multiplied by 23?",
    config=types.GenerateContentConfig(
        tools=[calculator_tool]
    )
)

# Check for function call
if response.candidates[0].content.parts:
    for part in response.candidates[0].content.parts:
        if part.function_call:
            print(f"Function: {part.function_call.name}")
            print(f"Args: {part.function_call.args}")
```

### Automatic Function Execution Loop

```python
async def run_agent_with_tools(
    user_message: str,
    tools: list[types.Tool],
    max_iterations: int = 5
) -> str:
    """
    Run agent with automatic function execution.

    Args:
        user_message: Initial user message
        tools: List of available tools
        max_iterations: Max tool call iterations

    Returns:
        Final text response
    """
    client = genai.Client(vertexai=True)
    chat = client.aio.chats.create(
        model=MODEL_ID,
        config=types.GenerateContentConfig(tools=tools)
    )

    response = await chat.send_message(user_message)

    for _ in range(max_iterations):
        # Check if model wants to call a function
        if not response.candidates[0].content.parts:
            break

        function_calls = [
            part.function_call
            for part in response.candidates[0].content.parts
            if part.function_call
        ]

        if not function_calls:
            break  # No more function calls

        # Execute all function calls
        function_responses = []
        for fc in function_calls:
            # Execute function (implement your tool execution logic)
            result = await execute_tool(fc.name, fc.args)

            function_responses.append(
                types.Part(
                    function_response=types.FunctionResponse(
                        name=fc.name,
                        response=result
                    )
                )
            )

        # Send function results back to model
        response = await chat.send_message(
            types.Content(parts=function_responses)
        )

    return response.text
```

## Endpoint Selection (Regional vs Global)

### Regional Endpoints

```python
# US regional endpoint
client = genai.Client(
    vertexai=True,
    project="my-project",
    location="us-central1"  # Regional endpoint
)
```

**Advantages**:
- Data residency guarantees (data stays in region)
- Compliance with regional regulations
- Potentially lower latency for regional users

**Use When**:
- GDPR, HIPAA, or other compliance requirements
- Serving users in specific geographic region
- Data sovereignty requirements

### Global Endpoints

```python
# Global endpoint
client = genai.Client(
    vertexai=True,
    project="my-project",
    location="us"  # Global endpoint
)
```

**Advantages**:
- Higher availability
- Potential for better global latency
- Automatic failover

**Use When**:
- Global user base
- Maximum availability required
- No data residency constraints

### Claude on Vertex AI (Special Case)

For Claude models on Vertex AI, endpoint selection affects both performance and cost:

```python
# Regional endpoint required for Claude
client = genai.Client(
    vertexai=True,
    project="my-project",
    location="us-east5"  # Claude available in specific regions
)

model = "claude-3-5-sonnet@20241022"
```

**Note**: Check Vertex AI documentation for current regional availability of specific models.

## Anti-Patterns to Avoid

### Recreating Client for Every Request
```python
# BAD: Creates unnecessary overhead
async def bad_generate(prompt: str):
    client = genai.Client(vertexai=True)  # New client every time!
    return await client.aio.models.generate_content(...)

# GOOD: Reuse client
CLIENT = genai.Client(vertexai=True)  # Module-level singleton

async def good_generate(prompt: str):
    return await CLIENT.aio.models.generate_content(...)
```

### Ignoring Safety Settings
```python
# BAD: No safety configuration
config = types.GenerateContentConfig(temperature=0.7)

# GOOD: Explicit safety settings
config = types.GenerateContentConfig(
    temperature=0.7,
    safety_settings=[...]  # Always configure
)
```

### Not Handling Streaming Errors
```python
# BAD: No error handling
async for chunk in stream:
    print(chunk.text)

# GOOD: Comprehensive error handling
try:
    async for chunk in asyncio.wait_for(stream, timeout=30):
        if chunk.text:
            print(chunk.text)
except asyncio.TimeoutError:
    handle_timeout()
except Exception as e:
    handle_error(e)
```

### Vague Function Descriptions
```python
# BAD: Generic, unhelpful description
function = types.FunctionDeclaration(
    name="get_data",
    description="Gets data",  # Not helpful!
    ...
)

# GOOD: Specific, actionable description
function = types.FunctionDeclaration(
    name="get_weather",
    description="Get current weather conditions for a specific city including temperature, humidity, and forecast",
    ...
)
```

## When to Use This Skill

Activate this skill when:
- Configuring Gemini model parameters
- Implementing safety controls
- Building streaming response UIs
- Integrating function calling
- Selecting Vertex AI endpoints
- Tuning model behavior for specific use cases

## Integration Points

This skill is a **required dependency** for:
- `adk-fundamentals`: Model configuration is part of agent setup
- `prompt-engineering`: Model parameters affect prompt effectiveness
- `rag-patterns`: RAG requires proper model configuration

## Related Resources

For deeper understanding:
- **Vertex AI Model Parameters**: https://cloud.google.com/vertex-ai/generative-ai/docs/learn/prompts/adjust-parameter-values
- **Safety Settings Guide**: https://ai.google.dev/gemini-api/docs/safety-settings
- **Function Calling Reference**: https://cloud.google.com/vertex-ai/generative-ai/docs/model-reference/function-calling
- **Streaming Guide**: https://cloud.google.com/vertex-ai/generative-ai/docs/samples/generativeaionvertexai-stream-text-basic
- **Claude on Vertex AI**: https://docs.claude.com/en/api/claude-on-vertex-ai
