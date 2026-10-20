---
description: Run Event-Driven Architecture and CQRS Standards Check
globs: ['**/events/**/*.ts', '**/commands/**/*.ts', '**/queries/**/*.ts', '**/messaging/**/*.ts']
---

# Architecture: Event-Driven Architecture & CQRS Standards

<audit_rules>

- You MUST implement proper event sourcing with immutable event logs for aggregate changes.
- You MUST separate command and query responsibilities using CQRS pattern.
- You MUST ensure events are immutable and contain all necessary data for replay.
- You MUST implement proper event versioning and schema evolution strategies.
- You MUST configure message brokers with proper durability and ordering guarantees.
- You MUST implement idempotent event handlers to prevent duplicate processing.
- You MUST ensure eventual consistency between command and query models.
- You MUST implement proper event replay and snapshot strategies for performance.
- You MUST configure dead letter queues for failed message processing.
- You MUST implement proper correlation IDs and causation tracking for event chains.
  </audit_rules>

<example_good>

```typescript
// Event Sourcing with CQRS
import { z } from 'zod'
import { EventStore } from '@/lib/event-store'
import { MessageBroker } from '@/lib/message-broker'

// Events
const UserEvents = {
  UserCreated: z.object({
    userId: z.string(),
    email: z.string(),
    name: z.string(),
    timestamp: z.date(),
  }),
  UserUpdated: z.object({
    userId: z.string(),
    changes: z.object({
      name: z.string().optional(),
      email: z.string().optional(),
    }),
    timestamp: z.date(),
  }),
  UserDeleted: z.object({
    userId: z.string(),
    timestamp: z.date(),
  }),
} as const

// Command Handler
export class UserCommandHandler {
  constructor(
    private eventStore: EventStore,
    private messageBroker: MessageBroker
  ) {}

  async CreateUser(command: CreateUserCommand): Promise<void> {
    const event = {
      type: 'UserCreated',
      data: {
        userId: generateId(),
        email: command.email,
        name: command.name,
        timestamp: new Date(),
      },
    }

    await this.eventStore.appendEvent('user', event.data.userId, event)
    await this.messageBroker.publish('user.events', event)
  }

  async UpdateUser(command: UpdateUserCommand): Promise<void> {
    const events = await this.eventStore.getEvents('user', command.userId)
    const user = this.rebuildUserFromEvents(events)

    const event = {
      type: 'UserUpdated',
      data: {
        userId: command.userId,
        changes: command.changes,
        timestamp: new Date(),
      },
    }

    await this.eventStore.appendEvent('user', command.userId, event)
    await this.messageBroker.publish('user.events', event)
  }
}

// Query Handler (Read Model)
export class UserQueryHandler {
  constructor(private readModelDb: Database) {}

  async GetUser(query: GetUserQuery): Promise<UserView | null> {
    return await this.readModelDb.userView.findUnique({
      where: { id: query.userId },
    })
  }

  async SearchUsers(query: SearchUsersQuery): Promise<UserView[]> {
    return await this.readModelDb.userView.findMany({
      where: {
        name: { contains: query.searchTerm },
      },
    })
  }
}

// Event Handler (Projection)
export class UserProjectionHandler {
  constructor(private readModelDb: Database) {}

  async handleUserCreated(event: UserEvent): Promise<void> {
    await this.readModelDb.userView.create({
      data: {
        id: event.data.userId,
        email: event.data.email,
        name: event.data.name,
        version: 1,
      },
    })
  }

  async handleUserUpdated(event: UserEvent): Promise<void> {
    await this.readModelDb.userView.update({
      where: { id: event.data.userId },
      data: {
        ...event.data.changes,
        version: { increment: 1 },
      },
    })
  }
}
```

</example_good>

<example_bad>

```typescript
// BAD: No event sourcing, direct database mutations
export class UserService {
  async createUser(userData: any) {
    // BAD: Direct mutation without events
    return await db.user.create(userData)
  }

  async updateUser(userId: string, changes: any) {
    // BAD: No event log, no audit trail
    return await db.user.update({
      where: { id: userId },
      data: changes,
    })
  }

  // BAD: No CQRS separation
  async getUserWithOrders(userId: string) {
    const user = await db.user.findUnique({ where: { id: userId } })
    const orders = await db.order.findMany({ where: { userId } })
    return { user, orders }
  }
}
```

</example_bad>
