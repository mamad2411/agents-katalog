# AGENT.md

## Tech Stack

- **TypeScript** (target: ES2022/ESNext)
- **pi-coding-agent**: Extension API for the pi harness.
- **Ollama REST API**: Communication with Ollama via HTTP requests (`fetch`).

## Entry Point: `src/index.ts`

- Exports a default function receiving `pi: ExtensionAPI`.
- Creates an instance of `OllamaClient`.
- Listens to `pi.on("model_select", ...)`.

### `src/index.ts` Logic

1. **Trigger**: On every model switch.
2. **Check**: If `previousModel.provider !== "ollama"`, do nothing.
3. **Filter**: Don't stop if `next === prev`.
4. **Action**: Call `client.stopModel(previousModelId, ctx.signal)` to clean up resources via the Ollama REST API.

### `src/ollama-client.ts`

- **`OllamaClient` class**: Encapsulates all network communication with Ollama.
- **`host`**: Read from `process.env.OLLAMA_HOST` (default: `http://localhost:11434`).
- **`generate(options, signal?)`**: Sends HTTP POST requests to `${host}/api/generate`.
- **`stopModel(modelName, signal?)`**: Convenience method that calls `generate()` with `{ model: modelName, keep_alive: 0 }` to force immediate model unloading.
