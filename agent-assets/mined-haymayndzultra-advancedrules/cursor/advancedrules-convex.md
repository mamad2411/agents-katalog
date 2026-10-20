# Convex Development Rules

## Technology Stack
- **Platform**: Convex real-time database
- **Language**: TypeScript/JavaScript
- **Build Tool**: Convex CLI
- **Package Manager**: npm/yarn
- **Architecture**: Real-time, reactive database with edge functions

## Core Principles
- Use new function syntax for all Convex functions
- Always include argument and return validators
- Use proper function registration (public vs internal)
- Follow file-based routing conventions
- Implement proper error handling
- Use indexes for efficient queries

## Function Guidelines

### New Function Syntax
- ALWAYS use the new function syntax for Convex functions:
```typescript
import { query } from "./_generated/server";
import { v } from "convex/values";

export const f = query({
  args: {},
  returns: v.null(),
  handler: async (ctx, args) => {
    // Function body
  },
});
```

### HTTP Endpoint Syntax
- HTTP endpoints are defined in `convex/http.ts` and require an `httpAction` decorator:
```typescript
import { httpRouter } from "convex/server";
import { httpAction } from "./_generated/server";

const http = httpRouter();

http.route({
  path: "/echo",
  method: "POST",
  handler: httpAction(async (ctx, req) => {
    const body = await req.bytes();
    return new Response(body, { status: 200 });
  }),
});
```

### Function Registration
- Use `internalQuery`, `internalMutation`, and `internalAction` for private functions
- Use `query`, `mutation`, and `action` for public functions
- NEVER register functions through `api` or `internal` objects
- ALWAYS include argument and return validators
- Use `returns: v.null()` for functions that don't return anything

### Function Calling
- Use `ctx.runQuery` to call queries from queries, mutations, or actions
- Use `ctx.runMutation` to call mutations from mutations or actions
- Use `ctx.runAction` to call actions from actions
- Use `FunctionReference` objects, not direct function calls
- Minimize calls from actions to queries/mutations to avoid race conditions

### Function References
- Use `api` object for public functions registered with `query`, `mutation`, or `action`
- Use `internal` object for private functions registered with `internalQuery`, `internalMutation`, or `internalAction`
- Follow file-based routing: `convex/example.ts` → `api.example.f`
- Support nested directories: `convex/messages/access.ts` → `api.messages.access.h`

## Validator Guidelines
- Use `v.int64()` for signed 64-bit integers (not deprecated `v.bigint()`)
- Use `v.record()` for defining record types
- Avoid `v.map()` and `v.set()` (not supported)
- Always validate function arguments and return types
- Use proper type validators for all data structures

## Schema Guidelines
- Always define schema in `convex/schema.ts`
- Import schema definition functions from `convex/server`
- System fields are automatically added with underscore prefix
- Use proper indexing for query performance
- Define relationships between tables properly

## TypeScript Guidelines
- Use `Id<TableName>` type for document IDs
- Be strict with types, especially around document IDs
- Provide correct types for Record keys and values
- Use proper type annotations when calling functions in same file
- Leverage TypeScript for type safety and IntelliSense

## Query Guidelines
- NEVER use `filter` in queries
- Define indexes in schema and use `withIndex` instead
- Use `.order('asc')` or `.order('desc')` for ordering
- Default ordering is ascending `_creationTime`
- Use `.unique()` to get single documents
- Use `.take(n)` for limiting results
- Use `.collect()` and iterate for deletions

### Full-Text Search
- Use search indexes for text-based queries:
```typescript
const messages = await ctx.db
  .query("messages")
  .withSearchIndex("search_body", (q) =>
    q.search("body", "hello hi").eq("channel", "#general")
  )
  .take(10);
```

## Mutation Guidelines
- Use `ctx.db.replace` to fully replace existing documents
- Use `ctx.db.patch` to shallow merge updates
- Both methods throw errors if document doesn't exist
- Use proper error handling for mutations
- Validate data before mutations

## Scheduling Guidelines
- Use `crons.interval` or `crons.cron` for scheduling
- Avoid deprecated helpers (`crons.hourly`, `crons.daily`, `crons.weekly`)
- Define crons in `crons.ts` file
- Export crons as default
- Use FunctionReference for cron targets

### Cron Example
```typescript
import { cronJobs } from "convex/server";
import { internal } from "./_generated/api";

const crons = cronJobs();

crons.interval("delete inactive users", { hours: 2 }, internal.users.deleteInactive, {});

export default crons;
```

## File Storage Guidelines
- Use `ctx.storage.getUrl()` for signed URLs
- Query `_storage` system table for metadata
- Avoid deprecated `ctx.storage.getMetadata`
- Handle file operations properly
- Implement proper file validation

### File Storage Example
```typescript
import { query } from "./_generated/server";
import { Id } from "./_generated/dataModel";

type FileMetadata = {
  _id: Id<"_storage">;
  _creationTime: number;
  contentType?: string;
  sha256: string;
  size: number;
}

export const exampleQuery = query({
  args: { fileId: v.id("_storage") },
  returns: v.null(),
  handler: async (ctx, args) => {
    const metadata: FileMetadata | null = await ctx.db.system.get(args.fileId);
    console.log(metadata);
    return null;
  },
});
```

## Project Structure
convex/
├─ schema.ts           # Database schema definition
├─ index.ts            # Main API functions
├─ http.ts             # HTTP endpoints
├─ crons.ts            # Scheduled jobs
├─ auth.ts             # Authentication functions
├─ users/              # User-related functions
│   ├─ queries.ts      # User queries
│   ├─ mutations.ts    # User mutations
│   └─ actions.ts      # User actions
├─ messages/            # Message-related functions
│   ├─ queries.ts      # Message queries
│   ├─ mutations.ts    # Message mutations
│   └─ actions.ts      # Message actions
└─ _generated/         # Auto-generated types and API

## Best Practices
- Organize functions by domain in separate files
- Use descriptive function names
- Implement proper error handling
- Use TypeScript for type safety
- Follow naming conventions consistently
- Document complex functions
- Test functions thoroughly

## Performance Optimization
- Use proper indexes for queries
- Minimize database calls
- Use efficient data structures
- Implement proper pagination
- Monitor function performance
- Use caching when appropriate

## Security Considerations
- Validate all input data
- Use proper authentication
- Implement proper authorization
- Secure sensitive operations
- Handle errors gracefully
- Follow security best practices

## Testing Strategy
- Test functions locally with Convex dev
- Use proper test data
- Test error scenarios
- Validate function outputs
- Test edge cases
- Maintain test coverage

## Deployment
- Use Convex CLI for deployment
- Configure environment variables
- Set up proper domains
- Monitor production functions
- Implement proper logging
- Handle deployment errors

## Common Patterns
- Repository pattern for data access
- Service layer for business logic
- Event-driven architecture
- Real-time subscriptions
- Background processing
- File upload handling
