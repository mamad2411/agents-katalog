---
name: gemini-agent-dev-support
description: Guidelines for Gemini API development. Used to pre-define architecture in the planning phase and verify code patterns in the coding/debugging phase.
---

# Gemini API Development Skill

## 1. Planning Phase (Pre-definition)
Before proposing an implementation plan, you must verify and align on these architectural constraints:
- **No Memory**: Query Docs MCP `search_docs` or refer to `llms.txt` for up-to-date SDK specifications.
- **SDK Import**: Strictly use `@google/genai` (JS/TS) or `google-genai` (Python). Never import legacy SDKs.
- **Origin**: Web apps must run on a local dev server (e.g. `localhost`). Absolutely no `file://` execution.
- **Credentials Policy**: Keep API keys and credentials on the server-side/backend proxy. Never expose keys in client-side code.
- **Time Grounding**: Plan must include dynamic system instruction time injection.
- **No Mocking**: Non-functional elements must be disabled or hidden. No static stub response in production code paths.

---

## 2. Coding & Debugging Phase (Standard Patterns)
Always use these clean code patterns without adding comments in generated production code:

### A. IME & Send Event
```javascript
input.addEventListener('keydown', (e) => {
  if (e.key === 'Enter') {
    if (e.isComposing || e.keyCode === 229) return;
    if (!e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  }
});
```
- Clear `input.value` immediately after sending.
- Disable input element and send button during `loading === true`.
- Prevent sending if `input.value.trim() === ""`.
- **Voice Input**: Implement actual microphone permission requests, UI state indicators (listening, error, retry), and text input fallback. Never use a silent mic icon placeholder.

### B. Model Selection & Time Awareness
```javascript
new GoogleGenAI({}).models.list();
```
```javascript
const systemInstruction = `Current local time: ${new Date().toLocaleString()}`;
```
```javascript
// API Key Validation (verify by listing models via SDK)
async function validateApiKey(apiKey) {
  try {
    const ai = new GoogleGenAI({ apiKey });
    await ai.models.list();
    return true;
  } catch {
    return false;
  }
}
```

### C. Tool Combination (Gemini 2.x vs 3.x)
```javascript
import { GoogleGenAI } from '@google/genai';
const ai = new GoogleGenAI({});

function adaptGenerateContent(options) {
  // call tools seperately
  // call official tools seperately
}

function withOfficial(options) {
  // append official tools
}

async function callGemini(modelName, userInput, tools = [], enableSearch = false) {
  const options = {
    model: modelName,
    contents: userInput,
    config: { tools }
  }
  return checkAllowToolCombine(modelName) ?
    await adaptGenerateContent(options) :
    await ai.model.generateContent(options);
}
```
- **Tool Grounding**: Update `systemInstruction` dynamically. If search is disabled, append: `"Tool google_search is disabled. Do not attempt to call it."`

### D. Tool Error Handling
```json
{
  "functionResponse": {
    "name": "unknown_or_failed_tool",
    "response": {
      "error": "Error message for model auto-correction."
    }
  }
}
```
- Never throw directly on tool execution error or unknown tool name. Return the structured error JSON above.

### E. History Schema
- No plural `functionCalls` field in history object. Map each single `functionCall` to its corresponding `functionResponse`.
- Preserve `thought`, `signature` (within interactions context), and server-side tool context in the dialog loop.

### F. Error Handling & Safe Rendering
```json
{
  "error": {
    "code": "API_LIMIT_EXCEEDED",
    "message": "Friendly error summary in Traditional Chinese.",
    "details": {
      "status": 429,
      "reason": "rate_limit_exceeded",
      "debug_info": "Debug stack trace without API keys."
    }
  }
}
```
```javascript
import { marked } from 'marked';
import DOMPurify from 'dompurify';

const safetyHtml = DOMPurify.sanitize(marked.parse(markdown));
```

---

## Output Format

### Verification Log
- Docs MCP / Skill Query Link: [e.g. search_docs query]
- Models: [e.g. gemini-2.5-flash]

### Checklist
| ID | Item | Result | Evidence |
| --- | --- | --- | --- |
| S1 | SDK / Tooling | PASS / FAIL / N/A | [code line or test screenshot link] |

### Code Changes
- `[file path]`: [description of change]

### Smoke Test Output
```text
[test execution logs]
```

### Remaining Risks
- [untested features, proxies, or "None"]

### Recurrence Protection
- [Describe protection mechanism: Rule / Hook / Test / Skill / "Not Needed" with reason]
