---
name: senior-security
description: Kit de ferramentas completo de engenharia de segurança para segurança de aplicações, testes de penetração, arquitetura de segurança e auditoria de conformidade. Inclui ferramentas de avaliação de segurança, modelagem de ameaças, implementação de criptografia e automação de segurança. Use ao projetar arquitetura de segurança, conduzir testes de penetração, implementar criptografia ou realizar auditorias de segurança.
---

# Senior Security

Kit completo para segurança sênior com ferramentas modernas e melhores práticas.

## Quick Start

### Principais Capacidades

Esta skill oferece três capacidades principais por meio de scripts automatizados:

```bash
# Script 1: Threat Modeler
python scripts/threat_modeler.py [options]

# Script 2: Security Auditor
python scripts/security_auditor.py [options]

# Script 3: Pentest Automator
python scripts/pentest_automator.py [options]
```

## Capacidades Principais

### 1. Threat Modeler

Ferramenta automatizada para tarefas de modelagem de ameaças.

**Recursos:**
- Scaffolding automatizado
- Melhores práticas integradas
- Templates configuráveis
- Verificações de qualidade

**Uso:**
```bash
python scripts/threat_modeler.py <project-path> [options]
```

### 2. Security Auditor

Ferramenta abrangente de análise e otimização.

**Recursos:**
- Análise profunda
- Métricas de desempenho
- Recomendações
- Correções automatizadas

**Uso:**
```bash
python scripts/security_auditor.py <target-path> [--verbose]
```

### 3. Pentest Automator

Ferramentas avançadas para tarefas especializadas.

**Recursos:**
- Automação em nível especialista
- Configurações personalizadas
- Pronto para integração
- Saída pronta para produção

**Uso:**
```bash
python scripts/pentest_automator.py [arguments] [options]
```

## Documentação de Referência

### Padrões de Arquitetura de Segurança

Guia abrangente disponível em `references/security_architecture_patterns.md`:

- Padrões e práticas detalhadas
- Exemplos de código
- Melhores práticas
- Anti-padrões a evitar
- Cenários do mundo real

### Guia de Teste de Penetração

Documentação completa de workflow em `references/penetration_testing_guide.md`:

- Processos passo a passo
- Estratégias de otimização
- Integrações de ferramentas
- Ajuste de desempenho
- Guia de solução de problemas

### Implementação de Criptografia

Guia de referência técnica em `references/cryptography_implementation.md`:

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
# Instalar dependências
npm install
# ou
pip install -r requirements.txt

# Configurar ambiente
cp .env.example .env
```

### 2. Executar Verificações de Qualidade

```bash
# Use o script de análise
python scripts/security_auditor.py .

# Revise as recomendações
# Aplique as correções
```

### 3. Implementar Melhores Práticas

Siga os padrões e práticas documentados em:
- `references/security_architecture_patterns.md`
- `references/penetration_testing_guide.md`
- `references/cryptography_implementation.md`

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
- Implemente autenticação adequada
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
python scripts/security_auditor.py .
python scripts/pentest_automator.py --analyze

# Deploy
docker build -t app:latest .
docker-compose up -d
kubectl apply -f k8s/
```

## Solução de Problemas

### Problemas Comuns

Consulte a seção abrangente de solução de problemas em `references/cryptography_implementation.md`.

### Obtendo Ajuda

- Revise a documentação de referência
- Verifique mensagens de saída do script
- Consulte a documentação da tech stack
- Revise logs de erros

## Recursos

- Referência de Padrões: `references/security_architecture_patterns.md`
- Guia de Workflow: `references/penetration_testing_guide.md`
- Guia Técnico: `references/cryptography_implementation.md`
- Scripts de Ferramentas: diretório `scripts/`