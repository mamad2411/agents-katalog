---
name: especificar-componente
description: "Produz a especificação visual detalhada de um componente — estados, acessibilidade, responsividade e tokens — como entrada para o frontend. Use quando o dev-ui-ux vai detalhar um componente antes da implementação."
author: "Pedro Andriow (https://github.com/Andriow)"
disable-model-invocation: true
---

# Skill: especificar-componente

Produz a especificação completa de um componente React antes de qualquer linha de código ser escrita: estados visuais, dados esperados, requisitos de acessibilidade, responsividade e tokens do design system. O arquivo gerado é a instrução principal que o `dev-frontend` segue para implementar.

**Agente:** dev-ui-ux  
**Guardrails aplicáveis:** `ux.md §1`, `ux.md §2`, `ux.md §4`, `ux.md §5`  
**Referências rápidas:** `References/accessibility-checklist.md`

---

## Quando usar

- Antes de qualquer novo componente ou tela ser implementado pelo `dev-frontend`
- Quando há ambiguidade visual nos critérios de aceite da história
- Quando o componente tem múltiplos estados ou regras de interação complexas
- Sempre que houver fluxo que afete acessibilidade (modais, formulários, notificações)

---

## Pré-requisitos

- `design-system/MASTER.md` existente (executar `criar-design-system` antes se não existir)
- Contrato BFF do arquiteto (shape dos dados que o componente consome)
- Arquivo de plano `plans/dev-frontend/<ticket>.md` do tech-lead (critérios de aceite)
- Critérios de aceite e regras de negócio da história

---

## Processo de execução

### Passo 1 — Identificar o componente e seu contexto

Antes de especificar, entender:

```
1. Qual é o nome do componente? (ex: CheckoutSummary, ProductCard, CancelOrderModal)
2. É uma tela completa, uma seção, ou um componente reutilizável?
3. Qual fluxo do usuário ele serve? (compra, cancelamento, cadastro...)
4. Quais dados ele exibe? (derivar do contrato BFF)
5. Qual a prioridade de estados: qual é o mais frequente?
```

---

### Passo 2 — Mapear todos os estados

Listar **todos** os estados possíveis — não apenas o happy path:

| Estado | Quando ocorre | O que mostrar |
|---|---|---|
| `default` | Renderização inicial com dados | Layout principal |
| `loading` | Aguardando resposta do BFF | Skeleton ou spinner contextual |
| `empty` | Lista sem itens / sem dados | Ilustração + mensagem + CTA |
| `error` | Falha na requisição | Mensagem de erro + botão de retry |
| `partial` | Dados parcialmente carregados | Indicar o que está indisponível |
| `hover` | Mouse sobre elemento interativo | Mudança visual de feedback |
| `focus` | Elemento focado por teclado | Ring de foco visível (`focus-visible`) |
| `active` | Durante clique/toque | Feedback tátil visual |
| `disabled` | Ação bloqueada por regra de negócio | Visual atenuado, `cursor: not-allowed` |
| `selected` | Item selecionado em lista | Destaque visual + `aria-selected` |
| `success` | Ação completada com sucesso | Confirmação temporária |

**Regra:** Skeleton é preferível a spinner para conteúdo com estrutura conhecida. Spinner para ações sem previsão de duração.

---

### Passo 3 — Definir requisitos de acessibilidade

Para cada componente, especificar:

**Semântica HTML:**
```
- Elemento base: <button> | <a> | <input> | <dialog> | <article> | <section> | <nav> | <ul> | <table>
- Role ARIA (se HTML nativo não resolve): role="[listbox|combobox|tabpanel|...]"
```

**Labels e anúncios:**
```
- aria-label: "[texto descritivo]" (quando label visível não existe ou não é suficiente)
- aria-labelledby: "[id-do-heading]" (quando heading existente serve como label)
- aria-describedby: "[id-da-descricao]" (informação adicional — erros, hints)
- aria-live="polite": para regiões que atualizam assincronamente
```

**Teclado:**
```
- Teclas suportadas: Enter (confirmar), Space (toggle), Escape (fechar/cancelar), Tab (navegar), 
                     Arrow keys (navegar em listas/menus), Home/End (primeiro/último item)
- Ordem de foco: descrever a sequência esperada
- Focus trap: [sim/não] — apenas em modais e drawers
- Retorno de foco: ao fechar modal/drawer, foco volta para [elemento X]
```

**Contraste mínimo (verificar com `design-system/MASTER.md`):**
```
- Texto sobre fundo: [cor texto] / [cor fundo] = [relação]:1 (mínimo 4.5:1)
- Ícone/borda: [cor] / [fundo] = [relação]:1 (mínimo 3:1)
- Estado de erro: garantir que não depende só de cor vermelha
```

---

### Passo 4 — Especificar interações e animações

Seguir `ux.md §3` — apenas `transform` e `opacity`:

```css
/* Hover de botão */
transition: background-color var(--duration-fast) var(--easing-out),
            transform var(--duration-fast) var(--easing-out);

/* Entrada de modal */
@keyframes slide-up {
  from { transform: translateY(8px); opacity: 0; }
  to   { transform: translateY(0);   opacity: 1; }
}

/* Skeleton pulse */
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50%       { opacity: 0.5; }
}

/* Sempre com prefers-reduced-motion */
@media (prefers-reduced-motion: reduce) {
  .modal { animation: none; }
}
```

---

### Passo 5 — Definir responsividade

Mobile-first obrigatório:

```
mobile (< 768px):  [comportamento, layout, tamanho de fonte, alvo de toque]
tablet (768-1024px): [ajustes em relação ao mobile]
desktop (> 1024px): [layout final]

Breakpoints específicos do projeto (do MASTER.md): [listar]
```

---

### Passo 6 — Escrever o arquivo de especificação

Salvar em `plans/dev-frontend/<ticket>-<nome-do-componente>-spec.md` usando o template de `Guidelines/ux/README.md §2`.

O arquivo deve ser **auto-suficiente**: o `dev-frontend` deve conseguir implementar sem perguntar sobre estados, acessibilidade ou responsividade.

---

### Passo 7 — Checklist de completude antes de passar ao dev-frontend

Verificar que a spec cobre:

- [ ] Todos os estados do componente descritos (mínimo: default, loading, empty, error)
- [ ] Shape dos dados TypeScript derivado do contrato BFF
- [ ] Todos os tokens do design system referenciados por nome (não hex, não px arbitrário)
- [ ] Requisitos de acessibilidade completos (semântica, labels, teclado, contraste)
- [ ] Comportamento responsivo em 3 breakpoints
- [ ] Animações com `prefers-reduced-motion` especificado
- [ ] Estado de toque (alvo ≥ 44×44px) verificado

---

## Anti-padrões bloqueados

- Especificar apenas o happy path (omitir loading, error, empty)
- Definir cor sem token do design system (ex: `#3b82f6` em vez de `--color-brand-500`)
- Omitir requisitos de acessibilidade para componentes interativos
- Especificar `transition: all` (`ux.md §3.2`)
- Criar spec de componente sem `design-system/MASTER.md` existente
- Especificar `outline: none` sem substituto de foco (`ux.md §1.6`)

---

## Checklist de conclusão

- [ ] Arquivo `plans/dev-frontend/<ticket>-<componente>-spec.md` criado
- [ ] Todos os estados cobertos
- [ ] Acessibilidade especificada (semântica + teclado + contraste + ARIA)
- [ ] Responsividade mobile-first em 3 breakpoints
- [ ] Tokens do design system usados (sem valores arbitrários)
- [ ] Animações com `prefers-reduced-motion`
- [ ] Spec revisada e passada ao `dev-frontend` com o caminho do arquivo
