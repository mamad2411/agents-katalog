---
name: pattern-clean-architecture
description: |
  Layered architecture with dependency inversion. Domain/Application/Presentation/
  Infrastructure separation. For complex business logic, long-term maintainability, 
  testability. AVOID for simple CRUD apps or MVPs. Foundational pattern.
---

# 🧅 Clean Architecture — Чистая Архитектура

<purpose>
Паттерн слоёной архитектуры с чётким разделением ответственностей.
Инверсия зависимостей: бизнес-логика не зависит от фреймворков.
</purpose>

---

## Когда Использовать

**Подходит для:**

- Проекты со сложной бизнес-логикой
- Долгоживущие проекты (>1 года поддержки)
- Проекты с высокими требованиями к тестируемости
- Команды >2 человек
- Проекты с возможной сменой технологий

**НЕ подходит для:**

- MVP / PoC с ограниченным временем
- Простые CRUD приложения
- Одноразовые скрипты
- Прототипы

**Сложность внедрения:** 🟡 Medium

---

## Концепция

### Принцип Зависимостей

```
Зависимости направлены ВНУТРЬ.
Внутренние слои ничего не знают о внешних.

    ┌─────────────────────────────────┐
    │         Infrastructure          │  ← Frameworks, DB, External
    │   ┌─────────────────────────┐   │
    │   │       Presentation      │   │  ← Controllers, Views
    │   │   ┌─────────────────┐   │   │
    │   │   │   Application   │   │   │  ← Use Cases
    │   │   │   ┌─────────┐   │   │   │
    │   │   │   │ Domain  │   │   │   │  ← Entities, Business Rules
    │   │   │   └─────────┘   │   │   │
    │   │   └─────────────────┘   │   │
    │   └─────────────────────────┘   │
    └─────────────────────────────────┘
```

### Ключевые Принципы

1. **Dependency Inversion** — зависимости направлены к центру
2. **Separation of Concerns** — каждый слой отвечает за своё
3. **Testability** — бизнес-логика тестируется без внешних зависимостей
4. **Framework Independence** — можно заменить фреймворк/БД

---

## Слои

### 1. Domain Layer (Core)

**Ответственность:** Бизнес-сущности и правила.

**Содержит:**

- Entities — бизнес-объекты с идентичностью
- Value Objects — иммутабельные объекты без идентичности
- Domain Services — логика, не принадлежащая одной сущности
- Domain Events — события предметной области
- Repository Interfaces — контракты (НЕ реализации!)

**Правила:**

- ❌ Никаких зависимостей от внешних библиотек
- ❌ Никаких импортов из других слоёв
- ✅ Только чистый язык (TypeScript/Python/etc.)
- ✅ Полностью тестируем в изоляции

**Пример структуры:**

```
/domain
├── entities/
│   ├── User.ts
│   └── Order.ts
├── value-objects/
│   ├── Email.ts
│   └── Money.ts
├── services/
│   └── PricingService.ts
├── events/
│   └── OrderPlaced.ts
└── repositories/
    ├── IUserRepository.ts    # Интерфейс!
    └── IOrderRepository.ts   # Интерфейс!
```

### 2. Application Layer (Use Cases)

**Ответственность:** Оркестрация бизнес-процессов.

**Содержит:**

- Use Cases / Interactors — конкретные сценарии использования
- DTOs — объекты передачи данных
- Application Services — координация use cases
- Port Interfaces — входные/выходные порты

**Правила:**

- ✅ Зависит от Domain Layer
- ❌ НЕ зависит от Infrastructure
- ❌ НЕ содержит бизнес-логику (только оркестрация)
- ✅ Один Use Case = один файл

**Пример структуры:**

```
/application
├── use-cases/
│   ├── user/
│   │   ├── CreateUser.ts
│   │   ├── GetUserById.ts
│   │   └── UpdateUserEmail.ts
│   └── order/
│       ├── PlaceOrder.ts
│       └── CancelOrder.ts
├── dtos/
│   ├── UserDTO.ts
│   └── OrderDTO.ts
└── ports/
    ├── input/
    │   └── IUserService.ts
    └── output/
        └── IEmailSender.ts
```

### 3. Presentation Layer (Interface Adapters)

**Ответственность:** Адаптация внешних запросов к внутренним контрактам.

**Содержит:**

- Controllers — обработка HTTP/CLI/etc.
- Presenters — форматирование ответов
- View Models — данные для отображения
- Mappers — преобразование между слоями

**Правила:**

- ✅ Зависит от Application Layer
- ✅ Вызывает Use Cases
- ❌ НЕ содержит бизнес-логику
- ❌ НЕ обращается напрямую к Domain

**Пример структуры:**

```
/presentation
├── http/
│   ├── controllers/
│   │   ├── UserController.ts
│   │   └── OrderController.ts
│   ├── middleware/
│   │   └── AuthMiddleware.ts
│   └── routes/
│       └── index.ts
├── cli/
│   └── commands/
│       └── CreateUserCommand.ts
└── graphql/
    ├── resolvers/
    └── schema/
```

### 4. Infrastructure Layer

**Ответственность:** Реализация внешних зависимостей.

**Содержит:**

- Repository Implementations — работа с БД
- External Services — интеграции, API клиенты
- Framework Configurations — настройки фреймворков
- Persistence — ORM, миграции

**Правила:**

- ✅ Реализует интерфейсы из Domain/Application
- ✅ Содержит все внешние зависимости
- ❌ Бизнес-логика не размещается здесь

**Пример структуры:**

```
/infrastructure
├── persistence/
│   ├── repositories/
│   │   ├── PostgresUserRepository.ts
│   │   └── PostgresOrderRepository.ts
│   ├── orm/
│   │   └── prisma/
│   └── migrations/
├── external/
│   ├── email/
│   │   └── SendGridEmailSender.ts
│   └── payment/
│       └── StripePaymentGateway.ts
├── config/
│   ├── database.ts
│   └── app.ts
└── di/
    └── container.ts    # Dependency Injection
```

---

## Dependency Injection

### Принцип

```typescript
// ❌ WRONG: Use Case зависит от конкретной реализации
class CreateUser {
  private repo = new PostgresUserRepository(); // Жёсткая связь!
}

// ✅ RIGHT: Use Case зависит от интерфейса
class CreateUser {
  constructor(private repo: IUserRepository) {} // Инъекция!
}
```

### Схема DI

```
Composition Root (main.ts / app.ts)
         │
         ├── Создаёт Infrastructure implementations
         ├── Создаёт Application use cases с инъекцией
         └── Конфигурирует Presentation layer
```

### Пример Composition Root

```typescript
// /infrastructure/di/container.ts

import { IUserRepository } from '@/domain/repositories/IUserRepository';
import { PostgresUserRepository } from '@/infrastructure/persistence/repositories/PostgresUserRepository';
import { CreateUser } from '@/application/use-cases/user/CreateUser';
import { UserController } from '@/presentation/http/controllers/UserController';

// Wiring
const userRepository: IUserRepository = new PostgresUserRepository();
const createUser = new CreateUser(userRepository);
const userController = new UserController(createUser);

export { userController };
```

---

## Структура Проекта

### Вариант 1: Flat (по слоям)

```
/src
├── domain/
├── application/
├── presentation/
├── infrastructure/
└── main.ts
```

**Когда использовать:** Небольшие проекты, один bounded context.

### Вариант 2: Modular (по фичам)

```
/src
├── modules/
│   ├── user/
│   │   ├── domain/
│   │   ├── application/
│   │   ├── presentation/
│   │   └── infrastructure/
│   └── order/
│       ├── domain/
│       ├── application/
│       ├── presentation/
│       └── infrastructure/
├── shared/
│   ├── domain/
│   └── infrastructure/
└── main.ts
```

**Когда использовать:** Средние/большие проекты, несколько bounded contexts.

---

## Data Flow

### Пример: Create User

```
HTTP Request
     │
     ▼
┌─────────────┐
│ Controller  │  ← Парсит request, валидирует input
└──────┬──────┘
       │ CreateUserDTO
       ▼
┌─────────────┐
│  Use Case   │  ← Оркестрирует логику
│ CreateUser  │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Domain    │  ← Создаёт User entity
│    User     │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Repository  │  ← IUserRepository.save()
│ (Interface) │
└──────┬──────┘
       │ Реализация
       ▼
┌─────────────┐
│  Postgres   │  ← PostgresUserRepository
│ Repository  │
└──────┬──────┘
       │
       ▼
   Database
```

---

## Тестирование

### Unit Tests

**Domain Layer:**

```typescript
// Тестируем без зависимостей
describe('User', () => {
  it('should validate email format', () => {
    expect(() => new User('invalid-email')).toThrow();
  });
});
```

**Application Layer:**

```typescript
// Мокаем репозитории
describe('CreateUser', () => {
  it('should create user', async () => {
    const mockRepo: IUserRepository = {
      save: jest.fn(),
      findById: jest.fn(),
    };
    
    const useCase = new CreateUser(mockRepo);
    await useCase.execute({ email: 'test@test.com' });
    
    expect(mockRepo.save).toHaveBeenCalled();
  });
});
```

### Integration Tests

**Infrastructure:**

```typescript
// Тестируем с реальной БД (test container)
describe('PostgresUserRepository', () => {
  it('should persist and retrieve user', async () => {
    const repo = new PostgresUserRepository(testDb);
    const user = new User('test@test.com');
    
    await repo.save(user);
    const found = await repo.findById(user.id);
    
    expect(found).toEqual(user);
  });
});
```

---

## Common Mistakes

### ❌ Анемичные Сущности

```typescript
// WRONG: Сущность без поведения
class User {
  id: string;
  email: string;
  name: string;
}

// RIGHT: Сущность с бизнес-логикой
class User {
  private constructor(
    public readonly id: string,
    private _email: Email,
    private _name: string
  ) {}

  changeEmail(newEmail: Email): void {
    // Валидация и бизнес-правила
    this._email = newEmail;
  }
}
```

### ❌ Бизнес-логика в Use Case

```typescript
// WRONG
class CreateOrder {
  execute(dto: CreateOrderDTO) {
    if (dto.items.length === 0) throw new Error('Empty order'); // Логика!
    const total = dto.items.reduce((sum, i) => sum + i.price, 0); // Логика!
  }
}

// RIGHT: Логика в Domain
class Order {
  static create(items: OrderItem[]): Order {
    if (items.length === 0) throw new DomainError('Empty order');
    return new Order(items, this.calculateTotal(items));
  }
}
```

### ❌ Прямые зависимости от Infrastructure

```typescript
// WRONG
import { PrismaClient } from '@prisma/client'; // В Application слое!

// RIGHT
import { IUserRepository } from '@/domain/repositories/IUserRepository';
```

---

## Чеклист Внедрения

### Domain

- [ ] Entities содержат бизнес-логику
- [ ] Value Objects иммутабельные
- [ ] Repository — только интерфейсы
- [ ] Нет внешних зависимостей

### Application

- [ ] Use Cases — один класс = один сценарий
- [ ] DTOs для входа/выхода
- [ ] Нет прямых зависимостей от Infrastructure

### Presentation

- [ ] Controllers только вызывают Use Cases
- [ ] Валидация входных данных
- [ ] Маппинг в/из DTOs

### Infrastructure

- [ ] Реализует интерфейсы из Domain/Application
- [ ] DI Container настроен
- [ ] Все внешние зависимости изолированы

---

## Quick Reference

```
Domain    → Entities, Value Objects, Interfaces
Application → Use Cases, DTOs, Orchestration  
Presentation → Controllers, Adapters, IO
Infrastructure → DB, External APIs, Framework

Зависимости: Infrastructure → Presentation → Application → Domain
                    ↓              ↓              ↓
              [implements]    [uses]        [uses]
```

---

**Связанные файлы:**

- `.claude/skills/pattern-modular-monolith/SKILL.md` — альтернативный паттерн
- `.claude/skills/workflow-new-project/SKILL.md` — применение при создании проекта

---

**END OF PATTERN**
