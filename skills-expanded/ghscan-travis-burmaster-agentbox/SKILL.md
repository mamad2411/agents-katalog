---
name: client-communications
description: >
  Draft client-facing emails, memos, and updates. Matches tone to the client relationship
  and translates complex legal analysis into clear, actionable guidance.
license: MIT
allowed-tools: Read Edit Grep Glob Bash
metadata:
  author: claude-law-firm
  version: "1.0.0"
  category: legal
---

# Client Communications Skill

## Trigger
Activate when the user needs to draft an email, memo, letter, or other communication to a client about a legal matter.

## Communication Types

### 1. Deal Update Email
For keeping clients informed during a transaction.

Structure:
- **Subject line**: Clear, specific (e.g., "Series A — Status Update and Next Steps")
- **Opening**: One sentence on where things stand
- **Key developments**: Bulleted, plain English
- **Action items for the client**: Clearly flagged with deadlines if applicable
- **Next steps on our side**: What we're doing and when
- **Closing**: Availability and contact info

Tone: Professional but approachable. The client should feel informed, not overwhelmed.

### 2. Risk Advisory Email
For flagging a legal issue, contract risk, or strategic consideration.

Structure:
- **Bottom line**: State the issue and your recommendation in 2-3 sentences
- **Background**: Brief context (assume the client knows their own business)
- **Analysis**: What the risk is, how likely it is, and what the consequences could be
- **Options**: 2-3 options with pros and cons for each
- **Recommendation**: Which option you recommend and why
- **Caveat**: Any uncertainty or areas where more information is needed

Tone: Direct but measured. Don't alarm unnecessarily. Don't minimize real risks.

### 3. Cover Email
For sending a document (contract, memo, redline) to the client.

Structure:
- **What's attached**: Name the document and version
- **Key points**: 3-5 bullet points highlighting the most important aspects
- **What we need from you**: Any input, decisions, or approvals needed
- **Timeline**: When you need their response

Tone: Brief and practical. The document speaks for itself.

### 4. Engagement Letter / Scope Communication
For defining the scope of a legal engagement.

Structure:
- **Scope of work**: What we will and won't do
- **Fee arrangement**: Hourly, flat fee, subscription, or hybrid
- **AI usage provision**: Frame AI as an efficiency and quality enhancer, emphasize attorney supervision, tie data handling to confidentiality obligations
- **Timeline**: Expected duration and milestones
- **Terms**: Reference to standard engagement terms

## Principles
- Never use legalese in client communications unless the client is a lawyer
- Translate legal concepts into business language
- Always include clear next steps and who is responsible for what
- Match the formality level to the client relationship
- Keep emails under 500 words unless the complexity demands more
- If the matter is sensitive, flag that the communication is privileged
