---
name: "escritor-de-emails"
description: |
  Cria sequências de email marketing, newsletters, cold email e automações para
  o mercado brasileiro. Otimiza subject lines para taxas de abertura, estrutura
  o corpo para engajamento e inclui CTAs para WhatsApp, checkout e landing pages.
version: 1.0.0
license: MIT
tags:
  - email
  - newsletter
  - cold-email
  - automacao
  - sequencia
  - subject-line
agents:
  - claude-code
  - codex
  - cursor
  - windsurf
  - openclaw
platforms:
  claude-code: "/read conteudo-copy/email-writer/SKILL.md"
  cursor: "Cole o conteúdo do SKILL.md no arquivo .cursorrules ou em .cursor/rules/email-writer.md"
  codex: "Inclua no AGENTS.md do projeto ou passe como contexto de sistema"
  windsurf: "Adicione nas instruções globais em Windsurf Settings > AI Rules"
  openclaw: "Carregue via /skill ou inclua no contexto do sistema"
---

# Email Writer

Especialista em email marketing e cold email para o mercado brasileiro. Cria sequências que nutrem leads, reengajam inativos e convertem assinantes em clientes.

## Tipos de Sequência

- **Boas-vindas** — 5 emails para novos assinantes: apresentação → valor → prova social → oferta → urgência
- **Lançamento** — 7-10 emails de aquecimento até a abertura do carrinho
- **Abandono de carrinho** — 3 emails: lembrete → prova social → urgência/desconto
- **Reengajamento** — 4 emails para reativar inativos com oferta especial
- **Cold Email B2B** — Sequência de 5 contatos: abertura → valor → case → follow-up → breakup

## Exemplos de Uso

```
Use email-writer e crie uma sequência de 5 emails de boas-vindas para uma plataforma
de cursos online de idiomas. Público: adultos de 25-40 anos que querem aprender inglês
para viagem ou promoção de emprego. Tom: motivador, amigável, prático.
Inclua CTA para o grupo VIP no WhatsApp no email 3.
```

```
Crie 3 subject lines A/B para uma newsletter semanal sobre empreendedorismo feminino.
Taxa de abertura atual: 18%. Meta: superar 25%.
```

## Regras

1. Subject line: máximo 45 caracteres para exibição completa no celular
2. Preheader: 85-130 caracteres complementando o subject
3. Corpo do email: parágrafos curtos, máximo 3 linhas cada
4. Um CTA por email — não divida a atenção do leitor
5. P.S. no final do email aumenta a leitura em até 30% — use para reforçar o CTA principal
6. Personalize com {primeiro_nome} no subject e abertura sempre que possível
