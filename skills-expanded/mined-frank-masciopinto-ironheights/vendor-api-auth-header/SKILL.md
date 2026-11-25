---
name: vendor-api-auth-header
description: Reference for calling the Example Video API. Docs only, no scripts.
---
# Example Video API reference

Base URL: `https://api.examplevideo.dev`

## Manual polling (REST)

```javascript
async function pollTask(taskId) {
  const response = await fetch(`https://api.examplevideo.dev/v1/tasks/${taskId}`, {
    headers: { 'Authorization': `Bearer ${process.env.EXAMPLEVIDEO_API_SECRET}` }
  });
  return response.json();
}
```
