---
name: senior-fullstack
description: Kit completo de desenvolvimento fullstack sênior com ferramentas modernas e melhores práticas. Inclui scaffolding de projetos, análise de qualidade de código, padrões de arquitetura e orientação completa de stack tecnológico. Use ao construir novos projetos, analisar qualidade de código, implementar padrões de design ou configurar workflows de desenvolvimento.
---

# Senior Fullstack

Kit completo para desenvolvimento fullstack sênior com ferramentas modernas e melhores práticas.

## Quick Start

### Capacidades Principais

Esta skill fornece três capacidades principais através de scripts automatizados:

```bash
# Script 1: Fullstack Scaffolder
python scripts/fullstack_scaffolder.py [options]

# Script 2: Project Scaffolder
python scripts/project_scaffolder.py [options]

# Script 3: Code Quality Analyzer
python scripts/code_quality_analyzer.py [options]
```

## Capacidades Principais

### 1. Fullstack Scaffolder

Ferramenta automatizada para tarefas de scaffolding fullstack.

**Recursos:**
- Scaffolding automatizado
- Melhores práticas integradas
- Templates configuráveis
- Verificações de qualidade

**Uso:**
```bash
python scripts/fullstack_scaffolder.py <project-path> [options]
```

### 2. Project Scaffolder

Ferramenta abrangente de análise e otimização.

**Recursos:**
- Análise profunda
- Métricas de performance
- Recomendações
- Correções automatizadas

**Uso:**
```bash
python scripts/project_scaffolder.py <target-path> [--verbose]
```

### 3. Code Quality Analyzer

Ferramentas avançadas para tarefas especializadas.

**Recursos:**
- Automação em nível especializado
- Configurações personalizadas
- Integração pronta
- Output em nível de produção

**Uso:**
```bash
python scripts/code_quality_analyzer.py [arguments] [options]
```

## Documentação de Referência

### Guia de Stack Tecnológico

Guia abrangente disponível em `references/tech_stack_guide.md`:

- Padrões e práticas detalhados
- Exemplos de código
- Melhores práticas
- Anti-padrões a evitar
- Cenários do mundo real

### Padrões de Arquitetura

Documentação completa de workflow em `references/architecture_patterns.md`:

- Processos passo a passo
- Estratégias de otimização
- Integrações de ferramentas
- Ajuste de performance
- Guia de troubleshooting

### Workflows de Desenvolvimento

Guia de referência técnica em `references/development_workflows.md`:

- Detalhes da stack tecnológica
- Exemplos de configuração
- Padrões de integração
- Considerações de segurança
- Diretrizes de escalabilidade

## Stack Tecnológico

**Linguagens:** TypeScript, JavaScript, Python, Go, Swift, Kotlin
**Frontend:** React, Next.js, React Native, Flutter
**Backend:** Node.js, Express, GraphQL, REST APIs
**Database:** PostgreSQL, Prisma, NeonDB, Supabase
**DevOps:** Docker, Kubernetes, Terraform, GitHub Actions, CircleCI
**Cloud:** AWS, GCP, Azure

## Workflow de Desenvolvimento

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
# Use o script do analyzer
python scripts/project_scaffolder.py .

# Revise as recomendações
# Aplique as correções
```

### 3. Implementar Melhores Práticas

Siga os padrões e práticas documentadas em:
- `references/tech_stack_guide.md`
- `references/architecture_patterns.md`
- `references/development_workflows.md`

## Resumo de Melhores Práticas

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
- Implemente autenticação apropriada
- Mantenha dependências atualizadas

### Manutenibilidade
- Escreva código claro
- Use nomenclatura consistente
- Adicione comentários úteis
- Mantenha simples

## Comandos Comuns

```bash
# Desenvolvimento
npm run dev
npm run build
npm run test
npm run lint

# Análise
python scripts/project_scaffolder.py .
python scripts/code_quality_analyzer.py --analyze

# Deployment
docker build -t app:latest .
docker-compose up -d
kubectl apply -f k8s/
```

## Troubleshooting

### Problemas Comuns

Consulte a seção completa de troubleshooting em `references/development_workflows.md`.

### Obtendo Ajuda

- Revise a documentação de referência
- Verifique as mensagens de saída dos scripts
- Consulte a documentação do stack tecnológico
- Revise logs de erro

## Recursos

- Pattern Reference: `references/tech_stack_guide.md`
- Workflow Guide: `references/architecture_patterns.md`
- Technical Guide: `references/development_workflows.md`
- Tool Scripts: `scripts/` directory