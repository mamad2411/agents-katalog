---
name: docs-export
description: Gera um documento Markdown detalhado sobre o problema resolvido na conversa atual e salva em docs/. Invocar EXCLUSIVAMENTE quando o usuário disser "enviar para minha pasta docs", "salvar na docs" ou "documentar isso".
---

# Docs Export

Exporta o diagnóstico completo da conversa atual para a pasta `docs/` do projeto como um arquivo Markdown legível e reutilizável.

**Gatilho obrigatório:** este skill só deve ser executado quando o usuário disser explicitamente "enviar para minha pasta docs", "salvar na docs" ou "documentar isso". Em nenhum outro contexto este skill deve ser acionado automaticamente.

**Modo de escrita:** este skill cria um único arquivo em `docs/`. É proibido editar qualquer outro arquivo do projeto durante a execução.

---

## Fase 1 — Extração de Contexto

Antes de escrever qualquer coisa, analise toda a conversa atual e extraia:

- **Título do problema** — uma frase curta que descreve o que foi resolvido
- **Data** — use a data atual disponível no contexto do sistema
- **Migrations ou arquivos envolvidos** — liste todos os arquivos criados ou modificados
- **A motivação** — qual risco, bug ou necessidade gerou a tarefa
- **A abordagem escolhida** — por que foi feita dessa forma e não de outra
- **Os passos técnicos** — o que cada trecho de código ou configuração faz
- **Resultados de testes** — saídas reais de comandos executados durante a conversa
- **Limitações ou observações** — qualquer ressalva técnica levantada durante a solução

**Gate: não prossiga para a Fase 2 sem ter todos os itens acima identificados.**

---

## Fase 2 — Geração do Nome do Arquivo

Monte o nome do arquivo seguindo o padrão:

```
YYYY-MM-DD-<slug-do-titulo>.md
```

Regras do slug:
- Letras minúsculas
- Palavras separadas por hífen
- Sem acentos ou caracteres especiais
- Máximo de 6 palavras

Exemplos:
- `2026-05-08-separacao-usuarios-permissoes-banco.md`
- `2026-05-08-rate-limiting-redis-login.md`
- `2026-05-08-auditoria-logs-append-only.md`

---

## Fase 3 — Estrutura do Documento

Gere o conteúdo do arquivo seguindo **obrigatoriamente** esta estrutura:

```markdown
# <Título do Problema>

**Data:** YYYY-MM-DD
**Arquivos envolvidos:** lista dos arquivos criados/modificados

---

## Contexto

<Por que esse problema existia? Qual era o risco ou necessidade?>

---

## Por que essa abordagem?

<Explique a decisão técnica: por que A e não B, quais padrões foram seguidos,
quais problemas a solução evita, como se alinha com as convenções do projeto.
Esta seção é a mais importante — não seja superficial.>

---

## O que foi feito — Passo a Passo

<Para cada arquivo ou bloco de código relevante, explique o que ele faz e por quê.
Use blocos de código com syntax highlighting quando pertinente.>

---

## Resultado dos Testes

<Saídas reais dos comandos executados durante a conversa. Use tabelas quando aplicável.>

---

## Observações e Limitações

<Ressalvas técnicas, dívidas técnicas identificadas, ou próximos passos recomendados.
Se não houver nenhuma, escreva: "Nenhuma limitação identificada.">
```

---

## Fase 4 — Escrita e Confirmação

1. Verifique se a pasta `docs/` existe no projeto. Se não existir, crie-a.
2. Escreva o arquivo com o nome gerado na Fase 2 dentro de `docs/`.
3. Confirme ao usuário com uma mensagem curta no formato:

```
Salvo em docs/<nome-do-arquivo>.md
```

Não adicione nenhum outro texto além dessa confirmação. O usuário já sabe o que o arquivo contém — ele pediu.