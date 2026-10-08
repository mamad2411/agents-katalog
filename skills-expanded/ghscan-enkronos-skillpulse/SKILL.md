# researcher-web

Performs structured web research with citations.

## Purpose
Used for information gathering tasks that require web lookups and cited synthesis.

## Inputs
- research query
- optional scope
- optional recency constraints

## Outputs
- structured summary
- cited findings
- risk notes if uncertainty is high

## Dependencies
- web search tool
- model access
- YAML manifest compatibility

## Fallback
If degraded, use:
- fallback model
- alternate skill: researcher-basic
