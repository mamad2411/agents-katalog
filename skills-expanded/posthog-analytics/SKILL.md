---
name: posthog-analytics
description: PostHog analytics and session replay integration for React Native mobile apps. Use when adding event tracking, understanding session replay behavior, or troubleshooting analytics setup.
---

# PostHog Analytics & Session Replay

## What's Already Configured

The bootstrap includes a complete PostHog setup with:

- **Session Replay** - Records user sessions with privacy protections
- **Automatic Screen Tracking** - Tracks navigation automatically via `ScreenTracker` component
- **Event Tracking** - Ready to use via `usePostHog()` hook
- **Privacy Controls** - Text inputs and images are masked by default

## Files Involved

| File | Purpose |
|------|---------|
| `lib/posthog.ts` | Configuration with session replay plugin |
| `app/_layout.tsx` | PostHogProvider wrapper and ScreenTracker component |
| `app.json` | PostHog plugin registration |
| `.env.example` | Environment variable template |

## How Session Replay Works

### What Gets Recorded
- ✅ Screen views and navigation
- ✅ Touch interactions (taps, swipes)
- ✅ UI changes and animations
- ✅ Network requests (with `captureNetworkTelemetry: true`)
- ✅ Console logs (with `captureLog: true`)

### Privacy Protections
- 🔒 **Text inputs masked** - All form inputs show as `****`
- 🔒 **Images masked** - Photos and avatars are blurred/hidden
- 🔒 **Sensitive data protected** - No actual typed content recorded

### Recording Behavior
- Starts automatically when app launches
- Continues throughout the session
- Stops when app is closed/backgrounded
- Each session is a separate replay in PostHog dashboard
- Data is compressed and sent in batches (not real-time)

### Data Usage
- ~100-500KB per minute of usage
- Throttled to 1 second intervals (`throttleDelayMs: 1000`)
- Only captures visual changes, not full video

## Configuration Options

All settings are in `lib/posthog.ts`:

| Setting | Default | Purpose |
|---------|---------|---------|
| `maskAllTextInputs` | `true` | Hide all text input content |
| `maskAllImages` | `true` | Blur/hide all images |
| `captureLog` | `true` | Include console logs in replay |
| `captureNetworkTelemetry` | `true` | Track API calls |
| `throttleDelayMs` | `1000` | Snapshot interval (milliseconds) |
| `captureNativeAppLifecycleEvents` | `true` | Track app open/close/background |

## Using PostHog in Your App

### Track Custom Events

Import the hook and use it anywhere:

```typescript
import { usePostHog } from 'posthog-react-native';

const posthog = usePostHog();

// Track an event
posthog?.capture('button_pressed', {
  button_name: 'checkout',
  screen: 'product_detail',
});
```

### Identify Users

Set user identity (typically after login):

```typescript
posthog?.identify(userId, {
  email: user.email,
  plan: 'premium',
});
```

### Reset on Logout

Clear user identity:

```typescript
posthog?.reset();
```

### Set User Properties

Update user metadata:

```typescript
posthog?.setPersonProperties({
  credits: 100,
  subscription_status: 'active',
});
```

## Environment Variables

Required for PostHog to work:

```env
EXPO_PUBLIC_POSTHOG_KEY=phc_your_project_key
EXPO_PUBLIC_POSTHOG_HOST=https://eu.i.posthog.com
```

If not set, PostHog is automatically disabled with a console warning.

## Rebuild Required

PostHog session replay uses native modules. After configuration changes to `app.json`, you must rebuild:

```bash
npx expo prebuild --clean
npx expo run:ios  # or run:android
```

Or with EAS:
```bash
eas build --profile development-client --platform ios
```

## Viewing Data in PostHog

### Session Replays
1. Go to PostHog → Session Replay
2. Click on a session to watch the replay
3. See timeline of events, network calls, and console logs

### Events
1. Go to PostHog → Events
2. See all captured events:
   - `$screen` - Automatic screen views
   - `$pageview` - Navigation tracking
   - Custom events you capture

### Users
1. Go to PostHog → Persons
2. See identified users with their properties
3. View their session history and events

## Common Issues

### "Waiting for events" in Dashboard
**Cause:** App hasn't been rebuilt after configuration changes  
**Fix:** Run `npx expo prebuild --clean` and rebuild the app

### No Session Replay
**Cause:** Session replay requires native modules to be rebuilt  
**Fix:** Clean rebuild with `npx expo prebuild --clean`

### Events Not Appearing
**Cause:** PostHog API key not set or app not rebuilt  
**Fix:** 
1. Verify `EXPO_PUBLIC_POSTHOG_KEY` is set in environment
2. Rebuild the app
3. Wait 1-2 minutes (there can be a delay)

### Privacy Concerns
**Cause:** Default settings mask all inputs and images  
**Fix:** Adjust `maskAllTextInputs` and `maskAllImages` in `lib/posthog.ts` if you need to see more data (consider privacy implications)

## Automatic Screen Tracking

The `ScreenTracker` component in `app/_layout.tsx` automatically tracks all screen views using Expo Router's navigation hooks. No manual tracking needed for navigation.

## When to Use PostHog

- **Product Analytics** - Understand user behavior and feature usage
- **Debugging** - Watch session replays to see exactly what users experienced
- **Feature Flags** - A/B testing and gradual rollouts (requires additional setup)
- **User Feedback** - Combine with support tickets to see what happened
- **Conversion Funnels** - Track user journeys through your app

## Performance Impact

- Minimal CPU overhead (snapshots are throttled)
- Network usage: ~100-500KB per minute
- Battery impact: Negligible
- Storage: Data is sent to PostHog, not stored locally

## Best Practices

1. **Always mask sensitive data** - Keep `maskAllTextInputs: true` for production
2. **Track meaningful events** - Don't over-track; focus on key user actions
3. **Identify users after login** - Enables user-specific analysis
4. **Reset on logout** - Prevents data leakage between users
5. **Use properties** - Add context to events for better analysis
6. **Test in development** - Verify events appear before deploying

## Reference

- PostHog React Native Docs: https://posthog.com/docs/libraries/react-native
- Session Replay Docs: https://posthog.com/docs/session-replay/mobile
