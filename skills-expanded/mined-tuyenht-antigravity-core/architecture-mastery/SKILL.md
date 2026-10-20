---
name: architecture-mastery
description: "Đỉnh cao kiến trúc tổng hợp: API, Microservices, GraphQL và Design Patterns cốt lõi."
version: 2.0
consolidates: architecture, api-patterns, microservices-communication, graphql-patterns
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Architecture Mastery - Software Architecture & Design

> **Unified Skill:** This consolidates all architecture knowledge into one hierarchical structure.

---

## 🎯 Core Principles

### SOLID Principles (Foundation)

**S - Single Responsibility:**
```
Each class/module should have ONE reason to change.
❌ UserController handles auth, profile, and notifications
✅ AuthController, ProfileController, NotificationController
```

**O - Open/Closed:**
```
Open for extension, closed for modification.
Use interfaces/abstractions to add new behavior without changing existing code.
```

**L - Liskov Substitution:**
```
Subtypes must be substitutable for their base types.
If S is subtype of T, objects of type T can be replaced with S without breaking.
```

**I - Interface Segregation:**
```
Many specific interfaces > One general interface.
❌ IAnimal { fly(), swim(), walk() } ← Not all animals do all
✅ IFlyable { fly() }, ISwimmable { swim() }, IWalkable { walk() }
```

**D - Dependency Inversion:**
```
Depend on abstractions, not concretions.
❌ class UserService { constructor(private db: MySQLDatabase) }
✅ class UserService { constructor(private db: IDatabase) }
```

---

## 🏗️ Layered Architecture

**Standard 3-Tier:**
```
┌─────────────────────────┐
│  Presentation Layer      │ ← Controllers, Views, API Routes
│  (UI/API)               │
├─────────────────────────┤
│  Business Logic Layer    │ ← Services, Use Cases, Domain Logic
│  (Services)             │
├─────────────────────────┤
│  Data Access Layer       │ ← Repositories, ORM, Database
│  (Repositories)         │
└──────────────────────┘
```

**Rules:**
- ✅ Upper layers depend on lower layers
- ❌ Lower layers NEVER depend on upper layers
- ❌ NO business logic in controllers
- ❌ NO database queries in controllers

---

## 📚 Architecture Patterns

### Pattern Navigation

**By Need:**
- **REST APIs?** → See [API Design Patterns](./patterns/api-design.md)
- **Microservices?** → See [Microservices Communication](./patterns/microservices.md)
- **GraphQL?** → See [GraphQL Patterns](./patterns/graphql.md)
- **Event-Driven?** → See [Event Sourcing](./patterns/event-sourcing.md)

---

## 🎯 Common Patterns

### 1. Repository Pattern

**Purpose:** Abstract data access

**Structure:**
```typescript
// Interface (abstraction)
interface IUserRepository {
  findById(id: string): Promise<User | null>
  save(user: User): Promise<User>
  delete(id: string): Promise<void>
}

// Implementation
class DatabaseUserRepository implements IUserRepository {
  async findById(id: string): Promise<User | null> {
    return await db.users.findUnique({ where: { id } })
  }
  
  async save(user: User): Promise<User> {
    return await db.users.create({ data: user })
  }
  
  async delete(id: string): Promise<void> {
    await db.users.delete({ where: { id } })
  }
}

// Service uses abstraction
class UserService {
  constructor(private repo: IUserRepository) {}
  
  async getUser(id: string) {
    return await this.repo.findById(id)
  }
}
```

**Benefits:**
- ✅ Easy to test (mock repository)
- ✅ Can swap database implementations
- ✅ Business logic isolated from data access

---

### 2. Service Layer Pattern

**Purpose:** Encapsulate business logic

**Structure:**
```typescript
// ❌ Bad: Business logic in controller
class UserController {
  async create(req: Request) {
    // Validation
    if (!req.body.email) throw new Error('Email required')
    if (!isValidEmail(req.body.email)) throw new Error('Invalid email')
    
    // Business logic (should NOT be here!)
    const existingUser = await db.users.findOne({ email: req.body.email })
    if (existingUser) throw new Error('Email already exists')
    
    const hashedPassword = await bcrypt.hash(req.body.password, 10)
    const user = await db.users.create({
      email: req.body.email,
      password: hashedPassword
    })
    
    await emailService.sendWelcome(user.email)
    
    return user
  }
}

// ✅ Good: Business logic in service
class UserService {
  constructor(
    private userRepo: IUserRepository,
    private emailService: IEmailService
  ) {}
  
  async createUser(data: CreateUserDTO): Promise<User> {
    // Check email uniqueness
    const existing = await this.userRepo.findByEmail(data.email)
    if (existing) throw new ConflictError('Email already exists')
    
    // Hash password
    const hashedPassword = await bcrypt.hash(data.password, 10)
    
    // Create user
    const user = await this.userRepo.save({
      email: data.email,
      password: hashedPassword
    })
    
    // Send welcome email
    await this.emailService.sendWelcome(user.email)
    
    return user
  }
}

// Controller is thin
class UserController {
  constructor(private userService: UserService) {}
  
  async create(req: Request) {
    // Validate input (presentation layer)
    const data = CreateUserDTO.parse(req.body)
    
    // Delegate to service
    const user = await this.userService.createUser(data)
    
    return { success: true, data: user }
  }
}
```

---

### 3. Dependency Injection

**Purpose:** Inversion of Control

**Structure:**
```typescript
// ❌ Bad: Hard dependencies
class UserService {
  private repo = new MySQLUserRepository() // ← Tightly coupled!
  
  async getUser(id: string) {
    return this.repo.findById(id)
  }
}

// ✅ Good: Inject dependencies
class UserService {
  constructor(private repo: IUserRepository) {} // ← Loosely coupled
  
  async getUser(id: string) {
    return this.repo.findById(id)
  }
}

// Usage (dependency injection container)
const repo = new MySQLUserRepository()
const service = new UserService(repo)

// Or for testing
const mockRepo = new MockUserRepository()
const service = new UserService(mockRepo)
```

**Benefits:**
- ✅ Testable (inject mocks)
- ✅ Flexible (swap implementations)
- ✅ Follows Dependency Inversion Principle

---

## 🌐 API Architecture

**Full guide:** [patterns/api-design.md](./patterns/api-design.md)

### REST Best Practices

**Resource naming:**
```
✅ /users
✅ /users/123
✅ /users/123/posts
✅ /users/123/posts/456

❌ /getUsers
❌ /user/get/123
❌ /createPost
```

**HTTP Methods:**
```
GET    /users      → List users
GET    /users/123  → Get user
POST   /users      → Create user
PUT    /users/123  → Replace user
PATCH  /users/123  → Update user
DELETE /users/123  → Delete user
```

**Status Codes:**
```
200 OK              → Successful GET, PUT, PATCH
201 Created         → Successful POST
204 No Content      → Successful DELETE
400 Bad Request     → Validation error
401 Unauthorized    → Not authenticated
403 Forbidden       → Not authorized
404 Not Found       → Resource doesn't exist
422 Unprocessable   → Semantic error
500 Server Error    → Internal error
```

---

## 🏢 Microservices Architecture

**Full guide:** [patterns/microservices.md](./patterns/microservices.md)

### When to Use Microservices

**✅ Use when:**
- Large team (>50 developers)
- Independent scaling needed
- Different tech stacks per service
- High organizational maturity

**❌ Don't use when:**
- Small team (<10 developers)
- Simple application
- Limited DevOps resources
- Unsure of service boundaries

### Communication Patterns

**Synchronous:**
- REST APIs
- gRPC

**Asynchronous:**
- Message queues (RabbitMQ, SQS)
- Event streams (Kafka)
- Pub/Sub (Redis, Google Pub/Sub)

---

## 🔮 GraphQL Architecture

**Full guide:** [patterns/graphql.md](./patterns/graphql.md)

### When to Use GraphQL

**✅ Use when:**
- Multiple clients with different needs
- Complex data relationships
- Need flexible queries
- Want type safety

**❌ Don't use when:**
- Simple CRUD APIs
- File uploads primary use case
- Caching requirements complex
- Team unfamiliar with GraphQL

---

## 📊 Decision Framework

### Choosing Architecture

```
Start Here
    ↓
Is it a simple CRUD app?
    ├─ YES → Monolith with MVC pattern
    └─ NO → Continue
             ↓
Multiple teams/services?
    ├─ YES → Microservices
    └─ NO → Modular Monolith
             ↓
API-first design?
    ├─ REST → Standard for public APIs
    ├─ GraphQL →Complex queries/multiple clients
    └─ gRPC → Internal services, performance-critical
```

---

## ✅ Architecture Checklist

**Before Starting:**
- [ ] Identified bounded contexts
- [ ] Defined service boundaries
- [ ] Chosen communication patterns
- [ ] Decided on data ownership
- [ ] Planned for failure modes

**During Development:**
- [ ] Following SOLID principles
- [ ] Using layered architecture
- [ ] Dependency injection implemented
- [ ] Business logic in services
- [ ] Controllers are thin (<10 lines per method)

**Before Deployment:**
- [ ] API documentation complete
- [ ] Error handling consistent
- [ ] Logging implemented
- [ ] Monitoring in place
- [ ] Security hardened

---

## 🔗 Related Files

- [API Design Patterns](./patterns/api-design.md)
- [Microservices Communication](./patterns/microservices.md)
- [GraphQL Patterns](./patterns/graphql.md)
- [Event Sourcing](./patterns/event-sourcing.md)

---

## 📚 External Resources

- [Clean Architecture (Uncle Bob)](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [Microservices Patterns](https://microservices.io/patterns/)
- [REST API Design](https://restfulapi.net/)
- [GraphQL Best Practices](https://graphql.org/learn/best-practices/)

---

**Created:** 2026-01-19  
**Version:** 2.0 (Consolidated)  
**Replaces:** architecture, api-patterns, microservices-communication, graphql-patterns  
**Structure:** Parent skill with pattern sub-files
