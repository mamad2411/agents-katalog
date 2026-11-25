---
name: celebrant-cloudflare
description: Compatibility route for approved Cloudflare deployment and domain handover on APC celebrant websites. It does not own mailbox, mail DNS, FormSubmit, or any notification action.
---

# Celebrant Cloudflare compatibility route

Use this short compatibility skill only when an existing workflow names `celebrant-cloudflare`. The current authority is the APC factory provider split:

1. Read `../apc-website-factory/SKILL.md` and its operating guide.
2. For approved website deployment, Pages/Workers, custom domain, or HTTPS work, use `/Users/jack/.agents/skills/cloudflare-deploy/SKILL.md`.
3. For mailbox, mail DNS, FormSubmit wiring, activation, and enquiry delivery, use `../cpanel-cloudflare-formsubmit-email-setup/SKILL.md`.

Before any provider action, present and obtain approval for the exact account/project, target domain, action, and intended outcome. After it, record a redacted readback of the actual requested boundary.

Never embed or retrieve credentials from repository files. Never send Slack or other notifications as part of this route. A successful Cloudflare deployment does not prove form delivery, mailbox operation, Drive archive, or complete handover.
