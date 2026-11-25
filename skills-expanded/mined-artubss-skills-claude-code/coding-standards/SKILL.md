---
name: coding-standards
description: Padrões de codificação universais, melhores práticas e padrões para desenvolvimento em TypeScript, JavaScript, React e Node.js.
author: affaan-m
version: "1.0"
---

# Padrões de Codificação & Melhores Práticas

Padrões de codificação universais aplicáveis a todos os projetos.

## Princípios de Qualidade de Código

### 1. Legibilidade em Primeiro Lugar
- Código é lido mais do que escrito
- Nomes de variáveis e funções claros
- Código auto-documentado preferível a comentários
- Formatação consistente

### 2. KISS (Keep It Simple, Stupid)
- Solução mais simples que funciona
- Evite engenharia excessiva
- Sem otimização prematura
- Fácil de entender > código clever

### 3. DRY (Don't Repeat Yourself)
- Extraia lógica comum em funções
- Crie componentes reutilizáveis
- Compartilhe utilitários entre módulos
- Evite programação copy-paste

### 4. YAGNI (You Aren't Gonna Need It)
- Não construa features antes de serem necessárias
- Evite generalidade especulativa
- Adicione complexidade apenas quando necessário
- Comece simples, refatore quando needed

## Padrões TypeScript/JavaScript

### Nomenclatura de Variáveis

```typescript
// ✅ GOOD: Nomes descritivos
const marketSearchQuery = 'election'
const isUserAuthenticated = true
const totalRevenue = 1000

// ❌ BAD: Nomes pouco claros
const q = 'election'
const flag = true
const x = 1000
```

### Nomenclatura de Funções

```typescript
// ✅ GOOD: Padrão verbo-substantivo
async function fetchMarketData(marketId: string) { }
function calculateSimilarity(a: number[], b: number[]) { }
function isValidEmail(email: string): boolean { }

// ❌ BAD: Pouco claro ou apenas substantivo
async function market(id: string) { }
function similarity(a, b) { }
function email(e) { }
```

### Padrão de Imutabilidade (CRÍTICO)

```typescript
// ✅ SEMPRE use spread operator
const updatedUser = {
  ...user,
  name: 'New Name'
}

const updatedArray = [...items, newItem]

// ❌ NUNCA mutate diretamente
user.name = 'New Name'  // BAD
items.push(newItem)     // BAD
```

### Tratamento de Erros

```typescript
// ✅ GOOD: Tratamento de erros abrangente
async function fetchData(url: string) {
  try {
    const response = await fetch(url)

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`)
    }

    return await response.json()
  } catch (error) {
    console.error('Fetch failed:', error)
    throw new Error('Failed to fetch data')
  }
}

// ❌ BAD: Sem tratamento de erros
async function fetchData(url) {
  const response = await fetch(url)
  return response.json()
}
```

### Melhores Práticas com Async/Await

```typescript
// ✅ GOOD: Execução paralela quando possível
const [users, markets, stats] = await Promise.all([
  fetchUsers(),
  fetchMarkets(),
  fetchStats()
])

// ❌ BAD: Sequencial quando desnecessário
const users = await fetchUsers()
const markets = await fetchMarkets()
const stats = await fetchStats()
```

### Segurança de Tipos

```typescript
// ✅ GOOD: Tipos apropriados
interface Market {
  id: string
  name: string
  status: 'active' | 'resolved' | 'closed'
  created_at: Date
}

function getMarket(id: string): Promise<Market> {
  // Implementation
}

// ❌ BAD: Usando 'any'
function getMarket(id: any): Promise<any> {
  // Implementation
}
```

## Melhores Práticas React

### Estrutura de Componentes

```typescript
// ✅ GOOD: Componente funcional com tipos
interface ButtonProps {
  children: React.ReactNode
  onClick: () => void
  disabled?: boolean
  variant?: 'primary' | 'secondary'
}

export function Button({
  children,
  onClick,
  disabled = false,
  variant = 'primary'
}: ButtonProps) {
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className={`btn btn-${variant}`}
    >
      {children}
    </button>
  )
}

// ❌ BAD: Sem tipos, estrutura pouco clara
export function Button(props) {
  return <button onClick={props.onClick}>{props.children}</button>
}
```

### Custom Hooks

```typescript
// ✅ GOOD: Custom hook reutilizável
export function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState<T>(value)

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value)
    }, delay)

    return () => clearTimeout(handler)
  }, [value, delay])

  return debouncedValue
}

// Uso
const debouncedQuery = useDebounce(searchQuery, 500)
```

### Gerenciamento de Estado

```typescript
// ✅ GOOD: Atualizações de estado apropriadas
const [count, setCount] = useState(0)

// Atualização funcional baseada no estado anterior
setCount(prev => prev + 1)

// ❌ BAD: Referência direta ao estado
setCount(count + 1)  // Pode ser obsoleto em cenários async
```

### Renderização Condicional

```typescript
// ✅ GOOD: Renderização condicional clara
{isLoading && <Spinner />}
{error && <ErrorMessage error={error} />}
{data && <DataDisplay data={data} />}

// ❌ BAD: Inferno de ternários
{isLoading ? <Spinner /> : error ? <ErrorMessage error={error} /> : data ? <DataDisplay data={data} /> : null}
```

## Padrões de Design de API

### Convenções REST API

```
GET    /api/markets              # Listar todos os markets
GET    /api/markets/:id          # Obter market específico
POST   /api/markets              # Criar novo market
PUT    /api/markets/:id          # Atualizar market (completo)
PATCH  /api/markets/:id          # Atualizar market (parcial)
DELETE /api/markets/:id          # Deletar market

# Parâmetros de query para filtragem
GET /api/markets?status=active&limit=10&offset=0
```

### Formato de Resposta

```typescript
// ✅ GOOD: Estrutura de resposta consistente
interface ApiResponse<T> {
  success: boolean
  data?: T
  error?: string
  meta?: {
    total: number
    page: number
    limit: number
  }
}

// Resposta de sucesso
return NextResponse.json({
  success: true,
  data: markets,
  meta: { total: 100, page: 1, limit: 10 }
})

// Resposta de erro
return NextResponse.json({
  success: false,
  error: 'Invalid request'
}, { status: 400 })
```

### Validação de Entrada

```typescript
import { z } from 'zod'

// ✅ GOOD: Validação com schema
const CreateMarketSchema = z.object({
  name: z.string().min(1).max(200),
  description: z.string().min(1).max(2000),
  endDate: z.string().datetime(),
  categories: z.array(z.string()).min(1)
})

export async function POST(request: Request) {
  const body = await request.json()

  try {
    const validated = CreateMarketSchema.parse(body)
    // Prossiga com dados validados
  } catch (error) {
    if (error instanceof z.ZodError) {
      return NextResponse.json({
        success: false,
        error: 'Validation failed',
        details: error.errors
      }, { status: 400 })
    }
  }
}
```

## Organização de Arquivos

### Estrutura de Projeto

```
src/
├── app/                    # Next.js App Router
│   ├── api/               # Rotas de API
│   ├── markets/           # Páginas de markets
│   └── (auth)/           # Páginas de auth (route groups)
├── components/            # Componentes React
│   ├── ui/               # Componentes UI genéricos
│   ├── forms/            # Componentes de form
│   └── layouts/          # Componentes de layout
├── hooks/                # Custom hooks React
├── lib/                  # Utilitários e configurações
│   ├── api/             # Clientes de API
│   ├── utils/           # Funções auxiliares
│   └── constants/       # Constantes
├── types/                # Tipos TypeScript
└── styles/              # Estilos globais
```

### Nomenclatura de Arquivos

```
components/Button.tsx          # PascalCase para componentes
hooks/useAuth.ts              # camelCase com prefixo 'use'
lib/formatDate.ts             # camelCase para utilitários
types/market.types.ts         # camelCase com sufixo .types
```

## Comentários & Documentação

### Quando Comentar

```typescript
// ✅ GOOD: Explique POR QUÊ, não O QUÊ
// Use exponential backoff para evitar sobrecarregar a API durante outages
const delay = Math.min(1000 * Math.pow(2, retryCount), 30000)

// Intencionalmente usando mutação aqui para performance com grandes arrays
items.push(newItem)

// ❌ BAD: Stating the obvious
// Incrementa contador por 1
count++

// Define nome para nome do usuário
name = user.name
```

### JSDoc para APIs Públicas

```typescript
/**
 * Busca markets usando similaridade semântica.
 *
 * @param query - Consulta de busca em linguagem natural
 * @param limit - Número máximo de resultados (padrão: 10)
 * @returns Array de markets ordenados por score de similaridade
 * @throws {Error} Se API OpenAI falhar ou Redis indisponível
 *
 * @example
 * ```typescript
 * const results = await searchMarkets('election', 5)
 * console.log(results[0].name) // "Trump vs Biden"
 * ```
 */
export async function searchMarkets(
  query: string,
  limit: number = 10
): Promise<Market[]> {
  // Implementation
}
```

## Melhores Práticas de Performance

### Memoização

```typescript
import { useMemo, useCallback } from 'react'

// ✅ GOOD: Memoize computações caras
const sortedMarkets = useMemo(() => {
  return markets.sort((a, b) => b.volume - a.volume)
}, [markets])

// ✅ GOOD: Memoize callbacks
const handleSearch = useCallback((query: string) => {
  setSearchQuery(query)
}, [])
```

### Lazy Loading

```typescript
import { lazy, Suspense } from 'react'

// ✅ GOOD: Lazy load componentes pesados
const HeavyChart = lazy(() => import('./HeavyChart'))

export function Dashboard() {
  return (
    <Suspense fallback={<Spinner />}>
      <HeavyChart />
    </Suspense>
  )
}
```

### Queries de Banco de Dados

```typescript
// ✅ GOOD: Selecione apenas colunas necessárias
const { data } = await supabase
  .from('markets')
  .select('id, name, status')
  .limit(10)

// ❌ BAD: Selecione tudo
const { data } = await supabase
  .from('markets')
  .select('*')
```

## Padrões de Testes

### Estrutura de Testes (Padrão AAA)

```typescript
test('calculates similarity correctly', () => {
  // Arrange
  const vector1 = [1, 0, 0]
  const vector2 = [0, 1, 0]

  // Act
  const similarity = calculateCosineSimilarity(vector1, vector2)

  // Assert
  expect(similarity).toBe(0)
})
```

### Nomenclatura de Testes

```typescript
// ✅ GOOD: Nomes de testes descritivos
test('returns empty array when no markets match query', () => { })
test('throws error when OpenAI API key is missing', () => { })
test('falls back to substring search when Redis unavailable', () => { })

// ❌ BAD: Nomes de testes vagos
test('works', () => { })
test('test search', () => { })
```

## Detecção de Code Smell

Atente-se para estes anti-padrões:

### 1. Funções Longas
```typescript
// ❌ BAD: Função > 50 linhas
function processMarketData() {
  // 100 linhas de código
}

// ✅ GOOD: Divida em funções menores
function processMarketData() {
  const validated = validateData()
  const transformed = transformData(validated)
  return saveData(transformed)
}
```

### 2. Deep Nesting
```typescript
// ❌ BAD: 5+ níveis de aninhamento
if (user) {
  if (user.isAdmin) {
    if (market) {
      if (market.isActive) {
        if (hasPermission) {
          // Faça algo
        }
      }
    }
  }
}

// ✅ GOOD: Early returns
if (!user) return
if (!user.isAdmin) return
if (!market) return
if (!market.isActive) return
if (!hasPermission) return

// Faça algo
```

### 3. Magic Numbers
```typescript
// ❌ BAD: Números sem explicação
if (retryCount > 3) { }
setTimeout(callback, 500)

// ✅ GOOD: Constantes nomeadas
const MAX_RETRIES = 3
const DEBOUNCE_DELAY_MS = 500

if (retryCount > MAX_RETRIES) { }
setTimeout(callback, DEBOUNCE_DELAY_MS)
```

**Lembre-se**: Qualidade de código não é negociável. Código claro e manutenível permite desenvolvimento rápido e refatoração confiante.