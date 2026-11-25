---
name: mixerbox-freecabletv
description: "MixerBox FreecableTV API skill. Use when working with MixerBox FreecableTV for services?funcs=GetShowsForChatGPT&mobile=0, services?funcs=GetMoviesForChatGPT&mobile=0, services?funcs=GetChannelsForChatGPT&mobile=0. Covers 3 endpoints."
version: 1.0.0
generator: lapsh
---

# MixerBox FreecableTV
API version: v1

## Auth
No authentication required.

## Base URL
https://api.freetv-app.com

## Setup
1. No auth setup needed
2. GET /services?funcs=GetShowsForChatGPT&mobile=0 -- verify access

## Endpoints

3 endpoints across 3 groups. See references/api-spec.lap for full details.

### services?funcs=GetShowsForChatGPT&mobile=0
| Method | Path | Description |
|--------|------|-------------|
| GET | /services?funcs=GetShowsForChatGPT&mobile=0 | Get the latest or trending TV shows for a specific country. |

### services?funcs=GetMoviesForChatGPT&mobile=0
| Method | Path | Description |
|--------|------|-------------|
| GET | /services?funcs=GetMoviesForChatGPT&mobile=0 | Get the latest or trending movies for a specific country. |

### services?funcs=GetChannelsForChatGPT&mobile=0
| Method | Path | Description |
|--------|------|-------------|
| GET | /services?funcs=GetChannelsForChatGPT&mobile=0 | Get specific type of channels, including news channels, sports channels and live channels. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all services?funcs=GetShowsForChatGPT&mobile=0?" -> GET /services?funcs=GetShowsForChatGPT&mobile=0
- "List all services?funcs=GetMoviesForChatGPT&mobile=0?" -> GET /services?funcs=GetMoviesForChatGPT&mobile=0
- "List all services?funcs=GetChannelsForChatGPT&mobile=0?" -> GET /services?funcs=GetChannelsForChatGPT&mobile=0

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
