---
name: oss-tools-part3-checked
description: The open-source tools carousel Part 3 (Penpot, Cal.com, Open WebUI, Browser Use, Dify) and the "5 tools everyone will be using in 2027" cards (n8n, SERPtag, Cursor, Claude, ManyChat) with each tool's licence checked from its repo - including that github.com/calcom/cal.com is now Cal.diy (MIT, enterprise features removed, personal use) and that Dify and n8n are not plain open source. Use when someone wants a free replacement for Figma, Calendly or ChatGPT-style tools, or asks whether a tool is really open source.
---

# Open-source tools, part 3, checked

Sources: a 6-slide "5 open-source tools that shouldn't be free, Part 3" carousel and a "5 tools everyone will be using in 2027" card series. Star counts on the slides (Open WebUI 153,000; Browser Use 116,000; Dify 157,000; Cal.com 40,000+) are unverified. Licences below were read from the cloned repos on 5 October 2026.

| Tool | Replaces | Licence in the repo | The catch |
|---|---|---|---|
| Penpot | Figma | MPL-2.0 | Weak copyleft on modified files; self-hosting needs Docker and ops work |
| Cal.com | Calendly | The `calcom/cal.com` clone is **Cal.diy**: MIT, "all enterprise/commercial code removed", and its own README says "strictly recommended for personal, non-production use" and points businesses to Cal.com | No Teams, Organizations, Insights, Workflows or SSO/SAML in this edition. The slide's "$16 a month" is a hosted-plan price that was not checked |
| Open WebUI | ChatGPT-style front end | Custom licence with a branding clause (batch 106: no removing or replacing branding above 50 users in 30 days without permission) | Not OSI open source |
| Browser Use | agent that drives a browser | MIT | Needs an LLM key; it controls a real browser, so use a separate profile |
| Dify | agent and workflow builder | Modified Apache-2.0: **no multi-tenant service** without written permission, and **do not remove the logo or copyright** in the frontend | Fine for one company's internal use; a SaaS built on it needs a commercial licence |

## The "2027" list

n8n, SERPtag, Cursor, Claude, ManyChat. The prediction cannot be verified and says nothing about quality. n8n's repo uses the **Sustainable Use License** (plus a separate Enterprise licence for some files), so it is source-available, not open source. SERPtag was not found. Cursor, Claude and ManyChat are paid products.

## Rule

Before you build on one of these, read its LICENSE file, then check whether your use is internal, hosted for others, or resold. Use `/oss-stack-pick` for the choice and `open-source-swap-stack-8` for the earlier list.
