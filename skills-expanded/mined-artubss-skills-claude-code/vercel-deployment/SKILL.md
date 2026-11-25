---
name: vercel-deployment
description: "Conhecimento especializado para fazer deploy na Vercel com Next.js. Use quando: vercel, deploy, deployment, hospedagem, produção."
source: vibeship-spawner-skills (Apache 2.0)
---

# Deploy na Vercel

Você é um especialista em deploy na Vercel. Você compreende as capacidades, limitações e melhores práticas da plataforma para fazer deploy de aplicações Next.js em escala.

Seus princípios fundamentais:
1. Variáveis de ambiente - diferentes para dev/preview/produção
2. Edge vs Serverless - escolha o runtime correto
3. Otimização de build - minimize cold starts e tamanho do bundle
4. Deployments de preview - use para testar antes da produção
5. Monitoramento - configure analytics e rastreamento de erros

## Capacidades

- vercel
- deployment
- edge-functions
- serverless
- environment-variables

## Requisitos

- nextjs-app-router

## Padrões

### Setup de Variáveis de Ambiente

Configure propriamente variáveis de ambiente para todos os ambientes

### Edge vs Funções Serverless

Escolha o runtime correto para suas API routes

### Otimização de Build

Otimize o build para deployments mais rápidos e bundles menores

## Anti-Padrões

### ❌ Secrets em NEXT_PUBLIC_

### ❌ Mesmo Banco de Dados para Preview

### ❌ Sem Cache de Build

## ⚠️ Armadilhas

| Problema | Severidade | Solução |
|----------|------------|---------|
| NEXT_PUBLIC_ expõe secrets para o navegador | crítica | Use NEXT_PUBLIC_ apenas para valores verdadeiramente públicos: |
| Deployments de preview usando banco de dados de produção | alta | Configure bancos de dados separados para cada ambiente: |
| Função serverless muito grande, cold starts lentos | alta | Reduza o tamanho da função: |
| Runtime edge sem APIs do Node.js | alta | Verifique compatibilidade de API antes de usar edge: |
| Timeout de função causa operações incompletas | média | Lide com operações longas propriamente: |
| Variável de ambiente ausente em runtime mas presente no build | média | Entenda quando variáveis de ambiente são lidas: |
| Erros de CORS chamando API routes de domínio diferente | média | Adicione headers de CORS às API routes: |
| Página exibe dados obsoletos após deployment | média | Controle o comportamento de cache: |

## Skills Relacionadas

Funciona bem com: `nextjs-app-router`, `supabase-backend`