---
name: graphile-v5-debugging
description: Debug PostGraphile v5 schema generation issues. Use when asked to "debug schema", "why is this field generated", "log inflector calls", "detect naming conflicts", "understand schema generation", or when troubleshooting PostGraphile v5 issues.
compatibility: PostGraphile v5+, graphile-config
metadata:
  author: constructive-io
  version: "1.0.0"
---

# PostGraphile v5 Debugging

Debug schema generation issues and understand how PostGraphile v5 builds your GraphQL schema.

## Official Documentation

- Debugging Guide: https://postgraphile.org/postgraphile/next/debugging
- Configuration: https://postgraphile.org/postgraphile/next/config

## When to Apply

Use this skill when:
- You don't understand why a field is named a certain way
- You want to see what inflectors are being called
- You need to detect naming conflicts between schemas
- You're troubleshooting unexpected schema behavior
- You want to understand the build process

## Graphile CLI Commands

PostGraphile v5 includes a `graphile` CLI toolbelt for debugging. These commands help you understand your configuration and schema generation.

### Available Commands

| Command | Purpose |
|---------|---------|
| `npx graphile config print` | Outputs resolved preset configuration |
| `npx graphile config print plugins` | Displays enabled plugins |
| `npx graphile behavior debug` | Debugs behavior configurations |
| `npx graphile inflection list` | Lists all available inflectors with documentation |

### graphile config print

Shows your resolved configuration after all presets merge:

```bash
npx graphile config print
npx graphile config print plugins  # Show enabled plugins
```

Use this when:
- Debugging configuration issues
- Verifying which plugins are loaded
- Checking configuration option values

### graphile behavior debug

Debug behavior configurations with scope options:

```bash
npx graphile behavior debug
```

Supports scope options like `pgResource`, `pgResourceUnique`, and `pgCodec` to narrow down behavior debugging.

### graphile inflection list

Lists all available inflectors with their arguments, documentation, and TypeScript definitions:

```bash
npx graphile inflection list
```

Use this when:
- Debugging naming/inflection issues
- Finding available inflector functions to override
- Understanding how database names become GraphQL names

## DEBUG Environment Variables

Enable detailed logging with DEBUG environment variables:

```bash
# Schema construction warnings (often includes fixes)
DEBUG="graphile-build:warn" npx postgraphile ...

# Hook execution order
DEBUG="graphile-build:SchemaBuilder" npx postgraphile ...

# SQL query details
DEBUG="@dataplan/pg:PgExecutor" npx postgraphile ...

# SQL queries with EXPLAIN output
DEBUG="@dataplan/pg:PgExecutor:explain" npx postgraphile ...
```

### Useful DEBUG Variables

| Variable | Purpose |
|----------|---------|
| `graphile-build:warn` | Recoverable errors during schema construction |
| `graphile-build:SchemaBuilder` | Hook execution order and nesting |
| `@dataplan/pg:PgExecutor` | SQL query details, inputs, and results |
| `@dataplan/pg:PgExecutor:explain` | SQL queries with EXPLAIN output |

## Ruru Explain Tab

Enable the Explain tab in Ruru (the GraphQL IDE) to see query execution plans:

```typescript
const preset: GraphileConfig.Preset = {
  grafast: {
    explain: true,  // Enable in development only
  },
};
```

**Warning**: Disable in production for security.

## Understanding Schema Generation

PostGraphile v5 builds the schema once at startup:

1. **Introspection** - Reads database structure
2. **Plugin Processing** - Plugins modify the build
3. **Inflection** - Names are transformed
4. **Type Generation** - GraphQL types are created
5. **Field Generation** - Fields are added to types
6. **Schema Finalization** - Final schema is cached

**Important**: The schema is built ONCE and cached. Changes require server restart.

## Inflector Logger Plugin

Log all inflector calls to understand naming:

```typescript
import type { GraphileConfig } from 'graphile-config';

const LOG_ENABLED = process.env.INFLECTOR_LOG === '1';

function log(category: string, message: string, details?: Record<string, unknown>) {
  if (!LOG_ENABLED) return;
  const detailsStr = details ? ` ${JSON.stringify(details)}` : '';
  console.log(`[Inflector:${category}]${detailsStr} => ${message}`);
}

export const InflectorLoggerPlugin: GraphileConfig.Plugin = {
  name: 'InflectorLoggerPlugin',
  version: '1.0.0',

  inflection: {
    replace: {
      // Log query field names
      rowByUnique(previous, _options, details) {
        const result = previous!(details);
        const { unique, resource } = details;
        log('rowByUnique', result, {
          resource: resource.name,
          uniqueAttributes: unique.attributes,
          isPrimary: unique.isPrimary,
        });
        return result;
      },

      // Log forward relation names (post.author)
      singleRelation(previous, _options, details) {
        const result = previous!(details);
        const { codec, relationName, registry } = details;
        const relation = registry.pgRelations[codec.name]?.[relationName];
        log('singleRelation', result, {
          fromType: codec.name,
          relationName,
          toType: relation?.remoteResource?.name,
          localAttributes: relation?.localAttributes,
        });
        return result;
      },

      // Log backward relation names (user.posts)
      _manyRelation(previous, _options, details) {
        const result = previous!(details);
        const { codec, relationName, registry } = details;
        const relation = registry.pgRelations[codec.name]?.[relationName];
        log('manyRelation', result, {
          fromType: codec.name,
          relationName,
          toType: relation?.remoteResource?.name,
        });
        return result;
      },

      // Log root connection fields (Query.users)
      allRowsConnection(previous, _options, resource) {
        const result = previous!(resource);
        log('allRowsConnection', result, { resource: resource.name });
        return result;
      },

      // Log table type names
      tableType(previous, _options, codec) {
        const result = previous!(codec);
        log('tableType', result, { codec: codec.name });
        return result;
      },

      // Log attribute names
      attribute(previous, _options, details) {
        const result = previous!(details);
        const { attributeName, codec } = details;
        log('attribute', result, { codec: codec.name, attributeName });
        return result;
      },

      // Log update mutation names
      updateByKeysField(previous, _options, details) {
        const result = previous!(details);
        const { resource, unique } = details;
        log('updateByKeysField', result, {
          resource: resource.name,
          isPrimary: unique.isPrimary,
        });
        return result;
      },

      // Log delete mutation names
      deleteByKeysField(previous, _options, details) {
        const result = previous!(details);
        const { resource, unique } = details;
        log('deleteByKeysField', result, {
          resource: resource.name,
          isPrimary: unique.isPrimary,
        });
        return result;
      },
    },
  },
};

export const InflectorLoggerPreset: GraphileConfig.Preset = {
  plugins: [InflectorLoggerPlugin],
};
```

### Usage

```bash
INFLECTOR_LOG=1 pnpm dev
```

### Sample Output

```
[Inflector:tableType] {"codec":"users"} => User
[Inflector:rowByUnique] {"resource":"users","uniqueAttributes":["id"],"isPrimary":true} => user
[Inflector:rowByUnique] {"resource":"users","uniqueAttributes":["email"],"isPrimary":false} => userByEmail
[Inflector:allRowsConnection] {"resource":"users"} => users
[Inflector:singleRelation] {"fromType":"posts","relationName":"author","toType":"users"} => author
[Inflector:manyRelation] {"fromType":"users","relationName":"posts","toType":"posts"} => posts
```

## Conflict Detector Plugin

Detect naming conflicts between tables in different schemas:

```typescript
import type { GraphileConfig } from 'graphile-config';

interface CodecInfo {
  name: string;
  schemaName: string;
  tableName: string;
}

export const ConflictDetectorPlugin: GraphileConfig.Plugin = {
  name: 'ConflictDetectorPlugin',
  version: '1.0.0',

  schema: {
    hooks: {
      build(build) {
        const codecsByName = new Map<string, CodecInfo[]>();

        for (const codec of Object.values(build.input.pgRegistry.pgCodecs)) {
          if (!codec.attributes || codec.isAnonymous) continue;

          const pgExtensions = codec.extensions?.pg as { schemaName?: string } | undefined;
          const schemaName = pgExtensions?.schemaName || 'unknown';
          const graphqlName = build.inflection.tableType(codec);

          const info: CodecInfo = {
            name: graphqlName,
            schemaName,
            tableName: codec.name,
          };

          if (!codecsByName.has(graphqlName)) {
            codecsByName.set(graphqlName, []);
          }
          codecsByName.get(graphqlName)!.push(info);
        }

        for (const [graphqlName, codecs] of codecsByName) {
          if (codecs.length > 1) {
            const locations = codecs.map(c => `${c.schemaName}.${c.tableName}`).join(', ');
            console.warn(
              `\nNAMING CONFLICT: GraphQL type "${graphqlName}" from multiple tables:\n` +
              `   Tables: ${locations}\n` +
              `   Resolution options:\n` +
              `   1. Add @name smart tag: COMMENT ON TABLE schema.table IS E'@name UniqueTypeName';\n` +
              `   2. Rename one of the tables\n` +
              `   3. Exclude one table with @omit smart tag\n`
            );
          }
        }

        return build;
      },
    },
  },
};

export const ConflictDetectorPreset: GraphileConfig.Preset = {
  plugins: [ConflictDetectorPlugin],
};
```

## Debugging Techniques

### 1. Print Schema to File

```typescript
import { printSchema } from 'graphql';
import fs from 'fs';

// After building schema
const schema = pgl.getSchema();
fs.writeFileSync('schema.graphql', printSchema(schema));
```

### 2. Log Build Information

```typescript
schema: {
  hooks: {
    build(build) {
      console.log('Available schemas:', build.options.pgSchemas);
      console.log('Number of codecs:', Object.keys(build.input.pgRegistry.pgCodecs).length);
      console.log('Number of resources:', Object.keys(build.input.pgRegistry.pgResources).length);
      return build;
    },
  },
},
```

### 3. Inspect a Specific Table

```typescript
schema: {
  hooks: {
    build(build) {
      const { pgRegistry } = build.input;
      
      // Find a specific table
      const usersCodec = Object.values(pgRegistry.pgCodecs).find(
        c => c.name === 'users'
      );
      
      if (usersCodec) {
        console.log('Users codec:', {
          name: usersCodec.name,
          attributes: Object.keys(usersCodec.attributes || {}),
          extensions: usersCodec.extensions,
        });
      }
      
      return build;
    },
  },
},
```

### 4. Log All Generated Fields

```typescript
schema: {
  hooks: {
    GraphQLObjectType_fields(fields, build, context) {
      const { Self } = context;
      console.log(`Fields for ${Self.name}:`, Object.keys(fields));
      return fields;
    },
  },
},
```

### 5. Check Behavior Resolution

```typescript
schema: {
  entityBehavior: {
    pgResourceUnique: {
      override: {
        provides: ['debugBehavior'],
        callback(behavior, [resource, unique]) {
          console.log(`Behavior for ${resource.name}.${unique.attributes.join(',')}:`, behavior);
          return behavior;
        },
      },
    },
  },
},
```

## Common Issues and Solutions

### Field Not Generated

1. Check if table is in the schemas array
2. Check for `@omit` smart tags
3. Check behavior settings
4. Use InflectorLoggerPlugin to see if inflector is called

### Wrong Field Name

1. Use InflectorLoggerPlugin to see what inflector produces
2. Check for `@name` smart tags
3. Check custom inflector overrides
4. Verify inflector plugin order in preset

### Naming Conflict

1. Use ConflictDetectorPlugin to identify conflicts
2. Add `@name` smart tags to disambiguate
3. Check `_schemaPrefix` inflector behavior

### Mutation Missing

1. Check table has primary key
2. Check for `@omit create,update,delete` smart tags
3. Check behavior settings for `-insert`, `-update`, `-delete`
4. Verify table is not a view

### Filter Not Available

1. Check if column is indexed (default behavior)
2. Use EnableAllFilterColumnsPlugin
3. Check for `-filterBy` behavior on column
4. Verify connection filter plugin is installed

## Complete Debug Preset

```typescript
import type { GraphileConfig } from 'graphile-config';

export const DebugPreset: GraphileConfig.Preset = {
  plugins: [
    InflectorLoggerPlugin,
    ConflictDetectorPlugin,
  ],
};

// Usage
const preset: GraphileConfig.Preset = {
  extends: [
    MyAppPreset,
    DebugPreset,  // Add for debugging
  ],
};
```

Run with:

```bash
INFLECTOR_LOG=1 pnpm dev
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| No log output | Check `INFLECTOR_LOG=1` is set |
| Logs appear once | Schema is cached; restart to see again |
| Can't find inflector | Check PostGraphile source for inflector name |
| Hook not called | Verify plugin is in preset's `plugins` array |

## Source Code References

- PgAttributesPlugin: https://github.com/graphile/crystal/blob/main/graphile-build/graphile-build-pg/src/plugins/PgAttributesPlugin.ts
- PgTablesPlugin: https://github.com/graphile/crystal/blob/main/graphile-build/graphile-build-pg/src/plugins/PgTablesPlugin.ts
- PgRelationsPlugin: https://github.com/graphile/crystal/blob/main/graphile-build/graphile-build-pg/src/plugins/PgRelationsPlugin.ts

## References

- PostGraphile v5 Debugging Docs: https://postgraphile.org/postgraphile/next/debugging
- PostGraphile v5 Configuration Docs: https://postgraphile.org/postgraphile/next/config
- See `graphile-v5-inflection` skill for customizing inflectors
- See `graphile-v5-plugins` skill for creating custom plugins
- See `graphile-v5-behaviors` skill for understanding behaviors
