---
id: "001"
title: "Update Constitution to Gemini"
stage: "constitution"
date: "2026-01-12"
surface: "agent"
model: "gpt-4"
feature: "Phase3_Todo_Chatbot"
branch: "main"
user: "user"
command: "/sp.constitution project: Phase3_Todo_Chatbot"
labels: ["constitution", "ai-model", "gemini"]
spec: null
ticket: null
adr: null
pr: null
files:
  - ".specify/memory/constitution.md"
  - "README.md"
tests: []
links: []
outcome: "Successfully updated constitution to reflect Gemini API instead of Claude, updated related documentation files, and incremented version from 1.0.0 to 1.1.0."
evaluation: "All required changes were made successfully. The constitution and related documentation now correctly reference Gemini API instead of Claude as specified in the requirements."
---

# Prompt History Record

## Prompt
```
/sp.constitution project: Phase3_Todo_Chatbot
version: 1.1
description: >
  Phase 3 adds an AI-powered chatbot on top of my Phase 2 full-stack Todo app.
  All CRUD operations are already implemented in Phase 2 agents, sub-agents, and skills.
  No manual coding is required. The agent will be generated using OpenAI Agents SDK
  style architecture but powered by Gemini API key (automation-based AI agent).

goals:
  - Add ChatKit-based chat interface for natural language task management
  - Integrate OpenAI Agents SDK architecture with Gemini model (via API key)
  - Build an automation-style chatbot agent (tool-calling + reasoning)
  - Expose Phase 2 agents as MCP tools:
      - add_task_tool
      - list_tasks_tool
      - complete_task_tool
      - delete_task_tool
      - update_task_tool
  - Store conversations and messages in the database (reuse Phase 2 tables)
  - Stateless server; conversation history fetched from DB on each request
  - Provide friendly AI responses and confirmations for all actions
  - Handle errors gracefully (e.g., task not found, invalid input)

constraints:
  - No manual CRUD logic; use existing Phase 2 agents only
  - Backend: FastAPI + MCP tools + OpenAI Agents SDK-style agent wrapper
  - AI Model: Gemini (via API key, NOT Claude)
  - Frontend: Next.js + React + ChatKit UI
  - Database: Reuse Phase 2 tables (Task, Conversation, Message)
  - Server must be stateless; each request independent
  - Agent must behave like an automation system (intent → tool → response)
  - Deployment must support local and production environments

deliverables:
  - Backend: POST `/api/{user_id}/chat` endpoint
  - MCP tool wrappers for Phase 2 agents
  - Automation chatbot agent (OpenAI Agents SDK pattern + Gemini)
  - ChatKit frontend component integrated with backend
  - Example conversation flows with tool execution
  - Step-by-step deployment instructions

tasks:
  - name: Generate backend /chat endpoint
    description: >
      Create a FastAPI POST /api/{user_id}/chat endpoint.
      Fetch conversation history from database,
      send user message to Gemini-powered automation agent,
      execute returned MCP tool calls,
      store assistant response in DB,
      return structured AI response + tool_calls.

  - name: Generate MCP tool wrappers
    description: >
      Wrap existing Phase 2 agents as MCP-compatible tools:
        - add_task_tool
        - list_tasks_tool
        - complete_task_tool
        - delete_task_tool
        - update_task_tool
      Ensure stateless execution and database consistency.

  - name: Initialize Automation Chatbot Agent
    description: >
      Create an automation-style agent using OpenAI Agents SDK design principles
      but powered by Gemini API key.
      The agent must:
        - Understand user intent
        - Decide which MCP tool to call
        - Execute tools
        - Generate human-friendly responses

  - name: Generate frontend ChatKit component
    description: >
      Create a Next.js + React ChatKit component.
      Show chat history, input box, typing/loading states.
      POST messages to /chat endpoint.
      Render assistant responses cleanly.

  - name: Generate example conversation flows
    description: >
      Provide at least 10 real-world conversations showing:
        - Natural language input
        - Selected MCP tool
        - Tool execution result
        - Final AI response

  - name: Generate deployment instructions
    description: >
      Provide step-by-step instructions to:
        - Run backend and frontend
        - Configure environment variables
        - Add Gemini API key
        - Setup Neon PostgreSQL
        - Configure ChatKit domain allowlist
```

## Response
```
I have successfully updated the project constitution and related documentation to reflect the change from Claude to Gemini API as specified in your requirements. Here's a summary of the changes made:

1. Updated the constitution file (.specify/memory/constitution.md):
   - Changed AI Model reference from "Claude via OpenAI Agents SDK" to "Gemini via API key (NOT Claude)"
   - Updated the Quality Gates section to reference "Gemini agent" instead of "Claude agent"
   - Incremented the version from 1.0.0 to 1.1.0 to reflect the technology stack change
   - Updated the last amended date to today's date (2026-01-12)
   - Updated the Sync Impact Report to reflect these changes

2. Updated the README.md file:
   - Changed the frontend description from "Next.js frontend with OpenAI ChatKit" to "Next.js frontend with ChatKit" (removing the OpenAI reference)

3. The plan-template.md, spec-template.md, and tasks-template.md files were checked but didn't contain specific references to Claude that needed updating.

All changes are consistent with your requirements for Phase 3 of the Todo Chatbot project, which specifies the use of Gemini API instead of Claude.
```