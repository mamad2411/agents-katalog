---
name: graphile-v5-behaviors
description: Control PostGraphile v5 schema generation with the behavior system. Use when asked to "disable mutations", "hide fields", "control what gets generated", "disable unique lookups", "make features opt-in", or when you need fine-grained control over the GraphQL schema.
compatibility: PostGraphile v5+, graphile-config
metadata:
  author: constructive-io
  version: "1.0.0"
---

# PostGraphile v5 Behaviors

Control what gets generated in your GraphQL schema using the behavior system.

## Official Documentation

- Behavior System: https://postgraphile.org/postgraphile/next/behavior

## When to Apply

Use this skill when:
- You want to disable certain queries or mutations
- You need to hide specific fields or types
- You want to make features opt-in instead of opt-out
- You need to control unique constraint lookups
- You want to enable/disable filtering on specific columns

## Understanding Behaviors

Behaviors are strings that control what gets generated. They can be:
- **Positive**: `single`, `update`, `delete`, `filterBy`, `manyToMany`
- **Negative**: `-single`, `-update`, `-delete`, `-filterBy`, `-manyToMany`

Behaviors are processed in phases:
1. **inferred** - Default behaviors based on database structure
2. **override** - Final say on what's enabled/disabled

## Common Behaviors

| Behavior | Controls |
|----------|----------|
| `single` | Single-row query lookups (e.g., `user(id)`) |
| `update` | Update mutations |
| `delete` | Delete mutations |
| `insert` | Insert mutations |
| `filterBy` | Column appears in filter arguments |
| `orderBy` | Column appears in orderBy arguments |
| `manyToMany` | Many-to-many relation fields |
| `constraint:resource:update` | Update by specific constraint |
| `constraint:resource:delete` | Delete by specific constraint |

## Using entityBehavior

### Basic Structure

```typescript
export const MyBehaviorPlugin: GraphileConfig.Plugin = {
  name: 'MyBehaviorPlugin',
  version: '1.0.0',

  schema: {
    entityBehavior: {
      // Target entity type
      pgResourceUnique: {
        // Phase: 'inferred' or 'override'
        override: {
          provides: ['myBehaviorControl'],
          callback(behavior, [resource, unique]) {
            // Return modified behavior
            return [behavior, '-single'];
          },
        },
      },
    },
  },
};
```

### Entity Types

| Entity Type | What it targets |
|-------------|-----------------|
| `pgResource` | Tables and views |
| `pgResourceUnique` | Unique constraints (including primary keys) |
| `pgCodecAttribute` | Table columns |
| `pgCodecRelation` | Foreign key relations |
| `pgManyToMany` | Many-to-many junction tables |

## Common Patterns

### Disable Non-Primary-Key Lookups

Only allow lookups by primary key, not by other unique constraints:

```typescript
export const PrimaryKeyOnlyPlugin: GraphileConfig.Plugin = {
  name: 'PrimaryKeyOnlyPlugin',
  version: '1.0.0',

  schema: {
    entityBehavior: {
      pgResourceUnique: {
        override: {
          provides: ['primaryKeyOnly'],
          callback(behavior, [_resource, unique]) {
            if (!unique.isPrimary) {
              // Disable query lookups and mutations for non-PK uniques
              return [
                behavior,
                '-single',
                '-constraint:resource:update',
                '-constraint:resource:delete',
              ];
            }
            return behavior;
          },
        },
      },
    },
  },
};
```

### Disable All Unique Lookups (Use Filters Instead)

Force users to use collection queries with filters:

```typescript
export const NoUniqueLookupPlugin: GraphileConfig.Plugin = {
  name: 'NoUniqueLookupPlugin',
  version: '1.0.0',

  schema: {
    entityBehavior: {
      pgResourceUnique: {
        override: {
          provides: ['noUniqueLookups'],
          callback(behavior, [_resource, unique]) {
            if (unique.isPrimary) {
              // Keep mutations but disable query lookups
              return [behavior, '-single'];
            }
            // Disable everything for non-PK uniques
            return [
              behavior,
              '-single',
              '-constraint:resource:update',
              '-constraint:resource:delete',
            ];
          },
        },
      },
    },
  },
};
```

### Make Many-to-Many Opt-In

By default, disable many-to-many fields; require explicit opt-in:

```typescript
export const ManyToManyOptInPlugin: GraphileConfig.Plugin = {
  name: 'ManyToManyOptInPlugin',
  version: '1.0.0',

  schema: {
    entityBehavior: {
      pgManyToMany: {
        inferred: {
          provides: ['manyToManyOptIn'],
          before: ['default'],
          callback(behavior) {
            // Disable by default
            return ['-manyToMany', behavior];
          },
        },
      },
    },
  },
};
```

Then enable for specific tables with smart tags:

```sql
COMMENT ON TABLE post_tags IS E'@behavior +manyToMany';
```

### Enable Filtering on All Columns

Override the default index-based filtering restriction:

```typescript
export const EnableAllFilterColumnsPlugin: GraphileConfig.Plugin = {
  name: 'EnableAllFilterColumnsPlugin',
  version: '1.0.0',

  schema: {
    entityBehavior: {
      pgCodecAttribute: {
        inferred: {
          after: ['postInferred'],
          provides: ['enableAllFilters'],
          callback(behavior) {
            return [behavior, 'filterBy'];
          },
        },
      },
    },
  },
};
```

### Disable Filtering on Specific Columns

```typescript
export const DisableSensitiveFiltersPlugin: GraphileConfig.Plugin = {
  name: 'DisableSensitiveFiltersPlugin',
  version: '1.0.0',

  schema: {
    entityBehavior: {
      pgCodecAttribute: {
        override: {
          provides: ['disableSensitiveFilters'],
          callback(behavior, [codec, attributeName]) {
            // Disable filtering on password-like columns
            if (attributeName.includes('password') || attributeName.includes('secret')) {
              return [behavior, '-filterBy'];
            }
            return behavior;
          },
        },
      },
    },
  },
};
```

## Inferred vs Override Phase

### Inferred Phase

- Runs early in behavior processing
- Good for setting defaults
- Can be overridden by smart tags and later phases

```typescript
inferred: {
  provides: ['myDefault'],
  before: ['default'],  // Run before default behaviors
  callback(behavior) {
    return ['-manyToMany', behavior];  // Disabled by default
  },
},
```

### Override Phase

- Runs after all other processing
- Has the final say
- Use for hard requirements that can't be overridden

```typescript
override: {
  provides: ['myOverride'],
  callback(behavior, entity) {
    // This WILL be applied regardless of smart tags
    return [behavior, '-single'];
  },
},
```

## Using Smart Tags

Smart tags provide per-entity behavior control without plugins:

```sql
-- Disable all mutations on a table
COMMENT ON TABLE audit_logs IS E'@behavior -insert -update -delete';

-- Enable many-to-many on a junction table
COMMENT ON TABLE post_tags IS E'@behavior +manyToMany';

-- Disable filtering on a column
COMMENT ON COLUMN users.internal_id IS E'@behavior -filterBy';

-- Disable a specific unique lookup
COMMENT ON CONSTRAINT users_email_key ON users IS E'@behavior -single';
```

## Complete Example: Primary Key Only Preset

```typescript
import type { GraphileConfig } from 'graphile-config';

export interface UniqueLookupOptions {
  disableAllUniqueLookups?: boolean;
}

export function createUniqueLookupPlugin(
  options: UniqueLookupOptions = {}
): GraphileConfig.Plugin {
  const { disableAllUniqueLookups = false } = options;

  return {
    name: 'UniqueLookupPlugin',
    version: '1.0.0',

    schema: {
      entityBehavior: {
        pgResourceUnique: {
          override: {
            provides: ['uniqueLookupControl'],
            callback(behavior, [_resource, unique]) {
              if (disableAllUniqueLookups) {
                if (unique.isPrimary) {
                  return [behavior, '-single'];
                }
                return [
                  behavior,
                  '-single',
                  '-constraint:resource:update',
                  '-constraint:resource:delete',
                ];
              }
              
              if (!unique.isPrimary) {
                return [
                  behavior,
                  '-single',
                  '-constraint:resource:update',
                  '-constraint:resource:delete',
                ];
              }
              return behavior;
            },
          },
        },
      },
    },
  };
}

export const PrimaryKeyOnlyPlugin = createUniqueLookupPlugin({ disableAllUniqueLookups: false });
export const NoUniqueLookupPlugin = createUniqueLookupPlugin({ disableAllUniqueLookups: true });

export const PrimaryKeyOnlyPreset: GraphileConfig.Preset = {
  plugins: [PrimaryKeyOnlyPlugin],
};

export const NoUniqueLookupPreset: GraphileConfig.Preset = {
  plugins: [NoUniqueLookupPlugin],
};
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Behavior not applied | Check phase (inferred vs override) |
| Smart tag overrides plugin | Use `override` phase instead of `inferred` |
| Can't find entity type | Check PostGraphile source for correct entity name |
| Behavior string format | Use array format: `[behavior, '-single']` |

## Source Code References

- PgRowByUniquePlugin (query lookups): https://github.com/graphile/crystal/blob/924b2515c6bd30e5905ac1419a25244b40c8bb4d/graphile-build/graphile-build-pg/src/plugins/PgRowByUniquePlugin.ts
- PgMutationUpdateDeletePlugin (mutations): https://github.com/graphile/crystal/blob/924b2515c6bd30e5905ac1419a25244b40c8bb4d/graphile-build/graphile-build-pg/src/plugins/PgMutationUpdateDeletePlugin.ts
- PgIndexBehaviorsPlugin (filtering): https://github.com/graphile/crystal/blob/924b2515c6bd30e5905ac1419a25244b40c8bb4d/graphile-build/graphile-build-pg/src/plugins/PgIndexBehaviorsPlugin.ts

## References

- PostGraphile v5 Behavior Docs: https://postgraphile.org/postgraphile/next/behavior
- See `graphile-v5-presets` skill for combining behavior plugins
- See `graphile-v5-connection-filter` skill for filter configuration
- See `graphile-v5-debugging` skill for `graphile behavior debug` CLI command
