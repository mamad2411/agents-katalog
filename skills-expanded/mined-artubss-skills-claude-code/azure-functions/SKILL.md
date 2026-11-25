---
name: azure-functions
description: "Padrões especialistas para desenvolvimento com Azure Functions, incluindo modelo isolated worker, orquestração de Durable Functions, otimização de cold start e padrões de produção. Cobre modelos de programação .NET, Python e Node.js. Use quando: azure function, azure functions, durable functions, azure serverless, function app."
source: vibeship-spawner-skills (Apache 2.0)
---

# Azure Functions

## Padrões

### Isolated Worker Model (.NET)

Modelo de execução .NET moderno com isolamento de processo

### Node.js v4 Programming Model

Abordagem moderna focada em código para TypeScript/JavaScript

### Python v2 Programming Model

Abordagem baseada em decoradores para funções Python

## Anti-Padrões

### ❌ Bloqueio de Chamadas Async

### ❌ Novo HttpClient Por Requisição

### ❌ Modelo In-Process para Novos Projetos

## ⚠️ Pontos Críticos

| Problema | Severidade | Solução |
|----------|-----------|---------|
| Problema | alta | ## Use padrão async com Durable Functions |
| Problema | alta | ## Use IHttpClientFactory (Recomendado) |
| Problema | alta | ## Sempre use async/await |
| Problema | média | ## Configure tempo máximo de execução (Consumption) |
| Problema | alta | ## Use isolated worker para novos projetos |
| Problema | média | ## Configure Application Insights corretamente |
| Problema | média | ## Verifique extension bundle (mais comum) |
| Problema | média | ## Adicione warmup trigger para inicializar seu código |