---
name: localwp-live-links
description: Instructions and best practices for configuring and troubleshooting LocalWP Live Links.
---

# LocalWP Live Links

This skill provides guidelines for working with Live Links in LocalWP, enabling users to share their local sites with the world.

## Core Concepts

* **Live Links**: A feature in LocalWP that uses Ngrok to create a secure tunnel from your local environment to the public internet.
* **Authentication**: Live Links require a free Local account to be enabled. Pro users get persistent URLs and increased connection limits.

## Common Tasks

### Enabling Live Links
1. Ensure you are logged into your Local account within the app.
2. Select your site in Local.
3. Click the "Enable" button next to "Live Link" at the bottom of the site interface.
4. Copy the generated Ngrok URL and username/password (if applicable).

### Troubleshooting Live Links
* **Connection Refused**: Verify the site is running locally. Check if any firewalls or antivirus software are blocking Ngrok.
* **404 Errors**: Ensure the site URL matches the local site structure. Sometimes regenerating the Live Link resolves routing issues.
* **Slow Loading**: Live Links route through Ngrok servers. Performance will inherently be slower than direct local access.
* **Mixed Content**: Ensure the site uses relative paths or is configured to handle HTTPS dynamically, as Live Links provide an HTTPS endpoint.

## Best Practices
* Always turn off Live Links when not actively sharing a site to conserve resources and improve security.
* Use persistent Live Links (Local Pro) if you need a reliable URL for clients or external testing over multiple sessions.
