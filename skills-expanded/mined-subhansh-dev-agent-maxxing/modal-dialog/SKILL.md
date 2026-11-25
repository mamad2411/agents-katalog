---
name: modal-dialog
description: Generate modal dialogs with backdrop blur, spring animations, and focus trapping.
---

# Modal Dialog Component

```css
.modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(20px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  animation: fadeIn 0.2s ease;
}

.modal-content {
  background: rgba(16, 18, 30, 0.95);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  padding: 32px;
  max-width: 480px;
  width: 90%;
  box-shadow: 0 40px 120px rgba(0, 0, 0, 0.65);
  animation: slideUp 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideUp {
  from { opacity: 0; transform: translateY(20px) scale(0.95); }
  to { opacity: 1; transform: translateY(0) scale(1); }
}
```

Rules:
- Always trap focus inside modal
- Close on Escape key
- Close on backdrop click
- Return focus to trigger element on close
