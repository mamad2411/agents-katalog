---
name: zapier-trigger
description: Best practices and steps for creating polling or REST hook triggers in a custom Zapier CLI integration.
---

# Zapier CLI Trigger Creation

This skill provides guidance on implementing triggers in your Zapier integration, which allow your app to watch for new data and kick off Zaps.

## Types of Triggers
1. **Polling Triggers**: Zapier regularly polls your API (e.g., every 5-15 minutes) to see if new records exist.
2. **REST Hooks**: Your app sends an HTTP POST to Zapier immediately when an event occurs, which is much faster and more efficient.

## Implementation Steps

### 1. Polling Trigger Example
Create a file like `triggers/new_contact.js`.

```javascript
const perform = async (z, bundle) => {
  const response = await z.request({
    url: 'https://api.example.com/v1/contacts',
    params: {
      order_by: 'id',
      order: 'desc'
    }
  });
  // Must return an array of objects
  return response.data;
};

module.exports = {
  key: 'new_contact',
  noun: 'Contact',
  display: {
    label: 'New Contact',
    description: 'Triggers when a new contact is created.'
  },
  operation: {
    perform: perform,
    sample: {
      id: 1,
      name: 'Alice'
    }
  }
};
```

### 2. Important Properties
- **key**: Unique identifier for the trigger.
- **noun**: The name of the object being handled.
- **display**: UI elements shown to the user (`label`, `description`).
- **operation.perform**: The function that actually fetches the data. It must return an array.
- **operation.sample**: A representative sample of the data. Required for the Zap editor.

### 3. Pagination
If your API returns a lot of data, use `bundle.meta.page` to handle pagination in polling triggers, which prevents missing data on high-volume accounts.

### 4. REST Hooks
If your API supports webhooks, you define `operation.performSubscribe` and `operation.performUnsubscribe` to register and unregister the webhook URL with your API.

### 5. Testing
Use `zapier test` to run the trigger locally and ensure it returns an array of objects. Make sure each object has an `id` field, which Zapier uses for deduplication.
