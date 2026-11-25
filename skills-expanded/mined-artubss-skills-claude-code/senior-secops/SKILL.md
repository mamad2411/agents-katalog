---
name: senior-secops
description: Kit completo de SecOps para segurança de aplicações, gerenciamento de vulnerabilidades, conformidade e práticas de desenvolvimento seguro. Inclui verificação de segurança, avaliação de vulnerabilidades, verificação de conformidade e automação de segurança. Use ao implementar controles de segurança, conduzir auditorias de segurança, responder a vulnerabilidades ou garantir conformidade regulatória.
---

# Senior Secops

Conjunto completo de ferramentas para SecOps sênior com práticas e ferramentas modernas.

## Início Rápido

### Capacidades Principais

Esta skill fornece três capacidades principais por meio de scripts automatizados:

```bash
# Script 1: Security Scanner
python scripts/security_scanner.py [options]

# Script 2: Vulnerability Assessor
python scripts/vulnerability_assessor.py [options]

# Script 3: Compliance Checker
python scripts/compliance_checker.py [options]
```

## Capacidades Principais

### 1. Security Scanner

Ferramenta automatizada para tarefas de verificação de segurança.

**Recursos:**
- Scaffolding automatizado
- Melhores práticas integradas
- Templates configuráveis
- Verificações de qualidade

**Uso:**
```bash
python scripts/security_scanner.py <project-path> [options]
```

### 2. Vulnerability Assessor

Ferramenta abrangente de análise e otimização.

**Recursos:**
- Análise profunda
- Métricas de performance
- Recomendações
- Correções automatizadas

**Uso:**
```bash
python scripts/vulnerability_assessor.py <target-path> [--verbose]
```

### 3. Compliance Checker

Ferramentas avançadas para tarefas especializadas.

**Recursos:**
- Automação em nível de especialista
- Configurações customizáveis
- Pronto para integração
- Output de qualidade produtiva

**Uso:**
```bash
python scripts/compliance_checker.py [arguments] [options]
```

## Documentação de Referência

### Padrões de Segurança

Guia abrangente disponível em `references/security_standards.md`:

- Padrões e práticas detalhadas
- Exemplos de código
- Melhores práticas
- Anti-padrões a evitar
- Cenários do mundo real

### Guia de Gerenciamento de Vulnerabilidades

Documentação de fluxo de trabalho completa em `references/vulnerability_management_guide.md`:

- Processos passo a passo
- Estratégias de otimização
- Integrações de ferramentas
- Ajuste de performance
- Guia de solução de problemas

### Requisitos de Conformidade

Guia de referência técnica em `references/compliance_requirements.md`:

- Detalhes da pilha tecnológica
- Exemplos de configuração
- Padrões de integração
- Considerações de segurança
- Diretrizes de escalabilidade

## Pilha Tecnológica

**Linguagens:** TypeScript, JavaScript, Python, Go, Swift, Kotlin
**Frontend:** React, Next.js, React Native, Flutter
**Backend:** Node.js, Express, GraphQL, REST APIs
**Banco de Dados:** PostgreSQL, Prisma, NeonDB, Supabase
**DevOps:** Docker, Kubernetes, Terraform, GitHub Actions, CircleCI
**Cloud:** AWS, GCP, Azure

## Fluxo de Desenvolvimento

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
python scripts/vulnerability_assessor.py .

# Review recommendations
# Apply fixes
```

### 3. Implemente Melhores Práticas

Siga os padrões e práticas documentadas em:
- `references/security_standards.md`
- `references/vulnerability_management_guide.md`
- `references/compliance_requirements.md`

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
- Implemente autenticação adequada
- Mantenha dependências atualizadas

### Manutenibilidade
- Escreva código claro
- Use nomenclatura consistente
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
python scripts/vulnerability_assessor.py .
python scripts/compliance_checker.py --analyze

# Deployment
docker build -t app:latest .
docker-compose up -d
kubectl apply -f k8s/
```

## Solução de Problemas

### Problemas Comuns

Consulte a seção abrangente de solução de problemas em `references/compliance_requirements.md`.

### Obtendo Ajuda

- Revise a documentação de referência
- Verifique as mensagens de saída dos scripts
- Consulte a documentação da pilha tecnológica
- Revise os logs de erro

## Recursos

- Referência de Padrões: `references/security_standards.md`
- Guia de Fluxo de Trabalho: `references/vulnerability_management_guide.md`
- Guia Técnico: `references/compliance_requirements.md`
- Scripts de Ferramentas: diretório `scripts/`