---
name: "ai-ml-pipeline"
description: "Kiến trúc AI/ML Pipeline: training workflows, model serving, vector databases và LLM integration."
---

# AI/ML Pipeline

> **Status:** Active | **Version:** 1.0.0

## When to Use

- Building AI-powered applications (chatbots, RAG, agents)
- Setting up ML training and inference pipelines
- Integrating LLMs (OpenAI, Anthropic, Google, local models)
- Building data processing and feature engineering workflows

## Core Patterns

### 1. LLM Integration (Vercel AI SDK)
```typescript
import { generateText, streamText, tool } from 'ai';
import { openai } from '@ai-sdk/openai';
import { z } from 'zod';

// Streaming response
const result = streamText({
  model: openai('gpt-4o'),
  messages: [{ role: 'user', content: prompt }],
  tools: {
    getWeather: tool({
      description: 'Get weather for a location',
      parameters: z.object({ city: z.string() }),
      execute: async ({ city }) => fetchWeather(city),
    }),
  },
  maxSteps: 5, // Multi-step tool use
});

// Structured output
const { object } = await generateObject({
  model: openai('gpt-4o'),
  schema: z.object({
    sentiment: z.enum(['positive', 'negative', 'neutral']),
    confidence: z.number().min(0).max(1),
    summary: z.string(),
  }),
  prompt: `Analyze: "${text}"`,
});
```

### 2. RAG Pipeline
```typescript
// 1. Embed documents
import { embedMany, embed } from 'ai';

const { embeddings } = await embedMany({
  model: openai.embedding('text-embedding-3-small'),
  values: documents.map(d => d.content),
});

// 2. Store in vector DB (Pinecone / Chroma / pgvector)
await vectorDB.upsert(
  documents.map((doc, i) => ({
    id: doc.id,
    values: embeddings[i],
    metadata: { source: doc.source, chunk: doc.chunk },
  }))
);

// 3. Query with context
async function ragQuery(question: string) {
  const { embedding } = await embed({
    model: openai.embedding('text-embedding-3-small'),
    value: question,
  });

  const results = await vectorDB.query({
    vector: embedding,
    topK: 5,
    includeMetadata: true,
  });

  return generateText({
    model: openai('gpt-4o'),
    system: `Answer based on context:\n${results.map(r => r.metadata.content).join('\n')}`,
    prompt: question,
  });
}
```

### 3. Agent Architecture
```typescript
// Multi-agent orchestration
interface Agent {
  name: string;
  description: string;
  execute(input: string, context: AgentContext): Promise<AgentResult>;
}

class Orchestrator {
  private agents: Map<string, Agent> = new Map();

  register(agent: Agent) {
    this.agents.set(agent.name, agent);
  }

  async run(task: string): Promise<string> {
    // 1. Route to appropriate agent
    const agent = await this.selectAgent(task);

    // 2. Execute with context
    const result = await agent.execute(task, this.context);

    // 3. Self-correct if needed
    if (result.confidence < 0.8) {
      return this.retry(agent, task, result.feedback);
    }

    return result.output;
  }
}
```

### 4. ML Training Pipeline (Python)
```python
# config-driven training pipeline
from dataclasses import dataclass
from pathlib import Path

@dataclass
class TrainingConfig:
    model_name: str = "bert-base-uncased"
    learning_rate: float = 2e-5
    batch_size: int = 32
    epochs: int = 3
    output_dir: Path = Path("./models")

class TrainingPipeline:
    def __init__(self, config: TrainingConfig):
        self.config = config

    def run(self):
        data = self.load_data()
        data = self.preprocess(data)
        model = self.train(data)
        metrics = self.evaluate(model, data.test)
        self.save(model, metrics)
        return metrics

    def load_data(self): ...
    def preprocess(self, data): ...
    def train(self, data): ...
    def evaluate(self, model, test_data): ...
    def save(self, model, metrics): ...
```

### 5. Model Serving
```python
# FastAPI model serving
from fastapi import FastAPI
from pydantic import BaseModel
import torch

app = FastAPI()

class PredictRequest(BaseModel):
    text: str

class PredictResponse(BaseModel):
    prediction: str
    confidence: float

# Load model once at startup
@app.on_event("startup")
async def load_model():
    app.state.model = torch.load("model.pt")
    app.state.model.eval()

@app.post("/predict", response_model=PredictResponse)
async def predict(request: PredictRequest):
    with torch.no_grad():
        result = app.state.model(request.text)
    return PredictResponse(
        prediction=result.label,
        confidence=result.score,
    )
```

## Architecture Patterns

### RAG System Architecture
```
User Query → Embedding → Vector Search → Context Assembly → LLM → Response
                              ↑
                    Document Ingestion Pipeline:
                    PDF/Web → Chunk → Embed → Store
```

### ML Pipeline Architecture
```
Data Source → ETL → Feature Store → Training → Model Registry → Serving → Monitoring
                                       ↑                          ↓
                                   Experiment                  A/B Test
                                   Tracking                   Feedback
```

## Key Dependencies (2026)

### TypeScript/JavaScript
| Package | Purpose |
|---------|---------|
| `ai` (Vercel AI SDK v5) | LLM integration |
| `@ai-sdk/openai` | OpenAI provider |
| `@ai-sdk/anthropic` | Anthropic provider |
| `@ai-sdk/google` | Google AI provider |
| `langchain` | Chain orchestration |
| `@pinecone-database/pinecone` | Vector DB |

### Python
| Package | Purpose |
|---------|---------|
| `transformers` | HuggingFace models |
| `torch` | PyTorch |
| `scikit-learn` | Classical ML |
| `fastapi` | Model serving |
| `mlflow` | Experiment tracking |
| `chromadb` | Vector DB |
| `langchain` | LLM orchestration |

## Quality Checklist
- [ ] Model versioning (MLflow / W&B)
- [ ] Input/output validation (Pydantic / Zod)
- [ ] Prompt injection protection
- [ ] Rate limiting on LLM calls
- [ ] Cost monitoring (token usage tracking)
- [ ] Hallucination detection / grounding
- [ ] Evaluation metrics (BLEU, ROUGE, human eval)
