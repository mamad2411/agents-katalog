---
description: Run Distributed Data Management and Polyglot Persistence Standards Check
globs:
  ['**/repositories/**/*.ts', '**/databases/**/*.ts', '**/data/**/*.ts', 'prisma/schema.prisma']
---

# Data: Distributed Data Management & Polyglot Persistence Standards

<audit_rules>

- You MUST implement database-per-service pattern with separate databases for each microservice.
- You MUST choose appropriate database types based on data access patterns (SQL vs NoSQL).
- You MUST implement proper data consistency patterns (eventual consistency for distributed data).
- You MUST configure proper connection pooling and database resource management.
- You MUST implement proper database migration strategies for distributed databases.
- You MUST ensure no direct cross-service database access (use APIs or events).
- You MUST implement proper data synchronization and conflict resolution strategies.
- You MUST configure proper database backup and disaster recovery procedures.
- You MUST implement proper database monitoring and performance optimization.
- You MUST ensure data privacy and compliance in distributed data stores.
  </audit_rules>

<example_good>

```typescript
// Database-per-service with polyglot persistence

// User Service - PostgreSQL (Relational)
export class UserRepository {
  constructor(private db: PostgresDatabase) {}

  async create(userData: CreateUser): Promise<User> {
    const user = await this.db.user.create({
      data: {
        id: generateId(),
        email: userData.email,
        name: userData.name,
        createdAt: new Date(),
        updatedAt: new Date(),
      },
    })

    // Publish event for other services
    await this.eventPublisher.publish('UserCreated', {
      userId: user.id,
      email: user.email,
      name: user.name,
    })

    return user
  }

  async findById(id: string): Promise<User | null> {
    return await this.db.user.findUnique({
      where: { id },
    })
  }
}

// Order Service - MongoDB (Document)
export class OrderRepository {
  constructor(private db: MongoDatabase) {}

  async createOrder(orderData: CreateOrder): Promise<Order> {
    const order = await this.db.orders.insertOne({
      _id: generateId(),
      userId: orderData.userId,
      items: orderData.items,
      total: orderData.total,
      status: 'pending',
      createdAt: new Date(),
      updatedAt: new Date(),
    })

    // Event for analytics service
    await this.eventPublisher.publish('OrderCreated', {
      orderId: order.insertedId,
      userId: orderData.userId,
      total: orderData.total,
    })

    return order
  }
}

// Analytics Service - ClickHouse (Time-series)
export class AnalyticsRepository {
  constructor(private db: ClickHouseDatabase) {}

  async recordUserActivity(event: UserActivityEvent): Promise<void> {
    await this.db.insert('user_activities', {
      user_id: event.userId,
      action: event.action,
      timestamp: event.timestamp,
      metadata: event.metadata,
    })
  }

  async getUserActivitySummary(userId: string, period: TimePeriod): Promise<ActivitySummary> {
    const query = `
      SELECT 
        count() as total_actions,
        uniq(action) as unique_actions,
        min(timestamp) as first_action,
        max(timestamp) as last_action
      FROM user_activities 
      WHERE user_id = ? AND timestamp >= ? AND timestamp <= ?
    `

    return await this.db.query(query, [userId, period.start, period.end])
  }
}

// Cache Service - Redis (Key-value)
export class CacheRepository {
  constructor(private redis: RedisClient) {}

  async getUserSession(sessionId: string): Promise<UserSession | null> {
    const data = await this.redis.get(`session:${sessionId}`)
    return data ? JSON.parse(data) : null
  }

  async setUserSession(sessionId: string, session: UserSession, ttl: number): Promise<void> {
    await this.redis.setex(`session:${sessionId}`, ttl, JSON.stringify(session))
  }

  async invalidateUserSessions(userId: string): Promise<void> {
    const pattern = `session:*`
    const keys = await this.redis.keys(pattern)

    for (const key of keys) {
      const session = await this.redis.get(key)
      if (session) {
        const parsed = JSON.parse(session)
        if (parsed.userId === userId) {
          await this.redis.del(key)
        }
      }
    }
  }
}

// Data consistency through events
export class DataConsistencyHandler {
  constructor(
    private userRepo: UserRepository,
    private analyticsRepo: AnalyticsRepository,
    private cacheRepo: CacheRepository
  ) {}

  async handleUserCreated(event: UserCreatedEvent): Promise<void> {
    // Update analytics data
    await this.analyticsRepo.recordUserActivity({
      userId: event.userId,
      action: 'user_registered',
      timestamp: event.timestamp,
      metadata: { email: event.email, name: event.name },
    })

    // Invalidate relevant cache entries
    await this.cacheRepo.invalidateUserSessions(event.userId)
  }
}
```

</example_good>

<example_bad>

```typescript
// BAD: Shared database, no service boundaries
export class UserService {
  // BAD: Direct access to other service's data
  async getUserWithOrders(userId: string) {
    const user = await db.user.findUnique({ where: { id: userId } })

    // BAD: Direct access to orders table (belongs to order service)
    const orders = await db.order.findMany({ where: { userId } })

    return { user, orders }
  }

  // BAD: No database-per-service pattern
  async updateUserAndOrders(userId: string, userData: any, orderData: any) {
    // BAD: Cross-service transaction
    await db.user.update({ where: { id: userId }, data: userData })
    await db.order.updateMany({ where: { userId }, data: orderData })
  }
}

// BAD: No polyglot persistence, one database for everything
const db = new PrismaClient() // Single database for all services
```

</example_bad>
