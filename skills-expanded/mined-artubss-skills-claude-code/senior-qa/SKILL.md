---
name: senior-qa
description: Kit de ferramentas abrangente para QA e testes, incluindo automação de testes e estratégias de testes para aplicações ReactJS, NextJS e NodeJS. Compreende geração de suite de testes, análise de cobertura, configuração de testes E2E e métricas de qualidade. Use ao projetar estratégias de teste, escrever casos de teste, implementar automação de testes, realizar testes manuais ou analisar cobertura de testes.
---

# Senior QA

Kit de ferramentas completo para senior QA com ferramentas modernas e melhores práticas.

## Início Rápido

### Principais Capacidades

Esta skill oferece três capacidades centrais por meio de scripts automatizados:

```bash
# Script 1: Test Suite Generator
python scripts/test_suite_generator.py [options]

# Script 2: Coverage Analyzer
python scripts/coverage_analyzer.py [options]

# Script 3: E2E Test Scaffolder
python scripts/e2e_test_scaffolder.py [options]
```

## Capacidades Centrais

### 1. Gerador de Suite de Testes

Ferramenta automatizada para tarefas de geração de suite de testes.

**Recursos:**
- Scaffolding automatizado
- Melhores práticas integradas
- Templates configuráveis
- Verificações de qualidade

**Uso:**
```bash
python scripts/test_suite_generator.py <project-path> [options]
```

### 2. Analisador de Cobertura

Ferramenta abrangente de análise e otimização.

**Recursos:**
- Análise profunda
- Métricas de desempenho
- Recomendações
- Correções automatizadas

**Uso:**
```bash
python scripts/coverage_analyzer.py <target-path> [--verbose]
```

### 3. Scaffolder de Testes E2E

Ferramentas avançadas para tarefas especializadas.

**Recursos:**
- Automação em nível especializado
- Configurações personalizadas
- Pronto para integração
- Output de qualidade produção

**Uso:**
```bash
python scripts/e2e_test_scaffolder.py [arguments] [options]
```

## Documentação de Referência

### Estratégias de Testes

Guia abrangente disponível em `references/testing_strategies.md`:

- Padrões e práticas detalhados
- Exemplos de código
- Melhores práticas
- Anti-padrões a evitar
- Cenários do mundo real

### Padrões de Automação de Testes

Documentação completa de workflow em `references/test_automation_patterns.md`:

- Processos passo a passo
- Estratégias de otimização
- Integrações de ferramentas
- Ajuste de desempenho
- Guia de resolução de problemas

### Melhores Práticas de QA

Guia de referência técnica em `references/qa_best_practices.md`:

- Detalhes da stack de tecnologia
- Exemplos de configuração
- Padrões de integração
- Considerações de segurança
- Diretrizes de escalabilidade

## Stack Tecnológico

**Linguagens:** TypeScript, JavaScript, Python, Go, Swift, Kotlin
**Frontend:** React, Next.js, React Native, Flutter
**Backend:** Node.js, Express, GraphQL, REST APIs
**Banco de Dados:** PostgreSQL, Prisma, NeonDB, Supabase
**DevOps:** Docker, Kubernetes, Terraform, GitHub Actions, CircleCI
**Cloud:** AWS, GCP, Azure

## Workflow de Desenvolvimento

### 1. Configuração e Setup

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
# Usar o script analisador
python scripts/coverage_analyzer.py .

# Revisar recomendações
# Aplicar correções
```

### 3. Implementar Melhores Práticas

Siga os padrões e práticas documentados em:
- `references/testing_strategies.md`
- `references/test_automation_patterns.md`
- `references/qa_best_practices.md`

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
python scripts/coverage_analyzer.py .
python scripts/e2e_test_scaffolder.py --analyze

# Deploy
docker build -t app:latest .
docker-compose up -d
kubectl apply -f k8s/
```

## Resolução de Problemas

### Problemas Comuns

Consulte a seção abrangente de resolução de problemas em `references/qa_best_practices.md`.

### Obtendo Ajuda

- Revise a documentação de referência
- Verifique as mensagens de saída dos scripts
- Consulte a documentação da stack tecnológica
- Revise logs de erro

## Recursos

- Referência de Padrões: `references/testing_strategies.md`
- Guia de Workflow: `references/test_automation_patterns.md`
- Guia Técnico: `references/qa_best_practices.md`
- Scripts de Ferramentas: diretório `scripts/`