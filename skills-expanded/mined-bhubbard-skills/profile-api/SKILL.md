---
name: profile-api
description: Interacting with the Gravatar Profile REST API to fetch rich user profile data using an email hash.
---

# Gravatar Profile REST API

The Gravatar Profile REST API allows you to fetch rich profile data including display names, avatars, locations, biographies, interests, and verified social media accounts. This solves the "Cold Start Problem" for user onboarding.

## Prerequisites
1. Generate the Gravatar SHA256 email hash (see the `gravatar-email-hash` skill).
2. (Recommended) Generate a Gravatar API key from the Developer Dashboard to include as a Bearer Token in the `Authorization` header.

## API Endpoint
The base URL is: `https://api.gravatar.com/v3`
To fetch a profile, use: `https://api.gravatar.com/v3/profiles/${hash}`

## Example Integration (JavaScript)

```javascript
const hash = getGravatarHash('user@example.com'); // See email hash skill
const profileUrl = `https://api.gravatar.com/v3/profiles/${hash}`;

// With authentication (recommended)
fetch(profileUrl, {
  headers: {
    'Authorization': 'Bearer YOUR_API_KEY'
  }
})
.then(response => response.json())
.then(profile => {
    console.log("User Profile Data:", profile);
    // You can access profile data like display name, location, about me, etc.
});
```

## Benefits
- Retrieve user profile data for over 70 million users.
- Simplify onboarding by leveraging existing data instead of asking users to fill out forms.
- Personalize user experiences using Gravatar interest data.
