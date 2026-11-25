---
name: zapier-auth
description: Guides the process of setting up and testing authentication (OAuth2, API Key, Basic, Session) for a custom Zapier CLI integration.
---

# Zapier CLI Authentication Guide

This skill provides instructions for implementing authentication in a custom Zapier CLI integration.

## Key Concepts
Authentication in the Zapier CLI is primarily defined in your `authentication.js` or directly within the main configuration object. Once a user authenticates, their credentials become available via `bundle.authData` in all subsequent triggers and actions.

## Supported Schemes
1. **OAuth v2**: Requires authorization URL, access token request logic, and optionally refresh token logic.
2. **API Key / Basic Auth**: Requires defining input fields for the user to provide credentials, and a `test` function to verify them.
3. **Session Auth**: Often used when an API uses session tokens instead of standard API keys.

## Implementation Steps

### 1. Define the Authentication Object
Create an `authentication.js` file (or define it in your `index.js`).
Example for API Key:
```javascript
const authentication = {
  type: 'custom',
  test: {
    url: 'https://api.example.com/v1/me'
  },
  fields: [
    { key: 'api_key', type: 'string', required: true, helpText: 'Found in your account settings.' }
  ],
  connectionLabel: '{{username}}'
};

module.exports = authentication;
```

### 2. Include in App Definition
Ensure it's included in your main `index.js` or app definition:
```javascript
const authentication = require('./authentication');

const App = {
  version: require('./package.json').version,
  platformVersion: require('zapier-platform-core').version,
  authentication: authentication,
  // ...
};
```

### 3. Middleware for Request Authentication
Usually, you want to attach the auth headers to every request automatically. Use `beforeRequest` middleware.
```javascript
const includeApiKey = (request, z, bundle) => {
  if (bundle.authData.api_key) {
    request.headers['Authorization'] = `Bearer ${bundle.authData.api_key}`;
  }
  return request;
};

// In App definition:
beforeRequest: [includeApiKey],
```

### 4. Testing Authentication
Run `zapier test` to verify your test endpoint.
Use `zapier env:set` to configure environment variables for local testing without hardcoding credentials in your code.
