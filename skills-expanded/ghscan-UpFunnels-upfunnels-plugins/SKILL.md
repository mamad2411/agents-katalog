---
name: crm
description: Consulta e altera contatos, leads de funil e números da organização na UpFunnels.
---

# Contatos e métricas

Use só estas ferramentas: `list_contacts`, `get_contact`, `create_contact`, `update_contact`, `delete_contact`, `export_contacts`, `list_funnel_leads`, `get_dashboard_metrics`, `get_funnel_metrics`.

- `list_contacts` lista contatos, com busca. Não entrega e-mail e telefone de toda a base.
- `get_contact` lê um contato pelo id.
- `create_contact` cria um contato. Não coloca em funil.
- `update_contact` atualiza nome, contato, status ou valor do negócio.
- `list_funnel_leads` lista quem está em cada etapa de um funil.
- `get_dashboard_metrics` devolve números da organização. Não devolve conversas.
- `get_funnel_metrics` devolve números de um funil.

Antes de `delete_contact` ou `export_contacts`, peça confirmação ao usuário. `delete_contact` apaga o contato. `export_contacts` exporta uma página da base com e-mail e telefone; não é arquivo CSV.
