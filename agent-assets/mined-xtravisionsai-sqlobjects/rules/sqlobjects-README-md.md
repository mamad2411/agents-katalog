# SQLObjects Development Rules

Comprehensive development rules and guidelines for the SQLObjects project, organized in hierarchical structure from general development practices to specific implementation details.

## Rules Structure

### Layer 1: Universal Development Standards

- **[00-development-workflow.md](00-development-workflow.md)** - Design-first development methodology
- **[01-development-standards.md](01-development-standards.md)** - Technical standards and tools

### Layer 2: SQLObjects Architecture Principles

- **[02-architecture-principles.md](02-architecture-principles.md)** - Foundation technology and design priorities
- **[03-session-management-rules.md](03-session-management-rules.md)** - Session and transaction architecture

### Layer 3: SQLObjects Core Implementation

- **[04-model-system-rules.md](04-model-system-rules.md)** - Model definition and field system
- **[05-query-operation-rules.md](05-query-operation-rules.md)** - Query building and CRUD operations
- **[06-relationship-performance-rules.md](06-relationship-performance-rules.md)** - Relationships and performance optimization

### Layer 4: SQLObjects Extensions and Integration

- **[07-signal-extension-rules.md](07-signal-extension-rules.md)** - Signal system and extension architecture
- **[08-testing-principles-rules.md](08-testing-principles-rules.md)** - Testing philosophy and behavior verification
- **[09-documentation-consistency-rules.md](09-documentation-consistency-rules.md)** - Documentation accuracy and maintenance

## Rules Accuracy Status

**Last Synchronized**: 2024 (matches current codebase)

**Verification**: All rules reflect actual implementation without fictional features

## Implementation Status

- **✅ Fully Implemented**: Expression syntax, bulk operations, signals, relationships, UPSERT, cascade operations, prefetch_related advanced configuration
- **🚧 Planned Features**: Window functions (v2.0), database health checks (v2.0), advanced cache management (v2.1)
- **❌ Not Planned**: File validators, complex monitoring (use external tools)

## Key Principles

### Design-First Development
All code changes must begin with text-based design analysis focusing on "why" and "what" before "how".

### Documentation-Code Consistency
All documentation must match actual implementation 100% with no fictional features.

### Backward Compatibility
Public APIs remain stable across minor versions with 2-version deprecation cycle for breaking changes.

### Performance Priority
Built on SQLAlchemy Core for maximum performance with bulk operations and database-specific optimizations.

### Type Safety and Developer Experience
Comprehensive type annotations, clear error messages, and intuitive APIs with minimal boilerplate.

## Using These Rules

### For New Contributors
1. Start with **00-development-workflow.md** to understand the process
2. Read **01-development-standards.md** for technical requirements
3. Review **02-architecture-principles.md** for design philosophy
4. Study relevant implementation rules for your area of work

### For Feature Development
1. **Design Phase**: Follow workflow rules for design-first approach
2. **Architecture**: Ensure alignment with architectural principles
3. **Implementation**: Follow implementation rules for your area
4. **Testing**: Apply testing principles for behavior verification

### For Bug Fixes
1. **Analysis**: Use workflow rules for problem reproduction and analysis
2. **Solution**: Design fix following relevant implementation rules
3. **Testing**: Apply testing standards and validation requirements
4. **Documentation**: Update rules if bug reveals missing guidance

## Integration with Documentation

- **Rules** (this directory): Architectural principles and design guidelines
- **Developer Guide**: Implementation details and best practices
- **Testing Principles**: Testing philosophy and patterns
- **Design Docs**: How SQLObjects works internally
- **Feature Docs**: How to use SQLObjects functionality
