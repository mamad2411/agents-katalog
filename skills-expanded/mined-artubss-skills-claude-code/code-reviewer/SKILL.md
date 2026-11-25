---
name: code-reviewer
description: Habilidade abrangente de revisão de código para TypeScript, JavaScript, Python, Swift, Kotlin, Go. Inclui análise automatizada de código, verificação de boas práticas, scanning de segurança e geração de checklist de revisão. Use ao revisar pull requests, fornecer feedback de código, identificar problemas ou garantir padrões de qualidade de código.
---

# Code Reviewer

Kit completo para revisor de código com ferramentas modernas e boas práticas.

## Quick Start

### Capacidades Principais

Esta habilidade fornece três capacidades principais através de scripts automatizados:

```bash
# Script 1: Pr Analyzer
python scripts/pr_analyzer.py [options]

# Script 2: Code Quality Checker
python scripts/code_quality_checker.py [options]

# Script 3: Review Report Generator
python scripts/review_report_generator.py [options]
```

## Capacidades Principais

### 1. Pr Analyzer

Ferramenta automatizada para tarefas de análise de PR.

**Funcionalidades:**
- Scaffolding automatizado
- Boas práticas integradas
- Templates configuráveis
- Verificações de qualidade

**Uso:**
```bash
python scripts/pr_analyzer.py <project-path> [options]
```

### 2. Code Quality Checker

Ferramenta abrangente de análise e otimização.

**Funcionalidades:**
- Análise profunda
- Métricas de desempenho
- Recomendações
- Correções automatizadas

**Uso:**
```bash
python scripts/code_quality_checker.py <target-path> [--verbose]
```

### 3. Review Report Generator

Ferramentas avançadas para tarefas especializadas.

**Funcionalidades:**
- Automação em nível especializado
- Configurações personalizadas
- Pronto para integração
- Saída de nível produção

**Uso:**
```bash
python scripts/review_report_generator.py [arguments] [options]
```

## Documentação de Referência

### Checklist de Revisão de Código

Guia abrangente disponível em `references/code_review_checklist.md`:

- Padrões e práticas detalhadas
- Exemplos de código
- Boas práticas
- Anti-padrões a evitar
- Cenários do mundo real

### Padrões de Codificação

Documentação completa de workflow em `references/coding_standards.md`:

- Processos passo a passo
- Estratégias de otimização
- Integrações de ferramentas
- Ajuste de desempenho
- Guia de resolução de problemas

### Anti-padrões Comuns

Guia de referência técnica em `references/common_antipatterns.md`:

- Detalhes da stack tecnológica
- Exemplos de configuração
- Padrões de integração
- Considerações de segurança
- Diretrizes de escalabilidade

## Tech Stack

**Linguagens:** TypeScript, JavaScript, Python, Go, Swift, Kotlin
**Frontend:** React, Next.js, React Native, Flutter
**Backend:** Node.js, Express, GraphQL, REST APIs
**Banco de Dados:** PostgreSQL, Prisma, NeonDB, Supabase
**DevOps:** Docker, Kubernetes, Terraform, GitHub Actions, CircleCI
**Cloud:** AWS, GCP, Azure

## Workflow de Desenvolvimento

### 1. Configuração e Inicialização

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
python scripts/code_quality_checker.py .

# Revisar recomendações
# Aplicar correções
```

### 3. Implementar Boas Práticas

Siga os padrões e práticas documentados em:
- `references/code_review_checklist.md`
- `references/coding_standards.md`
- `references/common_antipatterns.md`

## Resumo de Boas Práticas

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
- Use queries parametrizadas
- Implemente autenticação apropriada
- Mantenha dependências atualizadas

### Manutenibilidade
- Escreva código claro
- Use nomenclatura consistente
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
python scripts/code_quality_checker.py .
python scripts/review_report_generator.py --analyze

# Deployment
docker build -t app:latest .
docker-compose up -d
kubectl apply -f k8s/
```

## Resolução de Problemas

### Problemas Comuns

Verifique a seção abrangente de resolução de problemas em `references/common_antipatterns.md`.

### Obtendo Ajuda

- Revise a documentação de referência
- Verifique as mensagens de saída do script
- Consulte a documentação da tech stack
- Revise os logs de erro

## Recursos

- Referência de Padrões: `references/code_review_checklist.md`
- Guia de Workflow: `references/coding_standards.md`
- Guia Técnico: `references/common_antipatterns.md`
- Scripts de Ferramentas: diretório `scripts/`