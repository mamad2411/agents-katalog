---
name: ui-ux-code-generation
description: Gerar código de interface que incorpora princípios sólidos de UX — acessibilidade (WCAG/ARIA), cobertura completa de estados (idle/hover/focus/active/disabled/loading/empty/error/success), formulários validáveis, feedback imediato, targets táteis adequados e responsividade mobile-first. Ative sempre que o usuário pedir componentes, páginas, formulários, dashboards, botões, modais, menus ou qualquer UI funcional em HTML/CSS/React/Vue/Svelte e a qualidade da experiência (não apenas a estética) importar. Complementar à skill `frontend-design` (que cuida da direção estética bold): esta cuida do *comportamento* correto.
---

# UI/UX Code Generation

Gerar código de UI que *funciona bem para humanos* — não só código que renderiza. Este skill garante que cada componente gerado cubra estados, acessibilidade, feedback e entrada adequadamente, antes de qualquer preocupação estética.

## Quando Ativar

- Pedidos para criar componentes interativos (botões, forms, modais, dropdowns, tabs, menus).
- Construção de páginas com fluxos de usuário (login, checkout, onboarding, dashboard).
- Qualquer UI que aceite input do usuário ou mostre estado assíncrono.
- Revisão ou refatoração de código de interface para melhorar UX/acessibilidade.
- Conversão de mockup/design para código funcional.

## Relação com Outras Skills

- **`frontend-design`**: direção estética, tipografia expressiva, composição visual bold. Use *em conjunto* quando o pedido também exigir identidade visual forte.
- **Este skill**: comportamento, estados, acessibilidade, fluxo de interação. Priorize este quando o pedido envolver *funcionalidade* e *usabilidade*.
- Se ambas as dimensões importam, aplique as duas — estética sem UX é bonito e quebrado; UX sem estética é funcional e esquecível.

## Princípios Fundamentais (não-negociáveis)

### 1. Todo componente interativo cobre TODOS os estados

Nunca entregue um botão com só `:hover`. Todo elemento interativo precisa de:

| Estado       | Quando aparece                          | Design                              |
|--------------|-----------------------------------------|-------------------------------------|
| `idle`       | Estado padrão, sem interação            | Visualmente "pronto para ser usado" |
| `hover`      | Mouse sobre (apenas em dispositivos com ponteiro) | Feedback suave de interatividade |
| `focus-visible` | Navegação por teclado                | Ring/outline claro e visível        |
| `active`     | Durante o clique/toque                  | Pressionado, compresso              |
| `disabled`   | Ação indisponível                       | Opacidade reduzida, cursor `not-allowed`, `aria-disabled="true"` |
| `loading`    | Ação assíncrona em andamento            | Spinner/skeleton, conteúdo bloqueado, `aria-busy="true"` |
| `error`      | Falha                                   | Mensagem clara, cor de erro, ícone  |
| `empty`      | Lista/dados vazios                      | Ilustração + CTA ou explicação      |
| `success`    | Confirmação                             | Feedback positivo temporário        |

```tsx
// PASS: Botão com estados completos
<button
  type="button"
  onClick={handleClick}
  disabled={isLoading || isDisabled}
  aria-busy={isLoading}
  className="
    inline-flex items-center gap-2 rounded-lg px-4 py-2
    bg-indigo-600 text-white font-medium
    hover:bg-indigo-700
    focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-indigo-400 focus-visible:ring-offset-2
    active:bg-indigo-800 active:scale-[0.98]
    disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:bg-indigo-600
    transition-all duration-150
  "
>
  {isLoading && <Spinner aria-hidden="true" />}
  <span>{isLoading ? 'Salvando...' : 'Salvar'}</span>
</button>

// FAIL: Só idle e hover; quebra teclado, quebra loading, quebra disabled
<button onClick={handleClick} className="bg-indigo-600 hover:bg-indigo-700 px-4 py-2">
  Salvar
</button>
```

### 2. Acessibilidade é um requisito, não um extra

**Sempre:**

- HTML semântico primeiro (`<button>`, `<nav>`, `<main>`, `<label>`) — só use `<div role="button">` se não houver alternativa.
- Todo `<input>` tem `<label>` associado (por `htmlFor`/`for` ou envolvendo).
- Imagens funcionais têm `alt`; decorativas têm `alt=""` ou `aria-hidden="true"`.
- Ícones standalone têm `aria-label`; ícones + texto têm o ícone como `aria-hidden="true"`.
- Contraste mínimo: **4.5:1** para texto normal, **3:1** para texto grande (≥18pt ou ≥14pt bold) e elementos UI.
- Foco visível — nunca faça `outline: none` sem substituir por `:focus-visible` estilizado.
- Ordem de tab lógica segue ordem visual.
- Modais, dropdowns e menus prendem foco enquanto abertos (`focus trap`) e devolvem foco ao fechar.
- Estados e mudanças dinâmicas são anunciados via `aria-live="polite"` ou `role="status"` (`role="alert"` só para urgências).
- Zero dependência exclusiva em cor para transmitir informação — adicione ícone, texto ou padrão.

```tsx
// PASS: input acessível
<div>
  <label htmlFor="email" className="block text-sm font-medium">
    E-mail
    <span aria-hidden="true" className="text-red-600"> *</span>
  </label>
  <input
    id="email"
    name="email"
    type="email"
    required
    autoComplete="email"
    aria-describedby={error ? 'email-error' : 'email-hint'}
    aria-invalid={!!error}
    className="..."
  />
  {!error && (
    <p id="email-hint" className="mt-1 text-sm text-gray-600">
      Usaremos para enviar confirmação.
    </p>
  )}
  {error && (
    <p id="email-error" role="alert" className="mt-1 text-sm text-red-600">
      <ExclamationIcon aria-hidden="true" className="inline h-4 w-4 mr-1" />
      {error}
    </p>
  )}
</div>

// FAIL: sem label associado, erro não vinculado, asterisco sem aria
<div>
  <span>E-mail *</span>
  <input type="email" />
  {error && <span style={{color:'red'}}>{error}</span>}
</div>
```

### 3. Feedback imediato para toda ação

Ação do usuário → **mudança visível em < 100ms**.

- Clicks disparam estado `active` imediato (mesmo que a ação seja assíncrona).
- Operações > 1s mostram loading state (skeleton > spinner na maioria dos casos).
- Operações > 10s mostram progresso real se possível.
- Confirmações destrutivas vêm *antes* da ação (modal), não depois (undo).
- Success/error anunciados via toast, inline alert ou mudança de estado — nunca silenciosamente.
- **Optimistic UI** quando a chance de falha é baixa: atualize UI imediatamente, reverta se falhar.

### 4. Prevenção de erro > mensagem de erro

- Desabilite submit enquanto formulário inválido (mas mostre *por quê*).
- Valide em blur, não em cada keystroke (exceto para password strength, character counter).
- Confirme ações destrutivas com nome do item digitado (padrão do GitHub) para ações sérias.
- Use `<input type="...">` correto: `email`, `tel`, `url`, `number`, `date` — ativa teclado certo em mobile e validação nativa.
- `autocomplete` correto em todo input de formulário (`email`, `name`, `current-password`, `new-password`, `one-time-code`, `street-address`, etc).
- `inputmode="numeric"` para PINs/códigos; `pattern` para formatos específicos.

## Formulários Bem Feitos

```tsx
// Checklist implícito neste exemplo:
// - label associado via htmlFor
// - autocomplete apropriado
// - inputmode correto
// - validação em blur, não em change
// - erro vinculado via aria-describedby + aria-invalid
// - hint antes do erro aparecer
// - submit desabilitado durante envio com aria-busy
// - foco movido para primeiro erro após falha
// - success anunciado via role="status"

function LoginForm() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [touched, setTouched] = useState<Record<string, boolean>>({})
  const [errors, setErrors] = useState<Record<string, string>>({})
  const [status, setStatus] = useState<'idle' | 'submitting' | 'success' | 'error'>('idle')
  const firstErrorRef = useRef<HTMLInputElement>(null)

  const validateField = (name: string, value: string): string => {
    if (name === 'email') {
      if (!value) return 'E-mail é obrigatório'
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) return 'Formato de e-mail inválido'
    }
    if (name === 'password') {
      if (!value) return 'Senha é obrigatória'
      if (value.length < 8) return 'Mínimo 8 caracteres'
    }
    return ''
  }

  const handleBlur = (name: string, value: string) => {
    setTouched(t => ({ ...t, [name]: true }))
    const error = validateField(name, value)
    setErrors(e => ({ ...e, [name]: error }))
  }

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault()
    const nextErrors = {
      email: validateField('email', email),
      password: validateField('password', password),
    }
    setErrors(nextErrors)
    setTouched({ email: true, password: true })

    if (Object.values(nextErrors).some(Boolean)) {
      firstErrorRef.current?.focus()
      return
    }

    setStatus('submitting')
    try {
      await login({ email, password })
      setStatus('success')
    } catch (err) {
      setStatus('error')
    }
  }

  return (
    <form onSubmit={handleSubmit} noValidate className="space-y-4">
      <Field
        id="email"
        label="E-mail"
        type="email"
        autoComplete="email"
        inputMode="email"
        value={email}
        onChange={setEmail}
        onBlur={() => handleBlur('email', email)}
        error={touched.email ? errors.email : ''}
        ref={errors.email ? firstErrorRef : undefined}
        required
      />
      <Field
        id="password"
        label="Senha"
        type="password"
        autoComplete="current-password"
        value={password}
        onChange={setPassword}
        onBlur={() => handleBlur('password', password)}
        error={touched.password ? errors.password : ''}
        required
      />
      <button
        type="submit"
        disabled={status === 'submitting'}
        aria-busy={status === 'submitting'}
        className="..."
      >
        {status === 'submitting' ? 'Entrando...' : 'Entrar'}
      </button>
      {status === 'error' && (
        <p role="alert" className="text-red-600 text-sm">
          Não foi possível entrar. Verifique suas credenciais.
        </p>
      )}
      {status === 'success' && (
        <p role="status" className="text-green-600 text-sm">
          Login realizado. Redirecionando...
        </p>
      )}
    </form>
  )
}
```

### Regras de ouro em formulários

- **Um campo por linha** em formulários verticais; agrupe apenas campos logicamente relacionados (CEP + número, cartão + CVV) na mesma linha.
- **Labels em cima**, nunca só placeholder — placeholder some no foco e prejudica memória/acessibilidade.
- **Erros inline**, próximos ao campo; sumário geral só em formulários longos e como complemento.
- **Botão primário à direita** em desktop, **largura total** em mobile.
- **Botão "Cancelar" nunca é botão primário** — use link ou botão secundário.
- **Não limpe o formulário em erro** — preserve o que o usuário digitou (exceto senhas por design/segurança quando fizer sentido).

## Estados Vazios, de Erro e Loading

### Empty state ≠ tela em branco

```tsx
// PASS: Empty state útil
<div className="flex flex-col items-center text-center py-12">
  <InboxIcon aria-hidden="true" className="h-12 w-12 text-gray-400" />
  <h3 className="mt-4 text-lg font-semibold">Nenhuma tarefa ainda</h3>
  <p className="mt-1 text-sm text-gray-600 max-w-sm">
    Crie sua primeira tarefa para começar a organizar seu dia.
  </p>
  <button type="button" onClick={onCreate} className="mt-4 ...">
    Criar tarefa
  </button>
</div>

// FAIL: "Nada aqui" e ponto final
<p>Vazio.</p>
```

### Loading: prefira skeleton > spinner

- **Skeleton**: conteúdo previsível (lista, card, tabela). Reduz *perceived latency*.
- **Spinner**: ações pontuais (botão, pequenos refresh).
- **Progress bar**: operações longas com progresso conhecido (upload).
- **Indeterminate progress**: operações > 3s sem progresso conhecido.

```tsx
// Skeleton para lista
{isLoading ? (
  <ul aria-busy="true" aria-label="Carregando tarefas">
    {Array.from({ length: 5 }).map((_, i) => (
      <li key={i} className="flex items-center gap-3 py-3 animate-pulse">
        <div className="h-4 w-4 rounded bg-gray-200" />
        <div className="h-4 flex-1 rounded bg-gray-200" />
      </li>
    ))}
  </ul>
) : (
  <TaskList tasks={tasks} />
)}
```

### Error state acionável

Toda mensagem de erro responde a: **o que aconteceu?**, **por que importa?**, **o que fazer agora?**

```tsx
// PASS
<div role="alert" className="rounded-lg border border-red-200 bg-red-50 p-4">
  <h3 className="font-semibold text-red-900">Não foi possível carregar tarefas</h3>
  <p className="mt-1 text-sm text-red-800">
    Verificamos sua conexão de rede. Tente novamente em alguns segundos.
  </p>
  <button type="button" onClick={refetch} className="mt-3 ...">
    Tentar novamente
  </button>
</div>

// FAIL
<p style={{color:'red'}}>Error: 500</p>
```

## Responsividade & Touch

- **Mobile-first**: estilos base para mobile, `@media (min-width: ...)` adiciona para telas maiores.
- **Touch targets mínimos**: 44×44 CSS pixels (Apple HIG) / 48×48 dp (Material). Inclui padding — `h-11 w-11` mínimo em tap targets isolados.
- **Espaçamento entre targets** ≥ 8px para evitar toques errados.
- **Respeite `prefers-reduced-motion`**: cancele animações para quem configurou.
- **Respeite `prefers-color-scheme`** se dark mode for oferecido.
- **Container queries** (`@container`) > media queries para componentes reutilizáveis que adaptam ao container, não à viewport.
- **`max-width` em texto**: 60–75ch para legibilidade de parágrafos longos.
- **Fontes fluidas** com `clamp()`: `font-size: clamp(1rem, 0.9rem + 0.5vw, 1.25rem)`.

```css
/* Respeitar reduced motion */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

## Navegação & Orientação

- Usuário **sempre sabe onde está** (título de página, breadcrumb, item de menu destacado, URL semântica).
- Usuário **sempre sabe como voltar** (back button funciona, breadcrumb clicável, logo leva para home).
- **Links externos** sinalizados (ícone `↗` + `rel="noopener noreferrer"` + `target="_blank"` + `aria-label` dizendo "abre em nova aba").
- **Skip link** no topo: `<a href="#main" class="sr-only focus:not-sr-only">Pular para conteúdo</a>`.
- **Landmarks** (`<header>`, `<nav>`, `<main>`, `<footer>`) presentes e únicos (exceto `<nav>` que pode repetir com `aria-label` distinto).

## Microinterações com Propósito

Cada animação precisa justificar sua existência. Animação boa:
1. **Comunica causa e efeito** (item voou pro carrinho).
2. **Orienta atenção** (elemento novo pulsa uma vez).
3. **Indica progresso** (skeleton, spinner).
4. **Dá sensação de responsividade** (scale 0.98 no active).

Timing: 150–250ms para micro; 300–400ms para transições de tela. Easing: `ease-out` para entrada, `ease-in` para saída, `ease-in-out` para loop. Evite `linear` (exceto spinner).

## Performance UX

- **Core Web Vitals** como UX: LCP < 2.5s, INP < 200ms, CLS < 0.1.
- **Reserve espaço** para imagens (`width`/`height`) e conteúdo assíncrono para evitar layout shift.
- **Virtualização** (`react-window`, `react-virtuoso`) para listas > 100 itens.
- **Debounce** em search inputs (300–500ms); **throttle** em scroll/resize (16–60ms).
- **Lazy-load** de imagens fora do viewport (`loading="lazy"`) e de rotas (`React.lazy`).
- **Otimize fontes**: `font-display: swap`, pré-carregue apenas fontes críticas.

## Anti-padrões Comuns (evitar)

| Anti-padrão                                   | Problema                                    | Correção                              |
|-----------------------------------------------|---------------------------------------------|---------------------------------------|
| `<div onClick={...}>` como botão              | Sem foco, sem teclado, sem semântica        | Use `<button>`                        |
| `outline: none` sem substituto                | Quebra navegação por teclado                | Use `:focus-visible` estilizado       |
| Placeholder como label                        | Some no foco, ruim pra screen reader        | `<label>` sempre visível              |
| Desabilitar submit sem dizer por quê          | Usuário trava sem entender                  | Mostre erros ou hints                 |
| Validação a cada keystroke                    | Irritante, mostra erro antes de terminar    | Valide em blur (ou após primeira submissão) |
| Só `:hover` para affordance                   | Mobile não tem hover                        | Combine com cor/borda/sombra base     |
| Toast para erro crítico                       | Some antes de ser lido                      | Modal/inline para bloqueantes         |
| Infinite scroll sem alternativa               | Impossível achar "Fim", footer inacessível  | "Carregar mais" ou paginação          |
| Confirmação só por cor                        | Daltônicos perdem                           | Cor + ícone + texto                   |
| Modal sem foco preso                          | Tab escapa para fundo                       | Focus trap + ESC fecha                |
| `title` como única dica                       | Mobile não mostra, a11y pobre               | Texto visível ou `aria-describedby`   |
| Texto em cima de imagem sem overlay           | Contraste variável                          | Overlay escuro/gradiente sob o texto  |

## Checklist Final (antes de entregar)

Antes de considerar um componente pronto, confirme:

- [ ] Funciona com **teclado sozinho** (Tab, Shift+Tab, Enter, Espaço, Esc, setas onde faz sentido).
- [ ] Passa em **screen reader** mental (cada elemento tem rótulo/role apropriado).
- [ ] Tem **todos os estados** relevantes (idle, hover, focus-visible, active, disabled, loading, error, empty).
- [ ] **Contraste ≥ 4.5:1** para texto; ≥ 3:1 para UI.
- [ ] **Touch targets ≥ 44×44**.
- [ ] **Responsivo** mobile-first sem scroll horizontal.
- [ ] **Feedback visual** em < 100ms para toda ação.
- [ ] **Mensagens de erro** dizem *o que fazer*.
- [ ] **Empty states** têm CTA ou explicação.
- [ ] **Respeita `prefers-reduced-motion`**.
- [ ] **Inputs de form** têm `label`, `autocomplete`, `type` e `inputmode` corretos.
- [ ] **Nada depende exclusivamente de cor** para transmitir informação.

Se qualquer item falhar, corrija antes de entregar — não é opcional.