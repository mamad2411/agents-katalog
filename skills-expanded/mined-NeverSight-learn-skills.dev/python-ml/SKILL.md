---
name: python-ml
description: "Machine Learning y AI en Python. Cubre NumPy, Pandas, scikit-learn, LangChain + OpenAI (GPT-5, embeddings), pgvector para búsqueda vectorial, y pipelines de datos. Actívala al implementar features de ML/AI, RAG, embeddings, o procesamiento de datos."
disable-model-invocation: true
---

# Python ML & AI

Guía de Machine Learning y AI en Python 3.14. Stack: LangChain + OpenAI + pgvector.

---

## Stack ML/AI 2026

| Propósito | Herramienta |
|-----------|-------------|
| Procesamiento de datos | Pandas, NumPy |
| ML tradicional | scikit-learn, XGBoost |
| LLM / Agentes | LangChain + OpenAI (GPT-5) |
| Embeddings | OpenAI embeddings + pgvector |
| Vector store | pgvector en PostgreSQL |
| Tracking | MLflow o W&B |

```bash
uv add langchain langchain-openai langchain-community
uv add pgvector numpy pandas scikit-learn
```

---

## LangChain + OpenAI

```python
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

# Inicializar modelo
llm = ChatOpenAI(
    model="gpt-5",  # GPT-5 en 2026
    temperature=0.7,
    max_tokens=4096,
)

# Chat simple
messages = [
    SystemMessage(content="You are a helpful order management assistant."),
    HumanMessage(content="Summarize the status of order #123"),
]
response = await llm.ainvoke(messages)
print(response.content)

# Streaming
async for chunk in llm.astream(messages):
    print(chunk.content, end="")
```

### Agentes con LangChain

```python
from langgraph.prebuilt import create_react_agent
from langchain_community.tools import TavilySearchResults
from langchain_openai import ChatOpenAI

# Agente con herramientas
tools = [
    TavilySearchResults(max_results=3),
]

agent = create_react_agent(
    model=ChatOpenAI(model="gpt-5"),
    tools=tools,
)

# Ejecutar agente
result = await agent.ainvoke({
    "messages": [HumanMessage(content="Find recent news about PostgreSQL 18")],
})
```

### RAG con LangChain + pgvector

```python
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import PGVector
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# Configurar embeddings
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

# Conexión a pgvector
CONNECTION_STRING = "postgresql+psycopg://user:pass@localhost:5432/miapp"

# Crear vector store (o cargar existente)
vectorstore = PGVector(
    connection_string=CONNECTION_STRING,
    embedding_function=embeddings,
    collection_name="order_documents",
)

# Indexar documentos
from langchain_core.documents import Document

docs = [
    Document(page_content="Order #123 was shipped on 2026-06-15", metadata={"order_id": "123"}),
    Document(page_content="Customer CUST-001 has 5 pending orders", metadata={"customer_id": "CUST-001"}),
]
await vectorstore.aadd_documents(docs)

# Búsqueda por similitud
results = vectorstore.similarity_search("Which orders are pending?", k=3)
for doc in results:
    print(doc.page_content)

# RAG: retrieval + generación
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
retrieved_docs = await retriever.ainvoke("shipping status")

context = "\n".join(doc.page_content for doc in retrieved_docs)
prompt = ChatPromptTemplate.from_messages([
    ("system", "Answer based on the following context:\n{context}"),
    ("human", "{question}"),
])

llm = ChatOpenAI(model="gpt-5")
chain = prompt | llm
response = await chain.ainvoke({"context": context, "question": "What was shipped on June 15?"})
```

---

## pgvector directo (sin LangChain)

```sql
-- Habilitar extensión
CREATE EXTENSION IF NOT EXISTS vector;

-- Tabla con embeddings
CREATE TABLE order_embeddings (
    order_id UUID PRIMARY KEY REFERENCES orders(id),
    embedding VECTOR(3072)  -- text-embedding-3-large = 3072
);

-- Índice HNSW (más rápido que IVFFlat)
CREATE INDEX ON order_embeddings USING hnsw (embedding vector_cosine_ops);
```

```python
import asyncpg
import numpy as np
from openai import AsyncOpenAI

client = AsyncOpenAI()
conn = await asyncpg.connect("postgresql://user:pass@localhost/miapp")

# Generar embedding
response = await client.embeddings.create(
    model="text-embedding-3-large",
    input="pending orders for customer CUST-001",
)
embedding = response.data[0].embedding

# Buscar similares
rows = await conn.fetch("""
    SELECT order_id, 1 - (embedding <=> $1::vector) AS similarity
    FROM order_embeddings
    ORDER BY embedding <=> $1::vector
    LIMIT 10
""", str(embedding))
```

---

## Pandas + NumPy — Procesamiento de datos

```python
import pandas as pd
import numpy as np

# Cargar datos
df = pd.read_sql("SELECT * FROM orders", engine)

# Agregaciones
monthly = (
    df.groupby(pd.Grouper(key="created_at", freq="ME"))
    .agg(
        total_orders=("id", "count"),
        revenue=("total_amount", "sum"),
        avg_order=("total_amount", "mean"),
    )
    .reset_index()
)

# Preparar features para ML
from sklearn.preprocessing import LabelEncoder

le = LabelEncoder()
df["status_encoded"] = le.fit_transform(df["status"])
df["day_of_week"] = df["created_at"].dt.dayofweek
df["hour"] = df["created_at"].dt.hour

# Features y target
X = df[["day_of_week", "hour", "total_amount"]]
y = df["status_encoded"]
```

---

## Scikit-learn — ML tradicional

```python
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import pickle

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Entrenar
model = RandomForestClassifier(n_estimators=100, max_depth=10)
model.fit(X_train, y_train)

# Evaluar
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

# Guardar modelo
with open("models/order_status_classifier.pkl", "wb") as f:
    pickle.dump(model, f)

# Predecir con el modelo entrenado
prediction = model.predict([[2, 14, 250.0]])
print(le.inverse_transform(prediction))  # → "shipped"
```

---

## Buenas prácticas ML

```python
# ✅ Validación de datos con Pandera (similar a Pydantic para DataFrames)
import pandera as pa

class OrderSchema(pa.DataFrameModel):
    id: str
    customer_id: str
    total_amount: float = pa.Field(gt=0)
    status: str = pa.Field(isin=["pending", "confirmed", "shipped"])

    @pa.dataframe_check
    def check_amount_positive(cls, df):
        return df["total_amount"] > 0

# Validar
OrderSchema.validate(df)

# ✅ MLflow tracking
import mlflow

mlflow.set_experiment("order-status-predictor")
with mlflow.start_run():
    mlflow.log_params({"n_estimators": 100, "max_depth": 10})
    mlflow.log_metric("accuracy", accuracy)
    mlflow.sklearn.log_model(model, "model")
```

---

## Checklist ML

- [ ] LangChain para RAG con pgvector
- [ ] OpenAI embeddings (text-embedding-3-large) + HNSW index
- [ ] Pandas para transformaciones y análisis
- [ ] Scikit-learn para ML tradicional (clasificación, regresión)
- [ ] Pandera para validación de DataFrames
- [ ] MLflow para tracking de experimentos
- [ ] Modelo guardado como .pkl (no en DB)
- [ ] Sin datos sensibles en prompts de LLM
- [ ] Rate limiting y caching para llamadas a OpenAI
