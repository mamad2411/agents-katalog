# AI Research Engine - Development Instructions

## Overview
This document outlines the key prompts and development workflow for building an **AI-native company research engine** using **Mastra.ai, Convex.dev, and Assistant-UI**.

## Development Steps with Prompts:

### 1. Set up Mastra.ai
- **Prompt:** *"Create a new AI agent using Mastra that extracts company data from the web and stores it in a structured format."*
- Run:
  ```bash
  npx create-mastra@latest
  cd mastra-project
  npm install
  ```

### 2. Define a Company Research Agent
- **Prompt:** *"Create a Mastra agent named 'Company Research AI' that uses GPT-4 to search for companies and extract details such as name, website, industry, funding, and key people."*
- Add the following in `companyAgent.ts`:
  ```typescript
  import { Agent } from "mastra";
  import { openai } from "mastra/providers";

  export const companyResearchAgent = new Agent({
    name: "Company Research AI",
    instructions: "Extract and analyze company information from various sources.",
    model: openai("gpt-4"),
    memory: true,
    workflow: {
      steps: [
        { name: "search_companies", action: "search", description: "Find company details online." },
        { name: "extract_info", action: "extract", description: "Extract website, funding, and key people." },
        { name: "store_data", action: "store", description: "Save extracted data in Convex." }
      ]
    }
  });
  ```

### 3. Set up Convex.dev Backend
- **Prompt:** *"Create a Convex schema to store company data, including fields for name, industry, funding, and key people."*
- Define schema in `schema.ts`:
  ```typescript
  import { defineSchema, s } from "convex/schema";

  export default defineSchema({
    companies: {
      name: s.string(),
      website: s.string(),
      industry: s.string(),
      funding: s.optional(s.number()),
      key_people: s.optional(s.array(s.string())),
    },
  });
  ```

### 4. Develop API for Storing Company Data
- **Prompt:** *"Write a Convex function that allows Mastra agents to store extracted company data."*
- Add this in `functions.ts`:
  ```typescript
  import { mutation } from "convex/server";

  export const storeCompanyData = mutation(async ({ db }, companyData) => {
    await db.insert("companies", companyData);
  });
  ```

### 5. Integrate Assistant-UI for Real-time Search
- **Prompt:** *"Install Assistant-UI and add a chat interface for users to search for company data."*
- Run:
  ```bash
  npm install assistant-ui
  ```
- Modify the `App.tsx`:
  ```tsx
  import { ChatInterface } from "assistant-ui";
  import { companyResearchAgent } from "./companyAgent";

  function App() {
    return (
      <ChatInterface
        agent={companyResearchAgent}
        placeholder="Ask about a company..."
      />
    );
  }

  export default App;
  ```

### 6. Deploy the AI Research Engine
- **Prompt:** *"Deploy the Convex backend and run the Mastra agent in production."*
- Run:
  ```bash
  npx convex deploy
  npm start
  ```
