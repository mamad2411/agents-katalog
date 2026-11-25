---
name: avatar
description: Generate avatars with status indicators, initials fallback, and image loading states.
---

# Avatar Component

```css
.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  overflow: hidden;
  position: relative;
  flex-shrink: 0;
}

.avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-initials {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, var(--accent), var(--accent-deep));
  color: white;
  font-size: 14px;
  font-weight: 600;
}

.avatar-status {
  position: absolute;
  bottom: 0;
  right: 0;
  width: 12px;
  height: 12px;
  border-radius: 50%;
  border: 2px solid rgba(16, 18, 30, 0.95);
}

.avatar-status.online { background: #22c55e; }
.avatar-status.away { background: #f59e0b; }
.avatar-status.busy { background: #ef4444; }
.avatar-status.offline { background: #6b7280; }

.avatar-group {
  display: flex;
}

.avatar-group .avatar {
  margin-left: -8px;
  border: 2px solid rgba(16, 18, 30, 0.95);
}

.avatar-group .avatar:first-child {
  margin-left: 0;
}

.avatar-sm { width: 28px; height: 28px; font-size: 11px; }
.avatar-lg { width: 56px; height: 56px; font-size: 18px; }
.avatar-xl { width: 80px; height: 80px; font-size: 24px; }
```

Rules:
- Show initials when image fails to load
- Status dot: online/green, away/yellow, busy/red, offline/grey
- Avatar group: overlap with negative margin
