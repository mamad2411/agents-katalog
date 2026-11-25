---
name: "graphql-client"
description: "- Setting up a GraphQL client in a React or Next.js project"
---

# GraphQL Client Integration

## When to activate

- Setting up a GraphQL client in a React or Next.js project
- Consuming a GraphQL API with typed queries
- Configuring Apollo Client, urql, or Tanstack Query with GraphQL
- Adding GraphQL Code Generator for TypeScript type generation
- Implementing optimistic updates, subscriptions, or cache management
- User asks how to write a `useQuery`, `useMutation`, or `useSubscription` hook

## When NOT to use

- The project is building a GraphQL **server** — use a backend skill instead
- The API is REST-only — no GraphQL endpoint exists
- The project already has a configured GraphQL client and just needs a query written — no setup needed, write the query directly

## Instructions

### Apollo Client Setup (React / Next.js)

**Install:**
```bash
npm install @apollo/client graphql
```

**Client configuration** (`lib/apollo-client.ts`):
```typescript
import { ApolloClient, InMemoryCache, HttpLink, from } from "@apollo/client";
import { onError } from "@apollo/client/link/error";

const errorLink = onError(({ graphQLErrors, networkError }) => {
  if (graphQLErrors) {
    graphQLErrors.forEach(({ message, locations, path }) =>
      console.error(`GraphQL error: ${message}`, { locations, path })
    );
  }
  if (networkError) console.error("Network error:", networkError);
});

const httpLink = new HttpLink({ uri: process.env.NEXT_PUBLIC_GRAPHQL_URL });

export const client = new ApolloClient({
  link: from([errorLink, httpLink]),
  cache: new InMemoryCache({
    typePolicies: {
      // Example: normalize by id field
      Product: {
        keyFields: ["id"],
      },
      // Example: paginated field merge
      Query: {
        fields: {
          products: {
            keyArgs: ["filter"],
            merge(existing = { items: [] }, incoming) {
              return { ...incoming, items: [...existing.items, ...incoming.items] };
            },
          },
        },
      },
    },
  }),
  defaultOptions: {
    watchQuery: { fetchPolicy: "cache-and-network" },
  },
});
```

**Provider** (App Router: `app/providers.tsx`):
```typescript
"use client";
import { ApolloProvider } from "@apollo/client";
import { client } from "@/lib/apollo-client";

export function Providers({ children }: { children: React.ReactNode }) {
  return <ApolloProvider client={client}>{children}</ApolloProvider>;
}
```

### Query / Mutation / Subscription Hooks

**useQuery:**
```typescript
import { useQuery, gql } from "@apollo/client";

const GET_USER = gql`
  query GetUser($id: ID!) {
    user(id: $id) {
      id
      name
      email
    }
  }
`;

function UserProfile({ id }: { id: string }) {
  const { data, loading, error } = useQuery(GET_USER, {
    variables: { id },
    skip: !id,
  });

  if (loading) return <Skeleton />;
  if (error) return <ErrorMessage error={error} />;
  return <div>{data.user.name}</div>;
}
```

**useMutation:**
```typescript
const UPDATE_USER = gql`
  mutation UpdateUser($id: ID!, $input: UpdateUserInput!) {
    updateUser(id: $id, input: $input) {
      id
      name
      email
    }
  }
`;

function EditUser({ id }: { id: string }) {
  const [updateUser, { loading }] = useMutation(UPDATE_USER, {
    onCompleted: () => toast.success("Saved"),
    onError: (err) => toast.error(err.message),
  });

  return (
    <button
      onClick={() => updateUser({ variables: { id, input: { name: "New Name" } } })}
      disabled={loading}
    >
      Save
    </button>
  );
}
```

**useSubscription:**
```typescript
import { useSubscription } from "@apollo/client";

const ON_MESSAGE = gql`
  subscription OnMessage($roomId: ID!) {
    messageAdded(roomId: $roomId) {
      id
      content
      author { name }
    }
  }
`;

function ChatRoom({ roomId }: { roomId: string }) {
  const { data } = useSubscription(ON_MESSAGE, { variables: { roomId } });
  // data.messageAdded is the latest message
}
```

### Cache Updates After Mutation

**Prefer `cache.modify` for targeted updates** (avoids full refetch):
```typescript
const [addItem] = useMutation(ADD_ITEM, {
  update(cache, { data: { addItem } }) {
    cache.modify({
      fields: {
        items(existingRefs = [], { toReference }) {
          return [...existingRefs, toReference(addItem)];
        },
      },
    });
  },
});
```

**Use `refetchQueries` only when the cache update is non-trivial:**
```typescript
const [deleteItem] = useMutation(DELETE_ITEM, {
  refetchQueries: [{ query: GET_ITEMS }],
  awaitRefetchQueries: true,
});
```

**Optimistic updates** — show the result immediately, revert if the mutation fails:
```typescript
const [likePost] = useMutation(LIKE_POST, {
  optimisticResponse: {
    likePost: {
      __typename: "Post",
      id: postId,
      likeCount: currentLikeCount + 1,
      likedByMe: true,
    },
  },
});
```

### urql as a Lightweight Alternative

Use urql when you want a smaller bundle and simpler setup:
```bash
npm install urql graphql
```
```typescript
import { createClient, Provider } from "urql";
const client = createClient({ url: "/api/graphql" });

// In component
const [result] = useQuery({ query: GET_USER, variables: { id } });
const [, executeMutation] = useMutation(UPDATE_USER);
```

urql is the right choice for: Next.js apps where bundle size matters, projects not needing complex cache policies, apps with mostly read-heavy, simple queries.

### GraphQL Code Generator

**Install:**
```bash
npm install -D @graphql-codegen/cli @graphql-codegen/typescript @graphql-codegen/typescript-operations @graphql-codegen/typescript-react-apollo
```

**`codegen.ts`:**
```typescript
import type { CodegenConfig } from "@graphql-codegen/cli";

const config: CodegenConfig = {
  schema: process.env.NEXT_PUBLIC_GRAPHQL_URL,
  documents: ["src/**/*.tsx", "src/**/*.ts"],
  generates: {
    "src/generated/graphql.ts": {
      plugins: [
        "typescript",
        "typescript-operations",
        "typescript-react-apollo",
      ],
      config: {
        withHooks: true,
        withComponent: false,
        skipTypename: false,
      },
    },
  },
};
export default config;
```

**`package.json` scripts:**
```json
{
  "scripts": {
    "codegen": "graphql-codegen --config codegen.ts",
    "codegen:watch": "graphql-codegen --config codegen.ts --watch"
  }
}
```

Run `npm run codegen` after schema changes. Import typed hooks from `src/generated/graphql.ts` — no manual type declarations needed.

### Fragment Colocation

Define fragments alongside the components that use them:
```typescript
// UserCard.tsx
export const USER_CARD_FRAGMENT = gql`
  fragment UserCard on User {
    id
    name
    avatarUrl
  }
`;

// Parent query composes fragments
const GET_TEAM = gql`
  query GetTeam($id: ID!) {
    team(id: $id) {
      members {
        ...UserCard
      }
    }
  }
  ${USER_CARD_FRAGMENT}
`;
```

### GraphQL vs Network Errors

Apollo distinguishes two error types — handle both:
```typescript
const { data, error } = useQuery(GET_USER, { variables: { id } });

if (error?.networkError) {
  // Server unreachable, timeout, non-2xx HTTP
  return <NetworkErrorBanner />;
}

if (error?.graphQLErrors?.length) {
  // Server returned errors in the GraphQL response body
  const isUnauthorized = error.graphQLErrors.some(
    (e) => e.extensions?.code === "UNAUTHENTICATED"
  );
  if (isUnauthorized) redirect("/login");
  return <ErrorMessage errors={error.graphQLErrors} />;
}
```

## Example

Set up Apollo Client in a Next.js App Router project, write a typed query with codegen, and implement an optimistic update for a mutation.

**1. Configure the client** (`lib/apollo-client.ts`) and wrap the app in `ApolloProvider` via `app/providers.tsx`.

**2. Write the query document** in `src/queries/products.ts`:
```graphql
query GetProducts($filter: ProductFilter) {
  products(filter: $filter) {
    id
    name
    price
    inStock
  }
}

mutation UpdateStock($id: ID!, $quantity: Int!) {
  updateStock(id: $id, quantity: $quantity) {
    id
    inStock
  }
}
```

**3. Run codegen** — generates `useGetProductsQuery` and `useUpdateStockMutation` with full TypeScript types.

**4. Use in the component:**
```typescript
import { useGetProductsQuery, useUpdateStockMutation } from "@/generated/graphql";

export function ProductList() {
  const { data, loading } = useGetProductsQuery({
    variables: { filter: { inStock: true } },
  });

  const [updateStock] = useUpdateStockMutation({
    optimisticResponse: ({ id, quantity }) => ({
      updateStock: { __typename: "Product", id, inStock: quantity > 0 },
    }),
  });

  if (loading) return <Spinner />;
  return (
    <ul>
      {data?.products.map((p) => (
        <li key={p.id}>
          {p.name} — {p.inStock ? "In stock" : "Out of stock"}
          <button onClick={() => updateStock({ variables: { id: p.id, quantity: 10 } })}>
            Restock
          </button>
        </li>
      ))}
    </ul>
  );
}
```

---
