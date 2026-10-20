---
name: Proposal Monitor Domain
description: Regras de domínio do Proposal Monitor para modelagem de usuários, propostas, contas de e-mail e entidades comerciais.
---

# Proposal Monitor Domain

Skill para garantir consistência funcional no backend do Proposal Monitor.

## Quando Usar

- Ao alterar modelos `Proposal`, `EmailAccount`, `Person`, `Company`, `Work`.
- Ao alterar ingestão/processamento de e-mails.
- Ao revisar políticas de acesso a propostas.
- Ao criar ou ajustar fluxos de upsert via LLM.

## Regras de Domínio

1. Usuários são funcionários internos do cliente SaaS.
2. Propostas são globais e compartilhadas entre usuários autenticados.
3. `Proposal` não possui dono (`user_id`).
4. `EmailAccount` pertence a `User` e `Person`.
5. `Person` pertence a `Company`.
6. `Work` é única por `identity_key` (nome + local normalizados) e deve persistir `state`, `city`, `address`, `zipcode` quando disponíveis.
7. A LLM só deve marcar `is_proposal=true` para e-mails ligados a proposta/cotação/serviço/obra; demais e-mails devem ser ignorados.
8. Upsert de proposta atualiza somente campos vazios.

## Checklist de Mudança

- [ ] Migration aplicada e schema atualizado.
- [ ] Models com associações/validações consistentes.
- [ ] Policies e queries alinhadas às regras de visibilidade.
- [ ] Services de ingestão/análise/upsert sem regressão.
- [ ] Factories e specs atualizadas.
- [ ] Teste de fluxo real: `EmailMessage pending -> Analyze -> Upsert`.
