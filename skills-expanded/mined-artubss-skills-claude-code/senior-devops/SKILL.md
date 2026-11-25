---
name: senior-devops
description: Conjunto de habilidades DevOps abrangente para CI/CD, automação de infraestrutura, containerização e plataformas em nuvem (AWS, GCP, Azure). Inclui configuração de pipelines, infraestrutura como código, automação de deployment e monitoramento. Use ao configurar pipelines, implantar aplicações, gerenciar infraestrutura, implementar monitoramento ou otimizar processos de deployment.
---

# Senior Devops

Kit completo para DevOps sênior com ferramentas modernas e melhores práticas.

## Quick Start

### Principais Capacidades

Esta habilidade fornece três capacidades principais através de scripts automatizados:

```bash
# Script 1: Pipeline Generator
python scripts/pipeline_generator.py [options]

# Script 2: Terraform Scaffolder
python scripts/terraform_scaffolder.py [options]

# Script 3: Deployment Manager
python scripts/deployment_manager.py [options]
```

## Capacidades Principais

### 1. Pipeline Generator

Ferramenta automatizada para tarefas de geração de pipelines.

**Recursos:**
- Scaffolding automatizado
- Melhores práticas integradas
- Templates configuráveis
- Verificações de qualidade

**Uso:**
```bash
python scripts/pipeline_generator.py <project-path> [options]
```

### 2. Terraform Scaffolder

Ferramenta abrangente de análise e otimização.

**Recursos:**
- Análise profunda
- Métricas de desempenho
- Recomendações
- Correções automatizadas

**Uso:**
```bash
python scripts/terraform_scaffolder.py <target-path> [--verbose]
```

### 3. Deployment Manager

Ferramentas avançadas para tarefas especializadas.

**Recursos:**
- Automação de nível expert
- Configurações personalizadas
- Pronto para integração
- Output em nível de produção

**Uso:**
```bash
python scripts/deployment_manager.py [arguments] [options]
```

## Documentação de Referência

### Guia de Pipeline CI/CD

Guia abrangente disponível em `references/cicd_pipeline_guide.md`:

- Padrões e práticas detalhados
- Exemplos de código
- Melhores práticas
- Anti-padrões a evitar
- Cenários do mundo real

### Infraestrutura como Código

Documentação de workflow completa em `references/infrastructure_as_code.md`:

- Processos passo a passo
- Estratégias de otimização
- Integrações de ferramentas
- Ajuste de desempenho
- Guia de solução de problemas

### Estratégias de Deployment

Guia de referência técnica em `references/deployment_strategies.md`:

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

### 2. Execute Verificações de Qualidade

```bash
# Use the analyzer script
python scripts/terraform_scaffolder.py .

# Review recommendations
# Apply fixes
```

### 3. Implemente Melhores Práticas

Siga os padrões e práticas documentados em:
- `references/cicd_pipeline_guide.md`
- `references/infrastructure_as_code.md`
- `references/deployment_strategies.md`

## Resumo de Melhores Práticas

### Qualidade de Código
- Siga padrões estabelecidos
- Escreva testes abrangentes
- Documente decisões
- Revise regularmente

### Desempenho
- Meça antes de otimizar
- Use cache apropriado
- Otimize caminhos críticos
- Monitore em produção

### Segurança
- Valide todas as entradas
- Use consultas parametrizadas
- Implemente autenticação apropriada
- Mantenha dependências atualizadas

### Manutenibilidade
- Escreva código claro
- Use nomenclatura consistente
- Adicione comentários úteis
- Mantenha a simplicidade

## Comandos Comuns

```bash
# Development
npm run dev
npm run build
npm run test
npm run lint

# Analysis
python scripts/terraform_scaffolder.py .
python scripts/deployment_manager.py --analyze

# Deployment
docker build -t app:latest .
docker-compose up -d
kubectl apply -f k8s/
```

## Solução de Problemas

### Problemas Comuns

Verifique a seção abrangente de solução de problemas em `references/deployment_strategies.md`.

### Obtendo Ajuda

- Revise documentação de referência
- Verifique mensagens de saída dos scripts
- Consulte documentação da tech stack
- Revise logs de erro

## Recursos

- Pattern Reference: `references/cicd_pipeline_guide.md`
- Workflow Guide: `references/infrastructure_as_code.md`
- Technical Guide: `references/deployment_strategies.md`
- Tool Scripts: `scripts/` directory