---
name: mail-send
description: Use this skill when the user wants to use the SendGrid Mail Send API v3 to send emails.
---

# SendGrid Mail Send API v3

This skill provides guidelines for using the SendGrid Mail Send API v3.

## Overview
The Mail Send API v3 is the primary endpoint for sending emails through SendGrid. It allows for advanced features like personalization, attachments, and scheduling.

## Best Practices
- **Use the officially supported SDKs**: SendGrid provides SDKs for major languages (e.g., `@sendgrid/mail` for Node.js).
- **Batch sending**: Use personalization arrays to send to multiple recipients in a single API call to improve performance.
- **API Key Security**: Never hardcode your SendGrid API key in source code. Use environment variables (e.g., `SENDGRID_API_KEY`).
- **Error Handling**: Catch and log errors, particularly HTTP 4xx errors, which indicate malformed requests or invalid parameters.

## Example usage in Node.js
```javascript
const sgMail = require('@sendgrid/mail');
sgMail.setApiKey(process.env.SENDGRID_API_KEY);
const msg = {
  to: 'test@example.com',
  from: 'test@example.com',
  subject: 'Sending with Twilio SendGrid is Fun',
  text: 'and easy to do anywhere, even with Node.js',
  html: '<strong>and easy to do anywhere, even with Node.js</strong>',
};
sgMail
  .send(msg)
  .then(() => {
    console.log('Email sent');
  })
  .catch((error) => {
    console.error(error);
  });
```
