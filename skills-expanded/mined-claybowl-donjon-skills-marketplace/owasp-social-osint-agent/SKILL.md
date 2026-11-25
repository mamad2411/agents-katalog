# OWASP Social OSINT Agent

Tracks targets across handle changes via immutable IDs (e.g., Bluesky DIDs). Aggregates signals (GitHub commits/stars, Reddit karma + subreddit context, Twitter location/verified, HN reputation). Builds Pattern-of-Life heatmaps; outputs structured selectors to JSON (locations, emails, phone numbers, crypto addresses, aliases).

## Triggers
- "owasp social osint"
- "social media osint"
- "handle tracking"
- "pattern of life"
- "bluesky did"
- "social osint agent"

## Description
An OSINT agent focused on tracking individuals across social media platforms despite handle changes, using immutable identifiers like Bluesky DIDs. It aggregates various signals from platforms such as GitHub, Reddit, Twitter, and Hacker News to build a comprehensive profile and Pattern-of-Life analysis.

## Features
- Immutable ID tracking (e.g., Bluesky DIDs)
- Signal aggregation from multiple platforms:
  - GitHub: commits, stars
  - Reddit: karma, subreddit context
  - Twitter: location, verification status
  - Hacker News: reputation
- Pattern-of-Life heatmap generation
- Structured JSON output for:
  - Locations
  - Email addresses
  - Phone numbers
  - Cryptocurrency addresses
  - Aliases
- Handle change resilience
- Cross-platform correlation

## Usage
Use when you need to track an individual's online presence across multiple social media platforms, especially when they frequently change handles or usernames.

## Example
```
/owasp-social-osint-agent track user via bluesky did:did:plc:...
/owasp-social-osint-agent aggregate signals for github:username
/owasp-social-osint-agent generate pattern-of-life heatmap
/owasp-social-osint-agent export selectors to json
```
