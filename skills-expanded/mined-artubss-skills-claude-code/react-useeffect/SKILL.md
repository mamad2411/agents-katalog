---
name: react-useeffect
description: Melhores práticas de React useEffect da documentação oficial. Use ao escrever/revisar useEffect, useState para valores derivados, busca de dados ou sincronização de estado. Ensina quando NÃO usar Effect e alternativas melhores.
---

# Você Pode Não Precisar de um Effect

Effects são uma **saída de emergência** do React. Eles permitem sincronizar com sistemas externos. Se não houver nenhum sistema externo envolvido, você não deveria precisar de um Effect.

## Referência Rápida

| Situação | NÃO FAÇA | FAÇA |
|-----------|----------|------|
| Estado derivado de props/state | `useState` + `useEffect` | Calcule durante a renderização |
| Cálculos caros | `useEffect` para cache | `useMemo` |
| Resetar estado quando prop muda | `useEffect` com `setState` | Prop `key` |
| Respostas a eventos de usuário | `useEffect` observando state | Event handler direto |
| Notificar pai de mudanças | `useEffect` chamando `onChange` | Chamar no event handler |
| Buscar dados | `useEffect` sem cleanup | `useEffect` com cleanup OU framework |

## Quando Você PRECISA de Effects

- Sincronizar com **sistemas externos** (widgets não-React, APIs do navegador)
- **Inscrições** em stores externos (use `useSyncExternalStore` quando possível)
- **Analytics/logging** que executa porque o componente foi exibido
- **Busca de dados** com cleanup apropriado (ou use mecanismo integrado do framework)

## Quando Você NÃO Precisa de Effects

1. **Transformar dados para renderização** - Calcule no topo do nível, re-executa automaticamente
2. **Lidar com eventos de usuário** - Use event handlers, você sabe exatamente o que aconteceu
3. **Derivar estado** - Apenas compute: `const fullName = firstName + ' ' + lastName`
4. **Encadear atualizações de estado** - Calcule todo o próximo estado no event handler

## Árvore de Decisão

```
Precisa responder a algo?
├── Interação do usuário (clique, submit, arrastar)?
│   └── Use EVENT HANDLER
├── Componente apareceu na tela?
│   └── Use EFFECT (sincronização externa, analytics)
├── Props/state mudou e precisa de valor derivado?
│   └── CALCULE DURANTE A RENDERIZAÇÃO
│       └── Caro? Use useMemo
└── Precisa resetar estado quando prop muda?
    └── Use prop KEY no componente
```

## Orientação Detalhada

- [Anti-Padrões](./anti-patterns.md) - Erros comuns com correções
- [Alternativas Melhores](./alternatives.md) - useMemo, key prop, lifting state, useSyncExternalStore