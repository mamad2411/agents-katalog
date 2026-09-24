# Repo Referensi: vercel/ai

Repo: https://github.com/vercel/ai
Ref lokal: /Users/chaali0324/.agents/repo-refs/vercel_ai
API: curl "localhost:27126/repos/readme?name=vercel_ai"
Dibuat: 2026-09-16

## Cuplikan README
# vercel/ai

Source: https://github.com/vercel/ai
Fetched: 2026-09-16
Note: root README hanya pointer; isi dari packages/ai/README.md

## README
![hero illustration](https://github.com/vercel/ai/blob/HEAD/assets/hero.gif)

# AI SDK

The [AI SDK](https://ai-sdk.dev/docs) is a provider-agnostic TypeScript toolkit designed to help you build AI-powered applications and agents using popular UI frameworks like Next.js, React, Svelte, Vue, Angular, and runtimes like Node.js.

To learn more about how to use the AI SDK, check out our [API Reference](https://ai-sdk.dev/docs/reference) and [Documentation](https://ai-sdk.dev/docs).

## Installation

You will need Node.js 22+ and npm (or another package manager) installed on your local development machine.

```shell
npm install ai
```

## Skill for Coding Agents

If you use coding agents such as Claude Code or Cursor, we highly recommend adding the AI SDK skill to your repository:

```shell
npx skills add vercel/ai
```

## Unified Provider Architecture

The AI SDK provides a [unified API](https://ai-sdk.dev/docs/foundations/providers-and-models) to interact with model providers like [OpenAI](https://ai-sdk.dev/providers/ai-sdk-providers/openai), [Anthropic](https://ai-sdk.dev/providers/ai-sdk-providers/anthropic), [Google](https://ai-sdk.dev/providers/ai-sdk-providers/google), and [more](https://ai-sdk.dev/providers/ai-sdk-providers).

By default, the AI SDK uses the [Vercel AI Gateway](https://vercel.com/docs/ai-gateway) to give you access to all major providers out of the box. Just pass a model string for any supported model:

```ts
const result = await generateText({
  model: 'anthropic/claude-opus-4.6', // or 'openai/gpt-5.4', 'google/gemini-3-flash', etc.
  prompt: 'Hello!',
});
```

You can also connect to providers directly using their SDK packages:

```shell
npm install @ai-sdk/openai @ai-sdk/anthropic @ai-sdk/google
```

```ts
import { anthropic } from '@ai-sdk/anthropic';

const result = await generateText({
  model: anthropic('claude-opus-4-6'), // or openai('gpt-5.4'), google('gemini-3-flash'), etc.
  prompt: 'Hello!',
});
```

## Usage

### Generating Text

```ts
import { generateText } from 'ai';

const { text } = await generateText({
  model: 'openai/gpt-5.4', // use Vercel AI Gateway
  prompt: 'What is an agent?',
});
```

### Generating Structured Data

```ts
import { generateText, Output } from 'ai';
import { z } from 'zod';

const { output } = await generateText({
  model: 'openai/gpt-5.4',
  output:
