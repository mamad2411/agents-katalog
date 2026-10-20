---
name: python-graphql
description: "When to activate: Strawberry, Graphene, GraphQL, subscriptions, dataloaders, N+1, schema-first design"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: engineering
  language: python
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---

# Python GraphQL Patterns (Strawberry)

## Schema Definition
```python
import strawberry
from strawberry.fastapi import GraphQLRouter
from strawberry.dataloader import DataLoader
from typing import Optional
import asyncio

@strawberry.type
class User:
    id: int
    email: str
    name: str

@strawberry.type
class Post:
    id: int
    title: str
    author_id: int
    
    @strawberry.field
    async def author(self, info: strawberry.types.Info) -> User:
        return await info.context.loaders.user.load(self.author_id)

@strawberry.type
class Query:
    @strawberry.field
    async def user(self, id: int, info: strawberry.types.Info) -> Optional[User]:
        return await info.context.db.get_user(id)
    
    @strawberry.field
    async def posts(self, info: strawberry.types.Info, limit: int = 20, offset: int = 0) -> list[Post]:
        return await info.context.db.list_posts(limit=limit, offset=offset)

schema = strawberry.Schema(query=Query)
```

## DataLoader (N+1 Prevention)
```python
from strawberry.dataloader import DataLoader

async def load_users_by_ids(keys: list[int]) -> list[User | Exception]:
    users = await db.get_users_by_ids(keys)
    user_map = {u.id: u for u in users}
    return [user_map.get(key, Exception(f"User {key} not found")) for key in keys]

class Context:
    def __init__(self, db: Database) -> None:
        self.db = db
        self.loaders = Loaders(
            user=DataLoader(load_fn=load_users_by_ids),
        )

async def get_context(db: Database = Depends(get_db)) -> Context:
    return Context(db=db)

graphql_app = GraphQLRouter(schema, context_getter=get_context)
```

## Mutations with Input Types
```python
@strawberry.input
class CreatePostInput:
    title: str
    body: str

@strawberry.type
class CreatePostPayload:
    post: Optional[Post] = None
    errors: list[str] = strawberry.field(default_factory=list)

@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create_post(
        self,
        input: CreatePostInput,
        info: strawberry.types.Info,
    ) -> CreatePostPayload:
        if len(input.title) < 3:
            return CreatePostPayload(errors=["Title must be at least 3 characters"])
        
        post = await info.context.db.create_post(
            title=input.title,
            body=input.body,
            author_id=info.context.current_user.id,
        )
        return CreatePostPayload(post=post)
```

## Subscriptions
```python
import asyncio
from typing import AsyncGenerator

@strawberry.type
class Subscription:
    @strawberry.subscription
    async def post_created(self, info: strawberry.types.Info) -> AsyncGenerator[Post, None]:
        async with info.context.pubsub.subscribe("posts") as sub:
            async for event in sub:
                yield event
```
