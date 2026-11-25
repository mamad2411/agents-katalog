---
name: email-hash
description: Generates the foundational SHA256 email hash required for all Gravatar API operations (avatars and profiles).
---

# Gravatar Email Hash

The email hash is the foundation of all Gravatar functionality. It serves as the universal identifier for accessing both avatars and profile data. Email is the ultimate username for Gravatar.

## Requirements
1. **Trim** leading and trailing whitespace from the email.
2. **Lowercase** the email address.
3. Generate a **SHA256** hash of the resulting string and output as a hex string.

## Example Implementation (JavaScript/Node.js)

```javascript
const crypto = require('crypto');

function getGravatarHash(email) {
  // Trim and lowercase the email - BOTH steps are required
  const processedEmail = email.trim().toLowerCase();
  
  // Create SHA256 hash
  const hash = crypto.createHash('sha256').update(processedEmail).digest('hex');
  
  return hash;
}

const hash = getGravatarHash('user@example.com');
// hash: 84059b07d4be67b806386c0aad8070a23f18836bbaae342275dc0a83414c32ee
```
