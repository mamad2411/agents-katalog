---
name: plaid-fintech
description: "Padrões especializados para integração da API Plaid incluindo fluxos de Link token, sincronização de transações, verificação de identidade, Auth para ACH, verificação de saldo, tratamento de webhooks e melhores práticas de conformidade fintech. Use quando: plaid, vinculação de conta bancária, conexão bancária, ach, agregação de contas."
source: vibeship-spawner-skills (Apache 2.0)
---

# Plaid Fintech

## Padrões

### Criação e Troca de Link Token

Crie um link_token para Plaid Link e troque public_token por access_token.
Link tokens são de curta duração e uso único. Access tokens não expiram, mas
podem precisar de atualização quando usuários alteram senhas.


### Sincronização de Transações

Use /transactions/sync para atualizações incrementais de transações. Mais eficiente
que /transactions/get. Trate webhooks para atualizações em tempo real em vez de
polling.


### Tratamento de Erros de Item e Modo de Atualização

Trate erros ITEM_LOGIN_REQUIRED colocando usuários no modo de atualização do Link.
Ouça o webhook PENDING_DISCONNECT para solicitar proativamente que os usuários façam atualização.

## Anti-Padrões

### ❌ Armazenar Access Tokens em Texto Simples

### ❌ Polling em Vez de Webhooks

### ❌ Ignorar Erros de Item

## ⚠️ Pontos Delicados

| Problema | Severidade | Solução |
|----------|-----------|---------|
| Problema | crítica | Veja docs |
| Problema | alta | Veja docs |
| Problema | alta | Veja docs |
| Problema | alta | Veja docs |
| Problema | média | Veja docs |
| Problema | média | Veja docs |
| Problema | média | Veja docs |
| Problema | média | Veja docs |