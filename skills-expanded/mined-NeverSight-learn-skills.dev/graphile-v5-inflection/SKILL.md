---
name: graphile-v5-inflection
description: Customize GraphQL naming and inflection in PostGraphile v5. Use when asked to "customize naming", "change field names", "simplify relation names", "remove schema prefix", "fix pluralization", or when GraphQL names don't match your conventions.
compatibility: PostGraphile v5+, graphile-config
metadata:
  author: constructive-io
  version: "1.0.0"
---

# PostGraphile v5 Inflection

Customize how PostgreSQL names become GraphQL names using inflectors.

## Official Documentation

- Inflection Guide: https://postgraphile.org/postgraphile/next/inflection

## When to Apply

Use this skill when:
- GraphQL field names don't match your naming conventions
- You want to simplify relation names (e.g., `userByAuthorId` -> `author`)
- You want to remove schema prefixes from type names
- You need custom pluralization rules
- You want to shorten mutation names

## Understanding Inflectors

Inflectors are functions that transform names. PostGraphile v5 uses them to convert PostgreSQL names (snake_case) to GraphQL names (camelCase).

Key inflectors:
- `_attributeName` - Column names
- `_schemaPrefix` - Schema prefix for type names
- `singleRelation` - Forward relation names (e.g., `post.author`)
- `_manyRelation` - Backward relation names (e.g., `user.posts`)
- `rowByUnique` - Query field names (e.g., `user`, `userByEmail`)
- `updateByKeysField` - Update mutation names
- `deleteByKeysField` - Delete mutation names

## Creating an Inflector Plugin

```typescript
import type { GraphileConfig } from 'graphile-config';

export const MyInflectorPlugin: GraphileConfig.Plugin = {
  name: 'MyInflectorPlugin',
  version: '1.0.0',

  inflection: {
    replace: {
      // Override existing inflectors here
      myInflector(previous, options, details) {
        // Call previous to get default behavior
        const defaultResult = previous!(details);
        // Modify and return
        return defaultResult;
      },
    },
  },
};
```

## Common Customizations

### Remove Schema Prefix from All Schemas

By default, PostGraphile only removes the prefix for the first schema. Override to remove for all:

```typescript
inflection: {
  replace: {
    _schemaPrefix(_previous, _options, _details) {
      return '';  // No prefix for any schema
    },
  },
},
```

**Source**: https://github.com/graphile/crystal/blob/924b2515c6bd30e5905ac1419a25244b40c8bb4d/graphile-build/graphile-build-pg/src/plugins/PgTablesPlugin.ts#L261-L271

### Keep `id` Columns as `id`

Prevent renaming `id` to `rowId`:

```typescript
inflection: {
  replace: {
    _attributeName(_previous, _options, details) {
      const attribute = details.codec.attributes[details.attributeName];
      const name = attribute?.extensions?.tags?.name || details.attributeName;
      return this.coerceToGraphQLName(name);
    },
  },
},
```

**Source**: https://github.com/graphile/crystal/blob/924b2515c6bd30e5905ac1419a25244b40c8bb4d/graphile-build/graphile-build-pg/src/plugins/PgAttributesPlugin.ts#L289-L298

### Simplify Relation Names

Transform `userByAuthorId` to `author`:

```typescript
inflection: {
  replace: {
    singleRelation(previous, _options, details) {
      const { registry, codec, relationName } = details;
      const relation = registry.pgRelations[codec.name]?.[relationName];
      
      // Check for smart tag override
      if (typeof relation.extensions?.tags?.fieldName === 'string') {
        return relation.extensions.tags.fieldName;
      }

      // Extract base name from attribute (e.g., author_id -> author)
      if (relation.localAttributes.length === 1) {
        const attributeName = relation.localAttributes[0];
        const match = attributeName.match(/^(.+?)(_id|_uuid|Id|Uuid)$/);
        if (match) {
          return this.camelCase(match[1]);
        }
      }

      return previous!(details);
    },
  },
},
```

### Simplify Root Query Names

Transform `allUsers` to `users`:

```typescript
inflection: {
  replace: {
    allRowsConnection(_previous, _options, resource) {
      const resourceName = this._singularizedResourceName(resource);
      return this.camelCase(this.pluralize(resourceName));
    },
  },
},
```

### Shorten Primary Key Lookups

Transform `userById` to `user`:

```typescript
inflection: {
  replace: {
    rowByUnique(previous, _options, details) {
      const { unique, resource } = details;
      
      // Check for smart tag override
      if (typeof unique.extensions?.tags?.fieldName === 'string') {
        return unique.extensions?.tags?.fieldName;
      }
      
      // Shorten primary key lookups
      if (unique.isPrimary) {
        return this.camelCase(this._singularizedCodecName(resource.codec));
      }
      
      return previous!(details);
    },
  },
},
```

### Shorten Mutation Names

Transform `updateUserById` to `updateUser`:

```typescript
inflection: {
  replace: {
    updateByKeysField(previous, _options, details) {
      const { resource, unique } = details;
      if (unique.isPrimary) {
        return this.camelCase(`update_${this._singularizedCodecName(resource.codec)}`);
      }
      return previous!(details);
    },

    deleteByKeysField(previous, _options, details) {
      const { resource, unique } = details;
      if (unique.isPrimary) {
        return this.camelCase(`delete_${this._singularizedCodecName(resource.codec)}`);
      }
      return previous!(details);
    },
  },
},
```

## Complete Custom Inflector Plugin

```typescript
import type { GraphileConfig } from 'graphile-config';

export const CustomInflectorPlugin: GraphileConfig.Plugin = {
  name: 'CustomInflectorPlugin',
  version: '1.0.0',

  inflection: {
    replace: {
      // Remove schema prefix from all schemas
      _schemaPrefix(_previous, _options, _details) {
        return '';
      },

      // Keep id columns as id
      _attributeName(_previous, _options, details) {
        const attribute = details.codec.attributes[details.attributeName];
        const name = attribute?.extensions?.tags?.name || details.attributeName;
        return this.coerceToGraphQLName(name);
      },

      // Simplify root query names (allUsers -> users)
      allRowsConnection(_previous, _options, resource) {
        const resourceName = this._singularizedResourceName(resource);
        return this.camelCase(this.pluralize(resourceName));
      },

      // Shorten primary key lookups (userById -> user)
      rowByUnique(previous, _options, details) {
        const { unique, resource } = details;
        if (unique.isPrimary) {
          return this.camelCase(this._singularizedCodecName(resource.codec));
        }
        return previous!(details);
      },

      // Shorten update mutations (updateUserById -> updateUser)
      updateByKeysField(previous, _options, details) {
        const { resource, unique } = details;
        if (unique.isPrimary) {
          return this.camelCase(`update_${this._singularizedCodecName(resource.codec)}`);
        }
        return previous!(details);
      },

      // Shorten delete mutations (deleteUserById -> deleteUser)
      deleteByKeysField(previous, _options, details) {
        const { resource, unique } = details;
        if (unique.isPrimary) {
          return this.camelCase(`delete_${this._singularizedCodecName(resource.codec)}`);
        }
        return previous!(details);
      },
    },
  },
};

export const CustomInflectorPreset: GraphileConfig.Preset = {
  plugins: [CustomInflectorPlugin],
};
```

## Using Smart Tags for Per-Table Overrides

Instead of global inflector changes, use smart tags for specific tables:

```sql
-- Rename a table's GraphQL type
COMMENT ON TABLE users IS E'@name Person';

-- Rename a column
COMMENT ON COLUMN users.email_address IS E'@name email';

-- Rename a relation field
COMMENT ON CONSTRAINT posts_author_id_fkey ON posts IS E'@fieldName author';
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Inflector not called | Check plugin is in preset's `plugins` array |
| `previous` is undefined | Use `previous!()` with non-null assertion |
| Type errors | Ensure proper typing for `details` parameter |
| Changes not visible | Schema is built once; restart server |

## References

- PostGraphile v5 Inflection Docs: https://postgraphile.org/postgraphile/next/inflection
- See `graphile-v5-debugging` skill for logging inflector calls and `graphile inflection list` CLI command
- See `graphile-v5-presets` skill for combining inflector plugins
