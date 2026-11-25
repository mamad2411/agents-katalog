---
name: aws-testing
description: Testing strategies for AWS workloads. Use when writing unit tests, integration tests, contract tests, mocking AWS services, or setting up quality gates and CI/CD test pipelines.
---

# AWS Testing

Skill para estrategias de testing en workloads AWS: pruebas unitarias, integración, contratos, end-to-end, property-based testing, mocking de servicios AWS y quality gates en CI/CD.

## Principios fundamentales

- Test pyramid: muchos unit tests, algunos integration tests, pocos E2E tests.
- Lógica de negocio siempre testeable sin AWS: separar handler de service de repository.
- Mocks para unit tests, servicios reales (o LocalStack/DynamoDB Local) para integration tests.
- Cada PR debe pasar quality gates: tests, linting, type checking, coverage mínimo.
- Property-based testing para validar invariantes y encontrar edge cases que los tests manuales no cubren.

## Pirámide de testing para serverless

```
        ┌─────────┐
        │  E2E    │  Pocos: flujos críticos contra stack desplegado
        ├─────────┤
        │ Integr. │  Algunos: Lambda + DynamoDB Local, API contracts
        ├─────────┤
        │  Unit   │  Muchos: lógica de negocio pura, sin AWS
        └─────────┘
```

## Unit testing

### Python con pytest
```python
import pytest
from unittest.mock import MagicMock
from functions.orders.service import OrderService

@pytest.fixture
def mock_repo():
    return MagicMock()

def test_create_order_success(mock_repo):
    mock_repo.save.return_value = None
    service = OrderService(mock_repo)
    result = service.create({"item": "laptop", "quantity": 1, "price": 999.99})
    assert result["status"] == "created"
    mock_repo.save.assert_called_once()

def test_create_order_invalid_quantity(mock_repo):
    service = OrderService(mock_repo)
    with pytest.raises(ValueError, match="quantity must be positive"):
        service.create({"item": "laptop", "quantity": 0, "price": 999.99})
```

### TypeScript con Vitest
```typescript
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { OrderService } from './service';

describe('OrderService', () => {
  const mockRepo = { save: vi.fn(), findById: vi.fn() };

  beforeEach(() => vi.clearAllMocks());

  it('should create order successfully', async () => {
    mockRepo.save.mockResolvedValue(undefined);
    const service = new OrderService(mockRepo);
    const result = await service.create({ item: 'laptop', quantity: 1, price: 999.99 });
    expect(result.status).toBe('created');
    expect(mockRepo.save).toHaveBeenCalledOnce();
  });

  it('should reject invalid quantity', async () => {
    const service = new OrderService(mockRepo);
    await expect(service.create({ item: 'laptop', quantity: 0, price: 999.99 }))
      .rejects.toThrow('quantity must be positive');
  });
});
```

## Integration testing

### DynamoDB Local con Vitest
```typescript
import { DynamoDBClient, CreateTableCommand } from '@aws-sdk/client-dynamodb';
import { DynamoDBDocumentClient } from '@aws-sdk/lib-dynamodb';

const client = new DynamoDBClient({ endpoint: 'http://localhost:8000', region: 'local' });
const docClient = DynamoDBDocumentClient.from(client);

beforeAll(async () => {
  await client.send(new CreateTableCommand({
    TableName: 'test-orders',
    KeySchema: [
      { AttributeName: 'PK', KeyType: 'HASH' },
      { AttributeName: 'SK', KeyType: 'RANGE' },
    ],
    AttributeDefinitions: [
      { AttributeName: 'PK', AttributeType: 'S' },
      { AttributeName: 'SK', AttributeType: 'S' },
    ],
    BillingMode: 'PAY_PER_REQUEST',
  }));
});

it('should persist and retrieve order', async () => {
  const repo = new OrderRepository(docClient, 'test-orders');
  await repo.save({ id: 'order-1', item: 'laptop', quantity: 1 });
  const result = await repo.findById('order-1');
  expect(result).toMatchObject({ id: 'order-1', item: 'laptop' });
});
```

## Contract testing

### Validar respuestas contra OpenAPI spec
```typescript
import { describe, it, expect } from 'vitest';
import Ajv from 'ajv';
import spec from '../openapi.json';

const ajv = new Ajv({ allErrors: true });

describe('API Contract', () => {
  it('list orders response matches schema', async () => {
    const response = await callApi('GET', '/orders');
    const schema = spec.paths['/orders'].get.responses['200'].content['application/json'].schema;
    const validate = ajv.compile(schema);
    expect(validate(response.data)).toBe(true);
  });
});
```

## Property-based testing

### Con fast-check (TypeScript)
```typescript
import { describe, it, expect } from 'vitest';
import fc from 'fast-check';
import { calculateDiscount } from './pricing';

describe('calculateDiscount properties', () => {
  it('discount never exceeds original price', () => {
    fc.assert(
      fc.property(
        fc.float({ min: 0.01, max: 10000, noNaN: true }),
        fc.float({ min: 0, max: 1, noNaN: true }),
        (price, discountRate) => {
          const discount = calculateDiscount(price, discountRate);
          return discount >= 0 && discount <= price;
        }
      )
    );
  });

  it('zero discount rate returns zero discount', () => {
    fc.assert(
      fc.property(
        fc.float({ min: 0.01, max: 10000, noNaN: true }),
        (price) => calculateDiscount(price, 0) === 0
      )
    );
  });
});
```

### Con Hypothesis (Python)
```python
from hypothesis import given, strategies as st
from functions.pricing.service import calculate_discount

@given(
    price=st.floats(min_value=0.01, max_value=10000, allow_nan=False),
    discount_rate=st.floats(min_value=0, max_value=1, allow_nan=False),
)
def test_discount_never_exceeds_price(price, discount_rate):
    discount = calculate_discount(price, discount_rate)
    assert 0 <= discount <= price

@given(price=st.floats(min_value=0.01, max_value=10000, allow_nan=False))
def test_zero_rate_zero_discount(price):
    assert calculate_discount(price, 0) == 0
```

## Mocking de servicios AWS

### Patrón de inyección de dependencias (recomendado)
```typescript
// repository.ts - acepta cliente inyectado
export class OrderRepository {
  constructor(private readonly docClient: DynamoDBDocumentClient, private readonly tableName: string) {}

  async save(order: Order): Promise<void> {
    await this.docClient.send(new PutCommand({ TableName: this.tableName, Item: order }));
  }
}

// test - inyectar mock
const mockClient = { send: vi.fn() };
const repo = new OrderRepository(mockClient as any, 'test-table');
```

### aws-sdk-client-mock (alternativa)
```typescript
import { mockClient } from 'aws-sdk-client-mock';
import { DynamoDBDocumentClient, PutCommand } from '@aws-sdk/lib-dynamodb';

const ddbMock = mockClient(DynamoDBDocumentClient);

beforeEach(() => ddbMock.reset());

it('should save order', async () => {
  ddbMock.on(PutCommand).resolves({});
  await repo.save({ id: '1', item: 'laptop' });
  expect(ddbMock.calls()).toHaveLength(1);
});
```

## Quality gates en CI/CD

```yaml
# GitHub Actions example
jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '20' }
      - run: npm ci
      - run: npm run lint          # ESLint
      - run: npm run typecheck     # tsc --noEmit
      - run: npm run test:unit     # Vitest unit tests
      - run: npm run test:coverage # Coverage >= 80%
      - run: npm run test:integration # Con DynamoDB Local
```

### Coverage mínimo recomendado
| Tipo | Mínimo | Ideal |
|---|---|---|
| Lógica de negocio (service) | 90% | 95%+ |
| Handlers | 80% | 90%+ |
| Repositories | 70% | 80%+ |
| Global del proyecto | 80% | 85%+ |

## Anti-patrones a evitar

- ❌ Tests que dependen de servicios AWS reales para unit tests.
- ❌ No tener tests para lógica de negocio.
- ❌ Tests frágiles que dependen de orden de ejecución o estado compartido.
- ❌ Mocks que no reflejan el comportamiento real del servicio.
- ❌ Solo happy path, sin tests de error y edge cases.
- ❌ Coverage como métrica vanidosa (100% coverage con assertions vacías).
- ❌ Tests de integración sin cleanup (datos residuales entre tests).
- ❌ No correr tests en CI/CD.
- ❌ Ignorar property-based testing para lógica con invariantes.
- ❌ Tests lentos que nadie ejecuta localmente.

## Checklist de testing

- [ ] Unit tests para toda lógica de negocio con mocks.
- [ ] Integration tests con DynamoDB Local o LocalStack.
- [ ] Contract tests contra OpenAPI spec.
- [ ] Property-based tests para invariantes críticos.
- [ ] Coverage mínimo configurado y enforced en CI.
- [ ] Quality gates en CI: lint + typecheck + tests.
- [ ] Tests de error y edge cases, no solo happy path.
- [ ] Fixtures y factories para datos de test reutilizables.
- [ ] Tests ejecutables localmente en < 30 segundos.
- [ ] Cleanup automático en tests de integración.
