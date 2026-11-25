---
name: shopify-apps
description: "Padrões especializados para desenvolvimento de apps Shopify, incluindo apps Remix/React Router, apps incorporados com App Bridge, manipulação de webhooks, GraphQL Admin API, componentes Polaris, billing e extensões de app. Use quando: shopify app, shopify, embedded app, polaris, app bridge."
source: vibeship-spawner-skills (Apache 2.0)
---

# Shopify Apps

## Padrões

### Configuração de App React Router

Template moderno de app Shopify com React Router

### App Incorporado com App Bridge

Renderizar app incorporado no Shopify Admin

### Manipulação de Webhooks

Processamento seguro de webhooks com verificação HMAC

## Anti-Padrões

### ❌ REST API para Novos Apps

### ❌ Processamento de Webhook Antes da Resposta

### ❌ Polling em Vez de Webhooks

## ⚠️ Armadilhas

| Problema | Severidade | Solução |
|----------|-----------|---------|
| Problema | alta | ## Responder imediatamente, processar assincronamente |
| Problema | alta | ## Verificar headers de limite de taxa |
| Problema | alta | ## Solicitar acesso a dados de cliente protegidos |
| Problema | média | ## Usar apenas TOML (recomendado) |
| Problema | média | ## Lidar com ambos os formatos de URL |
| Problema | alta | ## Usar GraphQL para todo código novo |
| Problema | alta | ## Usar App Bridge mais recente via script tag |
| Problema | alta | ## Implementar todos os handlers GDPR |