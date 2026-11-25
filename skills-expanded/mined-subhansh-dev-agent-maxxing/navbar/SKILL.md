---
name: navbar
description: Generate navigation bars with glass effect, scroll-aware styling, and mobile hamburger menu.
---

# Navbar Component

```css
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  background: rgba(6, 6, 10, 0.8);
  backdrop-filter: blur(20px) saturate(1.3);
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
  z-index: 100;
  transition: all 0.3s ease;
}

.navbar.scrolled {
  background: rgba(6, 6, 10, 0.95);
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.3);
}

.nav-link {
  color: rgba(255, 255, 255, 0.5);
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
  padding: 8px 16px;
  border-radius: 8px;
  transition: all 0.2s ease;
}

.nav-link:hover {
  color: rgba(255, 255, 255, 0.9);
  background: rgba(255, 255, 255, 0.05);
}

.nav-link.active {
  color: var(--accent);
  background: rgba(var(--accent-rgb), 0.1);
}
```

Rules:
- Add `.scrolled` class on scroll > 50px
- Mobile: collapse links into hamburger menu
- Keep nav height consistent (64px desktop, 56px mobile)
