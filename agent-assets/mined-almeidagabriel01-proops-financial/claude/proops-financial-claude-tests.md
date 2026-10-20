# tests/ — Estratégia de Testes

Vitest para unit + integration. E2E manual no MVP, automatizado na v2.

---

## Estrutura

```
tests/
├── unit/
│   ├── parsers/            # Parsers OFX e CSV com fixtures reais
│   ├── ai/                 # Lógica de categorização e prompts
│   └── billing/            # Regras de plano, webhook handler
├── integration/
│   └── import-flow.test.ts # Flow completo: upload → parse → categorize → save
└── fixtures/               # Arquivos de exemplo reais
    ├── nubank-sample.csv
    ├── itau-sample.ofx
    └── bradesco-sample.csv
```

---

## Comandos

```bash
npm test              # Vitest — rodar todos os testes
npm run test:watch    # Modo watch para desenvolvimento
npm run test:coverage # Relatório de cobertura (meta: 80% no backend)
```

---

## Cobertura Mínima (NFR13)

**Meta: 80% de cobertura nos módulos de backend (`src/lib/`)**

| Módulo | Prioridade | Tipos de teste |
|--------|-----------|----------------|
| `parsers/` | CRÍTICO | Unit com fixtures reais |
| `ai/categorizer` | CRÍTICO | Unit com mock Claude API |
| `billing/` | ALTA | Unit (lógica de plano, webhook) |
| `utils/` | MÉDIA | Unit (formatação, normalização) |
| `supabase/` | BAIXA | Integration (banco real local) |

---

## Parsers — Testes Críticos

### O que testar
```typescript
// ofx-parser.test.ts
describe('OFX Parser', () => {
  it('extrai FITID como external_id', ...)
  it('converte valores para positivo (crédito) e negativo (débito)', ...)
  it('formata datas como ISO 8601', ...)
  it('lança erro para OFX malformado', ...)
})

// csv-parser.test.ts
describe('CSV Parser', () => {
  it('detecta formato Nubank automaticamente', ...)
  it('detecta formato Itaú automaticamente', ...)
  it('detecta formato Bradesco automaticamente', ...)
  it('gera SHA-256 correto como external_id', ...)
  it('normaliza descrição antes do hash', ...)
  it('detecta delimitador , e ; automaticamente', ...)
  it('ignora headers e linhas em branco', ...)
})
```

### Fixtures
Usar arquivos reais em `tests/fixtures/` — não fabricar dados:
- `nubank-sample.csv` — formato real exportado do Nubank
- `itau-sample.ofx` — OFX real do Itaú
- `bradesco-sample.csv` — CSV real do Bradesco

---

## IA — Testes de Categorização

```typescript
// ai/categorizer.test.ts
describe('Categorizer', () => {
  it('retorna categoria do dicionário do usuário sem chamar IA', ...)
  it('retorna categoria do cache global sem chamar IA', ...)
  it('chama Claude Haiku apenas quando cache/dicionário não têm match', ...)
  it('faz fallback para "outros" quando confiança < threshold', ...)
  it('salva resultado no cache após chamada à IA', ...)
  it('processa batch de 100 transações em uma única chamada API', ...)
})
```

### Mock da Claude API
```typescript
import { vi } from 'vitest'
vi.mock('@anthropic-ai/sdk', () => ({
  Anthropic: vi.fn(() => ({
    messages: {
      create: vi.fn().mockResolvedValue({
        content: [{ text: JSON.stringify([{ category: 'delivery', confidence: 0.95 }]) }]
      })
    }
  }))
}))
```

---

## Billing — Testes

```typescript
// billing/plans.test.ts
describe('Plan Utils', () => {
  it('isPremium retorna true para plan="premium"', ...)
  it('isPremium retorna true durante trial ativo', ...)
  it('isPremium retorna false após trial expirado com plan="free"', ...)
  it('isPremium retorna false para plan="free" sem trial', ...)
})

// billing/webhook-handler.test.ts
describe('Webhook Handler', () => {
  it('ativa Premium ao receber PAYMENT_CONFIRMED', ...)
  it('mantém Premium em período de graça (PAYMENT_OVERDUE)', ...)
  it('revoga Premium ao receber SUBSCRIPTION_CANCELED', ...)
  it('rejeita webhook com token inválido', ...)
})
```

---

## Integration — Import Flow

```typescript
// integration/import-flow.test.ts
// Usa banco Supabase local (supabase start)
describe('Import Flow (Integration)', () => {
  it('faz upload, parse, categorização e save end-to-end para OFX Itaú', ...)
  it('ignora duplicatas ao reimportar mesmo arquivo', ...)
  it('associa todas as transações ao user_id correto (RLS)', ...)
})
```

---

## Padrões

### Nomenclatura de testes
- Descritivos em PT-BR: `it('calcula saldo corretamente para mês sem dados', ...)`
- Arrange → Act → Assert (AAA) sem comentários explícitos

### Fixtures de usuário
```typescript
// helpers/test-user.ts
export const createTestUser = () => ({
  id: 'test-user-uuid',
  plan: 'free' as const,
  trial_ends_at: null,
  ai_queries_today: 0,
})
```

### Não testar implementação, testar comportamento
```typescript
// RUIM: testa detalhe interno
expect(parser._internalState).toBe(...)

// BOM: testa comportamento externo
expect(result.transactions[0].external_id).toMatch(/^[a-f0-9]{64}$/) // SHA-256
```
