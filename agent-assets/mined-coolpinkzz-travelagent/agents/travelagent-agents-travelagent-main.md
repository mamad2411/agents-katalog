# AgentTrip

Conference demo for React Bangalore. An AI travel agent that **builds the interface it needs** instead of only returning text.

## Core rule

The model never generates React, HTML, CSS, or executable code. It can only pick a registered component and supply validated props. React owns rendering. Do not use `streamUI` or RSC generative UI.

## Demo first

The product is a generic travel agent. Spiti is only one demo scenario, triggered by a prompt like “Plan the Spiti trip”. Prefer mock travel data and a deterministic event script. Real flight/hotel APIs, auth, payments, maps, and RAG are out of scope.

Keep Demo mode as the fallback. Live mode uses the Vercel AI SDK and the same event model.

## Architecture to explain on stage

1. User intent
2. Agent chooses a tool
3. Tool returns structured data
4. Agent emits a `ui` event
5. Registry maps that event to a React component
6. Human approval is a first-class waiting state
