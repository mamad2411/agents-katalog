---
name: push-notifications
description: Set up push notifications for iOS and Android using Expo Notifications and Supabase Edge Functions. Use when adding push notifications, configuring APNs/FCM credentials, sending notifications from the backend, or troubleshooting notification delivery.
---

# Push Notifications

## Stack

- **expo-notifications** — handles token registration, foreground/background receipt on device
- **Expo Push Notification Service (EPN)** — proxies to APNs (Apple) and FCM (Google); free, no quota
- **Supabase Edge Function** — sends notifications server-side via Expo Push API
- **APNs key** — required for iOS production builds (configured in Expo dashboard)
- **FCM key** — required for Android (configured in Expo dashboard)

You do NOT call APNs or FCM directly. Expo's push service handles the routing.

---

## Step 1: Install

```bash
cd mobile
npx expo install expo-notifications expo-device expo-constants
```

Add to `app.json`:
```json
{
  "expo": {
    "plugins": [
      [
        "expo-notifications",
        {
          "icon": "./assets/notification-icon.png",
          "color": "#ffffff",
          "sounds": ["./assets/notification-sound.wav"]
        }
      ]
    ]
  }
}
```

---

## Step 2: Register for Push Token

Add to your app initialization (e.g. `app/_layout.tsx`):

```typescript
import * as Notifications from "expo-notifications";
import * as Device from "expo-device";
import Constants from "expo-constants";

// Handle notifications when app is in foreground
Notifications.setNotificationHandler({
  handleNotification: async () => ({
    shouldShowAlert: true,
    shouldPlaySound: true,
    shouldSetBadge: false,
  }),
});

export async function registerForPushNotifications(): Promise<string | null> {
  if (!Device.isDevice) {
    console.warn("Push notifications require a physical device");
    return null;
  }

  const { status: existingStatus } = await Notifications.getPermissionsAsync();
  let finalStatus = existingStatus;

  if (existingStatus !== "granted") {
    const { status } = await Notifications.requestPermissionsAsync();
    finalStatus = status;
  }

  if (finalStatus !== "granted") {
    return null;
  }

  const projectId = Constants.expoConfig?.extra?.eas?.projectId;
  const token = (await Notifications.getExpoPushTokenAsync({ projectId })).data;

  return token;   // looks like: ExponentPushToken[xxxxx]
}
```

`projectId` comes from `eas.json` or `app.json` → `expo.extra.eas.projectId`. Find it in [expo.dev](https://expo.dev) under your project settings.

---

## Step 3: Store Token in Supabase

After registration, save the token to your database:

```typescript
// lib/notifications.ts
import { supabase } from "./supabase";
import { registerForPushNotifications } from "./pushNotifications";

export async function syncPushToken(userId: string) {
  const token = await registerForPushNotifications();
  if (!token) return;

  await supabase.from("push_tokens").upsert(
    { user_id: userId, token, platform: Platform.OS },
    { onConflict: "token" }
  );
}
```

Database schema:
```sql
create table push_tokens (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references auth.users not null,
  token text unique not null,
  platform text not null,  -- ios | android
  created_at timestamptz default now()
);

alter table push_tokens enable row level security;
create policy "users manage own tokens" on push_tokens
  using (auth.uid() = user_id)
  with check (auth.uid() = user_id);
```

Call `syncPushToken` after login:
```typescript
supabase.auth.onAuthStateChange((event, session) => {
  if (event === "SIGNED_IN" && session?.user) {
    syncPushToken(session.user.id);
  }
});
```

---

## Step 4: Send Notifications from Edge Function

```typescript
// supabase/functions/send-notification/index.ts
import { createClient } from "npm:@supabase/supabase-js@2";

const EXPO_PUSH_URL = "https://exp.host/--/api/v2/push/send";

interface PushMessage {
  to: string;
  title: string;
  body: string;
  data?: Record<string, unknown>;
  sound?: "default" | null;
  badge?: number;
}

export async function sendPushNotification(
  userIds: string[],
  notification: Omit<PushMessage, "to">
) {
  const supabase = createClient(
    Deno.env.get("PUBLIC_SUPABASE_URL")!,
    Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!
  );

  const { data: tokens } = await supabase
    .from("push_tokens")
    .select("token")
    .in("user_id", userIds);

  if (!tokens?.length) return;

  const messages: PushMessage[] = tokens.map(({ token }) => ({
    to: token,
    sound: "default",
    ...notification,
  }));

  // Expo accepts up to 100 messages per request
  const chunks = chunk(messages, 100);
  for (const batch of chunks) {
    await fetch(EXPO_PUSH_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(batch),
    });
  }
}

function chunk<T>(arr: T[], size: number): T[][] {
  return Array.from({ length: Math.ceil(arr.length / size) }, (_, i) =>
    arr.slice(i * size, i * size + size)
  );
}
```

---

## Step 5: Configure APNs Key (iOS Production)

Required for iOS push notifications in production builds.

1. [developer.apple.com/account/resources/authkeys](https://developer.apple.com/account/resources/authkeys) → **+**
2. Name: `Expo Push`, enable **Apple Push Notifications service (APNs)**
3. Download the `.p8` file — **download once only**
4. Note the **Key ID** and your **Team ID** (top right of developer.apple.com)

Upload to Expo:
1. [expo.dev](https://expo.dev) → Your project → **Credentials** → **iOS**
2. **Push Notifications** → Upload the `.p8` key, enter Key ID and Team ID

Or via CLI:
```bash
eas credentials --platform ios
# Select: Push Notifications → Upload APNs key
```

---

## Step 6: Configure FCM (Android Production)

1. Go to [console.firebase.google.com](https://console.firebase.google.com)
2. Create project (or use existing) → **Add app** → Android
3. Enter your package name (`com.yourorg.appname`)
4. Download `google-services.json` → place in `mobile/google-services.json`
5. **Project settings** → **Cloud Messaging** → copy **Server key**

Add to `app.json`:
```json
{
  "expo": {
    "android": {
      "googleServicesFile": "./google-services.json"
    }
  }
}
```

Upload FCM key to Expo:
```bash
eas credentials --platform android
# Select: Push Notifications → Upload FCM key
```

---

## Handle Notification Taps

```typescript
import { useEffect, useRef } from "react";
import * as Notifications from "expo-notifications";
import { router } from "expo-router";

export function useNotificationNavigation() {
  const responseListener = useRef<Notifications.Subscription>();

  useEffect(() => {
    // App opened from notification
    responseListener.current = Notifications.addNotificationResponseReceivedListener(
      (response) => {
        const data = response.notification.request.content.data;
        if (data?.screen) {
          router.push(data.screen as string);
        }
      }
    );

    return () => {
      responseListener.current?.remove();
    };
  }, []);
}
```

Pass `data: { screen: "/orders/123" }` when sending to deep-link on tap.

---

## Testing

```bash
# Test with Expo CLI (dev build or Expo Go)
npx expo push:send --to "ExponentPushToken[xxx]" --title "Test" --body "Hello"

# Or use the Expo push tool
open https://expo.dev/notifications
```

Physical device required for testing — simulator/emulator does not receive push notifications.

---

## Gotchas

**Notifications work in Expo Go but not in production build** — APNs key not uploaded to Expo. Run `eas credentials --platform ios` and verify Push Notifications key is configured.

**Android notifications not delivered** — `google-services.json` missing or wrong package name. Verify `package` in `app.json` matches Firebase project.

**Token is null on simulator** — Expected. Push tokens only work on physical devices. Check with `Device.isDevice`.

**"DeviceNotRegistered" error** — Token is stale (user uninstalled/reinstalled app). Delete the token from `push_tokens` table when this error is returned by Expo Push API.

**Notification not shown when app is in foreground** — Set `shouldShowAlert: true` in `setNotificationHandler`. By default foreground notifications are silent.

**iOS notification permission denied** — You can only ask for permission once. If denied, user must go to Settings manually. Always explain why before requesting.

**Badge count not clearing** — Call `Notifications.setBadgeCountAsync(0)` on app foreground:
```typescript
AppState.addEventListener("change", (state) => {
  if (state === "active") Notifications.setBadgeCountAsync(0);
});
```
