---
name: buffer-api
version: 1.1.0
description: "Schedule, create, and manage social media posts via the Buffer GraphQL API. Use this skill when the user wants to post to social media through Buffer, schedule posts, create ideas, list channels, retrieve posts, or manage their Buffer queue. Triggers on: Buffer, schedule a post, publish to social media, Buffer API, social media queue, Buffer channels, create Buffer post, Buffer idea, or any mention of posting to LinkedIn/Twitter/Instagram/Facebook/Bluesky/Threads/Pinterest/Mastodon/YouTube/TikTok via Buffer."
---

# Buffer GraphQL API

Schedule, create, and manage social media posts through Buffer's GraphQL API.

## Prerequisites

- A Buffer account (any plan) with verified email
- An API key from [Buffer API Settings](https://publish.buffer.com/settings/api)
- Store the key as `BUFFER_API_KEY` environment variable

Paid accounts can generate up to 5 API keys. Free accounts get 1. TikTok is not supported via the API at this time.

## Endpoint

```
POST https://api.buffer.com
Content-Type: application/json
Authorization: Bearer $BUFFER_API_KEY
```

All requests are GraphQL POST requests to this single endpoint.

## Authentication

Every request needs the `Authorization: Bearer` header:

```bash
curl -X POST 'https://api.buffer.com' \
  -H 'Content-Type: application/json' \
  -H "Authorization: Bearer $BUFFER_API_KEY" \
  -d '{"query": "{ account { organizations { id } } }"}'
```

## Supported Operations

| Operation | Type | Description |
|-----------|------|-------------|
| `account` | Query | Get authenticated user info |
| `channel` | Query | Fetch single channel by ID |
| `channels` | Query | Fetch all channels for an org |
| `post` | Query | Fetch single post by ID |
| `posts` | Query | Fetch posts with filters, sorting, pagination |
| `dailyPostingLimits` | Query | Check posting limits per channel per date |
| `createPost` | Mutation | Create and schedule a post |
| `deletePost` | Mutation | Delete a post by ID |
| `createIdea` | Mutation | Save an idea to the ideas board |

## Setup Flow

Before creating posts, you need your organization ID and channel IDs. Run these queries in order:

### 1. Get Organizations

```graphql
query GetOrganizations {
  account {
    organizations {
      id
    }
  }
}
```

### 2. Get Channels

```graphql
query GetChannels {
  channels(input: { organizationId: "YOUR_ORG_ID" }) {
    id
    name
    service
    type
  }
}
```

Filter by service type:

```graphql
query GetFilteredChannels {
  channels(
    input: {
      organizationId: "YOUR_ORG_ID"
      filter: { services: [linkedin] }
    }
  ) {
    id
    name
    service
    type
  }
}
```

**Service enum values:** `facebook`, `twitter`, `instagram`, `linkedin`, `pinterest`, `googlebusiness`, `mastodon`, `tiktok`, `bluesky`, `youtube`, `threads`, `startpage`

### 3. Get a Single Channel

```graphql
query GetChannel {
  channel(input: { channelId: "YOUR_CHANNEL_ID" }) {
    id
    name
    service
    type
    metadata {
      ... on LinkedInMetadata { handle }
      ... on TwitterMetadata { handle }
      ... on FacebookMetadata { facebookPageName }
      ... on InstagramMetadata { handle }
    }
  }
}
```

## Creating Posts

### Text Post

```graphql
mutation CreatePost {
  createPost(input: {
    text: "Hello from the Buffer API!",
    channelId: "YOUR_CHANNEL_ID",
    schedulingType: automatic,
    mode: addToQueue
  }) {
    ... on PostActionSuccess {
      post {
        id
        text
        status
      }
    }
    ... on MutationError {
      message
    }
  }
}
```

### Image Post

Same as text post, with `assets.images`:

```graphql
mutation CreateImagePost {
  createPost(input: {
    text: "Check out this image!",
    channelId: "YOUR_CHANNEL_ID",
    schedulingType: automatic,
    mode: addToQueue,
    assets: {
      images: [
        { url: "https://example.com/image.jpg" }
      ]
    }
  }) {
    ... on PostActionSuccess {
      post {
        id
        text
        assets { id mimeType }
      }
    }
    ... on MutationError {
      message
    }
  }
}
```

### Scheduled Post (Specific Time)

Use `mode: customSchedule` with a `dueAt` ISO 8601 timestamp:

```graphql
mutation CreateScheduledPost {
  createPost(input: {
    text: "Posting at a specific time",
    channelId: "YOUR_CHANNEL_ID",
    schedulingType: automatic,
    mode: customSchedule,
    dueAt: "2026-04-01T14:00:00.000Z"
  }) {
    ... on PostActionSuccess {
      post { id text status }
    }
    ... on MutationError { message }
  }
}
```

### Share Now

Use `mode: shareNow`:

```graphql
mutation ShareNow {
  createPost(input: {
    text: "Publishing immediately!",
    channelId: "YOUR_CHANNEL_ID",
    schedulingType: automatic,
    mode: shareNow
  }) {
    ... on PostActionSuccess {
      post { id text status }
    }
    ... on MutationError { message }
  }
}
```

### Share Next

Use `mode: shareNext` to push the post to the front of the queue:

```graphql
mutation ShareNext {
  createPost(input: {
    text: "This goes next in the queue",
    channelId: "YOUR_CHANNEL_ID",
    schedulingType: automatic,
    mode: shareNext
  }) {
    ... on PostActionSuccess {
      post { id text status }
    }
    ... on MutationError { message }
  }
}
```

### CreatePostInput Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `text` | String | Yes | Post content |
| `channelId` | ChannelId | Yes | Target channel |
| `schedulingType` | Enum | Yes | `automatic` or `notification` |
| `mode` | Enum | Yes | `addToQueue`, `shareNow`, `shareNext`, `customSchedule` |
| `dueAt` | DateTime | For customSchedule | ISO 8601 timestamp |
| `assets` | AssetsInput | No | Images, videos, documents, links |

### AssetsInput

```graphql
assets: {
  images: [{ url: "https://..." }]
  videos: [{ url: "https://...", title: "My Video" }]
  documents: [{ url: "https://..." }]
  link: { url: "https://..." }
}
```

## Creating Ideas

Save content ideas to the Buffer ideas board:

```graphql
mutation CreateIdea {
  createIdea(input: {
    organizationId: "YOUR_ORG_ID",
    content: {
      title: "Blog post idea"
      text: "Write about the new GraphQL API features"
    }
  }) {
    ... on Idea {
      id
      content { title text }
    }
  }
}
```

## Retrieving Posts

### Get Scheduled Posts

```graphql
query GetScheduledPosts {
  posts(
    input: {
      organizationId: "YOUR_ORG_ID",
      filter: { status: [scheduled] },
      sort: [{ field: dueAt, direction: asc }]
    }
  ) {
    totalCount
    edges {
      node {
        id
        text
        status
        createdAt
        dueAt
        channelId
      }
    }
    pageInfo {
      hasNextPage
      endCursor
    }
  }
}
```

### Get Sent Posts for a Channel

```graphql
query GetSentPosts {
  posts(
    input: {
      organizationId: "YOUR_ORG_ID",
      filter: {
        status: [sent],
        channelIds: ["YOUR_CHANNEL_ID"]
      }
    }
  ) {
    edges {
      node {
        id
        text
        createdAt
        channelId
      }
    }
  }
}
```

### Get Posts with Assets

```graphql
query GetPostsWithAssets {
  posts(
    input: {
      organizationId: "YOUR_ORG_ID",
      filter: { status: [sent], channelIds: ["YOUR_CHANNEL_ID"] }
    }
  ) {
    edges {
      node {
        id
        text
        assets {
          thumbnail
          mimeType
          source
          ... on ImageAsset {
            image { altText width height }
          }
        }
      }
    }
  }
}
```

### Paginated Posts

Use `first` and `after` for cursor-based pagination:

```graphql
query GetPaginatedPosts {
  posts(
    input: { organizationId: "YOUR_ORG_ID" },
    first: 10,
    after: "CURSOR_FROM_PREVIOUS_PAGE"
  ) {
    edges {
      node { id text status }
    }
    pageInfo {
      hasNextPage
      endCursor
    }
    totalCount
  }
}
```

### PostStatus Enum Values

`draft`, `scheduled`, `sent`, `error`, `deleted`, `approval_pending`, `approval_rejected`

### PostSortableKey Enum Values

`dueAt`, `createdAt`

## Deleting Posts

```graphql
mutation DeletePost {
  deletePost(input: { postId: "POST_ID" }) {
    ... on DeletePostSuccess {
      post { id status }
    }
    ... on MutationError { message }
  }
}
```

## curl Recipes

### Quick post to queue

```bash
curl -X POST 'https://api.buffer.com' \
  -H 'Content-Type: application/json' \
  -H "Authorization: Bearer $BUFFER_API_KEY" \
  -d "$(jq -n --arg text "Hello from the API" --arg ch "$BUFFER_CHANNEL_ID" '{
    query: "mutation CreatePost($input: CreatePostInput!) { createPost(input: $input) { ... on PostActionSuccess { post { id text } } ... on MutationError { message } } }",
    variables: { input: { text: $text, channelId: $ch, schedulingType: "automatic", mode: "addToQueue" } }
  }')"
```

### List scheduled posts

```bash
curl -X POST 'https://api.buffer.com' \
  -H 'Content-Type: application/json' \
  -H "Authorization: Bearer $BUFFER_API_KEY" \
  -d "$(jq -n --arg org "$BUFFER_ORG_ID" '{
    query: "query($input: PostsInput!) { posts(input: $input, first: 20) { edges { node { id text dueAt channelId } } } }",
    variables: { input: { organizationId: $org, filter: { status: ["scheduled"] }, sort: [{ field: "dueAt", direction: "asc" }] } }
  }')"
```

## Agentic Workflow & Vibe Coding

- **Iterative Scheduling:** Do not expect complex GraphQL payloads to perfectly schedule multi-asset posts on the first try. Draft the payload, test it as a draft or send it to the ideas board, isolate any specific schema or media attachment errors, refine ONE field at a time, and re-test until the post format is correct.
- **Vibe Coding:** Commit your working GraphQL queries or scheduling scripts locally before attempting destructive operations or bulk queue modifications.

## Error Handling

### Mutation Errors (Recoverable)

Returned as typed union members. Always include `... on MutationError { message }` in mutations:

```graphql
... on PostActionSuccess { post { id } }
... on MutationError { message }
```

Specific error types: `QueueLimitError`, `PostAlreadyExistsError`, `ValidationError`, `LimitReachedError`, `InvalidInputError`, `UnauthorizedError`, `VoidMutationError`

### Query Errors (Non-recoverable)

Returned in the standard GraphQL `errors` array with extension codes:

| Code | Meaning |
|------|---------|
| `NOT_FOUND` | Resource does not exist |
| `FORBIDDEN` | No permission |
| `UNAUTHORIZED` | Auth required or invalid |
| `UNEXPECTED` | Server error |
| `RATE_LIMIT_EXCEEDED` | Too many requests |

## Rate Limits

| Client Type | Limit |
|-------------|-------|
| Third-party clients | 100 requests / 15 min |
| Unknown/unauthenticated | 50 requests / 15 min |
| Account overall (all clients) | 2,000 requests / 15 min |

Response headers: `RateLimit-Limit`, `RateLimit-Remaining`, `RateLimit-Reset`

On 429, use the `retryAfter` value (seconds) from the error response.

## Query Limits

| Limit | Value |
|-------|-------|
| Max query complexity | 175,000 points |
| Max query depth | 25 levels |
| Max aliases | 30 |
| Max directives | 50 |
| Max tokens | 15,000 |

## Supported Channels

Facebook, Twitter/X, Instagram, LinkedIn, Pinterest, Google Business, Mastodon, TikTok (not via API), Bluesky, YouTube, Threads, Start Page

## Agentic OS Integration

If the current project root contains an `.agent/` directory, this skill MUST participate in the Agentic OS shared-memory model.

At the end of your execution, check for `.agent/state/last-run.json`. If it exists, append or update the file using its required schema to log your run. Ensure you capture your runtime (`agent_runtime`), `skill_executed`, a concise `summary`, `decisions`, and `next_steps`.

## Reference

- [Developer Docs](https://developers.buffer.com/)
- [API Reference](https://developers.buffer.com/reference.html)
- [GraphQL Explorer](https://developers.buffer.com/explorer.html)
- [API Changelog](https://developers.buffer.com/changelog.html)
- [API Status](https://status.buffer.com/)
- [Discord](https://discord.gg/9kb24u2tEv)
