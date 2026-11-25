---
name: react-component-performance
description: Diagnostique componentes React lentos e sugira correções de desempenho direcionadas.
risk: safe
source: "Dimillian/Skills (MIT)"
date_added: "2026-03-25"
---

# Desempenho de Componentes React

## Visão Geral

Identifique hotspots de renderização, isole atualizações caras e aplique otimizações direcionadas sem alterar o comportamento da UI.

## Quando Usar

- Quando o usuário solicita profile ou melhoria de um componente React lento.
- Quando você precisa reduzir re-renders, lag em listas ou trabalho custoso de renderização na UI React.

## Fluxo de Trabalho

1. Reproduza ou descreva a lentidão.
2. Identifique o que dispara re-renders (atualizações de state, mudanças de props, effects).
3. Isole state de mudança rápida de subtrees pesadas.
4. Estabilize props e handlers; memoize onde compensa.
5. Reduza trabalho custoso (computação, tamanho do DOM, comprimento de listas).
6. **Valide**: abra React DevTools Profiler → registre a interação → inspecione o Flamegraph para componentes renderizando mais de ~16 ms → compare com uma gravação baseline pré-otimização.

## Checklist

- Meça: use React DevTools Profiler ou log de renders; capture baseline.
- Encontre churn: identifique state atualizado em timer, scroll, input ou animação.
- Divida: mova state de mudança rápida para filho; mantenha listas pesadas estáticas.
- Memoize: envolva linhas folha com `memo` apenas quando props são estáveis.
- Estabilize props: use `useCallback`/`useMemo` para handlers e valores derivados.
- Evite trabalho derivado em render: pré-compute ou compute dentro de helpers memoizados.
- Controle tamanho de lista: window/virtualize listas longas; evite renderizar itens ocultos.
- Keys: garanta keys estáveis; evite index quando ordem pode mudar.
- Effects: verifique arrays de dependência; evite effects que re-executem a cada render.
- Style/layout: observe thrash de layout caro ou renders grandes de Markdown/diff.

## Padrões de Otimização

### Isole state de mudança rápida

Mova um timer ou contador de animação para um filho para que o parent list nunca re-renderize a cada tick.

```tsx
// ❌ Antes – todo parent (e list) re-renderiza a cada segundo
function Dashboard({ items }: { items: Item[] }) {
  const [tick, setTick] = useState(0);
  useEffect(() => {
    const id = setInterval(() => setTick(t => t + 1), 1000);
    return () => clearInterval(id);
  }, []);
  return (
    <>
      <Clock tick={tick} />
      <ExpensiveList items={items} /> {/* re-renderiza a cada segundo */}
    </>
  );
}

// ✅ Depois – apenas <Clock> re-renderiza; list fica intocada
function Clock() {
  const [tick, setTick] = useState(0);
  useEffect(() => {
    const id = setInterval(() => setTick(t => t + 1), 1000);
    return () => clearInterval(id);
  }, []);
  return <span>{tick}s</span>;
}

function Dashboard({ items }: { items: Item[] }) {
  return (
    <>
      <Clock />
      <ExpensiveList items={items} />
    </>
  );
}
```

### Estabilize callbacks com `useCallback` + `memo`

```tsx
// ❌ Antes – nova referência de handler em cada render quebra Row memo
function List({ items }: { items: Item[] }) {
  const handleClick = (id: string) => console.log(id); // nova ref cada render
  return items.map(item => <Row key={item.id} item={item} onClick={handleClick} />);
}

// ✅ Depois – handler estável; Row re-renderiza apenas quando seu item muda
const Row = memo(({ item, onClick }: RowProps) => (
  <li onClick={() => onClick(item.id)}>{item.name}</li>
));

function List({ items }: { items: Item[] }) {
  const handleClick = useCallback((id: string) => console.log(id), []);
  return items.map(item => <Row key={item.id} item={item} onClick={handleClick} />);
}
```

### Prefira dados derivados fora de render

```tsx
// ❌ Antes – recomputa a cada render
function Summary({ orders }: { orders: Order[] }) {
  const total = orders.reduce((sum, o) => sum + o.amount, 0); // executa cada render
  return <p>Total: {total}</p>;
}

// ✅ Depois – recomputa apenas quando orders muda
function Summary({ orders }: { orders: Order[] }) {
  const total = useMemo(() => orders.reduce((sum, o) => sum + o.amount, 0), [orders]);
  return <p>Total: {total}</p>;
}
```

### Padrões adicionais

- **Divida linhas**: extraia linhas de lista em componentes memoizados com props estreitas.
- **Adie renderização pesada**: lazy-render ou collapse conteúdo caro até ser expandido.

## Passos de Validação de Profile

1. Abra **React DevTools → Profiler** tab.
2. Clique **Record**, execute a interação lenta, depois **Stop**.
3. Mude para visualização **Flamegraph**; qualquer barra com componente e tempo > ~16 ms é candidata.
4. Use **Ranked chart** para ordenar por self render time e foque nos top offenders.
5. Aplique uma otimização por vez, re-registre e compare contagens de render e durações contra o baseline.

## Referência de Exemplo

Carregue `references/examples.md` quando o usuário quer um exemplo de refactor concreto.