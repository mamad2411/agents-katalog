---
name: x-cli
description: Interact with X API using the x CLI. Use when working with posts, timelines, media uploads, user data, or when the user mentions X, social media, posts, or x.
---

# X CLI

Interact with X API using the `x` command-line tool.

## Prerequisites

```bash
x --version
export X_API_KEY='your-api-key'
export X_API_SECRET='your-api-secret'
export X_ACCESS_TOKEN='your-access-token'
export X_ACCESS_SECRET='your-access-secret'
x auth status
```

## Authentication

- API credentials from X Developer Portal
- Environment variables: `X_API_KEY`, `X_API_SECRET`, `X_ACCESS_TOKEN`, `X_ACCESS_SECRET`
- Or: `x auth login` for OAuth flow

## Tweets

### Create & Manage

```bash
x tweet "Hello from the CLI!"
x tweet "Check this out" --media ./image.png
x tweet "Thread part 1" --thread
x tweet "Thread part 2" --reply-to TWEET_ID
x delete TWEET_ID --confirm
```

### Read Timeline

```bash
x timeline --limit 50
x timeline --user USERNAME --limit 20
x mentions --limit 20
x likes --user USERNAME
```

### Search

```bash
x search --query "#javascript" --limit 100
x search --query "from:elonmusk" --recent
x search --query "AI filter:images" --limit 50
```

## Media

```bash
x upload ./image.jpg --alt "Description"
x upload ./video.mp4 --media-type video
x tweet "Video content" --media MEDIA_ID
```

## Users

```bash
x user get USERNAME
x user followers USERNAME --limit 100
x user following USERNAME --limit 100
x follow USERNAME
x unfollow USERNAME --confirm
```

## Lists & Bookmarks

```bash
x lists list
x lists get LIST_ID --tweets
x lists create "Tech News" --description "Technology updates"
x bookmarks --limit 50
```

## Analytics

```bash
x analytics tweets --days 30
x analytics followers --growth
x export tweets --start 2024-01-01 --format csv
```

## Agent Best Practices

1. **Rate limits**: Respect X API rate limits (check `x limits`)
2. **Tweet length**: 280 characters max (4,000 for X Premium)
3. **Media formats**: JPG, PNG, GIF, MP4 supported
4. **Thread safety**: Use `--thread` flag for multi-tweet threads
