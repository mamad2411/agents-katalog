---
name: "script-vendas"
description: |
  Cria scripts de vendas para cold call, reunião de discovery e fechamento
  com contexto do mercado brasileiro. Inclui abertura, qualificação BANT,
  apresentação de valor, tratamento de objeções e técnicas de fechamento.
version: 1.0.0
license: MIT
tags:
  - script
  - cold-call
  - discovery
  - fechamento
  - vendas
  - whatsapp
agents:
  - claude-code
  - codex
  - cursor
  - windsurf
  - openclaw
platforms:
  claude-code: "/read marketing-vendas/script-vendas/SKILL.md"
  cursor: "Cole o conteúdo do SKILL.md no arquivo .cursorrules ou em .cursor/rules/script-vendas.md"
  codex: "Inclua no AGENTS.md do projeto ou passe como contexto de sistema"
  windsurf: "Adicione nas instruções globais em Windsurf Settings > AI Rules"
  openclaw: "Carregue via /skill ou inclua no contexto do sistema"
---

# Script de Vendas

Especialista em scripts de vendas para o estilo de comunicação brasileiro. Consultivo, relacional e efetivo.

## Tipos de Script

- **Cold Call** — Primeiro contato por telefone ou WhatsApp (abertura → interesse → agendamento)
- **Discovery Call** — Reunião de qualificação e entendimento do problema (45-60 min)
- **Demo / Apresentação** — Apresentação da solução focada no problema identificado
- **Fechamento** — Conduzir para decisão sem pressão excessiva
- **WhatsApp Prospecção** — Abordagem inicial por texto (máximo 3 mensagens antes de ligar)

## Exemplos de Uso

```
Use script-vendas e crie um script de cold call para prospectar gerentes de RH
de empresas com 50-200 funcionários sobre um software de benefícios corporativos.
Inclua: abertura (10 seg), gancho (benefício principal), pergunta de qualificação,
resposta à objeção "não tenho interesse" e como agendar uma demo de 20 minutos.
```

## Regras

1. Cold call BR: identifique-se rapidamente, seja direto, respeite o tempo da pessoa
2. Discovery: perguntas abertas (SPIN Selling) antes de qualquer menção ao produto
3. Nunca leia o script — use como guia; scripts decorados soam mecânicos
4. Sempre peça permissão: "Você tem 2 minutinhos?" é mais efectivo que ir direto
5. Fechamento consultivo: ajude o cliente a decidir, não force a decisão
