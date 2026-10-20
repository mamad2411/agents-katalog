---
description: Run Microservices Architecture and Domain-Driven Design Standards Check
globs:
  ['**/services/**/*.ts', '**/microservices/**/*.ts', 'docker-compose*.yml', 'api-gateway/**/*.ts']
---

# Architecture: Microservices & Domain-Driven Design Standards

<audit_rules>

- You MUST implement proper service decomposition using Domain-Driven Design (DDD) with bounded contexts.
- You MUST ensure each microservice has a single, well-defined responsibility aligned with business capabilities.
- You MUST implement API-first design with contract-based development using OpenAPI/Swagger specifications.
- You MUST configure proper database-per-service pattern with separate databases for each service.
- You MUST implement asynchronous communication using message brokers for inter-service communication.
- You MUST ensure services are stateless and externalize state using databases or caches.
- You MUST implement proper service discovery and registration mechanisms.
- You MUST configure circuit breakers, retries, and timeouts for resilience patterns.
- You MUST implement distributed tracing and correlation IDs for request tracking.
- You MUST ensure services are independently deployable with separate CI/CD pipelines.
  </audit_rules>

<example_good>

```typescript
// Service: User Management (Bounded Context)
import { z } from 'zod'
import { EventPublisher } from '@/lib/events'
import { UserRepository } from './repositories'

const CreateUserSchema = z.object({
  email: z.string().email(),
  name: z.string().min(1).max(100),
  role: z.enum(['user', 'admin']).default('user'),
})

export class UserService {
  constructor(
    private userRepository: UserRepository,
    private eventPublisher: EventPublisher,
    private tracer: Tracer
  ) {}

  async createUser(userData: unknown): Promise<User> {
    const span = this.tracer.startSpan('user.create')

    try {
      const validated = CreateUserSchema.parse(userData)

      // Business logic within bounded context
      const existingUser = await this.userRepository.findByEmail(validated.email)
      if (existingUser) {
        throw new Error('User already exists')
      }

      const user = await this.userRepository.create(validated)

      // Domain event
      await this.eventPublisher.publish('UserCreated', {
        userId: user.id,
        email: user.email,
        timestamp: new Date(),
      })

      span.setAttributes({
        'user.id': user.id,
        'user.email': user.email,
      })

      return user
    } catch (error) {
      span.recordException(error)
      throw error
    } finally {
      span.end()
    }
  }
}

// API Contract (OpenAPI)
export const userApiSpec = {
  '/users': {
    post: {
      summary: 'Create a new user',
      requestBody: {
        content: {
          'application/json': {
            schema: CreateUserSchema,
          },
        },
      },
      responses: {
        201: {
          description: 'User created successfully',
          content: {
            'application/json': {
              schema: UserSchema,
            },
          },
        },
      },
    },
  },
}
```

</example_good>

<example_bad>

```typescript
// BAD: Monolithic service with multiple responsibilities
export class UserService {
  // BAD: Handling payments in user service
  async processPayment(userId: string, amount: number) {
    // This should be in a separate PaymentService
  }

  // BAD: Handling notifications in user service
  async sendNotification(userId: string, message: string) {
    // This should be in a separate NotificationService
  }

  // BAD: Shared database with other services
  async createUser(userData: any) {
    // Direct database access without proper abstraction
    return await db.users.create(userData)
  }

  // BAD: Synchronous communication between services
  async getUserWithOrders(userId: string) {
    const user = await this.getUser(userId)
    // BAD: Direct HTTP call to order service
    const orders = await fetch(`http://order-service/orders/${userId}`)
    return { user, orders }
  }
}
```

</example_bad>
