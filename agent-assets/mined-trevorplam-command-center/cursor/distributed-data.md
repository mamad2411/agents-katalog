---
description: Run Distributed Data Management and Polyglot Persistence Standards Check
globs: ["**/database/**/*.ts", "**/persistence/**/*.ts", "**/data-access/**/*.ts"]
---
# Data: Distributed Data Management & Polyglot Persistence Standards

<audit_rules>
- You MUST implement proper database-per-service pattern with separate databases for each service.
- You MUST ensure appropriate database types based on data access patterns (SQL vs NoSQL).
- You MUST implement proper data consistency patterns (eventual consistency for distributed data).
- You MUST configure proper connection pooling and database resource management.
- You MUST implement proper database migration strategies for distributed databases.
- You MUST ensure no direct cross-service database access (use APIs or events).
- You MUST implement proper data synchronization and conflict resolution strategies.
- You MUST configure proper database backup and disaster recovery procedures.
- You MUST implement proper database monitoring and performance optimization.
- You MUST ensure proper data privacy and compliance in distributed data stores.
</audit_rules>

<example_good>
```typescript
// Database-per-service pattern implementation
import { Pool } from 'pg';
import { MongoClient } from 'mongodb';
import { Redis } from 'ioredis';

// Service-specific database configurations
export class DatabaseManager {
  private sqlPool: Pool;
  private mongoClient: MongoClient;
  private redisClient: Redis;

  constructor() {
    // PostgreSQL for relational data
    this.sqlPool = new Pool({
      host: process.env.POSTGRES_HOST,
      port: parseInt(process.env.POSTGRES_PORT || '5432'),
      database: process.env.POSTGRES_DB,
      user: process.env.POSTGRES_USER,
      password: process.env.POSTGRES_PASSWORD,
      max: 20, // Connection pool size
      idleTimeoutMillis: 30000,
      connectionTimeoutMillis: 2000,
    });

    // MongoDB for document data
    this.mongoClient = new MongoClient(process.env.MONGODB_URI);
    
    // Redis for caching and session data
    this.redisClient = new Redis({
      host: process.env.REDIS_HOST,
      port: parseInt(process.env.REDIS_PORT || '6379'),
      retryDelayOnFailover: 100,
      maxRetriesPerRequest: 3,
    });
  }

  // Repository pattern for SQL database
  getSqlRepository<T>(entityName: string): SqlRepository<T> {
    return new SqlRepository<T>(this.sqlPool, entityName);
  }

  // Repository pattern for MongoDB
  getMongoRepository<T>(collectionName: string): MongoRepository<T> {
    return new MongoRepository<T>(this.mongoClient, collectionName);
  }

  // Cache repository
  getCacheRepository(): CacheRepository {
    return new CacheRepository(this.redisClient);
  }

  async close(): Promise<void> {
    await this.sqlPool.end();
    await this.mongoClient.close();
    await this.redisClient.quit();
  }
}

// SQL Repository with connection pooling
export class SqlRepository<T> {
  constructor(
    private pool: Pool,
    private tableName: string
  ) {}

  async findById(id: string): Promise<T | null> {
    const query = `SELECT * FROM ${this.tableName} WHERE id = $1`;
    const result = await this.pool.query(query, [id]);
    return result.rows[0] || null;
  }

  async create(data: Partial<T>): Promise<T> {
    const fields = Object.keys(data).join(', ');
    const values = Object.values(data);
    const placeholders = values.map((_, i) => `$${i + 1}`).join(', ');
    
    const query = `
      INSERT INTO ${this.tableName} (${fields}) 
      VALUES (${placeholders}) 
      RETURNING *
    `;
    
    const result = await this.pool.query(query, values);
    return result.rows[0];
  }

  async update(id: string, data: Partial<T>): Promise<T | null> {
    const updates = Object.entries(data)
      .map(([key, _], i) => `${key} = $${i + 2}`)
      .join(', ');
    
    const values = [id, ...Object.values(data)];
    const query = `
      UPDATE ${this.tableName} 
      SET ${updates}, updated_at = NOW() 
      WHERE id = $1 
      RETURNING *
    `;
    
    const result = await this.pool.query(query, values);
    return result.rows[0] || null;
  }

  async delete(id: string): Promise<boolean> {
    const query = `DELETE FROM ${this.tableName} WHERE id = $1`;
    const result = await this.pool.query(query, [id]);
    return result.rowCount > 0;
  }
}

// MongoDB Repository
export class MongoRepository<T> {
  private db: any;
  private collection: any;

  constructor(
    private client: MongoClient,
    private collectionName: string
  ) {}

  private async getCollection() {
    if (!this.db) {
      this.db = this.client.db();
    }
    if (!this.collection) {
      this.collection = this.db.collection(this.collectionName);
    }
    return this.collection;
  }

  async findById(id: string): Promise<T | null> {
    const collection = await this.getCollection();
    return await collection.findOne({ _id: id });
  }

  async create(data: Partial<T>): Promise<T> {
    const collection = await this.getCollection();
    const result = await collection.insertOne({
      ...data,
      _id: generateId(),
      createdAt: new Date(),
      updatedAt: new Date(),
    });
    return await collection.findOne({ _id: result.insertedId });
  }

  async update(id: string, data: Partial<T>): Promise<T | null> {
    const collection = await this.getCollection();
    await collection.updateOne(
      { _id: id },
      { 
        $set: { 
          ...data, 
          updatedAt: new Date() 
        } 
      }
    );
    return await collection.findOne({ _id: id });
  }

  async delete(id: string): Promise<boolean> {
    const collection = await this.getCollection();
    const result = await collection.deleteOne({ _id: id });
    return result.deletedCount > 0;
  }
}

// Cache Repository
export class CacheRepository {
  constructor(private redis: Redis) {}

  async get(key: string): Promise<string | null> {
    return await this.redis.get(key);
  }

  async set(key: string, value: string, ttl?: number): Promise<void> {
    if (ttl) {
      await this.redis.setex(key, ttl, value);
    } else {
      await this.redis.set(key, value);
    }
  }

  async del(key: string): Promise<void> {
    await this.redis.del(key);
  }

  async exists(key: string): Promise<boolean> {
    const result = await this.redis.exists(key);
    return result === 1;
  }
}

// Eventual consistency through events
export class EventualConsistencyManager {
  constructor(
    private eventBus: EventBus,
    private localDb: DatabaseManager,
    private remoteServices: Map<string, RemoteServiceClient>
  ) {}

  async publishDataChangeEvent(event: DataChangeEvent): Promise<void> {
    // Publish event for eventual consistency
    await this.eventBus.publish('DataChanged', {
      aggregateType: event.aggregateType,
      aggregateId: event.aggregateId,
      changes: event.changes,
      timestamp: new Date(),
      version: event.version,
    });

    // Trigger synchronization with dependent services
    await this.triggerSynchronization(event);
  }

  private async triggerSynchronization(event: DataChangeEvent): Promise<void> {
    const dependentServices = this.getDependentServices(event.aggregateType);
    
    for (const serviceName of dependentServices) {
      const service = this.remoteServices.get(serviceName);
      if (service) {
        // Fire-and-forget synchronization
        service.synchronizeData(event).catch(error => {
          console.error(`Failed to sync with ${serviceName}:`, error);
        });
      }
    }
  }

  private getDependentServices(aggregateType: string): string[] {
    // Define service dependencies
    const dependencies = {
      'user': ['notification-service', 'analytics-service'],
      'order': ['inventory-service', 'payment-service', 'notification-service'],
      'product': ['inventory-service', 'search-service'],
    };
    
    return dependencies[aggregateType] || [];
  }
}
```
</example_good>

<example_bad>
```typescript
// BAD: Shared database across services
export class SharedDatabaseService {
  constructor(private db: Database) {}

  // BAD: Single database for all services
  async createUser(userData: any): Promise<User> {
    return await this.db.user.create(userData);
  }

  async createOrder(orderData: any): Promise<Order> {
    // BAD: Order service accessing same database
    return await this.db.order.create(orderData);
  }

  async createProduct(productData: any): Promise<Product> {
    // BAD: Product service accessing same database
    return await this.db.product.create(productData);
  }

  // BAD: Direct cross-service data access
  async getUserOrders(userId: string): Promise<any> {
    // BAD: Direct access to order data from user service
    const user = await this.db.user.findUnique({ where: { id: userId } });
    const orders = await this.db.order.findMany({ where: { userId } });
    return { user, orders };
  }
}

// BAD: No connection pooling
export class BadDatabaseService {
  constructor() {
    // BAD: Creating new connection for each query
    this.connection = new Connection(process.env.DATABASE_URL);
  }

  async query(sql: string, params?: any[]): Promise<any> {
    // BAD: No connection pooling
    return await this.connection.query(sql, params);
  }

  // BAD: No proper resource management
  async close(): Promise<void> {
    await this.connection.close();
  }
}
```
</example_bad>
