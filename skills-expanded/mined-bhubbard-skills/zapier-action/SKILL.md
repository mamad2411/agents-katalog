---
name: zapier-action
description: Guide on creating actions (creates or searches) for a custom Zapier CLI integration to push data or find records.
---

# Zapier CLI Action Creation

This skill covers implementing actions in a custom Zapier CLI integration. Actions allow users to create or update data in your app, or search for existing data.

## Types of Actions
1. **Creates**: Push new data into your app (e.g., Create Contact).
2. **Searches**: Find existing records in your app (e.g., Find Contact).

## Implementation Steps

### 1. Create Action Example
Create a file like `creates/create_contact.js`.

```javascript
const perform = async (z, bundle) => {
  const response = await z.request({
    method: 'POST',
    url: 'https://api.example.com/v1/contacts',
    body: {
      name: bundle.inputData.name,
      email: bundle.inputData.email
    }
  });
  
  // Must return a single object or an array of objects
  return response.data;
};

module.exports = {
  key: 'create_contact',
  noun: 'Contact',
  display: {
    label: 'Create Contact',
    description: 'Creates a new contact in the system.'
  },
  operation: {
    inputFields: [
      { key: 'name', label: 'Name', required: true, type: 'string' },
      { key: 'email', label: 'Email', required: true, type: 'string' }
    ],
    perform: perform,
    sample: {
      id: 123,
      name: 'Bob',
      email: 'bob@example.com'
    }
  }
};
```

### 2. Input Fields
The `operation.inputFields` array defines the form users fill out in the Zap editor. 
- You can specify `type`, `required`, and `helpText`.
- You can also make dynamic dropdowns by pointing an input field to a search or trigger.

### 3. The `perform` Function
- It uses `bundle.inputData` to access the values the user mapped in the editor.
- It makes the HTTP request to your API to perform the action.
- It must return the created object (or an array of objects).

### 4. Searches
Searches are very similar but are used to find an existing record. They often pair with a "Create" action to form a "Find or Create" action.

### 5. Error Handling
If the API returns a 4xx or 5xx error, you can throw a `z.errors.Error` or `z.errors.HaltedError` to properly fail the Zap and inform the user.
