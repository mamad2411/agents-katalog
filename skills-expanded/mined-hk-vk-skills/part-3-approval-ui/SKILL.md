---
name: part-3-approval-ui
description: **Cancellation:** `create_run` exposes `controller.is_cancelled` and `controller.cancelled_event`.
If the response stream is closed early (for example user cancel or client disconnect),
these are set so your backend loop can exit cooperatively.
`controller.cancelled_event` is a read-only signal object with `wait()` and `is_set()`.
`create_run` gives callbacks a \~50ms cooperative shutdown window before forced task cancellation.
Callback exceptions that happen during early-close cleanup are not re-raised to the stream consumer,
but are logged with traceback at warning level for debugging.
Put critical cleanup in `finally` blocks, since forced cancellation may happen after the grace window.

```python
async def run_callback(controller: RunController):
    while not controller.is_cancelled:
        # Long-running work / model loop
        await asyncio.sleep(0.05)
```

```python
async def run_callback(controller: RunController):
    await controller.cancelled_event.wait()
    # cancellation-aware shutdown pa...
metadata:
  source: llms.txt
  source_url: https://www.assistant-ui.com/llms-full.txt
  generated: 2026-03-24T19:54:04.964Z
---

# Part 3: Approval UI

> **Cancellation:** `create_run` exposes `controller.is_cancelled` and `controller.cancelled_event`.
If the response stream is closed early (for example user cancel or client disconnect),
these are set so your backend loop can exit cooperatively.
`controller.cancelled_event` is a read-only signal object with `wait()` and `is_set()`.
`create_run` gives callbacks a \~50ms cooperative shutdown window before forced task cancellation.
Callback exceptions that happen during early-close cleanup are not re-raised to the stream consumer,
but are logged with traceback at warning level for debugging.
Put critical cleanup in `finally` blocks, since forced cancellation may happen after the grace window.

```python
async def run_callback(controller: RunController):
    while not controller.is_cancelled:
        # Long-running work / model loop
        await asyncio.sleep(0.05)
```

```python
async def run_callback(controller: RunController):
    await controller.cancelled_event.wait()
    # cancellation-aware shutdown path
```

Backend Reference Implementation \[#backend-reference-implementation]

Full example: [`python/assistant-transport-backend-langgraph`](https://github.com/assistant-ui/assistant-ui/tree/main/python/assistant-transport-backend-langgraph)

Streaming Protocol \[#streaming-protocol]

The assistant-stream state replication protocol allows for streaming updates to an arbitrary JSON object.

Operations \[#operations]

The protocol supports two operations:

`set` \[#set]

Sets a value at a specific path in the JSON object.

`append-text` \[#append-text]

Appends text to an existing string value at a path.

Wire Format \[#wire-format]

The wire format is inspired by [AI SDK's data stream protocol](https://sdk.vercel.ai/docs/ai-sdk-ui/stream-protocol).

**State Update:**

**Error:**

Building a Frontend \[#building-a-frontend]

Now let's set up the frontend. The state converter is the heart of the integration—it transforms your agent's state into the format assistant-ui expects.

The `useAssistantTransportRuntime` hook is used to configure the runtime. It accepts the following config:

State Converter \[#state-converter]

The state converter is the core of your frontend integration. It transforms your agent's state into assistant-ui's message format.

Converting Messages \[#converting-messages]

Use the `createMessageConverter` API to transform your agent's messages to assistant-ui format:

**Reverse mapping:**

The message converter allows you to retrieve the original message format anywhere inside assistant-ui. This lets you access your agent's native message structure from any assistant-ui component:

Optimistic Updates from Commands \[#optimistic-updates-from-commands]

The converter also receives `connectionMetadata` which contains pending commands. Use this to show optimistic updates:

Handling Errors and Cancellations \[#handling-errors-and-cancellations]

The `onError` and `onCancel` callbacks receive an `updateState` function that allows you to update the agent state on the client side without making a server request:

Custom Headers and Body \[#custom-headers-and-body]

You can pass custom headers and body to the backend endpoint:

Dynamic Headers and Body \[#dynamic-headers-and-body]

You can also evaluate the header and body payloads on every request by passing an async function:

Transforming the Request Body \[#transforming-the-request-body]

Use `prepareSendCommandsRequest` to transform the entire request body before it is sent to the backend. This receives the fully assembled body object and returns the (potentially transformed) body.

This is useful for adding tracking IDs, transforming commands, or injecting metadata that depends on the assembled request:

Editing Messages \[#editing-messages]

By default, editing messages is disabled. To enable it, set `capabilities.edit` to `true`:

`add-message` commands always include `parentId` and `sourceId` fields:

Backend Handling \[#backend-handling]

When the backend receives an `add-message` command with a `parentId`, it should:

Resuming from a Sync Server \[#resuming-from-a-sync-server]

When a user refreshes the page, switches tabs, or reconnects after a network interruption, the backend may still be generating a response. `resumeRun` allows the frontend to reconnect to the active backend stream.

Setup \[#setup]

Pass a `resumeApi` URL to `useAssistantTransportRuntime` that points to your sync server:

Resuming on thread switch or page load \[#resuming-on-thread-switch-or-page-load]

When switching to a thread or mounting a component, check if the backend is still running and call `resumeRun`:

For the AssistantTransport runtime, you do not need to pass a `stream` parameter — the runtime uses the configured `resumeApi` endpoint to reconnect.

Accessing Runtime State \[#accessing-runtime-state]

Use the `useAssistantTransportState` hook to access the current agent state from any component:

You can also pass a selector function to extract specific values:

Type Safety \[#type-safety]

Use module augmentation to add types for your agent state:

After adding the type augmentation, `useAssistantTransportState` will be fully typed:

Accessing the Original Message \[#accessing-the-original-message]

If you're using `createMessageConverter`, you can access the original message format from any assistant-ui component using the converter's `toOriginalMessage` method:

You can also use `toOriginalMessages` to get all original messages when a ThreadMessage was created from multiple source messages:

Frontend Reference Implementation \[#frontend-reference-implementation]

Full example: [`examples/with-assistant-transport`](https://github.com/assistant-ui/assistant-ui/tree/main/examples/with-assistant-transport)

Custom Commands \[#custom-commands]

Defining Custom Commands \[#defining-custom-commands]

Use module augmentation to define a custom command:

Issuing Commands \[#issuing-commands]

Use the `useAssistantTransportSendCommand` hook to send custom commands:

Backend Integration \[#backend-integration]

The backend receives custom commands in the `commands` array, just like built-in commands:

Optimistic Updates \[#optimistic-updates]

Update the [state converter](#state-converter) to optimistically handle the custom command:

Cancellation and Error Behavior \[#cancellation-and-error-behavior]

Custom commands follow the same lifecycle as built-in commands. You can update your `onError` and `onCancel` handlers to take custom commands into account:

URL: /docs/runtimes/data-stream

Integration with data stream protocol endpoints for streaming AI responses.

The `@assistant-ui/react-data-stream` package provides integration with data stream protocol endpoints, enabling streaming AI responses with tool support and state management.

Overview \[#overview]

The data stream protocol is a standardized format for streaming AI responses that supports:

Installation \[#installation]

Basic Usage \[#basic-usage]

Advanced Configuration \[#advanced-configuration]

Custom Headers and Authentication \[#custom-headers-and-authentication]

Dynamic Headers \[#dynamic-headers]

Dynamic Body \[#dynamic-body]

Event Callbacks \[#event-callbacks]

Tool Integration \[#tool-integration]

Frontend Tools \[#frontend-tools]

Use `toToolsJSONSchema` to serialize client-side tools:

Backend Tool Processing \[#backend-tool-processing]

Your backend should handle tool calls and return results:

Assistant Cloud Integration \[#assistant-cloud-integration]

For Assistant Cloud deployments, use `useCloudRuntime`:

Message Conversion \[#message-conversion]

Framework-Agnostic Conversion (Recommended) \[#framework-agnostic-conversion-recommended]

For custom integrations, use the framework-agnostic utilities from `assistant-stream`:

The `GenericMessage` format can be easily converted to any LLM provider format:

AI SDK Specific Conversion \[#ai-sdk-specific-conversion]

For AI SDK integration, use `toLanguageModelMessages`:

Error Handling \[#error-handling]

The runtime automatically handles common error scenarios:

Best Practices \[#best-practices]

Performance Optimization \[#performance-optimization]

Error Boundaries \[#error-boundaries]

State Persistence \[#state-persistence]

Examples \[#examples]

Explore our [examples repository](https://github.com/assistant-ui/assistant-ui/tree/main/examples) for implementation references.

LocalRuntimeOptions \[#localruntimeoptions]

`useDataStreamRuntime` accepts all options from `LocalRuntimeOptions` in addition to its own options. These control the underlying local runtime behavior.

`maxSteps` \[#maxsteps]

The maximum number of agentic steps (tool call rounds) allowed per run. Defaults to unlimited.

`initialMessages` \[#initialmessages]

Pre-populate the thread with messages on first render. Useful for continuing an existing conversation.

`adapters` \[#adapters]

Extend the runtime with optional capability adapters. The `chatModel` adapter is handled internally by `useDataStreamRuntime` and cannot be overridden here.

See the [LocalRuntime adapters documentation](/docs/runtimes/custom/local#adapters) for details on implementing each adapter.

`cloud` \[#cloud]

Connect to [Assistant Cloud](/docs/cloud) for managed multi-thread support, persistence, and thread management.

`unstable_humanToolNames` \[#unstable\_humantoolnames]

Names of tools that should pause execution and wait for human or external approval before proceeding.

API Reference \[#api-reference]

For detailed API documentation, see the [`@assistant-ui/react-data-stream` API Reference](/docs/api-reference/integrations/react-data-stream).

URL: /docs/runtimes/helicone

Configure Helicone proxy for OpenAI API logging and monitoring.

Helicone acts as a proxy for your OpenAI API calls, enabling detailed logging and monitoring. To integrate, update your API base URL and add the Helicone-Auth header.

AI SDK by vercel \[#ai-sdk-by-vercel]

LangChain Integration (Python) \[#langchain-integration-python]

Summary \[#summary]

Update your API base URL to `https://oai.helicone.ai/v1` and add the `Helicone-Auth` header with your API key either in your Vercel AI SDK or LangChain configuration.

URL: /docs/runtimes/langserve

Connect to LangServe endpoints via Vercel AI SDK integration.

Overview \[#overview]

Integration with a LangServe server via Vercel AI SDK.

Getting Started \[#getting-started]

URL: /docs/runtimes/pick-a-runtime

Which runtime fits your backend? Decision guide for common setups.

Choosing the right runtime is crucial for your assistant-ui implementation. This guide helps you navigate the options based on your specific needs.

Quick Decision Tree \[#quick-decision-tree]

Core Runtimes \[#core-runtimes]

These are the foundational runtimes that power assistant-ui:

Pre-Built Integrations \[#pre-built-integrations]

For popular frameworks, we provide ready-to-use integrations built on top of our core runtimes:

Understanding Runtime Architecture \[#understanding-runtime-architecture]

How Pre-Built Integrations Work \[#how-pre-built-integrations-work]

The pre-built integrations (AI SDK, LangGraph, etc.) are **not separate runtime types**. They're convenient wrappers built on top of our core runtimes:

This means you get all the benefits of `LocalRuntime` (automatic state management, built-in features) with zero configuration for your specific framework.

When to Use Pre-Built vs Core Runtimes \[#when-to-use-pre-built-vs-core-runtimes]

**Use a pre-built integration when:**

**Use a core runtime when:**

Feature Comparison \[#feature-comparison]

Core Runtime Capabilities \[#core-runtime-capabilities]

Available Adapters \[#available-adapters]

Common Implementation Patterns \[#common-implementation-patterns]

Vercel AI SDK with Streaming \[#vercel-ai-sdk-with-streaming]

Custom Backend with `LocalRuntime` \[#custom-backend-with-localruntime]

Redux Integration with `ExternalStoreRuntime` \[#redux-integration-with-externalstoreruntime]

Examples \[#examples]

Explore our implementation examples:

Common Pitfalls to Avoid \[#common-pitfalls-to-avoid]

LocalRuntime Pitfalls \[#localruntime-pitfalls]

ExternalStoreRuntime Pitfalls \[#externalstoreruntime-pitfalls]

General Pitfalls \[#general-pitfalls]

Next Steps \[#next-steps]

URL: /docs/utilities/heat-graph

Headless, composable activity heatmap components for React.

`heat-graph` provides headless, Radix-style primitives for building GitHub-style activity heatmap graphs.

Installation \[#installation]

Quick Start \[#quick-start]

Anatomy \[#anatomy]

API Reference \[#api-reference]

Root \[#root]

The top-level provider. Renders a `<div>` that computes the grid layout and provides state to all children. Accepts all standard div props.

Grid \[#grid]

A `<div>` with CSS Grid layout. Renders `gridTemplateColumns` and `gridTemplateRows` based on the computed data. Accepts all standard div props.

Iterates over cells internally, calling the children render function for each cell. Each cell is wrapped in a context that `Cell` reads from.

Cell \[#cell]

A `<div>` that reads from cell context. Automatically applies:

Accepts all standard div props. Pass `colorScale` to override the Root-level color scale.

MonthLabels \[#monthlabels]

Iterates over month labels, calling the children render function for each label.

Each label has `{ month: number, column: number }`. Use `totalWeeks` to compute label positions. Use `MONTH_SHORT[label.month]` for English labels, or format with `Intl.DateTimeFormat` for localization.

DayLabels \[#daylabels]

Iterates over day-of-week labels, calling the children render function for each label.

Each label has `{ dayOfWeek: number, row: number }` where `dayOfWeek` is 0=Sun..6=Sat. Use `DAY_SHORT[label.dayOfWeek]` for English labels, or format with `Intl.DateTimeFormat` for localization.

Legend \[#legend]

Iterates over legend levels, calling the children render function for each item. Each item has `{ level: number, color: string | undefined }`.

LegendLevel \[#legendlevel]

A `<div>` that reads from legend item context. Automatically applies `backgroundColor` from the color scale. Use inside `Legend`.

Tooltip \[#tooltip]

Renders only when a cell is hovered. Positioned by Radix Popper relative to the hovered cell. Accepts Radix Popper `Content` props (`side`, `sideOffset`, `align`, etc.).

autoLevels(n) \[#autolevelsn]

Default classification function. Maps counts into `n` evenly-distributed levels (0 to n-1). Level 0 is always count 0.

To provide a custom classifier:

MONTH\_SHORT \[#month\_short]

English month abbreviations array: `["Jan", "Feb", ..., "Dec"]`. Index by `MonthLabel.month`.

DAY\_SHORT \[#day\_short]

English day abbreviations array: `["Sun", "Mon", ..., "Sat"]`. Index by `DayLabel.dayOfWeek`.

URL: /docs/utilities/tw-shimmer

Tailwind CSS v4 plugin for shimmer effects.

`tw-shimmer` is a zero-dependency Tailwind CSS v4 plugin that provides polished shimmer animations for both text and skeleton loaders. It uses sine-eased gradients with 17 carefully calculated stops and OKLCH color mixing for smooth, banding-free effects.

See the [interactive demo](/tw-shimmer) for live examples.

Installation \[#installation]

Add to your CSS:

Quick Start \[#quick-start]

Text Shimmer \[#text-shimmer]

Skeleton Loader \[#skeleton-loader]

Skeleton Card with Auto-Sizing \[#skeleton-card-with-auto-sizing]

API Reference \[#api-reference]

Core Utilities \[#core-utilities]

`shimmer` \[#shimmer]

Base utility for text shimmer. Applies a gradient animation over the text foreground color.

`shimmer-bg` \[#shimmer-bg]

Background shimmer for skeleton loaders. Applies a gradient animation over the element's background. Requires a base `bg-*` class.

`shimmer-container` \[#shimmer-container]

CSS-only auto-sizing helper using container queries. Sets `container-type: inline-size` and automatically derives speed and spread from the container width.

Customization Utilities \[#customization-utilities]

All utilities are **inheritable** — set on a parent to affect all shimmer children.

Speed and Width \[#speed-and-width]

Speed controls how fast the shimmer moves in pixels per second. Width tells the animation how wide the container is for timing calculations.

Color \[#color]

Use any Tailwind color with optional opacity:

Angle \[#angle]

Control the sweep direction. Default is `90deg` (vertical sweep).

Position Hints (Angled Shimmer) \[#position-hints-angled-shimmer]

For angled shimmers, use `shimmer-x-{n}` and `shimmer-y-{n}` to sync elements:

Repeat Delay \[#repeat-delay]

Control the pause between animation cycles:

CSS Variables \[#css-variables]

All values can be set via CSS variables for dynamic control:

Browser Support \[#browser-support]

Uses modern CSS features: `oklch()`, `color-mix()`, independent `translate` transform, and CSS Container Queries.

**Supported:** Chrome 111+, Firefox 113+, Safari 16.4+

Older browsers degrade gracefully — shimmer effects simply won't appear.

URL: /docs/ui/accordion

A vertically stacked set of interactive headings that reveal or hide content sections.

Installation \[#installation]

Usage \[#usage]

Examples \[#examples]

Variants \[#variants]

Use the `variant` prop on `Accordion` to change the visual style. Child components inherit the variant automatically.

Multiple Items Open \[#multiple-items-open]

Use `type="multiple"` to allow multiple items to be open simultaneously.

With Icons \[#with-icons]

Add icons or custom elements inside the trigger.

<PreviewCode file="components/docs/samples/accordion" name="AccordionWithIconsSample">
  <AccordionWithIconsSample />
</PreviewCode>

Controlled \[#controlled]

Use `value` and `onValueChange` for controlled accordion state.

<PreviewCode file="components/docs/samples/accordion" name="AccordionControlledSample">
  <AccordionControlledSample />
</PreviewCode>

FAQ Section \[#faq-section]

A practical example of using accordion for a FAQ section.

<PreviewCode file="components/docs/samples/accordion" name="AccordionFAQSample">
  <AccordionFAQSample />
</PreviewCode>

API Reference \[#api-reference]

Composable API \[#composable-api]

Accordion \[#accordion]

The root component that manages accordion state. Set `variant` here to style all child components.

<ParametersTable
  type="AccordionProps"
  parameters="[
{
name: &#x22;type&#x22;,
type: '&#x22;single&#x22; | &#x22;multiple&#x22;',
required: true,
description: &#x22;Whether only one or multiple items can be open at once.&#x22;,
},
{
name: &#x22;collapsible&#x22;,
type: &#x22;boolean&#x22;,
default: &#x22;false&#x22;,
description: &#x22;When type is 'single', allows closing the open item by clicking it again.&#x22;,
},
{
name: &#x22;defaultValue&#x22;,
type: &#x22;string | string[]&#x22;,
description: &#x22;The default open item(s) (uncontrolled).&#x22;,
},
{
name: &#x22;value&#x22;,
type: &#x22;string | string[]&#x22;,
description: &#x22;The controlled open item(s).&#x22;,
},
{
name: &#x22;onValueChange&#x22;,
type: &#x22;(value: string | string[]) => void&#x22;,
description: &#x22;Callback when the open item(s) change.&#x22;,
},
{
name: &#x22;variant&#x22;,
type: '&#x22;default&#x22; | &#x22;outline&#x22; | &#x22;ghost&#x22;',
default: '&#x22;default&#x22;',
description: &#x22;The visual style of the accordion. Child components inherit this automatically.&#x22;,
},
{
name: &#x22;className&#x22;,
type: &#x22;string&#x22;,
description: &#x22;Additional CSS classes.&#x22;,
},
]"
/>

AccordionItem \[#accordionitem]

A single collapsible section container.

<ParametersTable
  type="AccordionItemProps"
  parameters="[
{
name: &#x22;value&#x22;,
type: &#x22;string&#x22;,
required: true,
description: &#x22;A unique identifier for this item.&#x22;,
},
{
name: &#x22;disabled&#x22;,
type: &#x22;boolean&#x22;,
description: &#x22;Whether the item is disabled.&#x22;,
},
{
name: &#x22;className&#x22;,
type: &#x22;string&#x22;,
description: &#x22;Additional CSS classes.&#x22;,
},
]"
/>

AccordionTrigger \[#accordiontrigger]

The clickable header that toggles content visibility.

<ParametersTable
  type="AccordionTriggerProps"
  parameters="[
{
name: &#x22;className&#x22;,
type: &#x22;string&#x22;,
description: &#x22;Additional CSS classes.&#x22;,
},
]"
/>

AccordionContent \[#accordioncontent]

The collapsible content panel.

<ParametersTable
  type="AccordionContentProps"
  parameters="[
{
name: &#x22;className&#x22;,
type: &#x22;string&#x22;,
description: &#x22;Additional CSS classes.&#x22;,
},
]"
/>

Style Variants (CVA) \[#style-variants-cva]

URL: /docs/ui/assistant-modal

Floating chat bubble for support widgets and help desks.

A floating chat modal built on Radix UI Popover. Ideal for support widgets, help desks, and embedded assistants.

Getting Started \[#getting-started]

Anatomy \[#anatomy]

The `AssistantModal` component is built with the following primitives:

API Reference \[#api-reference]

Root \[#root]

Contains all parts of the modal. Based on Radix UI Popover.

<ParametersTable
  type="AssistantModalPrimitiveRootProps"
  parameters="[
{
name: &#x22;defaultOpen&#x22;,
type: &#x22;boolean&#x22;,
description: &#x22;The initial open state when uncontrolled.&#x22;,
},
{
name: &#x22;open&#x22;,
type: &#x22;boolean&#x22;,
description: &#x22;The controlled open state.&#x22;,
},
{
name: &#x22;onOpenChange&#x22;,
type: &#x22;(open: boolean) => void&#x22;,
description: &#x22;Callback when the open state changes.&#x22;,
},
{
name: &#x22;unstable_openOnRunStart&#x22;,
type: &#x22;boolean&#x22;,
description: &#x22;Automatically open the modal when the assistant starts running.&#x22;,
},
]"
/>

Trigger \[#trigger]

A button that toggles the modal open/closed state.

<ParametersTable
  type="AssistantModalPrimitiveTriggerProps"
  parameters="[
{
name: &#x22;asChild&#x22;,
type: &#x22;boolean&#x22;,
default: &#x22;false&#x22;,
description: &#x22;Merge props with child element instead of rendering a wrapper button.&#x22;,
},
]"
/>

This primitive renders a `<button>` element unless `asChild` is set.

Content \[#content]

The popover content container that holds the chat interface.

<ParametersTable
  type="AssistantModalPrimitiveContentProps"
  parameters="[
{
name: &#x22;side&#x22;,
type: &#x22;'top' | 'right' | 'bottom' | 'left'&#x22;,
default: &#x22;'top'&#x22;,
description: &#x22;The preferred side of the anchor to render against.&#x22;,
},
{
name: &#x22;align&#x22;,
type: &#x22;'start' | 'center' | 'end'&#x22;,
default: &#x22;'end'&#x22;,
description: &#x22;The preferred alignment against the anchor.&#x22;,
},
{
name: &#x22;dissmissOnInteractOutside&#x22;,
type: &#x22;boolean&#x22;,
description: &#x22;Whether to close the modal when clicking outside.&#x22;,
},
{
name: &#x22;asChild&#x22;,
type: &#x22;boolean&#x22;,
default: &#x22;false&#x22;,
description: &#x22;Merge props with child element instead of rendering a wrapper div.&#x22;,
},
]"
/>

Anchor \[#anchor]

An optional anchor element to position the modal relative to.

<ParametersTable
  type="AssistantModalPrimitiveAnchorProps"
  parameters="[
{
name: &#x22;asChild&#x22;,
type: &#x22;boolean&#x22;,
default: &#x22;false&#x22;,
description: &#x22;Merge props with child element instead of rendering a wrapper div.&#x22;,
},
]"
/>

Related Components \[#related-components]

URL: /docs/ui/assistant-sidebar

Side panel chat for co-pilot experiences and inline assistance.

A resizable side panel layout with your main content on the left and a Thread chat interface on the right. Ideal for co-pilot experiences and inline assistance.

Getting Started \[#getting-started]

API Reference \[#api-reference]

AssistantSidebar \[#assistantsidebar]

A layout component that creates a resizable two-panel interface.

<ParametersTable
  type="AssistantSidebarProps"
  parameters="[
{
name: &#x22;children&#x22;,
type: &#x22;ReactNode&#x22;,
description: &#x22;Content to display in the left panel (your main application).&#x22;,
},
]"
/>

The component uses `ResizablePanelGroup` from shadcn/ui internally, creating:

Customization \[#customization]

Since this component is copied to your project at `/components/assistant-ui/assistant-sidebar.tsx`, you can customize:

Related Components \[#related-components]

URL: /docs/ui/attachment

UI components for attaching and viewing files in messages.

Getting Started \[#getting-started]

API Reference \[#api-reference]

Composer Attachments \[#composer-attachments]

ComposerPrimitive.Attachments \[#composerprimitiveattachments]

Renders all attachments in the composer.

<ParametersTable
  type="ComposerPrimitiveAttachmentsProps"
  parameters="[
{
name: &#x22;components&#x22;,
type: &#x22;AttachmentComponents&#x22;,
description: &#x22;Components to render for different attachment types.&#x22;,
children: [
{
type: &#x22;AttachmentComponents&#x22;,
parameters: [
{
name: &#x22;Image&#x22;,
type: &#x22;ComponentType&#x22;,
description: &#x22;Component for image attachments.&#x22;,
},
{
name: &#x22;Document&#x22;,
type: &#x22;ComponentType&#x22;,
description: &#x22;Component for document attachments (PDF, etc.).&#x22;,
},
{
name: &#x22;File&#x22;,
type: &#x22;ComponentType&#x22;,
description: &#x22;Component for generic file attachments.&#x22;,
},
{
name: &#x22;Attachment&#x22;,
type: &#x22;ComponentType&#x22;,
description: &#x22;Fallback component for all attachment types.&#x22;,
},
],
},
],
},
]"
/>

ComposerPrimitive.AddAttachment \[#composerprimitiveaddattachment]

A button that opens the file picker to add attachments.

<ParametersTable
  type="ComposerPrimitiveAddAttachmentProps"
  parameters="[
{
name: &#x22;multiple&#x22;,
type: &#x22;boolean&#x22;,
default: &#x22;true&#x22;,
description: &#x22;Allow selecting multiple files at once.&#x22;,
},
{
name: &#x22;asChild&#x22;,
type: &#x22;boolean&#x22;,
default: &#x22;false&#x22;,
description: &#x22;Merge props with child element instead of rendering a wrapper button.&#x22;,
},
]"
/>

This primitive renders a `<button>` element unless `asChild` is set.

Message Attachments \[#message-attachments]

MessagePrimitive.Attachments \[#messageprimitiveattachments]

Renders all attachments in a user message.

<ParametersTable
  type="MessagePrimitiveAttachmentsProps"
  parameters="[
{
name: &#x22;components&#x22;,
type: &#x22;AttachmentComponents&#x22;,
description: &#x22;Components to render for different attachment types (same as ComposerPrimitive.Attachments).&#x22;,
},
]"
/>

Attachment Primitives \[#attachment-primitives]

AttachmentPrimitive.Root \[#attachmentprimitiveroot]

Container for a single attachment.

<ParametersTable
  type="AttachmentPrimitiveRootProps"
  parameters="[
{
name: &#x22;asChild&#x22;,
type: &#x22;boolean&#x22;,
default: &#x22;false&#x22;,
description: &#x22;Merge props with child element instead of rendering a wrapper div.&#x22;,
},
]"
/>

AttachmentPrimitive.Name \[#attachmentprimitivename]

Renders the attachment's file name.

AttachmentPrimitive.Remove \[#attachmentprimitiveremove]

A button to remove the attachment from the composer.

<ParametersTable
  type="AttachmentPrimitiveRemoveProps"
  parameters="[
{
name: &#x22;asChild&#x22;,
type: &#x22;boolean&#x22;,
default: &#x22;false&#x22;,
description: &#x22;Merge props with child element instead of rendering a wrapper button.&#x22;,
},
]"
/>

Attachment Types \[#attachment-types]

Attachments have the following structure:

The `type` field accepts custom strings (e.g. `"data-workflow"`) beyond the built-in types. When an unknown type is encountered, the generic `Attachment` component is used as a fallback. The `contentType` field is optional — it can be omitted for non-file attachments where a MIME type is not meaningful.

Related Components \[#related-components]

URL: /docs/ui/badge

A small label component for displaying status, categories, or metadata.

Installation \[#installation]

Usage \[#usage]

Examples \[#examples]

Variants \[#variants]

Use the `variant` prop to change the visual style.

Sizes \[#sizes]

Use the `size` prop to change the badge size.

With Icons \[#with-icons]

Badges automatically style SVG icons.

<PreviewCode file="components/docs/samples/badge" name="BadgeWithIconSample">
  <BadgeWithIconSample />
</PreviewCode>

As Link \[#as-link]

Use the `asChild` prop to render the badge as a different element, like a link.

<PreviewCode file="components/docs/samples/badge" name="BadgeAsLinkSample">
  <BadgeAsLinkSample />
</PreviewCode>

Animated \[#animated]

Combine with CSS transitions for scroll and color animations.

<PreviewCode file="components/docs/samples/badge" name="BadgeAnimatedSample">
  <BadgeAnimatedSample />
</PreviewCode>

API Reference \[#api-reference]

Badge \[#badge]

<ParametersTable
  type="BadgeProps"
  parameters="[
{
name: &#x22;variant&#x22;,
type: '&#x22;outline&#x22; | &#x22;secondary&#x22; | &#x22;muted&#x22; | &#x22;ghost&#x22; | &#x22;info&#x22; | &#x22;warning&#x22; | &#x22;success&#x22; | &#x22;destructive&#x22;',
default: '&#x22;outline&#x22;',
description: &#x22;The visual style of the badge.&#x22;,
},
{
name: &#x22;size&#x22;,
type: '&#x22;sm&#x22; | &#x22;default&#x22; | &#x22;lg&#x22;',
default: '&#x22;default&#x22;',
description: &#x22;The size of the badge.&#x22;,
},
{
name: &#x22;asChild&#x22;,
type: &#x22;boolean&#x22;,
default: &#x22;false&#x22;,
description: &#x22;Merge props with child element instead of rendering a span.&#x22;,
},
{
name: &#x22;className&#x22;,
type: &#x22;string&#x22;,
description: &#x22;Additional CSS classes.&#x22;,
},
]"
/>

Style Variants (CVA) \[#style-variants-cva]

URL: /docs/ui/context-display

Visualize token usage relative to a model's context window — ring, bar, or text — with a detailed hover popover.

Getting Started \[#getting-started]

Variants \[#variants]

Three preset variants are available, each wrapping the shared tooltip popover:

All presets accept `className` for styling overrides and `side` to control tooltip placement (`"top"`, `"bottom"`, `"left"`, `"right"`).

Composable API \[#composable-api]

For custom visualizations, use the building blocks directly:

API Reference \[#api-reference]

Preset Props \[#preset-props]

All preset variants (`Ring`, `Bar`, `Text`) share the same props:

Color Thresholds \[#color-thresholds]

Ring and Bar share the same severity colors:

Text displays numeric values only — no severity color.

Related \[#related]

URL: /docs/ui/diff-viewer

Render code diffs with syntax highlighting for additions and deletions.

Installation \[#installation]

Usage \[#usage]

As Markdown Language Override \[#as-markdown-language-override]

Integrate with `MarkdownTextPrimitive` to render diff code blocks:

Examples \[#examples]

Unified View \[#unified-view]

Shows all changes in a single column with `+`/`-` indicators. This is the default mode.

Split View \[#split-view]

Shows old content on the left, new content on the right side-by-side.

Interactive Mode Toggle \[#interactive-mode-toggle]

<PreviewCode file="components/docs/samples/diff-viewer" name="DiffViewerViewModesSample">
  <DiffViewerViewModesSample />
</PreviewCode>

Variants \[#variants]

Sizes \[#sizes]

Theming \[#theming]

DiffViewer uses CSS variables for colors. Override them in your CSS:

API Reference \[#api-reference]

DiffViewer \[#diffviewer]

The main component for rendering diffs.

<ParametersTable
  type="DiffViewerProps"
  parameters="[
{
name: &#x22;patch&#x22;,
type: &#x22;string&#x22;,
description: &#x22;Unified diff string (e.g., output from git diff).&#x22;,
},
{
name: &#x22;code&#x22;,
type: &#x22;string&#x22;,
description: &#x22;Alias for patch (for markdown integration).&#x22;,
},
{
name: &#x22;oldFile&#x22;,
type: &#x22;{ content: string; name?: string }&#x22;,
description: &#x22;Old file for direct comparison.&#x22;,
},
{
name: &#x22;newFile&#x22;,
type: &#x22;{ content: string; name?: string }&#x22;,
description: &#x22;New file for direct comparison.&#x22;,
},
{
name: &#x22;viewMode&#x22;,
type: '&#x22;unified&#x22; | &#x22;split&#x22;',
default: '&#x22;unified&#x22;',
description: &#x22;Display mode for the diff.&#x22;,
},
{
name: &#x22;variant&#x22;,
type: '&#x22;default&#x22; | &#x22;ghost&#x22; | &#x22;muted&#x22;',
default: '&#x22;default&#x22;',
description: &#x22;Visual style variant.&#x22;,
},
{
name: &#x22;size&#x22;,
type: '&#x22;sm&#x22; | &#x22;default&#x22; | &#x22;lg&#x22;',
default: '&#x22;default&#x22;',
description: &#x22;Font size.&#x22;,
},
{
name: &#x22;showLineNumbers&#x22;,
type: &#x22;boolean&#x22;,
default: &#x22;true&#x22;,
description: &#x22;Show line numbers.&#x22;,
},
{
name: &#x22;showIcon&#x22;,
type: &#x22;boolean&#x22;,
default: &#x22;true&#x22;,
description: &#x22;Show file extension badge in header.&#x22;,
},
{
name: &#x22;showStats&#x22;,
type: &#x22;boolean&#x22;,
default: &#x22;true&#x22;,
description: &#x22;Show addition/deletion counts in header.&#x22;,
},
{
name: &#x22;className&#x22;,
type: &#x22;string&#x22;,
description: &#x22;Additional CSS classes.&#x22;,
},
]"
/>

Composable API \[#composable-api]

Style Variants (CVA) \[#style-variants-cva]

Utilities \[#utilities]

Styling \[#styling]

Data Attributes \[#data-attributes]

Use data attributes for custom styling:

Custom CSS Example \[#custom-css-example]

Related Components \[#related-components]

URL: /docs/ui/file

Display file message parts with icon, name, size, and download button.

Getting Started \[#getting-started]

Variants \[#variants]

Use the `variant` prop to change the visual style.

Sizes \[#sizes]

Use the `size` prop to change padding and font size.

MimeType Icons \[#mimetype-icons]

The component automatically selects an appropriate icon based on the file's MIME type:

API Reference \[#api-reference]

Composable API \[#composable-api]

The component exports composable sub-components:

Custom Icon \[#custom-icon]

Pass `children` to `File.Icon` to override the default MIME type icon:

Utilities \[#utilities]

The component also exports utility functions:

Related Components \[#related-components]

URL: /docs/ui/image

Display image message parts with preview, loading states, and fullscreen dialog.

Getting Started \[#getting-started]

Variants \[#variants]

Use the `variant` prop to change the visual style.

Sizes \[#sizes]

Use the `size` prop to control the maximum width.

API Reference \[#api-reference]

Composable API \[#composable-api]

The component exports composable sub-components:

Related Components \[#related-components]

URL: /docs/ui/markdown

Display rich text with headings, lists, links, and code blocks.

Enabling markdown support \[#enabling-markdown-support]

Syntax highlighting \[#syntax-highlighting]

Syntax Highlighting is not included by default, see [Syntax Highlighting](/docs/ui/syntax-highlighting) to learn how to add it.

Related Components \[#related-components]

URL: /docs/ui/mention

Let users @-mention tools in the composer with a keyboard-navigable popover picker and inline chips.

Getting Started \[#getting-started]

With Lexical Rich Editor \[#with-lexical-rich-editor]

For inline mention chips in the composer (not just the popover), use `LexicalComposerInput` from `@assistant-ui/react-lexical`:

Replace `ComposerPrimitive.Input` with `LexicalComposerInput`:

`LexicalComposerInput` auto-wires to `MentionContext` — no extra props needed. Selected mentions appear as inline chips that are treated as atomic units (select, delete, undo as a whole).

Custom Formatter \[#custom-formatter]

The default directive format is `:type[label]{name=id}`. To use a custom format, pass a `formatter` to both the mention root and the message renderer:

Keyboard Navigation \[#keyboard-navigation]

The mention popover supports full keyboard navigation out of the box:

Components \[#components]

`ComposerMentionPopover.Root` \[#composermentionpopoverroot]

Wraps the composer with mention context and a tool mention adapter. Provides the `@`-trigger detection, keyboard navigation, and popover state.

`ComposerMentionPopover` \[#composermentionpopover]

Pre-built popover containing categories and items lists. Only renders when the `@` trigger is active.

`DirectiveText` \[#directivetext]

A `TextMessagePartComponent` that parses `:type[label]{name=id}` directives and renders them as styled inline chips.

`createDirectiveText(formatter)` \[#createdirectivetextformatter]

Factory function that creates a `TextMessagePartComponent` using a custom `Unstable_DirectiveFormatter`.

URL: /docs/ui/mermaid

Render Mermaid diagrams in chat messages with streaming support.

Getting Started \[#getting-started]

Configuration \[#configuration]

Configure mermaid options in `mermaid-diagram.tsx`:

Streaming Performance \[#streaming-performance]

The `MermaidDiagram` component is optimized for streaming scenarios:

Supported Diagram Types \[#supported-diagram-types]

Mermaid supports various diagram types including:

See the [Mermaid documentation](https://mermaid.js.org/) for complete syntax reference.

Related Components \[#related-components]

URL: /docs/ui/message-timing

Display streaming performance stats — TTFT, total time, tok/s, and chunk count — as a badge with hover popover.

Getting Started \[#getting-started]

What It Shows \[#what-it-shows]

The badge displays `totalStreamTime` inline and reveals a popover on hover with the full breakdown:

Accuracy \[#accuracy]

Timing accuracy depends on how your backend is connected.

assistant-stream (accurate) \[#assistant-stream-accurate]

When using `assistant-stream` on the backend, token counts come directly from the model's usage data sent in `step-finish` chunks. The `tokensPerSecond` metric is exact whenever your backend reports `outputTokens`.

Vercel AI SDK (estimated) \[#vercel-ai-sdk-estimated]

When using the AI SDK integration (`useChatRuntime`), token counts are **estimated** client-side using a 4 characters per token approximation. This can overcount significantly for short messages.

API Reference \[#api-reference]

`MessageTiming` component \[#messagetiming-component]

Renders `null` until `totalStreamTime` is available (i.e., while streaming or for user messages).

For the underlying `useMessageTiming()` hook, field definitions, and runtime-specific setup (LocalRuntime, ExternalStore, etc.), see the [Message Timing guide](/docs/guides/message-timing).

Related \[#related]

URL: /docs/ui/model-selector

Model picker with unified overlay positioning and runtime integration.

A select component that lets users switch between AI models. Uses item-aligned positioning so the selected model overlays the trigger for a unified look. Integrates with assistant-ui's `ModelContext` system to automatically propagate the selected model to your backend.

Getting Started \[#getting-started]

Variants \[#variants]

Use the `variant` prop to change the trigger's visual style.

Sizes \[#sizes]

Use the `size` prop to control the trigger dimensions.

Model Options \[#model-options]

Each model in the `models` array supports:

Runtime Integration \[#runtime-integration]

The default `ModelSelector` export automatically registers the selected model with assistant-ui's `ModelContext` system. When a user selects a model:

This works out of the box with `@assistant-ui/react-ai-sdk`.

API Reference \[#api-reference]

Composable API \[#composable-api]

For custom layouts, use the sub-components directly with `ModelSelector.Root`:

ModelSelector \[#modelselector]

<ParametersTable
  type="ModelSelectorProps"
  parameters="[
{
name: &#x22;models&#x22;,
type: &#x22;ModelOption[]&#x22;,
required: true,
description: &#x22;Array of available models to display.&#x22;,
},
{
name: &#x22;defaultValue&#x22;,
type: &#x22;string&#x22;,
description: &#x22;Initial model ID for uncontrolled usage.&#x22;,
},
{
name: &#x22;value&#x22;,
type: &#x22;string&#x22;,
description: &#x22;Controlled selected model ID.&#x22;,
},
{
name: &#x22;onValueChange&#x22;,
type: &#x22;(value: string) => void&#x22;,
description: &#x22;Callback when selected model changes.&#x22;,
},
{
name: &#x22;variant&#x22;,
type: '&#x22;outline&#x22; | &#x22;ghost&#x22; | &#x22;muted&#x22;',
default: '&#x22;outline&#x22;',
description: &#x22;Visual style of the trigger button.&#x22;,
},
{
name: &#x22;size&#x22;,
type: '&#x22;sm&#x22; | &#x22;default&#x22; | &#x22;lg&#x22;',
default: '&#x22;default&#x22;',
description: &#x22;Size of the trigger button.&#x22;,
},
{
name: &#x22;contentClassName&#x22;,
type: &#x22;string&#x22;,
description: &#x22;Additional class name for the dropdown content.&#x22;,
},
]"
/>

ModelOption \[#modeloption]

<ParametersTable
  type="ModelOption"
  parameters="[
{
name: &#x22;id&#x22;,
type: &#x22;string&#x22;,
required: true,
description: &#x22;Unique identifier sent to the backend as modelName.&#x22;,
},
{
name: &#x22;name&#x22;,
type: &#x22;string&#x22;,
required: true,
description: &#x22;Display name shown in trigger and dropdown.&#x22;,
},
{
name: &#x22;description&#x22;,
type: &#x22;string&#x22;,
description: &#x22;Optional subtitle shown below the model name.&#x22;,
},
{
name: &#x22;icon&#x22;,
type: &#x22;React.ReactNode&#x22;,
description: &#x22;Optional icon displayed before the model name.&#x22;,
},
]"
/>

URL: /docs/ui/part-grouping

Organize message parts into custom groups with flexible grouping functions.

Basic Usage \[#basic-usage]

Use the `MessagePrimitive.Unstable_PartsGrouped` component with a custom grouping function:

How Grouping Works \[#how-grouping-works]

The grouping function receives all message parts and returns an array of groups. Each group contains:

Use Cases & Examples \[#use-cases--examples]

Group by Parent ID \[#group-by-parent-id]

Group related content together using a parent-child relationship:

Group by Tool Name \[#group-by-tool-name]

Organize tool calls by their type:

Group Consecutive Text Parts \[#group-consecutive-text-parts]

Combine multiple text parts into cohesive blocks:

Group by Content Type \[#group-by-content-type]

Separate different types of content for distinct visual treatment:

Group by Custom Metadata \[#group-by-custom-metadata]

Use any custom metadata in your parts for grouping:

Integration with Assistant Streams \[#integration-with-assistant-streams]

When using assistant-stream libraries, you can add custom metadata to parts:

Python (assistant-stream) \[#python-assistant-stream]

TypeScript (assistant-stream) \[#typescript-assistant-stream]

API Reference \[#api-reference]

MessagePrimitive.Unstable\_PartsGrouped \[#messageprimitiveunstable\_partsgrouped]

<ParametersTable
  type="MessagePrimitiveUnstable_PartsGroupedProps"
  parameters="[
{
name: &#x22;groupingFunction&#x22;,
type: &#x22;(parts: readonly any[]) => MessagePartGroup[]&#x22;,
description:
&#x22;Function that takes an array of message parts and returns an array of groups. Each group contains a groupKey (for identification) and an array of indices.&#x22;,
required: true,
},
{
name: &#x22;components&#x22;,
type: &#x22;object&#x22;,
description:
&#x22;Component configuration for rendering different types of message content and groups.&#x22;,
children: [
{
type: &#x22;Components&#x22;,
parameters: [
{
name: &#x22;Empty&#x22;,
type: &#x22;EmptyMessagePartComponent&#x22;,
description: &#x22;Component for rendering empty messages&#x22;,
},
{
name: &#x22;Text&#x22;,
type: &#x22;TextMessagePartComponent&#x22;,
description: &#x22;Component for rendering text content&#x22;,
},
{
name: &#x22;Reasoning&#x22;,
type: &#x22;ReasoningMessagePartComponent&#x22;,
description:
&#x22;Component for rendering reasoning content (typically hidden)&#x22;,
},
{
name: &#x22;Source&#x22;,
type: &#x22;SourceMessagePartComponent&#x22;,
description: &#x22;Component for rendering source content&#x22;,
},
{
name: &#x22;Image&#x22;,
type: &#x22;ImageMessagePartComponent&#x22;,
description: &#x22;Component for rendering image content&#x22;,
},
{
name: &#x22;File&#x22;,
type: &#x22;FileMessagePartComponent&#x22;,
description: &#x22;Component for rendering file content&#x22;,
},
{
name: &#x22;Unstable_Audio&#x22;,
type: &#x22;Unstable_AudioMessagePartComponent&#x22;,
description:
&#x22;Component for rendering audio content (experimental)&#x22;,
},
{
name: &#x22;tools&#x22;,
type: &#x22;object | { Override: ComponentType }&#x22;,
description:
&#x22;Configuration for tool call rendering. Can be an object with by_name map and Fallback component, or an Override component.&#x22;,
},
{
name: &#x22;Group&#x22;,
type: &#x22;ComponentType<PropsWithChildren<{ groupKey: string | undefined; indices: number[] }>>&#x22;,
description:
&#x22;Component for rendering grouped message parts. Receives groupKey, indices array, and children to render.&#x22;,
},
],
},
],
},
]"
/>

MessagePartGroup Type \[#messagepartgroup-type]

Group Component Props \[#group-component-props]

The `Group` component receives:

Best Practices \[#best-practices]

Common Patterns \[#common-patterns]

Conditional Grouping \[#conditional-grouping]

Only group when certain conditions are met:

Nested Grouping \[#nested-grouping]

Create hierarchical groups:

Dynamic Group Rendering \[#dynamic-group-rendering]

Adjust group appearance based on content:

URL: /docs/ui/quote

Let users select and quote text from messages with a floating toolbar, composer preview, and inline quote display.

Getting Started \[#getting-started]

Customization \[#customization]

All three components expose sub-components for full control over styling:

API Reference \[#api-reference]

`QuoteBlock` \[#quoteblock]

Renders quoted text in user messages. Pass to `MessagePrimitive.Parts` as `components.Quote`.

**Sub-components:** `QuoteBlock.Root`, `QuoteBlock.Icon`, `QuoteBlock.Text`

`SelectionToolbar` \[#selectiontoolbar]

Floating toolbar that appears when text is selected within a message. Renders as a portal positioned above the selection.

**Sub-components:** `SelectionToolbar.Root`, `SelectionToolbar.Quote`

`ComposerQuotePreview` \[#composerquotepreview]

Quote preview inside the composer. Only renders when a quote is set.

**Sub-components:** `ComposerQuotePreview.Root`, `ComposerQuotePreview.Icon`, `ComposerQuotePreview.Text`, `ComposerQuotePreview.Dismiss`

`injectQuoteContext` \[#injectquotecontext]

Extracts `metadata.custom.quote` from each message and prepends the quoted text as a `> blockquote` text part. Use before `convertToModelMessages` in your route handler. For alternative backend approaches, see the [Quoting guide](/docs/guides/quoting#backend-handling).

`useMessageQuote` \[#usemessagequote]

Returns the quote attached to the current message, or `undefined`. Useful for building custom quote displays without `QuoteBlock`. For a usage example, see the [Quoting guide](/docs/guides/quoting#reading-quote-data).

`ComposerRuntime.setQuote` \[#composerruntimesetquote]

Set or clear the quote on the composer programmatically. The quote is automatically cleared when the message is sent. For a usage example, see the [Quoting guide](/docs/guides/quoting#programmatic-api).

Related \[#related]

URL: /docs/ui/reasoning

Collapsible UI for displaying AI reasoning and thinking messages.

Getting Started \[#getting-started]

How It Works \[#how-it-works]

The component consists of two parts:

Consecutive reasoning parts are automatically grouped together by the `ReasoningGroup` component.

Variants \[#variants]

Use the `variant` prop on `Reasoning.Root` to change the visual style:

ReasoningGroup \[#reasoninggroup]

`ReasoningGroup` wraps consecutive reasoning parts in a collapsible container. It auto-expands during streaming.

API Reference \[#api-reference]

Composable API \[#composable-api]

All sub-components are exported for custom layouts:

Related Components \[#related-components]

URL: /docs/ui/scrollbar

Replace the default scrollbar with a custom Radix UI scroll area.

If you want to show a custom scrollbar UI of the `ThreadPrimitive.Viewport` in place of the system default, you can integrate `radix-ui`'s Scroll Area.
An example implementation of this is [shadcn/ui's Scroll Area](https://ui.shadcn.com/docs/components/scroll-area).

Related Components \[#related-components]

URL: /docs/ui/select

A dropdown select component with composable sub-components.

Installation \[#installation]

Usage \[#usage]

Examples \[#examples]

Variants \[#variants]

Use the `variant` prop on `SelectTrigger` to change the visual style.

Sizes \[#sizes]

Use the `size` prop on `SelectTrigger` to change the height.

Scrollable \[#scrollable]

Long lists automatically become scrollable.

<PreviewCode file="components/docs/samples/select" name="SelectScrollableSample">
  <SelectScrollableSample />
</PreviewCode>

Groups \[#groups]

Use the composable API for grouped options:

<PreviewCode file="components/docs/samples/select" name="SelectGroupsSample">
  <SelectGroupsSample />
</PreviewCode>

Disabled Items \[#disabled-items]

<PreviewCode file="components/docs/samples/select" name="SelectDisabledItemsSample">
  <SelectDisabledItemsSample />
</PreviewCode>

With Placeholder \[#with-placeholder]

<PreviewCode file="components/docs/samples/select" name="SelectPlaceholderSample">
  <SelectPlaceholderSample />
</PreviewCode>

Disabled Select \[#disabled-select]

<PreviewCode file="components/docs/samples/select" name="SelectDisabledSample">
  <SelectDisabledSample />
</PreviewCode>

API Reference \[#api-reference]

Composable API \[#composable-api]

Select \[#select]

A convenience component that renders a complete select with options.

<ParametersTable
  type="SelectProps"
  parameters="[
{
name: &#x22;value&#x22;,
type: &#x22;string&#x22;,
required: true,
description: &#x22;The controlled value of the select.&#x22;,
},
{
name: &#x22;onValueChange&#x22;,
type: &#x22;(value: string) => void&#x22;,
required: true,
description: &#x22;Callback when the selected value changes.&#x22;,
},
{
name: &#x22;options&#x22;,
type: &#x22;SelectOption[]&#x22;,
required: true,
description: &#x22;Array of options to display.&#x22;,
},
{
name: &#x22;placeholder&#x22;,
type: &#x22;string&#x22;,
description: &#x22;Placeholder text when no value is selected.&#x22;,
},
{
name: &#x22;className&#x22;,
type: &#x22;string&#x22;,
description: &#x22;Additional CSS classes for the trigger.&#x22;,
},
{
name: &#x22;disabled&#x22;,
type: &#x22;boolean&#x22;,
description: &#x22;Whether the select is disabled.&#x22;,
},
]"
/>

SelectOption \[#selectoption]

<ParametersTable
  type="SelectOption"
  parameters="[
{
name: &#x22;value&#x22;,
type: &#x22;string&#x22;,
required: true,
description: &#x22;The value of the option.&#x22;,
},
{
name: &#x22;label&#x22;,
type: &#x22;ReactNode&#x22;,
required: true,
description: &#x22;The display label for the option.&#x22;,
},
{
name: &#x22;textValue&#x22;,
type: &#x22;string&#x22;,
description: &#x22;Optional text value for typeahead. Defaults to label if it's a string.&#x22;,
},
{
name: &#x22;disabled&#x22;,
type: &#x22;boolean&#x22;,
description: &#x22;Whether the option is disabled.&#x22;,
},
]"
/>

SelectTrigger \[#selecttrigger]

The button that opens the dropdown.

<ParametersTable
  type="SelectTriggerProps"
  parameters="[
{
name: &#x22;variant&#x22;,
type: '&#x22;outline&#x22; | &#x22;ghost&#x22; | &#x22;muted&#x22;',
default: '&#x22;outline&#x22;',
description: &#x22;The visual style of the trigger.&#x22;,
},
{
name: &#x22;size&#x22;,
type: '&#x22;sm&#x22; | &#x22;default&#x22; | &#x22;lg&#x22;',
default: '&#x22;default&#x22;',
description: &#x22;The size of the trigger.&#x22;,
},
{
name: &#x22;className&#x22;,
type: &#x22;string&#x22;,
description: &#x22;Additional CSS classes.&#x22;,
},
]"
/>

Style Variants (CVA) \[#style-variants-cva]

URL: /docs/ui/sources

Display URL sources with favicon, title, and external link.

Getting Started \[#getting-started]

Variants \[#variants]

Use the `variant` prop to change the visual style. The default is `outline`.

Sizes \[#sizes]

Use the `size` prop to change the size.

API Reference \[#api-reference]

`Sources` \[#sources]

The default export used as a `SourceMessagePartComponent`. Renders a single source part when `sourceType === "url"`. Also exposes compound sub-components for custom layouts.

Compound sub-components \[#compound-sub-components]

`Source` \[#source]

Root container rendered as an `<a>` tag. Accepts all `<a>` props plus `variant` and `size`.

`SourceIcon` \[#sourceicon]

Displays the favicon for the given URL. Falls back to the domain initial inside a muted box when the favicon fails to load.

`SourceTitle` \[#sourcetitle]

Truncated title text rendered as a `<span>`.

`sourceVariants` \[#sourcevariants]

The underlying CVA variant function used to generate badge class names. Use this when building custom source-like components that need to match the built-in styling.

Composable API \[#composable-api]

Use the named exports to build fully custom source layouts:

Related Components \[#related-components]

URL: /docs/ui/streamdown

Alternative markdown renderer with built-in syntax highlighting, math, and diagram support.

Installation \[#installation]

For additional features, install the optional plugins:

Basic Usage \[#basic-usage]

With Plugins (Recommended) \[#with-plugins-recommended]

When `@streamdown/code` is provided, the default theme is `["github-light", "github-dark"]` for light/dark mode support.

Migration from react-markdown \[#migration-from-react-markdown]

If you're migrating from `@assistant-ui/react-markdown`, your existing `SyntaxHighlighter` and `CodeHeader` components still work:

Props \[#props]

Plugin Configuration \[#plugin-configuration]

Code Highlighting \[#code-highlighting]

Math (LaTeX) \[#math-latex]

Mermaid Diagrams \[#mermaid-diagrams]

CJK Text Optimization \[#cjk-text-optimization]

Advanced Configuration \[#advanced-configuration]

Mermaid Options \[#mermaid-options]

Customize Mermaid diagram rendering with configuration and error handling:

Streaming Caret \[#streaming-caret]

Display a caret indicator during streaming:

Link Safety \[#link-safety]

Show confirmation before opening external links:

Incomplete Markdown Handling (Remend) \[#incomplete-markdown-handling-remend]

Configure how incomplete markdown syntax is handled during streaming:

Allowed HTML Tags \[#allowed-html-tags]

Allow specific HTML tags in markdown content:

Security Configuration \[#security-configuration]

Restrict allowed URLs for links and images. This overrides streamdown's default allow-all policy:

Detecting Inline vs Block Code \[#detecting-inline-vs-block-code]

When building custom code components, you can use `useIsStreamdownCodeBlock` to detect whether you're inside a code block or inline code:

You can also use `useStreamdownPreProps` to access the props passed to the parent `<pre>` element:

Comparison with react-markdown \[#comparison-with-react-markdown]

Re-exported Utilities \[#re-exported-utilities]

The package re-exports useful utilities:

Available Types \[#available-types]

Related Components \[#related-components]

URL: /docs/ui/syntax-highlighting

Code block syntax highlighting with react-shiki or react-syntax-highlighter.

react-shiki \[#react-shiki]

Options \[#options]

See [react-shiki documentation](https://github.com/AVGVSTVS96/react-shiki#props) for all available options.

Key options:

Dual/multi theme support \[#dualmulti-theme-support]

To use multiple themes, pass a theme object:

With `defaultColor="light-dark()"`, theme switching is automatic based on your site's `color-scheme`.
No custom Shiki CSS overrides are required.

Set `color-scheme` on your app root:

System-based (follows OS/browser preference):

Class-based theme switching:

If you need broader support for older browsers, you can still use the manual CSS-variable switching approach from the Shiki dual-theme docs.

For more information:

Bundle Optimization \[#bundle-optimization]

By default, `react-shiki` includes the full Shiki bundle, which contains all supported languages and themes.

To reduce bundle size, you can use the web bundle by changing the import to `react-shiki/web`, to include a smaller bundle of web related languages:

Custom Bundles \[#custom-bundles]

For strict bundle size control, `react-shiki` also supports custom bundles created using `createHighlighterCore` from `react-shiki/core` (re-exported from Shiki):

react-syntax-highlighter \[#react-syntax-highlighter]

Options \[#options-1]

Supports all options from [`react-syntax-highlighter`](https://github.com/react-syntax-highlighter/react-syntax-highlighter#props).

Bundle Optimization \[#bundle-optimization-1]

By default, the syntax highlighter uses a light build that only includes languages you register. To include all languages:

Related Components \[#related-components]

URL: /docs/ui/tabs

A multi-variant tabs component for organizing content into switchable panels.

Installation \[#installation]

Usage \[#usage]

Examples \[#examples]

Variants \[#variants]

Use the `variant` prop on `TabsList` to change the visual style. Child components inherit the variant automatically.

Sizes \[#sizes]

Use the `size` prop on `TabsList` to change the tab height. Child components inherit the size automatically.

With Icons \[#with-icons]

Tabs automatically style SVG icons placed inside triggers.

<PreviewCode file="components/docs/samples/tabs" name="TabsWithIconsSample">
  <TabsWithIconsSample />
</PreviewCode>

Controlled \[#controlled]

Use `value` and `onValueChange` for controlled tab state.

<PreviewCode file="components/docs/samples/tabs" name="TabsControlledSample">
  <TabsControlledSample />
</PreviewCode>

As Link \[#as-link]

Use the `asChild` prop on `TabsTrigger` to render as a different element, like a navigation link.

<PreviewCode file="components/docs/samples/tabs" name="TabsAsLinkSample">
  <TabsAsLinkSample />
</PreviewCode>

Animated Indicator \[#animated-indicator]

All variants feature smooth animated indicators that slide between tabs:

<PreviewCode file="components/docs/samples/tabs" name="TabsAnimatedIndicatorSample">
  <TabsAnimatedIndicatorSample />
</PreviewCode>

API Reference \[#api-reference]

Composable API \[#composable-api]

Tabs \[#tabs]

The root component that manages tab state.

<ParametersTable
  type="TabsProps"
  parameters="[
{
name: &#x22;defaultValue&#x22;,
type: &#x22;string&#x22;,
description: &#x22;The default active tab value (uncontrolled).&#x22;,
},
{
name: &#x22;value&#x22;,
type: &#x22;string&#x22;,
description: &#x22;The controlled active tab value.&#x22;,
},
{
name: &#x22;onValueChange&#x22;,
type: &#x22;(value: string) => void&#x22;,
description: &#x22;Callback when the active tab changes.&#x22;,
},
{
name: &#x22;className&#x22;,
type: &#x22;string&#x22;,
description: &#x22;Additional CSS classes.&#x22;,
},
]"
/>

TabsList \[#tabslist]

The container for tab triggers. Set `variant` and `size` here to style all child components.

<ParametersTable
  type="TabsListProps"
  parameters="[
{
name: &#x22;variant&#x22;,
type: '&#x22;default&#x22; | &#x22;line&#x22; | &#x22;ghost&#x22; | &#x22;pills&#x22; | &#x22;outline&#x22;',
default: '&#x22;default&#x22;',
description: &#x22;The visual style of the tabs. Child components inherit this automatically.&#x22;,
},
{
name: &#x22;size&#x22;,
type: '&#x22;sm&#x22; | &#x22;default&#x22; | &#x22;lg&#x22;',
default: '&#x22;default&#x22;',
description: &#x22;The size of the tabs. Child components inherit this automatically.&#x22;,
},
{
name: &#x22;className&#x22;,
type: &#x22;string&#x22;,
description: &#x22;Additional CSS classes.&#x22;,
},
]"
/>

TabsTrigger \[#tabstrigger]

An individual tab button.

<ParametersTable
  type="TabsTriggerProps"
  parameters="[
{
name: &#x22;value&#x22;,
type: &#x22;string&#x22;,
required: true,
description: &#x22;The unique value for this tab.&#x22;,
},
{
name: &#x22;asChild&#x22;,
type: &#x22;boolean&#x22;,
default: &#x22;false&#x22;,
description: &#x22;Merge props with child element instead of rendering a button.&#x22;,
},
{
name: &#x22;disabled&#x22;,
type: &#x22;boolean&#x22;,
description: &#x22;Whether the tab is disabled.&#x22;,
},
{
name: &#x22;className&#x22;,
type: &#x22;string&#x22;,
description: &#x22;Additional CSS classes.&#x22;,
},
]"
/>

TabsContent \[#tabscontent]

The content panel for a tab.

<ParametersTable
  type="TabsContentProps"
  parameters="[
{
name: &#x22;value&#x22;,
type: &#x22;string&#x22;,
required: true,
description: &#x22;The value matching the corresponding TabsTrigger.&#x22;,
},
{
name: &#x22;className&#x22;,
type: &#x22;string&#x22;,
description: &#x22;Additional CSS classes.&#x22;,
},
]"
/>

Style Variants (CVA) \[#style-variants-cva]

URL: /docs/ui/thread-list

Switch between conversations. Supports sidebar or dropdown layouts.

Getting Started \[#getting-started]

Anatomy \[#anatomy]

The `ThreadList` component is built with the following primitives:

API Reference \[#api-reference]

ThreadListPrimitive.Root \[#threadlistprimitiveroot]

Container for the thread list.

<ParametersTable
  type="ThreadListPrimitiveRootProps"
  parameters="[
{
name: &#x22;asChild&#x22;,
type: &#x22;boolean&#x22;,
default: &#x22;false&#x22;,
description: &#x22;Merge props with child element instead of rendering a wrapper div.&#x22;,
},
]"
/>

ThreadListPrimitive.Items \[#threadlistprimitiveitems]

Renders all threads in the list.

<ParametersTable
  type="ThreadListPrimitiveItemsProps"
  parameters="[
{
name: &#x22;archived&#x22;,
type: &#x22;boolean&#x22;,
description: &#x22;When true, renders archived threads instead of active threads.&#x22;,
},
{
name: &#x22;components&#x22;,
type: &#x22;object&#x22;,
required: true,
description: &#x22;Component configuration.&#x22;,
children: [
{
type: &#x22;Components&#x22;,
parameters: [
{
name: &#x22;ThreadListItem&#x22;,
type: &#x22;ComponentType&#x22;,
required: true,
description: &#x22;Component to render for each thread item.&#x22;,
},
],
},
],
},
]"
/>

ThreadListPrimitive.New \[#threadlistprimitivenew]

A button to create a new thread.

<ParametersTable
  type="ThreadListPrimitiveNewProps"
  parameters="[
{
name: &#x22;asChild&#x22;,
type: &#x22;boolean&#x22;,
default: &#x22;false&#x22;,
description: &#x22;Merge props with child element instead of rendering a wrapper button.&#x22;,
},
]"
/>

ThreadListItemPrimitive.Root \[#threadlistitemprimitiveroot]

Container for a single thread item. Automatically sets `data-active` and `aria-current` when this is the current thread.

<ParametersTable
  type="ThreadListItemPrimitiveRootProps"
  parameters="[
{
name: &#x22;asChild&#x22;,
type: &#x22;boolean&#x22;,
default: &#x22;false&#x22;,
description: &#x22;Merge props with child element instead of rendering a wrapper div.&#x22;,
},
]"
/>

ThreadListItemPrimitive.Trigger \[#threadlistitemprimitivetrigger]

A button that switches to this thread when clicked.

<ParametersTable
  type="ThreadListItemPrimitiveTriggerProps"
  parameters="[
{
name: &#x22;asChild&#x22;,
type: &#x22;boolean&#x22;,
default: &#x22;false&#x22;,
description: &#x22;Merge props with child element instead of rendering a wrapper button.&#x22;,
},
]"
/>

ThreadListItemPrimitive.Title \[#threadlistitemprimitivetitle]

Renders the thread's title.

<ParametersTable
  type="ThreadListItemPrimitiveTitleProps"
  parameters="[
{
name: &#x22;fallback&#x22;,
type: &#x22;ReactNode&#x22;,
description: &#x22;Content to display when the thread has no title.&#x22;,
},
]"
/>

ThreadListItemPrimitive.Archive \[#threadlistitemprimitivearchive]

A button to archive the thread.

<ParametersTable
  type="ThreadListItemPrimitiveArchiveProps"
  parameters="[
{
name: &#x22;asChild&#x22;,
type: &#x22;boolean&#x22;,
default: &#x22;false&#x22;,
description: &#x22;Merge props with child element instead of rendering a wrapper button.&#x22;,
},
]"
/>

ThreadListItemPrimitive.Unarchive \[#threadlistitemprimitiveunarchive]

A button to restore an archived thread.

<ParametersTable
  type="ThreadListItemPrimitiveUnarchiveProps"
  parameters="[
{
name: &#x22;asChild&#x22;,
type: &#x22;boolean&#x22;,
default: &#x22;false&#x22;,
description: &#x22;Merge props with child element instead of rendering a wrapper button.&#x22;,
},
]"
/>

ThreadListItemPrimitive.Delete \[#threadlistitemprimitivedelete]

A button to permanently delete the thread.

<ParametersTable
  type="ThreadListItemPrimitiveDeleteProps"
  parameters="[
{
name: &#x22;asChild&#x22;,
type: &#x22;boolean&#x22;,
default: &#x22;false&#x22;,
description: &#x22;Merge props with child element instead of rendering a wrapper button.&#x22;,
},
]"
/>

ThreadListItemMorePrimitive \[#threadlistitemmoreprimitive]

A dropdown menu for additional thread actions, built on Radix UI DropdownMenu.

ThreadListItemMorePrimitive.Root \[#threadlistitemmoreprimitiveroot]

Menu container that manages dropdown state.

<ParametersTable
  type="ThreadListItemMorePrimitiveRootProps"
  parameters="[
{
name: &#x22;asChild&#x22;,
type: &#x22;boolean&#x22;,
default: &#x22;false&#x22;,
description: &#x22;Merge props with child element instead of rendering a wrapper div.&#x22;,
},
]"
/>

ThreadListItemMorePrimitive.Trigger \[#threadlistitemmoreprimitivetrigger]

Button to open the menu.

<ParametersTable
  type="ThreadListItemMorePrimitiveTriggerProps"
  parameters="[
{
name: &#x22;asChild&#x22;,
type: &#x22;boolean&#x22;,
default: &#x22;false&#x22;,
description: &#x22;Merge props with child element instead of rendering a wrapper button.&#x22;,
},
]"
/>

ThreadListItemMorePrimitive.Content \[#threadlistitemmoreprimitivecontent]

Menu content container.

<ParametersTable
  type="ThreadListItemMorePrimitiveContentProps"
  parameters="[
{
name: &#x22;asChild&#x22;,
type: &#x22;boolean&#x22;,
default: &#x22;false&#x22;,
description: &#x22;Merge props with child element instead of rendering a wrapper div.&#x22;,
},
]"
/>

ThreadListItemMorePrimitive.Item \[#threadlistitemmoreprimitiveitem]

Individual menu item.

<ParametersTable
  type="ThreadListItemMorePrimitiveItemProps"
  parameters="[
{
name: &#x22;asChild&#x22;,
type: &#x22;boolean&#x22;,
default: &#x22;false&#x22;,
description: &#x22;Merge props with child element instead of rendering a wrapper div.&#x22;,
},
]"
/>

ThreadListItemMorePrimitive.Separator \[#threadlistitemmoreprimitiveseparator]

Visual separator between items.

<ParametersTable
  type="ThreadListItemMorePrimitiveSeparatorProps"
  parameters="[
{
name: &#x22;asChild&#x22;,
type: &#x22;boolean&#x22;,
default: &#x22;false&#x22;,
description: &#x22;Merge props with child element instead of rendering a wrapper div.&#x22;,
},
]"
/>

Related Components \[#related-components]

URL: /docs/ui/thread

The main chat container with messages, composer, and auto-scroll.

A complete chat interface that combines message rendering, auto-scrolling, composer input,
attachments, and conditional UI states. Fully customizable and composable.

Anatomy \[#anatomy]

The `Thread` component is built with the following primitives:

Getting Started \[#getting-started]

Examples \[#examples]

Welcome Screen \[#welcome-screen]

Viewport Spacer \[#viewport-spacer]

Conditional Send/Cancel Button \[#conditional-sendcancel-button]

Suggestions \[#suggestions]

Display suggested prompts using the Suggestions API. See the [Suggestions guide](/docs/guides/suggestions) for detailed configuration.

API Reference \[#api-reference]

The following primitives are used within the Thread component and can be customized in your `/components/assistant-ui/thread.tsx` file.

Root \[#root]

Contains all parts of the thread.

<ParametersTable
  type="ThreadPrimitiveRootProps"
  parameters="[
{
name: &#x22;asChild&#x22;,
type: &#x22;boolean&#x22;,
default: &#x22;false&#x22;,
description: &#x22;Merge props with child element instead of rendering a wrapper div.&#x22;,
},
{
name: &#x22;className&#x22;,
type: &#x22;string&#x22;,
description: &#x22;CSS class name.&#x22;,
},
]"
/>

This primitive renders a `<div>` element unless `asChild` is set.

Viewport \[#viewport]

The scrollable area containing all messages. Automatically scrolls to the bottom as new messages are added.

<ParametersTable
  type="ThreadPrimitiveViewportProps"
  parameters="[
{
name: &#x22;asChild&#x22;,
type: &#x22;boolean&#x22;,
default: &#x22;false&#x22;,
description: &#x22;Merge props with child element instead of rendering a wrapper div.&#x22;,
},
{
name: &#x22;autoScroll&#x22;,
type: &#x22;boolean&#x22;,
default: &#x22;true&#x22;,
description:
&#x22;Whether to automatically scroll to the bottom when new messages are added while the viewport was previously scrolled to the bottom.&#x22;,
},
{
name: &#x22;className&#x22;,
type: &#x22;string&#x22;,
description: &#x22;CSS class name.&#x22;,
},
]"
/>

This primitive renders a `<div>` element unless `asChild` is set.

Messages \[#messages]

Renders all messages in the thread. This primitive renders a separate component for each message.

<ParametersTable
  type="ThreadPrimitiveMessagesProps"
  parameters="[
{
name: &#x22;components&#x22;,
type: &#x22;MessageComponents&#x22;,
required: true,
description: &#x22;Components to render for different message types.&#x22;,
children: [
{
type: &#x22;MessageComponents&#x22;,
parameters: [
{
name: &#x22;Message&#x22;,
type: &#x22;ComponentType&#x22;,
description: &#x22;Default component for all messages.&#x22;,
},
{
name: &#x22;UserMessage&#x22;,
type: &#x22;ComponentType&#x22;,
description: &#x22;Component for user messages.&#x22;,
},
{
name: &#x22;EditComposer&#x22;,
type: &#x22;ComponentType&#x22;,
description:
&#x22;Component for user messages being edited.&#x22;,
},
{
name: &#x22;AssistantMessage&#x22;,
type: &#x22;ComponentType&#x22;,
description: &#x22;Component for assistant messages.&#x22;,
},
{
name: &#x22;SystemMessage&#x22;,
type: &#x22;ComponentType&#x22;,
description: &#x22;Component for system messages.&#x22;,
},
],
},
],
},
]"
/>

MessageByIndex \[#messagebyindex]

Renders a single message at the specified index.

<ParametersTable
  type="ThreadPrimitiveMessageByIndexProps"
  parameters="[
{
name: &#x22;index&#x22;,
type: &#x22;number&#x22;,
required: true,
description: &#x22;The index of the message to render.&#x22;,
},
{
name: &#x22;components&#x22;,
type: &#x22;MessageComponents&#x22;,
description: &#x22;Components to render for different message types.&#x22;,
},
]"
/>

Empty \[#empty]

Renders children only when there are no messages in the thread.

<ParametersTable
  type="ThreadPrimitiveEmptyProps"
  parameters="[
{
name: &#x22;children&#x22;,
type: &#x22;ReactNode&#x22;,
description: &#x22;Content to display when the thread is empty.&#x22;,
},
]"
/>

ScrollToBottom \[#scrolltobottom]

A button to scroll the viewport to the bottom. Disabled when the viewport is already at the bottom.

<ParametersTable
  type="ThreadPrimitiveScrollToBottomProps"
  parameters="[
{
name: &#x22;asChild&#x22;,
type: &#x22;boolean&#x22;,
default: &#x22;false&#x22;,
description: &#x22;Merge props with child element instead of rendering a wrapper button.&#x22;,
},
{
name: &#x22;className&#x22;,
type: &#x22;string&#x22;,
description: &#x22;CSS class name.&#x22;,
},
]"
/>

This primitive renders a `<button>` element unless `asChild` is set.

Suggestions \[#suggestions-1]

Renders all configured suggestions. Configure suggestions using the `Suggestions()` API in your runtime provider.

<ParametersTable
  type="ThreadPrimitiveSuggestionsProps"
  parameters="[
{
name: &#x22;components&#x22;,
type: &#x22;{ Suggestion: ComponentType }&#x22;,
description: &#x22;Custom component to render each suggestion.&#x22;,
},
]"
/>

AuiIf \[#auiif]

Conditionally renders children based on assistant state. This is a generic component that can access thread, message, composer, and other state.

<ParametersTable
  type="AuiIfProps"
  parameters="[
{
name: &#x22;condition&#x22;,
type: &#x22;(state: AssistantState) => boolean&#x22;,
required: true,
description: &#x22;A function that receives the assistant state and returns whether to render children.&#x22;,
},
]"
/>

Related Components \[#related-components]

URL: /docs/ui/tool-fallback

Default UI component for tools without dedicated custom renderers.

Getting Started \[#getting-started]

Examples \[#examples]

Streaming Demo \[#streaming-demo]

Interactive demo showing the full tool call lifecycle: running → complete.

Running State \[#running-state]

Shows a loading spinner and shimmer animation while the tool is executing.

Cancelled State \[#cancelled-state]

Shows a muted appearance when a tool call was cancelled.

Composable API \[#composable-api]

All sub-components are exported for custom layouts:

Related Components \[#related-components]

URL: /docs/ui/tool-group

Wrapper for consecutive tool calls with collapsible and styled options.

A wrapper component that groups consecutive tool calls together, displaying them in a collapsible container with auto-expand behavior during streaming.

Getting Started \[#getting-started]

Variants \[#variants]

Use the `variant` prop on `ToolGroup.Root` to change the visual style:

Examples \[#examples]

Streaming Demo (Custom UI + Fallback) \[#streaming-demo-custom-ui--fallback]

Interactive demo showing tool group with **custom tool UIs** and `ToolFallback` working together. Watch as weather cards stream in with loading states, followed by a search tool using the fallback UI.

Custom Tool UIs \[#custom-tool-uis]

ToolGroup works with any custom tool UI components:

Composable API \[#composable-api]

All sub-components are exported for custom layouts:

API Reference \[#api-reference]

ToolGroupRoot \[#toolgrouproot]

<ParametersTable
  type="ToolGroupRootProps"
  parameters="[
{
name: &#x22;variant&#x22;,
type: '&#x22;outline&#x22; | &#x22;ghost&#x22; | &#x22;muted&#x22;',
default: '&#x22;outline&#x22;',
description: &#x22;Visual variant of the tool group container.&#x22;,
},
{
name: &#x22;open&#x22;,
type: &#x22;boolean&#x22;,
description: &#x22;Controlled open state.&#x22;,
},
{
name: &#x22;onOpenChange&#x22;,
type: &#x22;(open: boolean) => void&#x22;,
description: &#x22;Callback when open state changes.&#x22;,
},
{
name: &#x22;defaultOpen&#x22;,
type: &#x22;boolean&#x22;,
default: &#x22;false&#x22;,
description: &#x22;Initial open state for uncontrolled usage.&#x22;,
},
]"
/>

ToolGroupTrigger \[#toolgrouptrigger]

<ParametersTable
  type="ToolGroupTriggerProps"
  parameters="[
{
name: &#x22;count&#x22;,
type: &#x22;number&#x22;,
required: true,
description: &#x22;Number of tool calls to display in the label.&#x22;,
},
{
name: &#x22;active&#x22;,
type: &#x22;boolean&#x22;,
default: &#x22;false&#x22;,
description: &#x22;Shows loading spinner and shimmer animation when true.&#x22;,
},
]"
/>

ToolGroup (Default Export) \[#toolgroup-default-export]

<ParametersTable
  type="ToolGroupProps"
  parameters="[
{
name: &#x22;startIndex&#x22;,
type: &#x22;number&#x22;,
required: true,
description: &#x22;The index of the first tool call in the group.&#x22;,
},
{
name: &#x22;endIndex&#x22;,
type: &#x22;number&#x22;,
required: true,
description: &#x22;The index of the last tool call in the group.&#x22;,
},
{
name: &#x22;children&#x22;,
type: &#x22;ReactNode&#x22;,
required: true,
description: &#x22;The rendered tool call components.&#x22;,
},
]"
/>

Related Components \[#related-components]

URL: /docs/copilots/assistant-frame

Share model context across iframe boundaries

The Assistant Frame API enables iframes to provide model context (tools and instructions) to a parent window's assistant. This is particularly useful for embedded applications, plugins, or sandboxed components that need to contribute capabilities to the main assistant.

Overview \[#overview]

The Assistant Frame system consists of two main components:

Basic Usage \[#basic-usage]

In the iframe (Provider) \[#in-the-iframe-provider]

The iframe acts as a provider of model context using `AssistantFrameProvider`:

In the parent window (Host) \[#in-the-parent-window-host]

The parent window consumes the iframe's context using `AssistantFrameHost`:

Advanced Usage \[#advanced-usage]

ModelContextRegistry \[#modelcontextregistry]

The `ModelContextRegistry` provides a flexible way to manage model context dynamically:

Multiple Providers \[#multiple-providers]

You can register multiple model context providers in the same iframe:

Security Considerations \[#security-considerations]

Origin Validation \[#origin-validation]

Both the provider and host can specify allowed origins for security:

Tool Execution \[#tool-execution]

Tools are executed in the iframe's context, keeping sensitive operations sandboxed:

API Reference \[#api-reference]

AssistantFrameProvider \[#assistantframeprovider]

Static class that manages model context providers in an iframe.

Methods \[#methods]

`addModelContextProvider(provider, targetOrigin?)` \[#addmodelcontextproviderprovider-targetorigin]

Registers a model context provider to share with parent windows.

`dispose()` \[#dispose]

Cleans up all resources and removes all providers.

AssistantFrameHost \[#assistantframehost]

Class that connects to an iframe's model context providers.

Constructor \[#constructor]

Methods \[#methods-1]

`getModelContext()` \[#getmodelcontext]

Returns the current merged model context from the iframe.

`subscribe(callback)` \[#subscribecallback]

Subscribes to model context changes.

`dispose()` \[#dispose-1]

Cleans up the connection to the iframe.

useAssistantFrameHost \[#useassistantframehost]

React hook that manages the lifecycle of an AssistantFrameHost.

ModelContextRegistry \[#modelcontextregistry-1]

A flexible registry for managing model context with dynamic updates.

Methods \[#methods-2]

`addTool(tool)` \[#addtooltool]

Adds a tool and returns a handle for updates/removal.

`addInstruction(instruction)` \[#addinstructioninstruction]

Adds a system instruction and returns a handle.

`addProvider(provider)` \[#addproviderprovider]

Adds another model context provider.

Use Cases \[#use-cases]

Embedded Analytics Dashboard \[#embedded-analytics-dashboard]

An analytics iframe can provide data query tools to the parent assistant:

Plugin System \[#plugin-system]

Third-party plugins can extend the assistant's capabilities:

Data Visualization \[#data-visualization]

Provide data visualization tools in an iframe:

URL: /docs/copilots/make-assistant-tool-ui

Register custom UI components to render tool executions and their status.

The `makeAssistantToolUI` utility is used to register a tool UI component with the Assistant.

Usage \[#usage]

API \[#api]

Parameters \[#parameters]

<ParametersTable
  type="AssistantToolUIProps<TArgs, TResult>"
  parameters="[
{
name: &#x22;toolName&#x22;,
type: &#x22;string&#x22;,
description:
&#x22;The name of the tool. This must match the name of the tool defined in the assistant.&#x22;,
},
{
name: &#x22;render&#x22;,
type: &#x22;ComponentType<ToolCallMessagePartProps<TArgs, TResult>>&#x22;,
description:
&#x22;A React component that renders the tool UI. Receives the following props:&#x22;,
required: true,
children: [
{
type: &#x22;ToolCallMessagePartProps<TArgs, TResult>&#x22;,
parameters: [
{
name: &#x22;type&#x22;,
type: '&#x22;tool-call&#x22;',
description: &#x22;The message part type&#x22;,
},
{
name: &#x22;toolCallId&#x22;,
type: &#x22;string&#x22;,
description: &#x22;Unique identifier for this tool call&#x22;,
},
{
name: &#x22;toolName&#x22;,
type: &#x22;string&#x22;,
description: &#x22;The name of the tool being called&#x22;,
},
{
name: &#x22;args&#x22;,
type: &#x22;TArgs&#x22;,
description: &#x22;The arguments passed to the tool&#x22;,
},
{
name: &#x22;argsText&#x22;,
type: &#x22;string&#x22;,
description: &#x22;String representation of the arguments&#x22;,
},
{
name: &#x22;result&#x22;,
type: &#x22;TResult | undefined&#x22;,
description: &#x22;The result of the tool execution (if complete)&#x22;,
},
{
name: &#x22;isError&#x22;,
type: &#x22;boolean | undefined&#x22;,
description: &#x22;Whether the result is an error&#x22;,
},
{
name: &#x22;status&#x22;,
type: &#x22;ToolCallMessagePartStatus&#x22;,
description:
'The execution status object with a type property: &#x22;running&#x22;, &#x22;complete&#x22;, &#x22;incomplete&#x22;, or &#x22;requires-action&#x22;',
},
{
name: &#x22;addResult&#x22;,
type: &#x22;(result: TResult | ToolResponse<TResult>) => void&#x22;,
description:
&#x22;Function to add a result (useful for human-in-the-loop tools)&#x22;,
},
{
name: &#x22;artifact&#x22;,
type: &#x22;unknown&#x22;,
description:
&#x22;Optional artifact data associated with the tool call&#x22;,
},
],
},
],
},
]"
/>

Returns \[#returns]

A React functional component that should be included in your component tree. This component doesn't render anything itself, but it registers the tool UI with the Assistant.

Example \[#example]

This example shows how to create a simple UI for a `get_weather` tool. The UI will display different messages depending on the status of the tool execution.

URL: /docs/copilots/make-assistant-tool

Create React components that provide reusable tools to the assistant.

`makeAssistantTool` creates a React component that provides a tool to the assistant. This is useful for defining reusable tools that can be composed into your application.

Usage \[#usage]

API Reference \[#api-reference]

Parameters \[#parameters]

<ParametersTable
  type="AssistantToolProps<TArgs, TResult>"
  parameters="[
{
name: &#x22;toolName&#x22;,
type: &#x22;string&#x22;,
description: &#x22;The unique identifier for the tool&#x22;,
required: true,
},
{
name: &#x22;parameters&#x22;,
type: &#x22;StandardSchemaV1<TArgs> | JSONSchema7&#x22;,
description:
&#x22;Schema defining the tool's parameters (typically a Zod schema)&#x22;,
required: true,
},
{
name: &#x22;execute&#x22;,
type: &#x22;(args: TArgs, context: ToolExecutionContext) => TResult | Promise<TResult>&#x22;,
description:
&#x22;Function that implements the tool's behavior (required for frontend tools)&#x22;,
required: true,
},
{
name: &#x22;description&#x22;,
type: &#x22;string&#x22;,
description: &#x22;Optional description of the tool's purpose&#x22;,
},
{
name: &#x22;render&#x22;,
type: &#x22;ComponentType<ToolCallMessagePartProps<TArgs, TResult>>&#x22;,
description:
&#x22;Optional custom UI component for rendering the tool execution. Receives the following props:&#x22;,
children: [
{
type: &#x22;ToolCallMessagePartProps<TArgs, TResult>&#x22;,
parameters: [
{
name: &#x22;type&#x22;,
type: '&#x22;tool-call&#x22;',
description: &#x22;The message part type&#x22;,
},
{
name: &#x22;toolCallId&#x22;,
type: &#x22;string&#x22;,
description: &#x22;Unique identifier for this tool call&#x22;,
},
{
name: &#x22;toolName&#x22;,
type: &#x22;string&#x22;,
description: &#x22;The name of the tool being called&#x22;,
},
{
name: &#x22;args&#x22;,
type: &#x22;TArgs&#x22;,
description: &#x22;The arguments passed to the tool&#x22;,
},
{
name: &#x22;argsText&#x22;,
type: &#x22;string&#x22;,
description: &#x22;String representation of the arguments&#x22;,
},
{
name: &#x22;result&#x22;,
type: &#x22;TResult | undefined&#x22;,
description: &#x22;The result of the tool execution (if complete)&#x22;,
},
{
name: &#x22;isError&#x22;,
type: &#x22;boolean | undefined&#x22;,
description: &#x22;Whether the result is an error&#x22;,
},
{
name: &#x22;status&#x22;,
type: &#x22;ToolCallMessagePartStatus&#x22;,
description:
'The execution status object with a type property: &#x22;running&#x22;, &#x22;complete&#x22;, &#x22;incomplete&#x22;, or &#x22;requires-action&#x22;',
},
{
name: &#x22;addResult&#x22;,
type: &#x22;(result: TResult | ToolResponse<TResult>) => void&#x22;,
description:
&#x22;Function to add a result (useful for human-in-the-loop tools)&#x22;,
},
{
name: &#x22;artifact&#x22;,
type: &#x22;unknown&#x22;,
description:
&#x22;Optional artifact data associated with the tool call&#x22;,
},
],
},
],
},
]"
/>

Returns \[#returns]

Returns a React component that:

Example with Multiple Tools \[#example-with-multiple-tools]

Best Practices \[#best-practices]

URL: /docs/copilots/make-assistant-visible

Make React components visible and interactive to assistants via higher-order component wrapping.

`makeAssistantVisible` is a higher-order component (HOC) that makes React components "visible" by the assistant, allowing it to understand and interact with the component's HTML structure.

Usage \[#usage]

API Reference \[#api-reference]

Parameters \[#parameters]

Behavior \[#behavior]

The HOC will:

Example \[#example]

Technical Details \[#technical-details]

When a component is made readable:

URL: /docs/copilots/model-context

Configure assistant behavior through system instructions, tools, and context providers.

Model Context is the foundation of intelligence in assistant-ui components. It provides configuration and capabilities to the assistant through a context provider system.

Core Concepts \[#core-concepts]

System Instructions \[#system-instructions]

System instructions define the base behavior and knowledge available to the assistant. These can be provided in several ways:

Tools \[#tools]

Tools are functions that the assistant can use to interact with your application. They can be provided through various mechanisms:

Context Provider System \[#context-provider-system]

The context provider system allows components to contribute to the model context. Here's a typical usage pattern:

Provider Composition \[#provider-composition]

Multiple providers can be registered, and their contexts will be composed:

Best Practices \[#best-practices]

URL: /docs/copilots/motivation

Add intelligence to React components through readable interfaces and assistant tools.

React revolutionized web development with components that combine logic, structure, and style. Now, with assistant-ui, we're adding a fourth dimension: intelligence. Let's learn how to build smart components through a practical banking app example.

The Evolution of Components \[#the-evolution-of-components]

Traditional React components combine three elements:

Adding Intelligence \[#adding-intelligence]

With assistant-ui, we can enhance this component with intelligence using four powerful APIs:

1\. Making Components Readable (makeAssistantVisible) \[#1-making-components-readable-makeassistantvisible]

First, let's make our buttons "readable" and interactive:

Now the assistant can:

2\. Adding System Instructions (useAssistantInstructions) \[#2-adding-system-instructions-useassistantinstructions]

Next, let's give the assistant specific instructions about its role:

3\. Creating Tools (makeAssistantTool) \[#3-creating-tools-makeassistanttool]

Let's add transaction-specific tools for the assistant:

4\. Adding Custom Context (Model Context) \[#4-adding-custom-context-model-context]

Finally, let's add dynamic context based on the user's transaction patterns:

The Result: An Intelligent Banking Experience \[#the-result-an-intelligent-banking-experience]

This enhanced component now provides:

The assistant can now:

This creates a more intuitive and safer banking experience while maintaining the familiar React component model.

Next Steps \[#next-steps]

Learn more about each API:

URL: /docs/copilots/use-assistant-instructions

React hook for setting system instructions to guide assistant behavior.

`useAssistantInstructions` is a React hook that allows you to set system instructions for your assistant-ui components.

Usage \[#usage]

API Reference \[#api-reference]

Parameters \[#parameters]

The hook accepts either:

Behavior \[#behavior]

The hook will:

Example \[#example]

URL: /docs/guides/attachments

Let users attach files, images, and documents to messages.

Enable users to attach files to their messages, enhancing conversations with images, documents, and other content.

Overview \[#overview]

The attachment system in assistant-ui provides a flexible framework for handling file uploads in your AI chat interface. It consists of:

Getting Started \[#getting-started]

Built-in Attachment Adapters \[#built-in-attachment-adapters]

SimpleImageAttachmentAdapter \[#simpleimageattachmentadapter]

Handles image files and converts them to data URLs for display in the chat UI. By default, images are shown inline but not sent to the LLM - use the VisionImageAdapter example above to send images to vision-capable models.

SimpleTextAttachmentAdapter \[#simpletextattachmentadapter]

Processes text files and wraps content in formatted tags:

CompositeAttachmentAdapter \[#compositeattachmentadapter]

Combines multiple adapters to support various file types:

Creating Custom Attachment Adapters \[#creating-custom-attachment-adapters]

Build your own adapters for specialized file handling. Below are complete examples for common use cases.

Vision-Capable Image Adapter \[#vision-capable-image-adapter]

Send images to vision-capable LLMs like GPT-4V, Claude 3, or Gemini Pro Vision:

PDF Document Adapter \[#pdf-document-adapter]

Handle PDF files by extracting text or converting to base64 for processing:

Using Custom Adapters \[#using-custom-adapters]

With LocalRuntime \[#with-localruntime]

When using `LocalRuntime`, you need to handle images in your `ChatModelAdapter` (the adapter that connects to your AI backend):

Advanced Features \[#advanced-features]

Progress Updates \[#progress-updates]

Provide real-time upload progress using async generators:

Validation and Error Handling \[#validation-and-error-handling]

Implement robust validation in your adapters:

External Source Attachments \[#external-source-attachments]

Add attachments from external sources (URLs, API data, CMS references) without needing a `File` object or an `AttachmentAdapter`:

External attachments are added as complete attachments directly — they skip the `AttachmentAdapter` entirely and can be removed without one.

Multiple File Selection \[#multiple-file-selection]

Enable multi-file selection with custom limits:

Backend Integration \[#backend-integration]

With Vercel AI SDK \[#with-vercel-ai-sdk]

Attachments are sent to the backend as file content parts.

Runtime Support \[#runtime-support]

Attachments work with all assistant-ui runtimes:

Best Practices \[#best-practices]

Resources \[#resources]

URL: /docs/guides/branching

Navigate between different conversation branches when editing or reloading messages.

Switch between different conversation branches.

A new branch is created when:

Branches are automatically tracked by assistant-ui by observing changes to the `messages` array.

Enabling branch support \[#enabling-branch-support]

You can show a branch picker by using `BranchPickerPrimitive`.

API \[#api]

You can access the current branch state or navigate via the API as well.
These APIs rely on the message scope and may only be called inside a message component.

URL: /docs/guides/chain-of-thought

Group reasoning and tool calls into a collapsible accordion UI.

LLMs often produce reasoning steps and tool calls in succession. Chain of Thought lets you visually group these consecutive parts into a single collapsible accordion, giving users a clean "thinking" UI.

Overview \[#overview]

When a model like OpenAI's `o4-mini` responds, it may emit a sequence of reasoning tokens and tool calls before producing its final text answer. By default, these parts render individually. `ChainOfThoughtPrimitive` groups consecutive reasoning + tool-call parts together and renders them through a single component.

Key benefits:

Quick Start \[#quick-start]

API Reference \[#api-reference]

ChainOfThoughtPrimitive.Root \[#chainofthoughtprimitiveroot]

Container element for the chain of thought group. Renders a `<div>`.

ChainOfThoughtPrimitive.AccordionTrigger \[#chainofthoughtprimitiveaccordiontrigger]

A button that toggles the collapsed/expanded state. Collapsed by default.

ChainOfThoughtPrimitive.Parts \[#chainofthoughtprimitiveparts]

Renders the grouped parts when expanded (nothing when collapsed).

Reading Collapsed State \[#reading-collapsed-state]

Use `AuiIf` to conditionally render based on the accordion state:

Full Example \[#full-example]

See the complete [with-chain-of-thought example](https://github.com/assistant-ui/assistant-ui/tree/main/examples/with-chain-of-thought) for a working implementation with tool calls and reasoning.

Related Guides \[#related-guides]

URL: /docs/guides/context-api

Read and update assistant state to build custom components.

The Context API provides direct access to assistant-ui's state management system, enabling you to build custom components that integrate seamlessly with the assistant runtime.

Introduction \[#introduction]

The Context API is assistant-ui's powerful state management system that enables you to build custom components with full access to the assistant's state and capabilities. It provides:

It's the foundation that powers all assistant-ui primitives. When the built-in components don't meet your needs, you can use the Context API to create custom components with the same capabilities.

The Context API is backed by the runtime you provide to `<AssistantRuntimeProvider>`. This runtime acts as a unified store that manages all assistant state, handles actions, and dispatches events across your entire application.

Core Concepts \[#core-concepts]

Scopes and Hierarchy \[#scopes-and-hierarchy]

assistant-ui organizes state into **scopes** - logical boundaries that provide access to relevant data and actions. Each scope corresponds to a specific part of the chat interface and automatically provides context-aware functionality.

**How scopes work:**

State Management Model \[#state-management-model]

The Context API follows a predictable state management pattern:

Essential Hooks \[#essential-hooks]

useAuiState \[#useauistate]

Read state reactively with automatic re-renders when values change. This hook works like Zustand's selector pattern - you provide a function that extracts the specific data you need, and your component only re-renders when that data changes.

The selector function receives all available scopes for your component's location and should return a specific value. The component re-renders only when that returned value changes.

**Common patterns:**

**Important:** Never create new objects in selectors. Return primitive values or stable references to avoid infinite re-renders.

useAui \[#useaui]

Access the API instance for imperative operations and actions. Unlike `useAuiState`, this hook returns a stable object that never changes, making it perfect for event handlers and imperative operations.

The API object is stable and doesn't cause re-renders. Use it for:

**Available actions by scope:**

useAuiEvent \[#useauievent]

Subscribe to events with automatic cleanup on unmount. This hook is perfect for reacting to user interactions, system events, or integrating with external analytics.

**Event name patterns:**

Working with Scopes \[#working-with-scopes]

Available Scopes \[#available-scopes]

Each scope provides access to specific state and actions:

Scope Resolution \[#scope-resolution]

The Context API automatically resolves the current scope based on component location:

Checking Scope Availability \[#checking-scope-availability]

Before accessing a scope, check if it's available:

Accessing Nested Scopes \[#accessing-nested-scopes]

Navigate through the scope hierarchy programmatically:

Common Patterns \[#common-patterns]

Conditional Rendering \[#conditional-rendering]

Custom Action Buttons \[#custom-action-buttons]

State-Aware Components \[#state-aware-components]

Event-Driven Updates \[#event-driven-updates]

Advanced Topics \[#advanced-topics]

Resolution Dynamics \[#resolution-dynamics]

When you call `aui.scope()`, the API resolves the current scope at that moment. This resolution happens each time you call the function, which matters when dealing with changing contexts:

For most use cases, this behavior is intuitive. In advanced scenarios where you need to track specific instances, store the resolved reference.

Performance Optimization \[#performance-optimization]

**Selector optimization:**

**Minimize re-renders:**

API Reference \[#api-reference]

Hooks \[#hooks]

Scope States \[#scope-states]

Available Actions by Scope \[#available-actions-by-scope]

Common Events \[#common-events]

Troubleshooting \[#troubleshooting]

Common Errors \[#common-errors]

**"Cannot access \[scope] outside of \[scope] context"**

**"Maximum update depth exceeded" / Infinite re-renders**

**"Scope resolution failed" / Stale scope references**

Quick Reference \[#quick-reference]

URL: /docs/guides/dictation

assistant-ui supports speech-to-text (dictation) via the `DictationAdapter` interface. This allows users to input messages using their voice.

DictationAdapter \[#dictationadapter]

Currently, the following dictation adapters are supported:

The `WebSpeechDictationAdapter` is supported in Chrome, Edge, and Safari. Check [browser compatibility](https://developer.mozilla.org/en-US/docs/Web/API/SpeechRecognition#browser_compatibility) for details.

Configuration \[#configuration]

UI \[#ui]

The dictation feature uses `ComposerPrimitive.Dictate` and `ComposerPrimitive.StopDictation` components.

Browser Compatibility Check \[#browser-compatibility-check]

You can check if the browser supports dictation:

Disabling Input During Dictation \[#disabling-input-during-dictation]

Some dictation services (like ElevenLabs Scribe) return cumulative transcripts that conflict with simultaneous typing. You can disable the text input during dictation:

Custom Adapters \[#custom-adapters]

You can create custom adapters to integrate with any dictation service by implementing the `DictationAdapter` interface.

DictationAdapter Interface \[#dictationadapter-interface]

Interim vs Final Results \[#interim-vs-final-results]

The `onSpeech` callback receives results with an optional `isFinal` flag:

**Both interim and final results are displayed directly in the input field**, just like native dictation on iOS/Android. Interim results replace each other until a final result commits the text. This provides seamless real-time feedback while the user speaks.

Example: ElevenLabs Scribe v2 Realtime \[#example-elevenlabs-scribe-v2-realtime]

[ElevenLabs Scribe](https://elevenlabs.io/docs/capabilities/speech-to-text) provides ultra-low latency (\~150ms) real-time transcription via WebSocket.

Install Dependencies \[#install-dependencies]

Backend API Route \[#backend-api-route]

Create an API route to generate single-use tokens:

Frontend Adapter \[#frontend-adapter]

Usage \[#usage]

Real-time Preview \[#real-time-preview]

The transcription is displayed directly in the input field as the user speaks — just like native dictation. No additional UI components are needed for basic use cases.

URL: /docs/guides/editing

Allow users to edit their messages with custom editor interfaces.

Give the user the ability to edit their message.

Enabling edit support \[#enabling-edit-support]

You can show an editor interface by using `ComposerPrimitive`.

URL: /docs/guides/latex

Render mathematical expressions in chat messages using KaTeX.

Render LaTeX mathematical expressions in chat messages using KaTeX.

Supported Formats \[#supported-formats]

By default, remark-math supports:

Supporting Alternative LaTeX Delimiters \[#supporting-alternative-latex-delimiters]

Many language models generate LaTeX using different delimiter formats:

You can use the `preprocess` prop to normalize these formats:

URL: /docs/guides/message-timing

Display stream timing metadata like duration, tokens per second, and time to first token.

Display stream performance metrics — duration, tokens per second, TTFT — on assistant messages.

Reading Timing Data \[#reading-timing-data]

Use `useMessageTiming()` inside a message component to access timing data:

Place it inside `MessagePrimitive.Root`, typically near the action bar:

`useMessageTiming()` Return Fields \[#usemessagetiming-return-fields]

Runtime Support \[#runtime-support]

DataStream \[#datastream]

Timing is tracked automatically inside `AssistantMessageAccumulator`. No setup required.

AI SDK (`useChatRuntime`) \[#ai-sdk-usechatruntime]

Timing is tracked automatically on the client side by observing streaming state transitions and content changes. Timing is finalized when each stream completes.

Local (`useLocalRuntime`) \[#local-uselocalruntime]

Pass timing in the `metadata` field of your `ChatModelRunResult`:

ExternalStore (`useExternalStoreRuntime`) \[#externalstore-useexternalstoreruntime]

Pass timing in the `metadata.timing` field of your `ThreadMessageLike` messages:

API Reference \[#api-reference]

`useMessageTiming()` \[#usemessagetiming]

Returns timing metadata for the current assistant message, or `undefined` for non-assistant messages or when no timing data is available.

Must be used inside a `MessagePrimitive.Root` context.

URL: /docs/guides/multi-agent

Render sub-agent conversations inside tool call UIs.

In a multi-agent (orchestrator) architecture, a main agent invokes sub-agents via tool calls. Each sub-agent may produce its own conversation (user/assistant messages, tool calls, etc.). assistant-ui supports rendering these nested conversations using the `MessagePartPrimitive.Messages` primitive.

Overview \[#overview]

When a tool call includes a `messages` field (`ToolCallMessagePart.messages`), it represents a sub-agent's conversation history. `MessagePartPrimitive.Messages` reads this field from the current tool call part and renders it as a nested thread.

Key behaviors:

Quick Start \[#quick-start]

Recursive Sub-Agents \[#recursive-sub-agents]

If a sub-agent's tool calls also have nested messages, the same pattern applies recursively:

ReadonlyThreadProvider \[#readonlythreadprovider]

For advanced use cases where you have a `ThreadMessage[]` array and want to render it as a thread outside of a tool call context, use `ReadonlyThreadProvider` directly:

`ReadonlyThreadProvider` inherits the parent's tool UI registrations and model context through scope inheritance.

Related \[#related]

URL: /docs/guides/quoting

Let users select and quote text from messages. Full guide including backend handling and programmatic API.

Get Started \[#get-started]

The \*\*[Quote](/docs/ui/quote)\*\* registry component gives you everything you need out of the box, including a floating selection toolbar, composer quote preview, and inline quote display.

It ships three composable pieces:

See the [Quote component page](/docs/ui/quote) for full setup steps and API reference.

How It Works \[#how-it-works]

When a user selects text in an assistant message, a floating toolbar appears with a Quote button. Clicking it calls `composer.setQuote()` to store the selection on the composer. The [Quote component](/docs/ui/quote) does this out of the box.

When the message is sent, the composer runtime automatically writes the quote to `message.metadata.custom.quote` and clears it from the composer.

On the backend, the route handler extracts the quote from metadata and surfaces it to the LLM. We export a helper called `injectQuoteContext` that handles this automatically for AI-SDK. Without this step, the quote appears in the UI but is not sent to the model as context. See [Backend Handling](#backend-handling) for more info and alternatives.

Data Shape \[#data-shape]

Backend Handling \[#backend-handling]

Quote data travels in message metadata, not content, so the LLM will not see it unless your backend extracts and surfaces it. The simplest path is [`injectQuoteContext`](/docs/ui/quote#forward-quote-context-to-the-llm), which prepends quoted text as a markdown blockquote before the message parts.

For provider-specific handling, work with the quote metadata directly.

Claude SDK Citations \[#claude-sdk-citations]

Pass the quoted text as a citation source so Claude produces citations that reference it:

OpenAI Message Context \[#openai-message-context]

Inject the quote as additional context in the user message:

Reading Quote Data \[#reading-quote-data]

Use `useMessageQuote` to access quote data in custom components:

Programmatic API \[#programmatic-api]

Set or clear quotes via the composer runtime:

Design Notes \[#design-notes]

Related \[#related]

URL: /docs/guides/speech

Read messages aloud with Web Speech API or custom TTS.

assistant-ui supports text-to-speech via the `SpeechSynthesisAdapter` interface.

SpeechSynthesisAdapter \[#speechsynthesisadapter]

Currently, the following speech synthesis adapters are supported:

Support for other speech synthesis adapters is planned for the future.

Passing a `SpeechSynthesisAdapter` to the runtime will enable text-to-speech support.

UI \[#ui]

The default action bar does not include a speech button. You need to add `ActionBarPrimitive.Speak` and `ActionBarPrimitive.StopSpeaking` to your assistant message action bar manually. See the example above for a complete implementation.

Example \[#example]

The following example uses the `WebSpeechSynthesisAdapter`.

URL: /docs/guides/suggestions

Display suggested prompts to help users get started with your assistant.

Suggestions are pre-defined prompts that help users discover what your assistant can do. They appear in the welcome screen and provide a quick way to start conversations.

Overview \[#overview]

The Suggestions API allows you to configure a list of suggested prompts that are displayed when the thread is empty. Users can click on a suggestion to either populate the composer or immediately send the message.

Quick Start \[#quick-start]

Configure suggestions using the `Suggestions()` API in your runtime provider:

Suggestion Format \[#suggestion-format]

Suggestions can be provided as either strings or objects with title, label, and prompt:

Simple Strings \[#simple-strings]

Objects with Title and Description \[#objects-with-title-and-description]

For more detailed suggestions with separate display text and prompts:

Displaying Suggestions \[#displaying-suggestions]

The default Thread component from the shadcn registry already includes suggestion rendering. The suggestions are displayed in the welcome screen when the thread is empty.

Customizing Suggestion Display \[#customizing-suggestion-display]

If you want to customize how suggestions are displayed, you can modify your Thread component:

Suggestion Primitives \[#suggestion-primitives]

ThreadPrimitive.Suggestions \[#threadprimitivesuggestions]

Renders all suggestions from the suggestions scope.

SuggestionPrimitive.Title \[#suggestionprimitivetitle]

Displays the suggestion's title (the first part when using object format, or the full text when using strings).

SuggestionPrimitive.Description \[#suggestionprimitivedescription]

Displays the suggestion's description/label (only shown when using object format).

SuggestionPrimitive.Trigger \[#suggestionprimitivetrigger]

A button that triggers the suggestion action when clicked.

**Props:**

Dynamic Suggestions \[#dynamic-suggestions]

You can dynamically change suggestions based on your application state:

Context-Aware Suggestions \[#context-aware-suggestions]

Suggestions can be tailored to different contexts or user intents:

Best Practices \[#best-practices]

Migration from Legacy API \[#migration-from-legacy-api]

If you're using the deprecated `ThreadPrimitive.Suggestion` component, migrate to the new API:

Before (Deprecated) \[#before-deprecated]

After (Recommended) \[#after-recommended]

The new API provides:

Related \[#related]

URL: /docs/guides/tool-ui

Render tool calls as interactive UI instead of plain text.

Create custom UI components for AI tool calls, providing visual feedback and interactive experiences when tools are executed.

Overview \[#overview]

Tool UIs in assistant-ui allow you to create custom interfaces that appear when AI tools are called. These generative UI components enhance the user experience by:

This guide demonstrates building tool UIs with the **Vercel AI SDK**.

Creating Tool UIs \[#creating-tool-uis]

There are two main approaches to creating tool UIs in assistant-ui:

1\. Client-Defined Tools (`makeAssistantTool`) \[#1-client-defined-tools-makeassistanttool]

If you're creating tools on the client side, use `makeAssistantTool` to register them with the assistant context. Then create a UI component with `makeAssistantToolUI`:

Learn more about creating tools in the [Tools Guide](/docs/guides/tools).

2\. UI-Only for Existing Tools (`makeAssistantToolUI`) \[#2-ui-only-for-existing-tools-makeassistanttoolui]

If your tool is defined elsewhere (e.g., in your backend API, MCP server, or LangGraph), use `makeAssistantToolUI` to create just the UI component:

Quick Start Example \[#quick-start-example]

This example shows how to implement the UI-only approach using `makeAssistantToolUI`:

Tool UI Patterns \[#tool-ui-patterns]

Component Pattern \[#component-pattern]

Create standalone tool UI components:

Hook Pattern \[#hook-pattern]

Use hooks for dynamic tool UI registration:

Inline Pattern \[#inline-pattern]

For tools that need access to parent component props:

Interactive Tool UIs \[#interactive-tool-uis]

User Input Collection \[#user-input-collection]

Create tools that collect user input during execution:

Multi-Step Interactions \[#multi-step-interactions]

Build complex workflows with human-in-the-loop patterns for multi-step user interactions:

Advanced Features \[#advanced-features]

Tool Status Handling \[#tool-status-handling]

The `status` prop provides detailed execution state:

Field-Level Validation \[#field-level-validation]

Use `useToolArgsFieldStatus` to show validation states:

Partial Results & Streaming \[#partial-results--streaming]

Display results as they stream in:

Custom Tool Fallback \[#custom-tool-fallback]

Provide a custom UI for tools without specific UIs:

Execution Context \[#execution-context]

Generative UI components have access to execution context through props:

Human Input Handling \[#human-input-handling]

When a tool calls `human()` during execution, the payload becomes available in the render function as `interrupt.payload`:

Learn more about tool human input in the [Tools Guide](/docs/guides/tools#human-in-the-loop).

Best Practices \[#best-practices]

1\. Handle All Status States \[#1-handle-all-status-states]

Always handle loading, error, and success states:

2\. Provide Visual Feedback \[#2-provide-visual-feedback]

Use animations and transitions for better UX:

3\. Make UIs Accessible \[#3-make-uis-accessible]

Ensure keyboard navigation and screen reader support:

4\. Optimize Performance \[#4-optimize-performance]

Use `useInlineRender` to prevent unnecessary re-renders:

Related Guides \[#related-guides]

URL: /docs/guides/tools

Give your assistant actions like API calls, database queries, and more.

Tools enable LLMs to take actions and interact with external systems. assistant-ui provides a comprehensive toolkit for creating, managing, and visualizing tool interactions in real-time.

Overview \[#overview]

Tools in assistant-ui are functions that the LLM can call to perform specific tasks. They bridge the gap between the LLM's reasoning capabilities and real-world actions like:

When tools are executed, you can display custom generative UI components that provide rich, interactive visualizations of the tool's execution and results. Learn more in the [Generative UI guide](/docs/guides/tool-ui).

Recommended: Tools() API \[#recommended-tools-api]

The `Tools()` API is the recommended way to register tools in assistant-ui. It provides centralized tool registration that prevents duplicate registrations and works seamlessly with all runtimes.

Quick Start \[#quick-start]

Create a toolkit object containing all your tools, then register it using `useAui()`:

Benefits \[#benefits]

Tool Definition \[#tool-definition]

Each tool in the toolkit is a `ToolDefinition` object with these properties:

Organizing Large Toolkits \[#organizing-large-toolkits]

For larger applications, split tools across multiple files:

UI-Only Tools \[#ui-only-tools]

For tools where execution happens elsewhere (e.g., backend MCP tools), omit the `execute` function:

Tool Execution Context \[#tool-execution-context]

Tools receive additional context during execution:

Human-in-the-Loop \[#human-in-the-loop]

Tools can pause execution to request user input or approval:

Alternative Methods (Legacy) \[#alternative-methods-legacy]

Using `makeAssistantTool` (Deprecated) \[#using-makeassistanttool-deprecated]

Register tools with the assistant context. Returns a React component that registers the tool when rendered:

**Why this is deprecated**: Component-based registration can lead to duplicate registrations if components are remounted or if the same tool is defined in multiple places.

Using `useAssistantTool` Hook (Deprecated) \[#using-useassistanttool-hook-deprecated]

Register tools dynamically using React hooks:

**Why this is deprecated**: Hook-based registration ties tool definitions to component lifecycle, making them harder to test and potentially causing duplicate registrations.

Using `makeAssistantToolUI` (Deprecated) \[#using-makeassistanttoolui-deprecated]

Create UI-only components for tools defined elsewhere:

**Why this is deprecated**: Component-based UI registration can cause issues with tool UI not appearing or appearing multiple times.

Tool Paradigms \[#tool-paradigms]

Frontend Tools \[#frontend-tools]

Tools that execute in the browser:

Backend Tools \[#backend-tools]

Tools executed server-side:

Client-Defined Tools with frontendTools \[#client-defined-tools-with-frontendtools]

The Vercel AI SDK adapter implements automatic serialization of client-defined tools. Tools registered via the `Tools()` API are automatically included in API requests:

MCP (Model Context Protocol) Tools \[#mcp-model-context-protocol-tools]

Integration with MCP servers using AI SDK's experimental MCP support:

Best Practices \[#best-practices]

Migration from Legacy APIs \[#migration-from-legacy-apis]

To migrate from legacy APIs to the `Tools()` API:

Example migration:

URL: /docs/api-reference/overview

API reference for primitives, runtime hooks, and context providers.

Cloud \[#cloud]

Runtime API \[#runtime-api]

AI SDK \[#ai-sdk]

Data Stream \[#data-stream]

assistant-stream (Framework-Agnostic) \[#assistant-stream-framework-agnostic]

LangGraph \[#langgraph]

Local Runtime \[#local-runtime]

External Store Runtime \[#external-store-runtime]

Thread List Runtime \[#thread-list-runtime]

Runtime Adapters \[#runtime-adapters]

Attachment \[#attachment]

Feedback \[#feedback]

Speech \[#speech]

Highest Level Context Providers \[#highest-level-context-providers]

<Component
  name="AssistantRuntimeProvider"
  isContextProvider="true"
  providedContexts="[
{ name: &#x22;Assistant Context&#x22;, color: contextColors[&#x22;Assistant Context&#x22;] },
{ name: &#x22;Thread Context&#x22;, color: contextColors[&#x22;Thread Context&#x22;] },
{
name: &#x22;Thread Composer Context&#x22;,
color: contextColors[&#x22;Composer Context&#x22;],
link: &#x22;#composer-context&#x22;,
},
]"
  docsLink="./context-providers/assistant-runtime-provider"
  tooltip="Provides the highest level context for the assistant-ui"
  props="runtime={runtime}"

<Component
  name="TextMessagePartProvider"
  isContextProvider="true"
  providedContexts="[
{
name: &#x22;Text MessagePart Context&#x22;,
color: contextColors[&#x22;MessagePart Context&#x22;],
link: &#x22;#MessagePart-context&#x22;,
},
]"
  docsLink="./context-providers/text-message-part-provider"
  tooltip="Provides context for text message parts"
  props="text={text}"

  The context available to components inside `<AssistantRuntimeProvider />`. You usually wrap your entire application in this context.

  AssistantRuntime \[#assistantruntime]

  Programmatically access the assistant's state and actions via `useAui()`.

  Instructions \[#instructions]

  Add system prompt instructions

  Tool UI \[#tool-ui]

  Register tool UIs

  Programmatically access the list of registered tool UIs via `useAuiState((s) => s.tools)` and `useAui().tools()`.

  ThreadListPrimitive \[#threadlistprimitive]

  Shows a list of threads and allows the user to switch between them.

{
name: &#x22;ThreadListItem Context&#x22;,
color: contextColors[&#x22;ThreadListItem Context&#x22;],
},
]"
      docsLink="#thread-list-primitive-items"
      tooltip="Container for thread list items, provides context for individual items"
      props="components={...}"
    />
  </Component>
</ContextLevel>

  The context for a single thread. Currently always corresponds to the runtime's main thread.

  ThreadRuntime \[#threadruntime]

  Programmatically access the thread's state and actions.

  ModelContext \[#modelcontext]

  ThreadViewportStore \[#threadviewportstore]

  ThreadPrimitive \[#threadprimitive]

  A conversation thread.

  AssistantModalPrimitive \[#assistantmodalprimitive]

  A floating modal that usually appears in the lower right corner of the screen. Common for support use cases.

  Manages the state and actions for the message composer

  ComposerRuntime \[#composerruntime]

  ComposerPrimitive \[#composerprimitive]

{
name: &#x22;Attachment Context&#x22;,
color: contextColors[&#x22;Attachment Context&#x22;],
},
]"
      docsLink="#composer-primitive-attachments"
      tooltip="Manages attachments in the composer"
    />

  Manages the state and actions for individual messages

  MessageRuntime \[#messageruntime]

  MessagePrimitive \[#messageprimitive]

{
name: &#x22;Attachment Context&#x22;,
color: contextColors[&#x22;Attachment Context&#x22;],
},
]"
      docsLink="#message-primitive-attachments"
      tooltip="Displays attachments in the message"
    />

  ActionBarPrimitive \[#actionbarprimitive]

  BranchPickerPrimitive \[#branchpickerprimitive]

  Manages the state and actions for message parts within messages

  MessagePartRuntime \[#messagepartruntime]

  MessagePartPrimitive \[#messagepartprimitive]

  MarkdownText \[#markdowntext]

  Manages the state and actions for attachments in messages and composer

  AttachmentRuntime \[#attachmentruntime]

  AttachmentPrimitive \[#attachmentprimitive]

  Manages the state and actions for individual thread list items

  ThreadListItemRuntime \[#threadlistitemruntime]

  ThreadListItem \[#threadlistitem]

Utilities \[#utilities]

URL: /docs/migrations/deprecation-policy

Stability guarantees and deprecation timelines for assistant-ui features.

assistant-ui is committed to providing a stable API, so you can spend your time building amazing things on top of it.

Rarely, we need to deprecate a feature we've already shipped, because it is causing performance, usability, or security issues.
In such cases, we will communicate the intent to unship as soon as possible by marking the feature as `@deprecated` and publishing a notice in the documentation.

Deprecations and breaking changes primarily affect new features released. The longer an API has been in the library, the less likely it is to be deprecated.
For features that have long existed in the library, we will provide a longer deprecation notice period (as described below).

Below is a list of features considered stable and those considered experimental.

Experimental Features \[#experimental-features]

These features may be removed at any time without notice.

Beta Features \[#beta-features]

A deprecation of these features will undergo a short (\<1) month deprecation notice period.

Stable Features \[#stable-features]

A deprecation of these features will undergo a long (>3 month) deprecation notice period.

The following features are considered stable:

URL: /docs/migrations/react-langgraph-v0-7

Guide to upgrading to the simplified LangGraph integration API.

Overview \[#overview]

This guide helps you migrate from the previous LangGraph integration pattern to the new simplified API introduced in `@assistant-ui/react-langgraph` v0.7. The new API consolidates thread management directly into `useLangGraphRuntime`, eliminating the need for separate runtime hooks and manual thread state management.

Key Changes \[#key-changes]

1\. Simplified Thread Management \[#1-simplified-thread-management]

The `useLangGraphRuntime` hook now directly handles thread lifecycle:

2\. New `initialize` Parameter \[#2-new-initialize-parameter]

The `stream` function now receives an `initialize` parameter that handles thread creation and loading automatically.

3\. Direct Cloud Integration \[#3-direct-cloud-integration]

Cloud persistence can now be configured directly in `useLangGraphRuntime` with the `cloud` parameter.

Migration Steps \[#migration-steps]

API Reference Changes \[#api-reference-changes]

Old API \[#old-api]

New API \[#new-api]

Benefits of the New API \[#benefits-of-the-new-api]

Common Migration Issues \[#common-migration-issues]

Issue: `threadListItemRuntime` is not defined \[#issue-threadlistitemruntime-is-not-defined]

**Solution**: Remove references to `useThreadListItemRuntime()`. Use the `initialize` parameter in the stream function instead.

Issue: Thread switching doesn't work \[#issue-thread-switching-doesnt-work]

**Solution**: Ensure you've implemented both `create` and `load` functions. The runtime needs both to manage thread lifecycle.

Issue: Cloud persistence not working \[#issue-cloud-persistence-not-working]

**Solution**: Pass the `AssistantCloud` instance directly to `useLangGraphRuntime` via the `cloud` parameter.

Example: Complete Migration \[#example-complete-migration]

Here's a complete before and after example for a typical LangGraph integration:

Before \[#before]

After \[#after]

Need Help? \[#need-help]

If you encounter issues during migration:

URL: /docs/migrations/v0-11

ContentPart renamed to MessagePart for better semantic clarity.

ContentPart renamed to MessagePart \[#contentpart-renamed-to-messagepart]

All ContentPart-related types, hooks, and components have been renamed to MessagePart for better semantic clarity and consistency.

What changed \[#what-changed]

The following types and components have been renamed:

Core Types \[#core-types]

Thread Message Parts \[#thread-message-parts]

Runtime and State Types \[#runtime-and-state-types]

Hooks \[#hooks]

Component Types \[#component-types]

Props Types \[#props-types]

Providers and Context \[#providers-and-context]

Primitives \[#primitives]

MessagePrimitive.Content renamed to MessagePrimitive.Parts \[#messageprimitivecontent-renamed-to-messageprimitiveparts]

The `MessagePrimitive.Content` component has been renamed to `MessagePrimitive.Parts` to better reflect its purpose of rendering message parts.

Migration \[#migration]

To migrate your codebase automatically, use the migration codemod:

Or run the specific migration:

Manual Migration Examples \[#manual-migration-examples]

If you prefer to migrate manually, here are some examples:

**Imports:**

**Type annotations:**

**Hooks:**

**JSX Components:**

**Providers:**

Why this change? \[#why-this-change]

The ContentPart naming was inconsistent with the rest of the codebase, where "message parts" are used throughout. This change improves semantic clarity and makes the API more intuitive by aligning terminology across the entire library.

The old ContentPart APIs have been completely removed. You must update all references to use the new MessagePart names.

URL: /docs/migrations/v0-12

Unified state API replaces individual context hooks.

Major Architecture Change: Unified State API \[#major-architecture-change-unified-state-api]

Version 0.12 introduces a complete rewrite of the state management system with a more consistent API.

Automatic Migration \[#automatic-migration]

We provide a codemod to automatically migrate your code:

This will automatically handle the hook renames and update your imports.

Breaking Changes \[#breaking-changes]

1\. Assistant API Hooks Renamed \[#1-assistant-api-hooks-renamed]

The core hooks have been renamed for consistency and clarity:

The variable naming convention has also changed from `api` to `aui`.

Migration \[#migration]

**Before:**

**After:**

**Automatic Migration:**

Run the codemod to automatically update your code:

The codemod will:

**Backwards Compatibility:**

The old names are still available as deprecated exports until v0.13:

2\. Context Hooks Replaced with Unified State API \[#2-context-hooks-replaced-with-unified-state-api]

All individual context hooks have been replaced with a single `useAuiState` hook and `useAui` for actions.

What changed \[#what-changed]

The following hooks have been removed:

**Removed Hooks:**

**Deprecated Hooks:**

Migration Examples \[#migration-examples]

**Before:**

**After:**

3\. Event Names Changed to camelCase \[#3-event-names-changed-to-camelcase]

Event names used with `useAuiEvent` have been standardized to use camelCase instead of kebab-case.

What changed \[#what-changed-1]

The following event names have been updated:

Events that remain unchanged:

Migration \[#migration-1]

**Before:**

**After:**

**Automatic Migration:**

Run the codemod to automatically update event names:

The codemod will automatically replace all occurrences of the old kebab-case event names with their new camelCase equivalents.

Getting Help \[#getting-help]

If you encounter issues during migration:

URL: /docs/migrations/v0-14

Primitives migrate from components prop to children render functions.

Children API for Primitives \[#children-api-for-primitives]

Version 0.14 replaces the `components` prop on primitives with a children render function pattern. This gives you full control over rendering with simple inline logic.

ThreadPrimitive.Messages \[#threadprimitivemessages]

**Before:**

**After:**

MessagePrimitive.Parts \[#messageprimitiveparts]

**Before:**

**After:**

`part.toolUI` and `part.dataRendererUI` \[#parttoolui-and-partdatarendererui]

Tool-call parts now expose a `toolUI` property that resolves to the registered tool UI (via `useAssistantToolUI` / `makeAssistantToolUI`) or `null` if none is registered. Data parts similarly expose `dataRendererUI`.

Returning `null` \[#returning-null]

Returning `null` from the children function renders registered tool UIs and data renderer UIs automatically via the registry. To explicitly render nothing (suppressing registered UIs), return `<></>`.

ThreadPrimitive.Suggestions \[#threadprimitivesuggestions]

**Before:**

**After:**

ThreadListPrimitive.Items \[#threadlistprimitiveitems]

**Before:**

**After:**

Attachments \[#attachments]

**Before:**

**After:**

`addResult` / `resume` on enriched part state \[#addresult--resume-on-enriched-part-state]

When using the children API, tool-call parts include `addResult` and `resume` methods directly on the part object. This means `<ToolFallback {...part} />` works without needing a wrapper component to provide these methods.

Backwards Compatibility \[#backwards-compatibility]

The `components` prop is still supported on all primitives but is deprecated and will be removed in a future version.

Getting Help \[#getting-help]

If you encounter issues during migration:

URL: /docs/runtimes/ai-sdk/v4-legacy

Legacy integration for Vercel AI SDK v4 using data stream runtime.

Overview \[#overview]

If you're using AI SDK v4 (legacy), you can integrate with assistant-ui using the `@assistant-ui/react-data-stream` package and its `useDataStreamRuntime` hook. This provides a compatible runtime that works with AI SDK v4's streaming responses.

Getting Started \[#getting-started]

Option 1: Using @assistant-ui/react-data-stream (Recommended) \[#option-1-using-assistant-uireact-data-stream-recommended]

Option 2: Using @assistant-ui/react-ai-sdk v0.1.10 (Legacy) \[#option-2-using-assistant-uireact-ai-sdk-v0110-legacy]

Alternatively, you can use the older version of the AI SDK integration package, though this version is no longer actively maintained:

With this legacy version, you would use the `useVercelUseChatRuntime` hook:

API Reference \[#api-reference]

`useDataStreamRuntime` \[#usedatastreamruntime]

The `useDataStreamRuntime` hook creates a runtime compatible with assistant-ui from AI SDK v4's streaming responses.

Options \[#options]

The `useDataStreamRuntime` hook accepts options similar to AI SDK v4's `useChat` hook:

Migration to AI SDK v6 \[#migration-to-ai-sdk-v6]

When you're ready to upgrade to AI SDK v6:

See our [AI SDK v6 documentation](/docs/runtimes/ai-sdk/v6) for the complete migration guide.

Example \[#example]

For a working example with AI SDK v4, you can adapt the patterns from our [AI SDK examples](https://github.com/assistant-ui/assistant-ui/tree/main/examples) using the `@assistant-ui/react-data-stream` package instead of the v6 integration.

URL: /docs/runtimes/ai-sdk/v5-legacy

Integrate Vercel AI SDK v5 with useChatRuntime for streaming chat.

Overview \[#overview]

This documentation is preserved for reference. For new projects, use [AI SDK v6](/docs/runtimes/ai-sdk/v6).

Getting Started \[#getting-started]

Key Differences from v6 \[#key-differences-from-v6]

Migration to v6 \[#migration-to-v6]

See the [AI SDK v6 documentation](/docs/runtimes/ai-sdk/v6) for the latest integration guide.

URL: /docs/runtimes/ai-sdk/v6

Integrate Vercel AI SDK v6 with assistant-ui for streaming chat.

Overview \[#overview]

Integration with the Vercel AI SDK v6 using the `useChatRuntime` hook from `@assistant-ui/react-ai-sdk`.

Getting Started \[#getting-started]

Tracking Token Usage \[#tracking-token-usage]

assistant-ui exports a `useThreadTokenUsage` hook to access thread-level token usage on the client.

Key Changes from v5 \[#key-changes-from-v5]

API Reference \[#api-reference]

useChatRuntime \[#usechatruntime]

Creates a runtime integrated with AI SDK's `useChat` hook.

Custom API URL \[#custom-api-url]

To use a different endpoint, pass a custom `AssistantChatTransport`:

System Messages and Frontend Tools \[#system-messages-and-frontend-tools]

`AssistantChatTransport` (used by default) automatically forwards system messages and frontend tools to your backend. To consume them, update your backend route:

Backend route with system/tools forwarding:

useAISDKRuntime (Advanced) \[#useaisdkruntime-advanced]

For advanced use cases where you need direct access to the `useChat` hook:

Example \[#example]

For a complete example, check out the [AI SDK v6 example](https://github.com/assistant-ui/assistant-ui/tree/main/examples/with-ai-sdk-v6) in our repository.

URL: /docs/runtimes/a2a

Connect to A2A (Agent-to-Agent) v1.0 protocol servers.

`@assistant-ui/react-a2a` provides a runtime adapter for the [A2A (Agent-to-Agent) v1.0 protocol](https://github.com/a2aproject/A2A), enabling your assistant-ui frontend to communicate with any A2A-compliant agent server.

Requirements \[#requirements]

Installation \[#installation]

Getting Started \[#getting-started]

A2AClient \[#a2aclient]

The built-in `A2AClient` handles all communication with the A2A server, including JSON serialization, SSE streaming, ProtoJSON enum normalization, and structured error handling.

You can pass a pre-built client to `useA2ARuntime`:

Client Options \[#client-options]

Client Methods \[#client-methods]

useA2ARuntime Options \[#usea2aruntime-options]

Hooks \[#hooks]

useA2ATask \[#usea2atask]

Returns the current A2A task object, including task state and status message.

useA2AArtifacts \[#usea2aartifacts]

Returns the artifacts generated by the current task.

useA2AAgentCard \[#usea2aagentcard]

Returns the agent card fetched from the server on initialization.

Task States \[#task-states]

The A2A protocol defines 9 task states. The runtime maps them to assistant-ui message statuses:

Artifacts \[#artifacts]

A2A agents can produce artifacts (files, code, data) alongside their responses. Artifacts are accumulated during streaming and accessible via the `useA2AArtifacts` hook.

The runtime supports:

Streaming vs Non-Streaming \[#streaming-vs-non-streaming]

The runtime automatically selects the communication mode based on the agent's capabilities:

Error Handling \[#error-handling]

The client throws `A2AError` instances with structured error information following the `google.rpc.Status` format:

Multi-Tenancy \[#multi-tenancy]

For multi-tenant A2A servers, pass a `tenant` option to the client:

This prepends `/{tenant}` to all API paths (e.g. `/my-org/message:send`).

Features \[#features]

URL: /docs/runtimes/custom/custom-thread-list

Plug a custom thread database for multi-thread persistence.

Overview \[#overview]

`useRemoteThreadListRuntime` lets you plug a custom thread database into assistant-ui. It keeps the UI and local runtime logic in sync while you provide persistence, archiving, and metadata for every conversation.

When to Use \[#when-to-use]

Use a Custom Thread List when you need to:

How It Works \[#how-it-works]

Custom Thread List merges two pieces of state:

When the hook mounts it calls `list()` on your adapter, hydrates existing threads, and uses your runtime hook to spawn a runtime whenever a thread is opened. Creating a new conversation calls `initialize(threadId)` so you can create a record server-side and return the canonical `remoteId`.

Build a Custom Thread List \[#build-a-custom-thread-list]

Adapter Responsibilities \[#adapter-responsibilities]

<ParametersTable
  type="RemoteThreadListAdapter"
  parameters="[
{
name: &#x22;list&#x22;,
type: &#x22;() => Promise<{ threads: RemoteThreadMetadata[] }>&#x22;,
description:
&#x22;Return the current threads. Each thread must include status, remoteId, and any metadata you want to show immediately.&#x22;,
required: true,
},
{
name: &#x22;initialize&#x22;,
type: &#x22;(localId: string) => Promise<{ remoteId: string; externalId?: string }>&#x22;,
description:
&#x22;Create a new remote record when the user starts a conversation. Return the canonical ids so later operations target the right thread.&#x22;,
required: true,
},
{
name: &#x22;rename&#x22;,
type: &#x22;(remoteId: string, title: string) => Promise<void>&#x22;,
description: &#x22;Persist title changes triggered from the UI.&#x22;,
required: true,
},
{
name: &#x22;archive&#x22;,
type: &#x22;(remoteId: string) => Promise<void>&#x22;,
description: &#x22;Mark the thread as archived in your system.&#x22;,
required: true,
},
{
name: &#x22;unarchive&#x22;,
type: &#x22;(remoteId: string) => Promise<void>&#x22;,
description: &#x22;Restore an archived thread to the active list.&#x22;,
required: true,
},
{
name: &#x22;delete&#x22;,
type: &#x22;(remoteId: string) => Promise<void>&#x22;,
description: &#x22;Permanently remove the thread and stop rendering it.&#x22;,
required: true,
},
{
name: &#x22;generateTitle&#x22;,
type: &#x22;(remoteId: string, unstable_messages: readonly ThreadMessage[]) => Promise<AssistantStream>&#x22;,
description:
&#x22;Return a streaming title generator. You can reuse your model endpoint or queue a background job.&#x22;,
required: true,
},
{
name: &#x22;fetch&#x22;,
type: &#x22;(threadId: string) => Promise<RemoteThreadMetadata>&#x22;,
description:
&#x22;Fetch metadata for a specific thread. Used when switching to a thread not in the initial list.&#x22;,
required: true,
},
{
name: &#x22;unstable_Provider&#x22;,
type: &#x22;ComponentType<PropsWithChildren>&#x22;,
description:
&#x22;Optional wrapper rendered around all thread runtimes. Use it to inject adapters such as history or attachments (see the Cloud adapter).&#x22;,
},
]"
/>

Thread Lifecycle Cheatsheet \[#thread-lifecycle-cheatsheet]

Avoiding Race Conditions in History Adapters \[#avoiding-race-conditions-in-history-adapters]

If you're building a history adapter that persists messages to your own database, use `aui.threadListItem().initialize()` to ensure the thread is fully initialized before saving:

The `initialize()` method:

See `AssistantCloudThreadHistoryAdapter` in the source code for a production-ready reference implementation.

Optional Adapters \[#optional-adapters]

If you need history or attachment support, expose them via `unstable_Provider`. The cloud implementation wraps each thread runtime with `RuntimeAdapterProvider` to inject:

Reuse that pattern to register any capability your runtime requires.

URL: /docs/runtimes/custom/external-store

Bring your own Redux, Zustand, or state manager.

Overview \[#overview]

`ExternalStoreRuntime` bridges your existing state management with assistant-ui components. It requires an `ExternalStoreAdapter<TMessage>` that handles communication between your state and the UI.

**Key differences from `LocalRuntime`:**

Example Implementation \[#example-implementation]

When to Use \[#when-to-use]

Use `ExternalStoreRuntime` if you need:

Key Features \[#key-features]

Architecture \[#architecture]

How It Works \[#how-it-works]

`ExternalStoreRuntime` acts as a bridge between your state management and assistant-ui:

Key Concepts \[#key-concepts]

Getting Started \[#getting-started]

Implementation Patterns \[#implementation-patterns]

Message Conversion \[#message-conversion]

Two approaches for converting your message format:

1\. Simple Conversion (Recommended) \[#1-simple-conversion-recommended]

2\. Advanced Conversion with `useExternalMessageConverter` \[#2-advanced-conversion-with-useexternalmessageconverter]

For complex scenarios with performance optimization:

Join Strategy \[#join-strategy]

Controls how adjacent assistant messages are combined:

This is useful when your backend sends multiple message chunks that should appear as a single message in the UI.

Essential Handlers \[#essential-handlers]

Basic Chat (onNew only) \[#basic-chat-onnew-only]

Full-Featured Chat \[#full-featured-chat]

Streaming Responses \[#streaming-responses]

Implement real-time streaming with progressive updates:

Message Editing \[#message-editing]

Enable message editing by implementing the `onEdit` handler:

Tool Calling \[#tool-calling]

Support tool calls with proper result handling:

Automatic Tool Result Matching \[#automatic-tool-result-matching]

The runtime automatically matches tool results with their corresponding tool calls. When messages are converted and joined:

File Attachments \[#file-attachments]

Enable file uploads with the attachment adapter:

Thread Management \[#thread-management]

Managing Thread Context \[#managing-thread-context]

When implementing multi-thread support with `ExternalStoreRuntime`, you need to carefully manage thread context across your application. Here's a comprehensive approach:

Complete Thread Implementation \[#complete-thread-implementation]

Here's a full implementation with proper context management:

Thread Context Best Practices \[#thread-context-best-practices]

Integration Examples \[#integration-examples]

Redux Integration \[#redux-integration]

Zustand Integration (v5) \[#zustand-integration-v5]

TanStack Query Integration \[#tanstack-query-integration]

Key Features \[#key-features-1]

Automatic Optimistic Updates \[#automatic-optimistic-updates]

When `isRunning` becomes true, the runtime automatically shows an optimistic assistant message:

Message Status Management \[#message-status-management]

Assistant messages get automatic status updates:

Tool Result Matching \[#tool-result-matching]

The runtime automatically matches tool results with their calls:

Working with External Messages \[#working-with-external-messages]

Converting Back to Your Format \[#converting-back-to-your-format]

Use `getExternalStoreMessages` to access your original messages:

Message part Access \[#message-part-access]

Binding External Messages Manually \[#binding-external-messages-manually]

Use `bindExternalStoreMessage` to attach your original message to a `ThreadMessage` or message part object. This is useful when you construct `ThreadMessage` objects yourself (outside of the built-in message converter) and want `getExternalStoreMessages` to work with them.

`bindExternalStoreMessage` is a no-op if the target already has a bound message. It mutates the target object in place.

Debugging \[#debugging]

Common Debugging Scenarios \[#common-debugging-scenarios]

Best Practices \[#best-practices]

1\. Immutable Updates \[#1-immutable-updates]

Always create new arrays when updating messages:

2\. Stable Handler References \[#2-stable-handler-references]

Memoize handlers to prevent runtime recreation:

3\. Performance Optimization \[#3-performance-optimization]

`LocalRuntime` vs `ExternalStoreRuntime` \[#localruntime-vs-externalstoreruntime]

When to Choose Which \[#when-to-choose-which]

Feature Comparison \[#feature-comparison]

Common Pitfalls \[#common-pitfalls]

Debugging Checklist \[#debugging-checklist]

Thread-Specific Debugging \[#thread-specific-debugging]

Common thread context issues and solutions:

**Messages disappearing when switching threads:**

**Thread list not updating:**

**Messages going to wrong thread:**

API Reference \[#api-reference]

`ExternalStoreAdapter` \[#externalstoreadapter]

The main interface for connecting your state to assistant-ui.

<ParametersTable
  type="ExternalStoreAdapter<T>"
  parameters="[
{
name: &#x22;messages&#x22;,
type: &#x22;readonly T[]&#x22;,
description: &#x22;Array of messages from your state&#x22;,
required: true,
},
{
name: &#x22;onNew&#x22;,
type: &#x22;(message: AppendMessage) => Promise<void>&#x22;,
description: &#x22;Handler for new messages from the user&#x22;,
required: true,
},
{
name: &#x22;isRunning&#x22;,
type: &#x22;boolean&#x22;,
description:
&#x22;Whether the assistant is currently generating a response. When true, shows optimistic assistant message&#x22;,
default: &#x22;false&#x22;,
},
{
name: &#x22;isDisabled&#x22;,
type: &#x22;boolean&#x22;,
description: &#x22;Whether the chat input should be disabled&#x22;,
default: &#x22;false&#x22;,
},
{
name: &#x22;suggestions&#x22;,
type: &#x22;readonly ThreadSuggestion[]&#x22;,
description: &#x22;Suggested prompts to display&#x22;,
},
{
name: &#x22;extras&#x22;,
type: &#x22;unknown&#x22;,
description: &#x22;Additional data accessible via runtime.extras&#x22;,
},
{
name: &#x22;setMessages&#x22;,
type: &#x22;(messages: readonly T[]) => void&#x22;,
description: &#x22;Update messages (required for branch switching)&#x22;,
},
{
name: &#x22;onEdit&#x22;,
type: &#x22;(message: AppendMessage) => Promise<void>&#x22;,
description: &#x22;Handler for message edits (required for edit feature)&#x22;,
},
{
name: &#x22;onReload&#x22;,
type: &#x22;(parentId: string | null, config: StartRunConfig) => Promise<void>&#x22;,
description:
&#x22;Handler for regenerating messages (required for reload feature)&#x22;,
},
{
name: &#x22;onCancel&#x22;,
type: &#x22;() => Promise<void>&#x22;,
description: &#x22;Handler for cancelling the current generation&#x22;,
},
{
name: &#x22;onAddToolResult&#x22;,
type: &#x22;(options: AddToolResultOptions) => Promise<void> | void&#x22;,
description: &#x22;Handler for adding tool call results&#x22;,
},
{
name: &#x22;onResume&#x22;,
type: &#x22;(config: ResumeRunConfig) => Promise<void>&#x22;,
description:
&#x22;Handler for resuming an interrupted run (e.g. after a page reload mid-generation)&#x22;,
},
{
name: &#x22;onResumeToolCall&#x22;,
type: &#x22;(options: { toolCallId: string; payload: unknown }) => void&#x22;,
description:
&#x22;Handler for resuming a suspended tool call (used with human-in-the-loop tool execution)&#x22;,
},
{
name: &#x22;isLoading&#x22;,
type: &#x22;boolean&#x22;,
description:
&#x22;Whether the adapter is in a loading state (e.g. initial data fetch). Displays a loading indicator instead of the composer&#x22;,
},
{
name: &#x22;messageRepository&#x22;,
type: &#x22;ExportedMessageRepository&#x22;,
description:
&#x22;Pre-built message repository with branching history. Use instead of `messages` when you need to restore branch state&#x22;,
},
{
name: &#x22;state&#x22;,
type: &#x22;ReadonlyJSONValue&#x22;,
description:
&#x22;Opaque serializable state passed to `onLoadExternalState` during thread import&#x22;,
},
{
name: &#x22;onImport&#x22;,
type: &#x22;(messages: readonly ThreadMessage[]) => void&#x22;,
description:
&#x22;Called when the runtime imports messages into the external store (e.g. on thread switch)&#x22;,
},
{
name: &#x22;onExportExternalState&#x22;,
type: &#x22;() => any&#x22;,
description:
&#x22;Called to retrieve external state when the runtime exports a thread snapshot&#x22;,
},
{
name: &#x22;onLoadExternalState&#x22;,
type: &#x22;(state: any) => void&#x22;,
description:
&#x22;Called with previously exported external state when restoring a thread snapshot&#x22;,
},
{
name: &#x22;convertMessage&#x22;,
type: &#x22;(message: T, index: number) => ThreadMessageLike&#x22;,
description:
&#x22;Convert your message format to assistant-ui format. Not needed if using ThreadMessage type&#x22;,
},
{
name: &#x22;adapters&#x22;,
type: &#x22;object&#x22;,
description: &#x22;Feature adapters (same as LocalRuntime)&#x22;,
children: [
{
type: &#x22;adapters&#x22;,
parameters: [
{
name: &#x22;attachments&#x22;,
type: &#x22;AttachmentAdapter&#x22;,
description: &#x22;Enable file attachments&#x22;,
},
{
name: &#x22;speech&#x22;,
type: &#x22;SpeechSynthesisAdapter&#x22;,
description: &#x22;Enable text-to-speech&#x22;,
},
{
name: &#x22;dictation&#x22;,
type: &#x22;DictationAdapter&#x22;,
description: &#x22;Enable speech-to-text dictation&#x22;,
},
{
name: &#x22;feedback&#x22;,
type: &#x22;FeedbackAdapter&#x22;,
description: &#x22;Enable message feedback&#x22;,
},
{
name: &#x22;threadList&#x22;,
type: &#x22;ExternalStoreThreadListAdapter&#x22;,
description: &#x22;Enable multi-thread management&#x22;,
},
],
},
],
},
{
name: &#x22;unstable_capabilities&#x22;,
type: &#x22;object&#x22;,
description: &#x22;Configure runtime capabilities&#x22;,
children: [
{
type: &#x22;unstable_capabilities&#x22;,
parameters: [
{
name: &#x22;copy&#x22;,
type: &#x22;boolean&#x22;,
description: &#x22;Enable message copy feature&#x22;,
default: &#x22;true&#x22;,
},
],
},
],
},
]"
/>

`ThreadMessageLike` \[#threadmessagelike]

A flexible message format that can be converted to assistant-ui's internal format.

<ParametersTable
  type="ThreadMessageLike"
  parameters="[
{
name: &#x22;role&#x22;,
type: '&#x22;assistant&#x22; | &#x22;user&#x22; | &#x22;system&#x22;',
description: &#x22;The role of the message sender&#x22;,
required: true,
},
{
name: &#x22;content&#x22;,
type: &#x22;string | readonly MessagePart[]&#x22;,
description: &#x22;Message content as string or structured message parts. Supports `data-*` prefixed types (e.g. `{ type: \&#x22;data-workflow\&#x22;, data: {...} }`) which are automatically converted to DataMessagePart.&#x22;,
required: true,
},
{
name: &#x22;id&#x22;,
type: &#x22;string&#x22;,
description: &#x22;Unique identifier for the message&#x22;,
},
{
name: &#x22;createdAt&#x22;,
type: &#x22;Date&#x22;,
description: &#x22;Timestamp when the message was created&#x22;,
},
{
name: &#x22;status&#x22;,
type: &#x22;MessageStatus&#x22;,
description:
&#x22;Status of assistant messages ({ type: \&#x22;running\&#x22; }, { type: \&#x22;complete\&#x22; }, { type: \&#x22;incomplete\&#x22; })&#x22;,
},
{
name: &#x22;attachments&#x22;,
type: &#x22;readonly CompleteAttachment[]&#x22;,
description: &#x22;File attachments (user messages only). Attachment `type` accepts custom strings beyond \&#x22;image\&#x22; | \&#x22;document\&#x22; | \&#x22;file\&#x22;, and `contentType` is optional.&#x22;,
},
{
name: &#x22;metadata&#x22;,
type: &#x22;object&#x22;,
description: &#x22;Additional message metadata&#x22;,
children: [
{
type: &#x22;metadata&#x22;,
parameters: [
{
name: &#x22;steps&#x22;,
type: &#x22;readonly ThreadStep[]&#x22;,
description: &#x22;Tool call steps for assistant messages&#x22;,
},
{
name: &#x22;custom&#x22;,
type: &#x22;Record<string, unknown>&#x22;,
description: &#x22;Custom metadata for your application&#x22;,
},
],
},
],
},
]"
/>

`ExternalStoreThreadListAdapter` \[#externalstorethreadlistadapter]

Enable multi-thread support with custom thread management.

<ParametersTable
  type="ExternalStoreThreadListAdapter"
  parameters="[
{
name: &#x22;threadId&#x22;,
type: &#x22;string&#x22;,
description:
&#x22;ID of the current active thread. **Deprecated** — this API is still under active development and might change without notice.&#x22;,
},
{
name: &#x22;isLoading&#x22;,
type: &#x22;boolean&#x22;,
description: &#x22;Whether the thread list is currently loading&#x22;,
},
{
name: &#x22;threads&#x22;,
type: &#x22;readonly ExternalStoreThreadData<\&#x22;regular\&#x22;>[]&#x22;,
description: &#x22;Array of active threads. Each entry is an `ExternalStoreThreadData` object.&#x22;,
},
{
name: &#x22;archivedThreads&#x22;,
type: &#x22;readonly ExternalStoreThreadData<\&#x22;archived\&#x22;>[]&#x22;,
description: &#x22;Array of archived threads. Each entry is an `ExternalStoreThreadData` object.&#x22;,
},
{
name: &#x22;onSwitchToNewThread&#x22;,
type: &#x22;() => Promise<void> | void&#x22;,
description:
&#x22;Handler for creating a new thread. **Deprecated** — this API is still under active development and might change without notice.&#x22;,
},
{
name: &#x22;onSwitchToThread&#x22;,
type: &#x22;(threadId: string) => Promise<void> | void&#x22;,
description:
&#x22;Handler for switching to an existing thread. **Deprecated** — this API is still under active development and might change without notice.&#x22;,
},
{
name: &#x22;onRename&#x22;,
type: &#x22;(threadId: string, newTitle: string) => Promise<void> | void&#x22;,
description: &#x22;Handler for renaming a thread&#x22;,
},
{
name: &#x22;onArchive&#x22;,
type: &#x22;(threadId: string) => Promise<void> | void&#x22;,
description: &#x22;Handler for archiving a thread&#x22;,
},
{
name: &#x22;onUnarchive&#x22;,
type: &#x22;(threadId: string) => Promise<void> | void&#x22;,
description: &#x22;Handler for unarchiving a thread&#x22;,
},
{
name: &#x22;onDelete&#x22;,
type: &#x22;(threadId: string) => Promise<void> | void&#x22;,
description: &#x22;Handler for deleting a thread&#x22;,
},
]"
/>

`ExternalStoreThreadData` \[#externalstorethreaddata]

Represents a single thread entry in the thread list.

<ParametersTable
  type="ExternalStoreThreadData<TState>"
  parameters="[
{
name: &#x22;id&#x22;,
type: &#x22;string&#x22;,
description: &#x22;Unique local identifier for the thread&#x22;,
required: true,
},
{
name: &#x22;status&#x22;,
type: '&#x22;regular&#x22; | &#x22;archived&#x22;',
description: &#x22;Whether the thread is active or archived&#x22;,
required: true,
},
{
name: &#x22;title&#x22;,
type: &#x22;string&#x22;,
description: &#x22;Display title for the thread&#x22;,
},
{
name: &#x22;remoteId&#x22;,
type: &#x22;string&#x22;,
description: &#x22;Remote/server-side identifier for the thread (used for persistence)&#x22;,
},
{
name: &#x22;externalId&#x22;,
type: &#x22;string&#x22;,
description: &#x22;External system identifier for the thread (e.g. from a third-party service)&#x22;,
},
]"
/>

Related Runtime APIs \[#related-runtime-apis]

Related Resources \[#related-resources]

URL: /docs/runtimes/custom/local

Quickest path to a working chat. Handles state while you handle the API.

Overview \[#overview]

`LocalRuntime` is the simplest way to connect your own custom backend to assistant-ui. It manages all chat state internally while providing a clean adapter interface to connect with any REST API, OpenAI, or custom language model.

`LocalRuntime` provides:

While LocalRuntime manages state in-memory by default, it offers multiple persistence options through adapters - use the history adapter for single-thread persistence, Assistant Cloud for managed multi-thread support, or implement your own storage with `useRemoteThreadListRuntime`.

When to Use \[#when-to-use]

Use `LocalRuntime` if you need:

Key Features \[#key-features]

Getting Started \[#getting-started]

Streaming Responses \[#streaming-responses]

Implement streaming by declaring the `run` function as an `AsyncGenerator`.

Streaming with Tool Calls \[#streaming-with-tool-calls]

Handle streaming responses that include function calls:

Tool Calling \[#tool-calling]

`LocalRuntime` supports OpenAI-compatible function calling with automatic or human-in-the-loop execution.

Basic Tool Definition \[#basic-tool-definition]

Tools should be registered using the `Tools()` API with `useAui()`:

The tools will be available to your adapter via the `context` parameter in the `run` function. See the [Tools guide](/docs/guides/tools) for more details on tool registration and advanced features.

Human-in-the-Loop Approval \[#human-in-the-loop-approval]

Require user confirmation before executing certain tools:

Tool Execution \[#tool-execution]

Tools are executed automatically by the runtime. The model adapter receives tool results in subsequent messages:

Multi-Thread Support \[#multi-thread-support]

`LocalRuntime` supports multiple conversation threads through two approaches:

1\. Assistant Cloud Integration \[#1-assistant-cloud-integration]

With Assistant Cloud, you get:

2\. Custom Database with useRemoteThreadListRuntime \[#2-custom-database-with-useremotethreadlistruntime]

For custom thread storage, use `useRemoteThreadListRuntime` with your own adapter:

Understanding the Architecture \[#understanding-the-architecture]

The complete multi-thread implementation requires:

Without the history adapter, threads would have no message persistence, making them effectively useless. The Provider pattern allows you to add thread-specific functionality while keeping the runtime creation simple.

  See `AssistantCloudThreadHistoryAdapter` in the source for a production reference.
</Callout>

Database Schema Example \[#database-schema-example]

Both approaches provide full multi-thread support. Choose Assistant Cloud for a managed solution or implement your own adapter for custom storage requirements.

Adapters \[#adapters]

Extend `LocalRuntime` capabilities with adapters. The runtime automatically enables/disables UI features based on which adapters are provided.

Attachment Adapter \[#attachment-adapter]

Enable file and image uploads:

Thread History Adapter \[#thread-history-adapter]

Persist and resume conversations:

Speech Synthesis Adapter \[#speech-synthesis-adapter]

Add text-to-speech capabilities:

Feedback Adapter \[#feedback-adapter]

Collect user feedback on messages:

Suggestion Adapter \[#suggestion-adapter]

Provide follow-up suggestions:

Advanced Features \[#advanced-features]

Resuming a Run \[#resuming-a-run]

`resumeRun` reconnects to an in-progress or interrupted assistant run. This is essential for scenarios like:

How it works \[#how-it-works]

When you call `resumeRun`, the local runtime:

Unlike `startRun` (which uses the ChatModelAdapter), `resumeRun` **requires** a `stream` parameter — you provide the async generator that produces the response.

Basic example \[#basic-example]

Reconnecting to a backend stream \[#reconnecting-to-a-backend-stream]

A common pattern is checking whether the backend is still running, then reconnecting:

ChatModelRunResult \[#chatmodelrunresult]

Each value yielded by the stream is a `ChatModelRunResult`:

The stream should yield the **full cumulative content** on each iteration (not deltas). Each yield replaces the previous content of the assistant message.

Custom Thread Management \[#custom-thread-management]

Access thread actions for advanced control with `useAui`:

Integration Examples \[#integration-examples]

OpenAI Integration \[#openai-integration]

Custom REST API Integration \[#custom-rest-api-integration]

Best Practices \[#best-practices]

Comparison with `ExternalStoreRuntime` \[#comparison-with-externalstoreruntime]

Troubleshooting \[#troubleshooting]

Common Issues \[#common-issues]

Tool UI Flickers or Disappears During Streaming \[#tool-ui-flickers-or-disappears-during-streaming]

A common issue when implementing a streaming `ChatModelAdapter` is seeing a tool's UI appear for a moment and then disappear. This is caused by failing to accumulate the `tool_calls` correctly across multiple stream chunks. State must be stored **outside** the streaming loop to persist.

**❌ Incorrect: Forgetting Previous Tool Calls**

This implementation incorrectly re-creates the `content` array for every chunk. If a later chunk contains only text, tool calls from previous chunks are lost, causing the UI to disappear.

**✅ Correct: Accumulating State**

This implementation uses a `Map` outside the loop to remember all tool calls.

Debug Tips \[#debug-tips]

API Reference \[#api-reference]

`ChatModelAdapter` \[#chatmodeladapter]

The main interface for connecting your API to `LocalRuntime`.

<ParametersTable
  type="ChatModelAdapter"
  parameters="[
{
name: &#x22;run&#x22;,
type: &#x22;ChatModelRunOptions => ChatModelRunResult | AsyncGenerator<ChatModelRunResult>&#x22;,
description:
&#x22;Function that sends messages to your API and returns the response&#x22;,
required: true,
},
]"
/>

`ChatModelRunOptions` \[#chatmodelrunoptions]

Parameters passed to the `run` function.

<ParametersTable
  type="ChatModelRunOptions"
  parameters="[
{
name: &#x22;messages&#x22;,
type: &#x22;readonly ThreadMessage[]&#x22;,
description: &#x22;The conversation history to send to your API&#x22;,
required: true,
},
{
name: &#x22;runConfig&#x22;,
type: &#x22;RunConfig&#x22;,
description: &#x22;Run configuration with optional custom metadata. `RunConfig` is `{ readonly custom?: Record<string, unknown> }`.&#x22;,
required: true,
},
{
name: &#x22;abortSignal&#x22;,
type: &#x22;AbortSignal&#x22;,
description: &#x22;Signal to cancel the request if user interrupts&#x22;,
required: true,
},
{
name: &#x22;context&#x22;,
type: &#x22;ModelContext&#x22;,
description: &#x22;Additional context including configuration and tools&#x22;,
required: true,
},
{
name: &#x22;unstable_assistantMessageId&#x22;,
type: &#x22;string | undefined&#x22;,
description: &#x22;The ID of the assistant message being generated. Useful for tracking or updating specific messages.&#x22;,
},
{
name: &#x22;unstable_threadId&#x22;,
type: &#x22;string | undefined&#x22;,
description: &#x22;The current thread/conversation identifier. Useful for passing to your backend API.&#x22;,
},
{
name: &#x22;unstable_parentId&#x22;,
type: &#x22;string | null | undefined&#x22;,
description: &#x22;The ID of the parent message this response is replying to. `null` if this is the first message in the thread.&#x22;,
},
{
name: &#x22;unstable_getMessage&#x22;,
type: &#x22;() => ThreadMessage&#x22;,
description: &#x22;Returns the current assistant message being generated. Useful for accessing message state during streaming.&#x22;,
},
{
name: &#x22;config&#x22;,
type: &#x22;ModelContext&#x22;,
description: &#x22;Deprecated. Renamed to `context`. Additional context including configuration and tools.&#x22;,
},
]"
/>

`LocalRuntimeOptions` \[#localruntimeoptions]

Configuration options for the `LocalRuntime`.

<ParametersTable
  type="LocalRuntimeOptions"
  parameters="[
{
name: &#x22;initialMessages&#x22;,
type: &#x22;readonly ThreadMessageLike[]&#x22;,
description: &#x22;Pre-populate the thread with messages&#x22;,
},
{
name: &#x22;maxSteps&#x22;,
type: &#x22;number&#x22;,
description:
&#x22;Maximum number of sequential tool calls before requiring user input&#x22;,
default: &#x22;2&#x22;,
},
{
name: &#x22;cloud&#x22;,
type: &#x22;AssistantCloud&#x22;,
description:
&#x22;Enable Assistant Cloud integration for multi-thread support and persistence&#x22;,
},
{
name: &#x22;adapters&#x22;,
type: &#x22;LocalRuntimeAdapters&#x22;,
description:
&#x22;Additional capabilities through adapters. Features are automatically enabled based on provided adapters&#x22;,
children: [
{
type: &#x22;adapters&#x22;,
parameters: [
{
name: &#x22;attachments&#x22;,
type: &#x22;AttachmentAdapter&#x22;,
description: &#x22;Enable file/image attachments&#x22;,
},
{
name: &#x22;speech&#x22;,
type: &#x22;SpeechSynthesisAdapter&#x22;,
description: &#x22;Enable text-to-speech for messages&#x22;,
},
{
name: &#x22;dictation&#x22;,
type: &#x22;DictationAdapter&#x22;,
description: &#x22;Enable speech-to-text dictation&#x22;,
},
{
name: &#x22;feedback&#x22;,
type: &#x22;FeedbackAdapter&#x22;,
description: &#x22;Enable message feedback (thumbs up/down)&#x22;,
},
{
name: &#x22;history&#x22;,
type: &#x22;ThreadHistoryAdapter&#x22;,
description: &#x22;Enable thread persistence and resumption&#x22;,
},
{
name: &#x22;suggestion&#x22;,
type: &#x22;SuggestionAdapter&#x22;,
description: &#x22;Enable follow-up suggestions&#x22;,
},
],
},
],
},
{
name: &#x22;unstable_humanToolNames&#x22;,
type: &#x22;string[]&#x22;,
description:
&#x22;Tool names that require human approval before execution (experimental API)&#x22;,
},
]"
/>

`RemoteThreadListAdapter` \[#remotethreadlistadapter]

Interface for implementing custom thread list storage.

<ParametersTable
  type="RemoteThreadListAdapter"
  parameters="[
{
name: &#x22;list&#x22;,
type: &#x22;() => Promise<RemoteThreadListResponse>&#x22;,
description: &#x22;Returns list of all threads (regular and archived)&#x22;,
required: true,
},
{
name: &#x22;initialize&#x22;,
type: &#x22;(threadId: string) => Promise<RemoteThreadInitializeResponse>&#x22;,
description: &#x22;Creates a new thread with the given ID&#x22;,
required: true,
},
{
name: &#x22;rename&#x22;,
type: &#x22;(remoteId: string, newTitle: string) => Promise<void>&#x22;,
description: &#x22;Updates the title of a thread&#x22;,
required: true,
},
{
name: &#x22;archive&#x22;,
type: &#x22;(remoteId: string) => Promise<void>&#x22;,
description: &#x22;Archives a thread&#x22;,
required: true,
},
{
name: &#x22;unarchive&#x22;,
type: &#x22;(remoteId: string) => Promise<void>&#x22;,
description: &#x22;Unarchives a thread&#x22;,
required: true,
},
{
name: &#x22;delete&#x22;,
type: &#x22;(remoteId: string) => Promise<void>&#x22;,
description: &#x22;Deletes a thread permanently&#x22;,
required: true,
},
{
name: &#x22;generateTitle&#x22;,
type: &#x22;(remoteId: string, unstable_messages: readonly ThreadMessage[]) => Promise<AssistantStream>&#x22;,
description: &#x22;Generates a title for the thread based on the conversation&#x22;,
required: true,
},
{
name: &#x22;fetch&#x22;,
type: &#x22;(threadId: string) => Promise<RemoteThreadMetadata>&#x22;,
description: &#x22;Fetches metadata for a specific thread&#x22;,
required: true,
},
{
name: &#x22;unstable_Provider&#x22;,
type: &#x22;(...args: any[]) => unknown&#x22;,
description: &#x22;Optional React provider component to wrap the runtime context&#x22;,
},
]"
/>

Related Runtime APIs \[#related-runtime-apis]

Related Resources \[#related-resources]

URL: /docs/runtimes/google-adk

Connect to Google ADK (Agent Development Kit) agents with streaming, tool calls, and multi-agent support.

The `@assistant-ui/react-google-adk` package provides integration with [Google ADK JS](https://github.com/google/adk-js), Google's official agent framework for TypeScript. It supports streaming text, tool calls, multi-agent orchestration, code execution, session state, tool confirmations, auth flows, and more.

Requirements \[#requirements]

You need a Google ADK agent running on a server. ADK supports `LlmAgent` with Gemini models, tool use, multi-agent orchestration (sequential, parallel, loop agents), and session management.

Installation \[#installation]

Getting Started \[#getting-started]

`createAdkStream` \[#createadkstream]

Creates an `AdkStreamCallback` that connects to an ADK endpoint via SSE. Supports two modes:

**Proxy mode** — POST to your own API route:

**Direct mode** — connect directly to an ADK server:

Direct ADK Server Connection \[#direct-adk-server-connection]

When connecting directly to an ADK server (without a proxy API route), use `createAdkSessionAdapter` to back your thread list with ADK sessions:

The session adapter maps ADK sessions to assistant-ui threads:

Server Helpers \[#server-helpers]

`createAdkApiRoute` \[#createadkapiroute]

One-liner API route handler that combines request parsing and SSE streaming:

Both `userId` and `sessionId` accept a static string or a function `(req: Request) => string` for dynamic resolution (e.g. from cookies, headers, or query params).

`adkEventStream` \[#adkeventstream]

Converts an `AsyncGenerator<Event>` from ADK's `Runner.runAsync()` into an SSE `Response`. Sends an initial `:ok` comment to keep connections alive through proxies.

`parseAdkRequest` / `toAdkContent` \[#parseadkrequest--toadkcontent]

Lower-level helpers for custom API routes. Parse incoming requests and convert to ADK's `Content` format. Supports user messages, tool results, `stateDelta`, `checkpointId`, and multimodal content:

Hooks \[#hooks]

Agent & Session State \[#agent--session-state]

Tool Confirmations \[#tool-confirmations]

When ADK's `SecurityPlugin` or tool callbacks request user confirmation before executing a tool, use `useAdkToolConfirmations` to read pending requests and `useAdkConfirmTool` to respond:

Auth Requests \[#auth-requests]

When a tool requires OAuth or other authentication, use `useAdkAuthRequests` to read pending requests and `useAdkSubmitAuth` to submit credentials:

`AdkAuthCredential` supports all ADK auth types: `apiKey`, `http`, `oauth2`, `openIdConnect`, `serviceAccount`.

Artifacts \[#artifacts]

Track file artifacts created or modified by the agent:

Artifact Fetching \[#artifact-fetching]

When using `createAdkSessionAdapter`, the returned `artifacts` object provides functions to fetch artifact content from the ADK server:

Escalation \[#escalation]

Detect when an agent requests escalation to a human operator:

Long-Running Tools \[#long-running-tools]

Track tools that are executing asynchronously and awaiting external input:

Per-Message Metadata \[#per-message-metadata]

Access grounding, citation, and token usage metadata per message:

Session State by Scope \[#session-state-by-scope]

ADK uses key prefixes to scope state. These helpers filter and strip the prefix:

Use `useAdkSessionState()` for the full unfiltered state delta.

Structured Events \[#structured-events]

Convert raw ADK events into typed, structured events for custom renderers:

State Delta \[#state-delta]

Send session state mutations along with messages using `stateDelta`:

This maps to ADK's `stateDelta` parameter on `/run_sse`.

RunConfig \[#runconfig]

Pass `AdkRunConfig` to control agent behavior:

Event Handlers \[#event-handlers]

Listen to streaming events:

Thread Management \[#thread-management]

ADK Session Adapter \[#adk-session-adapter]

Use `createAdkSessionAdapter` to persist threads via ADK's session API (see [Direct ADK Server Connection](#direct-adk-server-connection) above).

Custom Thread Management \[#custom-thread-management]

Cloud Persistence \[#cloud-persistence]

For persistent thread history via assistant-cloud:

Message Editing & Regeneration \[#message-editing--regeneration]

Provide a `getCheckpointId` callback to enable edit and regenerate buttons:

When `getCheckpointId` is provided:

The resolved `checkpointId` is passed to your `stream` callback via `config.checkpointId`.

Hooks Reference \[#hooks-reference]

Features \[#features]

ADK Python Backend \[#adk-python-backend]

The package automatically normalizes snake\_case event fields from ADK Python backends to camelCase. No configuration needed — connect to either ADK JS or ADK Python servers. This includes all nested fields: `function_call` → `functionCall`, `requested_tool_confirmations` → `requestedToolConfirmations`, etc.

URL: /docs/runtimes/langgraph

Connect to LangGraph Cloud API for agent workflows with streaming.

Requirements \[#requirements]

You need a LangGraph Cloud API server. You can start a server locally via [LangGraph Studio](https://github.com/langchain-ai/langgraph-studio) or use [LangSmith](https://www.langchain.com/langsmith) for a hosted version.

The state of the graph you are using must have a `messages` key with a list of LangChain-alike messages.

New project from template \[#new-project-from-template]

Installation in existing React project \[#installation-in-existing-react-project]

Advanced APIs \[#advanced-apis]

Message Accumulator \[#message-accumulator]

The `LangGraphMessageAccumulator` lets you append messages incoming from the server to replicate the messages state client side.

Message Conversion \[#message-conversion]

Use `convertLangChainMessages` to transform LangChain messages to assistant-ui format:

Event Handlers \[#event-handlers]

You can listen to streaming events by passing `eventHandlers` to `useLangGraphRuntime`:

Message Metadata \[#message-metadata]

When using `streamMode: "messages-tuple"`, each chunk includes metadata from the LangGraph server. Access accumulated metadata per message with the `useLangGraphMessageMetadata` hook:

Thread Management \[#thread-management]

Basic Thread Support \[#basic-thread-support]

The `useLangGraphRuntime` hook now includes built-in thread management capabilities:

Cloud Persistence \[#cloud-persistence]

For persistent thread history across sessions, integrate with assistant-cloud:

See the [Cloud Persistence guide](/docs/cloud/langgraph) for detailed setup instructions.

Message Editing & Regeneration \[#message-editing--regeneration]

LangGraph uses server-side checkpoints for state management. To support message editing (branching) and regeneration, you need to provide a `getCheckpointId` callback that resolves the appropriate checkpoint for server-side forking.

When `getCheckpointId` is provided:

The resolved `checkpointId` is passed to your `stream` callback via `config.checkpointId`. Your `sendMessage` helper should map it to the LangGraph SDK's `checkpoint_id` parameter (see the helper function in the setup section above).

Interrupt Persistence \[#interrupt-persistence]

LangGraph supports interrupting the execution flow to request user input or handle specific interactions. These interrupts can be persisted and restored when switching between threads:

This feature is particularly useful for applications that require user approval flows, multi-step forms, or any other interactive elements that might span multiple thread switches.

URL: /docs/runtimes/mastra/full-stack-integration

Integrate Mastra directly into Next.js API routes.

Integrate Mastra directly into your Next.js application's API routes. This approach keeps your backend and frontend code within the same project.

Congratulations! You have successfully integrated Mastra into your Next.js application using the full-stack approach. Your assistant-ui frontend now communicates with a Mastra agent running in your Next.js backend API route.

To explore more advanced Mastra features like memory, tools, workflows, and more, please refer to the [official Mastra documentation](https://mastra.ai/docs).

URL: /docs/runtimes/mastra/overview

TypeScript agent framework for AI applications with tools and workflows.

Mastra is an open-source TypeScript agent framework designed to provide the essential primitives for building AI applications. It enables developers to create AI agents with memory and tool-calling capabilities, implement deterministic LLM workflows, and leverage RAG for knowledge integration. With features like model routing, workflow graphs, and automated evals, Mastra provides a complete toolkit for developing, testing, and deploying AI applications.

Integrating with Next.js and assistant-ui \[#integrating-with-nextjs-and-assistant-ui]

There are two primary ways to integrate Mastra into your Next.js project when using assistant-ui:

Choose the guide that best fits your project architecture. Both methods allow seamless integration with the assistant-ui components.

URL: /docs/runtimes/mastra/separate-server-integration

Run Mastra as a standalone server connected to your frontend.

Run Mastra as a standalone server and connect your Next.js frontend (using assistant-ui) to its API endpoints. This approach separates your AI backend from your frontend application, allowing for independent development and scaling.

Congratulations! You have successfully integrated Mastra with assistant-ui using a separate server approach. Your assistant-ui frontend now communicates with a standalone Mastra agent server.

This setup provides a clear separation between your frontend and AI backend. To explore more advanced Mastra features like memory, tools, workflows, and deployment options, please refer to the [official Mastra documentation](https://mastra.ai/docs).

URL: /docs/api-reference/context-providers/assistant-runtime-provider

Root provider that connects your runtime to assistant-ui components.

The `AssistantRuntimeProvider` provides data and APIs used by assistant-ui components.

Almost all components in assistant-ui require an `AssistantRuntimeProvider` around them to function properly.

You must either wrap your app in an `AssistantRuntimeProvider` or pass a `runtime` to the `<Thread />` component instead.

Properties \[#properties]

URL: /docs/api-reference/context-providers/text-message-part-provider

Context provider for reusing text components outside of message content.

The `TextMessagePartProvider` provides data and APIs for `TextMessagePart` components.

This is useful if you want to reuse the same `Text` component outside of a message text, e.g. with the `@assistant-ui/react-markdown` package.

Properties \[#properties]

<ParametersTable
  type="TextMessagePartProviderProps"
  parameters="[
{
name: &#x22;text&#x22;,
type: &#x22;string&#x22;,
required: true,
description: &#x22;The text content to provide to child components.&#x22;,
},
{
name: &#x22;isRunning&#x22;,
type: &#x22;boolean&#x22;,
required: false,
description: &#x22;Whether the text is still being streamed. Defaults to false.&#x22;,
},
]"
/>

URL: /docs/api-reference/integrations/react-data-stream

Hooks for connecting to data stream protocol endpoints and Assistant Cloud.

Data Stream protocol integration for assistant-ui.

API Reference \[#api-reference]

`useDataStreamRuntime` \[#usedatastreamruntime]

Create a runtime that connects to a data stream protocol endpoint.

<ParametersTable
  parameters="[
{
name: &#x22;api&#x22;,
type: &#x22;string&#x22;,
description: &#x22;The API endpoint URL for the data stream protocol.&#x22;,
},
{
name: &#x22;protocol&#x22;,
type: '&#x22;ui-message-stream&#x22; | &#x22;data-stream&#x22;',
description: 'The streaming protocol to use. Defaults to &#x22;ui-message-stream&#x22;. Use &#x22;data-stream&#x22; for legacy AI SDK compatibility.',
},
{
name: &#x22;onData&#x22;,
type: &#x22;(data: { type: string; name: string; data: unknown; transient?: boolean }) => void&#x22;,
description: &#x22;Optional callback for data-* parts. Only applies when using the ui-message-stream protocol.&#x22;,
},
{
name: &#x22;onResponse&#x22;,
type: &#x22;(response: Response) => void | Promise<void>&#x22;,
description: &#x22;Optional callback called when a response is received.&#x22;,
},
{
name: &#x22;onFinish&#x22;,
type: &#x22;(message: ThreadMessage) => void&#x22;,
description: &#x22;Optional callback called when a message is finished.&#x22;,
},
{
name: &#x22;onError&#x22;,
type: &#x22;(error: Error) => void&#x22;,
description: &#x22;Optional callback called when an error occurs.&#x22;,
},
{
name: &#x22;onCancel&#x22;,
type: &#x22;() => void&#x22;,
description: &#x22;Optional callback called when a request is cancelled.&#x22;,
},
{
name: &#x22;credentials&#x22;,
type: &#x22;RequestCredentials&#x22;,
description: &#x22;Optional credentials mode for the fetch request.&#x22;,
},
{
name: &#x22;headers&#x22;,
type: &#x22;Record<string, string> | Headers | (() => Promise<Record<string, string> | Headers>)&#x22;,
description: &#x22;Optional headers to include in the request.&#x22;,
},
{
name: &#x22;body&#x22;,
type: &#x22;object | (() => Promise<object | undefined>)&#x22;,
description: &#x22;Optional additional body parameters to include in the request. Can be an object or an async function that returns one.&#x22;,
},
{
name: &#x22;sendExtraMessageFields&#x22;,
type: &#x22;boolean&#x22;,
description: &#x22;Whether to include extra message fields like IDs in the request.&#x22;,
},
]"
/>

`useCloudRuntime` \[#usecloudruntime]

Create a runtime that connects to Assistant Cloud using the data stream protocol.

<ParametersTable
  parameters="[
{
name: &#x22;cloud&#x22;,
type: &#x22;AssistantCloud&#x22;,
description: &#x22;The Assistant Cloud instance.&#x22;,
},
{
name: &#x22;assistantId&#x22;,
type: &#x22;string&#x22;,
description: &#x22;The ID of the assistant to connect to.&#x22;,
},
{
name: &#x22;protocol&#x22;,
type: '&#x22;ui-message-stream&#x22; | &#x22;data-stream&#x22;',
description: 'The streaming protocol to use. Defaults to &#x22;ui-message-stream&#x22;. Use &#x22;data-stream&#x22; for legacy AI SDK compatibility.',
},
{
name: &#x22;onData&#x22;,
type: &#x22;(data: { type: string; name: string; data: unknown; transient?: boolean }) => void&#x22;,
description: &#x22;Optional callback for data-* parts. Only applies when using the ui-message-stream protocol.&#x22;,
},
{
name: &#x22;onResponse&#x22;,
type: &#x22;(response: Response) => void | Promise<void>&#x22;,
description: &#x22;Optional callback called when a response is received.&#x22;,
},
{
name: &#x22;onFinish&#x22;,
type: &#x22;(message: ThreadMessage) => void&#x22;,
description: &#x22;Optional callback called when a message is finished.&#x22;,
},
{
name: &#x22;onError&#x22;,
type: &#x22;(error: Error) => void&#x22;,
description: &#x22;Optional callback called when an error occurs.&#x22;,
},
{
name: &#x22;onCancel&#x22;,
type: &#x22;() => void&#x22;,
description: &#x22;Optional callback called when a request is cancelled.&#x22;,
},
{
name: &#x22;credentials&#x22;,
type: &#x22;RequestCredentials&#x22;,
description: &#x22;Optional credentials mode for the fetch request.&#x22;,
},
{
name: &#x22;headers&#x22;,
type: &#x22;Record<string, string> | Headers | (() => Promise<Record<string, string> | Headers>)&#x22;,
description: &#x22;Optional headers to include in the request.&#x22;,
},
{
name: &#x22;body&#x22;,
type: &#x22;object | (() => Promise<object | undefined>)&#x22;,
description: &#x22;Optional additional body parameters to include in the request. Can be an object or an async function that returns one.&#x22;,
},
{
name: &#x22;sendExtraMessageFields&#x22;,
type: &#x22;boolean&#x22;,
description: &#x22;Whether to include extra message fields like IDs in the request.&#x22;,
},
]"
/>

`toLanguageModelMessages` \[#tolanguagemodelmessages]

Convert assistant-ui messages to AI SDK's `LanguageModelV2Message` format.

<ParametersTable
  parameters="[
{
name: &#x22;messages&#x22;,
type: &#x22;readonly ThreadMessage[]&#x22;,
description: &#x22;The messages to convert.&#x22;,
},
{
name: &#x22;options&#x22;,
type: &#x22;{ unstable_includeId?: boolean }&#x22;,
description: &#x22;Optional conversion options.&#x22;,
children: [
{
type: &#x22;{ unstable_includeId?: boolean }&#x22;,
parameters: [
{
name: &#x22;unstable_includeId&#x22;,
type: &#x22;boolean&#x22;,
description: &#x22;Whether to include message IDs in the converted messages.&#x22;,
},
],
},
],
},
]"
/>

Framework-Agnostic Utilities \[#framework-agnostic-utilities]

For custom integrations that don't use the AI SDK, use these utilities from `assistant-stream`:

`toGenericMessages` \[#togenericmessages]

Convert thread messages to a framework-agnostic format.

Returns an array of `GenericMessage` which can be one of:

`toToolsJSONSchema` \[#totoolsjsonschema]

Convert tool definitions to JSON Schema format.

By default, filters out disabled tools and backend-only tools. Use the `filter` option to customize:

URL: /docs/api-reference/integrations/react-hook-form

React Hook Form integration for AI-assisted form filling.

A React Hook Form integration for @assistant-ui.

API Reference \[#api-reference]

`useAssistantForm` \[#useassistantform]

Drop-in replacement hook for `useForm` that adds support for `@assistant-ui/react`.

Properties \[#properties]

<ParametersTable
  type="UseAssistantFormProps"
  parameters="[
{
name: &#x22;assistant&#x22;,
type: &#x22;object&#x22;,
optional: true,
description: &#x22;Configuration for useAssistantForm&#x22;,
children: [
{
parameters: [
{
name: &#x22;tools&#x22;,
type: &#x22;object&#x22;,
description: &#x22;Tools configuration for useAssistantForm&#x22;,
children: [
{
parameters: [
{
name: &#x22;set_form_field&#x22;,
type: &#x22;object&#x22;,
description: &#x22;Configuration for the set_form_field tool&#x22;,
children: [
{
parameters: [
{
name: &#x22;render&#x22;,
type: &#x22;ToolCallMessagePartComponent<{ name: string; value: string; }, {}>&#x22;,
description:
&#x22;The component to render when set_form_field is called.&#x22;,
},
],
},
],
},
{
name: &#x22;submit_form&#x22;,
type: &#x22;object&#x22;,
description: &#x22;Configuration for the submit_form tool&#x22;,
children: [
{
parameters: [
{
name: &#x22;render&#x22;,
type: &#x22;ToolCallMessagePartComponent<{}, {}>&#x22;,
description:
&#x22;The component to render when submit_form is called.&#x22;,
},
],
},
],
},
],
},
],
},
],
},
],
},
]"
/>

`formTools` \[#formtools]

The set of tools to use with `useAssistantForm` on the server side. While the AI SDK now supports forwarding frontend tools via `frontendTools()`, using `formTools` directly on the server gives you more control over tool execution.

URL: /docs/api-reference/integrations/vercel-ai-sdk

Vercel AI SDK integration with chat runtime hooks and transport utilities.

Vercel AI SDK integration for assistant-ui.

API Reference \[#api-reference]

`useChatRuntime` \[#usechatruntime]

Creates a runtime with AI SDK's `useChat` hook integration. This is the recommended approach for most use cases.

To customize the API endpoint, simply change the `api` parameter:

<ParametersTable
  parameters="[
{
name: &#x22;options&#x22;,
type: &#x22;UseChatRuntimeOptions&#x22;,
description: &#x22;Configuration options for the chat runtime.&#x22;,
children: [
{
type: &#x22;UseChatRuntimeOptions&#x22;,
parameters: [
{
name: &#x22;transport&#x22;,
type: &#x22;ChatTransport&#x22;,
description:
&#x22;Custom transport implementation. Defaults to AssistantChatTransport (which sends requests to '/api/chat' and forwards system messages and tools). Use `new AssistantChatTransport({ api: '/custom-endpoint' })` to customize the endpoint.&#x22;,
},
{
name: &#x22;cloud&#x22;,
type: &#x22;AssistantCloud&#x22;,
description:
&#x22;Optional AssistantCloud instance for chat persistence.&#x22;,
},
{
name: &#x22;adapters&#x22;,
type: &#x22;RuntimeAdapters&#x22;,
description:
&#x22;Optional runtime adapters to extend or override built-in functionality (attachments, speech, dictation, feedback, history).&#x22;,
},
{
name: &#x22;toCreateMessage&#x22;,
type: &#x22;(message: AppendMessage) => CreateUIMessage&#x22;,
description:
&#x22;Optional custom function to convert an AppendMessage into an AI SDK CreateUIMessage before sending.&#x22;,
},
{
name: &#x22;initialMessages&#x22;,
type: &#x22;UIMessage[]&#x22;,
description: &#x22;Initial messages to populate the chat.&#x22;,
},
{
name: &#x22;onFinish&#x22;,
type: &#x22;(message: UIMessage) => void&#x22;,
description: &#x22;Callback when a message completes streaming.&#x22;,
},
{
name: &#x22;onError&#x22;,
type: &#x22;(error: Error) => void&#x22;,
description: &#x22;Callback for handling errors.&#x22;,
},
],
},
],
},
]"
/>

`useAISDKRuntime` \[#useaisdkruntime]

For advanced use cases where you need direct access to the `useChat` hook from AI SDK.

<ParametersTable
  parameters="[
{
name: &#x22;chat&#x22;,
type: &#x22;ReturnType<typeof useChat>&#x22;,
description: &#x22;The chat helpers from @ai-sdk/react's useChat hook.&#x22;,
},
{
name: &#x22;options&#x22;,
type: &#x22;AISDKRuntimeAdapter&#x22;,
description: &#x22;Optional configuration options.&#x22;,
children: [
{
type: &#x22;AISDKRuntimeAdapter&#x22;,
parameters: [
{
name: &#x22;adapters&#x22;,
type: &#x22;RuntimeAdapters&#x22;,
description:
&#x22;Optional runtime adapters for attachments, feedback, speech, etc.&#x22;,
},
],
},
],
},
]"
/>

`AssistantChatTransport` \[#assistantchattransport]

A transport that extends the default AI SDK transport to automatically forward system messages and frontend tools to your backend.

<ParametersTable
  parameters="[
{
name: &#x22;options&#x22;,
type: &#x22;HttpChatTransportInitOptions&#x22;,
description: &#x22;Transport configuration options.&#x22;,
children: [
{
type: &#x22;HttpChatTransportInitOptions&#x22;,
parameters: [
{
name: &#x22;api&#x22;,
type: &#x22;string&#x22;,
description: &#x22;The API endpoint URL.&#x22;,
},
{
name: &#x22;headers&#x22;,
type: &#x22;Record<string, string> | Headers&#x22;,
description: &#x22;Optional headers to include in requests.&#x22;,
},
{
name: &#x22;credentials&#x22;,
type: &#x22;RequestCredentials&#x22;,
description: &#x22;Optional credentials mode for fetch requests.&#x22;,
},
],
},
],
},
]"
/>

`frontendTools` \[#frontendtools]

Helper function to convert frontend tool definitions to AI SDK format for use in your backend.

<ParametersTable
  parameters="[
{
name: &#x22;tools&#x22;,
type: &#x22;Record<string, unknown>&#x22;,
description:
&#x22;Frontend tools object forwarded from AssistantChatTransport.&#x22;,
},
]"
/>

URL: /docs/api-reference/primitives/action-bar-more

A dropdown menu for additional actions that don't fit in the main action bar.

Anatomy \[#anatomy]

API Reference \[#api-reference]

Root \[#root]

Contains all parts of the dropdown menu.

<ParametersTable
  type="ActionBarMorePrimitiveRootProps"
  parameters="[
{
name: &#x22;defaultOpen&#x22;,
type: &#x22;boolean&#x22;,
default: &#x22;false&#x22;,
description:
&#x22;The open state of the dropdown menu when it is initially rendered. Use when you do not need to control its open state.&#x22;,
},
{
name: &#x22;open&#x22;,
type: &#x22;boolean&#x22;,
description:
&#x22;The controlled open state of the dropdown menu. Must be used in conjunction with onOpenChange.&#x22;,
},
{
name: &#x22;onOpenChange&#x22;,
type: &#x22;(open: boolean) => void&#x22;,
description:
&#x22;Event handler called when the open state of the dropdown menu changes.&#x22;,
},
{
name: &#x22;modal&#x22;,
type: &#x22;boolean&#x22;,
default: &#x22;true&#x22;,
description:
&#x22;The modality of the dropdown menu. When set to true, interaction with outside elements will be disabled and only menu content will be visible to screen readers.&#x22;,
},
{
name: &#x22;dir&#x22;,
type: &#x22;'ltr' | 'rtl'&#x22;,
description: &#x22;The reading direction of the dropdown menu.&#x22;,
},
]"
/>

Trigger \[#trigger]

A button that toggles the dropdown menu.

This primitive renders a `<button>` element unless `asChild` is set.

<ParametersTable
  type="ActionBarMorePrimitiveTriggerProps"
  parameters="[
{
name: &#x22;asChild&#x22;,
},
]"
/>

Content \[#content]

The component that pops out when the dropdown menu is open.

This primitive renders a `<div>` element unless `asChild` is set.

<ParametersTable
  type="ActionBarMorePrimitiveContentProps"
  parameters="[
{
name: &#x22;asChild&#x22;,
},
{
name: &#x22;side&#x22;,
type: &#x22;'top' | 'right' | 'bottom' | 'left'&#x22;,
default: &#x22;'bottom'&#x22;,
description: &#x22;The preferred side of the trigger to render against.&#x22;,
},
{
name: &#x22;sideOffset&#x22;,
type: &#x22;number&#x22;,
default: &#x22;4&#x22;,
description: &#x22;The distance in pixels from the trigger.&#x22;,
},
{
name: &#x22;align&#x22;,
type: &#x22;'start' | 'center' | 'end'&#x22;,
default: &#x22;'center'&#x22;,
description: &#x22;The preferred alignment against the trigger.&#x22;,
},
{
name: &#x22;alignOffset&#x22;,
type: &#x22;number&#x22;,
default: &#x22;0&#x22;,
description: &#x22;An offset in pixels from the align option.&#x22;,
},
{
name: &#x22;portalProps&#x22;,
type: &#x22;PortalProps&#x22;,
description: &#x22;Props to pass to the Portal component.&#x22;,
},
]"
/>

Refer to Radix UI's Documentation for [DropdownMenu.Content](https://www.radix-ui.com/primitives/docs/components/dropdown-menu#content) for more details.

Item \[#item]

A menu item within the dropdown menu.

This primitive renders a `<div>` element unless `asChild` is set.

<ParametersTable
  type="ActionBarMorePrimitiveItemProps"
  parameters="[
{
name: &#x22;asChild&#x22;,
},
{
name: &#x22;disabled&#x22;,
type: &#x22;boolean&#x22;,
description: &#x22;When true, prevents the user from interacting with the item.&#x22;,
},
{
name: &#x22;onSelect&#x22;,
type: &#x22;(event: Event) => void&#x22;,
description:
&#x22;Event handler called when the user selects an item (via mouse or keyboard). Calling event.preventDefault in this handler will prevent the dropdown menu from closing when selecting that item.&#x22;,
},
{
name: &#x22;textValue&#x22;,
type: &#x22;string&#x22;,
description:
&#x22;Optional text used for typeahead purposes. By default the typeahead behavior will use the .textContent of the item.&#x22;,
},
]"
/>

Refer to Radix UI's Documentation for [DropdownMenu.Item](https://www.radix-ui.com/primitives/docs/components/dropdown-menu#item) for more details.

Separator \[#separator]

A visual separator between groups of items.

This primitive renders a `<div>` element unless `asChild` is set.

<ParametersTable
  type="ActionBarMorePrimitiveSeparatorProps"
  parameters="[
{
name: &#x22;asChild&#x22;,
},
]"
/>

Example Usage \[#example-usage]

Basic dropdown menu \[#basic-dropdown-menu]

Using with action hooks \[#using-with-action-hooks]

You can combine the dropdown menu items with action hooks from ActionBarPrimitive:

URL: /docs/api-reference/primitives/action-bar

Buttons for message actions like copy, edit, reload, speak, and feedback.

Buttons to interact with the message.

Anatomy \[#anatomy]

API Reference \[#api-reference]

Root \[#root]

Contains all parts of the action bar.

This primitive renders a `<div>` element unless `asChild` is set.

<ParametersTable
  type="ActionBarPrimitiveRootProps"
  parameters="[
{
name: &#x22;asChild&#x22;,
},
{
name: &#x22;hideWhenRunning&#x22;,
type: &#x22;boolean&#x22;,
default: &#x22;false&#x22;,
description: (
<span>
Do not render the ActionBar when the thread is in running state.
</span>
),
},
{
name: &#x22;autohide&#x22;,
type: '&#x22;always&#x22; | &#x22;not-last&#x22; | &#x22;never&#x22;',
default: '&#x22;never&#x22;',
description: (
<span>
Do not render the ActionBar unless the mouse is hovering over the
message.
<br />
<br />
<Code>&#x22;always&#x22;</Code>: always autohide.
<br />
<Code>&#x22;not-last&#x22;</Code>: only autohide if the message is not the last
one in the thread.
</span>
),
},
{
name: &#x22;autohideFloat&#x22;,
type: '&#x22;always&#x22; | &#x22;single-branch&#x22; | &#x22;never&#x22;',
default: '&#x22;never&#x22;',
description: (
<span>
Float the ActionBar during autohide.
<br />
<br />
<Code>&#x22;always&#x22;</Code>: always float during autohide.
<br />
<Code>&#x22;single-branch&#x22;</Code>: only float if the message is the only
one in the thread.
<br />
<br />
Note: this only sets `data-floating` on the ActionBar. You need to set
the appropriate styles on the ActionBar to make it float.
</span>
),
},
]"
/>

Edit \[#edit]

Enables edit mode on user message.

This primitive renders a `<button>` element unless `asChild` is set.

<ParametersTable
  type="ActionBarPrimitiveEditProps"
  parameters="[
{
name: &#x22;asChild&#x22;,
},
]"
/>

Reload \[#reload]

Regenerates the assistant message.

This primitive renders a `<button>` element unless `asChild` is set.

<ParametersTable
  type="ActionBarPrimitiveReloadProps"
  parameters="[
{
name: &#x22;asChild&#x22;,
},
]"
/>

Copy \[#copy]

Copies the message to the clipboard.

This primitive renders a `<button>` element unless `asChild` is set.

<ParametersTable
  type="ActionBarPrimitiveCopyProps"
  parameters="[
{
name: &#x22;asChild&#x22;,
},
{
name: &#x22;copiedDuration&#x22;,
type: &#x22;number&#x22;,
description:
&#x22;The duration in milliseconds to change the message status to 'copied'.&#x22;,
default: &#x22;3000&#x22;,
},
]"
/>

Copied state \[#copied-state]

Show a different icon for a few seconds after the message is copied.

or using the `data-copied` attribute:

Speak \[#speak]

Plays the message text as speech.

This primitive renders a `<button>` element unless `asChild` is set.

<ParametersTable
  type="ActionBarPrimitiveSpeakProps"
  parameters="[
{
name: &#x22;asChild&#x22;,
},
]"
/>

StopSpeaking \[#stopspeaking]

Stops the message text from being played as speech.

This primitive renders a `<button>` element unless `asChild` is set.

<ParametersTable
  type="ActionBarPrimitiveStopSpeakingProps"
  parameters="[
{
name: &#x22;asChild&#x22;,
},
]"
/>

Feedback Positive \[#feedback-positive]

Shows a positive feedback submission button.

This primitive renders a `<button>` element unless `asChild` is set.

<ParametersTable
  type="ActionBarPrimitiveFeedbackPositiveProps"
  parameters="[
{
name: &#x22;asChild&#x22;,
},
]"
/>

Feedback Negative \[#feedback-negative]

Shows a negative feedback submission button.

This primitive renders a `<button>` element unless `asChild` is set.

<ParametersTable
  type="ActionBarPrimitiveFeedbackNegativeProps"
  parameters="[
{
name: &#x22;asChild&#x22;,
},
]"
/>

ExportMarkdown \[#exportmarkdown]

Exports the message content as a Markdown file download by default, or calls a custom export handler when `onExport` is provided.

This primitive renders a `<button>` element unless `asChild` is set.

<ParametersTable
  type="ActionBarPrimitiveExportMarkdownProps"
  parameters="[
{
name: &#x22;asChild&#x22;,
},
{
name: &#x22;filename&#x22;,
type: &#x22;string&#x22;,
description:
&#x22;The filename for the downloaded Markdown file. Defaults to 'message-{timestamp}.md'. Ignored when onExport is provided.&#x22;,
},
{
name: &#x22;onExport&#x22;,
type: &#x22;(content: string) => void | Promise<void>&#x22;,
description:
&#x22;Optional callback function that receives the message content. When provided, overrides the default Markdown download behavior. Use this to implement custom export logic (PDF, JSON, TXT, etc.).&#x22;,
},
]"
/>

Examples \[#examples]

Default Markdown export:

With custom filename:

Export as PDF (with custom logic):

Export as JSON:

URL: /docs/api-reference/primitives/assistant-if

Conditional rendering component based on thread, message, or composer state.

Conditionally render children based on assistant state.

Anatomy \[#anatomy]

Overview \[#overview]

`AuiIf` is a generic conditional rendering component that provides access to the full assistant state. It replaces the deprecated `ThreadPrimitive.If`, `MessagePrimitive.If`, and `ComposerPrimitive.If` components with a single, flexible API.

API Reference \[#api-reference]

<ParametersTable
  type="AuiIfProps"
  parameters="[
{
name: &#x22;condition&#x22;,
type: &#x22;(state: AssistantState) => boolean&#x22;,
required: true,
description: &#x22;A function that receives the assistant state and returns whether to render children.&#x22;,
},
{
name: &#x22;children&#x22;,
type: &#x22;ReactNode&#x22;,
description: &#x22;Content to render when the condition returns true.&#x22;,
},
]"
/>

AssistantState \[#assistantstate]

The condition function receives an `AssistantState` object with the following properties:

<ParametersTable
  type="AssistantState"
  parameters="[
{
name: &#x22;thread&#x22;,
type: &#x22;ThreadState&#x22;,
description: &#x22;The current thread state (always available).&#x22;,
},
{
name: &#x22;message&#x22;,
type: &#x22;MessageState&#x22;,
description: &#x22;The current message state (available within a message context).&#x22;,
},
{
name: &#x22;composer&#x22;,
type: &#x22;ComposerState&#x22;,
description: &#x22;The current composer state (always available).&#x22;,
},
{
name: &#x22;part&#x22;,
type: &#x22;PartState&#x22;,
description: &#x22;The current message part state (available within a part context).&#x22;,
},
{
name: &#x22;attachment&#x22;,
type: &#x22;AttachmentState&#x22;,
description: &#x22;The current attachment state (available within an attachment context).&#x22;,
},
]"
/>

Examples \[#examples]

Thread State Conditions \[#thread-state-conditions]

Message State Conditions \[#message-state-conditions]

Composer State Conditions \[#composer-state-conditions]

Complex Conditions \[#complex-conditions]

Type Export \[#type-export]

You can import the `AuiIf.Condition` type for typing your condition functions:

Migration from Deprecated Components \[#migration-from-deprecated-components]

URL: /docs/api-reference/primitives/assistant-modal

A popover chat interface for floating assistant UI in the corner of the screen.

A modal chat UI usually displayed in the bottom right corner of the screen.

Anatomy \[#anatomy]

API Reference \[#api-reference]

Root \[#root]

Contains all parts of the assistant modal.

<ParametersTable
  type="AssistantModalPrimitiveRootProps"
  parameters="[
{
name: &#x22;defaultOpen&#x22;,
type: &#x22;boolean&#x22;,
default: &#x22;false&#x22;,
description:
&#x22;The open state of the assistant modal when it is initially rendered. Use when you do not need to control its open state.&#x22;,
},
{
name: &#x22;open&#x22;,
type: &#x22;boolean&#x22;,
description:
&#x22;Not recommended. The controlled open state of the assistant modal. Must be used in conjunction with onOpenChange.&#x22;,
},
{
name: &#x22;onOpenChange&#x22;,
type: &#x22;(open: boolean) => void&#x22;,
description:
&#x22;Event handler called when the open state of the assistant modal changes.&#x22;,
},
{
name: &#x22;modal&#x22;,
type: &#x22;boolean&#x22;,
default: &#x22;false&#x22;,
description:
&#x22;The modality of the assistant modal. When set to true, interaction with outside elements will be disabled and only modal content will be visible to screen readers.&#x22;,
},
]"
/>

Trigger \[#trigger]

A button that toggles the open state of the assistant modal. `AssistantModalPrimitive.Content` will position itself against this button.

This primitive renders a `<button>` element unless `asChild` is set.

<ParametersTable
  type="AssistantModalPrimitiveTriggerProps"
  parameters="[
{
name: &#x22;asChild&#x22;,
},
]"
/>

Anchor \[#anchor]

The anchor element that the assistant modal is attached to. Defaults to the `Trigger` element.

This primitive renders a `<div>` element unless `asChild` is set.

Content \[#content]

The component that pops out when the assistant modal is open.

This primitive renders a `<div>` element unless `asChild` is set.

<ParametersTable
  type="AssistantModalPrimitiveContentProps"
  parameters="[
{
name: &#x22;asChild&#x22;,
},
{
name: &#x22;side&#x22;,
type: &#x22;'top' | 'right' | 'bottom' | 'left'&#x22;,
default: &#x22;'top'&#x22;,
description: &#x22;The side of the assistant modal to position against.&#x22;,
},
{
name: &#x22;align&#x22;,
type: &#x22;'start' | 'center' | 'end'&#x22;,
default: &#x22;'end'&#x22;,
description: &#x22;The alignment of the assistant modal to position against.&#x22;,
},
{
name: &#x22;dissmissOnInteractOutside&#x22;,
type: &#x22;boolean&#x22;,
default: &#x22;false&#x22;,
description:
&#x22;Dismiss the assistant modal when the user interacts outside of it.&#x22;,
},
{
name: &#x22;portalProps&#x22;,
type: &#x22;{ container?: HTMLElement | null; forceMount?: true }&#x22;,
description:
&#x22;Props to pass to the underlying Radix UI Popover.Portal. Use container to render the modal into a specific DOM node, or forceMount to keep it mounted for animation control.&#x22;,
},
]"
/>

Refer to Radix UI's Documentation for [Popover.Content](https://www.radix-ui.com/primitives/docs/components/popover#content) for more details.

URL: /docs/api-reference/primitives/attachment

Components for displaying and managing file attachments in messages and composer.

Buttons to interact with attachments.

Anatomy \[#anatomy]

API Reference \[#api-reference]

Root \[#root]

Contains all parts of the attachment.

This primitive renders a `<div>` element unless `asChild` is set. Accepts all standard HTML div element props.

<ParametersTable
  type="AttachmentPrimitiveRootProps"
  parameters="[
{
name: &#x22;asChild&#x22;,
},
{
name: &#x22;...props&#x22;,
type: &#x22;HTMLAttributes<HTMLDivElement>&#x22;,
description: &#x22;All standard div element props are forwarded to the underlying element.&#x22;,
},
]"
/>

unstable\_Thumb \[#unstable\_thumb]

The thumbnail of the attachment.

This primitive renders a `<div>` element unless `asChild` is set. Accepts all standard HTML div element props.

<ParametersTable
  type="AttachmentPrimitiveThumbProps"
  parameters="[
{
name: &#x22;asChild&#x22;,
},
{
name: &#x22;...props&#x22;,
type: &#x22;HTMLAttributes<HTMLDivElement>&#x22;,
description: &#x22;All standard div element props are forwarded to the underlying element.&#x22;,
},
]"
/>

Name \[#name]

The name of the attachment.

This primitive renders a text node with the attachment's file name. It accepts no props.

Remove \[#remove]

Removes the attachment.

This primitive renders a `<button>` element unless `asChild` is set.

<ParametersTable
  type="AttachmentPrimitiveRemoveProps"
  parameters="[
{
name: &#x22;asChild&#x22;,
},
]"
/>

URL: /docs/api-reference/primitives/branch-picker

Navigate between conversation branches with previous/next controls.

View and switch between branches.

Anatomy \[#anatomy]

API Reference \[#api-reference]

Root \[#root]

Contains all parts of the branch picker.

This primitive renders a `<div>` element unless `asChild` is set.

<ParametersTable
  type="BranchPickerPrimitiveRootProps"
  parameters="[
{
name: &#x22;asChild&#x22;,
},
{
name: &#x22;hideWhenSingleBranch&#x22;,
type: &#x22;boolean&#x22;,
default: &#x22;false&#x22;,
description:
&#x22;Do not render the BranchPicker when there is only one branch at the current message.&#x22;,
},
]"
/>

Number \[#number]

The current branch number.

This primitive renders the raw number as a string.

Count \[#count]

The total number of branches.

This primitive renders the raw number as a string.

Previous \[#previous]

Navigates to the previous branch.

This primitive renders a `<button>` element unless `asChild` is set.

<ParametersTable
  type="BranchPickerPrimitivePreviousProps"
  parameters="[
{
name: &#x22;asChild&#x22;,
},
]"
/>

Next \[#next]

Navigates to the next branch.

This primitive renders a `<button>` element unless `asChild` is set.

<ParametersTable
  type="BranchPickerPrimitiveNextProps"
  parameters="[
{
name: &#x22;asChild&#x22;,
},
]"
/>

URL: /docs/api-reference/primitives/composer

Primitives for the text input, send button, and attachments.

The user interface to add new messages or edit existing ones.

Anatomy \[#anatomy]

API Reference \[#api-reference]

Root \[#root]

Contains all parts of the composer.

This primitive renders a `<form>` element unless `asChild` is set.

<ParametersTable
  type="ComposerRootProps"
  parameters="[
{
name: &#x22;asChild&#x22;,
},
]"
/>

Input \[#input]

The text input field for the user to type a new message.

This primitive renders a `<textarea>` element unless `asChild` is set.

<ParametersTable
  type="ComposerPrimitiveInputProps"
  parameters="[
{
name: &#x22;asChild&#x22;,
},
{
name: &#x22;submitMode&#x22;,
type: '&#x22;enter&#x22; | &#x22;ctrlEnter&#x22; | &#x22;none&#x22;',
default: '&#x22;enter&#x22;',
description:
'Controls how the Enter key submits messages. &#x22;enter&#x22;: plain Enter submits (Shift+Enter for newline). &#x22;ctrlEnter&#x22;: Ctrl/Cmd+Enter submits (plain Enter for newline). &#x22;none&#x22;: keyboard submission disabled.',
},
{
name: &#x22;cancelOnEscape&#x22;,
type: &#x22;boolean&#x22;,
default: &#x22;true&#x22;,
description:
&#x22;Whether to cancel message composition when Escape is pressed.&#x22;,
},
{
name: &#x22;unstable_focusOnRunStart&#x22;,
type: &#x22;boolean&#x22;,
default: &#x22;true&#x22;,
description:
&#x22;Whether to automatically focus the input when a new run starts.&#x22;,
},
{
name: &#x22;unstable_focusOnScrollToBottom&#x22;,
type: &#x22;boolean&#x22;,
default: &#x22;true&#x22;,
description:
&#x22;Whether to automatically focus the input when scrolling to bottom.&#x22;,
},
{
name: &#x22;unstable_focusOnThreadSwitched&#x22;,
type: &#x22;boolean&#x22;,
default: &#x22;true&#x22;,
description:
&#x22;Whether to automatically focus the input when switching threads.&#x22;,
},
{
name: &#x22;addAttachmentOnPaste&#x22;,
type: &#x22;boolean&#x22;,
default: &#x22;true&#x22;,
description:
&#x22;Whether to automatically add pasted files as attachments.&#x22;,
},
]"
/>

Keyboard Shortcuts \[#keyboard-shortcuts]

Default (`submitMode="enter"`):

With `submitMode="ctrlEnter"`:

Send \[#send]

The button to send the message.

This primitive renders a `<button>` element unless `asChild` is set.

<ParametersTable
  type="ComposerPrimitiveSendProps"
  parameters="[
{
name: &#x22;asChild&#x22;,
},
]"
/>

Cancel \[#cancel]

Sends a cancel action.

In edit composers, this action exits the edit mode.
In thread composers, this action stops the current run.

This primitive renders a `<button>` element unless `asChild` is set.

<ParametersTable
  type="ComposerPrimitiveCancelProps"
  parameters="[
{
name: &#x22;asChild&#x22;,
},
]"
/>

Attachments \[#attachments]

Renders attachments. This primitive renders a separate component for each attachment.

<ParametersTable
  type="ComposerPrimitiveAttachmentsProps"
  parameters="[
{
name: &#x22;components&#x22;,
type: &#x22;ComposerAttachmentsComponents&#x22;,
description: &#x22;The component to render for each attachment.&#x22;,
children: [
{
type: &#x22;ComposerPrimitiveAttachmentsProps['components']&#x22;,
parameters: [
{
name: &#x22;Image&#x22;,
type: &#x22;ComponentType&#x22;,
description: &#x22;The component to render for each image attachment.&#x22;,
},
{
name: &#x22;Document&#x22;,
type: &#x22;ComponentType&#x22;,
description:
&#x22;The component to render for each document attachment.&#x22;,
},
{
name: &#x22;File&#x22;,
type: &#x22;ComponentType&#x22;,
description: &#x22;The component to render for each file attachment.&#x22;,
},
{
name: &#x22;Attachment&#x22;,
type: &#x22;ComponentType&#x22;,
description: &#x22;The fallback component to render for each attachment type.&#x22;,
},
],
},
],
},
]"
/>

AttachmentByIndex \[#attachmentbyindex]

Renders a single attachment at the specified index within the composer.

<ParametersTable
  type="ComposerPrimitive.AttachmentByIndex.Props"
  parameters="[
{
name: &#x22;index&#x22;,
type: &#x22;number&#x22;,
required: true,
description: &#x22;The index of the attachment to render.&#x22;,
},
{
name: &#x22;components&#x22;,
type: &#x22;ComposerAttachmentsComponents&#x22;,
description: &#x22;The components to render for the attachment.&#x22;,
},
]"
/>

AddAttachment \[#addattachment]

Renders a button to add an attachment.

This primitive renders a `<button>` element unless `asChild` is set.

<ParametersTable
  type="ComposerPrimitiveAddAttachmentProps"
  parameters="[
{
name: &#x22;asChild&#x22;,
},
{
name: &#x22;multiple&#x22;,
type: &#x22;boolean | undefined&#x22;,
description: &#x22;Allow selecting multiple attachments at the same time.&#x22;,
default: &#x22;true&#x22;,
},
]"
/>

AttachmentDropzone \[#attachmentdropzone]

A drag-and-drop zone that accepts file drops and adds them as attachments to the composer.

When a file is dragged over the zone, a `data-dragging="true"` attribute is set on the element, which can be used for styling the active drag state.

This primitive renders a `<div>` element unless `asChild` is set.

<ParametersTable
  type="ComposerPrimitiveAttachmentDropzoneProps"
  parameters="[
{
name: &#x22;asChild&#x22;,
},
{
name: &#x22;disabled&#x22;,
type: &#x22;boolean | undefined&#x22;,
description: &#x22;When true, drag-and-drop is disabled and files will not be added on drop.&#x22;,
},
]"
/>

Dictate \[#dictate]

Renders a button to start dictation to convert voice to text.

Requires a `DictationAdapter` to be configured in the runtime.

This primitive renders a `<button>` element unless `asChild` is set.

<ParametersTable
  type="ComposerPrimitiveDictateProps"
  parameters="[
{
name: &#x22;asChild&#x22;,
},
]"
/>

StopDictation \[#stopdictation]

Renders a button to stop the current dictation session.

Only rendered when dictation is active.

This primitive renders a `<button>` element unless `asChild` is set.

<ParametersTable
  type="ComposerPrimitiveStopDictationProps"
  parameters="[
{
name: &#x22;asChild&#x22;,
},
]"
/>

DictationTranscript \[#dictationtranscript]

Renders the current interim (partial) transcript while dictation is active.

Only renders when there is an active interim transcript (returns `null` otherwise).

This primitive renders a `<span>` element.

Quote \[#quote]

A container for displaying a quote preview in the composer. Only renders when a quote is set via `composer.setQuote()`.

This primitive renders a `<div>` element.

QuoteText \[#quotetext]

Renders the quoted text content. Only renders when a quote is set.

This primitive renders a `<span>` element.

QuoteDismiss \[#quotedismiss]

A button that clears the current quote from the composer by calling `setQuote(undefined)`.

This primitive renders a `<button>` element unless `asChild` is set.

<ParametersTable
  type="ComposerPrimitiveQuoteDismissProps"
  parameters="[
{
name: &#x22;asChild&#x22;,
},
]"
/>

Conditional Rendering \[#conditional-rendering]

Use `AuiIf` for conditional rendering based on composer state:

Mention Primitives (Unstable) \[#mention-primitives-unstable]

Primitives for an @-mention picker in the composer. See the [Mention component guide](/docs/ui/mention) for a pre-built implementation.

Anatomy \[#anatomy-1]

Unstable\_MentionRoot \[#unstable\_mentionroot]

Provider that wraps the composer with mention trigger detection, keyboard navigation, and popover state.

Unstable\_MentionPopover \[#unstable\_mentionpopover]

Container that only renders when a mention trigger is active. Renders a `<div>` with `role="listbox"`.

Unstable\_MentionCategories \[#unstable\_mentioncategories]

Renders the top-level category list. Accepts a render function `(categories) => ReactNode`. Hidden when a category is selected or when in search mode.

Unstable\_MentionCategoryItem \[#unstable\_mentioncategoryitem]

A button that drills into a category. Renders `role="option"` with automatic `data-highlighted` and `aria-selected` when keyboard-navigated.

Unstable\_MentionItems \[#unstable\_mentionitems]

Renders the item list for the active category or search results. Accepts a render function `(items) => ReactNode`. Hidden when no category is selected and not in search mode.

Unstable\_MentionItem \[#unstable\_mentionitem]

A button that inserts a mention into the composer. Renders `role="option"` with automatic `data-highlighted` and `aria-selected` when keyboard-navigated.

Unstable\_MentionBack \[#unstable\_mentionback]

A button that navigates back from items to the category list. Only renders when a category is active.

unstable\_useMentionContext \[#unstable\_usementioncontext]

Hook to access the mention popover state and actions from within `Unstable_MentionRoot`.

unstable\_useToolMentionAdapter \[#unstable\_usetoolmentionadapter]

Hook that creates a `Unstable_MentionAdapter` from registered tools (via `useAssistantTool`).

URL: /docs/api-reference/primitives/composition

How to compose primitives with custom components using asChild.

`assistant-ui` primitives are composable. This means that all props are forwarded, classes are merged, and event handlers are chained.

Most primitives come with a default HTML element (usually `div` or `button`). If you already have a custom component, you can use the `asChild` prop to replace it:

Learn more on [Radix's composition guide](https://www.radix-ui.com/primitives/docs/guides/composition).

URL: /docs/api-reference/primitives/error

Components for displaying error messages in the chat interface.

A component for displaying error messages in the UI.

Anatomy \[#anatomy]

API Reference \[#api-reference]

Root \[#root]

Contains all parts of the error display. Renders a `<div>` element with `role="alert"`.

<ParametersTable
  type="ErrorPrimitiveRootProps"
  parameters="[
{
name: &#x22;asChild&#x22;,
type: &#x22;boolean&#x22;,
description:
&#x22;Change the component to the HTML tag or custom component of the only child.&#x22;,
},
]"
/>

Message \[#message]

Displays the error message. By default, it shows the error from the message context if available, or you can provide custom content.

<ParametersTable
  type="ErrorPrimitiveMessageProps"
  parameters="[
{
name: &#x22;children&#x22;,
type: &#x22;ReactNode&#x22;,
description:
&#x22;Optional custom content to display instead of the default error message.&#x22;,
},
]"
/>

Usage \[#usage]

The ErrorPrimitive is typically used within a MessagePrimitive.Error component to display error states in messages:

URL: /docs/api-reference/primitives/message-part

Primitives for text, images, tool calls, and other message content.

Each message can have any number of message parts.
Message parts are usually one of text, reasoning, audio, tool-call, or data.

Message part Types \[#message-part-types]

Text \[#text]

Standard text content, used for both user and assistant messages.

Reasoning \[#reasoning]

Exposes the assistant's reasoning process, showing how it arrived at its responses. This is typically used only in assistant messages.

Audio \[#audio]

Audio content that can be played back.

Tool Call \[#tool-call]

Interactive elements that represent tool operations.

Data \[#data]

Custom data events that can be rendered as UI at their position in the message stream. Each data part has a `name` and a `data` payload.

You can use either the explicit format `{ type: "data", name: "workflow", data: {...} }` or the shorthand `data-*` prefixed format `{ type: "data-workflow", data: {...} }`. The prefixed format is automatically converted to a `DataMessagePart` (stripping the `data-` prefix as the `name`). Unknown message part types that don't match any built-in type are silently skipped with a console warning.

Anatomy \[#anatomy]

Primitives \[#primitives]

Plain Text \[#plain-text]

Markdown Text \[#markdown-text]

Renders the message's text as Markdown.

Audio \[#audio-1]

Coming soon.

InProgress \[#inprogress]

Renders children only if the message part is in progress.

Tool UI \[#tool-ui]

You can map tool calls to UI components. We provide a few utility functions to make this easier, such as `makeAssistantToolUI`.

Data UI \[#data-ui]

You can map data events to UI components, similar to tool UIs. There are two approaches:

Inline configuration \[#inline-configuration]

Pass a `data` config to `MessagePrimitive.Parts`:

Global registration \[#global-registration]

Use `makeAssistantDataUI` or `useAssistantDataUI` to register data UIs globally. Global registrations take priority over inline configuration.

The hook variant allows access to component state:

Each data component receives the full data part as props: `{ type: "data", name: string, data: T, status: MessagePartStatus }`.

Messages (Sub-Agent) \[#messages-sub-agent]

Renders nested messages from a tool call part's `messages` field. This is used in multi-agent setups where a sub-agent's conversation is embedded inside a tool call.

This primitive must be used inside a tool call part context (e.g. inside a `makeAssistantToolUI` render function). It reads the `messages` field from the current `ToolCallMessagePart` and renders them in a readonly thread context.

Parent tool UI registrations are inherited — tools registered via `makeAssistantToolUI` at the parent level are available inside sub-agent messages.

See the [Multi-Agent Guide](/docs/guides/multi-agent) for detailed usage.

Context Provider \[#context-provider]

Message part context is provided by `MessagePrimitive.Parts` or `TextMessagePartProvider`

MessagePrimitive.Parts \[#messageprimitiveparts]

TextMessagePartProvider \[#textmessagepartprovider]

This is a helper context provider to allow you to reuse the message part components outside a message part.

Runtime API \[#runtime-api]

`useAui` (Message Part Actions) \[#useaui-message-part-actions]

`useAuiState` (Message Part State) \[#useauistate-message-part-state]

`useMessagePartText` \[#usemessageparttext]

URL: /docs/api-reference/primitives/message

Components for rendering message content, parts, and attachments.

A single message in a conversation. Messages may consist of multiple parts.

Anatomy \[#anatomy]

API Reference \[#api-reference]

Root \[#root]

Contains all parts of the message.

This primitive renders a `<div>` element unless `asChild` is set.

<ParametersTable
  type="MessagePrimitiveRootProps"
  parameters="[
{
name: &#x22;asChild&#x22;,
},
]"
/>

Parts \[#parts]

The content of the message. This renders a separate component for each message part.

<ParametersTable
  type="MessagePrimitivePartsProps"
  parameters="[
{
name: &#x22;components&#x22;,
required: false,
type: &#x22;MessagePartComponents&#x22;,
description: &#x22;The components to render for each message part.&#x22;,
children: [
{
type: &#x22;MessagePartComponents&#x22;,
parameters: [
{
name: &#x22;Text&#x22;,
type: &#x22;TextMessagePartComponent&#x22;,
description:
&#x22;The component to render for each text message part.&#x22;,
},
{
name: &#x22;Image&#x22;,
type: &#x22;ImageMessagePartComponent&#x22;,
description:
&#x22;The component to render for each image message part.&#x22;,
},
{
name: &#x22;Source&#x22;,
type: &#x22;SourceMessagePartComponent&#x22;,
description:
&#x22;The component to render for each source message part.&#x22;,
},
{
name: &#x22;File&#x22;,
type: &#x22;FileMessagePartComponent&#x22;,
description:
&#x22;The component to render for each file message part.&#x22;,
},
{
name: &#x22;Unstable_Audio&#x22;,
type: &#x22;Unstable_AudioMessagePartComponent&#x22;,
description:
&#x22;The component to render for each audio message part.&#x22;,
},
{
name: &#x22;Reasoning&#x22;,
type: &#x22;ReasoningMessagePartComponent&#x22;,
description:
&#x22;The component to render for each reasoning message part. Cannot be used alongside ChainOfThought.&#x22;,
},
{
name: &#x22;tools&#x22;,
type: &#x22;object&#x22;,
description:
&#x22;Configuration for tool call rendering. Cannot be used alongside ChainOfThought.&#x22;,
children: [
{
parameters: [
{
name: &#x22;by_name&#x22;,
type: &#x22;Record<string, ToolCallMessagePartComponent>&#x22;,
description:
&#x22;Map of tool names to their specific components.&#x22;,
},
{
name: &#x22;Fallback&#x22;,
type: &#x22;ToolCallMessagePartComponent&#x22;,
description:
&#x22;Fallback component for tool calls not matched by by_name.&#x22;,
},
{
name: &#x22;Override&#x22;,
type: &#x22;ComponentType<ToolCallMessagePartProps>&#x22;,
description:
&#x22;Override component that handles all tool calls. When set, by_name and Fallback are ignored.&#x22;,
},
],
},
],
},
{
name: &#x22;data&#x22;,
type: &#x22;object&#x22;,
description:
&#x22;Configuration for data part rendering.&#x22;,
children: [
{
parameters: [
{
name: &#x22;by_name&#x22;,
type: &#x22;Record<string, DataMessagePartComponent>&#x22;,
description:
&#x22;Map of data event names to their specific components.&#x22;,
},
{
name: &#x22;Fallback&#x22;,
type: &#x22;DataMessagePartComponent&#x22;,
description:
&#x22;Fallback component for data events not matched by by_name.&#x22;,
},
],
},
],
},
{
name: &#x22;ToolGroup&#x22;,
type: &#x22;ComponentType<PropsWithChildren<{ startIndex: number; endIndex: number }>>&#x22;,
description:
&#x22;Deprecated: This feature is still experimental and subject to change. Component for rendering grouped consecutive tool calls. When provided, consecutive tool-call message parts will be automatically grouped and wrapped with this component. Cannot be used alongside ChainOfThought.&#x22;,
children: [
{
type: &#x22;ToolGroupProps&#x22;,
parameters: [
{
name: &#x22;startIndex&#x22;,
type: &#x22;number&#x22;,
description: &#x22;Index of the first tool call in the group.&#x22;,
required: true,
},
{
name: &#x22;endIndex&#x22;,
type: &#x22;number&#x22;,
description: &#x22;Index of the last tool call in the group.&#x22;,
required: true,
},
{
name: &#x22;children&#x22;,
type: &#x22;ReactNode&#x22;,
description:
&#x22;The rendered tool call components within the group.&#x22;,
required: true,
},
],
},
],
},
{
name: &#x22;ReasoningGroup&#x22;,
type: &#x22;ReasoningGroupComponent&#x22;,
description:
&#x22;Component for rendering grouped consecutive reasoning parts. Cannot be used alongside ChainOfThought.&#x22;,
children: [
{
type: &#x22;ReasoningGroupProps&#x22;,
parameters: [
{
name: &#x22;startIndex&#x22;,
type: &#x22;number&#x22;,
description: &#x22;Index of the first reasoning part in the group.&#x22;,
required: true,
},
{
name: &#x22;endIndex&#x22;,
type: &#x22;number&#x22;,
description: &#x22;Index of the last reasoning part in the group.&#x22;,
required: true,
},
{
name: &#x22;children&#x22;,
type: &#x22;ReactNode&#x22;,
description:
&#x22;The rendered reasoning part components within the group.&#x22;,
required: true,
},
],
},
],
},
{
name: &#x22;ChainOfThought&#x22;,
type: &#x22;ComponentType&#x22;,
description:
&#x22;When set, groups all consecutive reasoning and tool-call parts into a single collapsible component. Mutually exclusive with Reasoning, tools, ToolGroup, and ReasoningGroup.&#x22;,
},
{
name: &#x22;Empty&#x22;,
type: &#x22;EmptyMessagePartComponent&#x22;,
description:
&#x22;Component to render when the message has no parts, or when unstable_showEmptyOnNonTextEnd is enabled and the last part is not text or reasoning.&#x22;,
},
],
},
],
},
{
name: &#x22;unstable_showEmptyOnNonTextEnd&#x22;,
required: false,
type: &#x22;boolean&#x22;,
description:
&#x22;When enabled, shows the Empty component if the last part in the message is anything other than Text or Reasoning. Defaults to true.&#x22;,
},
]"
/>

Quote \[#quote]

Renders a quote block if the message has quote metadata (`message.metadata.custom.quote`). Place this above `MessagePrimitive.Parts`.

<ParametersTable
  type="MessagePrimitiveQuoteProps"
  parameters="[
{
name: &#x22;children&#x22;,
required: true,
type: &#x22;(quote: QuoteInfo) => ReactNode&#x22;,
description: &#x22;Render function called when a quote is present. Receives { text, messageId }.&#x22;,
},
]"
/>

PartByIndex \[#partbyindex]

Renders a single message part at the specified index.

<ParametersTable
  type="MessagePrimitive.PartByIndex.Props"
  parameters="[
{
name: &#x22;index&#x22;,
type: &#x22;number&#x22;,
required: true,
description: &#x22;The index of the message part to render.&#x22;,
},
{
name: &#x22;components&#x22;,
required: false,
type: &#x22;MessagePartComponents&#x22;,
description: &#x22;The components to render for the message part.&#x22;,
},
]"
/>

Attachments \[#attachments]

Renders all attachments of the message.

<ParametersTable
  type="MessagePrimitive.Attachments.Props"
  parameters="[
{
name: &#x22;components&#x22;,
type: &#x22;AttachmentComponents&#x22;,
description: &#x22;The components to render for each attachment.&#x22;,
children: [
{
type: &#x22;AttachmentComponents&#x22;,
parameters: [
{
name: &#x22;Image&#x22;,
type: &#x22;ComponentType&#x22;,
description: &#x22;The component to render for image attachments.&#x22;,
},
{
name: &#x22;Document&#x22;,
type: &#x22;ComponentType&#x22;,
description: &#x22;The component to render for document attachments.&#x22;,
},
{
name: &#x22;File&#x22;,
type: &#x22;ComponentType&#x22;,
description: &#x22;The component to render for file attachments.&#x22;,
},
{
name: &#x22;Attachment&#x22;,
type: &#x22;ComponentType&#x22;,
description: &#x22;The fallback component to render for any attachment type.&#x22;,
},
],
},
],
},
]"
/>

AttachmentByIndex \[#attachmentbyindex]

Renders a single attachment at the specified index within the message.

<ParametersTable
  type="MessagePrimitive.AttachmentByIndex.Props"
  parameters="[
{
name: &#x22;index&#x22;,
type: &#x22;number&#x22;,
required: true,
description: &#x22;The index of the attachment to render.&#x22;,
},
{
name: &#x22;components&#x22;,
type: &#x22;AttachmentComponents&#x22;,
description: &#x22;The components to render for the attachment.&#x22;,
},
]"
/>

useMessageQuote() \[#usemessagequote]

A hook that returns the quote info attached to the current message, if any. Reads from `message.metadata.custom.quote`.

**Returns:** `QuoteInfo | undefined`

Unstable\_PartsGrouped \[#unstable\_partsgrouped]

Renders the parts of a message grouped by a custom grouping function. Use this component when you need to visually group related message parts together — for example, grouping parts that share a common parent ID, or collecting consecutive tool calls under a single header.

The `groupingFunction` prop controls how parts are grouped. It receives the full array of message parts and must return an array of group descriptors, each with a `groupKey` (or `undefined` for ungrouped parts) and an array of `indices` into the message parts array. The optional `components.Group` component is then rendered once per group and receives the `groupKey`, `indices`, and the rendered part children.

<ParametersTable
  type="MessagePrimitive.Unstable_PartsGrouped.Props"
  parameters="[
{
name: &#x22;groupingFunction&#x22;,
required: true,
type: &#x22;GroupingFunction&#x22;,
description:
&#x22;A function that receives the array of message parts and returns an array of groups. Each group has a groupKey (string or undefined for ungrouped parts) and an indices array of part positions.&#x22;,
},
{
name: &#x22;components&#x22;,
required: false,
type: &#x22;object&#x22;,
description: &#x22;The components to render for each message part type and for group wrappers.&#x22;,
children: [
{
parameters: [
{
name: &#x22;Text&#x22;,
type: &#x22;TextMessagePartComponent&#x22;,
description: &#x22;The component to render for each text message part.&#x22;,
},
{
name: &#x22;Reasoning&#x22;,
type: &#x22;ReasoningMessagePartComponent&#x22;,
description: &#x22;The component to render for each reasoning message part.&#x22;,
},
{
name: &#x22;Source&#x22;,
type: &#x22;SourceMessagePartComponent&#x22;,
description: &#x22;The component to render for each source message part.&#x22;,
},
{
name: &#x22;Image&#x22;,
type: &#x22;ImageMessagePartComponent&#x22;,
description: &#x22;The component to render for each image message part.&#x22;,
},
{
name: &#x22;File&#x22;,
type: &#x22;FileMessagePartComponent&#x22;,
description: &#x22;The component to render for each file message part.&#x22;,
},
{
name: &#x22;Unstable_Audio&#x22;,
type: &#x22;Unstable_AudioMessagePartComponent&#x22;,
description: &#x22;The component to render for each audio message part.&#x22;,
},
{
name: &#x22;Empty&#x22;,
type: &#x22;EmptyMessagePartComponent&#x22;,
description: &#x22;Component to render when the message has no parts.&#x22;,
},
{
name: &#x22;tools&#x22;,
type: &#x22;object&#x22;,
description: &#x22;Configuration for tool call rendering.&#x22;,
children: [
{
parameters: [
{
name: &#x22;by_name&#x22;,
type: &#x22;Record<string, ToolCallMessagePartComponent>&#x22;,
description: &#x22;Map of tool names to their specific components.&#x22;,
},
{
name: &#x22;Fallback&#x22;,
type: &#x22;ToolCallMessagePartComponent&#x22;,
description:
&#x22;Fallback component for tool calls not matched by by_name.&#x22;,
},
{
name: &#x22;Override&#x22;,
type: &#x22;ComponentType<ToolCallMessagePartProps>&#x22;,
description:
&#x22;Override component that handles all tool calls. When set, by_name and Fallback are ignored.&#x22;,
},
],
},
],
},
{
name: &#x22;data&#x22;,
type: &#x22;object&#x22;,
description: &#x22;Configuration for data part rendering.&#x22;,
children: [
{
parameters: [
{
name: &#x22;by_name&#x22;,
type: &#x22;Record<string, DataMessagePartComponent>&#x22;,
description:
&#x22;Map of data event names to their specific components.&#x22;,
},
{
name: &#x22;Fallback&#x22;,
type: &#x22;DataMessagePartComponent&#x22;,
description:
&#x22;Fallback component for data events not matched by by_name.&#x22;,
},
],
},
],
},
{
name: &#x22;Group&#x22;,
type: &#x22;ComponentType<PropsWithChildren<{ groupKey: string | undefined; indices: number[] }>>&#x22;,
description:
&#x22;Component for rendering a group of message parts. Receives the groupKey (undefined for ungrouped parts), the indices of all parts in the group, and the rendered part children.&#x22;,
children: [
{
type: &#x22;GroupProps&#x22;,
parameters: [
{
name: &#x22;groupKey&#x22;,
type: &#x22;string | undefined&#x22;,
description:
&#x22;The group key, or undefined for ungrouped parts.&#x22;,
required: true,
},
{
name: &#x22;indices&#x22;,
type: &#x22;number[]&#x22;,
description:
&#x22;Array of indices of the message parts belonging to this group.&#x22;,
required: true,
},
{
name: &#x22;children&#x22;,
type: &#x22;ReactNode&#x22;,
description:
&#x22;The rendered message part components within the group.&#x22;,
required: true,
},
],
},
],
},
],
},
],
},
]"
/>

Unstable\_PartsGroupedByParentId \[#unstable\_partsgroupedbyparentid]

A convenience wrapper around `MessagePrimitive.Unstable_PartsGrouped` that groups message parts by their `parentId` field. Parts without a `parentId` appear individually at their chronological position; parts sharing the same `parentId` are collected into a single group at the position of their first occurrence.

Accepts the same `components` prop as [`MessagePrimitive.Unstable_PartsGrouped`](#unstable_partsgrouped), but without a `groupingFunction` prop (the parent-ID grouping function is applied automatically).

Error \[#error]

Renders children only if the message has an error status.

URL: /docs/api-reference/primitives/selection-toolbar

A floating toolbar that appears when text is selected within a message.

A floating toolbar that appears near the user's text selection within a message. Used to provide contextual actions like quoting selected text.

Anatomy \[#anatomy]

Place this component inside `ThreadPrimitive.Root`:

API Reference \[#api-reference]

Root \[#root]

A floating container that renders as a portal positioned above the text selection. Only renders when there is a valid text selection within a single message.

This primitive renders a `<div>` element.

**Behavior:**

Quote \[#quote]

A button that captures the currently selected text and sets it as a quote in the thread composer.

This primitive renders a `<button>` element.

**Behavior:**

URL: /docs/api-reference/primitives/suggestion

Primitives for rendering individual suggestions. These primitives must be used within a suggestion context provided by `ThreadPrimitive.Suggestions`.

Quick Reference \[#quick-reference]

API Reference \[#api-reference]

`SuggestionPrimitive.Title` \[#suggestionprimitivetitle]

Displays the suggestion's title.

This primitive renders a `<span>` element.

`SuggestionPrimitive.Description` \[#suggestionprimitivedescription]

Displays the suggestion's description/label. This is only shown when suggestions are configured using the object format with separate title and label.

This primitive renders a `<span>` element.

`SuggestionPrimitive.Trigger` \[#suggestionprimitivetrigger]

A button that triggers the suggestion action when clicked. When clicked, it either sends the message immediately or populates the composer with the suggestion's prompt.

<ParametersTable
  type="SuggestionPrimitiveTriggerProps"
  parameters="[
{
name: &#x22;send&#x22;,
type: &#x22;boolean&#x22;,
description:
&#x22;When true, automatically sends the message. When false, only populates the composer with the suggestion's prompt.&#x22;,
},
{
name: &#x22;clearComposer&#x22;,
type: &#x22;boolean&#x22;,
default: &#x22;true&#x22;,
description:
&#x22;When send is false, determines whether to clear the composer before adding the suggestion (true) or append to existing text (false).&#x22;,
},
{
name: &#x22;asChild&#x22;,
type: &#x22;boolean&#x22;,
default: &#x22;false&#x22;,
description: &#x22;Merge props with child element instead of rendering a wrapper button.&#x22;,
},
{
name: &#x22;className&#x22;,
type: &#x22;string&#x22;,
description: &#x22;CSS class name.&#x22;,
},
]"
/>

This primitive renders a `<button>` element unless `asChild` is set.

Usage Example \[#usage-example]

See Also \[#see-also]

URL: /docs/api-reference/primitives/thread-list-item-more

Dropdown menu for additional thread actions like archive and delete.

A dropdown menu for displaying additional actions on a thread list item. Built on top of [Radix UI Dropdown Menu](https://www.radix-ui.com/primitives/docs/components/dropdown-menu).

Anatomy \[#anatomy]

API Reference \[#api-reference]

Root \[#root]

Contains all parts of the dropdown menu. Wraps Radix UI's `DropdownMenu.Root`.

<ParametersTable
  type="ThreadListItemMorePrimitiveRootProps"
  parameters="[
{
name: &#x22;open&#x22;,
type: &#x22;boolean&#x22;,
description: &#x22;The controlled open state of the dropdown menu.&#x22;,
},
{
name: &#x22;defaultOpen&#x22;,
type: &#x22;boolean&#x22;,
description: &#x22;The open state of the dropdown menu when it is initially rendered.&#x22;,
},
{
name: &#x22;onOpenChange&#x22;,
type: &#x22;(open: boolean) => void&#x22;,
description: &#x22;Event handler called when the open state changes.&#x22;,
},
{
name: &#x22;modal&#x22;,
type: &#x22;boolean&#x22;,
default: &#x22;true&#x22;,
description: &#x22;Whether the dropdown menu should be modal.&#x22;,
},
]"
/>

Trigger \[#trigger]

The button that toggles the dropdown menu. Wraps Radix UI's `DropdownMenu.Trigger`.

This primitive renders a `<button>` element unless `asChild` is set.

<ParametersTable
  type="ThreadListItemMorePrimitiveTriggerProps"
  parameters="[
{
name: &#x22;asChild&#x22;,
},
]"
/>

Content \[#content]

The container for the dropdown menu items. Wraps Radix UI's `DropdownMenu.Portal` and `DropdownMenu.Content`.

<ParametersTable
  type="ThreadListItemMorePrimitiveContentProps"
  parameters="[
{
name: &#x22;side&#x22;,
type: '&#x22;top&#x22; | &#x22;right&#x22; | &#x22;bottom&#x22; | &#x22;left&#x22;',
default: '&#x22;bottom&#x22;',
description: &#x22;The preferred side of the trigger to render against.&#x22;,
},
{
name: &#x22;sideOffset&#x22;,
type: &#x22;number&#x22;,
default: &#x22;4&#x22;,
description: &#x22;The distance in pixels from the trigger.&#x22;,
},
{
name: &#x22;align&#x22;,
type: '&#x22;start&#x22; | &#x22;center&#x22; | &#x22;end&#x22;',
default: '&#x22;center&#x22;',
description: &#x22;The preferred alignment against the trigger.&#x22;,
},
{
name: &#x22;alignOffset&#x22;,
type: &#x22;number&#x22;,
default: &#x22;0&#x22;,
description: &#x22;An offset in pixels from the align option.&#x22;,
},
{
name: &#x22;portalProps&#x22;,
type: &#x22;PortalProps&#x22;,
description: &#x22;Props to pass to the Portal component.&#x22;,
},
]"
/>

Item \[#item]

A menu item within the dropdown. Wraps Radix UI's `DropdownMenu.Item`.

This primitive renders a `<div>` element unless `asChild` is set.

<ParametersTable
  type="ThreadListItemMorePrimitiveItemProps"
  parameters="[
{
name: &#x22;asChild&#x22;,
},
{
name: &#x22;disabled&#x22;,
type: &#x22;boolean&#x22;,
description: &#x22;Whether the item is disabled.&#x22;,
},
{
name: &#x22;onSelect&#x22;,
type: &#x22;(event: Event) => void&#x22;,
description: &#x22;Event handler called when the user selects an item.&#x22;,
},
]"
/>

Separator \[#separator]

A visual separator between menu items. Wraps Radix UI's `DropdownMenu.Separator`.

<ParametersTable
  type="ThreadListItemMorePrimitiveSeparatorProps"
  parameters="[
{
name: &#x22;asChild&#x22;,
},
]"
/>

Examples \[#examples]

With Icons \[#with-icons]

Complete Thread List Item with More Menu \[#complete-thread-list-item-with-more-menu]

URL: /docs/api-reference/primitives/thread-list-item

Individual thread item with title, archive, and delete controls.

A single thread item within a thread list.

Anatomy \[#anatomy]

API Reference \[#api-reference]

Root \[#root]

Contains all parts of the thread list item.

This primitive renders a `<div>` element unless `asChild` is set. It automatically adds `data-active="true"` and `aria-current="true"` attributes when the thread is the currently active thread.

<ParametersTable
  type="ThreadListItemPrimitiveRootProps"
  parameters="[
{
name: &#x22;asChild&#x22;,
},
]"
/>

Trigger \[#trigger]

A button that switches to the thread when clicked.

This primitive renders a `<button>` element unless `asChild` is set.

<ParametersTable
  type="ThreadListItemPrimitiveTriggerProps"
  parameters="[
{
name: &#x22;asChild&#x22;,
},
]"
/>

Title \[#title]

Displays the title of the thread.

This primitive renders as a React Fragment with no wrapper DOM element. It outputs the thread's title text directly, or the `fallback` content if no title is available.

<ParametersTable
  type="ThreadListItemPrimitiveTitleProps"
  parameters="[
{
name: &#x22;fallback&#x22;,
type: &#x22;ReactNode&#x22;,
description: &#x22;Content to display when the thread has no title.&#x22;,
},
]"
/>

Archive \[#archive]

A button to archive the thread. Only shown for non-archived threads.

This primitive renders a `<button>` element unless `asChild` is set.

<ParametersTable
  type="ThreadListItemPrimitiveArchiveProps"
  parameters="[
{
name: &#x22;asChild&#x22;,
},
]"
/>

Unarchive \[#unarchive]

A button to unarchive the thread. Only shown for archived threads.

This primitive renders a `<button>` element unless `asChild` is set.

<ParametersTable
  type="ThreadListItemPrimitiveUnarchiveProps"
  parameters="[
{
name: &#x22;asChild&#x22;,
},
]"
/>

Delete \[#delete]

A button to permanently delete the thread.

This primitive renders a `<button>` element unless `asChild` is set.

<ParametersTable
  type="ThreadListItemPrimitiveDeleteProps"
  parameters="[
{
name: &#x22;asChild&#x22;,
},
]"
/>

Examples \[#examples]

Basic Thread List Item \[#basic-thread-list-item]

Archived Thread List Item \[#archived-thread-list-item]

URL: /docs/api-reference/primitives/thread-list

Display and manage multiple conversation threads with create and archive actions.

Displays a list of conversation threads.

Anatomy \[#anatomy]

API Reference \[#api-reference]

Root \[#root]

Contains all parts of the thread list.

This primitive renders a `<div>` element unless `asChild` is set.

<ParametersTable
  type="ThreadListPrimitiveRootProps"
  parameters="[
{
name: &#x22;asChild&#x22;,
},
]"
/>

New \[#new]

A button to create a new thread.

This primitive renders a `<button>` element unless `asChild` is set.

<ParametersTable
  type="ThreadListPrimitiveNewProps"
  parameters="[
{
name: &#x22;asChild&#x22;,
},
]"
/>

Items \[#items]

Renders all items in the thread list.

<ParametersTable
  type="ThreadListPrimitive.Items.Props"
  parameters="[
{
name: &#x22;archived&#x22;,
type: &#x22;boolean&#x22;,
default: &#x22;false&#x22;,
description: &#x22;Whether to show archived threads instead of active threads.&#x22;,
},
{
name: &#x22;components&#x22;,
type: &#x22;ThreadListItemComponents&#x22;,
required: true,
description: &#x22;The components to render for each thread list item.&#x22;,
children: [
{
type: &#x22;ThreadListItemComponents&#x22;,
parameters: [
{
name: &#x22;ThreadListItem&#x22;,
type: &#x22;ComponentType&#x22;,
required: true,
description: &#x22;The component to render for each thread in the list.&#x22;,
},
],
},
],
},
]"
/>

ItemByIndex \[#itembyindex]

Renders a single thread list item at the specified index.

<ParametersTable
  type="ThreadListPrimitive.ItemByIndex.Props"
  parameters="[
{
name: &#x22;index&#x22;,
type: &#x22;number&#x22;,
required: true,
description: &#x22;The index of the thread list item to render.&#x22;,
},
{
name: &#x22;archived&#x22;,
type: &#x22;boolean&#x22;,
default: &#x22;false&#x22;,
description: &#x22;Whether to render from archived threads instead of active threads.&#x22;,
},
{
name: &#x22;components&#x22;,
type: &#x22;ThreadListItemComponents&#x22;,
required: true,
description: &#x22;The components to render for the thread list item.&#x22;,
},
]"
/>

URL: /docs/api-reference/primitives/thread

Primitives for the message list, viewport, and welcome screen.

A conversation between a user and an assistant.

Anatomy \[#anatomy]

API Reference \[#api-reference]

Root \[#root]

Contains all parts of the thread.

This primitive renders a `<div>` element unless `asChild` is set.

<ParametersTable
  type="ThreadPrimitiveRootProps"
  parameters="[
{
name: &#x22;asChild&#x22;,
},
]"
/>

Viewport \[#viewport]

The scrollable area containing all messages. Anchors scroll to the bottom as new messages are added.

This primitive renders a `<div>` element unless `asChild` is set.

<ParametersTable
  type="ThreadPrimitiveViewportProps"
  parameters="[
{
name: &#x22;asChild&#x22;,
},
{
name: &#x22;autoScroll&#x22;,
type: &#x22;boolean&#x22;,
default: 'true (false when turnAnchor is &#x22;top&#x22;)',
description:
&#x22;Whether to automatically scroll to the bottom of the viewport when new messages are added while the viewport was previously scrolled to the bottom.&#x22;,
},
{
name: &#x22;turnAnchor&#x22;,
type: '&#x22;top&#x22; | &#x22;bottom&#x22;',
default: '&#x22;bottom&#x22;',
description:
'Controls scroll anchoring behavior for new messages. &#x22;bottom&#x22; is the classic chat behavior where messages anchor at the bottom. &#x22;top&#x22; anchors new user messages at the top of the viewport for a focused reading experience.',
},
{
name: &#x22;scrollToBottomOnRunStart&#x22;,
type: &#x22;boolean&#x22;,
default: &#x22;true&#x22;,
description: &#x22;Whether to scroll to bottom when a new run starts.&#x22;,
},
{
name: &#x22;scrollToBottomOnInitialize&#x22;,
type: &#x22;boolean&#x22;,
default: &#x22;true&#x22;,
description:
&#x22;Whether to scroll to bottom when thread history is first loaded.&#x22;,
},
{
name: &#x22;scrollToBottomOnThreadSwitch&#x22;,
type: &#x22;boolean&#x22;,
default: &#x22;true&#x22;,
description:
&#x22;Whether to scroll to bottom when switching to a different thread.&#x22;,
},
]"
/>

ViewportFooter \[#viewportfooter]

A footer container placed inside `ThreadPrimitive.Viewport` that measures its own height (including top margin) and reports it to the viewport context. The viewport uses this measurement in scroll calculations — for example, as the minimum height for `ViewportSlack` — so that the scroll-to-bottom behaviour accounts for any sticky footer overlapping the message list.

Multiple `ViewportFooter` components may be used; their heights are summed.

This primitive renders a `<div>` element unless `asChild` is set.

<ParametersTable
  type="ThreadPrimitiveViewportFooterProps"
  parameters="[
{
name: &#x22;asChild&#x22;,
},
]"
/>

Messages \[#messages]

Renders all messages. This primitive renders a separate component for each message.

<ParametersTable
  type="ThreadPrimitiveMessagesProps"
  parameters="[
{
name: &#x22;components&#x22;,
type: &#x22;MessageComponents&#x22;,
description: &#x22;The component to render for each message.&#x22;,
children: [
{
type: &#x22;MessageComponents&#x22;,
parameters: [
{
name: &#x22;Message&#x22;,
type: &#x22;ComponentType&#x22;,
description: &#x22;The component to render for each message.&#x22;,
},
{
name: &#x22;UserMessage&#x22;,
type: &#x22;ComponentType&#x22;,
description: &#x22;The component to render for user messages.&#x22;,
},
{
name: &#x22;AssistantMessage&#x22;,
type: &#x22;ComponentType&#x22;,
description: &#x22;The component to render for assistant messages.&#x22;,
},
{
name: &#x22;SystemMessage&#x22;,
type: &#x22;ComponentType&#x22;,
description: &#x22;The component to render for system messages.&#x22;,
},
{
name: &#x22;EditComposer&#x22;,
type: &#x22;ComponentType&#x22;,
description:
&#x22;The component to render when any message type is being edited. Used as a fallback when a role-specific edit composer is not provided.&#x22;,
},
{
name: &#x22;UserEditComposer&#x22;,
type: &#x22;ComponentType&#x22;,
description:
&#x22;The component to render when a user message is being edited. Takes precedence over EditComposer for user messages.&#x22;,
},
{
name: &#x22;AssistantEditComposer&#x22;,
type: &#x22;ComponentType&#x22;,
description:
&#x22;The component to render when an assistant message is being edited. Takes precedence over EditComposer for assistant messages.&#x22;,
},
{
name: &#x22;SystemEditComposer&#x22;,
type: &#x22;ComponentType&#x22;,
description:
&#x22;The component to render when a system message is being edited. Takes precedence over EditComposer for system messages.&#x22;,
},
],
},
],
},
]"
/>

MessageByIndex \[#messagebyindex]

Renders a single message at the specified index in the current thread.

<ParametersTable
  type="ThreadPrimitive.MessageByIndex.Props"
  parameters="[
{
name: &#x22;index&#x22;,
type: &#x22;number&#x22;,
required: true,
description: &#x22;The index of the message to render.&#x22;,
},
{
name: &#x22;components&#x22;,
type: &#x22;MessageComponents&#x22;,
description: &#x22;The component configuration for rendering the message.&#x22;,
children: [
{
type: &#x22;MessageComponents&#x22;,
parameters: [
{
name: &#x22;Message&#x22;,
type: &#x22;ComponentType&#x22;,
description: &#x22;The component to render for each message.&#x22;,
},
{
name: &#x22;UserMessage&#x22;,
type: &#x22;ComponentType&#x22;,
description: &#x22;The component to render for user messages.&#x22;,
},
{
name: &#x22;AssistantMessage&#x22;,
type: &#x22;ComponentType&#x22;,
description: &#x22;The component to render for assistant messages.&#x22;,
},
{
name: &#x22;SystemMessage&#x22;,
type: &#x22;ComponentType&#x22;,
description: &#x22;The component to render for system messages.&#x22;,
},
{
name: &#x22;EditComposer&#x22;,
type: &#x22;ComponentType&#x22;,
description:
&#x22;The component to render when any message type is being edited. Used as a fallback when a role-specific edit composer is not provided.&#x22;,
},
{
name: &#x22;UserEditComposer&#x22;,
type: &#x22;ComponentType&#x22;,
description:
&#x22;The component to render when a user message is being edited. Takes precedence over EditComposer for user messages.&#x22;,
},
{
name: &#x22;AssistantEditComposer&#x22;,
type: &#x22;ComponentType&#x22;,
description:
&#x22;The component to render when an assistant message is being edited. Takes precedence over EditComposer for assistant messages.&#x22;,
},
{
name: &#x22;SystemEditComposer&#x22;,
type: &#x22;ComponentType&#x22;,
description:
&#x22;The component to render when a system message is being edited. Takes precedence over EditComposer for system messages.&#x22;,
},
],
},
],
},
]"
/>

Empty \[#empty]

Renders children only when there are no messages.

ScrollToBottom \[#scrolltobottom]

A button to scroll the viewport to the bottom. Disabled when the viewport is already at bottom.

This primitive renders a `<button>` element unless `asChild` is set.

<ParametersTable
  type="ThreadPrimitiveScrollToBottomProps"
  parameters="[
{
name: &#x22;asChild&#x22;,
},
{
name: &#x22;behavior&#x22;,
type: '&#x22;auto&#x22; | &#x22;instant&#x22; | &#x22;smooth&#x22;',
description:
&#x22;The scroll behavior to use when scrolling to the bottom. Passed to the browser's scrollIntoView API.&#x22;,
},
]"
/>

Suggestion \[#suggestion]

A button that applies a suggestion prompt to the composer. When clicked, it sets the composer text to the given prompt and optionally sends the message immediately.

This primitive renders a `<button>` element unless `asChild` is set.

<ParametersTable
  type="ThreadPrimitiveSuggestionProps"
  parameters="[
{
name: &#x22;prompt&#x22;,
type: &#x22;string&#x22;,
required: true,
description:
&#x22;The text to place in the composer when this suggestion is activated.&#x22;,
},
{
name: &#x22;send&#x22;,
type: &#x22;boolean&#x22;,
default: &#x22;false&#x22;,
description:
&#x22;When true, immediately sends the message instead of only populating the composer.&#x22;,
},
{
name: &#x22;clearComposer&#x22;,
type: &#x22;boolean&#x22;,
default: &#x22;true&#x22;,
description:
&#x22;When send is false, determines whether the composer text is replaced by the prompt (true) or appended to it (false).&#x22;,
},
{
name: &#x22;asChild&#x22;,
},
]"
/>

`ThreadPrimitive.Suggestions` \[#threadprimitivesuggestions]

Renders all configured suggestions from the Suggestions API. Each suggestion is rendered using the provided Suggestion component.

<ParametersTable
  type="ThreadPrimitiveSuggestionsProps"
  parameters="[
{
name: &#x22;components&#x22;,
type: &#x22;{ Suggestion: ComponentType }&#x22;,
description: &#x22;Custom component to render each suggestion.&#x22;,
},
]"
/>

URL: /docs/api-reference/runtimes/assistant-runtime

Root runtime for managing threads, tool UIs, and assistant state.

The `AssistantRuntime` is the root runtime of the application.

`useAui` \[#useaui]

Access the assistant runtime via `useAui`:

Tool UI Registry \[#tool-ui-registry]

The tool UI registry is part of the assistant runtime. It allows you to display custom UI for tool calls, enabling generative UI.

URL: /docs/api-reference/runtimes/attachment-runtime

Hooks for accessing attachment state in composer and messages.

`useAuiState` (Attachment State) \[#useauistate-attachment-state]

Access the current attachment state reactively:

For imperative access and actions, use `useAui`:

Attachment Runtime \[#attachment-runtime]

Attachment State \[#attachment-state]

URL: /docs/api-reference/runtimes/composer-runtime

Runtime for programmatically controlling the message composer.

The composer runtime allows you to view or edit anything related to how new information is added and sent. For instance you can use the composer runtime to read the state, add attachments, update text, send a message, etc.

`useAui` (Composer Actions) \[#useaui-composer-actions]

Grabs the nearest composer (whether it’s the edit composer or the thread’s composer) via `useAui`:

`useAuiState` (Thread Composer State) \[#useauistate-thread-composer-state]

Access the thread’s new message composer state:

`useAui` (Edit Composer Actions) \[#useaui-edit-composer-actions]

Access edit composer actions via `useAui` from within a message component:

`ThreadComposerState` \[#threadcomposerstate]

The state of the thread composer which is the composer the user can interact with at the bottom.

URL: /docs/api-reference/runtimes/message-part-runtime

Hook for accessing message part state within parts.

`useAui` (Message Part Actions) \[#useaui-message-part-actions]

Access message part actions via `useAui`:

`useAuiState` (Message Part State) \[#useauistate-message-part-state]

Access the message part state reactively:

For imperative access, use `useAui`:

URL: /docs/api-reference/runtimes/message-runtime

Hooks for accessing message state and edit composer.

`useAui` (Message Actions) \[#useaui-message-actions]

Access message actions via `useAui`:

`useAuiState` (Message State) \[#useauistate-message-state]

Access message state reactively:

`useAuiState` (Edit Composer) \[#useauistate-edit-composer]

Access the edit composer state (used when editing a message):

URL: /docs/api-reference/runtimes/thread-list-item-runtime

Runtime for managing individual thread list items.

`useAui` (Thread List Item Actions) \[#useaui-thread-list-item-actions]

Access thread list item actions via `useAui`:

`useAuiState` (Thread List Item State) \[#useauistate-thread-list-item-state]

Access the state for a specific thread list item:

URL: /docs/api-reference/runtimes/thread-list-runtime

Runtime for accessing and managing the list of threads.

`useAui` (Thread List Actions) \[#useaui-thread-list-actions]

Access thread list actions via `useAui`:

`useAuiState` (Thread List State) \[#useauistate-thread-list-state]

Access thread list state reactively:

URL: /docs/api-reference/runtimes/thread-runtime

Runtime for thread state, messages, and viewport management.

`useAui` (Thread Actions) \[#useaui-thread-actions]

Access thread actions via `useAui`:

`useAuiState` (Thread State) \[#useauistate-thread-state]

Access the thread state reactively:

`useThreadViewport` \[#usethreadviewport]

Manage thread viewport state (e.g., scrolling):

URL: /docs/runtimes/langgraph/tutorial

Build a stockbroker assistant with LangGraph and assistant-ui.

<>
  {redirect(
        "/docs/runtimes/langgraph/tutorial/introduction",
      )}
</>

URL: /docs/runtimes/langgraph/tutorial/introduction

Build a stockbroker assistant with LangGraph and assistant-ui.

In this tutorial, we will build a stockbroker assistant using LangChain.js, LangGraph.js and assistant-ui.

We will go through the necessary steps to integrate assistant-ui with a LangGraph Cloud endpoint.
Code snippets focus on the setup of the frontend, but we will highlight relevant sections of the backend code as well.

This agent leverages the following features:

Prerequisites \[#prerequisites]

Final Result \[#final-result]

Get Started \[#get-started]

Begin Part 1 of the tutorial by [setting up the frontend](/docs/runtimes/langgraph/tutorial/part-1).

URL: /docs/runtimes/langgraph/tutorial/part-1

Create a Next.js project with the LangGraph assistant-ui template.

Create a new project \[#create-a-new-project]

Run the following command to create a new Next.js project with the LangGraph assistant-ui template:

You should see the following files in your project:

Setup environment variables \[#setup-environment-variables]

Create a `.env.local` file in your project with the following variables:

This connects the frontend to a LangGraph Cloud endpoint running under\
`https://assistant-ui-stockbroker.vercel.app/api`.\
This endpoint is running the LangGraph agent defined [in this repository](https://github.com/assistant-ui/assistant-ui-stockbroker/blob/main/backend).

Start the server \[#start-the-server]

You can start the server by running the following command:

The server will start and you can view the frontend by opening a browser tab to [http://localhost:3000](http://localhost:3000).

You should be able to chat with the assistant and see LLM responses streaming in real-time.

Explore features \[#explore-features]

Streaming \[#streaming]

Streaming message support is enabled by default. The LangGraph integration includes sophisticated message handling that efficiently manages streaming responses:

This means you'll see tokens appear smoothly as they're generated by the LLM, with proper handling of both text content and tool calls.

Markdown support \[#markdown-support]

Rich text rendering using Markdown is enabled by default.

Add conversation starter messages \[#add-conversation-starter-messages]

In order to help users understand what the assistant can do, we can add some conversation starter messages.

URL: /docs/runtimes/langgraph/tutorial/part-2

Display stock ticker information with generative UI components.

In the previous step, we set up the frontend to connect to a LangGraph Cloud endpoint.

In this step, we will set up a component to display stock ticker information.

For reference, this the corresponding code in the backend:

[https://github.com/assistant-ui/assistant-ui-stockbroker/blob/main/backend/src/tools.ts#L193C1-L216C3](https://github.com/assistant-ui/assistant-ui-stockbroker/blob/main/backend/src/tools.ts#L193C1-L216C3)

PriceSnapshotTool \[#pricesnapshottool]

We create a new file under `/components/tools/price-snapshot/PriceSnapshotTool.tsx` to define the tool.

First, we define the tool arguments and result types:

Then, we use `makeAssistantToolUI` to define the tool UI:

This simply displays the tool name and arguments passed to it, but not the result.

Bind tool UI \[#bind-tool-ui]

Try it out! \[#try-it-out]

Ask the assistant for the current stock price of Tesla. You should see the following text appear:

Next, we will visualize the function's result.

Visualizing tool results \[#visualizing-tool-results]

Install dependencies \[#install-dependencies]

The tool result component relies on shadcn/ui's `Card` component. We will install it as a dependency.

You will be prompted to setup a `components.json` file, after this step, a `card` UI component will be installed in your project.

Add `PriceSnapshot` \[#add-pricesnapshot]

We create a new file under `/components/tools/price-snapshot/price-snapshot.tsx` to define the new tool result UI.

Update `PriceSnapshotTool` \[#update-pricesnapshottool]

We will import the new `<PriceSnapshot />` component and use it in the `render` function whenever a tool result is available.

Try it out! \[#try-it-out-1]

Ask the assistant for the current stock price of Tesla. You should see the tool result appear:

Fallback tool UI \[#fallback-tool-ui]

Instead of defining a custom tool UI for every tool, we can also define a fallback UI for all tools that are not explicitly defined.

This requires shadcn/ui's `Button` component. We will install it as a dependency.

Then create a new file under `/components/tools/ToolFallback.tsx` to define the fallback UI.

Bind fallback UI \[#bind-fallback-ui]

The `Thread` component from `@assistant-ui/ui` already includes a built-in `ToolFallback` and `MarkdownText`, so no additional configuration is needed.

URL: /docs/runtimes/langgraph/tutorial/part-3

Add human-in-the-loop approval for tool calls.

Background: LangGraph implementation details \[#background-langgraph-implementation-details]

Our LangGraph backend interrupts the `purchase_stock` tool execution in order to ensure the user confirms the purchase. The user confirms the purchase by submitting a tool message with the `approve` field set to `true`.

Add approval UI \[#add-approval-ui]

We create a new file under `/components/tools/purchase-stock/PurchaseStockTool.tsx` to define the tool.

First, we define the tool arguments and result types:

Then we use `makeAssistantToolUI` to define the tool UI:

Finally, we add a `TransactionConfirmationPending` component to ask for approval.

This requires shadcn/ui's `Card` and `Button` components. We will install them as a dependency.

Then create a new file under `/components/tools/purchase-stock/transaction-confirmation-pending.tsx` to define the approval UI.

Bind approval UI \[#bind-approval-ui]

Try it out! \[#try-it-out]

Ask the assistant to buy 5 shares of Tesla. You should see the following appear:

Add `TransactionConfirmationFinal` to show approval result \[#add-transactionconfirmationfinal-to-show-approval-result]

We will add a component to display the approval result.

Update `PurchaseStockTool` \[#update-purchasestocktool]

We will import the new `<TransactionConfirmationFinal />` component and use it in the `render` function whenever an approval result is available.

Try it out! \[#try-it-out-1]

Confirm the purchase of shares. You should see the approval confirmation UI appear.

## Available Resources

No specific resources found.

## How to Use This Skill

Reference these resources when working with Part 3: Approval UI.