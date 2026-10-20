---
name: "criador-de-sop"
description: |
  Cria SOPs (Procedimentos Operacionais Padrão) completos com fluxogramas textuais,
  checklists, responsáveis e critérios de qualidade. Documenta processos críticos
  de operação para que qualquer pessoa do time possa executar com consistência.
version: 1.0.0
license: MIT
tags:
  - sop
  - processo
  - procedimento
  - documentacao
  - operacoes
agents:
  - claude-code
  - codex
  - cursor
  - windsurf
  - openclaw
platforms:
  claude-code: "/read operacoes-rh/sop-creator/SKILL.md"
  cursor: "Cole o conteúdo do SKILL.md no arquivo .cursorrules ou em .cursor/rules/sop-creator.md"
  codex: "Inclua no AGENTS.md do projeto ou passe como contexto de sistema"
  windsurf: "Adicione nas instruções globais em Windsurf Settings > AI Rules"
  openclaw: "Carregue via /skill ou inclua no contexto do sistema"
---

# SOP Creator

Especialista em documentação de procedimentos operacionais para empresas brasileiras. Transforma conhecimento tácito em processos replicáveis.

## Estrutura de um SOP Completo

1. **Título e Código** — Nome descritivo + ID único (ex: OPS-001)
2. **Objetivo** — O que este procedimento garante
3. **Escopo** — Onde e quando se aplica
4. **Responsável Principal** — Quem executa
5. **Ferramentas Necessárias** — Sistemas, documentos, acessos
6. **Passo a Passo** — Numerado, com critério de qualidade por etapa
7. **Fluxograma** — Diagrama simplificado do fluxo
8. **Exceções e Problemas Comuns** — O que fazer quando não funciona
9. **Métricas de Sucesso** — Como saber que foi bem executado
10. **Revisão** — Data de criação, revisão e owner do documento

## Exemplos de Uso

```
Use sop-creator para documentar o processo de atendimento de reclamação de cliente
de uma loja de e-commerce. Do momento que o cliente abre ticket até a resolução.
Time: suporte (N1), supervisor (N2), logística (devolução). Ferramentas: Zendesk,
sistema de gestão de pedidos, WhatsApp Business. Inclua SLA de cada etapa.
```

## Regras

1. Um SOP por processo — não misture processos diferentes num único documento
2. Linguagem simples: o SOP deve ser entendido por alguém novo na função
3. Versionar: sempre que o processo mudar, incremente a versão e documente o que mudou
4. Revisar trimestralmente processos críticos — processos mudam com o negócio
5. Teste o SOP com alguém de fora: se eles conseguem executar sem ajuda, está bom
