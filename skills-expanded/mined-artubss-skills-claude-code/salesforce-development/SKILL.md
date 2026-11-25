---
name: salesforce-development
description: "Padrões especializados para desenvolvimento da plataforma Salesforce, incluindo Lightning Web Components (LWC), triggers e classes Apex, APIs REST/Bulk, Connected Apps e Salesforce DX com scratch orgs e pacotes de 2ª geração (2GP). Use quando: salesforce, sfdc, apex, lwc, lightning web components."
source: vibeship-spawner-skills (Apache 2.0)
---

# Desenvolvimento Salesforce

## Padrões

### Lightning Web Component com Wire Service

Use o decorator @wire para data binding reativo com Lightning Data Service
ou métodos Apex. @wire se encaixa na arquitetura reativa do LWC e permite
otimizações de performance do Salesforce.


### Trigger Apex Bulkificada com Padrão Handler

Triggers Apex devem ser bulkificadas para processar 200+ registros por transação.
Use o padrão handler para separação de responsabilidades, testabilidade e
prevenção de recursão.


### Queueable Apex para Processamento Assíncrono

Use Queueable Apex para processamento assíncrono com suporte a tipos não-primitivos,
monitoramento via AsyncApexJob e encadeamento de jobs. Limite: 50 jobs
por transação, 1 job filho ao encadear.


## Anti-Padrões

### ❌ SOQL Dentro de Loops

### ❌ DML Dentro de Loops

### ❌ Hardcoding de IDs

## ⚠️ Armadilhas Críticas

| Problema | Severidade | Solução |
|----------|-----------|---------|
| Problema | crítica | Ver docs |
| Problema | alta | Ver docs |
| Problema | média | Ver docs |
| Problema | alta | Ver docs |
| Problema | crítica | Ver docs |
| Problema | alta | Ver docs |
| Problema | alta | Ver docs |
| Problema | crítica | Ver docs |