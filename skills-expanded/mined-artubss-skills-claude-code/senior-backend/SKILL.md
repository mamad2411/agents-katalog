---
name: senior-backend
description: Kit completo de desenvolvimento backend para construir sistemas backend escaláveis usando NodeJS, Express, Go, Python, Postgres, GraphQL, REST APIs. Inclui scaffolding de API, otimização de banco de dados, implementação de segurança e ajuste de desempenho. Use ao projetar APIs, otimizar consultas de banco de dados, implementar lógica de negócios, lidar com autenticação/autorização ou revisar código backend.
---

# Senior Backend

Kit completo para backend sênior com ferramentas modernas e melhores práticas.

## Início Rápido

### Principais Capacidades

Esta skill fornece três capacidades principais através de scripts automatizados:

```bash
# Script 1: Api Scaffolder
python scripts/api_scaffolder.py [options]

# Script 2: Database Migration Tool
python scripts/database_migration_tool.py [options]

# Script 3: Api Load Tester
python scripts/api_load_tester.py [options]
```

## Capacidades Principais

### 1. Api Scaffolder

Ferramenta automatizada para tarefas de scaffolding de API.

**Funcionalidades:**
- Scaffolding automatizado
- Melhores práticas embutidas
- Templates configuráveis
- Verificações de qualidade

**Uso:**
```bash
python scripts/api_scaffolder.py <project-path> [options]
```

### 2. Database Migration Tool

Ferramenta abrangente de análise e otimização.

**Funcionalidades:**
- Análise profunda
- Métricas de desempenho
- Recomendações
- Correções automatizadas

**Uso:**
```bash
python scripts/database_migration_tool.py <target-path> [--verbose]
```

### 3. Api Load Tester

Ferramentas avançadas para tarefas especializadas.

**Funcionalidades:**
- Automação em nível especialista
- Configurações personalizadas
- Pronto para integração
- Output de nível produção

**Uso:**
```bash
python scripts/api_load_tester.py [arguments] [options]
```

## Documentação de Referência

### Padrões de Design de API

Guia completo disponível em `references/api_design_patterns.md`:

- Padrões e práticas detalhados
- Exemplos de código
- Melhores práticas
- Anti-patterns a evitar
- Cenários do mundo real

### Guia de Otimização de Banco de Dados

Documentação de workflow completa em `references/database_optimization_guide.md`:

- Processos passo a passo
- Estratégias de otimização
- Integrações de ferramentas
- Ajuste de desempenho
- Guia de troubleshooting

### Práticas de Segurança Backend

Guia de referência técnica em `references/backend_security_practices.md`:

- Detalhes da stack de tecnologia
- Exemplos de configuração
- Padrões de integração
- Considerações de segurança
- Diretrizes de escalabilidade

## Stack de Tecnologia

**Linguagens:** TypeScript, JavaScript, Python, Go, Swift, Kotlin
**Frontend:** React, Next.js, React Native, Flutter
**Backend:** Node.js, Express, GraphQL, REST APIs
**Banco de Dados:** PostgreSQL, Prisma, NeonDB, Supabase
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
# Use o script analyzer
python scripts/database_migration_tool.py .

# Revise as recomendações
# Aplique as correções
```

### 3. Implementar Melhores Práticas

Siga os padrões e práticas documentados em:
- `references/api_design_patterns.md`
- `references/database_optimization_guide.md`
- `references/backend_security_practices.md`

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
python scripts/database_migration_tool.py .
python scripts/api_load_tester.py --analyze

# Deploy
docker build -t app:latest .
docker-compose up -d
kubectl apply -f k8s/
```

## Troubleshooting

### Problemas Comuns

Verifique a seção abrangente de troubleshooting em `references/backend_security_practices.md`.

### Obtendo Ajuda

- Revise a documentação de referência
- Verifique mensagens de output do script
- Consulte a documentação da stack de tecnologia
- Revise logs de erro

## Recursos

- Referência de Padrões: `references/api_design_patterns.md`
- Guia de Workflow: `references/database_optimization_guide.md`
- Guia Técnico: `references/backend_security_practices.md`
- Scripts de Ferramentas: diretório `scripts/`