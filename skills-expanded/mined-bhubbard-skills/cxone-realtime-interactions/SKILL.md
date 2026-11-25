---
name: cxone-realtime-interactions
description: Manage and interact with NICE CXone Real-time Interaction APIs and Analytics.
---

# NICE CXone Real-time Interactions Skill

This skill provides patterns for handling real-time interactions, streaming data, and analytics using the NICE CXone APIs.

## Key Concepts

- **Interactions**: Active conversations occurring over various channels (voice, chat, email, social).
- **Real-Time Data**: Streaming data about active calls, queue lengths, and agent states.
- **Studio API Actions**: Within the NICE CXone Studio environment, use "API actions" on the palette to interact with APIs directly within routing scripts.

## API Usage
- **Real-Time Data APIs**: Allow pulling metrics on active interactions. Consider using WebSocket subscriptions or real-time event streams if available, to reduce load compared to polling.
- **Interaction Analytics**: Retrieve data on interaction sentiment, keywords, and transcription snippets.

## Best Practices
- REST API responses are limited to 32 KB per request. Be mindful of payload sizes.
- For high-volume real-time data, ensure your application handles backpressure and network drops gracefully.
- Inject a `CorrelationId` in all headers to trace a single interaction through various microservices and API endpoints.
- Be aware of the data restrictions set in your system configuration ("Restrict Data" tab) which might hide certain campaigns or teams from your real-time dashboards.
