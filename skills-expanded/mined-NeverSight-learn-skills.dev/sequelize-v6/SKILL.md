---
name: sequelize-v6
description: Guía completa de Sequelize v6 para Node.js con ejemplos de JavaScript y TypeScript. Usa esta skill cuando el usuario necesite crear modelos, hacer queries, configurar asociaciones, migraciones, o cualquier tarea relacionada con Sequelize v6. Incluye data types con compatibilidad por DB, decorators de sequelize-typescript, y patrones comunes.
---

# Sequelize v6 - Quick Reference & Common Patterns

Guía práctica de Sequelize v6 con ejemplos comunes y patrones de uso.

## 📚 Navegación Rápida

| Tema | Archivo |
|------|---------|
| Primeros Pasos | [`docs/1-primeros-pasos.md`](docs/1-primeros-pasos.md) |
| Models | [`docs/2-models.md`](docs/2-models.md) |
| Querying | [`docs/3-querying.md`](docs/3-querying.md) |
| Associations | [`docs/4-associations.md`](docs/4-associations.md) |
| Migración v5→v6 | [`docs/5-migracion-v5-a-v6.md`](docs/5-migracion-v5-a-v6.md) |
| Migrations | [`docs/6-migrations.md`](docs/6-migrations.md) |

---

## 🔥 Patrones Comunes

### 1. Configuración Básica

```javascript
const { Sequelize } = require('sequelize');

const sequelize = new Sequelize('database', 'username', 'password', {
  host: 'localhost',
  dialect: 'mysql',
  logging: console.log,
});

// Probar conexión
await sequelize.authenticate();
```

[Documentación oficial - Getting Started](https://sequelize.org/docs/v6/getting-started)

### 2. Model Definition (JavaScript)

```javascript
const { Model, DataTypes } = require('sequelize');

class User extends Model {}

User.init({
  id: {
    type: DataTypes.INTEGER,
    primaryKey: true,
    autoIncrement: true
  },
  username: {
    type: DataTypes.STRING,
    allowNull: false,
    unique: true
  },
  email: {
    type: DataTypes.STRING,
    allowNull: false,
    validate: {
      isEmail: true
    }
  }
}, {
  sequelize,
  modelName: 'User',
  tableName: 'users',
  timestamps: true
});
```

[Documentación oficial - Model Definition](https://sequelize.org/docs/v6/core-concepts/model-definition/)

### 3. Model Definition (TypeScript con Decorators)

```typescript
import { Table, Column, Model, DataType } from 'sequelize-typescript';

@Table({ tableName: 'users' })
class User extends Model<User> {
  @Column({ primaryKey: true, autoIncrement: true })
  declare id: number;

  @Column({ allowNull: false })
  declare username: string;

  @Column({ allowNull: false })
  declare email: string;
}
```

[Documentación oficial - TypeScript](https://sequelize.org/docs/v6/other-topics/typescript/)
[sequelize-typescript README](https://github.com/sequelize/sequelize-typescript)

### 4. CRUD Operations

```javascript
// CREATE
const user = await User.create({ username: 'john', email: 'john@example.com' });

// READ - Find by PK
const user = await User.findByPk(1);

// READ - Find one
const user = await User.findOne({ where: { email: 'john@example.com' } });

// READ - Find all
const users = await User.findAll();

// UPDATE
await user.update({ username: 'john_doe' });
await User.update({ status: 'active' }, { where: { id: 1 } });

// DELETE
await user.destroy();
await User.destroy({ where: { id: 1 } });
```

[Documentación oficial - Model Querying](https://sequelize.org/docs/v6/core-concepts/model-querying-basics/)

### 5. WHERE Clauses con Operators

```javascript
const { Op } = require('sequelize');

const users = await User.findAll({
  where: {
    // Equals
    status: 'active',
    [Op.eq]: 'active',
    
    // Not equals
    status: { [Op.ne]: 'inactive' },
    
    // In
    status: { [Op.in]: ['active', 'pending'] },
    status: [Op.in]: ['active', 'pending'],
    
    // Like
    username: { [Op.like]: 'john%' },
    
    // Between
    age: { [Op.between]: [18, 65] },
    
    // Or
    [Op.or]: [
      { status: 'active' },
      { role: 'admin' }
    ],
    
    // And
    [Op.and]: [
      { status: 'active' },
      { age: { [Op.gte]: 18 } }
    ]
  }
});
```

[Documentación oficial - Operators](https://sequelize.org/docs/v6/core-concepts/model-querying/#operators)

### 6. Associations

```javascript
// HasOne
User.hasOne(Profile);
Profile.belongsTo(User);

// HasMany
User.hasMany(Post);
Post.belongsTo(User);

// BelongsToMany
User.belongsToMany(Project, { through: 'UserProjects' });
Project.belongsToMany(User, { through: 'UserProjects' });

// Eager Loading
const user = await User.findOne({
  where: { id: 1 },
  include: [Post, Profile]
});
```

[Documentación oficial - Associations](https://sequelize.org/docs/v6/core-concepts/assocs/)

### 7. Hooks

```javascript
User.addHook('beforeValidate', (user) => {
  user.email = user.email.toLowerCase();
});

User.addHook('beforeCreate', async (user) => {
  user.passwordHash = await hash(user.password);
});

User.addHook('afterCreate', (user) => {
  console.log('User created:', user.username);
});
```

[Documentación oficial - Hooks](https://sequelize.org/docs/v6/other-topics/hooks/)

### 8. Scopes

```javascript
// Default Scope
User.addScope('active', {
  where: { status: 'active' }
});

// Custom Scope
User.addScope('withPosts', {
  include: [Post]
});

// Apply Scope
const activeUsers = await User.scope('active').findAll();
const activeUsersWithPosts = await User.scope(['active', 'withPosts']).findAll();
```

[Documentación oficial - Scopes](https://sequelize.org/docs/v6/other-topics/scopes/)

### 9. Transactions

```javascript
const t = await sequelize.transaction();

try {
  const user = await User.create({ username: 'john' }, { transaction: t });
  const profile = await Profile.create({ userId: user.id }, { transaction: t });
  
  await t.commit();
} catch (error) {
  await t.rollback();
  throw error;
}
```

[Documentación oficial - Transactions](https://sequelize.org/docs/v6/other-topics/transactions/)

### 10. Raw Queries

```javascript
const { QueryTypes } = require('sequelize');

// SELECT
const results = await sequelize.query(
  'SELECT * FROM users WHERE status = :status',
  { 
    replacements: { status: 'active' },
    type: QueryTypes.SELECT,
    model: User,
    mapToModel: true
  }
);

// Raw results
const raw = await sequelize.query('SELECT * FROM users', { 
  raw: true,
  type: QueryTypes.SELECT
});
```

[Documentación oficial - Raw Queries](https://sequelize.org/docs/v6/core-concepts/raw-queries/)

---

## 📊 Data Types Quick Reference

Ver [`docs/2-models.md`](docs/2-models.md) para detalles completos con compatibilidad por DB.

| Type | JavaScript | PostgreSQL | MySQL | SQLite | SQL Server | Oracle |
|------|-----------|------------|-------|--------|------------|--------|
| STRING | `STRING` | ✅ | ✅ | ✅ | ✅ | ✅ |
| TEXT | `TEXT` | ✅ | ✅ | ✅ | ✅ | ✅ |
| INTEGER | `INTEGER` | ✅ | ✅ | ✅ | ✅ | ✅ |
| BIGINT | `BIGINT` | ✅ | ✅ | ✅ | ✅ | ✅ |
| FLOAT | `FLOAT` | ✅ | ✅ | ✅ | ✅ | ✅ |
| DOUBLE | `DOUBLE` | ✅ | ✅ | ✅ | ❌ | ❌ | |
| DECIMAL | `DECIMAL` | ✅ | ✅ | ✅ | ✅ | ✅ |
| BOOLEAN | `BOOLEAN` | ✅ | ✅ | ✅ | ✅ | ✅ |
| DATE | `DATE` | ✅ | ✅ | ✅ | ✅ | ✅ |
| JSON | `JSON` | ✅* | ✅** | ❌ | ✅* | ✅* |
| UUID | `UUID` | ✅ | ✅** | ✅** | ✅ | ❌ |

* PostgreSQL, SQL Server, Oracle
** MySQL 5.7+

---

## 🔗 Enlaces Oficiales

- [Documentación Principal v6](https://sequelize.org/docs/v6/)
- [Getting Started](https://sequelize.org/docs/v6/getting-started/)
- [Model Definition](https://sequelize.org/docs/v6/core-concepts/model-definition/)
- [Model Querying](https://sequelize.org/docs/v6/core-concepts/model-querying-basics/)
- [Associations](https://sequelize.org/docs/v6/core-concepts/assocs/)
- [TypeScript](https://sequelize.org/docs/v6/other-topics/typescript/)
- [Hooks](https://sequelize.org/docs/v6/other-topics/hooks/)
- [Transactions](https://sequelize.org/docs/v6/other-topics/transactions/)
- [Migrations](https://sequelize.org/docs/v6/other-topics/migrations/)
- [sequelize-typescript](https://github.com/sequelize/sequelize-typescript)
