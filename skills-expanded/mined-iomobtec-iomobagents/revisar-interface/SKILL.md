---
name: revisar-interface
description: "Audita a implementação de UI contra guardrails de acessibilidade WCAG 2.1 AA, tipografia e performance visual, em modo report ou fix. Use quando o dev-ui-ux ou o tech-lead vai validar a UI implementada."
author: "Pedro Andriow (https://github.com/Andriow)"
disable-model-invocation: true
---

# Skill: revisar-interface

Auditoria e correção de qualidade de interface: acessibilidade (WCAG 2.1 AA), animação, tipografia, formulários, performance visual e aderência ao design system. Opera em dois modos distintos — **nunca inferir o modo**; sempre perguntar ou derivar explicitamente da solicitação.

**Agente:** dev-ui-ux  
**Guardrails aplicáveis:** `ux.md` (todos os §)  
**Referências rápidas:** `References/accessibility-checklist.md`, `References/performance-checklist.md`

---

## Quando usar

- Após o `dev-frontend` abrir PR com implementação de componente ou tela
- Ao receber pedido de auditoria de interface existente
- Antes de uma release para validar qualidade visual e acessibilidade
- Quando o `tech-lead` escala uma revisão de PR de frontend ao `dev-ui-ux`

---

## Modos de operação

### Modo `report` (auditoria apenas — sem edição de arquivos)

Acionado quando a solicitação usa: *auditar*, *revisar*, *verificar*, *checar*, *inspecionar*, *analisar*, *relatório*.

**O agente NÃO edita nenhum arquivo no modo report.**

### Modo `fix` (auditoria + aplicar correções)

Acionado quando a solicitação usa: *corrigir*, *resolver*, *aplicar*, *consertar*, *ajustar*.

**Clarificar antes de agir se a solicitação for ambígua:**
```
Confirmar o modo de operação:
  A. Apenas relatório — listo as violações sem editar arquivos
  B. Aplicar correções — corrijo as violações encontradas

Qual prefere?
```

---

## Processo — Modo `report`

### Passo 1 — Mapear escopo

```bash
# Identificar todos os arquivos de componente no escopo
# (receber glob ou lista de arquivos como argumento)
```

Categorias de verificação:
1. Acessibilidade (CRITICAL) — `ux.md §1`
2. Touch & Interação (CRITICAL) — `ux.md §2`
3. Animação (HIGH) — `ux.md §3`
4. Tipografia (MEDIUM) — `ux.md §4`
5. Formulários (MEDIUM) — `ux.md §5`
6. Performance Visual (HIGH) — `ux.md §6`
7. Aderência ao design system (MEDIUM) — `design-system/MASTER.md`

### Passo 2 — Buscar diretrizes externas (web-interface-guidelines)

Usar `WebFetch` para buscar a versão mais recente das diretrizes em tempo real — nenhuma instalação manual necessária:

```
URL: https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md
```

**Se o fetch tiver sucesso:** incorporar as regras obtidas à auditoria. As 80+ regras em 17 categorias do documento externo complementam a checklist interna (Passo 3) — executar ambas e consolidar os achados.

**Se o fetch falhar** (sem conectividade, URL indisponível): registrar no relatório e prosseguir apenas com a checklist interna.

```
⚠️ web-interface-guidelines indisponível (sem conectividade ou repositório fora do ar).
   Executando checklist interna — cobertura pode ser menor que o habitual.
```

### Passo 3 — Checklist interna de auditoria

Verificar cada item e registrar `file:line` para cada violação encontrada:

#### CRITICAL — Acessibilidade

- [ ] `<div onClick>` / `<span onClick>` sem `role` e `onKeyDown` (`ux.md §1.2`)
- [ ] Botão icon-only sem `aria-label` (`ux.md §1.2`)
- [ ] Input sem `<label>` ou `aria-label` (`ux.md §1.3`)
- [ ] `user-scalable=no` ou `maximum-scale=1` no viewport meta (`ux.md §1.6`)
- [ ] `outline: none` / `outline: 0` sem substituto `focus-visible` (`ux.md §1.6`)
- [ ] Cor como único diferenciador de estado sem ícone ou texto (`ux.md §1.6`)
- [ ] Imagem significativa sem `alt` descritivo (`ux.md §6.1`)
- [ ] Modal/drawer sem focus trap ou sem retorno de foco ao fechar

#### CRITICAL — Touch

- [ ] Alvo de toque interativo menor que 44×44px (`ux.md §2`)
- [ ] `touch-action: manipulation` ausente em elementos interativos (`ux.md §2`)

#### HIGH — Animação e Performance

- [ ] `transition: all` (`ux.md §3.2`)
- [ ] Animação sem `@media (prefers-reduced-motion: reduce)` (`ux.md §3.2`)
- [ ] Animação de propriedades que causam layout (width, height, top, left) (`ux.md §3.1`)
- [ ] Imagem sem `width` e `height` explícitos (`ux.md §6.1`)
- [ ] Lista de mais de 50 itens sem virtualização (`ux.md §6.2`)
- [ ] `loading="lazy"` ausente em imagens abaixo do fold (`ux.md §6.1`)

#### MEDIUM — Tipografia e Formulários

- [ ] `...` (três pontos) em vez de `…` (ellipsis U+2026) (`ux.md §4.1`)
- [ ] Números em coluna sem `font-variant-numeric: tabular-nums` (`ux.md §4.2`)
- [ ] Heading sem `text-wrap: balance` (`ux.md §4.2`)
- [ ] `onPaste + preventDefault` bloqueando paste em input (`ux.md §5.2`)
- [ ] Campo sem `autocomplete` adequado (`ux.md §5.1`)
- [ ] Erro de formulário sem `aria-describedby` apontando para a mensagem (`ux.md §5.1`)
- [ ] Input com erro sem `aria-invalid="true"` (`ux.md §5.1`)

#### MEDIUM — Design System

- [ ] Valor hexadecimal ou px arbitrário em vez de token CSS (`design-system/MASTER.md`)
- [ ] Família tipográfica não declarada no MASTER.md
- [ ] Espaçamento fora da escala base-4

### Passo 4 — Formatar relatório

```markdown
## Auditoria de Interface — [data]

### Resumo

| Severidade | Violações |
|---|---|
| CRITICAL | N |
| HIGH     | N |
| MEDIUM   | N |
| Total    | N |

---

### CRITICAL

#### src/components/Button.tsx
src/components/Button.tsx:42 - icon button missing aria-label [ux.md §1.2]
src/components/Button.tsx:78 - transition: all — animate only transform/opacity [ux.md §3.2]

#### src/pages/checkout.tsx
src/pages/checkout.tsx:15 - input#email missing <label> [ux.md §1.3]

---

### HIGH

#### src/components/ProductList.tsx
src/components/ProductList.tsx:33 - list renders 200 items without virtualization [ux.md §6.2]

---

### Sem violações

src/components/Header.tsx — ✓ pass
src/components/Footer.tsx — ✓ pass

---

### Recomendações arquiteturais

[Padrões recorrentes que indicam problema estrutural — ex: "12 componentes sem focus-visible indica que o reset global de CSS está removendo outline sem substituto"]
```

---

## Processo — Modo `fix`

### Passo 1 — Auditoria baseline

Executar o Passo 1-4 do modo `report` para obter a lista completa de violações.

### Passo 2 — Priorizar correções

Aplicar na ordem: CRITICAL → HIGH → MEDIUM. Parar e reportar se uma correção exige decisão de produto (ex: qual texto usar em `aria-label`) ou decisão de design system (ex: qual token escolher para uma nova cor).

### Passo 3 — Aplicar correções

Para cada violação, aplicar a correção mínima necessária sem alterar lógica de negócio, estrutura de componente ou estilos não relacionados.

```tsx
// Exemplo: aria-label em botão icon-only
// ANTES (src/components/IconButton.tsx:42)
<button onClick={handleClose}><XIcon /></button>

// DEPOIS
<button onClick={handleClose} aria-label="Fechar">
  <XIcon aria-hidden="true" />
</button>
```

```css
/* Exemplo: substituir transition: all */
/* ANTES */
.card { transition: all 0.2s ease; }

/* DEPOIS */
.card {
  transition: transform var(--duration-fast) var(--easing-out),
              box-shadow var(--duration-fast) var(--easing-out);
}
```

### Passo 4 — Verificar ausência de regressões

Após cada correção, confirmar que:
- Nenhum estilo de layout foi alterado acidentalmente
- A lógica do componente permanece intacta
- Não foram introduzidas novas violações

### Passo 5 — Relatório de correções aplicadas

```markdown
## Correções aplicadas

| Arquivo | Linha | Violação | Correção |
|---|---|---|---|
| Button.tsx | 42 | Sem aria-label | Adicionado aria-label="Fechar" |
| Card.tsx | 15 | transition: all | Substituído por transform + box-shadow |

## Itens que requerem decisão humana

- src/components/StatusBadge.tsx:88 — cor como único diferenciador de status "ativo/inativo".
  Solução recomendada: adicionar ícone ou texto junto à cor, mas o texto adequado depende do domínio.
  Aguardando decisão do produto/tech-lead.
```

---

## Anti-padrões bloqueados

- Inferir o modo (report vs fix) sem confirmação quando solicitação for ambígua
- Editar arquivos no modo `report`
- Alterar lógica de negócio ao aplicar correções de acessibilidade
- Inventar conteúdo para `aria-label` quando o texto correto depende do domínio — marcar como `TODO: definir label com produto`
- Ignorar violações CRITICAL para reportar apenas MEDIUM/LOW
- Aplicar correção que introduz nova violação de guardrail

---

## Checklist de conclusão

**Modo report:**
- [ ] Todos os arquivos no escopo verificados
- [ ] Violações organizadas por severidade e arquivo
- [ ] Formato `file:line` em todas as referências
- [ ] Recomendações arquiteturais incluídas (padrões recorrentes)

**Modo fix:**
- [ ] Baseline documentado antes das correções
- [ ] Todas as correções CRITICAL aplicadas
- [ ] Itens que requerem decisão humana listados explicitamente
- [ ] Relatório de correções aplicadas entregue
