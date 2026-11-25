---
name: toast-notification
description: Generate toast notifications with slide-in animation, auto-dismiss, and stack management.
---

# Toast Notification Component

```css
.toast-container {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 9999;
  display: flex;
  flex-direction: column;
  gap: 8px;
  pointer-events: none;
}

.toast {
  pointer-events: auto;
  padding: 14px 20px;
  background: rgba(16, 18, 30, 0.95);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  backdrop-filter: blur(20px);
  color: rgba(255, 255, 255, 0.9);
  font-size: 14px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
  animation: toastIn 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
  display: flex;
  align-items: center;
  gap: 10px;
  max-width: 360px;
}

.toast.toast-exit {
  animation: toastOut 0.2s ease forwards;
}

.toast-success { border-left: 3px solid #22c55e; }
.toast-error { border-left: 3px solid #ef4444; }
.toast-info { border-left: 3px solid #3b82f6; }

@keyframes toastIn {
  from { opacity: 0; transform: translateX(100%); }
  to { opacity: 1; transform: translateX(0); }
}

@keyframes toastOut {
  to { opacity: 0; transform: translateX(100%); }
}
```

Auto-dismiss after 3-5 seconds. Stack newest on top.
