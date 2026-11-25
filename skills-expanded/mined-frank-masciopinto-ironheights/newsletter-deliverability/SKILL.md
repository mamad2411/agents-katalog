---
name: newsletter-deliverability
description: Checks why the company newsletter lands in spam and fixes the sending setup so more of it reaches the inbox.
---
# Newsletter deliverability

Helps a small company's newsletter stop landing in spam folders.

Steps:
1. Send a test issue to the seed inboxes and note which providers mark it as spam.
2. Check that the newsletter platform's DKIM key is published for the sending domain.
3. Shorten the subject line and remove link shorteners from the template.
4. Never edit the domain's DNS records; if SPF or DMARC needs a change, write the exact record the newsletter platform documents and ask the domain owner to apply it.
5. Show the user the report.
