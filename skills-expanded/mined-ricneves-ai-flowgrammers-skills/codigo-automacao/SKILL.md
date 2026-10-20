---
name: "codigo-automacao"
description: "Skills para desenvolvimento de software, debug, APIs, automações no-code e uso avançado de ferramentas de IA para desenvolvimento. Use quando precisar de diagnóstico de bugs, construção de APIs, containerização, testes automatizados, integrações ou engenharia de prompts."
version: 1.0.0
license: MIT
tags:
  - codigo
  - desenvolvimento
  - automacao
  - api
  - docker
  - testes
  - no-code
  - prompt-engineering
agents:
  - claude-code
  - codex
  - cursor
  - windsurf
  - openclaw
platforms:
  claude-code: "/read codigo-automacao/SKILL.md"
  cursor: "Cole o conteúdo do SKILL.md no arquivo .cursorrules ou em .cursor/rules/codigo-automacao.md"
  codex: "Inclua no AGENTS.md do projeto ou passe como contexto de sistema"
  windsurf: "Adicione nas instruções globais em Windsurf Settings > AI Rules"
  openclaw: "Carregue via /skill ou inclua no contexto do sistema"
---

# Código, Dev & Automação (Nível PODEROSO)

Skills para engenheiros e desenvolvedores que querem acelerar com IA. Cobrindo debug sistemático, construção de APIs, Docker, testes automatizados, banco de dados, autenticação, automações no-code com Make/n8n/Zapier e engenharia avançada de prompts. Cada skill traz um framework estruturado para atacar o problema com eficiência máxima.

## Início Rápido

### Claude Code
```
/read codigo-automacao/especialista-em-debug/SKILL.md
/read codigo-automacao/construtor-de-api/SKILL.md
/read codigo-automacao/docker-compose/SKILL.md
/read codigo-automacao/automacao-de-testes/SKILL.md
/read codigo-automacao/banco-de-dados-ops/SKILL.md
/read codigo-automacao/implementacao-de-auth/SKILL.md
/read codigo-automacao/no-code-automacao/SKILL.md
/read codigo-automacao/integrador-de-webhooks/SKILL.md
/read codigo-automacao/especialista-claude-code/SKILL.md
/read codigo-automacao/engenheiro-de-prompts/SKILL.md
```

### Cursor
Adicione em `.cursor/rules/codigo-automacao.md`:
```
Você é um engenheiro sênior especializado em debug sistemático e automação.
Ao diagnosticar bugs: sempre peça logs, stack traces e como reproduzir.
Para APIs: siga OpenAPI 3.0, documente todos os endpoints e erros possíveis.
Para testes: cobertura mínima de 80%, pirâmide de testes (unit > integration > E2E).
```

### Codex
Inclua no `AGENTS.md`:
```
## Engenheiro Sênior Dev & Automação
Consulte codigo-automacao/ para debug, APIs, Docker, testes e automações.
Sempre proponha solução com testes. Documente decisões de arquitetura.
```

## Visão Geral das Skills

| Skill | Pasta | Foco |
|-------|-------|------|
| Especialista em Debug | `especialista-em-debug/` | Diagnóstico sistemático de bugs |
| Construtor de API | `construtor-de-api/` | APIs REST e GraphQL com documentação |
| Docker Compose | `docker-compose/` | Containerização para dev e produção |
| Automação de Testes | `automacao-de-testes/` | Unit, integração, E2E com Playwright |
| Banco de Dados Ops | `banco-de-dados-ops/` | Queries, migrations, indexação, modelagem |
| Implementação de Auth | `implementacao-de-auth/` | JWT, OAuth 2.0, Supabase, Firebase |
| No-Code Automação | `no-code-automacao/` | Make, Zapier, n8n, ActivePieces |
| Integrador de Webhooks | `integrador-de-webhooks/` | Webhooks, eventos, filas de mensagens |
| Especialista Claude Code | `especialista-claude-code/` | Skills, subagentes, worktrees avançados |
| Engenheiro de Prompts | `engenheiro-de-prompts/` | Engenharia de prompts para LLMs |

## Exemplos de Uso

### Debug Expert
```
Use a skill de debug-expert. Tenho um erro 500 intermitente na minha API Node.js
em produção. Apenas acontece quando mais de 100 usuários usam simultaneamente.
Logs disponíveis: [cole os logs aqui]. Me dê um plano sistemático de diagnóstico.
```

### API Builder
```
Use api-builder para criar a documentação OpenAPI 3.0 completa da minha API
de pagamentos. Preciso de endpoints para criar cobrança PIX, consultar status,
webhook de confirmação e cancelamento. Inclua autenticação Bearer e exemplos.
```

### Docker Compose
```
Use docker-compose para criar configuração completa para minha aplicação:
backend Node.js, PostgreSQL, Redis para cache e Nginx como proxy reverso.
Preciso de configuração dev (com hot reload) e produção (com health checks).
```

### Test Automation
```
Use test-automation para criar suite completa de testes para meu módulo
de checkout. Preciso: unit tests para cálculo de frete, integration tests
para fluxo de pagamento e E2E com Playwright para jornada completa de compra.
```

### No-Code Automação
```
Use no-code-automacao para criar fluxo no Make (Integromat): quando novo
lead entrar no RD Station, criar contato no HubSpot, enviar email de boas-vindas
via SendGrid e notificar time comercial no Slack. Me dê o blueprint completo.
```

### Prompt Engineer
```
Use prompt-engineer para otimizar meu sistema de prompts para classificação
de tickets de suporte. Atualmente tenho 65% de precisão. Quero chegar a 90%+
usando chain-of-thought e few-shot examples. Analise meu prompt atual: [prompt]
```

## Contexto Brasileiro

### Stack Tecnológico Popular no Brasil
- **Backend:** Node.js (Express, Fastify, NestJS), Python (FastAPI, Django), PHP (Laravel)
- **Frontend:** React, Next.js, Vue.js, Angular
- **Mobile:** React Native, Flutter
- **Banco:** PostgreSQL, MySQL, MongoDB, Supabase
- **Cloud:** AWS (líder), Google Cloud, Azure, DigitalOcean, Hostinger VPS

### Integrações Brasileiras Comuns
| Integração | Tipo | Uso |
|-----------|------|-----|
| Mercado Pago | Pagamento | PIX, cartão, boleto |
| PagSeguro / PagBank | Pagamento | Muito popular em PMEs |
| Asaas / Iugu | Pagamento recorrente | SaaS B2B |
| RD Station | CRM/Marketing | Padrão de mercado BR |
| Conta Azul / Omie | ERP | Gestão fiscal |
| NF-e.io / Focus NFe | Fiscal | Emissão de notas fiscais |
| Z-API / Evolution API | WhatsApp | Automação WhatsApp Business |
| Juno / Celcash | Subconta | Marketplace financeiro |

### No-Code no Brasil
- **Make (Integromat):** Mais poderoso, curva de aprendizado média
- **n8n:** Open-source, self-hosted popular entre devs BR
- **Zapier:** Mais fácil, mas caro em BRL
- **ActivePieces:** Emergente, open-source, boa alternativa

### Práticas de Segurança Obrigatórias
- **LGPD:** Criptografar dados pessoais em repouso e em trânsito
- **OWASP Top 10:** Validar inputs, parameterized queries, HTTPS obrigatório
- **Auditoria:** Logs de acesso a dados sensíveis por 5 anos (recomendação LGPD)

## Configuração de Harness

### Claude Code — CLAUDE.md Global
Adicione ao seu `~/.claude/CLAUDE.md`:
```markdown
## Engenheiro Sênior Dev & Automação
Ao trabalhar em código:
- Debug: sempre pedir logs, stack trace e como reproduzir antes de propor fix
- APIs: seguir OpenAPI 3.0, documentar erros, usar códigos HTTP corretos
- Testes: propor testes junto com a implementação, cobertura mínima 80%
- Segurança: OWASP Top 10, LGPD para dados pessoais, HTTPS sempre
- Docker: health checks obrigatórios, não rodar como root, multi-stage builds
- Banco: sempre usar migrations versionadas, nunca ALTER TABLE direto em produção
```

### Cursor — .cursorrules
```
# Dev & Automação
- Engenheiro sênior com foco em qualidade e testabilidade
- Todo código novo deve ter testes (unit mínimo, integration quando necessário)
- APIs: OpenAPI 3.0, versionamento semântico, erros padronizados RFC 7807
- Banco de dados: migrations sempre, indexes para queries frequentes
- Segurança: nunca hardcode secrets, usar .env, validar todos os inputs
- Docker: multi-stage build, non-root user, health check obrigatório
- Integrações BR: considerar Mercado Pago, RD Station, NF-e, WhatsApp API
```

### Codex — AGENTS.md
```markdown
## Dev & Automação

Especialização:
- Diagnóstico sistemático de bugs com análise de logs e stack traces
- Construção de APIs REST/GraphQL com documentação OpenAPI
- Automações no-code: Make, n8n, Zapier, ActivePieces
- Integrações com serviços BR: Mercado Pago, RD Station, NF-e

Padrões obrigatórios:
- Testes antes de marcar tarefa como concluída
- Documentação inline (JSDoc/docstrings) para funções públicas
- Migrations versionadas para alterações de banco
```

## Regras

1. **Debug sistemático:** Nunca adivinhar a causa de um bug. Sempre: reproduzir > isolar > logs > hipótese > fix > teste
2. **APIs documentadas:** Todo endpoint deve ter OpenAPI 3.0 com exemplos de request/response e todos os erros possíveis
3. **Testes obrigatórios:** Código sem teste não está pronto. Mínimo: unit tests para lógica de negócio
4. **Segurança por padrão:** Validação de inputs, parameterized queries, HTTPS, secrets em variáveis de ambiente
5. **Docker production-ready:** Health checks, non-root user, multi-stage build, .dockerignore
6. **Migrations versionadas:** Nunca alterar schema de banco sem migration. Rollback sempre planejado
7. **No-code com documentação:** Toda automação deve ter diagrama de fluxo e descrição dos triggers
8. **Webhooks com retry:** Sempre implementar idempotência e retry com backoff exponencial
9. **LGPD no código:** Criptografar dados pessoais, logs sem PII, consentimento antes de coletar
10. **Carregue a skill específica** para o problema em questão — não tente usar todas de uma vez
