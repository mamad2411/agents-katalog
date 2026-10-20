---
name: criar-teste-unitario
description: "Escreve testes unitários Jest com mocking e isolamento de componentes. Use quando o dev-backend precisa cobrir lógica isolada com testes."
author: "Pedro Andriow (https://github.com/Andriow)"
disable-model-invocation: true
---

# Skill: criar-teste-unitario

Escreve **testes unitários Jest** para services, utils e regras de negócio em Node.js/NestJS: mocka dependências externas na fronteira, cobre casos de sucesso e de erro, e segue as convenções de nomenclatura do projeto.

**Agente:** dev-backend  
**Guardrails aplicáveis:** `00-core.md`, `testes.md`  
**Referências rápidas:** `References/testing-patterns.md`

---

## Quando usar

- Para cobrir a lógica de uma `Service` NestJS com testes isolados
- Para testar função utilitária ou regra de negócio pura
- Após implementar endpoint com `implementar-endpoint` — testes são parte da entrega
- Para aumentar cobertura de código existente identificado por `auditar-cobertura`

---

## O que é unitário

Teste unitário testa **uma unidade de lógica em isolamento**. No contexto NestJS:
- A unidade é a `Service` (ou função pura)
- Dependências (PrismaService, clients HTTP, outros services) são **mockadas**
- Não há banco de dados real, não há HTTP real
- Cada teste é rápido (< 100ms) e determinístico

---

## Processo de execução

### Passo 1 — Criar o arquivo de teste

Localização: ao lado do arquivo que está sendo testado (colocado):
```
src/modules/user/user.service.ts
src/modules/user/user.service.spec.ts  ← aqui
```

### Passo 2 — Montar o TestingModule

```typescript
import { Test, TestingModule } from '@nestjs/testing';
import { UserService } from './user.service';
import { PrismaService } from '../../prisma/prisma.service';
import { ConflictException, NotFoundException } from '@nestjs/common';

// Mock apenas da dependência de infraestrutura — testes.md §2
const mockPrismaService = {
  user: {
    findUnique: jest.fn(),
    findMany: jest.fn(),
    create: jest.fn(),
    update: jest.fn(),
  },
};

describe('UserService', () => {
  let service: UserService;
  let prisma: typeof mockPrismaService;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [
        UserService,
        { provide: PrismaService, useValue: mockPrismaService },
      ],
    }).compile();

    service = module.get<UserService>(UserService);
    prisma = module.get(PrismaService);
  });

  // Limpar mocks após cada teste — testes.md §3
  afterEach(() => jest.clearAllMocks());
});
```

### Passo 3 — Escrever casos de teste

Nomenclatura obrigatória: `should <comportamento> when <condição>` — `testes.md §1`

**Caso de sucesso:**
```typescript
describe('create', () => {
  it('should return created user when data is valid', async () => {
    // Arrange
    const dto = { name: 'João Silva', email: 'joao@example.com' };
    const dbUser = { id: 'uuid-1', ...dto, createdAt: new Date(), deletedAt: null };

    prisma.user.findUnique.mockResolvedValue(null);   // email não existe
    prisma.user.create.mockResolvedValue(dbUser);

    // Act
    const result = await service.create(dto);

    // Assert
    expect(result).toEqual({ id: 'uuid-1', name: 'João Silva', createdAt: dbUser.createdAt });
    expect(prisma.user.create).toHaveBeenCalledWith({ data: dto });
  });
});
```

**Caso de erro de negócio:**
```typescript
  it('should throw ConflictException when email already exists', async () => {
    // Arrange
    const dto = { name: 'João', email: 'joao@example.com' };
    prisma.user.findUnique.mockResolvedValue({ id: 'existing-id', ...dto });

    // Act & Assert
    await expect(service.create(dto)).rejects.toThrow(ConflictException);
    expect(prisma.user.create).not.toHaveBeenCalled();
  });
```

**Caso de not found:**
```typescript
describe('findOne', () => {
  it('should throw NotFoundException when user does not exist', async () => {
    prisma.user.findUnique.mockResolvedValue(null);

    await expect(service.findOne('non-existent-id')).rejects.toThrow(NotFoundException);
  });

  it('should return user when id exists', async () => {
    const user = { id: 'uuid-1', name: 'João', email: 'joao@example.com', createdAt: new Date() };
    prisma.user.findUnique.mockResolvedValue(user);

    const result = await service.findOne('uuid-1');

    expect(result.id).toBe('uuid-1');
    expect(prisma.user.findUnique).toHaveBeenCalledWith({ where: { id: 'uuid-1', deletedAt: null } });
  });
});
```

### Passo 4 — Cobrir casos de borda

Para cada método, cobrir:
- [ ] Caminho feliz (input válido, resultado esperado)
- [ ] Recurso não encontrado (404)
- [ ] Duplicidade / conflito (409)
- [ ] Regra de negócio violada (422)
- [ ] Input inválido — se validado na service (400)

### Passo 5 — Verificar que o mock não substitui lógica interna

Regra: só mockar dependências injetadas (PrismaService, clients, outros services).  
Nunca mockar métodos privados da própria service sendo testada (`testes.md §2`).

```typescript
// ⛔ mock de método interno — proibido
jest.spyOn(service as any, 'toResponseDto').mockReturnValue({...});

// ✅ mock apenas da dependência de infraestrutura
prisma.user.findUnique.mockResolvedValue(null);
```

### Passo 6 — Garantir que testes são independentes

- `beforeEach` recria o módulo e os mocks — nunca `beforeAll` com estado mutável
- `afterEach(() => jest.clearAllMocks())` — não acumular estado entre testes
- Não depender de ordem de execução dos casos

---

## Cobertura esperada por tipo de método

| Método | Casos mínimos |
|---|---|
| `create` | Sucesso, conflito/duplicidade |
| `findOne` | Sucesso, not found |
| `findAll` | Sucesso com resultados, sucesso sem resultados |
| `update` | Sucesso, not found, conflito se aplicável |
| `delete` (soft) | Sucesso, not found |
| Regra de negócio | Caminho feliz + cada condição de rejeição |

---

## Racionalizações bloqueadas

| Racionalização | Rebate |
|---|---|
| "O código é simples, não precisa de teste" | Código simples hoje volta complexo amanhã quando alguém adicionar lógica de negócio. Teste agora é documentação executável do comportamento esperado. |
| "Vou escrever os testes depois que a feature estiver pronta" | "Depois" raramente acontece. Testes escritos depois tendem a confirmar a implementação em vez de especificar o comportamento — perdem o valor de design. |
| "Mockar tudo é mais rápido e o teste ainda passa" | Teste que mocka a própria lógica interna não testa nada — é teatro de qualidade. Mock só nas dependências injetadas; o comportamento da service deve ser real. |
| "Cobertura de 80% já é suficiente, posso pular esse caso de erro" | Cobertura mede linhas executadas, não comportamento testado. O caso de erro que você pular é o que vai falhar em produção às 3h da manhã. |
| "Esse teste está quebrando, vou ajustar o mock para passar" | Teste quebrando é sinal — não ruído. Ajustar o mock para passar sem entender por que quebrou é silenciar o alarme sem apagar o incêndio. |

---

## Saída produzida

- Arquivo `<nome>.service.spec.ts` ao lado da service
- Todos os casos do checklist acima cobertos
- `npm test` passando sem erros
