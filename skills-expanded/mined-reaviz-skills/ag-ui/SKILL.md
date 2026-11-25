# useAgUi

React hook that connects an [AG-UI](https://docs.ag-ui.com) protocol agent endpoint to reachat. Returns the props needed by `<Chat>` plus session helpers, and streams responses via SSE (`text/event-stream`).

## Imports

```tsx
import { useAgUi } from 'reachat';
import type {
  AgUiEvent,
  AgUiEventType,
  AgUiMessage,
  AgUiTool,
  AgUiContext,
  AgUiToolCallInfo,
  AgUiRunAgentInput,
  UseAgUiOptions,
  UseAgUiReturn
} from 'reachat';
```

The AG-UI protocol types are bundled with reachat — no separate `@ag-ui/core` install is needed.

## Options

```ts
interface UseAgUiOptions {
  agent: string;                              // Endpoint URL (POST + SSE response)
  initialSessions?: Session[];
  initialActiveSessionId?: string;
  tools?: AgUiTool[];                         // Tools to expose to the agent
  context?: AgUiContext[];                    // Extra context per run
  forwardedProps?: Record<string, unknown>;   // Passthrough props to the agent
  headers?: Record<string, string>;           // Custom request headers
  onToolCall?: (toolCall: AgUiToolCallInfo) => Promise<void> | void;
  onError?: (error: Error) => void;
  onEvent?: (event: AgUiEvent) => void;       // Fires for every parsed event
}
```

## Return value

```ts
interface UseAgUiReturn {
  sessions: Session[];
  activeSessionId: string | undefined;
  isLoading: boolean;
  selectSession: (sessionId: string) => void;
  deleteSession: (sessionId: string) => void;
  createSession: () => void;
  sendMessage: (message: string) => void;
  stopMessage: () => void;
}
```

The shape mirrors the props `<Chat>` expects — pass them through directly.

## Basic usage

```tsx
import { Chat, SessionMessagePanel, SessionMessages, ChatInput, useAgUi } from 'reachat';

function App() {
  const agui = useAgUi({
    agent: 'https://my-agent.example.com/run',
    headers: { Authorization: `Bearer ${token}` },
    onError: err => console.error(err)
  });

  return (
    <Chat
      sessions={agui.sessions}
      activeSessionId={agui.activeSessionId}
      isLoading={agui.isLoading}
      onSelectSession={agui.selectSession}
      onDeleteSession={agui.deleteSession}
      onNewSession={agui.createSession}
      onSendMessage={agui.sendMessage}
      onStopMessage={agui.stopMessage}
    >
      <SessionMessagePanel>
        <SessionMessages />
        <ChatInput />
      </SessionMessagePanel>
    </Chat>
  );
}
```

## Tools and tool calls

Expose tools to the agent and respond when it invokes one:

```tsx
const agui = useAgUi({
  agent: '/api/agent',
  tools: [
    {
      name: 'searchDocs',
      description: 'Search the knowledge base',
      parameters: { query: { type: 'string' } }
    }
  ],
  onToolCall: async toolCall => {
    if (toolCall.toolCallName === 'searchDocs') {
      const args = JSON.parse(toolCall.args);
      const results = await searchKb(args.query);
      // Tool result handling — push back to your agent as needed
      console.log('searchDocs result', results);
    }
  }
});
```

## Streaming behavior

The hook calls `fetch(agent, { method: 'POST', body: JSON.stringify(input) })` and parses the SSE response, dispatching `AgUiEvent`s. It updates the active conversation in-place when `TEXT_MESSAGE_CONTENT` / `TEXT_MESSAGE_CHUNK` deltas arrive, and accumulates `TOOL_CALL_*` events into `AgUiToolCallInfo` before firing `onToolCall` on `TOOL_CALL_END`.

Supported event types include lifecycle (`RUN_STARTED`, `RUN_FINISHED`, `RUN_ERROR`, `STEP_*`), text (`TEXT_MESSAGE_*`), tool calls (`TOOL_CALL_*`), state (`STATE_SNAPSHOT`, `STATE_DELTA`, `MESSAGES_SNAPSHOT`), plus `RAW` and `CUSTOM`.

## Cancellation

`stopMessage()` aborts the in-flight `fetch` via `AbortController`. The hook also auto-aborts on unmount.

## Helpers

These utilities are exported alongside the hook for advanced integrations:

- `addConversationToSession(sessions, sessionId, conversation)` — immutably append
- `updateConversationInSession(sessions, sessionId, conversationId, response)` — patch a conversation's response
- `sessionsToAgUiMessages(session)` — convert reachat history into `AgUiMessage[]`
- `parseSSE(response, signal)` — async generator over `AgUiEvent | Error`
- `parseSSELine(line)` — single-line SSE parser
