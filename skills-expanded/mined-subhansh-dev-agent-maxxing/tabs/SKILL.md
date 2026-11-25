---
name: tabs
description: Generate tab navigation with animated indicator and keyboard support.
---

# Tabs Component

```css
.tabs {
  display: flex;
  gap: 4px;
  padding: 4px;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.06);
}

.tab {
  flex: 1;
  padding: 10px 16px;
  border: none;
  background: transparent;
  color: rgba(255, 255, 255, 0.4);
  font-size: 13px;
  font-weight: 500;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  position: relative;
}

.tab:hover {
  color: rgba(255, 255, 255, 0.7);
}

.tab.active {
  color: rgba(255, 255, 255, 0.9);
  background: rgba(255, 255, 255, 0.06);
}

.tab-panel {
  display: none;
  padding: 16px 0;
}

.tab-panel.active {
  display: block;
  animation: fadeIn 0.2s ease;
}
```

Rules:
- Arrow keys navigate between tabs
- Tab panels swap with fadeIn animation
- Active indicator can be a sliding background instead of color change
