---
name: create-pi-web-extension
description: >
  Como criar/extender extensões web no pi com arquitetura determinística,
  segurança mínima e testes automatizados (smoke + e2e via pi-test-harness).
---

# Criando Extensões Web para Pi (sem acoplamento frágil)

Use este skill quando o usuário quiser:
- expor estado da sessão em HTTP
- criar UI web para acompanhar trabalho do agente
- enviar ações da web para o pi de forma controlada

## Princípios

1. **URL determinística por modo** (`local | lan | public`)
2. **Sem depender de domínio externo** para UI essencial
3. **Health endpoint explícito** (`/api/health`)
4. **Estado por contrato** (`/api/state`)
5. **Ações autenticadas** (`POST /api/prompt` com token)
6. **Sem acoplar ao caso colony** — colony é apenas um produtor de sinais

## Referência first-party no lab

- Extensão: `packages/pi-stack/extensions/web-session-gateway.ts`
- Guia: `docs/guides/web-session-gateway.md`
- E2E harness: `packages/pi-stack/test/smoke/web-session-gateway-e2e-harness.test.ts`

## Processo recomendado

### 1) Definir contrato primeiro

Antes de codar, declarar:
- modos suportados (`local|lan|public`)
- endpoints (`health`, `state`, `action`)
- esquema mínimo de resposta (campos estáveis)
- requisito de autenticação (token/header/query)

### 2) Implementar mínimo vertical

- comando `/session-web start|status|open|stop`
- tool `session_web_status`
- backend HTTP mínimo
- UI web mínima (pode ser polling)

### 3) Testes obrigatórios

- **Smoke**: funções puras de resolução de host/url/config
- **E2E (pi-test-harness)**:
  - sobe servidor local
  - valida `health` 200
  - valida `state` sem token = 401
  - valida atualização de estado com sinal fake
  - valida integração com outra extensão por capability (não por suposição)

### 4) Só então evoluir UI

Evoluir para SSE/WebSocket, histórico rico, comandos avançados etc.

## Checklist de qualidade

- [ ] Funciona sem internet
- [ ] Não exige domínio externo para UI básica
- [ ] Não usa heurística opaca de IP sem override
- [ ] Tem fallback claro para `localhost`
- [ ] Tem teste para comportamento de erro (401/404/payload inválido)
- [ ] Tem teste de integração com fluxo real (harness)

## Anti-padrões

- Depender de `hosted UI` sem fallback local
- Misturar observabilidade web com regra de negócio de colony
- Expor endpoint mutável sem token
- Declarar “deve funcionar” sem e2e automatizado

## Snippet de direção para o agente

Use este framing ao delegar implementação:

> "Implemente web gateway first-party com contrato estável (`/api/health`, `/api/state`, `/api/prompt`), URL determinística por modo, token auth e e2e em `pi-test-harness`. Não acople ao fluxo de colony; trate colony como produtor opcional de telemetria."
