# Repo Referensi: vercel/ai-elements

Repo: https://github.com/vercel/ai-elements
Ref lokal: /Users/chaali0324/.agents/repo-refs/vercel_ai-elements
API: curl "localhost:27126/repos/readme?name=vercel_ai-elements"
Dibuat: 2026-09-16

## Cuplikan README
# vercel/ai-elements

Source: https://github.com/vercel/ai-elements
Fetched: 2026-09-16

## README
# ▲ AI Elements

[AI Elements](https://elements.ai-sdk.dev) is a component library built on top of [shadcn/ui](https://ui.shadcn.com/) to help you build AI-native applications faster.

## Overview

AI Elements provides pre-built, customizable React components specifically designed for AI applications, including conversations, messages, code blocks, reasoning displays, and more. The CLI makes it easy to add these components to your Next.js project.

## Installation

You can use the AI Elements CLI directly with npx, or install it globally:

```bash
# Use directly (recommended)
npx ai-elements@latest

# Or using shadcn cli
npx shadcn@latest add https://elements.ai-sdk.dev/api/registry/all.json
```

## Prerequisites

Before using AI Elements, ensure your project meets these requirements:

- **Node.js** 18 or later
- **Next.js** project with [AI SDK](https://ai-sdk.dev/) installed
- **shadcn/ui** initialized in your project (`npx shadcn@latest init`)
- **Tailwind CSS** configured (AI Elements supports CSS Variables mode only)

## Usage

### Install All Components

Install all available AI Elements components at once:

```bash
npx ai-elements@latest
```

This command will:

- Set up shadcn/ui if not already configured
- Install all AI Elements components to your configured components directory
- Add necessary dependencies to your project

### Install Specific Components

Install individual components using the `add` command:

```bash
npx ai-elements@latest add <component-name>
```

Examples:

```bash
# Install the message component
npx ai-elements@latest add message

# Install the conversation component
npx ai-elements@latest add conversation

# Install the code-block component
npx ai-elements@latest add code-block
```

### Alternative: Use with shadcn CLI

You can also install components using the standard shadcn/ui CLI:

```bash
# Install all components
npx shadcn@latest add https://elements.ai-sdk.dev/api/registry/all.json

# Install a specific component
npx shadcn@latest add https://elements.ai-sdk.dev/api/registry/message.json
```

## Quick Start Example

After installing components, you can use them in your React application:

```tsx
"use client";

import { useChat } from "@ai-sdk/react";
import {
  Conversation,
  ConversationContent,
} from "@/components/ai-elements/conversation";
import {
  Message,
  MessageContent,
  MessageResponse,
} from "@/component
