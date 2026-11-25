<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-dukrov
description: CTF writeups and security challenges by dukrov.
---

# Writeups by dukrov

Source repository: `/repos/dukrov`

## Repository Index

- vulnerability-report-templates/README.md
- vulnerability-report-templates/general.md

## Writeup Content


### File: vulnerability-report-templates/README.md

# 🐞 Vulnerability Report Templates

Hey there 👋  
This repo is a collection of clean, easy-to-use vulnerability report templates — built by a hacker, for hackers.

Whether you’re just starting out or you’re writing your 100th report, having a solid template saves time and keeps things professional. Plus, it helps avoid the dreaded *"Can you clarify the impact?"* message from triagers. We've all been there.

---

## ✨ What's Inside?

Pre-written templates for common vulnerability types like:

- Role Based Access Control
- IDOR (Insecure Direct Object Reference)
- XSS (Cross-Site Scripting)
- HTML Injection
- Open Redirect
- and more...

### 🤝 Want to Contribute?
Found a cool format? Got a clean template for a less-common bug? PRs are welcome! Just try to keep it simple, human-readable, and helpful.

### 💬 Why this exists
Writing good reports is a skill, and it makes a difference — not just for bounty payouts, but for helping fix real security problems. The goal here is to save time, reduce friction, and maybe even help someone land their first triage.

If this repo helps even one hacker write a better report — worth it.

Made with 💻 + ☕ by [dukrov](https://github.com/dukrov)



### File: vulnerability-report-templates/general.md

# [Summary of the vulnerability]  
A short and clear explanation of the issue and its impact.  
Example: An HTML injection vulnerability was discovered in the "Message" field of the email report feature, allowing arbitrary HTML to be rendered in the admin interface.

---

## Platform Affected  
Where this was found — domains, environments, or apps tested.

- Example: [app.example-staging.com](https://app.example-staging.com)

---

## Steps To Reproduce  

1. Navigate to the affected functionality  
2. Fill in a specific field or trigger an action  
3. Inject a payload or manipulate a request  
4. Observe the unexpected or insecure behavior  
5. Optional: Describe where/how the impact is visible  
6. Include anything else needed to reproduce cleanly  

---

## HTTP Requests  
Paste relevant requests & responses (can be redacted/simplified):

`POST /api/v1/submit HTTP/1.1 `
`Host: app.example.com`
`Authorization: Bearer YOUR-TOKEN`
`Cookie: _sess...`
`X-Csrf-Token: UgPst8X...`

`{ "field": "value", "payload": "<h1>HTML</h1>" }`


---

## Remediation  
Suggestions for fixing the issue.

- Example: Sanitize HTML content in the message field before rendering it in the admin interface.
- Or: Implement proper server-side validation and output encoding.

---

## Proof of Concept  

- Attach a screenshot, video, or hosted demo link.  
- You can embed images using Markdown:  
  `![screenshot](../assets/html-injection-example.png)`


