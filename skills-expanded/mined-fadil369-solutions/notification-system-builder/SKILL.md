---
name: "Notification System Builder"
version: "1.0.0"
description: "Builds notification systems with unified delivery, user preferences, and channel management."
author: "workspace"
activated: false
---

# Notification System Builder

## Overview

Builds unified notification systems across email, SMS, push, and in-app channels.

## Decision Framework

### When to use
- User needs updates from multiple sources
- Multiple delivery channels required
- User preferences for notification types needed

### When NOT to use
- Simple single-channel alerts
- Real-time streaming data

## Decision Tree

```
Is notification user-triggered?
├── Yes → In-app toast + optional email
├── No → Is it time-sensitive?
│   ├── Yes → Push notification + SMS fallback
│   └── No → Email digest or in-app badge
```

## Trigger Phrases

- "Add notifications"
- "Alert users when..."
- "Send email when..."
- "Push notifications for..."

## Notification Types

| Type | Channel | Priority | Retention |
|------|---------|----------|-----------|
| Transactional | Email + In-app | High | 30 days |
| Marketing | Email | Low | 90 days |
| System | In-app | Medium | 7 days |
| Alert | Push + SMS | Critical | Until read |

## Implementation Patterns

### Preference Schema
```json
{
  "channels": {
    "email": { "enabled": true, "frequency": "immediate" },
    "push": { "enabled": true, "quiet_hours": ["22:00", "08:00"] },
    "sms": { "enabled": false },
    "in_app": { "enabled": true }
  },
  "types": {
    "marketing": { "enabled": false },
    "updates": { "enabled": true },
    "alerts": { "enabled": true }
  }
}
```

### Delivery Queue
```javascript
class NotificationQueue {
  async enqueue(notification) {
    const prefs = await this.getUserPreferences(notification.userId);
    const channels = this.resolveChannels(notification.type, prefs);
    for (const channel of channels) {
      await this.queueChannelDelivery(notification, channel);
    }
  }
}
```

### Batching Strategy
```javascript
const batchWindow = {
  email: { duration: '1h', maxItems: 10 },
  push: { duration: '5m', maxItems: 5 },
  sms: { duration: '0', maxItems: 1 }
};
```
