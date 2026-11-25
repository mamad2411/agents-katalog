---
name: database-data-modeling
description: Design databases and data models following best practices, ORM patterns, and data modeling principles. Use when designing schemas, creating models, writing migrations, or when the user asks about databases, ORM, Sequelize, data modeling, or migrations.
---

# Database & Data Modeling Best Practices

Design efficient, maintainable database schemas and data models using ORM patterns and best practices.

## Data Modeling Principles

### Normalization

**First Normal Form (1NF):**

- Each column contains atomic values
- No repeating groups

**Second Normal Form (2NF):**

- 1NF + all non-key attributes fully dependent on primary key

**Third Normal Form (3NF):**

- 2NF + no transitive dependencies

**When to Denormalize:**

- Read-heavy workloads
- Performance-critical queries
- Reporting/analytics tables

### Entity Relationships

```typescript
// One-to-Many
User.hasMany(Order, { foreignKey: "userId" });
Order.belongsTo(User, { foreignKey: "userId" });

// Many-to-Many
User.belongsToMany(Role, { through: "UserRoles" });
Role.belongsToMany(User, { through: "UserRoles" });

// One-to-One
User.hasOne(Profile, { foreignKey: "userId" });
Profile.belongsTo(User, { foreignKey: "userId" });
```

## Sequelize ORM Patterns

### Model Definition

```typescript
import { DataTypes, Model, Optional } from "sequelize";

interface UserAttributes {
  id: number;
  email: string;
  password: string;
  name: string;
  createdAt?: Date;
  updatedAt?: Date;
}

interface UserCreationAttributes extends Optional<
  UserAttributes,
  "id" | "createdAt" | "updatedAt"
> {}

class User
  extends Model<UserAttributes, UserCreationAttributes>
  implements UserAttributes
{
  public id!: number;
  public email!: string;
  public password!: string;
  public name!: string;
  public readonly createdAt!: Date;
  public readonly updatedAt!: Date;
}

User.init(
  {
    id: {
      type: DataTypes.INTEGER,
      autoIncrement: true,
      primaryKey: true,
    },
    email: {
      type: DataTypes.STRING,
      allowNull: false,
      unique: true,
      validate: {
        isEmail: true,
      },
    },
    password: {
      type: DataTypes.STRING,
      allowNull: false,
      validate: {
        len: [8, 255],
      },
    },
    name: {
      type: DataTypes.STRING,
      allowNull: false,
    },
  },
  {
    sequelize: db,
    tableName: "users",
    timestamps: true,
    underscored: true,
  },
);
```

### Repository Pattern

```typescript
class UserRepository {
  async findById(id: number): Promise<User | null> {
    return User.findByPk(id);
  }

  async findByEmail(email: string): Promise<User | null> {
    return User.findOne({ where: { email } });
  }

  async create(data: UserCreationAttributes): Promise<User> {
    return User.create(data);
  }

  async update(id: number, data: Partial<UserAttributes>): Promise<User> {
    const user = await User.findByPk(id);
    if (!user) {
      throw new NotFoundError("User", id.toString());
    }
    return user.update(data);
  }

  async delete(id: number): Promise<void> {
    const user = await User.findByPk(id);
    if (!user) {
      throw new NotFoundError("User", id.toString());
    }
    await user.destroy();
  }

  async findAll(options?: FindOptions): Promise<User[]> {
    return User.findAll(options);
  }
}
```

### Query Patterns

**Basic Queries:**

```typescript
// Find by primary key
const user = await User.findByPk(1);

// Find one with conditions
const user = await User.findOne({
  where: { email: "user@example.com" },
});

// Find all with conditions
const users = await User.findAll({
  where: { status: "active" },
  order: [["createdAt", "DESC"]],
  limit: 10,
  offset: 0,
});
```

**Eager Loading:**

```typescript
// Include associations
const user = await User.findByPk(1, {
  include: [
    { model: Order, as: "orders" },
    { model: Profile, as: "profile" },
  ],
});

// Nested includes
const user = await User.findByPk(1, {
  include: [
    {
      model: Order,
      as: "orders",
      include: [
        {
          model: OrderItem,
          as: "items",
        },
      ],
    },
  ],
});
```

**Complex Queries:**

```typescript
// Using operators
const users = await User.findAll({
  where: {
    [Op.and]: [
      { status: "active" },
      { createdAt: { [Op.gte]: new Date("2024-01-01") } },
    ],
    email: { [Op.like]: "%@example.com" },
  },
});

// Aggregations
const count = await User.count({
  where: { status: "active" },
});

const total = await Order.sum("total", {
  where: { userId: 1 },
});
```

## Transactions

### Basic Transactions

```typescript
// Manual transaction
const transaction = await sequelize.transaction();

try {
  const user = await User.create(data, { transaction });
  const order = await Order.create({ userId: user.id }, { transaction });
  await transaction.commit();
  return { user, order };
} catch (error) {
  await transaction.rollback();
  throw error;
}
```

### Transaction Helper

```typescript
async function withTransaction<T>(
  fn: (transaction: Transaction) => Promise<T>,
): Promise<T> {
  const transaction = await sequelize.transaction();
  try {
    const result = await fn(transaction);
    await transaction.commit();
    return result;
  } catch (error) {
    await transaction.rollback();
    throw error;
  }
}

// Usage
const result = await withTransaction(async (t) => {
  const user = await User.create(data, { transaction: t });
  const order = await Order.create({ userId: user.id }, { transaction: t });
  return { user, order };
});
```

## Migrations

### Migration Structure

```typescript
// migrations/20240101000000-create-users.js
module.exports = {
  up: async (queryInterface, Sequelize) => {
    await queryInterface.createTable("users", {
      id: {
        type: Sequelize.INTEGER,
        autoIncrement: true,
        primaryKey: true,
      },
      email: {
        type: Sequelize.STRING,
        allowNull: false,
        unique: true,
      },
      password: {
        type: Sequelize.STRING,
        allowNull: false,
      },
      name: {
        type: Sequelize.STRING,
        allowNull: false,
      },
      created_at: {
        type: Sequelize.DATE,
        allowNull: false,
        defaultValue: Sequelize.literal("CURRENT_TIMESTAMP"),
      },
      updated_at: {
        type: Sequelize.DATE,
        allowNull: false,
        defaultValue: Sequelize.literal("CURRENT_TIMESTAMP"),
      },
    });

    await queryInterface.addIndex("users", ["email"]);
  },

  down: async (queryInterface, Sequelize) => {
    await queryInterface.dropTable("users");
  },
};
```

### Data Migrations

```typescript
// migrations/20240102000000-add-default-roles.js
module.exports = {
  up: async (queryInterface, Sequelize) => {
    await queryInterface.bulkInsert("roles", [
      { name: "admin", created_at: new Date(), updated_at: new Date() },
      { name: "user", created_at: new Date(), updated_at: new Date() },
    ]);
  },

  down: async (queryInterface, Sequelize) => {
    await queryInterface.bulkDelete("roles", {
      name: { [Sequelize.Op.in]: ["admin", "user"] },
    });
  },
};
```

## Indexing Strategies

### When to Index

```typescript
// Index frequently queried columns
User.init(
  {
    email: {
      type: DataTypes.STRING,
      unique: true,
      // Indexed automatically for unique
    },
  },
  {
    indexes: [
      // Single column index
      { fields: ["status"] },
      // Composite index
      { fields: ["userId", "status"] },
      // Partial index
      { fields: ["email"], where: { status: "active" } },
    ],
  },
);
```

### Index Best Practices

- Index foreign keys
- Index columns used in WHERE clauses
- Index columns used in JOINs
- Index columns used in ORDER BY
- Don't over-index (slows writes)
- Use composite indexes for multi-column queries

## Query Optimization

### Avoid N+1 Queries

```typescript
// ❌ Bad - N+1 queries
const orders = await Order.findAll();
for (const order of orders) {
  const user = await User.findByPk(order.userId); // N queries
}

// ✅ Good - Eager loading
const orders = await Order.findAll({
  include: [{ model: User, as: "user" }],
});
```

### Use Select Specific Columns

```typescript
// ❌ Bad - Select all columns
const users = await User.findAll();

// ✅ Good - Select only needed columns
const users = await User.findAll({
  attributes: ["id", "email", "name"],
});
```

### Pagination

```typescript
// ✅ Good - Use limit and offset
const users = await User.findAll({
  limit: 20,
  offset: 0,
  order: [["createdAt", "DESC"]],
});

// ✅ Better - Cursor-based pagination for large datasets
const users = await User.findAll({
  where: { id: { [Op.gt]: lastId } },
  limit: 20,
  order: [["id", "ASC"]],
});
```

## Data Validation

### Model-Level Validation

```typescript
User.init({
  email: {
    type: DataTypes.STRING,
    validate: {
      isEmail: true,
      notEmpty: true,
    },
  },
  age: {
    type: DataTypes.INTEGER,
    validate: {
      min: 0,
      max: 150,
    },
  },
});
```

### Custom Validators

```typescript
User.init({
  password: {
    type: DataTypes.STRING,
    validate: {
      len: [8, 255],
      isStrongPassword(value: string) {
        if (!/(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/.test(value)) {
          throw new Error(
            "Password must contain uppercase, lowercase, and number",
          );
        }
      },
    },
  },
});
```

## Best Practices

1. **Use migrations** - Never modify schema directly
2. **Use transactions** - For multi-step operations
3. **Index appropriately** - Balance read/write performance
4. **Avoid N+1 queries** - Use eager loading
5. **Validate at model level** - Catch errors early
6. **Use repository pattern** - Abstract data access
7. **Handle errors gracefully** - Catch and transform DB errors
8. **Use connection pooling** - For production
9. **Monitor query performance** - Use query logging in development
10. **Backup regularly** - Protect your data

## When Working with Databases

1. **Design schema first** - Plan before coding
2. **Use migrations** - Version control your schema
3. **Normalize appropriately** - Balance normalization vs performance
4. **Index strategically** - Based on query patterns
5. **Use transactions** - For data consistency
6. **Validate data** - At model and application level
7. **Optimize queries** - Avoid N+1, use eager loading
8. **Handle errors** - Transform DB errors to user-friendly messages
9. **Test migrations** - Ensure up and down work
10. **Document relationships** - Clear model associations
