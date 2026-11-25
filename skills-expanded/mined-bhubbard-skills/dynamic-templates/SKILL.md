---
name: dynamic-templates
description: Use this skill when the user wants to use SendGrid Dynamic Templates for sending emails.
---

# SendGrid Dynamic Templates

This skill provides guidelines for working with SendGrid Dynamic Transactional Templates.

## Overview
Dynamic Templates allow you to separate the design of your emails from your application code. You can create templates in the SendGrid UI and populate them with dynamic data at send time using Handlebars syntax.

## Best Practices
- **Handlebars Syntax**: Use Handlebars `{{}}` to inject dynamic variables passed in the `dynamic_template_data` of your API request.
- **Conditional Logic**: Use Handlebars helpers like `{{#if}}`, `{{#each}}`, and `{{#unless}}` to build dynamic blocks in your template.
- **Template IDs**: Reference templates by their ID (e.g., `d-1a2b3c4d5e6f7g8h9i0j`) in your API calls rather than hardcoding HTML.
- **Testing**: Use the SendGrid UI to preview templates with sample JSON data before integrating into your codebase.

## Example usage in Node.js
```javascript
const sgMail = require('@sendgrid/mail');
sgMail.setApiKey(process.env.SENDGRID_API_KEY);

const msg = {
  to: 'recipient@example.com',
  from: 'sender@example.com',
  templateId: 'd-your_template_id_here',
  dynamicTemplateData: {
    first_name: 'John',
    order_number: '12345',
    items: [
      { name: 'Widget', price: '$10.00' }
    ]
  },
};

sgMail.send(msg)
  .then(() => console.log('Email sent with dynamic template'))
  .catch(error => console.error(error));
```
