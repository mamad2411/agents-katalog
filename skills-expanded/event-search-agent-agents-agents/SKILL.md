# Agent Architecture

## Overview

This module implements a modular Retrieval-Augmented Generation (RAG)
pipeline where each agent has a single responsibility. The agents
communicate through a shared `AgentState` and execute sequentially to
transform a user query into a grounded response.

## Agent Architecture

![Agent Architecture](https://github.com/sachinp-iit/event-search-agent/blob/main/assets/Agent_Architecture.png)

------------------------------------------------------------------------

# Components

## QueryUnderstandingAgent

**Purpose**

Interprets the user's natural language query and converts it into
structured metadata for downstream retrieval.

**Responsibilities**

-   Normalize the query.
-   Determine intent/domain/category.
-   Incorporate conversation history and summaries.
-   Produce a `QueryUnderstandingSchema`.

**Input** - User query - Conversation history - Conversation summary

**Output** - Structured query object

------------------------------------------------------------------------

## RetrievalAgent

**Purpose**

Retrieves the most relevant transcript chunks.

**Responsibilities**

-   Uses the normalized query.
-   Delegates semantic search to `SearchService`.
-   Returns ranked transcript chunks.

**Input** - Structured query

**Output** - Retrieved transcript chunks

------------------------------------------------------------------------

## AnswerGenerationAgent

**Purpose**

Produces the final grounded answer using retrieved context.

**Responsibilities**

-   Builds the answer-generation prompt.
-   Injects transcript chunks.
-   Calls the LLM.
-   Returns the final response.

**Input** - User query - Retrieved transcript chunks

**Output** - Final answer

------------------------------------------------------------------------

## EntityExtractionAgent

**Purpose**

Extracts entities and relationships from conversation summaries to build
a knowledge graph.

**Responsibilities**

-   Converts summaries into structured entities.
-   Produces relationships.
-   Returns a `KnowledgeGraphSchema`.

**Input** - Conversation summary

**Output** - Knowledge graph entities and relations

------------------------------------------------------------------------

## AgentState

Shared LangGraph state passed between agents.

Stores:

-   User query
-   Normalized query
-   Intent/domain/category
-   Metadata filters
-   Retrieved chunks
-   Reranked chunks
-   Recommendations
-   Summary
-   Final response
-   Execution trace
-   Errors
-   Chat history

------------------------------------------------------------------------

# Overall Flow

1.  User submits a query.
2.  QueryUnderstandingAgent converts it into structured metadata.
3.  RetrievalAgent performs semantic search.
4.  Retrieved chunks are passed to AnswerGenerationAgent.
5.  The LLM generates a grounded response.
6.  Conversation summaries can optionally be processed by
    EntityExtractionAgent to populate a knowledge graph for long-term
    memory and analytics.

------------------------------------------------------------------------

# Design Principles

-   Single responsibility per agent.
-   Prompt-driven architecture.
-   Shared state through LangGraph.
-   Retrieval and generation are decoupled.
-   Easy to extend with reranking, recommendations, or additional
    agents.
