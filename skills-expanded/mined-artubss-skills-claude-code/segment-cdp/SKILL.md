---
name: segment-cdp
description: "Padrões especializados para Segment Customer Data Platform incluindo Analytics.js, rastreamento server-side, planos de rastreamento com Protocols, resolução de identidade, configuração de destinos e melhores práticas de governança de dados. Use quando: segment, analytics.js, customer data platform, cdp, tracking plan."
source: vibeship-spawner-skills (Apache 2.0)
---

# Segment CDP

## Padrões

### Integração Analytics.js no Navegador

Rastreamento client-side com Analytics.js. Inclui chamadas track, identify, page e group. ID anônimo persiste até que identify mescle com o usuário.


### Rastreamento Server-Side com Node.js

Rastreamento server-side de alto desempenho usando @segment/analytics-node. Não-bloqueante com batching interno. Essencial para eventos backend, webhooks e dados sensíveis.


### Design de Plano de Rastreamento

Projete esquemas de eventos usando convenção Object + Action. Defina propriedades obrigatórias, tipos e regras de validação. Conecte aos Protocols para aplicação.


## Anti-Padrões

### ❌ Nomes de Eventos Dinâmicos

### ❌ Rastreamento de Propriedades como Eventos

### ❌ Identificação Ausente Antes de Track

## ⚠️ Arestas Agudas

| Problema | Severidade | Solução |
|----------|-----------|---------|
| Problema | média | Consulte docs |
| Problema | alta | Consulte docs |
| Problema | média | Consulte docs |
| Problema | alta | Consulte docs |
| Problema | baixa | Consulte docs |
| Problema | média | Consulte docs |
| Problema | média | Consulte docs |
| Problema | alta | Consulte docs |