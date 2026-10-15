---
name: rice-agent-auth-gate
description: Guest users see an upsell/sign-in prompt instead of auth-required content or actions; never show a 404 or redirect
---

# Auth Gate Conventions

Two levels of auth gating, never a redirect or 404.

## Page-Level Gate (e.g. /network, /messages)

Use a wrapper component. If unauthenticated, show an upsell hero with:
- Feature name heading ("Network", "Messages", etc.)
- 1-2 sentence description of what they're missing
- "Sign in" button that opens AuthModal
- Nice illustration/icon

```tsx
// Guest sees this
<PageGate feature="Network" description="Connect with traders in your area" />
// Authenticated sees this
<NetworkList />
```

## Action-Level Gate (e.g. Like, Comment, Save)

Use `useRequireAuth` hook. If unauthenticated, open AuthModal. After login, action fires.

```tsx
const requireAuth = useRequireAuth()
<button onClick={() => requireAuth(() => toggleLike(postId), "like posts")}>
  Like
</button>
```

## AuthModal

Shared modal component with Login/Register tabs. Opened by both gates.
Props: `action` (e.g. "like posts"), `onSuccess` callback.

## Key Rule

Never redirect. Keep user in place — modal or inline upsell overlay.
