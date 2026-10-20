---
applyTo: "**/*.repository.ts"
---

# Models and Entities Instructions

## Overview
Models represent your application's data structure and business entities. This project uses TypeORM for database interactions with PostgreSQL, following Domain-Driven Design principles for business logic encapsulation.

**CRITICAL REQUIREMENTS**:
- **ALL entities are tested through REST API integration tests** (not unit tests)
- Use UUID v4 for all primary keys
- Follow factory pattern for entity creation
- Register all repositories in container
- Generate migrations for all schema changes

## Entity Structure

### Basic Entity Pattern
```typescript
import { Column, Entity, PrimaryGeneratedColumn, CreateDateColumn, UpdateDateColumn } from "typeorm";

export interface UserProps {
  id: string;
  firstName: string;
  lastName: string;
  email: string;
  createdAt?: Date;
  updatedAt?: Date;
}

@Entity({
  name: "user",
})
export class UserEntity {
  public static create(data: Partial<UserProps>): UserEntity {
    const entity = new UserEntity();
    Object.assign(entity, data);
    return entity;
  }

  @PrimaryGeneratedColumn("uuid")
  id: string;

  @Column({ name: "first_name" })
  firstName: string;

  @Column({ name: "last_name" })
  lastName: string;

  @Column({ unique: true })
  email: string;

  @CreateDateColumn({ name: "created_at" })
  createdAt: Date;

  @UpdateDateColumn({ name: "updated_at" })
  updatedAt: Date;
}
```

### Entity Guidelines
- All entities must have `.entity.ts` suffix
- Use `@PrimaryGeneratedColumn("uuid")` for primary keys
- Include `CreatedDateColumn` and `UpdateDateColumn` for audit trails
- Use snake_case for database column names with `name` property
- Define TypeScript interface for entity properties
- Implement static `create()` factory method

## Advanced Entity Patterns

### Entity with Business Logic
For entities that need business rules and validation:

```typescript
import { Column, Entity, PrimaryGeneratedColumn } from "typeorm";

export interface UserProps {
  id: string;
  firstName: string;
  lastName: string;
  email: string;
  status: UserStatus;
}

export enum UserStatus {
  ACTIVE = 'active',
  INACTIVE = 'inactive',
  SUSPENDED = 'suspended'
}

@Entity({ name: "user" })
export class UserEntity {
  public static create(data: Partial<UserProps>): UserEntity {
    const entity = new UserEntity();
    Object.assign(entity, data);
    
    // Business rule: new users are active by default
    if (!entity.status) {
      entity.status = UserStatus.ACTIVE;
    }
    
    // Validate business rules
    entity.validateBusinessRules();
    
    return entity;
  }

  @PrimaryGeneratedColumn("uuid")
  id: string;

  @Column({ name: "first_name" })
  firstName: string;

  @Column({ name: "last_name" })
  lastName: string;

  @Column({ unique: true })
  email: string;

  @Column({
    type: "enum",
    enum: UserStatus,
    default: UserStatus.ACTIVE
  })
  status: UserStatus;

  // Business methods
  public getFullName(): string {
    return `${this.firstName} ${this.lastName}`;
  }

  public isActive(): boolean {
    return this.status === UserStatus.ACTIVE;
  }

  public suspend(): void {
    if (this.status === UserStatus.SUSPENDED) {
      throw new Error("User is already suspended");
    }
    this.status = UserStatus.SUSPENDED;
  }

  public activate(): void {
    this.status = UserStatus.ACTIVE;
  }

  // Private validation
  private validateBusinessRules(): void {
    if (!this.email || !this.email.includes('@')) {
      throw new Error("Valid email is required");
    }
    
    if (!this.firstName?.trim() || !this.lastName?.trim()) {
      throw new Error("First name and last name are required");
    }
  }
}
```

### Entity Relationships
```typescript
import { Entity, Column, OneToMany, ManyToOne, JoinColumn } from "typeorm";

@Entity({ name: "order" })
export class OrderEntity {
  @PrimaryGeneratedColumn("uuid")
  id: string;

  @Column({ name: "user_id" })
  userId: string;

  @ManyToOne(() => UserEntity)
  @JoinColumn({ name: "user_id" })
  user: UserEntity;

  @OneToMany(() => OrderItemEntity, orderItem => orderItem.order)
  items: OrderItemEntity[];

  @Column({ name: "total_amount", type: "decimal", precision: 10, scale: 2 })
  totalAmount: number;
}

@Entity({ name: "order_item" })  
export class OrderItemEntity {
  @PrimaryGeneratedColumn("uuid")
  id: string;

  @Column({ name: "order_id" })
  orderId: string;

  @ManyToOne(() => OrderEntity, order => order.items)
  @JoinColumn({ name: "order_id" })
  order: OrderEntity;

  @Column()
  quantity: number;

## Repository Registration

### Container Registration
Always register repositories in `src/container/database.ts`:

```typescript
import { AwilixContainer, asValue } from "awilix";
import { dataSource } from "../config/db";
import { UserEntity } from "../app/features/users/models/user.entity";
import { OrderEntity } from "../app/features/orders/models/order.entity";

export async function registerDatabase(container: AwilixContainer) {
  await dataSource.initialize();
  
  // Run migrations automatically
  try {
    await dataSource.runMigrations();
  } catch (err) {
    container.cradle.logger.debug(`Migrations error: ${err}`);
    throw err;
  }

  // Register repositories
  container.register({
    dbDataSource: asValue(dataSource),
    
    // Entity repositories
    userRepository: asValue(dataSource.getRepository(UserEntity)),
    orderRepository: asValue(dataSource.getRepository(OrderEntity)),
    // Add new repositories here
  });
}
```

### Repository Usage Pattern
Use repositories in handlers for data access:

```typescript
export interface CreateUserHandlerDependencies {
  userRepository: Repository<UserEntity>;
  logger: Logger;
}

export default class CreateUserHandler implements CommandHandler<CreateUserCommand> {
  constructor(private dependencies: CreateUserHandlerDependencies) {}

  async execute(command: CreateUserCommand) {
    // Use entity factory method
    const userEntity = UserEntity.create({
      firstName: command.payload.firstName,
      lastName: command.payload.lastName,
      email: command.payload.email,
    });

    // Save using repository
    const savedUser = await this.dependencies.userRepository.save(userEntity);
    
    return { result: savedUser };
  }
}
```

## Repository Operations

### Query Optimization
Optimize database queries in query handlers:

```typescript
  // Select only needed fields
  await this.userRepository
    .createQueryBuilder('user')
    .select(['user.id', 'user.name', 'user.email'])
    .leftJoinAndSelect('user.profile', 'profile')
    .where('user.id = :id', { id })
    .getOne();
}
```

### Advanced Repository Patterns

#### Bulk Operations
```typescript
// Bulk insert
await this.userRepository
  .createQueryBuilder()
  .insert()
  .into(UserEntity)
  .values(userArray)
  .execute();

// Bulk update
await this.userRepository
  .createQueryBuilder()
  .update(UserEntity)
  .set({ status: UserStatus.INACTIVE })
  .where("lastLoginAt < :date", { date: inactiveDate })
  .execute();
```

#### Complex Queries
```typescript
// Query with multiple conditions and joins
const users = await this.userRepository
  .createQueryBuilder('user')
  .leftJoinAndSelect('user.orders', 'order')
  .leftJoinAndSelect('order.items', 'item')
  .where('user.status = :status', { status: UserStatus.ACTIVE })
  .andWhere('order.createdAt > :date', { date: lastMonth })
  .orderBy('user.createdAt', 'DESC')
  .take(10)
  .getMany();
```

#### Transactions
```typescript
// Using transactions for multi-table operations
await this.userRepository.manager.transaction(async manager => {
  const user = await manager.save(UserEntity, userData);
  const profile = await manager.save(ProfileEntity, { ...profileData, userId: user.id });
  await manager.save(AuditEntity, { action: 'USER_CREATED', userId: user.id });
});
```

## Database Migrations

### Migration Generation
Always generate migrations using the npm script:

```bash
# Generate migration after entity changes
npm run generate-migration

# This will auto-generate migration name based on changes
# Never add parameters to this command
```

### Migration Best Practices
- **Always generate migrations** after entity changes
- **Never create migrations manually** - use the auto-generation
- **Never add parameters** to `npm run generate-migration`
- Migrations are **auto-executed** at application start
- Review generated migrations before committing

### Example Migration Structure
```typescript
// Auto-generated migration example
import { MigrationInterface, QueryRunner } from "typeorm";

export class AddUserEntity1710240086737 implements MigrationInterface {
  name = "AddUserEntity1710240086737";

  public async up(queryRunner: QueryRunner): Promise<void> {
    await queryRunner.query(
      `CREATE TABLE "user" (
        "id" uuid NOT NULL DEFAULT uuid_generate_v4(), 
        "first_name" character varying NOT NULL, 
        "last_name" character varying NOT NULL, 
        "email" character varying NOT NULL,
        "created_at" TIMESTAMP NOT NULL DEFAULT now(),
        "updated_at" TIMESTAMP NOT NULL DEFAULT now(),
        CONSTRAINT "UQ_user_email" UNIQUE ("email"),
        CONSTRAINT "PK_user_id" PRIMARY KEY ("id")
      )`
    );
  }

  public async down(queryRunner: QueryRunner): Promise<void> {
    await queryRunner.query(`DROP TABLE "user"`);
  }
}
```

## Data Security

### SQL Injection Prevention
- **Use repository methods** instead of raw queries
- **Leverage TypeORM's query builder** for complex queries
- **Validate all input** in entity factory methods
- **Use parameterized queries** when raw SQL is necessary

```typescript
// Safe: Using repository methods
const users = await userRepository.findBy({ status: UserStatus.ACTIVE });

// Safe: Using query builder
const users = await userRepository
  .createQueryBuilder("user")
  .where("user.status = :status", { status: UserStatus.ACTIVE })
  .getMany();
```

## Testing Strategy

### Integration Testing
Entities are tested through REST API integration tests:

```typescript
describe("POST /api/users", () => {
  it("should create user with valid data", async () => {
    // This tests UserEntity.create() indirectly
    const userData = {
      firstName: "John",
      lastName: "Doe", 
      email: "john.doe@example.com"
    };

    const response = await request(app)
      .post("/api/users")
      .send(userData)
      .expect(201);

    expect(response.body.id).to.be.a('string');
    expect(response.body.email).to.equal(userData.email.toLowerCase());
  });

  it("should reject invalid email", async () => {
    const userData = {
      firstName: "John",
      lastName: "Doe",
      email: "invalid-email"
    };

    await request(app)
      .post("/api/users")
      .send(userData)
      .expect(400);
  });
});
```

### Why No Unit Tests for Entities
- Business logic is tested through realistic API scenarios
- Database interactions are tested with actual database
- Entity validation is verified through integration tests
- Factory methods are tested indirectly through handlers

## Best Practices

### Entity Design
- **Single Responsibility**: Each entity represents one business concept
- **Encapsulation**: Use private methods for internal business rules
- **Immutability**: Prefer creating new instances over modifying existing ones
- **Validation**: Validate business rules in factory methods and business methods
- **Naming**: Use descriptive names that reflect business domain

### Database Design
- **Use UUIDs**: Always use UUID v4 for primary keys
- **Audit Trails**: Include `created_at` and `updated_at` timestamps
- **Constraints**: Use database constraints for data integrity
- **Indexes**: Add indexes for frequently queried columns
- **Snake Case**: Use snake_case for database column names

### Performance Considerations
- **Lazy Loading**: Use lazy loading for related entities when appropriate
- **Query Optimization**: Use `select` to limit returned columns
- **Batch Operations**: Use batch operations for bulk data changes
- **Connection Pooling**: Leverage TypeORM's connection pooling

### Command Integration
Use entity props interfaces in commands for type safety:

```typescript
// Command using entity props interface
export interface CreateUserCommandPayload extends Partial<UserProps> {
  firstName: string;
  lastName: string;
  email: string;
}

export class CreateUserCommand implements Command<CreateUserCommandPayload> {
  constructor(public payload: CreateUserCommandPayload) {}
}
```

This ensures consistency between your commands and entities while maintaining type safety throughout the application.
