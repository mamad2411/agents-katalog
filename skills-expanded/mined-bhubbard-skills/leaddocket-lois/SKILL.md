---
name: leaddocket-lois
description: >
  Guide to using LOIS (LeadsAI), LeadDocket's built-in AI assistant, within
  the LeadDocket UI. LOIS operates at the individual lead level and can answer
  questions about a lead, provide analysis and summaries, create notes, and
  answer how-to questions about LeadDocket by searching the Help Center.
  Use this skill when the user asks about the LeadDocket AI assistant, how to
  query lead data conversationally, or how to use voice input in LeadDocket.
---

# LeadDocket — LOIS (LeadsAI)

**LOIS** (LeadsAI) is LeadDocket's built-in conversational AI assistant. It
is accessed directly in the LeadDocket UI at the lead level — not via API.

> Support article: [LOIS in Lead Docket](https://support.leaddocket.com/hc/en-us/articles/51820430138779-LOIS-in-Lead-Docket)

---

## Accessing LOIS

1. Open a lead in LeadDocket
2. Click the **LOIS icon** in the top navigation of the lead
3. The LOIS chat window opens on the right side
4. Type a question or request in the chat box

---

## Input Methods

| Method | How to use |
|--------|-----------|
| **Type** | Type directly into the chat box and press Enter |
| **Microphone icon** | Dictates your request; text appears in the chat box for you to review and submit |
| **Waveform icon** | Dictates and auto-submits when you stop or pause speaking |

---

## What LOIS Can Do

### Answer questions about the current lead

LOIS has access to all lead sections: notes, messages, tasks, dates, deadlines, payment information, files, and more.

```
Example questions:
- "What's the latest on this lead?"
- "How can I move this lead forward?"
- "What type of insurance does my client have?"
- "Summarize all messages from the last 30 days"
- "What tasks are overdue?"
```

### Add notes to the lead

LOIS can create and add a note directly to the lead. The response includes a link to the created note.

```
Example: "Add a note that the client confirmed their accident date is March 15, 2026"
```

### Answer LeadDocket how-to questions

LOIS searches the LeadDocket Help Center and returns answers with links to the relevant support articles.

```
Example questions:
- "How can I create a task template?"
- "Where would I add a referral source?"
- "How can I set up an auto-reply email for opportunities?"
```

---

## Follow-up Conversations

LOIS maintains context within a chat session — you can ask follow-up questions to refine or expand results.

```
Q: "What's the latest on this lead?"
A: [Summary]
Q: "Which task has the earliest due date?"
A: [Task detail from the context above]
```

---

## Clearing the Chat

LOIS does not support multiple ongoing conversations. Use **Clear Chat** before starting an unrelated request to avoid confusing the AI context.

---

## Limitations

| Limitation | Details |
|------------|---------|
| **Single lead only** | LOIS can only access the lead you have open. It cannot answer questions across multiple leads. |
| **No document content** | LOIS cannot read the contents of attached files/documents. |
| **No bulk queries** | Cannot answer "give me a list of the most important tasks across all my leads." |
| **Context window** | Very long conversations may lose early context. Use Clear Chat to reset. |

---

## Best Practices

- **Be in the right lead**: LOIS is lead-specific. Make sure you're on the lead you want to ask about before opening LOIS.
- **Be specific**: "What are all the notes from May?" gets a better response than "What happened?"
- **Use for note creation**: Dictating notes via LOIS (waveform icon → stop → note created) is faster than typing manual notes, especially after calls.
- **Clear chat between topics**: Switching from lead-specific questions to how-to questions (or vice versa) works best after clearing chat.
