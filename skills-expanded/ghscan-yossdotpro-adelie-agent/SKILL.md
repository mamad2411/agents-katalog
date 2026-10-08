# Skill: web-search-and-summarize

## Description
Search the web for information and then summarize the results

## When to use
- User wants to research a topic online
- User asks for current information about something
- User wants to gather information from multiple web sources

## Inputs
- query: Search query for web search

## Plan Template
```json
[
  {
    "action": "MCP_RUN",
    "args": {
      "server": "brave-search",
      "tool": "brave_search",
      "input": {
        "query": "$$input.query",
        "count": 5
      }
    }
  },
  {
    "action": "AI_TRANSFORM",
    "args": {
      "task": "Summarize the search results and provide key insights",
      "content": "$$1"
    }
  }
]
```

## Example
User: Search for information about quantum computing advances in 2024

## Expected behavior
The skill will search the web for "quantum computing advances in 2024", get the top 5 results, and then use AI to summarize the key findings and insights from those results.
