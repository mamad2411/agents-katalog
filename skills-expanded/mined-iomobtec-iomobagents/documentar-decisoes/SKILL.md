---
name: documentar-decisoes
description: "Cria ADRs em docs/decisions com contexto, alternativas e consequências, nunca deletando e apenas supersedendo decisões anteriores. Use quando uma decisão arquitetural relevante precisa ser registrada."
author: "Pedro Andriow (https://github.com/Andriow)"
disable-model-invocation: true
---

# Skill: documentar-decisoes

Registrar decisões técnicas e arquiteturais como ADRs (Architecture Decision Records) — documentos imutáveis que preservam o contexto de "por que fizemos dessa forma", não apenas "o que fizemos".

**Agente:** `arquiteto`, `tech-lead`  
**Referências rápidas:** `References/adr-template.md`

---

## Quando usar

- Ao tomar qualquer decisão arquitetural
- Ao adotar nova dependência significativa
- Ao definir padrão que todos os devs devem seguir
- Ao escolher entre duas abordagens igualmente válidas

---

## Processo

### Passo 1 — Determinar se é uma decisão ou um detalhe de implementação
Nem toda escolha técnica precisa de ADR. Usar este critério:

| Característica | Decisão (ADR necessário) | Detalhe (ADR dispensável) |
|---|---|---|
| Escopo | Impacta múltiplos componentes ou times | Impacta apenas o autor do código |
| Reversibilidade | Difícil ou custoso de reverter | Fácil de reverter sem consequências |
| Alcance | Afeta outros devs que precisam seguir o padrão | Escolha local sem efeito externo |
| Exemplos | Adotar nova lib, definir padrão de autenticação, escolher entre REST e gRPC | Nome de variável, estrutura interna de função, ordem de imports |

Se tiver dúvida, criar o ADR. O custo de criar um ADR desnecessário é baixo. O custo de não ter um ADR para uma decisão importante é alto.

### Passo 2 — Criar o arquivo ADR
Criar o arquivo no caminho padrão do repositório: `docs/decisions/ADR-<NNN>-<slug-da-decisao>.md`

O número `NNN` é o próximo número sequencial disponível na pasta. Verificar os ADRs existentes antes de numerar. Nunca reutilizar um número, mesmo que o ADR anterior tenha sido cancelado.

Formato do slug: lowercase com hífens, descritivo, sem artigos. Exemplos:
- `ADR-001-adotar-nestjs-como-framework-bff.md`
- `ADR-002-autenticacao-via-jwt-com-refresh-token.md`
- `ADR-042-usar-outbox-pattern-para-mensageria.md`

### Passo 3 — Preencher o ADR com o formato padrão

```markdown
# ADR-<NNN>: <título da decisão>

**Status:** Proposto | Aceito | Deprecado | Supersedido por ADR-<NNN>
**Data:** <YYYY-MM-DD>
**Autor:** <nome>

## Contexto

<O problema que precisava ser resolvido. Forças em jogo. Constraints técnicas, de negócio ou de equipe.
Por que isso é uma decisão e não um detalhe de implementação.>

## Decisão

<A decisão tomada, escrita em voz ativa e afirmativa: "Usaremos X porque Y.">

## Alternativas consideradas

| Alternativa | Por que não escolhemos |
|---|---|
| <opção A> | <motivo objetivo de rejeição> |
| <opção B> | <motivo objetivo de rejeição> |

## Consequências

**Positivas:** <o que melhora com esta decisão>
**Negativas:** <o que piora ou trade-off aceito conscientemente>
**Neutras:** <o que muda sem ser melhor ou pior>
```

Cada seção é obrigatória. ADR sem "Alternativas consideradas" não documenta o processo decisório — apenas o resultado.

### Passo 4 — Submeter para revisão
O ADR começa com status `Proposto`. Abrir PR para revisão do tech-lead ou arquiteto responsável. Somente após aprovação no PR, o status muda para `Aceito`. O merge do PR é o ato formal de aceitar a decisão.

### Passo 5 — Quando uma decisão é supersedida
Ao criar um ADR que substitui um anterior:
1. Criar o novo ADR normalmente com o próximo número sequencial
2. Atualizar o ADR antigo, mudando o status para `Supersedido por ADR-<NNN>` e adicionando link para o novo
3. Nunca deletar ADRs — o histórico de decisões é o valor do arquivo; deletar destrói contexto

### Passo 6 — Manter documentação complementar atualizada
Além do ADR em `docs/decisions/`, atualizar os seguintes pontos de acordo com o impacto da decisão:

- **`CLAUDE.md` do projeto:** Se a decisão afeta o comportamento esperado do agente de IA (convenções de código, padrões de geração, gotchas do repositório), atualizar o `CLAUDE.md` com a nova instrução
- **`plans/`:** Se existe um plano de desenvolvimento ativo que é impactado pela decisão, atualizar o plano correspondente
- **Comentários inline:** Para workarounds não óbvios no código, adicionar comentário referenciando o ADR: `// ADR-042: usamos X aqui porque Y — ver docs/decisions/ADR-042-...`

---

## Racionalizações bloqueadas

| Racionalização | Rebate |
|---|---|
| "Todo mundo sabe por que fizemos assim" | Em 6 meses, ninguém vai lembrar. Em 2 anos, quem sabia vai ter saído da empresa. |
| "O código é auto-explicativo" | Código explica o "o quê". ADR explica o "por que não fizemos de outro jeito" — e essa é a parte que se perde. |
| "ADR é burocracia" | 20 minutos para escrever um ADR vs horas re-debatendo a mesma decisão a cada 3 meses, multiplicado por toda a equipe. |
| "Vou escrever depois, quando tiver tempo" | O melhor momento para escrever um ADR é no momento da decisão, quando o contexto está fresco e as alternativas ainda são lembradas. "Depois" é nunca. |
| "A decisão pode mudar, não vale documentar" | Decisões que mudam são especialmente importantes de documentar — o ADR do estado anterior explica o que levou à mudança. |

---

## Anti-padrões bloqueados

- Deletar ou sobrescrever ADRs existentes — sempre criar novo ADR e marcar o antigo como supersedido
- ADR sem seção "Alternativas consideradas" — documenta resultado, não decisão
- ADR com status permanentemente em "Proposto" — ou aprova ou cancela, não deixa em limbo
- Criar ADR depois da implementação sem documentar as alternativas que foram consideradas na época
- Usar ADR para documentar detalhes de implementação (estrutura de função, nome de variável) — isso polui o histórico de decisões arquiteturais
- Não atualizar `CLAUDE.md` quando a decisão impacta o comportamento esperado do agente

---

## Checklist de conclusão

- [ ] Confirmado que é uma decisão (não detalhe de implementação) antes de criar o ADR
- [ ] Arquivo criado em `docs/decisions/ADR-<NNN>-<slug>.md` com número sequencial correto
- [ ] Seção "Contexto" descreve o problema e as forças em jogo, não apenas a solução
- [ ] Seção "Decisão" está escrita em voz ativa e afirmativa
- [ ] Seção "Alternativas consideradas" lista pelo menos duas alternativas rejeitadas com motivo objetivo
- [ ] Seção "Consequências" inclui pontos negativos e trade-offs aceitos (não apenas positivos)
- [ ] Status inicial definido como "Proposto" aguardando revisão
- [ ] PR aberto para revisão do tech-lead ou arquiteto
- [ ] Se supersede ADR anterior: ADR antigo atualizado com status "Supersedido por ADR-NNN"
- [ ] `CLAUDE.md` atualizado se a decisão impacta o comportamento do agente
- [ ] Comentários inline adicionados no código para workarounds não óbvios referenciando o ADR
