---
name: senior-architect
description: Competência abrangente de arquitetura de software para design de sistemas escaláveis e mantíveis usando ReactJS, NextJS, NodeJS, Express, React Native, Swift, Kotlin, Flutter, Postgres, GraphQL, Go, Python. Inclui geração de diagramas de arquitetura, padrões de design de sistemas, frameworks de decisão de tech stack e análise de dependências. Use ao projetar arquitetura de sistemas, tomar decisões técnicas, criar diagramas de arquitetura, avaliar trade-offs ou definir padrões de integração.
---

# Senior Architect

Kit completo para arquiteto sênior com ferramentas modernas e melhores práticas.

## Quick Start

### Principais Funcionalidades

Esta competência fornece três funcionalidades principais através de scripts automatizados:

```bash
# Script 1: Architecture Diagram Generator
python scripts/architecture_diagram_generator.py [options]

# Script 2: Project Architect
python scripts/project_architect.py [options]

# Script 3: Dependency Analyzer
python scripts/dependency_analyzer.py [options]
```

## Funcionalidades Principais

### 1. Architecture Diagram Generator

Ferramenta automatizada para tarefas de geração de diagramas de arquitetura.

**Funcionalidades:**
- Scaffolding automatizado
- Melhores práticas integradas
- Templates configuráveis
- Verificações de qualidade

**Uso:**
```bash
python scripts/architecture_diagram_generator.py <project-path> [options]
```

### 2. Project Architect

Ferramenta abrangente de análise e otimização.

**Funcionalidades:**
- Análise profunda
- Métricas de performance
- Recomendações
- Correções automatizadas

**Uso:**
```bash
python scripts/project_architect.py <target-path> [--verbose]
```

### 3. Dependency Analyzer

Ferramental avançada para tarefas especializadas.

**Funcionalidades:**
- Automação de nível expert
- Configurações customizadas
- Pronto para integração
- Output em nível de produção

**Uso:**
```bash
python scripts/dependency_analyzer.py [arguments] [options]
```

## Documentação de Referência

### Padrões de Arquitetura

Guia abrangente disponível em `references/architecture_patterns.md`:

- Padrões e práticas detalhados
- Exemplos de código
- Melhores práticas
- Anti-padrões a evitar
- Cenários do mundo real

### Fluxos de Design de Sistemas

Documentação completa de fluxos em `references/system_design_workflows.md`:

- Processos passo a passo
- Estratégias de otimização
- Integrações de ferramentas
- Tuning de performance
- Guia de troubleshooting

### Guia de Decisão Técnica

Guia de referência técnica em `references/tech_decision_guide.md`:

- Detalhes de tech stack
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

## Fluxo de Desenvolvimento

### 1. Setup e Configuração

```bash
# Instalar dependências
npm install
# ou
pip install -r requirements.txt

# Configurar ambiente
cp .env.example .env
```

### 2. Executar Verificações de Qualidade

```bash
# Use o script analyzer
python scripts/project_architect.py .

# Revise as recomendações
# Aplique as correções
```

### 3. Implementar Melhores Práticas

Siga os padrões e práticas documentados em:
- `references/architecture_patterns.md`
- `references/system_design_workflows.md`
- `references/tech_decision_guide.md`

## Resumo de Melhores Práticas

### Qualidade de Código
- Siga padrões estabelecidos
- Escreva testes abrangentes
- Documente decisões
- Revise regularmente

### Performance
- Meça antes de otimizar
- Use caching apropriado
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
- Mantenha a simplicidade

## Comandos Comuns

```bash
# Desenvolvimento
npm run dev
npm run build
npm run test
npm run lint

# Análise
python scripts/project_architect.py .
python scripts/dependency_analyzer.py --analyze

# Deployment
docker build -t app:latest .
docker-compose up -d
kubectl apply -f k8s/
```

## Troubleshooting

### Problemas Comuns

Verifique a seção abrangente de troubleshooting em `references/tech_decision_guide.md`.

### Obtendo Ajuda

- Revise a documentação de referência
- Verifique as mensagens de saída dos scripts
- Consulte a documentação da tech stack
- Revise os logs de erro

## Recursos

- Referência de Padrões: `references/architecture_patterns.md`
- Guia de Fluxos: `references/system_design_workflows.md`
- Guia Técnico: `references/tech_decision_guide.md`
- Scripts de Ferramentas: diretório `scripts/`