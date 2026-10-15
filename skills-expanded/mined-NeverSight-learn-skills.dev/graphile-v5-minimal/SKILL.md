---
name: graphile-v5-minimal
description: Configure PostGraphile v5 default plugins and features. Use when asked to "configure default plugins", "customize base schema", "keep id as id", "configure Node/Relay features", or when setting up PostGraphile v5 for your specific needs.
compatibility: PostGraphile v5+, graphile-build, graphile-build-pg
metadata:
  author: constructive-io
  version: "1.0.0"
---

# PostGraphile v5 Default Plugin Configuration

Configure PostGraphile v5's default plugins and features to match your project's needs.

## Official Documentation

- Configuration: https://postgraphile.org/postgraphile/next/config
- Node ID / Relay: https://postgraphile.org/postgraphile/next/node-id

## When to Apply

Use this skill when:
- Setting up PostGraphile v5 for a new project
- Deciding which default features to enable or disable
- Configuring how `id` columns are exposed in your schema
- Understanding what the default Amber preset includes

## Understanding Default Features

PostGraphile v5's Amber preset includes several features by default:

1. **Global Object Identification (Node interface)** - Relay-compatible `node(id: ID!)` query
2. **Node ID encoding** - Base64-encoded global IDs for all types
3. **`id` column renaming** - Renames `id` columns to `rowId` to avoid conflict with global `id`
4. **`nodeId` field** - Adds `nodeId` field to all types

These features are useful for Relay clients but can be disabled if not needed.

## Configuration Options

### Option 1: Keep All Default Features (Relay-Compatible)

Use the default Amber preset as-is:

```typescript
import { PostGraphileAmberPreset } from 'postgraphile/presets/amber';

const preset: GraphileConfig.Preset = {
  extends: [PostGraphileAmberPreset],
  // Your configuration
};
```

### Option 2: Disable Global Object Identification

If you don't need Relay compatibility, disable the Node-related plugins:

```typescript
import type { GraphileConfig } from 'graphile-config';
import { defaultPreset as graphileBuildPreset } from 'graphile-build';
import { defaultPreset as graphileBuildPgPreset } from 'graphile-build-pg';

const NODE_PLUGINS = [
  // Core Node plugins from graphile-build
  'NodePlugin',
  'AddNodeInterfaceToSuitableTypesPlugin',
  'NodeIdCodecBase64JSONPlugin',
  'NodeIdCodecPipeStringPlugin',
  'RegisterQueryNodePlugin',
  'NodeAccessorPlugin',
  // PG-specific Node plugins from graphile-build-pg
  'PgNodeIdAttributesPlugin',
  'PgTableNodePlugin',
];

export const CustomPreset: GraphileConfig.Preset = {
  extends: [graphileBuildPreset, graphileBuildPgPreset],
  disablePlugins: NODE_PLUGINS,
};
```

## Plugin Reference

| Plugin | What it does | When to disable |
|--------|--------------|-----------------|
| `NodePlugin` | Adds Node interface and `node()` query | Not using Relay |
| `AddNodeInterfaceToSuitableTypesPlugin` | Makes types implement Node | Not using Relay |
| `NodeIdCodecBase64JSONPlugin` | Encodes node IDs as base64 JSON | Not using Relay |
| `NodeIdCodecPipeStringPlugin` | Alternative node ID encoding | Not using Relay |
| `RegisterQueryNodePlugin` | Registers `node(id)` query | Not using Relay |
| `NodeAccessorPlugin` | Adds `nodeId` field to types | Not using Relay |
| `PgNodeIdAttributesPlugin` | Handles node ID for PG tables | Not using Relay |
| `PgTableNodePlugin` | Makes PG tables implement Node | Not using Relay |

## Keeping `id` Columns as `id`

By default, PostGraphile renames `id` columns to `rowId` to avoid conflict with the global `id` field. If you've disabled the Node plugins and want to keep `id` as `id`, override the `_attributeName` inflector:

```typescript
export const KeepIdPlugin: GraphileConfig.Plugin = {
  name: 'KeepIdPlugin',
  version: '1.0.0',

  inflection: {
    replace: {
      _attributeName(_previous, _options, details) {
        const attribute = details.codec.attributes[details.attributeName];
        const name = attribute?.extensions?.tags?.name || details.attributeName;
        // Don't rename 'id' to 'row_id'
        return this.coerceToGraphQLName(name);
      },
    },
  },
};
```

## Source Code References

### Why `id` gets renamed (PgAttributesPlugin)

```typescript
// From graphile-build-pg/src/plugins/PgAttributesPlugin.ts
_attributeName(options, { attributeName, codec, skipRowId }) {
  const attribute = codec.attributes[attributeName];
  const name = attribute.extensions?.tags?.name || attributeName;
  // Avoid conflict with 'id' field used for Relay.
  const nonconflictName =
    !skipRowId && name.toLowerCase() === "id" && !codec.isAnonymous
      ? "row_id"  // <-- This renames id to row_id!
      : name;
  return this.coerceToGraphQLName(nonconflictName);
}
```

Source: https://github.com/graphile/crystal/blob/924b2515c6bd30e5905ac1419a25244b40c8bb4d/graphile-build/graphile-build-pg/src/plugins/PgAttributesPlugin.ts#L289-L298

## Complete MinimalPreset

```typescript
import type { GraphileConfig } from 'graphile-config';
import { defaultPreset as graphileBuildPreset } from 'graphile-build';
import { defaultPreset as graphileBuildPgPreset } from 'graphile-build-pg';

const NODE_PLUGINS_TO_DISABLE = [
  'NodePlugin',
  'AddNodeInterfaceToSuitableTypesPlugin',
  'NodeIdCodecBase64JSONPlugin',
  'NodeIdCodecPipeStringPlugin',
  'RegisterQueryNodePlugin',
  'NodeAccessorPlugin',
  'PgNodeIdAttributesPlugin',
  'PgTableNodePlugin',
];

const KeepIdPlugin: GraphileConfig.Plugin = {
  name: 'KeepIdPlugin',
  version: '1.0.0',

  inflection: {
    replace: {
      _attributeName(_previous, _options, details) {
        const attribute = details.codec.attributes[details.attributeName];
        const name = attribute?.extensions?.tags?.name || details.attributeName;
        return this.coerceToGraphQLName(name);
      },
    },
  },
};

export const MinimalPreset: GraphileConfig.Preset = {
  extends: [graphileBuildPreset, graphileBuildPgPreset],
  disablePlugins: NODE_PLUGINS_TO_DISABLE,
  plugins: [KeepIdPlugin],
};
```

## Before and After

### Before (with Node/Relay)

```graphql
type User {
  nodeId: ID!        # Global node ID
  rowId: UUID!       # Your actual id column, renamed!
  name: String!
}

type Query {
  node(id: ID!): Node
  userByNodeId(nodeId: ID!): User
  user(rowId: UUID!): User  # Note: rowId, not id
}
```

### After (MinimalPreset)

```graphql
type User {
  id: UUID!          # Your id column, unchanged
  name: String!
}

type Query {
  user(id: UUID!): User  # Clean and simple
}
```

## Usage

```typescript
import { postgraphile } from 'postgraphile';
import { makePgService } from 'postgraphile/adaptors/pg';
import { MinimalPreset } from './minimal-preset';

const preset: GraphileConfig.Preset = {
  extends: [MinimalPreset],
  pgServices: [
    makePgService({
      connectionString: process.env.DATABASE_URL,
      schemas: ['public'],
    }),
  ],
};

const pgl = postgraphile(preset);
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `id` still renamed to `rowId` | Add the KeepIdPlugin inflector override |
| `nodeId` field still appears | Ensure all Node plugins are in disablePlugins |
| Type errors | Install `graphile-build` and `graphile-build-pg` types |
| Missing mutations | Node plugins don't affect mutations, check other plugins |

## References

- PostGraphile v5 Configuration Docs: https://postgraphile.org/postgraphile/next/config
- PostGraphile v5 Node ID Docs: https://postgraphile.org/postgraphile/next/node-id
- See `graphile-v5-inflection` skill for more inflector customizations
- See `graphile-v5-presets` skill for combining presets
