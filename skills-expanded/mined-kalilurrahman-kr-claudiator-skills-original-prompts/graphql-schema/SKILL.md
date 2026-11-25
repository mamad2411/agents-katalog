---
name: graphql-schema
description: Design GraphQL schema with types, queries, mutations, subscriptions. Outputs schema definition, resolvers, N+1 prevention, and error handling.
argument-hint: [data model, query requirements, real-time needs]
allowed-tools: Read, Write, Bash
---

# GraphQL Schema Design

Design production GraphQL API with types, queries, mutations, proper error handling, and N+1 query prevention. Not basic schema — pagination, authorization, batching, subscriptions.

## Process

1. **Define types.** Objects, scalars, enums, interfaces, unions.
2. **Design queries.** Read operations with filtering, sorting, pagination.
3. **Create mutations.** Write operations with input validation, errors.
4. **Add subscriptions.** Real-time updates for WebSocket clients.
5. **Prevent N+1.** DataLoader for batching, caching.
6. **Handle authorization.** Field-level permissions, context.
7. **Plan error handling.** Structured errors, codes, validation.

## Output Format

### GraphQL API: [Application Name]

**Types:** 15 object types  
**Queries:** 20 read operations  
**Mutations:** 12 write operations  
**Subscriptions:** 3 real-time channels  
**N+1 Prevention:** DataLoader batching

---

## Schema Definition (SDL)

```graphql
# User type
type User {
  id: ID!
  email: String!
  name: String!
  posts: [Post!]!
  createdAt: DateTime!
}

# Post type
type Post {
  id: ID!
  title: String!
  content: String!
  author: User!
  comments: [Comment!]!
  published: Boolean!
  createdAt: DateTime!
  updatedAt: DateTime!
}

# Comment type
type Comment {
  id: ID!
  content: String!
  author: User!
  post: Post!
  createdAt: DateTime!
}

# Query root type
type Query {
  # Get single user
  user(id: ID!): User
  
  # List users with pagination
  users(
    first: Int = 10
    after: String
    filter: UserFilter
  ): UserConnection!
  
  # Get single post
  post(id: ID!): Post
  
  # List posts with filters
  posts(
    first: Int = 10
    after: String
    published: Boolean
    authorId: ID
  ): PostConnection!
}

# Mutation root type
type Mutation {
  # Create user
  createUser(input: CreateUserInput!): CreateUserPayload!
  
  # Update user
  updateUser(id: ID!, input: UpdateUserInput!): UpdateUserPayload!
  
  # Delete user
  deleteUser(id: ID!): DeleteUserPayload!
  
  # Create post
  createPost(input: CreatePostInput!): CreatePostPayload!
  
  # Publish post
  publishPost(id: ID!): PublishPostPayload!
}

# Subscription root type
type Subscription {
  # New post published
  postPublished: Post!
  
  # New comment on post
  commentAdded(postId: ID!): Comment!
}

# Input types
input CreateUserInput {
  email: String!
  name: String!
  password: String!
}

input UpdateUserInput {
  email: String
  name: String
}

input CreatePostInput {
  title: String!
  content: String!
  published: Boolean = false
}

input UserFilter {
  email: String
  nameContains: String
}

# Pagination (Relay Cursor Connections)
type UserConnection {
  edges: [UserEdge!]!
  pageInfo: PageInfo!
  totalCount: Int!
}

type UserEdge {
  node: User!
  cursor: String!
}

type PageInfo {
  hasNextPage: Boolean!
  hasPreviousPage: Boolean!
  startCursor: String
  endCursor: String
}

# Mutation payloads
type CreateUserPayload {
  user: User
  errors: [UserError!]
}

type UserError {
  field: String!
  message: String!
  code: String!
}

# Custom scalars
scalar DateTime
scalar JSON
```

---

## Resolvers (Node.js + TypeScript)

```typescript
import { GraphQLResolverMap } from '@apollo/server';
import DataLoader from 'dataloader';

// User resolver
const userResolvers: GraphQLResolverMap = {
  Query: {
    user: async (_, { id }, { db }) => {
      return await db.user.findUnique({ where: { id } });
    },
    
    users: async (_, { first, after, filter }, { db }) => {
      const cursor = after ? { id: after } : undefined;
      
      const users = await db.user.findMany({
        take: first + 1,
        cursor,
        where: {
          ...(filter?.email && { email: filter.email }),
          ...(filter?.nameContains && {
            name: { contains: filter.nameContains }
          })
        },
        orderBy: { createdAt: 'desc' }
      });
      
      const hasNextPage = users.length > first;
      const nodes = hasNextPage ? users.slice(0, -1) : users;
      
      return {
        edges: nodes.map(user => ({
          node: user,
          cursor: user.id
        })),
        pageInfo: {
          hasNextPage,
          hasPreviousPage: !!after,
          startCursor: nodes[0]?.id,
          endCursor: nodes[nodes.length - 1]?.id
        },
        totalCount: await db.user.count({ where })
      };
    }
  },
  
  Mutation: {
    createUser: async (_, { input }, { db }) => {
      try {
        // Validation
        if (!input.email.includes('@')) {
          return {
            user: null,
            errors: [{
              field: 'email',
              message: 'Invalid email format',
              code: 'INVALID_EMAIL'
            }]
          };
        }
        
        // Check duplicate
        const existing = await db.user.findUnique({
          where: { email: input.email }
        });
        
        if (existing) {
          return {
            user: null,
            errors: [{
              field: 'email',
              message: 'Email already exists',
              code: 'DUPLICATE_EMAIL'
            }]
          };
        }
        
        // Create user
        const user = await db.user.create({
          data: {
            email: input.email,
            name: input.name,
            password: await hash(input.password)
          }
        });
        
        return { user, errors: [] };
        
      } catch (error) {
        return {
          user: null,
          errors: [{
            field: 'general',
            message: 'Failed to create user',
            code: 'INTERNAL_ERROR'
          }]
        };
      }
    }
  },
  
  // Field resolvers
  User: {
    // N+1 problem: This loads posts for each user individually
    // posts: async (user, _, { db }) => {
    //   return await db.post.findMany({ where: { authorId: user.id } });
    // },
    
    // Solution: Use DataLoader
    posts: async (user, _, { loaders }) => {
      return await loaders.postsByAuthor.load(user.id);
    }
  }
};
```

---

## DataLoader (N+1 Prevention)

```typescript
import DataLoader from 'dataloader';

// Create loaders in context
export function createLoaders(db: PrismaClient) {
  return {
    // Batch load users by ID
    userById: new DataLoader(async (ids: readonly string[]) => {
      const users = await db.user.findMany({
        where: { id: { in: [...ids] } }
      });
      
      // Return in same order as requested
      const userMap = new Map(users.map(u => [u.id, u]));
      return ids.map(id => userMap.get(id) || null);
    }),
    
    // Batch load posts by author ID
    postsByAuthor: new DataLoader(async (authorIds: readonly string[]) => {
      const posts = await db.post.findMany({
        where: { authorId: { in: [...authorIds] } }
      });
      
      // Group by author ID
      const postsByAuthor = new Map<string, Post[]>();
      for (const post of posts) {
        const existing = postsByAuthor.get(post.authorId) || [];
        postsByAuthor.set(post.authorId, [...existing, post]);
      }
      
      // Return array of arrays in same order
      return authorIds.map(id => postsByAuthor.get(id) || []);
    })
  };
}

// Apollo Server context
const server = new ApolloServer({
  typeDefs,
  resolvers,
  context: ({ req }) => ({
    db: prisma,
    user: req.user,
    loaders: createLoaders(prisma)  // Fresh loaders per request
  })
});
```

**Before DataLoader (N+1):**
```
Query: users { posts { title } }

SQL queries:
1. SELECT * FROM users
2. SELECT * FROM posts WHERE author_id = 1  (user 1's posts)
3. SELECT * FROM posts WHERE author_id = 2  (user 2's posts)
... 100 queries for 100 users
```

**After DataLoader (Batched):**
```
SQL queries:
1. SELECT * FROM users
2. SELECT * FROM posts WHERE author_id IN (1,2,3,...100)  (batched!)
```

---

## Authorization

### Field-Level Authorization
```typescript
const resolvers = {
  User: {
    email: (user, _, { user: currentUser }) => {
      // Only show email to user themselves or admins
      if (currentUser.id === user.id || currentUser.role === 'admin') {
        return user.email;
      }
      return null;
    }
  },
  
  Query: {
    user: async (_, { id }, { user, db }) => {
      if (!user) {
        throw new GraphQLError('Unauthorized', {
          extensions: { code: 'UNAUTHORIZED' }
        });
      }
      
      return await db.user.findUnique({ where: { id } });
    }
  }
};
```

### Directive-Based Authorization
```graphql
directive @auth(requires: Role = USER) on FIELD_DEFINITION | OBJECT

enum Role {
  USER
  ADMIN
}

type Query {
  user(id: ID!): User @auth(requires: USER)
  users: [User!]! @auth(requires: ADMIN)
}
```

```typescript
// Schema directive implementation
class AuthDirective extends SchemaDirectiveVisitor {
  visitFieldDefinition(field) {
    const { resolve = defaultFieldResolver } = field;
    const { requires } = this.args;
    
    field.resolve = async (source, args, context, info) => {
      if (!context.user) {
        throw new GraphQLError('Unauthorized');
      }
      
      if (requires === 'ADMIN' && context.user.role !== 'admin') {
        throw new GraphQLError('Forbidden');
      }
      
      return resolve(source, args, context, info);
    };
  }
}
```

---

## Subscriptions (Real-time)

```typescript
import { PubSub } from 'graphql-subscriptions';

const pubsub = new PubSub();

const resolvers = {
  Mutation: {
    publishPost: async (_, { id }, { db }) => {
      const post = await db.post.update({
        where: { id },
        data: { published: true }
      });
      
      // Publish event
      pubsub.publish('POST_PUBLISHED', { postPublished: post });
      
      return { post };
    },
    
    createComment: async (_, { input }, { db }) => {
      const comment = await db.comment.create({ data: input });
      
      // Publish to specific post subscribers
      pubsub.publish(`COMMENT_ADDED_${input.postId}`, {
        commentAdded: comment
      });
      
      return { comment };
    }
  },
  
  Subscription: {
    postPublished: {
      subscribe: () => pubsub.asyncIterator(['POST_PUBLISHED'])
    },
    
    commentAdded: {
      subscribe: (_, { postId }) => {
        return pubsub.asyncIterator([`COMMENT_ADDED_${postId}`]);
      }
    }
  }
};

// Client subscription (Apollo Client)
const subscription = gql`
  subscription OnCommentAdded($postId: ID!) {
    commentAdded(postId: $postId) {
      id
      content
      author { name }
    }
  }
`;

useSubscription(subscription, { variables: { postId: '123' } });
```

---

## Error Handling

```typescript
import { GraphQLError } from 'graphql';

// Custom error classes
class ValidationError extends GraphQLError {
  constructor(message: string, field: string) {
    super(message, {
      extensions: {
        code: 'VALIDATION_ERROR',
        field
      }
    });
  }
}

class NotFoundError extends GraphQLError {
  constructor(resource: string) {
    super(`${resource} not found`, {
      extensions: { code: 'NOT_FOUND' }
    });
  }
}

// Resolver with error handling
const resolvers = {
  Query: {
    post: async (_, { id }, { db }) => {
      const post = await db.post.findUnique({ where: { id } });
      
      if (!post) {
        throw new NotFoundError('Post');
      }
      
      return post;
    }
  },
  
  Mutation: {
    createPost: async (_, { input }, { user, db }) => {
      if (!user) {
        throw new GraphQLError('Unauthorized', {
          extensions: { code: 'UNAUTHORIZED' }
        });
      }
      
      if (input.title.length < 3) {
        throw new ValidationError('Title too short', 'title');
      }
      
      const post = await db.post.create({
        data: { ...input, authorId: user.id }
      });
      
      return { post, errors: [] };
    }
  }
};

// Error response
{
  "errors": [{
    "message": "Title too short",
    "extensions": {
      "code": "VALIDATION_ERROR",
      "field": "title"
    }
  }]
}
```

---

## Performance Optimization

### Query Complexity Limit
```typescript
import { createComplexityLimitRule } from 'graphql-validation-complexity';

const server = new ApolloServer({
  typeDefs,
  resolvers,
  validationRules: [
    createComplexityLimitRule(1000)  // Max complexity 1000
  ]
});
```

### Depth Limiting
```typescript
import depthLimit from 'graphql-depth-limit';

const server = new ApolloServer({
  validationRules: [depthLimit(5)]  // Max depth 5 levels
});
```

### Caching
```typescript
// Apollo Server cache
const server = new ApolloServer({
  cache: new InMemoryLRUCache({
    maxSize: 100 * 1024 * 1024,  // 100 MB
    ttl: 300  // 5 minutes
  })
});

// Field-level caching
const resolvers = {
  Query: {
    user: async (_, { id }, { dataSources }) => {
      return dataSources.userAPI.getUser(id);  // Caches by ID
    }
  }
};
```

## Rules

- Use cursor-based pagination (Relay spec) for large lists — offset pagination doesn't scale.
- DataLoader required for N+1 prevention — batches and caches database queries per request.
- Field-level authorization, not type-level — different users see different fields on same object.
- Structured error responses with codes — clients can handle errors programmatically.
- Query complexity/depth limits prevent abuse — malicious queries can overwhelm server.
- Fresh DataLoader instance per request — prevents data leakage between requests.
- Subscriptions use PubSub for real-time — WebSocket connections for live updates.
- Input validation in resolvers before DB — return validation errors in structured format.
- Custom scalars for DateTime, JSON — better type safety than String.
- Mutation payloads return object + errors — partial success handling, client doesn't need to guess.
