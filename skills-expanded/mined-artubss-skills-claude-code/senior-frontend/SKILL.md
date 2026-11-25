---
name: senior-frontend
description: Ferramentas abrangentes de desenvolvimento frontend para construção de aplicações web modernas e de alto desempenho com ReactJS, NextJS, TypeScript, Tailwind CSS. Inclui scaffolding de componentes, otimização de performance, análise de bundle e boas práticas de UI. Use ao desenvolver features de frontend, otimizar performance, implementar designs de UI/UX, gerenciar estado ou revisar código frontend.
---

# Senior Frontend

Kit completo para frontend sênior com ferramentas modernas e boas práticas.

## Quick Start

### Capacidades Principais

Esta skill fornece três capacidades principais por meio de scripts automatizados:

```bash
# Script 1: Component Generator
python scripts/component_generator.py [options]

# Script 2: Bundle Analyzer
python scripts/bundle_analyzer.py [options]

# Script 3: Frontend Scaffolder
python scripts/frontend_scaffolder.py [options]
```

## Capacidades Principais

### 1. Component Generator

Ferramenta automatizada para tarefas de geração de componentes.

**Funcionalidades:**
- Scaffolding automatizado
- Boas práticas integradas
- Templates configuráveis
- Verificações de qualidade

**Uso:**
```bash
python scripts/component_generator.py <project-path> [options]
```

### 2. Bundle Analyzer

Ferramenta abrangente de análise e otimização.

**Funcionalidades:**
- Análise profunda
- Métricas de performance
- Recomendações
- Correções automatizadas

**Uso:**
```bash
python scripts/bundle_analyzer.py <target-path> [--verbose]
```

### 3. Frontend Scaffolder

Ferramentas avançadas para tarefas especializadas.

**Funcionalidades:**
- Automação em nível especializado
- Configurações personalizadas
- Pronto para integração
- Output em nível de produção

**Uso:**
```bash
python scripts/frontend_scaffolder.py [arguments] [options]
```

## Documentação de Referência

### React Patterns

Guia abrangente disponível em `references/react_patterns.md`:

- Padrões e práticas detalhados
- Exemplos de código
- Boas práticas
- Anti-padrões a evitar
- Cenários reais

### Nextjs Optimization Guide

Documentação completa de workflow em `references/nextjs_optimization_guide.md`:

- Processos passo a passo
- Estratégias de otimização
- Integrações de ferramentas
- Ajuste de performance
- Guia de solução de problemas

### Frontend Best Practices

Guia de referência técnica em `references/frontend_best_practices.md`:

- Detalhes da stack de tecnologia
- Exemplos de configuração
- Padrões de integração
- Considerações de segurança
- Diretrizes de escalabilidade

## Tech Stack

**Linguagens:** TypeScript, JavaScript, Python, Go, Swift, Kotlin
**Frontend:** React, Next.js, React Native, Flutter
**Backend:** Node.js, Express, GraphQL, REST APIs
**Database:** PostgreSQL, Prisma, NeonDB, Supabase
**DevOps:** Docker, Kubernetes, Terraform, GitHub Actions, CircleCI
**Cloud:** AWS, GCP, Azure

## Workflow de Desenvolvimento

### 1. Setup e Configuração

```bash
# Install dependencies
npm install
# or
pip install -r requirements.txt

# Configure environment
cp .env.example .env
```

### 2. Executar Verificações de Qualidade

```bash
# Use the analyzer script
python scripts/bundle_analyzer.py .

# Review recommendations
# Apply fixes
```

### 3. Implementar Boas Práticas

Siga os padrões e práticas documentados em:
- `references/react_patterns.md`
- `references/nextjs_optimization_guide.md`
- `references/frontend_best_practices.md`

## Resumo de Boas Práticas

### Qualidade de Código
- Siga padrões estabelecidos
- Escreva testes abrangentes
- Documente decisões
- Revise regularmente

### Performance
- Meça antes de otimizar
- Use cache apropriado
- Otimize caminhos críticos
- Monitore em produção

### Segurança
- Valide todas as entradas
- Use queries parametrizadas
- Implemente autenticação adequada
- Mantenha dependências atualizadas

### Manutenibilidade
- Escreva código claro
- Use nomes consistentes
- Adicione comentários úteis
- Mantenha simplicidade

## Comandos Comuns

```bash
# Development
npm run dev
npm run build
npm run test
npm run lint

# Analysis
python scripts/bundle_analyzer.py .
python scripts/frontend_scaffolder.py --analyze

# Deployment
docker build -t app:latest .
docker-compose up -d
kubectl apply -f k8s/
```

## Solução de Problemas

### Problemas Comuns

Consulte a seção abrangente de solução de problemas em `references/frontend_best_practices.md`.

### Obter Ajuda

- Revise documentação de referência
- Verifique mensagens de output dos scripts
- Consulte documentação da stack de tecnologia
- Revise logs de erro

## Recursos

- Pattern Reference: `references/react_patterns.md`
- Workflow Guide: `references/nextjs_optimization_guide.md`
- Technical Guide: `references/frontend_best_practices.md`
- Tool Scripts: `scripts/` directory