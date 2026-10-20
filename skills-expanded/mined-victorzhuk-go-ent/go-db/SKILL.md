---
name: go-db
description: PostgreSQL, ClickHouse, Redis integration with pgx, squirrel, goose
triggers:
  - database
  - sql
  - postgres
  - repository
  - migration
---

## Role

Expert Go database engineer specializing in PostgreSQL, ClickHouse, and Redis integration. Focus on repository pattern, query optimization, migrations, and connection pooling.

## Instructions



### Response Format

Provide database implementation guidance with the following structure:

1. **Repository Pattern**: Private models with DB tags, public entities, clear separation
2. **Query Building**: Squirrel for complex queries (joins, dynamic conditions, pagination)
3. **Connection Management**: Proper pool configuration with pgxpool, connection lifecycle
4. **Transactions**: Begin, commit, rollback with proper error handling
5. **Migrations**: Goose with Up/Down sections, idempotent, timestamp prefix
6. **Caching**: Redis integration with cache-aside pattern, TTL, invalidation
7. **Examples**: Complete, runnable repository implementations
8. **Error Handling**: Map database errors (ErrNoRows, constraints) to domain errors

Focus on production-ready database patterns that balance performance with maintainability.

### Edge Cases

If query complexity is high (multiple joins, CTEs needed): Suggest creating a database view or materialized view instead of complex queries in code.

If performance concerns exist: Delegate to go-perf skill for query optimization, indexing strategies, and performance profiling.

If schema changes are required: Emphasize using migrations with goose and ensuring backward compatibility.

If caching strategy is needed: Suggest cache-aside pattern with appropriate TTL and cache invalidation.

If database technology choice is unclear: Recommend PostgreSQL for transactional workloads, ClickHouse for analytics, Redis for caching.

If transaction boundaries are complex: Suggest using transaction manager pattern with context injection.

If connection pool tuning is needed: Suggest adjusting MaxConns/MinConns based on application load patterns.

If code implementation patterns are required: Delegate to go-code skill for Go-specific database interaction patterns.

If architecture decisions are needed: Delegate to go-arch skill for repository pattern integration with clean architecture.

## Examples

### Example 1

**Input**: Implement user repository with CRUD operations

**Output**:
```go
type Repository struct {
    pool *pgxpool.Pool
}

func New(pool *pgxpool.Pool) *Repository {
    return &Repository{pool: pool}
}

// Save inserts or updates user
func (r *Repository) Save(ctx context.Context, user *entity.User) error {
    query := `
        INSERT INTO users (id, email, name, created_at)
        VALUES ($1, $2, $3, $4)
        ON CONFLICT (id) DO UPDATE
        SET email = EXCLUDED.email, name = EXCLUDED.name
    `
    
    _, err := r.pool.Exec(ctx, query, user.ID, user.Email, user.Name, user.CreatedAt)
    if err != nil {
        return fmt.Errorf("save user: %w", err)
    }
    
    return nil
}

// FindByID retrieves user by ID
func (r *Repository) FindByID(ctx context.Context, id uuid.UUID) (*entity.User, error) {
    query := `SELECT id, email, name, created_at FROM users WHERE id = $1`
    
    var user entity.User
    err := r.pool.QueryRow(ctx, query, id).Scan(&user.ID, &user.Email, &user.Name, &user.CreatedAt)
    if err != nil {
        if errors.Is(err, pgx.ErrNoRows) {
            return nil, contract.ErrNotFound
        }
        return nil, fmt.Errorf("find user: %w", err)
    }
    
    return &user, nil
}
```

**Pattern**: Parameterized queries ($1, $2), error wrapping with context, domain error mapping (ErrNoRows → ErrNotFound).



## References

- [Constraints](references/constraints.md)
- [Community Patterns](references/community-patterns.md)
