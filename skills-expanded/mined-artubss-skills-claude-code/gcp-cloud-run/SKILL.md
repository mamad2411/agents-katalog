---
name: gcp-cloud-run
description: "Habilidade especializada para criar aplicações serverless prontas para produção no GCP. Abrange serviços Cloud Run (containerizados), Cloud Run Functions (orientadas a eventos), otimização de cold start e arquitetura orientada a eventos com Pub/Sub."
source: vibeship-spawner-skills (Apache 2.0)
---

# GCP Cloud Run

## Padrões

### Padrão Cloud Run Service

Serviço web containerizado no Cloud Run

**Quando usar**: ['Aplicações web e APIs', 'Precisa de qualquer runtime ou biblioteca', 'Serviços complexos com múltiplos endpoints', 'Workloads containerizados sem estado']

```dockerfile
# Dockerfile - Build multi-stage para imagem menor
FROM node:20-slim AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

FROM node:20-slim
WORKDIR /app

# Copiar apenas dependências de produção
COPY --from=builder /app/node_modules ./node_modules
COPY src ./src
COPY package.json ./

# Cloud Run usa variável de ambiente PORT
ENV PORT=8080
EXPOSE 8080

# Executar como usuário não-root
USER node

CMD ["node", "src/index.js"]
```

```javascript
// src/index.js
const express = require('express');
const app = express();

app.use(express.json());

// Endpoint de health check
app.get('/health', (req, res) => {
  res.status(200).send('OK');
});

// Rotas de API
app.get('/api/items/:id', async (req, res) => {
  try {
    const item = await getItem(req.params.id);
    res.json(item);
  } catch (error) {
    console.error('Error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Shutdown gracioso
process.on('SIGTERM', () => {
  console.log('SIGTERM received, shutting down gracefully');
  server.close(() => {
    console.log('Server closed');
    process.exit(0);
  });
});

const PORT = process.env.PORT || 8080;
const server = app.listen(PORT, () => {
  console.log(`Server listening on port ${PORT}`);
});
```

```yaml
# cloudbuild.yaml
steps:
  # Build da imagem container
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'gcr.io/$PROJECT_ID/my-service:$COMMIT_SHA', '.']

  # Push da imagem container
  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'gcr.io/$PROJECT_ID/my-service:$COMMIT_SHA']

  # Deploy para Cloud Run
  - name: 'gcr.io/google.com/cloudsdktool/cloud-sdk'
    entrypoint: gcloud
    args:
      - 'run'
      - 'deploy'
      - 'my-service'
      - '--image=gcr.io/$PROJECT_ID/my-service:$COMMIT_SHA'
      - '--region=us-central1'
      - '--platform=managed'
      - '--allow-unauthenticated'
      - '--memory=512Mi'
      - '--cpu=1'
      - '--min-instances=1'
      - '--max-instances=100'
```

### Padrão Cloud Run Functions

Funções orientadas a eventos (anteriormente Cloud Functions)

**Quando usar**: ['Manipuladores de evento simples', 'Processamento de mensagens Pub/Sub', 'Triggers de Cloud Storage', 'Webhooks HTTP']

```javascript
// Função HTTP
// index.js
const functions = require('@google-cloud/functions-framework');

functions.http('helloHttp', (req, res) => {
  const name = req.query.name || req.body.name || 'World';
  res.send(`Hello, ${name}!`);
});
```

```javascript
// Função Pub/Sub
const functions = require('@google-cloud/functions-framework');

functions.cloudEvent('processPubSub', (cloudEvent) => {
  // Decodificar mensagem Pub/Sub
  const message = cloudEvent.data.message;
  const data = message.data
    ? JSON.parse(Buffer.from(message.data, 'base64').toString())
    : {};

  console.log('Received message:', data);

  // Processar mensagem
  processMessage(data);
});
```

```javascript
// Função Cloud Storage
const functions = require('@google-cloud/functions-framework');

functions.cloudEvent('processStorageEvent', async (cloudEvent) => {
  const file = cloudEvent.data;

  console.log(`Event: ${cloudEvent.type}`);
  console.log(`Bucket: ${file.bucket}`);
  console.log(`File: ${file.name}`);

  if (cloudEvent.type === 'google.cloud.storage.object.v1.finalized') {
    await processUploadedFile(file.bucket, file.name);
  }
});
```

```bash
# Deploy de função HTTP
gcloud functions deploy hello-http \
  --gen2 \
  --runtime nodejs20 \
  --trigger-http \
  --allow-unauthenticated \
  --region us-central1

# Deploy de função Pub/Sub
gcloud functions deploy process-messages \
  --gen2 \
  --runtime nodejs20 \
  --trigger-topic my-topic \
  --region us-central1

# Deploy de função Cloud Storage
gcloud functions deploy process-uploads \
  --gen2 \
  --runtime nodejs20 \
  --trigger-event-filters="type=google.cloud.storage.object.v1.finalized" \
  --trigger-event-filters="bucket=my-bucket" \
  --region us-central1
```

### Padrão Cold Start Optimization

Minimizar latência de cold start no Cloud Run

**Quando usar**: ['Aplicações sensíveis à latência', 'APIs voltadas ao usuário', 'Serviços de alto tráfego']

## 1. Ativar CPU Boost de Startup

```bash
gcloud run deploy my-service \
  --cpu-boost \
  --region us-central1
```

## 2. Definir Instâncias Mínimas

```bash
gcloud run deploy my-service \
  --min-instances 1 \
  --region us-central1
```

## 3. Otimizar Imagem Container

```dockerfile
# Usar distroless para imagem minimal
FROM node:20-slim AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

FROM gcr.io/distroless/nodejs20-debian12
WORKDIR /app
COPY --from=builder /app/node_modules ./node_modules
COPY src ./src
CMD ["src/index.js"]
```

## 4. Inicializar Dependências Pesadas com Lazy Loading

```javascript
// Carregar bibliotecas pesadas sob demanda
let bigQueryClient = null;

function getBigQueryClient() {
  if (!bigQueryClient) {
    const { BigQuery } = require('@google-cloud/bigquery');
    bigQueryClient = new BigQuery();
  }
  return bigQueryClient;
}

// Inicializar apenas quando necessário
app.get('/api/analytics', async (req, res) => {
  const client = getBigQueryClient();
  const results = await client.query({...});
  res.json(results);
});
```

## 5. Aumentar Memória (Mais CPU)

```bash
# Mais memória = mais CPU durante startup
gcloud run deploy my-service \
  --memory 1Gi \
  --cpu 2 \
  --region us-central1
```

## Anti-Padrões

### ❌ Trabalho Intensivo de CPU Sem Concurrency=1

**Por que é ruim**: CPU é compartilhada entre requisições concorrentes. Trabalho CPU-bound vai consumir recursos de outras requisições, causando timeouts.

### ❌ Escrever Arquivos Grandes em /tmp

**Por que é ruim**: /tmp é um sistema de arquivos em memória. Arquivos grandes consomem sua alocação de memória e podem causar erros OOM.

### ❌ Tarefas de Background de Longa Duração

**Por que é ruim**: Cloud Run reduz CPU quase a zero quando não está processando requisições. Tarefas de background serão extremamente lentas ou podem travar.

## ⚠️ Pontos Críticos

| Problema | Severidade | Solução |
|----------|-----------|---------|
| Problema | alta | ## Calcular memória incluindo uso de /tmp |
| Problema | alta | ## Definir concorrência apropriada |
| Problema | alta | ## Ativar CPU sempre alocada |
| Problema | média | ## Configurar pool de conexão com keep-alive |
| Problema | alta | ## Ativar CPU boost de startup |
| Problema | média | ## Definir explicitamente ambiente de execução |
| Problema | média | ## Definir timeouts consistentes |