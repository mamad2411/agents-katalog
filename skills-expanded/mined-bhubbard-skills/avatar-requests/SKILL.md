---
name: avatar-requests
description: How to request user avatars from Gravatar using the user's email hash.
---

# Gravatar Avatar Requests

Gravatar provides a simple API to request a user's avatar image based on their email address.

## How it works
1. Generate the Gravatar SHA256 email hash (see the `gravatar-email-hash` skill).
2. Construct the URL using the base URL: `https://0.gravatar.com/avatar/` appended with the hash.

## Example Usage

```javascript
// Assuming you have the hash
const hash = getGravatarHash('user@example.com');

// Avatar URL
const avatarUrl = `https://0.gravatar.com/avatar/${hash}`;

console.log(avatarUrl);
// Example output: https://0.gravatar.com/avatar/84059b07d4be67b806386c0aad8070a23f18836bbaae342275dc0a83414c32ee
```

## HTML Integration

You can easily use this URL in an image tag:
```html
<img src="https://0.gravatar.com/avatar/84059b07d4be67b806386c0aad8070a23f18836bbaae342275dc0a83414c32ee" alt="User avatar" />
```
