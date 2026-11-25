# Apollo Client Implementation

## Purpose
Configures Apollo Client to communicate with SIT Apollo Router and consumes generated GraphQL types.

## Role
Frontend Developer

## Phase
Development

## Triggered By
New webapp needs API integration.

## Inputs
- `RSBUILD_PUBLIC_API_URL` environment variable
- Generated types from `packages/api/src/generated/{service}/graphql/`

## Rules
ALL API calls via Apollo Client → SIT Apollo Router. NEVER call gRPC or REST directly from frontend. Generated types: `packages/api/src/generated/{service}/graphql/` ONLY. Client configured in: `shared/libs/apolloClient.ts`.

## Process

### Apollo Client Configuration
```typescript
// shared/libs/apolloClient.ts
import { ApolloClient, InMemoryCache, createHttpLink } from '@apollo/client'

const httpLink = createHttpLink({
  uri: process.env.RSBUILD_PUBLIC_API_URL,
})

export const apolloClient = new ApolloClient({
  link: httpLink,
  cache: new InMemoryCache(),
  defaultOptions: {
    watchQuery: { fetchPolicy: 'cache-first' },
    query: { fetchPolicy: 'cache-first' },
    mutate: { fetchPolicy: 'no-cache' },
  },
})
```

### Cache Policies
- Queries: `cache-first` (data doesn't change frequently)
- Mutations: `no-cache` (always get fresh data after mutation)
- Real-time data: `network-only`

## Outputs
Configured Apollo Client instance in `shared/libs/apolloClient.ts`.

## Quality Gates
- [ ] Client configured in shared/libs/apolloClient.ts
- [ ] URI from environment variable (not hardcoded)
- [ ] Generated types used (not hand-written interfaces)
- [ ] Cache policies appropriate per operation type

## References
- `.claude/skills/frontend-developer/environment-configuration/SKILL.md`
- `.claude/skills/frontend-developer/hook-development/SKILL.md`
