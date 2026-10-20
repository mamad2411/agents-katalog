# SQLObjects Architecture Principles

## Core Design Philosophy

### Foundation Technology Stack

- **Built on SQLAlchemy Core** (not ORM) for maximum performance and control
- **Django-style API** for familiar and intuitive developer experience
- **Async-first design** with comprehensive async/await support
- **Type safety** with full type annotations and runtime validation

### Design Priorities

1. **Performance First**: Optimize for database operations and memory usage
2. **Developer Experience**: Intuitive APIs with minimal boilerplate
3. **Type Safety**: Comprehensive type checking and validation
4. **Scalability**: Support for high-concurrency and large datasets

## Module Architecture and Responsibilities

### Core Module Boundaries

#### `model.py` - Model Foundation

- **ObjectModel base class**: Core model functionality with metaclass
- **ModelMixin**: Complete functionality integration through mixin chain
- **Metadata processing**: Table generation and schema management via ModelProcessor
- **CRUD operations**: save(), delete(), refresh() with signal integration

#### `fields/` - Type System

- **core.py**: Column descriptor, ColumnAttribute, field parameter processing
- **types/**: Type creation and SQLAlchemy type mapping
- **shortcuts.py**: Convenience functions for common field types
- **proxies.py**: DeferredObject, RelatedObject, RelatedCollection
- **relations/**: Relationship field definitions and descriptors

#### `queryset.py` - Query Interface

- **QuerySet class**: Chainable query building and execution interface
- **Q object**: Logical combination expressions for complex conditions
- **Method categories**: Query building, expression creation, execution
- **Expression integration**: Returns composable expression objects

#### `queries/` - Query Engine Components

- **builder.py**: QueryBuilder implementation with immutable query building
- **executor.py**: QueryExecutor implementation for unified query execution
- **dialect.py**: Database dialect-specific functionality

#### `objects/` - Objects Manager

- **core.py**: ObjectsManager and ObjectsDescriptor implementation
- **bulk.py**: Bulk operations (bulk_create, bulk_update, bulk_delete)
- **upsert.py**: UPSERT operation handling for different databases

#### `expressions/` - Composable Expressions

- **base.py**: Base expression classes and interfaces
- **terminal.py**: Terminal expressions (AllExpression, FirstExpression, etc.)
- **aggregate.py**: Aggregation expressions
- **subquery.py**: Subquery expressions for use in other queries
- **function.py**: Function expressions for database functions

#### `database/` - Connection Management

- **manager.py**: DatabaseManager singleton for multi-database management
- **config.py**: Database configuration and connection pool settings

#### `session.py` - Session Management

- **Session factories**: Context managers and session creation
- **Transaction control**: Commit/rollback and isolation levels
- **Multi-database support**: Named database routing

#### `contrib/` - Web Framework Integration

- **asgi.py**: `SessionMiddleware` — ASGI middleware for request-scoped session management
- **fastapi.py**: `get_db_session` — FastAPI dependency yielding a transactional session

### Cross-Module Integration Patterns

#### Unified Type System

- **TypeRegistry**: Central type mapping with LRU caching
- **Parameter extraction**: Automatic SQLAlchemy parameter conversion
- **Type validation**: Runtime type checking and coercion

#### Session Management Integration

- **using() method pattern**: Consistent session binding across all operations
- **ModelProxy pattern**: Transparent session attachment for detached instances
- **Context propagation**: Automatic session inheritance in async contexts

## Architecture Evolution Principles

### Backward Compatibility

- **API Stability**: Public interfaces remain stable across minor versions
- **Deprecation Process**: 2-version deprecation cycle with clear migration paths
- **Migration Tools**: Automated tools for major version upgrades

### Extension Strategy

- **Plugin Architecture**: New functionality through mixins and extensions
- **Hook Points**: Well-defined extension points for customization
- **Composition over Inheritance**: Favor mixins over deep inheritance hierarchies
- **Interface Segregation**: Small, focused interfaces over monolithic ones

## Key Design Decisions and Rationale

### SQLAlchemy Core vs ORM

**Decision**: Use SQLAlchemy Core as foundation
**Rationale**:

- Better performance for bulk operations
- More control over SQL generation
- Simpler async integration
- Reduced memory overhead

### Django-style API Design

**Decision**: Adopt Django ORM-like interface
**Rationale**:

- Familiar to many Python developers
- Proven patterns for common operations
- Intuitive query building and chaining
- Clear separation of concerns

### Async-First Architecture

**Decision**: Design all APIs as async-first
**Rationale**:

- Modern Python applications are increasingly async
- Better resource utilization for I/O-bound operations
- Consistent programming model
- Future-proof architecture

### Multi-Database Compatibility Strategy

**Implementation**: Database dialect detection with function mapping

**Approach**:

- Detect database dialect using `session.bind.dialect.name`
- Map to database-specific functions (PostgreSQL: `date_trunc()`, SQLite: `strftime()`, MySQL: `date_format()`)
- Provide `extract()` function fallback for unsupported databases
- Ensure consistent Python object types across databases

**Example Implementation**:
```python
# In QuerySet.execute_dates()
dialect_name = self._executor.session.bind.dialect.name

if dialect_name == "postgresql":
    date_expr = func.date_trunc("year", field_col)
elif dialect_name == "sqlite":
    date_expr = func.strftime("%Y-01-01", field_col)
elif dialect_name == "mysql":
    date_expr = func.date_format(field_col, "%Y-01-01")
else:
    # Fallback using extract
    date_expr = func.extract("year", field_col)
```

**Benefits**:

- Optimal performance using database-native functions
- Consistent Python API across all databases
- Graceful fallback for unsupported databases
- Type safety with unified return types

### Type Safety Implementation

**Decision**: Comprehensive type annotations with runtime validation
**Rationale**:

- Better IDE support and developer experience
- Catch errors at development time
- Self-documenting code
- Integration with modern Python tooling

## Current Version Feature Boundaries

### Implemented Features ✅

- **Expression Syntax**: Full support for User.field and string syntax
- **Basic Cache Control**: no_cache() and basic statistics
- **Bulk Operations**: bulk_create, bulk_update, bulk_delete with batch processing
- **Signal System**: Complete lifecycle hooks with automatic registration
- **Relationship Loading**: select_related and prefetch_related with expression syntax
- **Field System**: Complete type registry with Auto type inference
- **Validation System**: Field-level and model-level validation with custom validators
- **Window Functions**: ROW_NUMBER, RANK, DENSE_RANK, LAG, LEAD, FIRST_VALUE, LAST_VALUE, NTILE, PERCENT_RANK, NTH_VALUE via `func.xxx().over()`
- **CTE Support**: Common Table Expressions via `.cte()` and `.with_cte()`, including recursive CTEs
- **EXPLAIN Support**: Query plan analysis via `.explain(analyze=True, output="json")`

### Planned Features (TODO.md) 🚧

- **Advanced Cache Management**: Detailed statistics and management (v2.1)
- **Database Health Checks**: check_db_health(), switch_default_db() (v2.0)
- **Advanced SQL Functions**: Complex query patterns (v2.1+)

### Not Planned ❌

- **File Validators**: FileValidator, ImageValidator (use external libraries)
- **Complex Monitoring**: Built-in performance monitoring (use external tools)

## Architecture Constraints and Guidelines

### Module Dependencies

- **Circular Dependencies**: Strictly prohibited between core modules
- **Import Hierarchy**: Clear dependency tree with base → fields → queries → database
- **External Dependencies**: Minimize and carefully evaluate all external dependencies
- **Optional Dependencies**: Use optional imports for non-core functionality

### Interface Design

- **Consistency**: Similar operations have similar interfaces across modules
- **Discoverability**: Common operations easily discoverable through IDE completion
- **Flexibility**: Support both simple and advanced use cases
- **Error Handling**: Consistent error types and messages across all modules

### Performance Constraints

- **Memory Efficiency**: Minimize object creation and memory allocation
- **Query Optimization**: Generate efficient SQL for all operations
- **Caching Strategy**: Intelligent caching without memory leaks
- **Bulk Operations**: Always provide high-performance bulk alternatives
- **Database Optimization**: Use database-specific functions for optimal performance
- **Type Conversion**: Minimize overhead in cross-database type conversion
- **Fallback Performance**: Ensure fallback implementations remain performant

