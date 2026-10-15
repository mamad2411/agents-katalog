---
name: interactive-webpage
description: "Use when you need to create webpages or interactive artifacts, or modify the current UI. Includes resources, guidance, and conventions."
---

# Browser JS Environment: Extensible Agent UI and Web App Building

## Background
The current webpage is a Vite + Vue3-based LLM Agent UI where the user communicates with you. Do not replace the entire `document.body`.

This webpage contains all of your information and context. If the webpage is refreshed or switched away, your session is interrupted and all context is lost, just like variables in the webpage.

You can read and modify the interface through JavaScript.

The interface displays more than content. It also directly shows all of your context, including the system prompt, tool schema, tool calls, tool messages, and reasoning.

The UI provides an interaction area below your latest response.

## Immediate and Asynchronous Interaction
- Besides communicating with the user directly in the chat UI, you can add HTML components for immediate or asynchronous interaction
- Immediate interaction means writing a component during JavaScript execution, then `await`ing until the user completes feedback and using `console.log()` to receive the interaction result. After the JavaScript returns, the system sends the result back to you as a tool message
    - During immediate interaction, if the user does not act for too long, the tool call may time out and the system will report the timeout through a tool message
    - After a timeout, your interaction component still exists, but `console.log` can no longer return data to you; remember to close the interaction window
    - After a timeout, you can try again or switch to asynchronous interaction
- Asynchronous interaction means your tool calls and agentic loop may already be finished, and the user's later interaction automatically sends you a message
    - During asynchronous interaction, `console.log` from user interaction may no longer return through a tool message
    - Use `browserAgent.send({ text })` so you can receive the interaction result yourself
        - The `browserAgent` variable only exists in your JavaScript local scope and represents you; `browserAgent.send` sends a text message to yourself
- There is another pattern called parallel interaction
    - Principle: build the interaction component early, then continue your agentic loop; the user can interact with your component in parallel without interrupting you
    - The popup should avoid covering the main interface when possible. User actions can be recorded asynchronously on `browserAgent.local`
    - When you need the interaction result, check the user's recorded actions and results, then choose the appropriate path
- You can place the deliverable component in the interaction area or use a more prominent global popup, depending on the task
- If you need to record a large amount of data, store it in the `browserAgent.local` object for later filtering and lookup
    - Your multiple tool calls share a `browserAgent.local` object that belongs only to you

## Interaction Area
- The interaction area is below the latest response and is a div with an id
    - Use `browserAgent.shared.uiRootElement.querySelector('#browser-agent-interaction-area')` to get the corresponding element
- The interaction area starts as an empty div with height 0 and is invisible to the user unless you add content
- The interaction area can contain multiple components. Prefer appending child divs instead of overwriting `innerHTML`
- The user does not know the term "interaction area"; you can tell them it is "shown below my response"

## iframe
- If the task is a full webpage or standalone app, append an iframe component to the Interaction Area
- Put a row of control buttons above the iframe component, such as fullscreen, new window, close, or download when needed
    - Keep the control row low-key and visually consistent with the iframe page so it blends into the background

```js
// Fullscreen option:
iframe.requestFullscreen()

// New-window option:
openNewTabBtn.onclick = () => {
  const blob = new Blob([html], {type: 'text/html'});
  const url = URL.createObjectURL(blob);
  window.open(url, '_blank', 'noopener,noreferrer');
};
```

## Large Projects

Use the UMD versions of React and ReactDOM from a CDN to create large projects.
Use Babel Standalone to transform JSX into JavaScript in the browser.
Inline React, ReactDOM, compiled application code, and CSS into a single HTML file, then mount it in an iframe.

If you need to build many files, create your project folder under the OPFS (Origin Private File System) path `browser-agent/workspace`, then build your project there.

## Tips
- If you need `console.log` feedback while creating something, ensure every `console.log` is awaited in the main function and runs before the main function ends; do not put it inside an un-awaited `.then()`
- If you are a multimodal model that can inspect images, you can convert an image to a Blob and use `console.log(Blob)` to get visual feedback
    - Therefore, for image perception and processing tasks, you can inspect images yourself and use canvas to view the effect while processing, instead of introducing machine learning libraries or pushing the task back to the user
- When creating a floating widget, provide a close control to avoid fully blocking the current UI
    - If the user needs to reopen it after closing, you can keep an open button inside the interaction area
- When the user needs an interactive deliverable such as a webpage or standalone app, remind them at the end that you can help package the deliverable and automatically download it to their computer
- If your component needs drag-and-drop upload, note that the user's drag-and-drop action will also trigger the Agent UI's own drag-and-drop upload component
